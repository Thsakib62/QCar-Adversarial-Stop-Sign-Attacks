# Editorial-Manuscript Artifact Audit

The editorial manuscript supplied with this package is the wording reference. This audit distinguishes statements in that manuscript from facts independently recoverable from preserved artifacts. Raw experimental data and labels were not rewritten to force agreement.

## Confirmed Alignment

- The baseline and mitigation runtime source uses confidence thresholds 0.25 and 0.50, base throttle commands 0.065 and 0.075, and NMS IoU 0.45. These are commands/settings, not measured speeds.
- The YOLO training configuration records 100 epochs, batch size 8, image size 640, SGD, and `freeze: [10]`; the backbone groups 0–9 were frozen.
- The physical summary tables have six independent runs per primary design and six post-mitigation runs for each of seven additional designs.
- The separate held-out detector evaluation has 41 images, 118 boxes, and 54 attacked stop-sign boxes. Its checkpoint is distinct from the physical-training checkpoint.
- The source data support 8/18 pre-mitigation runs and 0/18 post-mitigation runs with at least one unmet required stop. Stops are nested within runs; an unattempted later stop after route termination is not a separately observed physical failure.

## Open Evidence Gaps

1. **Dataset totals:** the manuscript reports 350 images, 1,092 boxes, and 480 stop-sign instances, while the preserved checkpoint-linked split has 306 images, 964 boxes, and 422 stop-sign instances. The later combined folder has 347 images and 1,082 boxes. An original manifest supporting the larger manuscript totals has not been located.
2. **Attack-design identity:** the manuscript names Chen2, Eykholt1, and Eykholt3 as training patterns and says the three primary evaluated designs were excluded. The YOLO labels do not carry design IDs. That membership and exclusion cannot be independently checked per frame from the present artifacts.
3. **Figure 9 attribution:** both physical-training and auxiliary-training results are preserved, but the plotted curve embedded in the supplied PDF has not been traced by a figure-generation record to a unique results CSV. Do not label one archived curve as the paper's exact Figure 9 source without verification.
4. **Historical engine provenance:** a compatible TensorRT engine was copied from the QCar after re-export from the physical-training checkpoint. The video and physical summary CSVs do not provide a hash linking their runs to that exact engine binary.
5. **Missing controls:** no separately verified onboard inference latency, post-mitigation alignment counts, or matched clean-sign post-mitigation runs were found.
6. **Rights/privacy:** repository publication is not itself evidence of redistribution rights, privacy review, or permission to reuse third-party software or media. No project-wide license is granted.

## Reporting Boundaries

The held-out results measure an auxiliary offline checkpoint, not the checkpoint represented by `results/physical_training/`. The physical before/after comparison also changes confidence threshold and base throttle; it supports system-level recovery under tested conditions, not a detector-weights-only causal claim. The video is an edited qualitative demonstration, not a raw run record or statistical sample.
