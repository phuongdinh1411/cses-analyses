---
layout: simple
title: "Room Allocation - Interval Scheduling Problem"
permalink: /problem_soulutions/sorting_and_searching/room_allocation_analysis
difficulty: Medium
tags: [sweep-line, priority-queue, interval-scheduling, greedy]
prerequisites: [restaurant_customers, movie_festival]
---

# Room Allocation

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Sweep Line with Event Processing / Priority Queue |
| **CSES Link** | [Room Allocation](https://cses.fi/problemset/task/1164) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply sweep line algorithm with event-based processing
- [ ] Use a priority queue (min-heap) to efficiently track resource availability
- [ ] Manage room assignments while processing interval events
- [ ] Handle the classic "Meeting Rooms II" pattern with assignment tracking

---

## Problem Statement

**Problem:** There are n customers who want to book hotel rooms. Each customer has an arrival day and a departure day. You need to allocate rooms such that no two customers with overlapping stays share the same room. Find the minimum number of rooms needed and assign each customer to a specific room.

**Input:**
- Line 1: Integer n (number of customers)
- Lines 2 to n+1: Two integers a and d (arrival and departure days for each customer)

**Output:**
- Line 1: Integer k (minimum number of rooms needed)
- Line 2: n integers representing room assignments (room number for each customer in input order)

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= a <= d <= 10^9

### Example

```
Input:
3
1 2
2 4
4 4

Output:
2
1 2 1
```

**Explanation:**
- Customer 1 stays days 1-2, assigned Room 1
- Customer 2 stays days 2-4, overlaps with Customer 1 on day 2, assigned Room 2
- Customer 3 stays day 4, Customer 1 has left (departed day 2), assigned Room 1
- Minimum 2 rooms needed

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we find the minimum number of rooms and track which room each customer gets?

This is the classic **interval scheduling with resource assignment** problem. The minimum rooms needed equals the maximum number of overlapping intervals at any point in time. However, we also need to track which specific room each customer receives.

### Breaking Down the Problem

1. **What are we looking for?** Minimum rooms AND specific room assignment for each customer
2. **What information do we have?** Arrival and departure times for each customer
3. **What's the relationship?** Maximum concurrent stays = minimum rooms needed; we must reuse freed rooms

### The Sweep Line Insight

Think of this like a hotel front desk:
- When a customer **arrives**, they need a room. If a room is free, give them that room. Otherwise, create a new room.
- When a customer **departs**, their room becomes available for the next guest.
- The key insight: **Process events in chronological order**, and track room availability with a priority queue.

**Important:** When arrival and departure happen on the same day, process departures first. A room vacated on day 3 can be assigned to someone arriving on day 3.

---

## Solution 1: Brute Force

### Idea

For each customer (in order of arrival), scan all existing rooms to find one that is available. If none available, create a new room.

### Algorithm

1. Sort customers by arrival time (keeping track of original indices)
2. For each customer, iterate through all rooms to find an available one
3. If found, assign that room; otherwise, create a new room

### Code

```python
def solve_brute_force(n, customers):
 """
 Brute force solution - check all rooms for each customer.

 Time: O(n^2)
 Space: O(n)
 """
 # customers[i] = (arrival, departure, original_index)
 indexed = [(customers[i][0], customers[i][1], i) for i in range(n)]
 indexed.sort()  # Sort by arrival time

 room_end_times = []  # room_end_times[r] = departure day of current guest in room r
 assignments = [0] * n

 for arrival, departure, orig_idx in indexed:
  assigned = False
  for room_id in range(len(room_end_times)):
   if room_end_times[room_id] < arrival:  # Room is free
    room_end_times[room_id] = departure
    assignments[orig_idx] = room_id + 1
    assigned = True
    break

  if not assigned:
   room_end_times.append(departure)
   assignments[orig_idx] = len(room_end_times)

 return len(room_end_times), assignments
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | For each of n customers, scan up to n rooms |
| Space | O(n) | Store room end times and assignments |

### Why This Works (But Is Slow)

Correctness is guaranteed because we always try to reuse existing rooms before creating new ones. However, scanning all rooms for each customer is inefficient.

---

## Solution 2: Optimal Solution with Priority Queue

### Key Insight

> **The Trick:** Use a min-heap to efficiently find the room that becomes free earliest. If that room's end time is before our arrival, we can reuse it.

Instead of scanning all rooms, maintain a min-heap of (end_time, room_id). The room with the earliest end time is at the top. If it is free when we need it, pop and reuse; otherwise, create a new room.

### Algorithm

1. Create events: (arrival, departure, original_index) for each customer
2. Sort by arrival time
3. Use a min-heap of (departure_time, room_id) to track room availability
4. Also maintain a "free rooms" heap for room reuse
5. For each customer:
   - If the earliest-ending room is free (end_time < arrival), reuse it
   - Otherwise, create a new room

### Dry Run Example

Let's trace through with input:
```
3 customers: [(1,2), (2,4), (4,4)]
```

```
Initial state:
  available_rooms = []  (min-heap of (end_time, room_id))
  free_rooms = []       (min-heap of room_ids available for reuse)
  room_count = 0
  assignments = [0, 0, 0]

Sorted customers by arrival: [(1,2,0), (2,4,1), (4,4,2)]

Step 1: Process Customer 0 (arrival=1, departure=2)
  - available_rooms is empty, no free rooms
  - Create Room 1, room_count = 1
  - Push (2, 1) to available_rooms
  - assignments[0] = 1
  - available_rooms = [(2, 1)]

Step 2: Process Customer 1 (arrival=2, departure=4)
  - Top of heap: (2, 1), but end_time=2 is NOT < arrival=2
  - (Same-day departure doesn't free room until END of day)
  - Actually, CSES considers day overlap: if end=2 and arrival=2, they overlap
  - Create Room 2, room_count = 2
  - Push (4, 2) to available_rooms
  - assignments[1] = 2
  - available_rooms = [(2, 1), (4, 2)]

Step 3: Process Customer 2 (arrival=4, departure=4)
  - Top of heap: (2, 1), end_time=2 < arrival=4 -> Room 1 is free!
  - Pop (2, 1), reuse Room 1
  - Push (4, 1) to available_rooms
  - assignments[2] = 1
  - available_rooms = [(4, 1), (4, 2)]

Final: room_count = 2, assignments = [1, 2, 1]
```

### Visual Diagram

```
Timeline:
Day:    1    2    3    4
        |    |    |    |
Room 1: [====]         [==]     Customer 0, then Customer 2
Room 2:      [=========]        Customer 1

Customer 0: days 1-2, Room 1
Customer 1: days 2-4, Room 2 (overlaps with Customer 0 on day 2)
Customer 2: day 4, Room 1 (Customer 0 left after day 2)
```

### Code (Python)

```python
import heapq
from sys import stdin, stdout

def solve():
 """
 Optimal solution using priority queue.

 Time: O(n log n) - sorting + heap operations
 Space: O(n) - heap and assignments array
 """
 input_data = stdin.read().split()
 idx = 0
 n = int(input_data[idx]); idx += 1

 customers = []
 for i in range(n):
  a = int(input_data[idx]); idx += 1
  d = int(input_data[idx]); idx += 1
  customers.append((a, d, i))

 # Sort by arrival time
 customers.sort()

 # Min-heap: (departure_time, room_id)
 occupied_rooms = []
 # Min-heap of available room IDs for reuse
 free_rooms = []
 room_count = 0
 assignments = [0] * n

 for arrival, departure, orig_idx in customers:
  # Free up rooms that have ended before this arrival
  while occupied_rooms and occupied_rooms[0][0] < arrival:
   _, freed_room = heapq.heappop(occupied_rooms)
   heapq.heappush(free_rooms, freed_room)

  if free_rooms:
   # Reuse the smallest numbered free room
   room_id = heapq.heappop(free_rooms)
  else:
   # Create new room
   room_count += 1
   room_id = room_count

  assignments[orig_idx] = room_id
  heapq.heappush(occupied_rooms, (departure, room_id))

 stdout.write(f"{room_count}\n")
 stdout.write(" ".join(map(str, assignments)) + "\n")

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Sorting + each customer involves O(log n) heap operations |
| Space | O(n) | Heaps and assignment array |

---

## Common Mistakes

### Mistake 1: Wrong Event Ordering

```python
# WRONG: Using <= instead of <
while occupied_rooms and occupied_rooms[0][0] <= arrival:
 # This frees a room ending on day 2 for someone arriving day 2
 # But they actually overlap on day 2!
```

**Problem:** If Customer A departs on day 2 and Customer B arrives on day 2, they overlap (both use the room on day 2).

**Fix:** Use strict less than (`<`) when comparing departure with arrival:
```python
while occupied_rooms and occupied_rooms[0][0] < arrival:
```

### Mistake 2: Losing Track of Original Customer Order

```python
# WRONG: Forgetting to track original indices
customers.sort()  # Sorted, but lost original positions

# After processing, assignments are in sorted order, not input order!
```

**Problem:** The output must list room assignments in the original input order.

**Fix:** Store original index with each customer and use it for assignment:
```python
customers = [(arrival, departure, original_index) for ...]
# ...
assignments[orig_idx] = room_id  # Use original index
```

### Mistake 3: Not Reusing Room IDs Properly

```python
# WRONG: Always incrementing room count
room_id = len(occupied_rooms) + 1  # Creates too many rooms
```

**Problem:** Should reuse room IDs when rooms become free to get minimum room count.

**Fix:** Track freed room IDs in a separate structure and reuse them:
```python
if free_rooms:
 room_id = heapq.heappop(free_rooms)
else:
 room_count += 1
 room_id = room_count
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single customer | `n=1, (1,5)` | `1` room, assignment `1` | Only one room needed |
| All overlapping | `(1,10), (1,10), (1,10)` | `3` rooms | All customers need separate rooms |
| No overlapping | `(1,2), (3,4), (5,6)` | `1` room | Can reuse same room |
| Same day | `(5,5), (5,5)` | `2` rooms | Both need room on day 5 |
| Sequential | `(1,2), (2,3), (3,4)` | `2` rooms | Arrival=departure means overlap |
| Large n | n=200000 | Must handle | Test efficiency |
| Large values | a,d up to 10^9 | Handle without overflow | Use appropriate data types |

---

## When to Use This Pattern

### Use This Approach When:
- Finding minimum resources needed for overlapping intervals
- Need to track which specific resource is assigned to each interval
- Classic "meeting rooms" style problems
- Event scheduling with resource constraints

### Don't Use When:
- Only need to count maximum overlap (simpler sweep line suffices)
- Intervals have weights/priorities affecting assignment
- Need to maximize profit/value (consider greedy by end time)

### Pattern Recognition Checklist:
- [ ] Have intervals with start/end times? -> **Consider sweep line**
- [ ] Need minimum resources? -> **Track concurrent count or use priority queue**
- [ ] Need specific resource assignments? -> **Use priority queue with room tracking**
- [ ] Same start/end time means overlap? -> **Use `<` not `<=` for freeing**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Restaurant Customers (CSES)](https://cses.fi/problemset/task/1619) | Basic sweep line, just count max overlap |
| [Movie Festival (CSES)](https://cses.fi/problemset/task/1629) | Interval scheduling (max non-overlapping) |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Meeting Rooms II (LeetCode 253)](https://leetcode.com/problems/meeting-rooms-ii/) | Same problem, just return room count |
| [Car Pooling (LeetCode 1094)](https://leetcode.com/problems/car-pooling/) | Capacity constraint on single vehicle |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [My Calendar III (LeetCode 732)](https://leetcode.com/problems/my-calendar-iii/) | Dynamic event insertion |
| [Movie Festival II (CSES)](https://cses.fi/problemset/task/1632) | K members can watch movies |

---

## Key Takeaways

1. **The Core Idea:** Process intervals by arrival time, use min-heap to efficiently find/reuse freed resources
2. **Time Optimization:** O(n log n) via heap instead of O(n^2) linear scan
3. **Space Trade-off:** O(n) space for heaps to achieve logarithmic operations
4. **Pattern:** This is the canonical "interval partitioning" / "meeting rooms" pattern

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why departure < arrival (not <=) is the correct condition
- [ ] Track original indices when sorting intervals
- [ ] Implement in your preferred language in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Sweep Line](https://cp-algorithms.com/geometry/sweep-line.html)
- [CSES Room Allocation](https://cses.fi/problemset/task/1164) - Interval scheduling
- [LeetCode Meeting Rooms Problems](https://leetcode.com/tag/meeting-rooms/)
