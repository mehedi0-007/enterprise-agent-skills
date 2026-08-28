# V2 Routing Checker Fix

The previous checker was too coupled to its original matching logic.

This replacement:
- uses repository-relative skill paths for expected relationships
- inspects only the `Cross-Skill Routing` section
- accepts explicit backtick references or normal skill-name text inside that section
- reports the exact missing handoff

Run:

```bash
python3 scripts/check-semantic-routing.py
```
