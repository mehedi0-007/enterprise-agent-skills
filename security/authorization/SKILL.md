---
name: authorization
description: Design and review server-side access control, RBAC, ABAC, ownership, multi-tenancy, and privileged operations. Use whenever an operation exposes or changes protected data/state.
---

# Authorization

## Core Rule
Every protected operation must establish that the current principal may perform that operation on that resource in that context.

## Never Trust Client Controls
Hidden/disabled buttons and frontend route guards are UX, not security.

## Object-Level Authorization
For `/orders/:id`, authentication is not enough. Verify access to that specific order. Prevent IDOR/BOLA.

## Function-Level Authorization
Privileged actions need explicit permission checks.

## Multi-Tenancy
Tenant scope must be derived from trusted authenticated context and enforced in queries/operations. Do not trust arbitrary client-supplied tenant IDs.

## Least Privilege
Prefer the smallest permission set. Deny by default when policy is missing/unknown.

## Property-Level Authorization
A user may access a resource but not every field or mutation.

## Policy Model
Use the simplest model that expresses the actual policy:
- ownership
- RBAC
- ABAC
- relationship-based access

Do not introduce a policy engine without a policy complexity that justifies it.

## Verification
Test anonymous, unauthorized, cross-user, cross-tenant, horizontal escalation, vertical escalation, guessed IDs, privileged operations, and stale-permission cases.
