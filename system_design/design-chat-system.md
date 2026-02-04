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
9. [Implementation](#implementation)
10. [Key Takeaways](#key-takeaways)

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

### Protocol Comparison

| Protocol | Pros | Cons | Use Case |
|----------|------|------|----------|
| **HTTP Polling** | Simple | High latency, wasteful | Legacy systems |
| **Long Polling** | Near real-time | Connection overhead | Fallback |
| **WebSocket** | True real-time, bidirectional | Stateful | Primary choice |
| **Server-Sent Events** | Simple server push | Unidirectional | Notifications |

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

### 1. Message Delivery Flow (1:1 Chat)

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

### 3. Online Presence System

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

### 4. Message Sync for Multiple Devices

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

### Delivery Guarantees

| Guarantee | Implementation |
|-----------|----------------|
| **At-least-once** | Retry with idempotency key |
| **Ordering** | Sequential message IDs per chat |
| **No duplicates** | client_msg_id deduplication |

### Retry Strategy

```python
def send_with_retry(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = send_message(message)
            return result
        except TemporaryError:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)

    # Store in dead letter queue
    dlq.push(message)
    notify_offline(message.receiver_id, message)
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

## Implementation

### WebSocket Server (Node.js)

```javascript
const WebSocket = require('ws');
const Redis = require('ioredis');

class ChatWebSocketServer {
    constructor(port, redisConfig) {
        this.wss = new WebSocket.Server({ port });
        this.redis = new Redis(redisConfig);
        this.pubsub = new Redis(redisConfig);
        this.connections = new Map(); // userId -> WebSocket

        this.setupServer();
        this.setupPubSub();
    }

    setupServer() {
        this.wss.on('connection', async (ws, req) => {
            const userId = await this.authenticate(req);
            if (!userId) {
                ws.close(4001, 'Unauthorized');
                return;
            }

            this.connections.set(userId, ws);
            await this.registerSession(userId);
            await this.publishPresence(userId, 'online');

            ws.on('message', (data) => this.handleMessage(userId, data));
            ws.on('close', () => this.handleDisconnect(userId));
            ws.on('pong', () => this.handleHeartbeat(userId));

            // Start heartbeat
            ws.isAlive = true;
            this.startHeartbeat(ws, userId);
        });
    }

    setupPubSub() {
        // Subscribe to user-specific channels
        this.pubsub.psubscribe('chat:*', (err) => {
            if (err) console.error('Subscribe error:', err);
        });

        this.pubsub.on('pmessage', (pattern, channel, message) => {
            const userId = channel.split(':')[1];
            const ws = this.connections.get(userId);
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(message);
            }
        });
    }

    async handleMessage(userId, data) {
        const message = JSON.parse(data);

        switch (message.type) {
            case 'message':
                await this.routeMessage(userId, message.data);
                break;
            case 'typing':
                await this.broadcastTyping(userId, message.chatId);
                break;
            case 'ack':
                await this.handleAck(userId, message.messageId);
                break;
            case 'read':
                await this.handleReadReceipt(userId, message.chatId,
                                            message.messageId);
                break;
        }
    }

    async routeMessage(senderId, messageData) {
        const { receiverId, content, clientMsgId, chatId } = messageData;

        // Deduplication check
        const exists = await this.redis.get(`msg:${clientMsgId}`);
        if (exists) return;

        // Generate server message ID
        const messageId = generateTimeUUID();
        const timestamp = Date.now();

        // Store message
        await this.storeMessage({
            chatId,
            messageId,
            senderId,
            content,
            timestamp
        });

        // Mark as processed
        await this.redis.setex(`msg:${clientMsgId}`, 3600, messageId);

        // Send ACK to sender
        this.sendToUser(senderId, {
            type: 'ack',
            clientMsgId,
            messageId,
            status: 'sent'
        });

        // Route to receiver
        await this.deliverMessage(receiverId, {
            type: 'message',
            messageId,
            senderId,
            chatId,
            content,
            timestamp
        });
    }

    async deliverMessage(receiverId, message) {
        // Check if user is connected to this server
        const ws = this.connections.get(receiverId);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(message));
            return;
        }

        // Check if user is on another server
        const session = await this.redis.hgetall(`session:${receiverId}`);
        if (session && session.serverId) {
            // Publish to user's channel
            await this.redis.publish(
                `chat:${receiverId}`,
                JSON.stringify(message)
            );
        } else {
            // User is offline - push notification
            await this.sendPushNotification(receiverId, message);
        }
    }

    async registerSession(userId) {
        await this.redis.hset(`session:${userId}`, {
            serverId: process.env.SERVER_ID,
            connectedAt: Date.now()
        });
        await this.redis.expire(`session:${userId}`, 120);
    }

    startHeartbeat(ws, userId) {
        const interval = setInterval(() => {
            if (!ws.isAlive) {
                clearInterval(interval);
                return ws.terminate();
            }
            ws.isAlive = false;
            ws.ping();
        }, 30000);
    }

    async handleHeartbeat(userId) {
        await this.redis.expire(`session:${userId}`, 120);
        await this.redis.expire(`presence:${userId}`, 120);
    }

    async handleDisconnect(userId) {
        this.connections.delete(userId);
        await this.redis.del(`session:${userId}`);

        // Delay presence update (user might reconnect)
        setTimeout(async () => {
            const session = await this.redis.exists(`session:${userId}`);
            if (!session) {
                await this.publishPresence(userId, 'offline');
            }
        }, 5000);
    }
}
```

### Chat Service (Go)

```go
package chat

import (
    "context"
    "encoding/json"
    "time"

    "github.com/gocql/gocql"
    "github.com/redis/go-redis/v9"
    "github.com/segmentio/kafka-go"
)

type ChatService struct {
    cassandra *gocql.Session
    redis     *redis.Client
    kafka     *kafka.Writer
}

type Message struct {
    ChatID    gocql.UUID `json:"chat_id"`
    MessageID gocql.UUID `json:"message_id"`
    SenderID  int64      `json:"sender_id"`
    Content   string     `json:"content"`
    MsgType   string     `json:"msg_type"`
    MediaURL  string     `json:"media_url,omitempty"`
    CreatedAt time.Time  `json:"created_at"`
}

func (s *ChatService) SendMessage(ctx context.Context,
    msg *Message) error {

    // Generate time-based UUID for ordering
    msg.MessageID = gocql.TimeUUID()
    msg.CreatedAt = time.Now()

    // Store in Cassandra
    err := s.cassandra.Query(`
        INSERT INTO messages
        (chat_id, message_id, sender_id, content,
         msg_type, media_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `, msg.ChatID, msg.MessageID, msg.SenderID,
       msg.Content, msg.MsgType, msg.MediaURL,
       msg.CreatedAt).Exec()

    if err != nil {
        return err
    }

    // Update chat's last message
    err = s.updateChatLastMessage(ctx, msg)
    if err != nil {
        // Log but don't fail
        log.Printf("Failed to update last message: %v", err)
    }

    // Publish to Kafka for delivery
    msgBytes, _ := json.Marshal(msg)
    err = s.kafka.WriteMessages(ctx, kafka.Message{
        Topic: "chat-messages",
        Key:   []byte(msg.ChatID.String()),
        Value: msgBytes,
    })

    return err
}

func (s *ChatService) GetMessages(ctx context.Context,
    chatID gocql.UUID, before time.Time,
    limit int) ([]Message, error) {

    var messages []Message

    iter := s.cassandra.Query(`
        SELECT chat_id, message_id, sender_id, content,
               msg_type, media_url, created_at
        FROM messages
        WHERE chat_id = ? AND message_id < ?
        ORDER BY message_id DESC
        LIMIT ?
    `, chatID, gocql.UUIDFromTime(before), limit).Iter()

    var msg Message
    for iter.Scan(&msg.ChatID, &msg.MessageID, &msg.SenderID,
        &msg.Content, &msg.MsgType, &msg.MediaURL,
        &msg.CreatedAt) {
        messages = append(messages, msg)
    }

    return messages, iter.Close()
}

func (s *ChatService) SendGroupMessage(ctx context.Context,
    groupID int64, msg *Message) error {

    msg.MessageID = gocql.TimeUUID()
    msg.CreatedAt = time.Now()

    // Store message
    err := s.cassandra.Query(`
        INSERT INTO messages
        (chat_id, message_id, sender_id, content,
         msg_type, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    `, msg.ChatID, msg.MessageID, msg.SenderID,
       msg.Content, msg.MsgType, msg.CreatedAt).Exec()

    if err != nil {
        return err
    }

    // Get group members
    members, err := s.getGroupMembers(ctx, groupID)
    if err != nil {
        return err
    }

    // Fan-out to members via Kafka
    for _, memberID := range members {
        if memberID == msg.SenderID {
            continue // Don't send to self
        }

        delivery := map[string]interface{}{
            "user_id": memberID,
            "message": msg,
        }
        deliveryBytes, _ := json.Marshal(delivery)

        s.kafka.WriteMessages(ctx, kafka.Message{
            Topic: "message-delivery",
            Key:   []byte(fmt.Sprintf("%d", memberID)),
            Value: deliveryBytes,
        })
    }

    return nil
}

func (s *ChatService) MarkAsRead(ctx context.Context,
    userID int64, chatID gocql.UUID,
    messageID gocql.UUID) error {

    // Update read position
    err := s.cassandra.Query(`
        UPDATE user_chats
        SET last_read_at = ?, unread_count = 0
        WHERE user_id = ? AND chat_id = ?
    `, time.Now(), userID, chatID).Exec()

    if err != nil {
        return err
    }

    // Notify sender about read receipt
    msg, err := s.getMessage(ctx, chatID, messageID)
    if err != nil {
        return err
    }

    receipt := map[string]interface{}{
        "type":       "read_receipt",
        "chat_id":    chatID,
        "message_id": messageID,
        "reader_id":  userID,
        "read_at":    time.Now(),
    }
    receiptBytes, _ := json.Marshal(receipt)

    return s.kafka.WriteMessages(ctx, kafka.Message{
        Topic: "message-delivery",
        Key:   []byte(fmt.Sprintf("%d", msg.SenderID)),
        Value: receiptBytes,
    })
}
```

### Presence Service (Python)

```python
import asyncio
import json
from datetime import datetime, timedelta
from typing import Set, Dict
import aioredis

class PresenceService:
    def __init__(self, redis_url: str):
        self.redis = None
        self.redis_url = redis_url
        self.PRESENCE_TTL = 120  # seconds
        self.HEARTBEAT_INTERVAL = 30

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)
        self.pubsub = self.redis.pubsub()

    async def set_online(self, user_id: str, server_id: str):
        pipeline = self.redis.pipeline()

        # Set presence
        pipeline.setex(
            f"presence:{user_id}",
            self.PRESENCE_TTL,
            "online"
        )

        # Set session info
        pipeline.hset(f"session:{user_id}", mapping={
            "server_id": server_id,
            "connected_at": datetime.utcnow().isoformat()
        })
        pipeline.expire(f"session:{user_id}", self.PRESENCE_TTL)

        await pipeline.execute()

        # Notify friends
        await self.notify_presence_change(user_id, "online")

    async def set_offline(self, user_id: str):
        # Small delay to handle reconnections
        await asyncio.sleep(5)

        # Check if user reconnected
        exists = await self.redis.exists(f"session:{user_id}")
        if exists:
            return

        await self.redis.delete(f"presence:{user_id}")
        await self.notify_presence_change(user_id, "offline")

    async def heartbeat(self, user_id: str):
        pipeline = self.redis.pipeline()
        pipeline.expire(f"presence:{user_id}", self.PRESENCE_TTL)
        pipeline.expire(f"session:{user_id}", self.PRESENCE_TTL)
        await pipeline.execute()

    async def get_presence(self, user_id: str) -> str:
        presence = await self.redis.get(f"presence:{user_id}")
        return presence.decode() if presence else "offline"

    async def get_bulk_presence(self, user_ids: list) -> Dict[str, str]:
        pipeline = self.redis.pipeline()
        for user_id in user_ids:
            pipeline.get(f"presence:{user_id}")

        results = await pipeline.execute()

        return {
            user_id: (r.decode() if r else "offline")
            for user_id, r in zip(user_ids, results)
        }

    async def notify_presence_change(self, user_id: str, status: str):
        # Get user's friends who are online
        friends = await self.get_online_friends(user_id)

        message = json.dumps({
            "type": "presence",
            "user_id": user_id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Publish to each friend's channel
        for friend_id in friends:
            await self.redis.publish(f"chat:{friend_id}", message)

    async def get_online_friends(self, user_id: str) -> Set[str]:
        # Get friend list (from cache or DB)
        friends = await self.get_friends(user_id)

        # Check which friends are online
        presences = await self.get_bulk_presence(friends)

        return {
            friend_id
            for friend_id, status in presences.items()
            if status == "online"
        }

    async def subscribe_to_presence(self, user_id: str,
                                    friend_ids: list):
        """Subscribe to presence updates for friends"""
        channels = [f"presence:{fid}" for fid in friend_ids]
        await self.pubsub.subscribe(*channels)
```

---

## Key Takeaways

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Protocol | WebSocket | Real-time, bidirectional |
| Message storage | Cassandra | High write throughput, time-series |
| Session storage | Redis | Fast lookups, pub/sub |
| Message queue | Kafka | Reliable delivery, ordering |

### Scalability Patterns

1. **Horizontal scaling**: Shard by chat_id/user_id
2. **Connection distribution**: Consistent hashing for WebSocket servers
3. **Message fanout**: Async via Kafka for groups
4. **Presence**: Redis pub/sub with TTL

### Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| Single WebSocket server | Simple | Limited scale |
| Server cluster + Redis | Scalable | Added latency |
| Connection pinning | Fast delivery | Uneven load |

### Common Interview Questions

1. How do you handle millions of concurrent connections?
2. How do you ensure message ordering?
3. How do you handle message delivery to offline users?
4. How do you implement read receipts at scale?
5. How do you design group chat for large groups?

### Related Topics

- [Design News Feed](/cses-analyses/system_design/design-news-feed) - Similar fanout patterns
- [Design Key-Value Store](/cses-analyses/system_design/design-key-value-store) - Session storage
- [Consistent Hashing](/cses-analyses/system_design/consistent-hashing) - Connection distribution
