---
layout: simple
title: "Missing Coin Sum - Greedy Problem"
permalink: /problem_soulutions/sorting_and_searching/missing_coin_sum_analysis
difficulty: Medium
tags: [greedy, sorting, math, invariant]
prerequisites: []
---

# Missing Coin Sum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Greedy / Sorting |
| **Time Limit** | 1 second |
| **Key Technique** | Greedy Invariant |
| **CSES Link** | [Missing Coin Sum](https://cses.fi/problemset/task/2183) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize the greedy invariant pattern for constructible sums
- [ ] Understand why sorting enables greedy coin analysis
- [ ] Apply the "reachable range extension" technique to similar problems
- [ ] Prove correctness of greedy algorithms using loop invariants

---

## Problem Statement

**Problem:** Given n coins with positive values, find the smallest positive sum that cannot be formed using any subset of these coins.

**Input:**
- Line 1: Integer n (number of coins)
- Line 2: n integers representing coin values

**Output:**
- The smallest positive integer sum that cannot be constructed

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= coin value <= 10^9

### Example

```
Input:
5
2 9 1 2 7

Output:
6
```

**Explanation:** With coins [1, 2, 2, 7, 9], we can make:
- 1 (using coin 1)
- 2 (using coin 2)
- 3 (using coins 1+2)
- 4 (using coins 2+2)
- 5 (using coins 1+2+2)
- But we cannot make 6 (smallest coin after 5 would be 7, which skips 6)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** If we can already construct all sums from 1 to S, what happens when we add a new coin?

The core insight is a **greedy invariant**: If we process coins in sorted order and can currently make all sums from 1 to S, then adding a coin with value `c` allows us to make all sums from 1 to S+c **only if c <= S+1**.

### Breaking Down the Problem

1. **What are we looking for?** The smallest gap in constructible sums
2. **What information do we have?** A set of coin values
3. **What is the relationship between input and output?** If any coin is too large to "bridge" to the next sum, we have found our answer

### The Greedy Invariant

```
INVARIANT: After processing coins, we can make all sums in [1, current_sum]

If next coin <= current_sum + 1:
    We can extend our range to [1, current_sum + coin]

If next coin > current_sum + 1:
    We CANNOT make (current_sum + 1), so that is our answer
```

**Why does this work?**

Suppose we can make every sum from 1 to S. When we add coin c where c <= S+1:
- We can still make 1 to S (without using c)
- We can now make S+1 to S+c (by adding c to sums 0 to S)
- Since c <= S+1, there is no gap between S and S+1

---

## Solution 1: Brute Force (DP)

### Idea

Use dynamic programming to track all possible sums, then find the first missing one.

### Algorithm

1. Create a boolean array where dp[i] = true if sum i is achievable
2. For each coin, update reachable sums
3. Find the first index where dp[i] = false

### Code

```python
def solve_brute_force(n, coins):
    """
    DP solution - works but too slow for large sums.

    Time: O(n * S) where S = sum of coins
    Space: O(S)
    """
    total = sum(coins)
    dp = [False] * (total + 2)
    dp[0] = True

    for coin in coins:
        # Process backwards to avoid using same coin twice
        for s in range(total, coin - 1, -1):
            if dp[s - coin]:
                dp[s] = True

    # Find first missing sum
    for i in range(1, total + 2):
        if not dp[i]:
            return i

    return total + 1
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * S) | For each coin, update up to S states |
| Space | O(S) | Boolean array for all possible sums |

### Why This Works (But Is Slow)

This correctly finds all achievable sums but is impractical when coin values are large (up to 10^9). The greedy approach avoids materializing the DP array entirely.

---

## Solution 2: Optimal Greedy Solution

### Key Insight

> **The Trick:** Sort coins and maintain the invariant: "We can make all sums 1 to current_sum." If the next coin exceeds current_sum + 1, we found our answer.

### The Greedy Rule

```
If we can make [1, S] and next coin c <= S+1:
    We can now make [1, S+c]

If next coin c > S+1:
    We cannot make S+1, return S+1
```

### Algorithm

1. Sort coins in ascending order
2. Initialize current_sum = 0 (we can make sum 0 using no coins)
3. For each coin in sorted order:
   - If coin > current_sum + 1, return current_sum + 1
   - Otherwise, current_sum += coin
4. Return current_sum + 1

### Dry Run Example

Let us trace through with input `n = 5, coins = [2, 9, 1, 2, 7]`:

```
After sorting: [1, 2, 2, 7, 9]
current_sum = 0 (can make: nothing yet)

Step 1: coin = 1
  Check: 1 <= 0 + 1? YES (1 <= 1)
  current_sum = 0 + 1 = 1
  Can now make: [1, 1]

Step 2: coin = 2
  Check: 2 <= 1 + 1? YES (2 <= 2)
  current_sum = 1 + 2 = 3
  Can now make: [1, 3]

Step 3: coin = 2
  Check: 2 <= 3 + 1? YES (2 <= 4)
  current_sum = 3 + 2 = 5
  Can now make: [1, 5]

Step 4: coin = 7
  Check: 7 <= 5 + 1? NO (7 > 6)
  STOP! Cannot make 6.
  Return: 5 + 1 = 6

Answer: 6
```

### Visual Diagram

```
Sorted coins: [1, 2, 2, 7, 9]

Reachable range after each coin:

  coin=1    |-----|                  range: [1,1]
            1

  coin=2    |-----------|           range: [1,3]
            1     2     3

  coin=2    |-----------------|     range: [1,5]
            1  2  3  4  5

  coin=7    GAP at 6!
            1  2  3  4  5  ?  7
                           ^
                           Cannot reach 6!

  Answer: 6
```

### Code

**Python Solution:**

```python
def solve(n, coins):
    """
    Optimal greedy solution.

    Time: O(n log n) - dominated by sorting
    Space: O(1) - only need one variable
    """
    coins.sort()
    current_sum = 0

    for coin in coins:
        # If coin is too large, we found a gap
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += coin

    # All coins processed, smallest missing is total + 1
    return current_sum + 1


def main():
    n = int(input())
    coins = list(map(int, input().split()))
    print(solve(n, coins))


if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Sorting dominates; single pass is O(n) |
| Space | O(1) | Only one variable needed (excluding input) |

---

## Common Mistakes

### Mistake 1: Forgetting to Sort

```python
# WRONG
def solve_wrong(coins):
    current_sum = 0
    for coin in coins:  # NOT sorted!
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += coin
    return current_sum + 1

# Input: [5, 1, 2]
# Wrong output: 1 (because 5 > 0+1 immediately)
# Correct output: 9 (sorted: [1,2,5] can make 1-8)
```

**Problem:** Without sorting, we may encounter a large coin before small ones that could fill the gap.
**Fix:** Always sort coins first.

### Mistake 2: Off-by-One in the Condition

```python
# WRONG
if coin > current_sum:  # Should be current_sum + 1
    return current_sum

# CORRECT
if coin > current_sum + 1:
    return current_sum + 1
```

**Problem:** The condition checks if we can reach the NEXT sum (current_sum + 1), not the current one.
**Fix:** Use `current_sum + 1` in both the comparison and return value.

**Problem:** With n = 2*10^5 coins each up to 10^9, the sum can reach 2*10^14.
**Fix:** Use `long long` in C++.

### Mistake 4: Not Handling the "All Sums Possible" Case

```python
# WRONG - missing the final return
def solve_wrong(coins):
    coins.sort()
    current_sum = 0
    for coin in coins:
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += coin
    # Missing: return current_sum + 1

# CORRECT
def solve(coins):
    coins.sort()
    current_sum = 0
    for coin in coins:
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += coin
    return current_sum + 1  # All coins processed
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No coin with value 1 | `[2, 3, 4]` | 1 | Cannot make 1 without a 1-coin |
| Single coin = 1 | `[1]` | 2 | Can only make 1 |
| Single coin > 1 | `[5]` | 1 | Cannot make 1 |
| Consecutive coins | `[1, 2, 3]` | 7 | Can make 1-6, not 7 |
| All ones | `[1, 1, 1, 1]` | 5 | Can make 1-4 |
| Large gap | `[1, 2, 100]` | 4 | 100 > 3+1, cannot make 4 |
| Max values | `[10^9]` | 1 | Single large coin |

---

## When to Use This Pattern

### Use This Approach When:
- Finding the smallest unreachable sum from a set of values
- Problems involving "coverage" or "reachability" of consecutive integers
- Greedy problems where sorted order reveals optimal structure

### Dont Use When:
- Coins have limited quantities (need modified approach)
- You need to count ways to make each sum (use DP)
- The problem requires tracking which coins are used

### Pattern Recognition Checklist:
- [ ] Looking for smallest missing sum? -> **Consider greedy with sorted coins**
- [ ] Need to extend a "reachable range"? -> **Check if next element bridges the gap**
- [ ] Can formulate a loop invariant about coverage? -> **Greedy likely works**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Two Sum](https://leetcode.com/problems/two-sum/) | Basic sum-finding with hash maps |
| [Coin Combinations I](https://cses.fi/problemset/task/1635) | DP approach to coin sums |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Patching Array (LeetCode 330)](https://leetcode.com/problems/patching-array/) | Same invariant, but ADD coins to fill gaps |
| [Coin Combinations II](https://cses.fi/problemset/task/1636) | Count ordered ways to make sums |
| [Maximum Number of Consecutive Values (LC 1798)](https://leetcode.com/problems/maximum-number-of-consecutive-values-you-can-make/) | Identical problem, different framing |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Minimum Cost to Make Array Equal](https://leetcode.com/problems/minimum-cost-to-make-array-equal/) | Weighted median selection |
| [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Binary search + greedy |

---

## Key Takeaways

1. **The Core Idea:** If we can make [1, S] and have coin c <= S+1, we can extend to [1, S+c]
2. **Time Optimization:** Sorting enables O(n log n) instead of exponential DP
3. **Space Trade-off:** O(1) space by using invariant instead of DP array
4. **Pattern:** Greedy interval extension / reachable range expansion

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Prove why the greedy invariant is correct
- [ ] Identify the same pattern in "Patching Array" (LeetCode 330)
- [ ] Implement in under 5 minutes with proper edge case handling

---

## Additional Resources

- [CSES Missing Coin Sum](https://cses.fi/problemset/task/2183) - Smallest unachievable sum
- [CP-Algorithms: Greedy Algorithms](https://cp-algorithms.com/)
