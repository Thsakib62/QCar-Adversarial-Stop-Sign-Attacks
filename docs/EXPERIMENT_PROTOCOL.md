# Experiment Protocol

## Organization

1. **Clean baseline:** 30 complete runs with unmodified signs.
2. **Pre-mitigation attack:** six independent runs each for Lu2, Yang, and Lu3.
3. **Post-mitigation matched designs:** six independent runs each for Lu2, Yang, and Lu3 using the fine-tuned detector.
4. **Additional post-mitigation designs:** six runs each for Lu1, Eykholt1, Eykholt2, Eykholt3, Chen1, Chen2, and Chen3.

All three stop locations are observed in each complete route run. The same 0.8 m valid-stop threshold is used throughout.

## Outcome Definitions

- **Distance at first detection:** first accepted numeric camera/fusion detection distance for the target stop.
- **Final stopping distance:** recorded vehicle distance after the final stop action.
- **Missed stop outcome:** vehicle-level final-stop outcome where a valid final stopping distance is missing or exceeds 0.8 m.

Missing continuous measurements remain missing and are never replaced with zero. Manuscript-formatted tables show missed-stop outcomes only on final-stopping-distance rows; machine-readable outputs retain the stop-level counts.

## Model Conditions

- Baseline and attack trials use COCO-pretrained YOLOv5n (`yolov5n.pt` or the corresponding TensorRT engine).
- Mitigation trials use `qcar_aug_exp1v2_best.pt` or the corresponding `qcar_aug_exp1v2_best.engine`.
- The mitigation model starts from COCO-pretrained YOLOv5n, freezes layer groups 0–9, and updates the detection head.

## Safety

Runtime scripts directly initialize QCar hardware. Execute only with trained operators, a clear test area, emergency stop, controlled lighting/sign placement, and an initial wheels-off-ground check.
