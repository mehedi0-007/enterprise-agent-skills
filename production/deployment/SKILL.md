---
name: deployment
description: Design, plan, execute, review, and verify safe production deployments. Use when releasing application changes, database changes, infrastructure changes, rolling/canary/blue-green deployments, feature-flag rollouts, rollback, forward-fixes, or post-deploy validation.
---

# Deployment — Production Playbook

## 1. Mission

A deployment changes a live system while users, jobs, integrations, and old application versions may still be active.

The goal is:
- controlled change
- compatibility
- limited blast radius
- observable progress
- safe recovery
- verified outcome

A successful deployment is not:
```text
deployment command exited 0
```

It is:
```text
new version is running
+
system is healthy
+
critical behavior works
+
data/contracts remain correct
```

---

## 2. Activation

Use when:
- deploying application code
- changing database schema
- changing infrastructure/runtime
- enabling a major feature
- changing service dependencies
- performing canary/rolling/blue-green rollout
- deciding rollback strategy
- performing incident-driven release
- validating a release

Coordinate with:
- `production/ci-cd`
- `production/observability`
- `production/docker`
- `database/migrations`
- `backend/transactions`
- `backend/concurrency`

---

## 3. Deployment Classification

Before choosing strategy, classify:

### Change Scope
- application
- database schema
- data/backfill
- infrastructure
- configuration
- security/credentials

### Blast Radius
- single component
- single tenant
- region
- entire production

### Reversibility
- easily reversible
- code rollback only
- feature disable
- forward-fix
- data recovery required

### Compatibility
- old/new versions can coexist?
- schema compatible?
- API contract compatible?
- event consumers compatible?

---

## 4. Pre-Flight

Confirm:
- exact artifact/version
- source commit
- migration compatibility
- environment/configuration
- secrets/credentials
- dependency availability
- health/observability
- rollback/forward-fix path
- ownership/on-call
- deployment window/risk

Do not deploy first and discover the rollback plan afterward.

---

## 5. Artifact Identity

Deploy an immutable artifact.

For containers prefer:
```text
image digest
```

rather than:
```text
latest
```

The deployment record should identify:
- source commit
- artifact/version
- image/package digest where applicable
- migration state

The exact artifact that passed validation should be the artifact promoted through environments where practical.

---

## 6. Deployment Strategy Selection

### Rolling
Replace instances gradually.

Use when:
- old/new compatibility is strong
- multiple instances exist
- brief overlap is acceptable

Risks:
- old/new versions coexist
- incompatible schema/API changes can fail

### Blue/Green
Maintain two environments and switch traffic.

Use when:
- fast traffic cutover/rollback is valuable
- duplicate infrastructure cost is acceptable

Risks:
- database compatibility still matters
- external side effects/data changes may not be reversible by traffic switch

### Canary
Expose a small percentage of traffic first.

Use when:
- production regression detection is valuable
- traffic can be controlled
- observability is strong

Risks:
- low traffic may not expose rare failures
- both versions may coexist

### Feature Flag
Deploy code separately from user exposure.

Use when:
- behavior can be gated
- gradual exposure matters
- quick disable is valuable

Do not let flags become permanent hidden architecture.

---

## 7. Decision Matrix

| Situation | Often useful |
|---|---|
| Low-risk compatible app change | Rolling |
| High-risk user behavior change | Canary + feature flag |
| Need fast traffic switch | Blue/green |
| DB migration with old/new overlap | Expand/contract + rolling |
| Large irreversible behavior | Feature flag/canary + strong validation |
| Single-instance simple deployment | Controlled replacement/maintenance window |

This is a heuristic. Use the actual infrastructure and failure modes.

---

## 8. Database Compatibility

For rolling deployments:

```text
old application
      +
new application
      ↓
database must support both
```

Prefer:
```text
expand
→ compatible app
→ backfill
→ verify
→ switch
→ contract later
```

Do not deploy code that reads a column before the migration that creates it is safely available.

Do not drop a field while old instances/workers may still read it.

Use `database/migrations`.

---

## 9. Event/API Compatibility

During rolling releases:
- old/new clients may coexist
- old/new services may coexist
- old/new event consumers may coexist

Prefer additive changes first.

Avoid:
- immediate removal/rename
- changing field type in place
- changing event meaning
- changing required request fields
without compatibility strategy.

---

## 10. Health Gates

Before traffic:
- readiness passes
- startup completes
- dependencies are usable as required

During rollout:
- error rate
- latency
- saturation
- key business outcomes

After rollout:
- background jobs
- queues
- scheduled work
- database behavior
- external integrations

Use `production/observability`.

---

## 11. Canary Verification

Canary should define:
- percentage/target audience
- observation window
- success criteria
- abort criteria
- promotion condition

Example:

```text
5% traffic
→ observe 10 min
→ compare errors/latency/business metric
→ promote to 25%
→ observe
→ promote
```

Do not choose exact thresholds arbitrarily. Use service baselines/SLOs and known failure modes.

---

## 12. Rolling Deployment Risks

During rolling updates:
- load shifts between versions
- schema compatibility matters
- connection pools change
- cache behavior can shift
- event producers/consumers can overlap

A change that works with 100% new code may fail when 50% is old and 50% is new.

Test overlap behavior where relevant.

---

## 13. Blue/Green Risks

Switching traffic does not undo:
- database writes
- sent emails
- payments
- published events
- external resource creation

Blue/green is primarily a traffic/version technique.

Do not advertise blue/green as a universal rollback mechanism.

---

## 14. Feature Flags

Feature flags can reduce rollout risk.

Define:
- default state
- target audience
- rollout percentage
- authorization/tenant scope
- expiry/removal date
- metrics
- emergency disable path

Do not allow flags to bypass:
- authorization
- data validation
- security boundaries

Avoid nested flag combinations that are impossible to reason about.

---

## 15. Rollback Decision

Before rollback ask:

```text
Is failure caused by code?
   ↓
Can previous artifact safely run with current schema/data?
   ↓
Are external side effects already performed?
   ↓
Would rollback increase inconsistency?
```

Rollback code when safe.

Use feature disable when behavior can be isolated.

Use forward-fix when schema/data changes make old code unsafe.

Use data recovery when information was destroyed and no forward fix can reconstruct it.

---

## 16. Forward Fix

A forward fix is often safer than rollback when:
- migration is irreversible
- old code cannot safely operate on new schema
- external side effects already occurred
- data transformation has changed state

Do not mechanically revert commits during a production incident.

---

## 17. Post-Deploy Verification

Verify:
- health/readiness
- error rate
- latency
- resource saturation
- critical API workflows
- authentication/authorization
- database queries/locks
- queue depth/worker health
- external integrations
- important business outcomes

Compare to baseline, not only absolute thresholds.

---

## 18. Smoke Tests

Smoke tests should represent critical paths.

Examples:
- login
- create core resource
- read core resource
- update core resource
- critical payment workflow
- background job completion
- upload/download

Keep smoke tests deterministic and safe.

Do not make a production smoke test create irreversible real-world side effects unless the test is specifically designed and isolated for that purpose.

---

## 19. Deployment Monitoring Window

High-risk releases need an explicit observation period.

Monitor:
- new errors
- latency regressions
- dependency failures
- job retries
- customer-impact metrics

Do not declare success immediately after rollout if delayed/background failures may appear later.

---

## 20. Database and Connection Effects

A deployment can change:
- query patterns
- connection pool demand
- locks
- cache hit rate
- migration load

Review these after release.

A service can be healthy while the database is degrading.

---

## 21. Rollback Testing

A rollback plan is only credible if it has been tested or strongly verified.

Where practical:
- practice previous-artifact deployment
- verify schema compatibility
- verify config restoration
- verify flag disable
- verify health after rollback

Do not discover during a major incident that the old artifact no longer starts.

---

## 22. Deployment Record

For important releases retain:
- what changed
- who/which pipeline deployed
- artifact identity
- migration version
- start/end
- strategy
- validation result
- rollback/fix outcome

This supports incident investigation and accountability.

---

## 23. Incident During Deployment

If metrics degrade:

```text
stop promotion
   ↓
scope impact
   ↓
compare canary/current vs baseline
   ↓
mitigate
   ↓
decide rollback / disable / forward-fix
   ↓
verify recovery
```

Do not continue promoting simply because the deployment pipeline has already started.

---

## 24. Multi-Region / Multi-Cluster

For distributed deployments, define:
- rollout order
- traffic routing
- data replication dependencies
- regional health gates
- rollback scope
- capacity during partial rollout

Do not assume every region can be independently rolled back if schema/data is shared globally.

---

## 25. Configuration Changes

Configuration can be as risky as code.

Review:
- validation
- secret/credential changes
- default values
- feature flags
- timeout changes
- connection pool settings
- dependency endpoints

Treat high-risk config changes with the same observability and rollback discipline as code.

---

## 26. Security-Sensitive Deployments

For changes to:
- authentication
- authorization
- secret keys
- payment
- data exports
- tenant boundaries

use stronger validation/gates.

Do not optimize deployment speed by removing critical security checks.

---

## 27. Review Procedure

For a release ask:

1. What exactly is changing?
2. What is the blast radius?
3. Can old/new versions overlap safely?
4. Is the artifact immutable?
5. Are migrations compatible?
6. Which deployment strategy fits the risk?
7. What are the health gates?
8. What metrics/business signals determine success?
9. What is the abort condition?
10. What is the recovery method?
11. Can rollback really work?
12. What external side effects have happened?
13. How long will we monitor?
14. How will we know the release is complete?

---

## 28. Anti-Patterns

### Deploy and Hope
No pre-flight/recovery design.

### Latest Tag
Mutable artifact.

### Rollback = Git Revert
Ignores schema/data/external side effects.

### Blue/Green = Universal Rollback
Traffic switch cannot undo external effects.

### Canary Without Observability
No evidence for promotion.

### Full Rollout Before Validation
Entire production exposed immediately.

### Migration Coupled to Startup
Every replica attempts schema change.

### Permanent Feature Flags
Hidden complexity accumulates.

### Success = Process Started
No post-deploy validation.

### Ignore Old/New Overlap
Rolling deployment behaves like atomic replacement in developer's mental model.

---

## 29. Verification Checklist

- [ ] change scope classified
- [ ] blast radius understood
- [ ] immutable artifact identified
- [ ] pre-flight completed
- [ ] migration compatibility verified
- [ ] deployment strategy justified
- [ ] health gates defined
- [ ] canary criteria defined where used
- [ ] feature flags scoped/temporary
- [ ] rollback vs forward-fix decision made
- [ ] external side effects considered
- [ ] post-deploy smoke tests run
- [ ] metrics/business outcomes monitored
- [ ] observation window defined
- [ ] deployment record captured

## References
- `references/strategy-selection.md`
- `references/rollback.md`
- `references/post-deploy.md`
- `references/feature-flags.md`
- `references/database-compatibility.md`
