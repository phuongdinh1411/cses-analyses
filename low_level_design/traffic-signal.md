---
layout: simple
title: "Design Traffic Signal Control System"
permalink: /low_level_design/traffic-signal
---

# Design Traffic Signal Control System

**Difficulty**: Easy | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/traffic-signal.md)

---

## Requirements

1. Control traffic at intersection with multiple roads
2. Signal types: red, yellow, green
3. Configurable signal durations
4. Smooth transitions between signals
5. Detect and handle emergency situations
6. Scalable and extensible

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/trafficcontrolsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Signal** | Enum for red, yellow, green |
| **Road** | id, name, associated traffic light |
| **TrafficLight** | id, current signal, durations; methods for changing signals |
| **TrafficController** | Singleton; manages roads and traffic lights |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | TrafficController has a single instance managing all intersections |
| **Observer** | Traffic lights notify the controller of state changes; emergency overrides |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/trafficsignal) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/trafficsignal) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/trafficsignal) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/trafficsignal) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/traffic_signal) |
