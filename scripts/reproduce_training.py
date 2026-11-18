from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLASS_NAMES = ["obstacle_box", "stop_sign", "obstacle_bottle", "traffic_light", "car"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce qcar_aug_exp1v2 without overwriting the archived run.")
    parser.add_argument("--yolov5-root", type=Path, required=True)
    parser.add_argument("--device", default="0")
    args = parser.parse_args()
    yolov5_root = args.yolov5_root.resolve()
    output_project = REPO_ROOT / "results" / "training_reproduction"
    data_text = (
        f"path: '{REPO_ROOT.as_posix()}'\n"
        "train: data/training/images/train\n"
        "val: data/training/images/val\n"
        "nc: 5\n"
        f"names: {CLASS_NAMES!r}\n"
    )
    with tempfile.TemporaryDirectory(prefix="qcar_yolov5_") as temporary_directory:
        data_yaml = Path(temporary_directory) / "qcar.yaml"
        data_yaml.write_text(data_text, encoding="utf-8")
        command = [
            sys.executable,
            str(yolov5_root / "train.py"),
            "--weights", str(REPO_ROOT / "models" / "pytorch" / "yolov5n_coco_baseline.pt"),
            "--data", str(data_yaml),
            "--hyp", str(REPO_ROOT / "configs" / "training" / "hyp.yaml"),
            "--epochs", "100",
            "--batch-size", "8",
            "--imgsz", "640",
            "--optimizer", "SGD",
            "--freeze", "10",
            "--device", args.device,
            "--project", str(output_project),
            "--name", "qcar_aug_exp1v2_reproduction",
            "--exist-ok",
        ]
        subprocess.run(command, cwd=yolov5_root, check=True)


if __name__ == "__main__":
    main()
