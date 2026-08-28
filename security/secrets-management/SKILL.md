---
name: secrets-management
description: Design, provision, use, rotate, revoke, detect, and recover from application secrets safely. Use for API keys, database credentials, JWT signing keys, certificates, CI/CD credentials, service credentials, environment secrets, and workload identity.
---

# Secrets Management — Production Playbook

## 1. Mission

A secret is a credential or cryptographic value whose disclosure can enable unauthorized access, impersonation, data access, or code/deployment control.

Treat secrets as a lifecycle:

```text
create
  ↓
store
  ↓
provision
  ↓
use
  ↓
audit
  ↓
rotate
  ↓
revoke
  ↓
remove
```

The security objective is to minimize:
- number of people/systems that can read it
- lifetime
- blast radius
- places where it exists
- chance of accidental disclosure

OWASP's Secrets Management Cheat Sheet emphasizes standardized storage, strong access controls, automation, auditing, and complete secret lifecycle management. citeturn972125search0

---

## 2. Activation

Use when:
- adding a new credential
- configuring environment variables
- deploying to production
- adding API keys
- creating signing/encryption keys
- configuring CI/CD credentials
- adding cloud access
- integrating third-party services
- rotating credentials
- investigating leaked credentials
- reviewing logs/artifacts for secret exposure

---

## 3. What Counts as a Secret?

Potential secrets include:
- passwords
- database credentials
- API keys
- bearer tokens
- refresh tokens
- private signing keys
- encryption keys
- service-account credentials
- cloud access credentials
- webhook secrets
- certificates/private keys
- CI/CD deployment credentials

Do not assume something is safe because it is called:
- config
- token
- identifier
- secret-looking variable

When uncertain, treat it as sensitive until classified.

---

## 4. First Decision: Can the Credential Be Avoided?

Before creating a long-lived secret ask:

1. Does the platform support workload identity?
2. Can short-lived credentials be used?
3. Can the service use an IAM role/service account?
4. Can a provider issue scoped temporary credentials?
5. Can the operation be performed without a credential at all?

Prefer identity-based, short-lived access where the platform supports it.

Do not create static keys merely because they are familiar.

---

## 5. Secret Classes

Classify by impact.

### Low
Limited test/demo credential with no production access.

### Medium
Credential for a bounded service/environment.

### High
Production database, payment, signing, cloud administrator, or broad service credential.

### Critical
Credentials capable of widespread environment compromise or cryptographic trust compromise.

Higher-impact credentials require:
- stronger storage controls
- narrower access
- stronger auditability
- shorter lifetime where possible
- emergency rotation procedure

---

## 6. Storage

Do not store production secrets in:
- source code
- Git history
- frontend bundles
- public artifacts
- Docker images
- database rows without a justified encryption/access model
- unprotected local config committed to repositories

Use an environment-appropriate secret-management mechanism:
- cloud secret manager
- Vault-like system
- CI/CD secret store
- workload identity
- encrypted deployment configuration

OWASP recommends dedicated secret-management systems that provide centralized management, access control, auditing, and automated lifecycle capabilities when the environment requires them. citeturn972125search0

Do not introduce a complex secrets platform if the deployment environment already provides an adequate managed secret store.

---

## 7. Source Control

Never commit secrets.

Protect against:
- `.env` files
- test credentials
- pasted production keys
- private certificates
- service-account JSON
- generated config
- shell history containing secrets

Use:
- `.gitignore`
- secret-scanning tools
- pre-commit/CI checks
- repository history scanning when exposure occurs

A secret that was removed in a later commit may still exist in Git history.

---

## 8. Environment Separation

Separate credentials by environment:

```text
development
staging
production
```

Avoid:
- production DB credentials in developer laptops
- staging keys with production privileges
- shared team-wide credentials
- reusing one API key across unrelated applications

A compromise of one environment should not automatically compromise another.

---

## 9. Least Privilege

A credential should have the minimum permissions needed for the workload.

Examples:

Bad:
```text
application → cloud administrator
```

Better:
```text
application → read/write only required bucket
```

Bad:
```text
reporting service → full production DB write
```

Better:
```text
reporting service → read-only reporting access
```

Least privilege reduces blast radius when a credential is stolen. OWASP explicitly recommends minimizing secret access and privileges. citeturn972125search0

---

## 10. Secret Distribution

Secrets should enter the application through a controlled provisioning mechanism.

Preferred order where supported:

```text
workload identity / short-lived credential
        ↓
managed runtime secret injection
        ↓
environment configuration
        ↓
local development secret store
```

Avoid baking secrets into:
- images
- source
- compiled client assets
- build logs
- generated static files

A browser application should never receive a credential that is intended to remain secret from the browser user.

---

## 11. Build-Time vs Runtime Secrets

Be explicit about when a secret is needed.

### Runtime-only
Keep it out of image/build artifacts.

### Build-time
Ask whether the build actually needs the secret. If yes:
- minimize exposure
- prevent it from being persisted in layers/artifacts
- ensure build logs do not reveal it

Do not pass secrets through ordinary build arguments if the tooling can persist them in image metadata/history.

Prefer platform-supported secret mounts/mechanisms.

---

## 12. CI/CD

CI/CD systems often have powerful credentials.

Review:
- who can trigger workflows
- fork/PR behavior
- environment protections
- token permissions
- deployment identity
- secret scopes
- logs/artifacts
- third-party actions/scripts

GitHub documents using least-privilege `GITHUB_TOKEN` permissions and recommends OpenID Connect for short-lived cloud credentials instead of storing long-lived cloud secrets where possible. citeturn972125search4turn972125search6

Do not expose production credentials to untrusted pull requests.

---

## 13. Secret Exposure in Logs

Never log:
- passwords
- OTPs
- access tokens
- refresh tokens
- API keys
- private keys
- reset tokens
- full Authorization headers

Also watch for indirect leakage:
- URLs containing tokens
- exception objects
- request bodies
- headers
- serialized environment configuration
- debug dumps

Use redaction where appropriate, but do not rely on redaction as the primary defense.

---

## 14. Secret Exposure in Errors

Be careful with:
- third-party SDK exceptions
- connection strings
- signed URLs
- authentication headers
- configuration dumps

A safe client error should not reveal credentials or internal secret locations.

Log diagnostic details only where the logging system is trusted and access-controlled, and redact secrets.

---

## 15. Secret Rotation

Rotation means replacing a credential without unnecessary downtime.

For every important secret define:
- rotation interval where appropriate
- trigger conditions
- owner
- automation
- overlap period
- old-key invalidation
- verification

### Dual-Key Rotation

When zero downtime matters:

```text
old key active
       +
new key active
       ↓
deploy consumers using new
       ↓
verify usage
       ↓
revoke old
```

Do not revoke the old key before every dependent consumer can use the new one.

---

## 16. Emergency Rotation

If a secret is exposed:

```text
detect
  ↓
contain
  ↓
revoke/rotate
  ↓
assess blast radius
  ↓
inspect logs/access
  ↓
remove exposure
  ↓
deploy replacement
  ↓
verify
  ↓
document incident
```

Assume the secret is compromised; do not rely on hopes that nobody saw it.

---

## 17. Secret Scanning

Use automated secret scanning where practical.

Scan:
- working tree
- commits
- pull requests
- CI logs/artifacts where supported
- container/image sources

A scanner is a detection aid, not proof that no secret exists.

False negatives remain possible, especially for custom/encoded credentials.

---

## 18. Secret vs Public Configuration

Not every environment variable is secret.

Public configuration may include:
- feature flags
- public API base URL
- UI theme
- non-sensitive limits

Still classify deliberately.

The dangerous mistake is treating:
```text
"it's in an environment variable"
```
as equivalent to:
```text
"it's secret"
```

Environment variables can leak through:
- process inspection
- crash dumps
- logging
- build tooling
- debugging
- child processes

Use appropriate runtime controls.

---

## 19. Client-Side Applications

Any value shipped to a browser/mobile client should be assumed visible to the user.

Never send:
- database credentials
- server API secrets
- private signing keys
- privileged cloud credentials
- internal service tokens

Use a backend to perform privileged operations when the credential must remain secret.

"Obfuscated" or bundled credentials are not secrets.

---

## 20. Database Credentials

Review:
- separate DB users by service
- least privilege
- environment separation
- rotation capability
- connection-string exposure
- logs/metrics
- backup/config artifact exposure

Prefer separate credentials rather than one shared "application DB admin" account.

Do not grant schema/database ownership to ordinary application runtime accounts unless actually required.

---

## 21. API Keys

For third-party keys:
- scope permissions
- restrict environments/origins/IPs where supported
- set expiration/rotation if supported
- store outside source control
- audit use
- revoke unused keys

Do not expose a server API key through the frontend simply because the provider's JavaScript SDK is convenient.

---

## 22. Signing and Encryption Keys

Signing keys can be more sensitive than ordinary API keys because they may establish trust.

Define:
- algorithm
- key purpose
- active/previous key set
- rotation
- `kid`/key identifier where applicable
- validation behavior during rollover
- emergency revocation/replacement

Do not reuse one key for unrelated purposes.

Do not store private signing material in source control or client code.

---

## 23. Secret Access Auditing

For high-value secrets, be able to answer:
- who accessed it?
- which workload?
- when?
- from where?
- why?
- what happened afterward?

Use audit logs where the platform supports them.

Do not give everyone direct secret-manager access when applications can use workload identity/role-based access.

---

## 24. Local Development

Local development should be convenient without normalizing unsafe practices.

Prefer:
- local `.env` ignored by Git
- developer-specific secret store
- safe test credentials
- documented setup

Never ask developers to copy production credentials into local config as a normal setup step.

---

## 25. Testing

Test:
- secret absence/misconfiguration
- permission denied
- rotation
- expired credential
- revoked credential
- CI/CD isolation
- logging redaction
- client bundle exposure
- secret scanning
- emergency rotation procedure where practical

A test environment should not accidentally use production credentials.

---

## 26. Incident Response

If a credential may have leaked:

1. Identify exactly what was exposed.
2. Determine possible access scope.
3. Revoke/rotate immediately when safe.
4. Search logs/audit trails.
5. Search source/history/artifacts.
6. Replace dependent configuration.
7. Verify old credential no longer works.
8. Review lateral access/blast radius.
9. Document timeline and remediation.

Do not merely delete the leaked line from the latest code and consider the incident closed.

---

## 27. Review Decision Tree

```text
Need credential?
    ↓
Can workload identity/short-lived auth avoid it?
    ├─ yes → prefer that
    └─ no
         ↓
What is the blast radius?
         ↓
Can permissions be reduced?
         ↓
Where is it stored?
         ↓
How is it provisioned?
         ↓
Can it reach build artifacts/client code/logs?
         ↓
How is it rotated?
         ↓
How is it revoked?
         ↓
How is access audited?
         ↓
What happens if leaked?
```

---

## 28. Anti-Patterns

### Secret in Git
Even temporarily.

### `.env` Committed
Common accidental exposure.

### Secret in Docker Image
Build history/artifacts can preserve it.

### Production Credential Locally
Unnecessary blast radius.

### Shared Superuser Key
One credential compromises many systems.

### Long-Lived Static Cloud Key
Prefer workload identity/short-lived credentials when supported.

### Secret in Frontend
Anything shipped to the browser is not secret.

### Log Everything
Debug logging captures credentials/config.

### Rotate Without Coordination
New credential deployed before consumers can use it, causing outage.

### Delete From HEAD Only
Secret remains in Git history/artifacts.

### Scanner = Security
Secret scanning cannot prove absence of all secrets.

---

## 29. Verification Checklist

- [ ] secret necessity challenged
- [ ] workload identity/short-lived option considered
- [ ] secret classified by impact
- [ ] environment separation
- [ ] least privilege
- [ ] secure storage
- [ ] safe provisioning
- [ ] no source-control exposure
- [ ] no client exposure
- [ ] no image/build artifact exposure
- [ ] no logging/error exposure
- [ ] rotation strategy
- [ ] emergency revocation
- [ ] access auditing
- [ ] CI/CD protection
- [ ] secret scanning
- [ ] recovery procedure
- [ ] dependent systems tested after rotation

## References
- `references/secret-lifecycle.md`
- `references/rotation.md`
- `references/cicd-and-workload-identity.md`
- `references/incident-response.md`

## Review Procedure

1. Identify the credential and whether it is actually necessary.
2. Prefer workload identity/short-lived credentials where supported.
3. Review storage, provisioning, access, and least privilege.
4. Review source/build/log/client exposure.
5. Define rotation/revocation and emergency response.
6. Verify CI/CD and audit controls.

## Verification Checklist

- [ ] secret necessity challenged
- [ ] least privilege applied
- [ ] storage/provisioning secure
- [ ] source/build/client/log exposure reviewed
- [ ] rotation/revocation defined
- [ ] CI/CD exposure reviewed
- [ ] incident response path exists
