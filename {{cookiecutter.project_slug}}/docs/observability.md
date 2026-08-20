# Observability

Observability is a product contract, not a source of unbounded diagnostic
data. The platform emits a small, safe operational baseline. Product teams add
domain telemetry only when it answers a named operational question and has an
owner, dashboard, alert threshold, and runbook.

## Signal ownership

| Signal | Default behaviour | Purpose |
| --- | --- | --- |
| Logs | Structured JSON in non-debug environments. | Explain a request, task, or failure using stable event names and correlation IDs. |
| Traces | Disabled until `OTEL_EXPORTER_OTLP_ENDPOINT` is set. | Follow sampled HTTP requests and, when enabled, Celery task boundaries. |
| Metrics | Disabled until `METRICS_ENABLED=true`. | Measure request volume, error rate, and latency without inspecting individual requests. |
| Errors | Disabled until `SENTRY_DSN` is set. | Notify on unhandled failures; Sentry performance tracing is deliberately disabled to avoid duplicate tracing. |

Every production deployment must set `DEPLOYMENT_ENVIRONMENT`, `APP_VERSION`,
and `APP_BUILD_SHA`. These values identify a release in logs, traces, errors,
and `/version/` without identifying a user or request.

## Logs and correlation

`X-Request-ID` is accepted only when it is bounded and safe; otherwise the
platform creates a fresh opaque ID and returns it in the response. Request IDs
flow into Celery task logs. When a sampled trace is active, structured logs
also contain `trace_id` and `span_id`.

Use a static dotted event name and named, low-volume fields, for example
`invoice.export.completed` with `invoice_count` and `duration_ms`. Keep the
event name, level, and field names stable so operators can query them. Log an
error with enough non-sensitive context to explain the failed operation, then
let the exception retain its stack trace.

Never log request or response bodies, raw headers, query strings, credentials,
tokens, cookies, email content, unredacted third-party payloads, or regulated
data. The platform redacts known secret-bearing keys before JSON logs and
Sentry events, but callers remain responsible for not constructing unsafe log
events. Redaction is a last line of defence, not permission to log data.

## Traces and errors

Set `OTEL_EXPORTER_OTLP_ENDPOINT` only to a trusted collector endpoint. The
platform uses parent-based head sampling controlled by
`OTEL_TRACE_SAMPLE_RATIO`, defaulting to 10%. Start at that rate, review
collector cost and useful trace coverage, then adjust deliberately. HTTP probe
and metric paths are excluded from traces. Django and optional Celery tracing
are enabled; database and Redis auto-instrumentation are intentionally not,
because SQL statements and cache keys can contain sensitive or high-cardinality
data. Add either only after an ADR documents attribute filtering, cost, and
retention.

Sentry is reserved for redacted error events. It receives the deployment and
release name, does not send default PII, and does not create performance traces.
Do not enable a second tracing backend without an explicit ownership decision.

## Metrics

When enabled, `/metrics/` emits Prometheus/OpenMetrics text and requires:

1. `METRICS_ENABLED=true`.
2. A non-empty `METRICS_TOKEN`, supplied by the scraper as
   `Authorization: Bearer <METRICS_TOKEN>`.
3. Ingress or network-policy protection so the endpoint is reachable only by
   the monitoring system. The token is defence in depth, not a public-endpoint
   authentication scheme.

The platform records these bounded metrics for non-probe application routes:

| Metric | Labels | Use |
| --- | --- | --- |
| `http_server_requests_total` | `method`, Django route pattern, `status_code` | Traffic and error-rate SLOs. |
| `http_server_request_duration_seconds` | `method`, Django route pattern, `status_code` | Latency percentiles and saturation investigation. |

Routes are Django route patterns, never raw request paths; query parameters,
account IDs, UUID values, request IDs, email addresses, and exception messages
must never become labels. Probes and scrape requests do not increment the
application counters. Run one Uvicorn worker per container and scale with
replicas when scraping this in-process registry. Do not increase
`UVICORN_WORKERS` without adding a reviewed Prometheus multiprocess aggregation
strategy.

Baseline alert candidates are a sustained 5xx ratio and a sustained p95 request
latency breach, each scoped by a stable route. Set the thresholds, owner, and
runbook per product; the generic template cannot choose a meaningful user
journey, business objective, or paging policy.

For a product metric, define a static metric name, finite labels, and a
business outcome before adding code. Prefer counters such as
`billing_invoice_exports_total{outcome}` where `outcome` has a short fixed set.
Do not emit a metric for each customer, user, invoice, task ID, URL, error text,
or external identifier. Create a dashboard and alert/runbook in the same
change, then verify the metric appears in a controlled environment.

The implementation follows the official
[OpenTelemetry Python instrumentation guidance](https://opentelemetry.io/docs/languages/python/instrumentation/)
and [Prometheus Python client HTTP exposition guidance](https://prometheus.github.io/client_python/exporting/http/).
