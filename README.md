# BOMFlow

BOMFlow is a prototype for bringing sustainability signals into hardware design review. The project explores how a bill of materials can be reviewed for carbon impact alongside cost, availability, manufacturability, and release-readiness signals.

## Status

BOMFlow has completed **Phase 1: Discovery** and **Phase 2: Requirements**. No implementation workflow is defined yet.

Next focus:

- Start Architecture for the BOM Carbon Report, using the JSON report model, contributor-ranking decisions, and canonical acceptance BOM fixture shape from Requirements.

## Roadmap Shape

1. **BOM Carbon Report:** Generate a carbon report from one BOM and a mock emissions catalog.
2. **Design Review Delta:** Compare BOM revisions and highlight sustainability-impact changes for review.
3. **Integration Handoff:** Prepare structured outputs that could feed PLM, manufacturing, compliance, or release workflows.

The BOM Carbon Report is the first useful version. Design Review Delta and Integration Handoff remain inactive future mini-Loom cycles in the same BOMFlow project.

The first report should be review-ready: summary, top contributors, line items, data-quality flags, review notes, and methodology caveat. Compliance-style reporting is a future state.

## Technical Direction

The first implementation should be a local, scriptable automation that can run like a CI/action workflow against versioned fixtures. It should favor a small Python runner, structured inputs, and a durable JSON report model. Later cycles can add human-readable rendering, typed UI, service, persistence, and deployment layers when the workflow needs them.

## Loom Workflow

Project decisions and phase outputs live in [docs/loom](docs/loom):

- [Loom Index](docs/loom/README.md)
- [Progress Ledger](docs/loom/PROGRESS.md)
- [Completed Phase 1 Discovery](docs/loom/phases/01-discovery/README.md)
- [Discovery Progress](docs/loom/phases/01-discovery/PROGRESS.md)
- [Phase 2 Requirements](docs/loom/phases/02-requirements/README.md)
- [Requirements Progress](docs/loom/phases/02-requirements/PROGRESS.md)

Update the progress ledger whenever project direction, phase status, or completion evidence changes.
