---
layout: simple
title: "Design Stack Overflow"
permalink: /low_level_design/stack-overflow
---

# Design Stack Overflow

**Difficulty**: Easy | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/stack-overflow.md)

---

## Requirements

1. Post questions, answer questions, comment on both
2. Vote on questions and answers
3. Questions have tags
4. Search by keywords, tags, or user profiles
5. Track reputation scores
6. Handle concurrent access

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/stackoverflow-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **User** | id, username, email, reputation |
| **Question** | id, title, content, author, answers, comments, tags, votes, creation date |
| **Answer** | id, content, author, question, comments, votes, creation date |
| **Comment** | id, content, author, creation date |
| **Tag** | id, name |
| **Vote** | Associated with question or answer |
| **StackOverflow** | Main class: user creation, posting, voting, searching |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | StackOverflow main class ensures a single system instance |
| **Composite/Hierarchy** | Questions contain answers which contain comments, forming a tree |
| **Observer-like** | Reputation updates triggered by votes on questions/answers |
| **Facade** | StackOverflow class provides a simplified interface to the subsystems |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/stackoverflow) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/stackoverflow) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/stackoverflow) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/stackoverflow) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/stack_overflow) |
