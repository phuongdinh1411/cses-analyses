---
layout: simple
title: "Design an Observability Platform"
permalink: /system_design/design-observability-platform
---

# Design an Observability Platform

An observability platform collects, stores, correlates, and queries the three pillars of system health: **metrics**, **logs**, and **traces**. This guide focuses on the OpenTelemetry → Grafana / ELK stack that modern production systems use.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Back of the Envelope Estimation](#back-of-the-envelope-estimation)
3. [The Three Pillars](#the-three-pillars)
4. [High-Level Design](#high-level-design)
5. [OpenTelemetry Deep Dive](#opentelemetry-deep-dive)
6. [Metrics Stack (Prometheus + Grafana)](#metrics-stack-prometheus--grafana)
7. [Logging Stack (ELK)](#logging-stack-elk)
8. [Tracing Stack (Jaeger / Tempo)](#tracing-stack-jaeger--tempo)
9. [Alerting](#alerting)
10. [Database Design](#database-design)
11. [Handling Failures](#handling-failures)
12. [Trade-offs](#trade-offs)
13. [Interview Tips](#interview-tips)

---

## Requirements

### Functional Requirements

- **Metrics**: Collect numeric time-series data (CPU, latency, error rate); query and visualize
- **Logs**: Ingest structured/unstructured log lines; full-text search
- **Traces**: Track a request across service boundaries; show call graph and latency breakdown
- **Dashboards**: Visualize metrics and correlate with logs/traces
- **Alerting**: Fire alerts when metrics cross thresholds; route to on-call
- **Correlation**: From a slow trace, jump to the related logs; from an alert, jump to the trace

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Write throughput** | 1M+ metric data points/min; 100K+ log lines/sec |
| **Query latency** | Dashboard queries < 1s for recent data |
| **Retention** | Metrics: 15 days full resolution + 1 year downsampled; Logs: 30 days |
| **Availability** | 99.9% — observability can't be the thing that fails during an incident |
| **Cardinality** | Handle high-cardinality labels (user IDs, trace IDs) without OOM |

### Out of Scope

- Application performance management (APM) with profiling
- Security information and event management (SIEM)
- Business analytics / data warehousing

---

## Back of the Envelope Estimation

```
Instrumented services: 100 microservices
Metrics per service:   ~100 metrics × 30s scrape interval = 200 data points/min/service
Total metric ingestion: 100 × 200 = 20,000 data points/min = ~333/sec

Logs per service:      ~1,000 lines/sec at peak
Total log ingestion:   100 × 1,000 = 100,000 lines/sec
Log line size:         ~500 bytes
Log throughput:        50 MB/sec = 4.3 TB/day

Traces per service:    ~100 req/sec × 5 spans/req = 500 spans/sec
Total trace ingestion: 100 × 500 = 50,000 spans/sec
Span size:             ~1 KB
Trace throughput:      50 MB/sec

Storage (30 days logs): 4.3 TB/day × 30 = ~130 TB
  → After compression (10:1): ~13 TB
```

---

## The Three Pillars

```
                     ┌──────────────────┐
                     │    Observability  │
                     └──────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
     ┌────▼────┐      ┌─────▼────┐      ┌────▼────┐
     │ Metrics │      │   Logs   │      │ Traces  │
     └────┬────┘      └─────┬────┘      └────┬────┘
          │                 │                 │
     "What is broken?"  "Why is it    "Where is it slow?"
      (aggregated)       broken?"       (per-request)
                         (raw events)
```

| Pillar | Data type | Use case | Storage |
|--------|-----------|----------|---------|
| **Metrics** | Numeric time-series | Dashboards, alerting, capacity planning | Prometheus / Thanos |
| **Logs** | Text events with timestamp | Root cause analysis, audit trail | Elasticsearch |
| **Traces** | Spans with parent-child links | Latency breakdown, service map | Jaeger / Grafana Tempo |

---

## High-Level Design

```
┌──────────────────────────────────────────────────────────────────┐
│                    Instrumented Services                          │
│                  (OTel SDK auto-instrumented)                     │
└─────────────────────────┬────────────────────────────────────────┘
                          │ OTLP (gRPC/HTTP)
                ┌─────────▼──────────┐
                │   OTel Collector   │  ← central routing / batching
                │  (agent per host)  │
                └──┬──────┬──────┬───┘
                   │      │      │
         ┌─────────▼┐ ┌───▼──┐ ┌▼──────────┐
         │Prometheus │ │Loki/ │ │  Jaeger/  │
         │  remote  │ │ ES   │ │  Tempo    │
         │  write   │ │(logs)│ │ (traces)  │
         └─────────┬┘ └───┬──┘ └┬──────────┘
                   │      │     │
              ┌────▼──────▼─────▼────┐
              │       Grafana        │  ← unified query/viz/alert
              │  (dashboards, alerts)│
              └──────────┬───────────┘
                         │
                  ┌──────▼───────┐
                  │ Alertmanager │ → PagerDuty / Slack
                  └──────────────┘
```

---

## OpenTelemetry Deep Dive

OpenTelemetry (OTel) is the **vendor-neutral instrumentation standard** — write once, export to any backend.

### Auto-instrumentation (zero code change)

```python
# Install once per service; instruments FastAPI, SQLAlchemy, aiohttp automatically
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install

# Run service with auto-instrumentation
opentelemetry-instrument \
  --service_name=prices-api \
  --exporter_otlp_endpoint=http://otel-collector:4317 \
  python -m uvicorn app:app
```

### Manual instrumentation for custom spans

```python
from opentelemetry import trace, metrics
from opentelemetry.trace import SpanKind

tracer = trace.get_tracer("prices-api")
meter = metrics.get_meter("prices-api")

# Custom counter
requests_counter = meter.create_counter(
    "api.requests.total",
    description="Total API requests",
)

# Custom histogram (for latency distribution)
latency_histogram = meter.create_histogram(
    "api.request.duration",
    unit="ms",
)

@app.get("/prices/{symbol}")
async def get_prices(symbol: str):
    with tracer.start_as_current_span(
        "get_prices",
        kind=SpanKind.SERVER,
        attributes={"symbol": symbol},
    ) as span:
        start = time.monotonic()
        try:
            result = await db_fetch_prices(symbol)
            span.set_attribute("result.count", len(result))
            requests_counter.add(1, {"endpoint": "get_prices", "status": "success"})
            return result
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            requests_counter.add(1, {"endpoint": "get_prices", "status": "error"})
            raise
        finally:
            latency_histogram.record(
                (time.monotonic() - start) * 1000,
                {"endpoint": "get_prices"},
            )
```

### OTel Collector configuration

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024
  memory_limiter:
    check_interval: 1s
    limit_mib: 1000
  resource:
    attributes:
      - key: deployment.environment
        value: production
        action: insert

exporters:
  prometheusremotewrite:
    endpoint: http://prometheus:9090/api/v1/write
  loki:
    endpoint: http://loki:3100/loki/api/v1/push
  otlp/jaeger:
    endpoint: http://jaeger:4317

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch, memory_limiter]
      exporters: [prometheusremotewrite]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [loki]
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/jaeger]
```

---

## Metrics Stack (Prometheus + Grafana)

### Prometheus data model

```
metric_name{label1="value1", label2="value2"} <value> <timestamp>

Example:
  http_requests_total{method="GET", endpoint="/prices", status="200"} 42304 1700000000

Metric types:
  Counter    — monotonically increasing (requests, errors)
  Gauge      — can go up or down (memory usage, queue depth)
  Histogram  — samples observed values into buckets (latency distribution)
  Summary    — pre-computed quantiles (less flexible than histogram)
```

### PromQL examples

```promql
# Request rate over 5 minutes
rate(http_requests_total{service="prices-api"}[5m])

# Error rate percentage
100 * sum(rate(http_requests_total{status=~"5.."}[5m]))
    / sum(rate(http_requests_total[5m]))

# p99 latency (from histogram)
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket{service="prices-api"}[5m])
)

# Consumer lag across all partitions
sum by (topic) (kafka_consumer_group_lag{group="prices-consumer"})
```

### Cardinality problem

```
High cardinality = many unique label value combinations
BAD labels:  user_id, trace_id, request_id  (millions of unique values → OOM)
GOOD labels: status_code, method, endpoint, service, region

Rule: if a label value is unbounded, don't put it in a metric label.
  → Use traces for per-request data instead.
```

---

## Logging Stack (ELK)

### Elasticsearch

ELK = **E**lasticsearch + **L**ogstash (or Fluentd/Vector) + **K**ibana

```
Index strategy:
  logs-prices-api-2024.01.15   (daily indices, auto-rolled via ILM)

Index Lifecycle Management (ILM):
  Hot tier   (0–7 days):   SSD, full replica, frequent writes
  Warm tier  (7–30 days):  HDD, read-only, compressed
  Cold tier  (30–90 days): Frozen, on-demand retrieval
  Delete     (90+ days):   Automatic deletion
```

### Structured logging (JSON)

```python
import structlog
import logging

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),    # → parseable by Elasticsearch
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger()

async def process_order(order_id: str):
    log = structlog.get_logger().bind(order_id=order_id, service="orders")
    try:
        log.info("processing_order", amount=order.amount, symbol=order.symbol)
        result = await submit_to_exchange(order)
        log.info("order_submitted", exchange_id=result.id, latency_ms=result.latency)
    except Exception as e:
        log.error("order_failed", error=str(e), exc_info=True)
        raise
```

### Elasticsearch query examples (Kibana/OpenSearch)

```json
// Find all errors for a service in the last hour
{
  "query": {
    "bool": {
      "must": [
        { "term": { "level": "error" } },
        { "term": { "service": "prices-api" } },
        { "range": { "@timestamp": { "gte": "now-1h" } } }
      ]
    }
  },
  "sort": [{ "@timestamp": { "order": "desc" } }]
}

// Aggregate error count by endpoint
{
  "aggs": {
    "by_endpoint": {
      "terms": { "field": "endpoint.keyword" },
      "aggs": {
        "error_count": { "filter": { "term": { "level": "error" } } }
      }
    }
  }
}
```

---

## Tracing Stack (Jaeger / Tempo)

### Trace anatomy

```
Trace: one complete request across services
  ├── Span: prices-api   GET /prices/AAPL      [0ms ────────── 85ms]
  │     ├── Span: db-pool  acquire connection   [1ms ─ 3ms]
  │     ├── Span: postgres SELECT from ticks    [3ms ──────── 70ms]  ← slow!
  │     └── Span: serialize JSON               [70ms ─ 83ms]

Span attributes (key-value):
  http.method = "GET"
  http.url = "/prices/AAPL"
  db.statement = "SELECT * FROM ticks WHERE symbol = $1 LIMIT 100"
  db.rows_returned = 100

Span events (timestamped within a span):
  t=10ms: "cache miss"
  t=11ms: "query started"
```

### Sampling strategies

```
Problem: 100% trace sampling at 10,000 req/sec = too much storage

Options:
  Head-based (at ingestion point):
    - Probabilistic: sample 1% of all requests (cheap, but misses rare errors)
    - Rate-limiting: sample N traces/sec regardless of traffic

  Tail-based (at collector, after trace completes):
    - Sample 100% of error traces
    - Sample 100% of slow traces (p99 > threshold)
    - Sample 1% of fast, successful traces
    → Best coverage, higher collector cost

OTel Collector tail sampling config:
  processors:
    tail_sampling:
      decision_wait: 10s
      policies:
        - name: errors
          type: status_code
          status_code: {status_codes: [ERROR]}
        - name: slow-traces
          type: latency
          latency: {threshold_ms: 500}
        - name: probabilistic-1pct
          type: probabilistic
          probabilistic: {sampling_percentage: 1}
```

---

## Alerting

### Alert design principles

```
Alert on SYMPTOMS, not causes:
  ✅ "User-facing error rate > 1% for 5 minutes"
  ❌ "CPU on host-3 > 80%"  (may not affect users at all)

The four golden signals (Google SRE):
  Latency   — how long requests take (p50, p99)
  Traffic   — how many requests per second
  Errors    — rate of failed requests
  Saturation— how full is the system (queue depth, memory %)
```

### Prometheus alert rules

```yaml
# alerts.yml
groups:
  - name: prices-api
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5..", service="prices-api"}[5m]))
            /
            sum(rate(http_requests_total{service="prices-api"}[5m]))
          ) > 0.01
        for: 5m
        labels:
          severity: critical
          team: trading-infra
        annotations:
          summary: "Error rate {{ $value | humanizePercentage }} on prices-api"
          runbook: "https://wiki/runbooks/prices-api-errors"

      - alert: HighP99Latency
        expr: |
          histogram_quantile(0.99,
            rate(http_request_duration_seconds_bucket{service="prices-api"}[5m])
          ) > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency {{ $value }}s on prices-api (threshold: 500ms)"

      - alert: KafkaConsumerLagHigh
        expr: |
          sum by (topic, group) (kafka_consumer_group_lag) > 10000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Consumer group {{ $labels.group }} is {{ $value }} messages behind"
```

---

## Database Design

### Prometheus time-series storage

```
Prometheus uses a custom TSDB (time-series database):
  - In-memory chunks (2 hours of data)
  - Periodically flushed to disk as compressed blocks
  - Each block: 2-hour window, immutable after sealing
  - Compaction: merges small blocks, applies downsampling

For long-term storage:
  Thanos: uploads blocks to S3; global query layer across multiple Prometheus instances
  Cortex / Mimir: horizontally scalable, multi-tenant Prometheus
```

### Elasticsearch index design

```json
// Explicit mapping for logs index (better than dynamic mapping for production)
{
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "level":      { "type": "keyword" },
      "service":    { "type": "keyword" },
      "trace_id":   { "type": "keyword" },
      "span_id":    { "type": "keyword" },
      "message":    { "type": "text", "analyzer": "standard" },
      "error":      {
        "properties": {
          "type":    { "type": "keyword" },
          "message": { "type": "text" }
        }
      }
    }
  }
}
```

---

## Handling Failures

### What if the OTel Collector is down?

```
SDK-side buffering:
  - OTel SDKs buffer spans/metrics in memory (configurable size)
  - Retry with exponential backoff if collector unreachable
  - Drop when buffer full (observability data is not business-critical)

Collector redundancy:
  - Run as DaemonSet (one per node) so no single point of failure
  - Local file exporter as fallback: write to disk, tail and forward when collector recovers
```

### Backpressure handling

```
Elasticsearch can't keep up → Logstash/Vector buffer on disk → service logs go to file
Prometheus scrape too slow → increase scrape timeout; reduce cardinality

Never let observability failure affect the instrumented service:
  - All OTel writes are fire-and-forget (async, non-blocking)
  - Errors in telemetry export are swallowed or logged to stderr only
```

---

## Trade-offs

### ELK vs Loki for logs

| | ELK (Elasticsearch) | Loki (Grafana) |
|---|---|---|
| **Query model** | Full-text search + aggregations | Label-based (like Prometheus, no full-text index) |
| **Cost** | High (indexes everything) | Low (only indexes labels) |
| **Query speed** | Fast (full inverted index) | Slower (log-line scan) |
| **Choose when** | Need full-text search, complex aggregations | Cost matters; already using Grafana; logs are structured |

### Prometheus vs managed metrics

| | Self-hosted Prometheus | Grafana Cloud / Datadog |
|---|---|---|
| **Control** | Full | Limited |
| **Ops burden** | High (you manage HA, storage, upgrades) | None |
| **Cost** | Infra cost only | Per-series pricing (can get expensive) |
| **Choose when** | Strict data residency; large scale | Smaller team; want out-of-box integrations |

### Sampling trade-off

| | 100% sampling | Tail-based 10% | Head-based 1% |
|---|---|---|---|
| **Coverage** | Complete | High (catches all errors) | Miss rare events |
| **Cost** | Very high | Medium | Low |
| **Latency** | N/A | ~10s decision delay | None |
| **Choose when** | Low-traffic debug | Production recommendation | Very high traffic |

---

## Interview Tips

**Clarifying questions:**
- How many services? How many requests per second? (determines scale)
- Retention requirements? (determines storage cost)
- Is this self-hosted or SaaS? (determines ops burden discussion)
- What's the primary use case: dashboards, alerting, or debugging incidents?

**Common follow-ups:**
- "How would you handle high-cardinality metrics?" → Don't put unbounded values in labels; use traces for per-request data
- "How do you correlate logs and traces?" → Inject trace_id into log context (structlog `bind`); Grafana supports trace-to-log correlation via shared trace_id
- "What happens if Elasticsearch falls behind?" → Logstash disk buffer; reduce index rate via sampling; hot-warm-cold tiering
- "How do you alert without too many false positives?" → Alert on symptoms with sufficient `for:` duration; use `for: 5m` to avoid flapping

**Key numbers:**
- Prometheus: 1M+ samples/sec per instance; blocks compress ~10:1
- Elasticsearch: 100K+ documents/sec ingest; supports petabyte-scale clusters
- OTel Collector: 100K+ spans/sec per instance
