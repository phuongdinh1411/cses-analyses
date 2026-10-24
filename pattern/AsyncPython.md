---
layout: simple
title: "Async Python Patterns"
permalink: /pattern/async-python
---

# Async Python Patterns

Python's `asyncio` provides cooperative concurrency for I/O-bound workloads. This guide covers the mental model, common patterns, and pitfalls that distinguish senior Python engineers — especially in FastAPI / SQLAlchemy / data pipeline contexts.

---

## Quick Navigation: "I need to..."

| I need to... | Pattern | Section |
|--------------|---------|---------|
| Run multiple I/O calls concurrently | `gather()` / `TaskGroup` | [1](#1-concurrent-execution) |
| Build a REST API with async DB | FastAPI + async SQLAlchemy | [2](#2-fastapi--async-sqlalchemy) |
| Process a queue of work concurrently | Worker pool with `asyncio.Queue` | [3](#3-worker-pool-pattern) |
| Call blocking code from async context | `run_in_executor` | [4](#4-mixing-sync-and-async) |
| Avoid N+1 queries | Eager loading / batch fetch | [5](#5-avoiding-n1-queries) |
| Test async code | `pytest-asyncio` patterns | [6](#6-testing-async-code) |
| Understand when asyncio helps vs not | Concurrency vs parallelism | [7](#7-concurrency-model--when-to-use-what) |
| Handle timeouts and cancellation | `asyncio.timeout` / `shield` | [8](#8-timeouts-and-cancellation) |

---

## The Mental Model

```
asyncio is cooperative multitasking on a single thread.

Thread 1:  [task A runs] → await (I/O wait) → [task B runs] → await → [task A resumes]
                            ↑
                  event loop switches here

Key insight: "await" is the ONLY point where another coroutine can run.
If you block without await (time.sleep, requests.get, heavy CPU), you freeze the whole loop.
```

### asyncio vs threading vs multiprocessing

| | asyncio | threading | multiprocessing |
|---|---|---|---|
| **Parallelism** | No (1 thread) | Limited (GIL) | Yes (separate processes) |
| **Best for** | I/O-bound (DB, HTTP, file) | Legacy blocking libs | CPU-bound (math, ML) |
| **Overhead** | Very low | Medium (OS threads) | High (process spawn) |
| **Shared state** | Easy (same thread) | Hard (race conditions) | Hard (IPC needed) |
| **Example** | FastAPI, async DB driver | `requests` + `ThreadPoolExecutor` | NumPy, pandas, image processing |

---

## 1. Concurrent Execution

### `gather()` — run all, wait for all

```python
import asyncio
import aiohttp

async def fetch(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as resp:
        return await resp.json()

async def fetch_all(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        # All requests fire simultaneously; total time ≈ slowest single request
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls],
            return_exceptions=True,   # don't cancel all on single failure
        )
    return [r for r in results if not isinstance(r, Exception)]
```

### `TaskGroup` — structured concurrency (Python 3.11+)

```python
async def fetch_all_safe(urls: list[str]) -> list[dict]:
    results = []
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(url)) for url in urls]
    # If ANY task raises, TaskGroup cancels siblings and re-raises
    return [t.result() for t in tasks]
```

**`gather` vs `TaskGroup`:**

| | `gather(return_exceptions=True)` | `TaskGroup` |
|---|---|---|
| On error | Continues remaining tasks | Cancels all siblings |
| Use when | Partial results are useful | All-or-nothing semantics |
| Error handling | Check each result | Single `except` block |

### Semaphore — limit concurrency

```python
async def fetch_with_limit(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    sem = asyncio.Semaphore(max_concurrent)

    async def bounded_fetch(url: str) -> dict:
        async with sem:             # blocks if max_concurrent tasks are already running
            return await fetch(url)

    return await asyncio.gather(*[bounded_fetch(url) for url in urls])
```

---

## 2. FastAPI + Async SQLAlchemy

### Setup

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Use asyncpg driver for PostgreSQL
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/mydb",
    pool_size=20,
    max_overflow=10,
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id:    Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name:  Mapped[str]
```

### Dependency injection pattern

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select

app = FastAPI()

async def get_db() -> AsyncSession:
    """Yield a session per request; auto-close on exit."""
    async with AsyncSessionLocal() as session:
        yield session
        # No explicit commit — route handlers commit explicitly when needed

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = User(email=data.email, name=data.name)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # reload to get server-generated fields (id, created_at)
    return user
```

### Upsert

```python
from sqlalchemy.dialects.postgresql import insert as pg_insert

async def upsert_user(db: AsyncSession, data: dict) -> User:
    stmt = (
        pg_insert(User)
        .values(**data)
        .on_conflict_do_update(
            index_elements=["email"],
            set_={"name": data["name"], "updated_at": func.now()},
        )
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one()
```

---

## 3. Worker Pool Pattern

Use when you have many jobs to process but want to cap concurrency (rate limiting, DB connection limits).

```python
import asyncio
from asyncio import Queue

async def producer(queue: Queue, items: list):
    for item in items:
        await queue.put(item)
    # Signal workers to stop
    for _ in range(NUM_WORKERS):
        await queue.put(None)

async def worker(worker_id: int, queue: Queue, results: list):
    while True:
        item = await queue.get()
        if item is None:
            break
        try:
            result = await process(item)
            results.append(result)
        except Exception as e:
            print(f"Worker {worker_id} failed on {item}: {e}")
        finally:
            queue.task_done()

async def run_pool(items: list, num_workers: int = 5) -> list:
    queue: Queue = asyncio.Queue(maxsize=num_workers * 2)
    results = []

    workers = [asyncio.create_task(worker(i, queue, results)) for i in range(num_workers)]
    await producer(queue, items)
    await asyncio.gather(*workers)

    return results
```

---

## 4. Mixing Sync and Async

### Calling blocking code from async context

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)

async def run_blocking_io(func, *args):
    """Run a blocking I/O function without freezing the event loop."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)

async def example():
    # requests.get is blocking — wrap it
    response = await run_blocking_io(requests.get, "https://api.example.com/data")

    # pandas is CPU-heavy — use ProcessPoolExecutor
    cpu_executor = ProcessPoolExecutor(max_workers=4)
    result = await loop.run_in_executor(cpu_executor, compute_heavy, dataframe)
```

### Common mistake: blocking the event loop

```python
# ❌ BAD — freezes the event loop for the entire sleep duration
async def bad():
    time.sleep(5)           # blocks the thread → no other coroutine can run

# ✅ GOOD — yields control back to event loop
async def good():
    await asyncio.sleep(5)  # suspends only this coroutine

# ❌ BAD — synchronous HTTP call inside async function
async def bad_fetch(url):
    return requests.get(url).json()   # blocks thread

# ✅ GOOD — async HTTP with aiohttp
async def good_fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()
```

---

## 5. Avoiding N+1 Queries

```python
from sqlalchemy.orm import selectinload, joinedload

# ❌ N+1: 1 query for users, then 1 query PER user for orders
users = (await db.execute(select(User))).scalars().all()
for user in users:
    orders = await db.execute(select(Order).where(Order.user_id == user.id))

# ✅ selectinload: 2 queries total (1 for users, 1 for all orders WHERE user_id IN (...))
stmt = select(User).options(selectinload(User.orders))
users = (await db.execute(stmt)).scalars().all()
# user.orders is now pre-loaded — no extra queries

# ✅ joinedload: 1 query with JOIN (better for to-one relationships)
stmt = select(Order).options(joinedload(Order.user))
orders = (await db.execute(stmt)).scalars().all()
# order.user is pre-loaded

# ✅ Batch fetch: manual IN query
user_ids = [1, 2, 3, 4, 5]
orders = (
    await db.execute(select(Order).where(Order.user_id.in_(user_ids)))
).scalars().all()
```

---

## 6. Testing Async Code

### Setup

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"   # all async tests auto-decorated
```

```python
# conftest.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

TEST_DB_URL = "postgresql+asyncpg://user:pass@localhost/test_db"

@pytest.fixture(scope="session")
async def engine():
    eng = create_async_engine(TEST_DB_URL)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()

@pytest.fixture
async def db(engine):
    """Each test gets its own transaction, rolled back on exit."""
    async with engine.begin() as conn:
        session = AsyncSession(bind=conn)
        yield session
        await session.rollback()

@pytest.fixture
async def client(db):
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
```

### Test patterns

```python
async def test_create_user(client, db):
    response = await client.post("/users", json={"email": "a@b.com", "name": "Alice"})
    assert response.status_code == 200
    assert response.json()["email"] == "a@b.com"

    # Verify DB state directly
    result = await db.execute(select(User).where(User.email == "a@b.com"))
    user = result.scalar_one()
    assert user.name == "Alice"

@pytest.mark.parametrize("email,status_code", [
    ("valid@example.com", 200),
    ("not-an-email", 422),
    ("", 422),
])
async def test_email_validation(client, email, status_code):
    response = await client.post("/users", json={"email": email, "name": "Test"})
    assert response.status_code == status_code
```

---

## 7. Concurrency Model — When to Use What

```
Problem type          Best tool
─────────────────────────────────────────────────────
HTTP API server       FastAPI (asyncio)
DB queries            asyncpg / async SQLAlchemy
File I/O (many files) asyncio.gather + aiofiles
CPU computation       multiprocessing / ProcessPoolExecutor
Legacy sync library   ThreadPoolExecutor + run_in_executor
Background tasks      asyncio.create_task OR Celery (cross-process)
Scheduled jobs        Airflow (not asyncio)
```

### Connection pool sizing

```python
# Rule of thumb for async DB pool:
#   pool_size = num_workers × avg_concurrent_queries_per_worker
# For a FastAPI service with 4 uvicorn workers, each handling 50 concurrent requests,
# each using 1 DB query at a time:
#   pool_size = 4 × 50 = 200  (but PostgreSQL default max_connections = 100!)
# Solution: use PgBouncer connection pooler in front of PostgreSQL

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # connections kept open
    max_overflow=10,        # extra connections allowed on burst (closed when done)
    pool_timeout=30,        # raise error if no connection available after 30s
    pool_recycle=1800,      # recycle connections every 30min (avoids stale conn)
)
```

---

## 8. Timeouts and Cancellation

```python
import asyncio

# asyncio.timeout (Python 3.11+) — raises TimeoutError
async def fetch_with_timeout(url: str) -> dict:
    async with asyncio.timeout(5.0):    # 5 second deadline
        return await fetch(url)

# asyncio.wait_for — older equivalent
async def fetch_with_timeout_legacy(url: str) -> dict:
    return await asyncio.wait_for(fetch(url), timeout=5.0)

# Shield: protect a coroutine from cancellation (e.g., DB write)
async def process_and_save(data):
    result = transform(data)
    # Even if this coroutine is cancelled, the DB write completes
    await asyncio.shield(db.commit())

# Graceful shutdown pattern
async def main():
    tasks = [asyncio.create_task(worker(i)) for i in range(10)]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Blocking call in async def | Event loop stalls; all requests queue up | Use `run_in_executor` or async equivalent |
| Missing `await` | Returns coroutine object instead of result | Always `await` coroutine calls |
| Sharing session across requests | `MissingGreenlet` / state corruption | One session per request via `Depends` |
| `expire_on_commit=True` (default) | `DetachedInstanceError` after commit | Set `expire_on_commit=False` in sessionmaker |
| Creating tasks without reference | Task garbage-collected mid-run | Store reference: `tasks.add(asyncio.create_task(...))` |
| `asyncio.run()` inside async context | `RuntimeError: This event loop is already running` | Use `await` instead; use `nest_asyncio` for notebooks |

---

## Quick Reference

```python
# Run async function from sync context
asyncio.run(main())

# Create background task (fire and forget)
task = asyncio.create_task(background_job())
background_tasks = set()
background_tasks.add(task)
task.add_done_callback(background_tasks.discard)  # prevent GC

# Async context manager
class AsyncResource:
    async def __aenter__(self): ...
    async def __aexit__(self, *args): ...

async with AsyncResource() as r: ...

# Async iterator
class AsyncStream:
    def __aiter__(self): return self
    async def __anext__(self): ...

async for item in AsyncStream(): ...

# Async generator
async def generate():
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i

async for value in generate(): ...
```
