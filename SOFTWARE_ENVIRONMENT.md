# Software Environment

## Onboard QCar Deployment Environment

The following environment is reported for the onboard Quanser QCar deployment.

| Layer | Component | Version or configuration |
| --- | --- | --- |
| Hardware | Compute platform | NVIDIA Jetson TX2 |
| Hardware | Architecture | `aarch64` |
| Operating system | Ubuntu | 18.04.6 LTS |
| NVIDIA platform | JetPack | 4.4.1 |
| Runtime | Python | 3.6.9 |
| ML framework | PyTorch | 1.10.0 |
| ML framework | torchvision | 0.11.1 |
| GPU runtime | CUDA | 10.2.89 |
| GPU runtime | cuDNN | 8.0.0.180 |
| Inference runtime | TensorRT | 7.1.3.0 |
| Computer vision | OpenCV | 4.5.1 |
| Vehicle/sensor interface | Quanser software libraries | 2023.4.13 |
| Detector implementation | Ultralytics YOLOv5 | v6.1 |
| Detector implementation | YOLOv5 commit | `3752807c` |
| Detector architecture | Model family | YOLOv5n |

The manuscript states that trained YOLOv5n models were exported to TensorRT engine format for optimized onboard inference. Engine files are intentionally excluded from this review-stage repository.

## Training Environment Reported in the Manuscript

| Item | Manuscript-reported information |
| --- | --- |
| Training hardware | NVIDIA RTX 3060 workstation |
| Input resolution | 640 × 640 |
| YOLOv5 | v6.1, commit `3752807c` |
| Python, PyTorch, and CUDA | Reported as matching the onboard deployment versions |
| Training-workstation operating system | Not specified in the revised manuscript |

JetPack is an onboard Jetson platform component and is not attributed to the training workstation. For the reported fine-tuning run, backbone layers 0–9 were frozen and the detection head was updated.

## Later or Offline Analysis Environment

The revised manuscript does not identify a separate offline statistical-analysis software environment. Consequently, this review-stage repository does not characterize one.

A later reconstructed Windows environment was used for artifact inspection and revision support. It is not presented as the original onboard or model-training environment.
