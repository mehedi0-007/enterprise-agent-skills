# Retry and Flakiness

Retry infrastructure operations only when the failure is plausibly transient and repetition is safe.

Do not use retries to mask flaky tests. Flaky tests need diagnosis, isolation, and deterministic synchronization.
