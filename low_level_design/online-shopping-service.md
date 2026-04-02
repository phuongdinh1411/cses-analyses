---
layout: simple
title: "Design Online Shopping System like Amazon"
permalink: /low_level_design/online-shopping-service
---

# Design Online Shopping System like Amazon

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-shopping-service.md)

---

## Requirements

1. Browse products, add to cart, place orders
2. Multiple product categories with search
3. Manage profiles, view order history, track status
4. Inventory management
5. Multiple payment methods
6. Concurrent access
7. Scalable
8. User-friendly

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/onlineshoppingservice-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **User** | Id, name, email, password, orders list |
| **Product** | Id, name, description, price, quantity; update quantity, check availability |
| **Order** | Id, user, order items, total, status |
| **OrderItem** | Product, quantity |
| **OrderStatus** | Enum: pending, processing, shipped, delivered, cancelled |
| **ShoppingCart** | Add, remove, update items; map of product IDs to order items |
| **Payment** | Interface; CreditCardPayment implementation |
| **OnlineShoppingService** | Singleton; synchronized |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | OnlineShoppingService provides centralized management of users, products, and orders with synchronized access |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/onlineshoppingservice) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/onlineshoppingservice) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/onlineshoppingservice) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/onlineshoppingservice) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/online_shopping_service) |
