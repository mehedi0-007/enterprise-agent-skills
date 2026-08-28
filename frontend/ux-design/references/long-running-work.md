# Long-Running Work

When work may take seconds/minutes:
acknowledge → queue/process → expose status → notify/reveal completion → recover failure.

Do not make users wait on a request connection when a durable background job better represents the workflow.
