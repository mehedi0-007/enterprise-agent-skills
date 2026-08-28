# Backend / Database Consistency Contract

This document is the canonical boundary map for the backend and database skills.

## Request Flow

```text
transport
  ↓
api-design
  ↓
validation
  ↓
authentication
  ↓
authorization
  ↓
service-layer
  ↓
transactions / concurrency
  ↓
repository-pattern
  ↓
postgresql
```

These are logical responsibilities, not mandatory class names.

## Ownership

### API Design
Owns:
- public endpoint/resource semantics
- HTTP methods/statuses
- request/response contracts
- pagination/filter/sort contract
- API error contract
- idempotency contract exposed to clients

Does not own:
- business transaction implementation
- raw database queries
- domain authorization policy
- UI behavior

### Validation
Owns:
- shape/type/format/range validation at boundaries
- mapping malformed input into validation errors

Does not own:
- authorization
- mutable domain-state rules that belong to the use case/domain

### Authentication
Owns:
- proving identity
- session/token lifecycle
- credential/recovery lifecycle

Does not own:
- resource permissions

### Authorization
Owns:
- principal/action/resource decision
- tenant/object/function/property boundaries

Does not own:
- HTTP response formatting
- database transaction mechanics

### Service Layer
Owns:
- use-case orchestration
- application-level transaction boundary
- coordination of repositories/domain/infrastructure
- application workflow semantics

Does not own:
- HTTP parsing/serialization
- SQL construction
- every business invariant by default

### Transactions
Owns:
- atomicity
- isolation choices
- transaction retry semantics
- coordination of DB changes that must commit together

Does not own:
- general business orchestration
- external side-effect exactly-once claims

### Concurrency
Owns:
- shared-state race analysis
- lost update prevention
- uniqueness/state-transition race prevention
- lock/version/atomic-operation choice

Does not own:
- authentication or transport semantics

### Repository / Data Access
Owns:
- persistence queries
- projections
- DB-specific access patterns
- persistence error translation

Does not own:
- HTTP semantics
- broad business workflows
- arbitrary authorization policy

### PostgreSQL
Owns:
- database-specific capabilities and semantics
- data types
- constraints
- transaction/database behavior
- SQL/database primitives

The application still chooses when and why to use those capabilities.

### Query Optimization
Owns:
- measured query diagnosis
- plan interpretation
- workload bottleneck identification

### Indexing
Owns:
- index access-path design
- index lifecycle and operational tradeoffs

### Migrations
Owns:
- schema/data evolution
- compatibility windows
- deployment-safe change sequencing

## Conflict Resolution

When skills overlap:
1. Project requirements override generic advice.
2. Security and data-integrity invariants override convenience.
3. The more specific skill owns the detailed decision.
4. Cross-layer semantics must remain compatible.
5. Avoid duplicate policy.

## Canonical Examples

### Unique registration
- API → request contract
- validation → email format
- authorization → any privileged operation
- service → signup use case
- repository → INSERT
- PostgreSQL → UNIQUE constraint
- concurrency → race analysis
- transaction → atomic related DB work

### Order creation with payment
- API → create-order contract + idempotency
- authorization → customer/tenant permission
- service → orchestrates order workflow
- transaction → local DB atomicity
- concurrency → duplicate/race prevention
- repository → order persistence
- external provider → separate side-effect semantics
- outbox/reconciliation → reliable post-commit integration

### Slow list endpoint
- API → page/filter/sort contract
- service → use-case orchestration
- repository → query/projection
- query optimization → diagnose bottleneck
- indexing → change access path when justified
- performance → end-to-end effect
