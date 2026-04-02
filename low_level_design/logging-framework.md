---
layout: simple
title: "Design Logging Framework"
permalink: /low_level_design/logging-framework
---

# Design Logging Framework

**Difficulty**: Easy | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/logging-framework.md)

---

## Requirements

1. Log levels: DEBUG, INFO, WARNING, ERROR, FATAL
2. Messages include timestamp, level, content
3. Multiple output destinations: console, file, database
4. Configurable log level and output
5. Thread-safe concurrent logging
6. Extensible for new levels and destinations

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/loggingframework-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **LogLevel** | Enum for log levels: DEBUG, INFO, WARNING, ERROR, FATAL |
| **LogMessage** | timestamp, level, message content |
| **LogAppender** | Interface for output destinations |
| **ConsoleAppender** | Concrete appender; writes log messages to console |
| **FileAppender** | Concrete appender; writes log messages to file |
| **DatabaseAppender** | Concrete appender; writes log messages to database |
| **LoggerConfig** | Holds active log level and appender |
| **Logger** | Singleton; core logging functionality |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | Logger has a single instance across the application |
| **Strategy** | LogAppender interface allows swapping output destinations at runtime |
| **Open/Closed Principle** | New appenders can be added without modifying existing code |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/loggingframework) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/loggingframework) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/loggingframework) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/loggingframework) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/logging_framework) |
