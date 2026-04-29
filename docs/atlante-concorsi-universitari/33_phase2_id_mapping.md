# 33 — Phase 2 ID mapping

## Purpose

This note records the stable `ACU-P2` ID assignment for the 30 selected public-batch phase-2 candidate procedures listed in `docs/atlante-concorsi-universitari/32_phase2_candidate_procedure_list.md`.

Scope limits applied in this step:

- ID mapping only;
- optional empty workspace initialisation;
- no procedure-layer coding;
- no CSV population or enrichment.

---

## Mapping table

| Temporary candidate ID | Assigned ACU-P2 ID | University | Official source URL | Procedure title/reference | Procedure type | Document-chain class | Core/reserve | Caution note |
|---|---|---|---|---|---|---|---|---|
| P2-CAND-SAP-01 | ACU-P2-0001 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/234489` | 2025RTDA1_1 | RTDA / researcher | complete_chain | core | None. |
| P2-CAND-SAP-02 | ACU-P2-0002 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/232874` | 2025RTDA37_17 | RTDA / researcher | complete_chain | core | None. |
| P2-CAND-SAP-03 | ACU-P2-0003 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/235779` | RTDA n. 1/2025 | RTDA / researcher | complete_chain | core | None. |
| P2-CAND-SAP-04 | ACU-P2-0004 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/235790` | 2025RTDA01/146 Polo Rieti | RTDA / researcher | shared_call_chain | core | Shared/two-position context; keep sub-procedure attribution explicit during coding. |
| P2-CAND-SAP-05 | ACU-P2-0005 | Sapienza | `https://web.uniroma1.it/trasparenza/dettaglio_bando_albo/233363` | 2025PAR001 | PA / second fascia | shared_call_chain | core | Shared 14-position call; isolate one clearly separable sub-procedure. |
| P2-CAND-PAD-01 | ACU-P2-0006 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 1 | RTT | complete_chain | core | Shared source page; keep position-level segmentation. |
| P2-CAND-PAD-02 | ACU-P2-0007 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 2 | RTT | complete_chain | core | Shared source page; keep position-level segmentation. |
| P2-CAND-PAD-03 | ACU-P2-0008 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 3 | RTT | complete_chain | core | Shared source page; keep position-level segmentation. |
| P2-CAND-PAD-04 | ACU-P2-0009 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 4 | RTT | complete_chain | core | Shared source page; keep position-level segmentation. |
| P2-CAND-PAD-05 | ACU-P2-0010 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 12 | RTT | complete_chain | core | Shared source page; keep position-level segmentation. |
| P2-CAND-PAD-06 | ACU-P2-0011 | Padova | `https://www.unipd.it/procedura-2025RTT01` | 2025RTT01 — pos. 13 | RTT | complete_chain | core | Shared source page; keep position-level segmentation. |
| P2-CAND-NA-01 | ACU-P2-0012 | Napoli Federico II | `https://www.unina.it/it/w/r2_rtt_2025_25-` | R2_RTT_2025_25 | RTT | complete_chain | core | None. |
| P2-CAND-NA-02 | ACU-P2-0013 | Napoli Federico II | `https://www.unina.it/it/w/r2_rtt_2025_26` | R2_RTT_2025_26 | RTT | complete_chain | core | None. |
| P2-CAND-NA-03 | ACU-P2-0014 | Napoli Federico II | `https://www.unina.it/it/w/r2_rtt_2025_29` | R2_RTT_2025_29 | RTT | complete_chain | core | None. |
| P2-CAND-NA-04 | ACU-P2-0015 | Napoli Federico II | `https://www.dises.unina.it/en_GB/web/guest/ateneo/concorsi/concorsi-docenti-e-ricercatori/reclutamento-ricercatori-a-tempo-determinato` | A1_RTT_2025_01 | RTT | complete_chain | core | Long departmental listing; segment the correct procedure block only. |
| P2-CAND-NA-05 | ACU-P2-0016 | Napoli Federico II | `https://www.dises.unina.it/en_GB/web/guest/ateneo/concorsi/concorsi-docenti-e-ricercatori/reclutamento-ricercatori-a-tempo-determinato` | E1_RTT_2025_01 | RTT | complete_chain | core | Long departmental listing; segment the correct procedure block only. |
| P2-CAND-PA-01 | ACU-P2-0017 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | 5 posti RTT — STAA-01/L | RTT | shared_call_chain | core | Shared multi-position listing; keep SSD-specific boundaries explicit. |
| P2-CAND-PA-02 | ACU-P2-0018 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | 5 posti RTT — ECON-02/A | RTT | shared_call_chain | core | Shared multi-position listing; keep SSD-specific boundaries explicit. |
| P2-CAND-PA-03 | ACU-P2-0019 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | MEDS-07/A — Dip. PROMISE | RTT | complete_chain | core | Listing-page chain; ensure block-level separation from adjacent procedures. |
| P2-CAND-PA-04 | ACU-P2-0020 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | CEAR-08/D | RTT | complete_chain | core | Listing-page chain; ensure block-level separation from adjacent procedures. |
| P2-CAND-PA-05 | ACU-P2-0021 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | GIUR-04/A | RTT | complete_chain | core | Listing-page chain; ensure block-level separation from adjacent procedures. |
| P2-CAND-PA-06 | ACU-P2-0022 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | ICHI-02/B | RTT | complete_chain | core | Listing-page chain; ensure block-level separation from adjacent procedures. |
| P2-CAND-PA-07 | ACU-P2-0023 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | CEAR-02/A | RTT | complete_chain | core | Listing-page chain; ensure block-level separation from adjacent procedures. |
| P2-CAND-PA-08 | ACU-P2-0024 | Palermo | `https://www.unipa.it/amministrazione/arearisorseumane/settorereclutamentoeselezioni/Docenti/RicercatoriTD/index.html` | STAT-01/A | RTT | complete_chain | core | Listing-page chain with possible multi-post logic; isolate target block. |
| P2-CAND-POLI-01 | ACU-P2-0025 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-22654` | 2025_RTDA_DABC_14 | RTDA / researcher | complete_chain | core | None. |
| P2-CAND-POLI-02 | ACU-P2-0026 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-22659` | 2025_RTDA_DMEC_17 | RTDA / researcher | complete_chain | core | None. |
| P2-CAND-POLI-03 | ACU-P2-0027 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-22642` | 2025_RTDA_DIG_14 | RTDA / researcher | complete_chain | core | Page metadata date anomaly noted in candidate list; keep evidence chain document-led. |
| P2-CAND-POLI-04 | ACU-P2-0028 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-22450` | 2025_RTDA_DABC_4 | RTDA / researcher | complete_chain | core | None. |
| P2-CAND-POLI-05 | ACU-P2-0029 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-21610` | 2024_RTDA_DAER_10 | RTDA / researcher | complete_chain | core | Archived procedure page; keep stage ordering as published. |
| P2-CAND-POLI-06 | ACU-P2-0030 | Politecnico di Milano | `https://www.polimi.it/docenti-e-ricercatori/bandi-e-concorsi/bandi-e-concorsi-per-ricercatori/concorsi-a-tempo-determinato/r-d-23082` | 2025_RTT_DABC_19 | RTT | partial_chain | reserve | Partial-chain reserve case; call visible while later stages may still be pending publication. |

---

## Initialisation status

- Mapping note created and tracked in git.
- No procedure-level coding performed in this step.
- No CSV data population performed in this step.
