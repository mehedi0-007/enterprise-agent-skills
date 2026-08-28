# Health and Shutdown

Readiness answers "should traffic be sent here?"
Liveness answers "should this process be restarted?"

Shutdown:
signal → stop accepting new work → finish/abort safely → close resources → flush telemetry → exit.

Do not make liveness fail on every dependency outage.
