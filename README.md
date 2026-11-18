# QCar Physical Adversarial Stop-Sign Evaluation

This repository is the post-acceptance reproducibility package for **“Vulnerability Assessment of Adversarial Image Attacks in a Miniaturized Autonomous Vehicle Testbed without Relying on Way-Point Information.”** It documents and packages the Quanser QCar runtime, YOLOv5n models, camera–LiDAR fusion experiment records, adversarial-learning mitigation, statistical analysis, and range-separated detector evaluation.

## System Overview

- **Vehicle:** Quanser QCar with NVIDIA Jetson TX2 (`aarch64`)
- **Perception:** front CSI RGB camera and Ultralytics YOLOv5n
- **Ranging:** RPLiDAR A2 fused with accepted camera detections
- **Control:** approximately 20 Hz; detector 8–10 FPS; LiDAR 12–15 Hz
- **Stopping rule:** valid final stop at or below 0.8 m
- **Deployment:** PyTorch checkpoints and target-specific TensorRT engines
- **YOLOv5:** v6.1, commit `3752807c0b8af03d42de478fbcbf338ec4546a6c`

## Quick Start

Create a Python analysis environment with NumPy, pandas, and SciPy, then run:

```bash
python scripts/reproduce_statistics.py
python scripts/build_dataset_manifests.py
python scripts/verify_artifact.py
```

For detector evaluation, obtain a YOLOv5 v6.1 checkout at the pinned commit and run:

```bash
python scripts/reproduce_heldout_eval.py --yolov5-root /path/to/yolov5 --img 640 --batch-size 16 --device 0
```

Training, TensorRT export, and QCar launch commands are in [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md). QCar execution requires the Quanser hardware and onboard software stack.

## Repository Map

- `docs/` — protocol, provenance, manuscript mapping, and audit
- `environment/` — onboard, training, and offline environment records
- `src/` — QCar runtime, evaluation, and statistical source
- `configs/` — runtime, training, and dataset configuration
- `data/` — raw experiment tables and annotated image splits
- `models/` — baseline and fine-tuned PyTorch/TensorRT models
- `results/` — reference statistical, training, and held-out outputs
- `scripts/` — reproduction and integrity wrappers
- `manifests/` — file inventory and SHA-256 checksums

## Important Provenance

The checkpoint-linked historical training corpus reconstructed from run-adjacent cache evidence contains 306 images and 964 annotations. A later combined folder contains 347 images and 1,082 annotations. The manuscript snapshot available during packaging states 350 images and 1,092 annotations. This unresolved conflict and other required manuscript corrections are documented in [docs/ARTIFACT_AUDIT.md](docs/ARTIFACT_AUDIT.md); no raw artifact was altered to force agreement.

The detector test uses frames 0306–0346, which are disjoint from the reconstructed 0000–0305 training/model-selection pool. It is a **range-separated held-out evaluation**, not proof of cross-session or cross-site generalization.

## Limitations

Camera–LiDAR control behavior, real-time throughput, and physical stopping outcomes require a Quanser QCar, Jetson TX2, CSI camera, and RPLiDAR A2. Statistical tables and dataset integrity checks can be reproduced offline. TensorRT engine binaries are tied to the target software/hardware stack; the `.pt` checkpoint plus export procedure is the portable route.

## Citation and Rights

Citation metadata is provided in `CITATION.cff`. No project-wide reuse license has been selected. Dataset, model, third-party dependency, privacy, and redistribution approvals must be completed before public release; see `PRE_RELEASE_CHECKLIST.md`.
