---
name: indexing
description: Choose, review, and troubleshoot PostgreSQL indexes based on workload evidence. Use when queries need faster lookup/order/join behavior, when adding or removing indexes, or when index bloat/write overhead is a concern.
---

# Indexing

## Principle
Indexes are workload-specific structures with storage and write/update costs. Do not index every filtered column.

## Before Adding an Index
Inspect:
- actual query shape
- frequency and latency
- table size and growth
- selectivity/cardinality
- existing indexes
- WHERE predicates
- JOIN conditions
- ORDER BY/GROUP BY
- write/update rate

Use EXPLAIN/EXPLAIN ANALYZE to determine whether the planner can benefit from the index.

## B-tree
Use B-tree for the common equality/range/order cases:
- `=`
- `<`, `<=`, `>`, `>=`
- ordered retrieval
- many ordinary lookup patterns

## Composite Indexes
Column order matters.
Design the index around actual predicates and ordering, not the order columns happen to appear in a table.

Consider which predicates are equality conditions, which are ranges, and whether the same index can support required ordering.

## Partial Indexes
Use when only a subset of rows is queried frequently and the predicate is stable and meaningful.

Example concept:
an index only for active records rather than every historical record.

## Expression Indexes
Useful when queries consistently filter on a deterministic expression and the expression index matches the query.

## Covering / Included Columns
Consider included columns when avoiding heap access is valuable and the workload justifies the additional index size.

## Specialized Types
Evaluate GIN, GiST, BRIN, and other index types for workloads where their operator classes and access patterns fit. Do not choose an index type from the column data type alone.

## Write Cost
Every additional index can add:
- disk usage
- write/update work
- maintenance overhead

For high-write tables, require stronger evidence before adding indexes.

## Redundant Indexes
Before adding an index, inspect existing indexes for overlap. Remove/rework redundant indexes only after measuring workload impact.

## Verification
After index creation:
- confirm the intended query can use it
- compare execution plan and latency
- test representative parameters
- consider write overhead
- document why the index exists
