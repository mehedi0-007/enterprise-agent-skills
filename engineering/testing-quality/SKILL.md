---
name: testing-quality
description: Design a layered, risk-based test strategy and verify behavior before declaring software complete. Use when adding or changing features, APIs, database behavior, security controls, asynchronous workflows, or critical business logic.
---

# Testing Quality

## Mission
Use tests to provide evidence of behavior, not merely increase line coverage.

## Test Pyramid by Responsibility
Choose the cheapest test that gives meaningful confidence:
- unit tests for pure business rules and calculations
- integration tests for database, queues, external adapters, and module boundaries
- API tests for request/response contracts and authorization
- end-to-end tests for critical user/business journeys
- targeted performance/load tests for known capacity risks
- security/negative tests for access-control and abuse cases

Do not force every behavior into end-to-end tests.

## Start With Risk
Before adding tests ask:
1. What can break?
2. What would be expensive or unsafe if it broke?
3. Which boundary is most likely to fail?
4. What behavior must never regress?
5. Which test level gives strong confidence at reasonable cost?

Prioritize:
- money/billing
- authorization
- data integrity
- state transitions
- destructive operations
- concurrency
- external side effects
- compatibility

## Test Behavior, Not Implementation
Prefer assertions about observable behavior and contracts.
Avoid tests that break merely because an internal helper/class/mocking detail changes.

## Negative Cases
For important features, test more than the happy path:
- invalid input
- unauthorized access
- missing resources
- conflicts
- dependency failure
- timeout
- duplicate submission
- stale state
- concurrent requests
- retry/replay

## Database Testing
Integration tests should exercise real database semantics for important queries, constraints, transactions, and migrations. ORM mocks cannot prove SQL behavior.

## External Dependencies
Mock/stub at the application boundary for fast unit tests, but maintain integration/contract coverage for important real interactions.

## Async Tests
Verify:
- ordering assumptions
- retries
- duplicate delivery
- cancellation/timeouts
- out-of-order results
- eventual completion/failure

## Flaky Tests
Treat flakiness as a defect.
Do not hide failures with arbitrary sleeps or excessive retries.
Find the synchronization, isolation, timing, or shared-state cause.

## Coverage
Coverage is a signal, not proof of correctness.
A high percentage with weak assertions can provide little value.

## Verification
Before completion:
- run the relevant unit/integration/API/E2E tests
- include negative/security cases for sensitive behavior
- verify deterministic behavior
- run typecheck/build/lint where applicable
- record tests actually run
