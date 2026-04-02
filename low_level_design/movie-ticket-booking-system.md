---
layout: simple
title: "Design Movie Ticket Booking System"
permalink: /low_level_design/movie-ticket-booking-system
---

# Design Movie Ticket Booking System

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/movie-ticket-booking-system.md)

---

## Requirements

1. View movies in different theaters
2. Select movie, theater, showtime
3. Display seating, choose seats
4. Make payment and confirm
5. Handle concurrent bookings, real-time seat updates
6. Different seat types and pricing
7. Admin management of movies/shows
8. Scalable

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/movieticketbookingsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Movie** | Id, title, description, duration |
| **Theater** | Id, name, location, shows list |
| **Show** | Id, movie, theater, start/end time, seat map |
| **Seat** | Id, row, column, type, price, status |
| **SeatType** | Enum: normal, premium |
| **SeatStatus** | Enum: available, booked |
| **Booking** | Id, user, show, seats, total price, status |
| **BookingStatus** | Enum: pending, confirmed, cancelled |
| **User** | Id, name, email |
| **MovieTicketBookingSystem** | Singleton; ConcurrentHashMap |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | MovieTicketBookingSystem ensures centralized booking coordination and prevents double-booking of seats |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/movieticketbookingsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/movieticketbookingsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/movieticketbookingsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/movieticketbookingsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/movie_ticket_booking_system) |
