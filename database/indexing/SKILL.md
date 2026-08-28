---
name: indexing
description: Design, review, troubleshoot, and retire PostgreSQL indexes based on actual workload, query plans, data distribution, and operational cost. Use when adding, changing, validating, or removing indexes.
---

# Indexing — Production Playbook

## 1. Mission

An index is a workload-specific access path, not a decoration on a schema.

Choose an index only when:
- it solves a real access problem
- the workload justifies it
- the planner can benefit from it
- write/storage/maintenance costs are acceptable

Do not add an index merely because a column appears in `WHERE`, `JOIN`, or `ORDER BY`.

PostgreSQL documents that indexes can improve lookup performance but also add overhead to writes and maintenance. [PostgreSQL Indexes]

---

## 2. Activation

Use when:
- EXPLAIN shows a query would benefit from indexed access
- a hot query needs faster lookup/order
- a new high-volume table/query pattern is introduced
- a query's filtering/sorting pattern changes
- write performance/storage is being affected by excessive indexes
- duplicate/redundant indexes are suspected

---

## 3. Index Decision Sequence

```text
What query/workload needs improvement?
        ↓
Measure it
        ↓
Inspect EXPLAIN
        ↓
Can query shape/data access be simplified first?
        ↓ no
Is an existing index usable?
        ↓ no
Is the predicate/selectivity suitable?
        ↓
Choose access method
        ↓
Design column/order/predicate
        ↓
Estimate read benefit vs write/storage cost
        ↓
Build safely
        ↓
Measure again
        ↓
Monitor usage and impact
```

Use `database/query-optimization` for the diagnosis stage.

---

## 4. Start With the Query

Collect:
- exact query shape
- representative parameter values
- WHERE predicates
- JOIN predicates
- ORDER BY
- grouping
- expected rows returned
- table cardinality
- query frequency
- write/update frequency
- existing indexes

Do not design an index from the schema alone.

The same column may need different indexing depending on workload.

---

## 5. Selectivity

A selective predicate returns a relatively small fraction of a table.

Indexing tends to be more attractive when:
- the table is large
- the predicate narrows results substantially
- the query is frequent
- indexed access meaningfully reduces work

A low-selectivity predicate such as a boolean with 95% of rows matching may not benefit from an ordinary index.

But selectivity is not a universal rule:
- composite indexes can make combined predicates selective
- partial indexes can isolate a valuable subset
- ordering requirements can justify an index
- covering behavior can reduce heap access

Always verify with plans/workload.

---

## 6. B-tree

B-tree is the normal default for:
- equality
- ranges
- ordering
- many ordinary lookup patterns

Examples:
- `tenant_id = ?`
- `created_at >= ?`
- `price BETWEEN ? AND ?`
- `ORDER BY created_at DESC`

Do not choose B-tree solely because it is the default. The operator/workload still has to fit.

---

## 7. Composite Indexes

Column order matters.

For:

```sql
WHERE tenant_id = ?
  AND status = ?
ORDER BY created_at DESC
```

a useful index might be conceptually:

```text
(tenant_id, status, created_at)
```

but the correct order depends on:
- equality predicates
- range predicates
- ordering
- selectivity
- common query variants

Do not mechanically sort index columns by:
- highest cardinality
- table declaration order
- order of appearance in the SQL

Use the actual workload.

---

## 8. Equality + Range

A common pattern is:

```text
tenant_id = ?
created_at > ?
```

When designing the index, equality/range/order interactions matter.

The index must match the dominant query shape, not every possible combination.

If multiple query patterns exist, compare whether:
- one composite index covers the important workloads
- multiple indexes are justified
- a query can be rewritten
- a dedicated read model is more appropriate

Avoid index explosion.

---

## 9. ORDER BY

Indexes can support ordering and avoid or reduce sort work when the index ordering matches the query.

Review:
- direction
- leading index columns
- filtering predicates
- deterministic secondary order

For paginated queries, an index matching the filter + ordering can be particularly valuable.

Do not add an ordering index just because the query contains ORDER BY. First inspect whether sorting is actually a bottleneck.

---

## 10. Partial Indexes

A partial index covers only rows matching a predicate.

Good candidates:
- active records
- unprocessed jobs
- non-deleted records
- a small high-value subset

Example concept:

```sql
CREATE INDEX ...
ON orders (tenant_id, created_at)
WHERE status = 'OPEN';
```

Benefits:
- smaller index
- less write/maintenance cost
- focused access path

Requirements:
- predicate must correspond to the workload
- query predicate must allow PostgreSQL to recognize that the index applies

Do not create a partial index whose predicate is unrelated to the real query.

---

## 11. Expression Indexes

Use when queries consistently filter/order by a deterministic expression.

Example concept:

```sql
CREATE INDEX ...
ON users (lower(email));
```

Only do this when:
- the application consistently uses the same expression
- the expression index actually addresses the workload

Prefer canonicalizing data at write time when that better matches the domain and simplifies queries.

Do not create expression indexes to compensate for poorly designed data semantics without evaluating alternatives.

---

## 12. INCLUDE / Covering

PostgreSQL can include non-key columns in an index so certain queries can obtain needed data from the index without using them as ordering/search keys.

Use when:
- a hot read query benefits materially
- heap access is a significant cost
- added index size/write overhead is acceptable

Do not include every selected column.

Large included values can make indexes expensive and reduce their practical benefit.

---

## 13. Specialized Index Types

### GIN
Consider for workloads using operators over:
- arrays
- `jsonb`
- full-text/search-like structures

### GiST
Consider for:
- geometric/spatial
- ranges
- specialized operator classes

### BRIN
Consider for very large tables where values correlate with physical row order, such as append-heavy time-series/event data.

BRIN is often much smaller than a B-tree but has different lookup characteristics.

### Hash
Consider only when the workload/operator specifically benefits and PostgreSQL's supported behavior makes it appropriate; B-tree is usually the ordinary starting point.

Do not choose an index type based only on column data type.

---

## 14. Unique Indexes / Constraints

If uniqueness is a business/data invariant, prefer a database UNIQUE constraint/index.

Example:

```text
UNIQUE(tenant_id, normalized_email)
```

This is stronger than an application existence check.

A uniqueness constraint also protects against concurrent requests.

When reviewing a uniqueness design, ask:
- is the key normalized correctly?
- is uniqueness tenant-scoped?
- should NULL be allowed?
- should deleted rows remain unique?
- would a partial unique index better model the rule?

---

## 15. Soft Deletes and Partial Unique Indexes

For soft-deleted resources, a unique constraint may need to apply only to active rows.

Concept:

```sql
UNIQUE INDEX ... WHERE deleted_at IS NULL
```

This allows historical deleted records while preserving uniqueness for active records.

Only do this when the domain semantics actually permit reusing the identifier after deletion.

---

## 16. Foreign Keys

Foreign-key columns are common join/filter targets.

Do not blindly create an index for every foreign key, but review:
- parent-delete/update behavior
- join frequency
- child lookup patterns
- cascading operations
- table size

Indexing the referencing side can be important for efficient parent modifications and child lookups.

---

## 17. JSONB and Search

Do not index an entire JSON/document field with a generic strategy without understanding the operators actually used.

Ask:
- which JSON paths are queried?
- containment or equality?
- existence?
- text search?
- cardinality?
- update frequency?

A targeted expression/GIN strategy may be preferable to an oversized generic index.

If search has become complex enough, consider whether a dedicated search system/read model is appropriate.

---

## 18. Redundant Indexes

Before adding a new index, inspect existing ones.

Potential problems:
- exact duplicates
- overlapping prefixes
- indexes created by old migrations
- indexes only useful to obsolete queries

Do not remove an index solely because it "looks redundant." Confirm actual usage and workload.

PostgreSQL's catalog and monitoring statistics can help identify index usage, but low usage during a short observation window does not prove an index is safe to remove.

---

## 19. Write Cost

Every additional index can increase:
- INSERT cost
- UPDATE cost when indexed columns change
- DELETE cost
- storage
- maintenance
- vacuum/index cleanup work

For high-write tables, require stronger evidence before adding indexes.

An index that makes one rare dashboard query 50 ms faster may be a bad trade if it materially slows millions of writes.

---

## 20. High-Cardinality Myth

"High cardinality = always index it" is too simplistic.

Cardinality interacts with:
- selectivity of the actual predicate
- table size
- workload
- correlation
- query frequency
- combined predicates

A high-cardinality column can still have an unhelpful index for a query, and a low-cardinality predicate can benefit through a partial/composite design.

---

## 21. Statistics and Planner Decisions

The planner relies on statistics to estimate row counts and costs.

If EXPLAIN shows large estimation errors, investigate statistics before redesigning indexes or forcing planner behavior.

Possible causes:
- stale statistics
- skew
- correlated columns
- insufficient statistics detail

Use the `query-optimization` skill for diagnosis.

Do not assume "index exists but planner doesn't use it" means PostgreSQL is wrong.

---

## 22. Parameter Distribution

A query can have different optimal plans for different parameters.

Example:
- tenant A owns 80% of rows
- tenant B owns 0.01%

A plan suitable for one may be poor for the other.

Test representative distributions.

Do not benchmark only:
- an empty tenant
- a tiny local dataset
- a highly selective "lucky" parameter

---

## 23. Pagination Indexes

For keyset pagination:

```text
WHERE tenant_id = ?
  AND (created_at, id) < (?, ?)
ORDER BY created_at DESC, id DESC
LIMIT 50
```

the index often needs to support:
- tenant filtering
- ordering
- cursor continuation

Design and verify the index together with the exact pagination query.

---

## 24. Concurrent Index Creation

For large production tables, understand the operational implications of index creation.

PostgreSQL supports `CREATE INDEX CONCURRENTLY`, which avoids blocking normal table writes in the same way as a standard index build, but it has additional operational requirements and cannot be run inside a transaction block.

Choose the build strategy deliberately based on:
- table size
- production traffic
- lock tolerance
- migration tooling constraints
- failure/retry plan

Do not automatically use concurrent creation everywhere.

---

## 25. Index Lifecycle

Treat indexes as production assets.

For important indexes:
- document why they exist
- monitor usage
- inspect size
- watch write impact
- revisit after workload changes

Queries disappear, product behavior changes, and migrations accumulate obsolete indexes.

Periodically review the index inventory on high-value tables.

---

## 26. Decision Tree

```text
Observed slow query
      ↓
Did query-optimization confirm index-related bottleneck?
 ├─ no → do not add index
 └─ yes
      ↓
Can query shape/data access be improved first?
 ├─ yes → fix query/access pattern
 └─ no
      ↓
Does existing index already cover the pattern?
 ├─ yes → investigate statistics/plan/data distribution
 └─ no
      ↓
What access path fits?
 ├─ ordinary equality/range/order → B-tree
 ├─ focused subset → partial
 ├─ deterministic expression → expression
 ├─ read-heavy projection → INCLUDE consideration
 ├─ JSON/array/search operators → GIN consideration
 ├─ range/spatial operators → GiST consideration
 └─ huge physically correlated table → BRIN consideration
      ↓
Estimate write/storage cost
      ↓
Build safely
      ↓
Measure plan + latency + write impact
```

---

## 27. Removal Decision

An index candidate for removal should be evaluated against:
- actual usage
- query history
- deployment/release patterns
- constraints that depend on it
- uniqueness semantics
- uncommon but important jobs/admin workflows

Never drop a unique index/constraint casually; it may be enforcing a business invariant.

When removing:
1. document reason
2. confirm alternatives
3. measure workload
4. deploy safely
5. monitor for regressions

---

## 28. Verification

After creating/changing an index:
- [ ] target query is measured before/after
- [ ] EXPLAIN reviewed
- [ ] representative parameters tested
- [ ] result correctness unchanged
- [ ] write overhead considered
- [ ] storage size considered
- [ ] concurrency/locking impact understood
- [ ] migration/build method is appropriate
- [ ] existing index overlap reviewed
- [ ] why the index exists is documented

---

## 29. Anti-Patterns

### Index Every Filter
Creates unnecessary write/storage costs.

### One Index Per Query
Produces index explosion and maintenance burden.

### High Cardinality Means Automatic Index
Ignores actual selectivity and workload.

### Seq Scan Means Missing Index
A sequential scan can be optimal.

### Force Index Usage
Usually hides a deeper query/statistics problem.

### Giant Covering Index
Adds every selected column to one index.

### Partial Index With Weak Predicate
Creates complexity without meaningful selectivity.

### Duplicate Index
Adds another access path that provides little/no new capability.

### Drop by Inactivity Alone
Short monitoring windows miss rare but critical workloads.

---

## 30. References

- `references/composite-index-design.md`
- `references/partial-expression-covering.md`
- `references/specialized-indexes.md`
- `references/index-lifecycle.md`
- `references/production-index-builds.md`

## Review Procedure

1. Identify the measured query/workload.
2. Inspect current plan and existing indexes.
3. Determine whether query shape can be improved first.
4. Choose index type/columns/order/predicate from actual access patterns.
5. Evaluate write/storage/maintenance cost.
6. Plan safe production creation.
7. Measure the result and check regressions.

## Verification Checklist

- [ ] workload evidence exists
- [ ] existing indexes reviewed
- [ ] index shape matches query pattern
- [ ] selectivity/order considered
- [ ] write/storage cost considered
- [ ] build strategy is safe
- [ ] before/after measurement captured

## Cross-Skill Routing
- For `query-optimization` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
- For `migrations` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
