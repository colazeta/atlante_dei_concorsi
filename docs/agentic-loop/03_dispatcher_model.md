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

## 4. First implementation scope

The first dispatcher implementation is deliberately conservative.

It can:

- find open issues labelled `agent-ready`;
- select one issue per run;
- write a machine-readable dispatcher state file;
- produce a Codex handoff prompt;
- optionally post a status comment in controlled mode.

It must not yet:

- mutate labels automatically;
- execute Codex itself;
- fetch external sources;
- change substantive datasets;
- mark issues as done without completion evidence.

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

## 8. Stop conditions

The dispatcher must stop or remain idle when:

- no `agent-ready` issue exists;
- GitHub API access is unavailable;
- more context is required to safely select an issue;
- selected issue content conflicts with `AGENTS.md`;
- a previous dispatcher state indicates unresolved human input.

## 9. Later extensions

After the dry-run dispatcher is validated, later PRs may add:

- safe label mutation;
- scheduled execution;
- detection of linked PRs;
- CI status monitoring;
- automatic transition from `agent-running` to `agent-review` or `agent-blocked`;
- issue comment summaries after each run.
