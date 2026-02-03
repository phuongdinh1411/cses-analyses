---
layout: simple
title: "Half-Plane Intersection - Computational Geometry"
permalink: /problem_soulutions/geometry/half_plane_intersection_analysis
difficulty: Hard
tags: [geometry, half-plane, linear-programming, convex-region, computational-geometry]
prerequisites: [convex_hull, line_segment_intersection, point_location_test]
---

# Half-Plane Intersection

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Computational Geometry |
| **Time Complexity** | O(n log n) |
| **Key Technique** | Incremental Algorithm with Deque |

### Concept Explanation

A **half-plane** is the region of the 2D plane on one side of a line. Given a line `ax + by + c = 0`, the two half-planes are `ax + by + c >= 0` and `ax + by + c <= 0`.

The **half-plane intersection** problem asks: given `n` half-planes, find the region satisfying ALL constraints. This region is always **convex** (possibly empty, a point, a segment, or unbounded).

### Learning Goals

After studying this topic, you will be able to:
- [ ] Understand half-plane representation and orientation
- [ ] Implement the incremental half-plane intersection algorithm
- [ ] Handle edge cases: parallel lines, unbounded regions, empty intersections
- [ ] Apply half-plane intersection to 2D linear programming
- [ ] Recognize the duality between half-plane intersection and convex hull

---

## Problem Statement

**Problem:** Given `n` half-planes (each defined by a directed line where points to the left are included), compute the convex polygon representing their intersection.

**Input:** `n` half-planes, each as four integers `x1 y1 x2 y2` defining directed line from (x1,y1) to (x2,y2).

**Output:** Vertices of intersection polygon (CCW), or "EMPTY" / "UNBOUNDED"

**Constraints:** 1 <= n <= 10^5, coordinates in [-10^9, 10^9]

---

## Intuition: How to Think About This Problem

### The Incremental Algorithm

> **Key Insight:** Process half-planes in angular order, maintaining the boundary in a deque.

1. **Sort by angle** - Each half-plane's boundary line has an angle; sort all half-planes by this.
2. **Process sequentially** - Maintain current intersection boundary as edges in a deque.
3. **Prune both ends** - When adding a new half-plane, remove edges from front/back that fall outside.
4. **Add new edge** - Append the new half-plane's boundary.

### Why a Deque?

The boundary forms a **convex chain**. In angular order, new half-planes only cut edges from the ends, never the middle. This gives O(1) amortized operations per half-plane.

---

## Dry Run: 4 Half-Planes

```
Half-plane 1: y >= 0     (above x-axis)
Half-plane 2: x <= 10    (left of x=10)
Half-plane 3: y <= 10    (below y=10)
Half-plane 4: x >= 0     (right of y-axis)
```

### Step-by-Step

```
Step 0: Sort by angle -> H1(0deg), H2(90deg), H3(180deg), H4(270deg)

Step 1: Process H1 (y >= 0)
  Deque: [H1]

Step 2: Process H2 (x <= 10)
  H1 intersect H2 = (10, 0) - valid
  Deque: [H1, H2]

Step 3: Process H3 (y <= 10)
  H2 intersect H3 = (10, 10) - valid
  Deque: [H1, H2, H3]

Step 4: Process H4 (x >= 0)
  H3 intersect H4 = (0, 10) - valid
  H4 intersect H1 = (0, 0) - valid (closes the loop)
  Deque: [H1, H2, H3, H4]

Final: Square with vertices (0,0), (10,0), (10,10), (0,10)
```

```
    y=10  +----------+
          |          |
          |   IN     |
          |          |
    y=0   +----------+
         x=0        x=10
```

---

## Python Implementation

```python
from math import atan2
from collections import deque

EPS = 1e-9

class HalfPlane:
    def __init__(self, p, q):
        self.p = p
        self.d = (q[0] - p[0], q[1] - p[1])
        self.angle = atan2(self.d[1], self.d[0])

    def side(self, point):
        return self.d[0] * (point[1] - self.p[1]) - self.d[1] * (point[0] - self.p[0])

    def inside(self, point):
        return self.side(point) > -EPS

def line_intersection(h1, h2):
    cross = h1.d[0] * h2.d[1] - h1.d[1] * h2.d[0]
    if abs(cross) < EPS:
        return None
    dx, dy = h2.p[0] - h1.p[0], h2.p[1] - h1.p[1]
    t = (dx * h2.d[1] - dy * h2.d[0]) / cross
    return (h1.p[0] + t * h1.d[0], h1.p[1] + t * h1.d[1])

def half_plane_intersection(half_planes):
    """Returns vertices (CCW) or empty list. Time: O(n log n), Space: O(n)"""
    if not half_planes:
        return []

    half_planes.sort(key=lambda h: h.angle)

    # Remove parallel duplicates, keep most restrictive
    unique = [half_planes[0]]
    for hp in half_planes[1:]:
        if abs(hp.angle - unique[-1].angle) > EPS:
            unique.append(hp)
        elif hp.side(unique[-1].p) < 0:
            unique[-1] = hp
    half_planes = unique

    if len(half_planes) < 3:
        return []

    dq = deque()
    for hp in half_planes:
        while len(dq) >= 2:
            pt = line_intersection(dq[-1], dq[-2])
            if pt and not hp.inside(pt):
                dq.pop()
            else:
                break
        while len(dq) >= 2:
            pt = line_intersection(dq[0], dq[1])
            if pt and not hp.inside(pt):
                dq.popleft()
            else:
                break
        dq.append(hp)

    # Final cleanup
    while len(dq) >= 3:
        pt = line_intersection(dq[-1], dq[-2])
        if pt and not dq[0].inside(pt):
            dq.pop()
        else:
            break
    while len(dq) >= 3:
        pt = line_intersection(dq[0], dq[1])
        if pt and not dq[-1].inside(pt):
            dq.popleft()
        else:
            break

    if len(dq) < 3:
        return []

    dq_list = list(dq)
    return [line_intersection(dq_list[i], dq_list[(i+1) % len(dq_list)])
            for i in range(len(dq_list))]
```

---

## C++ Implementation

```cpp
#include <bits/stdc++.h>
using namespace std;

const double EPS = 1e-9;

struct Point {
    double x, y;
    Point(double x = 0, double y = 0) : x(x), y(y) {}
    Point operator-(const Point& p) const { return {x - p.x, y - p.y}; }
    Point operator+(const Point& p) const { return {x + p.x, y + p.y}; }
    Point operator*(double t) const { return {x * t, y * t}; }
    double cross(const Point& p) const { return x * p.y - y * p.x; }
};

struct HalfPlane {
    Point p, d;
    double angle;
    HalfPlane() {}
    HalfPlane(Point a, Point b) : p(a), d(b - a) { angle = atan2(d.y, d.x); }
    bool inside(const Point& pt) const { return d.cross(pt - p) > -EPS; }
    bool operator<(const HalfPlane& h) const { return angle < h.angle; }
};

Point intersection(const HalfPlane& h1, const HalfPlane& h2) {
    double t = (h2.p - h1.p).cross(h2.d) / h1.d.cross(h2.d);
    return h1.p + h1.d * t;
}

vector<Point> halfPlaneIntersection(vector<HalfPlane>& hp) {
    sort(hp.begin(), hp.end());

    vector<HalfPlane> unique;
    for (auto& h : hp) {
        if (unique.empty() || abs(h.angle - unique.back().angle) > EPS)
            unique.push_back(h);
        else if (h.d.cross(unique.back().p - h.p) < 0)
            unique.back() = h;
    }
    hp = unique;
    if (hp.size() < 3) return {};

    deque<HalfPlane> dq;
    for (auto& h : hp) {
        while (dq.size() >= 2 && !h.inside(intersection(dq[dq.size()-1], dq[dq.size()-2])))
            dq.pop_back();
        while (dq.size() >= 2 && !h.inside(intersection(dq[0], dq[1])))
            dq.pop_front();
        dq.push_back(h);
    }

    while (dq.size() >= 3 && !dq[0].inside(intersection(dq[dq.size()-1], dq[dq.size()-2])))
        dq.pop_back();
    while (dq.size() >= 3 && !dq[dq.size()-1].inside(intersection(dq[0], dq[1])))
        dq.pop_front();

    if (dq.size() < 3) return {};

    vector<Point> result;
    for (size_t i = 0; i < dq.size(); i++)
        result.push_back(intersection(dq[i], dq[(i + 1) % dq.size()]));
    return result;
}
```

---

## Common Mistakes

### Mistake 1: Not Handling Parallel Lines

```python
# WRONG
pt = line_intersection(h1, h2)
vertices.append(pt)  # pt could be None!

# CORRECT
pt = line_intersection(h1, h2)
if pt is not None:
    vertices.append(pt)
```

### Mistake 2: Forgetting Final Cleanup

The first half-plane may invalidate edges added near the end. Always perform a final cleanup pass checking both ends against the opposite end's constraints.

### Mistake 3: Angle Wraparound

Angles near -pi and pi are adjacent. When checking for parallel lines, also check if `|angle1 - angle2| ~ 2*pi`.

---

## Edge Cases

| Case | Input | Output | Why |
|------|-------|--------|-----|
| Empty intersection | Contradicting constraints | EMPTY | No feasible point |
| Unbounded | < 3 non-parallel half-planes | UNBOUNDED | Cannot close polygon |
| Single point | 3 half-planes at one point | Degenerate | Valid but degenerate |
| Parallel same direction | `y >= 0` and `y >= 5` | Keep `y >= 5` | More restrictive |
| Numerical instability | Near-parallel lines | Be careful | Use appropriate epsilon |

---

## When to Use This Pattern

**Use When:**
- Computing feasible region of 2D linear constraints
- Finding kernel of a simple polygon
- Solving 2D linear programming
- Computing Voronoi diagram cells

**Don't Use When:**
- Non-linear constraints
- Higher dimensions (need general LP)
- Only checking emptiness (simpler methods exist)

---

## Connection to Convex Hull (Duality)

| Primal | Dual |
|--------|------|
| Point (x, y) | Line y = ax + b |
| Half-plane intersection | Convex hull of dual points |

**Implication:** You can solve half-plane intersection by:
1. Transform each half-plane to its dual point
2. Compute convex hull of dual points
3. Transform hull edges back to vertices

This provides an alternative O(n log n) solution using any convex hull algorithm.

---

## Related Problems

| Difficulty | Problem | Connection |
|------------|---------|------------|
| Easier | Point Location Test | Which side of line |
| Easier | Convex Hull | Dual problem |
| Similar | Polygon Kernel | Half-planes from edges |
| Similar | 2D Linear Programming | Optimization over intersection |
| Harder | 3D Half-Space Intersection | Extension to 3D |

---

## Key Takeaways

1. **Core Idea:** Incrementally maintain convex boundary in a deque, processing half-planes by angle.
2. **Complexity:** O(n log n) time via sorting; O(n) space.
3. **Critical:** Handle parallel lines, final cleanup, numerical precision.
4. **Duality:** Half-plane intersection is dual to convex hull.

---

## Practice Checklist

- [ ] Implement from scratch without reference
- [ ] Handle all edge cases correctly
- [ ] Explain why deque maintains valid convex chain
- [ ] Apply to 2D LP and polygon kernel problems
- [ ] Understand duality with convex hull
