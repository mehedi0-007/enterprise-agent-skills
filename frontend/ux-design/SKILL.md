---
name: ux-design
description: Design user flows, interaction behavior, feedback, error recovery, and task completion paths for web applications. Use when adding features, workflows, forms, asynchronous actions, destructive actions, or navigation changes.
---

# UX Design

## Mission
Minimize user uncertainty and help users complete tasks successfully.

## Start With the User Journey
For each feature define:
1. entry point
2. user goal
3. required information
4. decision points
5. system feedback
6. success outcome
7. failure recovery
8. next useful action

## State Model
Most asynchronous workflows should explicitly model:
idle → submitting/loading → success or error

Also consider:
- empty
- partial
- unavailable
- permission denied
- offline/timeout
- stale data
- retrying

## Feedback
After an important user action, the UI should make the resulting state understandable.
Use the smallest feedback mechanism that is sufficient:
- inline status
- button state
- toast for transient confirmation
- banner for persistent/global issue
- dialog for decisions requiring attention

Do not use a toast as the only place to communicate critical information that can disappear before the user reads it.

## Recovery
An error message should help answer:
- what happened?
- what can the user do?
- can they retry?
- will their input be preserved?
- is another action needed?

Vercel's current guidelines emphasize that errors should provide a clear exit/recovery path rather than merely stating that something failed. citeturn194089search0

## Destructive Flow
Before an irreversible action:
- clarify consequence
- provide deliberate confirmation when risk justifies it
- use an explicit destructive label
- avoid surprising navigation
- give clear success/failure feedback

## Avoid Dead Ends
Every screen should leave the user with a useful next step or recovery path.

## Loading
Choose the lightest appropriate loading treatment:
- local spinner for a small local action
- skeleton when the layout is known and content is loading
- progress indicator for measurable long-running work

Skeletons should approximate the final layout to reduce layout shift. Vercel recommends stable skeletons that mirror final content. citeturn194089search0

## Optimistic UI
Use optimistic updates only when:
- failure is recoverable
- rollback behavior is clear
- temporary client state cannot cause harmful side effects

Avoid optimistic behavior for irreversible financial/security actions unless the product explicitly supports it.

## Verification
Walk through the full flow as a user, including slow network, failure, retry, refresh, back navigation, and duplicate activation.
