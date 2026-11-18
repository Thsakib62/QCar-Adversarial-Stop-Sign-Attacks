# TensorRT Export

Use `scripts/export_tensorrt.py` with the pinned YOLOv5 checkout. Export on a target-compatible Jetson TX2 environment with JetPack 4.4.1 and TensorRT 7.1.3.0. Engine binaries are not generally portable across TensorRT/CUDA/GPU combinations.

No original terminal command history proving the exact historical export invocation was found. The wrapper implements the YOLOv5 v6.1 `export.py --include engine --imgsz 640 640 --device 0` route supported by the archived repository and records this limitation.
