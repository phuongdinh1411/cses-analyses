---
layout: simple
title: "Convex Hull - Geometry Problem"
permalink: /problem_soulutions/geometry/convex_hull_analysis
difficulty: Medium
tags: [geometry, convex-hull, sorting, cross-product, monotone-chain]
prerequisites: [basic-geometry, cross-product]
---

# Convex Hull

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Convex Hull](https://cses.fi/problemset/task/2195) |
| **Difficulty** | Medium |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Andrew's Monotone Chain / Cross Product |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the cross product and its use in determining point orientation
- [ ] Implement Andrew's monotone chain algorithm for convex hull construction
- [ ] Handle collinear points and edge cases in geometric problems
- [ ] Apply sorting as a preprocessing step in computational geometry

---

## Problem Statement

**Problem:** Given n points in a 2D plane, find the convex hull - the smallest convex polygon that contains all the points.

**Input:**
- Line 1: Integer n (number of points)
- Lines 2 to n+1: Two integers x and y (coordinates of each point)

**Output:**
- Line 1: Integer m (number of vertices in the convex hull)
- Lines 2 to m+1: Coordinates of hull vertices in counter-clockwise order, starting from the leftmost-lowest point

**Constraints:**
- 1 <= n <= 2 * 10^5
- -10^9 <= x, y <= 10^9

### Example

```
Input:
6
0 0
1 1
2 2
3 1
2 0
1 2

Output:
4
0 0
2 0
3 1
1 2
```

**Explanation:** The convex hull forms a quadrilateral with vertices (0,0), (2,0), (3,1), and (1,2). Point (1,1) is inside the hull, and (2,2) lies on the edge between (1,2) and (3,1).

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we determine which points form the boundary of the smallest enclosing convex polygon?

The key insight is that as we traverse the hull boundary, we always turn in the same direction (counterclockwise). We can detect this using the **cross product** - if we ever make a clockwise turn, that point cannot be on the hull.

### Breaking Down the Problem

1. **What are we looking for?** The subset of points that form the convex boundary.
2. **What information do we have?** Coordinates of all points.
3. **What's the relationship between input and output?** Hull points are the "extreme" points that cannot be expressed as a convex combination of other points.

### Analogies

Think of this problem like stretching a rubber band around a set of nails on a board. The rubber band naturally wraps around the outermost nails, forming the convex hull. Inner nails don't affect the shape.

---

## Solution 1: Brute Force

### Idea

For each pair of points, check if all other points lie on the same side of the line formed by that pair. If yes, both points are on the hull.

### Algorithm

1. For each pair of points (p1, p2)
2. Check if all other points are on the same side using cross product
3. If yes, add both points to the hull set
4. Sort hull points to get proper order

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | Check n^2 pairs, each check is O(n) |
| Space | O(n) | Store hull points |

### Why This Works (But Is Slow)

Every edge of the convex hull has all other points on one side. However, checking all pairs is inefficient for large inputs.

---

## Solution 2: Andrew's Monotone Chain (Optimal)

### Key Insight

> **The Trick:** Sort points by x-coordinate, then build upper and lower hulls separately by maintaining the "turn left" property.

### Algorithm

1. Sort all points by x-coordinate (y as tiebreaker)
2. Build **lower hull**: Traverse left to right, keeping only points that make left turns
3. Build **upper hull**: Traverse right to left, keeping only points that make left turns
4. Combine both hulls (excluding duplicated endpoints)

### Cross Product Formula

For three points O, A, B:
```
cross(O, A, B) = (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x)
```

| Value | Meaning |
|-------|---------|
| > 0 | Counter-clockwise (left turn) |
| = 0 | Collinear |
| < 0 | Clockwise (right turn) |

### Dry Run Example

Let's trace through with input points: `(0,0), (1,1), (2,2), (3,1), (2,0), (1,2)`

```
Step 1: Sort by x-coordinate (then y)
  Sorted: [(0,0), (1,1), (1,2), (2,0), (2,2), (3,1)]

Step 2: Build Lower Hull (left to right)
  Start: []
  Add (0,0): [(0,0)]
  Add (1,1): [(0,0), (1,1)]
  Add (1,2): cross((0,0),(1,1),(1,2)) = 1 > 0 (left turn) -> keep
             [(0,0), (1,1), (1,2)]
  Add (2,0): cross((1,1),(1,2),(2,0)) = -2 < 0 (right turn) -> pop (1,2)
             cross((0,0),(1,1),(2,0)) = -1 < 0 (right turn) -> pop (1,1)
             [(0,0), (2,0)]
  Add (2,2): cross((0,0),(2,0),(2,2)) = 4 > 0 (left turn) -> keep
             [(0,0), (2,0), (2,2)]
  Add (3,1): cross((2,0),(2,2),(3,1)) = -2 < 0 (right turn) -> pop (2,2)
             cross((0,0),(2,0),(3,1)) = 2 > 0 (left turn) -> keep
             Lower hull: [(0,0), (2,0), (3,1)]

Step 3: Build Upper Hull (right to left)
  Start: []
  Add (3,1): [(3,1)]
  Add (2,2): [(3,1), (2,2)]
  Add (2,0): cross((3,1),(2,2),(2,0)) = 2 > 0 -> keep
             [(3,1), (2,2), (2,0)]
  Add (1,2): cross((2,2),(2,0),(1,2)) = 4 > 0 -> keep...
             But we need to pop (2,0) first: cross = -2 < 0 -> pop
             [(3,1), (2,2), (1,2)]
  ... continue until:
             Upper hull: [(3,1), (1,2), (0,0)]

Step 4: Combine (remove duplicate endpoints)
  Final hull: [(0,0), (2,0), (3,1), (1,2)]
```

### Visual Diagram

```
       (1,2)
        *---------* (2,2) <- not on hull
       /           \
      /    (1,1)    \
     /      *        \
    /                 \
(0,0)*-------*--------*(3,1)
            (2,0)

Hull: (0,0) -> (2,0) -> (3,1) -> (1,2) -> back to (0,0)
```

### Code

**Python Solution:**

```python
import sys
from typing import List, Tuple

def cross(o: Tuple[int, int], a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Calculate cross product of vectors OA and OB."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Find convex hull using Andrew's monotone chain algorithm.

    Time: O(n log n) - dominated by sorting
    Space: O(n) - store hull points
    """
    points = sorted(set(points))  # Remove duplicates and sort

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

    # Concatenate hulls, removing duplicate endpoints
    return lower[:-1] + upper[:-1]

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1

    points = []
    for _ in range(n):
        x = int(input_data[idx]); idx += 1
        y = int(input_data[idx]); idx += 1
        points.append((x, y))

    hull = convex_hull(points)

    print(len(hull))
    for x, y in hull:
        print(x, y)

if __name__ == "__main__":
    main()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<ll, ll> Point;

ll cross(Point O, Point A, Point B) {
    return (A.first - O.first) * (B.second - O.second)
         - (A.second - O.second) * (B.first - O.first);
}

vector<Point> convexHull(vector<Point>& points) {
    sort(points.begin(), points.end());
    points.erase(unique(points.begin(), points.end()), points.end());

    int n = points.size();
    if (n <= 1) return points;

    vector<Point> hull;

    // Build lower hull
    for (int i = 0; i < n; i++) {
        while (hull.size() >= 2 && cross(hull[hull.size()-2], hull[hull.size()-1], points[i]) <= 0)
            hull.pop_back();
        hull.push_back(points[i]);
    }

    // Build upper hull
    int lower_size = hull.size();
    for (int i = n - 2; i >= 0; i--) {
        while (hull.size() > lower_size && cross(hull[hull.size()-2], hull[hull.size()-1], points[i]) <= 0)
            hull.pop_back();
        hull.push_back(points[i]);
    }

    hull.pop_back();  // Remove duplicate endpoint
    return hull;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<Point> points(n);
    for (int i = 0; i < n; i++) {
        cin >> points[i].first >> points[i].second;
    }

    vector<Point> hull = convexHull(points);

    cout << hull.size() << "\n";
    for (auto& p : hull) {
        cout << p.first << " " << p.second << "\n";
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Sorting dominates; hull construction is O(n) |
| Space | O(n) | Store sorted points and hull |

---

## Common Mistakes

### Mistake 1: Integer Overflow in Cross Product

```cpp
// WRONG - may overflow with int
int cross(Point O, Point A, Point B) {
    return (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x);
}

// CORRECT - use long long
long long cross(Point O, Point A, Point B) {
    return (long long)(A.x - O.x) * (B.y - O.y)
         - (long long)(A.y - O.y) * (B.x - O.x);
}
```

**Problem:** With coordinates up to 10^9, the product can reach 10^18.
**Fix:** Use `long long` for cross product calculations.

### Mistake 2: Not Handling Collinear Points

```python
# WRONG - excludes collinear boundary points
while len(hull) >= 2 and cross(hull[-2], hull[-1], p) < 0:  # strict

# CORRECT for excluding collinear (typical requirement)
while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:  # non-strict
```

**Problem:** CSES problem typically wants minimal hull (no collinear points on edges).
**Fix:** Use `<= 0` to exclude collinear points from the hull boundary.

### Mistake 3: Wrong Output Order

```python
# WRONG - clockwise order
hull = upper[:-1] + lower[:-1]

# CORRECT - counter-clockwise order
hull = lower[:-1] + upper[:-1]
```

**Problem:** The problem specifies counter-clockwise output order.
**Fix:** Combine lower hull first, then upper hull.

### Mistake 4: Not Removing Duplicate Points

```python
# WRONG - duplicate points cause issues
points.sort()

# CORRECT - remove duplicates first
points = sorted(set(points))
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single point | `n=1, (0,0)` | `1\n0 0` | Hull is the point itself |
| Two points | `n=2, (0,0), (1,1)` | `2\n0 0\n1 1` | Hull is a line segment |
| All collinear | `(0,0), (1,1), (2,2)` | `2\n0 0\n2 2` | Only endpoints matter |
| All same point | `(1,1), (1,1), (1,1)` | `1\n1 1` | Deduplicate first |
| Square | `(0,0), (0,1), (1,0), (1,1)` | `4\n...` | All points on hull |
| Triangle with interior | `(0,0), (2,0), (1,2), (1,1)` | `3\n0 0\n2 0\n1 2` | Interior point excluded |

---

## When to Use This Pattern

### Use Monotone Chain When:
- You need to find the convex boundary of a point set
- All points fit in memory and can be sorted
- You need O(n log n) performance
- Output order matters (counter-clockwise)

### Don't Use When:
- Points arrive in a stream (use online algorithms)
- Working in 3D or higher dimensions (use different algorithms)
- You need to maintain hull under insertions/deletions (use dynamic convex hull)

### Pattern Recognition Checklist:
- [ ] Problem involves finding extreme/boundary points? -> **Consider convex hull**
- [ ] Need to find farthest pair of points? -> **Convex hull + rotating calipers**
- [ ] Enclosing shape problems? -> **Often involves convex hull**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Point Location Test](https://cses.fi/problemset/task/2189) | Practice cross product for orientation |
| [Line Segment Intersection](https://cses.fi/problemset/task/2190) | Understand geometric primitives |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Polygon Area](https://cses.fi/problemset/task/2191) | Apply cross product for area calculation |
| [Point in Polygon](https://cses.fi/problemset/task/2192) | Use cross product for containment test |
| [Erect the Fence (LeetCode 587)](https://leetcode.com/problems/erect-the-fence/) | Same problem, include collinear points |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Polygon Lattice Points](https://cses.fi/problemset/task/2193) | Pick's theorem with convex hull |
| [Minimum Euclidean Distance](https://cses.fi/problemset/task/2194) | Convex hull for optimization |

---

## Key Takeaways

1. **The Core Idea:** Sort points and build hull by maintaining left-turn property using cross product.
2. **Time Optimization:** Sorting + linear scan beats O(n^3) brute force with O(n log n).
3. **Space Trade-off:** O(n) space is necessary to store the hull.
4. **Pattern:** Computational geometry problems often rely on the cross product as a fundamental building block.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain what the cross product tells us about point orientation
- [ ] Implement Andrew's monotone chain from scratch
- [ ] Handle edge cases (collinear points, duplicates, small n)
- [ ] Solve this problem in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Convex Hull](https://cp-algorithms.com/geometry/convex-hull.html)
- [Visualgo: Convex Hull Visualization](https://visualgo.net/en/convexhull)
- [CSES Geometry Problems](https://cses.fi/problemset/list/)
