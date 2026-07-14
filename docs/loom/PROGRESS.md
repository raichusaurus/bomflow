# Loom Progress Ledger

Project-specific completion ledger for BOMFlow. This root file is the project cockpit: snapshot, phase status, next score-changing actions, decisions, and open questions.

## Project Snapshot

**Project:** bomflow  
**Date:** 2026-07-13  
**Owner:** John Hightshue + Codex  
**Current Focus:** Phase 5 Contracts & Tests  
**Total Complete:** 57%  
**Calculation Basis:** Equal phase weights; Discovery, Requirements, Architecture, and Planning & Decomposition are complete, and later phases are unopened.

## Top-Level Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Discovery | 100% | 1 | [Discovery Progress](phases/01-discovery/PROGRESS.md) | Complete; ready for Requirements. |
| Requirements | 100% | 1 | [Requirements Progress](phases/02-requirements/PROGRESS.md) | Complete; ready for Architecture. |
| Architecture | 100% | 1 | [Architecture Progress](phases/03-architecture/PROGRESS.md) | Complete; ready for Planning & Decomposition. |
| Planning & Decomposition | 100% | 1 | [Planning Progress](phases/04-planning-decomposition/PROGRESS.md) | Complete; ready for Contracts & Tests. |
| Contracts & Tests | 0% | 1 | Contracts & Tests Progress | Not started. |
| Implementation | 0% | 1 | Implementation Progress | Not started. |
| Review & Retrospective | 0% | 1 | Review Progress | Not started. |
| **Phase Total** | **57%** | | | Rounded from 400 / 700. |

## Scope Inventory

| Scope | Type | Parent | Source Evidence | Progress Doc | Intended Source Path | Intended Test Path | Inclusion Decision |
|-------|------|--------|-----------------|--------------|----------------------|--------------------|--------------------|
| Discovery | Phase | Project | [Discovery README](phases/01-discovery/README.md) | `phases/01-discovery/PROGRESS.md` | N/A | N/A | Included |
| Requirements | Phase | Project | [Requirements README](phases/02-requirements/README.md) | `phases/02-requirements/PROGRESS.md` | N/A | N/A | Included |
| Architecture | Phase | Project | [Architecture README](phases/03-architecture/README.md) | `phases/03-architecture/PROGRESS.md` | `bomflow/` package, `data/fixtures/`, `data/catalogs/`, `reports/`, `.github/workflows/` | `tests/` | Included |
| Planning & Decomposition | Phase | Project | [Planning README](phases/04-planning-decomposition/README.md) | `phases/04-planning-decomposition/PROGRESS.md` | `bomflow/` package, `data/fixtures/`, `data/catalogs/`, `reports/`, `.github/workflows/`, future `web/` | `tests/`, optional `schemas/` | Included |
| Contracts & Tests | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Implementation | Phase | Project | Not started | TBD | TBD | TBD | Included later |
| Review & Retrospective | Phase | Project | Not started | TBD | N/A | N/A | Included later |

## Progress Tree Index

| Scope | Type | Parent | Total | Current Focus | Progress Doc | Notes |
|-------|------|--------|-------|---------------|--------------|-------|
| Discovery | Phase | Project | 100% | Complete; ready for Requirements | [Progress](phases/01-discovery/PROGRESS.md) | Complete |
| Requirements | Phase | Project | 100% | Complete; ready for Architecture | [Progress](phases/02-requirements/PROGRESS.md) | Complete |
| Architecture | Phase | Project | 100% | Complete; ready for Planning & Decomposition | [Progress](phases/03-architecture/PROGRESS.md) | Complete |
| Planning & Decomposition | Phase | Project | 100% | Complete; ready for Contracts & Tests | [Progress](phases/04-planning-decomposition/PROGRESS.md) | Complete |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Start Contracts & Tests from the approved Planning handoff | Contracts & Tests | Opens Phase 5 with explicit contract targets and fixture expectations | John + Codex |

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
| 2026-06-25 | Architecture | Opened Architecture phase with draft artifact and progress ledger | Converts Requirements into local Python module boundaries, data flow, CLI shape, fixture paths, and report artifact structure. | John + Codex |
| 2026-06-25 | Architecture | Refined Architecture decisions from owner questions | Anchored Python runtime to a modern hardware automation stack, confirmed modularity, chose standard-library-first dependencies, clarified JSON consumer priority, timestamp determinism, schema contract boundary, and artifact paths. | John + Codex |
| 2026-06-25 | Architecture | Added explicit portfolio stack evidence roadmap | Keeps Python report core practical while planning credible CI, Vue/TypeScript, Go, Postgres, Docker, Terraform/AWS, and Rust follow-on slices where useful. | John + Codex |
| 2026-06-25 | Architecture | Closed Architecture phase gate | Owner approved the Architecture handoff to Planning & Decomposition. | John |
| 2026-06-25 | Planning & Decomposition | Opened Planning & Decomposition phase with draft implementation units and sequencing | Converts Architecture into work packages, contract candidates, implementation order, generated artifact policy, and follow-on stack slice recommendation. | John + Codex |
| 2026-07-13 | Planning & Decomposition | Closed Planning & Decomposition phase gate | Owner approved the generated artifact policy, `pytest` development test posture, framework-neutral TypeScript viewer follow-on, and handoff to Contracts & Tests. | John |

## Open Progress Questions

| Scope | Question | Needed To Score Accurately | Owner |
|-------|----------|----------------------------|-------|
| Contracts & Tests | Which executable contracts and focused fixtures should be created first from the approved Planning handoff? | Phase 5 scope and sequencing | John + Codex |
