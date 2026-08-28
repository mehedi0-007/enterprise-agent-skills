# Rotation

## Planned
Use overlapping credentials when consumers cannot switch instantaneously.

1. create replacement
2. provision replacement
3. switch consumers
4. verify
5. revoke old

## Emergency
Treat exposed credential as compromised.
Rotate/revoke first when practical, then investigate blast radius and artifacts.

Do not leave old credentials valid indefinitely after successful rotation.
