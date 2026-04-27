# 09 — Manual coding guide (one procedure)

This guide is for a new human coder entering one procedure into the atlas.

## 1) Before opening documents
1. Open `source_registry_template.csv` and confirm the university source row exists.
2. Create a working folder for the procedure (`raw/{procedure_id}/`) and save retrieval date.
3. Prepare the target CSVs: procedures, documents, profile requirements, evaluation criteria, committee members, candidates, relations.
4. Read the neutral-language policy in `00_scope_and_publication_principles.md` and `13_publication_language_policy.md`.

## 2) Decide whether documents belong to the same procedure
Treat documents as one procedure when at least two anchors match:
- same procedure code or bando reference;
- same academic field / SSD / settore;
- same position type and department;
- explicit reference to previous act number.

If uncertain, keep temporary split records and add note: `possible merge pending verification`.

## 3) Assign `procedure_id`
Format recommendation:
`UNI-<year>-<local_code>` or `UNI-<year>-<progressive_number>`.

Rules:
- stable over time;
- one id for all versions/corrections of the same procedure;
- do not reuse ids.

## 4) Classify each document
For every document, create one `documents_template.csv` row and set:
- `document_type` from controlled taxonomy only;
- `source_url`, `retrieval_date`, `official_source_flag`;
- `version` (`v1`, `v2`, ...), updating when corrected documents appear.

If a document type is unclear, use `other` and explain in `notes`.

## 5) Extract `number_of_positions`
Priority order:
1. explicit numeric field in call notice;
2. table/annex specifying positions;
3. correction document updating counts.

If contradictory numbers exist, keep latest official version and add note with previous value.
If not inferable: set `number_of_positions` to `not_determinable` in notes and keep numeric field empty in raw worksheet until adjudication.

## 6) Code profile requirements
Use `profile_requirements_template.csv`.
- Count raw fields directly from call text.
- Save short literal excerpts in `profile_excerpt_1` and `profile_excerpt_2`.
- Do not interpret intent; count only observable items.
- Compute class using method doc; if text missing, use `profile_specificity_class=not_determinable` and `human_review_required=true`.

## 7) Code evaluation criteria
Use `evaluation_criteria_template.csv`.
- Set `criteria_available` first.
- If available, count criteria/subcriteria and mark weights/thresholds/eliminatory criteria.
- Store supporting excerpts.
- If not available, use `criteria_narrowness_class=not_determinable` and explain in notes.

## 8) Code committee members
Use `committee_members_template.csv`.
- Add one row per person.
- Link each row to `source_document_id` and `source_url`.
- Use `confidence_level=high` when explicitly listed; otherwise `medium`/`low` with note.

## 9) Code candidates
Use `candidates_template.csv`.
- Add one row per publicly documented candidate.
- Use allowed `candidate_status` only.
- If candidate list is unavailable, do not invent names; record absence at procedure notes level.

## 10) Code committee-candidate documented relations
Use `committee_candidate_relations_template.csv`.
- Create relation rows only with documentary evidence.
- Fill `evidence_source_url`, `evidence_source_type`, and `evidence_text_excerpt`.
- Use `not_determinable` when evidence is insufficient.
- Set `relation_relevant_for_review` and `potential_conflict_review_signal` cautiously.

## 11) Record uncertainty and use `not_determinable`
Use `not_determinable` when:
- document missing from public sources;
- text illegible/incomplete;
- identity ambiguity cannot be resolved reliably.

Always explain uncertainty in `notes`.

## 12) When to trigger `human_review_required`
Trigger true when:
- key documents are missing;
- profile/criteria classes are `very_high`;
- relation evidence is ambiguous or sensitive;
- conflicting dates or counts exist.

## 13) Acceptable notes (examples)
- `Two versions found; v2 supersedes v1 on 2026-03-14.`
- `Candidate status marked not_determinable: no admission list published.`
- `Relation coded as same_academic_field based on explicit SSD in official CV.`

## 14) Wording to avoid
Avoid:
- `procedure manipulated`
- `conflict confirmed`
- `committee biased`

Prefer:
- `documented relationship`
- `potentially relevant relation for human review`
- `not determinable from available public documentation`
