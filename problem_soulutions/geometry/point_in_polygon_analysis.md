---
layout: simple
title: "Point in Polygon - Geometry Problem"
permalink: /problem_soulutions/geometry/point_in_polygon_analysis
difficulty: Medium
tags: [geometry, ray-casting, cross-product, computational-geometry]
---

# Point in Polygon

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Point in Polygon](https://cses.fi/problemset/task/2192) |
| **Difficulty** | Medium |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Ray Casting Algorithm |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the ray casting algorithm for point-in-polygon testing
- [ ] Use cross products to determine point position relative to a line
- [ ] Handle boundary cases (point on edge, point on vertex)
- [ ] Apply computational geometry techniques to containment problems

---

## Problem Statement

**Problem:** Given a polygon with n vertices and m query points, determine whether each point is inside, outside, or on the boundary of the polygon.

**Input:**
- Line 1: Two integers n and m (number of vertices, number of queries)
- Next n lines: Vertices (x, y) of the polygon in order
- Next m lines: Query points (x, y)

**Output:**
- For each query point: "INSIDE", "OUTSIDE", or "BOUNDARY"

**Constraints:**
- 3 <= n, m <= 1000
- -10^9 <= x, y <= 10^9
- All coordinates are integers

### Example

```
Input:
4 3
0 0
4 0
4 4
0 4
2 2
0 2
5 5

Output:
INSIDE
BOUNDARY
OUTSIDE
```

**Explanation:**
- Point (2,2) is inside the square
- Point (0,2) lies on the left edge
- Point (5,5) is outside the polygon

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we determine if a point is inside a polygon without checking infinitely many interior points?

The key insight is the **Ray Casting Algorithm**: cast a ray from the point to infinity and count how many polygon edges it crosses. An odd count means inside, even means outside.

### Breaking Down the Problem

1. **What are we looking for?** Classification of each point as INSIDE/OUTSIDE/BOUNDARY
2. **What information do we have?** Polygon vertices in order, query point coordinates
3. **What's the relationship?** A point inside a closed polygon will have the ray cross an odd number of edges

### Analogies

Think of this like escaping a fenced area. If you walk in a straight line from your position, you cross the fence an odd number of times if you started inside, and an even number if you started outside.

---

## Solution: Ray Casting Algorithm

### Key Insight

> **The Trick:** Cast a horizontal ray to the right from the query point. Count edge crossings. Odd = inside, Even = outside. First, check if the point lies exactly on any edge.

### Algorithm

1. **Check boundary first:** For each edge, check if the point lies on the edge
2. **Cast ray:** Imagine a horizontal ray going right from the point
3. **Count crossings:** Count how many polygon edges the ray intersects
4. **Determine result:** Odd crossings = INSIDE, Even crossings = OUTSIDE

### Dry Run Example

Let's trace through with polygon `[(0,0), (4,0), (4,4), (0,4)]` and point `(2,2)`:

```
Polygon (square):
    (0,4)-----(4,4)
      |         |
      |  (2,2)  |   <-- query point
      |    -----|-------> ray to infinity
      |         |
    (0,0)-----(4,0)

Step 1: Check if (2,2) is on any edge
  - Edge (0,0)-(4,0): y=0, point y=2, NOT on edge
  - Edge (4,0)-(4,4): x=4, point x=2, NOT on edge
  - Edge (4,4)-(0,4): y=4, point y=2, NOT on edge
  - Edge (0,4)-(0,0): x=0, point x=2, NOT on edge
  Result: Not on boundary

Step 2: Cast ray from (2,2) going right (y=2)
  - Edge (0,0)-(4,0): y range [0,0], ray y=2 not in range, NO crossing
  - Edge (4,0)-(4,4): y range [0,4], ray y=2 in range
    - Intersection x = 4, point x = 2, ray crosses at x=4, YES crossing
  - Edge (4,4)-(0,4): y range [4,4], ray y=2 not in range, NO crossing
  - Edge (0,4)-(0,0): y range [0,4], ray y=2 in range
    - Intersection x = 0, point x = 2, ray does NOT cross (0 < 2)

Step 3: Count = 1 (odd)
  Result: INSIDE
```

### Visual Diagram

```
   y
   ^
 4 +-------+
   |       |
   | * --> | -->  (ray crosses 1 edge)
   |       |
 0 +-------+---> x
   0       4

   * = query point (2,2)
   --> = ray direction
   Count = 1 (odd) -> INSIDE
```

### Code (Python)

```python
import sys
input = sys.stdin.readline

def cross_product(o, a, b):
  """Calculate (a - o) x (b - o). Positive if counter-clockwise."""
  return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def on_segment(p, a, b):
  """Check if point p lies on segment ab."""
  # Point must be collinear with segment
  if cross_product(a, b, p) != 0:
    return False
  # Point must be within bounding box
  return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
      min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))

def point_in_polygon(polygon, point):
  """
  Determine if point is inside, outside, or on boundary of polygon.
  Uses ray casting algorithm.

  Time: O(n) per query
  Space: O(1)
  """
  n = len(polygon)
  px, py = point

  # Check if point is on any edge
  for i in range(n):
    a = polygon[i]
    b = polygon[(i + 1) % n]
    if on_segment(point, a, b):
      return "BOUNDARY"

  # Ray casting: count crossings to the right
  crossings = 0
  for i in range(n):
    x1, y1 = polygon[i]
    x2, y2 = polygon[(i + 1) % n]

    # Ensure y1 <= y2 for consistent handling
    if y1 > y2:
      x1, y1, x2, y2 = x2, y2, x1, y1

    # Check if ray at height py intersects this edge
    # Use half-open interval [y1, y2) to avoid double-counting vertices
    if y1 <= py < y2:
      # Calculate x-coordinate of intersection
      # x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
      # Check if intersection is to the right of point
      # Rearranged to avoid division: (px - x1) * (y2 - y1) < (py - y1) * (x2 - x1)
      if (x2 - x1) * (py - y1) > (px - x1) * (y2 - y1):
        crossings += 1

  return "INSIDE" if crossings % 2 == 1 else "OUTSIDE"

def solve():
  n, m = map(int, input().split())
  polygon = [tuple(map(int, input().split())) for _ in range(n)]

  results = []
  for _ in range(m):
    point = tuple(map(int, input().split()))
    results.append(point_in_polygon(polygon, point))

  print('\n'.join(results))

if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * m) | O(n) per query, m queries |
| Space | O(n) | Store polygon vertices |

---

## Common Mistakes

### Mistake 1: Using Floating Point Division

```python
# WRONG - floating point precision issues
x_intersect = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
if px < x_intersect:
  crossings += 1
```

**Problem:** Floating point errors can cause incorrect results near edges.
**Fix:** Rearrange to use integer multiplication only:
```python
# CORRECT - integer arithmetic
if (x2 - x1) * (py - y1) > (px - x1) * (y2 - y1):
  crossings += 1
```

### Mistake 2: Double-Counting Vertices

```python
# WRONG - counts vertex twice when ray passes through it
if y1 <= py <= y2:  # Closed interval
  # ...
```

**Problem:** When the ray passes exactly through a vertex, both adjacent edges count it.
**Fix:** Use half-open interval `[y1, y2)`:
```python
# CORRECT - vertex counted only once
if y1 <= py < y2:  # Half-open interval
  # ...
```

### Mistake 3: Forgetting Boundary Check

```python
# WRONG - jumps straight to ray casting
crossings = 0
for i in range(n):
  # ray casting logic...
return "INSIDE" if crossings % 2 == 1 else "OUTSIDE"
```

**Problem:** Points on the boundary are classified as INSIDE or OUTSIDE.
**Fix:** Always check boundary first before ray casting.

---

## Edge Cases

| Case | Example | Expected | Why |
|------|---------|----------|-----|
| Point on vertex | Point = (0,0), vertex at (0,0) | BOUNDARY | Vertex is part of boundary |
| Point on edge | Point on line between vertices | BOUNDARY | Edge is part of boundary |
| Ray through vertex | Ray exactly hits a vertex | Correct count | Half-open interval handles this |
| Horizontal edge | Edge at same y as point | Correct count | Handle horizontal edges specially |
| Concave polygon | Non-convex shape | Works correctly | Ray casting works for any simple polygon |
| Large coordinates | 10^9 values | Works | Use long long to avoid overflow |

---

## When to Use This Pattern

### Use Ray Casting When:
- You need to test point containment in any simple polygon (convex or concave)
- You have multiple query points for the same polygon
- The polygon is defined by vertices in order

### Don't Use When:
- The polygon is convex (use cross product method - faster constant factor)
- You need to handle polygons with holes (need modified algorithm)
- You have very many queries (consider preprocessing with spatial data structures)

### Pattern Recognition Checklist:
- [ ] Need to determine if point is inside/outside a polygon? **Ray Casting**
- [ ] Polygon is convex? **Consider cross product method for all edges**
- [ ] Many queries on same polygon? **Still O(n) per query, but could preprocess**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Line Segment Intersection](https://cses.fi/problemset/task/2190) | Understand segment intersection basics |
| [Point Location Test](https://cses.fi/problemset/task/2189) | Learn cross product for left/right test |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Polygon Area](https://cses.fi/problemset/task/2191) | Uses cross products, similar polygon traversal |
| [Convex Hull](https://cses.fi/problemset/task/2195) | Related geometry concepts |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Polygon Lattice Points](https://cses.fi/problemset/task/2193) | Pick's theorem, boundary counting |
| [Minimum Euclidean Distance](https://cses.fi/problemset/task/2194) | Divide and conquer geometry |

---

## Key Takeaways

1. **The Core Idea:** Cast a ray and count edge crossings - odd means inside, even means outside
2. **Boundary Check:** Always check if point is on the boundary first
3. **Integer Arithmetic:** Avoid floating point by rearranging comparisons to use multiplication
4. **Half-Open Intervals:** Use `[y1, y2)` to avoid double-counting vertices

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why odd crossings means the point is inside
- [ ] Handle the boundary case correctly
- [ ] Avoid floating point arithmetic
- [ ] Explain how to handle the ray passing through a vertex
- [ ] Implement the solution in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Point in Polygon](https://cp-algorithms.com/geometry/point-in-polygon.html)
- [Wikipedia: Point in Polygon](https://en.wikipedia.org/wiki/Point_in_polygon)
- [CSES Geometry Problem Set](https://cses.fi/problemset/list/)
