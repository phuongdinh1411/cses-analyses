---
layout: simple
title: "Design ChatGPT — Hello Interview Style"
permalink: /system_design/hellointerview/chatgpt
---

# ChatGPT

**Patterns:** Real-time Updates · Managing Long Running Tasks  
**Difficulty:** Hard  
**Source:** hellointerview.com (AI-generated full solution)

---

## Summary

- **Key challenge:** Stream LLM tokens with <1s time-to-first-token for 200M DAU (~12K prompts/s, ~120K concurrent generations) on scarce, expensive GPUs.
- **Core design:** Chat API saves the message, builds the prompt from history and enqueues a Kafka job; GPU workers write tokens to a Redis Stream that a stateless Streaming Gateway pushes over SSE; finished replies go to PostgreSQL.
- **Techniques:** SSE for simple one-way streaming; Redis Stream buffer + Last-Event-ID to resume without re-running the model; Kafka queue whose lag drives autoscaling; paid/free topics + per-user token quotas for fairness; heartbeat reaper re-queues stalled jobs; truncation/summarization to cap context cost.

## Understanding the Problem

💬 **What is ChatGPT?**  
ChatGPT is a conversational AI where users send prompts and get responses streamed back from a large language model. Conversations are saved so users can return and continue with full context.

**Key scoping:** We treat the LLM as a **black box** we call — not something we train. All design is in the serving system around it. Text only (no images/audio/video). No editing or branching of messages.

---

### Functional Requirements

**Core Requirements**

- Users should be able to send a prompt in a chat and receive an AI-generated response
- Users should be able to view past chats and resume a conversation, with prior context carried into the prompt

**Below the line (out of scope):**

- Editing or branching existing messages
- Image, audio, or video input/output
- Sharing chats or collaborating
- Custom GPTs, tool/function calling, web browsing
- Full-text search across chat history

### Non-Functional Requirements

**Core Requirements**

- **Low time-to-first-token** (< 1 second from submit to first token appearing)
- Responses should be streamed token-by-token (not all-at-once at the end)
- The system should scale to **200M DAU** (~12K prompts/sec average, ~20K peak; ~120K concurrent streaming responses at average load)
- GPU resources are expensive and limited — must be **efficiently scheduled**
- Streams must survive **client reconnects** (browser refresh, mobile background)

**Below the line (out of scope):**

- Sub-100ms time-to-first-token (1 second is acceptable)

### Constraints & Estimates

- 200M DAU, ~5 prompts/user/day → 1B prompts/day → ~12K prompts/sec
- Average response: 500 tokens, generated at ~50 tokens/sec → 10 seconds/response
- Concurrent streaming: 12K prompts/sec × 10 seconds = **120K concurrent generations**
- Each GPU: handles ~10 concurrent 7B-param model inferences at 50 tok/sec
- Need: 120K / 10 = **12,000 GPUs** (approximate, depends on model size)
- Context window: average conversation has 10 turns × 500 tokens = 5K tokens of context

---

## The Set Up

### Planning the Approach

The main sub-problems:
1. **Streaming** – how to stream tokens to client (WebSocket / SSE)
2. **Context management** – how to persist and pass conversation history to LLM
3. **GPU scheduling** – how to route and queue inference requests across GPU workers
4. **Cost control** – how to handle long conversations without infinite context cost

### Defining the Core Entities

- **User** – id, email, tier (free/plus/team)
- **Conversation** – id, user_id, title, created_at, updated_at
- **Message** – id, conversation_id, role (user/assistant), content, token_count, created_at
- **GenerationJob** – id, conversation_id, prompt_tokens, status (queued/running/completed/failed), gpu_worker_id, created_at

### API or System Interface

```
// Start or continue a conversation
POST /conversations/{conv_id}/messages
{ "content": "What is the capital of France?" }
-> Initiates streaming response

// Stream tokens (SSE)
GET /conversations/{conv_id}/stream/{generation_id}
-> Content-Type: text/event-stream
data: {"token": "The"}
data: {"token": " capital"}
data: {"token": " of"}
data: {"token": " France"}
data: {"token": " is"}
data: {"token": " Paris"}
data: {"done": true, "usage": {"prompt_tokens": 150, "completion_tokens": 7}}

// Get conversation history
GET /conversations/{conv_id}/messages?limit=50&cursor=...
-> { messages: [...], next_cursor }

// List user's conversations
GET /conversations?limit=20&cursor=...
-> { conversations: [{ id, title, last_message_at }] }
```

---

## High-Level Design

### 1) Users should be able to send a prompt and receive an AI-generated response

**Request flow:**

```
Client → POST /conversations/{id}/messages
  → Chat API Server
  → Persist user message to DB (conversations, messages tables)
  → Load conversation history (last N messages)
  → Build prompt: [system prompt] + [conversation history] + [new user message]
  → Submit to GPU Dispatch Service
  → Return { generation_id } immediately (async)

Client → GET /conversations/{id}/stream/{generation_id}  (SSE connection)
  → Streaming Gateway holds SSE open
  → GPU Worker generates tokens → publishes to Redis Stream
  → Streaming Gateway subscribes → pushes tokens to client via SSE
```

**Why async (not synchronous)?**
- LLM generation takes 5–20 seconds
- HTTP connection would time out or force client to wait
- Async + SSE allows: submit → get generation_id → stream tokens as they arrive

**Persisting the response:**
- Each token streamed to client is also appended to a buffer
- On completion (done event), the full assistant message is persisted to DB as a single record

### 2) Users should be able to view past chats and resume a conversation

**Context loading on resume:**
1. User opens an old conversation
2. `GET /conversations/{id}/messages` → paginated message history from PostgreSQL
3. When user sends a new message:
   - Load last N messages (N = fit within context window budget, e.g., 15K tokens)
   - Build prompt: `[system] + [msg1 (user)] + [msg2 (assistant)] + ... + [new_msg (user)]`
4. Send full prompt to LLM

**Conversation title generation:**
- After first assistant response, asynchronously generate a title by calling LLM with `"Summarize this in 5 words: {first_user_message}"`
- Update conversation title

---

## Potential Deep Dives

### 1) How do we stream tokens back to the client?

**Server-Sent Events (SSE):**

SSE is simpler than WebSocket for one-directional streaming (server → client):
- Standard HTTP, works through proxies and firewalls
- Auto-reconnect built into browser EventSource API
- No protocol upgrade needed

```
Client:
  const es = new EventSource('/conversations/123/stream/gen_456');
  es.onmessage = e => {
    const data = JSON.parse(e.data);
    if (data.done) { es.close(); return; }
    appendToken(data.token);
  };
```

**Token delivery pipeline:**
```
GPU Worker
  → generates token "Paris"
  → Redis XADD gen:{generation_id}:tokens {token: "Paris", seq: 42}
  → Streaming Gateway (subscribed via XREAD)
  → SSE push to client: data: {"token":"Paris","seq":42}\n\n
```

**Back-pressure:** SSE connection speed limits how fast tokens flow. Streaming Gateway buffers tokens in Redis Stream; if client is slow, tokens queue in Redis (capped at 10K entries per stream).

**Token ordering:** Include `seq` number. If SSE delivers out of order (rare), client sorts by seq before display.

### 2) How do we keep the stream alive across reconnects and deploys?

**Problem:** User refreshes the browser mid-response. Response is 50% complete. We shouldn't re-run the LLM (expensive). We should resume the stream from where it left off.

**Solution: Durable token buffer in Redis Stream**

Redis Stream (`gen:{generation_id}:tokens`) stores all generated tokens with sequence numbers:
- TTL: 1 hour (long enough for reconnect scenarios)
- On reconnect: client sends `Last-Event-ID` header with last received sequence number
- Streaming Gateway: `XREAD gen:{id}:tokens COUNT 1000 AFTER {last_seq}` → replay missed tokens
- Then re-subscribe for new tokens

```
Client reconnects after refresh:
  GET /stream/{generation_id}
  Headers: Last-Event-ID: 42

Streaming Gateway:
  XRANGE gen:{generation_id}:tokens 43 +  → returns tokens 43, 44, 45 (already generated)
  → push to client immediately
  XREAD BLOCK gen:{generation_id}:tokens → wait for new tokens
```

**Handling rolling deploys:**
- Streaming Gateway is stateless (reads from Redis, not in-process memory)
- Rolling deploys: new Streaming Gateway pod comes up, client reconnects via load balancer to new pod
- New pod reads from Redis Stream (same generation_id) → seamless handover

### 3) How do we route and schedule generation requests across GPU workers?

**GPU Worker Pool:**

```
GPU Dispatch Service
  → Kafka ("generation-jobs")
  → GPU Workers (12,000 GPU pods)
```

Each GPU worker:
- Consumes a job from Kafka (one at a time, no prefetch)
- Loads model (or uses pre-loaded model in memory)
- Runs inference, publishes tokens to Redis Stream
- Commits Kafka offset on completion

**Why Kafka (not direct HTTP to GPU)?**
- Provides natural queuing when all GPUs are busy
- Consumer group: each job goes to exactly one worker
- Kafka consumer lag = visible queue depth → auto-scale workers

**Worker assignment:**
- Consumer group with `max.poll.records=1` per worker → each worker handles one job at a time
- Kafka partitions = number of GPU workers (or more for flexibility)
- Rebalancing handles worker failures automatically

**GPU type routing:**
- Small requests (short context, free tier): smaller/faster GPUs (A10)
- Large requests (long context, paid tier): high-memory GPUs (H100 for 128K context)
- Route based on `estimated_tokens = prompt_tokens × 1.1` and user tier

**Health and failure:**
- GPU worker heartbeat: writes `job:{id}:heartbeat` to Redis (EX 30s)
- Reaper: stalled jobs (no heartbeat for 60s) → re-queue to Kafka
- Failed job: publish `{"done": true, "error": "generation_failed"}` to token stream → client shows error

### 4) How do we keep heavy users from taking over GPU pools while giving paid tiers better experience?

**Token quota rate limiting (fixed-window counter):**

Per user, track tokens consumed in a fixed window:
- Free tier: 100K tokens/day, 10K tokens/hour
- Plus tier: 1M tokens/day, 100K tokens/hour
- Team tier: unlimited

Implementation:
```
Redis:
  INCRBY user:{id}:tokens_hour {tokens_used}  → atomic increment
  EXPIRE user:{id}:tokens_hour 3600 NX  → TTL set only on first write; auto-reset hourly
  If value > limit: HTTP 429 (rate limited)
```

**Priority queue by tier:**

Separate Kafka topics per tier:
```
Kafka("jobs-paid")    → consumed first (high priority workers)
Kafka("jobs-free")    → consumed when paid queue is empty (overflow workers)
```

Worker pools:
- 70% of GPUs: dedicated to paid tier jobs
- 30% of GPUs: flexible, work paid when backlog, switch to free when paid is drained

**Fairness within a tier (weighted fair queuing):**
- Track each user's token consumption in the last hour
- Heavy users are deprioritized within their tier queue
- Light users get promoted ahead of heavy users (even within the same tier)

### 5) As conversations get longer, how do we control inference cost without making the assistant feel forgetful?

**Problem:** LLM inference cost is proportional to `(context_tokens + output_tokens)`. A conversation with 50 turns × 500 tokens = 25K tokens of context. This is expensive and may exceed the model's context window.

**Strategies:**

**A) Context window truncation (simple):**
- Always include the system prompt + last N messages (N = fit within K tokens)
- Oldest messages are dropped
- Simple but loses early conversation context

**B) Summarization (better):**
- When conversation exceeds threshold (e.g., 10K tokens), asynchronously summarize older turns:
  - Call LLM: `"Summarize these messages in 200 words: {old_messages}"`
  - Store summary as a special `summary` message
  - Future prompts include: `[system] + [summary] + [recent 10 messages] + [new message]`
- Preserves key facts while reducing token count significantly

**C) Message importance scoring:**
- Track which messages are "referenced" (similar to later messages via embedding similarity)
- Keep important early messages; drop unimportant ones

**D) Retrieval-augmented conversation (RAG):**
- Embed all past messages as vectors (using embedding model)
- On new user prompt: retrieve top-K most relevant past messages (cosine similarity search)
- Include retrieved messages + recent context in the prompt
- Scales to arbitrarily long conversations
- Higher complexity: requires vector DB (Pinecone, pgvector)

**Best approach for MVP:** Truncation. For premium users: summarization.

#### Cancelling a run and reclaiming the GPU

If user clicks "Stop" mid-generation:
1. Client sends `DELETE /generations/{generation_id}`
2. API Server marks job as `cancelled` in DB
3. GPU Worker checks cancellation flag every 10 tokens: if cancelled → stop generation, publish `{"done": true, "cancelled": true}` to stream, release GPU

---

## Final Design

```
Client
  │ POST /messages (new prompt)
  ▼
Chat API Server
  ├─ Persist user message → PostgreSQL
  ├─ Load conversation history → PostgreSQL
  ├─ Build prompt (context assembly)
  ├─ Rate limit check → Redis (token quota counter)
  └─ Enqueue → Kafka("jobs-paid" or "jobs-free")
                      ↓
                GPU Workers (12K pods, one job at a time)
                  ├─ Load model (pre-loaded in memory)
                  ├─ Run inference
                  ├─ Publish tokens → Redis Stream (gen:{id}:tokens)
                  └─ On completion: persist assistant message → PostgreSQL

Client → GET /stream/{generation_id} (SSE)
  ↓
Streaming Gateway (stateless)
  ├─ XREAD Redis Stream (gen:{id}:tokens)
  └─ Push tokens to client via SSE (supports reconnect via Last-Event-ID)

PostgreSQL
  - conversations, messages (source of truth)
  - Sharded by user_id

Redis
  - Token streams (TTL 1 hour)
  - Rate limiting buckets
  - Job heartbeats

Kafka
  - jobs-paid, jobs-free (separated for tier priority)
```

---

## What is Expected at Each Level?

### Mid-level
- Correct entity design (conversations, messages)
- SSE for token streaming
- Context loading (last N messages)
- Basic GPU worker pool via job queue

### Senior
- Durable Redis Stream for reconnect support
- Kafka-based job dispatch with consumer groups
- Priority queue by tier (paid vs. free)
- Context window management (truncation)

### Staff+
- Conversation summarization for long context control
- Weighted fair queuing within a tier
- GPU type routing (A10 vs. H100 by context size)
- Stalled job reaper + heartbeat
- RAG for unlimited conversation memory
- Rolling deploy with stateless Streaming Gateway
