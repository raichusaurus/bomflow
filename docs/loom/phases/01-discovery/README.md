# Phase 1: Discovery

## Problem Statement

### Core Problem

Hardware teams can review a bill of materials for cost, availability, and manufacturability, but sustainability impact often sits outside the design review loop. That means carbon footprint and data-quality concerns may surface too late, after a design path is already socially or technically expensive to change.

### Why It Matters

BOMFlow should explore a customer-shaped automation where sustainability intelligence becomes part of the same review workflow as other hardware release signals.

### Current State

Working assumption: teams may handle BOM carbon analysis through spreadsheets, supplier portals, PLM metadata, or manual compliance workflows. That can be useful, but it is usually disconnected from versioned design review and CI/CD-style automation.

## Project Context

### Project Type

New prototype project for hardware workflow automation.

### Prior Art / Existing System

| Source / Artifact | What It Shows | Keep / Discard / Rethink | Notes |
|-------------------|---------------|---------------------------|-------|
| BOMFlow roadmap parts | Part 1: BOM Carbon Report; Part 2: Design Review Delta; Part 3: Integration Handoff | Keep as working roadmap | The BOM Carbon Report is the foundation. |

### Working Shape

BOMFlow is likely a small hardware automation project with three descriptive parts:

1. **BOM Carbon Report:** Generate a carbon report from one BOM and a mock emissions catalog.
2. **Design Review Delta:** Compare BOM revisions and highlight sustainability-impact changes for review.
3. **Integration Handoff:** Prepare structured outputs that could feed PLM, manufacturing, compliance, or release workflows.

### First Useful Version

Part 1, the BOM Carbon Report: Given one BOM and a mock emissions catalog, generate a clear carbon report that a hardware team could use during design review.

Design Review Delta and Integration Handoff are inactive future mini-Loom cycles in the same BOMFlow project. They are not required to prove the first useful version.

### Target Report Shape

The first BOM Carbon Report should be review-ready, not compliance-grade.

Minimum report sections:

- BOM summary: part count, quantity count, and total estimated kgCO2e.
- Top carbon contributors.
- Line-item table with part number, category, quantity, emission factor, and subtotal.
- Data quality flags for missing factors, estimated factors, and low-confidence matches.
- Review notes that highlight what a hardware engineer should inspect before release.
- Methodology caveat that mock data is not production-grade emissions science.

Future state: a compliance-style report could add evidence links, audit traceability, confidence scoring, and assumptions by part category. That should not be part of the first useful version.

### Explicitly Out of Scope

- Real supplier API integrations.
- Real PLM/manufacturing sync.
- Production-grade emissions methodology.
- Compliance-grade reporting.
- UI or visual workflow builder.
- Multi-user hosting or deployment.
- Design Review Delta and Integration Handoff implementation in the first useful version.

## Users & Stakeholders

### Primary User / Operator

The primary user for the BOM Carbon Report is a hardware engineer reviewing a BOM before design release.

This user needs a low-friction review artifact that shows carbon impact, data-quality concerns, and high-impact parts clearly enough to inform design review decisions.

### Setup / Workflow Operator

An automation engineer or workflow owner may configure the report generation and keep it repeatable, but they are not the first user the report must satisfy.

### Future / External Users

- Engineering managers who need release-gate visibility.
- Sustainability/compliance reviewers who need BOM-level evidence.
- Manufacturing or PLM operators who need structured metadata.
- Future maintainers or collaborators who need to understand the automation model.

### Stakeholders

| Stakeholder | Role | Needs | Constraints |
|-------------|------|-------|-------------|
| John | Builder | An interesting, credible, and useful project | Time, clarity, not overbuilding |
| Future maintainers / collaborators | Evaluator | Evidence of automation thinking, customer empathy, and code quality | Short attention window |
| Hardware engineer | Primary user | Useful review signal inside normal design workflow | Needs low-friction, explainable output |
| Automation engineer / workflow owner | Setup operator | Repeatable report generation and integration path | Should not need production integrations for the first version |
| Sustainability/compliance reviewer | Future stakeholder | BOM-level evidence and methodology caveats | Needs data-quality limits to be explicit |

### Decision Owner

John decides whether the project is worth continuing and when to move to Requirements.

## Context & Constraints

### Timeline

No hard deadline captured yet. The project should stay small enough to validate the first useful workflow quickly.

### Resources

- Team: John + Codex.
- Infrastructure: local repository first.
- Budget: none expected.

### Technical Constraints

- Prefer a small, inspectable implementation when Loom reaches Implementation.
- Keep room for Python action scripts, structured outputs, and integration boundaries.
- Avoid real external dependencies until the project needs them.

## Success & Validation

### Success Metrics

| Metric / Signal | Target | How We'll Measure |
|-----------------|--------|-------------------|
| Workflow alignment | Clear link to hardware review automation, scriptable execution, and integration boundaries | README/Loom docs can explain the mapping in under one minute |
| First useful version clarity | The BOM Carbon Report is the complete first useful version | Requirements can define the BOM Carbon Report without relying on future phases |
| Report usefulness | Hardware engineer can identify total impact, top contributors, and data-quality concerns | Report shape includes summary, line items, flags, review notes, and methodology caveat |
| Project evidence | Shows customer-shaped automation thinking | Final artifact can support a concise demo or project note |

### Validation Strategy

Discovery is ready to hand off to Requirements because the BOM Carbon Report has a clear primary user, first-version boundary, report shape, future-state boundaries, and non-goals.

### Evidence Ready For Requirements

- Primary user: hardware engineer reviewing a BOM before design release.
- First useful version: review-ready BOM Carbon Report from one BOM and mock emissions data.
- Target report shape: summary, top contributors, line items, data-quality flags, review notes, and methodology caveat.
- Scope boundaries: no supplier APIs, real PLM sync, UI, deployment, compliance-grade reporting, Design Review Delta, or Integration Handoff in the first useful version.
- Future cycles: Design Review Delta and Integration Handoff stay visible as inactive mini-Loom cycles in the same project.
- Requirements should convert the report shape and scope boundaries into acceptance criteria without rediscovering the product direction.

## Assumptions

| Assumption | Why We Believe It | How We'll Validate |
|-----------|------------------|-------------------|
| BOM Carbon Report is the right first slice | Design Review Delta and Integration Handoff depend on the report engine and output model | Requirements should show the BOM Carbon Report can stand alone |
| Mock emissions data is acceptable | The project is about automation shape, not emissions science | Make methodology limitations explicit |
| Review-ready reporting is enough for the first version | The primary user needs decision support during design review, not audit-grade compliance evidence | Requirements should keep compliance-style evidence as future state |
| One repo is the right home | The three roadmap parts form one project arc | Keep later parts as inactive mini-Loom cycles until they become active work |

## Risks & Opportunities

### Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| Project becomes too toy-like | Weak signal of real workflow value | Medium | Tie outputs to design review and future integration boundaries |
| Project overbuilds before clarity | Wasted time and muddy story | High | Use Loom gates before code |
| Emissions methodology gets scrutinized beyond scope | Distracts from automation story | Medium | Label data as mock and focus on workflow |

### Opportunities

- Natural growth path from carbon report to design-review delta to integration handoff.
- Future path toward compliance-style evidence once the review workflow is useful.
- Good project story: customer workflow to reusable automation.

## Discovery Outputs

### Key Insights

- BOMFlow should start with the BOM Carbon Report.
- The BOM Carbon Report is the complete first useful version.
- The first report should be review-ready, with compliance-style reporting left as future state.
- Design Review Delta and Integration Handoff are inactive future mini-Loom cycles in the same BOMFlow project.
- The first-user lens is a hardware engineer reviewing a BOM before design release.

### Open Questions

- None blocking Requirements.

### Requirements Handoff

- **Core problem:** Carbon/sustainability review is disconnected from hardware design automation.
- **Primary user / operator:** Hardware engineer reviewing a BOM before design release.
- **Setup / workflow operator:** Automation engineer or workflow owner configuring repeatable report generation.
- **Future / external users:** Hardware engineering teams, sustainability/compliance reviewers, PLM/manufacturing operators, future maintainers or collaborators.
- **Working shape:** One repo, current BOM Carbon Report MVP cycle plus inactive future mini-Loom cycles for Design Review Delta and Integration Handoff.
- **First useful version:** Review-ready BOM Carbon Report generated from one BOM and mock emissions data.
- **Target report shape:** BOM summary, top contributors, line-item table, data-quality flags, review notes, and methodology caveat.
- **Future state:** Compliance-style reporting with evidence links, audit traceability, confidence scoring, and category assumptions.
- **Explicitly out of scope:** Real supplier APIs, real PLM sync, UI, deployment, compliance-grade reporting, Design Review Delta, or Integration Handoff implementation in the first useful version.
- **Success / validation signals:** Workflow alignment, clear first useful version, report usefulness, project evidence.
- **Open questions carried forward:** None blocking Requirements.

### Next Steps

Move to Requirements and convert the Discovery handoff into concrete functional requirements, non-functional requirements, acceptance criteria, and explicit out-of-scope boundaries for the BOM Carbon Report.

## Phase Gate

- **Ready to move to Requirements?** [x] Yes [ ] No
- **Remaining concerns:** None blocking Requirements.
- **Owner decision:** Approved to move to Requirements.
