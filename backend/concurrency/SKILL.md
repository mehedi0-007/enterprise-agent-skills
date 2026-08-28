---
name: concurrency
description: Analyze and prevent race conditions, lost updates, duplicate side effects, and inconsistent state in backend systems. Use for counters, inventory, payments, state transitions, unique resources, background workers, or any read-modify-write workflow.
---

# Concurrency

## Goal
Assume important state may be modified by more than one request or worker at the same time.

## Identify Race-Prone Patterns
Treat these as suspicious until analyzed:
- read -> calculate -> write
- check if exists -> insert
- check balance -> debit
- read state -> decide -> update
- increment in application memory
- process job -> mark complete

The time between the read and write is an opportunity for another actor to change state.

## Preferred Controls
Choose the smallest mechanism that protects the invariant:
1. database constraint
2. atomic SQL update
3. optimistic locking/version column
4. row lock/select-for-update
5. transaction isolation
6. distributed lock only when database/application mechanisms are insufficient

Do not reach for Redis/distributed locks automatically.

## PostgreSQL Locking
PostgreSQL row locks can block conflicting updates/deletes and `SELECT ... FOR UPDATE` on the same rows until the transaction ends. Use explicit locking when the business invariant requires serial access to a row. 

## Unique Races
The safe pattern for uniqueness is usually:
- enforce uniqueness in the database
- attempt the write
- translate a unique violation into the appropriate application conflict

Do not depend on "check first, then insert" alone.

## Atomic Updates
Prefer an invariant-preserving SQL operation when possible.

Example concept:
`UPDATE accounts SET balance = balance - amount WHERE id = ? AND balance >= amount`

Then verify affected-row count rather than doing an unsafe read-modify-write in application code.

## Optimistic Locking
Use version/timestamp checks when conflicts are possible but contention is relatively low and retrying/rejecting stale writes is acceptable.

## Idempotency
For retried commands that create external effects, identify the command with an idempotency key and persist the result/state needed to make repeated submissions safe.

## Verification
Include concurrency tests for critical operations. Run multiple concurrent requests/workers and verify the invariant still holds.
