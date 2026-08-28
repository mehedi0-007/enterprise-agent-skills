# Autosave Flow

States:
editing → saving → saved
               └→ save-error

Do not show "Saved" before server confirmation.
On failure preserve user edits and make retry visible.
If concurrent edits are possible, define conflict behavior rather than silently overwriting.
