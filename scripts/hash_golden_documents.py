#!/usr/bin/env python3
"""Build SHA256 manifest for golden-dataset raw documents."""

from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "golden-dataset" / "atlante-concorsi-universitari"
RAW_DIR = BASE / "raw_documents"
MANIFEST_PATH = BASE / "qa_reports" / "document_hash_manifest.csv"

IGNORE_NAMES = {"README.md", ".gitkeep"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_metadata(path: Path) -> dict[str, str]:
    rel = path.relative_to(RAW_DIR)
    parts = rel.parts
    university_slug = parts[0] if len(parts) > 0 else ""
    procedure_id = parts[1] if len(parts) > 1 else ""
    stat = path.stat()
    modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
    return {
        "procedure_id": procedure_id,
        "university_slug": university_slug,
        "relative_file_path": str(rel),
        "sha256": sha256_file(path),
        "file_size_bytes": str(stat.st_size),
        "last_modified_at": modified,
    }


def main() -> int:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for path in RAW_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.name in IGNORE_NAMES:
            continue
        rows.append(file_metadata(path))

    rows.sort(key=lambda r: r["relative_file_path"])

    fieldnames = [
        "procedure_id",
        "university_slug",
        "relative_file_path",
        "sha256",
        "file_size_bytes",
        "last_modified_at",
    ]

    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Manifest written: {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Files hashed: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
