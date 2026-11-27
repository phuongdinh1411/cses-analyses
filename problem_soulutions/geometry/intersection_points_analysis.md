---
layout: simple
title: "Intersection Points - Geometry Problem"
permalink: /problem_soulutions/geometry/intersection_points_analysis
difficulty: Hard
tags: [sweep-line, coordinate-compression, fenwick-tree, geometry]
prerequisites: [line_segment_intersection]
---

# Intersection Points

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/1740](https://cses.fi/problemset/task/1740) |
| **Difficulty** | Hard |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Sweep Line + Fenwick Tree |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply sweep line algorithm to geometric intersection problems
- [ ] Use coordinate compression to handle large coordinate ranges
- [ ] Combine Fenwick Tree with sweep line for efficient counting
- [ ] Process geometric events in the correct order

---

## Problem Statement

**Problem:** Given n horizontal and vertical line segments, count the total number of intersection points.

**Input:**
- Line 1: n (number of segments)
- Next n lines: x1, y1, x2, y2 (endpoints of each segment)

**Output:**
- The total number of intersection points

**Constraints:**
- 1 <= n <= 10^5
- -10^9 <= x1, y1, x2, y2 <= 10^9
- Each segment is either horizontal (y1 = y2) or vertical (x1 = x2)

### Example

```
Input:
5
0 2 4 2
1 0 1 3
2 1 2 4
0 1 3 1
4 0 4 3

Output:
5
```

**Explanation:** Horizontal segment at y=2 intersects verticals at x=1,2,4. Horizontal at y=1 intersects verticals at x=1,2. Total: 5 intersections.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently count intersections without checking all O(n^2) pairs?

Use a **sweep line** moving left to right. A horizontal segment is "active" while the line is between its two x endpoints. Each vertical segment, when the line reaches it, counts the active horizontals whose y lies in its y-range.

### Breaking Down the Problem

1. **What are we looking for?** Count of intersection points
2. **What's the relationship?** Horizontal (y=k, x in [a,b]) intersects vertical (x=c, y in [d,e]) iff a <= c <= b AND d <= k <= e

### Analogy

Think of each horizontal segment as a wire stretched across the sweep line while the line is over it. A vertical segment at x is a probe: it counts how many wires currently cross the line between its bottom and top.

---

## Solution 1: Brute Force

### Idea

Check every horizontal-vertical pair for intersection.

### Code

```python
def solve_brute_force(n, segments):
  """
  Time: O(n^2), Space: O(n)
  """
  horizontal = []
  vertical = []

  for x1, y1, x2, y2 in segments:
    if y1 == y2:
      horizontal.append((min(x1, x2), max(x1, x2), y1))
    else:
      vertical.append((x1, min(y1, y2), max(y1, y2)))

  count = 0
  for hx1, hx2, hy in horizontal:
    for vx, vy1, vy2 in vertical:
      if hx1 <= vx <= hx2 and vy1 <= hy <= vy2:
        count += 1
  return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Check all pairs |
| Space | O(n) | Store segments |

---

## Solution 2: Sweep Line with Fenwick Tree (Optimal)

### Key Insight

> **The Trick:** Sweep x from left to right. A horizontal segment enters a Fenwick tree (indexed by compressed y) at its left end and leaves at its right end. A vertical segment queries the tree for the count of active y in [y1, y2].

### Event Types

| Event | Type | Description |
|-------|------|-------------|
| Horizontal start (x = left end) | 0 | Add its y to the Fenwick tree |
| Vertical (x = its x) | 1 | Count active y in [y1, y2] |
| Horizontal end (x = right end) | 2 | Remove its y |

At equal x the order is add, query, remove, so a vertical touching a horizontal's endpoint still counts.

### Dry Run Example

```
Segments:
  H1: y=2, x in [0,4]     H2: y=1, x in [0,3]
  V1: x=1, y in [0,3]     V2: x=2, y in [1,4]     V3: x=4, y in [0,3]

Events sorted by (x, type):
x=0: add H1 (y=2), add H2 (y=1)         active y = {1, 2}
x=1: V1 query [0,3] -> y=1, y=2   +2    total 2
x=2: V2 query [1,4] -> y=1, y=2   +2    total 4
x=3: remove H2 (y=1)                    active y = {2}
x=4: V3 query [0,3] -> y=2        +1    total 5
x=4: remove H1 (y=2)                    active y = {}

Total: 5
```

Intersections: (1,1), (1,2), (2,1), (2,2), (4,2).

### Python Solution

```python
import sys
from bisect import bisect_left, bisect_right


def main():
  data = sys.stdin.buffer.read().split()
  n = int(data[0])
  events = []          # (x, type, ...) with type 0 = add, 1 = query, 2 = remove
  hys = []
  for i in range(n):
    x1, y1, x2, y2 = map(int, data[1 + 4 * i: 5 + 4 * i])
    if y1 == y2:                                  # horizontal: active on [x1, x2]
      if x1 > x2:
        x1, x2 = x2, x1
      events.append((x1, 0, y1, 0))
      events.append((x2, 2, y1, 0))
      hys.append(y1)
    else:                                         # vertical: query at its x
      if y1 > y2:
        y1, y2 = y2, y1
      events.append((x1, 1, y1, y2))

  ys = sorted(set(hys))                           # compress only the y's we store
  m = len(ys)
  tree = [0] * (m + 1)

  def update(i, d):                               # Fenwick tree, 1-based inside
    i += 1
    while i <= m:
      tree[i] += d
      i += i & -i

  def prefix(i):                                  # sum of positions [0, i)
    s = 0
    while i > 0:
      s += tree[i]
      i -= i & -i
    return s

  # At equal x: add before query before remove, so touching endpoints count.
  events.sort(key=lambda e: (e[0], e[1]))
  ans = 0
  for x, t, a, b in events:
    if t == 0:
      update(bisect_left(ys, a), 1)
    elif t == 2:
      update(bisect_left(ys, a), -1)
    else:
      ans += prefix(bisect_right(ys, b)) - prefix(bisect_left(ys, a))
  print(ans)


main()
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Sort + Fenwick operations |
| Space | O(n) | Events + coordinate map |

---

## Common Mistakes

### Mistake 1: Wrong Event Order

```python
# WRONG: Remove before query at same x
events.sort(key=lambda e: (e[0], -e[1]))

# CORRECT: Add(0) < Query(1) < Remove(2)
events.sort(key=lambda e: (e[0], e[1]))
```

**Problem:** Processing removes before queries misses valid intersections.

### Mistake 2: No Coordinate Compression

```python
# WRONG: y can be 10^9
tree[y] += 1

# CORRECT: Compress first (ys = sorted distinct y of horizontals)
update(bisect_left(ys, y), 1)
```

**Problem:** Cannot use 10^9 as array index.

### Mistake 3: Off-by-One in Range Query

```python
# WRONG: bisect_right on the low end drops horizontals exactly at y1
prefix(bisect_right(ys, y2)) - prefix(bisect_right(ys, y1))

# CORRECT: prefix(i) sums positions [0, i), so take [first >= y1, first > y2)
prefix(bisect_right(ys, y2)) - prefix(bisect_left(ys, y1))
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Single horizontal | 1 segment | 0 | No vertical to intersect |
| Single vertical | 1 segment | 0 | No horizontal to intersect |
| All parallel | Same orientation | 0 | Parallel don't intersect |
| Large coordinates | 10^9 range | Correct | Needs compression |
| Same endpoint | Segments share point | 1 | Valid intersection |

---

## When to Use This Pattern

### Use Sweep Line + Fenwick When:
- Counting intersections between axis-aligned segments
- Need O(n log n) complexity
- Segments are horizontal/vertical only

### Don't Use When:
- Arbitrary segment orientations (use Bentley-Ottmann)
- Need actual intersection coordinates
- Very sparse input (brute force may suffice)

### Pattern Recognition Checklist:
- [ ] Horizontal and vertical only? -> Sweep line works
- [ ] Large coordinates? -> Use compression
- [ ] n > 10^4? -> Avoid O(n^2)

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Line Segment Intersection](https://cses.fi/problemset/task/2190) | Check if two segments intersect |
| [Point Location Test](https://cses.fi/problemset/task/2189) | Point position relative to line |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Polygon Area](https://cses.fi/problemset/task/2191) | Sweep for area calculation |
| [Point in Polygon](https://cses.fi/problemset/task/2192) | Ray casting technique |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Convex Hull](https://cses.fi/problemset/task/2195) | Graham scan algorithm |

---

## Key Takeaways

1. **Core Idea:** Sweep line converts 2D geometry to 1D event processing
2. **Optimization:** O(n^2) to O(n log n) with Fenwick Tree
3. **Critical Detail:** Event ordering (add < query < remove)
4. **Pattern:** Event-based sweep line with range query structure

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain sweep line for intersection counting
- [ ] Implement coordinate compression
- [ ] Write Fenwick tree operations
- [ ] Handle event ordering correctly
- [ ] Identify when sweep line applies

---

## Additional Resources

- [CP-Algorithms: Sweep Line](https://cp-algorithms.com/geometry/sweep-line.html)
- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
- [CSES Line Segment Intersection](https://cses.fi/problemset/task/2190) - Related line intersection problem
