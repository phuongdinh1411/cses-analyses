# Train Time Table

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

A train line has stations A and B. Trains travel both ways. After arriving, a train needs turnaround time T before it can depart again.

Given all trips (departure/arrival times), find the minimum trains needed at each station to cover all departures.

## Input Format
- N test cases
- Each test case:
  - First line: T (turnaround time in minutes)
  - Second line: NA, NB (trips from A to B, and B to A)
  - Next NA lines: departure and arrival times for A→B trips (HH:MM format)
  - Next NB lines: departure and arrival times for B→A trips

## Output Format
For each test case: "Case #x: a b" where a = trains starting at A, b = trains starting at B.

## Example
```
Input:
1
5
3 2
09:00 12:00
10:00 13:00
11:00 12:30
12:02 15:00
09:00 10:30

Output:
Case #1: 2 2
```
With turnaround time 5 minutes: 3 trains go from A to B, 2 from B to A. Station A needs 2 trains initially, and station B needs 2 trains initially to cover all departures.

## Solution

### Approach
Use greedy simulation with events:
1. Create events for all departures and arrivals
2. Sort by time
3. Track available trains at each station
4. When a train departs, use an available one or add a new train
5. When a train arrives (after turnaround), it becomes available

### Python Solution

```python
from collections import defaultdict

def solve():
  n = int(input())

  for case in range(1, n + 1):
    t = int(input())  # turnaround time
    na, nb = map(int, input().split())

    def parse_time(s):
      h, m = s.split(':')
      return int(h) * 60 + int(m)

    events = []  # (time, type, station)
    # type: 0 = departure, 1 = arrival (ready after turnaround)

    for _ in range(na):
      dep, arr = input().split()
      events.append((parse_time(dep), 0, 'A'))  # depart from A
      events.append((parse_time(arr) + t, 1, 'B'))  # arrive at B (available)

    for _ in range(nb):
      dep, arr = input().split()
      events.append((parse_time(dep), 0, 'B'))  # depart from B
      events.append((parse_time(arr) + t, 1, 'A'))  # arrive at A (available)

    # Sort: by time, then arrivals before departures (type 1 before 0)
    events.sort(key=lambda x: (x[0], -x[1]))

    # Use defaultdict for cleaner initialization
    available = defaultdict(int)
    needed = defaultdict(int)

    # Tuple unpacking in loop
    for time, event_type, station in events:
      if event_type == 0:  # departure
        if available[station] > 0:
          available[station] -= 1
        else:
          needed[station] += 1
      else:  # arrival (train becomes available)
        available[station] += 1

    print(f"Case #{case}: {needed['A']} {needed['B']}")

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
import heapq

def solve():
  n = int(input())

  for case in range(1, n + 1):
    t = int(input())
    na, nb = map(int, input().split())

    def to_minutes(s):
      h, m = s.split(':')
      return int(h) * 60 + int(m)

    # Collect all trips
    trips_from_a = []
    trips_from_b = []

    for _ in range(na):
      parts = input().split()
      dep = to_minutes(parts[0])
      arr = to_minutes(parts[1])
      trips_from_a.append((dep, arr))

    for _ in range(nb):
      parts = input().split()
      dep = to_minutes(parts[0])
      arr = to_minutes(parts[1])
      trips_from_b.append((dep, arr))

    trips_from_a.sort()
    trips_from_b.sort()

    # available_at_X is a min-heap of times when trains become available at X
    available_a = []
    available_b = []
    trains_a = 0
    trains_b = 0

    # Process trips from A
    for dep, arr in trips_from_a:
      # Check if train available at A before dep
      while available_a and available_a[0] <= dep:
        heapq.heappop(available_a)
        # Train is ready but we'll use one
      if available_a and available_a[0] <= dep:
        heapq.heappop(available_a)
      else:
        # Need to check heap properly
        pass

    # Actually, let's use the event-based approach properly
    # Reset and redo

    events = []
    for dep, arr in trips_from_a:
      events.append((dep, 0, 'A'))
      events.append((arr + t, 1, 'B'))
    for dep, arr in trips_from_b:
      events.append((dep, 0, 'B'))
      events.append((arr + t, 1, 'A'))

    events.sort(key=lambda x: (x[0], -x[1]))

    avail = {'A': 0, 'B': 0}
    need = {'A': 0, 'B': 0}

    for tm, typ, st in events:
      if typ == 0:
        if avail[st] > 0:
          avail[st] -= 1
        else:
          need[st] += 1
      else:
        avail[st] += 1

    print(f"Case #{case}: {need['A']} {need['B']}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O((NA + NB) log(NA + NB))
- **Space Complexity:** O(NA + NB)

### Key Insight
Model as an event simulation. Each trip creates two events: departure (needs a train) and arrival (train becomes available after turnaround). Process events chronologically. When departing, use an available train if possible, otherwise allocate a new one. Sort ties so arrivals process before departures at the same time.
