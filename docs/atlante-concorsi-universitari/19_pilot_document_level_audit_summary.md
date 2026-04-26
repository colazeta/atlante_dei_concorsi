# 19 — Pilot document-level audit summary (synthetic-safe)

Date: 2026-04-26
Scope:
- `procedures.csv`
- `documents.csv`

## Coverage summary

- Procedures expected: 10 (`ACU-PILOT-0001` ... `ACU-PILOT-0010`)
- Procedures present: 10/10
- Required document types checked per procedure:
  - `call_notice`
  - `committee_appointment`
  - `evaluation_criteria`
  - `acts_approval`
- Result: all 10 procedures contain all required document types.

## Document distribution by procedure

| procedure_id | docs | document types (set) |
|---|---:|---|
| ACU-PILOT-0001 | 5 | acts_approval, call_notice, committee_appointment, evaluation_criteria |
| ACU-PILOT-0002 | 5 | acts_approval, call_notice, committee_appointment, evaluation_criteria |
| ACU-PILOT-0003 | 5 | acts_approval, call_notice, committee_appointment, evaluation_criteria |
| ACU-PILOT-0004 | 5 | acts_approval, call_notice, committee_appointment, evaluation_criteria |
| ACU-PILOT-0005 | 5 | acts_approval, call_notice, committee_appointment, evaluation_criteria |
| ACU-PILOT-0006 | 7 | acts_approval, call_notice, committee_appointment, evaluation_criteria, other |
| ACU-PILOT-0007 | 7 | acts_approval, admission_list, call_notice, committee_appointment, evaluation_criteria, other |
| ACU-PILOT-0008 | 6 | acts_approval, call_notice, committee_appointment, evaluation_criteria, other |
| ACU-PILOT-0009 | 7 | acts_approval, admission_list, call_notice, committee_appointment, evaluation_criteria, other |
| ACU-PILOT-0010 | 7 | acts_approval, admission_list, call_notice, committee_appointment, evaluation_criteria, other |

## Metadata observations

- `deadline_date` format is consistent (`YYYY-MM-DD`) across the 10 procedures.
- `publication_date` is sometimes blank in document rows; notes generally explain when publication date is not clearly shown.
- `source_url` is populated for all procedure and document rows.

## Recurring taxonomy observations

`document_type=other` recurs for:
- committee kit documents,
- public discussion notices,
- evaluation judgments.

These are methodological granularity needs for potential future taxonomy refinement; no taxonomy changes were applied.

## Shared-document pattern observations

Shared official-source structures are present across related procedures (e.g., shared Unical source pages and support documents), consistent with multi-position calls.

## Recommendation

Proceed to the next coding layer (`profile_requirements` and `evaluation_criteria`) while preserving current conservative document-level coding rules.
