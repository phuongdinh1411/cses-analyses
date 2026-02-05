---
layout: simple
title: "Permutation Inversions - Counting Problem"
permalink: /problem_soulutions/counting_problems/permutation_inversions_analysis
difficulty: Hard
tags: [dp, combinatorics, counting, inversions, prefix-sum]
---

# Permutation Inversions

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [CSES - Permutation Inversions](https://cses.fi/problemset/task/2229) |
| **Difficulty** | Hard |
| **Category** | Dynamic Programming, Counting |
| **Time Limit** | 1 second |
| **Key Technique** | DP with Prefix Sum Optimization |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how inversions characterize permutations
- [ ] Design DP states for counting combinatorial objects
- [ ] Apply prefix sum optimization to reduce DP complexity
- [ ] Handle modular arithmetic in counting problems

---

## Problem Statement

**Problem:** Count the number of permutations of numbers 1 to n that have exactly k inversions. An inversion is a pair (i, j) where i < j but p[i] > p[j].

**Input:**
- Line 1: Two integers n and k

**Output:**
- The count of permutations modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 500
- 0 <= k <= n(n-1)/2

### Example

```
Input:
4 3

Output:
6
```

**Explanation:** The permutations of [1,2,3,4] with exactly 3 inversions are:
- [2,4,3,1] - inversions: (2,3), (2,1), (4,3), (4,1), (3,1) = wait, that's 5
- Actually: [3,2,1,4], [2,4,1,3], [4,1,2,3], [1,4,3,2], [3,1,4,2], [2,3,4,1]

Let me verify [3,2,1,4]: pairs (3,2), (3,1), (2,1) = 3 inversions. Correct!

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How does adding a new element to a permutation affect the inversion count?

When we insert element (i+1) into a permutation of elements 1 to i, the new element can be placed in any of (i+1) positions. If placed at position j (0-indexed from left), it creates exactly (i - j) new inversions because there are (i - j) elements to its right, all smaller than (i+1).

### Breaking Down the Problem

1. **What are we counting?** Permutations with exactly k inversions
2. **What's the recursive structure?** Build permutation by inserting elements one by one
3. **How do inversions grow?** Inserting element m at position j adds (m-1-j) inversions

### The Key Insight

When inserting the i-th element (1-indexed) into a permutation of (i-1) elements:
- There are i possible positions (0 to i-1)
- Position j creates (i-1-j) new inversions
- We can create 0, 1, 2, ..., or (i-1) new inversions

---

## Solution 1: Basic DP (TLE for large inputs)

### Idea

Let `dp[i][j]` = number of permutations of elements 1 to i with exactly j inversions.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Count of permutations of 1..i with exactly j inversions |

### State Transition

```
dp[i][j] = sum(dp[i-1][j-x]) for x in [0, min(j, i-1)]
```

**Why?** When inserting element i, we can add 0 to (i-1) inversions by choosing the position.

### Base Case

| Case | Value | Reason |
|------|-------|--------|
| `dp[1][0]` | 1 | Single element has 0 inversions |
| `dp[i][j]` where j < 0 | 0 | Invalid state |

### Code

```python
def count_permutations_basic(n, k):
    """
    Basic DP solution - O(n^2 * k) time.

    Time: O(n^2 * k) - too slow for large inputs
    Space: O(n * k)
    """
    MOD = 10**9 + 7

    # dp[i][j] = permutations of 1..i with j inversions
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[1][0] = 1

    for i in range(2, n + 1):
        for j in range(k + 1):
            # Insert element i: can add 0 to (i-1) inversions
            for add in range(min(j + 1, i)):
                dp[i][j] = (dp[i][j] + dp[i-1][j-add]) % MOD

    return dp[n][k]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 * k) | Three nested loops |
| Space | O(n * k) | DP table |

### Why This Is Slow

The innermost loop sums over up to min(i, j) values, making total complexity O(n * k * n) = O(n^2 * k).

---

## Solution 2: Optimal Solution with Prefix Sum

### Key Insight

> **The Trick:** The inner sum `dp[i-1][j] + dp[i-1][j-1] + ... + dp[i-1][j-(i-1)]` is a contiguous range sum. Use prefix sums!

### Optimized Transition

Instead of summing in a loop, precompute prefix sums:
```
prefix[j] = dp[i-1][0] + dp[i-1][1] + ... + dp[i-1][j]
dp[i][j] = prefix[j] - prefix[max(0, j-i)]
```

### Dry Run Example

Let's trace through with `n = 4, k = 3`:

```
Initial: dp[1][0] = 1 (permutation [1] has 0 inversions)

Building dp[2]:
  Element 2 can add 0 or 1 inversions
  dp[2][0] = dp[1][0] = 1       # [1,2]
  dp[2][1] = dp[1][0] = 1       # [2,1]

Building dp[3]:
  Element 3 can add 0, 1, or 2 inversions
  prefix = [1, 2, 2] for dp[2]
  dp[3][0] = dp[2][0] = 1                    # [1,2,3]
  dp[3][1] = dp[2][0] + dp[2][1] = 2         # [1,3,2], [2,1,3]
  dp[3][2] = dp[2][0] + dp[2][1] = 2         # [2,3,1], [3,1,2]
  dp[3][3] = dp[2][1] = 1                    # [3,2,1]

Building dp[4]:
  Element 4 can add 0, 1, 2, or 3 inversions
  prefix = [1, 3, 5, 6] for dp[3]
  dp[4][3] = dp[3][0] + dp[3][1] + dp[3][2] + dp[3][3]
           = 1 + 2 + 2 + 1 = 6

Answer: 6
```

### Visual Diagram

```
Permutation building process for n=4, k=3:

Start: [1]           inversions = 0

Insert 2:
  [1,2] -> 0 new inv  [2,1] -> 1 new inv

Insert 3:
  Position 0: [3,_,_] adds 2 inversions
  Position 1: [_,3,_] adds 1 inversion
  Position 2: [_,_,3] adds 0 inversions

Insert 4:
  Position 0: adds 3 inversions
  Position 1: adds 2 inversions
  Position 2: adds 1 inversion
  Position 3: adds 0 inversions

To reach exactly 3 inversions from dp[3]:
  From dp[3][3] add 0 -> still 3: 1 way
  From dp[3][2] add 1 -> reach 3: 2 ways
  From dp[3][1] add 2 -> reach 3: 2 ways
  From dp[3][0] add 3 -> reach 3: 1 way
  Total: 6 ways
```

### Code (Python)

```python
def count_permutations(n: int, k: int) -> int:
    """
    Count permutations of 1..n with exactly k inversions.
    Uses prefix sum optimization.

    Time: O(n * k)
    Space: O(k) with rolling array optimization
    """
    MOD = 10**9 + 7

    # dp[j] = permutations with j inversions
    dp = [0] * (k + 1)
    dp[0] = 1  # Base: permutation [1] has 0 inversions

    for i in range(2, n + 1):
        # Build prefix sum of current dp
        prefix = [0] * (k + 2)
        for j in range(k + 1):
            prefix[j + 1] = (prefix[j] + dp[j]) % MOD

        # Update dp using prefix sums
        new_dp = [0] * (k + 1)
        for j in range(k + 1):
            # Sum dp[max(0, j-(i-1))] to dp[j]
            left = max(0, j - (i - 1))
            new_dp[j] = (prefix[j + 1] - prefix[left]) % MOD

        dp = new_dp

    return dp[k]


def solve():
    n, k = map(int, input().split())
    print(count_permutations(n, k))


if __name__ == "__main__":
    solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * k) | Two nested loops, O(1) per cell |
| Space | O(k) | Rolling array optimization |

---

## Common Mistakes

### Mistake 1: Forgetting Modular Subtraction Can Go Negative

**Problem:** In C++, `(-1) % MOD` gives `-1`, not `MOD - 1`.
**Fix:** Always add MOD before taking modulo after subtraction.

### Mistake 2: Wrong Range for New Inversions

```python
# WRONG - element i can add at most i inversions
for add in range(i + 1):

# CORRECT - element i can add at most (i-1) inversions
for add in range(i):  # 0 to i-1
```

**Problem:** Inserting element i into positions 0..i-1 creates at most i-1 new inversions.
**Fix:** Remember the maximum inversions added equals (current element - 1).

### Mistake 3: Off-by-One in Prefix Sum Indexing

```python
# WRONG - prefix[j] should be sum of dp[0..j-1]
prefix[j] = prefix[j-1] + dp[j]

# CORRECT - shift index by 1 for cleaner range queries
prefix[j+1] = prefix[j] + dp[j]
# Then sum from l to r is prefix[r+1] - prefix[l]
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum inversions | `n=5, k=0` | 1 | Only sorted permutation [1,2,3,4,5] |
| Maximum inversions | `n=4, k=6` | 1 | Only reverse [4,3,2,1], max = n(n-1)/2 = 6 |
| k exceeds maximum | `n=3, k=5` | 0 | Max inversions for n=3 is 3 |
| Single element | `n=1, k=0` | 1 | Only [1] exists |
| Large n, small k | `n=500, k=0` | 1 | Only sorted permutation |

---

## When to Use This Pattern

### Use This Approach When:
- Counting permutations with specific properties
- DP transition involves summing over a contiguous range
- Combinatorial counting with additive constraints

### Pattern Recognition Checklist:
- [ ] Building objects incrementally? -> Consider insertion DP
- [ ] Transition sums over a range? -> Use prefix sum optimization
- [ ] Counting with modular arithmetic? -> Handle negative remainders

### Similar Techniques:
- Range sum queries in DP
- Sliding window DP
- Convolution-like transitions

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Coin Combinations I](https://cses.fi/problemset/task/1635) | Basic counting DP |
| [Dice Combinations](https://cses.fi/problemset/task/1633) | Sum over recent states |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Bracket Sequences I](https://cses.fi/problemset/task/2064) | Counting valid sequences |
| [Counting Tilings](https://cses.fi/problemset/task/2181) | Grid-based counting |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Counting Necklaces](https://cses.fi/problemset/task/2209) | Burnside's lemma |
| [Graph Paths II](https://cses.fi/problemset/task/1724) | Matrix exponentiation |

---

## Key Takeaways

1. **The Core Idea:** Insert elements one by one; each position choice determines new inversions
2. **Time Optimization:** Prefix sums reduce O(n^2 k) to O(nk)
3. **Space Trade-off:** Rolling array reduces space from O(nk) to O(k)
4. **Pattern:** Range-sum DP optimization using prefix sums

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why inserting element i can create 0 to i-1 inversions
- [ ] Derive the DP recurrence from scratch
- [ ] Implement prefix sum optimization correctly
- [ ] Handle modular arithmetic edge cases
- [ ] Solve this problem in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Counting Inversions](https://cp-algorithms.com/sequences/inversions.html)
- [CSES Inversion Probability](https://cses.fi/problemset/task/2169) - Expected inversions
- [Inversions in Permutations - Math Background](https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics))
