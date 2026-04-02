---
layout: simple
title: "Design a Social Network like Facebook"
permalink: /low_level_design/social-networking-service
---

# Design a Social Network like Facebook

**Difficulty**: Medium | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/social-networking-service.md)

---

## Requirements

1. User registration/authentication
2. User profiles with picture, bio, interests
3. Friend requests (send, accept, decline)
4. Posts with text, images, videos
5. Newsfeed in reverse chronological order
6. Likes and comments on posts
7. Privacy controls
8. Notifications (real-time)
9. Scalable

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/socialnetworkingservice-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **User** | Id, name, email, password, profile picture, bio, friends, posts |
| **Post** | Id, user id, content, images, videos, timestamp, likes, comments |
| **Comment** | Id, user id, post id, content, timestamp |
| **Notification** | Id, user id, type, content, timestamp |
| **NotificationType** | Enum: friend request, accepted, like, comment, mention |
| **SocialNetworkingService** | Singleton; ConcurrentHashMap + CopyOnWriteArrayList |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | SocialNetworkingService provides a single point of access for user management, posts, and notifications |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/socialnetworkingservice) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/socialnetworkingservice) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/socialnetworkingservice) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/socialnetworkingservice) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/social_networking_service) |
