# Phase 2: Requirements

## Requirements Purpose

Convert the Discovery handoff into concrete requirements for the first useful BOMFlow version: a JSON-first BOM Carbon Report generated from one BOM and one mock emissions catalog.

This phase should define what the report must do, how usefulness will be judged, what inputs and outputs are expected, and which tempting future features stay out of scope.

## Product Scope

### First Useful Version

BOMFlow must generate a BOM Carbon Report model that helps a hardware engineer review sustainability impact before design release.

The first durable artifact is structured JSON, not a compliance-grade emissions report or polished review UI. It should make carbon impact, top contributors, and data-quality concerns explicit enough that later renderers, frontends, or integrations can present them consistently.

### Primary User

The primary user is a hardware engineer reviewing a BOM before design release.

The report should help this user answer:

- What is the estimated carbon impact of this BOM?
- Which parts or categories contribute most to that estimate?
- Which line items need attention because the emissions data is missing, estimated, low-confidence, or otherwise weak?
- What should be reviewed before the design moves forward?

### Setup Operator

An automation engineer or workflow owner may configure the report generation and maintain the mock emissions catalog.

The first version should stay simple enough that this operator can run it locally and inspect or replace input files without setting up external systems.

## Functional Requirements

| ID | Requirement | Acceptance Signal |
|----|-------------|-------------------|
| FR-1 | Accept one BOM input file containing line items. | A user can run the workflow against a single BOM file without needing a second revision or external system. |
| FR-2 | Accept one mock emissions catalog. | The workflow can resolve emission factors from local mock data. |
| FR-3 | Match BOM line items to emissions factors. | Each report line shows whether a factor was matched, estimated, missing, or low-confidence. |
| FR-4 | Calculate line-item carbon subtotals. | Each line item includes quantity, emission factor, and estimated kgCO2e subtotal when data is available. |
| FR-5 | Calculate BOM-level summary totals. | The report includes part count, total quantity count, total estimated kgCO2e, and count of data-quality flags. |
| FR-6 | Identify top carbon contributors. | The report highlights highest-impact line items as the primary action surface and highest-impact categories as the summary lens. |
| FR-7 | Generate a line-item table. | The report includes part number, description or category when available, quantity, emission factor, subtotal, and data-quality status. |
| FR-8 | Generate data-quality flags. | The report explicitly calls out missing factors, estimated factors, low-confidence matches, and any line items excluded from totals. |
| FR-9 | Generate review notes. | The report includes concise notes describing what a hardware engineer should inspect before release. |
| FR-10 | Include a methodology caveat. | The report states that mock emissions data is not production-grade emissions science and should not be used for compliance claims. |
| FR-11 | Produce a durable JSON report artifact. | A user or future frontend can open the generated structured output after the run without rerunning the workflow. |

## Non-Functional Requirements

| ID | Requirement | Acceptance Signal |
|----|-------------|-------------------|
| NFR-1 | Keep the workflow local and scriptable. | The first version can run from the repository without hosted infrastructure. |
| NFR-2 | Keep inputs inspectable. | BOM and emissions inputs use plain structured files suitable for review and version control. |
| NFR-3 | Keep outputs explainable. | Calculations and caveats are visible enough that a reviewer can understand how totals were produced. |
| NFR-4 | Prefer small, maintainable implementation boundaries. | Architecture can later separate parsing, matching, calculation, and rendering without a rewrite. |
| NFR-5 | Avoid real external dependencies unless clearly needed. | No supplier API, PLM, manufacturing, or hosted service is required for the first useful version. |
| NFR-6 | Make future integration plausible. | Output shape should leave room for later structured handoff to review, PLM, compliance, or manufacturing workflows. |
| NFR-7 | Make the implementation stack credible for hardware workflow automation. | Architecture should prefer a Python action-style runner, structured artifacts, and CI execution first, while leaving clear boundaries for future typed UI, backend service, database, and deployment layers. |

## Stack Alignment

The first version should show credible automation and integration instincts without overbuilding. Requirements should leave Architecture with these handoff signals:

- A scriptable Python workflow that feels like an action/plugin rather than a one-off spreadsheet helper.
- Structured inputs and outputs that can later feed review, PLM, manufacturing, compliance, or release systems.
- CI-ready execution against fixtures so the workflow can run repeatably during design review.
- Clean module boundaries for parsing, matching, calculation, rendering, and future integration adapters.
- A durable JSON report artifact that can feed tests, future frontend rendering, and downstream automation.

The first version should not implement hosted infrastructure, real external integrations, a database, or a visual workflow builder. Later phases may still describe where a typed front-end, backend service, persistence, deployment automation, or systems-level utility code would fit in future cycles.

## Fixture Strategy

### Acceptance Fixture Decision

The first acceptance fixture should be one canonical mixed-case BOM, not a pure happy-path file.

The fixture should represent a small IoT environmental sensor assembly with enough variety to exercise the report model while staying easy to inspect by hand. It should be the shared demo and acceptance target for Architecture, Contracts & Tests, and Implementation.

Suggested fixture name:

- `canonical-iot-sensor.bom.json`

The canonical BOM should include roughly 10-12 line items across categories such as:

- PCB.
- MCU or processor.
- Environmental sensor.
- Power or battery.
- Connector.
- Passives.
- Mechanical enclosure.
- Cable, label, or packaging.

The canonical BOM should intentionally include:

- Clean part-specific emissions matches.
- At least one category-level estimated factor.
- At least one low-confidence match.
- At least one missing emissions factor.
- At least one missing or weak category that rolls into an explicit `uncategorized` bucket.
- Multiple rows in the same category so category contributor ranking is meaningful.
- At least one high-impact line item so line-item contributor ranking is meaningful.

This fixture is not expected to cover every test case. Contracts & Tests should add focused fixture files for happy path, missing factors, estimated factors, low confidence, uncategorized rows, invalid input, and later scale/performance behavior.

## Input Requirements

### BOM Input

The first version should require enough structured BOM data to calculate and explain the report.

Minimum fields:

| Field | Required | Purpose |
|-------|----------|---------|
| `part_number` | Yes | Stable line-item identifier for matching and review. |
| `quantity` | Yes | Multiplier for carbon subtotal. |
| `category` | Preferred | Enables category-based matching and contributor grouping. |
| `description` | Preferred | Helps human reviewers understand the line item. |
| `manufacturer` | Optional | Future matching signal; useful but not required for the first version. |
| `manufacturer_part_number` | Optional | Future matching signal; useful but not required for the first version. |

### Mock Emissions Catalog

The catalog should be local mock data with enough structure to support direct and estimated matches.

Minimum fields:

| Field | Required | Purpose |
|-------|----------|---------|
| `match_key` | Yes | Part number, category, or other local key used for lookup. |
| `match_type` | Yes | Explains whether the factor is part-specific, category-level, estimated, or fallback. |
| `emission_factor_kgco2e` | Yes | Factor used to calculate line-item subtotal. |
| `confidence` | Preferred | Supports low-confidence flags. |
| `source_note` | Preferred | Human-readable note explaining mock factor assumptions. |

## Output Requirements

The JSON report model should contain these top-level sections:

1. **BOM Summary:** part count, quantity count, total estimated kgCO2e, and data-quality flag counts.
2. **Top Carbon Contributors:** ranked line items by subtotal plus ranked categories by aggregate subtotal.
3. **Line-Item Table:** part number, category, quantity, emission factor, subtotal, and quality status.
4. **Data-Quality Flags:** missing factors, estimated factors, low-confidence matches, and excluded line items.
5. **Review Notes:** short, action-oriented observations for the hardware engineer.
6. **Methodology Caveat:** explicit statement that the report uses mock data and is not compliance-grade.

The first durable report artifact should be JSON. JSON keeps the report model explicit, testable, frontend-ready, and suitable for later Integration Handoff work.

Human-readable rendering, such as Markdown, HTML, or a frontend view, should consume the same structured report model later. Those rendered views are not required to close the first Requirements phase.

### Output Format Decision

| Decision | Choice | Rationale |
|----------|--------|-----------|
| First durable report artifact | JSON | Preserves structured data for tests, future frontend work, and future integration handoffs. |
| First human-readable rendering | Not required in Phase 2 | The report model should stay flexible before frontend or presentation choices are made. |
| Future rendered outputs | Frontend, Markdown, HTML, or CSV exports | These can be generated from the JSON/report model once the core semantics are stable. |

### Top-Contributor Decision

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary contributor ranking | Line items | Gives the hardware engineer exact parts to inspect during design review. |
| Summary contributor ranking | Categories | Shows design-level impact patterns and creates a useful frontend/dashboard lens. |
| Missing category handling | Explicit uncategorized bucket | Keeps category totals honest when BOM category data is incomplete. |

## Acceptance Criteria

The BOM Carbon Report is acceptable when:

- Given a valid single BOM and mock emissions catalog, the workflow generates a report artifact without external services.
- The report includes the required summary, top contributors, line-item table, data-quality flags, review notes, and methodology caveat.
- The total estimated kgCO2e equals the sum of line-item subtotals for rows with usable factors.
- Top contributors include both ranked line items and ranked categories.
- Missing emissions factors are visible and do not silently contribute to the total.
- Estimated or low-confidence factors are visible in both line-item details and data-quality summaries.
- The canonical acceptance BOM includes clean matches, estimated factors, low-confidence matches, missing factors, uncategorized handling, and enough category variety to prove rankings.
- The JSON structure exposes highest-impact items and weakest data-quality areas without requiring consumers to recalculate report semantics.
- The report language does not imply production-grade emissions science or compliance readiness.
- Future roadmap items are not required to understand, run, or evaluate the first report.

## Explicitly Out Of Scope

- Real supplier API integrations.
- Real PLM, manufacturing, ERP, or compliance-system sync.
- Production-grade emissions methodology.
- Compliance-grade reporting, audit evidence, or legal claims.
- UI or visual workflow builder.
- Multi-user hosting, authentication, or deployment.
- Design Review Delta implementation.
- Integration Handoff implementation.
- Multi-BOM comparison.
- Automatic sourcing recommendations or part substitutions.

## Future Hooks

These are not first-version requirements, but the requirements should avoid blocking them:

- Compare two BOM revisions and highlight carbon-impact deltas.
- Export structured metadata for design review or release workflows.
- Add evidence links, audit traceability, confidence scoring, and assumptions by part category.
- Support richer matching using manufacturer and manufacturer part number.
- Feed PLM, manufacturing, compliance, or release handoff systems.
- Add a broader fixture suite for focused validation beyond the canonical acceptance BOM.

## Risks And Requirement Controls

| Risk | Requirement Control |
|------|---------------------|
| The project feels too toy-like. | Require top contributors, data-quality flags, review notes, and future integration hooks. |
| The project overbuilds before implementation clarity. | Keep the first version to one BOM, one mock catalog, local execution, and a durable report artifact. |
| Mock emissions data is mistaken for real science. | Require methodology caveats and visible data-quality status. |
| Requirements drift toward future roadmap items. | Keep Design Review Delta and Integration Handoff explicitly out of scope. |

## Requirements Phase Gate

- **Agent recommendation:** [x] Ready [ ] Not ready
- **Owner decision:** [x] Approved [ ] Needs revision [ ] Deferred
- **Decision date:** 2026-06-24
- **Remaining concerns:** None blocking Architecture.
