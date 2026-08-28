---
name: accessibility
description: Build and review accessible web interfaces using semantic HTML, keyboard interaction, visible focus, labels, accessible names, status messages, and robust state communication. Use for every interactive UI feature.
---

# Accessibility

## Mission
Make the interface operable and understandable across keyboard, screen reader, low-vision, and other assistive-technology use cases.

## Prefer Native Semantics
Use real:
- button
- link
- input
- select
- textarea
- form
- heading
- table
- list

before custom ARIA widgets.

A native `<button>` already has interaction and accessibility semantics that custom clickable `<div>` elements do not. MDN also recommends preserving visible focus and using `:focus-visible` when styling. citeturn814403search8

## Keyboard
All important flows must be keyboard-operable.
Check:
- Tab order
- Enter/Space activation
- Escape behavior for dismissible overlays
- arrow-key behavior for complex widgets when required
- focus movement after dialogs/errors/navigation

Vercel's guidelines require keyboard-operable flows and visible, unobscured focus. citeturn194089search0

## Focus
Every focusable element needs a visible focus indication.
Do not use `outline: none` without a strong replacement. W3C identifies removing or obscuring the visible focus indicator as a failure technique. citeturn814403search25

## Labels and Names
Form controls need accessible names.
Icon-only buttons need accessible labels.
Do not rely on placeholder text as the sole label.

## Error Communication
Errors should be associated with their controls and communicated in text, not only by color.
Important status changes should be exposed programmatically where appropriate; MDN's accessibility guidance covers status messages and programmatic name/role/value. citeturn814403search5

## Disabled States
Use native `disabled` for actual native form controls when interaction should be removed. Remember that disabled controls are not focusable and do not participate in form submission. citeturn814403search0
Use `aria-disabled` only when the control needs to remain discoverable/focusable and the application also enforces the disabled behavior. citeturn814403search1

## Motion
Respect `prefers-reduced-motion`. Avoid motion that is required to understand the interface.

## Color
Do not use color as the sole indicator of error, status, selection, or success.
Provide text, shape, icon, or other redundant cues.

## Dialogs
A modal dialog should:
- move focus appropriately
- trap/manage focus while open as required
- have an accessible name
- restore focus appropriately on close
- allow keyboard dismissal when the interaction pattern permits

## Verification
Run keyboard-only testing, inspect accessibility tree/name/role/value, test focus, test zoom, test error/status announcements, and use automated accessibility tooling where available.
