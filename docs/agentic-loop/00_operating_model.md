# 00 — Governed agentic loop operating model

## 1. Purpose

The agentic loop is a controlled repository workflow for `atlante_dei_concorsi`.

It is designed to help maintain, validate and progressively extend the methodological and data-modelling infrastructure of the atlas. It is not designed to make public allegations, automate legal conclusions or run unrestricted scraping.

## 2. Design principle

The loop follows a conservative state-machine pattern:

1. read the latest repository state;
2. read the linked issue or task instruction;
3. identify the smallest authorised next action;
4. perform only that action;
5. write persistent state;
6. write a human-readable execution log;
7. run validation;
8. stop, continue, or request human review.

The loop must prefer stopping over speculative action.

## 3. Repository persistence

The loop stores its own memory in the repository, not in chat history.

Machine-readable state files live in:

```text
reports/agentic-loop/
```

Human-readable execution logs live in:

```text
docs/executions/
```

This makes each run auditable and reviewable through ordinary Git history.

## 4. Execution modes

### Dry-run mode

Dry-run mode may:

- create or update loop state;
- create or update execution logs;
- inspect repository structure;
- run validators;
- report blockers.

Dry-run mode must not:

- collect new external documents;
- update real golden-dataset rows;
- infer committee-candidate relations;
- change substantive coding taxonomies.

### Controlled implementation mode

Controlled implementation mode may perform a single authorised repository update when an issue explicitly defines scope, files and done criteria.

### Substantive coding mode

Substantive coding mode is disabled by default. It requires explicit issue-level approval and must respect the pilot runbook, source registry, evidence rules and human-review gates.

## 5. Agent roles

The loop may be decomposed into specialised logical roles:

- State Initialiser: creates or updates machine-readable state.
- Issue Interpreter: extracts scope, constraints and done criteria from the issue.
- Methodology Guard: checks proposed action against repository policy and pilot rules.
- Source Gatekeeper: stops unauthorised domain or source expansion.
- Workspace Builder: prepares empty/synthetic folder and CSV structures when authorised.
- Evidence Coding Assistant: may code only evidence-backed fields and only in authorised mode.
- Uncertainty Auditor: marks ambiguity, low confidence and human-review requirements.
- Validation Runner: runs repository validators and records results.
- PR Reporter: prepares draft PR summaries and handoff notes.
- Stop/Continue Decider: selects the next action or stops.

In the current foundation phase, only the State Initialiser, Issue Interpreter, Methodology Guard, Validation Runner and Stop/Continue Decider are active.

## 6. Quality score

The loop may use a quality score for operational completeness, not for truth or legal assessment.

The score reflects whether the execution state is complete, validated and reviewable. It must not be interpreted as a confidence score on real-world allegations or conflicts.

## 7. Default stop bias

When a step is ambiguous, sensitive, source-expanding or reputationally relevant, the correct behaviour is to stop and request human review.
