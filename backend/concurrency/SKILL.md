---
name: concurrency
description: Prevent races, lost updates, duplicate side effects, and inconsistent shared state. Use for inventory, balances, counters, unique resources, state transitions, workers, payments, and read-modify-write flows.
---

# Concurrency

## Assume Concurrent Actors
Requests, workers, cron jobs, and retries can overlap unless explicitly prevented.

## Suspicious Patterns
- check then insert
- read then calculate then write
- read balance then debit
- read status then update
- increment in application memory
- process then mark complete

## Prefer the Smallest Correct Mechanism
1. Database constraint
2. Atomic SQL statement
3. Optimistic locking
4. Row locking
5. Appropriate transaction isolation
6. Distributed lock only when genuinely necessary

## Database Constraints
For uniqueness, enforce uniqueness in the database and translate the resulting conflict. A preliminary existence check is not sufficient.

## Atomic Operations
Prefer a single conditional update when it can express the invariant. Verify affected-row count.

## Optimistic Locking
Useful when conflicts are possible but relatively infrequent and stale writes can be rejected/retried.

## Row Locks
Use row locks when the invariant requires serialized access to the same records. Keep lock duration short and acquire multiple locks in a consistent order where possible to reduce deadlock risk.

## Idempotency
For retried commands with side effects, persist an idempotency key/result or equivalent deduplication state.

## Verification
Write concurrency tests for critical invariants. Do not rely solely on single-threaded unit tests.
