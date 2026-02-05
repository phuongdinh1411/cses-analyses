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
| **CSES Link** | [https://cses.fi/problemset/task/2196](https://cses.fi/problemset/task/2196) |
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

Use a **sweep line** moving left to right. Track which vertical segments are "active" and count how many active verticals each horizontal segment crosses.

### Breaking Down the Problem

1. **What are we looking for?** Count of intersection points
2. **What's the relationship?** Horizontal (y=k, x in [a,b]) intersects vertical (x=c, y in [d,e]) iff a <= c <= b AND d <= k <= e

### Analogy

Think of vertical segments as "bookmarks" inserted at their x-coordinate. When processing a horizontal segment, count bookmarks whose y-range includes the horizontal's y-value.

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

> **The Trick:** Process events left-to-right. At each x: add vertical segments starting here, query for horizontal segments ending here, remove vertical segments ending here.

### Event Types

| Event | Type | Description |
|-------|------|-------------|
| Vertical Start | 0 | Add y-range to active set |
| Horizontal Query | 1 | Count active verticals at this y |
| Vertical End | 2 | Remove y-range from active set |

### Dry Run Example

```
Segments:
  H1: (0,2)-(4,2), H2: (0,1)-(3,1)
  V1: (1,0)-(1,3), V2: (2,1)-(2,4), V3: (4,0)-(4,3)

Events sorted by x:
x=1: V1 add [0,3]
x=2: V2 add [1,4]
x=3: H2 query y=1 -> V1[0,3] contains 1, V2[1,4] contains 1 -> +2
x=4: V3 add [0,3], H1 query y=2 -> V1,V2,V3 all contain 2 -> +3

Total: 5
```

### Visual Diagram

```
Y
4 |     +---V2
3 |   + | +---V3
2 |---+-+-+---H1
1 +---+-+-+---H2
0 +---V1V2V3
  0 1 2 3 4  X

Intersections: (1,2), (2,2), (4,2), (1,1), (2,1) = 5
```

### Python Solution

```python
import sys
from bisect import bisect_left, bisect_right
input = sys.stdin.readline

def main():
 n = int(input())
 events = []
 all_y = set()

 for _ in range(n):
  x1, y1, x2, y2 = map(int, input().split())
  if y1 == y2:  # Horizontal
   xmin, xmax = min(x1, x2), max(x1, x2)
   events.append((xmax, 1, y1, y1))  # Query
   all_y.add(y1)
  else:  # Vertical
   ymin, ymax = min(y1, y2), max(y1, y2)
   events.append((x1, 0, ymin, ymax))  # Add
   events.append((x1, 2, ymin, ymax))  # Remove
   all_y.add(ymin)
   all_y.add(ymax)

 ys = sorted(all_y)
 y_idx = {y: i for i, y in enumerate(ys)}
 m = len(ys)
 tree = [0] * (m + 2)

 def update(i, d):
  i += 1
  while i <= m:
   tree[i] += d
   i += i & (-i)

 def query(i):
  i += 1
  s = 0
  while i > 0:
   s += tree[i]
   i -= i & (-i)
  return s

 events.sort()
 ans = 0

 for x, t, a, b in events:
  if t == 0:  # Add vertical
   ai, bi = y_idx[a], y_idx[b]
   for yi in range(ai, bi + 1):
    update(yi, 1)
  elif t == 1:  # Query horizontal
   yi = y_idx[a]
   ans += query(yi) - (query(yi - 1) if yi > 0 else 0)
  else:  # Remove vertical
   ai, bi = y_idx[a], y_idx[b]
   for yi in range(ai, bi + 1):
    update(yi, -1)

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

# CORRECT: Compress first
tree[y_idx[y]] += 1
```

**Problem:** Cannot use 10^9 as array index.

### Mistake 3: Off-by-One in Range Query

```python
# WRONG: Excludes l
return query(r) - query(l)

# CORRECT: Includes l
return query(r) - query(l - 1)
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
