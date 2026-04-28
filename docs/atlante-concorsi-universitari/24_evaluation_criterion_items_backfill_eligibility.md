# 24 — Evaluation criterion items backfill eligibility audit

## Scope

Audited files:
- `data/golden-dataset/atlante-concorsi-universitari/procedures/evaluation_criteria.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/evaluation_criterion_items.csv`

Pilot procedures audited: 10 (`ACU-PILOT-0001` to `ACU-PILOT-0010`).

## Classification rules applied

- `not_determinable_no_backfill`: default for `criteria_narrowness_class=not_determinable` unless item coverage is already sufficient.
- `eligible_for_backfill`: non-`not_determinable` class with zero item rows.
- `complete`: item rows support aggregate checks (main/subcriteria counts, weight/threshold flags, linked-criteria support, discretionary support when share > 0).
- `needs_review`: item rows exist but do not support aggregate checks.

## Procedure-level eligibility table

| Procedure | Aggregate criteria class | Item row count | Eligibility status | Reason | Recommended next action |
|---|---|---:|---|---|---|
| ACU-PILOT-0001 | very_high | 29 | complete | Item rows support aggregate checks: main=12, sub=10, weights present, threshold present, linked=2, discretionary support present. | Keep current rows; use as reference pattern. |
| ACU-PILOT-0002 | high | 20 | complete | Item rows support aggregate checks: main=11, sub=0, weights present, threshold present, linked=2, discretionary support present. | Keep current rows; use as reference pattern. |
| ACU-PILOT-0003 | not_determinable | 0 | not_determinable_no_backfill | Aggregate class is `not_determinable` and no sufficient item decomposition is available. | Do not backfill now; retain conservative no-backfill stance. |
| ACU-PILOT-0004 | not_determinable | 0 | not_determinable_no_backfill | Aggregate class is `not_determinable` and no sufficient item decomposition is available. | Do not backfill now; retain conservative no-backfill stance. |
| ACU-PILOT-0005 | not_determinable | 0 | not_determinable_no_backfill | Aggregate class is `not_determinable` and no sufficient item decomposition is available. | Do not backfill now; retain conservative no-backfill stance. |
| ACU-PILOT-0006 | high | 15 | complete | Item rows support aggregate checks: main=13, sub=0, weights present, no threshold rows, linked=2, discretionary support present. | Keep current rows; use as reference pattern. |
| ACU-PILOT-0007 | not_determinable | 0 | not_determinable_no_backfill | Aggregate class is `not_determinable` and no sufficient item decomposition is available. | Do not backfill now; retain conservative no-backfill stance. |
| ACU-PILOT-0008 | not_determinable | 0 | not_determinable_no_backfill | Aggregate class is `not_determinable` and no sufficient item decomposition is available. | Do not backfill now; retain conservative no-backfill stance. |
| ACU-PILOT-0009 | not_determinable | 0 | not_determinable_no_backfill | Aggregate class is `not_determinable` and no sufficient item decomposition is available. | Do not backfill now; retain conservative no-backfill stance. |
| ACU-PILOT-0010 | not_determinable | 0 | not_determinable_no_backfill | Aggregate class is `not_determinable` and no sufficient item decomposition is available. | Do not backfill now; retain conservative no-backfill stance. |

## Summary

- **complete**: ACU-PILOT-0001, ACU-PILOT-0002, ACU-PILOT-0006.
- **eligible_for_backfill**: none in current pilot state.
- **not_determinable_no_backfill**: ACU-PILOT-0003, ACU-PILOT-0004, ACU-PILOT-0005, ACU-PILOT-0007, ACU-PILOT-0008, ACU-PILOT-0009, ACU-PILOT-0010.
- **needs_review**: none.
