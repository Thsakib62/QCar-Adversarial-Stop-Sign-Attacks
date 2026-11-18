# Model Artifacts

| File | Purpose | Portability |
|---|---|---|
| `pytorch/yolov5n_coco_baseline.pt` | baseline/attack detector | portable YOLOv5n checkpoint |
| `pytorch/qcar_physical_mitigation_best.pt` | checkpoint associated with the later physical-mitigation training run | portable checkpoint; exact historic deployment linkage requires a run log |
| `pytorch/qcar_aug_exp1v2_best.pt` | auxiliary offline held-out evaluation checkpoint | not the physical-mitigation checkpoint |
| `tensorrt/yolov5n_coco_baseline.engine` | baseline QCar deployment | Jetson/TensorRT stack dependent |
| `tensorrt/qcar_physical_mitigation_reexport.engine` | later export of the physical-mitigation checkpoint on the QCar | not independently verified as the original physical-run engine |
| `tensorrt/qcar_aug_exp1v2_best.engine` | auxiliary checkpoint export preserved from the earlier package | Jetson/TensorRT stack dependent |

The physical-training checkpoint has SHA-256 `6cf49b8f8d0b67d412546d6e67622b090e6d7c035b29e4f0e08a2e76d13afff6`. The later TensorRT re-export has SHA-256 `6d27ab6b41983010bb14a8894cd4da161665973c4258baa1a96acd16cb82fb6d`. The auxiliary offline checkpoint has SHA-256 `4fc9aa508079dd77ab183be989f69bb7187d225ac0a64199f46833e395f1e56f`. The held-out metrics in this repository belong only to that auxiliary checkpoint. Verify complete hashes with `python scripts/verify_artifact.py`.

TensorRT engines are retained as deployment provenance, not as the canonical portable models. Re-export the `.pt` checkpoint on the target stack when compatibility differs.
