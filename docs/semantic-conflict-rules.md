# V2 Semantic Conflict Rules

These are canonical decisions that skills must not contradict.

## Atomicity vs Concurrency

`transactions` answers:
> Which database operations must commit atomically, and what isolation semantics are required?

`concurrency` answers:
> How do multiple actors avoid violating shared-state invariants?

A transaction does not automatically eliminate races.

## Authorization vs Repository Scoping

`authorization` owns the policy decision.

`repository-pattern` may enforce trusted tenant/object scope at the persistence boundary as defense-in-depth.

Repository filtering does not replace authorization policy.

## Query Optimization vs Indexing

`query-optimization` diagnoses whether the query is slow and why.

`indexing` designs/changes the access path when an index is justified.

Do not add indexes solely because a predicate exists.

## UI vs API

`ui-design` / `ux-design` may decide how a feature is presented.

`api-design` owns the contract.

Frontend behavior must reflect actual server semantics.

## CI/CD vs Deployment

`ci-cd` builds, tests, secures, and promotes artifacts.

`deployment` changes live environments and verifies rollout/recovery.

A green pipeline does not imply a healthy production deployment.

## Observability vs Performance

`observability` makes behavior measurable and diagnosable.

`performance` uses measured evidence to improve latency/throughput/resource efficiency.

Do not create performance recommendations without evidence.

## OWASP vs Specialized Security

`owasp` routes and reviews.

Specialized security skills own implementation-level controls.

Do not copy whole checklists into every security skill.
