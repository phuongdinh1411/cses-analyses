---
layout: simple
title: "Design a Digital Wallet Service"
permalink: /low_level_design/digital-wallet-service
---

# Design a Digital Wallet Service

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/digital-wallet-service.md)

---

## Requirements

1. Create account, manage personal info
2. Add and remove payment methods (credit cards, bank accounts)
3. Fund transfers between users and external accounts
4. Transaction history and statements
5. Multiple currencies, currency conversions
6. Security of user info and transactions
7. Concurrent transactions
8. Scalable

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/digitalwalletservice-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **User** | id, name, email, password, list of accounts |
| **Account** | id, user, account number, currency, balance, transactions; deposit/withdraw methods |
| **Transaction** | id, source account, destination, amount, currency, timestamp |
| **PaymentMethod** | Abstract base class; extended by CreditCard and BankAccount |
| **CreditCard** | Concrete payment method for credit card details |
| **BankAccount** | Concrete payment method for bank account details |
| **Currency** | Enum for supported currencies |
| **CurrencyConverter** | Static conversion method for currency exchange |
| **DigitalWallet** | Singleton; synchronized methods for thread-safe transaction processing |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | DigitalWallet has a single instance managing all users and transactions |
| **Abstract Class/Polymorphism** | PaymentMethod abstract base with CreditCard and BankAccount subclasses |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/digitalwalletservice) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/digitalwalletservice) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/digitalwalletservice) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/digitalwalletservice) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/digital_wallet_service) |
