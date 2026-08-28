# Common Race Patterns

## Check-Then-Act
Unsafe:
check whether a row exists → insert.

Another request can insert between those operations.

Preferred:
database UNIQUE constraint → attempt insert → translate conflict.

## Read-Modify-Write
Unsafe:
read balance → subtract in application → write.

Preferred options:
- atomic conditional UPDATE
- row lock inside transaction
- optimistic version check

## Duplicate Jobs
A worker can receive the same logical job more than once.

Use:
- idempotency key
- durable job state
- unique constraint
- safe state transition

## Lock Ordering
If a transaction must lock multiple rows, use a consistent ordering to reduce deadlock risk.
