# Reproducibility Summary

## Scope

This document summarizes the configuration and reporting methodology associated with the manuscript. The review-stage repository does not contain the implementation, datasets, model files, raw records, statistical-analysis assets, or executable instructions required to reproduce the experiments end to end.

## Physical Platform and Sensors

The experiments use a Quanser QCar with an NVIDIA Jetson TX2 for onboard processing. A front-facing CSI RGB camera supplies images to a YOLOv5n detector, and an RPLiDAR A2 supplies 2D polar range measurements. Camera detections and LiDAR ranges are fused before control actions are issued; LiDAR does not independently recover a stop-sign detection missed by the visual detector.

## Runtime Configuration

| Item | Manuscript-reported configuration |
| --- | --- |
| Camera sensor sampling | 30 FPS |
| LiDAR sensor sampling | 30 Hz |
| Effective camera inference | approximately 8–10 FPS |
| Effective LiDAR updates | approximately 12–15 Hz |
| Control loop | 20 Hz (50 ms period) |
| Maximum accepted sample age, `tau_age` | 150 ms |
| Maximum camera–LiDAR timestamp skew, `tau_sync` | 80 ms |
| Calibrated stopping threshold | 0.8 m |

The runtime architecture uses concurrent camera, LiDAR, and control activities. The control activity consumes recent timestamped sensor records and forms a fused update only when the visual detection and LiDAR estimate satisfy the configured validity and timing conditions.

## Course and Trial Organization

The indoor course begins at a fixed start position and contains three stop locations separated by two left turns. The runtime does not use a preloaded map or externally supplied stop-sign way-points. Sign geometry, mounting position, approach geometry, lighting, and controller configuration are held constant as described in the manuscript.

The manuscript organizes the evaluation as follows:

1. **Clean-sign baseline:** 30 runs using the same three-stop route.
2. **Adversarial-sign evaluation:** ten physically printed adversarial designs are considered. Lu2, Yang, and Lu3 receive the primary six-run-per-design evaluation; the remaining seven designs are exercised once in the attack study.
3. **Mitigation evaluation:** the fine-tuned YOLOv5n detector replaces the baseline detector without changing sensing, fusion, thresholds, or control. Lu2, Yang, and Lu3 receive six post-mitigation runs per design, and the remaining seven designs also receive six post-mitigation runs per design.

This review-stage documentation does not reproduce the manuscript's numerical outcome tables.

## Dataset and Training Summary

The following values reproduce the manuscript-reported dataset and training description. Dataset-total verification remains listed in [`PREUPLOAD_CHECKLIST.md`](PREUPLOAD_CHECKLIST.md):

- 350 camera images at 640 × 640 resolution
- 1,092 bounding-box annotations
- Five classes: stop sign, traffic light, car, and two obstacle classes
- 480 stop-sign instances, comprising 175 clean and 305 adversarial instances
- Adversarial training exemplars corresponding to Lu3, Eykholt1, and Eykholt2, labeled as the stop-sign class
- 80% training and 20% validation split
- COCO-pretrained YOLOv5n initialization
- 100 training epochs
- Batch size 8
- Initial learning rate 0.030
- SGD optimization schedule
- Backbone layers 0–9 frozen
- Detection head updated during fine-tuning

The training description consistently uses the saved configuration: frozen backbone layers 0–9 with detection-head updating.

### Manuscript-Reported Augmentation Configuration

| Hyperparameter | Value |
| --- | ---: |
| HSV hue | 0.02 |
| HSV saturation | 0.5 |
| HSV value | 0.4 |
| Rotation | 10.0 degrees |
| Translation | 0.2 |
| Scale variation | 0.3 |
| Shear | 2.0 degrees |
| Perspective | 0.0005 |
| Vertical flip probability | 0.1 |
| Horizontal flip probability | 0.5 |
| Mosaic probability | 0.8 |
| Mixup probability | 0.1 |
| Copy-paste probability | 0.05 |

## Statistical Reporting

Baseline summaries use the mean, standard deviation, observed range, and 95% confidence intervals. Box plots use the median and interquartile range. Attack and mitigation distance summaries use valid numeric observations; missing values are not replaced with zero.

For pre/post comparisons, continuous metrics use bootstrap 95% confidence intervals and Mann–Whitney U tests on valid numeric values. Missed stop outcomes use Fisher's exact test because the pre- and post-mitigation runs are independent.

The term **missed stop outcome** refers consistently to a vehicle-level final-stop outcome. In Tables 5 and 7, missed stop outcome counts are shown only for final-stopping-distance rows. First-detection-distance rows report `n valid/total`, while the missed stop outcome field remains blank or is shown as a dash.

## Detector-Level Evaluation Reporting

The detector evaluation separated by a continuous frame range is described as a **range-separated held-out evaluation**. This wording recognizes reduced frame overlap without claiming full session, scene, or site independence.

Figure 9 represents training and model-selection behavior on the training/validation workflow. It is not presented as independent generalization evidence. Detector-level held-out reporting and closed-loop QCar outcomes are treated as distinct forms of evidence.
