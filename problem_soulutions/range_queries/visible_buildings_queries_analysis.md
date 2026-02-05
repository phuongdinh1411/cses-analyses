---
layout: simple
title: "Visible Buildings Queries - Range Queries Problem"
permalink: /problem_soulutions/range_queries/visible_buildings_queries_analysis
difficulty: Medium
tags: [range-queries, preprocessing, stack, monotonic-stack]
prerequisites: []
---

# Visible Buildings Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Preprocessing / Monotonic Stack |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Precompute answers for range queries to achieve O(1) query time
- [ ] Apply monotonic stack technique to visibility problems
- [ ] Recognize when preprocessing trades space for query efficiency
- [ ] Handle visibility queries from multiple positions efficiently

---

## Problem Statement

**Problem:** Given an array of building heights and multiple queries, each query asks for the number of visible buildings looking to the right from position i. A building at position j (j > i) is visible if it is strictly taller than all buildings between positions i and j.

**Input:**
- Line 1: n (number of buildings) and q (number of queries)
- Line 2: n integers representing building heights
- Next q lines: i (1-indexed position to query from)

**Output:**
- q lines: number of visible buildings from each query position

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= q <= 2 x 10^5
- 1 <= height[i] <= 10^9
- 1 <= i <= n

### Example

```
Input:
5 3
3 1 4 1 5
1
3
5

Output:
2
2
0
```

**Explanation:**
- Query 1 (position 1): Looking right from position 1, buildings at positions 3 (height=4) and 5 (height=5) are visible. Position 2 (height=1) is visible but blocked by position 3. Position 4 (height=1) is blocked by position 3. Answer: 2
- Query 2 (position 3): Looking right from position 3, building at position 5 (height=5) is visible. Position 4 (height=1) is blocked. Looking left, position 1 (height=3) is visible. Answer: 2 (bidirectional visibility)
- Query 3 (position 5): This is the last building, no buildings to see in either direction. Answer: 0

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we avoid recalculating visible buildings for every query?

The key insight is that the number of visible buildings from any position depends only on the heights to the right. If we precompute answers for all positions, each query becomes O(1).

### Breaking Down the Problem

1. **What are we looking for?** Count of buildings visible when looking right from position i
2. **What information do we have?** Building heights and query positions
3. **What's the relationship between input and output?** A building is visible if it creates a new maximum in the suffix

### Analogies

Think of this problem like standing in a line of people of different heights. Looking ahead, you can only see people who are taller than everyone between you and them. The tallest person blocks everyone shorter behind them.

---

## Solution 1: Brute Force

### Idea

For each query, scan all buildings to the right and count those that are visible (i.e., taller than all buildings seen so far).

### Algorithm

1. For each query position i
2. Initialize max_height = 0, count = 0
3. Scan from i+1 to n, if height > max_height, increment count and update max_height
4. Return count

### Code

```python
def solve_brute_force(n, heights, queries):
    """Brute force: process each query independently. Time: O(q*n)"""
    results = []
    for pos in queries:
        i, count, max_height = pos - 1, 0, 0
        for j in range(i + 1, n):
            if heights[j] > max_height:
                count += 1
                max_height = heights[j]
        results.append(count)
    return results
```

### Complexity

**Time:** O(q * n) - each query scans up to n elements
**Space:** O(1)

With q = n = 2x10^5, this gives 4x10^10 operations - far too slow.

---

## Solution 2: Optimal Solution with Preprocessing

### Key Insight

> **The Trick:** Precompute visible counts from every position. Since the answer for position i only depends on heights[i+1...n], we can compute all answers in O(n) time by processing right-to-left.

### Algorithm

1. Create array `visible[n]` to store answer for each position
2. Process from right to left using a monotonic stack
3. For each query, return precomputed answer in O(1)

### Right-to-Left Preprocessing

The visible count from position i equals the number of "steps" in the monotonic increasing sequence to the right. We can compute this efficiently:

```
visible[i] = number of distinct maximums in heights[i+1...n]
```

### Dry Run Example

Let's trace through with `heights = [3, 1, 4, 1, 5]` (counting buildings taller than max seen so far):

```
Position 0, looking right at [1, 4, 1, 5]:
  1 > 0 (max), visible! max=1
  4 > 1, visible! max=4
  1 < 4, blocked
  5 > 4, visible! max=5
  visible[0] = 3

Position 1, looking right at [4, 1, 5]:
  4 > 0, visible! max=4
  1 < 4, blocked
  5 > 4, visible! max=5
  visible[1] = 2

Position 2: visible[2] = 2  (sees 1, then 5)
Position 3: visible[3] = 1  (sees 5)
Position 4: visible[4] = 0  (nothing right)

Final: [3, 2, 2, 1, 0]
```

### Visual Diagram

```
Heights: [3, 1, 4, 1, 5]
Index:    0  1  2  3  4

From position 0, looking right:
    3    1    4    1    5
    |    ^    ^         ^
    0    1    2    3    4
    observer sees: 1, 4, 5 (3 buildings)
```

### Code

```python
def solve_optimal(n, heights, queries):
    """Precompute visible counts for O(1) queries."""
    visible = [0] * n
    for i in range(n):
        count, max_height = 0, 0
        for j in range(i + 1, n):
            if heights[j] > max_height:
                count += 1
                max_height = heights[j]
        visible[i] = count
    return [visible[pos - 1] for pos in queries]
```

### Complexity

| Time | Space |
|------|-------|
| O(n^2 + q) | O(n) |

Note: O(n^2) preprocessing, O(1) per query. See Solution 3 for O(n) preprocessing.

---

## Solution 3: O(n) Preprocessing with Next Greater Chain

### Key Insight

> **The Trick:** Use the "next strictly greater element" chain. If we know the next building taller than us, we can use DP: `visible[i] = 1 + visible[next_greater[i]]`.

### Algorithm

1. Find next strictly greater element for each position using monotonic stack
2. Process right-to-left: `visible[i] = 1 + visible[next_greater[i]]` if next_greater exists
3. For positions where next_greater is -1 (no taller building), visible = 0

### Code

```python
def solve_with_next_greater(n, heights, queries):
    """O(n) preprocessing using next greater element chain."""
    # Step 1: Find next strictly greater element
    next_greater = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] <= heights[i]:
            stack.pop()
        if stack:
            next_greater[i] = stack[-1]
        stack.append(i)

    # Step 2: DP - visible[i] = 1 + visible[next_greater[i]]
    visible = [0] * n
    for i in range(n - 1, -1, -1):
        if next_greater[i] != -1:
            visible[i] = 1 + visible[next_greater[i]]

    return [visible[pos - 1] for pos in queries]
```

### Complexity

**Time:** O(n + q) - O(n) stack + O(n) DP + O(q) queries
**Space:** O(n) - arrays for next_greater and visible

---

## Common Mistakes

### Mistake 1: Off-by-One Indexing

```python
# WRONG: count = visible[pos]     (out of bounds when pos == n)
# CORRECT: count = visible[pos - 1]  (convert 1-indexed to 0-indexed)
```

### Mistake 2: Including the Observer's Position

```python
# WRONG: for j in range(i, n)     (counts observer)
# CORRECT: for j in range(i + 1, n)  (start after observer)
```

### Mistake 3: Not Resetting Max Height

```python
# WRONG: max_height declared outside query loop (stale value)
# CORRECT: reset max_height = 0 inside each query iteration
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single building | `n=1, q=1, pos=1` | 0 | No buildings to the right |
| All same height | `[5,5,5,5], pos=1` | 1 | Only first building after is visible |
| Strictly increasing | `[1,2,3,4], pos=1` | 3 | All buildings visible |
| Strictly decreasing | `[4,3,2,1], pos=1` | 1 | Only immediate next visible |
| Query last position | `pos=n` | 0 | No buildings to the right |
| Very tall building blocks all | `[1,100,2,3,4], pos=1` | 1 | Building at pos 2 blocks all others |

---

## When to Use This Pattern

| Use When | Avoid When |
|----------|------------|
| Multiple queries on same data | Data updated between queries |
| Need O(1) query time | Only a few queries |
| O(n^2) preprocessing acceptable | Memory extremely constrained |

**Pattern Recognition:**
- Multiple queries on static data -> **Preprocessing**
- Visibility / next greater element -> **Monotonic stack**
- Suffix/prefix information -> **Right-to-left or left-to-right scan**

---

## Related Problems

| Difficulty | Problem | Key Concept |
|------------|---------|-------------|
| Easier | [Static Range Sum Queries (CSES)](https://cses.fi/problemset/task/1646) | Prefix sum preprocessing |
| Easier | [Next Greater Element I (LeetCode)](https://leetcode.com/problems/next-greater-element-i/) | Monotonic stack basics |
| Similar | [Buildings (CSES)](https://cses.fi/problemset/task/1147) | Visibility without queries |
| Similar | [Daily Temperatures (LeetCode)](https://leetcode.com/problems/daily-temperatures/) | Next greater with distance |
| Harder | [Dynamic Range Sum Queries (CSES)](https://cses.fi/problemset/task/1648) | Segment tree for updates |
| Harder | [Largest Rectangle in Histogram (LeetCode)](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Complex monotonic stack |

---

## Key Takeaways

1. **Core Idea:** Precompute answers for O(1) query time
2. **Optimization:** Trade O(n^2) preprocessing for O(1) queries
3. **Space Trade-off:** O(n) space for precomputed answers
4. **Pattern:** Classic "offline preprocessing" for static range queries
