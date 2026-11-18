import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODELS = {
    "baseline": (
        REPO_ROOT / "models" / "pytorch" / "yolov5n_coco_baseline.pt",
        REPO_ROOT / "models" / "tensorrt" / "yolov5n_coco_baseline.engine",
    ),
    "mitigation": (
        REPO_ROOT / "models" / "pytorch" / "qcar_physical_mitigation_best.pt",
        REPO_ROOT / "models" / "tensorrt" / "qcar_physical_mitigation_reexport.engine",
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a portable PyTorch checkpoint to a target-local TensorRT engine.")
    parser.add_argument("model", choices=MODELS)
    parser.add_argument("--yolov5-root", type=Path, required=True)
    parser.add_argument("--device", default="0")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    source, destination = MODELS[args.model]
    if destination.exists() and not args.force:
        raise FileExistsError(f"Refusing to overwrite {destination}; pass --force to replace it")
    yolov5_root = args.yolov5_root.resolve()
    subprocess.run(
        [
            sys.executable,
            str(yolov5_root / "export.py"),
            "--weights", str(source),
            "--include", "engine",
            "--imgsz", "640", "640",
            "--device", args.device,
        ],
        cwd=yolov5_root,
        check=True,
    )
    generated = source.with_suffix(".engine")
    if not generated.is_file():
        raise FileNotFoundError(f"YOLOv5 did not produce {generated}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(generated, destination)
    generated.unlink()
    print(f"Exported {destination.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
