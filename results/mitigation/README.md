# Mitigation Results

This directory preserves the YOLOv5 training curves and archived `results.csv` associated with `qcar_aug_exp1v2`. Statistical post-mitigation results are under `results/statistics/`.

The selected `best.pt` occurred at epoch 95 under YOLOv5 fitness. The original model-selection validation metrics were precision 96.20%, recall 93.61%, mAP@0.5 95.56%, and mAP@0.5:0.95 66.53%. Because neighboring frames occur across train and validation, these values describe model selection rather than independent held-out generalization.
