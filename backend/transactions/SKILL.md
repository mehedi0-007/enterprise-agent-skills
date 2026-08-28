---
name: transactions
description: Define database transaction boundaries and atomicity for backend workflows. Use when multiple writes must satisfy an invariant, when state transitions can race, or when failure consistency matters.
---

# Transactions

## Start With the Invariant
Ask what must be true after success and impossible after failure.

Examples:
- order and order items commit together
- inventory cannot go below zero
- two sides of a transfer change atomically
- state transition happens once

## Boundary
Keep the transaction around the smallest atomic database unit.
Avoid:
- user interaction inside transactions
- slow external HTTP calls inside DB transactions
- unnecessary long-running transactions

## Isolation
Understand the actual isolation level and its consequences. PostgreSQL defaults to Read Committed; stronger isolation can introduce serialization failures that must be retried.

## Read-Modify-Write
A transaction alone does not automatically make every read-modify-write safe under concurrency. Determine whether you need:
- atomic SQL
- row locks
- optimistic locking
- stronger isolation
- database constraints

## External Effects
DB rollback cannot undo an email/payment/webhook. For important workflows consider transactional outbox, post-commit dispatch, idempotency, and reconciliation.

## Verification
Test rollback, concurrent execution, duplicate requests, constraint conflicts, and retry behavior.
