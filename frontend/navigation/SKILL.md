---
name: navigation
description: Design information architecture, navigation hierarchy, active states, breadcrumbs, tabs, deep links, and back/forward behavior for web applications. Use when adding pages, sections, resources, or multi-step flows.
---

# Navigation

## Mission
Help users know where they are, where they can go, and how to return.

## Information Architecture
Group features by user mental model and task domain, not by internal database/module structure.

## Choose a Pattern
- primary navigation: top-level destinations
- sidebar: persistent product sections and nested navigation
- tabs: closely related peer views within one context
- breadcrumbs: useful for deep hierarchical location
- contextual menus: local/secondary actions
- command/search palette: fast access across many known destinations/actions

Do not use tabs for unrelated tasks.

## Active State
Current navigation location should be visually and programmatically apparent.
Do not rely on color alone.

## URLs
Important application states should be deep-linkable when practical.
Preserve relevant:
- filters
- tabs
- resource identifiers
- search terms
when doing so improves navigation/reload/share behavior.

## Back/Forward
Avoid hijacking browser navigation.
After a successful mutation, choose navigation deliberately and preserve a clear return path.

## Unsaved Changes
Warn before navigation only when leaving would lose meaningful user work. Do not create confirmation fatigue for trivial changes.

## Mobile
Preserve access to primary destinations while moving secondary navigation into an appropriate compact pattern.

## Verification
Test deep links, refresh, browser back/forward, keyboard navigation, screen readers, nested paths, mobile navigation, and unauthorized destinations.
