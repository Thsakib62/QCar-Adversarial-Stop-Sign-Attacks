# Vulnerability Assessment of Adversarial Image Attacks in a Miniaturized Autonomous Vehicle Testbed without Relying on Way-Point Information

> **Review-stage repository:** This repository currently contains documentation only. It is not the complete reproducibility artifact for the study.

## Associated Manuscript

This repository accompanies an IEEE Access manuscript under review by Tahmid Hasan Sakib, Abhijeet Solanki, Wesam Al Amiri, Syed Rafay Hasan, Syed Ali Asad Rizvi, and Terry N Guo.

The study examines physically realized adversarial stop-sign patterns in a miniature autonomous-vehicle testbed. The documented framework combines camera-based YOLOv5n detection, 2D LiDAR ranging, onboard sensor fusion, and closed-loop vehicle control without requiring a preloaded map or stop-sign way-points during runtime.

## Hardware Platform

- Quanser QCar miniature autonomous-vehicle platform
- NVIDIA Jetson TX2 onboard computer (`aarch64`)
- Front-facing CSI RGB camera
- RPLiDAR A2 2D LiDAR
- Onboard perception, fusion, and vehicle control

## Perception and Experiment Organization

The manuscript describes a multithreaded architecture with camera, LiDAR, and control activities. Experiments are organized into a clean-sign baseline, evaluation with physically printed adversarial stop signs, and a mitigation phase using a YOLOv5n detector fine-tuned on an adversarially augmented in-domain dataset. During training, backbone layers 0–9 were frozen and the detection head was updated. The same sensing, fusion, stopping threshold, and control structure are maintained across these phases.

## Onboard Software Summary

| Component | Version |
| --- | --- |
| Operating system | Ubuntu 18.04.6 LTS |
| NVIDIA JetPack | 4.4.1 |
| Python | 3.6.9 |
| PyTorch | 1.10.0 |
| torchvision | 0.11.1 |
| CUDA | 10.2.89 |
| cuDNN | 8.0.0.180 |
| TensorRT | 7.1.3.0 |
| OpenCV | 4.5.1 |
| Quanser software libraries | 2023.4.13 |
| Ultralytics YOLOv5 | v6.1, commit `3752807c` |

The manuscript reports deployment of trained YOLOv5n models exported to TensorRT engine format for optimized onboard inference. No model or engine file is included in this review-stage snapshot.

## Documentation

- [Reproducibility summary](REPRODUCIBILITY.md)
- [Software environment](SOFTWARE_ENVIRONMENT.md)
- [Artifact availability](ARTIFACT_AVAILABILITY.md)
- [Pre-upload verification items](PREUPLOAD_CHECKLIST.md)
- [Review-stage release manifest](RELEASE_MANIFEST.txt)

## Artifact Availability

This repository currently provides software-environment and reproducibility documentation associated with the manuscript under review. The complete experimental source code, trained model weights, dataset and annotations, statistical analysis artifacts, and execution instructions will be released through this repository upon acceptance of the manuscript.

## Citation

Basic citation metadata is provided in [`CITATION.cff`](CITATION.cff). Final publication metadata, including a verified DOI, will be added after it becomes available.
