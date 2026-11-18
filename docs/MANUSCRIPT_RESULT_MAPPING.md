# Manuscript Result Mapping

| Manuscript item | Evidence in this repository | Interpretation |
|---|---|---|
| Table 2 clean baseline | `data/baseline/nonattacked_30_runs_for_stats.csv`; `results/statistics/baseline_summary.csv` | Thirty clean vehicle runs; baseline alignment counts only. |
| Table 5 primary attacks | `data/pre_mitigation/Testbed Data - Attacked.csv`; `results/statistics/table5_attack_summary.csv` | Six runs per Lu2, Yang, and Lu3 design; missing numeric values are not zero. |
| Tables 7 and 8 mitigation | `data/pre_mitigation/`; `data/post_mitigation/`; `results/statistics/run_level_outcomes.csv` | Independent pre/post vehicle runs; Table 8 is the primary run-level binary comparison (8/18 vs 0/18). |
| Seven further patterns | `data/additional_patterns/7_Mitigations.csv` | Six post-mitigation runs per pattern, without matched pre-mitigation controls. |
| Training configuration | `configs/training/opt.yaml`; `configs/training/hyp.yaml`; `data/physical_training/`; `results/physical_training/results.csv` | Checkpoint-linked split and model-selection validation, not independent generalization. |
| Figure 9 | Training curves in `results/physical_training/` and `results/mitigation/` | Exact provenance of the curve printed in the PDF remains unverified. |
| Table 6(b) auxiliary held-out evaluation | `data/heldout_test/`; `results/heldout_evaluation/`; `models/pytorch/qcar_aug_exp1v2_best.pt` | Different checkpoint from the one associated with physical mitigation; 41 images, 118 annotations, 54 attacked stop-sign boxes. |
| Baseline runtime | `src/qcar_runtime/baseline_pytorch.py`; `src/qcar_runtime/baseline_tensorrt.py` | Baseline detector; confidence 0.25, throttle command 0.065. |
| Mitigation runtime | `src/qcar_runtime/mitigation_pytorch.py`; `src/qcar_runtime/mitigation_tensorrt.py`; `models/pytorch/qcar_physical_mitigation_best.pt` | Reproducibility entry points use the physical-training checkpoint; confidence 0.50, throttle command 0.075. Historical run-to-engine hash linkage is not proven. |
| Demonstration video | `media/ACCESS_DEMO.mp4`; `media/README.md` | Edited illustrative clip, not a run-level statistical input. |

See `docs/ARTIFACT_AUDIT.md` for the unresolved manuscript dataset count and attack-design provenance.
