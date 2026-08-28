---
name: responsive-design
description: Design interfaces that remain usable across mobile, tablet, laptop, and large screens. Use whenever layout, navigation, tables, dialogs, forms, or content density changes across viewport sizes.
---

# Responsive Design

## Mission
Preserve task completion and information hierarchy across viewport sizes, not merely shrink desktop layouts.

## Start With Constraints
Identify:
- smallest supported viewport
- largest practical viewport
- touch vs pointer interaction
- keyboard use
- safe areas/notches
- content that may wrap/grow unpredictably
- dense data such as tables

## Layout Principles
Prefer:
- CSS flex/grid
- intrinsic sizing
- wrapping
- responsive containers
- content-driven breakpoints

Avoid measuring layout in JavaScript when CSS can solve it.

Vercel's guidelines explicitly recommend letting the browser size and flow content rather than measuring layout in JavaScript, and checking mobile, laptop, and ultra-wide layouts. citeturn194089search0

## Breakpoints
Choose breakpoints based on where the content/layout actually stops working, not only standard device widths.

## Mobile
On smaller screens:
- preserve primary actions
- reduce secondary visual noise
- move complex secondary actions into menus when appropriate
- avoid horizontal scrolling unless the data itself requires it
- preserve readable touch targets
- ensure dialogs/forms remain usable with on-screen keyboards

## Tables
Do not blindly shrink a complex desktop table until text becomes unreadable.
Choose deliberately:
- horizontal scroll
- column prioritization
- row/card transformation
- responsive detail views
depending on task needs.

## Large Screens
Do not stretch readable content across the entire viewport without reason. Use max-width/container strategies when appropriate.

## Safe Areas
Account for device insets when fixed UI could overlap system areas.

## Verification
Test representative mobile, desktop, and wide layouts. Check zoom, long text, localization, keyboard, touch, and reduced motion.
