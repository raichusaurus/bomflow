# Loom Progress Ledger

Project-specific completion ledger for BOMFlow. This root file is the project cockpit: snapshot, phase status, next score-changing actions, decisions, and open questions.

## Project Snapshot

**Project:** bomflow  
**Date:** 2026-06-24  
**Owner:** John Hightshue + Codex  
**Current Focus:** Phase 3 Architecture  
**Total Complete:** 29%  
**Calculation Basis:** Equal phase weights; Discovery and Requirements are complete, and later phases are unopened.

## Top-Level Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Discovery | 100% | 1 | [Discovery Progress](phases/01-discovery/PROGRESS.md) | Complete; ready for Requirements. |
| Requirements | 100% | 1 | [Requirements Progress](phases/02-requirements/PROGRESS.md) | Complete; ready for Architecture. |
| Architecture | 0% | 1 | Architecture Progress | Not started. |
| Planning & Decomposition | 0% | 1 | Planning Progress | Not started. |
| Contracts & Tests | 0% | 1 | Contracts & Tests Progress | Not started. |
| Implementation | 0% | 1 | Implementation Progress | Not started. |
| Review & Retrospective | 0% | 1 | Review Progress | Not started. |
| **Phase Total** | **29%** | | | Rounded from 200 / 700. |

## Scope Inventory

| Scope | Type | Parent | Source Evidence | Progress Doc | Intended Source Path | Intended Test Path | Inclusion Decision |
|-------|------|--------|-----------------|--------------|----------------------|--------------------|--------------------|
| Discovery | Phase | Project | [Discovery README](phases/01-discovery/README.md) | `phases/01-discovery/PROGRESS.md` | N/A | N/A | Included |
| Requirements | Phase | Project | [Requirements README](phases/02-requirements/README.md) | `phases/02-requirements/PROGRESS.md` | N/A | N/A | Included |
| Architecture | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Planning & Decomposition | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Contracts & Tests | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Implementation | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Review & Retrospective | Phase | Project | Not started | TBD | N/A | N/A | Included later |

## Progress Tree Index

| Scope | Type | Parent | Total | Current Focus | Progress Doc | Notes |
|-------|------|--------|-------|---------------|--------------|-------|
| Discovery | Phase | Project | 100% | Complete; ready for Requirements | [Progress](phases/01-discovery/PROGRESS.md) | Complete |
| Requirements | Phase | Project | 100% | Complete; ready for Architecture | [Progress](phases/02-requirements/PROGRESS.md) | Complete |
| Architecture | Phase | Project | 0% | Start Architecture from Requirements handoff | TBD | Next |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Create Architecture phase artifact and progress ledger | Architecture | Opens Phase 3 and converts requirements into implementation structure | John + Codex |

## Decisions and Adjustments

| Date | Scope | Change | Reason | Owner |
|------|-------|--------|--------|-------|
| 2026-06-12 | Project | Renamed working project to BOMFlow | The artifact should stand on its own as a hardware workflow automation project. | John |
| 2026-06-16 | Discovery | Replaced lettered roadmap shorthand with descriptive roadmap parts | Discovery should use stable product language before Requirements. | John + Codex |
| 2026-06-16 | Discovery | Chose hardware engineer as primary user for the BOM Carbon Report | Hardware workflow automation context points to design-review support as the clearest first-user lens. | John + Codex |
| 2026-06-16 | Discovery | Chose BOM Carbon Report as the full first useful version | Keeps Requirements focused while preserving later roadmap extensions. | John |
| 2026-06-16 | Discovery | Chose review-ready report shape for the first version | Gives Requirements concrete output sections while leaving compliance-style reporting as future state. | John |
| 2026-06-16 | Discovery | Scoped Design Review Delta and Integration Handoff as future mini-Loom cycles | Keeps the product arc visible without creating current MVP requirements. | John |
| 2026-06-16 | Discovery | Closed Discovery phase gate | Discovery has enough context to hand off cleanly to Requirements. | John + Codex |
| 2026-06-24 | Requirements | Opened Requirements phase with draft requirements and progress ledger | Converts Discovery handoff into functional requirements, non-functional requirements, acceptance criteria, and scope boundaries. | John + Codex |
| 2026-06-24 | Requirements | Chose JSON as the first durable report artifact | Keeps the report model structured, frontend-ready, testable, and suitable for future integration handoff. | John |
| 2026-06-24 | Requirements | Chose both line-item and category contributor rankings | Line items give hardware engineers exact parts to inspect; categories show design-level impact patterns. | John |
| 2026-06-24 | Requirements | Chose a canonical mixed-case IoT sensor BOM as the first acceptance fixture | Gives Architecture, tests, and implementation a representative target while leaving broader fixture coverage for Contracts & Tests. | John |
| 2026-06-24 | Loom Process | Captured reusable phase-template feedback | Documents gate authority, phase decision logs, agent authority, artifact vs gate completion, next-phase handoff, and process-feedback capture as general Loom improvements. | John + Codex |
| 2026-06-24 | Requirements | Closed Requirements phase gate | Owner approved the Requirements handoff to Architecture. | John |

## Open Progress Questions

| Scope | Question | Needed To Score Accurately | Owner |
|-------|----------|----------------------------|-------|
| Architecture | What module boundaries, data model, and local execution shape should implement the JSON-first BOM Carbon Report? | Architecture scope and validation | John + Codex |
