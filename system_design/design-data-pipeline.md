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
4. [Ingestion Patterns](#ingestion-patterns)
5. [Batch Pipeline Deep Dive](#batch-pipeline-deep-dive)
6. [Streaming Pipeline Deep Dive](#streaming-pipeline-deep-dive)
7. [Exactly-Once Semantics](#exactly-once-semantics)
8. [Schema Evolution](#schema-evolution)
9. [Data Quality Framework](#data-quality-framework)
10. [Database & Storage Design](#database--storage-design)
11. [Partitioning & Compaction Strategy](#partitioning--compaction-strategy)
12. [Data Lineage & Audit](#data-lineage--audit)
13. [Security & Compliance](#security--compliance)
14. [Scalability & Backpressure](#scalability--backpressure)
15. [Architecture Patterns](#architecture-patterns)
16. [Handling Failures](#handling-failures)
17. [Observability](#observability)
18. [Cost Optimization](#cost-optimization)
19. [Trade-offs](#trade-offs)
20. [Interview Follow-ups](#interview-follow-ups)

---

## Requirements

### Functional Requirements

- **Ingest** data from heterogeneous sources: REST APIs, databases (CDC), file drops (CSV/Parquet), message streams
- **Transform** data: clean, normalize, enrich, join with reference data
- **Load** data into target stores: data warehouse, time-series DB, downstream services
- **Schedule** batch jobs with dependency management and backfill support
- **Stream processing** for low-latency data (sub-second to seconds)
- **Reprocessing**: re-run historical data without double-counting or corrupting live data
- **Data quality**: validate, quarantine, and alert on bad records

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Reliability** | Exactly-once or at-least-once delivery with idempotent loads |
| **Latency** | Batch: minutes to hours; Streaming: < 1 second end-to-end |
| **Throughput** | 1M+ events/sec streaming; TB/day batch |
| **Fault tolerance** | Auto-retry with backoff; partial failure isolation; no silent data loss |
| **Data quality** | Schema validation, null checks, range checks, freshness checks |
| **Auditability** | Full lineage: which source row produced which output row |
| **Backfill** | Re-run any historical window; idempotent loads prevent double-counting |
| **Schema evolution** | Backward/forward compatible schema changes without pipeline downtime |

### Clarifying Questions to Ask

> **Always ask these before designing:**
>
> - What is the acceptable end-to-end latency? (batch vs streaming decision)
> - Exactly-once or at-least-once semantics required?
> - How much historical data must be reprocessable, and in what SLA?
> - Are there PII/GDPR compliance requirements?
> - Expected data volume and growth rate?
> - Push-based (sources emit events) or pull-based (we poll sources)?
> - Is schema evolution expected? (new fields, renamed fields, type changes)

---

## Back of the Envelope Estimation

**Market data pipeline example:**

```
Sources:        50 exchanges × 1,000 symbols × 1 tick/sec = 50,000 events/sec
Event size:     ~200 bytes (symbol, timestamp, price, volume)
Raw throughput: 50,000 × 200B = 10 MB/sec = 36 GB/hour ≈ 850 GB/day
Kafka retention (7 days): ~6 TB
Processed store (10:1 Parquet compression): ~85 GB/day → ~30 TB/year

Batch job example (end-of-day P&L):
  10M trades × 1 KB each = 10 GB input
  Target: < 30 min processing → needs 10+ parallel workers
  Output rows: ~10M upserts into warehouse
```

---

## High-Level Design

```
┌──────────────────────────────────────────────────────────────────────┐
│                           Data Sources                               │
│   REST APIs    DB CDC (Debezium)    File drops    WebSocket feeds    │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │     Ingestion Layer     │
                    │  (Kafka / Kinesis)      │
                    │  Schema Registry        │
                    └──────────┬─────────────┘
                               │
              ┌────────────────┼─────────────────┐
              │                │                 │
    ┌─────────▼──────┐  ┌──────▼───────┐  ┌──────▼──────┐
    │ Stream Processor│  │  Batch Orch. │  │  DLQ Handler│
    │  (Flink/Spark)  │  │  (Airflow)   │  │  (alerts)   │
    └─────────┬───────┘  └──────┬───────┘  └─────────────┘
              │                 │
   ┌──────────▼─────────────────▼────────────┐
   │               Storage Layer             │
   │  Raw S3  │  Time-series DB  │ Warehouse │
   │ (archive)│  (TimescaleDB)   │ (Redshift)│
   └──────────────────┬──────────────────────┘
                      │
           ┌──────────▼──────────┐
           │    Serving Layer     │
           │  REST API / gRPC     │
           └─────────────────────┘
```

### Component responsibilities

| Component | Role |
|-----------|------|
| **Kafka** | Durable, ordered event log; decouples producers from consumers; replay buffer |
| **Schema Registry** | Enforces Avro/Protobuf schemas; rejects malformed events at ingestion |
| **Debezium** | CDC connector; streams DB row changes (INSERT/UPDATE/DELETE) as events |
| **Airflow** | DAG-based batch orchestration; dependency tracking; retry/alerting; backfill |
| **Flink / Spark Streaming** | Stateful stream processing; windowed aggregations; exactly-once checkpoints |
| **TimescaleDB** | Time-series-optimized PostgreSQL; hypertable auto-partitioning |
| **S3 / object store** | Raw event archive; immutable source of truth for reprocessing |
| **DLQ** | Dead-letter queue; quarantines bad records for human review |

---

## Ingestion Patterns

### 1. Push-based (sources emit to Kafka)

Best for: event streams, IoT, log aggregation.

```
Producer → Kafka (acks=all, min.insync.replicas=2)
```

- Producer sets `acks=all` → broker only ACKs after all ISR replicas confirm
- Use idempotent producer (`enable.idempotence=true`) to prevent duplicate messages on retry

### 2. Pull-based (pipeline polls sources)

Best for: REST APIs, databases without CDC, file drops.

```
Airflow Sensor → REST API → extract to S3 → trigger downstream tasks
```

- Use `ExternalTaskSensor` / `FileSensor` to gate downstream tasks on data availability
- Track watermarks: store last-seen `updated_at` or offset to avoid re-fetching all data

### 3. Change Data Capture (CDC)

Best for: syncing OLTP databases (Postgres, MySQL) into the pipeline without bulk scans.

```
Postgres WAL → Debezium Connector → Kafka topic (db.table.v1)
```

- Debezium reads the Write-Ahead Log — no additional DB load from polling
- Event shape: `{ "op": "c|u|d", "before": {...}, "after": {...}, "ts_ms": ... }`
- Enables full audit trail: every INSERT, UPDATE, DELETE is captured
- **Initial snapshot**: Debezium runs a consistent snapshot of the full table on first start, then tails WAL

### 4. File-based ingestion

Best for: partner data drops, legacy systems.

```
S3 file drop → S3 Event Notification → SQS → Airflow task / Lambda
```

- Use manifest files or file-naming conventions (`prices_20240101.parquet`) as idempotency keys
- Validate file hash (MD5/SHA-256) to detect corruption or partial uploads

---

## Batch Pipeline Deep Dive

### Airflow DAG design principles

**Key design decisions:**
1. `catchup=True` enables automatic backfill when deploying to new date ranges
2. Use `logical_date` (not wall clock) for idempotent date-partitioned processing
3. Each task should be idempotent: re-running must produce the same result
4. Fail loudly with explicit assertions — silent data corruption is worse than a failed job

```
DAG structure for end-of-day financial data:

extract → validate → transform → load_staging → quality_check → promote
                        ↓ (on failure)
                    dead_letter_queue
```

### Idempotency patterns for batch loads

| Pattern | How it works | Best for |
|---------|-------------|----------|
| **UPSERT (ON CONFLICT)** | Insert or update atomically by primary key | Low-volume, row-level uniqueness |
| **DELETE + INSERT** | Delete all rows for the partition, re-insert | Simple; holds brief locks |
| **Staging table swap** | Load into temp table; `ALTER TABLE … RENAME` | Zero-downtime large loads |
| **Partition swap** | Drop old partition; attach new one atomically | Huge tables; instant, lock-free |
| **Write-once partitions** | Partition by `date`; never overwrite a closed partition | Append-only warehouses (Redshift, BigQuery) |

### Backfill strategy

```
Problem: Re-run 2 years of data without blocking live pipeline or double-counting.

Strategy:
  1. Write to separate "backfill" partition or staging schema
  2. Run parallel Airflow DAGs partitioned by month (12 concurrent runs)
  3. Quality-check output against live data for overlap period
  4. Atomic swap: replace live partitions with backfill partitions
  5. No live pipeline downtime; rollback = swap back old partitions
```

---

## Streaming Pipeline Deep Dive

### Kafka topic design

```
Naming convention: {domain}.{entity}.{version}
  prices.ticks.v1     — raw market tick data
  prices.ohlcv.v1     — 1-min OHLCV bars (downstream of processor)
  alerts.risk.v1      — risk threshold breach events
  prices.ticks.dlq.v1 — dead-letter queue for malformed ticks

Partition strategy:
  Partition by symbol hash → ordered delivery per symbol
  → allows parallel consumers up to partition count
  → never partition by high-cardinality random key (breaks ordering)

Replication:
  replication.factor = 3  (production)
  min.insync.replicas = 2 → write fails if < 2 replicas ACK
  acks = all              → strongest durability guarantee
```

### Consumer group design

```
One consumer group per independent downstream consumer:
  group: ohlcv-aggregator   → reads prices.ticks.v1 → computes bars
  group: risk-engine        → reads prices.ticks.v1 → checks limits
  group: audit-logger       → reads prices.ticks.v1 → writes to S3

Each group maintains its own offset → independent processing rates
```

### Event time vs processing time

| | Event Time | Processing Time |
|---|---|---|
| **Definition** | When the event occurred (in source system) | When Kafka/Flink received it |
| **Use for** | Financial data, IoT, audit logs | Approximate dashboards only |
| **Problem** | Out-of-order events, late arrivals | Easy to implement but misleading |

### Windowing strategies

| Window Type | Use case | Example |
|-------------|----------|---------|
| **Tumbling** | Non-overlapping fixed periods | 1-min OHLCV bars |
| **Sliding** | Rolling average | 5-min rolling VWAP with 1-min slide |
| **Session** | Activity bursts | User session analytics (gap-based) |
| **Global** | Accumulate until trigger | End-of-day aggregation in stream |

### Late data handling

```
Watermark = "I've seen all events up to time T − 5s"
  → triggers window computation after watermark passes window end
  → allows 5-second late arrival window

Late events beyond watermark — three options:
  1. Drop        — simplest; acceptable if delay > 5s is rare
  2. Side output → Kafka DLQ for manual review or reprocessing
  3. Allowed lateness — keep window state open for extra N seconds
                        and emit updated results (use with idempotent sinks)
```

---

## Exactly-Once Semantics

### Delivery guarantees spectrum

| Guarantee | How | Risk |
|-----------|-----|------|
| **At-most-once** | No retry on failure | Data loss on crash |
| **At-least-once** | Retry + idempotent sink | Duplicates possible |
| **Exactly-once** | Transactions or 2-phase commit | Higher latency/complexity |

### Kafka transactions (producer side)

```
Producer API:
  producer.initTransactions()
  producer.beginTransaction()
    producer.send("topic-A", record1)
    producer.send("topic-B", record2)
    producer.sendOffsetsToTransaction(offsets, consumerGroup)
  producer.commitTransaction()     ← atomic: all-or-nothing

Consumers must use:
  isolation.level = read_committed  ← only see committed messages
```

### Flink exactly-once (2-phase commit sink)

```
Checkpoint N:
  1. Flink snapshots operator state to S3  (checkpoint barrier)
  2. Kafka sink starts a transaction
  3. Writes buffered records to Kafka (pre-commit phase)
  4. On barrier complete → commit Kafka transaction
  5. If crash before commit → transaction aborted; replay from checkpoint N-1

Result: each record written to sink exactly once,
        even if Flink job crashes and restarts.
```

### At-least-once + idempotent sink (practical alternative)

For most use cases, exactly-once transactions add complexity; this pattern is simpler:

```
Idempotency key = hash(source_system + event_id + event_timestamp)

Sink logic:
  INSERT INTO processed_events (idempotency_key, payload, ...)
  ON CONFLICT (idempotency_key) DO NOTHING

Re-processing the same event → conflict → safely ignored
```

---

## Schema Evolution

### Why it matters

Schema changes (new fields, renamed fields, type changes) happen constantly. Pipelines must handle them **without coordinated downtime across producers and consumers**.

### Avro / Protobuf compatibility rules

| Change | Backward Compatible | Forward Compatible | Full Compatible |
|--------|--------------------|--------------------|-----------------|
| Add optional field with default | ✅ | ✅ | ✅ |
| Delete optional field | ✅ | ❌ | ❌ |
| Add required field (no default) | ❌ | ✅ | ❌ |
| Rename field | ❌ | ❌ | ❌ |
| Change field type (int→long) | ✅ Avro | ✅ | ✅ |

**Rules:**
- **Backward compatible**: new schema can read data written with old schema (safe to upgrade consumers first)
- **Forward compatible**: old schema can read data written with new schema (safe to upgrade producers first)
- **Full compatible**: both directions — the safest; use as default

### Schema Registry enforcement

```
Producer registers schema → Registry validates compatibility against latest version
  BACKWARD  (default) → rejects if new schema can't read old messages
  FULL              → rejects if either direction broken

Consumer fetches schema by ID embedded in message:
  Magic byte (0x00) + Schema ID (4 bytes) + Avro payload
```

### Versioning strategy

```
Topic versioning: prices.ticks.v1  → prices.ticks.v2
  v1 and v2 run in parallel during migration window
  Producers write to v2; consumers migrate gradually
  Decommission v1 after all consumers migrated
  → Zero-downtime schema migration
```

---

## Data Quality Framework

### Quality dimensions

| Dimension | Check type | Example |
|-----------|-----------|---------|
| **Completeness** | Null/missing check | `close_price IS NOT NULL` |
| **Validity** | Range / type check | `close_price > 0 AND volume >= 0` |
| **Uniqueness** | Duplicate check | No duplicate `(symbol, date)` rows |
| **Timeliness** | Freshness check | `MAX(ts)` within last 15 min |
| **Consistency** | Cross-source check | Sum of trades ≈ reported volume |
| **Referential** | FK existence | Every `symbol` exists in instruments table |

### Three-tier quality gates

```
Tier 1 — At Ingestion (Schema Registry):
  Hard block: reject if schema is wrong
  Malformed events → DLQ immediately

Tier 2 — At Transform (validation task):
  Soft block: quarantine rows failing business rules
  Quarantined rows → separate "rejected" table + alert

Tier 3 — At Load (post-load assertion):
  Row count vs yesterday ± 20%
  Revenue sum sanity check
  Fail DAG if check fails → prevents downstream consumers from seeing bad data
```

### Anomaly detection for data quality

```
Statistical approach: for each metric M (row count, sum, null rate):
  Compute rolling mean and stddev over last 30 days
  Alert if today's value > mean ± 3σ

Time-series approach: use Prophet/STL decomposition to detect
  anomalies accounting for day-of-week patterns and seasonality
```

---

## Database & Storage Design

### Storage tier selection

| Store | Use case | Characteristics |
|-------|----------|----------------|
| **S3 (raw)** | Immutable archive; reprocessing source | Cheap; unlimited scale; no query |
| **S3 (processed Parquet)** | Analytics, ad-hoc queries via Athena/Spark | Columnar; 10:1 compression; query in place |
| **TimescaleDB** | Operational time-series queries (< 1s latency) | PostgreSQL; hypertable auto-partitioning |
| **Redshift / BigQuery** | Complex analytical SQL, joins, aggregations | MPP; columnar; suited for star schema |
| **Redis** | Hot cache for latest prices, session data | Sub-millisecond; volatile |

### TimescaleDB hypertable for tick data

```sql
CREATE TABLE ticks (
    symbol      VARCHAR(20)   NOT NULL,
    ts          TIMESTAMPTZ   NOT NULL,
    price       NUMERIC(18,6) NOT NULL,
    volume      BIGINT        NOT NULL,
    exchange    VARCHAR(10)
);

-- Auto-partition by time (1 day per chunk)
SELECT create_hypertable('ticks', 'ts', chunk_time_interval => INTERVAL '1 day');

-- Compress chunks older than 7 days (90%+ space savings)
ALTER TABLE ticks SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby   = 'ts DESC'
);
SELECT add_compression_policy('ticks', INTERVAL '7 days');

-- Index for typical query: latest N ticks for a symbol
CREATE INDEX ON ticks (symbol, ts DESC);
```

### Data warehouse: star schema

```
Fact table: fact_trades (trade_id, symbol_key, date_key, price, quantity, side)
Dimension: dim_symbol (symbol_key, symbol, name, sector, currency)
Dimension: dim_date   (date_key, date, year, month, day_of_week, is_holiday)

Benefits:
  Simple JOINs (denormalized)
  Efficient GROUP BY on dimensions
  Easy to add new dimension attributes without touching fact table
```

### SCD Type 2 for slowly changing dimensions

```sql
-- Track full history of instrument metadata changes
CREATE TABLE dim_instrument (
    surrogate_key   SERIAL PRIMARY KEY,
    symbol          VARCHAR(20) NOT NULL,
    exchange        VARCHAR(10),
    currency        CHAR(3),
    valid_from      DATE NOT NULL,
    valid_to        DATE,          -- NULL = current record
    is_current      BOOLEAN DEFAULT TRUE
);

-- On metadata change: close old row, insert new row
-- Fact table joins on surrogate_key → preserves historical accuracy
```

---

## Partitioning & Compaction Strategy

### Why partitioning matters

```
Without partitioning:
  SELECT * FROM ticks WHERE symbol = 'AAPL' AND ts BETWEEN ...
  → Full table scan of TB-scale table

With partitioning by date:
  → Only reads relevant day-partitions (partition pruning)
  → 100–1000× faster queries
```

### Partition strategies

| Strategy | Partition key | Best for |
|----------|--------------|---------|
| **Range by time** | `DATE(ts)` or `YEAR/MONTH` | Time-series, most pipeline data |
| **Hash by entity** | `symbol`, `user_id` | Even data distribution, parallel loads |
| **List by category** | `region`, `exchange` | Low-cardinality categorical filters |
| **Composite** | `(date, exchange)` | Multi-dimensional access patterns |

### Compaction (small file problem)

```
Problem: streaming pipelines write many small Parquet files
  → 1000s of 1MB files = poor read performance, high S3 API costs

Compaction job (runs hourly/daily):
  1. List all small files for a time partition
  2. Read all into memory (or Spark)
  3. Write out as 128MB–1GB Parquet files
  4. Delete original small files (after verify)
  5. Update metadata catalog (Hive Metastore / AWS Glue)

Target file size: 128MB–1GB (matches HDFS/S3 read buffer)
```

### Delta Lake / Apache Iceberg

For production data lakes, use a table format layer:

| Feature | Delta Lake / Iceberg |
|---------|---------------------|
| **ACID transactions** | Multiple writers without file conflicts |
| **Time travel** | Query table as of any past snapshot |
| **Schema evolution** | Add/rename columns without rewrite |
| **Partition evolution** | Change partition strategy without rewrite |
| **Compaction** | Built-in `OPTIMIZE` / `rewrite_data_files` |

---

## Data Lineage & Audit

### Why lineage matters

- **Debugging**: "Why is this P&L number wrong?" → trace back to source row
- **Compliance**: GDPR right-to-erasure → find all copies of a user's data
- **Impact analysis**: "If this source changes schema, what pipelines break?"

### Lineage capture approaches

| Approach | How | Trade-offs |
|----------|-----|-----------|
| **Metadata lineage** (coarse) | Record DAG/task → table → partition mapping | Low overhead; can't trace individual rows |
| **Row-level lineage** (fine) | Carry `source_id` through transformations | Full traceability; large storage overhead |
| **Column-level lineage** | Parse SQL/Spark transformations statically | Precise but complex; tool-assisted (OpenLineage) |

### Audit table pattern

```sql
CREATE TABLE pipeline_audit (
    run_id          UUID PRIMARY KEY,
    dag_id          VARCHAR(100),
    logical_date    DATE,
    source_table    VARCHAR(200),
    target_table    VARCHAR(200),
    rows_read       BIGINT,
    rows_written    BIGINT,
    rows_rejected   BIGINT,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    checksum        VARCHAR(64)   -- MD5 of output for integrity verification
);
```

### OpenLineage integration

```
Airflow → emits OpenLineage events automatically (with marquez provider)
Spark   → SparkListener emits lineage events at job start/end
Flink   → manual lineage emission at source/sink connectors

Stored in Marquez or Atlas for:
  - Upstream/downstream dependency graph
  - Column-level impact analysis
  - SLA tracking per dataset
```

---

## Security & Compliance

### Encryption

| Layer | Mechanism |
|-------|----------|
| **In transit** | TLS 1.2+ on all Kafka/HTTP connections |
| **At rest (S3)** | SSE-KMS with per-bucket keys |
| **At rest (DB)** | Transparent data encryption (TDE) |
| **Application-level** | Envelope encryption for PII fields (encrypt before write) |

### PII handling

```
Identification:
  Tag PII columns in schema metadata: { "pii": true, "pii_type": "email" }
  Schema Registry or data catalog enforces tagging

Techniques:
  Tokenization  → replace PII with reversible token (lookup table in secure vault)
  Pseudonymization → replace with deterministic hash (HMAC-SHA256 with rotating key)
  Masking       → replace with asterisks in non-prod environments
  Differential privacy → add statistical noise before aggregation
```

### GDPR right-to-erasure

```
Challenge: data archived in immutable S3 Parquet files

Solution:
  1. Tokenize PII at ingestion: store user_id → token mapping in secure vault
  2. On erasure request: delete the token from vault
  3. All future queries for that token return NULL (key not found)
  4. Historical Parquet files effectively pseudonymized
  5. Full deletion: compaction job rewrites affected Parquet files, dropping rows
```

### Access control

```
Column-level security:
  Apache Ranger / BigQuery Column Policy → restrict PII columns by role
  Row-level security → filter rows by user's region/team permissions

Kafka ACLs:
  Producer on prices.ticks.v1 → only market-data-ingestor service account
  Consumer on prices.ticks.v1 → only authorized consumer groups
```

---

## Scalability & Backpressure

### Horizontal scaling of each component

| Component | Scale-out mechanism |
|-----------|-------------------|
| **Kafka** | Add brokers; rebalance partitions |
| **Flink** | Add TaskManagers; increase parallelism per operator |
| **Airflow** | Celery/K8s executor; more workers |
| **TimescaleDB** | Read replicas; Citus for distributed hypertables |
| **S3 ingestion** | Parallel multipart upload; prefix-based sharding |

### Kafka partition count scaling

```
Rule of thumb:
  Partitions = max(desired throughput / throughput per partition,
                   desired consumer parallelism)

Throughput per partition: ~10-50 MB/s (depends on message size, broker hardware)
Consumer parallelism: max consumers in group = partition count

Under-partitioned: bottleneck at consumer; can't parallelize beyond partition count
Over-partitioned: more metadata overhead; more leader elections on failure
```

### Backpressure handling

```
Problem: fast producer overflows slow consumer

Kafka as buffer:
  Kafka decouples producer and consumer rates
  Consumer can fall behind (consumer lag) without affecting producer
  Max lag = Kafka retention × partition size

Flink backpressure:
  Network buffer fills → upstream operator blocks
  Visible in Flink UI as "backpressure ratio"
  Fix: scale out consumer operators or optimize slow operations

Airflow concurrency limits:
  pool_slots, dag_concurrency, task_concurrency
  Prevent runaway parallelism from overwhelming downstream systems
```

---

## Architecture Patterns

### Lambda Architecture

```
         ┌── Batch Layer (Hadoop/Spark) ──────────────────┐
Sources → │   - Full recomputation on historical data      │
         │   - High accuracy; high latency (hours)        │ → Merge view → Query
         └── Speed Layer (Flink) ─────────────────────────┘
              - Process recent data only
              - Low latency; approximate results

Pros: Fault tolerant; reprocessing is simple (re-run batch)
Cons: Two codebases to maintain; results can diverge
```

### Kappa Architecture

```
                    ┌── Streaming Layer (Flink) ─────────────┐
Sources → Kafka → → │   - All processing is streaming         │ → Query
                    │   - Reprocessing = replay Kafka topic   │
                    └────────────────────────────────────────┘

Pros: One codebase; simpler to maintain
Cons: Reprocessing requires long Kafka retention; stateful replay is complex
When: Business logic is the same for batch and streaming paths
```

### Hot path / Cold path design

```
Hot path (< 1 second):
  Tick data → Kafka → Flink → Redis cache → WebSocket API
  For: real-time dashboards, risk alerts, order management

Warm path (1 minute – 1 hour):
  Kafka → Flink → TimescaleDB
  For: operational queries, intraday analytics

Cold path (hours – days):
  S3 raw archive → Spark batch → Redshift warehouse
  For: historical analysis, ML training, regulatory reports

Rule: serve each query from the appropriate tier;
      never force cold-path queries through the hot path
```

### Medallion Architecture (Data Lakehouse)

```
Bronze (raw):   S3 raw zone — exact copy of source data; immutable; full history
Silver (clean): S3 cleaned — validated, deduplicated, standardized schema
Gold (curated): S3 aggregated — business-level aggregations, ready for BI/ML

Each layer is independently queryable (Iceberg/Delta tables)
Downstream can rebuild silver from bronze; gold from silver
```

---

## Handling Failures

### Failure taxonomy

| Failure | Detection | Recovery |
|---------|-----------|---------|
| Source API down | HTTP 5xx / timeout | Exponential backoff; alert after N failures; Kafka buffers |
| Bad data / schema mismatch | Schema Registry rejection | Dead-letter queue; human review |
| Transform bug | Data quality check failure | Roll back load; page on-call; fix and backfill |
| DB connection error | Connection timeout | Airflow retry; events buffered in Kafka |
| Kafka broker failure | Consumer lag spike | Kafka auto-reassigns partitions; transparent to consumer |
| Flink job crash | Heartbeat missing | Flink restarts from last checkpoint; replays in-flight events |
| Duplicate events | Downstream upsert | Idempotency key = `(source_id, event_timestamp)` |
| Poison pill message | DLQ or parse error | Skip + DLQ; never block pipeline on single bad record |

### Dead-letter queue pattern

```
Normal flow:  Source → Kafka:prices.ticks.v1 → Processor → DB
Failure flow: Source → Kafka:prices.ticks.v1 → Processor
                           [parsing/transform error]
                                    ↓
                       Kafka:prices.ticks.dlq.v1
                                    ↓
                          Alert + human review
                                    ↓
                         Fix & replay to main topic
```

### Handling source outage (3-hour gap)

```
During outage:
  - Producer fails to push events; no data in Kafka
  - Downstream consumers idle; consumer lag = 0 (no new messages)
  - Alert fires on data freshness: MAX(ts) > 15 min old

Recovery:
  - Source comes back online; pushes buffered events (or sends backfill)
  - Consumers process catch-up burst; consumer lag rises then recovers
  - Kafka retention (7 days) ensures no data loss if outage < retention window
  - If source has no buffer: use pull-based reconciliation job to detect and fill gaps
```

---

## Observability

### Metrics to instrument

| Signal | What to measure | Alert condition |
|--------|----------------|-----------------|
| **Consumer lag** | `messages_behind_high_water_mark` per consumer group | > 10,000 messages OR growing for > 5 min |
| **Pipeline SLA** | DAG run start → load complete duration | > 2× expected duration |
| **Data freshness** | `MAX(ts)` in target vs expected latest | > 15 min behind for streaming; > 2 hr for batch |
| **DLQ rate** | Messages arriving in DLQ per time window | Any message in DLQ |
| **Throughput** | Events/sec processed per consumer group | < 50% of baseline (possible upstream issue) |
| **Load duration** | DB write time per batch | > 3σ above baseline (possible index bloat) |
| **Rejection rate** | Rows rejected by quality checks / total rows | > 0.1% (indicates upstream schema change) |
| **Checkpoint duration** | Flink checkpoint completion time | > configured checkpoint interval (risk of job stall) |

### Distributed tracing for pipelines

```
Trace context propagation:
  Attach trace_id to each event at ingestion
  Pass trace_id through Kafka message headers
  Each processing step logs span with same trace_id

Enables:
  - End-to-end latency breakdown: source → Kafka → Flink → DB
  - Identify which step is the bottleneck
  - Correlate slow DB write with specific event batch
```

### Alerting runbooks

```
Consumer lag alert:
  1. Check if producer is healthy (throughput)
  2. Check consumer CPU/memory (might be overwhelmed)
  3. Check if downstream DB is slow (backpressure)
  4. Scale out consumer if CPU-bound

Data freshness alert:
  1. Check source system availability
  2. Check pipeline is running (Airflow/Flink job status)
  3. Check for schema change (new DLQ messages)
  4. Escalate to on-call if unresolved in 15 min
```

---

## Cost Optimization

### Storage costs

| Optimization | Mechanism | Savings |
|-------------|-----------|---------|
| **Columnar format** | Parquet vs CSV | 10:1 compression; 10–100× fewer bytes scanned |
| **Compression** | Snappy/ZSTD codec | 3–5× additional savings |
| **Tiered storage** | Hot → warm → cold S3 tiers | Up to 90% for rarely accessed historical data |
| **TTL-based deletion** | Auto-delete raw after raw→bronze copy confirmed | Reduce redundant copies |
| **TimescaleDB compression** | Compress chunks > 7 days old | 90%+ space savings |

### Compute costs

| Optimization | Mechanism |
|-------------|-----------|
| **Spot instances** | Batch Spark jobs tolerate interruption; use spot with checkpointing |
| **Right-sizing** | Profile actual CPU/memory; most pipelines are IO-bound not CPU-bound |
| **Idle cluster teardown** | Autoscale Flink to 0 during off-hours for non-critical streams |
| **Pushdown predicates** | Filter and project early in Spark/Flink; don't deserialize unused columns |

### Kafka cost optimization

```
Compression at producer: compression.type = lz4 or zstd
  → 3–5× less network bandwidth, broker storage

Log compaction for reference data topics:
  → Only retain latest value per key (removes update history)
  → Drastically reduces retention size for slowly changing data

Tiered storage (Confluent/MSK):
  → Offload old segments to S3; brokers only hold hot segments
  → Decouple storage cost from broker count
```

---

## Trade-offs

### Batch vs streaming

| | Batch (Airflow + SQL) | Streaming (Kafka + Flink) |
|---|---|---|
| **Latency** | Minutes to hours | Seconds |
| **Complexity** | Low | High (state management, watermarks) |
| **Cost** | Low | Higher (stateful cluster, 24/7) |
| **Reprocessing** | Simple (re-run DAG) | Complex (replay from Kafka) |
| **Exactly-once** | Easy (atomic upsert) | Requires transactions/checkpoints |
| **Use when** | End-of-day reports, ML features | Fraud detection, real-time dashboards |

### Lambda vs Kappa

| | Lambda | Kappa |
|---|---|---|
| **Design** | Separate batch + streaming layers | Streaming only; batch = replay |
| **Complexity** | High (two codebases) | Lower (one processing model) |
| **Reprocessing** | Re-run batch layer (simple) | Replay Kafka (needs long retention) |
| **Accuracy** | Batch layer "corrects" stream | Single consistent result |
| **Choose when** | Batch and streaming logic differ significantly | Same logic works for both |

### Push vs pull ingestion

| | Push | Pull |
|---|---|---|
| **Latency** | Lowest | Polling delay |
| **Source coupling** | Source must know pipeline endpoint | Pipeline controls schedule |
| **Backpressure** | Producer must respect consumer capacity | Consumer naturally self-throttles |
| **Use when** | Low-latency streams, IoT | REST APIs, file drops, legacy systems |

### Schema enforcement: strict vs lenient

| | Strict (Schema Registry) | Lenient (schema-on-read) |
|---|---|---|
| **Data quality** | High; rejects bad data at source | Low; bad data silently stored |
| **Evolution flexibility** | Low; requires schema registration | High; any format accepted |
| **Debugging** | Easy; failures at ingestion, not downstream | Hard; failures appear far from source |
| **Use when** | Production financial/healthcare data | Exploratory data, raw landing zone |

---

## Interview Follow-ups

### "How would you handle a 3-hour source outage?"

> Kafka acts as the buffer — events accumulate while the source is down. On recovery, consumers process the catch-up burst. Because Kafka retains 7 days of data, nothing is lost as long as the outage is shorter. If the source has no buffer (REST API with no history), use a gap-detection job: compare expected sequence numbers or timestamps, then trigger a targeted backfill for the missing window.

### "How do you ensure data quality?"

> Three layers: (1) **Schema Registry** rejects schema violations at ingestion — before data enters the pipeline. (2) **Validation tasks** in the DAG apply business-rule checks (nulls, ranges, referential integrity) and quarantine failing rows to a rejected table. (3) **Post-load assertions** compare row counts, sums, and distributions against historical baselines and fail the DAG if they exceed thresholds. The key principle: **fail loudly and early** rather than silently propagate corrupt data.

### "How would you backfill 5 years of historical data?"

> Partition the backfill by month → 60 parallel Airflow DAG runs. Write to a separate staging schema to avoid blocking live queries. For each partition: extract from S3 raw archive → transform → load into staging partitions → run quality checks. After all partitions pass, do an atomic partition swap (replace live partitions with backfill partitions). Rolling back is instant — just swap back. This keeps the live pipeline running throughout.

### "What if the stream processor crashes mid-window?"

> Flink checkpoints state to S3 every N seconds. On crash, Flink restarts from the last successful checkpoint, replays events from Kafka (which still holds them), and re-processes the in-progress window. With exactly-once checkpointing, the sink only sees committed writes — no duplicates. The recovery time is proportional to the checkpoint interval, so tune it based on acceptable recovery latency vs. checkpoint overhead.

### "How would you handle schema changes without downtime?"

> Use Schema Registry with `BACKWARD_TRANSITIVE` compatibility. Any change that breaks compatibility is rejected. For additive changes (new optional field), no pipeline change is needed — consumers ignore unknown fields. For breaking changes: create `prices.ticks.v2` topic alongside v1, migrate producers first, run consumers on both topics, then decommission v1 after all consumers migrate. The overlap window ensures zero downtime.

### "How would you handle 100× traffic spike (market open/close)?"

> Kafka absorbs the burst — producers write at full speed; consumers process at their sustainable rate. Consumer lag grows during the spike and drains afterward. Flink autoscales horizontally: add TaskManagers to increase parallelism up to partition count. Airflow uses dynamic task mapping to parallelize load tasks. Database: use connection pooling (PgBouncer) to prevent connection exhaustion; pre-warm read replicas before known spikes (market open).

### "How would you delete all data for a specific user (GDPR)?"

> At ingestion, tokenize user PII: store `user_id → opaque_token` in a secure vault. All downstream storage uses the token, never the raw PII. On erasure request: delete the token from the vault. All future queries return NULL for that token. For complete erasure from archives: schedule a compaction job that rewrites affected Parquet partitions filtering out the user's rows. This avoids full S3 rewrites until needed.

### Key numbers to know

| System | Number |
|--------|--------|
| **Kafka** | 100 MB/s+ per broker; 1M+ msg/sec per cluster |
| **Kafka partition** | ~10-50 MB/s max throughput |
| **Flink** | 10M+ events/sec per job; horizontal scale to 100s of nodes |
| **TimescaleDB** | 10M+ rows/sec insert; 90%+ compression |
| **S3** | 5500 GET/sec per prefix; 3500 PUT/sec per prefix |
| **Parquet** | 10:1 vs CSV; column pruning makes queries 10–100× faster |
| **Airflow** | 1,000+ concurrent tasks (Celery/K8s executor) |
