---
layout: simple
title: "Polygon Area - Geometry Problem"
permalink: /problem_soulutions/geometry/polygon_area_analysis
difficulty: Easy
tags: [geometry, shoelace-formula, cross-product, polygon]
---

# Polygon Area

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Polygon Area](https://cses.fi/problemset/task/2191) |
| **Difficulty** | Easy |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Shoelace Formula |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and apply the Shoelace formula for polygon area calculation
- [ ] Handle signed area to determine polygon orientation (clockwise vs counter-clockwise)
- [ ] Implement efficient O(n) polygon area computation
- [ ] Work with integer arithmetic to avoid floating-point precision issues

---

## Problem Statement

**Problem:** Given a polygon with n vertices, calculate its area. The polygon is simple (no self-intersections) and vertices are given in order (either clockwise or counter-clockwise).

**Input:**
- Line 1: Integer n - number of vertices
- Lines 2 to n+1: Two integers x and y - coordinates of each vertex

**Output:**
- A single integer: twice the area of the polygon (to avoid fractions)

**Constraints:**
- 3 <= n <= 1000
- -10^9 <= x, y <= 10^9

### Example

```
Input:
4
0 0
5 0
5 3
0 3

Output:
30
```

**Explanation:** The polygon is a rectangle with width 5 and height 3. Area = 5 x 3 = 15. Output is 2 x 15 = 30 (twice the area).

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we calculate the area of an arbitrary polygon without decomposing it into simpler shapes?

The Shoelace formula (also known as the Surveyor's formula) lets us compute the area directly from vertex coordinates using a simple summation pattern.

### Breaking Down the Problem

1. **What are we looking for?** The area enclosed by the polygon.
2. **What information do we have?** Ordered list of vertex coordinates.
3. **What's the relationship between input and output?** The area is related to the cross products of consecutive edge vectors.

### The Shoelace Intuition

Imagine drawing the polygon on graph paper. The Shoelace formula works by:
1. For each edge, compute the signed area of the trapezoid formed between that edge and the x-axis
2. Sum all these signed areas - overlapping parts cancel out automatically
3. The result is the signed area (positive for counter-clockwise, negative for clockwise)

```
         (x2,y2)
           /\
          /  \
         /    \
(x1,y1) /______\ (x3,y3)
        --------
         x-axis

Each edge contributes: (x_i * y_{i+1} - x_{i+1} * y_i) / 2
```

---

## Solution 1: Brute Force (Triangle Decomposition)

### Idea

Decompose the polygon into triangles from a fixed vertex, then sum all triangle areas.

### Algorithm

1. Pick vertex 0 as the pivot
2. For each consecutive pair of vertices (i, i+1), form a triangle with vertex 0
3. Calculate each triangle's area using the cross product
4. Sum all areas

### Code

```python
def polygon_area_triangles(vertices):
    """
    Calculate polygon area by triangle decomposition.

    Time: O(n)
    Space: O(1)
    """
    n = len(vertices)
    if n < 3:
        return 0

    total = 0
    x0, y0 = vertices[0]

    for i in range(1, n - 1):
        x1, y1 = vertices[i]
        x2, y2 = vertices[i + 1]
        # Cross product gives twice the signed area
        cross = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        total += cross

    return abs(total)  # Return twice the area
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through vertices |
| Space | O(1) | Only storing running sum |

### Why This Works

Each triangle from the pivot contributes a signed area. When summed, the areas correctly account for the polygon's total area, with signs handling convex and concave regions.

---

## Solution 2: Shoelace Formula (Optimal)

### Key Insight

> **The Trick:** Sum cross products of consecutive vertices in a cyclic manner. The formula handles any simple polygon regardless of convexity.

### The Formula

```
2 * Area = |sum of (x_i * y_{i+1} - x_{i+1} * y_i)| for i = 0 to n-1
```

Where indices wrap around: vertex n is vertex 0.

### Algorithm

1. Initialize sum to 0
2. For each vertex i from 0 to n-1:
   - Add: x[i] * y[i+1] - x[i+1] * y[i]
3. Return absolute value of sum (this is 2 times the area)

### Dry Run Example

Let's trace through with a rectangle: vertices = [(0,0), (5,0), (5,3), (0,3)]

```
Initial: sum = 0

i=0: (0,0) to (5,0)
  sum += 0*0 - 5*0 = 0
  sum = 0

i=1: (5,0) to (5,3)
  sum += 5*3 - 5*0 = 15
  sum = 15

i=2: (5,3) to (0,3)
  sum += 5*3 - 0*3 = 15
  sum = 30

i=3: (0,3) to (0,0)  [wraps to start]
  sum += 0*0 - 0*3 = 0
  sum = 30

Result: |30| = 30 (which is 2 * area = 2 * 15)
```

### Visual Diagram

```
    (0,3) -------- (5,3)
      |              |
      |   Area=15    |
      |              |
    (0,0) -------- (5,0)

Shoelace pattern:
  x0*y1 - x1*y0 = 0*0 - 5*0 = 0
  x1*y2 - x2*y1 = 5*3 - 5*0 = 15
  x2*y3 - x3*y2 = 5*3 - 0*3 = 15
  x3*y0 - x0*y3 = 0*0 - 0*3 = 0
                            ----
                  Total:     30 = 2 * Area
```

### Code (Python)

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    vertices = []
    for _ in range(n):
        x, y = map(int, input().split())
        vertices.append((x, y))

    # Shoelace formula
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]

    print(abs(area))

solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<pair<long long, long long>> v(n);
    for (int i = 0; i < n; i++) {
        cin >> v[i].first >> v[i].second;
    }

    // Shoelace formula
    long long area = 0;
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        area += v[i].first * v[j].second;
        area -= v[j].first * v[i].second;
    }

    cout << abs(area) << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through n vertices |
| Space | O(n) | Store vertex coordinates |

---

## Common Mistakes

### Mistake 1: Integer Overflow

```cpp
// WRONG - may overflow with int
int area = 0;
area += v[i].first * v[j].second;

// CORRECT - use long long
long long area = 0;
area += v[i].first * v[j].second;
```

**Problem:** With coordinates up to 10^9, the product can reach 10^18, exceeding int range.
**Fix:** Always use `long long` in C++ or Python's unlimited integers.

### Mistake 2: Forgetting to Wrap Around

```python
# WRONG - misses last edge
for i in range(n - 1):
    area += x[i] * y[i+1] - x[i+1] * y[i]

# CORRECT - includes edge from last to first vertex
for i in range(n):
    j = (i + 1) % n
    area += x[i] * y[j] - x[j] * y[i]
```

**Problem:** The polygon is closed; we need the edge from the last vertex back to the first.
**Fix:** Use modulo to wrap the index: `j = (i + 1) % n`.

### Mistake 3: Not Taking Absolute Value

```python
# WRONG - clockwise polygons give negative area
return area // 2

# CORRECT - handle both orientations
return abs(area) // 2
```

**Problem:** Clockwise vertices produce negative signed area.
**Fix:** Take absolute value before final output.

### Mistake 4: Dividing When Output Should Be 2x Area

```python
# WRONG - problem asks for 2 * area
print(abs(area) // 2)

# CORRECT - CSES wants twice the area
print(abs(area))
```

**Problem:** CSES outputs 2 times the area to avoid fractions.
**Fix:** Read the problem carefully; don't divide by 2.

---

## Edge Cases

| Case | Input Example | Output | Why |
|------|---------------|--------|-----|
| Triangle | 3 vertices | Valid area | Minimum valid polygon |
| Collinear points | All on one line | 0 | Degenerate polygon |
| Clockwise order | CW vertices | Same as CCW | Absolute value handles both |
| Large coordinates | 10^9 range | Use long long | Prevent overflow |
| Concave polygon | Star shape | Correct area | Shoelace handles concavity |

---

## When to Use This Pattern

### Use Shoelace Formula When:
- Computing area of a simple polygon given vertex coordinates
- You need an O(n) solution
- The polygon has no self-intersections
- You want to avoid floating-point issues (use integer arithmetic)

### Don't Use When:
- Polygon has self-intersections (need more complex algorithms)
- You only have edge lengths, not coordinates (use Heron's formula for triangles)
- Computing area of a region bounded by curves (need calculus/numerical methods)

### Pattern Recognition Checklist:
- [ ] Polygon with ordered vertices? --> **Shoelace formula**
- [ ] Need signed area (orientation)? --> **Don't take absolute value**
- [ ] Computing centroids? --> **Extended Shoelace with weighted sums**
- [ ] Lattice points on boundary? --> **Combine with Pick's theorem**

---

## Related Problems

### CSES Geometry Problems
| Problem | Link | Key Concept |
|---------|------|-------------|
| Point Location Test | [CSES 2189](https://cses.fi/problemset/task/2189) | Cross product for point-line relation |
| Line Segment Intersection | [CSES 2190](https://cses.fi/problemset/task/2190) | Cross product for intersection |
| Polygon Lattice Points | [CSES 2193](https://cses.fi/problemset/task/2193) | Pick's theorem + Shoelace |
| Convex Hull | [CSES 2195](https://cses.fi/problemset/task/2195) | Graham scan / Andrew's monotone chain |
| Point in Polygon | [CSES 2192](https://cses.fi/problemset/task/2192) | Ray casting + cross product |

### Similar LeetCode Problems
| Problem | Key Difference |
|---------|----------------|
| [Largest Triangle Area](https://leetcode.com/problems/largest-triangle-area/) | Find max area among all triangles |
| [Minimum Area Rectangle](https://leetcode.com/problems/minimum-area-rectangle/) | Find rectangle from point set |

---

## Key Takeaways

1. **The Core Idea:** Shoelace formula computes polygon area in O(n) using cross products of consecutive vertices.
2. **Why It Works:** Each term represents a signed trapezoid area; they sum to the total polygon area.
3. **Implementation Tips:** Use `long long`, wrap indices with modulo, take absolute value.
4. **Pattern:** This is fundamental to computational geometry - mastering it unlocks convex hull, point-in-polygon, and centroid calculations.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the Shoelace formula from first principles
- [ ] Implement it without looking at reference code
- [ ] Handle edge cases (overflow, orientation, wrap-around)
- [ ] Explain why signed area indicates polygon orientation
- [ ] Apply the technique to related problems (centroids, Pick's theorem)

---

## Additional Resources

- [CP-Algorithms: Polygon Area](https://cp-algorithms.com/geometry/area-of-simple-polygon.html)
- [Wikipedia: Shoelace Formula](https://en.wikipedia.org/wiki/Shoelace_formula)
- [Wikipedia: Pick's Theorem](https://en.wikipedia.org/wiki/Pick%27s_theorem)
