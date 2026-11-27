---
layout: simple
title: "Design Online Chess (Chess.com) — Hello Interview Style"
permalink: /system_design/hellointerview/online-chess
---

# Online Chess

**Patterns:** Real-time Updates · Dealing with Contention  
**Difficulty:** Hard  
**Source:** hellointerview.com (AI-generated full solution)

---

## Understanding the Problem

♟️ **What is Chess.com / Lichess?**  
Online chess platforms let players find an opponent of similar skill, play real-time games with per-player clocks, and climb a global rating leaderboard. The server validates every move and owns both clocks — players can't cheat by claiming illegal moves or extra time.

**Format:** 3-minute blitz (each player has 3 minutes total; clock runs only during their turn).

---

### Functional Requirements

**Core Requirements**

- Players should be able to find an opponent through skill-based matchmaking and start a game
- Players should be able to play a game in real time
- Players should be able to view a global leaderboard and see their own rank

**Below the line (out of scope):**

- Spectating live games
- In-game chat and social features
- Puzzles, training, and post-game analysis
- Tournaments and arena play
- Anti-cheat engine detection

### Non-Functional Requirements

**Core Requirements**

- 10M registered players, **500K concurrent games** at peak
- Matchmaking should pair players within **10 seconds**
- Move validation must be **fast** (< 50ms server processing per move)
- Clocks must be **fair** despite uneven network latency
- Leaderboard must be **correct** and **fast** (< 200ms query)

**Below the line (out of scope):**

- Sub-10ms move processing (50ms is fine for blitz chess)

### Constraints & Estimates

- 500K concurrent games × 2 players = **1M concurrent WebSocket connections**
- Move rate: ~1 move per 3 seconds per game → 500K × (2/3) ≈ **333K moves/sec** peak
- Each move event: ~100 bytes
- Leaderboard: 10M players, updated after every game finish
- Rating updates: 500K games/day × 2 players = 1M rating updates/day → ~12 updates/sec (easy)

---

## The Set Up

### Planning the Approach

Three independently challenging sub-problems:
1. **Matchmaking** – pair players by skill without race conditions
2. **Game Server** – real-time move processing, clock management, move validation
3. **Leaderboard** – globally ranked 10M players, fast to query and update

### Defining the Core Entities

- **Player** – id, username, rating (Elo), games_played, wins, losses
- **MatchmakingEntry** – player_id, rating, queued_at, status (waiting/matched)
- **Game** – id, white_player_id, black_player_id, status (active/finished), moves[] (PGN notation), result, started_at, finished_at
- **Clock** – game_id, white_remaining_ms, black_remaining_ms, last_move_ts, whose_turn
- **LeaderboardEntry** – player_id, rating, rank

### API or System Interface

```
// Join matchmaking queue
POST /matchmaking/join
-> { queue_id, estimated_wait_secs }

// Cancel matchmaking
DELETE /matchmaking/join

// Real-time game (WebSocket)
WS /games/{game_id}
Client → Server: { "type": "move", "from": "e2", "to": "e4", "promotion": null }
Server → Client: { "type": "move", "from": "e2", "to": "e4", "clocks": { "white_ms": 178000, "black_ms": 180000 } }
Server → Client: { "type": "game_over", "result": "white_wins", "reason": "checkmate" }
Server → Client: { "type": "clock_update", "white_ms": 177500, "black_ms": 180000 }

// Get leaderboard
GET /leaderboard?limit=100&offset=0
-> { players: [ { rank, username, rating } ] }

// Get my rank
GET /players/{id}/rank
-> { rank, rating, percentile }
```

---

## High-Level Design

### 1) Players should be able to find an opponent through matchmaking

**Matchmaking service:**

1. Player calls `POST /matchmaking/join` → writes row to `matchmaking_queue` table (PostgreSQL)
2. **Matchmaking Worker** (runs every 1 second):
   - Scan queue for unmatched players
   - Sort by `queued_at`; for each unmatched player, find the closest-rating opponent:
     ```sql
     SELECT * FROM matchmaking_queue
     WHERE status = 'waiting'
       AND ABS(rating - :target_rating) < :tolerance
       AND player_id != :player_id
     ORDER BY ABS(rating - :target_rating), queued_at
     LIMIT 1
     FOR UPDATE SKIP LOCKED;  -- prevent two workers from matching the same player
     ```
   - **Expanding search radius:** tolerance starts at ±50 Elo, expands by 25 Elo every 2 seconds of waiting
   - On match: update both rows to `status=matched`, create Game record, notify both players via WebSocket

**Race condition prevention:** `FOR UPDATE SKIP LOCKED` ensures two parallel matchmaking workers can't match the same player to two different opponents.

**Notification:** Matchmaking service publishes match result to Redis Pub/Sub → WebSocket server pushes "match found, game_id=X" to both players.

### 2) Players should be able to play a game in real time

**Game Server architecture:**

Each active game needs a stateful server that:
- Holds the current board state (FEN notation)
- Runs both clocks
- Validates moves (legal chess moves)
- Broadcasts to both players

```
Both players → WebSocket connection → Game Server (stateful per game)
```

**Move processing flow:**
1. Player sends `{ type: "move", from: "e2", to: "e4" }`
2. Game Server receives move:
   a. Verify it's this player's turn
   b. Validate move is legal (chess move validation library, e.g., `chess.js`)
   c. Record the timestamp of move receipt (for clock accounting)
   d. Update board state (FEN)
   e. Update clocks: `white_remaining -= (now - last_move_ts)`; `last_move_ts = now`; switch turn
   f. Persist move to DB (append to game.moves[])
   g. Broadcast to both players: `{ type: "move", from, to, clocks, next_turn }`
3. If game ends (checkmate/stalemate/timeout): send `game_over`, update game status, trigger rating update

**Clock management:**
- Server owns both clocks (not clients — prevents cheating)
- Last move timestamp tracked server-side
- Send clock updates to clients every 1 second (for display) and on every move

### 3) Players should be able to view the global leaderboard

**Leaderboard using Redis Sorted Set:**

```
ZADD leaderboard {rating} {player_id}  // O(log N)
ZREVRANK leaderboard {player_id}       // get rank, O(log N)
ZREVRANGE leaderboard 0 99 WITHSCORES  // top 100, O(log N + k)
```

**After each game finishes:**
- Rating Updater Service computes new Elo ratings (Elo formula)
- Updates `players` table (PostgreSQL)
- `ZADD leaderboard {new_rating} {player_id}` — updates sorted set atomically

This gives O(log N) rank updates and O(log N + k) top-N queries for 10M players.

---

## Potential Deep Dives

### 1) How do we prevent a player from being matched into two games?

**Race condition:** Two matchmaking workers run simultaneously. Worker A picks player X to match with player Y. Worker B simultaneously picks player X to match with player Z. Player X gets two games.

**Solution: `FOR UPDATE SKIP LOCKED`**

As shown above: when Worker A acquires a lock on player X's row (via `FOR UPDATE`), Worker B's query skips that row (via `SKIP LOCKED`). Worker B only sees unlocked rows → never duplicates the match.

**Additional guard:** `UNIQUE(player_id)` constraint on active games:
```sql
CREATE UNIQUE INDEX idx_active_game_player ON games(player_id)
  WHERE status = 'active';
```
Attempting to create a second active game for the same player fails at the DB level.

#### What if matchmaking outgrows Postgres?

At very high scale (millions of players queueing simultaneously), Postgres scanning + locking the queue every second is expensive.

**Alternative: Redis-based matching queue**
- Players join via `ZADD matchmaking_queue {rating} {player_id}`
- Matchmaking Worker: `ZRANGE matchmaking_queue {rating-50} {rating+50}` → find candidates
- Use `Lua script` for atomic match-and-remove (prevents race conditions without DB locks):
  ```lua
  local candidates = redis.call('ZRANGEBYSCORE', 'matchmaking_queue', min_rating, max_rating)
  if #candidates > 0 then
    redis.call('ZREM', 'matchmaking_queue', player_id, candidates[1])
    return candidates[1]
  end
  return nil
  ```
- Redis Lua scripts are atomic — no two workers can match the same player

### 2) How do we scale the game servers to 500K concurrent games?

**Problem:** 500K concurrent games × ~2 active WebSocket connections = 1M WebSocket connections. No single server can hold 1M connections (memory + file descriptors limit ~100K per server).

**Game Server Fleet:**

```
Players → Load Balancer (consistent hash by game_id) → Game Server Pool (100 servers × 10K games each)
```

**Assignment:**
- When a game is created: `Game Server Router` (backed by Redis hash map `game_id → server_address`) assigns game to a server with capacity
- Both players connect to the **same game server** (same server = no cross-server communication needed)
- Load balancer uses the routing table to send WebSocket upgrade to the right server

**Game server capacity:** Each server holds 5K games in memory:
- Board state: ~100 bytes (FEN string)
- Clock state: ~50 bytes
- Move history: ~500 bytes
- 5K games × 650 bytes = 3.25MB per server — trivial
- Bottleneck is WebSocket connections (10K connections × ~10KB per WebSocket = 100MB)
- With 100 game servers: 500K games ✓

**Server failure:**
1. Game server crashes → both players get WebSocket disconnect
2. Players reconnect → Router sees `game_id → crashed_server`, reassigns to new server
3. New server loads game state from PostgreSQL (last board position + clocks)
4. Players resend their last move if needed (the client buffers the last move)

### 3) How do we keep the clock fair despite uneven latency?

**Problem:** Player A is on WiFi (20ms RTT to server). Player B is on a slow connection (200ms RTT). Player A sends a move; server records receipt time. But B's connection is slow, so when B sends a move, the server receives it 200ms later. If we naively subtract `now - last_move_ts` from B's clock, B is penalized 200ms extra for every move.

**Solution: Lag compensation with client timestamps**

Client stamps the move with its local clock:
```json
{ "type": "move", "from": "e2", "to": "e4", "client_ts": 1700000000.123 }
```

Server approach:
1. Record **server receipt time**: `server_ts = now`
2. Network latency estimate: `latency = (server_ts - client_ts) / 2` (approximate, one-way is half RTT)
3. Clock deduction: `white_remaining -= (server_ts - last_move_ts) - latency`

This compensates for one-way network delay, making clocks fairer.

**Bounds:** Clamp latency compensation to [0, 500ms] to prevent abuse (player faking a very old client_ts to claim no time was used).

**Lichess approach:** Server records exact arrival time; each player accepts that their displayed clock may differ from server clock by one network RTT. This is the simplest correct solution — the server clock is authoritative; display is approximate.

### 4) How do we keep the leaderboard correct and fast at 10M players?

**Redis Sorted Set:**

As described in HLD:
- 10M players in sorted set: **~800MB memory** (10M × 80 bytes each) — fits on one Redis node
- Rank query: O(log N) ≈ 23 operations for 10M → microseconds
- Top-100 query: O(log N + 100) → microseconds

**Rating update atomicity:**
Both players' ratings change together after a game. Redis and PostgreSQL cannot share one transaction, so commit to the source of truth first and treat Redis as a rebuildable cache:

```python
# fragment: after a game finishes
white_new, black_new = compute_elo(white_old, black_old, result)

with pg.transaction():  # source of truth: both rows or neither
    pg.execute("UPDATE players SET rating = %s WHERE id = %s", (white_new, white_id))
    pg.execute("UPDATE players SET rating = %s WHERE id = %s", (black_new, black_id))

pipe = redis.pipeline(transaction=True)  # MULTI/EXEC: both ZADDs apply together
pipe.zadd("leaderboard", {white_id: white_new, black_id: black_new})
pipe.execute()  # if this fails, a reconciler re-syncs from PostgreSQL
```

**Redis as a cache for leaderboard display:**
- PostgreSQL is the source of truth.
- The Redis sorted set is rebuilt from PostgreSQL on startup or after a crash.
- The rebuild is dominated by scanning 10M rows from PostgreSQL. The ZADDs themselves, pipelined in batches, take seconds.

**Near-rank queries ("who's around me?"):**
```
ZREVRANK leaderboard {my_player_id}  → my_rank = R
ZREVRANGE leaderboard (R-5) (R+5) WITHSCORES  → 10 players around me
```

---

## Final Design

```
Player Browser
  │ WebSocket
  ▼
Load Balancer (consistent hash by game_id for game WS; round-robin for matchmaking)
  │
  ├─ Matchmaking Service
  │   ├─ Redis (player queue sorted by rating)
  │   ├─ PostgreSQL (matchmaking_queue table, FOR UPDATE SKIP LOCKED)
  │   └─ → Creates Game record + notifies players via Redis Pub/Sub
  │
  ├─ Game Server Fleet (100 servers, 5K games each)
  │   ├─ In-memory board state + clocks per game
  │   ├─ Move validation (chess.js)
  │   ├─ WebSocket broadcast to both players
  │   └─ Persist moves to PostgreSQL (async, batched)
  │
  ├─ Rating Updater (on game finish)
  │   ├─ Elo computation
  │   ├─ UPDATE players SET rating = ... (PostgreSQL)
  │   └─ ZADD leaderboard {new_rating} {player_id} (Redis)
  │
  └─ Leaderboard Service
      ├─ Redis Sorted Set (10M players, 800MB)
      └─ PostgreSQL (source of truth)
```

---

## What is Expected at Each Level?

### Mid-level
- Correct entity design and WebSocket API
- Skill-based matchmaking with Elo tolerance expansion
- Game server holds board state and clocks
- Redis Sorted Set for leaderboard

### Senior
- `FOR UPDATE SKIP LOCKED` for matchmaking race condition
- Consistent hash routing for game servers (both players to same server)
- Clock lag compensation with client timestamps
- Rating update atomicity across both players

### Staff+
- Redis Lua script for atomic matchmaking at extreme scale
- Game server fleet failure recovery (reload from DB, client buffers last move)
- Near-rank leaderboard queries
- Detailed Elo computation and anti-sandbagging considerations
- Discusses CRDTs or server reconciliation for extreme latency tolerance
