---
layout: simple
title: "Design Hotel Management System"
permalink: /low_level_design/hotel-management-system
---

# Design Hotel Management System

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/hotel-management-system.md)

---

## Requirements

1. Book rooms, check-in, check-out
2. Room types: single, double, deluxe, suite
3. Room availability and reservation status
4. Manage guest info, room assignments, billing
5. Multiple payment methods
6. Concurrent bookings
7. Reporting and analytics
8. Scalable

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/hotelmanagementsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Guest** | id, name, email, phone |
| **Room** | id, type, price, status; book/check-in/check-out methods |
| **RoomType** | Enum: single, double, deluxe, suite |
| **RoomStatus** | Enum: available, booked, occupied |
| **Reservation** | id, guest, room, dates, status |
| **ReservationStatus** | Enum: confirmed, cancelled |
| **Payment** | Interface defining payment contract |
| **CashPayment** | Concrete payment implementation for cash |
| **CreditCardPayment** | Concrete payment implementation for credit cards |
| **HotelManagementSystem** | Singleton; synchronized methods for thread-safe booking management |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | HotelManagementSystem has a single instance managing the entire hotel |
| **Strategy** | Payment interface allows swapping payment methods (cash, credit card) at runtime |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/hotelmanagementsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/hotelmanagementsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/hotelmanagementsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/hotelmanagementsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/hotel_management_system) |
