---
name: authentication
description: Design and review secure authentication, sessions, passwords, OTP, refresh tokens, MFA, identity providers, and account recovery. Use whenever identity establishment or credential lifecycle changes.
---

# Authentication

## Separate AuthN and AuthZ
Authentication establishes identity. Authorization decides access.

## Passwords
- Never store plaintext/reversible passwords.
- Use a maintained password-hashing algorithm/library.
- Rate-limit credential attacks.
- Avoid user enumeration through distinguishable login/recovery responses.

## Sessions/Tokens
Define:
- lifetime
- renewal
- revocation
- storage/transport
- audience/scope
- rotation
- replay behavior
- logout behavior

Treat bearer tokens as credentials.

## Refresh Tokens
Use unpredictable tokens. Define expiration, rotation/reuse detection where appropriate, revocation, session ownership, and safe storage. Never log raw tokens.

## OTP
OTP flows need:
- secure generation
- short expiration
- single use
- attempt/resend limits
- rate limiting
- replay protection
- enumeration resistance
- safe persistence

## Account Recovery
Recovery must be protected as strongly as login. Revoke/expire recovery artifacts after use.

## External Identity
Validate issuer, audience, signature, lifetime, and required claims. Decoding a token is not validation.

## Verification
Test expiry, replay, revocation, concurrent refresh, brute force, enumeration, logout, recovery, and privilege changes.
