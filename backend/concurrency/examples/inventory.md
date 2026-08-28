# Inventory Race

Unsafe:
1. read stock
2. verify stock >= requested
3. subtract
4. save

Two requests can both pass step 2.

Safer:
- atomic conditional UPDATE, or
- transaction + row lock when additional coordinated writes require it.

Always verify the affected-row count and keep the transaction short.
