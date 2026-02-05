---
layout: simple
title: "Flowers - Weighted LIS with Segment Tree"
permalink: /problem_soulutions/dynamic_programming_at/flowers_analysis
difficulty: Medium
tags: [dp, segment-tree, coordinate-compression, lis]
---

# Flowers

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | Weighted LIS + Segment Tree |
| **Problem Link** | [AtCoder DP Contest - Q](https://atcoder.jp/contests/dp/tasks/dp_q) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize weighted LIS problems and distinguish them from standard LIS
- [ ] Apply segment trees for DP optimization with range max queries
- [ ] Use coordinate compression to handle large value ranges
- [ ] Understand the connection between LIS and range query data structures

---

## Problem Statement

**Problem:** There are N flowers arranged in a row. Flower i has height h[i] and beauty value a[i]. You want to pick some flowers such that their heights form a strictly increasing sequence from left to right. Find the maximum total beauty you can achieve.

**Input:**
- Line 1: N (number of flowers)
- Line 2: h[1], h[2], ..., h[N] (heights)
- Line 3: a[1], a[2], ..., a[N] (beauty values)

**Output:**
- Maximum total beauty of picked flowers

**Constraints:**
- 1 <= N <= 2 x 10^5
- 1 <= h[i] <= N (all heights are distinct)
- 1 <= a[i] <= 10^9

### Example

```
Input:
4
3 1 4 2
10 20 30 40

Output:
60
```

**Explanation:** Pick flowers at positions 2 and 3 (heights 1 and 4, beauties 20 and 30). The heights [1, 4] are strictly increasing, and total beauty is 20 + 30 = 60. Alternatively, picking flowers at positions 2 and 4 gives heights [1, 2] with beauty 20 + 40 = 60.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** This is essentially a weighted Longest Increasing Subsequence (LIS) problem. Instead of maximizing the length of an increasing sequence, we maximize the sum of weights (beauties) along an increasing sequence.

Standard LIS finds the longest increasing subsequence, which is equivalent to assigning weight 1 to each element. Here, each element has a custom weight (beauty), making it a weighted LIS problem.

### Breaking Down the Problem

1. **What are we looking for?** Maximum sum of beauties for flowers with strictly increasing heights.
2. **What information do we have?** For each flower: position, height, and beauty value.
3. **What's the relationship between input and output?** We need to find an increasing subsequence of heights that maximizes beauty sum.

### Why Standard LIS O(n log n) Doesn't Work

The classic binary search LIS algorithm tracks the smallest ending element for each length. For weighted LIS, we can't simply track by length - we need to track by the maximum achievable beauty for each ending height.

### The Key Insight

For each flower i at height h[i]:
```
dp[i] = a[i] + max(dp[j]) for all j where h[j] < h[i] and j < i
```

We need to efficiently query "what's the maximum dp value among all previous flowers with height < h[i]?" This is a **range maximum query** - perfect for a segment tree!

---

## Solution 1: Brute Force (O(n^2))

### Idea

For each flower, check all previous flowers with smaller heights and take the maximum.

### Algorithm

1. For each flower i from left to right
2. Check all flowers j < i where h[j] < h[i]
3. dp[i] = a[i] + max(dp[j]) for valid j
4. Track global maximum

### Code

```python
def solve_brute_force(n, heights, beauties):
  """
  Brute force O(n^2) solution.

  Time: O(n^2)
  Space: O(n)
  """
  dp = [0] * n

  for i in range(n):
    max_prev = 0
    for j in range(i):
      if heights[j] < heights[i]:
        max_prev = max(max_prev, dp[j])
    dp[i] = beauties[i] + max_prev

  return max(dp)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Nested loops checking all pairs |
| Space | O(n) | DP array |

### Why This Works (But Is Slow)

For N = 2 x 10^5, O(n^2) means 4 x 10^10 operations - far too slow. We need a data structure to speed up the range maximum query.

---

## Solution 2: Optimal - Segment Tree (O(n log n))

### Key Insight

> **The Trick:** Use a segment tree indexed by height values to answer "maximum dp value for heights in range [0, h-1]" in O(log n).

Since we process flowers left to right, when we reach flower i, the segment tree contains dp values only for flowers we've already processed (j < i). Querying range [0, h[i]-1] gives us exactly what we need.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[h]` | Maximum beauty achievable ending with a flower of height h |

**In plain English:** The segment tree at position h stores the best total beauty we can get if we end our sequence at height h.

### State Transition

```
For flower i with height h[i] and beauty a[i]:
    best_prev = segment_tree.query(0, h[i] - 1)  // max in range [0, h[i]-1]
    dp[h[i]] = a[i] + best_prev
    segment_tree.update(h[i], dp[h[i]])
```

**Why?** We can only extend sequences that end at heights strictly less than h[i]. The segment tree efficiently finds the maximum among all such sequences.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| Initial tree | All 0s | No flowers picked yet means 0 beauty |

### Algorithm

1. Build a segment tree of size N (heights are in [1, N])
2. For each flower i from left to right:
   - Query max value in range [0, h[i]-1]
   - Update position h[i] with query_result + a[i]
   - Track global maximum
3. Return global maximum

### Dry Run Example

Let's trace through with input `N=4, heights=[3,1,4,2], beauties=[10,20,30,40]`:

```
Initial state:
  Segment tree: [0, 0, 0, 0, 0] (indices 0-4)
  answer = 0

Step 1: Process flower 0 (h=3, a=10)
  Query range [0, 2]: max = 0
  dp[3] = 10 + 0 = 10
  Update tree[3] = 10
  Tree: [0, 0, 0, 10, 0]
  answer = max(0, 10) = 10

Step 2: Process flower 1 (h=1, a=20)
  Query range [0, 0]: max = 0
  dp[1] = 20 + 0 = 20
  Update tree[1] = 20
  Tree: [0, 20, 0, 10, 0]
  answer = max(10, 20) = 20

Step 3: Process flower 2 (h=4, a=30)
  Query range [0, 3]: max = 20 (from tree[1])
  dp[4] = 30 + 20 = 50
  Update tree[4] = 50
  Tree: [0, 20, 0, 10, 50]
  answer = max(20, 50) = 50

Step 4: Process flower 3 (h=2, a=40)
  Query range [0, 1]: max = 20 (from tree[1])
  dp[2] = 40 + 20 = 60
  Update tree[2] = 60
  Tree: [0, 20, 60, 10, 50]
  answer = max(50, 60) = 60

Final answer: 60
```

### Visual Diagram

```
Flowers:    F0      F1      F2      F3
Heights:     3       1       4       2
Beauties:   10      20      30      40

Processing order (left to right):

  F1 (h=1) -----> F3 (h=2) -----> can extend
     20             20+40=60

  F1 (h=1) -----> F2 (h=4) -----> can extend
     20             20+30=50

Best path: F1 -> F3 with total beauty 60
   or      F1 -> F2 with total beauty 50
```

### Code (Python)

```python
class SegmentTree:
  """Segment tree for range maximum queries and point updates."""

  def __init__(self, n):
    self.n = n
    self.size = 1
    while self.size < n:
      self.size *= 2
    self.tree = [0] * (2 * self.size)

  def update(self, pos, value):
    """Update position pos with value (keeping maximum)."""
    pos += self.size
    self.tree[pos] = max(self.tree[pos], value)
    while pos > 1:
      pos //= 2
      self.tree[pos] = max(self.tree[2 * pos], self.tree[2 * pos + 1])

  def query(self, left, right):
    """Query maximum in range [left, right)."""
    result = 0
    left += self.size
    right += self.size
    while left < right:
      if left & 1:
        result = max(result, self.tree[left])
        left += 1
      if right & 1:
        right -= 1
        result = max(result, self.tree[right])
      left //= 2
      right //= 2
    return result


def solve(n, heights, beauties):
  """
  Weighted LIS using segment tree.

  Time: O(n log n)
  Space: O(n)
  """
  seg_tree = SegmentTree(n + 1)
  answer = 0

  for i in range(n):
    h = heights[i]
    a = beauties[i]

    # Query max beauty for heights < h
    best_prev = seg_tree.query(0, h)
    current = a + best_prev

    # Update segment tree at position h
    seg_tree.update(h, current)
    answer = max(answer, current)

  return answer


# Read input and solve
def main():
  n = int(input())
  heights = list(map(int, input().split()))
  beauties = list(map(int, input().split()))
  print(solve(n, heights, beauties))


if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | n flowers, each with O(log n) query and update |
| Space | O(n) | Segment tree of size O(n) |

---

## Common Mistakes

### Mistake 1: Wrong Query Range

```python
# WRONG - includes current height
best_prev = seg_tree.query(0, h[i] + 1)

# CORRECT - strictly less than current height
best_prev = seg_tree.query(0, h[i])  # range [0, h[i]) excludes h[i]
```

**Problem:** Including h[i] in the query could match a previous flower of the same height.
**Fix:** Query range [0, h[i]) to get strictly smaller heights.

### Mistake 2: Integer Overflow

**Problem:** Beauty values up to 10^9 and N up to 2x10^5 means sum can reach 2x10^14.
**Fix:** Use 64-bit integers (long long in C++).

### Mistake 3: Forgetting to Track Global Maximum

```python
# WRONG - only updates tree, forgets to track answer
seg_tree.update(h[i], current)

# CORRECT - track global maximum
seg_tree.update(h[i], current)
answer = max(answer, current)
```

**Problem:** The answer might be at any height, not just the last one.
**Fix:** Maintain a running maximum across all updates.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single flower | N=1, h=[1], a=[100] | 100 | Pick the only flower |
| All same beauty | N=3, h=[2,1,3], a=[10,10,10] | 20 | Pick h=[1,3] for 2 flowers |
| Decreasing heights | N=3, h=[3,2,1], a=[10,20,30] | 30 | Can only pick one flower |
| Increasing heights | N=3, h=[1,2,3], a=[10,20,30] | 60 | Pick all flowers |
| Large beauty values | N=2, h=[1,2], a=[10^9,10^9] | 2x10^9 | Handle large sums |

---

## When to Use This Pattern

### Use This Approach When:
- You need to find an optimal increasing/decreasing subsequence with weights
- The recurrence involves range max/min/sum queries over previous states
- Heights/values are bounded or can be coordinate compressed
- Standard O(n^2) DP is too slow

### Don't Use When:
- Standard LIS (unweighted) - use binary search O(n log n)
- Values are too large even after compression - consider other structures
- Problem requires actual subsequence reconstruction (need additional bookkeeping)

### Pattern Recognition Checklist:
- [ ] Subsequence selection with ordering constraint? -> **Consider LIS variant**
- [ ] DP state depends on range query of previous states? -> **Consider segment tree**
- [ ] Need max/min over elements satisfying a condition? -> **Consider data structure optimization**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Longest Increasing Subsequence](https://atcoder.jp/contests/dp/tasks/dp_q) | Standard LIS, foundational concept |
| [Range Maximum Query](https://cses.fi/problemset/task/1647) | Practice segment tree basics |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Increasing Subsequence](https://cses.fi/problemset/task/1145) | Count LIS instead of weighted sum |
| [Tower of Hanoi](https://atcoder.jp/contests/dp/tasks/dp_x) | Similar DP optimization technique |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [LIS with Multiple Constraints](https://codeforces.com/problemset/problem/1682/D) | 2D constraints |
| [Weighted Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Interval scheduling variant |

---

## Key Takeaways

1. **The Core Idea:** Weighted LIS is standard LIS with element weights; optimize with segment tree for range max queries.
2. **Time Optimization:** Reduced from O(n^2) to O(n log n) by using segment tree for range queries.
3. **Space Trade-off:** O(n) space for segment tree enables logarithmic query time.
4. **Pattern:** DP with range query optimization - applicable whenever DP transition involves finding optimal value in a range.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why this is a weighted LIS problem
- [ ] Implement a segment tree for range max queries from scratch
- [ ] Trace through the algorithm on a small example
- [ ] Identify the key difference between weighted and unweighted LIS
- [ ] Solve this problem in under 15 minutes

---

## Additional Resources

- [AtCoder DP Contest - Problem Q](https://atcoder.jp/contests/dp/tasks/dp_q) - Original problem
- [CP-Algorithms: Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html) - Segment tree tutorial
- [CSES Increasing Subsequence](https://cses.fi/problemset/task/1145) - Similar LIS-based DP
