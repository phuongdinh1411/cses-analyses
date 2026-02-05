---
layout: simple
title: "Line Segment Intersection - Geometry Problem"
permalink: /problem_soulutions/geometry/lines_and_queries_i_analysis
difficulty: Hard
tags: [convex-hull-trick, geometry, line-queries, optimization]
---

# Line Segment Intersection (Convex Hull Trick)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Geometry / Data Structures |
| **Time Limit** | 1 second |
| **Key Technique** | Convex Hull Trick |
| **CSES Link** | [Line Segment Intersection](https://cses.fi/problemset/task/2189) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand when the Convex Hull Trick (CHT) pattern applies
- [ ] Implement a convex hull data structure for line queries
- [ ] Determine when a line becomes useless and can be removed
- [ ] Apply CHT to optimize DP problems with linear transitions

---

## Problem Statement

**Problem:** Given n lines of the form y = mx + b, answer q queries. Each query gives an x-coordinate, and you must find the minimum (or maximum) y-value among all lines at that x.

**Input:**
- Line 1: Two integers n and q (number of lines and queries)
- Next n lines: Two integers m and b (slope and y-intercept of each line)
- Next q lines: One integer x (query x-coordinate)

**Output:**
- For each query, print the minimum y-value at x

**Constraints:**
- 1 <= n, q <= 2 * 10^5
- -10^9 <= m, b, x <= 10^9

### Example

```
Input:
3 4
1 3
2 1
-1 4

Output:
1
0
4
-2
```

**Explanation:** Lines: y = x + 3, y = 2x + 1, y = -x + 4. For query x=0: min(3, 1, 4) = 1.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When you have multiple lines and need to find the minimum y-value at various x-coordinates, how can you avoid checking all lines for each query?

The insight is that only lines on the **lower envelope** can give the minimum. Lines always dominated by others can be ignored.

### Breaking Down the Problem

1. **What are we looking for?** The minimum y-value among all lines at a given x
2. **What information do we have?** n lines defined by slope and intercept
3. **What's the relationship?** At different x-values, different lines achieve the minimum

Think of this like a city skyline from below - you only see the lowest roofs at each position.

---

## Solution 1: Brute Force

### Idea

For each query, evaluate all n lines and find the minimum.

### Algorithm

1. For each query x
2. Compute y = m*x + b for all lines
3. Return the minimum y

### Code

```python
def solve_brute_force(lines, queries):
 """
 Brute force: check all lines for each query.

 Time: O(n * q)
 Space: O(1)
 """
 results = []
 for x in queries:
  min_y = float('inf')
  for m, b in lines:
   y = m * x + b
   min_y = min(min_y, y)
  results.append(min_y)
 return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * q) | Check all n lines for each of q queries |
| Space | O(1) | Only store current minimum |

### Why This Works (But Is Slow)

Correctness is guaranteed since we check every line. However, with n, q up to 2*10^5, this gives 4*10^10 operations - far too slow.

---

## Solution 2: Convex Hull Trick (Optimal)

### Key Insight

> **The Trick:** Maintain only the lines that form the lower envelope. A line is useless if it's never the minimum for any x-coordinate.

### When Can We Remove a Line?

Consider three lines L1, L2, L3 sorted by slope. L2 is useless if the intersection of L1 and L3 is below or at the intersection of L1 and L2.

```
         L3
        /
    L2 /
   ---/----
  L1 /
    /

If L1 and L3 intersect before L1 and L2, then L2 is never optimal.
```

### Algorithm

1. Sort lines by slope
2. Add lines one by one, removing lines that become useless
3. For queries, binary search to find the optimal line

### Intersection Point Calculation

For lines y = m1*x + b1 and y = m2*x + b2:
```
m1*x + b1 = m2*x + b2
x = (b2 - b1) / (m1 - m2)
```

### Dry Run Example

Let's trace through with lines: (1, 3), (2, 1), (-1, 4)

```
Step 1: Sort by slope
  Lines: [(-1, 4), (1, 3), (2, 1)]
  Meaning: y = -x + 4, y = x + 3, y = 2x + 1

Step 2: Build convex hull

  Add L1: y = -x + 4
  Hull: [(-1, 4)]

  Add L2: y = x + 3
  Intersection L1-L2: x = (3-4)/(-1-1) = 0.5
  Hull: [(-1, 4), (1, 3)]

  Add L3: y = 2x + 1
  Intersection L2-L3: x = (1-3)/(1-2) = 2
  Check if L2 is still useful:
    L1-L3 intersection: x = (1-4)/(-1-2) = 1
    Since 1 < 2, L2 is still useful
  Hull: [(-1, 4), (1, 3), (2, 1)]

Step 3: Answer queries using binary search
  Query x=0:
    Check y = -0+4=4, y = 0+3=3, y = 0+1=1
    Binary search finds line (2,1), answer = 1
```

### Visual Diagram

```
y
^

|  \
| 4 \  L1: y = -x + 4

|    \
| 3   \   /

|      \ / L2: y = x + 3
|       X

|      / \
| 1   /   \

|    /  L3: y = 2x + 1
|   /
+--+--+--+--+---> x
   0  1  2  3

Lower envelope: Uses L1 for x < 0.5, L2 for 0.5 < x < 2, L3 for x > 2
```

### Code

```python
class ConvexHullTrick:
 """
 Convex Hull Trick for minimum line queries.
 Lines must be added in order of increasing slope.
 """
 def __init__(self):
  self.lines = []  # List of (slope, intercept)

 def bad(self, l1, l2, l3):
  """
  Check if l2 is useless given l1 and l3.
  Returns True if l1-l3 intersection is at or before l1-l2 intersection.
  """
  # Intersection of l1 and l2: x = (b2-b1)/(m1-m2)
  # Intersection of l1 and l3: x = (b3-b1)/(m1-m3)
  # l2 is bad if x13 <= x12
  # (b3-b1)/(m1-m3) <= (b2-b1)/(m1-m2)
  # Cross multiply (careful with signs):
  return (l3[1] - l1[1]) * (l1[0] - l2[0]) <= (l2[1] - l1[1]) * (l1[0] - l3[0])

 def add_line(self, m, b):
  """Add line y = mx + b. Must be called with increasing slopes."""
  line = (m, b)
  while len(self.lines) >= 2 and self.bad(self.lines[-2], self.lines[-1], line):
   self.lines.pop()
  self.lines.append(line)

 def query(self, x):
  """Find minimum y value at x using binary search."""
  if not self.lines:
   return float('inf')

  lo, hi = 0, len(self.lines) - 1
  while lo < hi:
   mid = (lo + hi) // 2
   m1, b1 = self.lines[mid]
   m2, b2 = self.lines[mid + 1]
   if m1 * x + b1 > m2 * x + b2:
    lo = mid + 1
   else:
    hi = mid

  m, b = self.lines[lo]
  return m * x + b


def solve_cht(lines, queries):
 """
 Optimal solution using Convex Hull Trick.

 Time: O(n log n + q log n)
 Space: O(n)
 """
 # Sort lines by slope
 sorted_lines = sorted(lines, key=lambda x: x[0])

 cht = ConvexHullTrick()
 for m, b in sorted_lines:
  cht.add_line(m, b)

 results = []
 for x in queries:
  results.append(cht.query(x))

 return results
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n + q log n) | Sort lines + binary search per query |
| Space | O(n) | Store lines in convex hull |

---

## Common Mistakes

### Mistake 1: Integer Overflow in Intersection Check

**Problem:** With values up to 10^9, multiplication can overflow 64-bit integers.
**Fix:** Use __int128 in C++ or careful division in Python.

### Mistake 2: Not Sorting Lines by Slope

```python
# WRONG - adding lines in arbitrary order
for m, b in lines:
 cht.add_line(m, b)

# CORRECT - sort first
sorted_lines = sorted(lines, key=lambda x: x[0])
for m, b in sorted_lines:
 cht.add_line(m, b)
```

**Problem:** The CHT algorithm requires lines in slope order.
**Fix:** Always sort by slope before adding.

### Mistake 3: Wrong Comparison Direction for Maximum

```python
# For MINIMUM queries
if m1 * x + b1 > m2 * x + b2:
 lo = mid + 1

# For MAXIMUM queries - flip the comparison!
if m1 * x + b1 < m2 * x + b2:
 lo = mid + 1
```

**Problem:** The binary search direction depends on whether you want min or max.
**Fix:** Flip comparison and maintain upper envelope for maximum queries.

---

## Edge Cases

| Case | Input | Notes |
|------|-------|-------|
| Single line | n=1 | Only one line, always return its value |
| Parallel lines | Same slope, different intercepts | Only keep the one with smallest intercept |
| All queries same x | Multiple queries at x=0 | Same answer for all |
| Negative slopes | m < 0 | Order matters: -3 < -1 < 0 < 1 |
| Large coordinates | x = 10^9 | Watch for overflow in y = mx + b |

---

## When to Use This Pattern

### Use Convex Hull Trick When:
- You need min/max of linear functions at various points
- DP transitions have the form: dp[i] = min(dp[j] + cost(j, i)) where cost is linear in j
- You have many lines and many queries

### Don't Use When:
- Lines are added in arbitrary slope order and queries are online (use Li Chao Tree instead)
- You only have a few lines or queries (brute force is fine)
- The functions are not linear

### Pattern Recognition Checklist:
- [ ] Looking for min/max of linear functions? **Consider CHT**
- [ ] DP with transition dp[i] = min(A[j] * B[i] + C[j])? **CHT applies**
- [ ] Need to handle online queries with arbitrary order? **Use Li Chao Tree**

---

## Related Problems

| Difficulty | Problem | Notes |
|------------|---------|-------|
| Similar | [Line Segment Intersection](https://cses.fi/problemset/task/2189) | Direct CHT application |
| Similar | [Polygon Area](https://cses.fi/problemset/task/2191) | Related geometry |
| Harder | Li Chao Segment Tree | Handles arbitrary insertion order |

---

## Key Takeaways

1. **The Core Idea:** Maintain only lines on the lower/upper envelope; others are never optimal
2. **Time Optimization:** From O(nq) brute force to O(n log n + q log n) with CHT
3. **Space Trade-off:** O(n) space to store the convex hull
4. **Pattern:** Convex Hull Trick is essential for optimizing linear DP transitions

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement CHT from scratch without looking at the solution
- [ ] Explain why some lines can be removed
- [ ] Recognize DP problems that can use CHT optimization
- [ ] Handle both minimum and maximum query variants

---

## Additional Resources

- [CP-Algorithms: Convex Hull Trick](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- [CSES Convex Hull](https://cses.fi/problemset/task/2195) - Related geometry with CHT
- [Li Chao Tree Tutorial](https://cp-algorithms.com/geometry/line_operations.html)
