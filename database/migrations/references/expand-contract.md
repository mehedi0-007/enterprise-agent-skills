# Expand / Migrate / Contract

Use staged compatibility when old/new application versions can overlap.

Example rename:
1. Add new column.
2. Deploy compatible read/write code.
3. Backfill.
4. Verify parity.
5. Switch reads.
6. Stop old writes.
7. Prove old readers are gone.
8. Contract/drop later.

Do not compress these into one migration if multiple application deployments are required.
