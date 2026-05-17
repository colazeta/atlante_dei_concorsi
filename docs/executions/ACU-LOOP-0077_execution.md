# ACU-LOOP-0077 — governed agentic-loop execution

## Summary

- Issue: #77
- Mode: `controlled_implementation`
- Status: `completed`
- Phase: `exception_based_review_gates`
- Human review required: `False`
- Updated at: `2026-05-17T14:05:00+00:00`

## Scope actually executed

Implemented exception-based review gates for autonomous continuation.

Changes include:

1. Added policy documentation for exception-based autonomous review behaviour.
2. Added a review gate decision schema with required output fields.
3. Added a decider script that returns one of `autonomous_allowed`, `continuation_needed`, `human_review_required`, or `blocked`.
4. Added `reports/review-gates/.gitkeep` to initialize report storage.
5. Updated this execution log and loop state artefact.

No golden dataset rows, raw documents, or snapshots were modified.

## Decision policy implemented

- Default: autonomous continuation.
- `low` confidence does not block by itself.
- `not_determinable` does not block by itself.
- `homepage_only` does not block by itself.
- `needs_human_review` is treated as human-attention metadata and remains non-blocking unless a policy breach exists.
- `blocking_status=blocking` is reserved for explicit policy exceptions only.

## Validation

- `methodology`: passed (command: `python3 scripts/validate_atlante_methodology.py`, return code: `0`)
- `golden_dataset`: passed (command: `python3 scripts/validate_golden_dataset.py`, return code: `0`, summary: `Result: PASSED (367 warning(s))`)
- `state_schema`: passed (command: `python3 scripts/validate_agentic_loop_state.py`, return code: `0`)

## Files touched

- `docs/agentic-loop/05_exception_based_review_policy.md`
- `schemas/agentic-loop/review_gate.schema.json`
- `scripts/review_gate_decider.py`
- `reports/review-gates/.gitkeep`
- `docs/executions/ACU-LOOP-0077_execution.md`
- `reports/agentic-loop/ACU-LOOP-0077_state.json`

## Next action

Integrate `scripts/review_gate_decider.py` into scheduled evaluator workflows so label transitions use exception-based non-blocking gates by default.
