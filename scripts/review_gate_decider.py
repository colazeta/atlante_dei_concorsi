#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BLOCKING_FLAGS = [
    "policy_breach",
    "unapproved_domain",
    "validator_failure",
    "raw_document_policy_breach",
    "relation_inference_outside_scope",
    "legal_or_reputational_conclusion",
    "task_outside_scope",
]


def decide(payload: dict[str, Any]) -> dict[str, Any]:
    issue_number = payload.get("issue_number")
    confidence_level = str(payload.get("confidence_level", "not_determinable"))
    verification_status = str(payload.get("verification_status", "not_determinable"))
    needs_human_review = bool(payload.get("needs_human_review", False))
    incomplete_coverage = bool(payload.get("incomplete_coverage", False))

    blocking_flag = None
    for flag in BLOCKING_FLAGS:
        if bool(payload.get(flag, False)):
            blocking_flag = flag
            break

    if blocking_flag:
        decision = "blocked"
        blocking_status = "blocking"
        requires_human_attention = True
        review_reason = f"Blocking policy exception detected: {blocking_flag}."
    elif incomplete_coverage:
        decision = "continuation_needed"
        blocking_status = "non_blocking"
        requires_human_attention = needs_human_review
        review_reason = "Coverage is incomplete but continuation is mechanically derivable."
    elif needs_human_review:
        decision = "human_review_required"
        blocking_status = "non_blocking"
        requires_human_attention = True
        review_reason = "Human attention requested as metadata; no policy breach detected."
    else:
        decision = "autonomous_allowed"
        blocking_status = "non_blocking"
        requires_human_attention = confidence_level in {"low", "not_determinable"} or verification_status in {
            "homepage_only",
            "not_determinable",
            "missing_recruitment_url",
        }
        review_reason = "Autonomous continuation allowed under exception-based gates."

    return {
        "issue_number": issue_number,
        "decision": decision,
        "confidence_level": confidence_level,
        "verification_status": verification_status,
        "requires_human_attention": requires_human_attention,
        "review_reason": review_reason,
        "blocking_status": blocking_status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Decide exception-based review gate outcome.")
    parser.add_argument("--input", required=True, help="Path to JSON input signals.")
    parser.add_argument("--output", required=False, help="Optional output JSON path.")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = decide(payload)
    serialized = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
