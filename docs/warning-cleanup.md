# V2 Warning Cleanup

This patch addresses the warnings from the first repository-wide final audit.

## Routing

It adds explicit handoffs for skills that participate in cross-layer work.

The handoffs intentionally remain short. They identify ownership without duplicating the target skill's implementation guidance.

## OWASP Claim Heuristic

The original heuristic flagged the phrase `OWASP compliant` even when it appeared in an anti-pattern such as "Do not claim OWASP compliant."

The replacement checker ignores explicit negative guidance and only flags positive unsupported compliance claims.

## Validation

Run:

```bash
python3 scripts/add-missing-routing-v2.py
python3 scripts/check-v2-warnings.py
python3 scripts/final-audit.py
```

The final audit should still be PASS, with the warning count reduced substantially.
