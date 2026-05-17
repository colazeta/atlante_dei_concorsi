# Italian university URL registry (official sources)

Registry governato degli URL ufficiali degli atenei italiani, orientato a intake controllato.

## Current scope

- execution type: controlled URL-registry expansion;
- rows mapped: **30** universities (expanded subset beyond bootstrap);
- homepage ufficiale valorizzata per tutte le righe;
- recruitment/concorsi URL valorizzato solo dove determinabile con sufficiente confidenza.

## Required CSV schema

`official_university_urls.csv` headers:

`university_id,university_name,university_type,official_homepage_url,recruitment_page_url,source_url,source_type,retrieval_date,confidence_level,verification_status,notes`

## Governance notes

- Nessuna modifica al golden dataset.
- Nessun documento raw/snapshot raccolto o committato.
- Incertezza preservata tramite `verification_status` e `notes`.
- Copertura ancora parziale rispetto all'universo completo degli atenei riconosciuti; richiede ulteriori run controllate.
