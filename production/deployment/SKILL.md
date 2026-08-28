---
name: deployment
description: Plan and execute safe application deployments, migrations, rollouts, rollback, and release validation. Use when shipping changes to staging/production or designing a deployment strategy.
---

# Deployment

## Mission
Release changes without unnecessary downtime, data corruption, or ambiguous recovery.

## Before Deployment
Confirm:
- artifact/version
- tests and required gates
- configuration/secrets
- database migration compatibility
- dependency changes
- observability
- rollback or forward-fix plan
- ownership/on-call context for risky releases

## Deployment Strategy
Choose based on risk and infrastructure:
- rolling
- blue/green
- canary
- feature flag
- maintenance window

For Kubernetes Deployments, rolling updates can be controlled with `maxUnavailable` and `maxSurge`; readiness should determine when new Pods are considered available. citeturn556704search7

## Database Compatibility
Use expand/contract techniques for schema changes when old and new application versions may overlap.
Deploy application compatibility before destructive schema cleanup.

## Health
A deployment is not successful merely because the process starts.
Verify:
- readiness
- critical request path
- dependency connectivity
- error rate
- latency
- background workers
- migrations

## Rollback
Before deploying, know whether rollback means:
- redeploy previous artifact
- disable feature flag
- revert configuration
- restore data
- apply a forward fix

Data migrations may be irreversible; do not assume code rollback can safely reverse them.

## Post-Deploy Validation
Compare key metrics against baseline.
Look for:
- error spikes
- latency regression
- saturation
- failed jobs
- database issues
- user-impacting errors

## Verification
Record deployment version, migration state, validation result, and any known limitations.
