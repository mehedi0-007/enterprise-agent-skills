# V2 Semantic Routing

This patch adds the canonical ownership/routing model for cross-skill consistency.

Files:
- `docs/semantic-routing-matrix.md`
- `docs/semantic-conflict-rules.md`
- `scripts/check-semantic-routing.py`

Run:

```bash
python3 scripts/check-semantic-routing.py
```

Unlike the earlier structural checker, this is intentionally advisory about missing routes: it identifies skills whose cross-layer handoffs deserve review rather than treating every missing mention as a hard implementation error.
