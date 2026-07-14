# Phase 4: Planning & Decomposition

## Planning Purpose

Translate the approved Architecture into sequenced implementation work for the BOM Carbon Report.

This phase decides what should be built first, what belongs in Contracts & Tests before implementation, what can wait, and how the first useful version should move from docs-only planning into a runnable local Python workflow.

Phase 4 should not reopen product scope or implement the code. It should make the next phases executable.

## Planning Inputs

| Input | Source | Planning Use |
|-------|--------|--------------|
| Product scope and acceptance criteria | [Requirements](../02-requirements/README.md) | Keep the work focused on the JSON-first BOM Carbon Report for one BOM and one mock catalog. |
| Architecture decisions | [Architecture](../03-architecture/README.md) | Preserve Python CLI, module boundaries, fixture paths, report shape, matching order, and standard-library-first posture. |
| Architecture handoff risks | [Architecture Handoff](../03-architecture/README.md#planning--decomposition-handoff) | Sequence test framework, generated report policy, schema contracts, CI, and follow-on stack proof. |
| Project progress ledger | [Project Progress](../../PROGRESS.md) | Update phase status and keep open questions visible. |

## Planning Principles

- Build the smallest runnable report engine that satisfies the approved report semantics.
- Lock contract expectations before implementation changes report behavior.
- Keep generated artifacts separate from source fixtures unless there is a deliberate demo reason to commit one.
- Prefer local, deterministic, inspectable workflow steps over infrastructure.
- Add portfolio stack evidence only when it proves real BOMFlow behavior.

## Workstream Sequence

| Order | Workstream | Purpose | Landing Phase |
|-------|------------|---------|---------------|
| 1 | Contracts and fixture contracts | Define executable expectations before implementation. | Phase 5 |
| 2 | Python package scaffold | Create the runnable local package and command surface. | Phase 6 |
| 3 | Fixture and catalog data | Add canonical BOM and mock emissions catalog source inputs. | Phase 6 |
| 4 | Core report engine | Implement input loading, matching, calculation, report assembly, and notes. | Phase 6 |
| 5 | CLI and generated artifact policy | Make the workflow runnable and decide generated output handling. | Phase 6 |
| 6 | CI proof | Run tests and fixture report generation in GitHub Actions once local commands exist. | Phase 6 or hardening slice |
| 7 | Optional human-readable/report-view slice | Consume report JSON in a thin TypeScript viewer when the JSON contract is stable. | Future mini-Loom |

## Implementation Units

| ID | Unit | Description | Dependencies | Primary Files | Acceptance Signal |
|----|------|-------------|--------------|---------------|-------------------|
| P4-1 | Contract test plan | Define the exact test targets for input validation, matching statuses, subtotal math, rankings, flags, caveat, deterministic timestamps, and CLI output. | Architecture | `docs/loom/phases/05-contracts-tests/README.md`, `tests/` | Phase 5 has an executable test list tied to acceptance criteria. |
| P4-2 | Schema/model contract decision | Decide whether fixture-driven Python tests are enough or whether JSON Schema files are needed for BOM, catalog, and report artifacts. | P4-1 | `tests/`, optional `schemas/` | Phase 5 records the binding contract mechanism before implementation. |
| P4-3 | Package scaffold | Create the `bomflow` package with modules from Architecture and a module entrypoint. | P4-1 | `bomflow/__init__.py`, `bomflow/cli.py`, `bomflow/models.py` | `python -m bomflow` can expose the intended command surface. |
| P4-4 | Canonical acceptance fixture | Add the mixed-case IoT sensor BOM fixture and mock emissions catalog. | P4-1, P4-2 | `data/fixtures/canonical-iot-sensor.bom.json`, `data/catalogs/mock-emissions-catalog.json` | Fixture includes matched, estimated, low-confidence, missing-factor, and uncategorized cases. |
| P4-5 | Input loading and validation | Load local JSON files and validate required fields without external services. | P4-3, P4-4 | `bomflow/io.py`, `bomflow/models.py` | Invalid input fails clearly; missing category normalizes to `uncategorized`. |
| P4-6 | Catalog lookup | Normalize emissions factors into part-number and category lookup structures. | P4-4, P4-5 | `bomflow/catalog.py` | Factors can be resolved deterministically by match type and key. |
| P4-7 | Matcher | Apply exact part-number match, category fallback, quality statuses, and missing-factor behavior. | P4-6 | `bomflow/matcher.py` | Each canonical fixture line receives the expected match status and inclusion behavior. |
| P4-8 | Calculator | Calculate line subtotals, BOM totals, excluded counts, and category totals. | P4-7 | `bomflow/calculator.py` | Summary total equals included line subtotals; category totals aggregate correctly. |
| P4-9 | Report builder | Assemble durable JSON with stable top-level sections and report lines. | P4-8 | `bomflow/report.py`, `bomflow/models.py` | Report JSON contains required sections, metadata, contributors, flags, notes, and caveat. |
| P4-10 | Review notes | Generate concise notes from contributors and quality flags. | P4-9 | `bomflow/notes.py` | Notes call attention to high contributors, missing factors, estimated factors, and low-confidence data. |
| P4-11 | CLI runner | Connect modules into `python -m bomflow report --bom ... --catalog ... --out ...`. | P4-5 through P4-10 | `bomflow/cli.py` | Command writes JSON, creates output directories, exits non-zero on invalid inputs, and prints path plus total. |
| P4-12 | Generated artifact policy | Decide whether `reports/bom-carbon-report.json` is committed as a demo artifact or treated as generated output. | P4-11 | `.gitignore`, `reports/` | Policy is recorded and tests do not rely on stale generated files. |
| P4-13 | CI workflow candidate | Add CI once local tests and CLI command exist. | P4-1 through P4-12 | `.github/workflows/bomflow.yml` | Push/PR can run tests and optionally generate the canonical report. |
| P4-14 | Follow-on stack slice | Choose the first useful stack proof after the Python report core. | P4-9, P4-11 | Future `web/`, `service/`, `Dockerfile`, or docs | Next mini-Loom has a concrete user/operator problem: a thin TypeScript report viewer, with framework choice deferred. |

## Phase 5 Contracts & Tests Handoff

Contracts & Tests should start with these contract candidates:

| Contract Candidate | Binding Expectation | Suggested Test Shape |
|--------------------|--------------------|----------------------|
| BOM input model | Required `line_items`; required `part_number`; positive numeric `quantity`; missing `category` becomes `uncategorized`. | Unit tests for valid, missing, and invalid BOM fixtures. |
| Emissions catalog model | Required `factors`; required `match_key`, `match_type`, and non-negative numeric factor; missing `confidence` becomes visible quality signal. | Unit tests for valid catalog and invalid factor records. |
| Matching statuses | Stable enum-like values: `matched`, `estimated`, `low_confidence`, `missing_factor`, and `uncategorized` signal. | Matcher tests against focused fixtures. |
| Calculation semantics | Totals include only usable factors; missing factors are excluded and counted. | Calculator tests with exact decimal-friendly fixture values. |
| Report shape | Stable top-level keys from Architecture and required line fields. | Fixture or snapshot-style assertions against generated JSON structure. |
| Timestamp determinism | Tests can set or inject `generated_at`. | Report builder or CLI test with deterministic value. |
| CLI behavior | Local command writes artifact, creates parent directory, exits clearly on invalid input. | Subprocess or direct CLI invocation tests. |

Default recommendation: use `pytest` for readable focused tests unless the repository intentionally stays standard-library-only with `unittest`. Do not add Pydantic, JSON Schema validators, or other validation dependencies unless Phase 5 decides standalone schema artifacts are worth the extra surface area.

## Implementation Order

Recommended implementation order after contracts are drafted:

1. Add package scaffold and CLI skeleton.
2. Add canonical BOM and mock catalog fixtures.
3. Add input loading and validation.
4. Add catalog lookup and matcher.
5. Add calculator and aggregation.
6. Add report builder and deterministic timestamp support.
7. Add review notes.
8. Wire the CLI end to end.
9. Add or update tests until the contract suite passes.
10. Add CI workflow once local commands are stable.

This order keeps every step runnable and avoids waiting until the end to discover that a report contract cannot be satisfied.

## Generated Artifact Policy

Approved policy:

- Treat `reports/` as generated output by default.
- Commit source fixtures and catalogs.
- Do not require committed generated reports for tests.
- Allow one clearly labeled example report under `examples/` later if it improves portfolio review or documentation; generate it from the canonical mock fixture.

This keeps implementation honest: the CLI and tests must regenerate artifacts instead of depending on stale JSON.

## Dependency And Tooling Decisions

| Decision | Phase 4 Recommendation | Rationale |
|----------|------------------------|-----------|
| Python dependencies | Standard library for runtime | Keeps the report engine inspectable and easy to run. |
| Test framework | Use `pytest` as a development dependency | More readable parameterized tests and CLI assertions, without adding an application runtime dependency. |
| JSON Schema | Defer unless Phase 5 needs standalone schemas | Fixture-driven tests are likely enough for the first local automation slice. |
| Packaging metadata | Add only enough to run and test consistently | Avoid overbuilding distribution before the CLI proves useful. |
| CI | Add after tests and CLI exist | CI should prove real behavior, not just empty scaffolding. |
| Generated reports | Ignore by default | Prevent stale generated artifacts from becoming accidental source of truth. |

## Follow-On Stack Slice

The first follow-on stack proof should be a thin TypeScript report viewer after the JSON report contract is stable. The preserved AllSpice role notes support a structured review surface but do not identify a frontend framework, so Vue, React, or another framework should be selected when this mini-Loom begins.

Recommended trigger:

- The Python CLI can generate the canonical JSON report.
- The report top-level keys and contributor structures are covered by tests.
- There is at least one representative generated report available for local UI development.

Recommended scope:

- Load generated report JSON.
- Show BOM summary, top line-item contributors, top category contributors, data-quality flags, and review notes.
- Show all line-item and category contributors by default and let users sort and filter both views while treating report JSON ordering as the initial order.
- Avoid editing, persistence, hosted service, auth, supplier APIs, or compliance claims.

A future catalog upload or configuration surface is separate from this report viewer slice. If added, it should use report conflict details to highlight all catalog rows involved in a duplicate normalized match key, let the user correct them, and regenerate the report.

Go, Postgres, Docker, Terraform/AWS, and Rust should remain deferred until they own a real service, persistence, deployment, or utility problem.

## Planning Decisions

| Decision | Choice | Rationale | Owner |
|----------|--------|-----------|-------|
| First workstream | Contracts & Tests before implementation | Prevents report semantics from drifting while code is being written. | John + Codex |
| Runtime implementation sequence | Package scaffold, fixtures, validation, lookup, matcher, calculator, report, notes, CLI, tests, CI | Preserves architecture boundaries and keeps progress runnable. | Codex |
| Generated report policy | Ignore routine output under `reports/`; allow one clearly labeled generated example under `examples/` later | Source fixtures remain durable inputs while reviewers can inspect a representative artifact without making generated output the source of truth. | John + Codex |
| Test framework posture | Use `pytest` as a development dependency | It improves test readability without becoming an application runtime dependency. | John + Codex |
| Schema posture | Start with executable tests and fixtures; add JSON Schema only if Phase 5 finds a downstream need | Avoids contract overhead before a consumer needs standalone schemas. | Codex |
| First follow-on stack proof | Framework-neutral TypeScript report viewer after JSON contract stability | Gives useful typed-frontend evidence while consuming the Python report artifact; framework selection waits for current evidence and needs. | John + Codex |
| Phase gate status | Draft plan opened; owner approval pending | Agent can recommend readiness but owner approves the phase gate. | John + Codex |

## Risks And Planning Controls

| Risk | Control |
|------|---------|
| Implementation starts before contracts are clear. | Make Phase 5 the next required phase and carry explicit contract candidates forward. |
| Planning over-specifies implementation details. | Keep module boundaries stable but allow exact file and helper names to evolve during implementation. |
| Generated reports become stale source artifacts. | Ignore generated outputs by default and regenerate in CLI/tests. |
| JSON Schema adds work without a consumer. | Use fixture-driven executable contracts first. |
| CI arrives too early to prove anything useful. | Add CI after local tests and CLI are stable. |
| Portfolio stack work distracts from the core report. | Defer the TypeScript viewer until the report artifact is stable; defer framework selection, service, and infrastructure until useful. |

## Contracts & Tests Handoff

If approved, Contracts & Tests should use:

- **Decisions:** Contracts before implementation, runtime standard-library-first, `pytest` for development testing, generated reports ignored by default, and a framework-neutral TypeScript viewer as the first follow-on stack slice.
- **Inputs:** Requirements acceptance criteria, Architecture report shape and matching rules, Planning implementation units and contract candidates.
- **Contract targets:** BOM input, emissions catalog input, report JSON shape, matching statuses, calculation totals, data-quality flags, deterministic timestamp, CLI behavior.
- **Open risks:** Whether to add standalone JSON Schema artifacts and the exact packaging metadata for the approved `pytest` development dependency. A labeled example report may be added later if useful for portfolio review.
- **Non-goals:** Implementing the Python engine during Phase 5, adding a UI, adding hosted service/infrastructure, adding real emissions science, or implementing future roadmap parts.
- **Validation signals:** Phase 5 exits with a clear test plan, fixtures or fixture expectations, contract assertions, and an implementation-ready definition of done.

## Loom Process Feedback

| Observation | Suggested Template/Guide Improvement | Project-Specific? |
|-------------|--------------------------------------|-------------------|
| Planning benefits from explicit work-package IDs that can carry into Contracts & Tests and Implementation. | Add a required implementation-unit table with IDs, dependencies, files, and acceptance signals to Planning templates. | No |
| Generated artifact policy belongs in Planning for local automation projects. | Add a prompt asking whether generated outputs should be committed, ignored, or regenerated in CI. | No |
| Portfolio stack evidence needs sequencing discipline. | Add a "follow-on stack slice" prompt that requires a user/operator problem before adding a stack element. | No |

## Phase Gate

- **Agent recommendation:** [x] Ready for owner review [ ] Not ready
- **Owner decision:** [x] Approved [ ] Needs revision [ ] Deferred
- **Decision date:** 2026-07-13
- **Remaining concerns:** None. Proceed to Contracts & Tests.
