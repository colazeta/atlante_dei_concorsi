# 18 — Pilot runbook (first real 10-procedure manual pilot)

## 1) Pilot objective
The objective is operational validation of the methodology:
- test whether documentation, CSV templates, schemas, and QA workflow are usable in practice;
- test coding consistency and evidence traceability.

This pilot does **not** aim to:
- publish findings;
- identify wrongdoing;
- produce legal conclusions;
- produce public risk scoring outputs.

## 2) Pilot scope
- 2 universities;
- 5 procedures per university;
- 10 procedures total;
- manual collection only;
- internal use only;
- no public-facing publication;
- no legal conclusions;
- no automated scraping.

## 3) University selection
Select two placeholders (e.g., `university_a`, `university_b`) with complementary characteristics:
- one relatively easy source structure;
- one more difficult or structurally different source;
- different website structures if possible;
- preference for accessible archives and multiple document types.

## 4) Procedure selection
For each university, select 5 procedures:
- preferably recently concluded;
- include different role types where available;
- avoid ongoing procedures for first pilot unless explicitly marked ongoing;
- avoid procedures already known for controversy;
- prioritise procedures with multiple available documents.

## 5) Pre-coding setup
For each selected procedure:
1. Assign `procedure_id` using internal convention.
2. Choose `university_slug` (placeholder slug style, e.g. `university_a`).
3. Initialize folders:

```bash
python3 scripts/init_golden_procedure.py \
  --university-slug university_a \
  --procedure-id ACU-PILOT-0001
```

4. Save raw documents under:
   `data/golden-dataset/atlante-concorsi-universitari/raw_documents/{university_slug}/{procedure_id}/`
5. Save snapshots under:
   `.../snapshots/{university_slug}/{procedure_id}/`
6. Save review notes under:
   `.../review_notes/{university_slug}/{procedure_id}/`
7. Record metrics in:
   `.../pilot_metrics/pilot_batch_001_metrics.csv`

## 6) Manual collection workflow (sequence)
1. Open official source page manually.
2. Save source URL.
3. Save source-page snapshot (HTML/PDF list/screenshot/text note) if possible.
4. Identify the target procedure and anchors (code, role, department, dates).
5. Download/save official documents.
6. Preserve original names where useful.
7. Prefix document files with ordering numbers (`01_`, `02_`, ...).
8. Never overwrite later versions; store separately (`v2`, `v3`).
9. Record retrieval date.
10. Record source URL in `procedures/documents.csv`.

## 7) Coding workflow
Populate files in this order:
1. `procedures.csv`
2. `documents.csv`
3. `profile_requirements.csv`
4. `evaluation_criteria.csv`
5. `committee_members.csv`
6. `candidates.csv`
7. `committee_candidate_relations.csv`
8. `pilot_batch_001_metrics.csv`

## 8) Evidence rules
- Every extracted field must be traceable to a source document or source URL.
- Every profile-specificity feature must include supporting excerpt(s).
- Every criteria-narrowness feature must include supporting excerpt(s).
- Every committee-candidate relation must include an evidence source.
- Absence of evidence must **not** be treated as evidence of absence unless search path is documented.

## 9) Uncertainty rules
Use `not_determinable` when:
- evidence is missing/incomplete;
- identity matching is uncertain;
- required details are not publicly available.

Use `confidence_level=low` when textual evidence exists but remains ambiguous.

Set `human_review_required=true` when:
- key fields are ambiguous;
- relation evidence is weak or sensitive;
- conflicting documents exist.

Keep relation `human_review_status=pending` when reviewer adjudication is needed.

Do **not** code a relation when no documentary evidence exists and no documented search path is available.

## 10) Prohibited actions
- Publishing pilot results.
- Using accusatory language.
- Adding legal conclusions.
- Creating a `conflict_of_interest_confirmed` field.
- Inferring relationships from weak name similarity.
- Treating coauthorship as automatic conflict.
- Treating same affiliation as automatic conflict.
- Scraping large volumes of data.
- Committing raw documents when repository policy excludes them.

## 11) Hashing and validation
Run after each pilot batch update:

```bash
python3 scripts/hash_golden_documents.py
python3 scripts/validate_golden_dataset.py
python3 scripts/validate_atlante_methodology.py
```

If validation fails:
1. read the reported file/column/error;
2. fix CSV headers/values or missing files;
3. re-run validation;
4. document unresolved ambiguity in review notes.

## 12) Pilot debrief
Complete:
`docs/atlante-concorsi-universitari/17_pilot_debrief_template.md`

Debrief must end with one decision:
- proceed to 50–100 manually coded procedures;
- repeat another 10-procedure pilot after codebook revisions;
- stop and redesign part of schema/method.

## 13) Minimum completion criteria
Pilot is complete only when all are true:
- 10 procedures coded;
- all documents linked to source URLs;
- QA checklist completed;
- pilot metrics filled;
- hash manifest generated;
- validation scripts pass;
- debrief completed.
