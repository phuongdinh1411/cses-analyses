---
layout: simple
title: "Design an Elevator System"
permalink: /low_level_design/elevator-system
---

# Design an Elevator System

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/elevator-system.md)

---

## Requirements

1. Multiple elevators, multiple floors
2. Capacity limit per elevator
3. Request from any floor, select destination
4. Optimize movement, minimize wait time
5. Prioritize by direction and proximity
6. Handle multiple concurrent requests
7. Thread safety

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/elevatorsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Direction** | Enum: UP, DOWN |
| **Request** | source floor, destination floor |
| **Elevator** | capacity, request list; processes requests concurrently |
| **ElevatorController** | Manages elevators; finds optimal elevator by proximity and direction |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Controller** | ElevatorController centralizes request dispatching and elevator selection logic |
| **Concurrency Management** | Each elevator processes its queue concurrently with thread-safe request handling |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/elevatorsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/elevatorsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/elevatorsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/elevatorsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/elevator_system) |
