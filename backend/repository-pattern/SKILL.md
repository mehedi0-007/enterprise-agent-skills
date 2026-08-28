---
name: repository-pattern
description: Design and review persistence boundaries and data-access abstractions in backend systems. Use when creating repositories, ORM query modules, SQL access, read models/projections, transactional persistence, or refactoring data access.
---

# Repository Pattern — Production Playbook

## 1. Mission

A repository/data-access boundary should make persistence behavior explicit, testable, and efficient without hiding important query semantics or introducing unnecessary abstraction.

The goal is not "every table gets a repository."

The goal is:
- clear persistence ownership
- correct data access
- deliberate query shape
- controlled coupling to the ORM/database
- visible transaction boundaries
- predictable performance

---

## 2. Activation

Use when:
- adding or changing database access
- deciding whether a repository abstraction is needed
- reviewing ORM-heavy services
- designing read/write persistence boundaries
- investigating N+1 or over-fetching
- introducing projections/read models
- coordinating persistence inside transactions
- changing ORM/database technology
- deciding where tenant/object scoping belongs

---

## 3. Start With the Use Case

Do not begin with "What methods should UserRepository have?"

First identify:
- use case
- data actually needed
- consistency requirement
- authorization/tenant scope
- read vs write
- transaction boundary
- expected cardinality
- performance characteristics

Then design the narrowest useful persistence operation.

---

## 4. Responsibility Boundary

### Repository/Data Access Owns

- SQL/ORM query construction
- persistence mapping
- projections/read models
- query-specific filtering/sorting
- pagination implementation
- persistence-level constraints/errors
- efficient data retrieval

### Application Service Owns

- use-case orchestration
- business decisions
- transaction boundary when multiple operations must be atomic
- coordination of repositories/infrastructure

### Domain Owns

- domain invariants
- state transitions
- business calculations/policies

### Repository Should NOT Own

- HTTP behavior
- UI concerns
- email/payment/queue workflows
- arbitrary authorization policy
- unrelated business orchestration

---

## 5. Repository Abstraction Decision

Before creating a repository, ask:

1. Is persistence behavior complex enough to deserve a boundary?
2. Is the abstraction already consistent with the project architecture?
3. Does it protect a meaningful dependency boundary?
4. Will tests benefit from the boundary?
5. Is the code likely to change independently of callers?
6. Would direct ORM/SQL access be clearer?

### When no repository may be better

For simple CRUD in a small module, direct ORM usage inside a well-defined application service may be simpler.

Do not create:
- `BaseRepository<T>`
- `GenericCrudRepository<T>`
- one-interface-per-table
just because they sound architecturally pure.

---

## 6. Intent-Revealing Interfaces

Prefer operations that describe data-access intent.

Good:
- `findActiveSubscriptionsForAccount(accountId)`
- `getOrderForUpdate(orderId)`
- `listInvoicesForOrganization(criteria)`
- `existsByNormalizedEmail(email)`

Suspicious:
- `find(options)`
- `query(rawSql)`
- `getMany(params)`
- a repository exposing every ORM feature to every caller

A generic query passthrough often turns the repository into a thin wrapper around the ORM and leaks persistence concerns upward.

---

## 7. Read vs Write

Do not assume reads and writes require the same abstraction.

### Reads
A read may require:
- projection
- aggregate query
- join
- reporting view
- cursor pagination
- optimized SQL

It may be inappropriate to load a full domain/ORM entity.

### Writes
A write may require:
- domain validation
- transaction
- constraints
- state transition
- concurrency control

Avoid forcing reporting queries through an entity repository just because the data "belongs to that entity."

---

## 8. Projections and Selectivity

Load only data the use case needs when practical.

Instead of:

```text
SELECT * FROM users
```

for a list that only needs:

```text
id, name, avatar
```

select the required fields.

Benefits:
- less I/O
- smaller memory footprint
- smaller network transfer
- less accidental sensitive data exposure
- better query predictability

Be careful with ORM defaults that eagerly load relationships or hidden fields.

---

## 9. N+1 Detection

Treat this pattern as a review trigger:

```text
1 query → N records
then
N queries → related data
```

Example:
```text
SELECT users
for each user:
    SELECT orders WHERE user_id = ?
```

Prefer:
- join where appropriate
- batched query
- explicit relation loading
- data loader/batching mechanism
- precomputed/read model

But do not automatically join every relationship. Large joins can:
- multiply rows
- increase memory
- over-fetch
- make pagination difficult

Choose based on actual data shape.

---

## 10. Authorization and Tenant Scope

A repository may enforce trusted scope at query level when that is part of the application's safety design.

For multi-tenant data, prefer:

```text
findInvoice(tenantId, invoiceId)
```

over:

```text
findInvoice(invoiceId)
```

when the tenant boundary is required for correctness.

However, repository scoping does not eliminate higher-level authorization policy.

The application must still determine whether the principal may perform the operation.

## Important
Never trust a client-provided `tenantId` simply because the repository receives one. Derive tenant context from authenticated server-side identity/context.

---

## 11. Transactions

Do not silently open a new transaction in every repository method.

Transaction ownership should normally be visible at the use-case boundary when several persistence operations must succeed/fail together.

Example:

```text
CreateOrder
  BEGIN
    repository.createOrder()
    repository.createItems()
    repository.reserveInventory()
  COMMIT
```

The repository methods participate in that transaction instead of independently committing.

### Transaction-specific methods

A method such as:

`getOrderForUpdate(...)`

can legitimately encode persistence semantics because the lock is part of the data-access requirement.

Keep transaction-related behavior explicit and documented.

---

## 12. Concurrency

Repositories are one of the final boundaries before database concurrency semantics.

Review for:
- check-then-insert
- read-modify-write
- stale update
- lost update
- duplicate processing
- lock ordering
- constraint races

Prefer the smallest database mechanism that protects the invariant:
1. constraint
2. atomic statement
3. optimistic locking
4. explicit row lock
5. stronger transaction isolation
6. distributed lock only when required

The repository should not hide important concurrency assumptions.

---

## 13. Pagination

Persistence code should support bounded collection access.

Review:
- max page size
- deterministic order
- stable tie-breaker
- offset vs keyset/cursor
- filter/index interaction

Do not expose a generic `findAll()` over an unbounded production dataset.

A repository API should make safe access patterns easy.

---

## 14. Sorting and Filtering

Prefer explicit allow-listed query criteria.

Avoid accepting arbitrary:
- column names
- SQL expressions
- ORM operators
- sort directives

A repository can map a safe application-level filter object to the actual query.

Example concept:

```text
ListOrdersCriteria
  status?: OrderStatus
  createdAfter?: Instant
  cursor?: Cursor
  limit: number
```

rather than exposing raw ORM options.

---

## 15. Persistence Errors

Repositories are a natural place to translate low-level persistence failures into stable persistence/application errors.

Example:

```text
PostgreSQL unique violation
      ↓
repository
DuplicateEmailPersistenceError
      ↓
application service
USER_ALREADY_EXISTS
      ↓
API
409 Conflict
```

Do not expose raw database error strings to callers.

Do not catch every DB error and pretend it means the same thing.

---

## 16. ORM Leakage

Ask whether callers can see:
- ORM entity classes
- lazy relation proxies
- ORM-specific query builders
- persistence decorators
- database-specific pagination objects
- ORM error types

Some leakage may be acceptable in small applications.

For larger systems, avoid allowing persistence implementation details to spread across the application because they make refactoring and testing harder.

Do not create abstractions merely to eliminate every ORM type from every layer.

---

## 17. Caching

Repository-level caching can be useful for stable/expensive reads, but it introduces consistency concerns.

Before adding cache define:
- key
- scope/tenant
- TTL/freshness
- invalidation
- stale behavior
- failure fallback
- cardinality

Never make a cache the only source of truth for correctness-sensitive state unless the architecture explicitly supports that model.

---

## 18. Search and Reporting Queries

Not every query belongs on the primary entity repository.

Complex search/reporting can use:
- dedicated query service
- read repository
- SQL projection
- database view/materialized view
- analytics store

Choose based on workload and consistency requirements.

Do not turn `UserRepository` into an all-purpose reporting engine.

---

## 19. Bulk Operations

For bulk writes/updates, ask:
- must every row satisfy domain rules?
- can one SQL operation preserve the invariant?
- what transaction size is acceptable?
- what locks occur?
- what audit events are required?
- are side effects needed per row?

Do not loop over thousands of `save()` calls when a safe set-based operation exists.

Do not use a bulk SQL shortcut if it bypasses required invariants or side effects.

---

## 20. Soft Deletes

If using soft deletion, define:
- which queries exclude deleted rows
- how admins retrieve deleted data
- uniqueness behavior
- restoration semantics
- retention/deletion policy

Beware "magic" global filters that make it unclear whether a query includes deleted records.

---

## 21. Testing

### Repository integration tests

Use a real or appropriately representative database for:
- query correctness
- constraints
- joins
- pagination
- transaction semantics
- locking/concurrency
- indexes where behavior matters

Mocks cannot prove that your SQL is correct.

### Unit tests

Use mocks/fakes when testing application logic that should not depend on persistence details.

Do not unit-test the ORM itself.

### Test Data

Use representative cardinality when evaluating query behavior.
A query that is fast on 50 rows may fail on 5 million.

---

## 22. Review Decision Tree

When reviewing a repository:

```text
Is this persistence logic?
 ├─ no → move upward/downward to correct layer
 └─ yes
      ↓
Is the operation intent-revealing?
 ├─ no → narrow the abstraction
 └─ yes
      ↓
Is returned data limited to what is needed?
 ├─ no → projection/select
 └─ yes
      ↓
Could this execute N+1 queries?
 ├─ yes → batch/join/load intentionally
 └─ no
      ↓
Is collection access bounded?
 ├─ no → add pagination/limit
 └─ yes
      ↓
Does concurrency affect correctness?
 ├─ yes → encode constraint/atomicity/locking
 └─ no
      ↓
Does it participate in a larger transaction?
 ├─ yes → make transaction ownership explicit
 └─ no
      ↓
Is authorization/tenant scope enforced appropriately?
 ├─ no → fix boundary
 └─ yes
      ↓
Is the abstraction actually reducing coupling?
 ├─ no → consider simpler direct access
 └─ yes → keep
```

---

## 23. Anti-Patterns

### Generic Base Repository
Adds indirection but no meaningful boundary.

### Repository Per Table
Created automatically even when persistence is trivial.

### Generic Query Escape Hatch
Every service can pass arbitrary ORM options.

### Business Policy in SQL
A repository secretly decides eligibility or authorization policy that should be application/domain behavior.

### Unbounded findAll
Works in development, fails at scale.

### Entity Everywhere
ORM entity becomes database model, domain model, API response, event payload, and test fixture simultaneously.

### Hidden Transactions
Each method commits independently although the use case requires atomicity.

### Magic Caching
Repository returns stale data without callers understanding freshness/invalidation.

### N+1 Hidden Behind ORM
Code looks clean while relation access triggers hundreds of queries.

---

## 24. Verification Checklist

- [ ] Repository responsibility is clear.
- [ ] Abstraction is justified.
- [ ] Methods express intent.
- [ ] No business workflow is hidden inside persistence.
- [ ] Query result is appropriately projected.
- [ ] No obvious N+1 behavior.
- [ ] Collection queries are bounded.
- [ ] Sort/filter fields are controlled.
- [ ] Tenant/object scope is correct.
- [ ] Transaction ownership is explicit.
- [ ] Concurrency assumptions are reviewed.
- [ ] Persistence errors are translated safely.
- [ ] ORM leakage is intentional.
- [ ] Bulk operations preserve invariants.
- [ ] Integration tests cover important DB behavior.
- [ ] Performance-sensitive queries are measured.
