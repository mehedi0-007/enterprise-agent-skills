---
name: performance
description: Diagnose, plan, implement, and verify application performance improvements across frontend, API, database, network, caching, concurrency, and infrastructure. Use when latency, throughput, resource usage, rendering, payload size, query cost, or scalability is a concern.
---

# Performance — Production Playbook

## 1. Mission

Performance work should improve a measured user/system outcome without reducing correctness, reliability, security, or maintainability unnecessarily.

Do not optimize because code "looks slow."

Start with:
- user-visible latency
- throughput
- resource utilization
- error rate
- workload shape
- explicit performance target

---

## 2. Activation

Use when:
- endpoint latency regresses
- p95/p99 exceeds target
- frontend interaction/rendering is slow
- database load is high
- throughput is insufficient
- memory/CPU is saturated
- payloads are large
- concurrency is increasing
- preparing for scale/load testing
- evaluating cache/queue/read-model changes

---

## 3. Define the Performance Target

A useful target includes:
- operation/user journey
- workload
- concurrency
- percentile or throughput
- data volume
- environment
- acceptable error rate

Example:
```text
GET /orders
p95 < 300 ms
500 concurrent users
10M orders
error rate < 0.1%
```

Do not use averages as the only target when tail latency matters.

---

## 4. Measure Before Changing

Record a baseline:
- p50/p95/p99 latency where useful
- throughput
- error rate
- CPU
- memory
- DB execution time
- query count
- connection wait
- payload size
- browser loading/render metrics where relevant

Use representative data and traffic.

A local benchmark with a tiny dataset is not evidence of production-scale behavior.

---

## 5. Find the Dominant Bottleneck

Trace the actual path:

```text
User
 ↓
Browser/rendering
 ↓
Network
 ↓
API gateway
 ↓
Application
 ↓
Database/cache
 ↓
External services
```

Classify the dominant problem:

```text
DB execution high
    → query/index/data problem

DB fast, API slow
    → application/serialization/network/dependency

Many queries/request
    → data-access/N+1

High connection wait
    → pool/concurrency

Large payload
    → data transfer/serialization

Browser render high
    → DOM/client JS/layout

External dependency high
    → timeout/retry/provider bottleneck
```

Do not optimize a non-dominant component.

---

## 6. Latency Budgets

For important user journeys, break total latency into budgets.

Example:

```text
300 ms total
├── network 50 ms
├── API 80 ms
├── DB 100 ms
├── external dependency 50 ms
└── margin 20 ms
```

Budgets help teams avoid optimizing one layer while another consumes the entire target.

---

## 7. Tail Latency

p95/p99 often reveal:
- lock contention
- cache misses
- GC pauses
- slow dependencies
- cold starts
- large queries
- queue delays

Do not declare success because average latency improved while p99 regressed substantially.

---

## 8. Frontend Performance

Review:
- JavaScript bundle size
- network waterfalls
- rendering cost
- layout shifts
- image/font loading
- unnecessary client-side work
- repeated requests
- expensive lists/tables

Prefer:
- server rendering when appropriate
- code splitting
- lazy loading for noncritical features
- responsive images
- stable layout dimensions
- selective hydration/client execution where architecture supports it

Do not move everything to the server or client blindly; measure the actual user journey.

---

## 9. Core Web Vitals / User Experience

For web applications, use user-centric performance signals where relevant, such as:
- LCP
- INP
- CLS

These are useful because a fast backend does not guarantee a responsive page.

Do not optimize synthetic scores while real users remain slow.

---

## 10. API Performance

Review:
- request count
- payload size
- serialization
- pagination
- query count
- dependency fan-out
- caching
- compression
- timeout behavior

A single slow endpoint is not always a SQL problem.

For APIs with multiple dependencies, consider:
- parallelization
- batching
- partial responses
- async processing
only when correctness semantics permit.

---

## 11. Database Performance

Use `database/query-optimization` and `database/indexing`.

Review:
- execution plan
- cardinality
- N+1
- scans
- joins
- sorts
- aggregation
- indexes
- locks
- connection waits
- result size

Do not add indexes before proving the database access path is the bottleneck.

---

## 12. Connection Pools

A service can be slow while SQL execution is fast because requests wait for connections.

Measure:
- active connections
- idle connections
- pool wait time
- transaction duration
- query duration
- number of application replicas

Do not simply increase pool size.

Too many concurrent DB connections can cause:
- memory pressure
- contention
- degraded DB throughput

Tune from observed limits.

---

## 13. Caching

Caching is useful when:
- reads repeat
- computation/read is expensive
- freshness requirements are known
- invalidation is manageable
- cache misses are safe

Define:
- key
- scope/tenant
- TTL
- invalidation
- stampede behavior
- stale policy
- failure fallback

Do not cache as a substitute for fixing an obvious inefficient query/access pattern.

---

## 14. Cache Stampede

If an expensive item expires and thousands of requests recompute it simultaneously, caching can create an outage.

Consider:
- request coalescing
- lock/single-flight
- jittered TTL
- stale-while-revalidate
- precomputation

Use the simplest mechanism that satisfies the workload.

---

## 15. Cache Invalidation

For every cache, identify:
- source of truth
- what event invalidates
- whether stale data is acceptable
- what happens if invalidation fails

Never claim strong freshness when invalidation is best-effort.

For authorization-sensitive data, include tenant/principal scope in the cache model.

---

## 16. Batching

Batching can reduce:
- network round trips
- DB queries
- API calls

Examples:
- N+1 query batching
- external API bulk endpoints
- GraphQL/data-loader style batching

But batching may increase:
- payload size
- tail latency
- memory
- failure scope

Measure the tradeoff.

---

## 17. Parallelism

Independent work may be executed concurrently.

Example:
```text
fetch customer
fetch feature flags
fetch preferences
```

can sometimes run in parallel.

Do not parallelize operations that:
- share mutable state unsafely
- compete for a constrained dependency
- must happen sequentially
- cause request amplification

Concurrency can turn a small latency gain into a resource-exhaustion problem.

---

## 18. Fan-Out

One request that triggers many downstream calls can create multiplicative load.

Example:
```text
1 API request
 → 20 service calls
 → each calls 5 others
```

Review:
- total calls
- dependency limits
- timeouts
- retries
- batching
- caching
- partial failure

Do not add retries to every layer of a fan-out tree.

---

## 19. Async Work

Move work off the synchronous request path when:
- it is long-running
- immediate result is not required
- workload can be queued
- retries are needed

But define:
- job state
- idempotency
- retry
- observability
- user notification
- eventual consistency

Use `frontend/async-ui-states` and backend queue/concurrency skills.

---

## 20. Backpressure

When producers can create work faster than consumers can process it, queues grow.

Monitor:
- queue depth
- oldest item age
- processing rate
- failure/retry rate
- worker concurrency

Controls can include:
- admission limits
- rate limits
- bounded queues
- worker scaling
- load shedding

Do not solve every queue problem by adding more workers; the dependency may be the actual bottleneck.

---

## 21. Concurrency Limits

Limit concurrency where a dependency or resource has finite capacity.

Examples:
- outbound API calls
- image processing
- PDF generation
- DB-intensive jobs
- browser rendering

Unbounded concurrency often converts latency into failure.

---

## 22. Load Testing

Load tests should represent realistic:
- traffic mix
- concurrency
- request sizes
- data sizes
- cache state
- dependency behavior

Test:
- normal expected load
- peak load
- sustained load
- burst/spike where relevant

Measure:
- latency percentiles
- throughput
- errors
- CPU/memory
- DB behavior
- queue behavior

Do not call a 2-minute benchmark "capacity planning."

---

## 23. Capacity Planning

For capacity decisions estimate:
- expected growth
- peak traffic
- concurrency
- data growth
- dependency limits
- headroom

A service is not at safe capacity merely because average CPU is below 50%.

Identify the limiting resource:
- CPU
- memory
- DB connections
- DB I/O
- network
- queue throughput
- external provider quota

---

## 24. Performance vs Cost

Optimizing infrastructure can increase cost.

Evaluate:
- extra replicas
- larger DB
- cache layer
- CDN
- precomputation
- denormalization
- dedicated read model

Prefer the cheapest change that meets the target without unacceptable complexity/risk.

---

## 25. Correctness Before Speed

Do not optimize by:
- removing validation
- weakening authorization
- skipping transactions
- reducing durability
- returning stale sensitive data
- dropping important audit/telemetry

A faster incorrect system is not a performance win.

---

## 26. Warm vs Cold Performance

Measure whether the problem occurs:
- after startup/cold cache
- under warm steady state
- after deployment
- during cache expiration
- under connection churn

Do not optimize only the warm-cache case if real users experience cold behavior.

---

## 27. Regression Prevention

For recurring performance-sensitive paths:
- establish benchmark/load test
- track latency/resource metrics
- run performance tests for meaningful changes
- monitor production after deploy

Do not rely solely on developer intuition.

---

## 28. Performance Changes

For each optimization record:

```text
Problem
Baseline
Hypothesis
Change
Result
Tradeoffs
```

Example:

```text
Problem: orders endpoint p95 = 900ms
Hypothesis: N+1 relationship loading
Change: batch order lookup
Result: p95 = 240ms
Tradeoff: extra query memory
```

This prevents "performance folklore."

---

## 29. Review Procedure

When performance is reported:

1. Define target.
2. Capture baseline.
3. Identify workload.
4. Trace end-to-end.
5. Find dominant bottleneck.
6. Form hypothesis.
7. Change the smallest relevant thing.
8. Benchmark again.
9. Check correctness.
10. Check resource/cost side effects.
11. Deploy safely.
12. Verify in production.

---

## 30. Anti-Patterns

### Optimize by Intuition
No baseline.

### Average-Only
Tail latency hidden.

### Cache Everything
Stale data/invalidations become the real problem.

### Scale Everything
More replicas hide a downstream bottleneck.

### Unlimited Parallelism
Resource exhaustion.

### Retry Storm
Multiple layers retry the same dependency failure.

### Benchmark Toy Data
Performance claims from unrealistically small data.

### Browser Score Theater
Synthetic frontend metric improved while real UX did not.

### Faster by Removing Safety
Validation/auth/durability weakened.

### One Metric
CPU alone used to diagnose all performance issues.

### No Post-Deploy Measurement
Optimization assumed successful without production evidence.

---

## 31. Verification Checklist

- [ ] performance target defined
- [ ] representative workload used
- [ ] baseline recorded
- [ ] end-to-end bottleneck identified
- [ ] tail latency considered
- [ ] frontend cost reviewed where relevant
- [ ] API/query count/payload reviewed
- [ ] DB plan reviewed
- [ ] connection pool wait considered
- [ ] cache justification/invalidation defined
- [ ] concurrency/fan-out reviewed
- [ ] async/backpressure considered
- [ ] load/capacity tested where needed
- [ ] correctness/security preserved
- [ ] cost/tradeoffs reviewed
- [ ] before/after measured
- [ ] production regression monitored

## References
- `references/performance-investigation.md`
- `references/caching.md`
- `references/load-testing.md`
- `references/frontend-performance.md`
- `references/capacity.md`
