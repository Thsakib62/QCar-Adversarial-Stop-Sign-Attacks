# Dataset Provenance

## Checkpoint-Linked Historical Corpus

The strongest available provenance links `qcar_aug_exp1v2` to the preserved split in `data/training/`:

- 244 training images and labels; 758 boxes
- 62 model-selection validation images and labels; 206 boxes
- 306 total images; 964 total boxes
- five classes: `obstacle_box`, `stop_sign`, `obstacle_bottle`, `traffic_light`, `car`
- filename pool spans frames 0000–0305, randomly distributed between train and validation
- `train.cache` and `val.cache` timestamps align with the May 9, 2025 run
- saved validation mosaics match filenames in this split

Per-class totals are 114 obstacle boxes, 422 stop signs, 81 obstacle bottles, 191 traffic lights, and 156 cars. The split is preserved exactly, including cache files and per-file manifests.

## Stop-Sign Semantics

By the acquisition naming rule supplied with the dataset:

- frames 0000–0200 contain clean stop-sign instances
- frames 0201 onward contain attacked stop-sign instances labeled as `stop_sign`
- attacked variants are Eykholt1, Eykholt2, or Lu3, but the individual variant is not encoded per frame

The reconstructed historical split contains 153 clean and 269 attacked stop-sign annotations. Train contains 125 clean and 199 attacked annotations; validation contains 28 clean and 70 attacked annotations.

## Range-Separated Held-Out Set

The held-out set contains continuous frames 0306–0346 from a post-training collection batch:

- 41 images and labels
- 118 boxes
- 54 attacked stop-sign boxes and no clean stop-sign boxes
- no filename or exact SHA-256 image overlap with the 0000–0305 historical pool

This separation reduces direct frame overlap but does not establish session, scene, site, or attack-variant independence. No explicit session IDs are available.

## Known Alternative Dataset Folder

A later combined source contains 347 images, 1,082 boxes, and frames 0000–0346. It combines the historical pool with the held-out range and must not be retroactively treated as the checkpoint’s original training corpus.

## Unresolved Manuscript Count

The manuscript snapshot states 350 images, 1,092 boxes, and 480 stop signs (175 clean and 305 adversarial). No preserved folder audited during packaging matches these totals. See `ARTIFACT_AUDIT.md`; the release does not silently choose a replacement value.

## Redistribution

Images and labels are staged in this local release package. Their public redistribution rights and participant/privacy status require explicit manual approval before upload. No dataset license is implied.
