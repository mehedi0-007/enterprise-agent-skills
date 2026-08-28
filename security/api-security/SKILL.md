---
name: api-security
description: Threat-model and review API endpoints for authorization, authentication, resource abuse, SSRF, unsafe input, sensitive business flows, and inventory/configuration risks. Use for new or modified APIs and webhooks.
---

# API Security

## Threat Model
Identify:
- attacker-controlled inputs
- trust boundaries
- sensitive data
- state changes
- expensive operations
- external destinations
- retry/replay opportunities
- authorization object and tenant

## OWASP API Risks
Review against the OWASP API Security Top 10 2023:
- BOLA
- broken authentication
- broken object property authorization
- unrestricted resource consumption
- broken function authorization
- sensitive business-flow abuse
- SSRF
- security misconfiguration
- improper inventory management
- unsafe API consumption

## Limits
Bound request body, file uploads, pagination, batch operations, expensive queries, authentication attempts, and sensitive business flows.

## SSRF
For server-side URLs:
- allow only required schemes
- validate destinations
- consider redirects
- restrict private/internal network access
- apply network egress controls where possible

## Webhooks
Verify signatures/authenticity, handle replay/duplicates, make processing idempotent, and define retry semantics.

## Property Exposure
Do not mass-assign fields such as role, owner, tenant, status, verification, or price unless explicitly authorized.

## Verification
Test abuse and negative authorization cases, not only valid requests.
