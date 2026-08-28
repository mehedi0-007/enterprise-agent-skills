---
name: transactions
description: Design transaction boundaries and atomicity for backend workflows. Use when multiple reads/writes must satisfy an invariant, when implementing financial/state transitions, or when concurrency can produce inconsistent state.
---

# Transactions

## Purpose
Use transactions to protect specific correctness invariants, not as a blanket wrapper around every service.

## Define the Invariant First
Before opening a transaction, identify what must be true if the operation succeeds.

Examples:
- order and order items are created together
- inventory cannot become negative
- a unique business state transition occurs once
- a transfer debits one account and credits another atomically

## Boundary
The transaction should normally surround the smallest set of database operations that must commit or roll back together.

Avoid:
- long-running transactions
- user interaction inside a transaction
- network calls inside a database transaction unless deliberately justified
- background work that holds a transaction open

## Isolation
Understand the isolation level before relying on a read-then-write pattern. PostgreSQL uses Read Committed by default; stronger isolation can change failure/retry behavior. Applications using Serializable must be prepared to retry serialization failures. 

## Concurrency
Ask:
- Can two requests execute this use case simultaneously?
- Can both read the same old state?
- Is a constraint enough?
- Is row locking required?
- Would an atomic UPDATE be safer?
- Is optimistic locking appropriate?
- Does the caller need an idempotency key?

## External Side Effects
A database transaction cannot automatically roll back an email, payment, webhook, or queue publish performed outside the database.

For important workflows consider:
- transactional outbox
- post-commit dispatch
- idempotency
- reconciliation

## Failure Handling
A rollback is not necessarily a user-visible 500. Translate known constraint/conflict failures to stable application errors.

## Verification
Test:
- atomic success
- rollback on failure
- concurrent execution
- duplicate requests
- deadlock/serialization retry behavior where relevant
- external side-effect failure behavior
