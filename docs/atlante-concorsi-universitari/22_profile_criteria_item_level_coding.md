# 22 — Profile/criteria item-level coding

## Why item-level coding is needed

The aggregate files (`profile_requirements.csv` and `evaluation_criteria.csv`) are the procedure-level summary layer. They preserve counts, classes, and selected excerpts, but they do not preserve every extracted element as a reusable evidence unit.

Item-level coding adds an explicit evidence layer where each extracted keyword, requirement, criterion, weight, or threshold is stored in its own row with:
- a stable item identifier;
- the related aggregate row identifier;
- text-level evidence (`item_text` / `criterion_text`);
- a document-level link (`source_document_id`);
- a supporting excerpt and confidence note.

## Relationship with aggregate rows

- `profile_requirements.csv` remains the summary row for each procedure profile coding.
- `evaluation_criteria.csv` remains the summary row for each procedure criteria coding.
- `profile_requirement_items.csv` and `evaluation_criterion_items.csv` provide the auditable decomposition feeding those summaries.
- Aggregate counts and class assignments must be reproducible from item-level rows plus method rules.

## How to code thematic keywords

In `profile_requirement_items.csv`, use `item_type=thematic_keyword` when the text states domain/topic focus (e.g., disease area, linguistic subdomain, disciplinary problem, target educational context).

Rules:
- keep one explicit keyword/phrase per row;
- preserve wording close to source text;
- avoid merging distinct topics into a single item;
- attach the shortest excerpt supporting that item.

## How to code methodological keywords

Use `item_type=methodological_keyword` for techniques, analytic approaches, experimental methods, computational tools, and protocol-specific approaches explicitly stated in source text.

Rules:
- one method/approach per row;
- keep method acronyms only when present in source;
- if a method appears only as part of a broader sentence, still store the method phrase as `item_text` and keep the sentence fragment in `source_excerpt`.

## How to code experience requirements

Use `item_type=experience_requirement` for explicit prior-background requirements (e.g., prior qualifications or documented experience expected by the notice).

Rules:
- do not transform forward-looking activity descriptions into prior-experience requirements unless the text explicitly implies prior qualification/experience;
- preserve conservative wording in `notes` when interpretation confidence is not high.

## How to code language requirements

Use `item_type=language_requirement` only when the call explicitly states required language knowledge (or equivalent wording).

Rules:
- include the named language(s) directly in `item_text`;
- keep excerpt text with the requirement statement;
- if no explicit language requirement is present, do not create inferred items.

## How to code criteria items

In `evaluation_criterion_items.csv`:
- `criterion_type=main_criterion` for top-level criterion blocks;
- `criterion_type=subcriterion` for explicitly stated subordinate criteria;
- `criterion_type=profile_linked_criterion` when criterion text explicitly links evaluation to declared field/profile alignment;
- `criterion_type=discretionary_criterion` when judgement is qualitative and non-quantified;
- `criterion_type=other_criterion_feature` for transparent edge cases that do not fit previous types.

## How to code weights and thresholds

- Use `criterion_type=weight` when a weight allocation is separately expressed.
- Use `criterion_type=threshold` when an explicit minimum/eligibility threshold is stated (e.g., 70/100).
- Record numeric weight in `weight_value` and unit in `weight_unit` (e.g., `points`, `%`) when available.
- Record threshold text in `threshold_value` exactly as written when the format is mixed or textual.
- Leave numeric fields empty when not explicitly available.

## How to avoid double counting

- Do not duplicate identical items within the same aggregate row.
- If the same phrase supports multiple coding dimensions, keep one row per coding purpose only when methodologically needed and explain in `notes`.
- Distinguish between `main_criterion` and `weight`: a criterion may have both a criterion row and a separate weight row only if both are explicitly present.
- Repeated references to the same concept in one document should normally map to a single item unless separate sections convey distinct requirements.

## How to preserve evidence excerpts

- Every item row must include `source_excerpt` and `source_document_id`.
- Excerpts should be short, document-faithful, and sufficient for audit traceability.
- Do not add accusatory or legal-conclusive language in any item field or notes.
- Keep `confidence_level` aligned with extraction quality (`low`, `medium`, `high`).

## How to handle `not_determinable` cases

When aggregate coding is `not_determinable`:
- keep the aggregate summary row in place;
- add item rows only for evidence that is explicitly readable and decomposition-safe;
- if decomposition is not robust, leave item layer sparse and explain limitations in `notes`;
- do not infer missing criteria or profile details from partial/noisy text.

This keeps the audit trail conservative while preserving reusable extracted evidence.
