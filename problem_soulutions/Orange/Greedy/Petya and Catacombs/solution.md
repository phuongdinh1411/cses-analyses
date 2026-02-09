# Petya and Catacombs

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

## Problem Statement

Petya explores Paris catacombs. Every minute he moves through a passage to another room. When entering a room at minute i, he notes:
- If visited before: the minute he was last in this room
- Otherwise: any non-negative integer strictly less than i

Initially at minute 0, Petya was in a room (no note for t₀). Find the minimum possible number of rooms.

## Input Format
- First line: n (1 ≤ n ≤ 2×10⁵) - number of notes
- Second line: n integers t₁, t₂, ..., tₙ (0 ≤ tᵢ < i)

## Output Format
Print the minimum possible number of rooms in Paris catacombs.

## Example
```
Input:
5
0 1 0 3 2

Output:
3
```
Notes: [0, 1, 0, 3, 2]. Minute 1: note 0 (could be revisiting start or new room - use new room). Minute 2: note 1 (revisit room from minute 1). Minute 3: note 0 (revisit start room). Minute 4: note 3 (new room). Minute 5: note 2 (revisit room from minute 2). Minimum rooms = 3.

## Solution

### Approach
Track which "last visit times" are available. When Petya enters a room:
- If tᵢ was a previous minute where a room was last visited, he's revisiting that room
- Otherwise, he's entering a new room

Use a set to track available "last visit" times. Initially, time 0 is available (starting room).

### Python Solution

```python
def solve():
    n = int(input())
    times = list(map(int, input().split()))

    available = {0}  # Times when rooms were last visited
    rooms = 1  # Start with 1 room (the initial room)

    for i, t in enumerate(times, 1):
        if t in available:
            # Revisiting a room - remove old time, add current time
            available.discard(t)
            available.add(i)
        else:
            # New room
            rooms += 1
            available.add(i)

    print(rooms)

if __name__ == "__main__":
    solve()
```

### Alternative Solution

```python
def solve():
  n = int(input())
  notes = list(map(int, input().split()))

  # Track which timestamps are "used" (a room was last visited at that time)
  used = [False] * (n + 1)
  used[0] = True  # Initial room at time 0
  rooms = 1

  for i in range(n):
    t = notes[i]
    current_time = i + 1

    if used[t]:
      # Revisiting room that was last visited at time t
      used[t] = False
      used[current_time] = True
    else:
      # Must be a new room
      rooms += 1
      used[current_time] = True

  print(rooms)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N)
- **Space Complexity:** O(N)

### Key Insight
Each room has a "last visited time". When we see note tᵢ, if time t was previously a room's last-visit-time, we can revisit that room (updating its last-visit to current time i). Otherwise, we must create a new room. Greedy assignment minimizes rooms.
