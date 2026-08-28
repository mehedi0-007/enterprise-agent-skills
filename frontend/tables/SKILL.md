---
name: tables
description: Design data-heavy tables for scanning, sorting, filtering, editing, and responsive use. Use for admin panels, SaaS dashboards, reporting, billing, audit logs, and operational interfaces.
---

# Tables

## Mission
Optimize for the user's task, not maximum information density.

## Before Building
Determine:
- what users compare
- what they scan
- which columns are essential
- whether rows represent actions or just information
- expected row count
- filtering/sorting needs
- whether users need bulk actions
- mobile requirements

## Column Priority
Keep essential identity/context visible.
Move secondary information into:
- expandable details
- row menus
- detail pages
- responsive layouts

Do not make every database field a visible column.

## Sorting
Only offer meaningful sort fields.
Make current sort state clear.
Use deterministic secondary ordering when pagination can otherwise reorder ties.

## Filtering
Expose filters that support real tasks.
Avoid dozens of low-value controls by default.
For complex filter sets consider a dedicated filter UI/drawer.

## Pagination / Infinite Scroll
Use pagination when users need bounded navigation and total/result awareness.
Use infinite scroll when continuous exploration is the task and preserving deep-linking/position is not critical.
For large datasets, combine UI pagination with server-side bounded queries/cursors as appropriate.

## Bulk Actions
Selection state must be clear.
Define behavior when selected records become stale or unavailable.
Destructive bulk actions need clear scope and confirmation when risk warrants it.

## Loading/Empty/Error
Design:
- initial loading
- refreshing
- empty dataset
- no results for current filters
- partial/error state
- permission-limited state

Distinguish "no data exists" from "filters returned no results."

## Verification
Test long values, narrow screens, many rows, slow networks, sorting/filter combinations, selection state, keyboard navigation, and screen-reader table semantics.
