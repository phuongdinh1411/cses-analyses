---
layout: simple
title: "Candies - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming_at/candies_analysis
difficulty: Medium
tags: [dp, prefix-sum, counting, modular-arithmetic]
prerequisites: [knapsack, prefix-sums]
---

# Candies

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | DP with Prefix Sum Optimization |
| **Source** | [AtCoder DP Contest - Problem M](https://atcoder.jp/contests/dp/tasks/dp_m) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply prefix sum optimization to reduce DP transition complexity from O(K) to O(1)
- [ ] Handle counting problems with individual constraints per element
- [ ] Implement modular arithmetic correctly in DP problems
- [ ] Recognize when range sum queries can optimize DP transitions

---

## Problem Statement

**Problem:** Distribute exactly K candies among N children, where each child i can receive between 0 and a_i candies (inclusive). Count the number of valid distributions modulo 10^9 + 7.

**Input:**
- Line 1: Two integers N and K (number of children and total candies)
- Line 2: N integers a_1, a_2, ..., a_N (maximum candies each child can receive)

**Output:**
- A single integer: the number of ways to distribute K candies, modulo 10^9 + 7

**Constraints:**
- 1 <= N <= 100
- 0 <= K <= 10^5
- 0 <= a_i <= K

### Example

```
Input:
3 4
1 2 3

Output:
5
```

**Explanation:** The 5 valid distributions (child1, child2, child3) are:
- (0, 1, 3): Child 1 gets 0, Child 2 gets 1, Child 3 gets 3
- (0, 2, 2): Child 1 gets 0, Child 2 gets 2, Child 3 gets 2
- (1, 0, 3): Child 1 gets 1, Child 2 gets 0, Child 3 gets 3
- (1, 1, 2): Child 1 gets 1, Child 2 gets 1, Child 3 gets 2
- (1, 2, 1): Child 1 gets 1, Child 2 gets 2, Child 3 gets 1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we count distributions efficiently when each child has a different maximum?

This is a classic counting DP problem. We need to count ordered sequences (x_1, x_2, ..., x_N) where:
- 0 <= x_i <= a_i for each child i
- x_1 + x_2 + ... + x_N = K

### Breaking Down the Problem

1. **What are we looking for?** The count of valid candy distributions
2. **What information do we have?** N children, K total candies, per-child limits a_i
3. **What's the relationship?** Each child's choice affects remaining candies for others

### Why Prefix Sum Optimization?

The naive DP transition sums over all possible candies (0 to a_i) for each child. This is a **contiguous range sum** - exactly what prefix sums compute in O(1).

```
dp[i][j] = dp[i-1][j] + dp[i-1][j-1] + ... + dp[i-1][j-a_i]
           └─────────────────────────────────────────────┘
                    Contiguous range sum!
```

---

## Solution 1: Naive DP (TLE)

### Idea

For each child i and each candy count j, try giving child i every possible amount from 0 to min(a_i, j).

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Number of ways to distribute exactly j candies among the first i children |

### State Transition

```
dp[i][j] = sum(dp[i-1][j-k]) for k = 0 to min(a_i, j)
```

### Code

```python
def solve_naive(n, k, limits):
 """
 Naive DP solution - O(N * K^2), will TLE for large inputs.

 Time: O(N * K^2)
 Space: O(N * K)
 """
 MOD = 10**9 + 7
 dp = [[0] * (k + 1) for _ in range(n + 1)]
 dp[0][0] = 1

 for i in range(1, n + 1):
  limit = limits[i - 1]
  for j in range(k + 1):
   for give in range(min(limit, j) + 1):
    dp[i][j] = (dp[i][j] + dp[i - 1][j - give]) % MOD

 return dp[n][k]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N * K^2) | For each of N*K states, sum over up to K values |
| Space | O(N * K) | 2D DP table |

### Why This Is Too Slow

With N = 100 and K = 10^5, we have 100 * (10^5)^2 = 10^12 operations - far too slow.

---

## Solution 2: Optimal - Prefix Sum Optimization

### Key Insight

> **The Trick:** The DP transition is a range sum. Use prefix sums to compute any range sum in O(1).

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Number of ways to distribute exactly j candies among the first i children |
| `prefix[j]` | Sum of dp[i-1][0] + dp[i-1][1] + ... + dp[i-1][j] |

**In plain English:** dp[i][j] counts how many ways we can give exactly j candies to children 1 through i, respecting each child's limit.

### State Transition with Prefix Sums

For child i with limit a_i, we can give them 0, 1, 2, ..., or min(a_i, j) candies:

```
dp[i][j] = dp[i-1][j] + dp[i-1][j-1] + ... + dp[i-1][max(0, j-a_i)]
         = prefix[j] - prefix[max(0, j-a_i) - 1]
```

**Why?**
- `prefix[j]` = sum of dp[i-1][0..j]
- `prefix[j-a_i-1]` = sum of dp[i-1][0..j-a_i-1]
- Difference gives dp[i-1][j-a_i..j], which is exactly what we need

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0][0]` | 1 | One way to distribute 0 candies to 0 children |
| `dp[0][j]` for j > 0 | 0 | Cannot distribute candies to 0 children |

### Algorithm

1. Initialize dp[0][0] = 1
2. For each child i from 1 to N:
   - Build prefix sum array from dp[i-1]
   - For each candy count j from 0 to K:
     - Calculate range [max(0, j-a_i), j] sum using prefix array
     - Set dp[i][j] = this sum
3. Return dp[N][K]

### Dry Run Example

Let's trace through with `N = 3, K = 4, limits = [1, 2, 3]`:

```
Initial: dp[0][0] = 1, dp[0][1..4] = 0

Processing Child 1 (limit = 1):
  prefix = [1, 1, 1, 1, 1]  (cumulative sum of dp[0])

  j=0: range [0,0], dp[1][0] = prefix[0] = 1
  j=1: range [0,1], dp[1][1] = prefix[1] = 1
  j=2: range [1,2], dp[1][2] = prefix[2] - prefix[0] = 1-1 = 0
  j=3: range [2,3], dp[1][3] = prefix[3] - prefix[1] = 1-1 = 0
  j=4: range [3,4], dp[1][4] = prefix[4] - prefix[2] = 1-1 = 0

  dp[1] = [1, 1, 0, 0, 0]

Processing Child 2 (limit = 2):
  prefix = [1, 2, 2, 2, 2]  (cumulative sum of dp[1])

  j=0: range [0,0], dp[2][0] = prefix[0] = 1
  j=1: range [0,1], dp[2][1] = prefix[1] = 2
  j=2: range [0,2], dp[2][2] = prefix[2] = 2
  j=3: range [1,3], dp[2][3] = prefix[3] - prefix[0] = 2-1 = 1
  j=4: range [2,4], dp[2][4] = prefix[4] - prefix[1] = 2-2 = 0

  dp[2] = [1, 2, 2, 1, 0]

Processing Child 3 (limit = 3):
  prefix = [1, 3, 5, 6, 6]  (cumulative sum of dp[2])

  j=0: range [0,0], dp[3][0] = prefix[0] = 1
  j=1: range [0,1], dp[3][1] = prefix[1] = 3
  j=2: range [0,2], dp[3][2] = prefix[2] = 5
  j=3: range [0,3], dp[3][3] = prefix[3] = 6
  j=4: range [1,4], dp[3][4] = prefix[4] - prefix[0] = 6-1 = 5

  dp[3] = [1, 3, 5, 6, 5]

Answer: dp[3][4] = 5
```

### Visual Diagram

```
Children:  [1]    [2]    [3]      (limits: 1, 2, 3)
            |      |      |
            v      v      v
Candies:   0-1    0-2    0-3      (each child can receive)

                K = 4 candies total
                     |
                     v
           Distribute across all children
                     |
                     v
             5 valid ways
```

### Code (Python)

```python
def solve(n, k, limits):
 """
 DP with prefix sum optimization for Candies problem.

 Time: O(N * K)
 Space: O(K) with space optimization
 """
 MOD = 10**9 + 7

 # dp[j] = ways to distribute j candies to children processed so far
 dp = [0] * (k + 1)
 dp[0] = 1

 for i in range(n):
  limit = limits[i]

  # Build prefix sum of current dp
  prefix = [0] * (k + 2)
  for j in range(k + 1):
   prefix[j + 1] = (prefix[j] + dp[j]) % MOD

  # Update dp using prefix sums
  new_dp = [0] * (k + 1)
  for j in range(k + 1):
   # Sum from dp[max(0, j-limit)] to dp[j]
   left = max(0, j - limit)
   new_dp[j] = (prefix[j + 1] - prefix[left]) % MOD

  dp = new_dp

 return dp[k]


def main():
 n, k = map(int, input().split())
 limits = list(map(int, input().split()))
 print(solve(n, k, limits))


if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N * K) | For each of N children, process K+1 candy counts in O(1) each |
| Space | O(K) | Only need current and prefix arrays |

---

## Common Mistakes

### Mistake 1: Negative Modulo

```python
# WRONG - may produce negative result
new_dp[j] = (prefix[j + 1] - prefix[left]) % MOD

# CORRECT - add MOD before taking modulo
new_dp[j] = (prefix[j + 1] - prefix[left] + MOD) % MOD
```

**Problem:** In some languages, (a - b) % MOD can be negative if a < b.
**Fix:** Add MOD before taking modulo to ensure positive result.

### Mistake 2: Off-by-One in Prefix Sum

```python
# WRONG - using 0-indexed prefix incorrectly
prefix[j] = sum of dp[0..j-1]  # excludes dp[j]

# CORRECT - be consistent with indexing
prefix[j+1] = sum of dp[0..j]  # includes dp[j]
```

**Problem:** Prefix sum index confusion leads to wrong range queries.
**Fix:** Use 1-indexed prefix array where prefix[j+1] = sum of dp[0..j].

### Mistake 3: Forgetting Base Case

```python
# WRONG - no initialization
dp = [0] * (k + 1)

# CORRECT - must set base case
dp = [0] * (k + 1)
dp[0] = 1  # One way to distribute 0 candies
```

**Problem:** Without dp[0] = 1, all values remain 0.
**Fix:** Always initialize the base case.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| K = 0 | N=3, K=0, a=[1,2,3] | 1 | Only one way: give 0 to everyone |
| Single child | N=1, K=5, a=[10] | 1 | One way if a[0] >= K |
| Impossible | N=2, K=10, a=[2,3] | 0 | Sum of limits < K |
| All limits = 0 | N=3, K=0, a=[0,0,0] | 1 | Only valid if K = 0 |
| Large K | N=100, K=10^5, a=[K]*100 | Large number | Tests efficiency |

---

## When to Use This Pattern

### Use Prefix Sum DP Optimization When:
- DP transition involves summing a contiguous range of previous values
- The range endpoints can be computed in O(1)
- Reducing O(K) transitions to O(1) is critical for time limits

### Don't Use When:
- The sum is over non-contiguous indices
- The DP state has complex dependencies beyond simple ranges
- The constraints are small enough for O(N * K^2)

### Pattern Recognition Checklist:
- [ ] DP transition is: `dp[i][j] = sum of dp[i-1][l..r]`? --> **Use prefix sums**
- [ ] Range [l, r] can be computed from j and constraints? --> **Yes**
- [ ] Need O(1) per transition to pass time limit? --> **Use prefix sums**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Prefix Sum Basics](https://leetcode.com/problems/range-sum-query-immutable/) | Core prefix sum technique |
| [Coin Combinations I](https://cses.fi/problemset/task/1635) | Basic counting DP |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Knapsack 2](https://atcoder.jp/contests/dp/tasks/dp_e) | Value-based DP with limits |
| [Dice Combinations](https://cses.fi/problemset/task/1633) | Simpler transition (fixed range 1-6) |
| [Slimes](https://atcoder.jp/contests/dp/tasks/dp_n) | Interval DP with range optimization |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Walk](https://atcoder.jp/contests/dp/tasks/dp_r) | Matrix exponentiation for counting |
| [Stones](https://atcoder.jp/contests/dp/tasks/dp_k) | Game theory with DP |

---

## Key Takeaways

1. **The Core Idea:** Transform O(K) range sums into O(1) using prefix sums
2. **Time Optimization:** Reduced from O(N * K^2) to O(N * K)
3. **Space Trade-off:** O(K) extra space for prefix array enables huge time savings
4. **Pattern:** Whenever DP transitions sum over contiguous ranges, prefix sums can help

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why prefix sum optimization works
- [ ] Handle the modular arithmetic correctly (negative results)
- [ ] Implement in your preferred language in under 15 minutes
- [ ] Identify similar problems that can use this optimization

---

## Additional Resources

- [AtCoder DP Contest](https://atcoder.jp/contests/dp) - Full problem set
- [CP-Algorithms: Prefix Sums](https://cp-algorithms.com/data_structures/prefix_sums.html)
- [CSES Problem Set - Dynamic Programming](https://cses.fi/problemset/list/)
