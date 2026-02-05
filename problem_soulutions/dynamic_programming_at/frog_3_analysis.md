---
layout: simple
title: "Frog 3 - Convex Hull Trick DP Optimization"
permalink: /problem_soulutions/dynamic_programming_at/frog_3_analysis
difficulty: Hard
tags: [dp, convex-hull-trick, optimization, li-chao-tree]
prerequisites: [frog_1, frog_2]
---

# Frog 3

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Dynamic Programming (Optimization) |
| **Time Limit** | 2 seconds |
| **Key Technique** | Convex Hull Trick / Li Chao Tree |
| **Problem Link** | [AtCoder DP Contest - Problem Z](https://atcoder.jp/contests/dp/tasks/dp_z) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when DP transitions can be optimized using Convex Hull Trick
- [ ] Transform quadratic DP recurrences into linear form (mx + b)
- [ ] Implement Li Chao Tree for efficient line queries
- [ ] Reduce O(N^2) DP to O(N log N) using geometric optimization

---

## Problem Statement

**Problem:** There are N stones numbered 1 to N. Stone i has height h_i. A frog starts at stone 1 and wants to reach stone N. The frog can jump from stone i to any stone j where j > i. The cost of jumping from stone i to stone j is (h_i - h_j)^2 + C, where C is a constant. Find the minimum total cost to reach stone N.

**Input:**
- Line 1: Two integers N and C (number of stones and jump constant cost)
- Line 2: N integers h_1, h_2, ..., h_N (heights of stones)

**Output:**
- Single integer: minimum total cost to reach stone N from stone 1

**Constraints:**
- 2 <= N <= 2 x 10^5
- 1 <= C <= 10^12
- 1 <= h_i <= 10^6

### Example

```
Input:
5 6
1 2 3 4 5

Output:
20
```

**Explanation:**
- Optimal path: 1 -> 3 -> 5
- Cost from stone 1 to stone 3: (1-3)^2 + 6 = 4 + 6 = 10
- Cost from stone 3 to stone 5: (3-5)^2 + 6 = 4 + 6 = 10
- Total cost: 10 + 10 = 20

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** The naive DP has O(N^2) transitions. How can we recognize that Convex Hull Trick applies?

The key insight is that when we expand the cost formula (h_i - h_j)^2 and rearrange the DP recurrence, we get an expression that looks like evaluating a linear function mx + b at a specific point. When the DP transition has this form, Convex Hull Trick can optimize it.

### Breaking Down the Problem

1. **What are we looking for?** Minimum cost path from stone 1 to stone N.
2. **What information do we have?** Heights of all stones, constant cost C.
3. **What's the relationship between input and output?** dp[i] depends on all dp[j] for j < i, creating O(N^2) transitions.

### The Mathematical Transformation

Starting with: `dp[i] = min(dp[j] + (h_i - h_j)^2 + C)` for all j < i

Expand the squared term:
```
dp[i] = min(dp[j] + h_i^2 - 2*h_i*h_j + h_j^2 + C)
```

Rearrange to isolate terms depending on j:
```
dp[i] = h_i^2 + C + min(-2*h_j * h_i + (dp[j] + h_j^2))
                     |________|   |__________________|
                        slope m      intercept b
```

This is now: `dp[i] = h_i^2 + C + min(m*x + b)` where:
- **m (slope)** = -2 * h_j
- **b (intercept)** = dp[j] + h_j^2
- **x (query point)** = h_i

Each stone j defines a line. We query the minimum value at x = h_i.

---

## Solution 1: Brute Force DP

### Idea

Try all possible previous stones for each stone and take the minimum cost.

### Algorithm

1. Initialize dp[0] = 0 (starting stone has no cost)
2. For each stone i from 1 to N-1:
   - Try all stones j from 0 to i-1
   - dp[i] = min(dp[j] + (h[i] - h[j])^2 + C)
3. Return dp[N-1]

### Code

```python
def frog3_brute_force(n, c, heights):
  """
  Brute force O(N^2) solution.

  Time: O(N^2)
  Space: O(N)
  """
  INF = float('inf')
  dp = [INF] * n
  dp[0] = 0

  for i in range(1, n):
    for j in range(i):
      cost = dp[j] + (heights[i] - heights[j]) ** 2 + c
      dp[i] = min(dp[i], cost)

  return dp[n - 1]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N^2) | For each stone, check all previous stones |
| Space | O(N) | Store dp values for N stones |

### Why This Works (But Is Slow)

The solution correctly considers all possible paths but with N up to 2x10^5, O(N^2) = 4x10^10 operations exceeds time limits.

---

## Solution 2: Convex Hull Trick with Li Chao Tree

### Key Insight

> **The Trick:** Transform the DP recurrence into line queries. Each previous state j contributes a line. Query the minimum value at point h_i using a Li Chao Tree.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i]` | Minimum cost to reach stone i from stone 0 |

**In plain English:** dp[i] stores the cheapest way to get to stone i.

### State Transition

```
dp[i] = h_i^2 + C + query_min_line(h_i)

where each line has:
  slope m = -2 * h_j
  intercept b = dp[j] + h_j^2
```

**Why?** We transformed (h_i - h_j)^2 + dp[j] into a linear form that can be queried efficiently.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 0 | Starting stone, no cost incurred |

### Algorithm

1. Build a Li Chao Tree for range of possible x values (heights)
2. Add line for stone 0: slope = -2*h[0], intercept = h[0]^2
3. For each stone i from 1 to N-1:
   - Query minimum at x = h[i]
   - dp[i] = h[i]^2 + C + query_result
   - Add new line: slope = -2*h[i], intercept = dp[i] + h[i]^2
4. Return dp[N-1]

### Li Chao Tree Explained

A Li Chao Tree is a segment tree variant that:
- Stores lines (not values) at each node
- Supports O(log N) line insertion
- Supports O(log N) minimum query at any point

At each node, we keep the "winner" line for the midpoint and recursively handle cases where a different line might be better in the left or right half.

### Dry Run Example

Let's trace through with input `N = 5, C = 6, heights = [1, 2, 3, 4, 5]`:

```
Initial state:
  dp = [0, INF, INF, INF, INF]
  Li Chao Tree: empty

Step 0: Process stone 0 (h=1)
  dp[0] = 0 (base case)
  Add line: m = -2*1 = -2, b = 0 + 1^2 = 1
  Line: y = -2x + 1

Step 1: Process stone 1 (h=2)
  Query at x=2: y = -2*2 + 1 = -3
  dp[1] = 2^2 + 6 + (-3) = 4 + 6 - 3 = 7
  Add line: m = -2*2 = -4, b = 7 + 4 = 11
  Line: y = -4x + 11

Step 2: Process stone 2 (h=3)
  Query at x=3:
    Line 1: y = -2*3 + 1 = -5
    Line 2: y = -4*3 + 11 = -1
    Minimum = -5
  dp[2] = 3^2 + 6 + (-5) = 9 + 6 - 5 = 10
  Add line: m = -6, b = 10 + 9 = 19
  Line: y = -6x + 19

Step 3: Process stone 3 (h=4)
  Query at x=4:
    Line 1: y = -2*4 + 1 = -7
    Line 2: y = -4*4 + 11 = -5
    Line 3: y = -6*4 + 19 = -5
    Minimum = -7
  dp[3] = 4^2 + 6 + (-7) = 16 + 6 - 7 = 15
  Add line: m = -8, b = 15 + 16 = 31

Step 4: Process stone 4 (h=5)
  Query at x=5:
    Line 1: y = -2*5 + 1 = -9
    Line 2: y = -4*5 + 11 = -9
    Line 3: y = -6*5 + 19 = -11
    Line 4: y = -8*5 + 31 = -9
    Minimum = -11
  dp[4] = 5^2 + 6 + (-11) = 25 + 6 - 11 = 20

Answer: dp[4] = 20
```

### Visual Diagram

```
Heights:    1     2     3     4     5
            |     |     |     |     |
Stone:      0     1     2     3     4

Optimal Path: 0 -----> 2 -----> 4

Cost:       0    10+10=20

Lines added to Li Chao Tree:
  After stone 0: y = -2x + 1
  After stone 1: y = -4x + 11
  After stone 2: y = -6x + 19
  After stone 3: y = -8x + 31
```

### Code (Python)

```python
class LiChaoTree:
  """
  Li Chao Tree for minimum line queries.
  Supports: add line y = mx + b, query min value at x.
  """
  def __init__(self, x_coords):
    """Initialize with possible x coordinates."""
    self.xs = sorted(set(x_coords))
    self.n = len(self.xs)
    self.size = 1
    while self.size < self.n:
      self.size *= 2
    # Each node stores (slope, intercept) or None
    self.lines = [None] * (2 * self.size)

  def _eval(self, line, x):
    """Evaluate line at point x. Returns inf if no line."""
    if line is None:
      return float('inf')
    m, b = line
    return m * x + b

  def add_line(self, m, b):
    """Add line y = mx + b to the tree."""
    self._update((m, b), 1, 0, self.n)

  def _update(self, line, node, left, right):
    """Recursively insert line into tree."""
    if right <= left:
      return
    if right - left == 1:
      # Leaf node: keep better line at this x
      if self._eval(line, self.xs[left]) < self._eval(self.lines[node], self.xs[left]):
        self.lines[node] = line
      return

    mid = (left + right) // 2
    mid_x = self.xs[mid]

    # Compare at midpoint
    if self._eval(line, mid_x) < self._eval(self.lines[node], mid_x):
      line, self.lines[node] = self.lines[node], line

    # Recurse to appropriate half
    if left < mid and self._eval(line, self.xs[left]) < self._eval(self.lines[node], self.xs[left]):
      self._update(line, 2 * node, left, mid)
    elif mid < right:
      self._update(line, 2 * node + 1, mid, right)

  def query(self, x):
    """Query minimum y value at point x."""
    # Binary search to find position
    pos = 0
    lo, hi = 0, self.n - 1
    while lo <= hi:
      m = (lo + hi) // 2
      if self.xs[m] <= x:
        pos = m
        lo = m + 1
      else:
        hi = m - 1
    return self._query(x, 1, 0, self.n)

  def _query(self, x, node, left, right):
    """Recursively query minimum at x."""
    if right <= left or node >= 2 * self.size:
      return float('inf')

    result = self._eval(self.lines[node], x)

    if right - left == 1:
      return result

    mid = (left + right) // 2
    if x < self.xs[min(mid, self.n - 1)]:
      return min(result, self._query(x, 2 * node, left, mid))
    else:
      return min(result, self._query(x, 2 * node + 1, mid, right))


def frog3_cht(n, c, heights):
  """
  Convex Hull Trick solution using Li Chao Tree.

  Time: O(N log N)
  Space: O(N)
  """
  tree = LiChaoTree(heights)
  dp = [0] * n

  # Add line for stone 0: m = -2*h[0], b = dp[0] + h[0]^2 = h[0]^2
  tree.add_line(-2 * heights[0], heights[0] ** 2)

  for i in range(1, n):
    h = heights[i]
    # Query minimum at x = h[i]
    min_val = tree.query(h)
    dp[i] = h * h + c + min_val
    # Add new line for stone i
    tree.add_line(-2 * h, dp[i] + h * h)

  return dp[n - 1]


# Main solution for competitive programming
def main():
  import sys
  input_data = sys.stdin.read().split()
  idx = 0
  n, c = int(input_data[idx]), int(input_data[idx + 1])
  idx += 2
  heights = [int(input_data[idx + i]) for i in range(n)]
  print(frog3_cht(n, c, heights))


if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N log N) | N insertions and queries, each O(log N) |
| Space | O(N) | Li Chao Tree and dp array |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** h_i up to 10^6 means h_i^2 up to 10^12, and C up to 10^12. Total can exceed int range.
**Fix:** Use 64-bit integers (long long in C++, int in Python handles this automatically).

### Mistake 2: Wrong Line Formula

```python
# WRONG - incorrect transformation
tree.add_line(-2 * h[i], dp[i])  # Missing h[i]^2 in intercept

# CORRECT
tree.add_line(-2 * h[i], dp[i] + h[i] * h[i])
```

**Problem:** The mathematical derivation requires intercept = dp[j] + h[j]^2.
**Fix:** Carefully follow the algebra when transforming the recurrence.

### Mistake 3: Forgetting to Add First Line

```python
# WRONG - start loop from 0
for i in range(n):
  min_val = tree.query(h[i])
  dp[i] = ...  # No line exists for i=0!

# CORRECT - handle base case separately
dp[0] = 0
tree.add_line(-2 * h[0], h[0] * h[0])
for i in range(1, n):
  ...
```

**Problem:** Must add the line for stone 0 before querying for stone 1.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum N | `N=2, C=1, h=[1,2]` | 2 | (1-2)^2 + 1 = 2 |
| Same heights | `N=3, C=5, h=[3,3,3]` | 10 | Two jumps of cost 0+5 each |
| Increasing heights | `N=5, C=6, h=[1,2,3,4,5]` | 20 | Balance jump cost vs constant |
| Large C | `N=3, C=10^12, h=[1,2,3]` | 2*10^12 + 4 | Must make 2 jumps minimum |
| Single jump optimal | `N=2, C=10^12, h=[1,10^6]` | 10^12 + (10^6-1)^2 | Direct jump |

---

## When to Use This Pattern

### Use Convex Hull Trick When:
- DP transition has form: dp[i] = min/max(A[j] * B[i] + C[j]) for j < i
- The transition is quadratic but can be linearized
- Slopes are monotonic (enables simpler deque-based approach)
- Need to optimize from O(N^2) to O(N log N) or O(N)

### Don't Use When:
- DP transition cannot be written as linear function queries
- N is small enough that O(N^2) passes
- The problem structure doesn't fit line queries

### Pattern Recognition Checklist:
- [ ] Is the DP transition O(N^2) and too slow?
- [ ] Can you expand/rearrange to get form: constant * variable + constant?
- [ ] Are you finding min/max over linear functions?
- [ ] Do slopes have special properties (monotonic)?

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Frog 1](https://atcoder.jp/contests/dp/tasks/dp_a) | Basic frog jumping DP |
| [Frog 2](https://atcoder.jp/contests/dp/tasks/dp_b) | Frog jumping with k-step limit |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES - Minimizing Coins](https://cses.fi/problemset/task/1634) | Standard DP optimization |
| [CF - Covered Points Count](https://codeforces.com/problemset/problem/1000/C) | Sweep line technique |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [AtCoder DP - Z Frog 3](https://atcoder.jp/contests/dp/tasks/dp_z) | This problem |
| [USACO - Circular Barn](http://www.usaco.org/index.php?page=viewproblem2&cpid=626) | CHT with modular arithmetic |
| [CF - Kalila and Dimna](https://codeforces.com/problemset/problem/319/C) | Divide and conquer CHT |

---

## Key Takeaways

1. **The Core Idea:** Transform quadratic DP transitions into linear function queries by algebraic manipulation.
2. **Time Optimization:** O(N^2) reduced to O(N log N) using Li Chao Tree for line queries.
3. **Space Trade-off:** O(N) extra space for the tree structure, same as naive DP.
4. **Pattern:** Convex Hull Trick - a fundamental technique for optimizing DP with linear structures.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the line form (slope, intercept) from a quadratic DP recurrence
- [ ] Implement Li Chao Tree from scratch
- [ ] Recognize CHT-applicable problems by their structure
- [ ] Handle edge cases with large values and integer overflow
- [ ] Explain why this optimization works geometrically

---

## Additional Resources

- [CP-Algorithms: Convex Hull Trick](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- [AtCoder DP Contest](https://atcoder.jp/contests/dp)
- [USACO Guide: Convex Hull Trick](https://usaco.guide/plat/convex-hull-trick)
