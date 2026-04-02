---
layout: simple
title: "Design Car Rental System"
permalink: /low_level_design/car-rental-system
---

# Design Car Rental System

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/car-rental-system.md)

---

## Requirements

1. Browse and reserve cars for specific dates
2. Car details: make, model, year, plate, price per day
3. Search by type, price range, availability
4. Create, modify, cancel reservations
5. Track availability
6. Customer data management
7. Payment processing
8. Concurrent reservations

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/carrentalsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Car** | make, model, year, plate, price per day, availability |
| **Customer** | name, contact, license number |
| **Reservation** | id, customer, car, dates, total price |
| **PaymentProcessor** | Interface; defines payment processing contract |
| **CreditCardPaymentProcessor** | Concrete payment processor for credit cards |
| **PayPalPaymentProcessor** | Concrete payment processor for PayPal |
| **RentalSystem** | Singleton; ConcurrentHashMap for thread-safe car and reservation management |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | RentalSystem has a single instance managing the entire fleet |
| **Strategy** | PaymentProcessor interface allows swapping payment methods at runtime |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/carrentalsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/carrentalsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/carrentalsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/carrentalsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/car_rental_system) |
