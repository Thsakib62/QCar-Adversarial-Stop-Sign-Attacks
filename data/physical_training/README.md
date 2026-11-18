# Physical-Training Image and Label Split

This directory preserves 244 training and 62 validation image/YOLO-label pairs from the checkpoint-linked physical-mitigation training run. Frames span `0000–0305`; labels contain 964 boxes across five classes, including 422 `stop_sign` boxes. The train/validation split contains adjacent frames and is not an independent held-out test.

The labels use `stop_sign` for both clean and attacked signs and do not encode individual attack-design names. See `docs/DATASET_PROVENANCE.md` for the distinction between verified label counts and larger manuscript totals.
