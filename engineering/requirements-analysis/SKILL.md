---
name: requirements-analysis
description: Turn ambiguous feature requests into explicit, testable requirements. Use when a request is incomplete, behavior is ambiguous, scope is non-trivial, or implementation could reasonably differ.
---

# Requirements Analysis

## Mission
Understand the problem and observable behavior before choosing implementation.

## Activation
Use for new features, changes to existing behavior, integrations, workflows, permissions, data changes, or bug fixes whose intended behavior is unclear.

## Procedure
1. Inspect the existing product, architecture, conventions, and related code.
2. Identify actor, goal, trigger, inputs, outputs, state changes, business rules, constraints, and non-goals.
3. Separate facts from assumptions.
4. Identify happy path and failure paths.
5. Identify authorization, data ownership, concurrency, retry, and external-dependency concerns.
6. Convert behavior into acceptance criteria.
7. Resolve material ambiguity instead of inventing business rules.
8. Prefer the smallest scope that solves the stated problem.

## Decision Table

| Question | If yes | If no |
|---|---|---|
| Can this operation be retried? | Define idempotency/replay behavior | Document why not |
| Does it mutate shared state? | Analyze transaction/concurrency | Simpler flow may suffice |
| Does it expose data? | Define authorization + field exposure | Continue |
| Can it be unbounded? | Add limits/pagination | Continue |
| Does it call an external system? | Define timeout/retry/failure semantics | Continue |

## Acceptance Criteria
Prefer observable statements:
Given [state], when [action], then [result].
Cover validation, authorization, not-found, conflict, dependency failure, retries, and concurrency when relevant.

## Anti-patterns
- Coding from a vague request.
- Treating assumptions as requirements.
- Designing APIs from database tables without considering clients.
- Adding speculative functionality.

## Verification
Before implementation, be able to explain what success means, who can perform the operation, what changes, what can fail, and how it will be tested.
