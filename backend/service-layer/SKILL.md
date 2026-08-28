---
name: service-layer
description: Design application/service boundaries and business logic placement in backend systems. Use when deciding what belongs in controllers, services, domain code, repositories, or infrastructure, or when a service is becoming large or tightly coupled.
---

# Service Layer

## Goal
Keep transport concerns, business decisions, persistence, and infrastructure responsibilities understandable and testable.

## Responsibilities

### Controller / Transport
Should handle:
- request parsing
- authentication context
- DTO validation
- HTTP-specific status/headers
- mapping transport input to application calls
- mapping application results to transport responses

Avoid:
- complex business rules
- direct multi-step database workflows
- authorization decisions that belong to business policy
- external integrations

### Application Service
Should orchestrate a use case:
- load required data
- invoke business rules
- coordinate repositories/integrations
- define application transaction boundaries
- produce an application result

Avoid turning it into a generic "god service".

### Domain
Place rules that must remain true regardless of HTTP, CLI, queue, or UI entry point here when practical.
Examples:
- state transition rules
- invariants
- pricing/business calculations
- eligibility rules

### Repository / Persistence
Own:
- queries
- persistence mapping
- data-access concerns
- query-specific optimization

Do not hide meaningful business decisions inside repositories.

### Infrastructure
Own external concerns:
- email provider
- object storage
- payment provider
- queue
- cache
- third-party APIs

## Transactions
A transaction should cover the smallest set of writes that must commit atomically.
Do not hold transactions across slow network calls unless there is a deliberate and justified design.
Be explicit about transaction ownership.

## Side Effects
For important state changes followed by external effects, consider:
- transactional outbox
- retry policy
- idempotency
- failure recovery
- eventual consistency

Do not assume "database write succeeded, therefore email/payment/webhook succeeded."

## Dependencies
Prefer dependencies pointing toward stable business/application abstractions.
Avoid circular dependencies and service-to-service chains that make behavior difficult to reason about.

## Service Size
When a service becomes difficult to understand:
1. identify distinct use cases
2. identify shared domain rules
3. separate infrastructure adapters
4. extract only cohesive responsibilities
5. preserve transaction and error semantics

Do not split classes merely to reduce line count.

## Verification
For each use case, be able to identify:
- entry point
- authorization boundary
- business rules
- data reads/writes
- transaction boundary
- external side effects
- retry/idempotency behavior
- failure behavior
- tests
