# Training

The complete YOLOv5 source is not vendored. Clone v6.1, check out commit `3752807c0b8af03d42de478fbcbf338ec4546a6c`, and run `scripts/reproduce_training.py`.

Archived run configuration is in `configs/training/`. The recorded `freeze: [10]` means YOLOv5 layer groups 0–9 were frozen while the detection head was updated. The archived `results.csv` and curves are in `results/mitigation/`.
