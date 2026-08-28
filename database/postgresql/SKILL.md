---
name: postgresql
description: Design, query, review, and troubleshoot PostgreSQL-backed applications. Use for schema design, SQL, indexes, transactions, constraints, query plans, migrations, and database performance decisions.
---

# PostgreSQL

## Goal
Use PostgreSQL features deliberately, preserving correctness first and optimizing based on evidence.

## Schema Design
Prefer:
- explicit primary keys
- foreign keys for real relationships
- NOT NULL where absence is invalid
- UNIQUE constraints for invariants
- CHECK constraints for database-enforceable rules
- appropriate data types
- timestamps with a clearly defined timezone convention

Do not rely solely on application validation for invariants that must never be violated.

## Query Design
- Select only needed columns.
- Avoid accidental N+1 queries.
- Use joins deliberately.
- Avoid unbounded result sets.
- Prefer keyset pagination for large/high-churn datasets when appropriate.
- Parameterize values; never construct SQL by string concatenation.

## Transactions
Define the smallest atomic unit required by the business invariant.
Understand isolation level and locking before changing them.
Design explicitly for concurrent requests.

## Indexes
Indexes improve reads but add storage and write/update overhead.
Do not add an index solely because a column appears in a WHERE clause.

Before adding an index, inspect:
- actual query frequency
- table size
- selectivity/cardinality
- existing indexes
- ORDER BY/GROUP BY needs
- write cost
- query plan

For multicolumn B-tree indexes, column order matters; leading equality constraints and the first non-equality constraint are particularly important.

Consider:
- B-tree
- GIN
- GiST
- BRIN
- partial indexes
- expression indexes
- covering indexes

only when the workload justifies them.

## Query Performance
When a query is slow:
1. reproduce with representative data
2. run EXPLAIN
3. use EXPLAIN ANALYZE when safe and appropriate
4. inspect row estimates vs actual rows
5. inspect scan type, joins, sorting, buffers, and execution time
6. identify the bottleneck
7. change one important variable
8. measure again

Do not declare a query optimized without evidence.

## Correctness
Watch for:
- missing joins
- duplicate rows
- incorrect NULL semantics
- race conditions
- lost updates
- incorrect transaction boundaries
- timezone mistakes
- implicit casts
- pagination instability

## Verification
Database changes should include:
- migration
- rollback/forward compatibility consideration
- constraint review
- index review
- representative query testing
- concurrency considerations
- backup/recovery implications for risky changes
