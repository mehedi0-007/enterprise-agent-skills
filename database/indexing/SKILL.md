---
name: indexing
description: Choose and review PostgreSQL indexes based on actual workload and query plans. Use when adding, changing, removing, or troubleshooting indexes.
---

# Indexing

## Before Adding
Inspect:
- real query
- frequency
- table size/growth
- selectivity
- existing indexes
- WHERE/JOIN predicates
- ORDER BY
- write/update frequency

## B-tree
Default choice for common equality, range, and ordering patterns.

## Composite Index
Design column order from actual predicate/order patterns. Equality predicates and range/order behavior matter; don't simply mirror table column order.

## Partial Index
Useful when a stable subset is queried frequently.

## Expression Index
Useful when the same deterministic expression is repeatedly used in predicates and an expression index matches the query.

## Included Columns
Consider covering behavior when avoiding heap access materially improves a hot query and index size/write cost is acceptable.

## Specialized Indexes
Evaluate GIN, GiST, BRIN, and other types from operator/workload requirements rather than data type alone.

## Costs
Indexes consume:
- disk
- cache
- write/update work
- maintenance

High-write tables require stronger evidence.

## Decision Tree

Need faster query?
→ inspect EXPLAIN
→ can query shape be simplified?
→ is existing index usable?
→ is predicate selective?
→ is a composite/partial/expression index appropriate?
→ measure after change
→ check write impact

## Verification
Confirm the target query uses or benefits from the index and compare representative performance before/after.
