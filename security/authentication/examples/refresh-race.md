# Concurrent Refresh Example

Two browser tabs both hold RT7.

A refreshes:
RT7 → invalidated → RT8

B refreshes RT7 immediately after.

Without a concurrency policy, B may appear to be malicious replay even though both requests came from the same user.

Define:
- atomic rotation
- session/grant concurrency behavior
- grace policy if justified
- replay response
- recovery behavior
