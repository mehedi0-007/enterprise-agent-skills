# Reading PostgreSQL Query Plans

## Sequential Scan
A sequential scan is not inherently bad. It can be cheaper when a table is small or a large fraction of rows is needed. It becomes suspicious when a large table is scanned for a highly selective predicate.

## Index Scan
Inspect whether the index predicate matches the query and whether heap fetches/random I/O dominate.

## Bitmap Scan
Often useful when many rows match and PostgreSQL benefits from combining index filtering with heap access.

## Nested Loop
Usually attractive when the outer side is small and the inner lookup is cheap. Large loop counts combined with expensive inner work are a common red flag.

## Hash Join
Often effective for equality joins when building a hash table is affordable. Inspect memory pressure and spill behavior.

## Merge Join
Useful when sorted inputs make the merge efficient or ordering is already available.

## Estimated vs Actual Rows
Large estimation errors can produce poor join/scan choices. Investigate statistics, data skew, correlated predicates, and query shape before forcing planner behavior.

## Rule
Treat the plan as evidence about the workload, not as a checklist of "bad" node types.
