---
name: ci-cd
description: Design, secure, validate, and review continuous integration and delivery pipelines. Use when creating or modifying CI workflows, test gates, artifact builds, deployment automation, release promotion, secrets/OIDC, workflow permissions, caching, concurrency, or supply-chain controls.
---

# CI/CD — Production Playbook

## 1. Mission

A CI/CD pipeline is production infrastructure.

Its job is to make software:
- reproducibly buildable
- automatically verifiable
- traceable to source
- securely promoted
- safely deployed
- recoverable when something fails

Do not treat CI/CD as "a YAML file that runs tests."

---

## 2. Activation

Use when:
- adding/modifying CI workflows
- adding tests/lint/typecheck/build
- building container/images/packages
- deploying staging/production
- changing workflow permissions
- configuring secrets/OIDC
- adding dependency/cache steps
- adding release automation
- reviewing supply-chain security
- adding rollback/manual approval

---

## 3. Pipeline Model

A useful pipeline:

```text
Change
  ↓
Validate
  ↓
Build
  ↓
Test
  ↓
Security checks
  ↓
Produce immutable artifact
  ↓
Verify artifact/provenance
  ↓
Deploy staging
  ↓
Validate
  ↓
Promote same artifact
  ↓
Production gates
  ↓
Deploy
  ↓
Post-deploy verification
```

Build once and promote the same artifact when practical.

Do not rebuild a separate "production" artifact from the same commit and assume it is identical.

---

## 4. Trigger Design

Choose triggers deliberately.

Common:
- pull request → validation only
- push to protected branch → integration/build
- tag/release → release pipeline
- manual dispatch → controlled operational action
- scheduled → maintenance/scanning

Do not allow untrusted pull-request code to reach production deployment paths.

---

## 5. Pull Requests From Forks / Untrusted Code

Treat PR code as attacker-controlled.

Review:
- secrets availability
- token permissions
- shell interpolation
- artifact uploads
- caches
- privileged runners
- reusable workflows

GitHub explicitly warns about script injection through attacker-controlled workflow contexts. Never interpolate untrusted values directly into shell commands without safe handling. citeturn380488search9

Never expose production credentials to ordinary PR validation.

---

## 6. Least-Privilege Workflow Permissions

Start from minimal permissions.

Example concept:

```yaml
permissions:
  contents: read
```

Then add only what jobs actually need.

Do not grant:
```text
contents: write
packages: write
deployments: write
id-token: write
```
globally when only one job requires one permission.

Split jobs so privileged operations have narrower permissions.

---

## 7. OIDC / Workload Identity

Prefer short-lived workload identity over long-lived cloud credentials when the provider supports it.

GitHub's current security guidance recommends OpenID Connect for authenticating to cloud providers and artifact attestations for build provenance. citeturn380488search9

Review:
- repository/branch/environment conditions
- audience
- cloud role scope
- production vs staging identities
- token lifetime

Do not give every workflow the ability to assume a production role.

---

## 8. Secrets

Use:
- environment/repository/org secret stores
- workload identity
- scoped credentials

Do not:
- commit secrets
- print secrets
- write them into artifacts
- expose production secrets to untrusted jobs
- put secrets in command-line arguments when the platform exposes safer mechanisms

Use `security/secrets-management` for full lifecycle design.

---

## 9. CI Stages

A typical order:

```text
format/lint
→ typecheck
→ unit tests
→ integration tests
→ build
→ security/dependency checks
→ artifact
```

Cheap deterministic checks can run early.

Do not skip critical tests just to reduce runtime.

Parallelize independent work when it does not weaken gates.

---

## 10. Build Reproducibility

Control:
- dependency lockfiles
- tool/runtime versions
- base images
- environment inputs
- build scripts

The same source + same controlled inputs should produce a predictable artifact.

Do not silently depend on:
- mutable `latest`
- current system packages
- floating package versions
- developer machine state

---

## 11. Dependency Caching

Caching can speed CI but introduces correctness/security considerations.

Cache:
- package manager directories
- compiler caches
- known build outputs

Do not cache:
- secrets
- mutable production credentials
- unsafe cross-branch state
- artifacts that can cross trust boundaries unexpectedly

Validate cache keys and scope.

A corrupted/stale cache should cause a rebuild, not a persistent broken pipeline.

---

## 12. Tests as Gates

A green pipeline should mean:
- required test classes passed
- build succeeded
- required security checks passed
- artifact was created

Do not call a workflow "CI complete" if only lint runs.

For high-risk changes add:
- integration tests
- migration checks
- security tests
- contract tests
- targeted performance checks

Use `engineering/testing-quality`.

---

## 13. Database Migration Gate

Schema changes can affect deployability.

Before deploying application code that depends on a schema change, verify migration compatibility.

For rolling deployments:
```text
expand migration
→ compatible application
→ backfill/verify
→ contract later
```

Do not make CI treat an irreversible migration as an ordinary code change with a fake rollback guarantee.

Use `database/migrations` and `production/deployment`.

---

## 14. Artifact Strategy

Prefer:
- immutable artifact
- unique version
- source commit association
- digest for container images
- build metadata/provenance

SLSA provenance provides verifiable information about where, when, and how an artifact was produced. citeturn380488search11

Do not deploy `latest` as the only artifact identity.

---

## 15. Provenance / Attestations

For higher-assurance systems, publish verifiable build provenance/attestations.

GitHub supports artifact attestations as part of its software supply-chain security guidance. citeturn380488search9

Decide what assurance level the product requires rather than blindly implementing a supply-chain framework.

---

## 16. Promotion

Prefer:

```text
build artifact A
    ↓
test A
    ↓
staging deploy A
    ↓
verify A
    ↓
production deploy A
```

instead of:

```text
build A → staging
build B → production
```

The latter can differ because dependencies/base layers/build-time inputs changed.

---

## 17. Environment Separation

Use distinct:
- secrets
- identities
- databases/resources
- deployment permissions

for:
```text
development
staging
production
```

A staging compromise should not directly expose production credentials.

---

## 18. Deployment Protection

Production should have appropriate gates for the organization's risk.

GitHub environments can require approvals, restrict deployment branches/tags, protect environment secrets, and apply deployment protection rules. citeturn380488search0turn380488search2

Use stronger gates for:
- production
- destructive migrations
- security-sensitive releases
- high-blast-radius infrastructure changes

Do not require manual approval for every low-risk change if automated verification is sufficient.

---

## 19. Deployment Concurrency

Prevent overlapping production deployments when concurrent releases could create ambiguity or inconsistent state.

GitHub supports concurrency groups for limiting simultaneous deployment workflows/jobs. citeturn380488search1

Example policy:
```text
production deployment group
→ one active deployment
```

Cancellation policy should be deliberate:
- cancel older queued deployment
- wait for current deployment
- do not cancel an already-started critical release blindly

---

## 20. Release Gates

Before production:
- artifact identified
- tests passed
- migration compatibility reviewed
- security gates passed
- required approval obtained
- target environment healthy
- rollback/forward-fix strategy known

A gate should protect against a real failure mode, not exist for ritual.

---

## 21. Deployment Health

A deployment is not complete when the process exits with code 0.

After deployment verify:
- readiness/health
- key API paths
- error rate
- latency
- background job health
- database connectivity
- migration state
- critical business flows

Coordinate with `production/observability`.

---

## 22. Rollback

Define what rollback actually means.

### Code rollback
Deploy previous immutable artifact.

### Feature rollback
Disable feature flag.

### Configuration rollback
Restore previous config.

### Database change
May not be safely reversible.

For destructive DB changes, a code rollback may be impossible or unsafe. Use forward fixes/data recovery plans.

Do not provide a "rollback" button that only redeploys old code when the schema has already changed incompatibly.

---

## 23. Manual vs Automatic Rollback

Automatic rollback is appropriate when:
- health signals are reliable
- rollback is safe
- failure is detectable
- rollback itself does not increase damage

Manual/forward fix may be safer when:
- data migrations are irreversible
- metrics are ambiguous
- partial business side effects occurred

Do not automate rollback merely because the platform supports it.

---

## 24. Failure Containment

A pipeline failure should fail closed.

Examples:
- missing production environment approval → no deployment
- artifact missing → no deployment
- security gate failed → no deployment
- migration compatibility check failed → no deployment
- target unhealthy → stop promotion

Avoid "best effort" production deployment logic that continues after critical checks fail.

---

## 25. Workflow Reuse

Reusable workflows/components can reduce duplication.

Reuse when:
- behavior is stable
- permissions are understood
- inputs/outputs are explicit

Avoid giant reusable workflows with dozens of hidden assumptions.

A shared workflow is effectively a platform API: changes can affect many repositories.

---

## 26. Third-Party Actions

Third-party actions execute code in your CI environment.

Review:
- publisher/source
- version pinning policy
- permissions
- secrets exposure
- maintenance
- required trust

Prefer well-known/trusted actions and pin versions according to organizational policy.

Do not blindly copy workflows from the internet.

---

## 27. Runner Security

Review:
- hosted vs self-hosted
- isolation
- network access
- cached credentials
- workspace cleanup
- privileged tools

Self-hosted runners can have persistent state and broader network access; treat them as high-trust infrastructure.

Do not send untrusted PR code to a powerful persistent self-hosted runner.

---

## 28. Build Matrix

Use matrices when multiple:
- runtimes
- operating systems
- dependency versions

must be supported.

Avoid combinatorial explosion.

Define the supported compatibility matrix explicitly.

---

## 29. Flaky CI

Treat flaky tests/workflows as engineering defects.

Do not hide flakiness with:
```text
retry 5 times
```

without understanding why.

Retries may be acceptable for genuinely transient infrastructure operations, but test flakiness needs diagnosis.

---

## 30. Notifications / Ownership

A failed production deployment needs an owner.

Useful metadata:
- service
- commit
- environment
- deployment version
- workflow/run ID
- failure phase

Avoid notification spam; alert on failures requiring action.

---

## 31. Security Testing

CI should catch common classes relevant to the project:
- dependency vulnerabilities
- secret leaks
- container/image vulnerabilities
- static analysis findings
- authorization/security tests
- unsafe migrations
- policy violations

Choose tools by actual threat/model and false-positive cost.

A scanner result should trigger review/remediation according to severity, not automatic "secure" status.

---

## 32. CI/CD Review Procedure

For a pipeline ask:

1. What events can trigger it?
2. Can attacker-controlled code execute?
3. What permissions does each job have?
4. Which jobs access secrets?
5. Can PR code reach production?
6. Are cloud credentials short-lived?
7. Is the artifact immutable/traceable?
8. Are migrations compatible?
9. Are tests meaningful?
10. Can two deployments race?
11. What production gates exist?
12. What happens after deployment?
13. What is the actual rollback/fix path?
14. What evidence proves success?

---

## 33. Anti-Patterns

### All-Powerful Workflow
One token/credential can build, release, and administer everything.

### Secrets on PRs
Untrusted code gets production credentials.

### Build Twice
Different artifacts for staging and production.

### `latest`
No immutable release identity.

### Retry Everything
Transient retry logic hides actual defects.

### Manual Approval Everywhere
Human gate replaces automated evidence.

### No Post-Deploy Validation
Green job mistaken for healthy release.

### Fake Rollback
Old code cannot run against new/destructive schema.

### Global Write Permissions
All jobs receive broad repository/token permissions.

### Unreviewed Third-Party Actions
Arbitrary code runs with CI privileges.

### Cache Trust
Cached state treated as authoritative and secure.

### Self-Hosted Runner for Untrusted PRs
Persistent high-trust machine executes attacker-controlled code.

---

## 34. Verification Checklist

- [ ] triggers intentional
- [ ] untrusted PR execution isolated
- [ ] permissions minimal
- [ ] secrets scoped
- [ ] OIDC/workload identity considered
- [ ] tests meaningful and risk-based
- [ ] builds reproducible
- [ ] caches scoped/safe
- [ ] artifact immutable/traceable
- [ ] provenance/attestation considered
- [ ] same artifact promoted where practical
- [ ] environments separated
- [ ] production protection configured
- [ ] deployment concurrency defined
- [ ] migrations gated
- [ ] post-deploy health verified
- [ ] rollback/forward-fix defined
- [ ] third-party actions reviewed
- [ ] runner trust model appropriate
- [ ] failures stop unsafe promotion
- [ ] ownership/notifications clear

## References
- `references/workflow-security.md`
- `references/artifacts-and-provenance.md`
- `references/deployment-gates.md`
- `references/retry-and-flakiness.md`
- `references/runner-trust.md`

## Review Procedure

1. Identify every trigger and trust boundary.
2. Inspect job permissions and secret access.
3. Verify tests/build/security gates are meaningful.
4. Verify artifact identity and promotion behavior.
5. Review migration/environment/deployment compatibility.
6. Review concurrency, runner trust, and third-party action risks.
7. Verify post-deploy validation and recovery paths.

## Cross-Skill Routing
For container build/runtime details, coordinate with `production/docker`.
For credential lifecycle and workflow secret exposure, coordinate with `security/secrets-management`.
For live rollout and post-deploy behavior, coordinate with `production/deployment`.
