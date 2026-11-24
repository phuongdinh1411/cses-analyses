---
layout: simple
title: "Design a Job Scheduler — Hello Interview Style"
permalink: /system_design/hellointerview/job-scheduler
---

# Job Scheduler

**Patterns:** Managing Long Running Tasks · Scaling Writes  
**Difficulty:** Medium  
**Source:** hellointerview.com (AI-generated full solution)

---

## Understanding the Problem

⏰ **What is a Job Scheduler?**  
A job scheduler automatically executes jobs at specified times or intervals. It's the backbone of systems like cron, AWS Lambda Scheduled Events, GitHub Actions scheduled workflows, and distributed task queues.

**Key terms:**
- **Task** – abstract work definition (e.g., "send email"). Reusable, can be executed multiple times.
- **Job** – a scheduled instance of a task. Specifies: which task, when to run, and parameters (e.g., "send email to john@example.com at 10AM Fri").

---

### Functional Requirements

**Core Requirements**

- Users should be able to schedule jobs to be executed immediately, at a future date, or on a recurring schedule (e.g., "every day at 10:00 AM")
- Users should be able to monitor the status of their jobs

**Below the line (out of scope):**

- Cancelling or rescheduling jobs
- Priority queues (all jobs treated equally)
- Complex job dependencies (DAG pipelines)

### Non-Functional Requirements

**Core Requirements**

- The system should execute jobs within **2 seconds** of their scheduled time
- The system should scale to **10K jobs/second**
- The system should guarantee **at-least-once execution** (no job silently dropped)
- The system should be **highly available** (scheduler itself shouldn't be a single point of failure)

**Below the line (out of scope):**

- Exactly-once execution (harder; at-least-once is acceptable)
- Sub-second precision

### Constraints & Estimates

- 10K jobs/sec at peak
- 10K × 86,400 sec/day = **864M jobs/day**
- Each job record: ~1KB → 864M × 1KB = **~864GB/day** of job records
- Status updates: each job writes ~3–5 status transitions → 2.5B writes/day → ~29K writes/sec

---

## The Set Up

### Planning the Approach

The main challenge is: given millions of scheduled jobs with arbitrary future timestamps, how do we efficiently poll for "jobs due now" at high throughput without scanning the entire table every second?

We'll need:
1. **Scheduler** – polls for due jobs and dispatches them
2. **Worker Pool** – actually runs the job code
3. **Job Store** – persists job definitions and state

### Defining the Core Entities

- **Task** – id, name, handler_code (or webhook URL), description
- **Job** – id, task_id, params (JSON), scheduled_at, status (pending/running/completed/failed), cron_expression (nullable), next_run_at, created_at, updated_at
- **JobExecution** – id, job_id, started_at, finished_at, status, output, error

### The API

```
// Create a one-time job
POST /jobs
{ "task_id": "send_email", "params": { "to": "john@example.com" }, "scheduled_at": "2024-12-01T10:00:00Z" }
-> { job_id, status: "pending" }

// Create a recurring job
POST /jobs
{ "task_id": "daily_report", "params": { "report_type": "sales" }, "cron": "0 9 * * *" }
-> { job_id, status: "pending", next_run_at: "2024-12-02T09:00:00Z" }

// Get job status
GET /jobs/{job_id}
-> { job_id, status, last_run_at, next_run_at, executions: [...] }

// List jobs
GET /jobs?status=pending&limit=50&cursor=...
-> { jobs: [...], next_cursor }
```

### Data Flow

```
User → API Server → Job Store (PostgreSQL)
                              ↓ poll
Scheduler → Pick due jobs → Kafka → Worker Pool → Execute → Update status
                                                 → Retry on failure
```

---

## High-Level Design

### 1) Users should be able to schedule jobs (immediate, future, recurring)

**Storing jobs:**

```sql
CREATE TABLE jobs (
  id              UUID PRIMARY KEY,
  task_id         TEXT NOT NULL,
  params          JSONB,
  scheduled_at    TIMESTAMP,  -- NULL for immediate
  cron_expression TEXT,       -- NULL for one-time
  next_run_at     TIMESTAMP NOT NULL,  -- computed: when to run next
  status          TEXT DEFAULT 'pending',  -- pending/running/completed/failed
  created_at      TIMESTAMP DEFAULT NOW()
);

-- Critical index: scheduler polls this frequently
CREATE INDEX idx_due_jobs ON jobs (next_run_at, status)
  WHERE status = 'pending';
```

**Scheduling logic:**
- **Immediate:** `next_run_at = NOW()`
- **Future one-time:** `next_run_at = scheduled_at`
- **Recurring (cron):** `next_run_at = compute_next(cron_expression, NOW())`

**Scheduler polling (Leader-based):**
1. Scheduler service (single elected leader) polls every second:
   ```sql
   SELECT * FROM jobs
   WHERE next_run_at <= NOW() + interval '5 seconds'
     AND status = 'pending'
   LIMIT 1000
   FOR UPDATE SKIP LOCKED;
   ```
2. Marks selected jobs as `status=running` atomically
3. Dispatches to Kafka queue
4. Workers consume from Kafka and execute

**`FOR UPDATE SKIP LOCKED`** is key: allows multiple scheduler instances to poll concurrently without conflicts — each locks its own batch of rows.

### 2) Users should be able to monitor the status of their jobs

**Job lifecycle:**
```
pending → running → completed
                 → failed → (retry → running)
```

**Status updates:**
- Worker transitions job to `running` when it dequeues
- Worker transitions to `completed` or `failed` on finish
- Write job execution record to `job_executions` table

**Monitoring API:**
- `GET /jobs/{id}` queries job + recent executions from DB
- For real-time updates: SSE endpoint, or simply polling `GET /jobs/{id}` every 5s

**Recurring job scheduling after completion:**

When a recurring job finishes:
```sql
UPDATE jobs
SET status = 'pending',
    next_run_at = compute_next_cron(cron_expression, NOW())
WHERE id = :job_id;
```

The job re-enters the queue for its next scheduled run.

---

## Potential Deep Dives

### 1) How can we ensure the system executes jobs within 2s of their scheduled time?

**Problem with simple polling:** If the scheduler polls every 10s, a job due at t=0 might not be picked up until t=9. We need polling granularity ≤ 2s.

**Solution A: Poll every 1 second**
- Simple, but heavy DB load: 10M pending jobs × 1 query/sec with index scan
- With index on `(next_run_at, status)`: query is O(log N + k) where k = jobs due
- For 10K jobs/sec, this means up to 10K rows per poll — manageable

**Solution B: Sorted Set in Redis for near-term jobs**
- Background job: scan DB for jobs due in next 5 minutes → load into Redis sorted set
  ```
  ZADD due_jobs {next_run_at_unix} {job_id}
  ```
- Scheduler polls Redis every 100ms instead of PostgreSQL
  ```
  ZRANGEBYSCORE due_jobs 0 {now} LIMIT 0 1000  → returns due job_ids
  ```
- Much lower latency, Redis handles 100K ops/sec easily
- DB is the source of truth; Redis is a lookahead buffer

**Combined approach (best):**
1. Redis sorted set for jobs due in next 5 min (fast polling)
2. DB as source of truth
3. Background sync: every 60s, reload next 5 min of jobs from DB into Redis

### 2) How can we ensure the system is scalable to support 10K jobs/second?

**Scheduler bottleneck:** Single scheduler polling DB and dispatching → bottleneck.

**Scale with multiple schedulers + Kafka:**

```
DB (jobs table)
  ↑ poll (sharded by job_id range or hash)
Scheduler Pod 1 → Kafka partition 0–3
Scheduler Pod 2 → Kafka partition 4–7
Scheduler Pod 3 → Kafka partition 8–11
                                   ↓
                             Worker Pool (autoscale)
                             Worker 1, 2, ..., N
```

**Key:** `FOR UPDATE SKIP LOCKED` allows multiple scheduler pods to safely poll the same jobs table without duplicating work. Each pod picks a non-overlapping batch.

**Worker pool scaling:**
- Kafka consumer group: workers autoscale based on Kafka consumer lag
- Kubernetes HPA: scale worker pods based on job queue depth
- Target: each worker handles 10–50 jobs/sec → 200–1000 workers for 10K jobs/sec

**DB write throughput:**
- 10K job status updates/sec → heavy write load
- Use **write buffering**: batch status updates in workers before writing (every 500ms)
- Or: use **Kafka for status updates** → consumer writes to DB asynchronously

### 3) How can we ensure at-least-once execution of jobs?

**Problem:** Worker picks up job, starts executing, then crashes. Job is stuck in `running` state forever.

**Solution: Heartbeat + reaper pattern**

1. **Worker heartbeat:** Each running job sends a heartbeat to Redis every 10s:
   ```
   SET job:{job_id}:heartbeat {ts} EX 30  (30s TTL)
   ```

2. **Reaper service** (runs every 60s): scans for jobs in `running` status where the heartbeat key has expired in Redis:
   ```sql
   SELECT id FROM jobs
   WHERE status = 'running'
     AND updated_at < NOW() - interval '30 seconds';
   ```
   Re-queues these jobs (set `status=pending`).

3. **Idempotent job execution:** Job handlers should be idempotent — running the same job twice produces the same result. This is the job developer's responsibility (at-least-once contract).

4. **Retry policy:** On failure, re-queue with exponential backoff:
   - Attempt 1: immediate retry
   - Attempt 2: retry in 1 min
   - Attempt 3: retry in 5 min
   - After N attempts: mark as `failed`, alert

**Exactly-once (harder):** Would require distributed transactions between the job execution and the status update — expensive. At-least-once + idempotent handlers is the standard industry approach.

---

## Final Design

```
Client
  │
  ▼
API Server ──→ PostgreSQL (jobs table, job_executions)
               ↑ poll every 1s
Scheduler Pods (3×, leader elected via Zookeeper)
  │  FOR UPDATE SKIP LOCKED
  │  → batch due jobs
  ▼
Redis Sorted Set (lookahead buffer: next 5 min of jobs)
  + Kafka (job dispatch queue, 12 partitions)
  ↓
Worker Pool (autoscale, 200–1000 pods)
  │  execute job
  ├─ Heartbeat → Redis (EX 30s)
  ├─ Success → UPDATE jobs SET status=completed + INSERT job_execution
  └─ Failure → retry with backoff OR mark failed

Reaper Service (every 60s)
  - Find stalled jobs (running + no heartbeat)
  - Re-queue them (set status=pending)
```

---

## What is Expected at Each Level?

### Mid-level
- Correct job/task entity design and REST APIs
- Simple DB polling approach
- Understands recurring cron scheduling
- Basic failure handling (retry on error)

### Senior
- `FOR UPDATE SKIP LOCKED` for concurrent schedulers
- Redis sorted set as lookahead buffer for low-latency dispatch
- Heartbeat + reaper for stalled job detection
- Worker autoscaling via Kafka consumer lag

### Staff+
- Multi-scheduler sharding for 10K jobs/sec
- Exactly-once trade-offs (why at-least-once + idempotency is the right answer)
- Kafka partitioning strategy for worker pool
- Discusses cron timezone handling and DST edge cases
- Checkpoint-based recovery for scheduler crash scenarios
