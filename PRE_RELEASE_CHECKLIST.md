# Pre-Release Checklist

## Blocking Manual Decisions

- [ ] Reconcile the manuscript’s 350-image/1,092-box/480-stop-sign statement with the checkpoint-linked 306-image/964-box/422-stop-sign corpus.
- [ ] Replace the manuscript’s “all layers” wording with frozen layer groups 0–9 and updated detection head.
- [ ] Update all seven-additional-design statements from five to six runs per design.
- [ ] Replace embedded Tables 5 and 7 with the regenerated values and presentation.
- [ ] Ensure missed stop outcome is consistently defined as a vehicle-level final-stop outcome.
- [ ] Describe Figure 9 as training/model-selection behavior, not independent generalization.
- [ ] Describe the held-out test as range-separated, not fully independent.

## Rights and Privacy

- [ ] Select an explicit project source-code license or intentionally publish without reuse permission.
- [ ] Confirm redistribution rights for all QCar images and labels.
- [ ] Confirm redistribution rights for trained `.pt` checkpoints and `.engine` binaries.
- [ ] Review Ultralytics YOLOv5 v6.1 GPL-3.0 obligations and Quanser software/API terms.
- [ ] Confirm that no identifiable people, screens, badges, addresses, or private facilities appear in images or plots.
- [ ] Confirm author names and final citation metadata; add DOI, publication year, journal volume, and pages when assigned.

## Technical Verification

- [ ] Run `python scripts/reproduce_statistics.py` in a clean analysis environment.
- [ ] Run `python scripts/build_dataset_manifests.py` and review counts.
- [ ] Run the held-out evaluation against a fresh pinned YOLOv5 checkout.
- [ ] Validate QCar launch scripts on the secured hardware testbed.
- [ ] Re-export TensorRT engines on the documented Jetson stack and compare behavior.
- [ ] Run `python scripts/verify_artifact.py` after the final checksum generation.
- [ ] Confirm Git LFS tracking before adding `.pt`, `.engine`, and dataset images.
- [ ] Review `docs/ARTIFACT_AUDIT.md` and close every open item.

## Upload Safety

- [ ] Confirm the upload source is only `github_full_release/`, not the master project.
- [ ] Inspect `git status` and staged file list before commit.
- [ ] Scan for absolute paths, credentials, tokens, private keys, caches, ZIP files, and unrelated experiments.
- [ ] Do not publish until acceptance and all rights checks are complete.
