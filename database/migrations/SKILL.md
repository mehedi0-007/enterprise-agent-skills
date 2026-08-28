---
name: migrations
description: Design, review, stage, execute, and verify safe PostgreSQL schema and data migrations in production. Use for columns, tables, constraints, indexes, type changes, renames, drops, backfills, data transformations, or ORM-generated migrations.
---

# Database Migrations — Production Playbook

## 1. Mission

A migration changes durable shared state and may outlive the application release that created it.

The goal is not merely "make the new schema exist." The goal is:

- preserve data correctness
- keep old/new application versions compatible when required
- control locks and operational impact
- make progress observable
- make recovery explicit
- prevent destructive cleanup before dependencies are gone

For production, think in terms of a **schema/application compatibility window**, not one migration file.

---

## 2. Activation

Use when:
- adding/removing/renaming columns or tables
- changing data types
- changing nullability
- adding/removing constraints
- adding unique indexes
- creating/dropping indexes on large tables
- backfilling data
- splitting/merging columns
- changing enum/status representation
- changing tenant/data ownership
- deploying changes while old application instances may still run

For a trivial development-only schema change with no shared production data, a simpler migration may be appropriate.

---

## 3. Discover Before Writing SQL

Inspect:

### Application
- current readers of affected fields/tables
- current writers
- background workers
- scheduled jobs
- scripts/admin tools
- old API versions
- event consumers/producers
- ORM behavior
- connection pools

### Database
- table size
- row count
- growth rate
- indexes/constraints
- foreign keys
- active traffic
- replication topology
- lock behavior
- existing long-running transactions

### Deployment
- rolling vs replacement deployment
- whether old and new versions overlap
- migration execution mechanism
- rollback capability
- maintenance window availability

Never design a production migration from the schema definition alone.

---

## 4. Classify the Change

### Low-risk additive
Examples:
- new nullable column
- new table
- compatible index
- additive data structure

May fit a single migration if operational impact is understood.

### Potentially risky
Examples:
- new NOT NULL constraint
- unique constraint on populated data
- large index build
- large backfill
- column type change
- large update/delete

Requires data/lock/workload analysis.

### Destructive/breaking
Examples:
- drop column/table
- rename without compatibility plan
- remove enum value used by clients
- change type incompatibly
- make a required field unavailable to older writers

Usually requires staged expand/migrate/contract deployment.

---

## 5. Expand → Migrate → Contract

For breaking changes, prefer staged evolution:

```text
Current schema
      ↓
EXPAND
  add compatible structure
      ↓
Deploy compatible application
      ↓
MIGRATE
  backfill/dual-write/cutover
      ↓
Verify convergence + old readers/writers gone
      ↓
CONTRACT
  remove obsolete structure
      ↓
Verify
```

Prisma's production migration guidance describes expand-and-contract specifically to keep old/new application versions compatible while data moves between schemas. citeturn391389search1

Xata's `pgroll` similarly implements an expand/contract model in which old and new schema representations coexist during rollout. citeturn391389search3

---

## 6. Compatibility First

When old and new applications can overlap, the database must support both during the migration window.

Example: rename `name` → `full_name`.

Unsafe:
1. rename column
2. deploy new code

Old application instances may still query `name`.

Safer:
1. add `full_name`
2. deploy code that can read/write old + new
3. backfill
4. switch reads to new
5. stop writing old
6. prove no readers remain
7. drop old column later

Do not hide compatibility work inside one migration file if it actually requires multiple deployments.

---

## 7. Column Additions

Before adding a column, decide:
- nullable?
- default?
- application version compatibility?
- existing-row behavior?
- write path?
- read path?

For a large production table, understand whether the chosen default/constraint operation causes substantial rewrite, locking, or other workload impact for the PostgreSQL version and exact statement.

Do not assume "ADD COLUMN" always has negligible cost.

---

## 8. Making a Column NOT NULL

For populated tables, avoid assuming:

```sql
ALTER TABLE users
ALTER COLUMN phone SET NOT NULL;
```

is always the right first migration.

Safer staged concept:
1. add column nullable
2. deploy code that writes it
3. backfill existing rows
4. verify no invalid rows remain
5. add/enforce constraint
6. remove temporary compatibility logic later

Choose the exact PostgreSQL technique based on version, table size, existing constraints, and lock requirements.

---

## 9. Backfills

Large data changes are operational workloads, not just SQL statements.

A safe backfill should consider:
- batch size
- transaction duration
- lock duration
- WAL generation
- replication lag
- vacuum interaction
- CPU/I/O impact
- restartability
- progress measurement
- throttling
- failure recovery

Avoid one huge transaction when it would hold locks or generate unacceptable WAL/resources.

### Batch pattern

Conceptually:

```text
find next bounded chunk
      ↓
update chunk
      ↓
commit
      ↓
measure
      ↓
throttle if necessary
      ↓
repeat
```

A backfill should be restartable or checkpointed.

---

## 10. Dual Write

Dual writing can bridge old/new schemas:

```text
write old column
write new column
```

Use only when necessary and make the window explicit.

Risks:
- one write succeeds and the other fails
- old/new values diverge
- retries duplicate work
- readers disagree
- compatibility code never gets removed

Prefer a single transaction when both values are database-local and must remain consistent.

Do not leave dual-write code indefinitely.

---

## 11. Dual Read

During a transition, the application may need:

```text
read new
fallback old
```

or another controlled compatibility strategy.

Define:
- source of truth
- precedence
- what happens on mismatch
- when fallback can be removed

Do not silently hide divergence forever.

---

## 12. Backfill Verification

Do not mark a backfill complete because the script "finished."

Verify:
- expected row count
- null/missing count
- old/new parity where applicable
- invalid conversions
- duplicates
- business invariants

Example:

```text
source rows = 10,000,000
target populated = 10,000,000
mismatches = 0
```

For transformed data, define a correctness invariant stronger than row count.

---

## 13. Index Migrations

Index creation has workload impact.

PostgreSQL documents that a normal `CREATE INDEX` blocks concurrent writes while the index is being built, whereas `CREATE INDEX CONCURRENTLY` allows normal inserts/updates/deletes to proceed but has additional restrictions/costs. citeturn391389search0

For large production tables, evaluate:
- build duration
- lock behavior
- replication
- disk space
- failure recovery
- migration tool transaction constraints

Do not automatically choose `CONCURRENTLY` everywhere.

For concurrent index creation, remember:
- it cannot run inside a transaction block
- failed builds may leave an invalid index that needs cleanup
- operational monitoring is important

---

## 14. Constraint Migrations

Before adding:
- UNIQUE
- NOT NULL
- FOREIGN KEY
- CHECK

inspect existing data first.

A constraint migration can fail or cause operational impact if current data does not satisfy the invariant.

Typical pattern:
1. detect violations
2. clean/backfill
3. establish compatible writes
4. validate/enforce
5. remove temporary code

The exact PostgreSQL mechanism should be chosen according to table size, traffic, and lock behavior.

---

## 15. Type Changes

Type changes deserve explicit compatibility analysis.

Ask:
- is conversion lossless?
- is every existing value convertible?
- does application code expect the old type?
- do indexes/constraints depend on it?
- can old application versions still write the old representation?
- does the operation rewrite the table?
- what happens to dependent views/functions?

For large/high-traffic tables, consider an additive new column + backfill + cutover instead of an in-place incompatible change.

Do not assume an ORM-generated type migration is operationally safe merely because it succeeds in development.

---

## 16. Rename Operations

A database rename is often application-breaking.

Treat it as:
- add new name
- compatibility period
- migrate readers/writers
- verify old references are gone
- remove old name

Search the repository, jobs, migrations, SQL strings, views, reports, and operational scripts before removing the old name.

---

## 17. Drop Operations

Drops are irreversible from the application's perspective unless a backup/recovery mechanism can restore the data.

Before dropping:
- prove no application readers remain
- prove no writers remain
- check workers/queues/scripts
- check reporting/admin paths
- confirm external integrations
- check replication/CDC/analytics consumers
- confirm retention/legal requirements where relevant

Use a separate contract deployment when necessary.

A useful principle from migration safety tooling is: **the default answer to "can we drop this now?" should be "prove it."** citeturn391389search4

---

## 18. Migration and Deployment Ordering

A safe rolling sequence may be:

```text
Migration 1: expand
      ↓
Deploy application A+B compatible code
      ↓
Backfill
      ↓
Verify
      ↓
Deploy code using only new schema
      ↓
Drain old versions
      ↓
Migration 2: contract
```

Do not combine all phases merely because the tooling permits multiple statements in one migration file.

The deployment dependency is the important unit.

---

## 19. Rollback vs Forward Fix

Ask whether the migration is actually reversible.

### Reversible
Adding a nullable column is often easy to reverse.

### Potentially irreversible
A destructive data transformation may not be safely reversible.

For irreversible changes:
- define recovery plan
- verify backups/restore capability
- prefer staged rollout
- use forward-fix strategy where appropriate
- document what data cannot be reconstructed

Do not write a fake `down` migration that claims to restore information that has been destroyed.

---

## 20. Migration Files Are History

Once a production migration has executed, treat it as part of the database change history.

Prefer a new migration to editing an old executed migration.

Changing migration history can make environments diverge.

---

## 21. ORM Migrations

ORM-generated migrations are a tool, not a deployment safety guarantee.

Always inspect generated SQL for:
- destructive operations
- table rewrites
- locks
- index strategy
- data conversion
- defaults
- constraint timing

A migration that is safe on a development database may be unsafe on a 500M-row production table.

---

## 22. Observability During Migration

Important migrations should expose:
- current phase
- progress
- rows processed
- rows remaining
- duration
- failures/retries
- lock wait
- replication lag where relevant
- backfill rate

Do not run long migrations as invisible shell commands with no progress signal.

---

## 23. Pre-Flight Review

Before production execution, answer:

### Data
- how many rows?
- what values exist?
- any invalid data?
- what invariants must hold?

### Locking
- which lock does the operation acquire?
- what existing queries may be blocked?
- how long might it wait?

### Compatibility
- can old code read/write during the migration?
- can new code operate before backfill completes?

### Recovery
- how do we stop?
- how do we resume?
- how do we recover if partially complete?
- is rollback possible?

### Operations
- disk/WAL impact?
- replication impact?
- monitoring?
- maintenance window?

---

## 24. Verification Gates

Use explicit gates:

```text
DISCOVERED
   ↓
CLASSIFIED
   ↓
DESIGNED
   ↓
PRE-FLIGHT PASSED
   ↓
EXPAND COMPLETE
   ↓
APPLICATION COMPATIBLE
   ↓
BACKFILL VERIFIED
   ↓
OLD READERS/WRITERS DRAINED
   ↓
CONTRACT EXECUTED
   ↓
POST-VERIFY
```

Do not advance a destructive phase because a person or agent says "looks ready."

Require evidence.

Migration-conductor is an example of this philosophy: it uses phase gates and refuses the destructive contract step until backfill parity and old-reader removal are proven. citeturn391389search4

---

## 25. Anti-Patterns

### One Giant Migration
Schema change + huge backfill + cleanup in one transaction.

### Rename-and-Deploy
Rename DB field and immediately deploy new application code under rolling deployment.

### Unbounded Backfill
Millions of rows updated in one giant transaction with no monitoring/throttling.

### ORM Blindness
Trusting generated SQL without inspecting it.

### Fake Rollback
Down migration claims to restore data that was intentionally destroyed.

### Drop by Grep Alone
Only searching the main application code and ignoring workers/scripts/consumers.

### Dual Write Forever
Temporary compatibility logic becomes permanent.

### No Convergence Proof
Dropping old columns without demonstrating old readers/writers are gone.

### No Operational Plan
No estimate/monitoring/recovery strategy for a large production migration.

---

## 26. Review Checklist

### Discovery
- [ ] affected readers/writers identified
- [ ] workers/scripts/consumers checked
- [ ] table size/growth known
- [ ] constraints/indexes/dependencies known

### Design
- [ ] risk classified
- [ ] compatibility strategy defined
- [ ] expand/migrate/contract used when necessary
- [ ] backfill strategy restartable
- [ ] lock impact understood
- [ ] external consumers considered

### Execution
- [ ] migration tested on representative data
- [ ] deployment ordering tested
- [ ] monitoring ready
- [ ] abort/resume path defined
- [ ] rollback/forward-fix path defined

### Verification
- [ ] data parity/invariants proven
- [ ] old readers/writers removed before contract
- [ ] constraints valid
- [ ] indexes valid/usable
- [ ] application health verified
- [ ] migration outcome documented

## References
- `references/expand-contract.md`
- `references/backfills.md`
- `references/locks-and-indexes.md`
- `references/rollback-and-recovery.md`
- `references/migration-risk-matrix.md`

## Review Procedure

1. Identify affected readers, writers, workers, and consumers.
2. Classify risk and reversibility.
3. Check old/new application compatibility.
4. Design expand/migrate/contract when needed.
5. Plan locks, backfill, monitoring, and recovery.
6. Verify data invariants before destructive cleanup.
7. Validate post-migration application behavior.

## Verification Checklist

- [ ] dependencies inventoried
- [ ] compatibility window understood
- [ ] risk/recovery classified
- [ ] backfill is bounded/restartable
- [ ] lock impact reviewed
- [ ] destructive step gated by evidence
- [ ] post-migration invariants verified

## Cross-Skill Routing
- For `postgresql` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
- For `deployment` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
