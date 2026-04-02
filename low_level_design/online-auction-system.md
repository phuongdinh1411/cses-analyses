---
layout: simple
title: "Design an Online Auction System"
permalink: /low_level_design/online-auction-system
---

# Design an Online Auction System

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-auction-system.md)

---

## Requirements

1. Register and log in
2. Create listings with item name, description, starting price, duration
3. Browse and search listings
4. Place bids on active listings
5. Auto-update highest bid, notify bidders
6. End auction at duration, declare winner
7. Handle concurrent access
8. Extensible

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/onlineauctionsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **User** | id, username, email |
| **AuctionStatus** | Enum: active, closed |
| **AuctionListing** | id, item name, description, starting price, duration, seller, current highest bid, bid list |
| **Bid** | id, bidder, amount, timestamp |
| **AuctionSystem** | Singleton; ConcurrentHashMap + CopyOnWriteArrayList for thread-safe management |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | AuctionSystem has a single instance managing all listings and bids |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/onlineauctionsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/onlineauctionsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/onlineauctionsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/onlineauctionsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/online_auction_system) |
