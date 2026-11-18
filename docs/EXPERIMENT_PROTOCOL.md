# Experiment Protocol

## Organization

1. **Clean baseline:** 30 complete runs with unmodified signs.
2. **Pre-mitigation attack:** six independent runs each for Lu2, Yang, and Lu3.
3. **Post-mitigation matched designs:** six independent runs each for Lu2, Yang, and Lu3 using the fine-tuned detector.
4. **Additional post-mitigation designs:** six runs each for Lu1, Eykholt1, Eykholt2, Eykholt3, Chen1, Chen2, and Chen3.

The three stop locations are sequential. If a run terminates after an earlier miss, a later unmet route requirement is not a separately observed stop attempt. The same 0.8 m trigger threshold is used throughout.

## Outcome Definitions

- **Distance at first detection:** first accepted numeric camera/fusion detection distance for the target stop.
- **Final stopping distance:** recorded vehicle distance after the final stop action.
- **Missed stop outcome:** vehicle-level final-stop outcome where a valid final stopping distance is missing or exceeds 0.8 m.

Missing continuous measurements remain missing and are never replaced with zero. Manuscript-formatted tables show missed-stop outcomes only on final-stopping-distance rows; machine-readable outputs retain the stop-level counts.

## Model Conditions

- Baseline and attack trials use COCO-pretrained YOLOv5n (`yolov5n.pt` or the corresponding TensorRT engine).
- The later physical-training checkpoint is preserved as `models/pytorch/qcar_physical_mitigation_best.pt`. A compatible TensorRT re-export is included, but the original physical-run engine hash is not established by the run summaries.
- The mitigation model starts from COCO-pretrained YOLOv5n, freezes layer groups 0–9, and updates the detection head.
- Baseline/pre-mitigation confidence threshold is 0.25 and base throttle command is 0.065; post-mitigation values are 0.50 and 0.075. Both use NMS IoU 0.45. These differences prevent detector-only causal attribution.

## Independent Run-Level Outcome

The editorial manuscript's Table 8 reports at least one missed required stop in 8/18 pre-mitigation vehicle runs (Lu2 1/6, Yang 1/6, Lu3 6/6), compared with 0/18 post-mitigation runs. Its two-sided Fisher exact p-value is 0.0029. Stop-level outcomes in Tables 5 and 7 are nested within these runs and must not be counted as independent trials.

## Safety

Runtime scripts directly initialize QCar hardware. Execute only with trained operators, a clear test area, emergency stop, controlled lighting/sign placement, and an initial wheels-off-ground check.
