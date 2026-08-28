# Polling and Jobs

Durable jobs commonly expose:
queued → processing → completed/failed/cancelled

Polling should:
- stop at terminal state
- back off
- respect rate limits
- avoid excessive background traffic
- remain discoverable after navigation
