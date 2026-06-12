# Loom Progress Ledger

Project-specific completion ledger for BOMFlow. This root file is the project cockpit: snapshot, phase status, next score-changing actions, decisions, and open questions.

## Project Snapshot

**Project:** bomflow  
**Date:** 2026-06-12  
**Owner:** John Hightshue + Codex  
**Current Focus:** Phase 1 Discovery  
**Total Complete:** 3%  
**Calculation Basis:** Equal phase weights; Discovery is in progress and all later phases are unopened.

## Top-Level Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Discovery | 20% | 1 | [Discovery Progress](phases/01-discovery/PROGRESS.md) | Initial direction captured; user/problem validation still open. |
| Requirements | 0% | 1 | Requirements Progress | Not started. |
| Architecture | 0% | 1 | Architecture Progress | Not started. |
| Planning & Decomposition | 0% | 1 | Planning Progress | Not started. |
| Contracts & Tests | 0% | 1 | Contracts & Tests Progress | Not started. |
| Implementation | 0% | 1 | Implementation Progress | Not started. |
| Review & Retrospective | 0% | 1 | Review Progress | Not started. |
| **Phase Total** | **3%** | | | Rounded from 20 / 700. |

## Scope Inventory

| Scope | Type | Parent | Source Evidence | Progress Doc | Intended Source Path | Intended Test Path | Inclusion Decision |
|-------|------|--------|-----------------|--------------|----------------------|--------------------|--------------------|
| Discovery | Phase | Project | [Discovery README](phases/01-discovery/README.md) | `phases/01-discovery/PROGRESS.md` | N/A | N/A | Included |
| Requirements | Phase | Project | Not started | TBD | N/A | N/A | Included later |
| Architecture | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Planning & Decomposition | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Contracts & Tests | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Implementation | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Review & Retrospective | Phase | Project | Not started | TBD | N/A | N/A | Included later |

## Progress Tree Index

| Scope | Type | Parent | Total | Current Focus | Progress Doc | Notes |
|-------|------|--------|-------|---------------|--------------|-------|
| Discovery | Phase | Project | 20% | Clarify problem, users, first useful version, and validation | [Progress](phases/01-discovery/PROGRESS.md) | Active |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Finish Discovery problem statement and first-user framing | Discovery | Moves Discovery toward phase gate readiness | John + Codex |
| Decide whether A/B/C are one project roadmap or separate Loom cycles | Discovery | Clarifies first useful version and out-of-scope boundaries | John |
| Capture validation evidence needed before Requirements | Discovery | Defines quality gate for moving forward | John + Codex |

## Decisions and Adjustments

| Date | Scope | Change | Reason | Owner |
|------|-------|--------|--------|-------|
| 2026-06-12 | Project | Renamed working project from allspice to bomflow | The project is for an AllSpice role, but the artifact should stand on its own. | John |
| 2026-06-12 | Process | Removed premature implementation spike | BOMFlow should begin with Loom Discovery before implementation. | John + Codex |

## Open Progress Questions

| Scope | Question | Needed To Score Accurately | Owner |
|-------|----------|----------------------------|-------|
| Discovery | Who is the first primary operator: hardware engineer, forward-deployed engineer, or sustainability/compliance reviewer? | Primary user framing | John |
| Discovery | Is A the full first useful version, or only a spike inside a larger A/B/C story? | First useful version boundary | John + Codex |
| Discovery | What evidence should this create for a portfolio or hiring review? | Success criteria and validation | John |
