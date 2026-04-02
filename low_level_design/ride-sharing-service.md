---
layout: simple
title: "Design Ride-Sharing Service like Uber"
permalink: /low_level_design/ride-sharing-service
---

# Design Ride-Sharing Service like Uber

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/ride-sharing-service.md)

---

## Requirements

1. Passengers request rides, drivers accept/fulfill
2. Specify pickup, destination, ride type (regular, premium)
3. Drivers view and accept/decline requests
4. Match by proximity
5. Fare calculation (distance, time, type)
6. Handle payments
7. Real-time tracking
8. Concurrent requests

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/ridesharingservice-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Passenger** | Id, name, contact, location |
| **Driver** | Id, name, contact, plate, location, status (available/busy) |
| **Ride** | Id, passenger, driver, source, destination, status, fare |
| **Location** | Latitude, longitude |
| **Payment** | Id, ride, amount, status |
| **RideService** | Singleton; ConcurrentHashMap + ConcurrentLinkedQueue |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | RideService acts as the central coordinator for ride matching, fare calculation, and payment processing |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/ridesharingservice) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/ridesharingservice) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/ridesharingservice) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/ridesharingservice) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/ride_sharing_service) |
