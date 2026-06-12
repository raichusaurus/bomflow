# Phase 1: Discovery

## Problem Statement

### Core Problem

Hardware teams can review a bill of materials for cost, availability, and manufacturability, but sustainability impact often sits outside the design review loop. That means carbon footprint and data-quality concerns may surface too late, after a design path is already socially or technically expensive to change.

### Why It Matters

BOMFlow should explore a customer-shaped automation where sustainability intelligence becomes part of the same review workflow as other hardware release signals. The project is also intentionally aligned with the AllSpice role context captured in [AllSpice role inspiration](../../../references/allspice-role-inspiration.md).

### Current State

Working assumption: teams may handle BOM carbon analysis through spreadsheets, supplier portals, PLM metadata, or manual compliance workflows. That can be useful, but it is usually disconnected from versioned design review and CI/CD-style automation.

## Project Context

### Project Type

New portfolio/prototype project for hardware workflow automation.

### Prior Art / Existing System

| Source / Artifact | What It Shows | Keep / Discard / Rethink | Notes |
|-------------------|---------------|---------------------------|-------|
| [AllSpice role inspiration](../../../references/allspice-role-inspiration.md) | Example project includes carbon emissions report for parts in a design | Keep | Strong role alignment, but should stay as context rather than the core product narrative. |
| BOMFlow A/B/C idea | A: carbon report; B: design-review delta; C: PLM/manufacturing sync | Keep as working roadmap | A is the foundation. |
| Premature implementation spike | Basic CLI/report shape | Rethink later | Removed so Loom can lead. |

### Working Shape

BOMFlow is likely a small hardware automation project that starts with a single-BOM carbon report, then grows into design-review deltas and integration handoffs.

### First Useful Version

A: Given one BOM and a mock emissions catalog, generate a clear carbon report that a hardware team could use during design review.

### Explicitly Out of Scope

- Real supplier API integrations.
- Real PLM/manufacturing sync.
- Production-grade emissions methodology.
- UI or visual workflow builder.
- Multi-user hosting or deployment.
- B and C implementation before A is shaped and validated.

## Users & Stakeholders

### Primary User / Operator

Open question. Candidate lenses:

- Hardware engineer reviewing a BOM before design release.
- Forward-deployed engineer building a reusable customer automation.
- Sustainability/compliance reviewer who needs BOM-level evidence.

### Future / External Users

- Engineering managers who need release-gate visibility.
- Manufacturing or PLM operators who need structured metadata.
- External evaluators reviewing John's technical judgment and communication.

### Stakeholders

| Stakeholder | Role | Needs | Constraints |
|-------------|------|-------|-------------|
| John | Builder and candidate | A project that is interesting, credible, and role-aligned | Time, portfolio clarity, not overbuilding |
| Portfolio / hiring evaluators | Evaluator | Evidence of automation thinking, customer empathy, and code quality | Short attention window |
| Hardware team persona | Target user | Useful review signal inside normal design workflow | Needs low-friction, explainable output |

### Decision Owner

John decides whether the project is worth continuing and when to move to Requirements.

## Context & Constraints

### Timeline

No hard deadline captured yet. The project should stay small enough to become application evidence quickly.

### Resources

- Team: John + Codex.
- Infrastructure: local repository first.
- Budget: none expected.

### Technical Constraints

- Prefer a small, inspectable implementation when Loom reaches Implementation.
- Keep room for Python action scripts, structured outputs, and integration boundaries because those match the target role context.
- Avoid real external dependencies until the project needs them.

## Success & Validation

### Success Metrics

| Metric / Signal | Target | How We'll Measure |
|-----------------|--------|-------------------|
| Role alignment | Clear link to hardware workflow automation, Actions-style execution, and integration boundaries | README/Loom docs can explain the mapping in under one minute |
| First useful version clarity | A is independently useful before B/C | Requirements can define A without relying on future phases |
| Portfolio evidence | Shows customer-shaped automation thinking | Final artifact can support an application note or demo |

### Validation Strategy

Before Requirements, validate that the A/B/C roadmap is still the right story and that A has a clear first operator, inputs, outputs, and non-goals.

### Evidence Needed Before Requirements

- Chosen primary operator.
- First useful version boundary for A.
- Target output shape for the carbon report.
- Decision on whether B and C are roadmap items in the same project or later Loom cycles.

## Assumptions

| Assumption | Why We Believe It | How We'll Validate |
|-----------|------------------|-------------------|
| A is the right first slice | B and C depend on the report engine and output model | Requirements should show A can stand alone |
| Mock emissions data is acceptable | The project is about automation shape, not emissions science | Make methodology limitations explicit |
| A single repo is the right home | A/B/C form one project arc | Revisit during Architecture |

## Risks & Opportunities

### Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| Project becomes too toy-like | Weak signal for senior integrations role | Medium | Tie outputs to design review and future integration boundaries |
| Project overbuilds before clarity | Wasted time and muddy story | High | Use Loom gates before code |
| Emissions methodology gets scrutinized beyond scope | Distracts from automation story | Medium | Label data as mock and focus on workflow |

### Opportunities

- Strong direct mapping to the role inspiration without making the product feel company-specific.
- Natural growth path from report to diff to PLM sync.
- Good interview story for forward-deployed engineering: customer workflow to reusable automation.

## Framework Feedback

### What Worked

The Loom framework caught the sequencing issue: we were implementing before Discovery and Requirements.

### Friction

"Let's Loom" can be misread as "prepare a Loom video" without checking the local Loom framework.

### Template / Process Improvements

For future sessions, treat "looming" as a trigger to inspect the Loom repo and start from the current phase gate.

## Discovery Outputs

### Key Insights

- BOMFlow should start with A: a single-BOM carbon report.
- B and C are likely extensions, not separate repos.
- The project needs a crisp first-user lens before Requirements.

### Open Questions

- Who is the primary operator for A?
- What should the report output include to be credible but not overbuilt?
- Should B and C be named as roadmap phases or planned as later mini-Loom cycles?

### Requirements Handoff

- **Core problem:** Carbon/sustainability review is disconnected from hardware design automation.
- **Primary user / operator:** Open.
- **Future / external users:** Hardware engineering teams, sustainability/compliance reviewers, PLM/manufacturing operators, portfolio / hiring evaluators.
- **Working shape:** One repo, phased A/B/C roadmap, starting with a single-BOM carbon report.
- **First useful version:** A report generated from one BOM and mock emissions data.
- **Explicitly out of scope:** Real supplier APIs, real PLM sync, UI, deployment, B/C implementation before A.
- **Success / validation signals:** Role alignment, clear first useful version, portfolio evidence.
- **Open questions carried forward:** Primary operator, report output shape, A/B/C roadmap structure.

### Next Steps

Finish Discovery by answering the open questions and deciding whether the phase gate is ready for Requirements.

## Phase Gate

- **Ready to move to Requirements?** [ ] Yes [x] No
- **Remaining concerns:** Primary operator and validation bar need to be explicit.
- **Owner decision:** Pending.
