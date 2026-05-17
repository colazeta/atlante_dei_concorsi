#!/usr/bin/env python3
"""Post-run evaluator for governed agent output completion.

This evaluator is intentionally conservative: it does not infer substantive success.
It only checks for observable completion evidence and recommends safe next labels.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "reports" / "agentic-dispatcher" / "post_run_evaluator_state.json"
QUEUE_DIR = ROOT / "reports" / "codex-handoff-queue"
LOOP_STATE_DIR = ROOT / "reports" / "agentic-loop"
REQUIRED_RUN_LABEL = "agent-running"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def load_loop_state(issue_number: int) -> dict[str, Any] | None:
    path = LOOP_STATE_DIR / f"ACU-LOOP-{issue_number:04d}_state.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def build_continuation_prompt(
    issue_number: int,
    expected_quality_score: int,
    current_quality_score: int,
    delta: int,
    loop_state: dict[str, Any] | None,
) -> str:
    next_action = (loop_state or {}).get("next_action") or "Review the latest loop artefacts and continue from the documented next step."
    return (
        f"Issue #{issue_number} requires continuation before review.\n\n"
        f"- Expected quality score: {expected_quality_score}\n"
        f"- Current quality score: {current_quality_score}\n"
        f"- Delta: {delta}\n"
        f"- Loop status: {(loop_state or {}).get('status')}\n"
        f"- Loop mode: {(loop_state or {}).get('mode')}\n\n"
        "Continue the issue using governed workflow, preserve uncertainty markers and review notes, "
        "run required validators, and report blockers explicitly.\n\n"
        f"Documented next action: {next_action}"
    )


def maybe_build_continuation(issue_number: int, expected_quality_score: int, current_quality_score_override: int | None = None) -> dict[str, Any]:
    loop_state = load_loop_state(issue_number)
    if current_quality_score_override is None and not loop_state:
        return {"continuation_needed": False, "reason": "No local loop state found for this issue."}
    current_score = current_quality_score_override if current_quality_score_override is not None else loop_state.get("quality_score")
    if not isinstance(current_score, int):
        return {"continuation_needed": False, "reason": "Loop state has no integer quality_score."}
    delta = expected_quality_score - current_score
    if delta <= 0:
        return {
            "continuation_needed": False,
            "expected_quality_score": expected_quality_score,
            "current_quality_score": current_score,
            "delta": delta,
            "reason": "Quality score meets or exceeds expected threshold.",
        }
    prompt = build_continuation_prompt(issue_number, expected_quality_score, current_score, delta, loop_state)
    continuation = {
        "issue_number": issue_number,
        "created_at_utc": utc_now(),
        "continuation_needed": True,
        "expected_quality_score": expected_quality_score,
        "current_quality_score": current_score,
        "delta": delta,
        "source_loop_state": f"reports/agentic-loop/ACU-LOOP-{issue_number:04d}_state.json" if loop_state else None,
        "continuation_prompt": prompt,
    }
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    queue_path = QUEUE_DIR / f"{issue_number}_continuation.json"
    queue_path.write_text(json.dumps(continuation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    continuation["queue_path"] = str(queue_path.relative_to(ROOT))
    return continuation


def gh_request(method: str, url: str, token: str | None, payload: dict[str, Any] | None = None) -> Any:
    data = None
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "atlante-agentic-post-run-evaluator",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, method=method, data=data, headers=headers)
    with urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8")
        return json.loads(text) if text else None


def evaluate(repo: str, issue_number: int, token: str | None) -> dict[str, Any]:
    issue = gh_request("GET", f"https://api.github.com/repos/{repo}/issues/{issue_number}", token)
    comments = gh_request("GET", issue["comments_url"], token) if issue.get("comments", 0) else []
    labels = [x.get("name") for x in issue.get("labels", []) if x.get("name")]
    issue_updated_at = issue.get("updated_at")
    last_comment_at = comments[-1].get("updated_at") if comments else None

    last_comment = comments[-1]["body"] if comments else ""
    has_summary = "summary" in last_comment.lower()
    has_testing = "testing" in last_comment.lower()
    has_blocker = any(k in last_comment.lower() for k in ["blocker", "blocked", "cannot proceed"]) 
    has_completion_signal = any(
        token in last_comment.lower()
        for token in ["status: completed", "status=`completed`", "status `completed`", "status completed"]
    )

    recommendation = "no_change"
    next_label = None
    rationale: list[str] = []
    warnings: list[str] = []
    stale_state = False

    if REQUIRED_RUN_LABEL not in labels:
        stale_state = True
        warnings.append("Issue does not have agent-running label; evaluator transition skipped.")

    issue_updated = parse_utc(issue_updated_at)
    last_comment_updated = parse_utc(last_comment_at)
    if issue_updated and last_comment_updated and issue_updated > last_comment_updated:
        stale_state = True
        warnings.append("Issue has newer activity after the latest comment; completion signal may be stale.")

    if stale_state:
        recommendation = "manual_review"
        rationale.append("Stale-state safeguards triggered; label transition requires human review.")
    elif has_blocker:
        recommendation = "set_blocked"
        next_label = "agent-blocked"
        rationale.append("Latest comment contains blocker language.")
    elif has_summary and has_testing and has_completion_signal:
        recommendation = "set_review"
        next_label = "agent-review"
        rationale.append("Latest comment includes summary/testing sections and an explicit completion signal.")
    else:
        rationale.append("No reliable completion marker detected in latest issue comment.")

    return {
        "evaluator_id": "ACU-POSTRUN-EVAL-0001",
        "status": "completed",
        "created_at_utc": utc_now(),
        "updated_at_utc": utc_now(),
        "repo": repo,
        "issue": {
            "number": issue_number,
            "title": issue.get("title"),
            "url": issue.get("html_url"),
            "labels": labels,
        },
        "signals": {
            "comment_count": len(comments),
            "issue_updated_at": issue_updated_at,
            "last_comment_updated_at": last_comment_at,
            "last_comment_has_summary": has_summary,
            "last_comment_has_testing": has_testing,
            "last_comment_has_blocker": has_blocker,
            "last_comment_has_completion_signal": has_completion_signal,
            "stale_state_detected": stale_state,
        },
        "recommendation": {
            "action": recommendation,
            "next_label": next_label,
            "rationale": rationale,
        },
        "warnings": warnings,
        "notes": [
            "Evaluator does not infer substantive correctness.",
            "Human review remains required before agent-done.",
        ],
    }


def mutate_labels(repo: str, issue_number: int, from_label: str, to_label: str, token: str | None) -> dict[str, Any]:
    if not token:
        return {"status": "skipped_no_token"}
    gh_request("POST", f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels", token, {"labels": [to_label]})
    encoded = quote(from_label, safe="")
    try:
        gh_request("DELETE", f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels/{encoded}", token)
    except HTTPError as exc:
        if exc.code != 404:
            raise
    return {"status": "completed", "added": [to_label], "removed": [from_label]}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    p.add_argument("--issue-number", type=int, required=True)
    p.add_argument("--apply", action="store_true", help="Apply recommended label transition from agent-running")
    p.add_argument("--expected-quality-score", type=int, default=99)
    p.add_argument("--current-quality-score", type=int, default=None, help="Optional override for regression testing.")
    args = p.parse_args()

    if not args.repo:
        raise SystemExit("--repo or GITHUB_REPOSITORY is required")

    token = os.environ.get("GITHUB_TOKEN")
    state = evaluate(args.repo, args.issue_number, token)
    continuation = maybe_build_continuation(args.issue_number, args.expected_quality_score, args.current_quality_score)
    state["continuation_needed"] = bool(continuation.get("continuation_needed"))
    state["continuation"] = continuation
    if state["continuation_needed"]:
        state["recommendation"] = {
            "action": "continuation_required",
            "next_label": None,
            "rationale": [
                f"Expected quality score {continuation.get('expected_quality_score')} is above current {continuation.get('current_quality_score')}.",
                "Continuation prompt generated; do not advance to agent-review yet.",
            ],
        }
    state["label_mutation"] = {"requested": args.apply, "status": "not_requested"}
    if state["continuation_needed"] and args.apply:
        state["label_mutation"] = {"requested": True, "status": "skipped_continuation_needed"}
    elif args.apply and state["recommendation"]["next_label"] in {"agent-review", "agent-blocked"}:
        state["label_mutation"] = mutate_labels(args.repo, args.issue_number, "agent-running", state["recommendation"]["next_label"], token)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
