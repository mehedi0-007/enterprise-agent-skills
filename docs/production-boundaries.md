# V2 Production Semantic Boundaries

## Canonical Ownership

```text
docker
  → container image/runtime construction

ci-cd
  → validation, build, security gates, artifact creation and promotion

deployment
  → live environment rollout, health gates, rollback/forward-fix

observability
  → telemetry, diagnosis, alerts, SLOs, operational evidence

performance
  → measured latency/throughput/resource optimization
```

## Cross-Cutting Rules

### Docker vs CI/CD
`docker` defines how the image is built and behaves at runtime.
`ci-cd` decides when/how the image is tested and promoted.

### CI/CD vs Deployment
`ci-cd` produces/promotes an artifact.
`deployment` changes the live environment and verifies the rollout.

### Deployment vs Observability
`deployment` chooses rollout/abort/recovery behavior.
`observability` supplies the health and diagnostic signals.

### Performance vs Observability
`observability` makes performance measurable.
`performance` interprets measurements and changes the system.

### Migrations
Schema/data changes are owned by `database/migrations`.
Production rollout compatibility is owned by `deployment`.
Neither should assume the other can be skipped.

## Canonical Release Flow

```text
source change
   ↓
CI validation
   ↓
build immutable artifact
   ↓
security/provenance checks
   ↓
staging
   ↓
deployment verification
   ↓
production rollout
   ↓
observability gates
   ↓
post-deploy verification
   ↓
performance/regression review
```

## Recovery

```text
failure
  ↓
stop promotion
  ↓
identify impact
  ↓
choose:
  feature disable
  code rollback
  configuration rollback
  forward-fix
  data recovery
  ↓
verify recovery
```

A rollback must consider schema/data compatibility and external side effects.
