# Workflow Security

Treat workflow definitions as privileged infrastructure.

## Review
- minimal token permissions
- untrusted input never interpreted as shell
- pull requests from forks have restricted secrets
- third-party actions are trusted/pinned
- deployment credentials use least privilege
- production deployment requires intended gates
- artifacts are traceable to source

GitHub explicitly documents script-injection risks for attacker-controlled contexts and recommends secure workflow practices, secrets protection, OIDC, and artifact provenance.
