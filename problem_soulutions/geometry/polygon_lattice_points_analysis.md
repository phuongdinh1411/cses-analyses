---
layout: simple
title: "Polygon Lattice Points - Geometry Problem"
permalink: /problem_soulutions/geometry/polygon_lattice_points_analysis
difficulty: Medium
tags: [geometry, picks-theorem, gcd, shoelace-formula, lattice-points]
prerequisites: [polygon_area]
---

# Polygon Lattice Points

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Polygon Lattice Points](https://cses.fi/problemset/task/2193) |
| **Difficulty** | Medium |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Pick's Theorem + Shoelace Formula |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply Pick's theorem to count lattice points in a polygon
- [ ] Use the Shoelace formula to calculate polygon area
- [ ] Count boundary lattice points using GCD
- [ ] Understand the relationship between area, interior, and boundary points

---

## Problem Statement

**Problem:** Given a polygon with n vertices, count the number of lattice points (points with integer coordinates) that lie inside the polygon and on its boundary.

**Input:**
- Line 1: n (number of vertices)
- Lines 2 to n+1: x_i, y_i (coordinates of each vertex in order)

**Output:**
- Two integers: the number of interior lattice points and boundary lattice points

**Constraints:**
- 3 <= n <= 10^5
- -10^9 <= x_i, y_i <= 10^9

### Example

```
Input:
4
0 0
5 0
5 4
0 4

Output:
12 18
```

**Explanation:** The polygon is a 5x4 rectangle. Interior points form a 4x3 grid (12 points). Boundary has 18 lattice points: 6 on top, 6 on bottom, 3 on left side (excluding corners), 3 on right side (excluding corners).

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we count lattice points without iterating through every point in the bounding box?

The brute force approach of checking every point in the bounding box is O(Area), which is far too slow when coordinates can be up to 10^9. We need a mathematical formula that gives us the answer directly from the polygon's geometry.

### Breaking Down the Problem

1. **What are we looking for?** Interior points (I) and boundary points (B)
2. **What information do we have?** Polygon vertices in order
3. **What's the relationship?** Pick's Theorem: A = I + B/2 - 1

### The Key Insight: Pick's Theorem

Pick's Theorem relates three quantities for any simple polygon with vertices at lattice points:
- **A** = Area of the polygon
- **I** = Number of interior lattice points
- **B** = Number of boundary lattice points

**Formula:** A = I + B/2 - 1

Rearranged to find I: **I = A - B/2 + 1**

So if we can compute A and B, we can find I!

---

## Solution: Pick's Theorem Approach

### Key Components

1. **Calculate Area (A):** Use the Shoelace Formula
2. **Count Boundary Points (B):** Use GCD for each edge
3. **Find Interior Points (I):** Apply Pick's Theorem

### Part 1: Shoelace Formula for Area

For a polygon with vertices (x_1, y_1), (x_2, y_2), ..., (x_n, y_n):

```
2A = |sum of (x_i * y_{i+1} - x_{i+1} * y_i)| for i = 1 to n
```

Where indices wrap around (so after n comes 1).

### Part 2: Counting Boundary Points with GCD

For a line segment from (x_1, y_1) to (x_2, y_2), the number of lattice points on the segment (including endpoints) is:

```
gcd(|x_2 - x_1|, |y_2 - y_1|) + 1
```

For boundary counting (excluding double-counted vertices):
```
B = sum of gcd(|dx|, |dy|) for each edge
```

### Part 3: Apply Pick's Theorem

```
I = A - B/2 + 1
```

### Dry Run Example

Let's trace through with the rectangle [(0,0), (5,0), (5,4), (0,4)]:

```
Step 1: Calculate 2A using Shoelace Formula
  Edge (0,0) -> (5,0): 0*0 - 5*0 = 0
  Edge (5,0) -> (5,4): 5*4 - 5*0 = 20
  Edge (5,4) -> (0,4): 5*4 - 0*4 = 20
  Edge (0,4) -> (0,0): 0*0 - 0*4 = 0

  2A = |0 + 20 + 20 + 0| = 40
  A = 20

Step 2: Count Boundary Points (B)
  Edge (0,0) -> (5,0): gcd(5, 0) = 5
  Edge (5,0) -> (5,4): gcd(0, 4) = 4
  Edge (5,4) -> (0,4): gcd(5, 0) = 5
  Edge (0,4) -> (0,0): gcd(0, 4) = 4

  B = 5 + 4 + 5 + 4 = 18

Step 3: Apply Pick's Theorem
  I = A - B/2 + 1
  I = 20 - 18/2 + 1
  I = 20 - 9 + 1
  I = 12

Result: Interior = 12, Boundary = 18
```

### Visual Diagram

```
  0   1   2   3   4   5
4 *---*---*---*---*---*    B = boundary point
  |   .   .   .   .   |    . = interior point
3 *   .   .   .   .   *
  |   .   .   .   .   |    Boundary: 18 points
2 *   .   .   .   .   *    Interior: 12 points (4x3 grid)
  |   .   .   .   .   |
1 *   .   .   .   .   *
  |   .   .   .   .   |
0 *---*---*---*---*---*
```

### Code (Python)

```python
import sys
from math import gcd

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1

    vertices = []
    for _ in range(n):
        x = int(input_data[idx]); idx += 1
        y = int(input_data[idx]); idx += 1
        vertices.append((x, y))

    # Calculate 2*Area using Shoelace formula (keep as integer)
    area2 = 0
    for i in range(n):
        j = (i + 1) % n
        area2 += vertices[i][0] * vertices[j][1]
        area2 -= vertices[j][0] * vertices[i][1]
    area2 = abs(area2)

    # Count boundary lattice points
    boundary = 0
    for i in range(n):
        j = (i + 1) % n
        dx = abs(vertices[j][0] - vertices[i][0])
        dy = abs(vertices[j][1] - vertices[i][1])
        boundary += gcd(dx, dy)

    # Pick's theorem: A = I + B/2 - 1
    # Rearranged: I = A - B/2 + 1
    # Using 2A to avoid floating point: 2I = 2A - B + 2
    interior = (area2 - boundary + 2) // 2

    print(interior, boundary)

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log(max_coord)) | n edges, GCD is O(log) |
| Space | O(n) | Store vertex coordinates |

---

## Common Mistakes

### Mistake 1: Using Floating Point for Area

```python
# WRONG - floating point precision issues
area = abs(area2) / 2
interior = area - boundary / 2 + 1  # May have rounding errors!
```

**Problem:** Floating point arithmetic can introduce precision errors with large coordinates.
**Fix:** Keep everything as integers. Use 2*Area and multiply the formula accordingly.

```python
# CORRECT - integer arithmetic
area2 = abs(area2)  # This is 2*Area
interior = (area2 - boundary + 2) // 2
```

### Mistake 2: Wrong GCD for Boundary Points

```python
# WRONG - adding 1 for each edge
boundary += gcd(dx, dy) + 1  # Double counts vertices!
```

**Problem:** Each vertex is shared by two edges. Adding +1 counts them twice.
**Fix:** Just use gcd(dx, dy) which counts points between vertices plus one endpoint.

```python
# CORRECT
boundary += gcd(dx, dy)  # Automatically handles vertex sharing
```

### Mistake 3: Integer Overflow

**Problem:** With coordinates up to 10^9, products can reach 10^18.
**Fix:** Use `long long` for all calculations.

### Mistake 4: Forgetting Absolute Value

```python
# WRONG - area can be negative depending on vertex order
area2 = sum(...)  # May be negative if vertices are clockwise
interior = (area2 - boundary + 2) // 2  # Wrong result!
```

**Problem:** Shoelace formula gives negative area for clockwise vertices.
**Fix:** Always take absolute value of the result.

---

## Edge Cases

| Case | Input | Notes |
|------|-------|-------|
| Triangle | 3 vertices | Minimum valid polygon |
| Collinear check | Vertices may be ordered CW or CCW | Use abs() for area |
| Zero interior | Very thin polygon | Formula still works |
| Large coordinates | x, y up to 10^9 | Use long long, avoid float |
| Axis-aligned edges | dx or dy = 0 | gcd(x, 0) = x, handles correctly |

---

## When to Use This Pattern

### Use Pick's Theorem When:
- Polygon has vertices at integer coordinates
- You need to count interior or boundary lattice points
- The polygon is simple (non-self-intersecting)
- Direct enumeration would be too slow

### Don't Use When:
- Polygon has non-integer vertices
- Polygon may self-intersect
- You need the actual coordinates of lattice points

### Pattern Recognition Checklist:
- [ ] Counting lattice points in a polygon? -> **Pick's Theorem**
- [ ] Need polygon area? -> **Shoelace Formula**
- [ ] Counting points on a line segment? -> **GCD of differences**

---

## Related Problems

### CSES Problems

| Problem | Link | Relationship |
|---------|------|--------------|
| Polygon Area | [https://cses.fi/problemset/task/2191](https://cses.fi/problemset/task/2191) | Uses Shoelace formula |
| Point in Polygon | [https://cses.fi/problemset/task/2192](https://cses.fi/problemset/task/2192) | Point location |
| Point Location Test | [https://cses.fi/problemset/task/2189](https://cses.fi/problemset/task/2189) | Cross product basics |
| Line Segment Intersection | [https://cses.fi/problemset/task/2190](https://cses.fi/problemset/task/2190) | Geometry fundamentals |

### Practice Order
1. **First:** Polygon Area (master Shoelace formula)
2. **Then:** This problem (combine with GCD and Pick's theorem)
3. **After:** Point in Polygon (ray casting algorithm)

---

## Key Takeaways

1. **Pick's Theorem:** A = I + B/2 - 1 relates area, interior, and boundary points
2. **Shoelace Formula:** Computes polygon area in O(n) time
3. **GCD Insight:** Number of lattice points on segment = gcd(|dx|, |dy|) + 1
4. **Integer Arithmetic:** Avoid floating point by working with 2*Area

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive Pick's theorem formula from scratch
- [ ] Implement Shoelace formula for polygon area
- [ ] Explain why gcd gives boundary point count
- [ ] Solve this problem in under 15 minutes
- [ ] Handle edge cases without looking at notes

---

## Additional Resources

- [CP-Algorithms: Pick's Theorem](https://cp-algorithms.com/geometry/picks-theorem.html)
- [CP-Algorithms: Shoelace Formula](https://cp-algorithms.com/geometry/area-of-simple-polygon.html)
- [Wikipedia: Pick's Theorem](https://en.wikipedia.org/wiki/Pick%27s_theorem)
- [CSES Polygon Lattice Points](https://cses.fi/problemset/task/2193) - Pick's theorem application
