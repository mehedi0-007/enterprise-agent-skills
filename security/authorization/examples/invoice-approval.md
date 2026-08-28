# Invoice Approval

Requirement:
A finance manager can approve invoices in their organization, but cannot approve their own invoice request.

Decision:
1. authentication identifies manager
2. tenant membership/role grants approval capability
3. invoice tenant must match trusted tenant
4. invoice state must be PENDING
5. manager cannot equal requester
6. optional amount threshold may further restrict approval
7. protected transition should be concurrency-safe

Do not encode all of this as `role == FINANCE_MANAGER`.
