# Node Service

A production Node API image should generally:
- install dependencies from lockfile
- build in a builder stage
- copy only runtime artifacts/dependencies
- run as non-root when practical
- receive config at runtime
- handle SIGTERM
- expose readiness/liveness semantics through the deployment environment
- log to stdout/stderr
