# Pre-Upload Checklist

## Upload Gate

Do not upload this review-stage package until every unresolved author check below has been addressed and the final submitted manuscript uses the same terminology and configuration.

## Confirmed Package Checks

- [x] The package contains documentation files only.
- [x] No implementation source code or research scripts are included.
- [x] No dataset images, labels, annotations, or experimental CSV records are included.
- [x] No model checkpoints, TensorRT engines, logs, videos, ZIP archives, or training outputs are included.
- [x] No absolute local paths, machine usernames, authentication tokens, passwords, or private configuration files are included.
- [x] No open-source or data license has been added.
- [x] The GitHub destination is identified as `Thsakib62/QCar-Adversarial-Stop-Sign-Attacks`.

## Scientific Consistency Requirements

### 1. Training-Layer Scope

- [x] Repository wording states that backbone layers 0–9 were frozen and the detection head was updated.
- [ ] Confirm that the final submitted manuscript uses the same frozen-backbone and detection-head wording.

### 2. Dataset Totals

- **Current revised manuscript:** reports 350 images, 1,092 bounding boxes, and 480 stop-sign instances.
- **Available annotated source collection and reconstructed run-associated split:** do not reproduce those totals.
- [ ] Identify the authoritative dataset snapshot and reconcile the manuscript totals before upload. The alternative unpublished source totals are intentionally not reproduced in this public package.

### 3. Tables 5 and 7

- [x] Repository methodology defines missed stop outcome as a vehicle-level final-stop outcome.
- [x] Repository methodology limits missed stop outcome counts to final-stopping-distance rows; detection-distance rows use `n valid/total` and a blank or dash in the missed-outcome field.
- [x] Repository methodology specifies Fisher's exact test for independent pre/post missed-stop outcomes.
- [x] Repository methodology specifies bootstrap 95% confidence intervals and Mann–Whitney U tests for valid continuous pre/post values.
- [ ] Confirm that the final submitted Tables 5 and 7 follow these same definitions and procedures.

### 4. Experiment Counts and Evaluation Terminology

- [x] Repository wording specifies six post-mitigation runs for each of the seven additional adversarial designs.
- [x] Repository wording describes the detector test as a range-separated held-out evaluation without claiming full independence.
- [x] Repository wording treats Figure 9 as training/model-selection behavior rather than independent generalization evidence.
- [ ] Confirm that the final submitted manuscript applies these statements consistently in text, captions, and tables.

### 5. cuDNN Version Formatting

- The revised manuscript reports cuDNN `8.0.0.180`; a supplied environment summary uses `8.0.0`.
- [ ] Confirm whether `8.0.0.180` is the required exact package/build notation and use one consistent form in the manuscript and repository.

## Manual Checks Before Public Upload

- [ ] Replace the manuscript placeholder `[REPOSITORY URL]` with `https://github.com/Thsakib62/QCar-Adversarial-Stop-Sign-Attacks` when appropriate for submission.
- [ ] Confirm the paper title and author ordering against the final submission PDF.
- [ ] Confirm that no DOI is added to the repository until the DOI is assigned and verified.
- [ ] Confirm that the repository should be made public at the current review stage.
- [ ] Review all rendered Markdown pages on GitHub after the first approved push.
- [ ] Re-run the documentation-only, path, credential, and sensitive-information audit immediately before pushing.
