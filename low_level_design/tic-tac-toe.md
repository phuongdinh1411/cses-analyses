---
layout: simple
title: "Design Tic Tac Toe Game"
permalink: /low_level_design/tic-tac-toe
---

# Design Tic Tac Toe Game

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/tic-tac-toe.md)

---

## Requirements

1. 3x3 grid
2. Two players alternate placing X and O
3. Three in a row (horizontal, vertical, or diagonal) wins
4. All cells filled with no winner is a draw
5. Display grid and accept moves
6. Handle turns and validate moves
7. Detect winner or draw

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/tictactoe-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Player** | name, symbol (X or O) |
| **Board** | 3x3 grid; methods to make moves, check winner, check if full |
| **Game** | Game flow, turn handling, move validation, outcome detection |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **OO Decomposition** | Clear separation of Player, Board, and Game responsibilities |
| **MVC-like Separation** | Board manages state, Game controls logic, display is separated from data |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/tictactoe) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/tictactoe) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/tictactoe) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/tictactoe) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/tic_tac_toe) |
