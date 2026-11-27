---
layout: simple
title: "Design Strava — Hello Interview Style"
permalink: /system_design/hellointerview/strava
---

# Strava

**Patterns:** Scaling Writes · Real-time Updates  
**Difficulty:** Medium  
**Source:** hellointerview.com (AI-generated full solution)

---

## Summary

- **Key challenge:** Ingest GPS from 10M concurrent activities (~2M points/sec, ~100MB/s) while the app keeps working fully offline.
- **Core design:** The app records GPS and computes stats on-device, batch-uploading to a stateless GPS Ingest Service → Kafka (by activity_id) → TimescaleDB/Cassandra; activity metadata lives in PostgreSQL.
- **Techniques:** Offline-first client with SQLite (device is source of truth); idempotent batches on (activity_id, batch_id) (safe retries); Kafka buffer (bursts, replay); time-series store keyed activity_id + timestamp (write throughput); Redis Pub/Sub + WebSocket (live sharing); Redis sorted set per segment (leaderboards).

## Understanding the Problem

🏃‍♂️🚴‍♀️ **What is Strava?**  
Strava is a fitness tracking app that lets users record running and cycling activities, see their route/stats in real time, and share completed activities with friends.

---

### Functional Requirements

**Core Requirements**

- Users should be able to start, pause, stop, and save their runs and rides
- While running/cycling, users should be able to view activity data including route, distance, and time
- Users should be able to view details about their own completed activities and the activities of their friends

**Below the line (out of scope):**

- Friend management (adding/removing friends)
- Commenting or liking runs
- Authentication and authorization

### Non-Functional Requirements

**Core Requirements**

- The system should be highly available (availability >> consistency)
- The app should function in remote areas without network connectivity (offline support)
- The app should provide the athlete with accurate and up-to-date local statistics during the run/ride
- The system should scale to 10 million concurrent activities

**Below the line (out of scope):**

- Sub-second global sync of live route to friends
- Strong consistency for leaderboard rankings

### Constraints & Estimates

- 10M concurrent activities, each emitting a GPS point every ~5 seconds
- 10M × 1 GPS point/5s = **2M GPS writes/second** peak
- Each GPS point: ~50 bytes (lat, lng, timestamp, elevation, heart_rate)
- 2M × 50 bytes = **100MB/s** ingestion rate
- Average activity: 1 hour × 720 points = ~36KB of GPS data
- 10M activities/day × 36KB = **360GB/day** new GPS data

---

## The Set Up

### Defining the Core Entities

- **User** – id, name, profile
- **Activity** – id, user_id, type (run/ride), status (active/paused/completed), start_time, end_time, distance_m, elapsed_seconds, route_encoded
- **GPSPoint** – activity_id, timestamp, lat, lng, elevation, heart_rate, speed
- **Friend** – user_id, friend_id

### The API

```
// Start an activity
POST /activities
{ "type": "run" }
-> { activity_id, started_at }

// Upload GPS batch (mobile batches points when network available)
POST /activities/{activity_id}/gps
{ "points": [{ "lat": 37.78, "lng": -122.4, "ts": 1700000000, "ele": 10, "hr": 145 }, ...] }
-> { received: N }

// Pause / Resume activity
PATCH /activities/{activity_id}
{ "status": "paused" | "active" }
-> { status, elapsed_seconds }

// Complete and save activity
POST /activities/{activity_id}/complete
{ "final_points": [...] }
-> { activity_id, distance_m, elapsed_seconds, pace, map_url }

// Get activity details
GET /activities/{activity_id}
-> { activity, gps_points, stats }

// Get friend feed
GET /activities/feed?limit=20&cursor=<id>
-> { activities: [...] }
```

---

## High-Level Design

### 1) Users should be able to start, pause, stop, and save their runs and rides

**Activity lifecycle state machine:**
```
CREATED → ACTIVE ⇄ PAUSED → COMPLETED
```

**Key design insight:** Most of the activity tracking is done **on the device (client-side)**. The phone's GPS sensor records points locally. The server is a durable sink for the data, not the source of truth during recording.

**Components:**
- **Mobile App** – records GPS locally, computes real-time stats (distance, pace, map) locally
- **Activity Service** – manages activity lifecycle (start, pause, complete)
- **GPS Ingest Service** – high-throughput write path for GPS point batches
- **Activity DB** (PostgreSQL) – stores completed activity metadata
- **GPS Time-Series Store** (TimescaleDB or Cassandra) – stores raw GPS points

**On activity start:**
1. POST `/activities` → Activity Service creates record with status=ACTIVE
2. App begins recording GPS locally (no server dependency)
3. App periodically uploads GPS batches (every 30s or when back online)

**On activity complete:**
1. App uploads any remaining GPS points
2. POST `/activities/{id}/complete` → Activity Service:
   - Marks activity COMPLETED
   - Triggers async **Stats Computation Job** (distance, elevation gain, splits)
   - Encodes route as polyline (Google Encoded Polyline format) for map display
3. Activity is now visible on the user's profile and friend feed

### 2) While running/cycling, users should be able to view activity data

**Critical insight:** All real-time stats during a run are computed **locally on the device**:
- Distance: Haversine formula between consecutive GPS points
- Pace: (time elapsed) / (distance covered)
- Map: render GPS points on local map tile cache (Mapbox offline tiles)
- Elapsed time: local clock

This means the system works **completely offline**. The device is the source of truth during the activity. Server sync is best-effort.

For users who want to see live stats on a connected device (e.g., phone + smartwatch):
- Bluetooth sync between devices
- No server round-trip needed for in-activity stats

### 3) Users should be able to view details about completed activities

**Activity feed (friends' completed activities):**

Similar to Instagram's feed problem, but simpler (much lower write rate — activities complete, not post every second).

Pull-on-read approach works fine at Strava's scale:
1. `GET /activities/feed` → Feed Service queries friends' recent completed activities
2. Users typically have < 500 friends → manageable fan-out
3. Cache friend IDs in Redis; cache recent activities per user in Redis (LRU, TTL 1 hour)

**Activity detail view:**
1. Fetch activity metadata from PostgreSQL
2. Fetch GPS points from TimescaleDB for route rendering
3. Serve pre-computed stats (pace splits, elevation chart data) from activity record

---

## Potential Deep Dives

### 1) How can we support tracking activities while offline?

**Offline-first architecture:**

The mobile app is the system of record during an active activity:

1. **Local GPS recording** – All points stored in SQLite on the device
2. **Offline stats computation** – Distance, pace, map rendered locally
3. **Background sync** – When connectivity returns, app uploads accumulated GPS batches
4. **Idempotent uploads** – Each GPS batch includes a `batch_id`; server deduplicates on `(activity_id, batch_id)` to handle retries

**Conflict resolution:** What if the user completes an activity while offline and the server never saw any intermediate GPS?
- App sends all GPS points + completion event in one final upload
- Server processes them in order (sorted by timestamp)
- Acceptable delay: activity appears on friends' feeds after re-connection

### 2) How can we scale to support 10 million concurrent activities?

**Problem:** 2M GPS writes/second is massive. Standard PostgreSQL can handle ~10K TPS — we need 200× that.

**GPS Ingest Architecture:**

```
Mobile App
  → Load Balancer
  → GPS Ingest Service (stateless, 500+ instances)
  → Kafka (partitioned by activity_id)
  → GPS Writers (consumer group)
  → TimescaleDB / Cassandra (time-series GPS store)
```

**Why Kafka in the middle?**
- Absorbs write bursts (10M activities don't all stop at once, but start/stop patterns cause spikes)
- Decouples ingest from storage
- Enables replay for reprocessing

**TimescaleDB (PostgreSQL extension for time-series):**
- Automatic partitioning (hypertables) by time
- Efficient `activity_id + timestamp` queries
- Compression for older data (GPS points from last year compressed 10–20×)

**Alternative — Cassandra:**
- Partition key: `activity_id`
- Clustering key: `timestamp`
- Excellent write throughput (100K+ writes/sec per node)
- Good for append-only GPS stream

**Back-of-envelope:**
- 2M writes/sec × 50 bytes = 100MB/sec → manageable with 10–20 Kafka partitions and 20 Cassandra nodes

### 3) How can we support real-time sharing of activities with friends?

**Use case:** "Track a friend running a marathon live."

**Architecture: WebSocket + GPS fan-out**

1. Activity owner opts into "live sharing" on activity start
2. Owner's app uploads GPS points more frequently (every 5s instead of batch)
3. GPS Ingest Service publishes to Kafka topic `live-activities`
4. **Live Sharing Service** maintains WebSocket connections for viewers
5. Fans subscribe via `GET /activities/{id}/live` (SSE or WebSocket)
6. Live Sharing Service reads from Kafka and pushes latest point to subscribers

**Scale consideration:**
- Popular races: 1 runner → thousands of viewers
- Use a pub/sub fan-out pattern (similar to FB Live Comments problem)
- Redis Pub/Sub for activity channels; WebSocket servers subscribe to relevant channels

### 4) How can we expose a leaderboard of top athletes?

**Use case:** Segment leaderboard (fastest runners on a specific route segment).

**Data structure:**
- Pre-defined **Segments** (popular route sections defined by GPS coordinates)
- When an activity completes, **Segment Matching Service** checks if the activity traversed any segments
- For matched segments, compute the user's time and upsert into a **Redis Sorted Set** per segment

```
Key: segment:{segment_id}:leaderboard
Score: elapsed_seconds (lower = better)
Member: user_id
```

**Leaderboard reads:**
```
ZRANGE segment:{id}:leaderboard 0 9 WITHSCORES  // top 10
ZRANK segment:{id}:leaderboard {user_id}         // my rank
```

**Scaling segment matching:**
- Naive: check all segments for every activity completion → O(segments × route_length)
- Better: geospatial index of segment start/end points; only check segments near the activity's bounding box
- Use Elasticsearch geo_shape index for efficient spatial matching

---

## Final Design

```
Mobile App (offline-first)
  │ GPS batches (async, over HTTP)
  ▼
GPS Ingest Service (stateless, ~500 pods)
  ├─→ Kafka (partitioned by activity_id)
  │     └─→ GPS Writers → TimescaleDB (raw GPS)
  │     └─→ Live Sharing Service → WebSocket → viewers
  │
  └─→ Activity Service → PostgreSQL (activity metadata)
                        └─→ Stats Worker (async: distance, pace, elevation)
                        └─→ Segment Matching → Redis Sorted Sets (leaderboards)

Feed Service
  ├─→ Redis (friend IDs cache, recent activity cache)
  └─→ PostgreSQL (friends' completed activities)
```

---

## What is Expected at Each Level?

### Mid-level
- Correctly identifies offline-first requirement
- Proposes client-side GPS recording and periodic upload
- Simple activity metadata in PostgreSQL
- Basic friend feed (pull-on-read)

### Senior
- Kafka-based GPS ingest pipeline for 2M writes/sec
- TimescaleDB or Cassandra for time-series GPS data
- Idempotent batch uploads with deduplication
- Segment leaderboard with Redis Sorted Sets

### Staff+
- Detailed offline sync / conflict resolution strategy
- Live sharing WebSocket architecture with Kafka fan-out
- Geospatial segment matching with Elasticsearch
- Compression strategy for archival GPS data
- Discusses Kafka partition strategy and consumer group scaling
