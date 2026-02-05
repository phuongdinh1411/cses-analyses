---
layout: simple
title: "Coin Combinations I - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/coin_combinations_i_analysis
difficulty: Easy
tags: [dp, counting, combinatorics, 1d-dp, permutations]
prerequisites: [dice_combinations]
---

# Coin Combinations I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Dynamic Programming |
| **Time Limit** | 1 second |
| **Key Technique** | 1D DP counting permutations |
| **CSES Link** | [Coin Combinations I](https://cses.fi/problemset/task/1635) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the "counting permutations" DP pattern
- [ ] Distinguish between permutations (order matters) and combinations (order doesn't matter)
- [ ] Generalize the Dice Combinations approach to variable coin values
- [ ] Implement efficient counting DP with modular arithmetic

---

## Problem Statement

**Problem:** Consider a money system consisting of n coins. Each coin has a positive integer value. Your task is to calculate the number of distinct **ordered ways** you can produce a money sum x using the available coins.

**Key Point:** Order matters! Using coins [1, 2] is different from [2, 1].

**Input:**
- Line 1: Two integers n and x (number of coins and target sum)
- Line 2: n integers c₁, c₂, ..., cₙ (coin values)

**Output:**
- The number of ways modulo 10⁹ + 7

**Constraints:**
- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10⁶
- 1 ≤ cᵢ ≤ 10⁶

### Example

```
Input:
3 9
2 3 5

Output:
8
```

**Explanation:** The 8 ordered ways to make sum 9 with coins [2, 3, 5]:
1. `2+2+2+3 = 9`
2. `2+2+3+2 = 9`
3. `2+3+2+2 = 9`
4. `3+2+2+2 = 9`
5. `2+2+5 = 9`
6. `2+5+2 = 9`
7. `5+2+2 = 9`
8. `3+3+3 = 9`

Notice: `2+2+5`, `2+5+2`, and `5+2+2` are counted as THREE different ways!

---

## Intuition: How to Think About This Problem

### Connection to Dice Combinations

This is a **generalization** of Dice Combinations:
- Dice Combinations: fixed "coins" of values 1, 2, 3, 4, 5, 6
- Coin Combinations I: variable coin values given as input

The same DP approach works!

### Pattern Recognition

> **Key Question:** When order matters in counting, we iterate over sums in the outer loop and coins in the inner loop.

This ensures each position in the sequence can use any coin, creating permutations.

### The Critical Insight: Loop Order Matters!

```python
# PERMUTATIONS (this problem) - sum first, then coins
for sum in range(1, x + 1):
 for coin in coins:
  dp[sum] += dp[sum - coin]

# COMBINATIONS (Coin Combinations II) - coins first, then sum
for coin in coins:
 for sum in range(coin, x + 1):
  dp[sum] += dp[sum - coin]
```

**Why?** In the permutation version, for each sum, we try ALL coins as the last coin. In the combination version, we process one coin at a time across all sums, preventing reordering.

---

## Solution: Dynamic Programming

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i]` | Number of **ordered sequences** of coins that sum to exactly `i` |

**In plain English:** `dp[9]` answers "How many different ordered sequences of coins add up to 9?"

### State Transition

```
dp[i] = sum of dp[i - c] for all coins c where i >= c
```

**Why?** To form sum `i` with the last coin being `c`:
- We need `i - c` to be achievable first
- Then we add coin `c` at the end
- Since we try all coins as the "last" coin, we get all permutations

### Base Case

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 1 | One way to make sum 0: use no coins (empty sequence) |

### Algorithm

```
1. Create dp array of size x+1, initialize to 0
2. Set dp[0] = 1 (base case)
3. For i from 1 to x:           # Outer: iterate sums
     For each coin c in coins:   # Inner: try each coin
       If i >= c:
         dp[i] += dp[i - c]
         dp[i] %= MOD
4. Return dp[x]
```

### Dry Run Example

Input: `coins = [2, 3, 5], x = 5`

```
Initialize: dp = [1, 0, 0, 0, 0, 0]  (dp[0] = 1)

i = 1: No coin <= 1, dp[1] = 0
       dp = [1, 0, 0, 0, 0, 0]

i = 2: coin=2: dp[2] += dp[0] = 1
       dp = [1, 0, 1, 0, 0, 0]

i = 3: coin=2: dp[3] += dp[1] = 0  (no change)
       coin=3: dp[3] += dp[0] = 1
       dp = [1, 0, 1, 1, 0, 0]

i = 4: coin=2: dp[4] += dp[2] = 1
       coin=3: dp[4] += dp[1] = 0  (no change)
       dp = [1, 0, 1, 1, 1, 0]

i = 5: coin=2: dp[5] += dp[3] = 1
       coin=3: dp[5] += dp[2] = 1 → dp[5] = 2
       coin=5: dp[5] += dp[0] = 1 → dp[5] = 3
       dp = [1, 0, 1, 1, 1, 3]

Answer: dp[5] = 3
```

The 3 ways to make 5: `[2,3]`, `[3,2]`, `[5]`

### Visual Diagram

```
Building solutions for coins = [2, 3, 5]:

Sum 0: 1 way []
       │
Sum 1: 0 ways (no coin fits)
       │
Sum 2: 1 way ────── [2]
       │
Sum 3: 1 way ────── [3]
       │
Sum 4: 1 way ────── [2,2]
       │
Sum 5: 3 ways ───── [2,3], [3,2], [5]
       │
Sum 6: 3 ways ───── [2,2,2], [3,3], ...

For sum 5:
  └─ End with 2: need dp[3] = 1 way → [3]+[2] = [3,2]
  └─ End with 3: need dp[2] = 1 way → [2]+[3] = [2,3]
  └─ End with 5: need dp[0] = 1 way → []+[5] = [5]
  Total: 3 ways
```

### Code

```python
def solve(n, x, coins):
 """
 Count ordered ways (permutations) to make sum x with given coins.

 Time: O(n * x) where n = number of coins
 Space: O(x) for dp array
 """
 MOD = 10**9 + 7

 dp = [0] * (x + 1)
 dp[0] = 1  # Base case: one way to make sum 0

 # For each target sum
 for i in range(1, x + 1):
  # Try each coin as the last coin
  for coin in coins:
   if i >= coin:
    dp[i] = (dp[i] + dp[i - coin]) % MOD

 return dp[x]

# Read input
n, x = map(int, input().split())
coins = list(map(int, input().split()))
print(solve(n, x, coins))
```

### Complexity Analysis

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n × x) | Outer loop: x iterations, Inner loop: n coins |
| Space | O(x) | DP array of size x+1 |

---

## Common Mistakes

### Mistake 1: Wrong Loop Order (Most Common!)

```python
# WRONG - This counts COMBINATIONS, not permutations!
for coin in coins:         # Coin in outer loop
 for i in range(coin, x + 1):
  dp[i] += dp[i - coin]

# CORRECT - This counts PERMUTATIONS (what we want)
for i in range(1, x + 1):  # Sum in outer loop
 for coin in coins:
  if i >= coin:
   dp[i] += dp[i - coin]
```

**Why wrong loop order gives combinations:** When we process one coin across all sums before moving to the next coin, we're saying "use coin A first, then coin B" - preventing B before A.

### Mistake 2: Forgetting Modulo

```python
# WRONG - Integer overflow for large x
dp[i] = dp[i] + dp[i - coin]

# CORRECT
dp[i] = (dp[i] + dp[i - coin]) % MOD
```

### Mistake 3: Wrong Base Case

```python
# WRONG - Starting with all zeros
dp = [0] * (x + 1)
# Without dp[0] = 1, nothing can be built!

# CORRECT
dp[0] = 1
```

### Mistake 4: Not Handling Large Coins

```python
# Could crash if coin > x and we don't check
for coin in coins:
 dp[i] += dp[i - coin]  # i - coin could be negative!

# CORRECT
for coin in coins:
 if i >= coin:
  dp[i] += dp[i - coin]
```

---

## Edge Cases

| Case | Input | Output | Why |
|------|-------|--------|-----|
| Target is 0 | `x = 0` | 1 | One way: use no coins |
| No valid coins | `coins = [5], x = 3` | 0 | Can't make 3 with coin 5 |
| Single coin | `coins = [2], x = 4` | 1 | Only [2,2] works |
| Coin equals target | `coins = [5], x = 5` | 1 | Just use [5] |
| All coins > target | `coins = [10,20], x = 5` | 0 | No way to make 5 |

---

## Permutations vs Combinations: Key Distinction

| Aspect | Coin Combinations I | Coin Combinations II |
|--------|--------------------|--------------------|
| **Order** | Matters | Doesn't matter |
| **[2,3] vs [3,2]** | Different | Same |
| **Loop order** | Sum outer, coin inner | Coin outer, sum inner |
| **Counts** | More ways | Fewer ways |
| **Example x=5, c=[2,3]** | 3 ways | 2 ways |

---

## When to Use This Pattern

### Use Coin Combinations I When:
- Order of coins/items matters
- Different arrangements count as different solutions
- You're counting "sequences" or "orderings"
- Problem says "in how many ways" with implicit order

### Use Coin Combinations II When:
- Order doesn't matter
- Only the multiset of coins matters
- Problem says "distinct sets" or "combinations"

### Pattern Recognition Checklist:
- [ ] "How many sequences..." → **Permutations (this problem)**
- [ ] "How many ways to arrange..." → **Permutations**
- [ ] "How many combinations..." → **Combinations (Coin Combinations II)**
- [ ] "How many subsets..." → **Combinations**

---

## Related Problems

### Prerequisites (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Dice Combinations (CSES)](https://cses.fi/problemset/task/1633) | Same pattern with fixed coins 1-6 |
| [Climbing Stairs (LeetCode)](https://leetcode.com/problems/climbing-stairs/) | Simplest version with 2 coins |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Coin Combinations II (CSES)](https://cses.fi/problemset/task/1636) | Counts combinations (order doesn't matter) |
| [Combination Sum IV (LeetCode)](https://leetcode.com/problems/combination-sum-iv/) | Same as this problem |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Minimizing Coins (CSES)](https://cses.fi/problemset/task/1634) | Minimize number of coins |
| [Removing Digits (CSES)](https://cses.fi/problemset/task/1637) | Different "coin" selection rule |
| [Book Shop (CSES)](https://cses.fi/problemset/task/1158) | 2D DP (0/1 Knapsack) |

---

## Key Takeaways

1. **Core Pattern:** This is "counting permutations" DP - order matters, so we sum outer and coin inner.

2. **Loop Order Is Critical:**
   - Sum outer + coin inner = **permutations** (this problem)
   - Coin outer + sum inner = **combinations** (Coin Combinations II)

3. **Recurrence:** `dp[i] = Σ dp[i-c]` for all coins c where i ≥ c

4. **Base Case:** `dp[0] = 1` (empty sequence is one way to make sum 0)

5. **Complexity:** O(n × x) time, O(x) space

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why loop order determines permutations vs combinations
- [ ] Write the solution from scratch in under 5 minutes
- [ ] Modify for different constraints (e.g., limited coin usage)
- [ ] Explain the difference to Coin Combinations II clearly
- [ ] Trace through a small example by hand
