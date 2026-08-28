# UI State Machines

For non-trivial flows, prefer explicit states over contradictory boolean combinations.

Example:
DRAFT → SUBMITTING → PROCESSING → SUCCESS
                         └────────→ FAILED → RETRY

Document valid transitions and invalid transitions.

A UI state should represent server/application reality where the product requires confirmed truth.
