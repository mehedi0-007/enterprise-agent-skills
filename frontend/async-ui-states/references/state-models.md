# Async State Models

Prefer a small explicit state machine.

Mutation:
`idle → submitting → success/error`

Job:
`idle → submitting → queued → processing → completed/failed/cancelled`

Autosave:
`unsaved → saving → saved/save-failed`

The model should make impossible combinations difficult to represent.
