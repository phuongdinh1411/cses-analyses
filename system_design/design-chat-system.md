---
layout: simple
title: "Design a Chat System"
permalink: /system_design/design-chat-system
---

# Design a Chat System

A chat system enables real-time messaging between users. Examples include WhatsApp, Facebook Messenger, Slack, and Discord.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Back of the Envelope Estimation](#back-of-the-envelope-estimation)
3. [System APIs](#system-apis)
4. [High-Level Design](#high-level-design)
5. [Communication Protocols](#communication-protocols)
6. [Database Design](#database-design)
7. [Deep Dive](#deep-dive)
8. [Message Delivery](#message-delivery)
9. [Key Takeaways](#key-takeaways)
10. [Interview Tips](#interview-tips)

---

## Requirements

### Functional Requirements

- **1:1 chat**: Send and receive messages between two users
- **Group chat**: Support group conversations (up to 500 members)
- **Online presence**: Show online/offline status
- **Message history**: Persist and retrieve chat history
- **Media sharing**: Support images, videos, and files

### Non-Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Low latency** | Messages delivered in < 100ms |
| **High availability** | 99.99% uptime |
| **Scalability** | Support 500 million DAU |
| **Reliability** | No message loss, ordered delivery |

### Extended Requirements

- Push notifications for offline users
- End-to-end encryption
- Read receipts and typing indicators
- Message reactions and replies

---

## Back of the Envelope Estimation

### Traffic Estimates

```
Daily Active Users (DAU): 500 million
Avg messages per user per day: 40
Total messages: 500M × 40 = 20 billion/day
                = ~230,000 messages/second

Peak traffic: 3× average = 700,000 messages/second
```

### Storage Estimates

```
Avg message size: 100 bytes (text)
Messages per day: 20 billion
Message storage per day: 20B × 100 bytes = 2 TB

Per year: 2 TB × 365 = 730 TB (text only)
Media storage: ~10× text = 7.3 PB/year
```

### Connection Estimates

```
Concurrent connections: 10% of DAU = 50 million
WebSocket connections per server: 50,000
Servers needed: 50M / 50K = 1,000 servers
```

### Summary

| Metric | Value |
|--------|-------|
| Messages/second | 230,000 (avg), 700,000 (peak) |
| Storage (text) | 730 TB/year |
| Concurrent connections | 50 million |
| WebSocket servers | 1,000+ |

---

## System APIs

### Send Message

```
POST /v1/messages
```

**Request:**
```json
{
  "sender_id": "user123",
  "receiver_id": "user456",
  "message_type": "text",
  "content": "Hello!",
  "client_msg_id": "uuid-123"
}
```

**Response:**
```json
{
  "message_id": "msg789",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "sent"
}
```

### Send Group Message

```
POST /v1/groups/{group_id}/messages
```

**Request:**
```json
{
  "sender_id": "user123",
  "message_type": "text",
  "content": "Hello everyone!",
  "client_msg_id": "uuid-456"
}
```

### Get Messages

```
GET /v1/messages?user_id={user_id}&chat_id={chat_id}&before={timestamp}&limit={limit}
```

**Response:**
```json
{
  "messages": [
    {
      "message_id": "msg789",
      "sender_id": "user456",
      "content": "Hi there!",
      "timestamp": "2024-01-15T10:29:00Z",
      "status": "read"
    }
  ],
  "has_more": true
}
```

### WebSocket Events

```javascript
// Client → Server
{ "type": "message", "data": {...} }
{ "type": "typing", "chat_id": "chat123" }
{ "type": "ack", "message_id": "msg789" }

// Server → Client
{ "type": "message", "data": {...} }
{ "type": "typing", "user_id": "user456", "chat_id": "chat123" }
{ "type": "presence", "user_id": "user456", "status": "online" }
```

---

## High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                         Load Balancer                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   WebSocket   │    │   API Server  │    │  Presence     │
│   Server      │    │   (REST)      │    │  Service      │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                    ┌───────────────┐
                    │ Message Queue │
                    │   (Kafka)     │
                    └───────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Chat        │   │  Message DB   │   │  User/Session │
│   Service     │   │  (Cassandra)  │   │  Cache (Redis)│
└───────────────┘   └───────────────┘   └───────────────┘
```

### Components

| Component | Responsibility |
|-----------|----------------|
| **WebSocket Server** | Maintain persistent connections, real-time messaging |
| **API Server** | REST APIs for message history, user management |
| **Chat Service** | Message routing, delivery logic |
| **Presence Service** | Track user online/offline status |
| **Message Queue** | Decouple message producers and consumers |
| **Push Notification** | Notify offline users |

---

## Communication Protocols

> **Interview context**: After the high-level design, the interviewer will ask: "How do clients receive messages in real-time? What protocol would you use?"

### The Challenge

HTTP is request-response: the client must ask for data. But in a chat system, the server needs to **push** messages to clients instantly. How do we achieve this?

### Protocol Options

| Protocol | How It Works | Pros | Cons |
|----------|--------------|------|------|
| **HTTP Polling** | Client polls server every N seconds | Simple | High latency, wasteful |
| **Long Polling** | Server holds request until data available | Near real-time | Connection overhead |
| **WebSocket** | Persistent bidirectional connection | True real-time | Stateful, complex |
| **Server-Sent Events** | Server pushes over HTTP | Simple server push | Unidirectional only |

### Why WebSocket?

> **Interviewer might ask**: "Why not just use long polling? It's simpler."

**Long polling limitations**:
- Each message requires a new HTTP request
- Headers overhead on every request (~800 bytes)
- Server must track pending requests
- Harder to implement server → client push efficiently

**WebSocket advantages**:
- Single persistent connection (established once)
- True bidirectional: server can push anytime
- Low overhead after handshake (~2-6 bytes per frame)
- Native browser support

**When to use long polling**: As a fallback when WebSocket is blocked (corporate firewalls, old proxies).

### WebSocket Architecture

```
┌──────────┐         ┌─────────────────┐         ┌──────────┐
│  User A  │◄───────►│  WebSocket      │◄───────►│  User B  │
│ (Client) │   WS    │  Server Cluster │   WS    │ (Client) │
└──────────┘         └────────┬────────┘         └──────────┘
                              │
                              ▼
                     ┌────────────────┐
                     │ Service        │
                     │ Discovery      │
                     │ (user→server)  │
                     └────────────────┘
```

### Connection Flow

```
1. Client connects to Load Balancer
2. LB routes to WebSocket server
3. Server authenticates user (JWT/session)
4. Register connection in Service Discovery
5. Subscribe to user's message channels

┌────────┐                              ┌────────────┐
│ Client │                              │ WS Server  │
└───┬────┘                              └─────┬──────┘
    │                                         │
    │─────── WebSocket Upgrade ──────────────►│
    │                                         │
    │◄────── 101 Switching Protocols ─────────│
    │                                         │
    │─────── Auth: JWT Token ────────────────►│
    │                                         │
    │◄────── Auth OK, Connected ──────────────│
    │                                         │
    │◄─────────── Messages ──────────────────►│
    │                                         │
```

---

## Database Design

> **Interview context**: "Now let's discuss data storage. What database would you use for messages?"

### The Challenge

Chat messages have specific access patterns:
- **Write-heavy**: 230K messages/second
- **Time-ordered**: Messages retrieved in chronological order
- **Per-conversation**: Always query by chat_id, then time
- **High volume**: 730TB/year of text alone

### Why Cassandra for Messages?

> **Interviewer might ask**: "Why not MySQL or PostgreSQL?"

| Requirement | Cassandra | Traditional SQL |
|-------------|-----------|-----------------|
| Write throughput | Excellent (distributed) | Limited (single master) |
| Horizontal scaling | Built-in | Complex sharding |
| Time-series queries | Optimized | Requires careful indexing |
| Availability | AP (highly available) | CP (consistency focus) |

**Key insight**: Messages are append-only and queried by (chat_id, time). This is exactly what Cassandra excels at.

### Message Table (Cassandra)

```sql
CREATE TABLE messages (
    chat_id     UUID,
    message_id  TIMEUUID,
    sender_id   BIGINT,
    content     TEXT,
    msg_type    TEXT,      -- text, image, video, file
    media_url   TEXT,
    created_at  TIMESTAMP,
    PRIMARY KEY (chat_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

### Chat Table (Cassandra)

```sql
CREATE TABLE chats (
    chat_id       UUID PRIMARY KEY,
    chat_type     TEXT,      -- direct, group
    participants  SET<BIGINT>,
    created_at    TIMESTAMP,
    last_message  TEXT,
    last_msg_time TIMESTAMP
);

-- User's chat list
CREATE TABLE user_chats (
    user_id       BIGINT,
    chat_id       UUID,
    unread_count  INT,
    last_read_at  TIMESTAMP,
    PRIMARY KEY (user_id, chat_id)
);
```

### Group Table (PostgreSQL)

```sql
CREATE TABLE groups (
    group_id    BIGINT PRIMARY KEY,
    name        VARCHAR(100),
    avatar_url  TEXT,
    owner_id    BIGINT,
    created_at  TIMESTAMP,
    member_count INT DEFAULT 0
);

CREATE TABLE group_members (
    group_id    BIGINT,
    user_id     BIGINT,
    role        VARCHAR(20), -- admin, member
    joined_at   TIMESTAMP,
    PRIMARY KEY (group_id, user_id)
);

CREATE INDEX idx_user_groups ON group_members(user_id);
```

### Session Table (Redis)

```
# User's WebSocket server location
Key: session:{user_id}
Value: {
    "server_id": "ws-server-42",
    "connected_at": 1705312200,
    "device": "mobile"
}
TTL: Refreshed on heartbeat

# Online status
Key: presence:{user_id}
Value: "online" | "away" | "offline"
TTL: 5 minutes (refreshed by heartbeat)
```

---

## Deep Dive

> **Interview context**: "Let's dive deeper into some interesting challenges..."

### 1. Message Delivery Flow (1:1 Chat)

> **Interviewer might ask**: "Walk me through what happens when User A sends a message to User B."

```
┌──────────┐                                           ┌──────────┐
│  User A  │                                           │  User B  │
└────┬─────┘                                           └────┬─────┘
     │                                                      │
     │──── Send Message ────►┌─────────────┐                │
     │                       │ WS Server 1 │                │
     │                       └──────┬──────┘                │
     │                              │                       │
     │                              ▼                       │
     │                       ┌─────────────┐                │
     │                       │ Chat Service│                │
     │                       └──────┬──────┘                │
     │                              │                       │
     │              ┌───────────────┼───────────────┐       │
     │              │               │               │       │
     │              ▼               ▼               ▼       │
     │       ┌──────────┐   ┌──────────┐   ┌──────────┐    │
     │       │ Save to  │   │ Find B's │   │ Send ACK │    │
     │       │ Cassandra│   │ WS Server│   │ to A     │    │
     │       └──────────┘   └────┬─────┘   └────┬─────┘    │
     │                           │              │          │
     │◄────── ACK (sent) ────────┼──────────────┘          │
     │                           │                         │
     │                           ▼                         │
     │                    ┌─────────────┐                  │
     │                    │ WS Server 2 │──── Message ────►│
     │                    └─────────────┘                  │
     │                                                     │
     │                           ◄────── ACK (delivered) ──│
     │                                                     │
```

### 2. Message Delivery Flow (Group Chat)

> **Interviewer might ask**: "Group chat with 500 members is different from 1:1. How do you handle it?"

**The challenge**: One message → 500 deliveries. This is a **fan-out** problem.

```
┌──────────┐
│  User A  │
│  (sends) │
└────┬─────┘
     │
     ▼
┌─────────────┐
│ WS Server   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Chat Service │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         Message Queue (Kafka)       │
│  Topic: group-messages-{group_id}   │
└─────────────────┬───────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌───────┐   ┌───────┐    ┌───────┐
│User B │   │User C │    │User D │
│(WS 2) │   │(WS 3) │    │(offline)
└───────┘   └───────┘    └───────┘
                              │
                              ▼
                         ┌───────────┐
                         │Push Notif │
                         └───────────┘
```

**Why use Kafka for fan-out?**
- Decouples sender from delivery
- Handles backpressure (slow consumers don't block sender)
- Reliable delivery with retries
- Partitioning by user_id for ordered delivery

### 3. Online Presence System

> **Interviewer might ask**: "How do you show who's online? This seems simple but gets complex at scale."

**The challenge**:
- 50 million concurrent users
- Each user has hundreds of friends
- Status changes must propagate quickly
- But we can't broadcast every change to everyone

```
┌─────────────────────────────────────────────────────────┐
│                   Presence Architecture                  │
└─────────────────────────────────────────────────────────┘

User connects:
┌────────┐    ┌─────────┐    ┌─────────┐    ┌─────────────┐
│ Client │───►│ WS      │───►│ Presence│───►│ Redis       │
│        │    │ Server  │    │ Service │    │ PUBLISH     │
└────────┘    └─────────┘    └─────────┘    │ presence:   │
                                            │ user123=on  │
                                            └──────┬──────┘
                                                   │
              ┌────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│         Subscribed clients receive update               │
│                                                         │
│  User A's friends → "User A is now online"              │
└─────────────────────────────────────────────────────────┘

Heartbeat mechanism:
┌────────┐  Heartbeat    ┌─────────┐
│ Client │──(every 30s)─►│ Server  │
└────────┘               └────┬────┘
                              │
                              ▼
                        ┌──────────┐
                        │  Redis   │
                        │ EXPIRE   │
                        │ 60s      │
                        └──────────┘

If heartbeat stops → TTL expires → User marked offline
```

**Why heartbeat + TTL?**
- Handles ungraceful disconnects (network drop, app crash)
- No need to detect disconnection explicitly
- Redis handles cleanup automatically via TTL

### 4. Message Sync for Multiple Devices

> **Interviewer might ask**: "Users have phones, tablets, and laptops. How do you sync messages across devices?"

```
User has multiple devices (phone, tablet, laptop):

┌─────────┐  ┌─────────┐  ┌─────────┐
│ Phone   │  │ Tablet  │  │ Laptop  │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┼────────────┘
                  │
                  ▼
           ┌─────────────┐
           │ WS Servers  │
           │ (different) │
           └──────┬──────┘
                  │
                  ▼
           ┌─────────────┐
           │ User has    │
           │ 3 sessions  │
           │ in Redis    │
           └──────┬──────┘
                  │
                  ▼
    Message delivery to ALL sessions

Sync strategy:
1. Each device maintains last_sync_timestamp
2. On reconnect: fetch messages since last_sync
3. Conflict resolution: server timestamp wins
```

### 5. Message Status Tracking

```
Message states:
┌──────┐    ┌──────┐    ┌───────────┐    ┌──────┐
│ Sent │───►│Stored│───►│ Delivered │───►│ Read │
└──────┘    └──────┘    └───────────┘    └──────┘

Storage:
┌────────────────────────────────────────────────┐
│  message_status table                          │
│  ─────────────────────────────────────         │
│  message_id | user_id | status | timestamp     │
│  msg123     | user456 | delivered | 10:30:01   │
│  msg123     | user456 | read      | 10:30:05   │
└────────────────────────────────────────────────┘

Read receipt flow:
User B reads message →
  Client sends ACK →
    Update status →
      Notify User A via WebSocket
```

---

## Message Delivery

> **Interview context**: "Let's discuss delivery guarantees. This is where things get interesting."

### The Challenge: Delivery Guarantees

> **Interviewer might ask**: "How do you ensure messages are delivered reliably?"

| Guarantee | Challenge | Solution |
|-----------|-----------|----------|
| **At-least-once** | Network failures | Retry with exponential backoff |
| **Ordering** | Concurrent messages | Sequential IDs per chat (TimeUUID) |
| **No duplicates** | Retries cause duplicates | client_msg_id deduplication |

### Why Not Exactly-Once?

> **Interviewer might ask**: "Can you guarantee exactly-once delivery?"

**The hard truth**: Exactly-once delivery is impossible in distributed systems without significant complexity. Instead:

1. **At-least-once delivery** (guaranteed)
2. **Idempotent processing** (client_msg_id dedup)
3. **Result**: Effectively exactly-once from user's perspective

### Retry Strategy

```
Retry with exponential backoff + jitter:
  Attempt 1: immediate
  Attempt 2: 1s + random(0-1s)
  Attempt 3: 2s + random(0-1s)
  Attempt 4: 4s + random(0-1s)
  After max retries: Dead letter queue + push notification
```

### Offline Message Handling

```
┌──────────────────────────────────────────────────────┐
│                Offline User Flow                      │
└──────────────────────────────────────────────────────┘

1. User B is offline
2. Message arrives for B
3. Check Redis: B has no active session
4. Store message in Cassandra (normal flow)
5. Send push notification via FCM/APNs
6. When B comes online:
   - Connect to WebSocket
   - Fetch unread messages since last_sync
   - Receive new real-time messages

┌─────────┐
│ User A  │── Send ──►┌────────────┐
└─────────┘           │ WS Server  │
                      └─────┬──────┘
                            │
                            ▼
                      ┌────────────┐
                      │ B offline? │──YES──►┌────────────┐
                      └─────┬──────┘        │ Push Notif │
                           NO               │ Service    │
                            │               └────────────┘
                            ▼
                      ┌────────────┐
                      │ Deliver to │
                      │ B's WS     │
                      └────────────┘
```

---

## Key Takeaways

### Design Decisions Summary

| Decision | Choice | Why |
|----------|--------|-----|
| **Protocol** | WebSocket | True real-time, bidirectional, low overhead |
| **Message storage** | Cassandra | High write throughput, time-series optimized |
| **Session storage** | Redis | Fast lookups, pub/sub for cross-server messaging |
| **Message queue** | Kafka | Reliable fan-out, ordering guarantees |
| **Presence** | Redis + TTL | Simple, automatic cleanup on disconnect |

### Trade-offs to Discuss

| Decision | Option A | Option B |
|----------|----------|----------|
| Protocol | WebSocket (stateful) | Long polling (stateless) |
| Delivery | At-least-once + dedup | Exactly-once (complex) |
| Group fanout | Sync (simple) | Async via Kafka (scalable) |
| Presence | Push updates | Pull on demand |

### Scalability Phases

```
Phase 1: Small scale (~10K concurrent)
└── Single WS server + Redis + PostgreSQL

Phase 2: Medium scale (~1M concurrent)
└── WS cluster + Redis pub/sub + Cassandra

Phase 3: Large scale (~50M concurrent)
└── Multiple DCs + Kafka + sharded everything
```

---

## Interview Tips

### How to Approach (45 minutes)

```
1. CLARIFY (3-5 min)
   "1:1 only or groups? How large? Need presence? Read receipts?"

2. HIGH-LEVEL DESIGN (5-7 min)
   Draw: Clients → LB → WS Servers → Message Queue → Database

3. DEEP DIVE (25-30 min)
   - Protocol choice (WebSocket vs alternatives)
   - Message routing (how to find recipient's server)
   - Group chat fan-out strategy
   - Presence system design
   - Offline message handling

4. WRAP UP (5 min)
   - Discuss E2E encryption, push notifications
   - Mention monitoring, rate limiting
```

### Key Phrases That Show Depth

| Instead of... | Say... |
|---------------|--------|
| "We use WebSocket" | "HTTP is request-response, so we need WebSocket for server-initiated push. It's bidirectional and has low per-message overhead after the initial handshake." |
| "Store in Cassandra" | "Messages are append-only and queried by (chat_id, time) - perfect for Cassandra's time-series model with chat_id as partition key." |
| "Use Redis for presence" | "Redis with TTL handles presence elegantly - heartbeat refreshes TTL, and if heartbeat stops, TTL expires and user is automatically offline." |

### Common Follow-up Questions

| Question | Key Points |
|----------|------------|
| "How handle 50M connections?" | Horizontal scaling, ~50K connections/server, 1000+ servers |
| "How ensure ordering?" | TimeUUID per chat, Kafka partition by chat_id |
| "How handle offline users?" | Store message, send push notification, sync on reconnect |
| "How scale group chat?" | Async fan-out via Kafka, not blocking sender |
| "How implement E2E encryption?" | Signal protocol, keys exchanged out-of-band, server can't read |

### Related Topics

- [Design News Feed](/cses-analyses/system_design/design-news-feed) - Similar fanout patterns
- [Design Key-Value Store](/cses-analyses/system_design/design-key-value-store) - Session storage
- [Consistent Hashing](/cses-analyses/system_design/consistent-hashing) - Connection distribution
