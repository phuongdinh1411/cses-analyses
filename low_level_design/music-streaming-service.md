---
layout: simple
title: "Design Music Streaming Service like Spotify"
permalink: /low_level_design/music-streaming-service
---

# Design Music Streaming Service like Spotify

**Difficulty**: Hard | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/music-streaming-service.md)

---

## Requirements

1. Browse/search songs, albums, artists
2. Create/manage playlists
3. User authentication/authorization
4. Play, pause, skip, seek within songs
5. Recommendations based on preferences/history
6. Handle concurrent requests
7. Scalable
8. Extensible (social sharing, offline playback)

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/musicstreamingservice-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **Song** | Core music entity with title, artist, album, duration |
| **Album** | Collection of songs by an artist with release info |
| **Artist** | Artist name, albums, songs catalog |
| **User** | Id, username, password, playlists list |
| **Playlist** | List of songs with add/remove operations |
| **MusicLibrary** | Singleton; stores and manages songs, albums, artists |
| **UserManager** | Singleton; registration, login |
| **MusicPlayer** | Play, pause, skip, seek functionality |
| **MusicRecommender** | Singleton; recommendations from preferences/history |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | MusicLibrary centralizes the music catalog; UserManager handles all user operations; MusicRecommender provides a single recommendation engine |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/musicstreamingservice) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/musicstreamingservice) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/musicstreamingservice) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/musicstreamingservice) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/music_streaming_service) |
