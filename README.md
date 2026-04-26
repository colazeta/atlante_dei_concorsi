# Atlante dei Concorsi Universitari

Repository for the methodological and data-modelling foundation of a documentary atlas of Italian university recruitment procedures.

## What this module contains

- Methodological documentation (`docs/atlante-concorsi-universitari/00-13`) for scope, coding rules, taxonomies, quality checks, publication language, and pilot setup.
- Technology-neutral JSON Schemas (`schemas/atlante-concorsi-universitari/`) for procedures, documents, profile/criteria coding, committee members, candidates, documented relations, and source registry entries.
- CSV templates (`data/templates/atlante-concorsi-universitari/`) aligned with schema fields for manual coding and import pipelines.
- A lightweight validation script (`scripts/validate_atlante_methodology.py`) to check expected files, JSON validity, and schema/CSV header alignment.

## What this module does **not** contain yet

- Crawlers or scraping implementations.
- Dashboard or public UI.
- Runtime risk-scoring engine.
- Agentic browsing/verification runtime.

## Run validation

From repository root:

```bash
python3 scripts/validate_atlante_methodology.py
```

Expected output on success:

```text
Validation passed: expected files, JSON parsing, and schema/CSV header alignment are OK.
```

## Next development phase (recommended)

1. Build ingestion connectors that only collect official/public documentary sources.
2. Implement deterministic parsers that populate raw fields first, then derived indicators.
3. Add pipeline-level schema validation and QA workflow gates before golden dataset ingestion.
4. Introduce controlled publication views that enforce neutral language and uncertainty labels.
