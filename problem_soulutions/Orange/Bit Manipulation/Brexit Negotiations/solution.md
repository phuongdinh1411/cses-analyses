# Brexit Negotiations

## Problem Information
- **Source:** Kattis
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 1024MB

## Problem Statement

Brexit negotiations have n topics with dependencies. Each topic has a base duration eᵢ minutes. At the start of each meeting, delegates take 1 extra minute for each previous meeting to recap.

If a meeting is the k-th meeting (0-indexed), its total time is eᵢ + k minutes.

Find an ordering of topics (respecting dependencies) that minimizes the longest meeting duration.

## Input Format
- First line: n (1 ≤ n ≤ 4 × 10^5)
- Next n lines: eᵢ (duration) and dᵢ (number of dependencies), followed by dᵢ prerequisite topic numbers

## Output Format
Output the minimum possible length of the longest meeting.

## Example
```
Input:
4
3 0
5 1 1
1 1 2
2 2 1 3

Output:
6
```
4 topics. Topic 1: duration 3, no dependencies. Topic 2: duration 5, depends on topic 1. Topic 3: duration 1, depends on topic 2. Topic 4: duration 2, depends on topics 1 and 3. Optimal order: 1,2,3,4. Meeting times: 3+0=3, 5+1=6, 1+2=3, 2+3=5. Maximum is 6.

## Solution

### Approach
Key insight: Process topics in **reverse** topological order, choosing the topic with smallest base duration among those with no dependents.

If we process topics in order n-1, n-2, ..., 0 (reversed), a topic processed at position i has recap time (n-1-i). We want topics with large base durations to have small recap times (processed early in reversed order = late in actual order).

Use a min-heap with (base_duration, topic_id) to greedily select topics.

### Python Solution

```python
import heapq
from collections import defaultdict

def solve():
  n = int(input())

  base_time = [0] * (n + 1)
  deps = [[] for _ in range(n + 1)]  # deps[u] = topics that depend on u
  out_degree = [0] * (n + 1)  # number of topics u depends on

  for u in range(1, n + 1):
    line = list(map(int, input().split()))
    base_time[u] = line[0]
    d = line[1]
    for v in line[2:2+d]:
      deps[u].append(v)
      out_degree[v] += 1

  # Process in reverse order using min-heap
  # Start with topics that have no dependents (out_degree = 0)
  heap = []
  for u in range(1, n + 1):
    if out_degree[u] == 0:
      heapq.heappush(heap, (base_time[u], u))

  max_meeting = 0
  recap_time = n - 1  # First topic processed has recap = n-1

  while heap:
    dur, u = heapq.heappop(heap)
    total_time = dur + recap_time
    max_meeting = max(max_meeting, total_time)
    recap_time -= 1

    for v in deps[u]:
      out_degree[v] -= 1
      if out_degree[v] == 0:
        heapq.heappush(heap, (base_time[v], v))

  print(max_meeting)

if __name__ == "__main__":
  solve()
```

### Alternative Explanation

```python
import heapq

def solve():
  n = int(input())

  time = [0] * (n + 1)
  prereqs = [[] for _ in range(n + 1)]
  dep_count = [0] * (n + 1)

  for i in range(1, n + 1):
    parts = list(map(int, input().split()))
    time[i] = parts[0]
    d = parts[1]
    prereqs[i] = parts[2:2+d]
    for p in prereqs[i]:
      dep_count[p] += 1

  # Reverse topological sort: process nodes with no dependents first
  # Assign highest recap times to smallest base durations
  pq = [(time[i], i) for i in range(1, n + 1) if dep_count[i] == 0]
  heapq.heapify(pq)

  ans = 0
  position = n - 1  # Recap time for current position

  while pq:
    t, u = heapq.heappop(pq)
    ans = max(ans, t + position)
    position -= 1

    for p in prereqs[u]:
      dep_count[p] -= 1
      if dep_count[p] == 0:
        heapq.heappush(pq, (time[p], p))

  print(ans)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N log N) for heap operations
- **Space Complexity:** O(N + E) where E is total dependencies

### Key Insight
This is a scheduling problem. The k-th meeting (0-indexed) costs e + k time. To minimize maximum, we want to:
- Schedule short meetings late (high recap time)
- Schedule long meetings early (low recap time)

Processing in reverse topological order with a min-heap achieves this optimally.
