# Italian university URL registry (official sources)

Registry governato degli URL ufficiali degli atenei italiani, orientato a intake controllato.

## Current scope

- execution type: controlled URL-registry expansion (issue #61 continuation);
- rows mapped in `official_university_urls.csv`: **80** universities;
- row-level reconciliation table created for remaining institutions: `missing_universities_to_verify.csv` (**19** rows);
- homepage ufficiale valorizzata dove determinabile da fonte istituzionale;
- recruitment/concorsi URL valorizzato solo dove determinabile con confidenza sufficiente.

## Required CSV schema

`official_university_urls.csv` headers:

`university_id,university_name,university_type,official_homepage_url,recruitment_page_url,source_url,source_type,retrieval_date,confidence_level,verification_status,notes`

Fallback reconciliation file headers:

`universe_source,university_name,university_type,official_homepage_url,recruitment_page_url,confidence_level,verification_status,notes`

## Governance notes

- Nessuna modifica al golden dataset.
- Nessun documento raw/snapshot raccolto o committato.
- Incertezza preservata tramite `verification_status` e `notes`.
- Le 19 istituzioni residue sono riconciliate a livello riga nel file di verifica, con stati non bloccanti (`homepage_only`, `needs_human_review`).
