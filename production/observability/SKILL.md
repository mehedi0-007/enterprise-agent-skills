---
name: observability
description: Design and review production logs, metrics, traces, health signals, alerts, SLIs/SLOs, correlation, telemetry cost, and incident diagnostics. Use when instrumenting services, defining operational dashboards/alerts, preparing releases, troubleshooting incidents, or reviewing whether a system is operable.
---

# Observability — Production Playbook

## 1. Mission

Observability is about being able to infer what is happening inside a system from its externally available telemetry.

A production service should help operators answer:
- Is the system working?
- Who is affected?
- What changed?
- Where is the failure?
- Why is it failing?
- How long has it been happening?
- Is the system recovering?

OpenTelemetry defines common semantic conventions across logs, metrics, traces, resources, and profiles so telemetry can be consistently named and correlated across technologies. citeturn382653search1turn382653search4

---

## 2. Activation

Use when:
- adding instrumentation
- creating dashboards/alerts
- debugging production failures
- adding a new service
- defining health/readiness endpoints
- reviewing incident readiness
- investigating latency/error regressions
- adding async workers
- changing important business workflows

---

## 3. Start With Operational Questions

Do not begin by adding every available metric.

Start with questions:

### Availability
Can users complete the intended operation?

### Performance
How long does it take?

### Correctness
Are important operations succeeding correctly?

### Capacity
How close are dependencies/resources to their limits?

### Diagnosis
Can an operator identify the failing component and affected request?

Each telemetry signal should help answer at least one useful operational question.

---

## 4. The Core Signals

### Logs
Best for discrete events and detailed diagnostic context.

Examples:
- authorization failure
- deployment event
- payment-provider error
- worker retry
- state transition

### Metrics
Best for aggregated trends and alerting.

Examples:
- request rate
- error rate
- latency
- queue depth
- resource utilization

### Traces
Best for following one request/work item across boundaries.

Examples:
```text
HTTP request
 → service
 → database
 → payment API
 → queue
```

OpenTelemetry standardizes common HTTP, database, messaging, and other trace semantic conventions to improve cross-system analysis. citeturn382653search7

Do not force every fact into every signal.

---

## 5. Logs: Structured and Actionable

Prefer structured logs with fields such as:
- timestamp
- severity
- service
- environment
- operation
- request/trace ID
- resource ID where safe
- error code/category

OpenTelemetry provides semantic conventions for log records and correlation with other telemetry. citeturn382653search0turn382653search9

Avoid huge free-form log messages that cannot be searched/aggregated.

---

## 6. What Not to Log

Never log:
- passwords
- access/refresh tokens
- API keys
- OTPs
- private signing keys
- session credentials

Be cautious with:
- full request bodies
- PII
- payment information
- authorization headers
- file contents
- reset URLs

Redaction is useful, but prevention is better than logging sensitive values and hoping a filter catches them.

---

## 7. Log Levels

Use severity intentionally.

Example:
- DEBUG → detailed development/troubleshooting context
- INFO → important normal operations
- WARN → abnormal but handled condition
- ERROR → operation failed and requires attention
- FATAL/CRITICAL → service/process cannot safely continue

Do not log every expected 4xx as ERROR by default if the condition is normal client behavior.

Do not hide genuine system failures as INFO.

---

## 8. Metrics

Start with meaningful service indicators.

Common:
- request rate
- error rate
- latency distribution
- saturation
- queue depth
- dependency error rate
- retry count

Use histograms/distributions for latency rather than only averages when tail performance matters.

OpenTelemetry's metric semantic conventions provide common instruments/units and recommend consistent naming. citeturn382653search5

---

## 9. Cardinality

Metric labels/attributes can explode the number of time series.

Dangerous high-cardinality dimensions:
- user ID
- request ID
- arbitrary URL
- full error message
- raw query
- email
- UUID per request

Prefer bounded dimensions:
- endpoint/template route
- status class
- region
- service
- operation type

Trace/log context can carry identifiers that should not become metric labels.

---

## 10. Naming

Use consistent names and units.

Prefer:
```text
http.server.request.duration
```

over random per-service variants such as:
```text
apiTime
request_ms
latencyThing
```

OpenTelemetry semantic conventions exist specifically to standardize names and meaning across codebases and technologies. citeturn382653search4

---

## 11. Tracing

Use traces to follow important cross-boundary work.

At minimum consider spans for:
- inbound HTTP/RPC
- outbound HTTP/RPC
- database operations
- messaging
- object storage
- important domain operations where they materially improve diagnosis

Do not create thousands of tiny custom spans that add noise/cost without diagnostic value.

---

## 12. Trace Correlation

Propagate trace/request context through:
- service calls
- queues/messages
- background jobs

Where supported, correlate logs with trace/span identifiers.

The goal is:

```text
user request
   ↓
trace
   ├── API span
   ├── DB span
   ├── external API span
   └── worker span
```

An operator should be able to move from a failing log/error to the request trace when tooling supports it.

---

## 13. Sampling

For high-volume systems, not every trace must necessarily be retained.

Choose sampling from:
- traffic volume
- cost
- debugging needs
- compliance
- rare/high-value errors

Be careful not to drop the traces most useful for diagnosing failures.

Error/high-latency/important business traces often deserve stronger retention than routine healthy traffic.

---

## 14. Business Metrics

Infrastructure metrics alone cannot answer whether the product works.

Consider business signals for important systems:
- successful checkout rate
- invitation acceptance
- job completion
- export success
- payment success/failure
- message processing outcome

Do not expose personal identifiers as metric dimensions just to make dashboards convenient.

---

## 15. SLIs

An SLI is a measurable representation of service behavior.

Good candidates are tied to user experience:
- availability of successful requests
- latency within target
- successful job completion

Avoid creating an SLI only because the metric is easy to collect.

---

## 16. SLOs

An SLO defines a target level of reliability.

Example concept:
```text
99.9% of valid API requests complete successfully
within defined latency criteria over a measurement window.
```

The exact objective must match:
- user expectations
- business impact
- cost
- architecture capability

Do not choose 99.99% merely because "higher is better."

---

## 17. Error Budgets

When formal SLOs exist, the error budget can help balance:
- reliability work
- feature velocity
- release risk

Use it to inform engineering decisions rather than creating a dashboard nobody acts on.

---

## 18. Alerting

Alert on actionable symptoms.

Good:
```text
customer-visible error rate is above target
```

Less useful:
```text
CPU = 80%
```

CPU may be normal or may be the symptom of a deeper problem.

An alert should answer:
- what is wrong?
- impact?
- urgency?
- where?
- useful diagnostic link/context?

Do not alert on every anomaly.

---

## 19. Alert Severity

Map alerts to action.

Example:
- page/on-call → immediate customer or system impact
- ticket → requires investigation but not immediate response
- dashboard-only → useful context without paging

Do not page humans for conditions that routinely self-recover and have no user impact.

---

## 20. Alert Fatigue

Too many noisy alerts make real incidents harder to notice.

Review:
- frequency
- false positives
- duplicate alerts
- unclear ownership
- thresholds without action

Every paging alert should have:
- owner
- runbook/diagnostic path
- expected response
- reason it deserves waking someone up

---

## 21. Health Signals

Distinguish:

### Liveness
Should this process be restarted?

### Readiness
Should this instance receive traffic?

### Startup
Has initialization completed?

Kubernetes explicitly separates startup, liveness, and readiness probes. It warns that incorrect liveness checks can cause cascading failures, while readiness controls whether a Pod should receive traffic. citeturn382653search2turn382653search8

Do not make liveness fail merely because a recoverable dependency is temporarily unavailable unless restart is actually the desired recovery action.

---

## 22. Health Endpoint Design

A health endpoint should be:
- cheap
- deterministic
- appropriate to its purpose
- safe to expose

Avoid making liveness perform a full dependency graph check.

A deeper readiness/dependency check can be appropriate when the service should not receive traffic without that dependency.

Do not expose sensitive diagnostics publicly through health endpoints.

---

## 23. Dependency Health

For critical dependencies:
- database
- queue
- cache
- external provider

monitor:
- error rate
- latency
- connection failures
- timeouts
- saturation

Do not make every dependency failure restart every service.

A dependency outage should not become a restart storm.

---

## 24. Database Observability

Important signals include:
- query latency
- slow query frequency
- connection pool usage/wait
- transaction duration
- lock waits
- deadlocks
- replication lag where applicable
- cache/buffer behavior
- storage growth

Coordinate with:
- `database/query-optimization`
- `database/indexing`
- `backend/transactions`
- `backend/concurrency`

---

## 25. Queue / Worker Observability

For workers track:
- queue depth
- oldest message age
- processing latency
- success/failure
- retry count
- dead-letter count
- concurrency
- throughput

A worker can be "healthy" while the queue is growing without bound.

Queue age can be more actionable than worker process health alone.

---

## 26. Deployment Observability

For releases correlate:
- deployment version
- commit
- image/artifact identity
- migration version
- error/latency changes
- worker failures

A sudden regression after deployment should be attributable to a release.

Coordinate with `production/ci-cd` and `production/deployment`.

---

## 27. Incident Investigation Workflow

When an alert fires:

```text
Confirm impact
    ↓
Scope affected users/operations
    ↓
Check recent changes
    ↓
Check service symptoms
    ↓
Trace representative failures
    ↓
Inspect dependencies
    ↓
Check resource saturation
    ↓
Identify likely cause
    ↓
Mitigate
    ↓
Verify recovery
    ↓
Record timeline/root cause
```

Do not immediately restart everything.

First determine whether restart is:
- mitigation
- masking
- worsening

---

## 28. Debugging by Correlation

Use a common identifier across boundaries where appropriate:

```text
requestId / traceId
```

Example:
```text
HTTP 500
  ↓
trace
  ↓
DB timeout
  ↓
connection pool saturation
```

Without correlation, operators may see three unrelated symptoms.

---

## 29. Sampling and Rare Events

Do not let sampling hide:
- errors
- security events
- critical business failures
- unusual high-latency requests

Use adaptive or rule-based sampling where the telemetry system supports it.

---

## 30. Telemetry Cost

Telemetry is production data.

Review:
- log volume
- trace storage
- metric cardinality
- retention
- ingestion cost
- PII/compliance

More telemetry is not automatically better observability.

Keep high-value signals and remove low-value noise.

---

## 31. Privacy

Observability systems often become copies of application data.

Treat them with appropriate access controls.

Review:
- PII
- identifiers
- request bodies
- URLs
- headers
- uploaded content
- payment data

Prefer aggregated/safe metadata when detailed payloads are unnecessary.

---

## 32. Dashboards

A dashboard should support a decision.

Useful overview:
- request rate
- success/error
- latency
- saturation
- important business signal
- dependency health
- current deployment

Avoid dashboards containing hundreds of unrelated graphs.

---

## 33. Runbooks

Important alerts should link to actionable runbooks that explain:
- meaning
- likely causes
- immediate checks
- mitigation
- escalation
- rollback/forward-fix considerations

A metric without an action path has lower operational value.

---

## 34. Testing Observability

Do not assume instrumentation works.

Test:
- logs emitted on important failures
- correlation IDs propagate
- traces span important boundaries
- metrics update
- health checks change appropriately
- alerts fire under synthetic/test conditions
- sensitive fields are redacted
- telemetry remains usable under load

---

## 35. Review Procedure

For a production service ask:

1. What user-facing outcomes matter?
2. Which signals represent them?
3. Can a failure be traced across boundaries?
4. Are logs structured and safe?
5. Are metrics low-cardinality?
6. Are traces useful rather than noisy?
7. Are errors/high-latency cases retained?
8. Are health endpoints semantically correct?
9. Are dependencies observable?
10. Are queues observable?
11. Can deployments be correlated with regressions?
12. Are alerts actionable?
13. Are runbooks available?
14. Is telemetry privacy/cost controlled?
15. Can operators diagnose a realistic failure without reproducing it locally?

---

## 36. Anti-Patterns

### Log Everything
Huge volume, sensitive data, low signal.

### High-Cardinality Metrics
Per-user/request IDs become metric labels.

### Average Latency Only
Hides tail failures.

### Alert on CPU
Pages on infrastructure symptoms without user impact.

### Liveness = DB Health
Database hiccup triggers restart storm.

### Trace Every Tiny Function
Noise and cost obscure meaningful spans.

### No Correlation
Logs/traces/metrics cannot be connected.

### Health = 200
Endpoint always returns success regardless of readiness.

### Business Blindness
Infrastructure green while payments/orders/jobs are failing.

### Dashboard Dump
Hundreds of graphs with no decision context.

### No Runbook
Alert wakes humans who have no next action.

### No Telemetry Tests
Instrumentation breaks silently.

---

## 37. Verification Checklist

- [ ] operational questions defined
- [ ] logs structured/actionable
- [ ] secrets/PII protected
- [ ] metrics meaningful
- [ ] metric cardinality bounded
- [ ] traces cover important boundaries
- [ ] context correlation works
- [ ] business outcomes measured where important
- [ ] SLIs/SLOs defined where appropriate
- [ ] alerts actionable
- [ ] alert ownership/runbooks clear
- [ ] liveness/readiness/startup semantics correct
- [ ] dependency health observable
- [ ] DB/queue health observable
- [ ] deployment correlation available
- [ ] telemetry cost/retention reviewed
- [ ] observability tested under representative failures

## References
- `references/signals-and-correlation.md`
- `references/metrics-cardinality.md`
- `references/health-probes.md`
- `references/alerts-slos.md`
- `references/incident-diagnosis.md`

## Cross-Skill Routing
For release/rollout correlation and health gates, coordinate with `deployment`.
For performance diagnosis and optimization, coordinate with `performance`.
