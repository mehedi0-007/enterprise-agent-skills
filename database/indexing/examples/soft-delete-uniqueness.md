# Soft Delete + Uniqueness

Requirement:
Only active accounts must have unique email within a tenant.

Possible design:
unique partial index over `(tenant_id, normalized_email)` with predicate `deleted_at IS NULL`.

Review:
- is reuse after deletion really allowed?
- is normalization consistent?
- do all relevant queries use the same tenant/email semantics?
- does the constraint reflect the domain invariant?

The database should enforce the concurrency-sensitive invariant.
