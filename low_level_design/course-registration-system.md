---
layout: simple
title: "Design Course Registration System"
permalink: /low_level_design/course-registration-system
---

# Design Course Registration System

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/course-registration-system.md)

---

## Requirements

1. Students register for courses, view registered courses
2. Course: code, name, instructor, max capacity
3. Search by code or name
4. Block registration at max capacity
5. Handle concurrent registrations
6. Data consistency, prevent race conditions
7. Extensible

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/courseregistrationsystem-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Student** | Id, name, email, registered courses list |
| **Course** | Code, name, instructor, max capacity, enrolled count |
| **Registration** | Student, course, timestamp |
| **CourseRegistrationSystem** | Singleton; ConcurrentHashMap + CopyOnWriteArrayList; synchronized registerCourse |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | CourseRegistrationSystem ensures a single point of coordination for all registration operations |
| **Observer** | Placeholder for future notification support (e.g., notifying students when a seat opens) |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/courseregistrationsystem) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/courseregistrationsystem) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/courseregistrationsystem) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/courseregistrationsystem) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/course_registration_system) |
