---
name: docker
description: Design, build, review, and troubleshoot production container images and runtime configurations. Use for Dockerfiles, Compose files, container security, image size, reproducibility, build caching, secrets, health, shutdown behavior, and production runtime hardening.
---

# Docker — Production Playbook

## 1. Mission

A production container should be:
- reproducible
- minimal enough for its purpose
- free of unnecessary secrets/tools
- non-root where practical
- correctly configured for runtime
- observable
- responsive to shutdown
- easy to rebuild and deploy

Do not optimize only for image size. Optimize for security, correctness, reproducibility, startup/runtime behavior, and operational simplicity.

---

## 2. Activation

Use when:
- creating/reviewing a Dockerfile
- containerizing an application
- changing base images
- improving build speed
- debugging image/runtime failures
- adding health checks
- changing container users/permissions
- handling build/runtime secrets
- preparing images for production deployment

---

## 3. Separate Build From Runtime

Prefer multi-stage builds when build tools are not needed at runtime.

Concept:

```text
builder
├── compiler
├── package manager
├── dev dependencies
└── source/build process
        ↓
runtime
├── application artifact
├── production dependencies
└── minimal runtime tooling
```

Benefits:
- smaller runtime image
- smaller attack surface
- fewer accidental tools/secrets
- clearer runtime dependency set

Do not blindly copy the entire build filesystem into the runtime stage.

---

## 4. Base Image Selection

Choose based on:
- supported runtime
- security maintenance
- compatibility
- libc/runtime requirements
- image ecosystem
- patch/update process

Do not choose an ultra-minimal image if it introduces compatibility or debugging problems that outweigh its benefit.

Do not assume "smallest image" means "most secure."

Pin or otherwise control base-image versions according to the project's reproducibility policy.

---

## 5. Build Context

Use `.dockerignore` to exclude:
- `.git`
- local dependencies
- test output
- editor files
- local secrets
- caches
- large unnecessary assets

A clean context improves:
- build speed
- cache effectiveness
- security
- reproducibility

Never rely on `.dockerignore` as the only secret-protection mechanism. A secret that was already copied into another build layer may still exist in image history.

---

## 6. Dependency Reproducibility

Use lockfiles and deterministic dependency installation.

Prefer patterns that:
- reuse cache for unchanged dependency manifests
- avoid downloading unnecessary development packages into runtime
- fail clearly when dependency resolution changes unexpectedly

Do not remove lockfiles to "make Docker builds easier."

---

## 7. Layer and Cache Strategy

Order Dockerfile instructions so stable inputs are installed before frequently changing source when that improves cache reuse.

Example concept:

```text
copy dependency manifests
install dependencies
copy source
build
```

Do not contort the Dockerfile into unreadable micro-optimizations for tiny build gains.

Build cache is a performance tool; correctness/reproducibility remains primary.

---

## 8. Secrets During Build

Never bake production secrets into:
- image layers
- source
- build artifacts
- final environment defaults

If a build genuinely requires a secret, use the build system's supported secret mechanism so it does not become a normal persisted build argument/layer.

Do not use:
```text
ARG SECRET=...
```
as a safe secret-management strategy.

Build-time access should be:
- minimal
- scoped
- temporary
- auditable

Prefer redesigning builds so secrets are not required at all.

---

## 9. Runtime Configuration

Inject environment-specific configuration at runtime rather than baking it into the image.

Examples:
- database URL
- API keys
- feature config
- environment endpoints

The same immutable image should ideally move through environments while runtime configuration changes.

Do not rebuild the image just because the environment changed unless the application artifact itself must change.

---

## 10. Non-Root Runtime

Run as a non-root user when the workload supports it.

Why:
A container escape or application exploit can have greater impact under unnecessary root privileges.

Review:
- file ownership
- writable directories
- temporary storage
- ports
- mounted volumes

Do not switch to a non-root user without testing filesystem/runtime behavior.

---

## 11. Filesystem

Prefer an image whose application directories are read-only except where the process genuinely needs write access.

Where supported, consider read-only root filesystem plus explicit writable mounts/temp storage.

Do not write durable application state into the container filesystem because containers are replaceable.

---

## 12. PID 1 and Signals

The main process must receive termination signals and shut down correctly.

Review:
- SIGTERM handling
- graceful shutdown
- child-process reaping
- timeout before forced kill
- connection draining

For Node/web servers, make sure the actual application process can respond to container termination rather than hiding it behind a shell that mishandles signals.

A container that ignores graceful termination can cause:
- dropped requests
- incomplete jobs
- slow deployments
- duplicate work

---

## 13. Health Checks

Health has different meanings.

### Liveness
Should the process be restarted?

### Readiness
Should traffic be sent here?

Do not make liveness depend on every external dependency or a transient database outage unless restart is actually the correct recovery action.

Readiness can be stricter when the service cannot safely serve requests.

Prefer application-level health semantics over "process exists."

---

## 14. Startup vs Readiness

A process can be alive but not ready.

Examples:
- warming cache
- loading configuration
- establishing required resources
- running startup initialization

Use startup/readiness behavior that prevents traffic from reaching an instance before it can serve correctly.

Do not use a health check that reports success before the actual service is ready.

---

## 15. Logging

For containerized services, prefer predictable stdout/stderr logging when the platform collects container output.

Use structured logs where possible.

Never log:
- passwords
- access/refresh tokens
- API keys
- OTPs
- private keys

Container logging should integrate with centralized observability rather than depend on persistent local log files.

---

## 16. Time and Signals

Do not make the application dependent on the container's local timezone unless required.

Prefer:
- explicit timezone handling
- UTC-oriented server defaults where appropriate
- application-level formatting at the edge

Avoid debugging time issues by manually changing the container timezone without understanding the application contract.

---

## 17. Ports and Networking

Expose only required ports.

Do not assume:
```text
internal network = secure
```

Application authorization remains necessary.

Bind/listen according to the deployment environment's expectations.

Avoid unnecessary network listeners inside the image.

---

## 18. Dependency and Image Security

Review:
- base-image vulnerabilities
- package vulnerabilities
- stale operating-system packages
- unnecessary binaries
- unnecessary shells/tools
- image provenance/scanning

A vulnerability scanner provides evidence, not absolute safety.

Define policy for:
- critical vulnerabilities
- exceptions
- patch timing
- image rebuild cadence

---

## 19. Image Metadata

Use metadata/labels where they improve:
- ownership
- version
- source commit
- build provenance
- support/debugging

An immutable version or digest should identify what was actually deployed.

Do not rely only on mutable tags like:
```text
latest
```

for production rollback/auditability.

---

## 20. Runtime Resource Limits

Containers need operational resource expectations.

Review:
- CPU
- memory
- concurrency
- file descriptors
- request limits
- worker counts

Do not assume adding more CPU/memory fixes application/database contention.

Container resource settings should match observed workload.

---

## 21. Graceful Shutdown

Define what happens when the container is terminating:

```text
receive termination signal
      ↓
stop accepting new work
      ↓
finish/abort safe in-flight work
      ↓
close DB/queue connections
      ↓
flush important telemetry
      ↓
exit before deadline
```

For background workers, determine whether current jobs can be safely interrupted or should be allowed to complete.

Do not terminate active payment/data-integrity operations without understanding their retry/idempotency behavior.

---

## 22. Configuration Validation

Fail fast on required configuration at startup when appropriate.

Examples:
- missing database URL
- invalid signing configuration
- missing storage credential
- invalid environment setting

Avoid starting a service that will fail every request due to missing critical configuration.

Do not include secret values in the resulting error.

---

## 23. Build vs Runtime Dependencies

Runtime should contain only what execution actually requires.

Examples:
- compilers
- test runners
- package caches
- source maps/source trees if not needed
- Git
- debugging shells

can often stay out of the runtime image.

But do not remove tools required for:
- TLS/CA certificates
- native modules
- font rendering
- database drivers
- process supervision
without testing.

---

## 24. Reproducible Image Identity

A deployment should be able to answer:

```text
Which source?
Which dependencies?
Which base image?
Which build?
Which image digest?
```

Prefer immutable artifact identity.

Do not rely on rebuilding "the same Dockerfile later" to reproduce exactly the same production binary unless the dependency/base-image inputs are also controlled.

---

## 25. Compose / Local Development

Local Compose configuration should model production-relevant dependencies without pretending to be production infrastructure.

Avoid:
- committing production secrets
- privileged containers without need
- host filesystem mounts that hide container behavior
- relying on undocumented startup ordering

Use health/dependency semantics where useful, but do not assume `depends_on` alone means the application is ready.

---

## 26. Containers and Migrations

Do not automatically run destructive DB migrations from every application container startup when multiple replicas may start concurrently.

Prefer a deliberate migration/deployment process.

Coordinate with:
- `database/migrations`
- `production/deployment`

---

## 27. Security Hardening

Where supported and justified, review:
- non-root
- read-only filesystem
- dropped Linux capabilities
- seccomp/AppArmor/SELinux policy
- minimal network access
- secret injection
- no privileged mode
- no host namespace sharing without need

Do not apply hardening blindly if it breaks legitimate runtime behavior; test and document exceptions.

---

## 28. Troubleshooting Order

When a container fails:

```text
1. image built?
2. container starts?
3. process launches?
4. configuration valid?
5. filesystem permissions?
6. network/DNS?
7. dependency connectivity?
8. readiness?
9. application logs?
10. resource exhaustion?
11. signal/shutdown behavior?
```

Do not immediately rebuild the entire image if the failure is runtime configuration.

---

## 29. Review Procedure

For a production Dockerfile ask:

1. Is build/runtime separated?
2. Is base image maintained and controlled?
3. Is dependency installation reproducible?
4. Is build context clean?
5. Could secrets enter layers/artifacts?
6. Does runtime run non-root?
7. What filesystem must be writable?
8. Does PID 1 handle signals?
9. Are health/readiness semantics correct?
10. Is image identity traceable?
11. Are unnecessary tools removed?
12. Are vulnerabilities scanned/patched?
13. Are resources bounded?
14. Is startup configuration validated?
15. Does shutdown preserve correctness?

---

## 30. Anti-Patterns

### `latest` in Production
Mutable artifact identity.

### Secret ARG
Credential embedded in build history/layers.

### Copy Everything
Entire repository/node_modules/dev tools enter runtime.

### Root Forever
No reason to retain elevated runtime privileges.

### Shell as PID 1
Signal/graceful-shutdown problems.

### Health = Process Alive
Traffic reaches an unready service.

### Persistent Data in Container
Data disappears on replacement.

### Debug Tools in Runtime
Larger attack surface.

### Huge One-Stage Image
Build dependencies remain in production.

### Rebuild Per Environment
Environment config changes artifact identity unnecessarily.

### Migration on Every Startup
Replica race/duplicate migration execution.

### Blind Hardening
Security settings break the application without documented testing.

---

## 31. Verification Checklist

- [ ] multi-stage/build-runtime separation reviewed
- [ ] base image controlled
- [ ] dependencies reproducible
- [ ] build context minimized
- [ ] secrets absent from layers/artifacts
- [ ] runtime configuration externalized
- [ ] non-root tested
- [ ] filesystem writes intentional
- [ ] signal/graceful shutdown tested
- [ ] readiness/liveness semantics correct
- [ ] logs safe
- [ ] image vulnerability scan performed
- [ ] immutable image identity available
- [ ] resource expectations reviewed
- [ ] startup config validation tested
- [ ] migrations not accidentally coupled to replica startup
- [ ] runtime hardening exceptions documented

## References
- `references/dockerfile-patterns.md`
- `references/secrets-and-builds.md`
- `references/health-and-shutdown.md`
- `references/image-security.md`

## Cross-Skill Routing
For pipeline/build promotion behavior, coordinate with `ci-cd`.
For live rollout/runtime health and recovery, coordinate with `deployment`.
