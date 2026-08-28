---
name: owasp
description: Apply current OWASP security guidance as a structured application/API review baseline. Use for security reviews, threat modeling, authentication, authorization, input handling, sessions, secrets, and API design.
---

# OWASP Security Review

## Use OWASP as a Baseline
Consult current OWASP project guidance and Cheat Sheet Series rather than treating this file as a frozen security standard.

## Review
- authentication
- authorization
- input validation
- output encoding
- injection
- session/token security
- cryptography
- secrets
- file uploads
- SSRF
- API security
- logging/error handling
- dependencies/configuration

## API Checklist
Use the OWASP API Security Top 10 2023 as a specific API review checklist.

## Security Claims
Do not claim "secure", "OWASP compliant", or "production safe" merely because a checklist was read. Record evidence and remaining risk.

## Verification
Use automated security tests/scanners where available, negative authorization tests, dependency checks, configuration review, and manual threat modeling for high-risk flows.
