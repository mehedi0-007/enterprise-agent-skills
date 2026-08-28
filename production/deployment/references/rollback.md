# Rollback vs Forward Fix

Code rollback is safe only if the current schema/config/data remains compatible.

Feature disable is useful when behavior is isolated behind a flag.

Forward fix is often safer after irreversible migrations or external side effects.

Never claim rollback restores external side effects automatically.
