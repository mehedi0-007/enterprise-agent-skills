---
name: migrations
description: Design safe, repeatable database schema/data migrations for production systems. Use whenever changing tables, constraints, indexes, columns, data shape, or database objects.
---

# Database Migrations

## Goal
Make schema changes safe under existing application traffic and deploy ordering.

## Compatibility First
Assume old and new application versions may overlap during deployment.

Prefer an expand-and-contract approach for breaking changes:
1. add new structure compatibly
2. deploy code that can use both where needed
3. backfill/transform data
4. switch reads/writes
5. remove old structure later

Do not rename/drop a heavily used column as part of a single blind deploy unless the environment guarantees no old readers/writers.

## Adding Columns
For existing large tables:
- determine whether a default/constraint causes a rewrite or long lock
- consider nullable/additive deployment first
- backfill in controlled batches when appropriate
- add stronger constraints after data is compliant

## Indexes
Consider whether index creation can block application traffic and whether online/concurrent techniques are appropriate for the deployment environment.

## Data Backfills
Backfills should be:
- restartable
- bounded
- observable
- safe to rerun or checkpointed
- designed around lock/transaction duration

Avoid one enormous transaction for millions of rows when it can create unacceptable lock, WAL, timeout, or replication pressure.

## Constraints
Before adding NOT NULL, UNIQUE, or foreign-key constraints:
- check existing data
- plan cleanup/backfill
- understand validation/locking impact
- ensure application behavior is compatible

## Rollback
A migration rollback is not always simply "drop what was added". Data transformations can be irreversible.

Define:
- what can be reversed
- what requires a forward fix
- backup/recovery expectations
- application rollback compatibility

## Verification
For every migration:
- test against representative schema/data
- test deployment order
- verify performance/locking implications
- verify application compatibility
- document irreversible operations
