---
layout: simple
title: "Real-Time Transport Pattern — System Design School"
permalink: /system_design/sds/concepts/patterns-realtime
---

System Design School

- Learn

- Practice

- Primer

- Roadmap

- Pricing

Ask AI TutorStart learning

System Design Primer12

★The TemplateIntroductionWhat Is System Design?What Are System Design Interviews?Level Expectations

Show all 12 →

Design Solutions35

LeetCode (Online Judge)Typeahead / AutocompleteDistributed Rate LimiterTicketmasterNews Feed

Show all 35 →

AI System Design6

RAG SystemChatGPTImage Generation ServiceCoding Agent CLI (Claude Code)

Show all 6 →

Patterns5

The 10 PatternsScaling Reads & WritesAsynchronous JobsReal-Time TransportHandling Large Files

Key Technologies5

Networking EssentialsTechnology ChoicesRedisTries & Prefix Search

Show all 5 →

# Real-Time Transport: Long-Polling, SSE, and WebSockets

mediumReal-timeWebSocketsPub/sub

Real-time features invert the normal flow of the web. Chat messages, live comments, presence indicators, and collaborative cursors all need the server to send data the client never asked for, the moment it arrives. Standard request-response cannot do that: the client asks, the server answers, and the connection closes.

Polling is the naive workaround. The client re-asks every few seconds and diffs the result. It wastes requests that usually return nothing, and it still trails one interval behind. The alternatives keep a connection open so the server can push instead.

## The core need: server-initiated messages

The problem is direction. HTTP is client-initiated. Real-time features need the server to send data when it has news, not when the client happens to ask. Three transports solve this. They differ in two things: how much of the connection stays open, and in which direction data flows. The comparison below shows that shape at a glance; each transport's mechanism is then drawn as a sequence in its own section.

### Long-polling

The client sends a request. The server holds it open instead of replying right away. When data arrives, the server responds. The client reads it, then immediately sends the next request. It is pull that imitates push.

Long-polling works everywhere, because it is ordinary HTTP. No special protocol, no upgrade step, no proxy trouble. The cost is overhead: every update pays for a full request and response, with headers each time. Between updates the connection cycles open and closed. For low-frequency updates this is fine. For a busy chat it wastes work.

### Server-Sent Events (SSE)

The client opens one HTTP connection and keeps it open. The server streams events down it as they occur. The browser's EventSource API handles reconnection automatically if the stream drops.

SSE is one-directional: server to client only. That fits feeds well: notifications, live scores, a comment stream, a progress bar. It cannot carry client-to-server messages on the same channel, so a chat still needs a normal request to send. SSE is simpler than WebSockets and rides plain HTTP.

### WebSockets

A WebSocket starts as an HTTP request that asks to upgrade the connection. Once the server agrees, the same TCP connection becomes a persistent, two-way channel. Either side can send a message at any time.

Full-duplex. Both directions are open at once. A phone call is full-duplex; a walkie-talkie is half-duplex. WebSockets are full-duplex, which is why they suit chat, collaborative editing, and multiplayer games where both sides speak.

WebSockets carry the least overhead per message once connected. The trade is complexity: it is a distinct protocol, some older proxies mishandle it, and — as the next section shows — a persistent connection changes how the whole backend is shaped.

Choosing among the three comes down to direction and per-message overhead.

TransportDirectionOverheadReach for it when

Long-pollingClient asks, server repliesHigh — a full request per updateUpdates are rare and it must work everywhere

SSEServer to client onlyLow — one open streamOne-way feeds: notifications, live scores, comment streams

WebSocketFull-duplex, both waysLowest per messageTwo-way and chatty: chat, collaborative editing, games

Design checkpoint

You pick WebSockets so the server can push. A user is connected to one of 50 gateway servers. Another user sends them a message, but that message lands on a different gateway. What is the missing piece?

A bigger load balancerA connection registry plus pub/sub to route to the right gatewaySticky sessions pinned by client IP

## The real problem: stateful connections

Every transport above leaves you holding an open connection. That single fact reshapes the backend. Normal HTTP is stateless: any server can handle any request, so a load balancer sprays traffic across a fleet and nothing remembers anything. A persistent connection is the opposite. It pins one client to one server for its whole lifetime.

Now picture delivery. User A is connected to gateway 3. User B, connected to gateway 17, sends A a message. Gateway 17 holds the message but not A's connection. It cannot reach A directly. Two pieces close this gap.

The first is a connection registry: a fast lookup of which gateway currently holds each user's connection. When a client connects, its gateway records user -> gateway in a shared store. When it disconnects, the entry is removed.

The second is an internal pub/sub backplane: a message bus every gateway subscribes to. To deliver a message, the receiving gateway looks up the target user, then publishes the message to the gateway that holds them. That gateway pushes it down the open connection.

This is why "just use WebSockets" is a half-answer. The transport is one line. The connection registry and the routing backplane are the design.

## Scaling the connection layer

Connections, not requests, are the unit of load here. A single server holds tens of thousands of open sockets, each consuming memory and a file descriptor even when idle. You scale out by adding gateway servers, and each new gateway subscribes to the same pub/sub backplane. The registry keeps the mapping current as clients connect and drop.

Two pressures show up at scale. Reconnection storms come first: when a gateway restarts, every client on it reconnects at once, and they all hit the registry and re-subscribe together. Spreading reconnects with jittered backoff smooths the spike. Backpressure comes second.

Backpressure. A slow or stalled client cannot drain messages as fast as the server sends them. The server's send buffer grows and memory climbs. Under backpressure the server must slow down, drop, or disconnect the laggard, rather than buffer without limit.

Fan-out volume is the other watch item. Broadcasting one event to a million connected clients is a million socket writes, spread across every gateway that holds a subscriber. That load is real and belongs in the estimate, not the transport choice.

## What a strong answer sounds like

How do you push live updates to connected clients?

BadPoll on a timer▾

GoodPick the right transport▾

GreatTransport plus registry plus backplane▾

## The transferable pattern

Any feature where the server must reach the client first follows the same shape. Choose a transport that keeps a channel open in the direction you need. Accept that the open connection makes each server stateful, pinning clients to servers. Then add the two pieces that make a stateful fleet routable: a registry that tracks where each client lives, and a message bus that carries events to the server holding the target. Chat, live comments, presence, collaborative editing, and multiplayer all reduce to this.

The Chat App system design applies this structure to WebSocket gateways, ordered message storage, offline sync, group delivery, and presence across a large fleet.

Fan-out to many recipients — a post reaching every follower — is a related but separate problem, worked out in full in News Feed. Real-time transport delivers the message once you know where it must go; fan-out decides who receives it.

Key idea. The transport is the easy half. The connection registry and pub/sub backplane that route messages across a stateful fleet are what the design is really about.

## Sources and further reading

- Using server-sent events — MDN — the EventSource API and automatic reconnection behavior.

- The WebSocket Protocol — RFC 6455 — the HTTP upgrade handshake and full-duplex framing.

- WebSockets vs Server-Sent Events — Ably — a side-by-side comparison of the trade-offs covered here.

Explain

Add to Chat

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

Was this lesson clear?

👍👎

### How to Solve Any System Design Interview

#### Comments

Join the Discussion

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

On this page

The core need: server-initiated messagesLong-pollingServer-Sent Events (SSE)WebSocketsThe real problem: stateful connectionsScaling the connection layerWhat a strong answer sounds likeThe transferable patternSources and further reading

Read0%

Need help?Ask about this section

On this pageThe core need: server-initiated messages0%

Send feedback
