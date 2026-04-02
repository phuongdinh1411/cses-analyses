---
layout: simple
title: "Design Online Food Delivery Service like Swiggy"
permalink: /low_level_design/food-delivery-service
---

# Design Online Food Delivery Service like Swiggy

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/food-delivery-service.md)

---

## Requirements

1. Browse restaurants, view menus, place orders
2. Restaurants manage menus, prices, availability
3. Delivery agents accept and fulfill orders
4. Order tracking and status updates
5. Multiple payment methods
6. Concurrent orders
7. Scalable
8. Real-time notifications

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/fooddeliveryservice-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Customer** | Id, name, email, phone |
| **Restaurant** | Id, name, address, menu items list |
| **MenuItem** | Id, name, description, price, availability |
| **Order** | Id, customer, restaurant, items, status, delivery agent |
| **OrderItem** | Menu item, quantity |
| **OrderStatus** | Enum: PENDING, CONFIRMED, PREPARING, OUT_FOR_DELIVERY, DELIVERED, CANCELLED |
| **DeliveryAgent** | Id, name, phone, availability |
| **FoodDeliveryService** | Singleton |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | FoodDeliveryService provides centralized coordination for restaurants, orders, delivery agents, and customers |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/fooddeliveryservice) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/fooddeliveryservice) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/fooddeliveryservice) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/fooddeliveryservice) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/food_delivery_service) |
