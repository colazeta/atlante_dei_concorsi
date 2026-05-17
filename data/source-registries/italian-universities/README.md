# Italian university URL registry (official sources)

This directory contains a governed registry of **official URLs** for Italian universities.

## Current scope

- execution type: controlled URL-registry setup;
- rows currently mapped: **10** universities (bootstrap subset);
- each row includes official homepage, optional recruitment/concorsi page, source provenance, confidence and verification status.

## Required CSV schema

`official_university_urls.csv` uses the following headers:

`university_id,university_name,university_type,official_homepage_url,recruitment_page_url,source_url,source_type,retrieval_date,confidence_level,verification_status,notes`

## Governance notes

- No golden-dataset rows were modified.
- No raw documents, snapshots, candidate data, committee data, relations or conclusions were collected.
- Uncertainty is preserved through `verification_status` and `notes`.
- This registry is ready for iterative expansion once issue-level approval confirms full-universe completion steps.
