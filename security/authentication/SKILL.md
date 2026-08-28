---
name: authentication
description: Design and review secure user and service authentication. Use for login, registration, password changes, OTP, sessions, JWTs, refresh tokens, MFA, identity providers, and account recovery.
---

# Authentication

## Goal
Establish identity securely while minimizing credential exposure and session/token risk.

## Separate Authentication From Authorization
Authentication answers "Who are you?"
Authorization answers "Are you allowed to do this?"
Never treat a valid login as permission to access every resource.

## Passwords
- Never store plaintext or reversible passwords.
- Use a modern password-hashing algorithm supported by the platform/library.
- Do not invent cryptographic algorithms.
- Apply appropriate password policy without unnecessarily harming usability.
- Protect login and recovery flows against brute force and enumeration.

## Sessions and Tokens
For every session/token design, define:
- lifetime
- renewal/refresh
- revocation
- storage
- transport
- scope/audience
- rotation
- replay behavior
- logout behavior

Bearer tokens must be treated as credentials.

For browser applications, prefer secure cookie/session patterns when appropriate; if tokens are used, understand the XSS/CSRF tradeoffs before choosing storage.

## Refresh Tokens
For refresh-token systems:
- use sufficiently unpredictable tokens
- define expiration
- consider rotation
- detect/revoke reuse where appropriate
- bind sessions to a manageable device/session record when required
- do not log raw tokens

## OTP / Recovery Codes
OTP and recovery flows should define:
- cryptographically secure generation
- short expiration
- single use
- attempt limits
- resend limits
- rate limiting
- replay protection
- enumeration resistance
- safe storage (never plaintext when persistence is required)

## MFA
Treat each factor as a credential with its own lifecycle, recovery, and revocation considerations.

## External Identity Providers
Validate issuer, audience, signature, token lifetime, and required claims according to the provider/protocol. Do not trust decoded token contents without cryptographic validation.

## Account Recovery
Recovery can be as powerful as login. Apply equivalent protection:
- rate limits
- anti-enumeration behavior
- short-lived recovery artifacts
- revocation after use
- audit events for sensitive changes

## Verification
Test:
- invalid credentials
- expired credentials
- revoked sessions/tokens
- replay
- brute-force/rate limits
- enumeration resistance
- logout/revocation
- recovery
- concurrent refresh
- privilege changes after authentication
