# Pagination and Sorting

For large collections:
- bound page size
- use deterministic order
- consider keyset/cursor pagination
- provide indexes that match common access patterns
- restrict arbitrary sorting/filtering

Offset pagination remains valid for some UX patterns; don't replace it without evidence that deep-page/churn behavior matters.
