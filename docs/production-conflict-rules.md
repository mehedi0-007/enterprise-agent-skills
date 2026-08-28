# V2 Production Conflict Rules

## 1. Image Build vs Deployment

Building a container successfully does not mean the service is production-ready.

## 2. CI Green vs Production Healthy

A passing CI pipeline proves only the checks that actually ran. Production health requires live verification.

## 3. Rollback vs Migration

Code rollback is unsafe when the current schema/data is incompatible with the old artifact.

## 4. Health vs Liveness

A dependency outage does not automatically mean the process should restart.

Use readiness/liveness semantics deliberately.

## 5. Performance vs Scaling

Adding replicas is not automatically a performance fix. The limiting resource may be the database, dependency, queue, or connection pool.

## 6. Observability vs Alerting

Not every telemetry signal should page someone. Alerts need actionable ownership.

## 7. Security vs Pipeline Speed

Do not bypass security gates just to shorten deployment time.

## 8. Artifact vs Environment

Prefer promoting the same immutable artifact across environments rather than rebuilding separately for production.
