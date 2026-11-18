# Manuscript Result Mapping

| Manuscript item | Raw source | Analysis or configuration | Generated/reference output | Model |
|---|---|---|---|---|
| Table 2 clean baseline statistics | `data/baseline/nonattacked_30_runs_for_stats.csv` | `src/statistics/analyze_qcar_statistics.py` | `results/statistics/baseline_summary.csv` | COCO YOLOv5n baseline |
| Representative baseline values | `data/baseline/nonattacked_30_runs_for_stats.csv` | direct run rows and baseline summary | `results/statistics/cleaned_long_format.csv` | COCO YOLOv5n baseline |
| Table 5 adversarial evaluation | `data/pre_mitigation/Testbed Data - Attacked.csv` and clean baseline | `scripts/reproduce_statistics.py` | `results/statistics/table5_attack_summary.csv`; `results/statistics/manuscript_ready_table5.txt` | COCO YOLOv5n baseline |
| Table 7 mitigation comparison | pre/post raw CSVs and clean baseline | `scripts/reproduce_statistics.py` | `results/statistics/table7_pre_post_summary.csv`; `results/statistics/statistical_tests.csv`; `results/statistics/manuscript_ready_table7.txt` | baseline and `qcar_aug_exp1v2_best.pt` |
| Seven additional designs | `data/additional_patterns/7_Mitigations.csv` | `scripts/reproduce_statistics.py` | `results/statistics/seven_design_post_mitigation_summary.csv` | `qcar_aug_exp1v2_best.pt` |
| Figure 9 training/model-selection curve | archived run `results.csv` | `configs/training/opt.yaml`; `configs/training/hyp.yaml` | `results/mitigation/training_results.csv`; `results/mitigation/results.png` | `qcar_aug_exp1v2_best.pt` |
| Original validation metrics | archived run `results.csv` | YOLOv5 validation during training | training curves and CSV | `qcar_aug_exp1v2_best.pt` |
| Range-separated held-out detector test | `data/heldout_test/images/`, labels, and manifest | `scripts/reproduce_heldout_eval.py` | `results/heldout_evaluation/heldout_test_metrics.csv`; `per_class_metrics.csv`; validation folder | `qcar_aug_exp1v2_best.pt` |
| QCar baseline runtime | QCar runtime source | `scripts/run_qcar_runtime.py baseline-*` | physical testbed logs summarized in baseline CSV | `yolov5n_coco_baseline.pt/.engine` |
| QCar mitigation runtime | QCar runtime source | `scripts/run_qcar_runtime.py mitigation-*` | physical post-mitigation CSVs | `qcar_aug_exp1v2_best.pt/.engine` |

The original validation curve is training/model-selection evidence because neighboring frames occur across train and validation. It is not mapped as independent generalization evidence.
