# Logic Placement Examples

## Controller
`parse request → call CreateOrder → map result`

## Application Service
`load customer → authorize operation → invoke domain rule → persist → coordinate outbox`

## Domain
`Order.canCancel(now, actorContext)` or a domain policy that enforces an invariant.

## Repository
`findOpenOrdersForCustomer(customerId)`

## Infrastructure
`StripePaymentGateway.charge(...)`

## Rule
Place behavior where it remains correct if the transport changes from HTTP to queue, CLI, or scheduled execution.
