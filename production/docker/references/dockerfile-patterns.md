# Dockerfile Patterns

Prefer:
1. stable dependency manifests
2. dependency install
3. source copy
4. build
5. minimal runtime stage

Use `.dockerignore`.
Use lockfiles.
Keep dev/build tooling out of runtime where practical.
