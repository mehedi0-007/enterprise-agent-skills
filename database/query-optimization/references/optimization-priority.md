# Optimization Priority

Prefer, in order:

1. Remove unnecessary work.
2. Fix N+1/repeated queries.
3. Bound rows/payload.
4. Simplify query shape.
5. Fix statistics/estimation when proven.
6. Add/change an index when the plan/workload justifies it.
7. Add caching when repeated expensive work has safe freshness/invalidation.
8. Consider architectural/read-model changes for persistent high-volume workloads.

This is a heuristic, not a rigid law.
