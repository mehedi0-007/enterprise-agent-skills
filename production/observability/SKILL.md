---
name: observability
description: Design actionable logs, metrics, traces, health checks, alerts, and service-level indicators. Use when instrumenting services, troubleshooting production behavior, or preparing systems for operation.
---

# Observability

## Mission
Make it possible to answer:
- Is the system healthy?
- What is failing?
- Who/what is affected?
- Why is it failing?
- How long has it been failing?
- Is recovery working?

OpenTelemetry defines traces, metrics, logs, and baggage as telemetry signals, and emphasizes instrumentation that lets operators investigate unknown problems. citeturn556704search1turn556704search2

## The Three Core Signals

### Logs
Use structured logs for discrete events and diagnostics.
Include safe context:
- timestamp
- severity
- operation
- request/trace correlation
- safe resource identifiers
- error code

Do not log secrets or unnecessary sensitive payloads.

OpenTelemetry supports correlation of logs with trace/span context. citeturn556704search6

### Metrics
Track user/system behavior, not vanity numbers.

Useful categories:
- request rate
- error rate
- latency distribution
- saturation/resource utilization
- queue depth
- dependency failures
- business-critical outcomes

A metric is a runtime measurement; good SLIs should represent behavior users care about. citeturn556704search9turn556704search1

### Traces
Use traces to follow a request across services/components.
Capture meaningful spans:
- inbound request
- DB query groups
- external calls
- queue operations
- important domain operations

Avoid high-cardinality uncontrolled attributes.

## Correlation
Propagate request/trace context across synchronous and asynchronous boundaries where supported.

## Health Endpoints
Separate:
- liveness: process can continue
- readiness: service is ready to receive traffic
- dependency health where useful

Do not make liveness fail merely because a noncritical dependency is temporarily unavailable.

## SLI/SLO
Define SLIs from user-visible behavior when the product warrants formal reliability targets. Use SLOs to express desired reliability and drive alerting/error budgets.

## Alerts
Alert on symptoms that require action, not every abnormal metric.
A useful alert should indicate:
- impact
- urgency
- likely scope
- diagnostic link/context

## Verification
Simulate failures and confirm logs, metrics, traces, health behavior, and alerts make the failure understandable without reproducing it locally.
