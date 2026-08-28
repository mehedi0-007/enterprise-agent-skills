---
name: architecture
description: Design and evaluate maintainable application architecture and boundaries. Use when adding substantial features, modules, integrations, data flows, or refactoring structural problems.
---

# Architecture

## Mission
Choose the simplest architecture that satisfies current requirements while preserving clear ownership, testability, and changeability.

## Inspect First
Before proposing structure, inspect:
- module boundaries
- dependency direction
- application entry points
- data ownership
- transaction boundaries
- external integrations
- existing conventions
- test boundaries
- deployment/runtime constraints

Do not invent a new architecture without comparing it to the existing one.

## Core Principles
- Cohesion over abstraction.
- Explicit dependencies over hidden coupling.
- Business rules independent of transport where practical.
- Stable boundaries around volatile infrastructure.
- Prefer one deployable unit until there is a real reason to split it.
- Avoid premature microservices/event buses/CQRS.

## Layering Heuristic

Transport:
- HTTP/messaging parsing
- DTO validation
- protocol status/headers

Application:
- use-case orchestration
- transaction ownership
- authorization coordination
- external side-effect coordination

Domain:
- business invariants
- state transitions
- calculations/policies

Persistence:
- queries and persistence mapping

Infrastructure:
- databases, queues, email, payment, storage, external APIs

These are responsibilities, not mandatory classes.

## Decision Process
For each new abstraction ask:
1. What problem does it solve?
2. What code depends on it?
3. What dependency direction does it enforce?
4. What complexity does it add?
5. Can the same goal be achieved more simply?
6. How will it be tested?
7. What happens when the underlying dependency fails?

## Red Flags
- God services
- circular dependencies
- pass-through repositories
- business rules in controllers
- ORM entities becoming the public API
- infrastructure imported throughout domain code
- abstractions created only for theoretical future requirements

## Architecture Decision Record
For consequential decisions record context, decision, alternatives, consequences, and operational impact.

## Verification
A design is ready when ownership, boundaries, failure behavior, transaction semantics, testing boundaries, and migration/rollback implications are explicit.

## Activation

Use when creating or changing system/module boundaries, dependencies, data ownership, integration patterns, or major technical design.

## Review Procedure

1. State requirements and constraints.
2. Identify bounded responsibilities and ownership.
3. Map data/control flow and trust boundaries.
4. Compare simple and more complex options.
5. Review failure, scaling, operability, security, and migration implications.
6. Make assumptions and tradeoffs explicit.
7. Verify the architecture against realistic workflows.

## Verification Checklist

- [ ] requirements drive the design
- [ ] responsibilities are cohesive
- [ ] dependency direction is clear
- [ ] data ownership is explicit
- [ ] failure modes considered
- [ ] security/operability considered
- [ ] migration/rollback implications considered
