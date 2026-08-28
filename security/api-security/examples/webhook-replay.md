# Webhook Replay

Provider sends event `evt_123`.

Attacker or network replay sends the same valid payload again.

Safe handler:
- verifies signature
- checks event ID/deduplication
- returns defined acknowledgement for duplicate
- does not repeat payment/state side effect
