#!/usr/bin/env python3
"""Governed issue dispatcher for Atlante dei Concorsi.

The dispatcher does not execute Codex directly. It selects an explicitly
approved issue and writes a machine-readable state plus a handoff prompt.

Current implementation scope:
- dry-run selection of one issue labelled agent-ready;
- optional controlled issue comment;
- optional safe label mutation from agent-ready to agent-running;
- no dataset changes;
- no external content collection.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_DIR = ROOT / "reports" / "agentic-dispatcher"
ALLOWED_MODES = {"dry_run", "controlled"}
REQUIRED_LABELS = {
    "agent-ready": "0E8A16",
    "agent-running": "FBCA04",
    "agent-review": "1D76DB",
    "agent-blocked": "D73A4A",
    "agent-done": "5319E7",
    "agent-needs-human": "BFDADC",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def github_request(method: str, url: str, token: str | None, payload: dict[str, Any] | None = None) -> Any:
    data = None
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "atlante-agentic-dispatcher",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(url, data=data, headers=headers, method=method)
    with urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8")
        return json.loads(text) if text else None


def list_ready_issues(repo: str, label: str, token: str | None) -> list[dict[str, Any]]:
    params = urlencode({"state": "open", "labels": label, "per_page": 50, "sort": "created", "direction": "asc"})
    url = f"https://api.github.com/repos/{repo}/issues?{params}"
    issues = github_request("GET", url, token)
    result: list[dict[str, Any]] = []
    for issue in issues:
        if "pull_request" in issue:
            continue
        result.append(issue)
    return result


def labels_of(issue: dict[str, Any]) -> list[str]:
    return [label.get("name", "") for label in issue.get("labels", []) if label.get("name")]


def ensure_label(repo: str, label: str, token: str | None) -> str:
    if not token:
        return "skipped_no_token"
    encoded = quote(label, safe="")
    get_url = f"https://api.github.com/repos/{repo}/labels/{encoded}"
    try:
        github_request("GET", get_url, token)
        return "exists"
    except HTTPError as exc:
        if exc.code != 404:
            raise
    create_url = f"https://api.github.com/repos/{repo}/labels"
    github_request("POST", create_url, token, {"name": label, "color": REQUIRED_LABELS.get(label, "EDEDED")})
    return "created"


def add_issue_labels(repo: str, issue_number: int, labels: list[str], token: str | None) -> None:
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required for label mutation")
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    github_request("POST", url, token, {"labels": labels})


def remove_issue_label(repo: str, issue_number: int, label: str, token: str | None) -> None:
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required for label mutation")
    encoded = quote(label, safe="")
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels/{encoded}"
    try:
        github_request("DELETE", url, token)
    except HTTPError as exc:
        if exc.code != 404:
            raise


def build_handoff_prompt(repo: str, issue: dict[str, Any]) -> str:
    number = issue["number"]
    title = issue["title"]
    return f"""Execute GitHub issue #{number} in `{repo}`: {title}

Operational instructions:

1. Read the full issue body and all comments before editing files.
2. Follow `AGENTS.md` and all repository governance rules.
3. Create a dedicated branch from `main`.
4. Implement only the scope requested by the issue.
5. Preserve uncertainty, caveats, source references and review notes.
6. Do not modify the golden dataset unless the issue explicitly authorises it.
7. Do not commit raw documents or snapshots unless policy explicitly allows it.
8. Run the relevant validators:
   - `python3 scripts/validate_atlante_methodology.py`
   - `python3 scripts/validate_golden_dataset.py`
   - `python3 scripts/validate_agentic_loop_state.py`
9. Open a draft PR when done.
10. In the PR body, report scope, files changed, validation results, blockers and next action.
11. If blocked, do not guess. Comment on the issue with the blocker and stop.
"""


def write_state(state: dict[str, Any], report_dir: Path) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "dispatcher_state.json"
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def post_issue_comment(repo: str, issue_number: int, token: str | None, body: str) -> None:
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required for controlled comments")
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    github_request("POST", url, token, {"body": body})


def mutate_selected_issue_labels(repo: str, issue_number: int, eligible_label: str, token: str | None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "requested": True,
        "added": [],
        "removed": [],
        "ensured_labels": {},
        "status": "not_started",
    }
    for label in REQUIRED_LABELS:
        result["ensured_labels"][label] = ensure_label(repo, label, token)
    add_issue_labels(repo, issue_number, ["agent-running"], token)
    result["added"].append("agent-running")
    remove_issue_label(repo, issue_number, eligible_label, token)
    result["removed"].append(eligible_label)
    result["status"] = "completed"
    return result


def build_state(
    repo: str,
    mode: str,
    label: str,
    report_dir: Path,
    token: str | None,
    mutate_labels: bool,
) -> dict[str, Any]:
    now = utc_now()
    blocking_issues: list[str] = []
    selected_issue: dict[str, Any] | None = None
    handoff_prompt: str | None = None
    candidate_count = 0
    label_mutation: dict[str, Any] = {"requested": mutate_labels, "status": "not_requested", "added": [], "removed": [], "ensured_labels": {}}

    try:
        candidates = list_ready_issues(repo, label, token)
        candidate_count = len(candidates)
    except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
        candidates = []
        blocking_issues.append(f"Could not query GitHub issues: {exc}")

    if candidates:
        issue = candidates[0]
        selected_issue = {
            "number": issue["number"],
            "title": issue["title"],
            "url": issue["html_url"],
            "labels": labels_of(issue),
        }
        handoff_prompt = build_handoff_prompt(repo, issue)

    if mutate_labels and mode != "controlled":
        blocking_issues.append("Label mutation is allowed only in controlled mode.")
    elif mutate_labels and selected_issue and not blocking_issues:
        try:
            label_mutation = mutate_selected_issue_labels(repo, int(selected_issue["number"]), label, token)
        except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
            label_mutation["status"] = "failed"
            blocking_issues.append(f"Could not mutate issue labels: {exc}")

    if blocking_issues:
        status = "blocked"
        next_action = "Fix dispatcher access, permissions or configuration, then re-run."
    elif not selected_issue:
        status = "idle"
        next_action = f"No open issue with label `{label}` found. Add `{label}` to an approved issue."
    else:
        status = "selected"
        if mutate_labels:
            next_action = "Issue moved to agent-running. Start Codex/agent execution using the generated handoff prompt."
        else:
            next_action = "Use the generated handoff prompt to start Codex/agent execution."

    state = {
        "dispatcher_id": "ACU-DISPATCHER-0001",
        "mode": mode,
        "status": status,
        "created_at_utc": now,
        "updated_at_utc": now,
        "eligible_label": label,
        "selected_issue": selected_issue,
        "handoff_prompt": handoff_prompt,
        "blocking_issues": blocking_issues,
        "next_action": next_action,
        "candidate_count": candidate_count,
        "label_mutation": label_mutation,
        "notes": [
            "Dispatcher does not execute Codex directly in this phase.",
            "Dispatcher mutates labels only when explicitly requested in controlled mode.",
            "Dispatcher must only select issues explicitly labelled agent-ready.",
        ],
    }
    write_state(state, report_dir)
    return state


def maybe_comment(repo: str, state: dict[str, Any], token: str | None) -> None:
    selected = state.get("selected_issue")
    if not selected:
        return
    issue_number = int(selected["number"])
    mutation = state.get("label_mutation", {})
    mutation_text = "not requested"
    if mutation.get("requested"):
        mutation_text = f"status={mutation.get('status')}; added={mutation.get('added')}; removed={mutation.get('removed')}"
    body = f"""## Agentic dispatcher handoff

The dispatcher selected this issue because it is labelled `{state['eligible_label']}`.

Current dispatcher mode: `{state['mode']}`

Label mutation: `{mutation_text}`

Next action:

```text
{state['next_action']}
```

Codex/agent handoff prompt:

```text
{state['handoff_prompt']}
```

No dataset files were changed by the dispatcher.
"""
    post_issue_comment(repo, issue_number, token, body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Select the next governed agent-ready issue.")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--mode", choices=sorted(ALLOWED_MODES), default="dry_run")
    parser.add_argument("--label", default="agent-ready")
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument("--comment", action="store_true", help="In controlled mode, post handoff comment to selected issue")
    parser.add_argument("--mutate-labels", action="store_true", help="In controlled mode, move selected issue from agent-ready to agent-running")
    args = parser.parse_args()

    if not args.repo:
        print("ERROR: --repo or GITHUB_REPOSITORY is required")
        return 1

    token = os.environ.get("GITHUB_TOKEN")
    state = build_state(args.repo, args.mode, args.label, args.report_dir, token, args.mutate_labels)

    if args.comment and args.mode == "controlled" and state["status"] == "selected":
        try:
            maybe_comment(args.repo, state, token)
        except Exception as exc:  # noqa: BLE001 - dispatcher should record controlled-comment failures clearly
            state["blocking_issues"].append(f"Could not post dispatcher comment: {exc}")
            state["status"] = "blocked"
            state["next_action"] = "Fix comment permissions or run without --comment."
            write_state(state, args.report_dir)

    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0 if state["status"] in {"idle", "selected", "blocked"} else 1


if __name__ == "__main__":
    sys.exit(main())
