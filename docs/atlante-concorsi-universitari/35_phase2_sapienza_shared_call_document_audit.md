# 35 — Phase 2 Sapienza shared-call document audit (micro-batch 2)

## Audit scope

Issue: #31.

Procedures audited:
- ACU-P2-0004
- ACU-P2-0005

Focus constraints applied:
- shared-call attribution only;
- whether ACU-P2-0004 is defensibly coded as one constrained sub-procedure;
- whether ACU-P2-0005 is correctly kept narrow/partial;
- absence of over-attribution;
- CSV structural integrity;
- document taxonomy use;
- no substantive coding modifications unless a clear documentary/CSV consistency error is found.

Files inspected:
- `docs/atlante-concorsi-universitari/32_phase2_candidate_procedure_list.md`
- `docs/atlante-concorsi-universitari/33_phase2_id_mapping.md`
- `docs/atlante-concorsi-universitari/34_phase2_sapienza_document_layer_audit.md`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/procedures.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/documents.csv`

---

## Findings

## 1) Shared-call attribution checks

### ACU-P2-0004 (`2025RTDA01/146 Polo Rieti`)

- Mapping and candidate notes consistently mark ACU-P2-0004 as `shared_call_chain` with an explicit caution to preserve sub-procedure boundaries.
- The candidate-list description indicates a two-position/shared context with stage visibility that is still attributable to one selected sub-procedure (call, commission, preliminary minutes by SSD, interview notices, acts approval).

Audit conclusion:
- **Defensible as one constrained sub-procedure**, provided that all downstream rows remain tied only to the selected ACU-P2-0004 slice and do not absorb documents from the sibling position.

### ACU-P2-0005 (`2025PAR001`)

- Mapping and candidate notes consistently flag this as a shared 14-position call requiring strict isolation of a clearly separable sub-procedure.
- Suitability is medium and explicitly conditioned by narrow segmentation.

Audit conclusion:
- **Correctly kept narrow/partial at this stage**; no evidence in current CSVs of broad multi-position ingestion under ACU-P2-0005.

---

## 2) Absence of over-attribution

Current dataset state for this micro-batch:
- `procedures.csv`: no row yet for ACU-P2-0004 or ACU-P2-0005.
- `documents.csv`: no document rows yet for ACU-P2-0004 or ACU-P2-0005.

Interpretation:
- There is currently **no material over-attribution risk realized in CSV content**, because coding rows for these two IDs have not yet been populated.
- Risk remains prospective and should be controlled during next-layer coding by keeping one sub-procedure per ACU-P2 ID.

---

## 3) CSV integrity

Checks on scoped CSVs found:
- valid parse with stable column shape;
- no malformed quoting or comma-shift anomalies affecting scoped inspection;
- no row-level documentary inconsistencies for ACU-P2-0004/0005 because no rows exist yet.

Result:
- **CSV integrity OK** for this audit scope.

---

## 4) Document taxonomy use

Given absence of `documents.csv` rows for ACU-P2-0004/0005, no direct misclassification is present yet.

Forward taxonomy guardrails (for next-layer coding):
- use `call_notice`, `committee_appointment`, `evaluation_criteria`, `admission_list`, `acts_approval` only when the document clearly belongs to the isolated sub-procedure;
- avoid assigning shared/global call artifacts to ACU-P2-0004 or ACU-P2-0005 unless they are explicitly applicable to the selected sub-procedure;
- keep `other` limited and justified only when taxonomy coverage is genuinely missing.

---

## Corrections made

- No corrections required in `procedures.csv` or `documents.csv`.
- No substantive coding changes made.
- Only this audit note was added.

---

## Validation results

Commands requested in issue workflow were executed after this audit note update.

- `python3 scripts/hash_golden_documents.py` → pass
- `python3 scripts/validate_atlante_methodology.py` → pass
- `python3 scripts/validate_golden_dataset.py` → pass
- `git diff --check` → pass
- `git status --short` → clean aside from expected audit-note addition before commit

---

## Approval decision for next-layer coding

- **ACU-P2-0004: approved for next-layer coding**, with strict one-sub-procedure segmentation and explicit shared-call boundary control.
- **ACU-P2-0005: approved for next-layer coding**, but only as a narrow/partial isolated slice of the shared 14-position call; no broad chain import.

Overall progression recommendation:
- **Proceed**, maintaining anti-over-attribution controls and conservative taxonomy assignment at document row level.
