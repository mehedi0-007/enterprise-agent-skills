# Slow Query Investigation

Observation:
`GET /orders` p95 increased from 120 ms to 900 ms.

Do not immediately add an index.

Investigate:
1. current generated SQL
2. rows returned
3. query count
4. EXPLAIN/ANALYZE
5. recent data growth
6. estimate/actual row divergence
7. ordering/filtering
8. application serialization/network size

Possible finding:
Query executes in 40 ms, but endpoint makes 101 queries.

Correct fix:
address N+1 rather than indexing a query that isn't the dominant cost.
