---
layout: simple
title: "Design a Library Management System"
permalink: /low_level_design/library-management-system
---

# Design a Library Management System

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/library-management-system.md)

---

## Requirements

1. Manage books, members, borrowing activities
2. Add, update, remove books from catalog
3. Book details: title, author, ISBN, year, availability
4. Members borrow and return books
5. Member details: name, id, contact, borrowing history
6. Enforce borrowing rules (max books, duration)
7. Handle concurrent access
8. Extensible

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/librarymanagementsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Book** | ISBN, title, author, year, availability |
| **Member** | Id, name, contact, borrowed books list |
| **LibraryManager** | Singleton; ConcurrentHashMap; add/remove books, register members, borrow/return, search |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | LibraryManager ensures a single centralized catalog and member registry |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/librarymanagementsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/librarymanagementsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/librarymanagementsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/librarymanagementsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/library_management_system) |
