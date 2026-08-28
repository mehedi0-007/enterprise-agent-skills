---
name: production-readiness
description: Review software for operational, security, reliability, performance, testing, deployment, and rollback readiness. Use before declaring a substantial feature or release complete.
---

# Production Readiness

## Goal
Do not equate "code compiles" with "production ready".

## Review Categories

### Correctness
- requirements implemented
- acceptance criteria verified
- edge cases covered
- failure paths handled
- concurrency behavior understood

### Security
- authentication checked
- authorization checked
- input validated
- secrets protected
- sensitive data not leaked
- rate limits considered
- security-sensitive logging reviewed

### Data
- migrations safe
- constraints correct
- indexes appropriate
- transaction boundaries correct
- rollback/compatibility strategy considered

### Reliability
- dependency failures handled
- timeouts configured where appropriate
- retries bounded and safe
- idempotency considered
- partial failure behavior understood

### Performance
- no obvious N+1 queries
- expensive operations identified
- unbounded lists avoided
- database queries measured when performance is relevant
- caching used only when justified

### Observability
- useful structured logs
- actionable errors
- metrics for important operations
- tracing/correlation where the system supports it
- health/readiness behavior appropriate

### Testing
- unit tests for business rules
- integration tests for important boundaries
- end-to-end tests for critical flows
- failure cases tested
- tests are deterministic

### Deployment
- build succeeds
- configuration documented
- environment variables/secrets understood
- migration order safe
- rollback plan exists for risky changes
- health checks pass

## Evidence Rule
Every important "verified" claim should have evidence:
- test output
- build output
- query plan/benchmark
- static analysis
- manual reproduction
- deployment/health result

Never claim a check passed if it was not actually run.

## Final Gate
Before declaring complete:
1. Review requirements.
2. Review changed files.
3. Run appropriate tests.
4. Run build/typecheck/lint where applicable.
5. Review security and data changes.
6. Review operational impact.
7. Report remaining known limitations explicitly.
