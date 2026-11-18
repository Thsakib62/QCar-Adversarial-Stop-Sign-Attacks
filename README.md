# QCar Physical Adversarial Stop-Sign Evaluation

This repository accompanies **Vulnerability Assessment of Adversarial Image Attacks in a Miniaturized Autonomous Vehicle Testbed without Relying on Way-Point Information**. It preserves QCar runtime code, annotated data, model artifacts, physical-run summaries, statistical analysis, and an auxiliary detector evaluation.

## Demonstration

[Watch or download the 70-second QCar demonstration](media/ACCESS_DEMO.mp4). The video presents a clean-sign baseline, a Lu3 attacked-sign run with a collision indicated in the recording, and a Lu3 mitigation run. Camera, LiDAR, terminal, and external-camera views are shown. This is an **illustrative sequence**, not a substitute for the run-level outcomes in Tables 5, 7, and 8; the video alone does not establish rates, model identity, or causal attribution. See [video notes](media/README.md).

## System and Experiment

- Quanser QCar with Jetson TX2, front CSI camera, RPLiDAR A2, and YOLOv5n v6.1 (`3752807c`).
- Thirty clean baseline runs; six pre- and six post-mitigation runs each for Lu2, Yang, and Lu3; six post-mitigation runs each for seven further designs.
- Pre/post detector confidence thresholds: **0.25/0.50**. Base throttle commands: **0.065/0.075**. Both use NMS IoU 0.45 and a 0.8 m stop threshold. Throttle commands are not measured speeds.
- The sensing, fusion, and control architecture is retained, but the changed runtime settings mean the physical improvement cannot be attributed to detector weights alone.
- At the independent vehicle-run level, 8/18 pre-mitigation routes and 0/18 post-mitigation routes missed at least one required stop (two-sided Fisher exact test, `p = 0.0029`). Later unmet stop requirements after route termination are not additional observed attempts.

## Reproducibility Map

- `data/` contains raw run summaries, the archived training splits, and the range-separated held-out set.
- `models/` distinguishes the physical-mitigation checkpoint from the **different auxiliary offline-evaluation checkpoint**.
- `results/statistics/` contains Table 2, 5, and 7 analyses; `results/physical_training/` contains the physical-mitigation training run; `results/heldout_evaluation/` contains auxiliary detector-level results.
- `src/`, `scripts/`, `configs/`, and `environment/` contain runtime, analysis, and environment records.
- [Reproducibility instructions](docs/REPRODUCIBILITY.md), [result mapping](docs/MANUSCRIPT_RESULT_MAPPING.md), and [artifact audit](docs/ARTIFACT_AUDIT.md) explain provenance and limits.

## Evidence Limits

The manuscript reports 350 images, 1,092 annotations, and 480 stop-sign instances. The preserved checkpoint-linked split has 306 images and 964 annotations; the larger assembled folder has 347 images and 1,082 annotations. No verified per-image attack-design IDs or source corpus reproducing the manuscript totals has been located. The auxiliary held-out set has 41 images and 118 boxes, including 54 attacked stop-sign boxes, and **does not measure the physical-mitigation checkpoint**. See [dataset provenance](docs/DATASET_PROVENANCE.md) before reusing counts or making cross-pattern claims.

## Publication and Citation

An [earlier TechRxiv preprint](https://www.techrxiv.org/doi/abs/10.36227/techrxiv.177273783.33405285/v1) is available under DOI [10.36227/techrxiv.177273783.33405285/v1](https://doi.org/10.36227/techrxiv.177273783.33405285/v1). It predates the accepted IEEE Access article and should not be used as the source for revised numerical results or the final experimental interpretation. The IEEE Early Access or version-of-record link will be added when assigned; until then, cite the preprint explicitly as a preprint if it is the version used.

No project-wide reuse license is granted by this repository. Third-party dependency terms and rights to redistribute images, models, and the video require independent review.
