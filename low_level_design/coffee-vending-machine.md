---
layout: simple
title: "Design Coffee Vending Machine"
permalink: /low_level_design/coffee-vending-machine
---

# Design Coffee Vending Machine

**Difficulty**: Easy | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/coffee-vending-machine.md)

---

## Requirements

1. Support espresso, cappuccino, latte
2. Each type has price and recipe
3. Display menu with prices
4. Choose coffee and submit payment
5. Dispense coffee and return change
6. Track ingredient inventory
7. Handle concurrent requests

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/coffeevendingmachine-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Coffee** | name, price, recipe (ingredient-to-quantity map) |
| **Ingredient** | name, quantity; synchronized update method |
| **Payment** | amount paid |
| **CoffeeMachine** | Singleton; menu, ingredients, dispensing |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | CoffeeMachine has a single instance managing all operations |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/coffeevendingmachine) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/coffeevendingmachine) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/coffeevendingmachine) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/coffeevendingmachine) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/coffee_vending_machine) |
