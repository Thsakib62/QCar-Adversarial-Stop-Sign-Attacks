# Reproducibility Guide

## Scope

Offline users can regenerate Tables 2, 5, and 7 summaries, rebuild dataset manifests, verify all checksums, inspect the reported checkpoint, and rerun the range-separated detector evaluation. Physical closed-loop claims require the Quanser testbed described in `HARDWARE.md`.

## Prerequisites

- Analysis: Python 3.10 or newer, NumPy, pandas, SciPy
- YOLO tasks: a clone of Ultralytics YOLOv5 v6.1 at commit `3752807c0b8af03d42de478fbcbf338ec4546a6c`
- QCar runtime: the exact Jetson/Quanser stack in `SOFTWARE_ENVIRONMENT.md`
- TensorRT export: perform export on the target-compatible Jetson/TensorRT stack

Pin YOLOv5:

```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
git checkout 3752807c0b8af03d42de478fbcbf338ec4546a6c
```

## Statistical Results

```bash
python scripts/reproduce_statistics.py
```

Inputs remain unchanged under `data/baseline/`, `data/pre_mitigation/`, `data/post_mitigation/`, and `data/additional_patterns/`. Outputs are written to `results/statistics/`. The script uses valid numeric values only, sample SD (`ddof=1`), 10,000 bootstrap resamples with seed 42, two-sided Mann–Whitney U tests, and two-sided Fisher exact tests.

## Dataset Manifests

```bash
python scripts/build_dataset_manifests.py
python src/evaluation/summarize_stop_sign_semantics.py
```

These commands validate YOLO labels, pair images and labels, compute per-file SHA-256 values, and regenerate clean/attacked stop-sign summaries from the filename rule.

## Held-Out Evaluation

```bash
python scripts/reproduce_heldout_eval.py --yolov5-root /path/to/yolov5 --img 640 --batch-size 16 --device 0 --workers 4
```

The wrapper supplies repository-relative data as an in-memory YOLO configuration, avoiding machine-specific paths. The reference evaluation used confidence threshold 0.001 and NMS IoU threshold 0.6, as implemented in `src/evaluation/evaluate_heldout.py`.

## Training Reproduction

```bash
python scripts/reproduce_training.py --yolov5-root /path/to/yolov5 --device 0
```

This launches 100 epochs at 640 pixels, batch size 8, SGD, and `--freeze 10`. It writes a new run under `results/training_reproduction/` and does not overwrite archived outputs. Stochastic training and environment differences may prevent bitwise-identical weights.

## TensorRT Export

On the Jetson TX2 stack:

```bash
python scripts/export_tensorrt.py mitigation --yolov5-root /path/to/yolov5 --device 0 --force
python scripts/export_tensorrt.py baseline --yolov5-root /path/to/yolov5 --device 0 --force
```

The `.pt` checkpoint is the canonical portable model. TensorRT engines may be incompatible across TensorRT, CUDA, JetPack, GPU architecture, or export settings.

## QCar Launch

Only run these commands on a secured testbed with an emergency-stop procedure and the vehicle wheels initially clear of the ground:

```bash
python scripts/run_qcar_runtime.py baseline-pytorch --yolov5-root /path/to/yolov5
python scripts/run_qcar_runtime.py baseline-tensorrt --yolov5-root /path/to/yolov5
python scripts/run_qcar_runtime.py mitigation-pytorch --yolov5-root /path/to/yolov5
python scripts/run_qcar_runtime.py mitigation-tensorrt --yolov5-root /path/to/yolov5
```

The release copies replace only machine-specific model/data paths with environment-driven paths. Experimental control constants remain unchanged.

## Integrity

```bash
python scripts/verify_artifact.py
```

Any failure indicates a missing or modified release file. Rebuild checksums only after an intentional, reviewed change.
