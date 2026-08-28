---
name: ui-design
description: Design clear, intentional web interfaces and component hierarchies. Use when deciding where features/actions belong, choosing UI patterns, defining visual hierarchy, or reviewing whether a screen communicates priority and state effectively.
---

# UI Design

## Mission
Make the interface communicate hierarchy, action priority, state, and recovery paths clearly.

## Before Adding a Feature
Determine:
- user goal
- task frequency
- urgency
- destructive/irreversible nature
- primary vs secondary action
- whether the feature affects the whole page or a local object
- whether the user needs persistent visibility or contextual access
- whether the action belongs in navigation, page content, toolbar, row actions, menu, dialog, or drawer

## Placement Heuristics
Prefer:
- page-level actions in the page header/toolbar
- object-specific actions near the object
- frequent primary actions visible
- infrequent secondary actions contextualized
- destructive actions visually and spatially separated from routine actions when practical

Do not hide essential tasks in obscure menus.

## Choose the Simplest Appropriate Pattern
Use:
- link for navigation
- button for an action
- menu for a compact set of secondary actions
- dialog for focused decisions/confirmation that require attention
- drawer/sheet for contextual work where preserving the current page matters
- full page for substantial workflows, complex editing, or deep context
- tooltip mainly for supplemental explanation, not essential instructions

Do not use a modal for every task.

## Visual Hierarchy
Every screen should make the following reasonably discoverable:
1. What am I looking at?
2. What is the primary task?
3. What is the primary action?
4. What state is the system in?
5. What can I do next?

Use spacing, typography, position, size, grouping, and contrast to establish hierarchy rather than decoration alone.

## Interaction States
Interactive controls should have appropriate:
- default
- hover
- focus
- active/pressed
- disabled or unavailable
- loading
- success/error feedback where applicable

Do not communicate state by color alone.

## Icons
Use icons to support recognition, not replace necessary text. Icon-only controls need accessible names and should be used only when the icon's meaning is well established.

## Destructive Actions
For irreversible/high-impact actions:
- make the consequence clear
- use an explicit action label
- require deliberate confirmation when accidental activation would be costly
- avoid ambiguous labels such as "Continue"
- provide a recovery path when possible

## Empty, Sparse, Dense, Error States
Design all important states, not only the ideal populated screen. Vercel's Web Interface Guidelines explicitly call for empty, sparse, dense, and error states and for screens to provide a next step or recovery path. citeturn194089search0

## Verification
Review:
- hierarchy
- action discoverability
- appropriate component choice
- clear state feedback
- destructive-action safety
- accessible names/focus
- mobile behavior
- empty/error/recovery states
