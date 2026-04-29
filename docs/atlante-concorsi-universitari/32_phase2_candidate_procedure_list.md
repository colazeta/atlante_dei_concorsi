# 32 — Phase 2 candidate procedure list

## Purpose

This note proposes a reviewed candidate list of phase-2 procedures before any `ACU-P2` IDs are initialised or coded.

Reference issue: `#23`.

Reference documents:

- `docs/atlante-concorsi-universitari/29_phase2_codebook_refinements.md`
- `docs/atlante-concorsi-universitari/30_phase2_university_procedure_selection.md`
- `docs/atlante-concorsi-universitari/31_phase2_source_verification.md`

This note does not add rows to the golden dataset and does not initialise procedure IDs. The IDs below are temporary candidate IDs only.

---

## 1. Selection outcome

Recommended immediate phase-2 candidate set:

```text
30 candidate procedures
```

Recommended operational choice:

```text
Start with a 30-procedure public-university batch, then add a private-university probe only after a more stable private procedure chain is identified.
```

Reason: the five public university environments below already expose sufficiently rich procedure chains. The private-university component remains methodologically important, but Bocconi and LUISS need one more source-chain check before assigning `ACU-P2` IDs.

Recommended public-university batch:

1. Sapienza Università di Roma — 5 candidates;
2. Università degli Studi di Padova — 6 candidates;
3. Università degli Studi di Napoli Federico II — 5 candidates;
4. Università degli Studi di Palermo — 8 candidates;
5. Politecnico di Milano — 6 candidates.

Private component:

- Bocconi remains preferred over LUISS, but no Bocconi procedure should receive an `ACU-P2` ID until procedure-level call/commission/criteria/outcome chains are verified.
- LUISS remains a reserve/fallback, with stronger document-level fragments but weaker stable index structure.

---

## 2. Candidate procedure table by university

### 2.1 Sapienza Università di Roma

| Temporary candidate ID | University | Official source URL | Procedure title/reference | Type | Department/structure | GSD/SSD | Source environment | Chain class | Visible stages | Suitability | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P2-CAND-SAP-01 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/234489` | 2025RTDA1_1 | RTDA / researcher | Dipartimento di Scienze Giuridiche | GIUR-15/A | Amministrazione trasparente detail page | complete_chain | call; commission; criteria/preliminary minutes; interview notice; acts approval | high | Single-procedure detail page with complete official chain. |
| P2-CAND-SAP-02 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/232874` | 2025RTDA37_17 | RTDA / researcher | Dipartimento di Ingegneria Informatica, Automatica e Gestionale | IEGE-01/A | Amministrazione trasparente detail page | complete_chain | call; commission; preliminary minutes/criteria; acts approval | high | Strong single-procedure chain; technical/management engineering field. |
| P2-CAND-SAP-03 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/235779` | RTDA n. 1/2025 | RTDA / researcher | Dipartimento di Matematica Guido Castelnuovo | MATH-03/B; MATH-04/A | Amministrazione trasparente detail page | complete_chain | call; commission; preliminary minutes; criteria annex; shortlist; interview notice; acts approval | high | Rich chain and explicit project/profile text. |
| P2-CAND-SAP-04 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/235790` | 2025RTDA01/146 Polo Rieti | RTDA / researcher | Dipartimento di Psicologia dinamica clinica e salute | PSIC-04/A; PSIC-01/C | Amministrazione trasparente detail page | shared_call_chain | call; commission; preliminary minutes by SSD; interview notices; acts approval | medium-high | Useful shared/two-position case; requires careful sub-procedure attribution. |
| P2-CAND-SAP-05 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/233363` | 2025PAR001 | PA / second fascia | Multiple departments | multiple SSDs | Amministrazione trasparente shared call page | shared_call_chain | call; commission/criteria/acts appear by section where available | medium | Useful shared 14-position procedure; include only after identifying one clearly separable sub-procedure. |

### 2.2 Università degli Studi di Padova

| Temporary candidate ID | University | Official source URL | Procedure title/reference | Type | Department/structure | GSD/SSD | Source environment | Chain class | Visible stages | Suitability | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P2-CAND-PAD-01 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 1 | RTT | DSF | CHEM-07/A | Dedicated procedure page | complete_chain | call; commission; criteria; candidate list; judgments; scores/winner; acts approval | high | Complete chain and clean stage labels. |
| P2-CAND-PAD-02 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 2 | RTT | DISSGeA | GEOG-01/A | Dedicated procedure page | complete_chain | call; commission; criteria; candidate list; judgments; scores/winner; acts approval | high | Complete chain in same shared page. |
| P2-CAND-PAD-03 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 3 | RTT | DISSGeA | HIST-01/A | Dedicated procedure page | complete_chain | call; commission; criteria; candidate list; judgments; scores/winner; acts approval | high | Complete chain; good test of sub-position segmentation. |
| P2-CAND-PAD-04 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 4 | RTT | ICEA | IIND-03/B | Dedicated procedure page | complete_chain | call; commission; criteria; candidate list/convocation; judgments; scores/winner; acts approval | high | Complete engineering-related RTT chain. |
| P2-CAND-PAD-05 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 12 | RTT | Dipartimento di Scienze Statistiche | STAT-01/A; STAT-01/B | Dedicated procedure page | complete_chain | call; commission; criteria; candidate list; judgments; scores/winner; acts approval | high | Complete chain with two SSDs. |
| P2-CAND-PAD-06 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 13 | RTT | Dipartimento di Scienze Statistiche | STAT-02/A | Dedicated procedure page | complete_chain | call; commission; criteria; candidate list; judgments; scores/winner; acts approval | high | Complete chain; useful statistics/economics candidate. |

### 2.3 Università degli Studi di Napoli Federico II

| Temporary candidate ID | University | Official source URL | Procedure title/reference | Type | Department/structure | GSD/SSD | Source environment | Chain class | Visible stages | Suitability | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P2-CAND-NA-01 | Napoli Federico II | `https://www.unina.it/it/w/r2_rtt_2025_25-` | R2_RTT_2025_25 | RTT | Dipartimento di Scienze Chimiche | CHEM-02/A | Central procedure page | complete_chain | call; commission; criteria; admitted list; calendar; acts approval | high | Single procedure page with complete stage list. |
| P2-CAND-NA-02 | Napoli Federico II | `https://www.unina.it/it/w/r2_rtt_2025_26` | R2_RTT_2025_26 | RTT | Dipartimento di Scienze Chimiche | CHEM-03/A | Central procedure page | complete_chain | call; commission; criteria; admitted list; calendar; acts approval | high | Complete central Unina chain. |
| P2-CAND-NA-03 | Napoli Federico II | `https://www.unina.it/it/w/r2_rtt_2025_29` | R2_RTT_2025_29 | RTT | Dipartimento di Studi Umanistici | LIFI-01/A | Central procedure page | complete_chain | call; commission; criteria; admitted list; calendar; acts approval | high | Complete chain and humanities field. |
| P2-CAND-NA-04 | Napoli Federico II | `https://www.dises.unina.it/en_GB/web/guest/ateneo/concorsi/concorsi-docenti-e-ricercatori/reclutamento-ricercatori-a-tempo-determinato` | A1_RTT_2025_01 | RTT | Dipartimento di Scienze Sociali | GSPS-05/A | Departmental listing page | complete_chain | call; commission; criteria; admitted list; calendar; acts approval | medium-high | Good chain but source is long departmental listing; requires block segmentation. |
| P2-CAND-NA-05 | Napoli Federico II | `https://www.dises.unina.it/en_GB/web/guest/ateneo/concorsi/concorsi-docenti-e-ricercatori/reclutamento-ricercatori-a-tempo-determinato` | E1_RTT_2025_01 | RTT | Dipartimento di Scienze Sociali | GSPS-06/A | Departmental listing page | complete_chain | call; commission; criteria; admitted list/calendar; acts approval | medium-high | Complete chain; confirms need for `dises.unina.it` domain. |

### 2.4 Università degli Studi di Palermo

| Temporary candidate ID | University | Official source URL | Procedure title/reference | Type | Department/structure | GSD/SSD | Source environment | Chain class | Visible stages | Suitability | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P2-CAND-PA-01 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | 5 posti RTT — STAA-01/L | RTT | not yet isolated | STAA-01/L | Recruitment-office listing page | shared_call_chain | call; commission; criteria; oral notice; acts approval; final report | high | Complete chain in shared multi-position page. |
| P2-CAND-PA-02 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | 5 posti RTT — ECON-02/A | RTT | not yet isolated | ECON-02/A | Recruitment-office listing page | shared_call_chain | call; commission; criteria; oral notice; acts approval; final report | high | Complete chain; social-science field. |
| P2-CAND-PA-03 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | MEDS-07/A — Dip. PROMISE | RTT | PROMISE | MEDS-07/A | Recruitment-office listing page | complete_chain | call; commission; criteria; oral notice; acts approval; final report | high | Complete medical-field chain. |
| P2-CAND-PA-04 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | CEAR-08/D | RTT | not yet isolated | CEAR-08/D | Recruitment-office listing page | complete_chain | commission; criteria; oral notice; admitted notice; acts approval; final report | high | Complete chain with extra admitted-stage notice. |
| P2-CAND-PA-05 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | GIUR-04/A | RTT | not yet isolated | GIUR-04/A | Recruitment-office listing page | complete_chain | commission; criteria; oral notice; acts approval; final report | high | Complete legal-field chain. |
| P2-CAND-PA-06 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | ICHI-02/B | RTT | not yet isolated | ICHI-02/B | Recruitment-office listing page | complete_chain | commission; criteria; oral notice; acts approval; final report | high | Complete chain; technical/industrial chemistry field. |
| P2-CAND-PA-07 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | CEAR-02/A | RTT | not yet isolated | CEAR-02/A | Recruitment-office listing page | complete_chain | commission; criteria; oral notice; acts approval; final report | high | Complete engineering/environmental chain. |
| P2-CAND-PA-08 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | STAT-01/A | RTT | not yet isolated | STAT-01/A | Recruitment-office listing page | complete_chain | commission; criteria; oral notice; acts approval; relation/final report | high | Complete chain; includes statistical field and possible multi-post logic. |

### 2.5 Politecnico di Milano

| Temporary candidate ID | University | Official source URL | Procedure title/reference | Type | Department/structure | GSD/SSD | Source environment | Chain class | Visible stages | Suitability | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P2-CAND-POLI-01 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-22654` | 2025_RTDA_DABC_14 | RTDA / researcher | DABC | CEAR-08 | Dedicated procedure page | complete_chain | call; sorteggio; commission; first meeting; acts approval; final verbale | high | Very clean technical-source chain. |
| P2-CAND-POLI-02 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-22659` | 2025_RTDA_DMEC_17 | RTDA / researcher | Dipartimento di Meccanica | IMIS-01 | Dedicated procedure page | complete_chain | call; sorteggio; commission; meeting request; acts approval; verbale | high | Complete chain in mechanical engineering field. |
| P2-CAND-POLI-03 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-22642` | 2025_RTDA_DIG_14 | RTDA / researcher | Dipartimento di Ingegneria Gestionale | IIND-05 | Dedicated procedure page | complete_chain | call; sorteggio; commission; first verbale; acts approval | high | Complete chain with date anomaly in page metadata, useful for robustness. |
| P2-CAND-POLI-04 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-22450` | 2025_RTDA_DABC_4 | RTDA / researcher | DABC | CEAR-08 | Dedicated procedure page | complete_chain | call; sorteggio; commission; first meeting; acts approval | high | Clean chain with bilingual call naming. |
| P2-CAND-POLI-05 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-21610` | 2024_RTDA_DAER_10 | RTDA / researcher | not yet isolated | IIND-01 | Dedicated procedure page | complete_chain | call; sorteggio; commission; first meeting; acts approval; final pages | high | Complete archived chain; useful for aerospace/naval engineering profile. |
| P2-CAND-POLI-06 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-23082` | 2025_RTT_DABC_19 | RTT | DABC | CEAR-07 | Dedicated procedure page | partial_chain | call visible; later stages not yet visible in checked page | medium | Useful partial/open-chain control case; include only if a difficult-chain reserve is needed. |

---

## 3. Private-university assessment

### Bocconi

Candidate status:

```text
private_probe_pending
```

Bocconi has an official concorsi landing page for L. 240/2010 categories and an Assistant Professors L. 240/2010 page, but procedure-level call/commission/criteria/outcome chains were not sufficiently exposed in the checked public pages to assign `ACU-P2` IDs at this stage.

Recommendation:

- keep Bocconi as preferred private candidate;
- run a targeted follow-up verification on the linked international faculty-recruiting pages;
- only initialise Bocconi `ACU-P2` IDs if at least 4 procedure chains expose call/commission/criteria/outcome evidence.

### LUISS

Candidate status:

```text
reserve_private_fallback
```

LUISS exposes official procedure PDFs and verbali, including art. 18 procedure material, but the source environment is fragmented and does not yet provide a stable procedure-level index comparable to the public universities.

Recommendation:

- keep LUISS as reserve;
- add `api.luiss.it` only if LUISS is reactivated as private fallback;
- do not include LUISS in the first `ACU-P2` initialisation batch.

---

## 4. Recommended final selection for ID initialisation

Recommended first phase-2 initialisation batch:

| University | Candidate IDs | Count | Recommendation |
|---|---|---:|---|
| Sapienza | P2-CAND-SAP-01 to P2-CAND-SAP-05 | 5 | initialise after reviewing SAP-05 shared-call segmentation |
| Padova | P2-CAND-PAD-01 to P2-CAND-PAD-06 | 6 | initialise |
| Napoli Federico II | P2-CAND-NA-01 to P2-CAND-NA-05 | 5 | initialise after domain update confirmation |
| Palermo | P2-CAND-PA-01 to P2-CAND-PA-08 | 8 | initialise, but segment long listing carefully |
| Politecnico di Milano | P2-CAND-POLI-01 to P2-CAND-POLI-05 | 5 | initialise |
| Politecnico difficult reserve | P2-CAND-POLI-06 | 1 | reserve/partial-chain test |
| Bocconi | none yet | 0 | private probe pending |

Recommended core initialisation count:

```text
29 high/medium-high candidates + 1 partial-chain reserve = 30 total candidates
```

Do not initialise Bocconi or LUISS IDs yet.

---

## 5. Procedure-type distribution

Approximate distribution for the proposed 30 candidates:

| Type | Count | Notes |
|---|---:|---|
| RTT / tenure-track researcher | 19 | Padova, Napoli, Palermo, Polimi partial reserve. |
| RTDA / researcher legacy-type | 9 | Sapienza and Polimi. |
| PA / second fascia | 2 | Sapienza shared PA procedure plus possible LUISS reserve not yet initialised. |
| PO / first fascia | 0 | Not yet sufficiently represented; should be added in the next tranche. |

This distribution is researcher-heavy. It is acceptable for the first phase-2 initialisation tranche, but the second tranche should deliberately add PA/PO procedures.

---

## 6. Document-chain distribution

| Chain class | Count | Notes |
|---|---:|---|
| complete_chain | 25 | Main phase-2 backbone. |
| shared_call_chain | 4 | Sapienza shared call, Palermo shared RTT blocks, Padova shared page logic. |
| partial_chain | 1 | Polimi 2025_RTT_DABC_19 as difficult-chain reserve. |
| noisy_pdf_chain | 0 explicitly pre-classified | To be reassessed after document opening/OCR. |
| private_source_chain | 0 selected for IDs | Private probe pending. |

---

## 7. Exclusions and reserves

| Candidate | Status | Reason |
|---|---|---|
| Bocconi L. 240/2010 recruitment pages | private_probe_pending | Source landing page visible, but procedure-level chains not yet confirmed. |
| LUISS art. 18 / L. 240 PDFs | reserve_private_fallback | Official PDFs visible, but stable index and chain completeness are weaker. |
| Generic PICA pages | excluded_as_primary_source | Application portal, not primary official evidence source for this golden dataset stage. |

---

## 8. Recommended next action

Create a follow-up issue to initialise only the 30 selected candidate procedures as empty phase-2 workspace entries, without coding substantive layers yet.

Before initialisation:

1. confirm `dises.unina.it` is allowed;
2. decide whether to include P2-CAND-POLI-06 as the one partial-chain reserve;
3. review SAP-05 to avoid over-broad shared-call attribution;
4. keep Bocconi/LUISS out of the first initialisation batch.

---

## 9. Final recommendation

Status:

```text
ready_for_acu_p2_initialisation_public_batch
```

Not yet authorised:

```text
ready_for_private_university_batch
ready_for_bulk_coding
ready_for_public_scoring
ready_for_external_enrichment
ready_for_automated_crawling
```
