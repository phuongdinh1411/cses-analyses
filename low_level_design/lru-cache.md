---
layout: simple
title: "Design LRU Cache"
permalink: /low_level_design/lru-cache
---

# Design LRU Cache

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/lru-cache.md)

---

## Requirements

1. put(key, value) -- insert key-value pair; evict least recently used entry at capacity
2. get(key) -- retrieve value and promote to most recently used; return -1 if absent
3. Fixed capacity set at initialization
4. Thread-safe concurrent access
5. O(1) time complexity for both get and put operations

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/lrucache-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Node** | Doubly linked list node: key, value, prev, next pointers |
| **LRUCache** | HashMap + doubly linked list with sentinel head/tail nodes; synchronized get/put for thread safety |

Helper methods within LRUCache:
- **addToHead** -- insert node right after the head sentinel
- **removeNode** -- detach a node from the list
- **moveToHead** -- remove then re-insert at head (mark as most recently used)
- **removeTail** -- evict the least recently used node (before tail sentinel)

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **HashMap + Doubly Linked List** | HashMap provides O(1) lookup; doubly linked list maintains access order for O(1) eviction |
| **Sentinel Nodes** | Dummy head and tail nodes simplify edge-case handling for insertions and deletions |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/lrucache) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/lrucache) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/lrucache) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/lrucache) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/lru_cache) |
