# Optimistic UI and Concurrency

Optimistic state is a prediction.

On server success:
reconcile with canonical state.

On failure:
rollback/reconcile.

Prevent older responses from overwriting newer user intent with cancellation, sequence/version checks, or framework primitives.
