#!/usr/bin/env python3
"""Build deterministic mapping progress history for static UX time-tracker."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_JSON = ROOT / "site/data/university_registry.json"
MISSING_CSV = ROOT / "data/source-registries/italian-universities/missing_universities_to_verify.csv"
OUTPUT_JSON = ROOT / "site/data/mapping_progress_history.json"


def _load_registry_summary() -> dict:
    payload = json.loads(REGISTRY_JSON.read_text(encoding="utf-8"))
    return payload["summary"]


def _missing_count() -> int:
    with MISSING_CSV.open(encoding="utf-8", newline="") as handle:
        return len(list(csv.DictReader(handle)))


def build() -> dict:
    summary = _load_registry_summary()
    missing_count = _missing_count()
    today = date.today().isoformat()

    history = [
        {
            "snapshot_date": "2026-01-20",
            "snapshot_source": "bootstrap_registry",
            "universities_total": 10,
            "universities_with_homepage": 10,
            "universities_with_recruitment_url": 4,
            "universities_homepage_only": 6,
            "universities_needs_human_attention": 6,
            "universities_not_determinable": 0,
            "competition_sources_total": 0,
            "competition_sources_classified": 0,
            "status_label": "partial coverage",
            "notes": "Bootstrap registry milestone (10 universities mapped).",
        },
        {
            "snapshot_date": "2026-02-10",
            "snapshot_source": "expanded_subset",
            "universities_total": 30,
            "universities_with_homepage": 30,
            "universities_with_recruitment_url": 12,
            "universities_homepage_only": 18,
            "universities_needs_human_attention": 18,
            "universities_not_determinable": 0,
            "competition_sources_total": 0,
            "competition_sources_classified": 0,
            "status_label": "partial coverage",
            "notes": "Expanded subset milestone (30 universities mapped).",
        },
        {
            "snapshot_date": "2026-03-18",
            "snapshot_source": "controlled_registry_expansion",
            "universities_total": 80,
            "universities_with_homepage": 80,
            "universities_with_recruitment_url": 28,
            "universities_homepage_only": 9,
            "universities_needs_human_attention": 52,
            "universities_not_determinable": 1,
            "competition_sources_total": 0,
            "competition_sources_classified": 0,
            "status_label": "needs continuation",
            "notes": "Controlled registry expansion milestone (80 universities mapped).",
        },
        {
            "snapshot_date": "2026-04-12",
            "snapshot_source": "coverage_audit",
            "universities_total": 80,
            "universities_with_homepage": 80,
            "universities_with_recruitment_url": 28,
            "universities_homepage_only": 9,
            "universities_needs_human_attention": 52,
            "universities_not_determinable": 1,
            "competition_sources_total": 0,
            "competition_sources_classified": 0,
            "status_label": "coverage audit",
            "notes": "99 expected / 80 present / 19 missing coverage audit recorded.",
        },
        {
            "snapshot_date": today,
            "snapshot_source": "registry_plus_missing_reconciliation",
            "universities_total": summary["total_universities_mapped"],
            "universities_with_homepage": summary["with_verified_homepage"],
            "universities_with_recruitment_url": summary["with_recruitment_url"],
            "universities_homepage_only": summary["homepage_only"],
            "universities_needs_human_attention": summary["needing_attention"],
            "universities_not_determinable": summary["not_determinable"],
            "competition_sources_total": 0,
            "competition_sources_classified": 0,
            "status_label": "reconciliation backlog",
            "notes": f"80 mapped + missing_universities_to_verify.csv with {missing_count} rows pending verification.",
        },
    ]

    return {
        "generated_at_utc": f"{today}T00:00:00Z",
        "source_registry_json": str(REGISTRY_JSON.relative_to(ROOT)),
        "source_missing_csv": str(MISSING_CSV.relative_to(ROOT)),
        "history": history,
    }


def main() -> None:
    payload = build()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON.relative_to(ROOT)} ({len(payload['history'])} snapshots)")


if __name__ == "__main__":
    main()
