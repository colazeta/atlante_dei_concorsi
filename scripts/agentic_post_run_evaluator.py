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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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

    last_comment = comments[-1]["body"] if comments else ""
    has_summary = "summary" in last_comment.lower()
    has_testing = "testing" in last_comment.lower()
    has_blocker = any(k in last_comment.lower() for k in ["blocker", "blocked", "cannot proceed"]) 

    recommendation = "no_change"
    next_label = None
    rationale: list[str] = []

    if has_blocker:
        recommendation = "set_blocked"
        next_label = "agent-blocked"
        rationale.append("Latest comment contains blocker language.")
    elif has_summary and has_testing:
        recommendation = "set_review"
        next_label = "agent-review"
        rationale.append("Latest comment includes summary and testing sections.")
    else:
        rationale.append("No completion marker detected in latest issue comment.")

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
            "last_comment_has_summary": has_summary,
            "last_comment_has_testing": has_testing,
            "last_comment_has_blocker": has_blocker,
        },
        "recommendation": {
            "action": recommendation,
            "next_label": next_label,
            "rationale": rationale,
        },
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
    args = p.parse_args()

    if not args.repo:
        raise SystemExit("--repo or GITHUB_REPOSITORY is required")

    token = os.environ.get("GITHUB_TOKEN")
    state = evaluate(args.repo, args.issue_number, token)
    state["label_mutation"] = {"requested": args.apply, "status": "not_requested"}
    if args.apply and state["recommendation"]["next_label"] in {"agent-review", "agent-blocked"}:
        state["label_mutation"] = mutate_labels(args.repo, args.issue_number, "agent-running", state["recommendation"]["next_label"], token)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
