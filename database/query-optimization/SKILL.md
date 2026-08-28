---
name: query-optimization
description: Diagnose and improve PostgreSQL query performance using measurements and execution plans. Use when latency, database load, slow queries, or N+1 behavior is reported.
---

# Query Optimization

## Never Optimize Blindly
A slow query is an observation, not a diagnosis.

## Diagnostic Workflow
1. Capture representative SQL and parameters.
2. Measure baseline latency/resource use.
3. Run EXPLAIN.
4. Use EXPLAIN ANALYZE when safe.
5. Compare estimated vs actual rows.
6. Inspect scan type, join strategy, sort/aggregate cost, loops, buffers where available.
7. Identify the bottleneck.
8. Change one major factor.
9. Re-measure.
10. Verify result correctness.

## Interpretation Heuristics

### Sequential Scan
Not automatically bad. It can be optimal for small tables or queries returning a large fraction of rows.
Suspicious when a huge table is scanned for a highly selective predicate.

### Nested Loop
Can be excellent when the outer side is small and the inner side is efficiently indexed.
Suspicious when loops are enormous or cardinality estimates are badly wrong.

### Hash/Merge Join
Evaluate whether the join cardinality, memory, ordering, and input sizes justify the chosen strategy.

### Estimated vs Actual Rows
Large divergence can indicate stale statistics, skew, correlated predicates, or an inaccurate planner model. Investigate before forcing a plan.

## Common Root Causes
- missing/unsuitable index
- wrong index column order
- stale statistics
- N+1
- over-fetching
- huge sort
- bad join cardinality
- functions/casts blocking useful indexes
- unbounded pagination

## Optimization Priority
Prefer:
1. remove unnecessary work
2. fix query shape
3. fix data access pattern
4. add/revise index if justified
5. consider caching only after consistency/freshness are defined

## Verification
Keep before/after evidence and test representative parameters, not only a favorable case.
