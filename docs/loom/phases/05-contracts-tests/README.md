# Phase 5: Contracts & Tests

## Phase Purpose

Lock the executable behavior of the first BOM Carbon Report before the Python engine is implemented.

This phase converts approved requirements, architecture, and planning into model contracts, fixture expectations, and a traceable test matrix. It should make implementation unambiguous without implementing production modules.

## Phase Inputs

| Input | Source | Use |
|-------|--------|-----|
| Product behavior and acceptance criteria | [Requirements](../02-requirements/README.md) | Trace required behavior to executable checks. |
| Models, matching, calculations, and report shape | [Architecture](../03-architecture/README.md) | Lock fields, statuses, precedence, totals, and output sections. |
| Contract candidates and implementation units | [Planning](../04-planning-decomposition/README.md) | Preserve the Phase 5 boundary and Implementation handoff. |
| Project ledger | [Project Progress](../../PROGRESS.md) | Track decisions, questions, completion, and gate status. |

## Contract Strategy

Approved strategy:

- Use `pytest` as the development test runner.
- Make JSON fixtures plus Python assertions the binding contracts for the first slice.
- Defer standalone JSON Schema until a consumer needs language-neutral validation.
- Keep runtime validation implementable with the Python standard library.
- Approval-gate changes to top-level report keys, required line fields, statuses, match precedence, and total inclusion rules after this phase closes.
- Commit focused fixtures and executable contract tests during Phase 5, before production implementation begins.
- The Phase 5 suite is expected to fail because the production package does not exist yet; failures must be attributable to missing implementation, not malformed fixtures or ambiguous assertions.

## Model Contracts

### BOM Input

| Contract | Binding Expectation | Failure Behavior |
|----------|---------------------|------------------|
| Root | JSON object with a non-empty `line_items` array. | Reject clearly. |
| Part number | Each line has a non-empty string `part_number`. | Reject the BOM. |
| Quantity | Each line has a positive number; booleans are invalid. | Reject the BOM. |
| Category | Missing, empty, or whitespace category becomes `uncategorized`. | Do not reject for category absence. |
| Optional fields | Preserve `description`, `manufacturer`, and `manufacturer_part_number` when present. | Absence is valid. |

### Emissions Catalog Input

| Contract | Binding Expectation | Failure Behavior |
|----------|---------------------|------------------|
| Root | JSON object with a `factors` array. An empty array is valid. | Reject a missing or non-array `factors` value. |
| Match fields | Each factor has non-empty `match_key` and supported `match_type`. | Reject the catalog. |
| Factor | `emission_factor_kgco2e` is numeric and non-negative; booleans are invalid. | Reject the catalog. |
| Confidence | Missing confidence becomes `unknown` and creates a visible signal when used. | Do not reject for confidence absence. |
| Source note | Preserve `source_note` when present. | Absence is valid. |
| Duplicate key | Conflicting records for the same normalized `match_type` and `match_key` are retained as a reportable data-quality condition. | Continue report generation; identify every conflicting factor row. |

Supported first-slice `match_type` values are `part_number` and `category`.

Normalization rules:

- Part numbers and part-number match keys trim surrounding whitespace but remain case-sensitive.
- Categories and category match keys trim surrounding whitespace and normalize to lowercase.
- Match types trim surrounding whitespace and normalize to lowercase.
- Matching and duplicate/conflict detection use the same normalized values.

An empty factor array represents valid but entirely uncovered catalog data. Report generation continues, every BOM line receives a `missing_factor` error and is excluded, contributor arrays are empty, and the total is zero.

A factor of exactly zero is valid, usable data and is not flagged by default. When the CLI is run with `--warn-on-zero-factor`, matched zero-factor lines remain included with zero subtotals and receive a `zero_factor` warning.

Duplicate factors do not stop report generation, but the matcher cannot choose a trustworthy value. Each affected BOM line receives `conflicting_factor`, has null factor and subtotal values, and is excluded from totals. Its error flag identifies the normalized conflicting key plus every conflicting catalog row position and value. The generated report is partial and must make exclusions visible. Users correct the source catalog and regenerate the report; a future input UI may highlight and edit the conflicting rows directly.

## Matching Contract

Matching is deterministic:

1. Exact `part_number` match against a `part_number` factor.
2. Normalized category match against a `category` factor.
3. `missing_factor` if neither produces a usable factor.

| Result | `match_status` | Included | Required Signal |
|--------|----------------|----------|-----------------|
| Acceptable part match | `matched` | Yes | No match-quality flag required. |
| Category fallback | `estimated` | Yes | Estimated-factor flag. |
| Usable weak-confidence factor | `low_confidence` | Yes | Low-confidence flag. |
| No usable factor | `missing_factor` | No | Missing-factor and exclusion signal. |
| Conflicting factors | `conflicting_factor` | No | Conflict error with source row positions and values. |
| Missing/weak category | Primary status above; category is `uncategorized` | Depends | Independent uncategorized signal. |

Tests must prove that a part match wins over a category fallback and that `uncategorized` is a data-quality condition, not a replacement for the primary match status.

## Calculation Contract

- `subtotal_kgco2e = quantity * emission_factor_kgco2e` for usable factors.
- Missing-factor lines have no numeric subtotal and do not contribute to totals.
- `part_count` counts all BOM lines; `quantity_count` sums all quantities.
- `total_estimated_kgco2e` is the sum of included line subtotals.
- `excluded_line_count` counts lines where `included_in_total` is false.
- `coverage_status` is `complete` when no lines are excluded and `partial` when one or more lines are excluded.
- Warnings on included lines do not make coverage partial.
- Category totals aggregate included subtotals under normalized categories.
- Contributor rankings sort by subtotal descending.
- Ties use ascending `part_number` for lines and ascending category name for categories.
- This ordering is the JSON artifact's deterministic default; downstream UIs may offer alternate user-selected sorting without changing report semantics.
- Contributor arrays contain every included line item and category; the durable artifact does not truncate to a fixed top-N subset.
- The future UI shows all contributors by default and lets users sort and filter both views.
- Tests use exact decimal-friendly values or `pytest.approx`.
- Preserve source `quantity` and `emission_factor_kgco2e` values as supplied.
- Round calculated line subtotals, category totals, and the BOM total to three decimal places.
- Calculate aggregates from serialized rounded line subtotals so visible report values add up exactly.

## Report Contract

Required top-level keys:

1. `report_metadata`
2. `bom_summary`
3. `top_carbon_contributors`
4. `line_items`
5. `data_quality_flags`
6. `review_notes`
7. `methodology_caveat`

Each report line requires `part_number`, `description`, `category`, `quantity`, `match_status`, `match_type`, `emission_factor_kgco2e`, `subtotal_kgco2e`, `confidence`, `source_note`, and `included_in_total`.

Additional expectations:

- `generated_at` is a valid, timezone-aware ISO-8601 timestamp, preferably UTC.
- Tests validate its presence, format, and timezone but do not compare its exact value.
- Contributor arrays arrive ranked; consumers do not recalculate rankings.
- Each quality flag requires `flag_type`, `severity`, `part_number`, and a human-readable `message`.
- A flag may include optional `details` for additional structured context without changing the core contract.
- Stable first-slice flag types and severities are:

| `flag_type` | Default `severity` | Meaning |
|-------------|--------------------|---------|
| `missing_factor` | `error` | No factor was found and the line is excluded from totals. The report still generates. |
| `conflicting_factor` | `error` | Multiple factors conflict; the line is excluded and the report still generates. |
| `estimated_factor` | `warning` | A category-level estimated factor was used. |
| `low_confidence` | `warning` | A usable factor with weak or unknown confidence was used. |
| `uncategorized` | `warning` | The line lacks useful category data. |
| `zero_factor` | `warning` | Opt-in signal that a usable matched factor is exactly zero. |
- Notes surface high contributors and any missing, estimated, or low-confidence data present.
- The caveat explicitly says mock data is not compliance-grade.
- UI consumers should label a `partial` total as a partial estimate rather than presenting it as complete.
- Tests assert structure and semantics, not object key order or one monolithic snapshot.

## Fixture Plan

| Fixture | Purpose | Minimum Cases |
|---------|---------|---------------|
| Canonical BOM + mock catalog | Shared mixed-case acceptance path | Part matches, category estimates, weak confidence, missing factor, uncategorized line, conflicting factors, repeated category, dominant contributor, and partial coverage. |
| `happy-path.bom.json` | Small calculation proof | Two or three matched lines with hand-checkable totals. |
| `matching-catalog.json` | Precedence/status proof | Competing part/category factors and weak/unknown confidence. |
| `missing-factor.bom.json` | Exclusion proof | At least one included and one excluded line. |
| `invalid-bom-*.json` | BOM rejection | Missing/empty lines, missing part, invalid quantity. |
| `invalid-catalog-*.json` | Catalog rejection | Missing factors, bad match type, invalid factor. |

Focused fixtures belong under `tests/fixtures/` and should stay smaller than the canonical acceptance fixture.

### Canonical BOM Composition

The canonical IoT sensor BOM contains ten lines:

| Line | Category | Contract Behavior |
|------|----------|-------------------|
| Main PCB | `pcb` | Clean part match and high contributor. |
| MCU | `processor` | Clean part match. |
| Environmental sensor | `sensor` | Low-confidence part match. |
| Battery | `power` | Clean part match and dominant contributor. |
| Connector | `connector` | Category-level estimate. |
| Resistor pack | `passives` | Category-level estimate. |
| Capacitor pack | `passives` | Clean part match and repeated-category aggregation. |
| Enclosure | `mechanical` | Conflicting part factors and exclusion. |
| Cable | `cable` | Missing factor and exclusion. |
| Product label | `uncategorized` after normalization | Clean part match plus independent uncategorized warning. |

### Canonical Expected Values

| Line | Quantity | Factor | Subtotal |
|------|----------|--------|----------|
| Main PCB | 1 | 4.00 | 4.00 |
| MCU | 1 | 2.00 | 2.00 |
| Environmental sensor | 1 | 1.50 | 1.50 |
| Battery | 1 | 8.00 | 8.00 |
| Connectors | 2 | 0.50 | 1.00 |
| Resistor pack | 20 | 0.02 | 0.40 |
| Capacitor pack | 10 | 0.03 | 0.30 |
| Enclosure | 1 | conflicting 2.00 and 2.50 | Excluded |
| Cable | 1 | Missing | Excluded |
| Product label | 1 | 0.10 | 0.10 |

The canonical report must produce:

- `part_count`: 10
- `quantity_count`: 39
- `total_estimated_kgco2e`: 17.3
- `excluded_line_count`: 2
- `coverage_status`: `partial`
- `data_quality_flag_count`: 6
- Flags: two `estimated_factor` warnings and one each of `low_confidence`, `conflicting_factor`, `missing_factor`, and `uncategorized`.

## Test Matrix

| ID | Level | Target | Assertion | Trace |
|----|-------|--------|-----------|-------|
| CT-1 | Unit | BOM validation | Required fields reject; category normalizes. | FR-1, NFR-2 |
| CT-2 | Unit | Catalog validation | Factor fields validate; absent confidence becomes `unknown`. | FR-2, FR-8 |
| CT-3 | Unit | Matcher | Exact part match wins over category. | FR-3 |
| CT-4 | Unit | Statuses | All status and uncategorized signals stay explicit. | FR-3, FR-8 |
| CT-5 | Unit | Calculator | Subtotals, totals, counts, exclusions, and categories follow contract. | FR-4, FR-5 |
| CT-6 | Unit | Rankings | Lines/categories rank with deterministic ties. | FR-6 |
| CT-7 | Unit | Report | Required top-level and line fields exist. | FR-7, FR-11, NFR-6 |
| CT-8 | Unit | Flags/notes | Weak data is visible and actionable. | FR-8, FR-9 |
| CT-9 | Unit | Caveat | Mock-data and non-compliance language is explicit. | FR-10 |
| CT-10 | Unit | Timestamp | `generated_at` is present, valid ISO-8601, and timezone-aware; its exact value is ignored. | NFR-1, NFR-3 |
| CT-11 | Fixture | Canonical report | Every required section, status family, and contributor lens appears. | FR-1–FR-11 |
| CT-12 | CLI | Success | Creates parents, writes JSON, prints path/total, exits zero; optional zero-factor warning mode is honored. | FR-11, NFR-1 |
| CT-13 | CLI | Invalid input | Exits non-zero with useful error and no false success. | FR-1, FR-2, NFR-3 |

For structurally valid inputs, partial reports are written and exit zero by default. The CLI prints the artifact path, total, and excluded-line count. With `--fail-on-data-errors`, the same partial artifact is written first and the command then exits non-zero, allowing CI to require complete coverage without losing diagnostics. Structurally unreadable or invalid inputs remain fatal and do not produce a report.

## Planned Test Layout

```text
tests/
  conftest.py
  test_validation.py
  test_matching.py
  test_calculation.py
  test_report_generation.py
  test_cli.py
```

Tests assert public behavior at module boundaries. Private helpers and internal container types are not contracts.

The stable Python boundary is:

```python
from bomflow import generate_report

report = generate_report(bom_data, catalog_data)
```

Focused tests call `generate_report` with in-memory dictionaries. CLI tests exercise file loading, artifact writing, optional flags, messages, and exit codes. Tests do not lock helper function names in matcher, calculator, validation, or report-building modules.

## Implementation Definition Of Done

- CT-1 through CT-13 are executable and pass locally with `pytest`.
- Tests regenerate the canonical report instead of reading a committed `reports/` artifact.
- Runtime uses only the Python standard library.
- Invalid inputs fail clearly with non-zero CLI behavior.
- Timestamp presence, ISO-8601 format, and timezone awareness are covered without exact-value assertions.
- Contract changes are recorded rather than silently absorbed by code or snapshots.

## Decisions To Confirm

| Decision | Draft Choice | Rationale | Owner |
|----------|--------------|-----------|-------|
| Binding mechanism | Pytest assertions over focused JSON fixtures | Executable and sufficient before a language-neutral consumer exists. | John |
| JSON Schema | Defer until a consumer needs language-neutral validation | No current downstream validator needs it. | John |
| Timestamp contract | Validate presence, ISO-8601 format, and timezone; ignore exact value | Prevents time-dependent failures without adding an injection seam that the first version does not otherwise need. | John |
| Ranking ties | Ascending stable semantic key in JSON; UI consumers may re-sort | Keeps the artifact deterministic while allowing users to choose how a future viewer presents the data. | John |
| Phase 5 code boundary | Commit fixtures and executable contract tests before Phase 6 | The tests and contracts define what Implementation must satisfy. | John |
| Data-quality flag shape | Require `flag_type`, `severity`, `part_number`, and `message`; allow optional `details` | Supports automation, UI filtering/emphasis, item traceability, and direct human interpretation. | John |
| Flag types and severities | `missing_factor` is `error`; `estimated_factor`, `low_confidence`, and `uncategorized` are `warning` | Distinguishes excluded data from usable-but-weak data while allowing the report to complete. | John |
| Empty emissions catalog | Accept `factors: []` and generate an all-missing, zero-total report | Distinguishes valid-but-uncovered data from malformed input and keeps coverage visible in the report. | John |
| Duplicate catalog factors | Generate a partial report, mark affected lines `conflicting_factor`, exclude them, and identify all conflicting rows/values | Preserves useful trustworthy results without silently choosing an ambiguous factor; users can correct the catalog and regenerate. | John |
| Match-key normalization | Trim all keys; preserve part-number case; lowercase categories and match types | Protects potentially significant manufacturer identifiers while making human-entered categorical fields forgiving and deterministic. | John |
| Zero-valued factors | Accept and include without a default flag; add `zero_factor` warning only with `--warn-on-zero-factor` | Distinguishes explicit zero from missing data while letting operators opt into stricter quality signaling. | John |
| Partial-report status | Require `bom_summary.coverage_status` with `complete` or `partial` based on excluded lines | Lets JSON and UI consumers describe incomplete totals honestly without interpreting individual flags. | John |
| Canonical conflict coverage | Include conflicting factors in the shared BOM/catalog acceptance path | Makes the primary demo prove partial reporting, actionable conflict details, and the source-correction workflow. | John |
| Canonical fixture composition | Use ten IoT sensor BOM lines spanning every approved status and repeated passives | Keeps the shared acceptance path representative but small enough to audit manually. | John |
| Canonical fixture values | Use decimal-friendly quantities and factors totaling 17.3 kgCO2e with two exclusions and six flags | Makes every subtotal, aggregate, exclusion, and quality count hand-checkable. | John |
| Numeric serialization | Preserve source numbers; round calculated carbon values to three decimal places and aggregate visible subtotals | Gives stable gram-level JSON precision without implying unrealistic accuracy and keeps displayed arithmetic internally consistent. | John |
| Partial-report CLI exit | Exit zero by default; `--fail-on-data-errors` writes the artifact and then exits non-zero | Supports human diagnostic workflows and strict CI enforcement without discarding the useful partial report. | John |
| Contributor extent and UI defaults | Retain and show all contributors by default; allow UI sorting and filtering | Preserves complete durable data and gives users control over presentation without changing report semantics. | John |
| Test interface boundary | Lock one public `bomflow.generate_report` API plus the CLI; leave internal helpers flexible | Enables fast focused tests and end-to-end user checks without making refactoring an accidental contract break. | John |

## Risks And Controls

| Risk | Control |
|------|---------|
| Tests mirror implementation details. | Assert boundaries and durable JSON semantics only. |
| A golden snapshot hides regressions. | Use focused structural and numeric assertions. |
| Canonical fixture is hard to reason about. | Pair it with small rule-specific fixtures. |
| `uncategorized` conflicts with match status. | Keep it as normalized category plus independent signal. |
| Schemas add maintenance without a consumer. | Defer them until a language-neutral boundary exists. |

## Implementation Handoff

If approved, Implementation receives binding input validation, matching, calculation, report, timestamp, and CLI contracts; a committed, initially failing `pytest` suite; a canonical mixed-case pair plus focused fixtures; standard-library runtime constraints; and approval-gated report semantics.

Non-goals remain production engine code in Phase 5, standalone schema without a consumer, UI/service/infrastructure work, and production emissions science.

## Contract Suite Validation

Phase 5 produced 25 collected pytest cases across validation, matching, calculation, report generation, and CLI behavior.

Pre-implementation validation on 2026-07-14:

- Canonical BOM and catalog JSON parse successfully.
- Test modules compile successfully.
- `pytest --collect-only` collects all 25 cases.
- The full suite fails because `bomflow` and `python -m bomflow` do not exist yet.
- No production package or implementation scaffold was added in Phase 5.

This is the intended red contract state. Phase 6 should make the suite pass without weakening approved assertions.

## Phase Gate

- **Agent recommendation:** [x] Ready for owner review [ ] Not ready
- **Owner decision:** [ ] Approved [ ] Needs revision [ ] Deferred
- **Decision date:** TBD
- **Remaining concerns:** None from the agent. Owner gate review remains.
