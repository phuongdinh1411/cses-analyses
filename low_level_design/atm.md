---
layout: simple
title: "Design ATM"
permalink: /low_level_design/atm
---

# Design ATM

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/atm.md)

---

## Requirements

1. Balance inquiry, cash withdrawal, cash deposit
2. Authenticate with card and PIN
3. Interact with bank backend
4. Cash dispenser for distributing cash
5. Handle concurrent access
6. User-friendly interface

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/atm-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Card** | card number, PIN |
| **Account** | account number, balance; debit/credit methods |
| **Transaction** | Abstract base; subclassed by WithdrawalTransaction and DepositTransaction |
| **BankingService** | Manages accounts; ConcurrentHashMap for thread-safe access |
| **CashDispenser** | Synchronized cash dispensing |
| **ATM** | Coordinates BankingService and CashDispenser |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Template Method** | Abstract Transaction class defines the algorithm skeleton; subclasses implement specific steps |
| **Facade** | ATM class provides a simplified interface to BankingService and CashDispenser subsystems |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/atm) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/atm) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/atm) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/atm) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/atm) |
