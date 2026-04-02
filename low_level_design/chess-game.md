---
layout: simple
title: "Design Chess Game"
permalink: /low_level_design/chess-game
---

# Design Chess Game

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/chess-game.md)

---

## Requirements

1. Standard chess rules
2. Two players with own pieces
3. 8x8 grid, alternating colors
4. 16 pieces per player (king, queen, 2 rooks, 2 bishops, 2 knights, 8 pawns)
5. Validate legal moves, prevent illegal ones
6. Detect checkmate and stalemate
7. Handle player turns
8. User interface

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/chessgame-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Piece** | Abstract class; color, row, column; abstract canMove method |
| **King** | Subclass of Piece; moves one square in any direction |
| **Queen** | Subclass of Piece; moves any number of squares along rank, file, or diagonal |
| **Rook** | Subclass of Piece; moves any number of squares along rank or file |
| **Bishop** | Subclass of Piece; moves any number of squares diagonally |
| **Knight** | Subclass of Piece; moves in an L-shape (2+1 squares) |
| **Pawn** | Subclass of Piece; moves forward one square (or two from starting position), captures diagonally |
| **Board** | 8x8 grid; piece placement, move validation, checkmate/stalemate detection |
| **Player** | Name; make move method |
| **Move** | Piece, destination coordinates |
| **Game** | Game flow, turns, result |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Strategy/Polymorphism** | Each piece type implements its own movement logic via the abstract canMove method, allowing uniform move validation |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/chessgame) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/chessgame) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/chessgame) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/chessgame) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/chess_game) |
