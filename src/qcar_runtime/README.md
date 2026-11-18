# QCar Runtime Sources

The four scripts correspond to baseline versus mitigation and PyTorch versus TensorRT execution. They initialize physical hardware at module start. Use `scripts/run_qcar_runtime.py` rather than invoking them directly.

The public copies differ from the archived source only by replacing machine-specific model/data paths with `QCAR_WEIGHTS` and `QCAR_DATA_YAML`. Control behavior and experimental thresholds were not intentionally changed. Original hashes are recorded in `docs/ARTIFACT_AUDIT.md`.
