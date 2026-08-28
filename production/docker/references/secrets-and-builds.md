# Build Secrets

Do not use ordinary ARG/ENV instructions for sensitive build secrets.

If a build truly needs a secret, use the supported build secret mechanism so the secret is not persisted as a normal layer/input.

Prefer redesigning the build to avoid secret access.
