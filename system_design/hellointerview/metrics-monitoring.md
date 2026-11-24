---
layout: simple
title: "Design a Metrics Monitoring Platform (Datadog/Prometheus) — Hello Interview Style"
permalink: /system_design/hellointerview/metrics-monitoring
---

# Metrics Monitoring Platform

**Patterns:** Scaling Writes · Scaling Reads  
**Difficulty:** Hard  
**Source:** hellointerview.com (AI-generated full solution)

---

## Understanding the Problem

📊 **What is a Metrics Monitoring Platform?**  
A metrics monitoring platform (like Datadog, Prometheus/Grafana, or CloudWatch) collects performance data from servers and services, stores it as time-series data, visualizes it on dashboards, and triggers alerts when thresholds are breached.

---

### Functional Requirements

**Core Requirements**

- The platform should be able to ingest metrics (CPU, memory, latency, custom counters) from services
- Users should be able to query and visualize metrics on dashboards with filters, aggregations, and time ranges
- Users should be able to define alert rules with thresholds over time windows (e.g., "alert if p99 latency > 500ms for 5 min")
- Users should receive notifications when alerts fire (email, Slack, PagerDuty)

**Below the line (out of scope):**

- Log aggregation and full-text search
- Distributed tracing (spans, traces)
- Anomaly detection via ML

### Non-Functional Requirements

**Core Requirements**

- The system should scale to ingest **5M metrics/second** from 500K servers
- Dashboard queries should return within **seconds**, even spanning days or weeks
- Alerts should evaluate with low latency **(< 1 minute** from metric emission to alert firing)
- The system should be highly available; eventual consistency for dashboards is OK
- The system should handle **late or out-of-order data** gracefully

**Below the line (out of scope):**

- Multi-region replication
- Strong consistency guarantees

### Constraints & Estimates

- 500K servers, each emitting 100 metrics every 10 seconds
- 500K × 100 / 10 = **5M metrics/sec**
- Each metric: `{ timestamp, service, host, metric_name, tags, value }` ≈ 150 bytes
- 5M × 150B = **750MB/sec** ingestion
- Storage: 5M × 150B × 86,400 sec/day = **~62TB/day** raw (before compression)
- With 10× compression (time-series compress well): ~6TB/day
- 1 year retention: ~2PB (need tiered storage)

---

## The Set Up

### Planning the Approach

Three largely independent pipelines:
1. **Ingest** – receive 5M metrics/sec reliably
2. **Storage** – store time-series data efficiently, support fast range queries
3. **Query & Alert** – low-latency dashboard queries + sub-minute alert evaluation

### Defining the Core Entities

- **Metric** – name (e.g., `cpu.utilization`), tags (`{ host: "web-01", service: "api" }`), timestamp, value
- **AlertRule** – id, metric_name, tag_filters, aggregation (avg/p99/count), threshold, window_secs, comparison (>/</>=), notification_channels[]
- **Alert** – id, rule_id, fired_at, resolved_at, trigger_value, status (firing/resolved)
- **Dashboard** – id, name, panels (list of queries + visualization config)

### Data Flow

```
Servers (agents) → Ingest API → Kafka → Time-Series Writers → TSDB
                                     → Alert Evaluator → Alert DB → Notification Service
Dashboards: Query Engine → TSDB (pre-aggregated rollups + raw) → Response
```

### API or System Interface

```
// Ingest metrics (called by agents on each server)
POST /metrics/ingest
Content-Type: application/x-protobuf
{ metrics: [ { name, tags, timestamp, value }, ... ] }   // batch of 100 metrics
-> { status: "accepted" }

// Query metrics for dashboard
GET /metrics/query?name=cpu.utilization&tags=service:api&from=2024-01-01&to=2024-01-02&step=5m&agg=avg
-> { series: [ { timestamp, value } ] }

// Create alert rule
POST /alerts/rules
{ "name": "High CPU", "query": "avg(cpu.utilization{service=api}[5m]) > 80", "channels": ["slack://ops"] }
-> { rule_id }

// Get firing alerts
GET /alerts?status=firing
-> { alerts: [ { rule, fired_at, current_value } ] }
```

---

## High-Level Design

### 1) The platform can ingest metrics from services

**Agent (runs on each server):**
- Collects metrics (CPU, memory, custom app metrics via StatsD/Prometheus client libs)
- Batches 100 metrics every 10s → `POST /metrics/ingest`
- Serializes with Protobuf (compact, 3–5× smaller than JSON)
- Retries with exponential backoff on failure

**Ingest pipeline:**
```
Agents → Ingest API (stateless, 1000 pods) → Kafka (100 partitions)
```

- Ingest API: validate, decompress → publish to Kafka
- Kafka provides durability buffer: even if TSDB is slow, metrics aren't lost
- Partitioning: by `{metric_name + tags hash}` → same metric series always to same partition → ordered within partition

**Ingest API throughput:**
- 5M metrics/sec × 150B = 750MB/sec
- 1000 pods × 750KB/pod/sec → trivial per-pod

### 2) Users can query and visualize metrics on dashboards

**Query flow:**

```
Dashboard → Query Engine → TSDB (pre-aggregated rollups for wide ranges, raw for recent)
```

**Key design:** Fast dashboard queries require **pre-aggregated rollups**:

| Data age | Resolution | Storage |
|---|---|---|
| Last 24 hours | Raw (10s intervals) | Hot TSDB |
| Last 7 days | 1-min aggregates | Warm TSDB |
| Last 30 days | 5-min aggregates | Warm TSDB |
| Last 1 year | 1-hour aggregates | Cold S3/Parquet |
| > 1 year | 1-day aggregates | Glacier |

Query Engine picks the right rollup tier based on `(time_range, requested_step)`.

### 3) Users can define alert rules with thresholds

Alert rule example: `avg(cpu.utilization{service=api}[5m]) > 80`

**Alert Evaluator (streaming):**
- Consumes from Kafka (same metrics stream as storage)
- Maintains per-rule sliding windows in memory using **Redis sorted sets** or in-process time-bucket maps
- Evaluates each rule every 30s
- When threshold exceeded for required duration → fire alert

### 4) Users receive notifications when alerts fire

- Alert fires → write Alert record to DB → publish to Kafka("alerts")
- Notification Worker: consume from Kafka → send to configured channels (email/Slack/PagerDuty)
- Deduplication: don't re-fire until alert resolves and re-triggers

---

## Potential Deep Dives

### 1) How do we serve low-latency dashboard queries over weeks of data?

**The problem with raw data:** Querying 2 weeks of raw 10s-interval metrics for a time-range chart means reading millions of data points just to render 100 chart pixels.

**Solution: Downsample + rollup storage**

Rollup Workers (Kafka consumers) continuously compute aggregates at multiple resolutions:

```
Kafka (raw metrics)
  → Rollup Worker
    → Writes to TimescaleDB:
      raw_metrics    (10s resolution, TTL 24h)
      metrics_1m     (1-min avg/min/max, TTL 7d)
      metrics_5m     (5-min avg/min/max, TTL 30d)
      metrics_1h     (1-hour avg/min/max, TTL 1y)
```

**TimescaleDB continuous aggregates** do this automatically:
```sql
CREATE MATERIALIZED VIEW metrics_1m
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 minute', timestamp) AS bucket,
  metric_name,
  tags,
  avg(value) AS avg_val,
  min(value) AS min_val,
  max(value) AS max_val
FROM raw_metrics
GROUP BY bucket, metric_name, tags;
```

**Query Engine routing:**
```python
def choose_rollup(from_ts, to_ts, step):
    span_hours = (to_ts - from_ts) / 3600
    if span_hours <= 24 and step <= 60:
        return "raw_metrics"  # live dashboard
    elif span_hours <= 168 and step <= 300:
        return "metrics_1m"   # last week
    elif span_hours <= 720 and step <= 3600:
        return "metrics_5m"   # last month
    else:
        return "metrics_1h"   # long range
```

**Result caching:**
- Dashboard queries are often repeated (refresh every 30s)
- Cache query results in Redis: key = `query_hash`, TTL = 60s
- For wide time ranges (weeks), cache for longer (5 min)

### 2) How do we reduce alert latency below 1 minute?

**Problem:** Alert evaluates `avg(cpu.utilization[5min]) > 80`. With a 1-minute evaluation loop, the worst case is 1 min + 5 min window = alert fires up to 6 minutes after the event.

**Solution: Streaming alert evaluation**

Instead of polling the TSDB every 60s, evaluate alerts in the **streaming path** (Kafka consumer):

```
Kafka (raw metrics)
  → Alert Evaluator Worker (Kafka Streams or Flink)
    - For each metric: check which alert rules apply (index by metric_name + tags)
    - Maintain per-rule sliding time window (last N seconds of values) in memory
    - Re-evaluate rule on every new data point
    - Fire when threshold exceeded for required duration
```

**Sliding window state management:**
- Use a Redis sorted set per active rule: `ZADD rule:{id}:window {timestamp} {value}`
- On each new metric: add to sorted set + `ZREMRANGEBYSCORE` to remove old data outside window
- Compute avg: `ZRANGE + SUM / COUNT` → compare to threshold
- This allows evaluation on every new data point → latency = propagation delay through Kafka (seconds, not minutes)

**Alert evaluation at scale:**
- 5M metrics/sec × average 0.1 alert rules/metric = 500K rule evaluations/sec
- Partition by `rule_id` to colocate rule state
- Each evaluation: Redis ops → ~1ms → need 500 alert evaluator workers

### 3) How do we ensure high availability during spikes and failures?

**Ingest HA:**
- Kafka provides durability buffer — 7-day retention
- If TSDB slows down, Kafka consumer lag grows; metrics are stored safely in Kafka
- Multiple TSDB write workers autoscale on Kafka lag

**TSDB HA (TimescaleDB):**
- Primary + 2 synchronous replicas → no data loss on primary failure
- Automatic failover with Patroni

**Alert Evaluator HA:**
- Kafka consumer group: if one evaluator crashes, Kafka rebalances partitions to other evaluators
- Sliding window state: checkpoint to Redis periodically; on restart, reload from Redis + replay recent Kafka messages

**Handling late/out-of-order data:**
- Metric from a slow/offline server arrives 5 minutes late
- TimescaleDB handles late inserts (open chunk allows late writes)
- Alert evaluator: use **watermarking** — wait 60s after event time before closing a window (Flink-style)
- Dashboard: re-query at slightly past the visible time range to pick up late data

### 4) How do we handle cardinality explosion?

**Problem:** Tags on metrics can explode combinatorially. If a metric has tags `{service, host, region, endpoint, status_code}`, the number of unique tag combinations (series) can be billions — a "cardinality bomb."

**Example:** `http.requests{ service: api, host: web-01, endpoint: /checkout, status: 200 }` × (100 services × 1000 hosts × 500 endpoints × 50 status codes) = 2.5 billion unique series.

**Solutions:**

**A) High-cardinality index (specialized TSDBs):**
- **InfluxDB** handles high cardinality but struggles above 10M series
- **Prometheus** famously struggles above ~1M active series
- **VictoriaMetrics** designed for 100M+ series

**B) Tag cardinality limits:**
- Reject metrics with high-cardinality tags at ingest (e.g., user_id, session_id as metric tags)
- Whitelist approved tag keys; reject unknown tags
- Dashboard: flag queries that would scan > 1M series

**C) Adaptive rollup:**
- For high-cardinality metrics: aggregate away high-cardinality dimensions in rollups
- Keep per-host raw data for 1 hour only; aggregate to per-service after that

---

## Final Design

```
Agents (500K servers)
  │ protobuf batch every 10s
  ▼
Ingest API (1000 stateless pods)
  ↓
Kafka (100 partitions, 7-day retention)
  ├─→ TSDB Writers → TimescaleDB
  │     (raw 10s, rollup 1m/5m/1h)
  ├─→ Alert Evaluator Workers (Kafka Streams)
  │     → Redis (sliding windows per rule)
  │     → Alert DB (PostgreSQL) on threshold breach
  │     → Kafka("alerts") → Notification Workers → Slack/Email/PagerDuty
  └─→ Rollup Workers → TimescaleDB (continuous aggregates)

Query Engine
  ├─ Redis (query result cache, TTL 60s)
  └─ TimescaleDB (route to raw/1m/5m/1h based on time range)

TimescaleDB
  - Primary + 2 replicas (Patroni)
  - Tiered storage: hot (SSD) → warm (HDD) → cold (S3 Parquet)
  - Automatic compression for chunks > 1 week old
```

---

## What is Expected at Each Level?

### Mid-level
- Correct entity design (metric, alert rule, dashboard)
- Agents batch-push metrics to ingest API
- TimescaleDB or InfluxDB for time-series storage
- Simple polling-based alert evaluation

### Senior
- Kafka ingestion buffer for 5M metrics/sec
- Pre-computed rollups at multiple resolutions for fast dashboard queries
- Streaming alert evaluation (reduce latency from minutes to seconds)
- Redis query result caching

### Staff+
- Cardinality explosion problem and solutions
- Watermarking for out-of-order data
- Tiered storage (hot/warm/cold) for 2PB/year at acceptable cost
- Alert evaluator fault tolerance (Kafka rebalancing + Redis state checkpoint)
- Discusses Flink vs. Kafka Streams for stateful alert evaluation
