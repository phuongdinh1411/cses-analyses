---
layout: simple
title: "Design Splitwise"
permalink: /low_level_design/splitwise
---

# Design Splitwise

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/splitwise.md)

---

## Requirements

1. Create accounts, manage profiles
2. Create groups, add users
3. Add expenses with amount, description, participants
4. Auto-split expenses by share
5. View balances, settle up
6. Different split methods: equal, percentage, exact
7. View transaction history
8. Handle concurrent transactions

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/splitwise-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **User** | Id, name, email, balance map with other users |
| **Group** | Member list, expense list |
| **Expense** | Id, amount, description, paying user, splits list |
| **Split** | Abstract class; EqualSplit, PercentSplit, ExactSplit subclasses |
| **EqualSplit** | Splits expense equally among all participants |
| **PercentSplit** | Splits expense by percentage for each participant |
| **ExactSplit** | Splits expense by exact amounts for each participant |
| **Transaction** | Id, sender, receiver, amount |
| **SplitwiseService** | Singleton; ConcurrentHashMap + CopyOnWriteArrayList |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | SplitwiseService provides centralized management of users, groups, and expenses |
| **Inheritance/Polymorphism** | Split hierarchy allows flexible expense splitting strategies (equal, percentage, exact) through a common abstract interface |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/splitwise) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/splitwise) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/splitwise) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/splitwise) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/splitwise) |
