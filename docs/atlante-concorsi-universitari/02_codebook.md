# 02 — Codebook

## Coding levels
- **L1 Documentary fact**: copied or normalized from a source document.
- **L2 Derived descriptive indicator**: deterministic transformation of L1 fields.
- **L3 Potential review signal**: generated from L2 thresholds, never conclusive.

## Missingness and uncertainty
Use controlled values:
- `not_available`: source exists but field not present.
- `not_determinable`: public documentation insufficient.
- `unknown`: temporary placeholder pending coding.

## Confidence levels
- `high`: explicit in official source.
- `medium`: explicit in a public source but partial ambiguity.
- `low`: inferred from public text with substantial uncertainty.

## Human review flags
Use:
- `human_review_required` (boolean)
- `human_review_status`: `pending`, `reviewed`, `rejected`, `confirmed_as_documented_relation`

## Explainability rule
Every score field must have a decomposition in raw components and documented formula references in module docs.
