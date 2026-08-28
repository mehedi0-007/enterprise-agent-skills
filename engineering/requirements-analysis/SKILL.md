---
name: requirements-analysis
description: Turn ambiguous feature requests into explicit, testable requirements and acceptance criteria. Use before implementing a non-trivial feature, when requirements are incomplete, or when behavior could be interpreted multiple ways.
---

# Requirements Analysis

## Goal
Understand what must be built before deciding how to build it.

## Workflow
1. Inspect the existing product and relevant code before proposing changes.
2. Identify the user/problem, desired outcome, scope, constraints, and non-goals.
3. Separate explicit requirements from assumptions.
4. Identify actors, permissions, inputs, outputs, state transitions, and failure cases.
5. Identify business rules and invariants that must always hold.
6. Identify integration, data, compatibility, security, and operational constraints.
7. Convert requirements into observable acceptance criteria.
8. Resolve materially ambiguous requirements with the user; do not silently invent business behavior.
9. Keep the smallest scope that satisfies the stated outcome.

## Acceptance Criteria
Prefer observable statements:
- Given [state], when [action], then [result].
- Include success, validation failure, authorization failure, not-found, conflict, and dependency-failure cases when relevant.
- Include idempotency/retry behavior for operations that can be repeated.

## Avoid
- Coding before understanding the behavior.
- Treating assumptions as requirements.
- Adding speculative features.
- Requiring implementation details in product requirements unless they are actual constraints.

## Verification
Before implementation begins, be able to state:
- What problem is solved.
- Who can perform the action.
- What inputs are accepted.
- What outputs/state changes occur.
- What happens on failure.
- How success can be tested.
