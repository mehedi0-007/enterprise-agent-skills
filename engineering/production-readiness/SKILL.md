---
name: production-readiness
description: Assess whether a feature or release is safe to operate in production. Use before declaring substantial work complete, before deployment, or when reviewing operational risk.
---

# Production Readiness

## Gate
"Builds successfully" is not equivalent to "production ready."

## Review Matrix

### Correctness
- requirements and acceptance criteria
- edge cases
- failure paths
- concurrency
- idempotency

### Security
- authentication
- authorization
- input/output handling
- secrets
- sensitive logging
- abuse/rate limits

### Data
- schema constraints
- migrations
- indexes
- transaction boundaries
- compatibility with old/new application versions

### Reliability
- timeouts
- bounded retries
- dependency failures
- graceful degradation
- recovery

### Performance
- query count
- unbounded work
- hot paths
- large payloads
- measured bottlenecks

### Observability
- structured logs
- metrics
- tracing/correlation
- actionable errors
- health/readiness

### Testing
- unit
- integration
- critical end-to-end
- negative cases
- deterministic behavior

### Deployment
- configuration
- migration ordering
- health checks
- rollback/forward-fix plan

## Evidence Rule
Do not claim a check passed unless it was actually run or inspected. Report known limitations.

## Release Decision
Classify findings:
- Blocker: unsafe to deploy.
- High: significant correctness/security/reliability risk.
- Medium: should be fixed or explicitly accepted.
- Low: improvement without material current risk.

## Verification
Run the appropriate build/typecheck/lint/tests and inspect the actual diff. Review security and operational implications before finalizing.
