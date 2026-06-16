# Loom Progress Ledger

Project-specific completion ledger for BOMFlow. This root file is the project cockpit: snapshot, phase status, next score-changing actions, decisions, and open questions.

## Project Snapshot

**Project:** bomflow  
**Date:** 2026-06-16  
**Owner:** John Hightshue + Codex  
**Current Focus:** Phase 2 Requirements  
**Total Complete:** 14%  
**Calculation Basis:** Equal phase weights; Discovery is complete and all later phases are unopened.

## Top-Level Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Discovery | 100% | 1 | [Discovery Progress](phases/01-discovery/PROGRESS.md) | Complete; ready for Requirements. |
| Requirements | 0% | 1 | Requirements Progress | Not started. |
| Architecture | 0% | 1 | Architecture Progress | Not started. |
| Planning & Decomposition | 0% | 1 | Planning Progress | Not started. |
| Contracts & Tests | 0% | 1 | Contracts & Tests Progress | Not started. |
| Implementation | 0% | 1 | Implementation Progress | Not started. |
| Review & Retrospective | 0% | 1 | Review Progress | Not started. |
| **Phase Total** | **14%** | | | Rounded from 100 / 700. |

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
| Discovery | Phase | Project | 100% | Complete; ready for Requirements | [Progress](phases/01-discovery/PROGRESS.md) | Complete |
| Requirements | Phase | Project | 0% | Convert Discovery handoff into requirements | TBD | Next |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Create Requirements phase artifact and progress ledger | Requirements | Opens Phase 2 and preserves Discovery handoff continuity | John + Codex |

## Decisions and Adjustments

| Date | Scope | Change | Reason | Owner |
|------|-------|--------|--------|-------|
| 2026-06-12 | Project | Renamed working project to BOMFlow | The artifact should stand on its own as a hardware workflow automation project. | John |
| 2026-06-16 | Discovery | Replaced lettered roadmap shorthand with descriptive roadmap parts | Discovery should use stable product language before Requirements. | John + Codex |
| 2026-06-16 | Discovery | Chose hardware engineer as primary user for the BOM Carbon Report | Public AllSpice product/docs context points to automation supporting hardware design review. | John + Codex |
| 2026-06-16 | Discovery | Chose BOM Carbon Report as the full first useful version | Keeps Requirements focused while preserving later roadmap extensions. | John |
| 2026-06-16 | Discovery | Chose review-ready report shape for the first version | Gives Requirements concrete output sections while leaving compliance-style reporting as future state. | John |
| 2026-06-16 | Discovery | Scoped Design Review Delta and Integration Handoff as future mini-Loom cycles | Keeps the product arc visible without creating current MVP requirements. | John |
| 2026-06-16 | Discovery | Closed Discovery phase gate | Discovery has enough context to hand off cleanly to Requirements. | John + Codex |

## Open Progress Questions

| Scope | Question | Needed To Score Accurately | Owner |
|-------|----------|----------------------------|-------|
| Requirements | What acceptance criteria should define a useful BOM Carbon Report? | Requirements scope and validation | John + Codex |
