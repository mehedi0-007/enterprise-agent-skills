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

## Review Procedure

1. Verify functional correctness and tests.
2. Review security, failure, performance, and operability.
3. Verify configuration, secrets, migrations, and dependencies.
4. Verify health/observability/alerts.
5. Verify deployment/recovery strategy.
6. Identify residual risks and evidence.

## Verification Checklist

- [ ] tests appropriate to risk pass
- [ ] security reviewed
- [ ] failure/recovery reviewed
- [ ] migrations/config/secrets reviewed
- [ ] observability/alerts ready
- [ ] performance/capacity acceptable
- [ ] deployment/rollback or forward-fix defined
- [ ] residual risk documented

## Activation

Use when deciding whether a feature, service, or release is ready for production, especially when security, reliability, migrations, observability, or recovery risks are involved.
