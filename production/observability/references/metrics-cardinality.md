# Metrics Cardinality

Prefer bounded dimensions:
- route template
- status class
- service
- region
- operation

Avoid:
- request ID
- user ID
- arbitrary URL
- raw exception/message
- unbounded tenant/customer identifiers

Put high-cardinality detail in traces/logs when needed.
