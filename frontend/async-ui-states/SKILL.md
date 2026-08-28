---
name: async-ui-states
description: Design, implement, and review frontend behavior around asynchronous operations such as data fetching, mutations, uploads, polling, background jobs, optimistic updates, retries, cancellation, and concurrent requests.
---

# Asynchronous UI States — Production Playbook

## Mission
Make async behavior understandable without claiming server-side success before it is confirmed.

## State Model
Simple mutation:
idle → submitting → success/error

Long-running work:
idle → submitting → queued → processing → completed/failed/cancelled

Autosave:
unsaved → saving → saved/save-failed

Prefer explicit mutually exclusive states over contradictory boolean combinations.

## Initial Load vs Refresh
Initial load has no useful data yet, so skeleton/loading UI may be appropriate.
Refresh often has useful existing data. Preserve it when safe and indicate refresh rather than blanking the whole screen.

## Loading Scope
Choose the smallest useful scope:
- page
- section
- row
- button

Do not block unrelated UI for a local operation.

## Mutations
During a mutation:
- communicate progress
- prevent unsafe duplicate activation
- preserve relevant context

On success, reflect confirmed server state.
On failure, preserve recoverable work and provide recovery.

## Duplicate Submission
Duplicates can come from:
- double click/Enter
- browser/client retry
- multiple tabs
- network uncertainty

UI can prevent accidental repeats, but backend idempotency/constraints/concurrency controls remain the real guarantee.

Coordinate with `backend/api-design`, `backend/concurrency`, and `backend/transactions`.

## Retry
Before retrying ask:
1. Could the earlier request have succeeded?
2. Is it safe to repeat?
3. Is the error transient?
4. Could the operation duplicate a side effect?
5. Does the backend expose idempotency/status reconciliation?

Reads are often easy to retry. Non-idempotent writes require stronger protection.

## Automatic Retry
Use bounded attempts, backoff/jitter, and stop on permanent errors.
Respect server rate-limit guidance such as `Retry-After`.
Never retry validation, authorization, or known business conflicts automatically.

## Optimistic UI
Use when:
- likely to succeed
- rollback is clear
- failure is recoverable
- temporary inconsistency is acceptable

Risky:
- payment
- permission changes
- destructive actions
- financial transfers
- irreversible operations

On failure, rollback/reconcile without overwriting newer user intent.

## Out-of-Order Responses
Older async responses can arrive after newer intent.

Example:
search `app` → A
search `apple` → B
B returns first
A returns later

Use cancellation, request sequencing, version checks, or framework data-fetching primitives so stale A cannot overwrite current B.

## Cancellation
Cancellation means the client no longer wants the result. It does not necessarily mean the server-side operation was undone.

For non-idempotent mutations, never tell the user "cancelled" if the server may already have completed the action. Reconcile actual operation state instead.

## Navigation During Work
If work is durable/important, do not tie completion to one page's lifetime.
Long-running operations should generally have a durable server-side job/status model.

## Polling
For durable background jobs define:
- interval/backoff
- stop condition
- terminal states
- maximum duration
- behavior when tab is hidden
- rate-limit handling
- manual refresh

Never poll forever.

## Long-Running Jobs
Typical states:
queued → processing → completed/failed/cancelled

Expose useful progress only when it is trustworthy.
Do not invent precise percentages without real progress.

## Uploads
Model:
selected → validating → uploading → processing → complete/failed

"Upload finished" may only mean bytes arrived. Server-side scanning/transcoding/processing may still be pending.

## Search-as-You-Type
Use debounce when appropriate.
Cancel/supersede obsolete requests.
Handle empty queries intentionally.
Do not create request-per-keystroke traffic without considering backend capacity.

## Autosave
Show:
- unsaved
- saving
- saved
- save failed

Do not show "saved" before the persistence point is confirmed.
Concurrent saves need sequencing/version checks so an old response cannot mark newer work as saved.

## Partial Success
For bulk/multi-item operations represent:
- succeeded
- failed
- pending

Do not turn partial completion into a generic "Success."

## Timeout
A client timeout does not prove server failure.

For possibly non-idempotent mutations:
- query operation status
- use idempotency keys
- inspect current resource state
- reconcile

Do not blindly resubmit.

## Network / Offline
Preserve user work where safe.
Distinguish network failure from validation/business failure.
Do not claim server success without confirmation unless the product intentionally uses an offline-first consistency model.

## Error Mapping
Typical UI intent:
- validation → correct input
- authentication → re-authenticate
- authorization → explain access state
- conflict → reload/merge
- rate limit → wait/retry
- transient server failure → retry/recover
- timeout → treat completion as unknown until reconciled

Use the project's real API contract.

## Stale Data
If old data remains visible during refresh:
- distinguish stale/refreshing from error/empty
- protect fresh local edits from stale responses
- revalidate intentionally

## Review Procedure
For each async interaction ask:
1. What is the initial state?
2. What starts work?
3. What is visible while waiting?
4. Can it be triggered twice?
5. What happens if it is slow?
6. What if response order changes?
7. Can it be cancelled?
8. What if client times out after server success?
9. Is retry safe?
10. What is confirmed success?
11. What is failure?
12. What work is preserved?
13. Is optimistic UI justified?
14. Is work durable?
15. How does the user discover completion later?
16. What if permissions/data change mid-operation?

## Anti-Patterns
- spinner as the only state model
- blind retry after mutation timeout
- unlimited polling
- fake progress
- stale response overwriting newer intent
- treating client abort as server rollback
- full page blank during every refresh
- upload marked complete before server processing
- optimistic high-risk actions without recovery
- partial success hidden

## Verification Checklist
- [ ] state model explicit
- [ ] loading scope appropriate
- [ ] initial vs refresh distinguished
- [ ] success is actually confirmed where required
- [ ] failure/recovery defined
- [ ] duplicate activation reviewed
- [ ] retry safety reviewed
- [ ] timeout semantics understood
- [ ] stale responses handled
- [ ] cancellation semantics defined
- [ ] optimistic update justified
- [ ] polling bounded
- [ ] long-running jobs durable
- [ ] uploads model post-upload processing
- [ ] partial success represented
- [ ] user work preserved
- [ ] permissions/data changes considered
- [ ] slow/failure scenarios tested

## References
- `references/state-models.md`
- `references/retry-timeout.md`
- `references/optimistic-concurrency.md`
- `references/polling-jobs.md`
- `references/testing-async-ui.md`
