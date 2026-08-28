---
name: docker
description: Build secure, small, reproducible production container images and runtime configurations. Use when creating or reviewing Dockerfiles, Compose configurations, container images, or containerized deployments.
---

# Docker

## Mission
Produce containers that are reproducible, minimal, secure, observable, and easy to deploy.

## Image Design
Prefer:
- multi-stage builds when build tooling is not needed at runtime
- minimal trusted base images
- pinned/controlled versions where reproducibility matters
- non-root runtime users when practical
- explicit working directory
- only required files in the runtime image

Docker recommends keeping images clean/modular and using build cache deliberately. citeturn556704search15

## Build Context
Avoid copying:
- `.git`
- local dependencies
- secrets
- test artifacts
- editor/system files

Use `.dockerignore`.

## Dependency Installation
For reproducible builds:
- use lockfiles
- separate dependency installation from frequently changing source where possible
- leverage cache intentionally
- avoid downloading arbitrary remote scripts without verification

## Runtime
Containers should:
- write logs to stdout/stderr when platform collection expects it
- receive configuration from environment/runtime mechanisms
- not depend on manual changes inside a running container
- handle termination signals correctly
- avoid storing durable application state in the container filesystem

## Security
Do not bake credentials into images.
Prefer runtime secret injection.
Use non-root execution when compatible.
Keep dependencies/base images maintained.

## Health
Do not confuse container process health with application readiness.
Use application-level health/readiness checks when the deployment platform supports them.

## Verification
Build from a clean context, inspect image contents/size, run the container as the intended user, verify health/termination behavior, and scan images/dependencies where tooling exists.
