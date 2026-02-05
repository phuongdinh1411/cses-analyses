---
layout: simple
title: "Line Segment Tracing - Geometry Problem"
permalink: /problem_soulutions/geometry/line_segments_trace_analysis
difficulty: Medium
tags: [geometry, graph-traversal, sweep-line, hashing]
---

# Line Segment Tracing

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Geometry / Graph |
| **Time Limit** | 1 second |
| **Key Technique** | Graph Traversal + Hashing |
| **CSES Link** | [Geometry Section](https://cses.fi/problemset/list/) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Model connected line segments as a graph problem
- [ ] Use coordinate hashing for efficient point matching
- [ ] Identify endpoints for path traversal (degree-1 vertices)
- [ ] Trace paths through connected geometric structures

---

## Problem Statement

**Problem:** Given n line segments, trace the path formed by connecting segments that share endpoints. Output the ordered sequence of points forming the complete path.

**Input:**
- Line 1: n (number of line segments)
- Lines 2 to n+1: Four integers x1, y1, x2, y2 (segment endpoints)

**Output:**
- The sequence of points forming the trace path from start to end

**Constraints:**
- 1 <= n <= 10^5
- -10^6 <= coordinates <= 10^6
- Segments form a single connected path (no branches)

### Example

```
Input:
3
0 0 1 1
1 1 2 0
2 0 3 1

Output:
(0,0) (1,1) (2,0) (3,1)
```

**Explanation:** Segment 1 connects (0,0) to (1,1). Segment 2 shares endpoint (1,1) and goes to (2,0). Segment 3 shares (2,0) and ends at (3,1). The trace follows this chain.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently find which segments connect to each other?

Each segment has two endpoints. If two segments share an endpoint, they are connected. This is exactly a **graph problem** where points are nodes and segments are edges.

### Breaking Down the Problem

1. **What are we looking for?** A path that visits all segment endpoints in connection order.
2. **What information do we have?** Segment endpoints that may or may not connect.
3. **What's the relationship?** Segments connect when they share an endpoint - forming a graph edge.

### Analogies

Think of this like connecting train stations. Each segment is a rail line between two stations. We want to find the route that travels through all stations, starting from a terminal (a station with only one line).

---

## Solution 1: Brute Force (O(n^2))

### Idea

For each segment, check all other segments to find connections by comparing endpoints.

### Algorithm

1. For each pair of segments, check if they share an endpoint
2. Build adjacency list of connected segments
3. Find a starting segment (one with only one connection)
4. Traverse the path, recording visited points

### Code

```python
def trace_brute_force(n, segments):
  """
  Brute force: check all pairs for connections.

  Time: O(n^2)
  Space: O(n)
  """
  def connects(seg1, seg2):
    """Check if two segments share an endpoint."""
    p1, p2 = (seg1[0], seg1[1]), (seg1[2], seg1[3])
    p3, p4 = (seg2[0], seg2[1]), (seg2[2], seg2[3])
    return p1 in (p3, p4) or p2 in (p3, p4)

  # Build adjacency list - O(n^2)
  adj = [[] for _ in range(n)]
  for i in range(n):
    for j in range(i + 1, n):
      if connects(segments[i], segments[j]):
        adj[i].append(j)
        adj[j].append(i)

  # Find starting segment (degree 1)
  start = next((i for i in range(n) if len(adj[i]) == 1), 0)

  # Traverse and build path
  path = []
  visited = [False] * n
  curr = start

  while curr != -1:
    visited[curr] = True
    x1, y1, x2, y2 = segments[curr]

    if not path:
      path.extend([(x1, y1), (x2, y2)])
    elif (x1, y1) == path[-1]:
      path.append((x2, y2))
    else:
      path.append((x1, y1))

    curr = next((nb for nb in adj[curr] if not visited[nb]), -1)

  return path
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Check all n*(n-1)/2 pairs |
| Space | O(n) | Adjacency list storage |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check every possible connection. However, for n=10^5 segments, n^2 = 10^10 operations is far too slow.

---

## Solution 2: Optimal Solution (O(n) with Hash Map)

### Key Insight

> **The Trick:** Use a hash map keyed by coordinates to find connected segments in O(1) instead of O(n).

Instead of comparing all pairs, store each point with its connected neighbors. Points appearing in multiple segments are connection points.

### Algorithm

1. Build graph: for each segment, add both endpoints as nodes and connect them
2. Find start: locate a point with exactly one neighbor (path endpoint)
3. Traverse: follow the unique unvisited neighbor at each step

### Dry Run Example

Let's trace through with segments: [(0,0,1,1), (1,1,2,0), (2,0,3,1)]

```
Step 1: Build Graph
  Process segment (0,0) - (1,1):
    graph[(0,0)] = [(1,1)]
    graph[(1,1)] = [(0,0)]

  Process segment (1,1) - (2,0):
    graph[(1,1)] = [(0,0), (2,0)]  # (1,1) now has 2 neighbors
    graph[(2,0)] = [(1,1)]

  Process segment (2,0) - (3,1):
    graph[(2,0)] = [(1,1), (3,1)]  # (2,0) now has 2 neighbors
    graph[(3,1)] = [(2,0)]

Final graph:
  (0,0) -> [(1,1)]           degree 1 <- START
  (1,1) -> [(0,0), (2,0)]    degree 2
  (2,0) -> [(1,1), (3,1)]    degree 2
  (3,1) -> [(2,0)]           degree 1 <- END

Step 2: Find Start Point
  (0,0) has degree 1 -> start = (0,0)

Step 3: Traverse
  current = (0,0), visited = {(0,0)}
  path = [(0,0)]

  neighbors of (0,0): [(1,1)]
  (1,1) not visited -> current = (1,1)
  path = [(0,0), (1,1)], visited = {(0,0), (1,1)}

  neighbors of (1,1): [(0,0), (2,0)]
  (0,0) visited, (2,0) not -> current = (2,0)
  path = [(0,0), (1,1), (2,0)], visited = {(0,0), (1,1), (2,0)}

  neighbors of (2,0): [(1,1), (3,1)]
  (1,1) visited, (3,1) not -> current = (3,1)
  path = [(0,0), (1,1), (2,0), (3,1)], visited = all

  No unvisited neighbors -> DONE

Output: [(0,0), (1,1), (2,0), (3,1)]
```

### Visual Diagram

```
Segments:
  Seg1: (0,0)-----(1,1)
  Seg2:           (1,1)-----(2,0)
  Seg3:                     (2,0)-----(3,1)

Graph representation:
  (0,0) --- (1,1) --- (2,0) --- (3,1)
    ^                             ^
  START                          END
  (degree 1)                (degree 1)

Trace path:
  (0,0) -> (1,1) -> (2,0) -> (3,1)
```

### Code (Python)

```python
def trace_segments(n, segments):
  """
  Optimal solution using hash map for O(1) lookups.

  Time: O(n) - single pass to build graph, single pass to traverse
  Space: O(n) - hash map stores 2n points (at most)
  """
  # Build graph from segments
  graph = {}

  for x1, y1, x2, y2 in segments:
    p1, p2 = (x1, y1), (x2, y2)

    if p1 not in graph:
      graph[p1] = []
    if p2 not in graph:
      graph[p2] = []

    graph[p1].append(p2)
    graph[p2].append(p1)

  # Find starting point (degree 1 vertex)
  start = None
  for point, neighbors in graph.items():
    if len(neighbors) == 1:
      start = point
      break

  if start is None:
    return []  # Cycle or empty

  # Traverse the path
  path = [start]
  visited = {start}
  current = start

  while True:
    next_point = None
    for neighbor in graph[current]:
      if neighbor not in visited:
        next_point = neighbor
        break

    if next_point is None:
      break

    path.append(next_point)
    visited.add(next_point)
    current = next_point

  return path
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Build graph in O(n), traverse in O(n) |
| Space | O(n) | Store at most 2n points in hash map |

---

## Common Mistakes

### Mistake 1: Not Handling Segment Direction

```python
# WRONG - assumes segments are always ordered
path.append((x2, y2))  # Always adds second endpoint

# CORRECT - check which endpoint connects
if (x1, y1) == path[-1]:
  path.append((x2, y2))
else:
  path.append((x1, y1))
```

**Problem:** Segments may be given in any direction.
**Fix:** Check which endpoint matches the current path end.

### Mistake 2: Using Floating Point for Coordinates

```python
# WRONG - floating point comparison issues
if abs(p1[0] - p2[0]) < 1e-9 and abs(p1[1] - p2[1]) < 1e-9:
  # Points are "equal"

# CORRECT - use integer coordinates
if p1 == p2:  # Exact integer comparison
```

**Problem:** Floating point equality is unreliable.
**Fix:** Use integer coordinates or proper tolerance handling.

### Mistake 3: Forgetting to Handle Cycles

```python
# WRONG - assumes linear path exists
start = None
for point, neighbors in graph.items():
  if len(neighbors) == 1:
    start = point
    break
# start might be None if all points have degree 2!

# CORRECT - handle cycle case
if start is None:
  start = next(iter(graph.keys()))  # Any point works for cycle
```

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| Single segment | n=1, [(0,0,1,1)] | [(0,0), (1,1)] | Only two points |
| Two connected | n=2, sharing one point | Path of 3 points | Simple chain |
| Cycle | All points degree 2 | Start anywhere | No natural endpoint |
| Collinear points | Segments on same line | Still works | Connectivity matters, not geometry |
| Large coordinates | 10^6 values | Use long long | Prevent overflow |

---

## When to Use This Pattern

### Use This Approach When:
- Segments/edges share endpoints that need matching
- Building paths through connected geometric objects
- Need O(1) lookup for coordinate matching

### Don't Use When:
- Segments can intersect at non-endpoints (use sweep line)
- Multiple disconnected paths exist (need different algorithm)
- Approximate matching needed (use spatial indexing)

### Pattern Recognition Checklist:
- [ ] Are objects connected by shared coordinates? -> **Hash map approach**
- [ ] Is it a single path/chain? -> **Find degree-1 endpoints**
- [ ] Need intersection detection? -> **Consider sweep line instead**

---

## Related Problems

### CSES Problems

| Problem | Technique |
|---------|-----------|
| [Line Segment Intersection](https://cses.fi/problemset/task/2190) | Sweep line algorithm |
| [Point in Polygon](https://cses.fi/problemset/task/2192) | Ray casting |
| [Polygon Area](https://cses.fi/problemset/task/2191) | Shoelace formula |
| [Convex Hull](https://cses.fi/problemset/task/2195) | Graham scan / Andrew's algorithm |

### LeetCode Problems

| Problem | Connection |
|---------|------------|
| [Valid Path](https://leetcode.com/problems/find-if-path-exists-in-graph/) | Graph traversal basics |
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Connected components |

---

## Key Takeaways

1. **The Core Idea:** Model geometric connectivity as a graph and use hash maps for O(1) point lookup.
2. **Time Optimization:** From O(n^2) pair checking to O(n) with hash-based adjacency.
3. **Space Trade-off:** O(n) hash map storage enables linear time traversal.
4. **Pattern:** Coordinate hashing + graph traversal for geometric path problems.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a graph from line segments using a hash map
- [ ] Identify path endpoints (degree-1 vertices)
- [ ] Trace the complete path without revisiting points
- [ ] Handle edge cases (single segment, cycles)

---

## Additional Resources

- [CP-Algorithms: Geometry Basics](https://cp-algorithms.com/geometry/basic-geometry.html)
- [CP-Algorithms: Sweep Line](https://cp-algorithms.com/geometry/sweep-line.html)
- [CSES Problem Set - Geometry](https://cses.fi/problemset/list/)
