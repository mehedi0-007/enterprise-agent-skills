# Inventory Reservation

Invariant:
inventory cannot become negative.

Safer approach:
1. Begin transaction if additional writes must be atomic.
2. Perform a conditional update that decreases inventory only when enough stock exists, or lock the inventory row if the workflow requires serial read/decision/write behavior.
3. Check affected-row count.
4. Create reservation/order state in the same transaction if required.
5. Commit.
6. Do not call external payment/email systems while holding the DB transaction unless justified.
