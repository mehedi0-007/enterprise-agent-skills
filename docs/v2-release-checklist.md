# V2 Release Checklist

## Required
- [ ] `final-audit.py` returns PASS
- [ ] Git working tree is understood
- [ ] all intended skill changes are committed
- [ ] remote branch is pushed
- [ ] README describes skill layout and usage
- [ ] no secrets are present
- [ ] generated ZIP/temp files are not accidentally committed

## Recommended
- [ ] run the audit in a clean clone
- [ ] inspect the final diff
- [ ] tag the v2 release
- [ ] keep changelog/release notes
- [ ] periodically rerun the audit as skills evolve

## Final Quality Standard

A skill should improve agent decisions, not merely increase documentation length.

Each skill should:
1. activate on a clear class of task
2. define decision guidance
3. identify failure modes
4. hand off adjacent concerns
5. provide verification
6. avoid unsupported absolute claims
