# Data Layout

- `baseline/` — 30 clean baseline runs
- `pre_mitigation/` — six runs each for Lu2, Yang, and Lu3
- `post_mitigation/` — six post-mitigation runs each for Lu2, Yang, and Lu3
- `additional_patterns/` — six post-mitigation runs each for seven additional designs
- `training/` — checkpoint-linked 244/62 train/model-selection split and manifests
- `heldout_test/` — frames 0306–0346, labels, manifests, and split provenance

The raw experimental CSV files preserve their original names and contents. Reproduction scripts write only under `results/`. Public redistribution of image data requires explicit approval; no data license is granted by this package.
