# Phase 3: Architecture

## Architecture Purpose

Translate the approved BOM Carbon Report requirements into an implementation shape that is small, local, scriptable, testable, and credible as hardware workflow automation.

This phase defines the module boundaries, data flow, report model, fixture locations, command shape, and validation seams for the first useful BOMFlow version. It should give Planning & Decomposition enough structure to break the work into implementation tasks without reopening product scope.

## Architecture Drivers

| Driver | Architectural Response |
|--------|------------------------|
| JSON-first report artifact | Build around an internal report model that serializes directly to durable JSON. |
| Local and scriptable workflow | Provide a Python CLI/action-style runner with file inputs and file output. |
| Inspectable inputs | Store BOM and emissions catalog fixtures as plain JSON files. |
| Explainable calculations | Keep parsing, matching, subtotal calculation, contributor ranking, and notes generation as visible steps. |
| Future integration plausibility | Keep output sections stable enough for future frontend, PLM, compliance, or release-handoff adapters. |
| Portfolio stack evidence | Use the first version to prove Python actions and CI, while preserving practical follow-on slices for Vue/TypeScript, Go, Postgres, deployment, and Rust utility work. |
| Avoid overbuilding | Defer database, hosted service, UI, authentication, supplier APIs, and real emissions methodology. |

## Stack Alignment

BOMFlow should demonstrate competence in a modern hardware automation stack where that stack makes the project stronger. The target stack centers on Python for action-style automation, GitHub Actions for CI/CD, Vue/TypeScript for front-end review surfaces, Go for server-side product work, Postgres for persistence, Docker/Terraform/AWS for deployment thinking, and Rust for backend utility functions.

Architecture decision:

- **Commit to Python for the first automation core.** The BOM Carbon Report should feel like a local action/plugin that can later run in CI.
- **Make CI part of the first credible implementation path.** The report should run repeatably against fixtures in local checks and a future GitHub Actions workflow.
- **Prefer practical stack proof over decorative stack usage.** Vue/TypeScript, Go, Postgres, Docker, Terraform, AWS, and Rust should appear when they own a useful slice, not as empty wrappers around the Python report.
- **Use structured JSON as the integration bridge.** Future UI, service, PLM, compliance, or release-handoff work should consume the report artifact rather than bypassing the Python report engine.
- **Stage the broader stack deliberately.** The architecture should show how each stack element can enter the project without compromising the first useful version.

This keeps the MVP small while making BOMFlow a deliberate portfolio artifact, not just a Python script.

### Stack Evidence Roadmap

| Stack Element | First Practical Use In BOMFlow | Phase / Slice | Current Decision |
|---------------|--------------------------------|---------------|------------------|
| Python | Action-style CLI/report engine for BOM Carbon Report | First implementation slice | In scope now |
| GitHub Actions | Run fixture-based report generation and tests on push/PR | First implementation or immediate hardening slice | In scope for early automation |
| JSON contracts | Stable report artifact for downstream consumers | First implementation plus Contracts & Tests | In scope now |
| Markdown or HTML | Human-readable report generated from the same JSON model | Optional first-version enhancement if low effort; otherwise next slice | Practical, but secondary to JSON |
| Vue/TypeScript | Thin review surface that loads generated report JSON and presents summary, contributors, flags, and notes | Follow-on review UI slice | Preserve as likely next stack proof |
| Go | Small service boundary that serves stored reports or exposes report metadata if BOMFlow becomes service-shaped | Later service/integration slice | Defer until it owns real behavior |
| Postgres | Persist report runs, BOM metadata, and handoff history for service/UI workflows | Later service/integration slice | Defer until persistence is useful |
| Docker | Containerize local CLI or service for repeatable execution | CI/deployment hardening slice | Use when it simplifies reproducibility |
| Terraform/AWS | Minimal deployable environment for hosted review or handoff service | Deployment slice | Defer until a service exists |
| Rust | Utility for performance-sensitive parsing, normalization, or diffing if Python becomes limiting | Later utility slice | Defer until there is a real systems need |

Portfolio stack principle:

Every stack element should be able to answer: "What user or operator problem does this solve in BOMFlow?" If the answer is only "to show the stack," defer it but keep the transition boundary clear.

## System Context

The first version is a local command that consumes one BOM file and one mock emissions catalog, generates a structured BOM Carbon Report, and writes a JSON artifact.

```text
canonical BOM JSON
        |
        v
    BOM parser
        |
        v
mock emissions catalog JSON --> catalog loader --> matcher
                                                   |
                                                   v
                                           carbon calculator
                                                   |
                                                   v
                                            report builder
                                                   |
                                                   v
                                      JSON report artifact
```

Future consumers such as Markdown rendering, frontend review surfaces, PLM handoff, or compliance metadata export should consume the report artifact rather than reimplementing the matching and calculation logic.

Future stack-oriented consumers should follow the same rule:

- Vue/TypeScript consumes report JSON.
- Go service layer serves, stores, or coordinates report artifacts.
- Postgres stores report run metadata and history.
- Rust utilities operate behind narrow parsing, normalization, or diff interfaces.

## Proposed Repository Shape

```text
bomflow/
  __init__.py
  cli.py
  models.py
  io.py
  catalog.py
  matcher.py
  calculator.py
  report.py
  notes.py
data/
  fixtures/
    canonical-iot-sensor.bom.json
  catalogs/
    mock-emissions-catalog.json
reports/
  bom-carbon-report.json
tests/
  fixtures/
  test_cli.py
  test_report_generation.py
  test_matching.py
  test_calculation.py
.github/
  workflows/
    bomflow.yml
```

The exact file layout can change during Planning & Decomposition if the repository already has stronger conventions, but the implementation should preserve these responsibilities.

Path decision:

- Keep `data/fixtures/` for canonical BOMs because they are source inputs.
- Keep `data/catalogs/` for mock emissions assumptions because they are editable local data, not generated output.
- Keep `reports/` for generated artifacts, with the expectation that Planning or Implementation may add it to `.gitignore` if generated reports should not be committed.
- Keep `tests/` for executable contracts and implementation checks.
- Add `.github/workflows/` once there is a runnable scaffold and a stable local command worth automating.

Future stack paths, added only when their slices are active:

```text
web/                 # Vue/TypeScript report viewer
service/             # Go service boundary
infra/               # Terraform/AWS deployment definitions
docker/ or Dockerfile
crates/              # Rust utility code, only if justified
```

## Module Boundaries

| Module | Responsibility | Should Not Own |
|--------|----------------|----------------|
| `bomflow.models` | Typed or documented data structures for BOM lines, catalog factors, matches, report lines, flags, and report output. | File paths, CLI parsing, or presentation formatting. |
| `bomflow.io` | Load and validate local JSON input files; write JSON report artifacts. | Carbon matching rules or review-note generation. |
| `bomflow.catalog` | Normalize catalog records into lookup structures by part number, category, and future keys. | BOM parsing or subtotal math. |
| `bomflow.matcher` | Resolve each BOM line to a part-specific, category-level, estimated, low-confidence, or missing factor. | Report aggregation or file output. |
| `bomflow.calculator` | Calculate line subtotals, BOM summary totals, and category totals. | Human-facing notes or CLI behavior. |
| `bomflow.report` | Assemble the final JSON report model, including contributors, tables, flags, and methodology caveat. | Raw input loading. |
| `bomflow.notes` | Generate concise review notes from totals, contributors, and data-quality flags. | Matching or calculation correctness. |
| `bomflow.cli` | Provide the local command entrypoint and connect modules into the workflow. | Domain rules that should be unit tested elsewhere. |

## Execution Shape

The first CLI should be boring and repeatable:

```bash
python -m bomflow report \
  --bom data/fixtures/canonical-iot-sensor.bom.json \
  --catalog data/catalogs/mock-emissions-catalog.json \
  --out reports/bom-carbon-report.json
```

Expected behavior:

- Read exactly one BOM and one mock catalog.
- Generate the report without network access or external services.
- Create parent output directories when needed.
- Exit non-zero on invalid input or unwritable output.
- Print a short success message with the report path and total estimated kgCO2e.
- Accept a deterministic generated-at value in tests, either through an injectable clock or a CLI/test override.

Timestamp decision:

Generated reports should include `generated_at` for real runs, but tests should not depend on wall-clock time. Contracts & Tests should choose the exact mechanism, with a default preference for an injectable clock in the report builder and a CLI-level override only if it keeps tests and demos simpler.

## Input Model

### BOM File

The BOM fixture should be a JSON object with metadata plus line items:

```json
{
  "bom_id": "canonical-iot-sensor",
  "revision": "A",
  "description": "IoT environmental sensor assembly",
  "line_items": [
    {
      "part_number": "PCB-001",
      "description": "Main sensor PCB",
      "category": "pcb",
      "quantity": 1,
      "manufacturer": "MockFab",
      "manufacturer_part_number": "MF-PCB-001"
    }
  ]
}
```

Required architecture-level validation:

- `line_items` must be present and non-empty.
- Each line item must have `part_number` and numeric positive `quantity`.
- Missing `category` should be normalized into `uncategorized`, not treated as a parser failure.
- Optional fields should pass through when present.

### Emissions Catalog

The catalog should be a JSON object with factor records:

```json
{
  "catalog_id": "mock-emissions-catalog",
  "methodology_note": "Mock data for workflow demonstration only.",
  "factors": [
    {
      "match_key": "PCB-001",
      "match_type": "part_number",
      "emission_factor_kgco2e": 3.4,
      "confidence": "high",
      "source_note": "Mock part-specific PCB factor."
    }
  ]
}
```

Required architecture-level validation:

- `factors` must be present.
- Each factor must have `match_key`, `match_type`, and numeric non-negative `emission_factor_kgco2e`.
- Missing `confidence` should default to `unknown` and produce a visible quality signal.
- `source_note` should be preserved in report details when available.

## Matching Strategy

The first matcher should use deterministic local rules:

1. Match exact BOM `part_number` to catalog `match_key` where `match_type` is `part_number`.
2. If no part match exists, match normalized BOM `category` to catalog `match_key` where `match_type` is `category`.
3. If a category factor is marked as estimated or low-confidence, preserve that status in the report.
4. If no usable factor exists, mark the line as missing, exclude it from carbon totals, and include it in data-quality flags.

Quality statuses should be explicit and stable:

| Status | Meaning | Included In Total |
|--------|---------|-------------------|
| `matched` | Part-specific factor with acceptable confidence. | Yes |
| `estimated` | Category-level or explicitly estimated factor. | Yes |
| `low_confidence` | Factor exists but confidence is weak. | Yes |
| `missing_factor` | No usable factor found. | No |
| `uncategorized` | Missing or weak category data; may combine with another status. | Depends on factor availability |

## Calculation Rules

Line subtotal:

```text
subtotal_kgco2e = quantity * emission_factor_kgco2e
```

Summary totals:

- `part_count`: number of BOM line items.
- `quantity_count`: sum of line-item quantities.
- `total_estimated_kgco2e`: sum of subtotals for lines with usable factors.
- `excluded_line_count`: number of missing-factor lines excluded from totals.
- `data_quality_flag_count`: total count of generated quality flags.

Contributor rankings:

- `top_line_items`: report lines with usable factors sorted by subtotal descending.
- `top_categories`: category aggregates sorted by subtotal descending.
- Missing or weak category values must roll into `uncategorized`.

The report should round presentation values consistently, but tests should avoid brittle floating-point expectations by using numeric tolerances or exact decimal-friendly fixture values.

## JSON Report Shape

The durable report artifact should preserve the Requirements sections as top-level keys:

```json
{
  "report_metadata": {
    "report_id": "bom-carbon-report",
    "bom_id": "canonical-iot-sensor",
    "bom_revision": "A",
    "generated_at": "ISO-8601 timestamp or deterministic test value",
    "catalog_id": "mock-emissions-catalog"
  },
  "bom_summary": {
    "part_count": 0,
    "quantity_count": 0,
    "total_estimated_kgco2e": 0,
    "data_quality_flag_count": 0,
    "excluded_line_count": 0
  },
  "top_carbon_contributors": {
    "line_items": [],
    "categories": []
  },
  "line_items": [],
  "data_quality_flags": [],
  "review_notes": [],
  "methodology_caveat": "Mock emissions data for workflow demonstration only; not compliance-grade."
}
```

Each report line should include:

- `part_number`
- `description`
- `category`
- `quantity`
- `match_status`
- `match_type`
- `emission_factor_kgco2e`
- `subtotal_kgco2e`
- `confidence`
- `source_note`
- `included_in_total`

Report-consumer decision:

The JSON should optimize for downstream automation first, but still be pleasant to inspect directly. That means stable semantic keys, readable enum values, preserved source notes, review notes in plain language, and no requirement for consumers to recalculate totals or infer quality status. A Markdown or HTML renderer can come later, but the JSON itself should already tell a coherent review story.

## Schema And Contract Boundary

Architecture should sketch the report shape and name the stability expectations, but it should not lock a full JSON Schema yet. The broader Loom templates currently place "Schema / Model Contracts" inside Phase 5 Contracts & Tests, while Phase 4 Planning asks which schemas, interfaces, commands, or workflows should become contract/test candidates.

BOMFlow should use that split:

| Phase | Schema Responsibility |
|-------|-----------------------|
| Architecture | Define conceptual input/output shape, stable top-level report sections, and fields that downstream consumers will expect. |
| Planning & Decomposition | Add explicit work items for BOM input schema, emissions catalog schema, report schema, fixture coverage, and compatibility checks. |
| Contracts & Tests | Lock executable schema/model contracts with fixtures and tests before implementation. |
| Implementation | Satisfy the contracts without silently changing report semantics. |

Default contract approach:

- Prefer standard-library Python data structures and validation first.
- Use executable tests and fixture assertions as the first schema contract.
- Add JSON Schema only if Phase 5 decides downstream compatibility needs a standalone schema artifact.
- Treat changes to top-level report keys, required fields, enum values, and inclusion/exclusion semantics as approval-gated contract changes after Phase 5.

## Testing Architecture

Contracts & Tests should be able to validate behavior at three levels:

| Level | Target | Validation |
|-------|--------|------------|
| Unit | `matcher`, `calculator`, `report` | Matching hierarchy, subtotal math, flags, rankings, and caveat presence. |
| Fixture | canonical BOM + mock catalog | Mixed-case acceptance fixture generates expected sections and totals. |
| CLI | `python -m bomflow report ...` | Local command writes the JSON artifact and exits successfully. |

Initial test fixture coverage should include:

- Canonical mixed-case IoT sensor BOM.
- Happy path with all matched factors.
- Missing factor behavior.
- Estimated category factor behavior.
- Low-confidence factor behavior.
- Uncategorized line behavior.
- Invalid BOM input.

Dependency decision:

Use the Python standard library for the implementation unless Planning or Contracts & Tests identifies a concrete reason to add a dependency. The current default is `dataclasses`, `argparse`, `json`, `pathlib`, and focused tests. `pytest` is acceptable if this repository standardizes on it during Contracts & Tests; Pydantic or a JSON Schema validator should wait until the schema contract needs more than simple local validation.

## Future Integration Hooks

The architecture should leave these extension points visible without implementing them:

- Additional input loaders for CSV, PLM export, or supplier data.
- Markdown or HTML rendering from the JSON report.
- Vue/TypeScript frontend rendering from the JSON report.
- Design Review Delta comparison from two report artifacts or two BOM revisions.
- Integration Handoff adapters for PLM, manufacturing, compliance, or release workflows.
- Richer matching using manufacturer and manufacturer part number.
- Real emissions methodology and evidence links.
- Go service and Postgres persistence layer if BOMFlow later becomes a hosted workflow service.
- Docker container for repeatable CLI/service execution.
- Terraform/AWS deployment path once there is something service-shaped to deploy.
- Rust utility code only for performance-sensitive parsing or transformation that Python cannot handle cleanly.

## Architecture Decisions

| Decision | Choice | Rationale | Owner |
|----------|--------|-----------|-------|
| Runtime shape | Local Python package with CLI/action-style runner | Matches requirements for scriptable hardware workflow automation and CI-ready execution. | John + Codex |
| Stack evidence strategy | Python action core and CI early; Vue/TypeScript likely next; Go, Postgres, Docker, Terraform/AWS, and Rust enter only when they own useful behavior | Demonstrates a credible modern automation stack while avoiding decorative implementation. | John + Codex |
| Dependency posture | Standard library first; add dependencies only for clear testing, validation, or maintainability needs | Keeps the first automation core easy to inspect, run, and explain. | Codex |
| Durable artifact | JSON report generated from internal report model | Preserves structured semantics for tests, future UI, and future integration handoff. | John |
| JSON consumer priority | Automation-first, human-inspectable JSON | Supports downstream integrations while still letting a reviewer understand the artifact directly. | John + Codex |
| First fixture path | `data/fixtures/canonical-iot-sensor.bom.json` | Keeps the canonical acceptance fixture easy to inspect and reuse. | John + Codex |
| First catalog path | `data/catalogs/mock-emissions-catalog.json` | Separates BOM input from mock emissions assumptions. | John + Codex |
| Module style | Small modules for IO, catalog normalization, matching, calculation, report assembly, notes, and CLI | Supports focused tests and avoids a one-off script blob. | Codex |
| Matching strategy | Deterministic exact part match, then category match, then missing-factor flag | Keeps behavior explainable and testable before richer matching exists. | Codex |
| Schema boundary | Architecture sketches shape; Phase 5 locks executable schema/model contracts | Matches existing Loom contract flow and avoids over-specifying before Planning. | Codex |
| Timestamp handling | Real generated timestamp in normal runs; deterministic clock or override in tests | Keeps reports useful while making tests stable and repeatable. | Codex |
| Rust boundary | No Rust in the first slice; revisit for narrow parsing, normalization, diffing, or performance utilities | Shows judgment about the stack instead of adding unnecessary complexity. | John + Codex |
| Gate status | Draft architecture opened; owner approval pending | Starts Phase 3 without marking it complete on the agent's authority alone. | John + Codex |

## Risks And Architecture Controls

| Risk | Control |
|------|---------|
| Architecture becomes heavier than the MVP needs. | Keep runtime local, file-based, and CLI-first; defer service and UI layers. |
| Report model becomes too presentation-specific. | Store semantic sections in JSON and let future renderers consume them. |
| Matching behavior is hard to explain. | Use deterministic match order and preserve source notes, confidence, and statuses. |
| Mock data looks more authoritative than intended. | Include methodology caveat and quality flags in the required report model. |
| Future integration is blocked by a one-off script. | Preserve clean module boundaries and stable JSON sections. |
| Tests become flaky because generated timestamps vary. | Use an injectable clock or deterministic override for contract tests. |
| Schema expectations drift between docs, fixtures, and implementation. | Carry schemas into Phase 5 as executable model/fixture contracts and approval-gate semantic changes. |
| Stack proof becomes decorative. | Require each stack element to own a useful product, automation, integration, or deployment responsibility before adding it. |
| Stack proof is deferred so long it never materializes. | Planning should create explicit future stack slices with triggers, especially CI and Vue/TypeScript review UI. |

## Planning & Decomposition Handoff

If approved, Planning & Decomposition should use:

- **Decisions:** Python CLI/action-style runner, early CI proof, standard-library-first dependency posture, JSON report artifact, deterministic matching, canonical fixture and catalog paths, small module boundaries, staged portfolio stack evidence path.
- **Inputs:** Requirements artifact, canonical IoT sensor fixture definition, mock emissions catalog structure, report shape in this document.
- **Implementation units:** Package scaffold, fixture data, input validation, catalog lookup, matcher, calculator, report builder, review notes, CLI, report schema/model contracts, tests, CI workflow candidate, optional human-readable renderer candidate.
- **Open risks:** Packaging metadata, exact test framework, whether generated reports should be committed, whether Phase 5 needs standalone JSON Schema or fixture-driven executable contracts are enough, and which follow-on stack slice should come immediately after the Python report core.
- **Non-goals:** Hosted service, UI, supplier API, database, compliance-grade methodology, multi-BOM delta, integration handoff.
- **Validation signals:** CLI writes a durable JSON artifact; tests cover mixed-case fixture, matching statuses, subtotal math, contributor rankings, flags, caveat, deterministic timestamps, and schema/model stability; CI can run the same checks once scaffold exists.

## Loom Process Feedback

| Observation | Suggested Template/Guide Improvement | Project-Specific? |
|-------------|--------------------------------------|-------------------|
| Architecture benefits from a required report-shape section when Requirements chooses JSON-first output. | Add a "Durable Artifact Shape" section to Architecture templates for structured-output projects. | No |
| Fixture paths are architecture decisions, not just test details, when they shape CLI examples and acceptance flow. | Add "Fixture and Artifact Paths" to Architecture templates for local automation projects. | No |
| Loom has schema prompts across Architecture, Planning, and Contracts & Tests, but the ownership boundary is implicit. | Add explicit guidance: Architecture sketches data shape, Planning creates schema work items, Contracts & Tests locks executable schema/model contracts, Implementation satisfies them. | No |

## Phase Gate

- **Agent recommendation:** [x] Ready for owner review [ ] Not ready
- **Owner decision:** [x] Approved [ ] Needs revision [ ] Deferred
- **Decision date:** 2026-06-25
- **Remaining concerns:** None blocking Planning & Decomposition. Remaining choices about test framework, standalone schema contracts, generated report commit policy, and first follow-on stack slice should be sequenced in Planning rather than reopened in Architecture.
