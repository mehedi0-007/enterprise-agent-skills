---
name: performance
description: Diagnose and improve application performance using evidence across frontend, backend, database, and infrastructure. Use when latency, throughput, resource utilization, or user-perceived performance is a concern.
---

# Performance

## Mission
Optimize user/system outcomes, not arbitrary benchmark numbers.

## Start With a Target
Define:
- latency target
- throughput target
- concurrency
- payload size
- resource constraints
- affected user journey

## Measure Before Changing
Establish baseline:
- p50/p95/p99 latency when relevant
- request rate
- error rate
- CPU/memory
- database latency
- query count
- frontend loading metrics where relevant

Do not optimize based on code appearance.

## Find the Dominant Cost
Trace the request:
client
→ network
→ application
→ database/cache
→ external dependencies
→ response

Identify which component contributes most to latency/resource use.

## Common Problems
Investigate:
- N+1 queries
- unbounded data
- excessive serialization
- large payloads
- repeated external calls
- blocking work in request path
- missing pagination
- inefficient indexes/query plans
- cache misses/thrashing
- unnecessary frontend work
- connection pool exhaustion

## Caching
Cache only when:
- expensive computation/read is repeated
- freshness is defined
- invalidation is understood
- cache failure is safe
- key cardinality is controlled

## Async Work
Move genuinely long-running/non-interactive work off the synchronous request path when product semantics permit.
Define queue/backpressure/retry/idempotency behavior.

## Frontend Performance
For web apps consider:
- critical rendering path
- bundle size
- image/font costs
- layout shifts
- unnecessary client-side JavaScript
- request waterfalls

Use real measurements, such as field/user telemetry, when available.

## Verification
Measure after each significant optimization, test under representative load/data, and ensure correctness/regression safety.
