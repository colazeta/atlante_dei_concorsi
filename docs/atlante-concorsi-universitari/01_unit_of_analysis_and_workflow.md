# 01 — Unit of analysis and expected workflow

## Main unit of analysis
The main unit is the **procedure** (`procedure_id`), not the individual document.
A procedure may include multiple positions, multiple document versions, committee appointments, criteria, minutes, outcomes, and later updates.

## Expected procedural workflow (generic)
1. call/bando;
2. possible correction or extension;
3. appointment of committee;
4. publication of criteria, if available;
5. list of admitted/excluded candidates, if available;
6. evaluation minutes;
7. final ranking or outcome;
8. approval of acts;
9. possible correction, annulment, litigation-related document, or later update.

## Status conventions
Suggested values for `status`:
- `announced`
- `in_progress`
- `outcome_published`
- `acts_approved`
- `updated_after_approval`
- `annulled`
- `not_determinable`

## Synthetic example (fictional, non-real)
> **Synthetic example — fictional names only**
>
> `procedure_id`: SYN-UNI-2026-001  
> `university`: Università Tirrena di Studi Avanzati  
> `department`: Dipartimento di Scienze Documentarie  
> `position_type`: ricercatore_tenure_track  
> `number_of_positions`: 1  
> Documents attached to this same procedure include: `call_notice`, `committee_appointment`, `evaluation_criteria`, `minutes`, `final_ranking`, `acts_approval`.  
> Committee member (fictional): Prof. Elena Valli. Candidate (fictional): Dott. Marco Liri.
