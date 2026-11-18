# Mitigation Results

This directory preserves training curves and an archived `results.csv` associated with the auxiliary offline checkpoint. The physical-training run is separately preserved under `results/physical_training/`; statistical post-mitigation results are under `results/statistics/`. The exact source of Figure 9 as printed in the manuscript has not been verified.

The selected `best.pt` occurred at epoch 95 under YOLOv5 fitness. The original model-selection validation metrics were precision 96.20%, recall 93.61%, mAP@0.5 95.56%, and mAP@0.5:0.95 66.53%. Because neighboring frames occur across train and validation, these values describe model selection rather than independent held-out generalization.
