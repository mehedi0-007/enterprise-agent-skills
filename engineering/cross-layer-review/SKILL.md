---
name: cross-layer-review
description: Review a feature across frontend, API, service, database, security, observability, testing, and deployment boundaries. Use before merging substantial cross-layer changes or declaring a feature production ready.
---

# Cross-Layer Review

## Mission
Catch defects created at the seams between layers. A feature is not complete when each layer works independently but their contracts disagree.

## Review Flow

### 1. User → UI
Check:
- discoverability
- affordance
- loading/error/empty states
- accessibility
- responsive behavior
- destructive-action handling

### 2. UI → API
Check:
- request schema
- response schema
- status codes
- field naming/types
- pagination/filter semantics
- validation errors
- authentication/authorization behavior
- retry/idempotency semantics

### 3. API → Application
Check:
- controller boundaries
- DTO validation
- authorization context
- use-case/service responsibility
- stable error translation

### 4. Application → Database
Check:
- transaction boundary
- constraints
- query count
- indexes
- concurrency
- migration compatibility
- data ownership

### 5. Application → External Systems
Check:
- timeout
- retry policy
- idempotency
- partial failure
- reconciliation/outbox where appropriate
- secret handling

### 6. Runtime → Operations
Check:
- structured logs
- metrics
- tracing/correlation
- health/readiness
- alerts
- deployment compatibility
- rollback/forward-fix plan

### 7. Tests
Check that tests cover the contract between layers, not only individual functions.

## Contract Mismatch Examples
Look for:
- frontend expects field X but API returns Y
- frontend treats 404 as empty but API uses 404 for authorization hiding
- API accepts a retry but service produces duplicate side effects
- service assumes uniqueness but database has no constraint
- migration removes a field before old code stops reading it
- backend logs an identifier that frontend displays as a sensitive value
- UI shows optimistic success while backend operation is not safely reversible

## Evidence
Inspect actual schemas, tests, SQL/migrations, UI states, and runtime configuration. Do not infer that layers agree merely because types compile.

## Verification
For substantial features, document the cross-layer contracts and test the critical path end to end.
