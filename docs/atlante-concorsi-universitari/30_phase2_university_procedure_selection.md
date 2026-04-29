# 30 — Phase 2 university and procedure selection note

## Purpose

This note defines the proposed second-phase sampling strategy for the Atlante dei Concorsi Universitari after completion of the first 10-procedure manual pilot.

The first pilot covered:

- Università di Bologna;
- Università della Calabria;
- 10 procedures;
- end-to-end coding across document, profile, criteria, committee, candidate and first-pass relation layers.

The pilot debrief concluded:

```text
ready_to_scale_with_conditions
```

This phase-2 selection note translates that conditional readiness into a controlled expansion plan.

---

## 1. Scale-up objective

Phase 2 should expand from 10 procedures to approximately **30–50 procedures**, without yet moving to public scoring, external enrichment, or automated crawler deployment.

The objective is to test whether the manual/code-assisted methodology remains stable across:

- additional universities;
- additional source environments;
- additional procedure types;
- both clean and difficult document chains;
- public and private university contexts.

---

## 2. Sampling principles

The phase-2 sample should be selected according to six principles.

### 2.1 Source-environment diversity

Select universities that expose competition documents through different publication architectures, for example:

- dedicated recruitment portals;
- albo pretorio / albo online environments;
- amministrazione trasparente pages;
- document-list pages with nested attachments;
- private-university careers/recruitment sections.

### 2.2 Procedure-type diversity

Include at least:

- RTT / tenure-track researcher procedures;
- professore associato / seconda fascia procedures;
- professore ordinario / prima fascia procedures.

Optional, if source documents are comparable:

- technical-administrative competitions;
- fixed-term research/teaching appointments;
- other academic selection procedures.

For phase 2, however, the primary focus should remain on research/academic career competitions.

### 2.3 Geographic diversity

The first pilot already covered Emilia-Romagna and Calabria. Phase 2 should add universities from different macro-areas:

- North-West;
- North-East;
- Centre;
- South;
- Islands, if feasible.

### 2.4 Institutional diversity

Include:

- large generalist public universities;
- medium public universities;
- at least one private university;
- at least one technical/polytechnic institution, if feasible.

### 2.5 Document-chain diversity

Deliberately include both:

- clean cases with complete document chains;
- difficult cases with shared calls, broken attachment URLs, scanned PDFs, unclear criteria documents, or partial candidate/outcome visibility.

This is important because the methodology needs to scale to real source heterogeneity, not only clean portals.

### 2.6 Conservative feasibility

Do not include procedures where the official page cannot be stabilised at all. At this stage, every selected procedure should have at least:

- a stable official source page;
- a call notice or equivalent;
- some trace of commission/criteria/outcome stage, even if partially incomplete.

---

## 3. Proposed additional universities

The following universities are recommended for phase 2. They are proposed as **selection candidates**, not yet as final coded sources. Each must be verified against official pages before procedure-level coding begins.

| Priority | University | Type | Region / macro-area | Reason for inclusion | Expected source value |
|---|---|---|---|---|---|
| Core | Sapienza Università di Roma | Public, large generalist | Lazio / Centre | Very large university with high procedure volume and likely heterogeneous document chains. | Stress-test large-scale public-university sourcing. |
| Core | Università degli Studi di Padova | Public, large generalist | Veneto / North-East | Strong public university with structured administrative publication practices. | Test comparatively structured public source environment. |
| Core | Università degli Studi di Napoli Federico II | Public, large generalist | Campania / South | Large southern university with high procedure volume and likely varied document chains. | Test southern large-university environment distinct from Unical. |
| Core | Università degli Studi di Palermo | Public, large generalist | Sicily / Islands | Adds island coverage and a different administrative publication environment. | Test geographic and portal diversity. |
| Technical | Politecnico di Milano | Public, technical/polytechnic | Lombardia / North-West | Adds technical/polytechnic profile and engineering-heavy procedures. | Test sectoral/procedure specificity in technical fields. |
| Private | LUISS Guido Carli or Università Bocconi | Private university | Lazio or Lombardia | Adds private-university publication logic and different governance/document practices. | Test private-university source comparability. |

### Private university choice

For the private-university component, choose **one** between:

- LUISS Guido Carli;
- Università Bocconi.

Selection should depend on which institution provides the more stable and transparent official procedure documentation for the target period.

If both are feasible, prefer the one that better exposes:

- call notice;
- appointment/commission documents;
- criteria documents;
- outcome or acts approval documents.

---

## 4. Proposed procedure allocation

Target total: **30–50 procedures**.

Recommended operational target: **36 procedures**, because it is large enough to test scaling but still manageable manually.

| University group | Procedures | Notes |
|---|---:|---|
| Sapienza | 6 | Mix RTT, PA, PO. |
| Padova | 6 | Mix RTT, PA, PO; include at least one difficult document chain if available. |
| Napoli Federico II | 6 | Mix procedure types; prioritise complete document chains. |
| Palermo | 6 | Include at least one professor procedure and one RTT. |
| Politecnico di Milano | 6 | Focus on technical/engineering fields and procedure specificity. |
| Private university selected | 6 | Test private publication model; include only procedures with adequate official documentation. |

Alternative smaller target: **30 procedures**, with 5 per university.

Alternative larger target: **48 procedures**, with 8 per university, only if manual throughput remains manageable.

---

## 5. Procedure-type quotas

For a 36-procedure phase-2 sample, use the following target mix:

| Procedure type | Target count | Rationale |
|---|---:|---|
| RTT | 12 | Maintains continuity with first pilot and current academic recruitment relevance. |
| PA / seconda fascia | 12 | Expands professor-procedure coverage. |
| PO / prima fascia | 8 | Tests higher-rank procedure documents and smaller candidate sets. |
| Reserve / difficult cases | 4 | Use for procedures with unusual or incomplete chains. |

The reserve should not be used to force bad data. It should be used for methodologically useful edge cases.

---

## 6. Document-chain requirements

Each selected procedure should be classified before coding as one of:

| Chain class | Definition | Use in phase 2 |
|---|---|---|
| complete_chain | call, commission, criteria and outcome/acts are present. | Core sample. |
| partial_chain | one key stage is missing or inaccessible. | Include selectively. |
| shared_call_chain | general call covers multiple sub-procedures. | Include to test attribution rules. |
| noisy_pdf_chain | documents exist but extraction/OCR is weak. | Include sparingly to test not_determinable rules. |
| private_source_chain | private university publication model. | Include if documentation is sufficient. |

For the 36-procedure target, aim for:

- at least 20 complete_chain procedures;
- at least 6 shared_call_chain procedures;
- at least 4 noisy_pdf_chain procedures;
- at least 4 private_source_chain procedures;
- no more than 8 partial_chain procedures.

---

## 7. Exclusions for phase 2

Do not include procedures that require, from the start:

- external enrichment to identify candidates;
- non-official sources to identify commissions;
- scraping behind authentication;
- non-public documents;
- interpretation of conflicts or relationships;
- public-facing risk scoring.

Do not include procedures where only press/news material is available and official documentation is absent.

---

## 8. Operational workflow

For each selected university:

1. create/update a source registry entry;
2. identify 5–8 candidate procedures;
3. classify each procedure’s document chain;
4. select final procedures according to quotas;
5. initialise procedure IDs;
6. code document layer first;
7. audit document layer;
8. code profile and criteria layers;
9. audit aggregate/item consistency;
10. code committee/candidate layers;
11. audit committee/candidate extraction;
12. code relation first-pass only where eligible;
13. run validation after each batch.

---

## 9. Proposed phase-2 IDs

Reserve the following ID range:

```text
ACU-P2-0001 to ACU-P2-0050
```

Suggested pattern:

| University | Suggested ID range |
|---|---|
| Sapienza | ACU-P2-0001 to ACU-P2-0008 |
| Padova | ACU-P2-0009 to ACU-P2-0016 |
| Napoli Federico II | ACU-P2-0017 to ACU-P2-0024 |
| Palermo | ACU-P2-0025 to ACU-P2-0032 |
| Politecnico di Milano | ACU-P2-0033 to ACU-P2-0040 |
| Private university | ACU-P2-0041 to ACU-P2-0050 |

The range is intentionally larger than the initial target to allow substitutions.

---

## 10. Immediate next tasks

Before any phase-2 coding starts:

1. verify official source pages for the six proposed universities;
2. choose the private university based on source stability;
3. create a source registry expansion plan;
4. select 5–8 candidate procedures per university;
5. prepare a final phase-2 procedure list;
6. create issue(s) for the first phase-2 university batch.

---

## 11. Readiness decision

Phase 2 is ready to proceed to **university/procedure selection**, not yet to bulk coding.

Status:

```text
ready_for_phase2_selection
```

Not yet authorised:

```text
ready_for_public_scoring
ready_for_automated_crawling
ready_for_external_enrichment
```
