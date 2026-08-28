---
name: secrets-management
description: Design, store, rotate, revoke, audit, and use application secrets safely. Use for API keys, database credentials, signing keys, certificates, tokens, CI/CD credentials, and environment configuration.
---

# Secrets Management

## Goal
Minimize secret exposure, scope, lifetime, and blast radius.

## Never
Do not:
- commit secrets to source control
- hardcode production credentials
- log raw secrets
- expose secrets in API responses
- put secrets in client-side bundles
- share one credential across unrelated systems when avoidable

## Centralize
Use an appropriate secret-management mechanism for the environment:
- managed cloud secret store
- dedicated secret manager
- CI/CD secret store
- short-lived workload identity where available

Choose based on operational context; do not introduce a heavyweight secret manager without a real need.

## Least Privilege
Each service/account should receive only the secrets and permissions it needs.
Do not give every application access to every environment secret.

## Lifecycle
Treat every secret as having:
1. creation
2. provisioning
3. use
4. rotation
5. revocation
6. expiration/decommissioning

Prefer automated rotation where practical.

## Environment Separation
Production credentials must not be reused casually in development/test.
Use separate accounts/keys and minimum permissions.

## CI/CD
Ensure:
- secrets are injected securely
- pipeline output cannot reveal them
- forks/PRs cannot unexpectedly access privileged secrets
- service accounts have narrowly scoped permissions
- secret access is auditable

## Tokens and Signing Keys
Define:
- issuer
- audience/scope
- lifetime
- rotation
- revocation/rollover strategy
- old-key compatibility window where required

## Detection
Use secret scanning and review tools where available.
If a secret is exposed, treat it as compromised:
1. revoke/rotate
2. assess blast radius
3. inspect access logs
4. remove the secret from source/history where appropriate
5. document the incident

## Verification
Review:
- source control
- logs
- CI/CD configuration
- runtime environment
- client bundles
- error messages
- monitoring
for accidental secret exposure.
