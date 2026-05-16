# 01 — Agentic loop governance policy

## 1. Governance objective

The agentic loop must increase procedural reliability, not substantive aggressiveness.

Its function is to make repository operations traceable, repeatable and validated while preserving the cautious evidentiary posture of the Atlante dei Concorsi Universitari project.

## 2. Non-negotiable safeguards

The loop must never produce or imply:

- confirmed conflicts of interest;
- corruption findings;
- rigging findings;
- illegality findings;
- reputational accusations;
- public risk classifications of named people or procedures.

The repository may document public procedure information, source traces, coding uncertainty, methodological limits and review needs.

## 3. Evidence standard

Every substantive coded field must be traceable to a source document, source URL or documented search path.

Where evidence is incomplete, the loop must use conservative values such as:

- `not_determinable`;
- `low` confidence;
- `human_review_required=true`;
- `pending` review status.

Absence of evidence must not be treated as evidence of absence unless the search path is explicitly documented and the codebook permits that interpretation.

## 4. Source expansion

New source domains, university sections or automated collection methods require explicit approval.

The loop may record a proposed source expansion as a blocker. It must not silently expand the collection perimeter.

## 5. Relation coding

The loop must not infer sensitive relations from weak evidence.

In particular:

- similar names are not sufficient;
- same affiliation is not sufficient;
- coauthorship is not automatically a conflict;
- shared academic field is not a conflict;
- relation coding must remain descriptive and evidence-based.

## 6. Publication boundary

The golden dataset and pilot materials are internal unless a separate publication workflow is explicitly approved.

Agentic runs must not generate public-facing conclusions from pilot material.

## 7. Review gates

Human review is mandatory when:

- identity matching is uncertain;
- relation evidence is weak or sensitive;
- documents conflict;
- a procedure is ongoing;
- the next step could affect reputational interpretation;
- the agent proposes a taxonomy or schema change;
- validation fails in a way that cannot be mechanically corrected.

## 8. Auditability

Each run must leave enough trace for a reviewer to answer:

1. What did the agent read?
2. What did it decide?
3. Which files did it modify?
4. Which validation checks passed or failed?
5. Why did it continue or stop?
6. What requires human judgement?
