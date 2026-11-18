# Model Artifacts

| File | Purpose | Portability |
|---|---|---|
| `pytorch/yolov5n_coco_baseline.pt` | baseline/attack detector | portable YOLOv5n checkpoint |
| `pytorch/qcar_aug_exp1v2_best.pt` | manuscript mitigation checkpoint selected by YOLOv5 fitness | canonical portable mitigation artifact |
| `tensorrt/yolov5n_coco_baseline.engine` | baseline QCar deployment | Jetson/TensorRT stack dependent |
| `tensorrt/qcar_aug_exp1v2_best.engine` | mitigation QCar deployment | Jetson/TensorRT stack dependent |

The selected mitigation checkpoint is the `best.pt` from `qcar_aug_exp1v2`; its SHA-256 begins `4fc9aa50`. A different stray `best.pt` was excluded. Verify complete hashes with `python scripts/verify_artifact.py`.

TensorRT engines are retained as deployment provenance, not as the canonical portable models. Re-export the `.pt` checkpoint on the target stack when compatibility differs.
