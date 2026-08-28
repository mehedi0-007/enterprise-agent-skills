---
name: transactions
description: Design and review transaction boundaries, isolation, locking, retries, and consistency for backend workflows. Use when multiple database operations must remain atomic, when concurrent requests can violate invariants, or when a workflow mixes database state with external side effects.
---

# Transactions — Production Playbook

## 1. Mission

A transaction protects a specific consistency invariant.

Do not wrap a method in a transaction merely because it touches the database. First identify what must become true together and what must never be partially committed.

A transaction is a correctness mechanism first and a performance concern second.

---

## 2. Activation

Use when:
- multiple database writes must succeed/fail together
- a read influences a subsequent write
- inventory/balance/counters/state transitions are involved
- uniqueness or business invariants can race
- multiple repositories participate in one use case
- isolation level matters
- row locks are being considered
- serialization/deadlock retries are possible
- database changes trigger external events/messages

---

## 3. Start With the Invariant

Write the invariant before choosing transaction mechanics.

Examples:

### Order creation
If an order is committed, its required order items must also exist.

### Inventory
Inventory must never become negative.

### Transfer
For an internal transfer, the debit and credit must both commit or neither does.

### State transition
An order cannot move from `CANCELLED` back to `PAID` through a concurrent stale write.

If you cannot state the invariant, you are not ready to choose the transaction boundary.

---

## 4. Define the Atomic Unit

A transaction normally contains the smallest set of database operations that must commit atomically.

Example:

```text
CreateOrder
BEGIN
  insert order
  insert items
  reserve inventory
COMMIT
```

Not:

```text
BEGIN
  send email
  call payment provider
  wait for external HTTP
  perform expensive computation
  insert database rows
COMMIT
```

Long transactions hold resources and increase contention.

Keep network calls, user interaction, and unrelated expensive work outside the transaction unless there is an explicit consistency requirement that justifies it.

---

## 5. Transaction Ownership

The application/use-case boundary should normally own transactions when a use case spans several persistence operations.

Example:

```text
Controller
   ↓
CreateOrder service/use case
   ↓
BEGIN
   repository A
   repository B
   repository C
COMMIT
```

Do not let each repository silently create its own independent transaction when the whole use case must be atomic.

This aligns with the Service Layer pattern: the application boundary coordinates operations and transaction behavior. citeturn161681search2

---

## 6. Read-Only vs Read-Write

Do not assume every database interaction needs a transaction.

A simple independent read may not need an explicit application transaction.

A read that participates in a correctness-sensitive decision may need transactional semantics or a stronger database operation.

Ask:
- Is the read merely informational?
- Is the result immediately used to make a write decision?
- Can another transaction change the relevant rows?
- What invariant depends on this read?

---

## 7. Isolation Levels

Understand the chosen isolation level before relying on it.

PostgreSQL's default is Read Committed. Under Read Committed, each command sees a snapshot established when that command begins, so two commands in the same transaction can observe different committed data. PostgreSQL also supports Repeatable Read and Serializable with stronger guarantees and different failure behavior. citeturn161681search10

### Practical decision

Use the weakest isolation level that still protects the required invariant.

Do not increase isolation simply because "Serializable is safer."

Stronger isolation may:
- increase contention
- produce serialization failures
- require retries
- reduce throughput

If Serializable is chosen, the application must be prepared to retry transactions that fail due to serialization conflicts.

---

## 8. Transaction vs Lock

A transaction alone does not make a read-modify-write sequence safe.

Example:

```text
BEGIN
read balance = 100
calculate 100 - 80
write 20
COMMIT
```

Two concurrent transactions can both read 100.

Possible controls:
- atomic conditional UPDATE
- row lock
- optimistic version check
- stronger isolation
- constraint

Choose the narrowest correct mechanism.

---

## 9. Row-Level Locking

When the invariant requires serial access to the same rows, explicit row locks may be appropriate.

PostgreSQL row-level locks can block conflicting updates/deletes and `SELECT ... FOR UPDATE` on the same rows until the transaction ends. citeturn161681search9

Example use case:

```text
SELECT inventory
FOR UPDATE
WHERE product_id = ?
```

then:

```text
validate quantity
update inventory
```

The lock is useful because another transaction cannot concurrently modify the locked row in a conflicting way until the first transaction ends.

### Do not lock automatically

Locks have cost:
- waiting
- contention
- deadlock risk
- reduced concurrency

First ask whether an atomic SQL statement or constraint can express the invariant more simply.

---

## 10. Constraints vs Transactions

Use database constraints whenever they can enforce an invariant directly.

Example:

```text
UNIQUE(user_id, provider)
```

is stronger than:

```text
SELECT ...
IF NOT EXISTS:
  INSERT ...
```

The existence check can race.

A transaction can coordinate the workflow, but a database constraint is often the ultimate enforcement mechanism for uniqueness.

---

## 11. Atomic SQL

Prefer a single atomic database statement when it naturally represents the invariant.

Example concept:

```sql
UPDATE accounts
SET balance = balance - :amount
WHERE id = :id
  AND balance >= :amount;
```

Then verify affected-row count.

This can be safer and faster than:
```text
SELECT balance
UPDATE balance
```

inside ordinary Read Committed transactions.

Do not replace domain logic with SQL merely to reduce statement count; the SQL operation must still preserve the intended business rule.

---

## 12. Optimistic Concurrency

Consider optimistic locking when:
- conflicts are relatively infrequent
- stale updates should be rejected
- holding locks is undesirable
- a version can be stored with the resource

Pattern:

```text
read version = 12
update ... WHERE id = ? AND version = 12
increment version
```

If zero rows are updated, the caller knows the record changed concurrently.

Define whether the application should:
- retry
- reload
- return a conflict
- ask the user to resolve

---

## 13. Lock Ordering and Deadlocks

Deadlocks can occur when transactions acquire locks in conflicting order.

Example:

```text
Transaction A: lock account 1 → wait for account 2
Transaction B: lock account 2 → wait for account 1
```

Mitigation:
- acquire multiple locks in a consistent order
- keep transactions short
- avoid unnecessary locks
- handle deadlock errors with bounded retry where appropriate

Never assume deadlocks mean the database is broken. They are a normal concurrency condition that the application may need to handle.

---

## 14. Retry Semantics

Not every transaction failure should be retried.

Retry candidates may include transient serialization/deadlock/conflict conditions.

Do not automatically retry:
- validation errors
- authorization failures
- permanent constraint violations
- malformed input
- known business conflicts

Microsoft's retry guidance emphasizes understanding failure type, idempotency, transaction consistency, and preventing layered retries from amplifying load. citeturn161681search7

### Retry policy
If retrying:
- keep attempts bounded
- use backoff/jitter
- retry the entire transaction unit when required by the database semantics
- avoid nested retry loops
- log retry-causing failures
- verify the operation is safe to repeat

---

## 15. Retries and Idempotency

Transaction retry does not automatically solve external side effects.

Bad:

```text
BEGIN
  write database
  charge payment provider
COMMIT
```

If the transaction is retried, the payment may execute twice.

The transaction boundary must be separated from external side-effect reliability.

Use, where appropriate:
- provider idempotency
- transactional outbox
- durable workflow state
- reconciliation

Microsoft's retry guidance explicitly ties safe retry behavior to idempotency. citeturn161681search7

---

## 16. Transaction + External Events

If a database state change must reliably produce an event/message, avoid an uncontrolled dual write:

```text
DB COMMIT
+
PUBLISH MESSAGE
```

A failure between the two can produce inconsistency.

The transactional outbox pattern records the state change and outbox message in the same transaction, then asynchronously publishes the message after commit. AWS documents this as a solution to the dual-write problem and notes that consumers must still tolerate duplicate messages. citeturn161681search0

Typical flow:

```text
BEGIN
  update business state
  insert outbox event
COMMIT
       ↓
outbox worker
       ↓
publish event
       ↓
consumer
       ↓
idempotent processing
```

---

## 17. Exactly Once

Do not claim exactly-once semantics casually.

A system may provide:
- exactly-once database state transition
- at-least-once message delivery
- idempotent consumer behavior

Those are different guarantees.

AWS specifically notes that transactional outbox implementations can produce duplicate messages and recommends idempotent consumers. citeturn161681search0

Describe the actual guarantee.

---

## 18. Savepoints

Use savepoints deliberately for partial rollback within a larger transaction when the database/application architecture needs that behavior.

Do not add savepoints automatically.

If partial failure can be safely represented as a normal application outcome, a simpler transaction boundary may be preferable.

---

## 19. Transaction Scope and Performance

Avoid:
- transactions spanning slow network calls
- huge batches with excessive lock/WAL pressure
- waiting for user input
- doing unrelated reads/writes while locks are held
- keeping idle transactions open

A long transaction can increase:
- lock contention
- resource usage
- vacuum pressure
- replication lag
- deadlock opportunities

Measure operational impact for high-volume workloads.

---

## 20. Multi-Service Transactions

Do not assume a normal database transaction can span independent services safely.

If one business operation spans multiple services/datastores, consider whether you need:
- orchestration
- saga
- compensating actions
- transactional outbox
- workflow state

AWS notes that distributed transactions can introduce latency/coordination concerns and provides saga patterns for multi-service consistency. citeturn161681search3turn161681search8

Avoid introducing distributed transaction machinery before the system actually requires it.

---

## 21. Failure Matrix

For each transactional use case, reason through:

| Failure point | Expected result |
|---|---|
| validation before BEGIN | no transaction needed |
| first DB write fails | rollback |
| later DB write fails | all atomic DB changes rollback |
| unique conflict | stable application conflict |
| deadlock | bounded retry or failure |
| serialization conflict | retry transaction if safe |
| app crashes after COMMIT | committed state remains; recovery process must continue |
| external call after COMMIT fails | retry/reconcile |
| outbox publish fails | outbox remains pending |
| duplicate event delivered | consumer deduplicates/idempotently processes |

---

## 22. Testing

Critical transaction behavior needs integration tests against a real/representative database.

Test:
- atomic success
- rollback
- constraint conflict
- concurrent requests
- lost-update prevention
- lock behavior
- deadlock handling
- serialization retry
- duplicate command
- outbox publishing/retry
- crash/restart recovery behavior where applicable

Mocks cannot prove database isolation or locking semantics.

---

## 23. Review Procedure

When reviewing a transaction:

1. What invariant requires atomicity?
2. What exact operations are atomic?
3. Is the transaction boundary visible?
4. Could it be smaller?
5. What isolation level is used and why?
6. Is there a read-modify-write race?
7. Would a constraint/atomic statement be simpler?
8. Are locks required?
9. Could lock ordering deadlock?
10. What failures are retryable?
11. Is retrying the whole transaction safe?
12. Are external side effects inside the boundary?
13. If so, why?
14. If not, how is the dual-write problem handled?
15. What happens after commit if the process crashes?
16. Are concurrency tests present?

---

## 24. Anti-Patterns

### Transaction Everywhere
All database methods wrapped in transactions without a consistency requirement.

### Huge Transaction
Network calls, loops, and unrelated computation while locks are held.

### Check-Then-Act
Reliance on prior existence checks instead of database constraints.

### Fake Atomicity
Multiple independently committed repository methods called from one use case.

### Retry Everything
Retries applied to permanent errors or unsafe side effects.

### External Call Inside DB Transaction
Payment/email/HTTP called while a database transaction remains open without strong justification.

### Exactly-Once Claims
Describing at-least-once systems as exactly-once.

### Distributed Transaction Too Early
Introducing sagas/2PC for a workflow that a single database transaction can solve.

---

## 25. Verification Checklist

- [ ] invariant is explicit
- [ ] atomic unit is explicit
- [ ] transaction owner is clear
- [ ] isolation level is understood
- [ ] read-modify-write races are analyzed
- [ ] constraints/atomic SQL considered
- [ ] locks justified and scoped
- [ ] lock ordering considered
- [ ] retryable failures identified
- [ ] retries are bounded and safe
- [ ] external side effects are not accidentally part of DB atomicity
- [ ] dual-write strategy exists where needed
- [ ] multi-service consistency strategy is explicit
- [ ] integration/concurrency tests exist
- [ ] operational impact is understood

## References

- `references/isolation-and-locking.md`
- `references/retry-strategy.md`
- `references/transactional-outbox.md`

## Cross-Skill Routing
- For `concurrency` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
- For `repository-pattern` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
