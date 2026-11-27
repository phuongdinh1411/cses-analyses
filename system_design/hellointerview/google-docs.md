---
layout: simple
title: "Design Google Docs — Hello Interview Style"
permalink: /system_design/hellointerview/google-docs
---

# Google Docs

**Patterns:** Real-time Updates  
**Difficulty:** Hard  
**Source:** hellointerview.com (AI-generated full solution)

---

## Summary

- **Key challenge:** Merging concurrent edits without losing changes and propagating them in <500ms, at ~5M ops/sec across 1M concurrently edited documents.
- **Core design:** Clients send insert/delete ops over WebSocket to the one stateful Document Server owning that doc (found via a Redis-backed Document Router); its in-process OT Engine transforms, versions, and broadcasts each op, persisting ops to PostgreSQL and snapshots to S3.
- **Techniques:** Operational Transformation (merge concurrent ops); single Document Server per doc (serialize edits); consistent hashing by doc_id (co-locate collaborators); snapshot every 100 ops + recent op log (fast reload, bounded storage); client pending-ops state machine (responsive local edits).

## Understanding the Problem

📄 **What is Google Docs?**  
Google Docs is a browser-based collaborative document editor where multiple users can edit the same document simultaneously and see each other's changes in real time.

---

### Functional Requirements

**Core Requirements**

- Users should be able to create new documents
- Multiple users should be able to edit the same document concurrently
- Users should be able to view each other's changes in real-time
- Users should be able to see the cursor position and presence of other users

**Below the line (out of scope):**

- Sophisticated rich-text structure (assume plain text editor)
- Permissions and collaboration access control
- Document history and versioning
- Comments and suggestions

### Non-Functional Requirements

**Core Requirements**

- Changes should propagate to all collaborators within **< 500ms**
- The system should scale to **millions of concurrent documents**
- The document state must be **strongly consistent** — no data loss, no corrupted merges
- The system should handle **concurrent edits** without losing changes

**Below the line (out of scope):**

- Offline editing (complex CRDT territory)
- Sub-100ms propagation

### Constraints & Estimates

- 1M concurrent documents being edited
- Average 5 collaborators per active document
- Each editor makes ~1 keystroke/second during active editing → ~5 ops/sec per document
- 1M documents × 5 ops/sec = **5M operations/sec** peak
- Each op: ~100 bytes (small delta)
- Document size: average 50KB, max 1MB

---

## Set Up

### Planning the Approach

The hardest part of Google Docs is **concurrent editing** — two users type at the same time and their changes must be merged correctly. We'll cover:
1. How to represent and transmit edits (operations)
2. How to reconcile concurrent edits (Operational Transformation)
3. How to scale WebSocket connections across a fleet of servers

### Defining the Core Entities

- **Document** – id, title, owner_id, content (text), version (monotonic counter), created_at, updated_at
- **Operation** – doc_id, client_id, type (insert/delete), position, text (for insert) or length (for delete), client_version, server_version
- **DocumentSession** – doc_id, user_id, cursor_position, last_seen_version, connected_at
- **User** – id, name, color (for cursor display)

### Defining the API

```
// Create a document
POST /documents
{ "title": "Meeting Notes" }
-> { doc_id }

// Open a document (REST, returns initial state)
GET /documents/{doc_id}
-> { doc_id, title, content, version }

// Real-time collaboration (WebSocket)
WS /documents/{doc_id}/collaborate?user_id={user_id}

// Messages (client → server):
{ "type": "operation", "op": { "type": "insert", "pos": 5, "text": "hello" }, "client_version": 42 }
{ "type": "cursor", "pos": 7 }
{ "type": "ping" }

// Messages (server → client):
{ "type": "operation", "op": {...}, "server_version": 43, "user_id": "other_user" }
{ "type": "cursor", "user_id": "other_user", "pos": 7, "color": "#FF5733" }
{ "type": "ack", "server_version": 43 }  // confirms our op was applied
```

---

## High-Level Design

### 1) Users should be able to create new documents

Simple CRUD:
1. `POST /documents` → Document Service → INSERT into PostgreSQL
2. Return `doc_id`
3. User is redirected to `/documents/{doc_id}` → loads the editor with initial content

### 2) Multiple users should be able to edit the same document concurrently

**The core challenge: concurrent edit conflict resolution**

Scenario: Document = `"Hello World"`
- User A (at version 10) types "!" at position 11 → operation: `insert(11, "!")`
- User B (at version 10) types " there" at position 5 → operation: `insert(5, " there")`
- Both arrive at the server nearly simultaneously

Naive: apply in arrival order → might garble the document.

**Operational Transformation (OT):**

The key insight: when operation B arrives after operation A has been applied, we must **transform** B to account for A's changes.

```
Server has applied A: "Hello World!" (version 11)
B arrives with client_version=10 (before A)
Transform B against A:
  - A inserted 1 char at position 11
  - B inserts at position 5, which is BEFORE A's position 11
  - B's position doesn't change (insert before A's position)
Transformed B: insert(5, " there") against version 11
Result: "Hello there World!" ✓
```

**Transformation rules for insert/delete:**

```python
def transform_insert_against_insert(op, against):
    # op: insert at pos_op
    # against: insert at pos_against (already applied)
    if op.pos < against.pos:
        return op  # op is before against, no shift needed
    elif op.pos > against.pos:
        return Operation(insert, op.pos + len(against.text), op.text)  # shift right
    else:  # same position: break tie by user_id
        if op.user_id < against.user_id:
            return op
        else:
            return Operation(insert, op.pos + len(against.text), op.text)
```

**Server-side OT algorithm:**
1. Each document has a server-side `operation_log[]` and monotonic `version`
2. When operation op arrives with `client_version = V`:
   - Retrieve all server operations from version V to current
   - Transform op against each of those operations in order
   - Apply transformed op to document
   - Increment version, append to log
   - Broadcast transformed op to all other collaborators

#### Collaborative Edits Breakdown

**Client-side state machine:**

The client maintains:
- `confirmed_state`: document as server has acknowledged it
- `pending_ops[]`: operations sent but not yet confirmed by server
- `uncommitted_ops[]`: operations typed but not yet sent

Before sending an op: transform it against all pending_ops (compose them).

Client receives server op:
1. Transform server op against all pending_ops
2. Apply to `confirmed_state`
3. Update the pending_ops accordingly (transform them against the server op)
4. Reapply pending_ops to get the displayed state

This is the standard **Jupiter OT protocol** used by Google Wave and adapted in Google Docs.

### 3) Users should be able to view each other's changes in real-time

#### When the Document is Loaded

1. Client opens WebSocket to **Collaboration Server**
2. `GET /documents/{id}` returns current content + version
3. Client initializes editor with this state

#### When Updates Happen

1. User types → generates operation (insert/delete at position)
2. Client sends op via WebSocket with `client_version`
3. **Collaboration Server** (holds WebSocket):
   - Forwards op to **OT Engine** (stateful, runs per document)
   - OT Engine transforms + applies → new server_version
   - OT Engine broadcasts transformed op to all other collaborators via WebSocket
   - Sends `ack { server_version }` back to sender
4. All clients receive ops → apply OT transform locally → update display

**Persistence:**
- OT Engine asynchronously persists accepted ops to PostgreSQL
- Periodically writes a document **snapshot** (full content at version N) to avoid replaying ops from the beginning on reconnect

### 4) Users should be able to see the cursor position and presence of other users

**Cursor update flow:**
1. User moves cursor → client sends `{ type: "cursor", pos: 7 }`
2. Collaboration Server broadcasts to all collaborators: `{ type: "cursor", user_id, pos, color }`
3. Clients display colored cursor indicators

**Cursor positions need transformation too** (like operations) when remote operations shift text.

**Presence:**
- On WebSocket connect: broadcast `{ user joined: name, color }`
- On disconnect: broadcast `{ user left: name }`
- Heartbeat (ping/pong) to detect stale connections

---

## Potential Deep Dives

### 1) How do we scale to millions of WebSocket connections?

**Single collaboration server per document:**

For OT to work correctly, all edits on a document must be serialized through **one OT Engine** instance. This is the central coordination point.

**Problem:** 1M concurrent documents, each needing a dedicated OT Engine. Can one server handle 1M document engines?

**Document Server (stateful per document):**

```
Client → Load Balancer → Document Router → Document Server (holds doc state)
```

- **Document Router** maintains a mapping: `doc_id → document_server_address` (stored in Redis)
- When a client opens a document, the router finds (or assigns) a document server for that doc_id
- All collaborators on the same document connect to the **same document server**
- Document server runs the OT Engine in-process (fast, no network hop)

**Scaling document servers:**
- Each document server handles N concurrent documents (e.g., 10K docs)
- For 1M concurrent docs: 1M / 10K = **100 document servers**
- Document servers are stateful but can checkpoint to DB and hand off documents when scaling

**Client connection management:**
- Load balancer routes WebSocket by `doc_id` using consistent hashing
- If a document server crashes: clients reconnect → Router assigns to a new server → new server loads latest snapshot + recent ops from DB → reconstructs state

### 2) How do we keep storage under control?

**Problem:** Storing every individual keystroke operation would generate enormous data:
- 1M docs × 5 ops/sec × 86,400 sec/day = 432 billion ops/day — impractical to store forever

**Snapshot + recent ops strategy:**

1. **Snapshot every N operations** (e.g., N=100):
   - Full document content at version V is stored as a blob in S3/PostgreSQL
   - Only keep the last 100 operations in the ops table
   
2. **Document load reconstruction:**
   - Find latest snapshot at version V_snap
   - Replay ops from V_snap to current V_current
   - If 100 ops max, replay is fast (< 1ms)

3. **Storage tiering:**
   - Hot (last 100 ops): PostgreSQL (fast access, recent edits)
   - Snapshots: S3 (cheap, compressed)
   - Old ops: archive to S3 Glacier after 30 days (rarely needed, only for version history)

**Snapshot creation:**
- Document server creates snapshot after every 100 ops
- Async write to S3
- Update `latest_snapshot_version` in document metadata

**Back-of-envelope:**
- 1M active documents × 50KB avg = 50GB of active document content in memory or Redis
- Snapshot writes: 1M docs × 1 snapshot/100 ops × 5 ops/sec = 50K snapshots/sec → batch write

---

## Final Design

```
Client (Browser)
  │  WebSocket
  ▼
Load Balancer (consistent hash by doc_id)
  ▼
Document Server (100 servers, 10K docs each)
  │  per-document OT Engine (in-process)
  ├─ Apply op → transform → broadcast to collaborators
  ├─ Persist ops to PostgreSQL (async batch)
  ├─ Write snapshots to S3 (every 100 ops)
  └─ Cursor/presence broadcast

Document Router (Redis)
  - doc_id → document_server mapping

PostgreSQL
  - documents (id, title, owner, latest_snapshot_version)
  - operations (doc_id, version, op_data, applied_at)
  - snapshots (doc_id, version, s3_key)

Client page load:
  GET /documents/{id} → REST API
    → Load latest snapshot from S3
    → Load ops since snapshot from PostgreSQL
    → Return { content, version }
```

---

## What is Expected at Each Level?

### Mid-level
- Understands the concurrent edit problem
- Proposes a WebSocket-based real-time update mechanism
- Knows about OT conceptually
- Basic document CRUD and version tracking

### Senior
- Explains OT transformation rules clearly
- Document Server per document for serialized OT
- Snapshot + ops log storage strategy
- Cursor sharing and presence

### Staff
- Full OT client-side state machine (confirmed/pending/uncommitted ops)
- Document Server fault tolerance (checkpoint + replay)
- Scaling to 1M documents (100 document servers, consistent hash routing)
- Storage tiering and snapshot GC policy
- Discusses CRDTs as an alternative to OT (better for offline support)
