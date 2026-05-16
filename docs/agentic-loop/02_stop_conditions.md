# 02 — Stop conditions

## 1. General rule

The loop must stop whenever continuing would require a substantive judgement, an unauthorised expansion of scope, or a change that cannot be mechanically validated.

Stopping is a successful governance outcome when it prevents speculative or unsafe repository changes.

## 2. Hard stop conditions

The loop must stop immediately if:

- the issue does not define a clear scope;
- the requested action conflicts with `AGENTS.md`;
- a new university/source domain is required but not approved;
- the action would collect or code real data while the loop is in dry-run mode;
- the action would infer a committee-candidate relation;
- the action would create or imply a legal conclusion;
- the action would use accusatory terminology;
- a validator fails and the cause is not a trivial formatting error;
- required repository files are missing;
- raw documents or snapshots would be committed contrary to policy;
- CI status is unknown after material changes.

## 3. Human-review stop conditions

The loop must request human review if:

- identity matching is ambiguous;
- documentary evidence is incomplete;
- source pages are multi-position or ambiguous;
- different documents conflict;
- relation evidence is weak, sensitive or reputationally relevant;
- the procedure is ongoing;
- the next action would modify schema semantics, codebook definitions or publication policy.

## 4. Domain-approval stop conditions

The loop must request domain approval before:

- adding a new university website;
- using a departmental listing not already approved;
- following third-party mirrors or unofficial copies;
- using search-engine snippets as evidence;
- introducing automated fetch/scrape behaviour.

## 5. Completion conditions

A dry-run loop is complete when:

- state file exists and validates;
- execution log exists;
- no substantive dataset change was made;
- methodology validator ran or its failure was recorded;
- golden-dataset validator ran or its failure was recorded;
- next action is either explicit or blocked.

A controlled implementation loop is complete when:

- all intended files are changed;
- validators pass;
- the PR explains scope and limits;
- no stop condition remains unresolved.
