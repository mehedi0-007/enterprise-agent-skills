---
name: ci-cd
description: Design reliable and secure continuous integration and deployment pipelines. Use when adding GitHub Actions or other CI/CD workflows, build/test automation, deployment gates, artifact handling, or release automation.
---

# CI/CD

## Mission
Make every change reproducibly buildable, testable, auditable, and deployable.

## CI Pipeline
A typical pipeline should progressively gate:
1. formatting/lint
2. typecheck/build
3. unit tests
4. integration tests
5. security/dependency checks
6. artifact creation
7. deployment eligibility

GitHub describes CI as continuously building/testing changes and commonly includes linting, security checks, coverage, and functional tests. citeturn556704search12

## Fail Fast, But Not Blindly
Run cheap deterministic checks early.
Do not skip critical integration/security checks merely to make CI faster.

## Reproducibility
Pin/lock:
- dependency versions
- tool versions where appropriate
- build inputs
- deployment artifact identity

Prefer building once and promoting the same artifact across environments.

## Secrets and Permissions
Use least privilege.
Do not expose secrets to untrusted pull-request code.
GitHub recommends secure secret handling and supports OIDC for short-lived cloud authentication. citeturn556704search0turn556704search8

Avoid embedding untrusted PR content directly into shell commands; GitHub explicitly warns about script injection through attacker-controlled workflow context. citeturn556704search16

## Third-Party Actions
Pin trusted actions/versions according to the project's supply-chain policy.
Review permissions and avoid unnecessarily broad `GITHUB_TOKEN` access.

## Deployment Gates
Before deployment verify:
- artifact exists
- tests passed
- required approvals/gates passed
- migrations are compatible
- target environment configuration is present
- rollback/forward-fix plan exists for risky changes

## Artifacts
Treat build artifacts as immutable release inputs.
GitHub provides artifact attestations to establish software provenance. citeturn556704search0

## Verification
Test workflows on representative branches/events, inspect permissions, verify secrets are not leaked, and confirm deployment failures leave the environment recoverable.
