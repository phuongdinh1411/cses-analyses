---
layout: simple
title: "Coin Combinations II - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/coin_combinations_ii_analysis
difficulty: Easy
tags: [dp, counting, combinations, 1d-dp]
prerequisites: [coin_combinations_i]
---

# Coin Combinations II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Dynamic Programming |
| **Time Limit** | 1 second |
| **Key Technique** | 1D DP counting combinations |
| **CSES Link** | [Coin Combinations II](https://cses.fi/problemset/task/1636) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the "counting combinations" DP pattern
- [ ] Understand why loop order determines permutations vs combinations
- [ ] Implement the unbounded knapsack variant for counting
- [ ] Contrast this solution with Coin Combinations I

---

## Problem Statement

**Problem:** Consider a money system consisting of n coins. Each coin has a positive integer value. Your task is to calculate the number of distinct **unordered ways** you can produce a money sum x using the available coins.

**Key Point:** Order does NOT matter! Using coins {2, 3} is the SAME as {3, 2}.

**Input:**
- Line 1: Two integers n and x (number of coins and target sum)
- Line 2: n integers c1, c2, ..., cn (coin values)

**Output:**
- The number of ways modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 100
- 1 <= x <= 10^6
- 1 <= ci <= 10^6

### Example

```
Input:
3 9
2 3 5

Output:
3
```

**Explanation:** The 3 unordered ways (combinations) to make sum 9 with coins [2, 3, 5]:
1. {2, 2, 2, 3} = 9 (three 2s and one 3)
2. {2, 2, 5} = 9 (two 2s and one 5)
3. {3, 3, 3} = 9 (three 3s)

**Contrast with Coin Combinations I:** In that problem, {2,2,2,3}, {2,2,3,2}, {2,3,2,2}, {3,2,2,2} would count as 4 different ways. Here, they all count as just 1 way because order doesn't matter!

---

## Intuition: Why Loop Order Matters

This is the **critical concept** for this problem. The difference between Coin Combinations I and II is just the loop order!

### The Two Loop Orders

```python
# Coin Combinations I (PERMUTATIONS) - sum outer, coin inner
for target_sum in range(1, x + 1):
    for coin in coins:
        dp[target_sum] += dp[target_sum - coin]

# Coin Combinations II (COMBINATIONS) - coin outer, sum inner
for coin in coins:
    for target_sum in range(coin, x + 1):
        dp[target_sum] += dp[target_sum - coin]
```

### Why Does This Work?

**Permutations (sum outer):** For each sum, we try ALL coins as the possible "last" coin. This means we can reach sum 5 via [2,3] or [3,2] - both get counted separately.

**Combinations (coin outer):** We process coins ONE AT A TIME. When we're processing coin 3, we've already "decided" how many 2s to use. We can only ADD 3s to existing solutions - we can never go back and add more 2s. This enforces an implicit ordering: we use 2s first, then 3s, then 5s.

### Visual Explanation

```
PERMUTATIONS (wrong loop order for this problem):
Sum 5: Try coin 2 -> need dp[3] -> already includes [3] -> gives [3,2]
       Try coin 3 -> need dp[2] -> already includes [2] -> gives [2,3]
       Both [2,3] and [3,2] counted separately!

COMBINATIONS (correct loop order):
Process coin 2 first: dp[2]=1 ([2,2]->wait, dp[2]=1 means {2})
Process coin 3 next:  dp[5] can use dp[2] -> {2} + 3 = {2,3}
                      We CANNOT get {3,2} because 3 is processed AFTER 2
Only {2,3} counted once!
```

---

## Solution: Dynamic Programming

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i]` | Number of **unordered** ways (combinations) to make sum exactly `i` |

**In plain English:** `dp[9]` answers "How many different combinations of coins (as multisets) add up to 9?"

### State Transition

```
dp[i] = dp[i] + dp[i - coin]   (for current coin being processed)
```

**Why?** When processing a specific coin:
- `dp[i]` already contains ways to make sum `i` using PREVIOUS coins only
- `dp[i - coin]` contains ways to make sum `i - coin`
- Adding current coin to each way in `dp[i - coin]` gives new ways to make `i`

### Base Case

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 1 | One way to make sum 0: use no coins (empty multiset) |

### Algorithm

```
1. Create dp array of size x+1, initialize to 0
2. Set dp[0] = 1 (base case)
3. For each coin in coins:           # Outer: process one coin type at a time
     For i from coin to x:           # Inner: update all reachable sums
       dp[i] = (dp[i] + dp[i - coin]) % MOD
4. Return dp[x]
```

---

## Dry Run Example

Input: `coins = [2, 3, 5], x = 9`

```
Initialize: dp = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                  ^
                  dp[0] = 1 (base case)

=== Processing coin = 2 ===
i=2: dp[2] += dp[0] = 1    Meaning: {2}
i=3: dp[3] += dp[1] = 0    (no change)
i=4: dp[4] += dp[2] = 1    Meaning: {2,2}
i=5: dp[5] += dp[3] = 0    (no change)
i=6: dp[6] += dp[4] = 1    Meaning: {2,2,2}
i=7: dp[7] += dp[5] = 0    (no change)
i=8: dp[8] += dp[6] = 1    Meaning: {2,2,2,2}
i=9: dp[9] += dp[7] = 0    (no change)

dp = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
         {2} {2,2} {2,2,2} {2,2,2,2}

=== Processing coin = 3 ===
i=3: dp[3] += dp[0] = 1    Meaning: {3}
i=4: dp[4] += dp[1] = 0    (no change, still 1)
i=5: dp[5] += dp[2] = 1    Meaning: {2,3}
i=6: dp[6] += dp[3] = 2    Meanings: {2,2,2}, {3,3}
i=7: dp[7] += dp[4] = 1    Meaning: {2,2,3}
i=8: dp[8] += dp[5] = 2    Meanings: {2,2,2,2}, {2,3,3}
i=9: dp[9] += dp[6] = 2    Meanings: {2,2,2,3}, {3,3,3}

dp = [1, 0, 1, 1, 1, 1, 2, 1, 2, 2]

=== Processing coin = 5 ===
i=5: dp[5] += dp[0] = 2    Add: {5}
i=6: dp[6] += dp[1] = 2    (no change)
i=7: dp[7] += dp[2] = 2    Add: {2,5}
i=8: dp[8] += dp[3] = 3    Add: {3,5}
i=9: dp[9] += dp[4] = 3    Add: {2,2,5}

dp = [1, 0, 1, 1, 1, 2, 2, 2, 3, 3]

Answer: dp[9] = 3
```

**The 3 combinations:** {2,2,2,3}, {3,3,3}, {2,2,5}

---

## Code

### Python

```python
def solve(n, x, coins):
    """
    Count unordered ways (combinations) to make sum x with given coins.

    Time: O(n * x) where n = number of coins
    Space: O(x) for dp array
    """
    MOD = 10**9 + 7

    dp = [0] * (x + 1)
    dp[0] = 1  # Base case: one way to make sum 0

    # Process each coin type one at a time
    for coin in coins:
        # Update all sums reachable with this coin
        for i in range(coin, x + 1):
            dp[i] = (dp[i] + dp[i - coin]) % MOD

    return dp[x]

# Read input
n, x = map(int, input().split())
coins = list(map(int, input().split()))
print(solve(n, x, coins))
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    const int MOD = 1e9 + 7;

    int n, x;
    cin >> n >> x;

    vector<int> coins(n);
    for (int i = 0; i < n; i++) {
        cin >> coins[i];
    }

    vector<long long> dp(x + 1, 0);
    dp[0] = 1;

    // Coin outer, sum inner = COMBINATIONS
    for (int coin : coins) {
        for (int i = coin; i <= x; i++) {
            dp[i] = (dp[i] + dp[i - coin]) % MOD;
        }
    }

    cout << dp[x] << "\n";
    return 0;
}
```

### Complexity Analysis

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * x) | Outer loop: n coins, Inner loop: up to x iterations |
| Space | O(x) | DP array of size x+1 |

---

## Common Mistakes

### Mistake 1: Wrong Loop Order (Most Common!)

```python
# WRONG - This counts PERMUTATIONS, not combinations!
for i in range(1, x + 1):      # Sum in outer loop
    for coin in coins:
        if i >= coin:
            dp[i] += dp[i - coin]

# CORRECT - This counts COMBINATIONS (what we want)
for coin in coins:             # Coin in outer loop
    for i in range(coin, x + 1):
        dp[i] += dp[i - coin]
```

**This is THE mistake students make.** Remember:
- **Coin outer = Combinations** (this problem)
- **Sum outer = Permutations** (Coin Combinations I)

### Mistake 2: Forgetting Modulo

```python
# WRONG - Integer overflow for large x
dp[i] = dp[i] + dp[i - coin]

# CORRECT
dp[i] = (dp[i] + dp[i - coin]) % MOD
```

### Mistake 3: Wrong Base Case

```python
# WRONG - No way to build anything
dp = [0] * (x + 1)

# CORRECT - Need dp[0] = 1 as the "seed"
dp[0] = 1
```

### Mistake 4: Starting Inner Loop at Wrong Index

```python
# WRONG - Crashes when coin > i
for i in range(1, x + 1):
    dp[i] += dp[i - coin]  # i - coin could be negative!

# CORRECT - Start at coin value
for i in range(coin, x + 1):
    dp[i] += dp[i - coin]
```

---

## Comparison: Coin Combinations I vs II

| Aspect | Coin Combinations I | Coin Combinations II |
|--------|--------------------|--------------------|
| **Order** | Matters (permutations) | Doesn't matter (combinations) |
| **{2,3} vs {3,2}** | Different (count both) | Same (count once) |
| **Loop order** | Sum outer, coin inner | **Coin outer, sum inner** |
| **Answer count** | More (or equal) | Fewer (or equal) |
| **Example: x=5, coins=[2,3,5]** | 3 ways | 2 ways |
| **Example: x=9, coins=[2,3,5]** | 8 ways | 3 ways |
| **CSES Task** | 1635 | 1636 |

### Memory Aid

Think of it this way:
- **Permutations = Playing with all toys at once** (sum outer: at each sum, try all coins)
- **Combinations = Putting toys away one type at a time** (coin outer: fully decide on each coin before moving to next)

---

## Edge Cases

| Case | Input | Output | Why |
|------|-------|--------|-----|
| Target is 0 | `x = 0` | 1 | One way: use no coins (empty set) |
| No valid coins | `coins = [5], x = 3` | 0 | Can't make 3 with only coin 5 |
| Single coin divides target | `coins = [2], x = 4` | 1 | Only {2,2} |
| Single coin doesn't divide | `coins = [2], x = 5` | 0 | Can't make odd sum with even coin |
| Coin equals target | `coins = [5], x = 5` | 1 | Just {5} |

---

## Related Problems

### Prerequisites (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Coin Combinations I (CSES)](https://cses.fi/problemset/task/1635) | Understand permutation counting first |
| [Dice Combinations (CSES)](https://cses.fi/problemset/task/1633) | Simpler version of permutation counting |

### Similar Problems
| Problem | Key Similarity |
|---------|----------------|
| [Coin Change 2 (LeetCode)](https://leetcode.com/problems/coin-change-ii/) | Identical problem |
| [Combination Sum IV (LeetCode)](https://leetcode.com/problems/combination-sum-iv/) | Permutation version (like Coin Combinations I) |

### Harder Problems (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Minimizing Coins (CSES)](https://cses.fi/problemset/task/1634) | Minimize count instead of counting ways |
| [Money Sums (CSES)](https://cses.fi/problemset/task/1745) | Which sums are possible (subset sum variant) |
| [Book Shop (CSES)](https://cses.fi/problemset/task/1158) | 2D DP (bounded knapsack) |

---

## Key Takeaways

1. **The Golden Rule:** Loop order determines whether you count permutations or combinations:
   - **Coin outer, sum inner = Combinations** (this problem)
   - **Sum outer, coin inner = Permutations** (Coin Combinations I)

2. **Why it works:** Processing coins one at a time enforces an implicit ordering. Once you're done with coin A, you can't go back and add more of it.

3. **Recurrence:** `dp[i] = dp[i] + dp[i - coin]` (for each coin being processed)

4. **Base Case:** `dp[0] = 1` (empty multiset is one way to make sum 0)

5. **Complexity:** O(n * x) time, O(x) space - same as Coin Combinations I!

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why coin-outer gives combinations and sum-outer gives permutations
- [ ] Write both Coin Combinations I and II from scratch
- [ ] Trace through a small example showing how the loop order prevents double-counting
- [ ] Identify which version to use based on problem wording
- [ ] Explain the relationship to the unbounded knapsack problem
