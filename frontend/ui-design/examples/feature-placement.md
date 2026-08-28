# Feature Placement Example

Feature:
"Export all invoices."

Reasoning:
- applies to invoice collection → page-level action
- potentially expensive → explicit export control
- likely long-running → async job/status
- sensitive data → authorization
- large result → server-side bounds
- audit useful → observable export event

UI might be:
Page header → `Export invoices`
Then:
Export dialog/drawer → format + filters + scope
Then:
`Queued → Processing → Download ready`
