# 29 — Phase 2 codebook refinements

## Purpose

This document hardens the coding rules before the second-phase scale-up of the Atlante dei Concorsi Universitari.

The first 10-procedure manual pilot concluded `ready_to_scale_with_conditions`. The main condition is that scale-up must preserve conservative, evidence-based coding and avoid turning extraction limitations into substantive claims.

This document refines six areas that emerged as fragile:

1. minimum decomposition threshold for criteria scoring;
2. treatment of `not_determinable` criteria rows;
3. shared/general call coding;
4. candidate placeholder rule;
5. relation-review eligibility rule;
6. name normalisation.

No rule in this document authorises legal conclusions, accusations, conflict findings, or external enrichment.

---

## 1. Minimum decomposition threshold for criteria scoring

### Objective

Criteria scoring must be assigned only when the source document is sufficiently legible and structurally decomposable. A criteria document may be officially available but still not safe for decomposition.

### Decomposition-safe criteria document

A criteria document is decomposition-safe only when all of the following are true:

| Requirement | Meaning |
|---|---|
| Text access | The relevant text can be read with sufficient reliability, either from native text or clean extraction. |
| Procedure attribution | The criteria can be clearly attributed to the specific procedure being coded. |
| Criterion boundaries | Top-level criteria can be separated without guessing. |
| Countability | Criteria/subcriteria can be counted using explicit labels, headings, enumerations or clear structural blocks. |
| Weight evidence | Weights are explicitly stated if `has_weights=true`. |
| Threshold evidence | Thresholds are explicitly stated if `has_thresholds=true`. |
| Discretionary evidence | Qualitative/non-quantified criteria can be identified from explicit wording, not inferred from generic evaluative language alone. |

### Minimum evidence for aggregate coding

Use the following minimum evidence checklist before assigning non-`not_determinable` criteria scores:

| Field | Minimum evidence required |
|---|---|
| `number_of_criteria` | Explicit criteria blocks, labels, headings or a stable list of distinct criteria. |
| `number_of_subcriteria` | Explicitly enumerated subordinate items or titled subcriteria. Pure scoring bands do not count. |
| `has_weights` | At least one explicit maximum score, weight, percentage or points allocation. |
| `has_thresholds` | Explicit minimum score, eligibility threshold, pass/fail threshold, or equivalent threshold statement. |
| `has_eliminatory_criteria` | Explicit language that a criterion excludes, disqualifies, prevents admission, or prevents eligibility. |
| `number_of_criteria_linked_to_profile` | Explicit link to the profile, sector, field, call-specific activities, language requirement, or procedure-specific scientific area. |
| `share_non_quantified_discretionary_criteria` | Sufficiently clear denominator and numerator, or a documented conservative estimate based on explicitly qualitative items. |

### Decision tree

```text
Can the criteria document be reliably read?
│
├── No → criteria_narrowness_class = not_determinable
│
└── Yes
    │
    ├── Are criteria clearly attributable to the specific procedure?
    │   ├── No → not_determinable
    │   └── Yes
    │       │
    │       ├── Can top-level criteria be counted without guessing?
    │       │   ├── No → not_determinable
    │       │   └── Yes → aggregate criteria coding may proceed
```

### Coding rule

If one or more core elements are not decomposition-safe, prefer `not_determinable` over a partial score. Partial scores are permitted only when the uncertain element is not required for the intended aggregate field and the uncertainty is clearly documented in `notes`.

---

## 2. Treatment of `not_determinable` criteria rows

### Meaning

`not_determinable` means that the available official evidence does not support decomposition-safe criteria coding. It does not mean that criteria are absent, invalid, weak, or suspicious.

### When to use `not_determinable`

Use `criteria_narrowness_class=not_determinable` when:

- the criteria document is inaccessible;
- text extraction is too noisy for reliable counting;
- the document is legible but not clearly attributable to the specific procedure;
- criteria are visible but boundaries are ambiguous;
- the document is a general or shared file and the relevant section cannot be isolated;
- the coder cannot distinguish main criteria from subcriteria without interpretation.

### Aggregate row rule

For `evaluation_criteria.csv`:

- keep `criteria_available=true` if a criteria document exists in the official registered source;
- set `criteria_narrowness_class=not_determinable` if the document is not decomposition-safe;
- leave `criteria_narrowness_score` empty/null when the score is not defensible;
- set `human_review_required=true`;
- explain the documentary limitation in `notes`.

### Item-level rule

For `evaluation_criterion_items.csv`:

| Situation | Item-level action |
|---|---|
| Criteria document unavailable or unreadable | Do not create item rows. |
| Criteria document exists but is not decomposition-safe | Usually do not backfill item rows. |
| Some isolated elements are readable | Add only those elements if explicitly supported and mark confidence conservatively. |
| Aggregate class is `not_determinable` | Do not force item rows merely to satisfy counts. |

### Standard note wording

Use a note close to:

```text
Criteria document is officially registered, but text/structure was not decomposition-safe for robust criteria scoring. No criteria counts or score were inferred.
```

---

## 3. Shared/general call coding

### Problem

Some university pages contain general calls covering multiple sub-procedures. The profile or criteria evidence may appear partly in the general call and partly in procedure-specific attachments.

### Rule of attribution

Only code a profile or criterion for a specific procedure when the text is clearly attributable to that procedure.

### Safe evidence hierarchy

Prefer sources in this order:

1. procedure-specific attachment;
2. procedure-specific section inside a general call;
3. general call text that explicitly names/includes the procedure;
4. general call text applicable to all listed procedures, but only for generic procedural requirements.

### Do not import generic text as profile specificity

Do not treat general eligibility rules, generic legal requirements, or general application requirements as procedure-specific profile specificity unless they are clearly tied to the specific post.

Examples of text that should not inflate profile specificity:

- generic application requirements;
- general legal eligibility rules;
- standard participation requirements;
- standard publication limits applicable to all procedures;
- generic duties of the academic role.

### Coding shared calls

When using a shared call:

- cite the shared call document ID;
- record in `notes` that the source is shared/general;
- only extract items clearly linked to the procedure code, GSD/SSD, department, project, activity description or language requirement;
- use `not_determinable` if procedure-specific attribution cannot be established.

### Decision tree

```text
Is the call shared across multiple procedures?
│
├── No → code normally
│
└── Yes
    │
    ├── Is there a procedure-specific section?
    │   ├── Yes → code only that section
    │   └── No
    │       │
    │       ├── Does the general text apply equally to all procedures?
    │       │   ├── Yes → code only generic eligibility, not profile specificity
    │       │   └── No → not_determinable for procedure-specific profile items
```

---

## 4. Candidate placeholder rule

### Purpose

Candidate placeholders preserve the fact that an outcome/admission source exists while avoiding unsupported candidate identity/status extraction.

### When one placeholder row is appropriate

Create exactly one placeholder candidate row for a procedure only when all conditions are met:

1. an official registered document indicates that candidate/outcome/admission information should exist;
2. the document is inaccessible, broken, not extractable, or not sufficiently legible;
3. no reliable candidate identity/status can be extracted;
4. the procedure should still be represented in `candidates.csv` for audit completeness.

### Required placeholder values

Use:

```text
person_name = not_determinable
candidate_status = not_determinable
confidence_level = low
```

The row must include:

- `procedure_id`;
- `source_document_id`;
- `source_url`;
- notes explaining the limitation.

### When not to create a placeholder

Do not create a placeholder when:

- there is no registered candidate/outcome/admission source;
- the source only documents procedure stage without candidate information;
- candidate information is expected from the workflow but no registered document exists;
- the row would imply a candidate count.

### Standard note wording

Use wording close to:

```text
Official outcome/admission source is registered, but candidate identity/status was not reliably extractable in this pass. Placeholder row created only to document non-determinability; no candidate count or identity inferred.
```

### Prohibited behaviour

Do not:

- create multiple placeholders for unknown candidates;
- infer the number of candidates;
- infer identities from other sources;
- enrich with external profiles;
- convert placeholder rows into relation-eligible candidate evidence.

---

## 5. Relation-review eligibility rule

### Purpose

The relation layer records documented committee-candidate relationships or a narrowly defined registered-source review outcome. It does not discover conflicts, infer relationships, or make legal assessments.

### Eligibility for first-pass relation review

A procedure is eligible for `committee_candidate_relations.csv` first-pass review only when:

1. committee members are determinable;
2. at least one candidate is determinable;
3. relevant registered official sources have been reviewed;
4. relation review is limited to registered official sources;
5. no external enrichment is used.

### Procedures not eligible

Do not create relation rows when:

- candidates are only placeholder/not_determinable;
- committee members are not determinable;
- no registered source can be reviewed;
- the only available information is the procedural role itself.

### Registered-source-only absence coding

Use:

```text
relation_type = no_documented_relation_in_registered_sources
```

only when:

- committee members and candidates are determinable;
- registered official sources were reviewed;
- no explicit committee-candidate relationship evidence is documented in those registered sources;
- no external enrichment was performed.

### Meaning limitation

This value means:

```text
No committee-candidate relationship evidence was identified in the registered official sources reviewed.
```

It does not mean:

```text
No relationship exists.
```

### Standard notes

Use wording close to:

```text
No committee-candidate relationship evidence identified in registered official sources only. No external enrichment performed.
```

### Pairwise rule

Do not create one row per committee-candidate pair merely to say that no evidence was found. For registered-source-only first-pass review, use one procedure-level review row unless an explicit documented relation is present.

---

## 6. Name normalisation

### Objective

Name normalisation should support internal consistency without external enrichment or identity resolution beyond the official documents.

### General rule

Preserve official-document names while applying light formatting normalisation only.

Allowed:

- trimming extra spaces;
- normalising repeated whitespace;
- preserving accents and diacritics when present;
- preserving compound surnames as written;
- removing academic titles only if they are clearly titles, not part of the name field;
- keeping a note if the source format is ambiguous.

Not allowed:

- external identity enrichment;
- guessing full names from initials;
- matching names to university profile pages;
- adding ORCID/Scopus/Scholar/LinkedIn information;
- resolving homonyms externally;
- inferring gender, nationality, seniority or relationship.

### Titles

If a source says `Prof. Mario Rossi`, code:

```text
person_name = Mario Rossi
```

If title removal creates ambiguity, preserve the source form and note the issue.

### Accents and diacritics

Preserve source spelling:

```text
D'Angelo
De Santis
García
Müller
```

Do not transliterate unless the source already uses transliteration.

### Initials

If only initials are provided, do not expand them.

Example:

```text
M. Rossi
```

should remain:

```text
M. Rossi
```

with confidence lowered if needed.

### Affiliation variants

Do not harmonise affiliations beyond light formatting unless the same source explicitly provides the standard form.

Examples:

- `Università della Calabria` and `Unical` should not automatically be merged unless a separate normalisation layer is introduced.
- Department variants should be preserved in the source-derived field and later handled by a dedicated entity-resolution process.

### Duplicate check

Within the same procedure, two rows should be treated as duplicates only if the name and role/affiliation clearly refer to the same person in the same source context.

---

## Phase-2 operating rules

Before adding new procedures in phase 2:

1. confirm source pages and document chains first;
2. code procedure/document layer before substantive layers;
3. code profile aggregate and item layers together;
4. code criteria aggregate only when decomposition-safe;
5. do not force criteria item backfill for `not_determinable` rows;
6. code committees/candidates only from registered official documents;
7. apply candidate placeholders sparingly;
8. code relation review only when eligibility conditions are met;
9. keep all relation-review outcomes internal-only unless separately approved;
10. run validation and audit after each batch.

---

## Phase-2 go condition

Issue `#20` may proceed to university/procedure selection only after these refinements are accepted.

Recommended readiness after this document:

```text
ready_for_phase2_selection
```

but not yet:

```text
ready_for_public_scoring
ready_for_automated_crawling
ready_for_external_enrichment
```
