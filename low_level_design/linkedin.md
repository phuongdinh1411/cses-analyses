---
layout: simple
title: "Design LinkedIn"
permalink: /low_level_design/linkedin
---

# Design LinkedIn

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/linkedin.md)

---

## Requirements

1. User registration and authentication
2. Profiles with picture, headline, summary, experience, education, skills
3. Connection requests (send, accept, decline)
4. Messaging between connections
5. Job postings by employers
6. Search for users, companies, jobs
7. Notifications (real-time)
8. Scalable for large concurrent users

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/linkedin-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **User** | id, name, email, password, profile, connections, messages |
| **Profile** | picture, headline, summary, experiences, educations, skills |
| **Experience** | Profile component for work history |
| **Education** | Profile component for educational background |
| **Skill** | Profile component for skills |
| **Connection** | connected user, date |
| **Message** | id, sender, receiver, content, timestamp |
| **JobPosting** | id, title, description, requirements, location, date |
| **Notification** | id, user, type, content, timestamp |
| **NotificationType** | Enum: connection request, message, job posting |
| **LinkedInService** | Singleton; ConcurrentHashMap + CopyOnWriteArrayList for thread-safe management |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | LinkedInService has a single instance managing the entire platform |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/linkedin) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/linkedin) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/linkedin) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/linkedin) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/linkedin) |
