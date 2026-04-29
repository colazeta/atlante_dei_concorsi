# 31 — Phase 2 source verification

## Purpose

This note verifies the official source environments for the candidate phase-2 universities before any new procedures are coded or initialised.

Reference issue: `#22`.

Reference selection note:

- `docs/atlante-concorsi-universitari/30_phase2_university_procedure_selection.md`

This verification is limited to official university domains and source pages. It does not initialise `ACU-P2` procedure IDs, download raw documents, enrich personal names, infer relationships, or assess conflicts.

---

## 1. Summary recommendation

Recommended phase-2 university set:

1. Sapienza Università di Roma;
2. Università degli Studi di Padova;
3. Università degli Studi di Napoli Federico II;
4. Università degli Studi di Palermo;
5. Politecnico di Milano;
6. Università Bocconi.

Private university recommendation:

```text
Prefer Università Bocconi over LUISS for the first private-university phase-2 test.
```

Reason: Bocconi exposes a clearer public recruitment/concorsi landing page for L. 240/2010 categories. LUISS has official PDFs and procedure records, but the stable public landing/index structure for complete procedure chains is less clear and appears more fragmented across API/backoffice/static-document paths.

Recommended status:

```text
ready_for_phase2_procedure_selection_with_domain_updates
```

The main required domain update is for Federico II: add `dises.unina.it` if procedures are to be selected from the currently visible recruitment pages found there.

---

## 2. Source URL table

| University | Candidate official source URLs checked | Source-environment classification | Suitability |
|---|---|---|---|
| Sapienza Università di Roma | `https://www.uniroma1.it/it/pagina/settore-concorsi-professori`; `https://www.uniroma1.it/it/pagina/settore-concorsi-ricercatori`; `https://web.uniroma1.it/trasparenza/albo-pretorio`; example detail `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/233363` | Mixed: central recruitment pages + Amministrazione trasparente / Albo detail pages | medium-high |
| Università degli Studi di Padova | `https://www.unipd.it/procedura-2025RUA01`; examples: `https://www.unipd.it/procedura-2024RTT04`, `https://www.unipd.it/procedura-2025RUA02` | Dedicated procedure pages with nested attachments | high |
| Università degli Studi di Napoli Federico II | example pages under `https://www.unina.it/` and `https://www.dises.unina.it/.../reclutamento-ricercatori-a-tempo-determinato` | Mixed central/departmental recruitment pages; long listing pages with document links | high, conditional on domain update |
| Università degli Studi di Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html`; `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/chiamata/art18-appr-atti/index.html` | Recruitment office pages with procedure blocks and linked official attachments | high |
| Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi`; `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato`; example official PDF path under `www.polimi.it/fileadmin/...` | Dedicated recruitment portal with filterable procedure lists and official PDF attachments | high |
| Università Bocconi | `https://www.unibocconi.it/it/docenti-e-ricerca/docenti/reclutamento-docenti/concorsi`; `https://www.unibocconi.it/it/docenti-e-ricerca/docenti/reclutamento-docenti/reclutamento-assistant-professors-l2402010` | Private-university recruitment pages for L. 240/2010 categories | medium |
| LUISS Guido Carli | `https://www.luiss.it/`; `https://backoffice.luiss.it/`; `https://apigw.luiss.it/`; example official PDFs under `https://apigw.luiss.it/prod/sites/default/files/...` | Fragmented private-university evidence environment: official PDFs visible, but stable procedure-chain index less clear | low-medium |

---

## 3. Document availability matrix

| University | Call notices | Committee appointments | Criteria / minutes | Candidate/admission/outcome/acts | Direct document URLs | Main limitation |
|---|---|---|---|---|---|---|
| Sapienza | available | available in Albo/detail pages where procedure chain is complete | available in some detail pages as verbali/preliminari | approval acts available in some detail pages | mixed; page-level + PDF attachments | source spread across central pages and transparency detail pages |
| Padova | available | available | available as `Verbale 1 - criteri` | available: candidate lists, judgments, scores, approval acts in many procedure pages | strong; many `Download` links | multi-position pages require careful sub-procedure attribution |
| Napoli Federico II | available | available | available | available: admitted lists, calendars, approval acts in visible examples | likely available, but often inside long listing pages | useful pages may be on `dises.unina.it`, requiring domain allowlist update |
| Palermo | available | available | available as `Verbale 1 - Criteri` | available: oral-test notices, approval acts, final reports | strong page-level attachments | long pages with many procedures; careful block segmentation required |
| Politecnico di Milano | available | available in procedure chain/PDF attachments | available as verbali/criteria PDFs | likely available for archived/completed procedures | strong PDF URLs under official domain | current/open lists include many active cases; need select completed/archived cases |
| Bocconi | available at category/competition level | to be verified procedure by procedure | to be verified procedure by procedure | to be verified procedure by procedure | likely mixed | private source comparability and outcome-stage completeness must be checked carefully |
| LUISS | available in PDFs/procedure records | available in verbali/commission records | available in verbali | sometimes available in procedure PDFs, but chain completeness must be verified | fragmented: `apigw`, `api`, `backoffice`, static PDFs | stable landing/index is weaker than Bocconi; additional domain `api.luiss.it` may be needed |

---

## 4. University-by-university assessment

### 4.1 Sapienza Università di Roma

Assessment: **medium-high suitability**.

Useful source pattern:

- central pages explain the offices responsible for professor and researcher competitions;
- Albo/trasparenza detail pages expose procedure-level documents;
- some detail pages include bando, commission appointment, approval acts and preliminary/minutes attachments.

Strengths:

- high volume;
- official source pages;
- useful transparency detail records;
- good stress test for central + Albo source integration.

Limitations:

- source navigation is more fragmented than Unibo/Unical;
- procedure-specific extraction may require starting from detail pages rather than only office pages;
- some detail pages may concern other recruitment/collaboration categories, requiring filtering to academic procedures.

Recommendation:

Include Sapienza, but require a pre-selection filter to distinguish professor/RTT procedures from other Albo entries.

### 4.2 Università degli Studi di Padova

Assessment: **high suitability**.

Useful source pattern:

- procedure pages such as `procedura-2025RUA01` expose general bando, attachments and repeated sub-procedure sections;
- procedure blocks include commission appointment, criteria, candidate lists, judgments, scores/winner and approval acts.

Strengths:

- strong document-chain completeness;
- many official attachments;
- good support for profile/criteria/candidate/committee layers;
- useful test of shared/general call and many-subprocedure attribution rules.

Limitations:

- multi-position pages can be long and require careful mapping of each attachment to the correct sub-procedure;
- direct downloads must be verified before coding.

Recommendation:

Include Padova as a core phase-2 university.

### 4.3 Università degli Studi di Napoli Federico II

Assessment: **high suitability, conditional on domain update**.

Useful source pattern:

- visible recruitment listings include bando, online application, commission, criteria, admitted lists, calendars and approval acts;
- several examples show complete or near-complete RTT chains.

Strengths:

- rich document chains;
- useful procedure codes;
- clear stage labels in visible examples;
- strong candidate for southern large-university coverage.

Limitations:

- relevant pages may appear on departmental subdomains such as `dises.unina.it`, not only `www.unina.it`;
- long dynamic/listing pages may require careful extraction;
- domain allowlist should be updated before procedure coding.

Required domain update:

```text
dises.unina.it
```

Recommendation:

Include Federico II, but add `dises.unina.it` to the allowed domains before source-specific procedure selection.

### 4.4 Università degli Studi di Palermo

Assessment: **high suitability**.

Useful source pattern:

- recruitment office pages organise procedures by academic role/type;
- RTT pages expose bando, commission appointment, criteria, oral-discussion notice, approval acts and final report.

Strengths:

- strong document-chain completeness;
- useful island/geographic coverage;
- good fit for testing document-chain classes including complete_chain and shared blocks.

Limitations:

- long pages with many grouped procedures require careful segmentation;
- some links may be repeated or organised by subject/SSD rather than by single procedure URL.

Recommendation:

Include Palermo as a core phase-2 university.

### 4.5 Politecnico di Milano

Assessment: **high suitability**.

Useful source pattern:

- central `Bandi e concorsi` page branches into professor and researcher opportunities;
- researcher pages expose active/in-course/archived procedure entries;
- official PDFs under `www.polimi.it/fileadmin/...` include verbali/criteria and commission details.

Strengths:

- technical/polytechnic environment;
- official PDF infrastructure;
- many RTT/technical-field procedures;
- strong test for technical profile specificity.

Limitations:

- phase-2 should prefer completed/archived procedures over currently open procedures;
- professor procedure pages should be separately verified before final allocation.

Recommendation:

Include Politecnico di Milano as the technical/polytechnic component.

### 4.6 Università Bocconi

Assessment: **medium suitability**.

Useful source pattern:

- public recruitment/concorsi landing page for L. 240/2010 categories;
- pages mention recruitment categories for faculty, assistant professors, lecturers, post-doc researchers and research grants.

Strengths:

- stronger private-university landing structure than LUISS in the preliminary check;
- good candidate for testing private-university comparability;
- official domain is stable and public.

Limitations:

- procedure-level chains must be verified before coding;
- public pages may describe recruitment processes more than expose full chains of bando/commission/criteria/outcome;
- source completeness may vary by category.

Recommendation:

Select Bocconi as the preferred private-university candidate, conditional on identifying at least 4–6 procedure chains with adequate official documentation.

### 4.7 LUISS Guido Carli

Assessment: **low-medium suitability**.

Useful source pattern:

- official PDFs and verbali exist under LUISS-controlled domains;
- some verbali contain committee composition and criteria text;
- regulatory documents are available.

Strengths:

- potentially rich official PDFs;
- good private-university comparison case if stable chains are identified.

Limitations:

- stable public landing/index for full procedure chains is less clear;
- evidence appears fragmented across `apigw.luiss.it`, `api.luiss.it`, `backoffice.luiss.it` and static PDFs;
- additional domain `api.luiss.it` may be needed if LUISS is selected.

Potential domain update if LUISS is retained:

```text
api.luiss.it
```

Recommendation:

Do not select LUISS for the first private-university phase-2 batch unless Bocconi proves insufficient. Keep LUISS as reserve/private fallback.

---

## 5. Recommended final phase-2 university set

Recommended set:

| Slot | University | Status |
|---|---|---|
| 1 | Sapienza Università di Roma | include |
| 2 | Università degli Studi di Padova | include |
| 3 | Università degli Studi di Napoli Federico II | include after adding `dises.unina.it` |
| 4 | Università degli Studi di Palermo | include |
| 5 | Politecnico di Milano | include |
| 6 | Università Bocconi | include conditionally after procedure-chain check |
| Reserve | LUISS Guido Carli | reserve/private fallback |

---

## 6. Domains to add before procedure selection

Required:

```text
dises.unina.it
```

Potential only if LUISS is later selected:

```text
api.luiss.it
```

No broad external domains should be added at this stage.

`pica.cineca.it` may appear as an application portal, but it should not be treated as a primary evidence source for the golden dataset unless a separate source-policy decision authorises it. The primary evidence should remain on official university-controlled pages and documents.

---

## 7. Next operational step

After this verification note:

1. add `dises.unina.it` to allowed domains;
2. keep `api.luiss.it` out unless LUISS is selected later;
3. create a phase-2 procedure-candidate list for the recommended university set;
4. target 5–8 candidate procedures per university;
5. classify each candidate procedure by document-chain class before initialising `ACU-P2` IDs.

No phase-2 procedure coding should start until the candidate procedure list is reviewed.

---

## 8. Final decision

Status:

```text
ready_for_phase2_procedure_candidate_selection
```

Not authorised yet:

```text
ready_for_bulk_coding
ready_for_public_scoring
ready_for_external_enrichment
ready_for_automated_crawling
```
