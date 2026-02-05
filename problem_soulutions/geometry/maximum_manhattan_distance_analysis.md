---
layout: simple
title: "Maximum Manhattan Distance - Geometry Problem"
permalink: /problem_soulutions/geometry/maximum_manhattan_distance_analysis
difficulty: Medium
tags: [geometry, coordinate-transformation, manhattan-distance, math]
---

# Maximum Manhattan Distance

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Rotated Coordinates (x+y, x-y) |
| **CSES Link** | - |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Transform Manhattan distance to Chebyshev distance using rotated coordinates
- [ ] Recognize when coordinate transformation simplifies a problem
- [ ] Apply the (x+y, x-y) transformation pattern to geometry problems
- [ ] Optimize O(n^2) pairwise comparisons to O(n) using mathematical insight

---

## Problem Statement

**Problem:** Given n points in a 2D plane, find the maximum Manhattan distance between any two points.

**Input:**
- Line 1: n (number of points)
- Next n lines: x_i, y_i (coordinates of each point)

**Output:**
- Maximum Manhattan distance between any pair of points

**Constraints:**
- 1 <= n <= 2 * 10^5
- -10^9 <= x, y <= 10^9

### Example

```
Input:
4
0 0
1 1
2 2
3 3

Output:
6
```

**Explanation:** The maximum Manhattan distance is between (0,0) and (3,3): |0-3| + |0-3| = 6.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we avoid checking all O(n^2) pairs?

The Manhattan distance |x1-x2| + |y1-y2| has four possible expansions depending on the signs. The maximum always equals max of |(x1+y1) - (x2+y2)| or |(x1-y1) - (x2-y2)|.

### The Mathematical Insight

For two points (x1, y1) and (x2, y2):

```
Manhattan Distance = |x1-x2| + |y1-y2|

Expanding all sign combinations:
= max( (x1-x2) + (y1-y2),   when x1>=x2, y1>=y2
       (x1-x2) - (y1-y2),   when x1>=x2, y1<=y2
      -(x1-x2) + (y1-y2),   when x1<=x2, y1>=y2
      -(x1-x2) - (y1-y2) )  when x1<=x2, y1<=y2

Rearranging:
= max( (x1+y1) - (x2+y2),
       (x1-y1) - (x2-y2),
      -(x1-y1) + (x2-y2),
      -(x1+y1) + (x2+y2) )

= max( |u1-u2|, |v1-v2| )  where u=x+y, v=x-y
```

### Analogies

Think of rotating the coordinate system by 45 degrees. In the rotated system (u, v) = (x+y, x-y), Manhattan distance becomes Chebyshev distance (max of coordinate differences), which is easier to optimize.

---

## Solution 1: Brute Force

### Idea

Check all pairs and compute Manhattan distance for each.

### Algorithm

1. For each pair of points (i, j)
2. Calculate |x_i - x_j| + |y_i - y_j|
3. Track the maximum

### Code

```python
def solve_brute_force(points):
    """
    Brute force: check all pairs.

    Time: O(n^2)
    Space: O(1)
    """
    n = len(points)
    max_dist = 0

    for i in range(n):
        for j in range(i + 1, n):
            dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            max_dist = max(max_dist, dist)

    return max_dist
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Check all n*(n-1)/2 pairs |
| Space | O(1) | Only store max distance |

### Why This Works (But Is Slow)

Correctness is guaranteed by exhaustive search. However, with n up to 2*10^5, we have about 2*10^10 operations - far too slow.

---

## Solution 2: Rotated Coordinates (Optimal)

### Key Insight

> **The Trick:** Transform to rotated coordinates (u, v) = (x+y, x-y). The maximum Manhattan distance equals max(max_u - min_u, max_v - min_v).

### Why This Works

After transformation, for any two points:
- Original: Manhattan(P1, P2) = |x1-x2| + |y1-y2|
- Transformed: max(|u1-u2|, |v1-v2|)

The maximum over all pairs of max(|u1-u2|, |v1-v2|) equals max(range of u, range of v).

### Algorithm

1. Transform each point: u = x + y, v = x - y
2. Find min and max of u values
3. Find min and max of v values
4. Return max(max_u - min_u, max_v - min_v)

### Dry Run Example

Let's trace through with points [(0,0), (1,1), (2,2), (3,3)]:

```
Step 1: Transform coordinates
  (0,0) -> u=0+0=0, v=0-0=0
  (1,1) -> u=1+1=2, v=1-1=0
  (2,2) -> u=2+2=4, v=2-2=0
  (3,3) -> u=3+3=6, v=3-3=0

Step 2: Find ranges
  u values: [0, 2, 4, 6]  -> range = 6 - 0 = 6
  v values: [0, 0, 0, 0]  -> range = 0 - 0 = 0

Step 3: Maximum distance = max(6, 0) = 6
```

### Visual Diagram

```
Original Coordinates:           Rotated Coordinates (45 deg):

y                               v (x-y)
^                               ^

|     (3,3)                     |
|   (2,2)                       |

| (1,1)                         0--*--*--*--*--> u (x+y)
*(0,0)                          0  2  4  6
+---------> x

Manhattan distance = 6          Chebyshev distance = max(6-0, 0-0) = 6
```

### Code

```python
import sys
input = sys.stdin.readline

def solve():
    """
    Optimal solution using rotated coordinates.

    Time: O(n)
    Space: O(1)
    """
    n = int(input())

    min_u = min_v = float('inf')
    max_u = max_v = float('-inf')

    for _ in range(n):
        x, y = map(int, input().split())
        u = x + y  # rotated coordinate 1
        v = x - y  # rotated coordinate 2

        min_u = min(min_u, u)
        max_u = max(max_u, u)
        min_v = min(min_v, v)
        max_v = max(max_v, v)

    print(max(max_u - min_u, max_v - min_v))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through all points |
| Space | O(1) | Only store 4 values (min/max for u and v) |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** With coordinates up to 10^9, x+y can reach 2*10^9, exceeding int range.
**Fix:** Use `long long` for all calculations.

### Mistake 2: Forgetting One Transformation

```python
# WRONG - only using x+y
max_dist = max_u - min_u

# CORRECT - use both transformations
max_dist = max(max_u - min_u, max_v - min_v)
```

**Problem:** The maximum might come from the x-y transformation.
**Fix:** Always compute and compare both ranges.

### Mistake 3: Wrong Transformation Formula

```python
# WRONG - dividing by sqrt(2)
u = (x + y) / math.sqrt(2)

# CORRECT - no division needed
u = x + y
```

**Problem:** The geometric rotation involves sqrt(2), but for finding max distance we only need the relative differences.
**Fix:** Use simple x+y and x-y without any scaling.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single point | n=1, (5,5) | 0 | Distance to itself is 0 |
| Two points | n=2, (0,0), (3,4) | 7 | Direct calculation |
| All same point | n=3, all (1,1) | 0 | All distances are 0 |
| Negative coords | (-10^9, -10^9), (10^9, 10^9) | 4*10^9 | Handle negative values |
| Diagonal line | (0,0), (k,k) for any k | 2*|k| | x-y values all equal |
| Anti-diagonal | (0,k), (k,0) | 2*k | x+y values all equal |

---

## When to Use This Pattern

### Use Rotated Coordinates When:
- Computing Manhattan distances between many points
- Finding closest/farthest pairs under Manhattan metric
- Problems involving taxicab geometry
- Need to optimize O(n^2) pairwise Manhattan calculations

### Don't Use When:
- Working with Euclidean distance (use different techniques)
- Problem requires actual pairs, not just the distance value
- Coordinates are in 3D+ (transformation becomes more complex)

### Pattern Recognition Checklist:
- [ ] Problem mentions Manhattan distance? Consider coordinate rotation
- [ ] Need max/min over all pairs? Consider transforming to find extremes
- [ ] L1 norm optimization? Rotated coordinates often help

---

## Related Problems

### Similar Difficulty (CSES)

| Problem | Key Difference |
|---------|----------------|
| [Point Location Test](https://cses.fi/problemset/task/2189) | Cross product for point-line relationship |
| [Convex Hull](https://cses.fi/problemset/task/2195) | Finding boundary of point set |
| [Nearest Smaller Values](https://cses.fi/problemset/task/1645) | 1D analogue using monotonic stack |

### LeetCode Problems

| Problem | Connection |
|---------|------------|
| [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Distance-based, but Euclidean |
| [Minimum Time Visiting All Points](https://leetcode.com/problems/minimum-time-visiting-all-points/) | Chebyshev distance (max of |dx|, |dy|) |
| [Best Position for a Service Centre](https://leetcode.com/problems/best-position-for-a-service-centre/) | Geometric median problem |

### Harder Extensions

| Problem | New Concept |
|---------|-------------|
| 3D Manhattan Distance | Use 2^3 = 8 transformations |
| K-th Largest Manhattan Distance | Combine with binary search |
| Manhattan MST | Divide into 8 regions per point |

---

## Key Takeaways

1. **The Core Idea:** Transform (x, y) to (x+y, x-y) to convert Manhattan to Chebyshev distance
2. **Time Optimization:** O(n^2) pairwise checks reduced to O(n) by finding range extremes
3. **Space Trade-off:** O(1) extra space - just track 4 values
4. **Pattern:** Coordinate transformation is powerful for geometry problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the (x+y, x-y) transformation from scratch
- [ ] Explain why max Manhattan = max(range of x+y, range of x-y)
- [ ] Implement in O(n) time and O(1) space
- [ ] Handle edge cases (overflow, single point, negative coordinates)
- [ ] Recognize this pattern in new problems

---

## Additional Resources

- [CP-Algorithms: Manhattan Distance](https://cp-algorithms.com/geometry/manhattan-distance.html)
- [Wikipedia: Taxicab Geometry](https://en.wikipedia.org/wiki/Taxicab_geometry)
- [Chebyshev Distance](https://en.wikipedia.org/wiki/Chebyshev_distance)
- [CSES Convex Hull](https://cses.fi/problemset/task/2195) - Computational geometry problem
