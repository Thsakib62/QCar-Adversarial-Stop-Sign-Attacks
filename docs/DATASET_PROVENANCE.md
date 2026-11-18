# Dataset Provenance

## Physical-Mitigation Training Evidence

`data/physical_training/` preserves the checkpoint-linked image and YOLO-label split from the later fine-tuning run. The saved training configuration and metrics are under `configs/training/` and `results/physical_training/`.

- 244 training images and labels, 765 boxes; 62 model-selection validation images and labels, 199 boxes.
- 306 distinct frames, `frame_0000` through `frame_0305`, and 964 boxes overall.
- Five classes in order: `obstacle_box`, `stop_sign`, `obstacle_bottle`, `traffic_light`, `car`.
- 422 stop-sign boxes: 153 in frames `0000–0200` (clean by the supplied naming rule) and 269 in frames `0201–0305` (attacked by that rule).
- The train/validation image split interleaves neighboring frames; its validation curve is model-selection evidence, not independent generalization.

The five-class YOLO labels encode every stop-sign instance as class `1`, without a clean/attacked flag or attack-design ID. The current manuscript names Chen2, Eykholt1, and Eykholt3 as training patterns, but the preserved filenames and labels do not independently identify those designs per image. These names should not be inferred from the label index. The claim that Lu2, Yang, and Lu3 were absent from training likewise cannot be verified from the annotations alone.

## Auxiliary Offline Detector Evaluation

`data/training/` preserves the separate training split associated with the **auxiliary offline-evaluation checkpoint**. It also has 306 images and 964 boxes, but has a different train/validation allocation and image content. Its manifests and cache-provenance record belong to that auxiliary analysis, not to the physical-training split.

`data/heldout_test/` contains frames `0306–0346`: 41 images, 41 labels, and 118 boxes. All 54 stop-sign boxes are attacked by the naming rule; there are no clean stop-sign boxes. The other 64 annotations are different classes. The attack design is not encoded per frame, and the split is range-separated rather than proven independent by session or site. The reported detector metrics in `results/heldout_evaluation/` evaluate the auxiliary checkpoint only, **not** the physical-mitigation checkpoint.

## Manuscript Aggregate Not Reproduced

The editorial manuscript reports 350 images, 1,092 boxes, and 480 stop-sign boxes (175 clean, 305 attacked). Neither the preserved 306-image checkpoint-linked split nor the 347-image later assembled folder reproduces those totals. The missing four-image/ten-box provenance cannot be supplied by changing labels or silently adding held-out frames to training. This numerical discrepancy remains open pending an original dataset or collection manifest supporting the manuscript totals.

No project-wide dataset license or per-image redistribution clearance is implied by the presence of images in this repository.
