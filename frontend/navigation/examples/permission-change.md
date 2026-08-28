# Permission Change

User loses access to Billing while on `/billing/invoices/123`.

Expected:
- backend denies protected API access
- UI reflects access change
- sensitive data is not fetched again
- navigation removes/updates Billing
- user gets a useful next destination

Do not rely on hiding Billing in the sidebar.
