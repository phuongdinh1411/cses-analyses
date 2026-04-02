---
layout: simple
title: "Design Online Stock Brokerage System"
permalink: /low_level_design/online-stock-brokerage-system
---

# Design Online Stock Brokerage System

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-stock-brokerage-system.md)

---

## Requirements

1. Create/manage trading accounts
2. Buy/sell stocks, view portfolio and history
3. Real-time stock quotes
4. Order placement, execution, settlement
5. Business rules: check balances, stock availability
6. Concurrent access
7. Scalable
8. Secure

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/onlinestockbrokeragesystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **User** | User id, name, email |
| **Account** | Account id, user, balance; deposit/withdraw |
| **Stock** | Symbol, name, price; update price |
| **Order** | Abstract class; order id, account, stock, quantity, price, status; abstract execute() |
| **BuyOrder** | Concrete subclass of Order; executes buy logic |
| **SellOrder** | Concrete subclass of Order; executes sell logic |
| **OrderStatus** | Enum: PENDING, EXECUTED, REJECTED |
| **Portfolio** | Stocks owned; add/remove stocks |
| **StockBroker** | Singleton; manages accounts, stocks, order processing |
| **InsufficientFundsException** | Custom exception for insufficient account balance |
| **InsufficientStockException** | Custom exception for insufficient stock holdings |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | StockBroker provides centralized management of accounts, stocks, and order processing |
| **Abstract Class/Polymorphism** | Order is abstract with BuyOrder and SellOrder subclasses, each implementing their own execute() logic |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/onlinestockbrokeragesystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/onlinestockbrokeragesystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/onlinestockbrokeragesystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/onlinestockbrokeragesystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/online_stock_brokerage_system) |
