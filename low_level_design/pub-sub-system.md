---
layout: simple
title: "Design Pub Sub System"
permalink: /low_level_design/pub-sub-system
---

# Design Pub Sub System

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/pub-sub-system.md)

---

## Requirements

1. Publishers publish messages to specific topics
2. Subscribers subscribe to topics and receive messages
3. Multiple publishers and subscribers
4. Real-time message delivery
5. Handle concurrent access, thread safety
6. Scalable and efficient

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/pubsubsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Message** | content |
| **Topic** | set of subscribers; methods to add/remove subscribers and broadcast messages |
| **Subscriber** | Interface with onMessage method |
| **PrintSubscriber** | Concrete subscriber; prints received messages to console |
| **Publisher** | Sends messages to a topic |
| **PubSubSystem** | Central manager; ConcurrentHashMap + ExecutorService for async delivery |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Observer** | Topics notify all registered subscribers when a new message is published |
| **Interface-based Abstraction** | Subscriber interface allows any class to receive messages by implementing onMessage |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/pubsubsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/pubsubsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/pubsubsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/pubsubsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/pub_sub_system) |
