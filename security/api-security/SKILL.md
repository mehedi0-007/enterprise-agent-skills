---
name: api-security
description: Threat-model and review API endpoints for common security failures. Use when creating or modifying APIs, webhooks, file endpoints, external integrations, or sensitive business flows.
---

# API Security

## Threat Model First
For a new endpoint identify:
- attacker-controlled inputs
- authenticated identity
- authorization boundary
- sensitive data
- expensive operations
- external destinations
- state changes
- replay/automation opportunities
- trust boundaries

## OWASP API Risks
Use the OWASP API Security Top 10 as a review checklist, especially:
- broken object-level authorization
- broken authentication
- broken object property-level authorization
- unrestricted resource consumption
- broken function-level authorization
- unrestricted access to sensitive business flows
- SSRF
- security misconfiguration
- improper inventory management
- unsafe consumption of APIs

OWASP highlights authorization as a major recurring API security challenge.

## Input
Validate:
- body
- path parameters
- query parameters
- headers
- content type
- file metadata
- webhook payloads

Use allow-lists where practical.

## Resource Consumption
Bound:
- request body size
- pagination limits
- upload size
- expensive query parameters
- batch sizes
- polling frequency
- authentication attempts
- expensive business operations

Use rate limiting and quotas appropriate to the business risk.

## Object Authorization
Never assume an authenticated user may access an object just because they know its ID.
Enforce ownership/relationship/permission server-side.

## Property Authorization
Do not mass-assign security-sensitive properties such as:
- role
- ownerId
- tenantId
- verified
- accountStatus
- price
unless the operation explicitly authorizes those changes.

## SSRF
When accepting URLs or making server-side requests:
- restrict allowed schemes
- validate destinations
- avoid unrestricted private/internal address access
- consider redirects
- use network-level egress controls where possible
- do not rely solely on hostname string checks

## Webhooks
Verify authenticity/signature where supported.
Handle replay and duplicate delivery.
Make processing idempotent.
Do not trust webhook fields as authorization decisions without validating their source and context.

## API Inventory
Know which endpoints, versions, internal routes, admin routes, and deprecated versions are deployed. Remove or protect forgotten endpoints.

## Verification
Review both positive and negative authorization cases and abuse scenarios. Test limits and malformed input, not only happy paths.
