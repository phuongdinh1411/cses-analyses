---
layout: simple
title: "Line Segment Intersection - Geometry Problem"
permalink: /problem_soulutions/geometry/line_segment_intersection_analysis
difficulty: Medium
tags: [geometry, cross-product, computational-geometry]
prerequisites: [point_location, convex_hull]
---

# Line Segment Intersection

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Line Segment Intersection](https://cses.fi/problemset/task/2190) |
| **Difficulty** | Medium |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Cross Product / Orientation Test |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the cross product and its geometric meaning
- [ ] Use orientation tests to determine relative positions of points
- [ ] Detect if two line segments intersect (including edge cases)
- [ ] Handle collinear points correctly in geometric problems

---

## Problem Statement

**Problem:** Given two line segments, determine if they intersect.

**Input:**
- Line 1: Four integers x1, y1, x2, y2 - endpoints of first segment
- Line 2: Four integers x3, y3, x4, y4 - endpoints of second segment

**Output:**
- "YES" if the segments intersect, "NO" otherwise

**Constraints:**
- -10^9 <= x, y <= 10^9
- Segments may be points (both endpoints same)

### Example

```
Input:
0 0 4 4
0 4 4 0

Output:
YES
```

**Explanation:** The two segments form an "X" shape, crossing at point (2, 2).

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we determine if two line segments cross without computing the actual intersection point?

The insight is that two segments intersect if and only if:
1. The endpoints of each segment are on **opposite sides** of the line containing the other segment, OR
2. An endpoint lies exactly **on** the other segment (collinear case)

### Breaking Down the Problem

1. **What are we looking for?** Whether two segments share any point
2. **What information do we have?** Four points defining two segments
3. **What's the relationship?** Use orientation to check if points "straddle" each segment

### The Cross Product Analogy

Think of the cross product as a "turn detector":
- Standing at point A, looking toward point B
- **Positive cross product:** Point C is on your LEFT
- **Negative cross product:** Point C is on your RIGHT
- **Zero cross product:** Point C is directly AHEAD or BEHIND (collinear)

```
        C (left, cross > 0)
       /
      /
A -------- B
      \
       \
        D (right, cross < 0)
```

---

## Core Concept: Cross Product

### Definition

For vectors AB and AC, the 2D cross product is:

```
cross(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)
```

### Geometric Meaning

| Cross Product Value | Meaning |
|---------------------|---------|
| > 0 | C is counter-clockwise (left) from AB |
| < 0 | C is clockwise (right) from AB |
| = 0 | A, B, C are collinear |

---

## Solution: Orientation-Based Intersection Test

### Key Insight

> **The Trick:** Two segments intersect if their endpoints have opposite orientations relative to each other.

### Algorithm

1. Compute orientation of (A, B, C) and (A, B, D) for segment AB and points C, D of segment CD
2. Compute orientation of (C, D, A) and (C, D, B)
3. **General case:** Segments intersect if orientations differ on both tests
4. **Collinear case:** Check if segments actually overlap on the line

### Visual Diagram

```
Segment 1: A(0,0) to B(4,4)
Segment 2: C(0,4) to D(4,0)

    4 |  C
      |    \
    2 |      X (intersection)
      |    /
    0 +--A----------> x
      0  2  4

Orientation tests:
- cross(A,B,C) = (4-0)*(4-0) - (4-0)*(0-0) = 16 > 0  (C is LEFT of AB)
- cross(A,B,D) = (4-0)*(0-0) - (4-0)*(4-0) = -16 < 0 (D is RIGHT of AB)
  -> C and D are on opposite sides of AB: CHECK

- cross(C,D,A) = (4-0)*(0-4) - (-4-0)*(0-0) = -16 < 0 (A is RIGHT of CD)
- cross(C,D,B) = (4-0)*(4-4) - (-4-0)*(4-0) = 16 > 0  (B is LEFT of CD)
  -> A and B are on opposite sides of CD: CHECK

Both checks pass -> INTERSECT
```

### Dry Run Example

Let's trace through with segments A(1,1)-B(5,5) and C(1,5)-D(5,1):

```
Step 1: Calculate orientations for segment AB
  cross(A, B, C) = (5-1)*(5-1) - (5-1)*(1-1) = 16 - 0 = 16 > 0
  cross(A, B, D) = (5-1)*(1-1) - (5-1)*(5-1) = 0 - 16 = -16 < 0
  -> d1=16, d2=-16 have opposite signs: YES

Step 2: Calculate orientations for segment CD
  cross(C, D, A) = (5-1)*(1-5) - (1-5)*(1-1) = -16 - 0 = -16 < 0
  cross(C, D, B) = (5-1)*(5-5) - (1-5)*(5-1) = 0 + 16 = 16 > 0
  -> d3=-16, d4=16 have opposite signs: YES

Step 3: Both conditions met -> Output "YES"
```

### Code

**Python:**
```python
def cross(o, a, b):
    """
    Compute cross product of vectors OA and OB.
    Returns positive if B is counter-clockwise from A (relative to O).
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def on_segment(p, q, r):
    """Check if point q lies on segment pr (assuming collinear)."""
    return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
            min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

def segments_intersect(p1, p2, p3, p4):
    """
    Check if segment p1-p2 intersects segment p3-p4.

    Time: O(1)
    Space: O(1)
    """
    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)

    # General case: segments straddle each other
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    # Collinear cases: check if any endpoint lies on the other segment
    if d1 == 0 and on_segment(p3, p1, p4): return True
    if d2 == 0 and on_segment(p3, p2, p4): return True
    if d3 == 0 and on_segment(p1, p3, p2): return True
    if d4 == 0 and on_segment(p1, p4, p2): return True

    return False

# Read input and solve
x1, y1, x2, y2 = map(int, input().split())
x3, y3, x4, y4 = map(int, input().split())

if segments_intersect((x1, y1), (x2, y2), (x3, y3), (x4, y4)):
    print("YES")
else:
    print("NO")
```

**C++:**
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<ll, ll> Point;

ll cross(Point o, Point a, Point b) {
    return (a.first - o.first) * (b.second - o.second)
         - (a.second - o.second) * (b.first - o.first);
}

bool onSegment(Point p, Point q, Point r) {
    return min(p.first, r.first) <= q.first && q.first <= max(p.first, r.first) &&
           min(p.second, r.second) <= q.second && q.second <= max(p.second, r.second);
}

bool segmentsIntersect(Point p1, Point p2, Point p3, Point p4) {
    ll d1 = cross(p3, p4, p1);
    ll d2 = cross(p3, p4, p2);
    ll d3 = cross(p1, p2, p3);
    ll d4 = cross(p1, p2, p4);

    // General case
    if (((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) &&
        ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0))) {
        return true;
    }

    // Collinear cases
    if (d1 == 0 && onSegment(p3, p1, p4)) return true;
    if (d2 == 0 && onSegment(p3, p2, p4)) return true;
    if (d3 == 0 && onSegment(p1, p3, p2)) return true;
    if (d4 == 0 && onSegment(p1, p4, p2)) return true;

    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll x1, y1, x2, y2, x3, y3, x4, y4;
    cin >> x1 >> y1 >> x2 >> y2;
    cin >> x3 >> y3 >> x4 >> y4;

    if (segmentsIntersect({x1, y1}, {x2, y2}, {x3, y3}, {x4, y4})) {
        cout << "YES\n";
    } else {
        cout << "NO\n";
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(1) | Fixed number of arithmetic operations |
| Space | O(1) | Only store a few variables |

---

## Common Mistakes

### Mistake 1: Forgetting Collinear Cases

```python
# WRONG - only handles general case
def intersect_wrong(p1, p2, p3, p4):
    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)
    return (d1 * d2 < 0) and (d3 * d4 < 0)  # Misses collinear!
```

**Problem:** This misses cases where segments are collinear and overlap.
**Fix:** Add explicit checks for when cross products are zero.

### Mistake 2: Integer Overflow

```cpp
// WRONG - int may overflow with coordinates up to 10^9
int cross(pair<int,int> o, pair<int,int> a, pair<int,int> b) {
    return (a.first - o.first) * (b.second - o.second) - ...;
}
```

**Problem:** With coordinates up to 10^9, products can exceed 10^18.
**Fix:** Use `long long` for all calculations.

### Mistake 3: Wrong Sign Comparison

```python
# WRONG - checking d1 * d2 <= 0 includes unintended cases
if d1 * d2 <= 0 and d3 * d4 <= 0:  # Too permissive!
    return True
```

**Problem:** This says "YES" even when segments don't actually touch in collinear cases.
**Fix:** Handle strict inequality and collinear cases separately.

---

## Edge Cases

| Case | Input Example | Expected | Why |
|------|---------------|----------|-----|
| Crossing segments | (0,0)-(4,4), (0,4)-(4,0) | YES | Standard X intersection |
| Parallel segments | (0,0)-(4,0), (0,1)-(4,1) | NO | Never meet |
| Collinear overlap | (0,0)-(4,0), (2,0)-(6,0) | YES | Share segment (2,0)-(4,0) |
| Collinear no overlap | (0,0)-(2,0), (3,0)-(5,0) | NO | On same line but gap exists |
| Touch at endpoint | (0,0)-(2,2), (2,2)-(4,0) | YES | Segments share point (2,2) |
| T-junction | (0,0)-(4,0), (2,0)-(2,2) | YES | One endpoint on other segment |
| Point segments | (2,2)-(2,2), (0,0)-(4,4) | YES | Point lies on the line segment |
| Same segment | (0,0)-(4,4), (0,0)-(4,4) | YES | Identical segments |

---

## When to Use This Pattern

### Use Cross Product Orientation When:
- Determining if points are on left/right side of a line
- Checking line segment intersection
- Computing convex hulls (sorting by angle)
- Checking if a point is inside a polygon

### Algorithm Selection Guide:

| Situation | Approach |
|-----------|----------|
| Check 2 segments once | Cross product method (this problem) |
| Check many segment pairs | Consider sweep line |
| Find intersection point | Use parametric equations after confirming intersection |
| Many segments, report all intersections | Bentley-Ottmann algorithm |

### Pattern Recognition Checklist:
- [ ] Need to determine relative position of points? -> **Cross product**
- [ ] Checking if segments cross? -> **Orientation test**
- [ ] Building convex hull? -> **Cross product for turn direction**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Point Location Test](https://cses.fi/problemset/task/2189) | Learn cross product basics |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Polygon Area](https://cses.fi/problemset/task/2191) | Use cross product for area |
| [Point in Polygon](https://cses.fi/problemset/task/2192) | Ray casting with segment tests |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Polygon Lattice Points](https://cses.fi/problemset/task/2193) | Pick's theorem |
| [Convex Hull](https://cses.fi/problemset/task/2195) | Cross product for angles |

---

## Key Takeaways

1. **The Core Idea:** Two segments intersect if endpoints of each segment lie on opposite sides of the line containing the other segment.
2. **Cross Product:** A fundamental tool that tells you the relative orientation of three points.
3. **Collinear Cases:** Always handle the zero cross product case separately - it requires bounding box checks.
4. **Pattern:** This orientation-based approach extends to many geometry problems (convex hull, polygon tests).

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement the cross product formula from memory
- [ ] Explain what positive/negative/zero cross product means geometrically
- [ ] Handle all collinear edge cases correctly
- [ ] Solve this problem in under 10 minutes

---

## Additional Resources

- [CP-Algorithms: Line Intersection](https://cp-algorithms.com/geometry/segments-intersection.html)
- [CP-Algorithms: Basic Geometry](https://cp-algorithms.com/geometry/basic-geometry.html)
- [CSES Geometry Section](https://cses.fi/problemset/list/)
