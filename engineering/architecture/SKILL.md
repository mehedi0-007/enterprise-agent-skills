---
name: architecture
description: Design and evaluate maintainable application architecture and boundaries. Use when adding a substantial feature, module, integration, data flow, or when existing structure is becoming difficult to change.
---

# Architecture

## Goal
Choose the simplest architecture that satisfies current requirements while preserving clear boundaries and future changeability.

## First Principles
- Prefer simple, explicit designs over speculative abstractions.
- Keep business rules independent from transport and infrastructure where practical.
- Make ownership of data and behavior explicit.
- Minimize coupling and hidden side effects.
- Prefer cohesive modules with narrow responsibilities.
- Do not introduce microservices, event buses, repositories, or abstractions merely because they are fashionable.

## Analyze Before Changing
Inspect:
- module boundaries
- dependency direction
- data ownership
- transaction boundaries
- external integrations
- synchronous vs asynchronous flows
- error propagation
- security boundaries
- test boundaries
- operational concerns

## Decision Questions
For each architectural choice ask:
1. What requirement forces this choice?
2. What simpler design was considered?
3. What coupling does this introduce?
4. What failure modes does it create?
5. What consistency guarantees are required?
6. What is the rollback/migration path?
7. How will the design be tested and observed?

## Layering
A typical application may separate:
- transport/controller: HTTP or messaging concerns
- application/service: orchestration and use cases
- domain: business rules and invariants
- persistence/repository: data access
- infrastructure: external systems

These are guidelines, not mandatory layers. Avoid pass-through abstractions with no meaningful responsibility.

## Architecture Decision Record
For important decisions document:
- context
- decision
- alternatives
- consequences
- operational implications

## Verification
A design is not complete until boundaries, failure behavior, data ownership, testing strategy, and migration/rollback implications are understood.
