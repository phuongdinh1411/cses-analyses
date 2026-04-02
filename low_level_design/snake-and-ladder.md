---
layout: simple
title: "Design a Snake and Ladder Game"
permalink: /low_level_design/snake-and-ladder
---

# Design a Snake and Ladder Game

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/snake-and-ladder.md)

---

## Requirements

1. Board with 100 numbered cells
2. Predefined snakes and ladders
3. Multiple players with unique pieces
4. Roll dice to move forward
5. Snake head -- slide to tail
6. Ladder base -- climb to top
7. First to final cell wins
8. Support concurrent game sessions

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/snakeandladdergame-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Board** | Size (100), snake/ladder positions; determine new position after move |
| **Player** | Name, current position |
| **Snake** | Start (head), end (tail) |
| **Ladder** | Start (base), end (top) |
| **Dice** | Roll returns random value 1-6 |
| **SnakeAndLadderGame** | Board, players, dice; game loop logic |
| **GameManager** | Singleton; manages multiple game sessions in separate threads |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | GameManager provides a single coordination point for managing multiple concurrent game sessions |
| **Concurrency via Threading** | Each game session runs in its own thread, allowing multiple games simultaneously |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/snakeandladdergame) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/snakeandladdergame) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/snakeandladdergame) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/snakeandladdergame) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/snake_and_ladder) |
