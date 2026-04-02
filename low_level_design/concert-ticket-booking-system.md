---
layout: simple
title: "Design a Concert Ticket Booking System"
permalink: /low_level_design/concert-ticket-booking-system
---

# Design a Concert Ticket Booking System

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/concert-ticket-booking-system.md)

---

## Requirements

1. View available concerts and seating
2. Search by artist, venue, date, time
3. Select seats and purchase tickets
4. Handle concurrent booking (no double-booking)
5. Fair booking opportunities
6. Secure payment processing
7. Booking confirmations via email/SMS
8. Waiting list for sold-out concerts

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/concertticketbookingsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Concert** | Id, artist, venue, date/time, seats list |
| **Seat** | Id, number, type, price, status |
| **SeatType** | Enum: regular, premium, VIP |
| **SeatStatus** | Enum: available, booked, reserved |
| **Booking** | Id, user, concert, seats, total price, status |
| **BookingStatus** | Enum: pending, confirmed, cancelled |
| **User** | Id, name, email |
| **ConcertTicketBookingSystem** | Singleton |
| **SeatNotAvailableException** | Custom exception |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | ConcertTicketBookingSystem ensures centralized booking coordination and prevents double-booking |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/concertbookingsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/concertbookingsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/concertbookingsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/concertbookingsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/concert_booking_system) |
