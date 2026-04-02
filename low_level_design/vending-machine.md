---
layout: simple
title: "Design a Vending Machine"
permalink: /low_level_design/vending-machine
---

# Design a Vending Machine

**Difficulty**: Easy | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/vending-machine.md)

---

## Requirements

1. Multiple products with different prices and quantities
2. Accept coins and notes of different denominations
3. Dispense product and return change
4. Track available products and quantities
5. Handle multiple transactions concurrently
6. Interface for restocking and collecting money
7. Handle insufficient funds or out-of-stock

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/vendingmachine-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Product** | name, price |
| **Coin** | Enum for coin denominations |
| **Note** | Enum for note denominations |
| **Inventory** | Manages products/quantities; uses concurrent hash map |
| **VendingMachineState** | Interface for different states (idle, ready, dispense) |
| **IdleState** | Implements state interface; waiting for user interaction |
| **ReadyState** | Implements state interface; product selected, awaiting payment |
| **DispenseState** | Implements state interface; dispensing product and returning change |
| **VendingMachine** | Singleton; manages state, product, payment |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **State** | VendingMachine transitions between IdleState, ReadyState, and DispenseState |
| **Singleton** | VendingMachine has a single instance |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/vendingmachine) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/vendingmachine) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/vendingmachine) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/vendingmachine) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/vending_machine) |
