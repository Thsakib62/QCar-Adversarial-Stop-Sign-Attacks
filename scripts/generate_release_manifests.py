from __future__ import annotations

import csv
import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = REPO_ROOT / "manifests"
SHA_FILE = MANIFEST_DIR / "SHA256SUMS.txt"
ARTIFACT_FILE = MANIFEST_DIR / "ARTIFACT_MANIFEST.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(relative_path: str) -> tuple[str, str, str]:
    if relative_path.startswith("data/training/") or relative_path.startswith("data/heldout_test/"):
        return "annotated_dataset", "Annotated image/label data or dataset provenance", "required"
    if relative_path.startswith("data/"):
        return "raw_experiment_data", "Preserved experimental input", "required"
    if relative_path.startswith("models/") and not relative_path.endswith("README.md"):
        return "model", "Baseline or mitigation model artifact", "required"
    if relative_path.startswith("results/"):
        return "result", "Reference generated result", "review"
    if relative_path.startswith("src/") or relative_path.startswith("scripts/"):
        return "source", "Reproduction or runtime source", "review"
    if relative_path.startswith("configs/") or relative_path.startswith("environment/"):
        return "configuration", "Configuration or environment record", "review"
    if relative_path.startswith("docs/") or relative_path.endswith(".md") or relative_path.endswith(".cff"):
        return "documentation", "Release documentation", "review"
    return "metadata", "Release metadata", "review"


def main() -> None:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(
        path
        for path in REPO_ROOT.rglob("*")
        if path.is_file() and path not in {SHA_FILE, ARTIFACT_FILE}
    )
    hashes = {path: sha256(path) for path in files}
    SHA_FILE.write_text(
        "".join(f"{hashes[path]}  {path.relative_to(REPO_ROOT).as_posix()}\n" for path in files),
        encoding="utf-8",
    )

    inventory_files = files + [SHA_FILE]
    rows = []
    for path in inventory_files:
        relative = path.relative_to(REPO_ROOT).as_posix()
        category, purpose, redistribution_review = describe(relative)
        rows.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": hashes.get(path, sha256(path)),
                "category": category,
                "purpose": purpose,
                "redistribution_review": redistribution_review,
            }
        )
    rows.append(
        {
            "path": "manifests/ARTIFACT_MANIFEST.csv",
            "bytes": "",
            "sha256": "",
            "category": "metadata",
            "purpose": "Self-referential release inventory; hash intentionally omitted",
            "redistribution_review": "review",
        }
    )
    with ARTIFACT_FILE.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(files)} checksums and {len(rows)} inventory rows")


if __name__ == "__main__":
    main()
