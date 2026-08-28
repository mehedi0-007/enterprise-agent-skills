# Signals and Correlation

Logs → discrete diagnostic events.
Metrics → aggregate behavior/trends.
Traces → request/workflow path.

Use shared trace/request context so one failed user request can be connected to downstream DB/API/worker activity.

OpenTelemetry semantic conventions provide common names for these signals and operations.
