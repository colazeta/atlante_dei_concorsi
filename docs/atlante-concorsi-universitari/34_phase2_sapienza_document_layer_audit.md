# 34 — Phase 2 Sapienza document-layer audit (micro-batch 1)

## Audit scope

Issue: #28 (first phase-2 Sapienza micro-batch).

Procedures audited:
- ACU-P2-0001
- ACU-P2-0002
- ACU-P2-0003

Files inspected only:
- `data/golden-dataset/atlante-concorsi-universitari/procedures/procedures.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/documents.csv`
- `docs/atlante-concorsi-universitari/33_phase2_id_mapping.md`

Constraints applied in this audit:
- no raw-document downloads;
- no external enrichment;
- no conflict/relationship inference;
- neutral documentary checks only.

---

## Procedure coverage

| Procedure ID | procedures.csv rows | University match vs mapping | Source URL match vs mapping | Procedure code/reference/title match vs mapping | Procedure type match vs mapping | Result |
|---|---:|---|---|---|---|---|
| ACU-P2-0001 | 1 | Yes (`Sapienza Università di Roma` ↔ `Sapienza`) | Yes (`.../234489`) | Yes (`2025RTDA1_1`) | Yes (`RTDA`) | OK |
| ACU-P2-0002 | 1 | Yes (`Sapienza Università di Roma` ↔ `Sapienza`) | Yes (`.../232874`) | Yes (`2025RTDA37_17`) | Yes (`RTDA`) | OK |
| ACU-P2-0003 | 1 | Yes (`Sapienza Università di Roma` ↔ `Sapienza`) | Yes (`.../235779`) | Yes (`RTDA n. 1/2025`) | Yes (`RTDA`) | OK |

Summary: each audited procedure has exactly one `procedures.csv` row and matches the phase-2 mapping note on university, URL, reference/title, and type.

---

## Document coverage

| Procedure ID | Document rows | document_type values present | Core types present | Additional visibility checks |
|---|---:|---|---|---|
| ACU-P2-0001 | 5 | `call_notice`, `committee_appointment`, `evaluation_criteria`, `acts_approval`, `other` | Yes (`call_notice`, `committee_appointment`, `evaluation_criteria`; `acts_approval` visible and present) | `admission_list`: not visible in current rows; `other` used for colloquio notice (taxonomy gap) |
| ACU-P2-0002 | 4 | `call_notice`, `committee_appointment`, `evaluation_criteria`, `acts_approval` | Yes (`call_notice`, `committee_appointment`, `evaluation_criteria`; `acts_approval` visible and present) | `admission_list`: not visible in current rows |
| ACU-P2-0003 | 7 | `call_notice`, `committee_appointment`, `evaluation_criteria` (x2), `admission_list`, `acts_approval`, `other` | Yes (all core types, plus visible `admission_list` and `acts_approval`) | Duplicate-like criteria stage represented by two distinct criteria-related files |

---

## Document row integrity

All rows in `documents.csv` for ACU-P2-0001..0003 were checked for mandatory documentary fields.

Result:
- `document_id`: populated for all rows;
- `procedure_id`: populated for all rows;
- `document_type`: populated for all rows;
- `title`: populated for all rows;
- `source_url`: populated for all rows;
- `retrieval_date`: populated for all rows (`2026-04-29`);
- `official_source_flag`: populated for all rows (`true`);
- `notes`: neutral documentary tone, non-accusatory.

No field-level integrity gaps found in scoped rows.

---

## CSV integrity findings

Checks performed on the two CSV files:
- consistent column counts per row (no extra trailing fields / no `row[None]` condition);
- no malformed quoting found by parser;
- no comma-shift symptoms from unquoted commas;
- no row-shape anomalies attributable to line-ending/whitespace breaks.

Result: no CSV structural integrity defects detected in the audited scope.

---

## Taxonomy issues (for future backlog)

1. `other` classification candidates that may warrant a dedicated taxonomy value:
   - ACU-P2-0001-DOC-05 (avviso convocazione colloquio)
   - ACU-P2-0003-DOC-07 (avviso colloquio pubblico / telematico)

2. Criteria-stage multiplicity:
   - ACU-P2-0003 has two `evaluation_criteria` rows (verbale preliminare + allegato criteri). This appears documentary-consistent and not an erroneous duplicate; retain as separate records.

3. Source-visibility limitations:
   - ACU-P2-0001 and ACU-P2-0002 currently show no `admission_list` row in dataset scope; this is treated as not visible in the available source chain, not as a defect.

---

## Corrections made

No corrections were required in `procedures.csv` or `documents.csv` for this micro-batch.

Only this audit note was added.

---

## Recommendation

- ACU-P2-0001..0003: **approved for next-layer coding** from a document-layer consistency perspective.
- Progression recommendation: **safe to proceed** to ACU-P2-0004..0005 document-layer coding, maintaining the same constraints and neutral documentary validation workflow.
