# Optimistic UI

Use when the expected result can be safely reversed.

Steps:
1. optimistic local change
2. send server request
3. confirm
4. reconcile/rollback on failure
5. ignore stale responses

Avoid for irreversible/high-risk operations unless product semantics explicitly support it.
