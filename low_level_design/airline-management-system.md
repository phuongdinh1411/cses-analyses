---
layout: simple
title: "Design Airline Management System"
permalink: /low_level_design/airline-management-system
---

# Design Airline Management System

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/airline-management-system.md)

---

## Requirements

1. Search flights by source, destination, date
2. Book flights, select seats, make payments
3. Manage flight schedules, aircraft/crew assignments
4. Handle passenger info and baggage
5. Support passengers, airline staff, administrators
6. Handle cancellations, refunds, flight changes
7. Data consistency, concurrent access
8. Scalable and extensible

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/airlinemanagementsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Flight** | Flight number, source, destination, departure/arrival times, available seats |
| **Aircraft** | Tail number, model, total seats |
| **Passenger** | Id, name, email, phone |
| **Booking** | Booking number, passenger, flight, seat, price, status |
| **Seat** | Seat number, type, status |
| **Payment** | Id, method, amount, status |
| **FlightSearch** | Search by source, destination, date |
| **BookingManager** | Singleton; creation/cancellation |
| **PaymentProcessor** | Singleton; payment processing |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | BookingManager and PaymentProcessor ensure a single point of coordination for bookings and payments |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/airlinemanagementsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/airlinemanagementsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/airlinemanagementsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/airlinemanagementsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/airline_management_system) |
