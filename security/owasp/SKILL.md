---
name: owasp
description: Use OWASP guidance as a security review framework for application and API development. Use when reviewing authentication, authorization, input handling, sessions, secrets, API endpoints, or production security.
---

# OWASP Security Review

## Purpose
Use recognized OWASP guidance as a structured security baseline, then adapt it to the application's actual threat model.

## Core Review Areas
At minimum consider:
- authentication
- authorization
- input validation
- output encoding
- session/token security
- cryptography
- secrets management
- API security
- file uploads
- SSRF
- injection
- security logging
- dependency/configuration security
- secure error handling

## API Review
Use OWASP API Security Top 10 (2023) as a checklist:
1. Broken Object Level Authorization
2. Broken Authentication
3. Broken Object Property Level Authorization
4. Unrestricted Resource Consumption
5. Broken Function Level Authorization
6. Unrestricted Access to Sensitive Business Flows
7. Server-Side Request Forgery
8. Security Misconfiguration
9. Improper Inventory Management
10. Unsafe Consumption of APIs

## Secure Defaults
Prefer:
- deny by default
- least privilege
- server-side enforcement
- explicit allow-lists
- safe failure
- minimal data exposure

## Verification
Security claims require evidence:
- automated tests
- negative authorization tests
- dependency/security scanning where available
- configuration review
- manual threat-model review for high-risk flows

Do not claim "OWASP compliant" merely because this checklist was consulted.

## Sources
Use current OWASP project guidance and the OWASP Cheat Sheet Series as primary references.
