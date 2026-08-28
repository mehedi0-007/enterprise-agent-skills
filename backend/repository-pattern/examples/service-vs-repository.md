# Service vs Repository

## Example

Requirement:
"Cancel an order if it is still cancellable."

Repository:
`getOrderForUpdate(orderId)`

Domain:
`order.cancel(policy, now)`

Application service:
1. authenticate/authorize
2. begin transaction
3. load order with appropriate concurrency control
4. invoke domain transition
5. persist
6. create outbox event if required
7. commit

The repository does not decide whether the order may be cancelled. The domain/application policy does.
