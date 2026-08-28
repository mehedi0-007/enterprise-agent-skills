# Release Strategy

## Rolling
Good default for compatible services with multiple instances.
Risk: old/new versions overlap, so compatibility matters.

## Blue/Green
Keep two environments and switch traffic.
Useful for fast rollback when infrastructure cost is acceptable.

## Canary
Gradually increase traffic to the new version.
Useful when detecting production regressions early matters.

## Feature Flags
Decouple deployment from exposure.
Do not let flags become permanent undocumented branches.

Choose the simplest strategy that matches the blast radius and operational capability.
