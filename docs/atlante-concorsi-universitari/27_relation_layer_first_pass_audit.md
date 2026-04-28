# 27 — Relation-layer first-pass audit (`committee_candidate_relations.csv`)

## Audit scope

Audited files only:
- `data/golden-dataset/atlante-concorsi-universitari/procedures/committee_candidate_relations.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/committee_members.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/candidates.csv`

No external browsing or enrichment was used.

---

## 1) Coverage table

| Procedure | Relation-review rows present | Expected status | Result |
|---|---:|---|---|
| ACU-PILOT-0001 | 0 | No relation row (candidate placeholder) | Pass |
| ACU-PILOT-0002 | 0 | No relation row (candidate placeholder) | Pass |
| ACU-PILOT-0003 | 0 | No relation row (candidate placeholder) | Pass |
| ACU-PILOT-0004 | 0 | No relation row (candidate placeholder) | Pass |
| ACU-PILOT-0005 | 0 | No relation row (candidate placeholder) | Pass |
| ACU-PILOT-0006 | 1 | One procedure-level first-pass review row | Pass |
| ACU-PILOT-0007 | 1 | One procedure-level first-pass review row | Pass |
| ACU-PILOT-0008 | 1 | One procedure-level first-pass review row | Pass |
| ACU-PILOT-0009 | 1 | One procedure-level first-pass review row | Pass |
| ACU-PILOT-0010 | 1 | One procedure-level first-pass review row | Pass |

---

## 2) Skipped-procedure rationale

Procedures without relation rows (`ACU-PILOT-0001..0005`) currently have candidate rows coded as placeholders (`person_name=not_determinable`, `candidate_status=not_determinable`), so relation coding is not eligible at this first-pass stage.

---

## 3) Enum / field consistency check (rows for 0006..0010)

All five first-pass relation rows were checked for consistency:
- `relation_type=no_documented_relation_in_registered_sources`;
- `confidence_level=low`;
- `human_review_required=true`;
- `human_review_status=pending`;
- `publication_status=internal_only`;
- notes explicitly state registered-source-only review and no external enrichment.

Audit result: **Pass (all 5 rows consistent)**.

---

## 4) Pairwise overcoding check

No pairwise committee-candidate rows were found that merely state absence of evidence.

Audit result: **Pass**.

---

## 5) Candidate determinability check (eligibility for 0006..0010)

| Procedure | Candidate rows | Determinable candidate rows | Eligible for procedure-level relation-review row |
|---|---:|---:|---|
| ACU-PILOT-0006 | 1 | 1 | Yes |
| ACU-PILOT-0007 | 7 | 7 | Yes |
| ACU-PILOT-0008 | 1 | 1 | Yes |
| ACU-PILOT-0009 | 5 | 5 | Yes |
| ACU-PILOT-0010 | 4 | 4 | Yes |

---

## 6) Recommendation

Current first-pass relation layer is complete for the intended scope:
- relation-review rows exist for all eligible procedures (`0006..0010`);
- non-eligible procedures with placeholder candidates (`0001..0005`) remain correctly uncoded at relation layer;
- conservative semantics and review flags are consistently applied.

Recommendation: **safe to keep this first-pass layer as baseline and proceed only with evidence-backed updates in subsequent passes.**
