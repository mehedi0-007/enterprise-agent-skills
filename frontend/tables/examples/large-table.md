# Large Table

1M invoices.

Do not fetch all rows.

Design:
- server-side filters
- cursor/appropriate pagination
- bounded page size
- deterministic ordering
- selective projection
- database index aligned to common filter/order
- loading/error/empty states
- responsive detail strategy
- measure API + DB + browser performance
