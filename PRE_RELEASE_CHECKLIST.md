# Release Review Checklist

This repository is public. The following items remain open and are disclosed rather than silently treated as verified.

## Evidence and Manuscript

- [ ] Locate an original source manifest supporting the manuscript's 350-image, 1,092-box, and 480-stop-sign training totals.
- [ ] Locate per-image evidence identifying Chen2, Eykholt1, and Eykholt3 in the fine-tuning corpus.
- [ ] Establish the historical engine hash used in the physical mitigation runs.
- [ ] Establish the exact source run for the Figure 9 curve.
- [ ] Link the edited demonstration segments to raw run IDs if such records exist.

## Rights and Privacy

- [ ] Choose a project source-code license or intentionally retain all-rights-reserved status.
- [ ] Confirm redistribution rights for QCar images, labels, checkpoints, engines, and demonstration video.
- [ ] Review Ultralytics YOLOv5 and Quanser dependency terms.
- [ ] Review images and video for personal or facility information before further distribution.
- [ ] Add final DOI and publication metadata when assigned.

## Technical Verification

- [ ] Re-run dataset and statistical reproduction in a clean analysis environment.
- [ ] Validate launch scripts on the secured physical testbed before any new trials.
- [ ] Re-export TensorRT engines only on a compatible Jetson stack if needed.
- [ ] Verify release checksums after any intentional package change.
