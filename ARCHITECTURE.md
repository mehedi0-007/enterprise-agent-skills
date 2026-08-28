# Enterprise Agent Skills — Architecture

## Purpose

This repository is a portable engineering judgment layer for AI coding agents.

It is intentionally framework-agnostic. Framework-specific syntax belongs in the project/codebase; these skills encode decisions, boundaries, failure modes, verification, and production tradeoffs.

## Skill Layers

```text
engineering
    ↓
requirements / architecture / planning / verification
    ↓
backend + database + security + frontend
    ↓
production
    ↓
cross-layer verification
```

## Canonical Responsibilities

| Area | Primary responsibility |
|---|---|
| requirements-analysis | understand intent, scope, acceptance criteria |
| architecture | choose boundaries and major design |
| testing-quality | verify behavior and risk |
| cross-layer-review | verify contracts between layers |
| api-design | public transport contract |
| validation | input shape/business validation boundary |
| service-layer | application/use-case orchestration |
| repository-pattern | persistence access |
| transactions | DB atomicity |
| concurrency | shared-state correctness |
| postgresql | DB capabilities/semantics |
| query-optimization | measured query diagnosis |
| indexing | index selection/lifecycle |
| migrations | schema/data evolution |
| authentication | identity/session/credential lifecycle |
| authorization | access decisions |
| api-security | API attack surface/abuse |
| owasp | security review orchestration |
| secrets-management | credential lifecycle |
| ui-design | visual hierarchy/control placement |
| ux-design | task flow/recovery |
| responsive-design | layout under changing constraints |
| accessibility | semantic/assistive interaction |
| forms | data-entry workflow |
| tables | structured data interaction |
| navigation | information architecture/routing |
| async-ui-states | client/server async lifecycle |
| docker | container artifact/runtime |
| ci-cd | delivery pipeline |
| observability | diagnosis/operability |
| performance | measured system optimization |
| deployment | live release/change control |

## Boundary Rules

### Request boundary
`api-design` defines what clients send/receive.
`validation` enforces input shape and constraints.
`authorization` decides access.
`service-layer` executes the use case.

### Persistence boundary
`repository-pattern` performs persistence operations.
`transactions` defines atomicity.
`concurrency` defines how shared-state races are prevented.
`query-optimization` diagnoses performance.
`indexing` changes access paths.
`migrations` changes durable schema/data.

### Frontend boundary
`ui-design` chooses interaction/control hierarchy.
`ux-design` defines user workflow behavior.
`forms` owns data-entry interaction.
`tables` owns collection interaction.
`navigation` owns information architecture.
`async-ui-states` represents network/server lifecycle.
`accessibility` applies across all interactive UI.
`responsive-design` applies across all layouts.

### Production boundary
`docker` produces/configures container runtime.
`ci-cd` builds/tests/promotes artifacts.
`deployment` changes live environments.
`observability` proves health/diagnoses failures.
`performance` measures and optimizes outcomes.

## Cross-Skill Principle

When two skills overlap, one is the primary owner and the other provides constraints.

Do not solve the same problem twice.

Example:
- A slow paginated table: `tables` defines UX; `query-optimization` diagnoses DB cost; `indexing` changes indexes.
- An export button: `ui-design` chooses placement; `ux-design` defines workflow; `api-design` defines endpoint semantics; `api-security` controls resource abuse; `async-ui-states` represents job state.
