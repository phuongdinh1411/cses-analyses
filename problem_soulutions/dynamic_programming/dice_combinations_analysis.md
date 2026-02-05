---
layout: simple
title: "Dice Combinations - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/dice_combinations_analysis
difficulty: Easy
tags: [dp, counting, combinatorics, 1d-dp]
prerequisites: []
---

# Dice Combinations

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Dynamic Programming |
| **Time Limit** | 1 second |
| **Key Technique** | 1D DP with counting |
| **CSES Link** | [Dice Combinations](https://cses.fi/problemset/task/1633) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Define DP states for counting problems
- [ ] Write recurrence relations for counting combinations
- [ ] Implement bottom-up DP with modular arithmetic
- [ ] Recognize the "number of ways" DP pattern

---

## Problem Statement

**Problem:** Count the number of ways to construct a sum n by throwing a dice one or more times. Each throw produces a value between 1 and 6.

**Input:**
- A single integer n (the target sum)

**Output:**
- The number of ways modulo 10^9 + 7

**Constraints:**
- 1 ≤ n ≤ 10^6

### Example

```
Input:
3

Output:
4
```

**Explanation:** The four ways to make sum 3 are:
1. `1 + 1 + 1 = 3`
2. `1 + 2 = 3`
3. `2 + 1 = 3`
4. `3 = 3`

Note: Order matters! `1 + 2` and `2 + 1` are counted as different ways.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** This is a "count the number of ways" problem with choices at each step. That screams Dynamic Programming!

The key insight is that reaching sum `n` can only happen by:
- Reaching sum `n-1` and then rolling a 1, OR
- Reaching sum `n-2` and then rolling a 2, OR
- ... and so on up to rolling a 6

### Breaking Down the Problem

1. **What are we counting?** Number of sequences of dice rolls that sum to n
2. **What choices do we have at each step?** Roll 1, 2, 3, 4, 5, or 6
3. **What's the subproblem?** Number of ways to reach a smaller sum

### Analogy: Climbing Stairs

This is exactly like "Climbing Stairs" but with 6 step sizes instead of 2!

```
Climbing Stairs:  ways(n) = ways(n-1) + ways(n-2)
Dice Combinations: ways(n) = ways(n-1) + ways(n-2) + ... + ways(n-6)
```

---

## Solution 1: Recursion (Brute Force)

### Idea

Try all possible dice rolls recursively. For each sum, try subtracting 1, 2, 3, 4, 5, or 6 and count ways to reach the remainder.

### Code

```python
def solve_recursive(n):
  """
  Recursive solution - for understanding only.

  Time: O(6^n) - exponential, will TLE
  Space: O(n) - recursion depth
  """
  MOD = 10**9 + 7

  def count_ways(target):
    if target == 0:
      return 1  # Found a valid combination
    if target < 0:
      return 0  # Invalid, overshot

    total = 0
    for dice in range(1, 7):  # Roll 1 to 6
      total += count_ways(target - dice)
    return total % MOD

  return count_ways(n)
```

### Why This Is Too Slow

For n = 10, we compute `count_ways(4)` multiple times:
- Once via 10 → 9 → 8 → 7 → 6 → 5 → 4
- Once via 10 → 9 → 8 → 7 → 6 → 4
- Once via 10 → 9 → 8 → 7 → 5 → 4
- ... many more times!

This is the classic "overlapping subproblems" indicator for DP.

---

## Solution 2: Dynamic Programming (Optimal)

### Key Insight

> **The Trick:** Instead of recomputing, store the number of ways to reach each sum from 0 to n.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i]` | Number of ways to construct sum `i` using dice rolls |

**In plain English:** `dp[5]` answers "How many dice roll sequences sum to exactly 5?"

### State Transition

```
dp[i] = dp[i-1] + dp[i-2] + dp[i-3] + dp[i-4] + dp[i-5] + dp[i-6]
```

**Why?** To reach sum `i`, we must have been at some smaller sum and rolled a dice:
- From sum `i-1`, roll a 1 → reach sum `i`
- From sum `i-2`, roll a 2 → reach sum `i`
- ... and so on

Each of these is a distinct way, so we ADD them all.

### Base Case

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 1 | There's exactly ONE way to have sum 0: don't roll at all |

Note: `dp[0] = 1` is a common DP convention for counting problems. It represents the "empty" solution.

### Algorithm

```
1. Create dp array of size n+1, initialize to 0
2. Set dp[0] = 1 (base case)
3. For i from 1 to n:
     For dice from 1 to 6:
       If i >= dice:
         dp[i] += dp[i - dice]
         dp[i] %= MOD
4. Return dp[n]
```

### Dry Run Example

Let's trace through with `n = 4`:

```
Initialize: dp = [0, 0, 0, 0, 0]
Base case:  dp = [1, 0, 0, 0, 0]

i = 1:
  dice=1: dp[1] += dp[0] = 1    → dp = [1, 1, 0, 0, 0]
  dice=2,3,4,5,6: i < dice, skip

i = 2:
  dice=1: dp[2] += dp[1] = 1    → dp[2] = 1
  dice=2: dp[2] += dp[0] = 1    → dp[2] = 2
  dice=3,4,5,6: i < dice, skip
  → dp = [1, 1, 2, 0, 0]

i = 3:
  dice=1: dp[3] += dp[2] = 2    → dp[3] = 2
  dice=2: dp[3] += dp[1] = 1    → dp[3] = 3
  dice=3: dp[3] += dp[0] = 1    → dp[3] = 4
  → dp = [1, 1, 2, 4, 0]

i = 4:
  dice=1: dp[4] += dp[3] = 4    → dp[4] = 4
  dice=2: dp[4] += dp[2] = 2    → dp[4] = 6
  dice=3: dp[4] += dp[1] = 1    → dp[4] = 7
  dice=4: dp[4] += dp[0] = 1    → dp[4] = 8
  → dp = [1, 1, 2, 4, 8]

Answer: dp[4] = 8
```

### Visual Diagram

```
Building up solutions:

Sum 0: 1 way (empty)
       │
       ▼
Sum 1: 1 way ──────────────── [1]
       │
       ├─ roll 1 → sum 2
       ▼
Sum 2: 2 ways ─────────────── [1+1], [2]
       │
       ├─ roll 1,2,3 → sum 3
       ▼
Sum 3: 4 ways ─────────────── [1+1+1], [1+2], [2+1], [3]
       │
       ├─ roll 1,2,3,4 → sum 4
       ▼
Sum 4: 8 ways
```

### Code

```python
def solve_dp(n):
  """
  Bottom-up DP solution.

  Time: O(n) - single pass, 6 operations per element
  Space: O(n) - dp array
  """
  MOD = 10**9 + 7

  # dp[i] = number of ways to make sum i
  dp = [0] * (n + 1)
  dp[0] = 1  # Base case: one way to make sum 0

  for i in range(1, n + 1):
    for dice in range(1, 7):
      if i >= dice:
        dp[i] = (dp[i] + dp[i - dice]) % MOD

  return dp[n]

# Read input and solve
n = int(input())
print(solve_dp(n))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Loop from 1 to n, with 6 operations each |
| Space | O(n) | Array of size n+1 |

---

## Common Mistakes

### Mistake 1: Wrong Base Case

```python
# WRONG - forgetting base case
dp = [0] * (n + 1)
# dp[0] is 0, so all dp values stay 0!

# CORRECT
dp[0] = 1
```

**Problem:** Without `dp[0] = 1`, there's no starting point for the recurrence.

### Mistake 2: Forgetting Modulo

```python
# WRONG - will overflow for large n
dp[i] = dp[i] + dp[i - dice]

# CORRECT
dp[i] = (dp[i] + dp[i - dice]) % MOD
```

**Problem:** Numbers grow exponentially. For n = 10^6, the answer has millions of digits without modulo.

### Mistake 3: Off-by-One in Array Size

```python
# WRONG - will crash on dp[n]
dp = [0] * n

# CORRECT
dp = [0] * (n + 1)
```

### Mistake 4: Wrong Loop Order (for 2D DP variants)

For this problem, order doesn't matter since we only look backward. But for similar problems like Coin Combinations (counting combinations, not permutations), loop order matters!

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum input | n = 1 | 1 | Only way: roll 1 |
| Small input | n = 2 | 2 | Ways: [1+1], [2] |
| n = 6 | 6 | 32 | All dice values usable |
| Large input | n = 10^6 | (large number) | Test for TLE and overflow |

---

## Related Concepts: Permutations vs Combinations

This problem counts **permutations** (order matters):
- `[1, 2]` and `[2, 1]` are different

Compare with **Coin Combinations II** which counts **combinations** (order doesn't matter):
- `[1, 2]` and `[2, 1]` would be the same

The difference is in loop structure:

```python
# PERMUTATIONS (this problem) - inner loop over choices
for i in range(1, n + 1):       # For each sum
  for dice in range(1, 7):    # Try each dice value
    dp[i] += dp[i - dice]

# COMBINATIONS - outer loop over choices
for dice in range(1, 7):        # For each dice value
  for i in range(dice, n + 1): # Update all reachable sums
    dp[i] += dp[i - dice]
```

---

## When to Use This Pattern

### Use This Approach When:
- Counting number of ways to reach a target
- You have a set of "step sizes" (here: 1-6)
- Order of steps matters (permutations)
- Optimal substructure: solution to n depends on solutions to smaller values

### Pattern Recognition Checklist:
- [ ] "How many ways..." or "Count the number of..." → **Counting DP**
- [ ] Can reach state from multiple previous states → **Sum previous states**
- [ ] Order matters → **Inner loop over choices**
- [ ] Order doesn't matter → **Outer loop over choices**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Climbing Stairs (LeetCode)](https://leetcode.com/problems/climbing-stairs/) | Same pattern with 2 choices instead of 6 |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Coin Combinations I (CSES)](https://cses.fi/problemset/task/1635) | Variable coin values instead of 1-6 |
| [Coin Combinations II (CSES)](https://cses.fi/problemset/task/1636) | Counts combinations, not permutations |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Minimizing Coins (CSES)](https://cses.fi/problemset/task/1634) | Minimize instead of count |
| [Book Shop (CSES)](https://cses.fi/problemset/task/1158) | 2D DP (knapsack variant) |

---

## Key Takeaways

1. **The Core Idea:** Count ways to reach sum n by summing ways to reach all sums we can jump from (n-1 through n-6)

2. **DP State:** `dp[i]` = number of ways to construct sum i

3. **Recurrence:** `dp[i] = sum(dp[i-k] for k in 1..6 if i >= k)`

4. **Base Case:** `dp[0] = 1` (one way to make sum 0: do nothing)

5. **Pattern:** This is the "Counting Paths" DP pattern - very common in competitive programming!

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Write the recurrence relation from scratch
- [ ] Explain why dp[0] = 1 makes sense
- [ ] Implement this in under 5 minutes
- [ ] Modify it for different step sizes (e.g., 1-10 instead of 1-6)
- [ ] Explain the difference between permutations and combinations counting
