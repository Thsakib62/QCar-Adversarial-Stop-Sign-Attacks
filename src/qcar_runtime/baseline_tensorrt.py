import time
import os
import numpy as np
import cv2
import torch
import matplotlib.pyplot as plt
from threading import Thread
from models.common import DetectMultiBackend
from utils.general import check_img_size, non_max_suppression
from utils.plots import Annotator, colors
from utils.torch_utils import select_device
from pal.products.qcar import QCar, QCarCameras
from pal.utilities.lidar import Lidar

import matplotlib
matplotlib.use('TkAgg')  # For testing, try `Qt5Agg` if available

# Initialize QCar
myCar = QCar()

# Initialize YOLOv5 Model
# Original PyTorch model loading:
# device = select_device('0' if torch.cuda.is_available() else 'cpu')
# model = DetectMultiBackend(weights='yolov5n.pt', device=device)
# stride, names, pt = model.stride, model.names, model.pt
device = select_device('0')
ENGINE_PATH = os.environ.get("QCAR_WEIGHTS", "models/tensorrt/yolov5n_coco_baseline.engine")
DATA_YAML = os.environ.get("QCAR_DATA_YAML", "configs/dataset/coco.yaml")
STOP_SIGN_LABELS = ('stop sign', 'stop_sign')
STOP_SIGN_CONTROL_LABEL = 'stop sign'
model = DetectMultiBackend(weights=ENGINE_PATH, device=device, data=DATA_YAML)
stride, names, pt = model.stride, model.names, model.pt
img_size = check_img_size(640, s=stride)
engine_input = model.bindings['images']
use_fp16 = engine_input.dtype == np.float16
print("TensorRT input shape:", engine_input.shape)
print("TensorRT input dtype:", engine_input.dtype)
print("Class names:", names)
engine_class_count = model.bindings['output'].shape[-1] - 5
assert len(names) == engine_class_count, "DATA_YAML class count {} does not match engine class count {}".format(
    len(names), engine_class_count)
assert tuple(engine_input.shape) == (1, 3, 640, 640)
model.warmup(imgsz=engine_input.shape, half=use_fp16)

# Initialize Cameras
cameras = QCarCameras(enableFront=True)

# Initialize LIDAR
numMeasurements = 360
lidarMeasurementMode = 2
lidarInterpolationMode = 0
MAX_DISTANCE = 3.0  # meters
MIN_ANGLE = np.deg2rad(28) # 50 degrees in radians
MAX_ANGLE = np.deg2rad(143) # 130 degrees in radians
myLidar = Lidar(type='RPLidar', numMeasurements=numMeasurements, rangingDistanceMode=lidarMeasurementMode, interpolationMode=lidarInterpolationMode)

# Initialize Car Parameters
base_speed = 0.065 # battery1 = 0.06, battery2 = 0.07
stop_speed = 0.0
turn_steering = 0.5
LEDs = np.array([0, 0, 0, 0, 0, 0, 1, 1])  # Default LEDs (rear lights on)

# Global variables to share data between threads
detected_object = None
object_distance = None
object_detected = False
object_position = None  # Store the position of the detected object (left, center, right)
terminate_threads = False
fps = 0  # For FPS calculation
BENCHMARK_EVERY_N_FRAMES = 30

# Added global variables
stop_sign_count = 0
exit_after_stop = False
in_cooldown = False
ignore_detections = False
aligning_with_stop_sign = False

# Initialize Matplotlib for LiDAR Plot
ax = plt.subplot(111, projection='polar')
plt.ion()  # Turn on interactive mode
plt.show()

def get_object_position(bbox, frame_width):
    """Classify object position as left, center, or right based on bounding box location."""
    x_center = (bbox[0] + bbox[2]) / 2  # Calculate the x-center of the bounding box
    # if x_center < frame_width / 3:
    #     return 'left'
    # elif x_center > 2 * frame_width / 3:
    #     return 'right'
    # else:
    #     return 'center'
    if x_center < frame_width / 5 * 2:
        return 'left'
    elif x_center > frame_width / 5 * 3:
        return 'right'
    else:
        return 'center'


def lidar_distance_for_position(position):
    """Get the minimum LiDAR distance for a given position (left, center, right)."""
    global object_distance

    # Define angle ranges for each position
    if position == 'left':
        angle_range = (MIN_ANGLE, np.deg2rad(75))  # Angles less than 90 degrees
    elif position == 'center':
        angle_range = (np.deg2rad(75), np.deg2rad(95))  # Angles near 90 degrees
    elif position == 'right':
        angle_range = (np.deg2rad(95), MAX_ANGLE)  # Angles greater than 90 degrees
    else:
        return None

    # Filter distances within the angle range
    angles = myLidar.angles.flatten()
    distances = myLidar.distances.flatten()
    within_range = (angles >= angle_range[0]) & (angles <= angle_range[1]) & (distances > 0)
    filtered_distances = distances[within_range]

    if len(filtered_distances) > 0:
        return np.min(filtered_distances)  # Return the closest distance in this range
    else:
        return None

def lidar_update():
    global object_distance, object_detected

    while not terminate_threads:
        myLidar.read()
        distances = myLidar.distances.flatten()
        angles = myLidar.angles.flatten()

        # Filter angles and distances within the relevant FOV and distance
        angles = np.mod(angles, 2 * np.pi)
        within_fov = (angles >= MIN_ANGLE) & (angles <= MAX_ANGLE)
        within_distance = (distances > 0) & (distances <= MAX_DISTANCE)

        valid_points = within_fov & within_distance
        filtered_distances = distances[valid_points]
        filtered_angles = angles[valid_points]

        # Update polar scatter plot
        ax.cla()  # Clear previous points
        ax.scatter(filtered_angles, filtered_distances, marker='.')
        ax.set_theta_zero_location("W")
        ax.set_theta_direction(-1)
        plt.pause(0.1)

        time.sleep(0.1)

def camera_thread():
    global detected_object, object_detected, object_distance, object_position, fps, ignore_detections

    frame_count = 0
    with cameras:
        while not terminate_threads:
            start_time = time.time()
            cameras.readAll()
            frame = cameras.csiFront.imageData
            frame_width = frame.shape[1] if frame is not None else 0

            if frame is not None:
                preprocess_start = time.perf_counter()
                frame_resized = cv2.resize(frame, (img_size, img_size))
                # Original PyTorch tensor conversion:
                # img = frame_resized.transpose(2, 0, 1)
                # img = torch.from_numpy(img).to(device).float() / 255.0
                img = np.ascontiguousarray(frame_resized.transpose(2, 0, 1))
                img = torch.from_numpy(img).to(device)
                img = img.half() if use_fp16 else img.float()
                img /= 255.0
                img = img.unsqueeze(0)
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                preprocess_ms = (time.perf_counter() - preprocess_start) * 1000.0

                # YOLOv5 Inference
                inference_start = time.perf_counter()
                pred = model(img, augment=False, visualize=False)
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                inference_ms = (time.perf_counter() - inference_start) * 1000.0

                nms_start = time.perf_counter()
                pred = non_max_suppression(pred, 0.25, 0.45)
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                nms_ms = (time.perf_counter() - nms_start) * 1000.0
                frame_count += 1

                annotator = Annotator(frame_resized, line_width=2)
                if len(pred[0]) and not ignore_detections:
                    for *xyxy, conf, cls in reversed(pred[0]):
                        label = f'{names[int(cls)]} {conf:.2f}'
                        annotator.box_label(xyxy, label, color=colors(cls, True))

                        # Filter for only "stop sign"
                        detected_label = names[int(cls)]
                        if detected_label.lower() in STOP_SIGN_LABELS:
                            # Determine the object's position based on bounding box
                            object_position = get_object_position(xyxy, frame_width)

                            # Get dynamic distance from LiDAR for the object's position
                            detected_object = STOP_SIGN_CONTROL_LABEL
                            object_detected = True
                            object_distance = lidar_distance_for_position(object_position)

                            # Print and annotate position and distance
                            if object_distance is not None:
                                print(f"{detected_object.capitalize()} detected at {object_position} with distance {object_distance:.2f} meters")

                # Resize frame for display (800x640) without padding
                display_frame = cv2.resize(frame_resized, (800, 640))

                # Display FPS
                end_time = time.time()
                fps = 1 / (end_time - start_time)
                if frame_count % BENCHMARK_EVERY_N_FRAMES == 0:
                    print("Timing | preprocess: {:.1f} ms | inference: {:.1f} ms | NMS: {:.1f} ms | displayed FPS: {:.2f}".format(
                        preprocess_ms, inference_ms, nms_ms, fps))
                cv2.putText(display_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # Display the frame with detections
                cv2.imshow('Front CSI Camera', display_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            time.sleep(0.1)

def control_car():
    global object_distance, object_detected, object_position, detected_object, stop_sign_count, exit_after_stop, terminate_threads, in_cooldown, ignore_detections, aligning_with_stop_sign

    # Timers for stop and turn behaviors
    stop_timer = None
    turn_timer = None
    cooldown_timer = None  # Cooldown to prevent immediate re-detection
    stable_detection_count = 0  # To count consecutive stable detections
    required_stable_detections = 10  # Set the number of consecutive detections needed
    aligning_with_stop_sign = True

    while not terminate_threads:
        # Reset speed and steering
        speed = base_speed
        steering = -0.093  # Right offset for straight driving
        action = "No obstacle detected - going straight"
        LED_status = LEDs.copy()

        # Get the current time
        current_time = time.time()

        # Aligning with stop sign while approaching (extend alignment until stopping distance of 0.8 meters)
        if aligning_with_stop_sign and detected_object == 'stop sign' and object_distance > 0.8:
            stable_detection_count += 1
            if stable_detection_count >= required_stable_detections:
                # Reduce speed slightly during alignment for finer adjustments
                speed = base_speed - 0.01
                if object_position == 'left':
                    steering = 0.25  # Adjust left (smaller adjustment for finer tuning)
                    action = f"Stop sign detected at {object_position} with distance {object_distance:.2f} meters - Adjusting Left"
                elif object_position == 'right':
                    steering = -0.5  # Adjust right (smaller adjustment for finer tuning)
                    action = f"Stop sign detected at {object_position} with distance {object_distance:.2f} meters - Adjusting Right"
                else:
                    steering = -0.093  # Centered, go straight
                    action = f"Stop sign detected at {object_position} with distance {object_distance:.2f} meters - No Adjustment"

        # Check for cooldown period after completing a turn
        elif in_cooldown:
            if current_time - cooldown_timer < 1:
                action = "In cooldown period after turn - ignoring stop sign detections."
                ignore_detections = True
            else:
                # End cooldown period
                in_cooldown = False
                cooldown_timer = None
                ignore_detections = False
                aligning_with_stop_sign = True
                stable_detection_count = 0  # Reset stable count before starting alignment

        # Handling stop behavior at stop signs
        elif stop_timer:
            if (stop_sign_count == 1 and current_time - stop_timer < 5) or (stop_sign_count == 2 and current_time - stop_timer < 5) or (stop_sign_count == 3 and current_time - stop_timer < 10):
                # Keep the car stopped for 5 seconds at first two stop signs, 10 seconds at third
                speed = stop_speed
                action = f"Stop sign {stop_sign_count} - stopping for {'5' if stop_sign_count < 3 else '10'} seconds"
                LED_status[4] = 1  # Rear brake lights on
                LED_status[6] = 1
            else:
                # After stopping, check if we need to turn or terminate
                if stop_sign_count in [1, 2]:
                    # Start the left turn after stopping at first or second stop sign
                    stop_timer = None
                    turn_timer = current_time
                    ignore_detections = True  # Ignore detections during turn
                    aligning_with_stop_sign = False  # Stop aligning during the turn
                    # Clear detection state
                    object_detected = False
                    object_distance = None
                    object_position = None
                    detected_object = None
                    stable_detection_count = 0  # Reset stable count after stopping
                elif stop_sign_count == 3:
                    # At third stop sign, set exit condition
                    exit_after_stop = True
                    terminate_threads = True
                    print("Experiment complete. Exiting code after 10 seconds stop.")
                    break  # Exit the loop

        # Handling turn behavior after first or second stop sign
        elif turn_timer:
            if current_time - turn_timer < 5:
                # Turn left for 5 seconds
                speed = base_speed -0.004
                steering = turn_steering
                action = "Turning left for 5 seconds"
                LED_status[0] = 1  # Left indicator on
                LED_status[2] = 1
            else:
                # Reset the turn timer and initiate cooldown
                turn_timer = None
                cooldown_timer = current_time
                in_cooldown = True

        # Check for new detections if not in the middle of stopping, turning, or cooldown
        elif not ignore_detections and object_detected and object_distance is not None:
            if aligning_with_stop_sign and detected_object == 'stop sign' and object_distance > 0.8:
                stable_detection_count += 1
                if stable_detection_count >= required_stable_detections:
                    # Fine-tuned steering adjustments for precise alignment
                    speed = base_speed - 0.008
                    if object_position == 'left':
                        steering = 0.25  # Adjust left
                        action = f"Stop sign detected at {object_position} with distance {object_distance:.2f} meters - Adjusting Left"
                    elif object_position == 'right':
                        steering = -0.5  # Adjust right
                        action = f"Stop sign detected at {object_position} with distance {object_distance:.2f} meters - Adjusting Right"
                    else:
                        steering = -0.093  # Centered, go straight
                        action = f"Stop sign detected at {object_position} with distance {object_distance:.2f} meters - No Adjustment"

            elif detected_object == 'stop sign' and object_distance <= 0.8:
                # Stop the car when within 0.8 meters of the stop sign
                stop_sign_count += 1
                stop_timer = current_time
                speed = stop_speed
                action = f"Stop sign {stop_sign_count} detected at {object_position} with distance {object_distance:.2f} meters - stopping the car"
                LED_status[4] = 1  # Rear brake lights on
                LED_status[6] = 1
                stable_detection_count = 0  # Reset after stopping

        # Collision avoidance: Stop if any object is closer than 0.4 meters
        if detected_object != 'stop sign' and object_distance is not None and object_distance < 0.5:
            speed = stop_speed
            action = f"Obstacle detected with distance {object_distance:.2f} meters - stopping the car"
            LED_status[4] = 1  # Rear brake lights on
            LED_status[6] = 1

        print(action)  # Print the action message

        # Send commands to the car
        myCar.read_write_std(throttle=speed, steering=steering, LEDs=LED_status)
        time.sleep(0.05)  # Adjusted loop frequency for smoother control

# Start the threads for camera and control
camera_thread_instance = Thread(target=camera_thread)
control_thread_instance = Thread(target=control_car)
camera_thread_instance.start()
control_thread_instance.start()

try:
    # Run LiDAR plotting in the main thread to keep it responsive and active
    lidar_update()
except KeyboardInterrupt:
    # Set terminate flag to stop threads on manual interruption
    terminate_threads = True
finally:
    # Ensure all threads are joined and resources are properly cleaned up
    camera_thread_instance.join()
    control_thread_instance.join()
    myLidar.terminate()
    myCar.terminate()
    cv2.destroyAllWindows()
    plt.close()
