# Bulk Delete

User selects 120 records.

UI:
- show `120 selected`
- explicit destructive action
- confirmation states exact scope
- show processing/progress if asynchronous
- final result says `113 deleted, 7 failed`
- failed rows can be retried if safe

Backend:
- re-check authorization per resource
- enforce concurrency/state rules
- define atomic vs partial semantics
