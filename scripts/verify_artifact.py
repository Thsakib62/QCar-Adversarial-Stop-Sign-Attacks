from __future__ import annotations

import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKSUM_FILE = REPO_ROOT / "manifests" / "SHA256SUMS.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    failures = []
    checked = 0
    for line in CHECKSUM_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative_path = line.split("  ", 1)
        path = REPO_ROOT / relative_path
        actual = sha256(path) if path.is_file() else "MISSING"
        checked += 1
        if actual.lower() != expected.lower():
            failures.append((relative_path, expected, actual))
    if failures:
        for relative_path, expected, actual in failures:
            print(f"FAIL {relative_path}: expected {expected}, got {actual}")
        raise SystemExit(1)
    print(f"Verified {checked} files against manifests/SHA256SUMS.txt")


if __name__ == "__main__":
    main()
