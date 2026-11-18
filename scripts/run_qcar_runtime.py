import argparse
import os
import runpy
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VARIANTS = {
    "baseline-pytorch": ("baseline_pytorch.py", "models/pytorch/yolov5n_coco_baseline.pt", None),
    "baseline-tensorrt": ("baseline_tensorrt.py", "models/tensorrt/yolov5n_coco_baseline.engine", "coco"),
    "mitigation-pytorch": ("mitigation_pytorch.py", "models/pytorch/qcar_physical_mitigation_best.pt", None),
    "mitigation-tensorrt": ("mitigation_tensorrt.py", "models/tensorrt/qcar_physical_mitigation_reexport.engine", "qcar"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch a QCar runtime variant on compatible Quanser hardware.")
    parser.add_argument("variant", choices=VARIANTS)
    parser.add_argument("--yolov5-root", type=Path, required=True)
    args = parser.parse_args()
    script_name, weights, data_kind = VARIANTS[args.variant]
    yolov5_root = args.yolov5_root.resolve()
    sys.path.insert(0, str(yolov5_root))
    os.environ["QCAR_WEIGHTS"] = str(REPO_ROOT / weights)
    if data_kind == "coco":
        os.environ["QCAR_DATA_YAML"] = str(yolov5_root / "data" / "coco.yaml")
    elif data_kind == "qcar":
        os.environ["QCAR_DATA_YAML"] = str(REPO_ROOT / "configs" / "dataset" / "qcar.yaml")
    os.chdir(REPO_ROOT)
    runpy.run_path(str(REPO_ROOT / "src" / "qcar_runtime" / script_name), run_name="__main__")


if __name__ == "__main__":
    main()
