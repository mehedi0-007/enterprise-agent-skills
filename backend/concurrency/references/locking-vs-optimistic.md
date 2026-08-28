# Locking vs Optimistic Concurrency

## Optimistic
Good when:
- conflicts are rare
- stale updates are acceptable to reject
- user/app can retry or reconcile

## Pessimistic/Row Lock
Good when:
- the critical section is short
- conflicting operations must serialize
- the invariant is difficult to express as a single atomic statement

## Constraint/Atomic SQL First
If uniqueness or a conditional state transition can be enforced in one database operation, prefer that over application-managed locks.
