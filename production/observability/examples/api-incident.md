# API Incident

Alert:
5xx rate above SLO.

Investigation:
1. confirm affected route/status
2. check deployment timeline
3. open representative trace
4. find DB timeout spans
5. inspect DB connection pool wait
6. mitigate load/dependency issue
7. verify 5xx and latency recover
8. document root cause

The trace connects API symptom → DB cause.
