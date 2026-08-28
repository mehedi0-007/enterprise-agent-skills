#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

# Canonical minimal additions. Existing sections with these exact H2 headings
# are left untouched so this script is safe to run repeatedly.
ADDITIONS = {
"backend/api-design/SKILL.md": {
"Review Procedure": """1. Identify resource/use-case and actor.
2. Define request/response and HTTP semantics.
3. Review validation, authorization, pagination, errors, retries, idempotency, and concurrency.
4. Check external side effects and compatibility.
5. Verify observability and tests before implementation.""",
"Verification Checklist": """- [ ] contract is explicit
- [ ] authorization boundary defined
- [ ] validation and limits defined
- [ ] status/error semantics defined
- [ ] pagination/filter/sort bounded
- [ ] retry/idempotency behavior reviewed
- [ ] concurrency/external side effects reviewed
- [ ] compatibility considered""",
},
"backend/error-handling/SKILL.md": {
"Activation": "Use when designing or reviewing exceptions, API errors, validation failures, dependency failures, retries, logging, or user-facing failure behavior.",
"Review Procedure": """1. Classify the error: client/input, authentication, authorization, business conflict, dependency, or internal failure.
2. Decide whether it is retryable.
3. Preserve a stable machine-readable contract.
4. Prevent sensitive/internal detail leakage.
5. Ensure logs/telemetry contain useful diagnostic context.
6. Verify behavior at API/UI boundaries.""",
"Verification Checklist": """- [ ] error categories are deliberate
- [ ] retryability is explicit
- [ ] client contract is stable
- [ ] sensitive details are not exposed
- [ ] useful diagnostic context exists
- [ ] relevant tests cover failure paths""",
},
"backend/validation/SKILL.md": {
"Activation": "Use when validating request bodies, query/path parameters, commands, imported data, or other untrusted input.",
"Review Procedure": """1. Identify the trust boundary and authoritative source of truth.
2. Validate shape/type/range/format.
3. Separate structural validation from business rules and authorization.
4. Define error mapping.
5. Check size/depth/resource bounds.
6. Verify server-side enforcement.""",
"Verification Checklist": """- [ ] untrusted inputs identified
- [ ] structural validation defined
- [ ] business validation separated
- [ ] authorization not delegated to validation
- [ ] resource limits considered
- [ ] stable error mapping defined
- [ ] negative tests exist""",
},
"backend/repository-pattern/SKILL.md": {
"Review Procedure": """1. Identify the exact persistence operation the use case needs.
2. Decide whether a repository abstraction adds meaningful value.
3. Review projection, query count, pagination, and trusted tenant/object scope.
4. Check transaction participation and concurrency semantics.
5. Inspect ORM leakage and persistence error translation.
6. Verify query behavior with integration tests.""",
"Verification Checklist": """- [ ] abstraction justified
- [ ] method intent is clear
- [ ] data access is bounded
- [ ] N+1/over-fetching reviewed
- [ ] tenant/object scope correct
- [ ] transaction/concurrency assumptions explicit
- [ ] persistence errors safely translated
- [ ] DB integration behavior tested""",
},
"database/indexing/SKILL.md": {
"Review Procedure": """1. Identify the measured query/workload.
2. Inspect current plan and existing indexes.
3. Determine whether query shape can be improved first.
4. Choose index type/columns/order/predicate from actual access patterns.
5. Evaluate write/storage/maintenance cost.
6. Plan safe production creation.
7. Measure the result and check regressions.""",
"Verification Checklist": """- [ ] workload evidence exists
- [ ] existing indexes reviewed
- [ ] index shape matches query pattern
- [ ] selectivity/order considered
- [ ] write/storage cost considered
- [ ] build strategy is safe
- [ ] before/after measurement captured""",
},
"database/migrations/SKILL.md": {
"Review Procedure": """1. Identify affected readers, writers, workers, and consumers.
2. Classify risk and reversibility.
3. Check old/new application compatibility.
4. Design expand/migrate/contract when needed.
5. Plan locks, backfill, monitoring, and recovery.
6. Verify data invariants before destructive cleanup.
7. Validate post-migration application behavior.""",
"Verification Checklist": """- [ ] dependencies inventoried
- [ ] compatibility window understood
- [ ] risk/recovery classified
- [ ] backfill is bounded/restartable
- [ ] lock impact reviewed
- [ ] destructive step gated by evidence
- [ ] post-migration invariants verified""",
},
"database/postgresql/SKILL.md": {
"Activation": "Use when choosing PostgreSQL features, types, constraints, SQL semantics, transactions, locking, extensions, or database-specific behavior.",
"Review Procedure": """1. Identify the required database behavior.
2. Check PostgreSQL semantics/version support.
3. Prefer database constraints for enforceable invariants.
4. Review transaction, locking, planner, and operational effects.
5. Verify migration and deployment implications.
6. Test against a representative PostgreSQL environment.""",
"Verification Checklist": """- [ ] PostgreSQL-specific behavior is intentional
- [ ] version compatibility checked
- [ ] constraints considered
- [ ] transaction/locking behavior understood
- [ ] performance implications reviewed
- [ ] migration/deployment impact reviewed
- [ ] representative DB tests exist""",
},
"database/query-optimization/SKILL.md": {
"Review Procedure": """1. Capture the real query/workload and baseline.
2. Inspect generated SQL and execution plan.
3. Compare estimated vs actual rows.
4. Review scans, joins, sorts, loops, buffers, and application query count.
5. Identify the dominant bottleneck.
6. Apply the smallest justified change.
7. Re-measure correctness, latency, and resource impact.""",
"Verification Checklist": """- [ ] baseline captured
- [ ] representative parameters used
- [ ] generated SQL inspected
- [ ] plan reviewed
- [ ] cardinality/loops examined
- [ ] N+1/payload/connection issues considered
- [ ] change re-measured
- [ ] correctness preserved""",
},
"engineering/architecture/SKILL.md": {
"Activation": "Use when creating or changing system/module boundaries, dependencies, data ownership, integration patterns, or major technical design.",
"Review Procedure": """1. State requirements and constraints.
2. Identify bounded responsibilities and ownership.
3. Map data/control flow and trust boundaries.
4. Compare simple and more complex options.
5. Review failure, scaling, operability, security, and migration implications.
6. Make assumptions and tradeoffs explicit.
7. Verify the architecture against realistic workflows.""",
"Verification Checklist": """- [ ] requirements drive the design
- [ ] responsibilities are cohesive
- [ ] dependency direction is clear
- [ ] data ownership is explicit
- [ ] failure modes considered
- [ ] security/operability considered
- [ ] migration/rollback implications considered""",
},
"engineering/cross-layer-review/SKILL.md": {
"Activation": "Use when a feature crosses backend, database, security, frontend, infrastructure, or deployment boundaries.",
"Review Procedure": """1. Map the end-to-end feature flow.
2. Identify contracts between layers.
3. Check error/state/authorization semantics across boundaries.
4. Check persistence, concurrency, and migration implications.
5. Check frontend behavior against actual API semantics.
6. Check observability and deployment implications.
7. Verify the complete flow with representative tests.""",
"Verification Checklist": """- [ ] contracts agree across layers
- [ ] authorization matches actual operations
- [ ] API errors map correctly to UX
- [ ] DB/schema changes are compatible
- [ ] async/concurrency behavior agrees
- [ ] observability covers the flow
- [ ] deployment/recovery path is coherent""",
},
"engineering/production-readiness/SKILL.md": {
"Review Procedure": """1. Verify functional correctness and tests.
2. Review security, failure, performance, and operability.
3. Verify configuration, secrets, migrations, and dependencies.
4. Verify health/observability/alerts.
5. Verify deployment/recovery strategy.
6. Identify residual risks and evidence.""",
"Verification Checklist": """- [ ] tests appropriate to risk pass
- [ ] security reviewed
- [ ] failure/recovery reviewed
- [ ] migrations/config/secrets reviewed
- [ ] observability/alerts ready
- [ ] performance/capacity acceptable
- [ ] deployment/rollback or forward-fix defined
- [ ] residual risk documented""",
},
"engineering/requirements-analysis/SKILL.md": {
"Activation": "Use when turning ambiguous feature requests, bug reports, or stakeholder goals into explicit engineering requirements.",
"Review Procedure": """1. Identify the user/business outcome.
2. Separate must-have scope from assumptions.
3. Define actors, inputs, outputs, states, and constraints.
4. Capture edge cases and failure behavior.
5. Define acceptance criteria that can be verified.
6. Identify unresolved risk without inventing product policy.""",
"Verification Checklist": """- [ ] goal is explicit
- [ ] actors/stakeholders identified
- [ ] scope bounded
- [ ] acceptance criteria testable
- [ ] edge/failure cases listed
- [ ] assumptions documented
- [ ] ambiguity called out""",
},
"engineering/testing-quality/SKILL.md": {
"Activation": "Use when deciding what tests to add or reviewing test coverage for new or changed behavior.",
"Review Procedure": """1. Identify risk and critical behavior.
2. Choose unit/integration/contract/end-to-end tests accordingly.
3. Include negative and concurrency/failure cases where relevant.
4. Avoid tests that assert incidental implementation details.
5. Run representative checks and inspect failures.
6. Maintain deterministic, useful test data.""",
"Verification Checklist": """- [ ] critical behavior covered
- [ ] failure/negative paths covered
- [ ] integration boundaries covered where needed
- [ ] concurrency/security cases included where relevant
- [ ] tests are deterministic
- [ ] assertions verify behavior, not incidental implementation""",
},
"security/api-security/SKILL.md": {
"Review Procedure": """1. Identify endpoint principal, asset, action, and trust boundaries.
2. Check applicable OWASP API risks.
3. Review authentication/authorization, object/property access, and tenant scope.
4. Review resource abuse, SSRF, uploads, webhooks, replay, and external APIs.
5. Review errors, auditability, and negative tests.
6. Route detailed controls to specialized security skills.""",
"Verification Checklist": """- [ ] object/function/property authorization reviewed
- [ ] tenant isolation reviewed
- [ ] resource abuse/rate limits reviewed
- [ ] SSRF/upload/webhook risks reviewed where applicable
- [ ] replay/idempotency reviewed
- [ ] third-party responses treated as untrusted
- [ ] negative security tests exist""",
},
"security/authentication/SKILL.md": {
"Review Procedure": """1. Identify the authentication model and trust boundary.
2. Review credential/session/token lifecycle.
3. Review storage, transport, expiry, revocation, and rotation.
4. Review recovery, OTP/MFA, enumeration, and brute-force resistance.
5. Review concurrent refresh/retry behavior.
6. Verify audit and compromise-response behavior.""",
"Verification Checklist": """- [ ] identity lifecycle defined
- [ ] credential storage secure
- [ ] session/token lifetime defined
- [ ] revocation/rotation defined
- [ ] recovery flows reviewed
- [ ] enumeration/abuse controls reviewed
- [ ] concurrent refresh/retry tested""",
},
"security/owasp/SKILL.md": {
"Review Procedure": """1. Identify assets, principals, and trust boundaries.
2. Map applicable OWASP risks.
3. Route detailed analysis to the specialized security skill.
4. Require evidence through negative tests and configuration review.
5. Classify residual risk and remediation priority.
6. Avoid unsupported claims of "OWASP compliant" or "secure.""",
"Verification Checklist": """- [ ] applicable OWASP categories mapped
- [ ] specialized security skills invoked
- [ ] concrete controls identified
- [ ] evidence/tests recorded
- [ ] residual risk documented
- [ ] unsupported security claims avoided""",
},
"security/secrets-management/SKILL.md": {
"Review Procedure": """1. Identify the credential and whether it is actually necessary.
2. Prefer workload identity/short-lived credentials where supported.
3. Review storage, provisioning, access, and least privilege.
4. Review source/build/log/client exposure.
5. Define rotation/revocation and emergency response.
6. Verify CI/CD and audit controls.""",
"Verification Checklist": """- [ ] secret necessity challenged
- [ ] least privilege applied
- [ ] storage/provisioning secure
- [ ] source/build/client/log exposure reviewed
- [ ] rotation/revocation defined
- [ ] CI/CD exposure reviewed
- [ ] incident response path exists""",
},
}

def h2_exists(text, title):
    return re.search(rf"^##\s+{re.escape(title)}\s*$", text, re.M) is not None

changed = 0
missing_files = []

for rel, additions in ADDITIONS.items():
    p = ROOT / rel
    if not p.exists():
        missing_files.append(rel)
        continue
    text = p.read_text(encoding="utf-8")
    original = text
    # Add missing headings at the end; preserve all existing content.
    for title, body in additions.items():
        if not h2_exists(text, title):
            text = text.rstrip() + f"\n\n## {title}\n\n{body.strip()}\n"
    if text != original:
        p.write_text(text, encoding="utf-8")
        changed += 1

print(f"Normalized files: {changed}")
if missing_files:
    print("Missing files:")
    for rel in missing_files:
        print(f"  - {rel}")
    raise SystemExit(1)
