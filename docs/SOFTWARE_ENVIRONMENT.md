# Software Environments

## Onboard QCar Deployment

| Component | Version |
|---|---:|
| Architecture | aarch64 |
| Ubuntu | 18.04.6 LTS |
| JetPack | 4.4.1 |
| Python | 3.6.9 |
| PyTorch | 1.10.0 |
| torchvision | 0.11.1 |
| CUDA | 10.2.89 |
| cuDNN | 8.0.0.180 in manuscript; 8.0.0 in project summary |
| TensorRT | 7.1.3.0 |
| OpenCV | 4.5.1 |
| Quanser libraries | 2023.4.13 |
| YOLOv5 | v6.1, commit `3752807c` |

## Original Training Environment

The manuscript verifies an NVIDIA RTX 3060 workstation. Exact OS and framework package versions were not stored with the archived run, so they are not reconstructed from the later Windows environment. Training options and hyperparameters are preserved in `configs/training/`.

## Later Offline Evaluation

The held-out evaluation was run in a separate Windows environment using an NVIDIA GeForce RTX 3060, Python 3.10.8, and PyTorch 2.7.0+cu118. This environment was used only for later offline detector evaluation and provenance reconstruction.

## Dependency Boundary

The full Ultralytics and Quanser distributions are not vendored. Install Quanser packages from the vendor-supported QCar image and clone the pinned YOLOv5 revision. Verify the relevant third-party license terms before redistribution.
