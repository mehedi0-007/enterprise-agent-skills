# V2 Final Audit Fix

The previous final auditor flagged the phrase `OWASP compliant` even when the skill was explicitly rejecting that claim.

This replacement makes the heuristic context-aware for negative guidance and anti-pattern examples.

Install the script and rerun:

```bash
python3 scripts/final-audit.py
```
