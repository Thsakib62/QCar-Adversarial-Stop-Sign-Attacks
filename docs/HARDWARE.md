# Hardware

## Vehicle and Compute

- Quanser QCar miniaturized autonomous-vehicle testbed
- NVIDIA Jetson TX2 onboard computer, `aarch64`
- Front-facing CSI RGB camera
- RPLiDAR A2 two-dimensional LiDAR

## Runtime Rates

- Camera sensor: 30 frames/s
- Effective control loop: approximately 20 Hz
- YOLOv5n inference: approximately 8–10 frames/s, depending on model complexity
- LiDAR update: approximately 12–15 Hz

## Fusion and Stopping

The runtime associates accepted camera detections with a LiDAR angular sector and uses the fused range in the navigation state machine. The calibrated valid-stop threshold is 0.8 m and is held constant across baseline, attack, and mitigation conditions. The manuscript also records an age threshold of 150 ms and a camera–LiDAR synchronization threshold of 80 ms.

## Hardware-Dependent Claims

Real-time rates, sensor synchronization, steering behavior, route completion, and final stopping distance require equivalent QCar hardware and a controlled physical setup. Offline replay can inspect software logic but cannot independently reproduce electromechanical or environmental behavior.
