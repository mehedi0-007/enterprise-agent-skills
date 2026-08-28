---
name: ux-design
description: Design and review user flows, task completion, feedback, recovery, async interactions, destructive actions, and navigation behavior for web applications. Use when adding or changing workflows, forms, mutations, uploads, long-running operations, or user-facing error handling.
---

# UX Design — Production Playbook

## 1. Mission

UX design should reduce uncertainty and help users complete meaningful tasks with minimal unnecessary effort.

For every important interaction, the user should be able to understand:
- where they are
- what they can do
- what the system expects
- whether their action was accepted
- whether work is still happening
- what happened
- what they can do next

A production workflow is not just the happy path.

---

## 2. Activation

Use when:
- adding a new user workflow
- changing navigation
- adding a form
- adding asynchronous mutation
- adding destructive operations
- adding upload/import/export
- designing onboarding
- handling errors/retries
- adding optimistic UI
- designing empty/loading/processing states

---

## 3. Start With the User Goal

Before choosing UI:
1. identify the user's goal
2. identify what information they need
3. identify decisions they must make
4. identify system actions
5. identify success criteria
6. identify failure/recovery
7. identify whether the task can be interrupted/resumed

Do not design screens independently of the task flow.

---

## 4. Model the User Journey

A useful flow:

```text
Entry
  ↓
Context
  ↓
Input/decision
  ↓
Confirmation if risk warrants
  ↓
Action accepted
  ↓
Processing/loading
  ↓
Success
```

Failure branches must also exist:

```text
                  ┌→ validation error
                  │
Input → submit ───┼→ permission error
                  │
                  ├→ dependency failure
                  │
                  └→ timeout/offline
```

Each failure needs an appropriate recovery path.

---

## 5. State Machine Thinking

For non-trivial interactions, explicitly define states.

Example:

```text
DRAFT
  ↓ submit
SUBMITTING
  ↓
PROCESSING
  ├→ SUCCESS
  └→ FAILED
       ↓ retry
    SUBMITTING
```

Do not invent UI state by scattering booleans such as:

```text
isLoading
isSaving
isProcessing
hasError
isDone
```

without understanding whether contradictory combinations are possible.

Where the state machine is meaningful, make the state transitions explicit in application logic.

---

## 6. Feedback Timing

Feedback should match the duration and importance of the action.

### Immediate/frequent
Use local control feedback.

Example:
- button pressed state
- inline validation

### Normal request
Show loading state if the user would otherwise wonder whether the action started.

### Long-running operation
Show processing state and progress when meaningful.

### Critical operation
Give explicit confirmation of the final outcome.

Do not show a spinner for every tiny interaction if it adds more noise than clarity.

---

## 7. Loading Strategy

Choose the smallest correct loading scope.

### Local mutation
Update only the affected action/control.

### Content fetch
Use skeleton or local loading state when content structure is known.

### Long job
Show queued/processing/completed/failed states.

Vercel's current Web Interface Guidelines emphasize avoiding layout shift and using skeletons that correspond to the final content structure. citeturn194089search0

Avoid:
- freezing the entire page for a small request
- layout jumps
- spinner overlays that obscure unrelated work

---

## 8. Success Feedback

After successful action:
- show the resulting state
- confirm important outcomes
- provide next useful action

For persistent state changes, the resulting UI should usually reflect the new state rather than relying only on a toast.

Bad:
```text
Saved!
```
while the screen still shows stale values.

Better:
```text
server success
   ↓
state updated
   ↓
UI reflects saved state
```

---

## 9. Error Design

Every important error should answer, as appropriate:
1. What happened?
2. What does it mean?
3. What can the user do now?
4. Can they retry?
5. Will their work be preserved?

Different errors deserve different UI:

### Validation
Inline/field-level guidance.

### Permission
Explain access limitation and next action.

### Not found
Explain missing resource and recovery/navigation.

### Conflict/stale data
Explain that the resource changed and offer reload/merge.

### Timeout/network
Preserve input and offer retry/reconnect.

### Server failure
Explain safely and provide retry or support path.

Do not expose raw backend exception text.

---

## 10. Preserve User Work

When a submission fails for a recoverable reason:
- preserve entered data
- preserve filters/search state where practical
- preserve selections when safe
- do not force users to re-enter everything

Reset only the part that cannot safely be retained.

---

## 11. Retry

A retry control should be shown when retry can plausibly succeed.

Before allowing retry ask:
- Is the operation safe to repeat?
- Is it idempotent?
- Could the first request have succeeded?
- Can retry duplicate the side effect?
- Does the backend have idempotency protection?

For unsafe operations, the UI should not encourage blind repeated submission.

Coordinate with the backend `api-design`, `transactions`, and `concurrency` skills.

---

## 12. Optimistic UI

Optimistic UI shows expected success before server confirmation.

Use when:
- the action is likely to succeed
- rollback is straightforward
- failure is recoverable
- temporary inconsistency is acceptable

Good:
- toggling a low-risk preference
- local list reordering

Risky:
- payment
- permission change
- destructive deletion
- legal/compliance action
- irreversible resource mutation

If optimistic UI is used:
1. update local state
2. send request
3. confirm
4. rollback/reconcile on failure
5. prevent stale responses from overwriting newer state

Do not create irreversible user-visible outcomes before the server confirms them.

---

## 13. Double Submission

Repeated clicking can create duplicates.

For important mutations:
- show in-progress state
- prevent duplicate activation where appropriate
- use backend idempotency for operations that need it

The UI control alone is not the concurrency guarantee.

---

## 14. Race Conditions in UI

Asynchronous responses can arrive out of order.

Example:

```text
search "app" → request A
search "apple" → request B
                 ↓
B finishes first
                 ↓
A finishes later
```

A naive UI may show results for "app" after "apple."

Use:
- request cancellation
- sequence/version checks
- framework-supported data-fetching concurrency control

Apply similar thinking to:
- filters
- auto-save
- rapid navigation
- repeated edits

---

## 15. Destructive Flows

Use a risk-based approach.

### Low-risk/reversible
Direct action + undo may be ideal.

### Medium-risk
Clear confirmation may be appropriate.

### High-risk/irreversible
Use deliberate confirmation and explicit consequence.

The confirmation should identify:
- object
- scope
- consequence
- reversibility

Example:

```text
Delete 42 customer records?

This cannot be undone.

[Cancel] [Delete 42 records]
```

Avoid:
```text
Are you sure?
[Yes] [No]
```

The user's decision should be understandable from the dialog itself.

---

## 16. Confirmation Fatigue

Do not ask for confirmation on everything.

Excessive dialogs train users to dismiss them without reading.

Prefer:
- undo for reversible actions
- clear inline consequences
- deliberate button placement
- confirmation only when the risk justifies interruption

---

## 17. Undo

Undo is often better than confirmation when:
- the action is reversible
- undo is technically reliable
- the user is likely to make mistakes
- the system can retain enough state for recovery

Examples:
- archive
- remove from list
- move item
- delete draft with recoverable trash

Do not offer a misleading undo if the external side effect already occurred and cannot actually be reversed.

---

## 18. Empty States

Distinguish:

### First-use empty
The user has never created anything.

Show:
- explanation
- value
- primary first action

### Filtered empty
Data exists, but current filters match nothing.

Show:
- current filter context
- clear/reset filters
- optionally broaden search

### Permission-limited empty
Data may exist but the user cannot see it.

Do not falsely claim "there is no data" when the real reason is access restriction.

---

## 19. Onboarding

Do not make onboarding a tour of every UI element unless necessary.

Good onboarding:
- gets the user to first value quickly
- asks only necessary information
- introduces concepts in context
- provides clear next action

Avoid:
- long multi-step tutorials before value
- blocking dialogs for optional education
- asking for information before the product needs it

---

## 20. Multi-Step Workflows

For long forms/wizards:
- make progress understandable
- preserve previous input
- allow review
- validate at useful boundaries
- define what happens if user leaves
- avoid restarting unexpectedly
- make navigation back safe

If a workflow can be paused, define save/resume behavior.

---

## 21. Autosave

Autosave can reduce loss, but it introduces state ambiguity.

Define:
- what is saved
- when it saves
- whether save is server confirmed
- conflict behavior
- recovery after refresh/navigation
- visible saved/saving/error status

Do not imply "Saved" based solely on local state.

---

## 22. Navigation After Mutation

After successful mutation, decide whether to:
- remain on page
- navigate to created resource
- return to list
- close dialog/drawer

Base this on user workflow.

Avoid surprising navigation after every mutation.

Preserve browser back/forward semantics.

---

## 23. Permissions and UX

Do not hide every unavailable feature automatically.

Possible treatments:
- hide truly irrelevant features
- disable when the feature is relevant but unavailable
- explain permission requirement when discoverability helps
- offer request-access flow if the product supports it

Never rely on UX hiding as authorization; use server-side enforcement.

---

## 24. Long-Running Operations

For imports/exports/generation:
- acknowledge request
- show queued/processing state
- show progress if measurable
- allow safe navigation
- notify/reveal completion
- handle failure/retry
- define cancellation where possible

Do not keep users staring at a spinner for several minutes when the task can be represented as a background job.

---

## 25. Offline / Network Failure

Where offline/network interruption is plausible:
- distinguish network failure from validation failure
- preserve local work when safe
- make retry visible
- avoid losing edits
- define whether actions can be queued locally

Do not claim a mutation succeeded without server confirmation unless the product intentionally supports an offline-first consistency model.

---

## 26. Accessibility

Every flow must remain usable with:
- keyboard
- screen reader where applicable
- zoom/reflow
- reduced motion

Important dynamic state changes should be communicated accessibly.

Use `frontend/accessibility` for detailed implementation review.

---

## 27. Cross-Layer Contract

UX behavior must agree with backend semantics.

Examples:

```text
API returns 409 conflict
        ↓
UI should not display "server down"
        ↓
show stale/conflict recovery
```

```text
API returns 202
        ↓
UI should represent processing
        ↓
not pretend operation completed
```

```text
API supports idempotency
        ↓
UI can safely retry according to contract
```

Use `engineering/cross-layer-review` for complete feature reviews.

---

## 28. Testing Strategy

Test flows with:
- slow network
- offline/timeout
- duplicate clicks
- refresh during request
- browser back
- stale data
- concurrent edits
- permission changes
- partial failure
- empty data
- very large data
- mobile viewport
- keyboard navigation

Test state transitions, not only final screenshots.

---

## 29. Review Procedure

For a new workflow ask:

1. What is the user's goal?
2. What is the happy path?
3. What can fail?
4. What state exists while work is happening?
5. What state is shown after success?
6. What happens after timeout?
7. Can the user safely retry?
8. Can the request duplicate a side effect?
9. Is input preserved?
10. Can responses arrive out of order?
11. What happens on refresh/back?
12. Is confirmation justified?
13. Is there an undo/recovery path?
14. What is the empty state?
15. What happens when permissions change?
16. Can the workflow be completed accessibly?

---

## 30. Anti-Patterns

### Happy Path Only
No designed failure/recovery behavior.

### Spinner Forever
No meaningful processing state.

### Toast-Only Success
Persistent state remains visually stale.

### Blind Retry
Could duplicate an unsafe side effect.

### Optimistic Everything
Financial/security/destructive actions appear successful before confirmation.

### Confirmation Everywhere
Users stop reading dialogs.

### Lost Form State
Network failure forces complete re-entry.

### Stale Async Response
Older request overwrites newer state.

### Empty = Error
No data treated as system failure.

### Permission = Hidden
Users cannot understand why capability is unavailable.

### Backend Semantics Ignored
202/409/429 treated like success or generic failure.

---

## 31. Verification Checklist

- [ ] user goal is explicit
- [ ] happy path defined
- [ ] failure states defined
- [ ] loading/processing state defined
- [ ] success state reflects actual server result
- [ ] retry safety reviewed
- [ ] duplicate actions handled
- [ ] stale/out-of-order responses handled
- [ ] input preserved on recoverable failure
- [ ] destructive action risk assessed
- [ ] confirmation/undo choice justified
- [ ] empty/no-result states defined
- [ ] long-running work represented appropriately
- [ ] navigation/back behavior tested
- [ ] permission changes considered
- [ ] accessibility considered
- [ ] cross-layer API semantics match UI behavior

## References
- `references/state-machines.md`
- `references/error-recovery.md`
- `references/optimistic-ui.md`
- `references/destructive-actions.md`
- `references/long-running-work.md`

## Cross-Skill Routing
For network/server lifecycle behavior, defer to `frontend/async-ui-states`.
For API contract semantics, coordinate with `backend/api-design`.
For forms and tables, use the specialized frontend skills rather than duplicating their detailed interaction rules.
