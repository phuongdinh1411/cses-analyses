---
layout: simple
title: "Minimum Euclidean Distance - Geometry Problem"
permalink: /problem_soulutions/geometry/minimum_euclidean_distance_analysis
difficulty: Hard
tags: [geometry, divide-and-conquer, closest-pair, computational-geometry]
---

# Minimum Euclidean Distance

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Minimum Euclidean Distance](https://cses.fi/problemset/task/2194) |
| **Difficulty** | Hard |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Divide and Conquer (Closest Pair Algorithm) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the classic Closest Pair of Points algorithm
- [ ] Apply divide and conquer to geometric problems
- [ ] Optimize strip processing using the "7 points" insight
- [ ] Handle squared distances to avoid floating-point precision issues

---

## Problem Statement

**Problem:** Given n points in a 2D plane, find the minimum squared Euclidean distance between any two points.

**Input:**
- Line 1: n (number of points)
- Lines 2 to n+1: x and y coordinates of each point

**Output:**
- The minimum squared Euclidean distance between any two points

**Constraints:**
- 2 <= n <= 200,000
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
2
```

**Explanation:** The closest pair is any two adjacent points like (0,0) and (1,1). The squared distance is (1-0)^2 + (1-0)^2 = 1 + 1 = 2.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Given n points, how do we avoid checking all O(n^2) pairs?

The key insight is that **divide and conquer** can reduce this to O(n log n) by exploiting the geometric property that points far apart in x-coordinate cannot be close together.

### Breaking Down the Problem

1. **What are we looking for?** The minimum squared distance between any two points.
2. **What information do we have?** All point coordinates.
3. **What is the relationship between input and output?** We must find the pair of points that are geometrically closest.

### Analogies

Think of this like finding the two closest houses in a city. Instead of measuring every pair, you first divide the city in half, find the closest pair in each half, then only check houses near the dividing line that might be closer.

---

## Solution 1: Brute Force

### Idea

Check every pair of points and compute their squared distance.

### Algorithm

1. For each pair of points (i, j) where i < j
2. Calculate squared Euclidean distance
3. Track the minimum

### Code

```python
def solve_brute_force(points):
    """
    Brute force solution - check all pairs.

    Time: O(n^2)
    Space: O(1)
    """
    n = len(points)
    min_dist = float('inf')

    for i in range(n):
        for j in range(i + 1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dist_sq = dx * dx + dy * dy
            min_dist = min(min_dist, dist_sq)

    return min_dist
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Check all n*(n-1)/2 pairs |
| Space | O(1) | Only store minimum |

### Why This Works (But Is Slow)

Correctness is guaranteed by exhaustive search, but with n = 200,000 points, we would need ~20 billion operations, which is far too slow.

---

## Solution 2: Divide and Conquer (Optimal)

### Key Insight

> **The Trick:** After finding the minimum distance d in left and right halves, we only need to check points within distance d of the dividing line. Furthermore, for each point in this strip, we only need to check at most 7 other points!

### Algorithm

1. Sort points by x-coordinate
2. Recursively find minimum distance in left and right halves
3. Let d = min(left_min, right_min)
4. Build a "strip" of points within distance d of the middle x-coordinate
5. Sort strip by y-coordinate
6. For each point in strip, only compare with next 7 points (they are sorted by y)
7. Return the overall minimum

### Why Only 7 Points?

```
Consider a d x 2d rectangle around the dividing line:

         d       d
    +----+------+----+
    |    |      |    |
  d |  L |      |  R |
    |    |      |    |
    +----+------+----+
    |    |      |    |
  d |  L |      |  R |
    |    |      |    |
    +----+------+----+
         ^
     dividing line

Each d x d square can contain at most 4 points (any more would have
distance < d within that half, contradicting our found minimum d).
So the 2d x d rectangle contains at most 8 points including the
current point, meaning at most 7 other points to check.
```

### Dry Run Example

Let's trace through with points: `[(2,3), (12,30), (40,50), (5,1), (12,10), (3,4)]`

```
Step 1: Sort by x-coordinate
  Sorted: [(2,3), (3,4), (5,1), (12,10), (12,30), (40,50)]

Step 2: Divide at middle
  Left half:  [(2,3), (3,4), (5,1)]
  Right half: [(12,10), (12,30), (40,50)]
  Mid x = 5

Step 3: Recursive calls
  Left minimum:  (2,3) to (3,4) = 1+1 = 2
  Right minimum: (12,10) to (12,30) = 0+400 = 400
  d = min(2, 400) = 2, sqrt(d) ~ 1.41

Step 4: Build strip (points with |x - 5| < sqrt(2) ~ 1.41)
  Strip candidates: [(5,1)] only (others too far)

Step 5: Check strip pairs
  Only 1 point in strip, no pairs to check

Result: 2 (squared distance between (2,3) and (3,4))
```

### Visual Diagram

```
Points plotted:
                      (12,30)
                         *



  (3,4)               (12,10)
    *                    *
  (2,3)
    *
        (5,1)                        (40,50)
          *                              *

  --------|-------- dividing line at x=5

  LEFT    |    RIGHT
```

### Code

```python
import sys
from functools import cmp_to_key
sys.setrecursionlimit(300000)

def solve():
    n = int(input())
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))

    def dist_sq(p1, p2):
        """Calculate squared Euclidean distance."""
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return dx * dx + dy * dy

    def closest_in_strip(strip, d):
        """Find minimum distance in strip, given current minimum d."""
        min_d = d
        strip.sort(key=lambda p: p[1])  # Sort by y

        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j][1] - strip[i][1])**2 < min_d:
                min_d = min(min_d, dist_sq(strip[i], strip[j]))
                j += 1
        return min_d

    def closest_pair(pts):
        """Divide and conquer to find closest pair."""
        n = len(pts)

        # Base case: brute force for small inputs
        if n <= 3:
            min_d = float('inf')
            for i in range(n):
                for j in range(i + 1, n):
                    min_d = min(min_d, dist_sq(pts[i], pts[j]))
            return min_d

        mid = n // 2
        mid_x = pts[mid][0]

        # Recursively find minimum in each half
        left_min = closest_pair(pts[:mid])
        right_min = closest_pair(pts[mid:])
        d = min(left_min, right_min)

        # Build strip of points close to dividing line
        strip = [p for p in pts if (p[0] - mid_x)**2 < d]

        # Find minimum in strip
        return closest_in_strip(strip, d)

    # Sort by x-coordinate
    points.sort()
    print(closest_pair(points))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log^2 n) | T(n) = 2T(n/2) + O(n log n) for strip sorting |
| Space | O(n) | Recursion stack and strip storage |

**Note:** Can be optimized to O(n log n) by maintaining a y-sorted list alongside x-sorted list, avoiding re-sorting the strip each time.

---

## Common Mistakes

### Mistake 1: Using Floating-Point Distance

```python
# WRONG - floating point precision issues
import math
dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
```

**Problem:** Floating-point arithmetic can introduce precision errors.
**Fix:** Use squared distances throughout and only output the squared result.

### Mistake 2: Checking All Points in Strip

```python
# WRONG - defeats purpose of algorithm
for i in range(len(strip)):
    for j in range(i+1, len(strip)):  # No early termination!
        min_d = min(min_d, dist_sq(strip[i], strip[j]))
```

**Problem:** This is O(n^2) in the strip, losing the efficiency gain.
**Fix:** Sort strip by y and only check while y-difference squared is less than current minimum.

### Mistake 3: Integer Overflow

**Problem:** With coordinates up to 10^9, dx^2 can reach 10^18, exceeding int range.
**Fix:** Use `long long` for all distance calculations.

### Mistake 4: Wrong Strip Condition

```python
# WRONG - using d instead of sqrt(d)
strip = [p for p in pts if abs(p[0] - mid_x) < d]
```

**Problem:** d is the squared distance, but x-difference should be compared to sqrt(d).
**Fix:** Compare (p[0] - mid_x)^2 < d, or take sqrt of d for the comparison.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Two points | `n=2, (0,0), (3,4)` | 25 | Only one pair, distance = 3^2 + 4^2 |
| Coincident points | `n=2, (5,5), (5,5)` | 0 | Same point, distance = 0 |
| All collinear | `n=4` on y=x line | min adjacent | Adjacent points are closest |
| Large coordinates | 10^9 values | Use long long | Prevent overflow |
| Points on axes | All x=0 or y=0 | Standard algorithm | Works normally |

---

## When to Use This Pattern

### Use Divide and Conquer Closest Pair When:
- Finding minimum distance between any two points in 2D
- Large number of points (n > 1000) where O(n^2) is too slow
- Need O(n log n) or O(n log^2 n) complexity

### Simpler Alternatives:
- **Small n (< 1000):** Brute force O(n^2) is fine
- **Points on a grid with small range:** Use spatial hashing
- **Only need approximate answer:** Use randomized algorithms

### Pattern Recognition Checklist:
- [ ] Finding closest/minimum distance between point pairs? This is likely it
- [ ] Large n requiring subquadratic time? Consider divide and conquer
- [ ] Geometric problem with sortable coordinates? D&C often applies

---

## Related Problems

### CSES Geometry Problems

| Problem | Link | Relationship |
|---------|------|--------------|
| Point Location Test | [CSES 2189](https://cses.fi/problemset/task/2189) | Basic geometry |
| Line Segment Intersection | [CSES 2190](https://cses.fi/problemset/task/2190) | Line geometry |
| Convex Hull | [CSES 2195](https://cses.fi/problemset/task/2195) | D&C in geometry |

### Similar Problems

| Problem | Key Difference |
|---------|----------------|
| K Closest Points to Origin (LC 973) | Distance from fixed point, not between pairs |
| Closest Pair in 3D | Extend to 3 dimensions |

---

## Key Takeaways

1. **The Core Idea:** Divide and conquer reduces O(n^2) to O(n log^2 n) by exploiting geometric properties.
2. **The Strip Insight:** Only 7 points need to be checked for each strip point.
3. **Avoid Float Errors:** Use squared distances to avoid precision issues.
4. **Integer Overflow:** With large coordinates, use 64-bit integers.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why only 7 points need checking in the strip
- [ ] Implement the algorithm without looking at the solution
- [ ] Handle the base case correctly (n <= 3)
- [ ] Avoid integer overflow with large coordinates
- [ ] Understand the O(n log^2 n) time complexity derivation

---

## Additional Resources

- [CP-Algorithms: Closest Pair of Points](https://cp-algorithms.com/geometry/nearest_points.html)
- [Computational Geometry - Closest Pair](https://en.wikipedia.org/wiki/Closest_pair_of_points_problem)
- [CSES Minimum Euclidean Distance](https://cses.fi/problemset/task/2194) - Closest pair of points
