# 04 — Post-run evaluator model

## Purpose

The post-run evaluator determines whether open `agent-running` issues can safely move to review, should be marked blocked, or require continuation.

## Machine-readable classification

Each evaluated issue includes `recommendation.action` with one of:

- `set_review`
- `set_blocked`
- `continuation_needed`
- `manual_review`
- `no_change`

`continuation_needed` is mandatory when work is incomplete but the next step is mechanically derivable.

## Scope of evaluation

The evaluator scans **all open issues** labeled `agent-running` by default. It may also evaluate a single explicit issue via `--issue-number`.

It must not rely only on `reports/agentic-dispatcher/dispatcher_state.json`.

## Continuation queue

When `continuation_needed=true`, the evaluator writes:

- `reports/codex-handoff-queue/{issue_number}_continuation.json`

Queue items include:

- expected and current quality score
- delta
- source loop state reference
- continuation prompt

## Regression guard for issue #61

If expected universe is 99 and current registry rows are 80 (delta 19), classification must be `continuation_needed` and queue item generation is required. The evaluator must not classify this as `agent-review` only because `Summary` and `Testing` markers are present.
