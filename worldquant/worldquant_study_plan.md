---
layout: simple
title: "WorldQuant Senior SWE — Study Plan"
permalink: /worldquant/worldquant_study_plan
---

# WorldQuant Senior SWE — Study Plan

**Role:** Senior Software Engineer at WorldQuant  
**JD focus:** Python, distributed systems, data pipelines (ETL/streaming), PostgreSQL, Kafka, Airflow, observability  
**Timeline:** 8 weeks

---

## In 60 seconds

- **One schedule, two repos.** The main track is the [python-books eight-week route](https://github.com/phuongdinh1411/python-books#eight-week-route) (Python → SQL → Kafka → ETL → financial system design → security → mocks). This repo supplies the **daily DSA track** and the system-design pages.
- **Daily rhythm:** 60–90 min main track + 1–2 DSA problems (≤ 25 min each) + 10 min reviewing yesterday's mistakes.
- **This page** holds the topic notes for each track. [WorldQuant Senior SWE Prep](/worldquant/worldquant_senior_swe_prep) holds the job research, question bank, and progress tracker.

## Unified 8-week schedule

| Week | Main track (python-books) | DSA track (this repo, daily) | System design (this repo) |
|---|---|---|---|
| 1 | Python internals + asyncio | Arrays, hashing, two pointers; [Counting Pairs](/worldquant/counting_pairs), [Degree of an Array](/worldquant/degree_of_an_array) | — |
| 2 | FastAPI + async SQLAlchemy + pytest | Sliding window + monotonic deque; [Sliding Window Minimum](/worldquant/sliding_window_minimum), [Rolling Rank](/worldquant/rolling_rank_in_a_sliding_window) | — |
| 3 | SQL + PostgreSQL | Binary search on answer, heaps; [Top-K Portfolio](/worldquant/top_k_portfolio_selection_with_stability_constraint) | [Key-value store](/system_design/design-key-value-store) |
| 4 | Kafka + idempotent ingestion | Graphs (BFS/DFS, union-find, topological sort); [Longest Increasing Path](/worldquant/longest_consecutive_increasing_path_in_a_grid) | [Message queue](/system_design/design-message-queue) |
| 5 | ETL/Airflow + backfills | DP (knapsack, intervals); [Biological Hazards](/worldquant/biological_hazards) | [Data pipeline](/system_design/design-data-pipeline) |
| 6 | Financial system design | Quant-flavoured streaming stats; [Online EWMA](/worldquant/online_ewma_mean_and_variance), [Rolling Correlation](/worldquant/rolling_correlation_with_missing_values), [Rolling IC](/worldquant/rolling_information_coefficient_at_scale) | [Payment system](/system_design/design-payment-system), [Observability](/system_design/design-observability-platform) |
| 7 | Network/security + low-level design | Segment/Fenwick tree; [Cross-Sectional Rank](/worldquant/cross_sectional_rank_transform), [Min Swaps](/worldquant/minimum_swaps_to_sort_by_popularity) | Low-level design pages below |
| 8 | Mocks + behavioral | Timed mixed sets: 2 mediums in 45 min | Timed 45-min mocks (topics below) |

---

## Priority Stack

If time is limited, study in this order — each row is a bigger differentiator than the one below it for this specific role:

| Priority | Topic | Why |
|----------|-------|-----|
| 1 | Python asyncio + FastAPI + SQLAlchemy | Biggest gap most candidates have; directly listed |
| 2 | Data pipeline HLD (Kafka + ETL/Airflow) | Most role-specific; WorldQuant runs massive data pipelines |
| 3 | PostgreSQL internals + SQL optimization | Directly tested; financial data is relational |
| 4 | Distributed systems (fault tolerance, exactly-once) | "Design distributed, scalable, fault-tolerant systems" |
| 5 | DSA mediums at speed | Table stakes — likely covered, needs speed drilling |
| 6 | Observability (OpenTelemetry / Grafana / ELK) | Nice-to-have but easy 30-minute win |

---

## DSA Track (daily, weeks 1–8)

**Goal:** Solve any LeetCode medium in ≤ 20–25 minutes. Focus on speed and correctness, not new concepts.

| Topic | Resource | Target |
|-------|----------|--------|
| Graphs (BFS/DFS/Dijkstra/Union-Find) | [`pattern/Graph.md`](/pattern/graph) | 5 medium problems |
| DP (knapsack, intervals, bitmask) | [`pattern/DP.md`](/pattern/dp), [`KnapsackDP`](/pattern/knapsack-dp-youknowwho) | 5 medium problems |
| Binary search on answer | [`pattern/BinarySearch.md`](/pattern/binary-search) | 3 problems |
| Heaps / Priority queues | [`pattern/Heap.md`](/pattern/heap) | 3 problems |
| Segment tree / Fenwick tree | [`pattern/SegmentTree.md`](/pattern/segment-tree), [`FenwickTree.md`](/pattern/fenwick-tree) | 2 problems each |

### Recommended LeetCode Problems

```
Graphs:    207 (Course Schedule), 743 (Network Delay), 684 (Redundant Connection)
DP:        322 (Coin Change), 1143 (LCS), 416 (Partition Equal Subset)
Binary Search: 1011 (Ship Packages), 875 (Koko Bananas)
Heap:      215 (Kth Largest), 295 (Median from Stream)
```

---

## System Design (HLD)

**Goal:** Fluently walk through a distributed system design with trade-offs, failure modes, and scaling strategies.

### Existing resources to review

| Topic | Resource | Gap to fill |
|-------|----------|-------------|
| Message queues / event streaming | [`design-message-queue.md`](/system_design/design-message-queue) | Add Kafka internals: partitions, consumer groups, offset management |
| Key-value store / caching | [`design-key-value-store.md`](/system_design/design-key-value-store) | Add Redis pub/sub, eviction policies (LRU vs LFU) |
| Distributed object storage | [`design-s3-object-storage.md`](/system_design/design-s3-object-storage) | Review consistent hashing |
| Payment / financial systems | [`design-payment-system.md`](/system_design/design-payment-system) | Emphasize idempotency, exactly-once delivery |

### WorldQuant-specific guides

| Guide | Why it matters for WorldQuant |
|-------|-------------------------------|
| [`design-data-pipeline.md`](/system_design/design-data-pipeline) | WorldQuant runs large-scale financial data pipelines; this is likely to come up |
| [`design-observability-platform.md`](/system_design/design-observability-platform) | OpenTelemetry/Grafana/ELK are explicitly listed in the JD |

### System design interview framework (40-minute timeline)

```
0–5 min   Clarify scope: scale, consistency requirements, read/write ratio
5–15 min  High-level design: components, data flow, APIs
15–30 min Deep dive: chosen bottleneck (storage, queue, caching layer)
30–35 min Trade-offs, failure handling, monitoring
35–40 min Follow-up questions
```

---

## Python Deep Dive (main track weeks 1–2)

**Goal:** Demonstrate senior-level Python knowledge — not just "Python works" but *why* it works and where it breaks.

### asyncio internals

```python
# sketch: fetch() and aiohttp are assumed
import asyncio

# Event loop runs ONE coroutine at a time — no parallelism, only concurrency
# Use asyncio when: I/O-bound work (DB, HTTP, file reads)
# Use multiprocessing when: CPU-bound work (number crunching)

async def fetch_all(urls: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        # gather() fires all coroutines concurrently, waits for all
        return await asyncio.gather(*[fetch(session, url) for url in urls])

# TaskGroup (Python 3.11+) — cancels siblings on first failure
async def safe_fetch_all(session, urls: list[str]) -> list[str]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(session, url)) for url in urls]
    return [t.result() for t in tasks]
```

| Concept | Key point |
|---------|-----------|
| Event loop | Single-threaded; runs coroutines cooperatively via `await` yield points |
| `gather()` vs `wait()` | `gather` raises the first error but does **not** cancel the other awaitables (or collects errors with `return_exceptions=True`); `wait` returns `(done, pending)` sets so you handle partial results |
| `TaskGroup` | Structured concurrency (Python 3.11+): cancels siblings on first failure and raises an `ExceptionGroup`; preferred over bare `gather` |
| GIL impact | asyncio overlaps I/O waits on one thread, so the GIL is not the bottleneck; for CPU work use `ProcessPoolExecutor` |
| Blocking-call pitfall | Blocking code inside `async def` stalls every coroutine; use an async library, or offload with `asyncio.to_thread` / `run_in_executor` |

### FastAPI patterns

```python
# sketch: User model and async_session come from the SQLAlchemy block below
from collections.abc import AsyncIterator
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Dependency injection: DB session per request, auto-closed
async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session  # `async with` closes the session after the response

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

### SQLAlchemy async patterns

```python
# fragment: User, user_id, and data are assumed
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload

# Async engine — use asyncpg driver
engine = create_async_engine("postgresql+asyncpg://user:pass@host/db")
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Eager loading prevents N+1 queries
stmt = select(User).options(selectinload(User.orders)).where(User.id == user_id)

# Upsert pattern (PostgreSQL)
from sqlalchemy.dialects.postgresql import insert
stmt = insert(User).values(**data).on_conflict_do_update(
    index_elements=["email"], set_={"name": data["name"]}
)
```

### pytest patterns

```python
# sketch: needs pytest-asyncio (asyncio_mode = "auto") or @pytest.mark.anyio
import pytest
from httpx import AsyncClient

@pytest.fixture
async def db_session():
    async with async_session() as session:
        yield session
        await session.rollback()  # clean state between tests

@pytest.mark.parametrize("email,valid", [
    ("a@b.com", True),
    ("notanemail", False),
])
async def test_email_validation(email, valid):
    assert validate_email(email) == valid

# Testing async FastAPI routes
async def test_get_user(client: AsyncClient):
    response = await client.get("/users/1")
    assert response.status_code == 200
```

### Python internals cheat sheet

| Question | Answer |
|----------|--------|
| What is the GIL? | Global Interpreter Lock — only one thread runs Python bytecode at a time |
| When does asyncio help? | I/O-bound: DB, HTTP, file. Not CPU-bound. |
| `threading` vs `asyncio` | threading for legacy blocking libs; asyncio for modern async-native code |
| `__slots__` | Replaces the per-instance `__dict__` with fixed slots — saves memory when you have many small instances; measure with `tracemalloc` |
| Descriptor protocol | How `@property`, `@classmethod` work — `__get__/__set__/__delete__` |
| `functools.cache` vs `lru_cache` | `cache` = unbounded `lru_cache`; use `lru_cache(maxsize=N)` for bounded caching |

---

## Data Pipelines & Databases (main track weeks 3–5)

**Goal:** Design, build, and diagnose production data pipelines — the core of WorldQuant's engineering work.

### PostgreSQL internals

| Topic | What to know |
|-------|-------------|
| `EXPLAIN ANALYZE` | Read the query plan: Seq Scan vs Index Scan, actual vs estimated rows, buffers |
| Index types | B-tree (default, range/equality), GIN (full-text, JSONB), partial index (`WHERE active = true`) |
| MVCC | Each transaction sees a snapshot; old row versions accumulate until VACUUM runs |
| `VACUUM ANALYZE` | Reclaims dead tuple space; updates planner statistics — run after bulk loads |
| Window functions | `ROW_NUMBER()`, `LAG()`, `LEAD()`, `SUM() OVER (PARTITION BY ...)` — essential for financial data |

### SQL optimization checklist

```sql
-- 1. Use covering index (include all SELECTed columns)
CREATE INDEX idx_orders_user ON orders(user_id) INCLUDE (amount, created_at);

-- 2. Avoid function on indexed column (prevents index use)
-- BAD:  WHERE DATE(created_at) = '2024-01-01'
-- GOOD: WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02'

-- 3. Use CTEs for readability; use subqueries for performance when CTE is materialized
-- PostgreSQL 12+: CTEs are inlined by default (MATERIALIZED to force old behavior)

-- 4. Upsert with ON CONFLICT
INSERT INTO prices (symbol, date, close)
VALUES ('AAPL', '2024-01-01', 185.20)
ON CONFLICT (symbol, date) DO UPDATE SET close = EXCLUDED.close;
```

### Kafka fundamentals

```
Producer → [Topic: prices] → Consumer Group A (analytics service)
                           → Consumer Group B (risk service)

Topic partitioning:
  - Partition count = max parallelism for a consumer group
  - Messages with same key → same partition → ordered delivery per key
  - Offset = position within partition; consumers commit offsets

Delivery semantics:
  at-most-once   → commit before processing (may lose messages)
  at-least-once  → commit after processing (may duplicate — handle with idempotency)
  exactly-once   → Kafka transactions + idempotent producer, Kafka-to-Kafka only;
                   external sinks still need idempotent writes (upsert by key)
```

| Setting | Purpose |
|---------|---------|
| `acks=all` | Producer waits for all in-sync replicas to acknowledge |
| `enable.idempotence=true` | Deduplicates retried producer sends |
| `isolation.level=read_committed` | Consumer only reads committed transactions |
| `auto.offset.reset=earliest` | New consumer group starts from beginning of topic |

### Airflow DAG patterns

```python
# sketch: fetch_from_source_api, normalize, upsert_to_postgres are assumed
from airflow.decorators import dag, task
from datetime import datetime, timedelta

@dag(
    schedule="0 6 * * *",          # daily at 06:00 (scheduler timezone, UTC by default)
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
)
def prices_pipeline():

    @task
    def extract() -> list[dict]:
        return fetch_from_source_api()

    @task
    def transform(raw: list[dict]) -> list[dict]:
        return [normalize(row) for row in raw]

    @task
    def load(rows: list[dict]):
        upsert_to_postgres(rows)

    load(transform(extract()))

prices_pipeline()
```

| Pattern | Use case |
|---------|---------|
| `@task` decorator (TaskFlow API) | Clean Python tasks with automatic XCom passing |
| Sensor operators | Wait for file/DB condition before proceeding |
| `depends_on_past=True` | A task instance runs only if the same task succeeded in the previous run |
| External task sensor | Cross-DAG dependencies |

### Batch vs streaming decision matrix

| Factor | Choose Batch | Choose Streaming |
|--------|-------------|-----------------|
| Latency requirement | Minutes to hours OK | Seconds or less required |
| Data volume | Any | Continuous high-throughput |
| Complexity | Simple transforms | Complex stateful aggregations |
| Cost | Lower ops overhead | Higher (Kafka cluster, state management) |
| Example | End-of-day P&L calculation | Real-time fraud detection |

---

## Low-Level Design & Software Architecture (week 7)

**Goal:** Design clean, extensible systems — demonstrate senior judgment on trade-offs.

### Existing resources to review

| Resource | Focus for WorldQuant |
|----------|---------------------|
| [`digital-wallet-service.md`](/low_level_design/digital-wallet-service) | Idempotency keys, double-spend prevention, audit log |
| [`logging-framework.md`](/low_level_design/logging-framework) | Observer pattern, structured logging, async log buffers |
| [`lru-cache.md`](/low_level_design/lru-cache) | Thread safety with `asyncio.Lock`, TTL-based expiration |

### Design patterns for financial software

| Pattern | When to use | Example |
|---------|------------|---------|
| **Strategy** | Swappable algorithms | Different pricing models per instrument |
| **Factory** | Object creation based on type | Create `EquityOrder` vs `FuturesOrder` |
| **Observer** | React to state changes | Publish P&L updates to multiple consumers |
| **Circuit Breaker** | Protect against cascading failures | Stop calling a failing downstream API |
| **Saga** | Distributed transactions without 2PC | Multi-service trade settlement |
| **Outbox** | Reliable event publishing | Write event to DB + publish to Kafka atomically |

### Circuit breaker implementation sketch

```python
import time

class ServiceUnavailableError(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.state = "CLOSED"   # CLOSED → OPEN → HALF_OPEN → CLOSED or OPEN
        self.failures = 0
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.reset_at = 0.0

    async def call(self, func, *args):
        if self.state == "OPEN":
            if time.monotonic() < self.reset_at:
                raise ServiceUnavailableError()
            self.state = "HALF_OPEN"

        try:
            result = await func(*args)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _on_failure(self):
        self.failures += 1
        if self.state == "HALF_OPEN" or self.failures >= self.threshold:
            self.state = "OPEN"
            self.reset_at = time.monotonic() + self.reset_timeout

    def _on_success(self):
        self.failures = 0
        self.state = "CLOSED"
```

---

## Mock Interviews & Behavioral (week 8)

### System design mock topics (most likely for WorldQuant)

1. **Design a real-time market data pipeline** — Kafka ingestion → normalization → time-series DB → API
2. **Design a backtesting platform** — historical data retrieval, parallel simulation, result storage
3. **Design a financial data warehouse** — ETL, slowly-changing dimensions, query optimization

### Behavioral prep (STAR format)

| Question type | Story to prepare |
|---------------|-----------------|
| Debugging production incident | A time you diagnosed a non-obvious failure under pressure |
| High-autonomy architecture decision | A time you owned a technical direction without explicit direction |
| Mentoring a junior engineer | A time your code review or pairing meaningfully improved someone's work |
| Trade-off decision | A time you chose simplicity over completeness (or vice versa) and why |
| Cross-functional communication | A time you translated a technical constraint for a non-engineer stakeholder |

### "Why WorldQuant" prep

- WorldQuant's **BRAIN platform** — quantitative alpha research using statistical signals
- They run **systematic strategies** — everything is data-driven, pipelines are business-critical
- Unique angle: engineering work directly ties to investment performance — high stakes, high feedback loop

---

## Pages Built for This Plan

| Page | Status | Why |
|------|--------|-----|
| [`system_design/design-data-pipeline.md`](/system_design/design-data-pipeline) | ✅ Created | Core WorldQuant use case |
| [`pattern/AsyncPython.md`](/pattern/async-python) | ✅ Created | Senior Python differentiator |
| [`system_design/design-observability-platform.md`](/system_design/design-observability-platform) | ✅ Created | OpenTelemetry/Grafana/ELK from JD |
