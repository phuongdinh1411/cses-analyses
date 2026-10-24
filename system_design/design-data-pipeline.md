---
layout: simple
title: "Design a Data Pipeline System"
permalink: /system_design/design-data-pipeline
---

# Design a Data Pipeline System

A data pipeline moves, transforms, and delivers data from sources to consumers reliably and at scale. This covers both **batch ETL** (nightly P&L, end-of-day aggregations) and **streaming** (real-time market data, fraud signals).

---

## Table of Contents

1. [Requirements](#requirements)
2. [Back of the Envelope Estimation](#back-of-the-envelope-estimation)
3. [High-Level Design](#high-level-design)
4. [Batch Pipeline Deep Dive](#batch-pipeline-deep-dive)
5. [Streaming Pipeline Deep Dive](#streaming-pipeline-deep-dive)
6. [Database Design](#database-design)
7. [API Design](#api-design)
8. [Handling Failures](#handling-failures)
9. [Observability](#observability)
10. [Trade-offs](#trade-offs)
11. [Interview Tips](#interview-tips)

---

## Requirements

### Functional Requirements

- **Ingest** data from heterogeneous sources: REST APIs, databases, file drops (CSV/Parquet), message streams
- **Transform** data: clean, normalize, enrich, join with reference data
- **Load** data into target stores: data warehouse, time-series DB, downstream services
- **Schedule** batch jobs on a cron-like schedule with dependency management
- **Stream processing** for low-latency data (sub-second to seconds)
- **Reprocessing**: re-run historical data without affecting live pipeline

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Reliability** | Exactly-once or at-least-once delivery with idempotent loads |
| **Latency** | Batch: minutes to hours; Streaming: < 1 second |
| **Throughput** | 1M+ events/sec for streaming; TB/day for batch |
| **Fault tolerance** | Automatic retry with backoff; partial failure isolation |
| **Data quality** | Schema validation, null checks, range checks at ingestion |
| **Auditability** | Full lineage: which source row produced which output row |
| **Backfill** | Re-run any historical window without double-counting |

### Out of Scope

- Real-time ML model inference (separate serving system)
- Data catalog / discovery UI
- Access control / column-level security

---

## Back of the Envelope Estimation

**Market data pipeline example:**

```
Sources:        50 exchanges × 1,000 symbols × 1 tick/sec = 50,000 events/sec
Event size:     ~200 bytes (symbol, timestamp, price, volume)
Raw throughput: 50,000 × 200B = 10 MB/sec = 36 GB/hour = ~850 GB/day
Kafka retention: 7 days = ~6 TB
Processed store: ~10:1 compression (Parquet columnar) = ~85 GB/day
Annual growth:  ~30 TB/year

Batch job example (end-of-day P&L):
  - 10M trades × 1KB each = 10 GB input
  - Processing time target: < 30 minutes
  - Parallelism needed: 10+ workers
```

---

## High-Level Design

```
┌──────────────────────────────────────────────────────────────────┐
│                         Data Sources                             │
│  REST APIs   DB replicas   File drops   WebSocket feeds          │
└─────────────────────────────┬────────────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Ingestion Layer   │
                    │  (Kafka / Kinesis)  │
                    └─────────┬──────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
    ┌─────────▼──────┐ ┌──────▼──────┐ ┌─────▼────────┐
    │ Stream Processor│ │Batch Orchestr│ │Schema Registry│
    │  (Flink / Spark)│ │  (Airflow)  │ │  (Confluent)  │
    └─────────┬───────┘ └──────┬──────┘ └──────────────┘
              │                │
   ┌──────────▼────────────────▼──────────┐
   │              Storage Layer           │
   │  Time-series DB │ Data Warehouse │ S3 │
   │   (TimescaleDB) │  (Redshift/PG) │    │
   └──────────────────┬───────────────────┘
                      │
              ┌───────▼────────┐
              │  Serving Layer  │
              │  REST / gRPC    │
              └────────────────┘
```

### Component responsibilities

| Component | Role |
|-----------|------|
| **Kafka** | Durable, ordered event log; decouples producers from consumers |
| **Schema Registry** | Enforces Avro/Protobuf schemas; rejects malformed events at ingestion |
| **Airflow** | DAG-based batch orchestration; dependency tracking; retry/alerting |
| **Flink / Spark Streaming** | Stateful stream processing; windowed aggregations |
| **TimescaleDB** | Time-series optimized PostgreSQL extension; hypertable partitioning |
| **S3 / object store** | Raw event archive; source of truth for reprocessing |

---

## Batch Pipeline Deep Dive

### Airflow DAG: end-of-day financial data

```python
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

@dag(
    dag_id="eod_prices_pipeline",
    schedule="0 20 * * 1-5",       # weekdays at 8pm
    start_date=datetime(2024, 1, 1),
    catchup=True,                   # backfill enabled
    retries=3,
    retry_delay=timedelta(minutes=10),
    tags=["finance", "prices"],
)
def eod_prices_pipeline():

    @task
    def extract(logical_date=None) -> str:
        """Download raw prices for the given trading day."""
        date_str = logical_date.strftime("%Y-%m-%d")
        path = f"s3://raw-prices/{date_str}.parquet"
        download_from_vendor(date_str, path)
        return path

    @task
    def validate(path: str) -> str:
        """Schema + range checks — fail loudly rather than silently corrupt."""
        df = read_parquet(path)
        assert not df["close"].isna().any(), "Null close prices found"
        assert (df["close"] > 0).all(), "Non-positive prices found"
        assert (df["volume"] >= 0).all(), "Negative volume found"
        return path

    @task
    def transform(path: str) -> list[dict]:
        df = read_parquet(path)
        df["returns"] = df.groupby("symbol")["close"].pct_change()
        df["adj_close"] = df["close"] * df["adj_factor"]
        return df.to_dict("records")

    @task
    def load(rows: list[dict]):
        """Idempotent upsert — safe to re-run."""
        hook = PostgresHook(postgres_conn_id="warehouse")
        hook.run("""
            INSERT INTO daily_prices (symbol, date, close, adj_close, volume, returns)
            VALUES %s
            ON CONFLICT (symbol, date) DO UPDATE SET
                close = EXCLUDED.close,
                adj_close = EXCLUDED.adj_close,
                volume = EXCLUDED.volume,
                returns = EXCLUDED.returns,
                updated_at = NOW()
        """, parameters=rows)

    raw_path = extract()
    valid_path = validate(raw_path)
    transformed = transform(valid_path)
    load(transformed)

eod_prices_pipeline()
```

### Idempotency patterns for batch loads

| Pattern | How it works |
|---------|-------------|
| **DELETE + INSERT** | Delete rows for the date, re-insert. Simple but holds locks. |
| **UPSERT (ON CONFLICT)** | Insert or update atomically. Preferred for most cases. |
| **Staging table** | Load into temp table, then swap. Useful for large bulk loads. |
| **Partition swap** | Drop old partition, attach new one. Instant, zero lock time. |

---

## Streaming Pipeline Deep Dive

### Kafka topic design

```
Topic naming convention: {domain}.{entity}.{version}
  prices.ticks.v1        — raw market tick data
  prices.ohlcv.v1        — 1-minute OHLCV bars (downstream)
  alerts.risk.v1         — risk threshold breach events

Partition strategy:
  prices.ticks.v1  → partition by symbol hash
    → guarantees ordered delivery per symbol
    → allows parallel consumers up to partition count

Replication:
  replication.factor=3   for production
  min.insync.replicas=2  — write fails if < 2 replicas ACK
```

### Stream processor: 1-minute OHLCV bars

```python
# Flink DataStream pseudocode
env = StreamExecutionEnvironment.get_execution_environment()

ticks = (
    env
    .add_source(FlinkKafkaConsumer("prices.ticks.v1", TickSchema(), kafka_props))
    .assign_timestamps_and_watermarks(
        WatermarkStrategy
            .for_bounded_out_of_orderness(Duration.of_seconds(5))
            .with_timestamp_assigner(TickTimestampAssigner())
    )
)

ohlcv = (
    ticks
    .key_by(lambda t: t.symbol)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(OHLCVAggregator())   # open=first, high=max, low=min, close=last, vol=sum
)

ohlcv.add_sink(FlinkKafkaProducer("prices.ohlcv.v1", OHLCVSchema(), kafka_props))
ohlcv.add_sink(TimescaleDBSink("ohlcv_bars"))
```

### Late data handling

```
Event time vs processing time:
  Event time  — when the tick occurred (use this for financial data)
  Processing time — when Kafka received it (affected by network delays)

Watermark = "I've seen all events up to time T-5s"
  → allows 5-second late arrival window
  → triggers window computation after watermark passes window end

Late events beyond watermark:
  Option 1: Drop (simplest, acceptable if delay > 5s is rare)
  Option 2: Side output → separate late-events topic for manual review
  Option 3: Update result (complex; only for non-idempotent sinks)
```

---

## Database Design

### TimescaleDB hypertable for tick data

```sql
-- TimescaleDB partitions automatically by time (chunk_time_interval)
CREATE TABLE ticks (
    symbol      VARCHAR(20)  NOT NULL,
    ts          TIMESTAMPTZ  NOT NULL,
    price       NUMERIC(18,6) NOT NULL,
    volume      BIGINT       NOT NULL,
    exchange    VARCHAR(10)
);

SELECT create_hypertable('ticks', 'ts', chunk_time_interval => INTERVAL '1 day');

-- Compression (90%+ space savings for time-series)
ALTER TABLE ticks SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'ts DESC'
);
SELECT add_compression_policy('ticks', INTERVAL '7 days');

-- Index for typical query: latest N ticks for a symbol
CREATE INDEX ON ticks (symbol, ts DESC);
```

### Data warehouse: slowly changing dimensions

```sql
-- SCD Type 2: track historical instrument metadata
CREATE TABLE instruments (
    id          SERIAL PRIMARY KEY,
    symbol      VARCHAR(20)  NOT NULL,
    name        VARCHAR(200),
    currency    CHAR(3),
    exchange    VARCHAR(10),
    valid_from  DATE         NOT NULL,
    valid_to    DATE,           -- NULL means current record
    is_current  BOOLEAN DEFAULT TRUE
);

CREATE UNIQUE INDEX ON instruments (symbol, valid_from);
```

---

## API Design

```
GET  /v1/prices/{symbol}?start=2024-01-01&end=2024-12-31&interval=1d
     → Returns OHLCV bars for the given date range

GET  /v1/prices/{symbol}/latest
     → Returns most recent tick/bar (cache-friendly, low latency)

POST /v1/pipeline/runs
     → Trigger a manual backfill run
     Body: { "dag_id": "eod_prices_pipeline", "start_date": "...", "end_date": "..." }

GET  /v1/pipeline/runs/{run_id}
     → Poll status of a pipeline run: QUEUED | RUNNING | SUCCESS | FAILED

GET  /v1/pipeline/lineage/{symbol}/{date}
     → Trace which source records produced a given output row (audit)
```

---

## Handling Failures

### Failure taxonomy

| Failure | Detection | Recovery |
|---------|-----------|---------|
| Source API down | HTTP 5xx / timeout | Retry with exponential backoff; alert if > N failures |
| Bad data / schema mismatch | Schema Registry rejection | Dead-letter queue; human review |
| Transform bug | Data quality check failure | Roll back load; page on-call |
| Load DB down | Connection error | Airflow retry; events buffered in Kafka |
| Kafka broker failure | Consumer lag spike | Kafka auto-reassigns partitions to other brokers |
| Duplicate events | Downstream upsert logic | Idempotency key = (source_id, event_timestamp) |

### Dead-letter queue pattern

```
Normal flow:  Source → Kafka:prices.ticks.v1 → Processor → DB
Failure flow: Source → Kafka:prices.ticks.v1 → Processor → [parsing error]
                                                          → Kafka:prices.ticks.dlq.v1
                                                          → Alert + human review
```

### At-least-once with idempotent sink

```python
def process_and_load(event):
    idempotency_key = f"{event['source_id']}:{event['event_id']}"

    # Check if already processed
    if cache.exists(idempotency_key):
        return  # Skip duplicate

    # Process
    transformed = transform(event)

    # Load with idempotency
    db.execute("""
        INSERT INTO events (idempotency_key, ...)
        VALUES (%s, ...)
        ON CONFLICT (idempotency_key) DO NOTHING
    """, (idempotency_key, ...))

    cache.set(idempotency_key, 1, ex=86400)  # 24hr TTL
```

---

## Observability

| Signal | What to measure | Alert condition |
|--------|----------------|-----------------|
| **Consumer lag** | Kafka `messages_behind_high_water_mark` per consumer group | > 10,000 messages or growing for > 5 min |
| **Pipeline SLA** | Time from scheduled start to load complete | > 2× expected duration |
| **Data freshness** | `MAX(ts)` in target table vs expected latest | > 15 min behind for streaming |
| **Error rate** | DLQ message count per time window | Any message in DLQ |
| **Throughput** | Events/sec processed | < 50% of baseline (possible upstream issue) |
| **Load duration** | Time for DB write per batch | > 3σ above baseline (possible index bloat) |

---

## Trade-offs

### Batch vs streaming

| | Batch (Airflow + SQL) | Streaming (Kafka + Flink) |
|---|---|---|
| **Latency** | Minutes to hours | Seconds |
| **Complexity** | Low | High |
| **Cost** | Low | Higher (stateful cluster) |
| **Reprocessing** | Simple (re-run DAG) | Complex (replay from Kafka) |
| **Use when** | End-of-day reports, ML features | Fraud detection, real-time dashboards |

### Lambda vs Kappa architecture

| | Lambda | Kappa |
|---|---|---|
| **Design** | Separate batch + streaming layers | Streaming only; batch = replay |
| **Complexity** | High (two codebases) | Lower (one processing model) |
| **Reprocessing** | Re-run batch layer | Replay Kafka topic (needs long retention) |
| **Choose when** | Batch and streaming have very different logic | Same logic works for both |

---

## Interview Tips

**Clarifying questions to ask first:**
- What is the acceptable latency? (determines batch vs streaming)
- What are the consistency requirements? (exactly-once vs at-least-once)
- How much historical data needs to be reprocessable?
- Are there schema evolution requirements?

**Common follow-ups:**
- "How would you handle a 3-hour source outage?" → Kafka buffers events; catch up on recovery
- "How do you ensure data quality?" → Schema Registry + validation tasks + DLQ
- "How would you backfill 5 years of data?" → Parallel Airflow runs partitioned by month; write to staging, then swap
- "What if your stream processor crashes mid-window?" → Flink checkpoints state to S3; restore from last checkpoint

**Key numbers to know:**
- Kafka: 100MB/s+ per broker; 1M+ msg/sec per cluster
- TimescaleDB: 10M+ rows/sec insert throughput with compression
- Airflow: 1,000+ concurrent tasks with Celery executor
