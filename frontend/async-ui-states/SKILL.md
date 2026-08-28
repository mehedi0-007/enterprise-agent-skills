---
name: async-ui-states
description: Design UI behavior around network requests and asynchronous operations. Use for mutations, saves, uploads, deletes, searches, polling, background processing, and data fetching.
---

# Asynchronous UI States

## Mission
Eliminate uncertainty during asynchronous operations and prevent duplicate or unsafe actions.

## State Model
At minimum consider:
idle
→ loading/submitting
→ success
or
→ error

For longer workflows also consider:
queued
→ processing
→ completed
or
→ failed/retryable

## Duplicate Actions
Prevent duplicate submission when repeated activation could create duplicates or unsafe side effects.
Do not merely disable a button without communicating that work is in progress.

## Loading Feedback
Choose based on scope:
- local button state for one action
- inline spinner for a local region
- skeleton for unknown content loading
- progress for measurable work

Vercel recommends loading states that avoid layout shift and skeletons that mirror final content. citeturn194089search0

## Failure
On failure:
- preserve user input when possible
- explain the problem
- provide a retry or next step
- avoid resetting unrelated state

## Optimistic Updates
Use only when the operation can be safely rolled back and failure is recoverable.
For financial/security/irreversible actions, prefer explicit server confirmation unless the product has a deliberate alternative.

## Polling / Long Jobs
For jobs that outlive the initial request:
- show queued/processing state
- provide progress if meaningful
- allow safe refresh/navigation when practical
- make retry semantics clear

## Race Conditions in UI
Handle out-of-order responses so stale data does not overwrite newer state.
Examples:
- search-as-you-type
- rapidly changing filters
- repeated saves

Use request cancellation, sequence checks, or equivalent mechanisms appropriate to the framework.

## Verification
Test slow network, timeout, retry, duplicate clicks, refresh during request, navigation during request, out-of-order responses, and partial failures.
