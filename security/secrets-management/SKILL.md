---
name: secrets-management
description: Safely provision, use, rotate, revoke, and audit application secrets. Use for API keys, database credentials, signing keys, certificates, CI/CD credentials, and runtime secrets.
---

# Secrets Management

## Never
- commit secrets
- hardcode production credentials
- log raw secrets
- expose secrets to browser bundles
- return secrets through APIs
- reuse production credentials casually in development

## Lifecycle
Every secret needs:
creation → provisioning → use → rotation → revocation → decommissioning

## Least Privilege
Scope credentials to the smallest workload/resource/environment.

## Storage
Prefer the environment's appropriate secret store or short-lived workload identity. Do not introduce complex infrastructure without operational justification.

## CI/CD
Protect secrets from:
- PRs/forks
- build logs
- artifacts
- shell tracing
- overly broad service accounts

## Exposure Response
If a secret is exposed:
1. revoke/rotate
2. assess blast radius
3. inspect access logs
4. remove exposure from source/history where appropriate
5. document remediation

## Verification
Review source, logs, CI/CD, runtime environment, client bundles, and error paths for leakage.
