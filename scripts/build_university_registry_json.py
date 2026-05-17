#!/usr/bin/env python3
"""Build deterministic JSON payload for the static university mapping UX."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = ROOT / "data/source-registries/italian-universities/official_university_urls.csv"
OUTPUT_JSON = ROOT / "site/data/university_registry.json"


def normalize(value: str | None) -> str:
    return (value or "").strip()


def truthy(value: str) -> bool:
    return normalize(value).lower() not in {"", "none", "null", "n/a", "na"}


def build() -> dict:
    with INPUT_CSV.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    entries = []
    for row in rows:
        recruitment = normalize(row.get("recruitment_page_url"))
        status = normalize(row.get("verification_status"))
        notes = normalize(row.get("notes"))
        has_recruitment = truthy(recruitment)
        attention = status in {"needs_human_review", "not_determinable"} or (not has_recruitment)

        entries.append(
            {
                "university_id": normalize(row.get("university_id")),
                "university_name": normalize(row.get("university_name")),
                "university_type": normalize(row.get("university_type")),
                "official_homepage_url": normalize(row.get("official_homepage_url")),
                "recruitment_page_url": recruitment,
                "source_url": normalize(row.get("source_url")),
                "source_type": normalize(row.get("source_type")),
                "retrieval_date": normalize(row.get("retrieval_date")),
                "confidence_level": normalize(row.get("confidence_level")),
                "verification_status": status,
                "notes": notes,
                "has_verified_homepage": truthy(normalize(row.get("official_homepage_url"))),
                "has_recruitment_url": has_recruitment,
                "is_homepage_only": status == "homepage_only",
                "needs_attention": attention,
                "is_not_determinable": status == "not_determinable",
            }
        )

    entries.sort(key=lambda item: (item["university_name"].casefold(), item["university_id"]))

    summary = {
        "total_universities_mapped": len(entries),
        "with_verified_homepage": sum(1 for e in entries if e["has_verified_homepage"]),
        "with_recruitment_url": sum(1 for e in entries if e["has_recruitment_url"]),
        "homepage_only": sum(1 for e in entries if e["is_homepage_only"]),
        "needing_attention": sum(1 for e in entries if e["needs_attention"]),
        "not_determinable": sum(1 for e in entries if e["is_not_determinable"]),
    }

    verification_statuses = sorted({e["verification_status"] for e in entries if e["verification_status"]})
    confidence_levels = sorted({e["confidence_level"] for e in entries if e["confidence_level"]})

    return {
        "generated_at_utc": "2026-05-17T00:00:00Z",
        "source_csv": str(INPUT_CSV.relative_to(ROOT)),
        "summary": summary,
        "filters": {
            "verification_status": verification_statuses,
            "confidence_level": confidence_levels,
        },
        "entries": entries,
    }


def main() -> None:
    payload = build()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSON.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Wrote {OUTPUT_JSON.relative_to(ROOT)} ({len(payload['entries'])} entries)")


if __name__ == "__main__":
    main()
