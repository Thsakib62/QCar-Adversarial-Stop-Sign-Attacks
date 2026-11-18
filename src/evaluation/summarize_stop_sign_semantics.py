from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
TRAIN_LABELS = REPO_ROOT / "data" / "training" / "labels"
HELDOUT_LABELS = REPO_ROOT / "data" / "heldout_test" / "labels"
RESULTS = REPO_ROOT / "results" / "heldout_evaluation"


def frame_number(path: Path) -> int:
    return int(path.stem.split("_")[-1])


def stop_sign_count(path: Path) -> int:
    return sum(
        1
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.split() and int(line.split()[0]) == 1
    )


def summarize(label_dir: Path) -> dict[str, Counter[str]]:
    summary = {"clean": Counter(), "attacked": Counter()}
    for label_path in sorted(label_dir.glob("frame_*.txt")):
        condition = "clean" if frame_number(label_path) <= 200 else "attacked"
        occurrences = stop_sign_count(label_path)
        summary[condition]["images"] += 1
        summary[condition]["images_with_stop_sign"] += int(occurrences > 0)
        summary[condition]["stop_sign_annotations"] += occurrences
    return summary


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    scopes = {
        ("historical_training", "train"): summarize(TRAIN_LABELS / "train"),
        ("historical_model_selection", "val"): summarize(TRAIN_LABELS / "val"),
        ("range_heldout", "test"): summarize(HELDOUT_LABELS),
    }
    rows = []
    for (scope, split), summary in scopes.items():
        for condition, values in summary.items():
            if values["images"]:
                rows.append(
                    {
                        "dataset_scope": scope,
                        "split": split,
                        "stop_sign_condition": condition,
                        "images": values["images"],
                        "images_with_stop_sign": values["images_with_stop_sign"],
                        "stop_sign_annotations": values["stop_sign_annotations"],
                    }
                )
    with (RESULTS / "stop_sign_condition_breakdown.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    manifest = []
    for label_path in sorted(HELDOUT_LABELS.glob("frame_*.txt")):
        number = frame_number(label_path)
        occurrences = stop_sign_count(label_path)
        if number <= 200 or occurrences == 0:
            raise RuntimeError(f"Unexpected held-out stop-sign semantics for {label_path.name}")
        manifest.append(
            {
                "image_path": f"data/heldout_test/images/{label_path.stem}.jpg",
                "label_path": f"data/heldout_test/labels/{label_path.name}",
                "frame_number": number,
                "stop_sign_occurrences": occurrences,
                "stop_sign_condition": "attacked",
                "attack_variant": "Eykholt1_or_Eykholt2_or_Lu3_not_encoded_per_frame",
            }
        )
    with (REPO_ROOT / "data" / "heldout_test" / "stop_sign_condition_manifest.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)


if __name__ == "__main__":
    main()
