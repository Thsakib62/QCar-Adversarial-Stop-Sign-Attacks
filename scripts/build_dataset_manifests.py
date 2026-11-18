from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLASS_NAMES = ["obstacle_box", "stop_sign", "obstacle_bottle", "traffic_light", "car"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def label_summary(path: Path) -> tuple[str, int, Counter[str]]:
    present: list[str] = []
    counts: Counter[str] = Counter()
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        fields = line.split()
        if not fields:
            continue
        if len(fields) != 5:
            raise ValueError(f"Expected five YOLO fields in {path}:{line_number}")
        class_id = int(fields[0])
        coordinates = [float(value) for value in fields[1:]]
        if class_id not in range(len(CLASS_NAMES)) or not all(0 <= value <= 1 for value in coordinates):
            raise ValueError(f"Invalid YOLO annotation in {path}:{line_number}")
        class_name = CLASS_NAMES[class_id]
        counts[class_name] += 1
        if class_name not in present:
            present.append(class_name)
    return ";".join(present), sum(counts.values()), counts


def write_manifest(split: str, image_dir: Path, label_dir: Path, output: Path) -> dict[str, object]:
    rows = []
    totals: Counter[str] = Counter()
    images = sorted(image_dir.glob("frame_*.jpg"))
    for image_path in images:
        label_path = label_dir / f"{image_path.stem}.txt"
        if not label_path.is_file():
            raise FileNotFoundError(f"Missing label for {image_path}")
        presence, object_count, counts = label_summary(label_path)
        totals.update(counts)
        rows.append(
            {
                "split": split,
                "image_path": image_path.relative_to(REPO_ROOT).as_posix(),
                "label_path": label_path.relative_to(REPO_ROOT).as_posix(),
                "frame_number": int(image_path.stem.split("_")[-1]),
                "class_presence": presence,
                "object_count": object_count,
                "image_sha256": sha256(image_path),
                "label_sha256": sha256(label_path),
            }
        )
    unpaired_labels = {path.stem for path in label_dir.glob("frame_*.txt")} - {path.stem for path in images}
    if unpaired_labels:
        raise RuntimeError(f"Unpaired labels in {label_dir}: {sorted(unpaired_labels)}")
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return {
        "images": len(rows),
        "labels": len(rows),
        "objects": sum(totals.values()),
        "class_counts": {name: totals[name] for name in CLASS_NAMES},
        "frame_min": min(row["frame_number"] for row in rows),
        "frame_max": max(row["frame_number"] for row in rows),
    }


def main() -> None:
    training_root = REPO_ROOT / "data" / "training"
    heldout_root = REPO_ROOT / "data" / "heldout_test"
    summaries = {
        "train": write_manifest(
            "train",
            training_root / "images" / "train",
            training_root / "labels" / "train",
            training_root / "train_manifest.csv",
        ),
        "val": write_manifest(
            "val",
            training_root / "images" / "val",
            training_root / "labels" / "val",
            training_root / "val_manifest.csv",
        ),
        "heldout_test": write_manifest(
            "test",
            heldout_root / "images",
            heldout_root / "labels",
            heldout_root / "heldout_test_manifest.csv",
        ),
    }
    train_rows = list(csv.DictReader((training_root / "train_manifest.csv").open(encoding="utf-8")))
    val_rows = list(csv.DictReader((training_root / "val_manifest.csv").open(encoding="utf-8")))
    heldout_rows = list(csv.DictReader((heldout_root / "heldout_test_manifest.csv").open(encoding="utf-8")))
    historical_frames = {int(row["frame_number"]) for row in train_rows + val_rows}
    heldout_frames = {int(row["frame_number"]) for row in heldout_rows}
    historical_hashes = {row["image_sha256"] for row in train_rows + val_rows}
    heldout_hashes = {row["image_sha256"] for row in heldout_rows}
    if historical_frames != set(range(306)):
        raise RuntimeError("Historical train/validation manifests are not exactly frames 0000-0305")
    if heldout_frames != set(range(306, 347)):
        raise RuntimeError("Held-out manifest is not exactly frames 0306-0346")
    if historical_hashes & heldout_hashes:
        raise RuntimeError("Exact image-content overlap found between historical and held-out splits")
    summaries["integrity"] = {
        "filename_overlap_historical_vs_heldout": len(historical_frames & heldout_frames),
        "sha256_image_overlap_historical_vs_heldout": len(historical_hashes & heldout_hashes),
    }
    (training_root / "dataset_counts.json").write_text(json.dumps(summaries, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
