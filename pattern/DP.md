---
layout: simple
title: "Dynamic Programming Patterns"
permalink: /pattern/dp
---

# Dynamic Programming — Comprehensive Pattern Guide

---

## What Is DP?

Dynamic Programming is a technique for solving problems that have two properties:

1. **Optimal substructure**: The optimal solution can be built from optimal solutions of subproblems
2. **Overlapping subproblems**: The same subproblems are solved repeatedly

DP = **recursion + memoization** (or equivalently, building a table bottom-up).

```
Fibonacci WITHOUT DP:              Fibonacci WITH DP:

       fib(5)                          fib(5)
      /      \                        /      \
   fib(4)   fib(3)                fib(4)   fib(3) <- cached!
   /    \    /    \               /    \
fib(3) fib(2) fib(2) fib(1)  fib(3) fib(2) <- cached!
 ...    ...    ...              /    \
                            fib(2) fib(1) <- cached!

Calls: 15 (exponential)        Calls: 5 (linear)
```

---

## Table of Contents

1. [How to Approach DP Problems](#1-how-to-approach-dp-problems)
2. [Top-Down vs Bottom-Up](#2-top-down-vs-bottom-up)
3. [Linear DP](#3-linear-dp)
4. [Grid DP](#4-grid-dp)
5. [Knapsack Family](#5-knapsack-family)
6. [Longest Increasing Subsequence](#6-longest-increasing-subsequence)
7. [Longest Common Subsequence](#7-longest-common-subsequence)
8. [Interval DP](#8-interval-dp)
9. [State Machine DP](#9-state-machine-dp)
10. [Tree DP](#10-tree-dp)
11. [Bitmask DP](#11-bitmask-dp)
12. [Digit DP](#12-digit-dp)
13. [Probability / Expected Value DP](#13-probability--expected-value-dp)
14. [DP on DAGs](#14-dp-on-dags)
15. [DP Optimizations](#15-dp-optimizations)
16. [Pattern Recognition Cheat Sheet](#16-pattern-recognition-cheat-sheet)

---

## 1. How to Approach DP Problems

### The 5-Step Framework

Every DP problem can be solved with this framework:

```
Step 1: DEFINE THE STATE
        "What information do I need to describe a subproblem?"
        -> dp[i] = ..., dp[i][j] = ...

Step 2: DEFINE THE TRANSITION
        "How do I build the answer from smaller subproblems?"
        -> dp[i] = some function of dp[i-1], dp[i-2], ...

Step 3: DEFINE THE BASE CASE
        "What are the smallest subproblems I know the answer to?"
        -> dp[0] = ..., dp[1] = ...

Step 4: DEFINE THE ANSWER
        "Which state gives me the final answer?"
        -> return dp[n], or max(dp), or dp[n][target]

Step 5: OPTIMIZE SPACE (optional)
        "Do I only need the last row/few states?"
        -> reduce from O(n^2) space to O(n)
```

### Recognizing DP Problems

| Signal | Example |
|--------|---------|
| "Count the number of ways" | How many paths from top-left to bottom-right? |
| "Minimum/maximum cost" | Minimum coins to make change |
| "Is it possible?" | Can we partition into two equal-sum subsets? |
| "Longest/shortest" | Longest increasing subsequence |
| Choices at each step | Take or skip each item |
| Problem has optimal substructure | Shortest path through a grid |

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing state | Add dimensions until subproblems are unique |
| Wrong transition direction | Ensure you only use already-computed states |
| Off-by-one in base cases | Trace through smallest examples manually |
| Not considering "do nothing" | Often dp[i] = dp[i-1] is a valid transition |
| Forgetting modular arithmetic | Apply MOD at every addition/multiplication |

---

## 2. Top-Down vs Bottom-Up

### Top-Down (Memoization)

Start from the final answer, recurse into subproblems, cache results.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

### Bottom-Up (Tabulation)

Start from base cases, fill the table iteratively.

```python
def fib(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

### When to Use Which

| | Top-Down | Bottom-Up |
|--|----------|-----------|
| **Pros** | Natural to think recursively; only computes needed states | No recursion overhead; easier to optimize space |
| **Cons** | Recursion limit; function call overhead | Must figure out correct iteration order; computes all states |
| **Best for** | Complex state spaces; sparse states | Simple iteration order; when you need all states |
| **Contest tip** | Start with top-down, convert if TLE | Preferred for performance-critical problems |

### Space Optimization

If `dp[i]` only depends on `dp[i-1]` (and possibly `dp[i-2]`), you don't need the full array:

```python
# Before: O(n) space
dp = [0] * (n + 1)
dp[1] = 1
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]

# After: O(1) space
a, b = 0, 1
for _ in range(2, n + 1):
    a, b = b, a + b
```

---

## 3. Linear DP

The simplest DP pattern: states form a 1D sequence.

### Pattern

```
dp[i] = answer considering elements 0..i (or i..n-1)
dp[i] depends on dp[i-1], dp[i-2], ..., or dp[j] for j < i
```

### Example: Maximum Subarray Sum (Kadane's Algorithm)

**Problem**: Find the contiguous subarray with the largest sum.

```
Array:  [-2, 1, -3, 4, -1, 2, 1, -5, 4]

State:  dp[i] = maximum subarray sum ENDING at index i

Transition:
  dp[i] = max(arr[i], dp[i-1] + arr[i])
          ^           ^
          start new   extend previous

Base: dp[0] = arr[0]
Answer: max(dp)
```

```python
def max_subarray(arr):
    dp = arr[0]
    best = arr[0]
    for i in range(1, len(arr)):
        dp = max(arr[i], dp + arr[i])
        best = max(best, dp)
    return best
```

### Example: Coin Combinations (Count Ways)

**Problem**: Given coins `[1, 3, 5]`, how many ways to make sum `n`?

```
State:  dp[s] = number of ways to form sum s

Transition:
  dp[s] = sum(dp[s - coin] for coin in coins if s >= coin)

Base: dp[0] = 1 (one way to make sum 0: use no coins)
Answer: dp[n]
```

```python
def coin_ways(coins, n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for s in range(1, n + 1):
        for coin in coins:
            if s >= coin:
                dp[s] += dp[s - coin]
    return dp[n]
```

### Example: House Robber

**Problem**: Rob houses in a line, can't rob two adjacent. Maximize total.

```
Houses: [2, 7, 9, 3, 1]

State:  dp[i] = max money from houses 0..i

Transition:
  dp[i] = max(dp[i-1],          # skip house i
              dp[i-2] + arr[i])  # rob house i

Base: dp[0] = arr[0], dp[1] = max(arr[0], arr[1])
Answer: dp[n-1]
```

```python
def rob(nums):
    if len(nums) == 1:
        return nums[0]
    a, b = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        a, b = b, max(b, a + nums[i])
    return b
```

---

## 4. Grid DP

States are 2D positions in a grid.

### Pattern

```
dp[i][j] = answer for cell (i, j)
dp[i][j] depends on dp[i-1][j], dp[i][j-1], dp[i-1][j-1], etc.
```

### Example: Unique Paths

**Problem**: Count paths from top-left to bottom-right, moving only right or down.

```
Grid 3x3:

dp[0][0]=1  dp[0][1]=1  dp[0][2]=1
dp[1][0]=1  dp[1][1]=2  dp[1][2]=3
dp[2][0]=1  dp[2][1]=3  dp[2][2]=6

Transition: dp[i][j] = dp[i-1][j] + dp[i][j-1]
                        (from above) + (from left)
Answer: dp[m-1][n-1] = 6
```

```python
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]
```

### Example: Minimum Path Sum

**Problem**: Find the path from top-left to bottom-right with minimum sum.

```
Grid:
1  3  1
1  5  1
4  2  1

dp:
1  4  5
2  7  6
6  8  7

Transition: dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
Answer: dp[m-1][n-1] = 7  (path: 1->3->1->1->1)
```

```python
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
    return dp[m-1][n-1]
```

### Space Optimization for Grid DP

Since each row only depends on the previous row:

```python
def min_path_sum_optimized(grid):
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = grid[0][0]
    for j in range(1, n):
        dp[j] = dp[j-1] + grid[0][j]
    for i in range(1, m):
        dp[0] += grid[i][0]
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j-1])
            #                       ^ old row  ^ current row
    return dp[n-1]
```

---

## 5. Knapsack Family

The most important DP family. Three major variants.

### 5.1 0/1 Knapsack

**Problem**: N items, each with weight and value. Pick items to maximize value without exceeding capacity W. Each item used **at most once**.

```
State:  dp[i][w] = max value using items 0..i-1 with capacity w

Transition:
  dp[i][w] = max(
      dp[i-1][w],                    # don't take item i
      dp[i-1][w - weight[i]] + val[i]  # take item i (if w >= weight[i])
  )

Base: dp[0][w] = 0 for all w
Answer: dp[n][W]
```

```python
def knapsack_01(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i-1][w]  # don't take
            if w >= weights[i-1]:
                dp[i][w] = max(dp[i][w],
                               dp[i-1][w - weights[i-1]] + values[i-1])
    return dp[n][W]
```

**Space-optimized** (iterate w in reverse to avoid using item twice):

```python
def knapsack_01_optimized(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i] - 1, -1):  # REVERSE!
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[W]
```

**Why reverse?** Forward iteration would let `dp[w - weights[i]]` use the current item's contribution (already updated in this iteration), effectively using the item multiple times. Reverse ensures we only use `dp` values from the previous iteration.

### 5.2 Unbounded Knapsack

**Problem**: Same as 0/1, but each item can be used **unlimited times**.

```python
def knapsack_unbounded(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(weights[i], W + 1):  # FORWARD! (reuse allowed)
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[W]
```

Forward iteration naturally allows reuse: `dp[w - weights[i]]` may already include item `i`.

### 5.3 Bounded Knapsack

**Problem**: Item i can be used at most `count[i]` times.

**Approach**: Convert each item with count `c` into binary groups: 1, 2, 4, ..., remainder. This reduces to 0/1 knapsack with O(N log C) items.

```python
def knapsack_bounded(weights, values, counts, W):
    # binary grouping: split count c into 1, 2, 4, ..., remainder
    items = []
    for i in range(len(weights)):
        c = counts[i]
        k = 1
        while k <= c:
            items.append((weights[i] * k, values[i] * k))
            c -= k
            k *= 2
        if c > 0:
            items.append((weights[i] * c, values[i] * c))

    # now solve 0/1 knapsack
    dp = [0] * (W + 1)
    for w_item, v_item in items:
        for w in range(W, w_item - 1, -1):
            dp[w] = max(dp[w], dp[w - w_item] + v_item)
    return dp[W]
```

### Knapsack Variant Summary

| Variant | Item usage | Iteration direction | Time |
|---------|-----------|-------------------|------|
| 0/1 | At most once | **Reverse** w | O(NW) |
| Unbounded | Unlimited | **Forward** w | O(NW) |
| Bounded | At most c[i] | Binary grouping + reverse | O(NW log C) |

### Common Knapsack Disguises

| Problem | Knapsack form |
|---------|--------------|
| Subset Sum | 0/1 knapsack, values = weights, check dp[target] > 0 |
| Partition Equal Subset | 0/1 knapsack with target = total_sum / 2 |
| Coin Change (min coins) | Unbounded, minimize count instead of maximize value |
| Coin Change (count ways) | Unbounded, count instead of max |
| Target Sum (+/-) | 0/1 knapsack, target = (sum + target) / 2 |

---

## 6. Longest Increasing Subsequence

### Problem

Find the length of the longest strictly increasing subsequence.

```
Array: [10, 9, 2, 5, 3, 7, 101, 18]
LIS:   [2, 3, 7, 101] or [2, 3, 7, 18] or [2, 5, 7, 101] ...
Length: 4
```

### O(N^2) DP Solution

```
State:  dp[i] = length of LIS ending at index i

Transition:
  dp[i] = 1 + max(dp[j] for j < i if arr[j] < arr[i])

Base: dp[i] = 1 for all i (each element is a subsequence of length 1)
Answer: max(dp)
```

```python
def lis_n2(arr):
    n = len(arr)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

### O(N log N) with Binary Search

Maintain a list `tails` where `tails[k]` = smallest ending element of all increasing subsequences of length `k+1`.

```python
from bisect import bisect_left

def lis_nlogn(arr):
    tails = []
    for x in arr:
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)     # extends longest subsequence
        else:
            tails[pos] = x      # found a better (smaller) ending
    return len(tails)
```

### Trace

```
arr = [10, 9, 2, 5, 3, 7, 101, 18]

x=10:  tails = [10]
x=9:   tails = [9]           (9 replaces 10 at pos 0)
x=2:   tails = [2]           (2 replaces 9)
x=5:   tails = [2, 5]        (5 extends)
x=3:   tails = [2, 3]        (3 replaces 5 at pos 1)
x=7:   tails = [2, 3, 7]     (7 extends)
x=101: tails = [2, 3, 7, 101] (101 extends)
x=18:  tails = [2, 3, 7, 18]  (18 replaces 101 at pos 3)

Length = 4
```

Note: `tails` is NOT the actual LIS. It's a working structure. To reconstruct the actual LIS, track parent pointers.

### Variations

| Variation | Change |
|-----------|--------|
| Non-decreasing (allow equal) | Use `bisect_right` instead of `bisect_left` |
| Longest Decreasing | Reverse the array, find LIS |
| Count of LIS | Additional array tracking count per length |
| Minimum deletions for sorted | n - LIS length |

---

## 7. Longest Common Subsequence

### Problem

Find the length of the longest subsequence common to two strings.

```
s1 = "ABCBDAB"
s2 = "BDCAB"
LCS = "BCAB" (length 4)
```

### Implementation

```
State:  dp[i][j] = LCS of s1[0..i-1] and s2[0..j-1]

Transition:
  If s1[i-1] == s2[j-1]:
      dp[i][j] = dp[i-1][j-1] + 1     # characters match, extend
  Else:
      dp[i][j] = max(dp[i-1][j],       # skip from s1
                      dp[i][j-1])       # skip from s2

Base: dp[0][j] = dp[i][0] = 0
Answer: dp[m][n]
```

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

### Reconstruct the LCS

```python
def lcs_string(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # backtrack
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            result.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(result))
```

### LCS Family

| Problem | Relation to LCS |
|---------|----------------|
| Edit Distance | Similar DP table, different transition |
| Shortest Common Supersequence | `len(s1) + len(s2) - LCS` |
| Longest Palindromic Subsequence | LCS of string and its reverse |
| Diff (version control) | LCS = unchanged lines |

---

## 8. Interval DP

### Pattern

Problems where the answer for a range `[i, j]` depends on sub-ranges.

```
State:  dp[i][j] = answer for the subarray/substring from i to j

Transition:
  dp[i][j] = best over all split points k in [i, j-1]:
              combine(dp[i][k], dp[k+1][j])

Iteration: by increasing length of interval
Base: dp[i][i] = base value (single element)
Answer: dp[0][n-1]
```

### Example: Matrix Chain Multiplication

**Problem**: Given matrices A1 x A2 x ... x An, find the order of multiplication that minimizes total scalar multiplications.

```
dimensions = [10, 30, 5, 60]
Matrices: A1(10x30), A2(30x5), A3(5x60)

(A1*A2)*A3 = 10*30*5 + 10*5*60 = 1500 + 3000 = 4500
A1*(A2*A3) = 30*5*60 + 10*30*60 = 9000 + 18000 = 27000

Optimal: (A1*A2)*A3 = 4500
```

```python
def matrix_chain(dims):
    n = len(dims) - 1  # number of matrices
    dp = [[0] * n for _ in range(n)]

    # length of chain
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = (dp[i][k] + dp[k+1][j] +
                        dims[i] * dims[k+1] * dims[j+1])
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n-1]
```

### Example: Burst Balloons

**Problem**: Burst balloons in an order to maximize coins. Bursting balloon i gives `nums[left] * nums[i] * nums[right]`.

```python
def max_coins(nums):
    nums = [1] + nums + [1]  # add boundary balloons
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):  # k = last balloon to burst
                dp[i][j] = max(dp[i][j],
                    dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])

    return dp[0][n-1]
```

### Example: Palindrome Partitioning (Min Cuts)

**Problem**: Minimum cuts to partition a string into palindromes.

```python
def min_cut(s):
    n = len(s)

    # precompute: is s[i..j] a palindrome?
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i+1][j-1]):
                is_pal[i][j] = True

    # dp[i] = min cuts for s[0..i]
    dp = list(range(n))  # worst case: cut after every character
    for i in range(1, n):
        if is_pal[0][i]:
            dp[i] = 0
            continue
        for j in range(1, i + 1):
            if is_pal[j][i]:
                dp[i] = min(dp[i], dp[j-1] + 1)

    return dp[n-1]
```

---

## 9. State Machine DP

### Pattern

The problem has distinct **states** you can be in, with transitions between them. Each step, you transition between states.

```
State Machine:

   ┌──────┐    buy     ┌──────┐
   │ NOT  │ ──────────> │ HOLD │
   │HOLDING│ <────────── │  ING │
   └──────┘    sell     └──────┘
```

### Example: Best Time to Buy and Sell Stock with Cooldown

**Problem**: Buy and sell stocks, but after selling you must wait one day.

```
States: REST (not holding, can buy)
        HOLD (holding stock, can sell)
        COOL (just sold, must wait)

Transitions:
  rest[i] = max(rest[i-1], cool[i-1])       # do nothing or finish cooldown
  hold[i] = max(hold[i-1], rest[i-1] - p[i]) # keep holding or buy
  cool[i] = hold[i-1] + p[i]                 # sell

Answer: max(rest[n-1], cool[n-1])
```

```python
def max_profit_cooldown(prices):
    if not prices:
        return 0
    n = len(prices)
    rest = [0] * n
    hold = [0] * n
    cool = [0] * n
    hold[0] = -prices[0]

    for i in range(1, n):
        rest[i] = max(rest[i-1], cool[i-1])
        hold[i] = max(hold[i-1], rest[i-1] - prices[i])
        cool[i] = hold[i-1] + prices[i]

    return max(rest[n-1], cool[n-1])
```

### Example: Best Time to Buy and Sell Stock with K Transactions

```python
def max_profit_k(prices, k):
    n = len(prices)
    if k >= n // 2:  # unlimited transactions
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))

    # dp[t][i] = max profit using at most t transactions on days 0..i
    dp = [[0] * n for _ in range(k + 1)]
    for t in range(1, k + 1):
        best_buy = -prices[0]  # best "buy" position so far
        for i in range(1, n):
            dp[t][i] = max(dp[t][i-1],              # don't sell today
                           best_buy + prices[i])      # sell today
            best_buy = max(best_buy, dp[t-1][i] - prices[i])  # buy today
    return dp[k][n-1]
```

### Stock Problem Family

| Variant | States | Extra |
|---------|--------|-------|
| One transaction | buy price tracking | O(n) greedy |
| Unlimited transactions | hold/not-hold | O(n) |
| K transactions | k x hold/not-hold | O(nk) |
| With cooldown | rest/hold/cool | 3 states |
| With transaction fee | hold/not-hold, subtract fee on sell | 2 states |

---

## 10. Tree DP

### Pattern

DP on a rooted tree where each node's value depends on its children.

```
State:  dp[node] = answer for the subtree rooted at node
Transition: dp[node] = combine(dp[child1], dp[child2], ...)
Direction: bottom-up (leaves -> root), naturally done via post-order DFS
```

### Example: Maximum Independent Set

**Problem**: Select nodes with maximum total weight such that no two adjacent nodes are selected.

```
         1 (w=10)
        / \
   (w=20)2  3(w=30)
      /
  (w=40)4

dp[node][0] = max weight NOT selecting node
dp[node][1] = max weight selecting node

Transitions:
  dp[node][0] = sum(max(dp[child][0], dp[child][1]) for child)
                # if we don't select node, children can be either
  dp[node][1] = weight[node] + sum(dp[child][0] for child)
                # if we select node, children must NOT be selected
```

```python
def max_independent_set(adj, weight, root=0):
    n = len(adj)
    dp = [[0, 0] for _ in range(n)]  # [not_selected, selected]

    def dfs(node, par):
        dp[node][1] = weight[node]
        for child in adj[node]:
            if child == par:
                continue
            dfs(child, node)
            dp[node][0] += max(dp[child][0], dp[child][1])
            dp[node][1] += dp[child][0]

    dfs(root, -1)
    return max(dp[root][0], dp[root][1])
```

### Example: Tree Diameter

**Problem**: Find the longest path between any two nodes.

```python
def tree_diameter(adj, root=0):
    n = len(adj)
    max_depth = [0] * n  # longest path going down from node
    diameter = [0]

    def dfs(node, par):
        first = second = 0  # two longest paths through children
        for child in adj[node]:
            if child == par:
                continue
            dfs(child, node)
            d = max_depth[child] + 1
            if d > first:
                second = first
                first = d
            elif d > second:
                second = d
        max_depth[node] = first
        diameter[0] = max(diameter[0], first + second)

    dfs(root, -1)
    return diameter[0]
```

### Example: Counting Paths Through Each Node (Rerooting DP)

When you need dp for **every node as root**, not just one root. Reroot in O(N) instead of running DFS N times.

```
Phase 1: Root at node 0, compute dp_down[node] (standard tree DP)
Phase 2: For each node, compute dp_up[node] (contribution from parent's side)
         dp_up[child] = combine(dp_up[node], dp_down[siblings])
Phase 3: answer[node] = combine(dp_down[node], dp_up[node])
```

This is called **rerooting technique** and avoids O(N^2) recomputation.

---

## 11. Bitmask DP

### Pattern

When you have a **small set** (N <= 20) and need to track which elements are used. Represent the set as a bitmask.

```
State:  dp[mask] = answer when the elements in `mask` have been used/visited
        mask is an integer where bit i = 1 means element i is included

Transition:
  dp[mask | (1 << j)] = f(dp[mask], j)  for each unused j
```

### Example: Traveling Salesman Problem (TSP)

**Problem**: Visit all N cities exactly once and return to start. Minimize total distance.

```
State:  dp[mask][i] = min cost to visit all cities in `mask`,
                      ending at city i

Transition:
  dp[mask | (1<<j)][j] = min(dp[mask][i] + dist[i][j])
                          for each i in mask, j not in mask

Base: dp[1][0] = 0 (start at city 0, only city 0 visited)
Answer: min(dp[(1<<n)-1][i] + dist[i][0]) for all i
```

```python
def tsp(dist):
    n = len(dist)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0

    for mask in range(1 << n):
        for i in range(n):
            if dp[mask][i] == INF:
                continue
            if not (mask & (1 << i)):
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue  # already visited
                new_mask = mask | (1 << j)
                dp[new_mask][j] = min(dp[new_mask][j],
                                      dp[mask][i] + dist[i][j])

    full = (1 << n) - 1
    return min(dp[full][i] + dist[i][0] for i in range(n))
```

### Example: Assignment Problem

**Problem**: N workers, N tasks. Assign each worker exactly one task to minimize total cost.

```python
def min_assignment(cost):
    n = len(cost)
    INF = float('inf')
    dp = [INF] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        worker = bin(mask).count('1')  # which worker we're assigning next
        if worker >= n:
            continue
        for task in range(n):
            if mask & (1 << task):
                continue
            dp[mask | (1 << task)] = min(
                dp[mask | (1 << task)],
                dp[mask] + cost[worker][task]
            )

    return dp[(1 << n) - 1]
```

### Bitmask Tricks

```python
# Check if bit i is set
mask & (1 << i)

# Set bit i
mask | (1 << i)

# Clear bit i
mask & ~(1 << i)

# Iterate over all subsets of mask
sub = mask
while sub > 0:
    # process sub
    sub = (sub - 1) & mask

# Count set bits
bin(mask).count('1')  # or mask.bit_count() in Python 3.10+
```

### Complexity

Time: O(2^N * N) or O(2^N * N^2), Space: O(2^N * N)

Only feasible for N <= ~20.

---

## 12. Digit DP

### Pattern

Count numbers in range [L, R] with some digit property. Use the trick: `count(R) - count(L-1)`.

```
State:  dp[pos][tight][...extra state...]

pos:    current digit position (left to right)
tight:  are we still constrained by the upper bound?
extra:  problem-specific (digit sum, last digit, etc.)
```

### Example: Count Numbers with Digit Sum = S

**Problem**: How many numbers from 1 to N have digit sum equal to S?

```python
from functools import lru_cache

def count_digit_sum(N, S):
    digits = [int(d) for d in str(N)]

    @lru_cache(maxsize=None)
    def solve(pos, remaining, tight, started):
        """
        pos:       current digit index
        remaining: remaining digit sum needed
        tight:     still bounded by N's digits?
        started:   have we placed a non-zero digit? (handles leading zeros)
        """
        if remaining < 0:
            return 0
        if pos == len(digits):
            return 1 if remaining == 0 and started else 0

        limit = digits[pos] if tight else 9
        count = 0

        for d in range(0, limit + 1):
            count += solve(
                pos + 1,
                remaining - d,
                tight and (d == limit),
                started or (d > 0)
            )

        return count

    return solve(0, S, True, False)
```

### Digit DP Template

```python
def digit_dp(N):
    digits = [int(d) for d in str(N)]

    @lru_cache(maxsize=None)
    def solve(pos, tight, state):
        if pos == len(digits):
            return base_case(state)

        limit = digits[pos] if tight else 9
        result = 0

        for d in range(0, limit + 1):
            new_state = transition(state, d)
            result += solve(pos + 1,
                           tight and (d == limit),
                           new_state)

        return result

    return solve(0, True, initial_state)
```

### Common Digit DP Problems

| Problem | Extra state |
|---------|------------|
| Count numbers with digit sum S | remaining_sum |
| Count numbers with no repeated digits | used_digits (bitmask) |
| Count numbers divisible by K | current_remainder |
| Count numbers with digit d appearing exactly k times | count_of_d |

---

## 13. Probability / Expected Value DP

### Pattern

```
State:  dp[state] = probability of reaching state, OR
        dp[state] = expected number of steps from state to goal

For expected value (working backwards from goal):
  dp[goal] = 0
  dp[state] = 1 + sum(p_transition * dp[next_state])
```

### Example: Expected Dice Rolls to Reach N

**Problem**: Roll a 6-sided die repeatedly. What's the expected number of rolls to reach sum >= N?

```python
def expected_rolls(n):
    # dp[i] = expected rolls to reach sum >= n, starting from sum i
    dp = [0.0] * (n + 7)  # padding for sums beyond n

    for i in range(n - 1, -1, -1):
        # from sum i, roll 1-6 with equal probability
        dp[i] = 1  # one roll
        for face in range(1, 7):
            dp[i] += dp[min(i + face, n)] / 6.0

    return dp[0]
```

### Example: Sushi (AtCoder DP Contest)

**Problem**: N plates with sushi. Each step, pick random plate. If it has sushi, eat one piece. Expected steps to eat all sushi?

This is a classic expected value DP where states are grouped by count of plates with 1, 2, 3 pieces.

---

## 14. DP on DAGs

### Pattern

Any DP where dependencies form a Directed Acyclic Graph. Process nodes in **topological order**.

```
For each node u in topological order:
    for each edge u -> v:
        dp[v] = combine(dp[v], dp[u] + edge_weight)
```

### Example: Longest Path in DAG

```python
from collections import deque

def longest_path_dag(adj, n):
    # compute in-degree
    in_deg = [0] * n
    for u in range(n):
        for v, w in adj[u]:
            in_deg[v] += 1

    # topological sort (Kahn's)
    queue = deque()
    dp = [0] * n
    for i in range(n):
        if in_deg[i] == 0:
            queue.append(i)

    while queue:
        u = queue.popleft()
        for v, w in adj[u]:
            dp[v] = max(dp[v], dp[u] + w)
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)

    return max(dp)
```

### Example: Number of Paths in DAG

```python
def count_paths_dag(adj, n, src, dst):
    # topological sort then accumulate
    # dp[v] = number of paths from src to v
    in_deg = [0] * n
    for u in range(n):
        for v in adj[u]:
            in_deg[v] += 1

    queue = deque()
    dp = [0] * n
    dp[src] = 1
    for i in range(n):
        if in_deg[i] == 0:
            queue.append(i)

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            dp[v] += dp[u]
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)

    return dp[dst]
```

---

## 15. DP Optimizations

When the basic DP is too slow, apply these optimizations.

### 15.1 Convex Hull Trick

**When**: Transition has the form `dp[i] = min(dp[j] + b[j] * a[i])` where slopes `b[j]` are monotonic.

Reduces O(N^2) to O(N).

```
The transitions are linear functions: y = b[j]*x + dp[j]
For each new x = a[i], query the minimum y over all lines.
Maintain a convex hull of lines; query in O(1) or O(log N).
```

### 15.2 Divide and Conquer Optimization

**When**: `dp[i][j] = min(dp[i-1][k] + cost(k+1, j))` and the optimal `k` for `j` is monotonically non-decreasing.

Reduces O(KN^2) to O(KN log N).

```
If opt[j] <= opt[j+1], we can use divide and conquer:
  solve(l, r, opt_l, opt_r):
    mid = (l + r) / 2
    find opt[mid] in [opt_l, opt_r]
    solve(l, mid-1, opt_l, opt[mid])
    solve(mid+1, r, opt[mid], opt_r)
```

### 15.3 Knuth's Optimization

**When**: `dp[i][j] = min(dp[i][k] + dp[k+1][j] + cost(i,j))` for interval DP, and `opt[i][j-1] <= opt[i][j] <= opt[i+1][j]`.

Reduces interval DP from O(N^3) to O(N^2).

### 15.4 SOS DP (Sum over Subsets)

**When**: For each bitmask, compute the sum over all its submasks.

```python
# O(3^n) brute force -> O(n * 2^n) with SOS
for bit in range(n):
    for mask in range(1 << n):
        if mask & (1 << bit):
            dp[mask] += dp[mask ^ (1 << bit)]
```

### 15.5 Matrix Exponentiation

**When**: Linear recurrence with constant coefficients and very large N.

`dp[n] = a1*dp[n-1] + a2*dp[n-2] + ... + ak*dp[n-k]`

Build transition matrix and raise to power N in O(K^3 log N).

```python
import numpy as np

def fib_matrix(n):
    """Fibonacci in O(log n) using matrix exponentiation."""
    if n <= 1:
        return n

    def mat_mul(A, B, mod=10**9+7):
        return [[(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % mod,
                 (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % mod],
                [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % mod,
                 (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % mod]]

    def mat_pow(M, p):
        result = [[1,0],[0,1]]  # identity
        while p:
            if p & 1:
                result = mat_mul(result, M)
            M = mat_mul(M, M)
            p >>= 1
        return result

    # [F(n+1), F(n)] = [[1,1],[1,0]]^n * [F(1), F(0)]
    M = [[1,1],[1,0]]
    result = mat_pow(M, n)
    return result[0][1]
```

### Optimization Summary

| Optimization | Original | Optimized | Condition |
|-------------|----------|-----------|-----------|
| Convex Hull Trick | O(N^2) | O(N) | Linear transitions, monotonic slopes |
| D&C Optimization | O(KN^2) | O(KN log N) | Monotone optimal split point |
| Knuth's | O(N^3) | O(N^2) | Quadrangle inequality on cost |
| SOS DP | O(3^N) | O(N * 2^N) | Sum over all submasks |
| Matrix Exponent. | O(N) | O(K^3 log N) | Linear recurrence, huge N |

---

## 16. Pattern Recognition Cheat Sheet

### By Problem Type

| You see... | Think... | Pattern |
|------------|----------|---------|
| "Count ways" with choices at each step | Linear DP or Knapsack | Sec 3, 5 |
| Grid traversal, paths | Grid DP | Sec 4 |
| "Take or skip" with weight/capacity | Knapsack | Sec 5 |
| "Longest increasing/decreasing" | LIS | Sec 6 |
| Two strings, matching | LCS / Edit Distance | Sec 7 |
| Merge/split intervals optimally | Interval DP | Sec 8 |
| Buy/sell, hold/not-hold states | State Machine DP | Sec 9 |
| Tree + subtree values | Tree DP | Sec 10 |
| Small N (<=20), subset tracking | Bitmask DP | Sec 11 |
| "How many numbers in [L,R] with property" | Digit DP | Sec 12 |
| Random events, "expected number of" | Probability DP | Sec 13 |
| Graph with dependencies | DP on DAG | Sec 14 |
| Recurrence with huge N (10^18) | Matrix Exponentiation | Sec 15 |

### By Constraint Size

| N range | Likely approach |
|---------|----------------|
| N <= 20 | Bitmask DP O(2^N * N) |
| N <= 500 | Interval DP O(N^3) |
| N <= 5000 | O(N^2) DP (LCS, LIS naive) |
| N <= 10^5 | O(N log N) DP (LIS optimized, HLD) |
| N <= 10^6 | O(N) DP (linear, Kadane's) |
| N <= 10^18 | Matrix exponentiation O(K^3 log N) |

### Quick Complexity Reference

| Pattern | Time | Space |
|---------|------|-------|
| Linear DP | O(N) or O(NS) | O(N) or O(1) |
| Grid DP | O(MN) | O(MN) or O(N) |
| 0/1 Knapsack | O(NW) | O(W) |
| LIS | O(N log N) | O(N) |
| LCS | O(MN) | O(MN) or O(N) |
| Interval DP | O(N^3) or O(N^2) | O(N^2) |
| Tree DP | O(N) | O(N) |
| Bitmask DP | O(2^N * N) | O(2^N) |
| Digit DP | O(D * S * 10) | O(D * S) |
| Matrix Exponent. | O(K^3 log N) | O(K^2) |
