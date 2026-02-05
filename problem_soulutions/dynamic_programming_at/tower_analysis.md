---
layout: simple
title: "Tower - AtCoder DP Problem X"
permalink: /problem_soulutions/dynamic_programming_at/tower_analysis
difficulty: Hard
tags: [dp, sorting, greedy, optimization]
prerequisites: [knapsack, longest_increasing_subsequence]
---

# Tower (DP X)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | Sorting + DP (LIS-like) |
| **Problem Link** | [AtCoder DP Contest - X Tower](https://atcoder.jp/contests/dp/tasks/dp_x) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when sorting order determines valid DP transitions
- [ ] Apply the (w + s) sorting trick for stacking problems
- [ ] Design LIS-like DP for optimization with constraints
- [ ] Understand why greedy sorting enables correct DP solutions

---

## Problem Statement

**Problem:** Given N blocks, each with weight w_i, strength s_i, and value v_i, stack blocks to maximize total value. A block can support weight at most s_i on top of it. Find the maximum total value of a valid tower.

**Input:**
- Line 1: N (number of blocks)
- Lines 2 to N+1: w_i s_i v_i (weight, strength, value of block i)

**Output:**
- Maximum total value achievable

**Constraints:**
- 1 <= N <= 1000
- 1 <= w_i, s_i <= 10^4
- 1 <= v_i <= 10^9

### Example

```
Input:
3
4 1 10
3 2 20
2 4 30

Output:
50
```

**Explanation:**
- Block 1: w=4, s=1, v=10 (w+s=5) - can support up to 1 weight
- Block 2: w=3, s=2, v=20 (w+s=5) - can support up to 2 weight
- Block 3: w=2, s=4, v=30 (w+s=6) - can support up to 4 weight

Optimal tower: [Block 3 at bottom, Block 2 on top]
- Block 3 supports Block 2's weight: s_3=4 >= w_2=3. Valid.
- Total value: 30 + 20 = 50

Why not add Block 1? Block 2 can only support weight 2, but Block 1 weighs 4. Invalid.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** In what order should we consider blocks for stacking?

The critical insight is that the order we consider blocks matters. If we process blocks in the wrong order, we might miss valid configurations. The magic formula is: **sort by (w_i + s_i)**.

### Why Sort by (w + s)?

Consider two blocks A and B. When can A be below B?
- A below B requires: weight_above_A >= w_B, so s_A >= w_B

When can B be below A?
- B below A requires: s_B >= w_A

For a consistent ordering where if A can be below B, we always consider A first:
- If s_A >= w_B (A can support B), then ideally w_A + s_A <= w_B + s_B

This sorting ensures that when processing block i, all blocks that could potentially be below it have already been processed.

### Breaking Down the Problem

1. **What are we looking for?** Maximum value tower where each block supports the weight above it.
2. **What constraints exist?** Block at position k must have s_k >= sum of weights of all blocks above.
3. **What's the key insight?** Sort by (w+s) to ensure valid DP transitions.

### Analogies

Think of this like building a human pyramid. The strongest person (highest strength relative to their weight) goes at the bottom. The sorting by (w+s) ensures that people who are "relatively stronger" are processed first, making them valid candidates for lower positions.

---

## Brute Force Approach (TLE)

Try all 2^N subsets and N! orderings: O(N! * 2^N). Even N=10 gives ~3.7 billion operations.

---

## Optimal Solution: DP with Sorting

### Key Insight

> **The Trick:** Sort blocks by (w + s), then use DP where dp[i][j] = minimum weight to achieve value j using first i blocks.

Alternatively, we can use dp[j] = minimum weight to achieve value j, processing blocks in sorted order.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[j]` | Minimum total weight of tower with total value exactly j |

**In plain English:** For each possible total value, what's the lightest tower we can build?

### State Transition

```
For each block i (in sorted order):
    For j from max_value down to v_i:
        if dp[j - v_i] <= s_i:  # Block i can support the tower above
            dp[j] = min(dp[j], dp[j - v_i] + w_i)
```

**Why?** If we have a tower of value (j - v_i) with weight dp[j-v_i], and block i can support that weight (dp[j-v_i] <= s_i), we can place block i at the bottom.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 0 | Empty tower has zero weight |
| `dp[j]` for j > 0 | INF | Initially impossible |

### Algorithm

1. Sort blocks by (w_i + s_i) in ascending order
2. Initialize dp[0] = 0, dp[j] = INF for j > 0
3. For each block in sorted order, update dp in reverse value order
4. Find maximum j where dp[j] < INF

### Dry Run Example

Let's trace through with a 4-block example:

```
Input:
4 blocks:
Block A: w=4, s=3, v=10  (w+s=7)
Block B: w=3, s=4, v=20  (w+s=7)
Block C: w=2, s=2, v=15  (w+s=4)
Block D: w=1, s=1, v=5   (w+s=2)
```

**Step 1: Sort by (w + s)**
```
Sorted order: D (w+s=2), C (w+s=4), A (w+s=7), B (w+s=7)
```

**Step 2: Initialize DP**
```
dp[0] = 0 (empty tower has weight 0)
dp[j] = INF for all j > 0 (initially impossible)
```

**Step 3: Process blocks in sorted order**

| Block | Check & Update | Meaning |
|-------|----------------|---------|
| D (w=1, s=1, v=5) | dp[0]=0 <= s=1, so dp[5] = 1 | Tower with just D has weight 1 |
| C (w=2, s=2, v=15) | dp[0]=0 <= s=2, so dp[15] = 2 | Tower with just C |
| | dp[5]=1 <= s=2, so dp[20] = 3 | Tower [C bottom, D top], weight=3 |
| A (w=4, s=3, v=10) | dp[0]=0 <= s=3, so dp[10] = 4 | Tower with just A |
| | dp[15]=2 <= s=3, so dp[25] = 6 | Tower [A bottom, C top] |
| | dp[20]=3 <= s=3, so dp[30] = 7 | Tower [A, C, D] |
| B (w=3, s=4, v=20) | dp[0]=0 <= s=4, so dp[20] = min(3, 3) = 3 | No change |
| | dp[15]=2 <= s=4, so dp[35] = 5 | Tower [B, C] |
| | dp[25]=6 > s=4, skip | B cannot support weight 6 |
| | dp[20]=3 <= s=4, so dp[40] = 6 | Tower [B, C, D] |

**Final DP state (non-INF values):**
```
dp[0]=0, dp[5]=1, dp[10]=4, dp[15]=2, dp[20]=3,
dp[25]=6, dp[30]=7, dp[35]=5, dp[40]=6
```

**Answer:** Maximum value j where dp[j] < INF is **40** (using blocks B, C, D).

### Code (Python)

```python
def solve(n, blocks):
  """Tower stacking DP with (w+s) sorting."""
  blocks.sort(key=lambda x: x[0] + x[1])  # Sort by w + s

  max_val = sum(v for w, s, v in blocks)
  INF = float('inf')
  dp = [INF] * (max_val + 1)
  dp[0] = 0

  for w, s, v in blocks:
    for j in range(max_val, v - 1, -1):  # Reverse to avoid reuse
      if dp[j - v] <= s:  # Can this block support weight above?
        dp[j] = min(dp[j], dp[j - v] + w)

  return max(j for j in range(max_val + 1) if dp[j] < INF)


if __name__ == "__main__":
  n = int(input())
  blocks = [tuple(map(int, input().split())) for _ in range(n)]
  print(solve(n, blocks))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N * V) | N blocks, V = sum of all values |
| Space | O(V) | DP array indexed by value |

---

## Common Mistakes

### Mistake 1: Wrong Sorting Order

```python
# WRONG - sorting by w alone
blocks.sort(key=lambda x: x[0])

# WRONG - sorting by s alone
blocks.sort(key=lambda x: x[1])
```

**Problem:** Neither w nor s alone determines valid stacking order. A block with high s but low w might need to be below a block with low s but high w.

**Fix:** Sort by (w + s) to ensure consistent ordering.

### Mistake 2: Wrong DP Transition Direction

```python
# WRONG - forward iteration allows reusing blocks
for j in range(v, max_val + 1):
  if dp[j - v] <= s:
    dp[j] = min(dp[j], dp[j - v] + w)
```

**Problem:** Forward iteration can use the same block multiple times.

**Fix:** Iterate backwards from max_val to v.

### Mistake 3: Checking Weight Instead of DP Value

```python
# WRONG - comparing raw weight instead of tower weight
if w <= s:  # This doesn't check accumulated weight!
  dp[j] = ...
```

**Problem:** We need to check if the current block can support the TOTAL weight of the tower above it, not just one block's weight.

**Fix:** Check `dp[j - v] <= s` where dp[j-v] is the minimum weight of tower with value j-v.

### Mistake 4: Integer Overflow

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single block | N=1, w=5, s=0, v=100 | 100 | Can always use one block |
| All same w+s | All blocks have w+s=10 | Max subset value | Sorting doesn't differentiate |
| No valid pairs | All s=0, w>0 | Max single v | No block can support another |
| Maximum values | N=1000, v=10^9 each | Sum if stackable | Handle 10^12 total value |
| Zero strength | s_i=0 for all | Max single v | Each block can only be on top |

---

## When to Use This Pattern

### Use This Approach When:
- Stacking/ordering problems with pairwise constraints
- Constraints involve sum of properties (like total weight above)
- Need to find optimal subset AND ordering simultaneously
- LIS-like problems with additional constraints

### Don't Use When:
- Ordering doesn't affect validity (simple knapsack)
- Constraints are independent of position
- Need to track actual sequence (not just value)

### Pattern Recognition Checklist:
- [ ] Is there a stacking or ordering component?
- [ ] Do constraints involve cumulative properties (weight above, etc.)?
- [ ] Can we find a sorting key that enables DP?
- [ ] Does sorting by (a + b) make sense for constraint pairs?

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [0/1 Knapsack](https://atcoder.jp/contests/dp/tasks/dp_d) | Basic DP with value/weight trade-off |
| [LIS](https://atcoder.jp/contests/dp/tasks/dp_q) | DP with ordering constraints |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Box Stacking](https://www.geeksforgeeks.org/box-stacking-problem-dp-22/) | 3D variant with rotations |
| [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | 2D LIS variant |
| [Maximum Height by Stacking Cuboids](https://leetcode.com/problems/maximum-height-by-stacking-cuboids/) | 3D with height optimization |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [DP on Trees](https://atcoder.jp/contests/dp/tasks/dp_p) | Tree structure instead of sequence |
| [Bitmask DP](https://atcoder.jp/contests/dp/tasks/dp_o) | Exponential state space |

---

## Key Takeaways

1. **The Core Idea:** Sort by (w + s) to ensure valid stacking order, then use knapsack-style DP.
2. **Time Optimization:** Sorting reduces from factorial complexity to polynomial.
3. **Space Trade-off:** O(sum of values) space for O(N * V) time.
4. **Pattern:** Stacking problems often require clever sorting + DP combination.

---

## Practice Checklist

- [ ] Explain why (w + s) sorting works
- [ ] Implement the DP solution from scratch
- [ ] Handle edge cases (single block, zero strength)
- [ ] Recognize similar stacking problems in contests
