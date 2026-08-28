# Worker Lag

Worker processes are "healthy" but queue oldest-message age rises.

Correct conclusion:
the process health signal is insufficient.

Check:
- worker throughput
- failure/retry rate
- concurrency
- dependency latency
- queue depth/age

Scale or fix the bottleneck based on evidence.
