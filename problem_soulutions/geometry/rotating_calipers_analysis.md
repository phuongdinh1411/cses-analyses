---
layout: simple
title: "Rotating Calipers - Computational Geometry Technique"
permalink: /problem_soulutions/geometry/rotating_calipers_analysis
difficulty: Hard
tags: [geometry, convex-hull, rotating-calipers, antipodal-pairs]
prerequisites: [convex_hull]
---

# Rotating Calipers

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Computational Geometry |
| **Time Complexity** | O(n) after convex hull |
| **Key Technique** | Two-Pointer on Convex Hull |

### Learning Goals

After studying this technique, you will be able to:
- [ ] Understand antipodal pairs and their properties on convex hulls
- [ ] Implement rotating calipers to find the diameter of a point set
- [ ] Calculate the minimum enclosing rectangle of a convex polygon
- [ ] Apply cross product to maintain the antipodal property efficiently

---

## Concept Explanation

### What is Rotating Calipers?

**The Technique:** Rotating Calipers is an algorithm that maintains a pair of parallel lines (like calipers) tangent to a convex polygon, rotating them around the polygon to solve various geometric problems in linear time.

**Core Problems Solved:**
- **Diameter:** Maximum distance between any two points
- **Width:** Minimum distance between parallel supporting lines
- **Minimum Area Rectangle:** Smallest rectangle enclosing all points

### Antipodal Pairs

Two vertices of a convex polygon are **antipodal** if there exist two parallel lines, each passing through one vertex, such that the polygon lies entirely between them.

```
        Line 1 ───────────●───────────
                         /A\
                        /   \
                       /     \
                      /       \
                     ●─────────●
                    /           \
                   /             \
        Line 2 ──●───────────────●──
                 B

        A and B are antipodal - parallel lines through them
        sandwich the entire polygon
```

---

## Intuition: Two Parallel Lines Visualization

### The Caliper Analogy

Imagine holding a physical caliper (the measuring tool with two parallel jaws):

1. **Place the caliper** around the convex hull with jaws touching two vertices
2. **Rotate the caliper** around the polygon, keeping both jaws in contact
3. **As you rotate**, one jaw stays fixed while the other advances along edges
4. **Track measurements** during the rotation to find diameter, width, etc.

### Visual: Complete Rotation

```
Step 1:          Step 2:          Step 3:          Step 4:
  ═══●═══          ═══●═══                           ═══●═══
     │\               │\            ╲│               ╱│
     │ \              │ \            │╲             ╱ │
     │  ●             │  ●           │ ●           ●  │
     │ /              │ /            │╱             ╲ │
     │/               │/            ╱│               ╲│
  ═══●═══          ═══●═══       ═══●═══          ═══●═══

Calipers rotate 180 degrees, visiting all antipodal pairs
```

### Key Insight

> **The Trick:** The "opposite" vertex (the one furthest from a given edge) changes monotonically as we traverse the hull. We never need to backtrack.

---

## Algorithm: Finding Diameter

### Step-by-Step Process

1. **Build Convex Hull** of input points (O(n log n))
2. **Initialize**: Start with vertices 0 and the vertex furthest from edge (0,1)
3. **Rotate**: For each edge, advance the opposite pointer while it increases distance
4. **Track Maximum**: Update diameter whenever we find a larger distance

### Dry Run Example

**Input Points:** (0,0), (4,0), (4,3), (2,5), (0,3)

**Convex Hull (CCW):** P0(0,0), P1(4,0), P2(4,3), P3(2,5), P4(0,3)

```
Step 0: Initialize
        Hull vertices: P0(0,0) -> P1(4,0) -> P2(4,3) -> P3(2,5) -> P4(0,3)

             P3(2,5)
              /\
             /  \
        P4(0,3)  P2(4,3)
            |    |
            |    |
        P0(0,0)--P1(4,0)

Step 1: Edge P0-P1 (bottom edge)
        Find furthest vertex from this edge
        Cross products:
          cross(P0P1, P0P2) = (4,0) x (4,3) = 12
          cross(P0P1, P0P3) = (4,0) x (2,5) = 20  <- maximum
          cross(P0P1, P0P4) = (4,0) x (0,3) = 12
        Antipodal vertex: P3
        Distance P0-P3 = sqrt(4+25) = sqrt(29)
        Distance P1-P3 = sqrt(4+25) = sqrt(29)
        max_dist = sqrt(29) ~ 5.39

Step 2: Edge P1-P2 (right edge)
        Current antipodal: P3
        Check if P4 gives larger cross product:
          cross(P1P2, P1P3) = (0,3) x (-2,5) = 0*5 - 3*(-2) = 6
          cross(P1P2, P1P4) = (0,3) x (-4,3) = 0*3 - 3*(-4) = 12
        Advance to P4
        Distance P1-P4 = sqrt(16+9) = 5
        Distance P2-P4 = sqrt(16+0) = 4
        max_dist = sqrt(29) (unchanged)

Step 3: Edge P2-P3 (top-right edge)
        Current antipodal: P4
        Check if P0 gives larger cross product:
          cross(P2P3, P2P4) = (-2,2) x (-4,0) = 8
          cross(P2P3, P2P0) = (-2,2) x (-4,-3) = 6+8 = 14
        Advance to P0
        Distance P2-P0 = sqrt(16+9) = 5
        Distance P3-P0 = sqrt(4+25) = sqrt(29)
        max_dist = sqrt(29) (unchanged)

Step 4: Edge P3-P4 (top-left edge)
        Current antipodal: P0
        Check if P1 gives larger cross product:
          cross(P3P4, P3P0) = (-2,-2) x (-2,-5) = 10-4 = 6
          cross(P3P4, P3P1) = (-2,-2) x (2,-5) = 10+4 = 14
        Advance to P1
        Distance P3-P1 = sqrt(4+25) = sqrt(29)
        Distance P4-P1 = sqrt(16+9) = 5
        max_dist = sqrt(29) (unchanged)

Step 5: Edge P4-P0 (left edge)
        Current antipodal: P1
        Check if P2 gives larger cross product:
          cross(P4P0, P4P1) = (0,-3) x (4,-3) = 12
          cross(P4P0, P4P2) = (0,-3) x (4,0) = 0
        Stay at P1
        Already computed distances

Final Result: Diameter = sqrt(29) ~ 5.39
Antipodal pairs achieving diameter: (P0,P3), (P1,P3), (P3,P1)
```

---

## Code Implementation

### Python Solution

```python
import math
from typing import List, Tuple

Point = Tuple[float, float]

def cross(o: Point, a: Point, b: Point) -> float:
  """Cross product of vectors OA and OB."""
  return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def dist_sq(a: Point, b: Point) -> float:
  """Squared distance between two points."""
  return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def convex_hull(points: List[Point]) -> List[Point]:
  """Andrew's monotone chain algorithm. Returns CCW hull."""
  points = sorted(set(points))
  if len(points) <= 1:
    return points

  # Build lower hull
  lower = []
  for p in points:
    while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
      lower.pop()
    lower.append(p)

  # Build upper hull
  upper = []
  for p in reversed(points):
    while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
      upper.pop()
    upper.append(p)

  return lower[:-1] + upper[:-1]

def rotating_calipers_diameter(points: List[Point]) -> float:
  """
  Find diameter (maximum distance between any two points).

  Time: O(n log n) for hull, O(n) for calipers
  Space: O(n) for hull storage
  """
  hull = convex_hull(points)
  n = len(hull)

  if n == 1:
    return 0
  if n == 2:
    return math.sqrt(dist_sq(hull[0], hull[1]))

  # Find initial antipodal vertex (furthest from edge 0-1)
  j = 1
  while cross(hull[0], hull[1], hull[(j + 1) % n]) > \
    cross(hull[0], hull[1], hull[j]):
    j = (j + 1) % n

  max_dist_sq = 0

  # Rotate through all edges
  for i in range(n):
    # Check distance from current edge endpoints to antipodal vertex
    max_dist_sq = max(max_dist_sq, dist_sq(hull[i], hull[j]))
    max_dist_sq = max(max_dist_sq, dist_sq(hull[(i + 1) % n], hull[j]))

    # Advance j while it gives larger cross product (further from edge)
    next_i = (i + 1) % n
    next_next_i = (i + 2) % n
    while cross(hull[next_i], hull[next_next_i], hull[(j + 1) % n]) > \
      cross(hull[next_i], hull[next_next_i], hull[j]):
      j = (j + 1) % n
      max_dist_sq = max(max_dist_sq, dist_sq(hull[i], hull[j]))
      max_dist_sq = max(max_dist_sq, dist_sq(hull[next_i], hull[j]))

  return math.sqrt(max_dist_sq)

def rotating_calipers_width(points: List[Point]) -> float:
  """
  Find width (minimum distance between parallel supporting lines).

  Time: O(n log n) for hull, O(n) for calipers
  """
  hull = convex_hull(points)
  n = len(hull)

  if n <= 2:
    return 0

  j = 1
  min_width = float('inf')

  for i in range(n):
    next_i = (i + 1) % n

    # Advance j to furthest point from edge i -> next_i
    while True:
      curr_cross = abs(cross(hull[i], hull[next_i], hull[j]))
      next_cross = abs(cross(hull[i], hull[next_i], hull[(j + 1) % n]))
      if next_cross > curr_cross:
        j = (j + 1) % n
      else:
        break

    # Width = perpendicular distance from j to edge (i, next_i)
    edge_len = math.sqrt(dist_sq(hull[i], hull[next_i]))
    if edge_len > 0:
      height = abs(cross(hull[i], hull[next_i], hull[j])) / edge_len
      min_width = min(min_width, height)

  return min_width
```

#---

## Common Mistakes

### Mistake 1: Not Maintaining Antipodal Property

```python
# WRONG: Checking all vertices for each edge
for i in range(n):
  for j in range(n):  # O(n^2) - defeats the purpose!
    max_dist = max(max_dist, dist(hull[i], hull[j]))
```

**Problem:** This is O(n^2), not using the monotonic property.
**Fix:** Maintain a single pointer `j` that only advances, never backtracks.

### Mistake 2: Incorrect Cross Product Sign Check

```python
# WRONG: Using >= instead of >
while cross(hull[i], hull[ni], hull[(j+1)%n]) >= cross(hull[i], hull[ni], hull[j]):
  j = (j + 1) % n  # May loop forever on collinear points!
```

**Problem:** When points are collinear, `>=` causes infinite loop.
**Fix:** Use strict `>` and handle collinear cases separately.

### Mistake 3: Forgetting to Check Both Edge Endpoints

```python
# WRONG: Only checking one endpoint
max_dist = max(max_dist, dist_sq(hull[i], hull[j]))
# Missing: dist_sq(hull[(i+1)%n], hull[j])
```

**Problem:** Diameter might be between non-adjacent vertices.
**Fix:** Check distances from both endpoints of the current edge to the antipodal vertex.

---

## Edge Cases

| Case | Input | Handling | Notes |
|------|-------|----------|-------|
| Single point | n = 1 | Return 0 | No distance to measure |
| Two points | n = 2 | Return distance | Direct calculation |
| Collinear points | All on line | Hull has 2 points | Falls back to two-point case |
| Regular polygon | n-gon | Normal rotation | Multiple pairs with same diameter |
| Very large coordinates | 10^9 | Use long long | Avoid overflow in cross/dist |
| Degenerate hull | Repeated points | Deduplicate first | Pre-process input |

---

## When to Use Rotating Calipers

### Use This Technique When:

| Problem Type | Application |
|--------------|-------------|
| **Furthest Pair** | Find maximum distance between any two points |
| **Width Calculation** | Find minimum distance between parallel tangents |
| **Minimum Rectangle** | Find smallest area/perimeter enclosing rectangle |
| **Bridge Finding** | Find edges connecting two separate convex hulls |

### Problem Recognition Checklist:
- [ ] Need to find extremal distances on a point set? **Consider rotating calipers**
- [ ] Working with convex hull and need O(n) complexity? **Rotating calipers**
- [ ] Finding minimum enclosing shapes? **Rotating calipers + extensions**

### Do Not Use When:
- Points are not on a convex hull boundary (find hull first)
- Need exact rectangle alignment with axes (simpler methods exist)
- Working with non-convex polygons (different algorithms needed)

---

## Applications

### 1. Diameter (Furthest Pair)
- **Use:** Maximum distance between any two points
- **Complexity:** O(n log n) total

### 2. Width (Minimum Strip)
- **Use:** Narrowest strip containing all points
- **Application:** Manufacturing, packing problems

### 3. Minimum Area Rectangle
- **Use:** Smallest rectangle enclosing all points
- **Property:** One edge of optimal rectangle lies on hull edge

### 4. Minimum Perimeter Rectangle
- **Use:** Rectangle with smallest perimeter enclosing points
- **Similar to:** Area variant but optimizes different metric

### 5. Onion Peeling
- **Use:** Repeatedly find and remove convex hull layers
- **Application:** Statistical depth, outlier detection

---

## Related CSES Problems

| Problem | Relationship | Key Concept |
|---------|--------------|-------------|
| [Convex Hull](https://cses.fi/problemset/task/2195) | **Prerequisite** | Must build hull before rotating calipers |
| [Point in Polygon](https://cses.fi/problemset/task/2192) | Related | Uses similar cross product techniques |
| [Polygon Area](https://cses.fi/problemset/task/2191) | Related | Cross product for area calculation |
| [Minimum Euclidean Distance](https://cses.fi/problemset/task/2194) | Alternative | Different approach (divide and conquer) |

---

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Convex Hull | O(n log n) | O(n) |
| Rotating Calipers | O(n) | O(1) |
| **Total** | **O(n log n)** | **O(n)** |

**Why O(n) for Calipers?**
- Each vertex is visited at most twice (once as edge endpoint, once as antipodal)
- The antipodal pointer `j` only advances, never backtracks
- Total pointer movements bounded by 2n

---

## Key Takeaways

1. **Core Idea:** Maintain parallel supporting lines that rotate around the convex hull
2. **Efficiency:** Exploits monotonic movement of antipodal vertex along hull
3. **Versatility:** Single framework solves diameter, width, and rectangle problems
4. **Prerequisite:** Always requires convex hull as input

---

## Practice Checklist

Before moving on, verify you can:
- [ ] Build convex hull using Andrew's monotone chain algorithm
- [ ] Implement rotating calipers to find diameter
- [ ] Explain why antipodal vertex moves monotonically
- [ ] Handle edge cases (collinear points, small inputs)
- [ ] Extend to minimum enclosing rectangle if needed
