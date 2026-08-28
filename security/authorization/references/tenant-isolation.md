# Tenant Isolation

Tenant boundaries should be derived from trusted authenticated context.

For data access, enforce tenant scope close to the persistence boundary where practical:
`WHERE tenant_id = trustedTenantId`.

Still perform application-level authorization for role, ownership, state, and action-specific policy.

Test every route that accepts object IDs, tenant IDs, bulk inputs, exports, jobs, and admin operations.
