from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
WEIGHTS = REPO_ROOT / "models" / "pytorch" / "qcar_aug_exp1v2_best.pt"
OUTPUT_ROOT = REPO_ROOT / "results" / "heldout_evaluation"
VALIDATION_PROJECT = OUTPUT_ROOT / "yolov5_validation"
VALIDATION_NAME = "qcar_aug_exp1v2_heldout_test"
CLASS_NAMES = ["obstacle_box", "stop_sign", "obstacle_bottle", "traffic_light", "car"]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate the reported YOLOv5n checkpoint on the held-out range.")
    parser.add_argument("--yolov5-root", type=Path, required=True, help="YOLOv5 v6.1 checkout at commit 3752807c")
    parser.add_argument("--img", type=int, default=640)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--device", default="0")
    parser.add_argument("--workers", type=int, default=4)
    return parser.parse_args()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def percent(value: float) -> str:
    return f"{100.0 * value:.2f}"


def main() -> None:
    args = parse_arguments()
    yolov5_root = args.yolov5_root.resolve()
    if not (yolov5_root / "val.py").is_file():
        raise FileNotFoundError(f"YOLOv5 val.py not found under {yolov5_root}")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    previous_cwd = Path.cwd()
    os.chdir(yolov5_root)
    sys.path.insert(0, str(yolov5_root))
    try:
        import torch
        import val

        captured: dict[str, object] = {}
        original_ap_per_class = val.ap_per_class

        def capture_ap_per_class(*function_args, **function_kwargs):
            result = original_ap_per_class(*function_args, **function_kwargs)
            captured["per_class"] = result
            return result

        val.ap_per_class = capture_ap_per_class
        data = {
            "path": str(REPO_ROOT),
            "test": "data/heldout_test/images",
            "nc": len(CLASS_NAMES),
            "names": CLASS_NAMES,
        }
        overall, _, speed = val.run(
            data=data,
            weights=str(WEIGHTS),
            batch_size=args.batch_size,
            imgsz=args.img,
            conf_thres=0.001,
            iou_thres=0.6,
            task="test",
            device=args.device,
            workers=args.workers,
            verbose=True,
            save_txt=True,
            save_conf=True,
            project=str(VALIDATION_PROJECT),
            name=VALIDATION_NAME,
            exist_ok=True,
            half=False,
            plots=True,
        )
    finally:
        os.chdir(previous_cwd)

    if "per_class" not in captured:
        raise RuntimeError("YOLOv5 did not return per-class statistics")

    _, _, precision, recall, _, ap_matrix, ap_classes = captured["per_class"]
    per_class_rows: list[dict[str, object]] = []
    for class_id, class_name in enumerate(CLASS_NAMES):
        matches = [index for index, value in enumerate(ap_classes) if int(value) == class_id]
        if not matches:
            raise RuntimeError(f"No evaluation statistics were produced for {class_name}")
        index = matches[0]
        per_class_rows.append(
            {
                "class_name": class_name,
                "precision": f"{float(precision[index]):.8f}",
                "recall": f"{float(recall[index]):.8f}",
                "AP@0.5": f"{float(ap_matrix[index, 0]):.8f}",
                "AP@0.5:0.95": f"{float(ap_matrix[index].mean()):.8f}",
            }
        )

    overall_row = {
        "precision": f"{float(overall[0]):.8f}",
        "recall": f"{float(overall[1]):.8f}",
        "mAP@0.5": f"{float(overall[2]):.8f}",
        "mAP@0.5:0.95": f"{float(overall[3]):.8f}",
    }
    write_csv(OUTPUT_ROOT / "heldout_test_metrics.csv", list(overall_row), [overall_row])
    write_csv(
        OUTPUT_ROOT / "per_class_metrics.csv",
        ["class_name", "precision", "recall", "AP@0.5", "AP@0.5:0.95"],
        per_class_rows,
    )

    table_lines = [
        "Held-out YOLOv5n detector evaluation",
        "Split: post-training attacked-sign collection, continuous frames 0306-0346",
        "",
        "Class                 Precision (%)  Recall (%)  AP@0.5 (%)  AP@0.5:0.95 (%)",
        "--------------------  -------------  ----------  -----------  ----------------",
    ]
    for row in per_class_rows:
        table_lines.append(
            f"{row['class_name']:<20}  {percent(float(row['precision'])):>13}  "
            f"{percent(float(row['recall'])):>10}  {percent(float(row['AP@0.5'])):>11}  "
            f"{percent(float(row['AP@0.5:0.95'])):>16}"
        )
    table_lines.append(
        f"{'Overall':<20}  {percent(float(overall[0])):>13}  {percent(float(overall[1])):>10}  "
        f"{percent(float(overall[2])):>11}  {percent(float(overall[3])):>16}"
    )
    (OUTPUT_ROOT / "manuscript_ready_heldout_table.txt").write_text(
        "\n".join(table_lines) + "\n", encoding="utf-8"
    )

    stop_sign = next(row for row in per_class_rows if row["class_name"] == "stop_sign")
    paragraph = (
        "The held-out test evaluation was performed on a range-separated, post-training attacked-sign "
        "collection comprising continuous frames 0306-0346. The COCO-pretrained YOLOv5n model, "
        "fine-tuned with backbone layers 0-9 frozen and the detection head updated, achieved "
        f"{percent(float(overall[2]))}% mAP@0.5 and {percent(float(overall[3]))}% mAP@0.5:0.95. "
        f"For attacked stop signs, precision was {percent(float(stop_sign['precision']))}%, recall was "
        f"{percent(float(stop_sign['recall']))}%, and AP@0.5 was {percent(float(stop_sign['AP@0.5']))}%. "
        "This range-separated evaluation does not establish cross-session or cross-site generalization."
    )
    (OUTPUT_ROOT / "manuscript_ready_heldout_paragraph.txt").write_text(paragraph + "\n", encoding="utf-8")

    runtime = {
        "overall": {key: float(value) for key, value in overall_row.items()},
        "per_class": [
            {key: value if key == "class_name" else float(value) for key, value in row.items()}
            for row in per_class_rows
        ],
        "speed_ms_per_image": {
            "preprocess": float(speed[0]),
            "inference": float(speed[1]),
            "nms": float(speed[2]),
        },
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "pytorch": torch.__version__,
        },
        "validation_output": "results/heldout_evaluation/yolov5_validation/qcar_aug_exp1v2_heldout_test",
    }
    (OUTPUT_ROOT / "evaluation_runtime.json").write_text(json.dumps(runtime, indent=2) + "\n", encoding="utf-8")
    print("Held-out metrics written to results/heldout_evaluation")


if __name__ == "__main__":
    main()
