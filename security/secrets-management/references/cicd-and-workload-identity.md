# CI/CD and Workload Identity

Prefer short-lived workload identity over static cloud credentials where supported.

Review:
- workflow permissions
- branch/environment protections
- PR/fork secrets
- deployment scope
- artifact access
- logs

GitHub OIDC can issue short-lived cloud credentials tied to workflow identity and conditions, reducing stored long-lived cloud secrets.
