# N+1 API Investigation

Observation:
API p95 = 800ms.

Trace:
- API work = 100ms
- database = 40ms/query
- 20 user records
- 20 additional queries

Hypothesis:
N+1 dominates.

Change:
batch related records.

Re-measure:
if p95 falls substantially while correctness remains intact, the query count—not an index on one small query—was the dominant issue.
