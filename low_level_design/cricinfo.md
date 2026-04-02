---
layout: simple
title: "Design CricInfo"
permalink: /low_level_design/cricinfo
---

# Design CricInfo

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/cricinfo.md)

---

## Requirements

1. Cricket match, team, player, live score info
2. View schedules and results
3. Search matches, teams, players
4. Detailed match info: scorecard, commentary, stats
5. Real-time live score updates
6. Handle concurrent access
7. Scalable for large volume
8. Extensible

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/cricinfo-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Match** | Id, title, venue, start time, teams, status, scorecard |
| **Team** | Id, name, player list |
| **Player** | Id, name, role |
| **Scorecard** | Team scores, list of innings |
| **Innings** | Id, batting/bowling team, list of overs |
| **Over** | List of balls |
| **Ball** | Ball number, bowler, batsman, result |
| **MatchStatus** | Enum: scheduled, in progress, completed, abandoned |
| **MatchService** | Singleton |
| **ScorecardService** | Singleton |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | MatchService manages all match data centrally; ScorecardService handles scorecard updates as a single coordination point |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/cricinfo) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/cricinfo) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/cricinfo) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/cricinfo) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/cricinfo) |
