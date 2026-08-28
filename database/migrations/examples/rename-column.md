# Safe Rename

Requirement:
`users.name` → `users.full_name`

Unsafe:
```sql
ALTER TABLE users RENAME COLUMN name TO full_name;
```
followed by rolling application deployment.

Safer:
1. Add `full_name`.
2. Deploy code that writes both and can read either.
3. Backfill.
4. Verify parity.
5. Switch reads to `full_name`.
6. Remove writes to `name`.
7. Prove old readers are gone.
8. Drop `name` in a later contract migration.
