# Artifact Audit

This report preserves unresolved differences rather than rewriting data or manuscript statements. Resolve every **Open** item against the final accepted manuscript before public release.

## Open Conflicts

### Dataset Size and Composition — Open

- Manuscript snapshot: 350 images, 1,092 boxes, 480 stop-sign instances (175 clean, 305 adversarial).
- Checkpoint-linked historical split: 306 images, 964 boxes, 422 stop signs (153 clean, 269 adversarial).
- Later combined folder: 347 images, 1,082 boxes, 476 stop signs.
- No audited folder matches the manuscript totals. The checkpoint-linked split is supported by May 9, 2025 cache timestamps and validation mosaic filenames, but the runtime `data/qcar.yaml` was later edited and was not archived inside the run.

### Training Layer Statement — Open in Manuscript, Resolved in Artifact

- Manuscript snapshot says all layers were fine-tuned.
- `configs/training/opt.yaml` records `freeze: [10]`, meaning layer groups 0–9 were frozen.
- Required final wording: initialized from COCO-pretrained YOLOv5n, backbone layers 0–9 frozen, detection head updated.

### Additional-Design Run Count — Open in Manuscript, Resolved in Raw Data

- Manuscript snapshot states five post-mitigation runs for each of seven additional designs.
- `7_Mitigations.csv` contains six runs for each design, 42 rows total.
- Required final wording and tables use six runs per design.

### Table 5 Values — Open in Manuscript, Regenerated Draft Matches Raw Data

- The Table 5 embedded in the manuscript snapshot contains older means, ranges, misses, and percentage changes.
- The separate revised Table 5 document matches the regenerated values in `results/statistics/manuscript_ready_table5.txt`.
- Table 5 percentage change is computed as `100 * (attack_mean - baseline_mean) / baseline_mean`.

### Table 7 Values and Tests — Open in Manuscript, Regenerated Draft Matches Raw Data

- The Table 7 embedded in the manuscript snapshot contains older aggregates and repeats missed outcomes on first-detection rows.
- The separate revised Table 7 document matches the regenerated numeric values, bootstrap intervals, Mann–Whitney tests, and Fisher tests.
- Final presentation must show missed outcomes/Fisher only on final-stop rows and use dashes on first-detection rows.

### Missed-Outcome Definition — Open Wording Check

- The packaging decision defines missed stop outcome consistently as a vehicle-level final-stop outcome: missing final-stop measurement or final distance above 0.8 m.
- Some manuscript text also mentions absence of an accepted visual detection. Ensure the final definition does not turn a missing first-detection field into an outcome when a valid final stop exists.

### Figure 9 Interpretation — Open Wording Check

- Manuscript snapshot calls the model-selection validation curve evidence of good generalization.
- Neighboring video frames occur across the historical train/validation split.
- Required final wording treats Figure 9 as training/model-selection behavior, not independent generalization evidence.

### Held-Out Independence — Open Wording Check

- Frames 0306–0346 are disjoint by filename and exact image hash from the checkpoint-linked 0000–0305 pool.
- No explicit session/site IDs exist, all held-out stop signs are attacked, and attack variant is not encoded per frame.
- Required wording: range-separated held-out evaluation; do not claim full independence, cross-session, cross-site, or unseen-attack-type generalization.

## Model Audit

| Artifact | Role | SHA-256 |
|---|---|---|
| `models/pytorch/qcar_aug_exp1v2_best.pt` | reported mitigation checkpoint | `4fc9aa508079dd77ab183be989f69bb7187d225ac0a64199f46833e395f1e56f` |
| `models/tensorrt/qcar_aug_exp1v2_best.engine` | mitigation deployment engine | `234d99be5cd2ca67fba61c14bf59cd10d2aeece07fd995ae12b086e13297ad04` |
| `models/pytorch/yolov5n_coco_baseline.pt` | baseline detector | `4f180cf23ba0717ada0badd6c685026d73d48f184d00fc159c2641284b2ac0a3` |
| `models/tensorrt/yolov5n_coco_baseline.engine` | baseline deployment engine | `6149cc84c130b055765ded0c99ed93e33367c1cc9da412cd136a18f08a821838` |

A separate `best.pt` found in the old working repository has SHA-256 `df91fcbd0e68b8cd1bb99e0c6d1883b9fbbac930fd832c190cb63521c48860e2` and is intentionally excluded because it does not match the selected `qcar_aug_exp1v2/weights/best.pt` checkpoint.

## Runtime Source Audit

The master project notes identify `14_3stop_try_4_with_obj_tracking.py` for baseline/attack and `16_testbed_with_transfered_weights.py` for mitigation, with TensorRT variants added later. Release copies replace hard-coded model/YAML paths only. Original source SHA-256 values are:

- baseline PyTorch: `7fba1a825b2a3f58a17272270def90a65af942f695a88cccf6e09fc3f9c4a29b`
- baseline TensorRT: `36fe6c6983e574837d68267266406de09a7dbca9d310defcda5cffe8780cb037`
- mitigation PyTorch: `d26c0e5c9befa5ba8ee1bfe548a9e52036c3af82598d2fcb2a532ed465b3f300`
- mitigation TensorRT: `dd09a1f5a74119dae0e510f21d35d6b921605c384e2b07f86ad7d76576ac7cf0`

## Environment Audit

- Onboard deployment environment is verified separately from the later Windows held-out environment.
- Exact original RTX 3060 training package versions are not preserved; do not substitute the held-out evaluation environment.
- The manuscript gives cuDNN 8.0.0.180, while a project summary gives 8.0.0. Preserve the manuscript value unless the final environment record proves otherwise.

## Release-Rights Audit

No explicit project license or dataset redistribution permission was located. Model checkpoints, engine files, images, labels, Quanser-dependent code, and any third-party-derived files require manual rights review before public upload.
