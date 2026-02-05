---
layout: simple
title: "Minimum Euclidean Distance - Geometry Problem"
permalink: /problem_soulutions/geometry/all_manhattan_distances_analysis
difficulty: Medium
tags: [geometry, sorting, prefix-sums, divide-and-conquer]
---

# Minimum Euclidean Distance

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Sorting + Prefix Sums |
| **CSES Link** | [Minimum Euclidean Distance](https://cses.fi/problemset/task/2194) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the decomposition technique to separate x and y contributions in Manhattan distance
- [ ] Use sorting and prefix sums to compute pairwise distance sums in O(n log n)
- [ ] Understand how to transform O(n^2) pairwise computations into O(n) using prefix sums
- [ ] Handle large sums with appropriate data types to avoid overflow

---

## Problem Statement

**Problem:** Given n points in a 2D plane, calculate the sum of Manhattan distances between all pairs of points.

The Manhattan distance between points (x1, y1) and (x2, y2) is |x1 - x2| + |y1 - y2|.

**Input:**
- Line 1: Integer n (number of points)
- Lines 2 to n+1: Two integers x and y (coordinates of each point)

**Output:**
- Single integer: the sum of Manhattan distances between all pairs

**Constraints:**
- 1 <= n <= 2 * 10^5
- -10^9 <= x, y <= 10^9

### Example

```
Input:
3
0 0
1 1
2 2

Output:
8

Explanation:
Pair (0,0)-(1,1): |0-1| + |0-1| = 2
Pair (0,0)-(2,2): |0-2| + |0-2| = 4
Pair (1,1)-(2,2): |1-2| + |1-2| = 2
Total: 2 + 4 + 2 = 8
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we avoid computing O(n^2) pairwise distances?

The crucial insight is that Manhattan distance is **separable**: the distance |x1-x2| + |y1-y2| can be computed as the sum of x-coordinate differences plus y-coordinate differences. This means we can compute the total x-contribution and y-contribution independently.

### Breaking Down the Problem

1. **What are we computing?** Sum of |xi - xj| + |yi - yj| for all pairs i < j
2. **Key observation:** This equals (sum of |xi - xj| for all pairs) + (sum of |yi - yj| for all pairs)
3. **1D problem:** We only need to solve: given n numbers, find sum of |ai - aj| for all pairs

### The 1D Subproblem

If we sort the numbers, we can use a clever counting technique:
- For a sorted array, |ai - aj| = aj - ai when i < j
- Each element contributes based on how many elements are before/after it

---

## Solution 1: Brute Force

### Idea

Compute Manhattan distance for every pair and sum them up.

### Code

```python
def solve_brute_force(n, points):
    """
    Brute force: compute all pairwise distances.
    Time: O(n^2), Space: O(1)
    """
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            total += dist
    return total
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Check all n*(n-1)/2 pairs |
| Space | O(1) | Only store running sum |

### Why This Works (But Is Slow)

Correctness is guaranteed by definition, but with n = 2*10^5, we'd need ~2*10^10 operations, which is far too slow.

---

## Solution 2: Optimal Solution (Sorting + Prefix Sums)

### Key Insight

> **The Trick:** Separate x and y contributions, then solve the 1D problem: "sum of pairwise absolute differences" using sorting.

For a **sorted** array a[0] <= a[1] <= ... <= a[n-1]:
- When computing sum of |a[i] - a[j]| for all pairs, element a[i] appears in two roles:
  - Subtracted by all elements after it: contributes -a[i] * (n - 1 - i) times
  - Subtracts all elements before it: contributes +a[i] * i times
- Net contribution of a[i] = a[i] * (i - (n - 1 - i)) = a[i] * (2*i - n + 1)

Alternatively, using prefix sums:
- For each element at index i, its contribution = a[i] * i - prefix_sum[i]

### Dry Run Example

Let's trace through with input `n = 3, points = [(0,0), (1,1), (2,2)]`:

```
Step 1: Extract x-coordinates: [0, 1, 2]
Step 2: Extract y-coordinates: [0, 1, 2]

Step 3: Compute sum of pairwise differences for x-coordinates
  Sorted x: [0, 1, 2]

  For i=0, x[0]=0: contributes 0 * 0 - 0 = 0
  For i=1, x[1]=1: contributes 1 * 1 - (0) = 1
  For i=2, x[2]=2: contributes 2 * 2 - (0+1) = 3

  X contribution = 0 + 1 + 3 = 4

Step 4: Same for y-coordinates
  Y contribution = 4

Step 5: Total = 4 + 4 = 8
```

### Visual Diagram

```
Points: (0,0), (1,1), (2,2)

Decompose Manhattan distances:
  |x1-x2| + |y1-y2|

X-coordinates: [0, 1, 2] (already sorted)

  Index:   0    1    2
  Value:   0    1    2
           |____|    |
              1      |
           |_________|
                 2

  Pairs: |0-1|=1, |0-2|=2, |1-2|=1
  Sum = 4

Y-coordinates: [0, 1, 2] (same in this example)
  Sum = 4

Total = 4 + 4 = 8
```

### Algorithm

1. Extract all x-coordinates and y-coordinates into separate arrays
2. Sort both arrays
3. Use prefix sums to compute sum of pairwise absolute differences for each array
4. Return the sum of both contributions

### Code

```python
def compute_pairwise_sum(coords):
    """
    Compute sum of |a[i] - a[j]| for all pairs i < j in a sorted array.

    For element at index i in sorted array:
    - It's subtracted by (n-1-i) elements after it
    - It subtracts i elements before it
    - Net contribution: coords[i] * (2*i - n + 1)

    Or equivalently with prefix sums:
    - contribution[i] = coords[i] * i - prefix_sum[i-1]
    """
    coords.sort()
    n = len(coords)
    total = 0
    prefix_sum = 0

    for i in range(n):
        # coords[i] is subtracted by all elements before (indices 0 to i-1)
        # So it contributes: coords[i] * i - sum(coords[0:i])
        total += coords[i] * i - prefix_sum
        prefix_sum += coords[i]

    return total


def solve(n, points):
    """
    Optimal solution using decomposition and prefix sums.
    Time: O(n log n), Space: O(n)
    """
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]

    return compute_pairwise_sum(x_coords) + compute_pairwise_sum(y_coords)


# Read input and solve
def main():
    n = int(input())
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    print(solve(n, points))


if __name__ == "__main__":
    main()
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Dominated by sorting |
| Space | O(n) | Store coordinate arrays |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** With coordinates up to 10^9 and n up to 2*10^5, products can exceed 32-bit integers.
**Fix:** Use 64-bit integers (long long in C++, Python handles this automatically).

### Mistake 2: Not Sorting Before Computing

```python
# WRONG - formula only works for sorted arrays
def wrong_approach(coords):
    total = 0
    prefix = 0
    for i, c in enumerate(coords):
        total += c * i - prefix  # Assumes sorted!
        prefix += c
    return total

# CORRECT - sort first
def correct_approach(coords):
    coords.sort()  # Essential!
    # ... rest of computation
```

**Problem:** The prefix sum formula assumes elements are in sorted order.
**Fix:** Always sort the coordinates first.

### Mistake 3: Forgetting to Handle Both Dimensions

```python
# WRONG - only computing x-contribution
def incomplete(points):
    x_coords = [p[0] for p in points]
    return compute_pairwise_sum(x_coords)

# CORRECT - sum both contributions
def complete(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    return compute_pairwise_sum(x_coords) + compute_pairwise_sum(y_coords)
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single point | n=1, [(0,0)] | 0 | No pairs exist |
| Two points | n=2, [(0,0), (3,4)] | 7 | Single pair: |3|+|4|=7 |
| Same point | n=2, [(5,5), (5,5)] | 0 | Distance is zero |
| Negative coords | n=2, [(-10^9,0), (10^9,0)] | 2*10^9 | Handle negative values |
| Large n | n=2*10^5 | (varies) | Must be O(n log n) |

---

## When to Use This Pattern

### Use This Approach When:
- Computing sum/average of pairwise distances or differences
- Manhattan distance or any separable distance metric
- The problem involves absolute differences of coordinates

### Don't Use When:
- You need individual pairwise distances (not just the sum)
- Using Euclidean distance (not separable like Manhattan)
- The distance metric is not decomposable by dimension

### Pattern Recognition Checklist:
- [ ] Computing sum over all pairs? Consider sorting + prefix sums
- [ ] Manhattan distance involved? Decompose into x and y components
- [ ] Need to avoid O(n^2)? Look for mathematical reformulation
- [ ] Absolute differences? Sorting often helps

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Sum of Two Values](https://cses.fi/problemset/task/1640) | Basic pair-finding with hash maps |
| [Nearest Smaller Values](https://cses.fi/problemset/task/1645) | Practice with stack-based techniques |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Line Segment Intersection](https://cses.fi/problemset/task/2190) | Different geometry technique |
| [Polygon Area](https://cses.fi/problemset/task/2191) | Coordinate geometry with different formula |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Convex Hull](https://cses.fi/problemset/task/2195) | More complex geometry algorithm |
| [Point in Polygon](https://cses.fi/problemset/task/2192) | Ray casting algorithm |

---

## Key Takeaways

1. **Decomposition:** Manhattan distance separates into independent x and y contributions
2. **Sorting + Prefix Sums:** Transform O(n^2) pairwise sums into O(n log n)
3. **Counting Technique:** Each sorted element contributes based on its position
4. **Overflow Prevention:** Always use 64-bit integers for distance problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why Manhattan distance is separable
- [ ] Derive the contribution formula for each element in sorted order
- [ ] Implement the solution in under 15 minutes
- [ ] Handle edge cases (n=1, negative coordinates, overflow)
- [ ] Apply this pattern to similar "sum of pairwise differences" problems

---

## Additional Resources

- [CP-Algorithms: Coordinate Compression](https://cp-algorithms.com/algebra/coordinate-compression.html)
- [CSES Convex Hull](https://cses.fi/problemset/task/2195) - Related geometry problem
- [Manhattan Distance Properties](https://en.wikipedia.org/wiki/Taxicab_geometry)
