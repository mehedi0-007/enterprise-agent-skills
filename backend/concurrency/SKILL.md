---
name: concurrency
description: Detect and prevent race conditions, lost updates, duplicate side effects, stale writes, and unsafe concurrent worker/request behavior. Use for shared mutable state, inventory, balances, counters, uniqueness, state transitions, background jobs, retries, payments, and read-modify-write workflows.
---

# Concurrency — Production Playbook

## 1. Mission

Assume important backend state can be touched by multiple actors at the same time unless the system explicitly prevents that.

Actors include:
- HTTP requests
- background workers
- scheduled jobs
- retries
- webhook deliveries
- multiple service instances
- users editing the same record

The goal is to preserve business invariants under overlap.

---

## 2. Activation

Use this skill when:
- one operation reads state and later writes based on that state
- two actors can modify the same resource
- uniqueness is enforced by application logic
- counters/balances/inventory are changed
- jobs can be delivered more than once
- webhooks may be duplicated/reordered
- users can edit the same record
- retries may overlap with original execution
- distributed workers process a shared queue

---

## 3. First Question: What Can Race?

Look for:

```text
read → decide → write
check → insert
read → calculate → save
process → mark complete
send external effect → record result
```

These are not automatically unsafe, but they require explicit concurrency analysis.

---

## 4. Identify the Invariant

Write what must remain true.

Examples:

- balance cannot become negative
- stock cannot go below zero
- username is unique
- only one active subscription exists per account
- a payment command is processed once
- a task cannot be claimed by two workers
- stale edits cannot silently overwrite newer data

If the invariant is unclear, implementation should stop and clarify it.

---

## 5. Choose the Smallest Correct Mechanism

Prefer, in this order when sufficient:

1. database constraint
2. atomic database statement
3. optimistic concurrency/version check
4. row-level lock
5. appropriate transaction isolation
6. distributed lock

The goal is not maximum locking. The goal is the smallest mechanism that guarantees the invariant.

---

## 6. Database Constraints Win Many Races

For uniqueness, prefer a real constraint:

```text
UNIQUE(email_normalized)
```

rather than:

```text
SELECT user WHERE email = ?
if none:
    INSERT user
```

The pre-check can race.

Safe pattern:

```text
attempt INSERT
   ↓
database enforces uniqueness
   ↓
translate conflict
```

Application validation can improve UX but is not the final concurrency control.

---

## 7. Atomic Updates

If the invariant can be expressed as one SQL statement, prefer that over read-modify-write.

Example:

```sql
UPDATE inventory
SET available = available - :quantity
WHERE product_id = :id
  AND available >= :quantity;
```

Then inspect affected-row count.

Meaning:
- 1 row updated → reservation succeeded
- 0 rows → insufficient stock or missing record

This avoids an unsafe application-level read followed by write.

---

## 8. Lost Updates

Problem:

```text
User A reads version 5
User B reads version 5
A writes version 6
B writes version 6
```

B may silently overwrite A.

Choose:
- optimistic version check
- ETag / If-Match at API boundary
- atomic update
- row lock where appropriate

For optimistic concurrency:

```text
UPDATE resource
SET ...
WHERE id = ?
  AND version = 5;
```

Then:
- affected rows = 1 → success
- affected rows = 0 → stale write/conflict

Do not silently overwrite newer state.

---

## 9. Optimistic Concurrency

Prefer when:
- conflicts are relatively infrequent
- holding locks would hurt concurrency
- stale writes should be rejected/reconciled
- clients can reload/retry

Define the user/application behavior after conflict:
- automatic retry
- reload
- merge
- return conflict
- require explicit user decision

Do not add optimistic locking without a clear conflict policy.

---

## 10. Pessimistic / Row Locking

Use row locks when concurrent operations must serialize access to the same row(s).

PostgreSQL's `SELECT ... FOR UPDATE` can lock selected rows against conflicting updates/deletes until the transaction ends. citeturn649864search9

Good candidates:
- balance transfers
- inventory reservation
- strict state transitions
- job claiming when a database lock is the intended mechanism

Costs:
- waiting
- contention
- deadlocks
- lower parallelism

Keep lock duration short.

---

## 11. Lock Ordering

If one operation can lock multiple resources:

Bad:

```text
Transaction A: lock A → lock B
Transaction B: lock B → lock A
```

Potential deadlock.

Prefer a consistent acquisition order, such as ascending ID.

If consistent ordering is impossible, design bounded deadlock handling and retry the appropriate transaction.

---

## 12. Transaction Alone Is Not Enough

A transaction gives atomic commit/rollback, but the chosen isolation level determines what concurrent operations can observe.

A Read Committed transaction can still contain unsafe read-modify-write logic.

Therefore ask separately:
- is the operation atomic?
- is the read stable enough?
- can another transaction change the row?
- do we need a lock/version/constraint?

Do not treat "inside transaction" as equivalent to "concurrency safe."

---

## 13. Isolation as a Concurrency Tool

Choose isolation based on the invariant.

PostgreSQL defaults to Read Committed. Stronger levels can prevent more anomalies but can increase contention or surface serialization failures. citeturn649864search10

Do not raise isolation globally to solve one specific race.

Prefer a local mechanism if it protects the invariant more simply:
- atomic update
- lock
- constraint
- version check

---

## 14. Check-Then-Act

Review every:

```text
if condition:
    perform action
```

where the condition depends on mutable shared state.

Examples:
- if no active subscription → create
- if stock >= quantity → decrement
- if job status = pending → process
- if email unused → insert

Ask whether another actor can change the state after the check.

Possible solutions:
- unique constraint
- conditional update
- transaction + lock
- optimistic version
- explicit state transition constraint

---

## 15. State Machines

When resources have states:

```text
PENDING
PAID
SHIPPED
CANCELLED
```

do not allow arbitrary updates.

Define allowed transitions and enforce them at the appropriate layer.

For concurrency-sensitive transitions, use conditional updates or locks.

Example concept:

```sql
UPDATE orders
SET status = 'CANCELLED'
WHERE id = :id
  AND status = 'PENDING';
```

Then affected-row count tells whether the transition succeeded.

This avoids:
```text
read status
if pending:
    update status
```
as two unconstrained operations.

---

## 16. Counters and Aggregates

Avoid:

```text
count = readCount()
count++
save(count)
```

when multiple writers exist.

Prefer:
```sql
UPDATE counters
SET count = count + 1
WHERE id = :id;
```

Then periodically reconcile derived counters against authoritative data when correctness matters.

For complex aggregate maintenance, decide whether:
- synchronous transaction
- event-driven update
- periodic reconciliation

best fits the consistency requirement.

---

## 17. Idempotency

Concurrency and retries often overlap.

For externally visible commands:
- define a logical operation identity
- persist deduplication state where necessary
- protect it with uniqueness/concurrency controls
- make concurrent duplicate requests converge to one result

Example:

```text
request A key = abc
request B key = abc
        ↓
unique/idempotency record
        ↓
one operation executes
        ↓
both receive defined result
```

Do not claim exactly-once execution merely because duplicates are usually rare.

---

## 18. Queue Workers

Assume jobs may be delivered more than once.

Workers should be safe under:
- duplicate delivery
- retry
- process crash
- timeout after side effect
- partial completion
- concurrent workers

Use where appropriate:
- durable job state
- unique job/business key
- lease/visibility timeout
- idempotent processing
- atomic claim/update

Do not mark a job "done" before required durable effects are complete unless the workflow deliberately uses another state model.

---

## 19. Webhooks and Event Ordering

External events can be:
- duplicated
- delayed
- reordered

Do not assume delivery order unless the provider contract guarantees it.

Use:
- event IDs/deduplication
- version/timestamp checks when meaningful
- monotonic state transition rules
- reconciliation jobs

For state derived from events, define whether an older event can overwrite newer state.

---

## 20. External Side Effects

The hardest concurrency problems often involve:

```text
database state
+
external side effect
```

Example:
two requests both observe unpaid state, both call payment provider.

Controls may include:
- idempotency key at provider
- local operation record
- DB uniqueness
- transaction + outbox
- workflow state machine

Never depend on timing ("the second request will probably see the first result").

---

## 21. Distributed Locks

Use distributed locks only when:
- the invariant spans resources that cannot be protected by a simpler database mechanism
- there is a clear lease/expiry model
- lock ownership and crash behavior are understood
- contention and failure modes are acceptable

A distributed lock introduces its own failure modes:
- lock expiry while work continues
- lost lock
- clock/lease assumptions
- orphaned state
- network partitions

Do not add Redis/distributed locking automatically to ordinary CRUD.

---

## 22. Cache Concurrency

Caches can create stale-read races and thundering-herd behavior.

Review:
- cache stampede
- stale overwrite
- invalidation ordering
- concurrent recomputation
- tenant isolation
- authorization scope

For correctness-sensitive state, keep the database/source of truth authoritative unless the architecture explicitly supports another model.

---

## 23. Multi-Instance Applications

Never rely on in-memory process state for a cross-instance invariant.

Unsafe examples:
- local mutex for unique username
- in-memory "already processing" set
- local rate counter
- local lock in one Node process

These fail when there are multiple replicas.

Use shared durable coordination:
- database constraint/transaction
- shared queue
- distributed coordination mechanism when justified

---

## 24. Testing Concurrency

Single-threaded tests do not prove concurrency safety.

For important invariants:
1. identify competing operations
2. run them concurrently
3. use representative database state
4. assert the invariant after completion
5. repeat enough to expose timing-sensitive behavior where practical

Test:
- duplicate create
- concurrent updates
- concurrent state transition
- inventory/balance races
- duplicate worker delivery
- deadlock/retry behavior
- stale write rejection

Where useful, inject controlled barriers so two operations overlap at the dangerous point.

---

## 25. Review Procedure

For each shared-state operation ask:

1. What state is shared?
2. Who can modify it?
3. Can operations overlap?
4. Which invariant must hold?
5. Is there a check-then-act sequence?
6. Can a database constraint enforce it?
7. Can an atomic statement enforce it?
8. Would optimistic concurrency be enough?
9. Is a lock justified?
10. What isolation level is assumed?
11. Can a deadlock occur?
12. What happens on retry?
13. What happens after process crash?
14. Are external effects duplicated?
15. Is the behavior safe across multiple application instances?

---

## 26. Anti-Patterns

### Check Then Insert
Application-level existence check without DB uniqueness.

### Read Modify Write
Application calculates from stale shared state.

### Transaction Means Safe
Assuming any transaction automatically solves races.

### Global Serializable
Increasing isolation globally to avoid understanding one local race.

### Unbounded Retry
Repeated transaction/operation retry increases load and hides bugs.

### Local Mutex
Using in-memory locks in a horizontally scaled application.

### Distributed Lock Everywhere
Adding Redis locks where a database constraint/atomic update would solve the problem more simply.

### Silent Lost Update
Last writer wins without explicit policy.

### Exactly-Once Claim
Calling an at-least-once workflow exactly-once.

### Order Assumption
Assuming webhook/queue events arrive in order without a provider guarantee.

---

## 27. Verification Checklist

- [ ] shared state identified
- [ ] invariant explicitly stated
- [ ] competing actors identified
- [ ] check-then-act patterns reviewed
- [ ] DB constraints considered
- [ ] atomic SQL considered
- [ ] optimistic concurrency considered
- [ ] row locks justified if used
- [ ] isolation assumptions explicit
- [ ] lock ordering reviewed
- [ ] deadlock/retry behavior defined
- [ ] idempotency considered
- [ ] crash/restart behavior considered
- [ ] multi-instance behavior safe
- [ ] external side effects protected
- [ ] concurrency tests exist for critical paths

## References

- `references/race-patterns.md`
- `references/locking-vs-optimistic.md`
- `references/idempotent-workers.md`

## Cross-Skill Routing
- For `transactions` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
- For `postgresql` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
