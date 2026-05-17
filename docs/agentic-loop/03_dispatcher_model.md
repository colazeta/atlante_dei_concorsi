# 03 — Agentic dispatcher model

## 1. Purpose

The dispatcher is the GitHub-native coordination layer for governed agentic work.

The repository already supports controlled execution tasks, state files and execution logs. The remaining problem is operational continuity: long-running work still requires a human to repeatedly identify the next issue, paste prompts and ask the agent to continue.

The dispatcher solves that coordination problem without making the system uncontrolled.

## 2. Core principle

The dispatcher may only act on issues explicitly marked as ready for agent execution.

No label, no autonomous action.

## 3. Supported labels

The dispatcher recognises the following labels:

```text
agent-ready
agent-running
agent-review
agent-blocked
agent-done
agent-needs-human
```

Label meanings:

- `agent-ready`: the issue is approved for agent selection.
- `agent-running`: an agent is currently expected to work on the issue.
- `agent-review`: an output exists and needs human review.
- `agent-blocked`: the agent could not proceed and recorded a blocker.
- `agent-done`: completion evidence exists and the issue can be closed or archived.
- `agent-needs-human`: the next step requires explicit human input or judgement.

## 4. Current implementation scope

The dispatcher is deliberately conservative.

It can:

- find open issues labelled `agent-ready`;
- select one issue per run;
- write a machine-readable dispatcher state file;
- produce a Codex handoff prompt;
- optionally post a status comment in controlled mode;
- optionally move the selected issue from `agent-ready` to `agent-running` in controlled mode, but only when label mutation is explicitly requested.

It must not yet:

- execute Codex itself;
- fetch external sources;
- change substantive datasets;
- mark issues as `agent-done` automatically without explicit human-reviewed completion evidence.

## 5. State persistence

Dispatcher state is stored under:

```text
reports/agentic-dispatcher/
```

The current state file is:

```text
reports/agentic-dispatcher/dispatcher_state.json
```

This makes dispatcher runs auditable through Git history.

## 6. Selection logic

The dispatcher should:

1. query open issues labelled `agent-ready`;
2. ignore pull requests;
3. select a single issue;
4. prefer the oldest eligible issue unless a priority rule is later introduced;
5. write the selected issue number, title, labels and handoff prompt into dispatcher state.

## 7. Handoff prompt

The generated handoff prompt should instruct Codex/agent to:

- read the selected issue;
- follow `AGENTS.md`;
- create a branch;
- implement only the requested scope;
- preserve uncertainty and caveats;
- run validators;
- open a draft PR;
- report blockers instead of guessing.

## 8. Label mutation

Label mutation is opt-in.

Dry-run mode must never mutate labels.

Controlled mode may mutate labels only when the `mutate_labels` workflow input or `--mutate-labels` CLI flag is set.

The first supported mutation is intentionally narrow:

```text
agent-ready → agent-running
```

The dispatcher may create missing workflow labels if the GitHub token has permission. If label creation or mutation fails, the dispatcher records the blocker in state and must not silently proceed.

## 9. Stop conditions

The dispatcher must stop or remain idle when:

- no `agent-ready` issue exists;
- GitHub API access is unavailable;
- more context is required to safely select an issue;
- selected issue content conflicts with `AGENTS.md`;
- label mutation fails in controlled mode;
- a previous dispatcher state indicates unresolved human input.

## 10. Post-run evaluator extension

A conservative post-run evaluator is now available in:

```text
scripts/agentic_post_run_evaluator.py
```

It inspects issue-level completion signals and writes machine-readable output to:

```text
reports/agentic-dispatcher/post_run_evaluator_state.json
```

Current evaluator behaviour:

- reads issue labels and latest comment text;
- recommends `agent-review` when structured output markers are present;
- recommends `agent-blocked` when blocker language is present;
- may optionally apply `agent-running -> agent-review|agent-blocked`;
- never auto-applies `agent-done` and keeps human review mandatory.

## 11. Later extensions

Later PRs may add:

- detection of linked PRs;
- CI status monitoring;
- issue comment summaries after each run;
- safe completion detection before applying `agent-done`.

## 12. Scheduled autonomy profile

The repository now includes an hourly, conservative autonomy cadence:

1. **Dispatcher schedule** (`.github/workflows/agentic-dispatcher.yml`) runs at minute `17` each hour and defaults to controlled mode with comment posting and `agent-ready -> agent-running` mutation enabled.
2. **Continuation evaluator schedule** (`.github/workflows/agentic-continuation-evaluator.yml`) runs at minute `47` each hour and evaluates the currently selected issue from `reports/agentic-dispatcher/dispatcher_state.json` unless an explicit issue number is provided.
3. The evaluator may apply only `agent-running -> agent-review|agent-blocked`, preserving mandatory human review before any `agent-done` outcome.

This staggered schedule keeps the system governed: selection and continuation checks are automated, while substantive acceptance remains human-controlled.
