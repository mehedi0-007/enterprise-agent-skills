---
name: repository-pattern
description: Define and review persistence boundaries in backend applications. Use when deciding where database queries belong, designing repositories/data-access modules, reviewing query abstractions, or preventing business logic from leaking into persistence code.
---

# Repository Pattern

## Purpose
Keep persistence concerns explicit without turning repositories into generic wrappers or hiding important business behavior.

## Responsibilities
A repository/data-access component may own:
- database queries
- persistence mapping
- query-specific projections
- persistence-specific filters/sorting
- persistence error translation
- efficient data retrieval

It should not own:
- HTTP concerns
- authorization policy
- unrelated business workflows
- email/payment/queue side effects
- arbitrary orchestration across unrelated use cases

## Before Introducing a Repository
Ask:
1. Is there meaningful persistence behavior to isolate?
2. Will the abstraction improve testing or changeability?
3. Is the codebase already using a consistent data-access pattern?
4. Would direct ORM/SQL access be clearer for this simple operation?

Do not introduce a repository only because "clean architecture" says every model must have one.

## Query Design
Repositories should expose operations aligned with use cases or meaningful data-access capabilities, not an enormous set of generic methods.

Prefer:
- getById
- findActiveByEmail
- listForOrganization
- save
- delete

over a generic abstraction that hides important query semantics.

Return only data needed by the caller when practical. Avoid accidental full-row loading.

## Boundaries
Keep business decisions in services/domain code.
A repository can answer:
"Which orders are pending for this customer?"

It should not decide:
"Should this customer be allowed to cancel the order?"

That policy belongs to the application/domain layer.

## Transactions
Do not make every repository method silently open its own transaction.
Transaction ownership should be explicit at the application/use-case boundary when multiple operations must be atomic.

## Error Handling
Translate low-level persistence errors when callers need a stable domain/application error. Preserve enough diagnostic context for logs without leaking database internals to API clients.

## Performance
Watch for:
- N+1 queries
- over-fetching
- unbounded lists
- repeated identical queries
- accidental joins
- loading large blobs unnecessarily

When performance matters, measure the actual query rather than optimizing the abstraction first.

## Anti-Patterns
Avoid:
- repository-per-table purely for ceremony
- generic "BaseRepository" with dozens of unused methods
- business logic hidden in SQL helpers
- repositories returning ORM entities everywhere when a read model/projection is clearer
- transaction boundaries that are impossible to see from the use case

## Verification
Review:
- clear responsibility
- predictable transaction ownership
- no business rules hidden in persistence
- query count is appropriate
- no accidental sensitive-field exposure
- tests cover important persistence behavior
