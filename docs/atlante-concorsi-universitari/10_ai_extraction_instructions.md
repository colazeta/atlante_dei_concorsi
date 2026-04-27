# 10 — AI extraction instructions (conservative mode)

These instructions define how a future AI extraction agent must convert public documents into structured records.

## 1) Extraction priorities
1. Procedure-level anchors (`procedure_id`, procedure code, university, position type, dates).
2. Document registry fields (`document_type`, URL, publication/retrieval date, version).
3. Committee and candidate entities with source linkage.
4. Raw fields for profile specificity and criteria narrowness.
5. Derived indicators only after raw fields are complete.

## 2) Preserve evidence
For every extracted factual field, keep traceability:
- source URL;
- document id (if mapped);
- short evidence excerpt when relevant.

Do not overwrite evidence from earlier versions; append a new versioned record.

## 3) No inference beyond text
The agent must not infer legal conclusions or hidden intent.
If a field is absent or ambiguous, set null/empty and use `not_determinable` class/status where defined.

## 4) `evidence_text_excerpt` rules
- Keep excerpts short and literal.
- Prefer one excerpt per relation or sensitive coded fact.
- Do not paraphrase if wording precision matters.
- If no reliable excerpt is available, leave excerpt empty and lower confidence.

## 5) Missing dates
- If only month/year are present, do not fabricate day.
- Keep date null and write note: `partial date in source (YYYY-MM)`.
- Use `retrieval_date` when publication date is missing.

## 6) Ambiguous names
When names are ambiguous (homonyms, abbreviations):
- do not merge identities automatically;
- keep separate provisional rows;
- set `confidence_level=low` and `human_review_required=true` for related relations.

## 7) Multiple document versions
If multiple versions exist:
- keep one row per version in documents;
- increment `version` (`v1`, `v2`, ...);
- preserve old rows;
- mark supersession in notes.

## 8) Raw vs derived fields
Raw fields are extracted counts/flags/excerpts.
Derived fields are computed (`profile_specificity_score`, classes, `criteria_narrowness_score`, classes).
Never compute derived fields when required raw inputs are missing.

## 9) Confidence level policy
- `high`: explicit and unambiguous in official source.
- `medium`: explicit but minor ambiguity remains.
- `low`: interpretation needed or source quality limited.

## 10) Language policy for outputs
Prohibited in outputs:
- accusations;
- legal conclusions;
- wording implying proven misconduct.

Allowed formulations:
- `documented relationship`
- `potentially relevant relation for human review`
- `not determinable from available public documentation`
