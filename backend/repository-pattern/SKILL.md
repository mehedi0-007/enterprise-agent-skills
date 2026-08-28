---
name: repository-pattern
description: Design persistence boundaries and data-access abstractions. Use when creating repositories, reviewing ORM usage, designing queries, or deciding whether a repository abstraction is justified.
---

# Repository Pattern

## Mission
Isolate persistence concerns without hiding meaningful query semantics or creating abstraction ceremony.

## Use a Repository When
- persistence logic is non-trivial
- a meaningful data-access boundary improves testability/changeability
- queries are reused coherently
- the application needs a stable persistence port

Do not create a repository merely because every entity is expected to have one.

## Repository Owns
- SQL/ORM query construction
- projections
- persistence mapping
- persistence-specific filters
- persistence error translation

## Repository Does Not Own
- HTTP
- authorization policy
- unrelated workflows
- email/payment/queue orchestration
- business decisions

## Interface Shape
Prefer intent-revealing operations over a generic CRUD abstraction when queries have meaningful semantics.

Good:
`findActiveSubscriptionsForAccount(accountId)`

Suspicious:
`find({ where, joins, options, rawSql, ... })`

The latter can become an accidental database API exposed to the entire application.

## Performance
Repositories are a common location for:
- N+1
- over-fetching
- missing pagination
- inefficient joins
- repeated queries

Review actual generated SQL when performance matters.

## Transaction Ownership
Do not hide transaction boundaries inside individual repository calls when a use case spans multiple operations.

## Verification
Review query shape, returned data, authorization-sensitive fields, transaction behavior, and test coverage.
