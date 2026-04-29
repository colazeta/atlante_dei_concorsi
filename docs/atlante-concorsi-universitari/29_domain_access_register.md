# 29 — Domain access register and source-expansion protocol

## 1) Purpose

This document records the web domains that the Atlante dei Concorsi Universitari project is allowed to access during controlled source expansion.

It has two functions:

1. act as an audit register of domains already approved for Codex/cloud-agent access;
2. define the approval gate that must be followed before a new university or source family is added to the browsing perimeter.

This is **not** a registry of all sources used as evidence in the dataset. Source-level evidence must still be recorded in the relevant source registry, procedure files, document tables, review notes, and QA outputs.

## 2) Core rule

The agent must **not** expand the allowed browsing perimeter autonomously.

When a task requires access to a domain that is not already allowed, the agent must stop and propose the domain for human approval before relying on that source.

The proposal must include:

- domain requested;
- university or institution to which the domain belongs;
- reason for access;
- expected source type, for example call page, transparency portal, PDF archive, albo pretorio, procedure page, document repository;
- example URL, where available;
- whether the domain is official, institutional, or third-party;
- proposed HTTP methods, normally `GET`, `HEAD`, `OPTIONS` only;
- risk notes, including redirects, mixed domains, login walls, or unclear ownership.

The agent must not bypass domain restrictions through mirrors, cached copies, search-result snippets, URL shorteners, scraping proxies, or generic archival services unless these are explicitly approved as separate domains.

## 3) Approval workflow for a new expansion

Before starting a new university/source expansion, follow this sequence:

1. Identify candidate universities or source families.
2. Identify the minimum set of domains required to access official or public documentation.
3. Check this register to determine whether each domain is already approved.
4. For every new domain, prepare a domain-access request table.
5. Wait for human approval.
6. Only after approval, update the Codex cloud environment allowlist.
7. Update this register in the same repository change or in the immediately following documentation change.
8. Continue collection/coding only for approved domains.

If a domain is rejected or deferred, the task must document the limitation and avoid treating non-access as evidence of absence.

## 4) Domain request template

Use this table whenever a new expansion requires additional domains.

| Requested domain | University / institution | Official status | Source type | Example URL | Reason for access | Proposed HTTP methods | Risk notes | Decision | Approved by | Decision date |
|---|---|---:|---|---|---|---|---|---|---|---|
| `example.university.it` | Example University | Official | Call/procedure archive | `https://example.university.it/...` | Needed to retrieve procedure pages and documents | `GET`, `HEAD`, `OPTIONS` | None identified | Proposed |  |  |

Decision values:

- `Proposed`: identified by the agent but not yet approved;
- `Approved`: approved for inclusion in the Codex environment allowlist;
- `Rejected`: not approved;
- `Deferred`: not decided yet;
- `Deprecated`: previously approved but no longer needed.

## 5) Approved domain register

Initial register based on the project environment configuration currently used for the first controlled expansion.

| Domain | University / institution | Official status | Source type | Scope of use | HTTP methods | Status | Approved by | Approval date | Notes |
|---|---|---:|---|---|---|---|---|---|---|
| `unibo.it` | University of Bologna | Official | Main institutional domain | General university pages and redirects related to recruitment procedures | `GET`, `HEAD`, `OPTIONS` | Approved | Project lead | 2026-04-29 | Use only when required by official procedure navigation. |
| `www.unibo.it` | University of Bologna | Official | Main institutional website | Recruitment pages, notices, institutional information and linked procedure material | `GET`, `HEAD`, `OPTIONS` | Approved | Project lead | 2026-04-29 | Prefer specific official pages over broad crawling. |
| `bandi.unibo.it` | University of Bologna | Official | Calls/procedure portal | Calls, procedure pages, attachments and related public documents | `GET`, `HEAD`, `OPTIONS` | Approved | Project lead | 2026-04-29 | Primary domain for Bologna procedure evidence. |
| `unical.it` | University of Calabria | Official | Main institutional domain | General university pages and recruitment-related redirects | `GET`, `HEAD`, `OPTIONS` | Approved | Project lead | 2026-04-29 | Use only when needed for official navigation or source verification. |
| `unical-portaleamministrazionetrasparente.it` | University of Calabria | Official / administration-transparency portal | Transparency and procedure-document portal | Public recruitment documentation, transparency records and attachments | `GET`, `HEAD`, `OPTIONS` | Approved | Project lead | 2026-04-29 | Primary domain for Calabria transparency evidence. |

## 6) Pending domain requests

Add future requests here before enabling new domains in the Codex environment.

| Requested domain | University / institution | Official status | Source type | Example URL | Reason for access | Proposed HTTP methods | Risk notes | Decision | Approved by | Decision date |
|---|---|---:|---|---|---|---|---|---|---|---|

## 7) Minimum documentation after approval

For every approved domain, subsequent data-collection work must record:

- the exact URL used;
- retrieval date;
- procedure or evidence item linked to the source;
- whether the page was used as a source page, document container, or direct evidence;
- any redirects or cross-domain dependencies;
- whether the source was accessible without login;
- any uncertainty affecting source interpretation.

## 8) Safety and methodological constraints

Domain access does not authorise broad scraping.

The pilot remains conservative and evidence-preserving:

- access only public or official material;
- avoid large-scale scraping unless a separate ingestion protocol is approved;
- do not infer wrongdoing from source availability, domain structure, missing pages, redirects, or archive gaps;
- do not treat inability to access a domain as substantive evidence;
- keep all claims traceable to source URLs and documents;
- preserve neutral language and uncertainty labels.

## 9) Recommended Codex environment setting

For controlled university-source expansion, the recommended network posture is:

```text
Agent internet access: enabled only for the approved allowlist
Allowed domains: approved domains in this register
Allowed HTTP methods: GET, HEAD, OPTIONS
Approval policy: never, only within workspace and approved network perimeter
Sandbox: workspace-write
```

This keeps the agent operationally autonomous inside the repository while preserving human control over the external-source perimeter.
