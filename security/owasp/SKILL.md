---
name: owasp
description: Orchestrate OWASP-based application and API security reviews and route findings to the appropriate specialized security skill. Use during security review, threat modeling, architecture review, feature review, or before production release.
---

# OWASP Security Review — Production Playbook

## 1. Mission

Use OWASP guidance as a security baseline and review framework, not as a magic compliance stamp.

The job of this skill is to:
1. identify applicable security risks
2. route detailed work to specialized skills
3. require evidence for security claims
4. prevent common omissions
5. document residual risk

OWASP states that the API Security Top 10 is an awareness document intended to educate developers, designers, architects, managers, and organizations about common API security weaknesses. citeturn762137search1

---

## 2. Activation

Use when:
- reviewing a feature for security
- designing a security-sensitive architecture
- reviewing an API
- preparing a production release
- adding authentication/authorization
- handling secrets
- exposing files/webhooks/external URLs
- changing privileged workflows
- investigating a suspected security weakness

---

## 3. Do Not Duplicate Specialized Skills

This skill is the orchestrator.

Route deeper reasoning to:

```text
authentication
    → identity, sessions, tokens, MFA, recovery

authorization
    → RBAC, tenant isolation, object/function/property access

api-security
    → API abuse, SSRF, resource limits, webhooks, inventory

secrets-management
    → secret lifecycle, storage, rotation, CI/CD exposure
```

Do not repeat their detailed rules here unless needed for the review.

---

## 4. Security Review Workflow

```text
Feature/system
     ↓
Identify assets
     ↓
Identify principals
     ↓
Map trust boundaries
     ↓
Identify attack surfaces
     ↓
Map applicable OWASP risks
     ↓
Route each risk to specialized skill
     ↓
Evaluate controls
     ↓
Test negative cases
     ↓
Review operational detection/recovery
     ↓
Classify residual risk
     ↓
Record evidence
```

---

## 5. Asset Identification

Ask what could be harmed:

### Confidentiality
- PII
- credentials
- payment information
- internal data
- tenant data
- private files
- business secrets

### Integrity
- balances
- permissions
- billing state
- ownership
- workflow state
- audit records

### Availability
- APIs
- workers
- databases
- expensive business operations
- queues
- external dependencies

### Trust
- authentication credentials
- signing keys
- API keys
- service identities
- deployment credentials

---

## 6. Trust Boundary Mapping

Identify transitions between:
- browser → API
- user → organization
- tenant → tenant
- API → database
- service → service
- application → external provider
- webhook provider → application
- CI/CD → production
- application → object storage

For each boundary ask:
- what is trusted?
- what is untrusted?
- how is identity established?
- how is authorization enforced?
- what input validation occurs?
- what can be manipulated?

---

## 7. OWASP API Security Top 10 Mapping

For API-facing work, review the 2023 categories:

1. Broken Object Level Authorization
2. Broken Authentication
3. Broken Object Property Level Authorization
4. Unrestricted Resource Consumption
5. Broken Function Level Authorization
6. Unrestricted Access to Sensitive Business Flows
7. Server-Side Request Forgery
8. Security Misconfiguration
9. Improper Inventory Management
10. Unsafe Consumption of APIs

OWASP's 2023 list explicitly highlights authorization, sensitive business flows, and SSRF among the API risks. citeturn762137search2turn762137search8

### Route findings

| Finding | Primary skill |
|---|---|
| Login/token/session issue | authentication |
| Object/tenant access | authorization |
| API abuse/SSRF/webhook | api-security |
| Credential/key exposure | secrets-management |
| Multiple areas | cross-layer security review |

---

## 8. Authentication Review

Ask:
- how is identity established?
- what credentials exist?
- how are they stored?
- what is their lifetime?
- can they be revoked?
- what happens on compromise?
- are recovery flows as strong as login?
- are tokens validated correctly?

Load `security/authentication` for detailed analysis.

---

## 9. Authorization Review

Ask:
- can a caller access another user's object?
- cross tenant?
- privileged function?
- sensitive property?
- bulk endpoint?
- admin/support path?
- async job?
- stale cached permission?

Load `security/authorization`.

OWASP explicitly distinguishes authentication from authorization and recommends least privilege and deny-by-default approaches. citeturn762137search3

---

## 10. API Abuse Review

Ask:
- can this be automated?
- is it expensive?
- can a request trigger a financial/business effect?
- can it be replayed?
- can users enumerate resources?
- can clients request excessive data?
- does it fetch external URLs?
- does it receive untrusted webhooks?

Load `security/api-security`.

---

## 11. Secrets Review

Ask:
- where are credentials stored?
- who can read them?
- how are they provisioned?
- can CI/CD expose them?
- how are they rotated?
- how are they revoked?
- are logs/artifacts safe?

OWASP's Secrets Management guidance emphasizes centralization/standardization, access control, automation, auditing, and secret lifecycle management. citeturn762137search0

Load `security/secrets-management`.

---

## 12. Input and Output Security

Review every attacker-controlled boundary:
- body
- query
- path
- headers
- files
- URLs
- webhook payloads
- external API responses

Ask:
- is it validated?
- bounded?
- canonicalized where necessary?
- interpreted by another system?
- safely encoded on output?
- used as a query/command/template?

Do not treat validation as the sole defense.

---

## 13. Security Configuration

Review:
- debug mode
- default credentials
- CORS
- cookie/security headers
- TLS
- exposed management endpoints
- unnecessary services
- permissive IAM
- public storage
- production logging
- environment separation

Configuration security should be verified against the actual deployment environment.

---

## 14. Dependency / Supply Chain

For important releases consider:
- dependency vulnerabilities
- unpinned/untrusted build actions
- compromised packages
- malicious scripts
- container/image provenance
- CI/CD permissions

Do not claim a dependency is safe solely because it is popular.

Use available vulnerability scanning and lockfiles.

---

## 15. Business Logic Abuse

Not every security vulnerability is an injection bug.

Review:
- free-trial creation
- coupon usage
- referrals
- voting
- invitations
- password recovery
- exports
- billing
- role changes
- resource provisioning

Ask:
```text
Can a normal user automate this faster/cheaper than the business intends?
```

OWASP added "Unrestricted Access to Sensitive Business Flows" specifically to highlight abuse of legitimate API operations such as scalping and fake-account creation. citeturn762137search8

---

## 16. Security vs Usability

Do not automatically choose maximum friction.

For each control ask:
- what threat does it mitigate?
- what is the attack cost?
- what user friction does it add?
- is there a lower-friction control?
- what happens to legitimate recovery?

Security controls should be proportionate to risk.

---

## 17. Threat Modeling

For high-risk features, enumerate:
- assets
- actors
- entry points
- trust boundaries
- abuse cases
- security controls
- residual risk

Useful categories:
- spoofing
- tampering
- repudiation
- information disclosure
- denial of service
- elevation of privilege

Do not produce a threat model that lists threats without mapping them to controls and tests.

---

## 18. Security Test Plan

A review should result in concrete tests.

Examples:
- unauthorized object ID
- cross-tenant object ID
- forged role/property
- expired/revoked token
- replayed OTP/webhook
- oversized request
- excessive batch
- SSRF destination
- malicious file
- dependency timeout
- privileged endpoint without role
- stale permission after revocation

Security findings without reproducible test cases are harder to validate and regress.

---

## 19. Evidence and Claims

Do not say:
- "OWASP compliant"
- "secure"
- "production safe"
- "no vulnerabilities"

unless the scope, evidence, and applicable assurance process justify that claim.

Instead report:

```text
Finding
Risk
Affected boundary
Control
Evidence
Residual risk
Recommended remediation
```

OWASP's Top 10 is an awareness baseline, not a certification framework. citeturn762137search1

---

## 20. Risk Classification

Use project-specific risk definitions, but a practical baseline is:

### Critical
Likely direct compromise, broad tenant escape, credential theft, or severe destructive impact.

### High
Material unauthorized access/privilege escalation or serious integrity/availability issue.

### Medium
Meaningful but bounded security weakness or defense-in-depth gap.

### Low
Limited exposure/improvement with low immediate impact.

Risk should consider:
- exploitability
- impact
- affected population
- privileges required
- detection/recovery
- compensating controls

---

## 21. Security Review Decision Tree

```text
New feature/change
      ↓
What assets matter?
      ↓
Who are the principals?
      ↓
Where are trust boundaries?
      ↓
Authentication involved?
 └→ authentication skill

Authorization involved?
 └→ authorization skill

API attack surface?
 └→ api-security skill

Secrets/credentials?
 └→ secrets-management skill

Business abuse?
 └→ api-security + threat model

Deployment/configuration?
 └→ production + security review

      ↓
Negative tests
      ↓
Evidence
      ↓
Residual risk
```

---

## 22. Anti-Patterns

### OWASP Checklist Theater
Checking boxes without testing actual behavior.

### One Skill Does Everything
Putting all security policy into one huge file.

### "We Use JWT"
Treating a technology choice as a security design.

### "It's Internal"
Assuming network location replaces authorization.

### "Input Is Validated"
Assuming validation eliminates authorization/abuse/logic risks.

### "No Findings"
Interpreting absence of a checklist item as proof of security.

### Security Without Recovery
Preventing compromise but ignoring rotation/revocation/recovery.

---

## 23. Verification Checklist

- [ ] assets identified
- [ ] principals identified
- [ ] trust boundaries mapped
- [ ] applicable OWASP API risks mapped
- [ ] authentication reviewed
- [ ] authorization reviewed
- [ ] API abuse reviewed
- [ ] secrets reviewed
- [ ] configuration/dependencies reviewed
- [ ] business-logic abuse reviewed
- [ ] negative security tests defined
- [ ] findings have evidence
- [ ] residual risk documented
- [ ] high-risk issues have remediation owners/plans

## References
- `references/owasp-mapping.md`
- `references/threat-model-template.md`
- `references/security-review-report.md`
