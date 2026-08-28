---
name: service-layer
description: Place application orchestration and business behavior in appropriate backend layers. Use when implementing use cases, controllers, services, repositories, integrations, transactions, or refactoring large services.
---

# Service Layer

## Responsibility Map

Controller/transport:
- parse protocol
- validate DTO shape
- authenticate context
- map application result to protocol

Application service:
- execute a use case
- orchestrate domain/repositories/integrations
- own transaction boundary when appropriate
- coordinate side effects

Domain:
- enforce business invariants
- calculate business decisions
- model meaningful state transitions

Repository:
- persistence/query behavior

Infrastructure:
- external systems and technical adapters

## Decision Rule
Put logic where it remains correct if the entry point changes.

If the same business rule would be needed from HTTP, queue, CLI, and scheduled jobs, it should not live only in a controller.

## Transactions
A use case that needs multiple writes to commit atomically should normally own that transaction boundary. Avoid each repository opening independent hidden transactions.

## External Side Effects
Database commit and external side effects are separate reliability domains.
For important workflows consider outbox/event patterns, idempotency, retries, and reconciliation.

## Service Size
Split by cohesive use cases/responsibilities, not arbitrary line count.
A large service may be a symptom of:
- too many use cases
- mixed infrastructure
- missing domain concepts
- unclear ownership

## Anti-patterns
- controllers containing business workflows
- services that merely proxy every repository method
- repositories making authorization decisions
- services calling each other in circular chains
- network calls inside DB transactions without strong justification

## Verification
For each use case identify entry point, authorization, business rules, data access, transaction boundary, side effects, retry behavior, and tests.
