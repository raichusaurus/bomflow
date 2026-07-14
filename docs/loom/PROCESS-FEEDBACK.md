# Loom Process Feedback

Reusable feedback for improving Loom phase templates and guides. These observations came from the BOMFlow Requirements phase, but the suggestions are intended to apply across projects.

## Phase Gate Authority

Phase templates should separate agent readiness recommendations from owner approval.

Suggested template:

```md
## Phase Gate

- **Agent recommendation:** [ ] Ready [ ] Not ready
- **Owner decision:** [ ] Approved [ ] Needs revision [ ] Deferred
- **Decision date:** TBD
- **Remaining concerns:** TBD
```

Rationale: an agent can draft, score, and recommend, but should not mark a phase complete or start the next phase without explicit owner approval.

## Phase Decision Log

Each phase artifact should include a local decision log, even when the root project ledger also records decisions.

Suggested template:

```md
## Phase Decisions

| Decision | Choice | Rationale | Owner |
|----------|--------|-----------|-------|
```

Rationale: phase-level decisions are easier to review when they live next to the requirements, architecture, plan, or test contracts they shape.

## Agent Authority

Phase guides should make agent authority explicit.

Suggested template:

```md
## Agent Authority

The agent may:

- Draft phase artifacts.
- Recommend phase readiness.
- Update progress scores for draft completeness.
- Identify open questions, risks, and next-phase handoff items.

The agent may not:

- Mark a phase gate approved without explicit owner approval.
- Start the next phase unless asked or approved.
- Convert a recommendation into an owner decision.
```

Rationale: this prevents a drafted handoff from being mistaken for a closed gate.

## Artifact Completeness Vs Gate Completion

Progress ledgers should distinguish artifact completeness from phase-gate completion.

Suggested template:

```md
**Artifact Completeness:** 100%
**Gate Status:** Pending owner approval
**Phase Complete:** 95%
```

Rationale: a phase artifact can be complete enough for review while the phase itself remains open until the owner approves the gate.

## Next Phase Handoff

Phase artifacts should prepare the next phase without automatically starting it.

Suggested template:

```md
## Next Phase Handoff

If approved, the next phase should use:

- Decisions:
- Inputs:
- Open risks:
- Non-goals:
- Validation signals:
```

Rationale: this preserves momentum and context while respecting gate authority.

## Loom Process Feedback Capture

Each phase template should include a lightweight process-feedback section.

Suggested template:

```md
## Loom Process Feedback

| Observation | Suggested Template/Guide Improvement | Project-Specific? |
|-------------|--------------------------------------|-------------------|
```

Rationale: Loom should improve as phases expose reusable workflow lessons. Capturing feedback locally makes process learning visible without mixing it into product scope.

## Highest-Priority Template Change

Add explicit gate authority to every phase template first.

The most important distinction is:

- Agent recommendation: the draft appears ready.
- Owner approval: the phase gate is closed.

That split should be visible in every phase artifact and progress ledger.

## Schema Contract Ownership

Loom templates should make schema ownership explicit across phases.

Suggested guidance:

```md
## Schema / Model Contract Boundary

- Architecture sketches conceptual data shape, source of truth, stable identifiers, and downstream compatibility expectations.
- Planning & Decomposition creates work items for schemas, model contracts, fixture coverage, and compatibility checks.
- Contracts & Tests locks executable schema/model contracts with fixtures, tests, and stability rules.
- Implementation satisfies those contracts and approval-gates semantic contract changes.
```

Rationale: structured-output projects can otherwise drift between architecture diagrams, planning tasks, test fixtures, and implementation details without a single phase owning when schemas become binding.

## Planning Work Package IDs

Planning templates should include explicit work-package IDs that can carry into Contracts & Tests and Implementation.

Suggested template:

```md
## Implementation Units

| ID | Unit | Description | Dependencies | Primary Files | Acceptance Signal |
|----|------|-------------|--------------|---------------|-------------------|
```

Rationale: stable IDs make it easier to trace planned work into tests, implementation commits, progress ledgers, and follow-on phase handoffs.

## Generated Artifact Policy

Local automation projects should decide generated artifact handling during Planning & Decomposition.

Suggested prompt:

```md
## Generated Artifact Policy

- Which files are source inputs?
- Which files are generated outputs?
- Should generated examples be committed, ignored, regenerated in CI, or published separately?
- What prevents stale generated files from becoming accidental source of truth?
```

Rationale: generated reports, snapshots, exports, and demo files can blur source-of-truth boundaries if the project does not decide their lifecycle before implementation.

## Follow-On Stack Slice

Planning templates should ask which future stack element should come next and what user or operator problem it solves.

Suggested template:

```md
## Follow-On Stack Slice

- Recommended next stack element:
- Trigger for starting:
- Useful scope:
- Explicit non-goals:
```

Rationale: stack evidence is strongest when each language, framework, service, or infrastructure piece owns real behavior instead of acting as decorative scaffolding.
