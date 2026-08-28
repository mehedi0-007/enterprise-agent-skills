---
name: postgresql
description: Design and review PostgreSQL schemas, SQL, constraints, transactions, indexes, and operational database behavior. Use for PostgreSQL-specific decisions and when database correctness or performance matters.
---

# PostgreSQL

## Core Rules
- Use explicit constraints for database-enforceable invariants.
- Choose data types deliberately.
- Parameterize values.
- Avoid unbounded reads.
- Understand NULL semantics.
- Design transactions around business invariants.
- Measure before optimizing.

## Schema
Prefer:
- primary keys
- foreign keys
- NOT NULL when absence is invalid
- UNIQUE for uniqueness
- CHECK for local invariants

Do not rely exclusively on application checks for invariants that must never be violated.

## Query Review
Check:
- N+1
- unnecessary columns
- duplicate rows from joins
- unstable pagination
- implicit casts
- expensive sorts/aggregations
- unbounded results

## Performance
Use EXPLAIN to inspect planner decisions. Use EXPLAIN ANALYZE carefully because it executes the statement.

## Indexes
Indexes have read benefits and write/storage costs. Evaluate workload, selectivity, query predicates, ordering, and existing indexes before adding one.

## Concurrency
Understand transaction isolation, locks, constraints, and atomic updates before changing concurrency behavior.

## References
See sibling skills:
- `query-optimization`
- `indexing`
- `migrations`
