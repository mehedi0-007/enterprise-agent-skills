---
name: migrations
description: Design safe production database schema and data migrations under rolling deployments and existing traffic. Use for columns, constraints, indexes, data backfills, renames, drops, and schema evolution.
---

# Database Migrations

## Compatibility Model
Assume old and new application versions may coexist during deployment unless the deployment system guarantees otherwise.

## Expand and Contract
For breaking changes:
1. Add compatible structure.
2. Deploy code that understands the new structure.
3. Backfill/transform data.
4. Switch reads/writes.
5. Remove old structure in a later change.

## Large Tables
Consider:
- lock duration
- table rewrite behavior
- index build impact
- WAL/replication
- statement timeouts
- batch size
- application traffic

## Backfills
Make large backfills:
- restartable
- observable
- bounded
- idempotent or checkpointed
- safe under concurrent application traffic

## Constraints
Before adding NOT NULL/UNIQUE/FK:
- inspect existing violations
- clean/backfill
- understand validation/locking impact
- deploy compatible application behavior

## Renames/Drops
Treat destructive changes as multi-step migrations when old application versions may still reference the object.

## Rollback
Data transformations may be irreversible. Prefer a tested forward-fix strategy when rollback cannot safely reconstruct data.

## Verification
Test against representative data and deployment order. Document lock/performance implications and irreversible operations.
