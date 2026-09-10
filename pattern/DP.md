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

Calls: 15 (exponential)        6 distinct subproblems, cached
```

The memo caches 6 distinct subproblems `fib(0)..fib(5)` and computes each once, instead of re-computing them exponentially — naive `fib(5)` makes 15 total calls, and that blows up to `~2^n` as `n` grows.

---

## Quick Navigation: "I need to..."

| I need to... | Family | Section |
|--------------|--------|---------|
| Choose take-or-skip along a **line** (rob houses, climb stairs) | Linear | [3](#3-linear-dp) |
| Walk a **grid** moving only right/down; count paths or min cost | Grid | [4](#4-grid-dp) |
| Fill a **capacity/target** with items (subset sum, coin change) | Knapsack | [5](#5-knapsack-family) |
| Find **longest increasing** subsequence | LIS | [6](#6-longest-increasing-subsequence) |
| Match / align **two strings** | LCS | [7](#7-longest-common-subsequence) |
| Combine a **range `[i,j]`** where the split order matters | Interval | [8](#8-interval-dp) |
| Track a **mode you're in** (holding/selling stock) that transitions | State Machine | [9](#9-state-machine-dp) |
| Compute a subtree value from its **children** | Tree | [10](#10-tree-dp) |
| Track **which of ≤20 items** are used (visit-all, assign) | Bitmask | [11](#11-bitmask-dp) |
| Count numbers in **`[L,R]`** with a **digit** property | Digit | [12](#12-digit-dp) |
| Compute a **probability / expected count** over random steps | Probability | [13](#13-probability--expected-value-dp) |
| DP where dependencies form a **directed acyclic graph** | DP on DAG | [14](#14-dp-on-dags) |
| A correct DP that is **too slow** and needs speeding up | Optimizations | [15](#15-dp-optimizations) |

---

## How to Identify a DP Problem

Before picking a family, confirm it's DP at all. Two questions:

```
(1) Can I phrase the answer as a sequence of CHOICES, where each choice
    leads to a smaller version of the SAME problem?
        (take/skip an item, go right/down, split at k, pick next city...)

(2) Do those smaller problems OVERLAP — i.e. the same subproblem is
    reached by many different choice-paths?

Both YES  → Dynamic Programming.
Only (1)  → plain recursion / divide & conquer (subproblems don't repeat).
Neither   → greedy, simulation, or a different paradigm.
```

The third tell is the **ask**: DP answers *"count the ways"*, *"minimum/maximum cost"*, or *"is it possible?"* — never *"give me any one valid answer"* (that's usually greedy/backtracking).

`★ Insight ─────────────────────────────────────`
- **Optimal substructure + overlapping subproblems** are the two license conditions. If subproblems don't overlap, memoization buys nothing and it's just recursion. If there's no optimal substructure (a locally-best choice can't be trusted), DP's whole "build from smaller answers" premise collapses.
- The *state* is whatever you must remember to make the next choice correctly — and nothing more. Too little state → subproblems aren't actually independent (wrong answer). Too much state → the table explodes (TLE/MLE). Finding the minimal sufficient state IS the problem.
`─────────────────────────────────────────────────`

### Which family? — a symptom → family router

```
What does a subproblem look like?

 a 1-D position along a line/array ............... Linear DP        (§3)
   └ with a running "mode" that flips ............ State Machine    (§9)
 a cell (i,j) in a grid, move right/down ......... Grid DP          (§4)
 "used capacity so far" toward a target/budget ... Knapsack         (§5)
 a prefix of ONE sequence, order matters ......... LIS              (§6)
 a pair of prefixes of TWO sequences ............. LCS / Edit Dist  (§7)
 a contiguous range [i,j], you pick a split k .... Interval DP      (§8)
 a node whose value = f(its children) ............ Tree DP          (§10)
 a SUBSET of ≤ ~20 elements (which are used) ..... Bitmask DP       (§11)
 a position while building a number digit-by-digit Digit DP         (§12)
 a state + a probability/expected value .......... Probability DP   (§13)
 a node in a dependency graph (topo order) ....... DP on DAG        (§14)
```

Many problems are a family **in disguise** — the input *is* the DP structure once you rename it:

| Problem smells like... | Really is... |
|------------------------|--------------|
| "reach sum ≥ N", "make change", "partition into equal halves" | Knapsack over a target (§5) |
| grid of cells with only right/down moves | Grid DP (§4) |
| "two strings", "edit / align / common" | LCS family (§7) |
| "≤ 20 cities/workers, visit-all / assign-all" | Bitmask DP (§11) |
| "longest path where each step must increase" | LIS (§6) or DP-on-DAG (§14) |
| a rooted tree, answer per subtree | Tree DP (§10) |

---

## Master LeetCode Comparison Table

One canonical LeetCode problem per family — the walkthrough for each lives in its section below.

| LC # | Problem | Family | Difficulty | State `dp[...]` = | Transition (the one line) |
|------|---------|--------|-----------|-------------------|---------------------------|
| **198** | House Robber | Linear | Medium | max loot from houses `0..i` | `max(dp[i-1], dp[i-2]+a[i])` |
| **64** | Minimum Path Sum | Grid | Medium | min cost to reach cell `(i,j)` | `grid[i][j] + min(up, left)` |
| **416** | Partition Equal Subset Sum | Knapsack | Medium | can we hit sum `s`? | `dp[s] or dp[s-a[i]]` (reverse s) |
| **300** | Longest Increasing Subsequence | LIS | Medium | smallest tail of an LIS of length `k+1` | binary-search replace in `tails` |
| **1143** | Longest Common Subsequence | LCS | Medium | LCS of prefixes `s1[:i], s2[:j]` | match→`diag+1`, else `max(up,left)` |
| **312** | Burst Balloons | Interval | Hard | max coins bursting all inside `(i,j)` | try each `k` as **last** to burst |
| **309** | Buy/Sell w/ Cooldown | State Machine | Medium | best profit in `rest/hold/cool` at day `i` | 3 coupled state updates |
| **337** | House Robber III | Tree | Medium | `(rob_node, skip_node)` per subtree | `rob=val+Σskip_child; skip=Σmax(child)` |
| **847** | Shortest Path Visiting All Nodes | Bitmask | Hard | BFS layer of `(mask, node)` | flip a bit when stepping to a neighbor |
| **233** | Number of Digit One | Digit | Hard | count of 1s while building `≤ N` | per position, `tight` + count-so-far |
| **688** | Knight Probability in Chessboard | Probability | Medium | prob still on board after `k` moves | `Σ dp[k-1][prev]/8` |
| **329** | Longest Increasing Path in Matrix | DP on DAG | Hard | longest strictly-increasing path from `(i,j)` | `1 + max(neighbors greater)` (memo) |
| **1137** | N-th Tribonacci | Optimizations | Easy | linear recurrence, huge `n` | rolling window / matrix power (§15.5) |

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
17. [Practice Order](#17-practice-order)

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
| 0/1 knapsack inner loop iterated **forward** | Iterate the capacity/sum **reverse** so each item is used once (§5, LC 416) |
| Tree DP returning one number | Return a **pair** `(use_node, skip_node)` so the parent can choose (§10, LC 337) |
| Rolling variables committed in wrong order | Compute all next-states from *old* values, then assign together — `a, b = b, max(...)` not two lines (§3, LC 198; §9 states) |
| Reaching for matrix-expo on the Easy version | Only when `n` is astronomically large; rolling window otherwise (§15.5, LC 1137) |

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

### Example: Coin Counting — Ordered vs Unordered (loop order matters!)

**Problem**: Given coins `[1, 3, 5]`, how many ways to make sum `n`?

There are **two** different questions hiding here, and the *only* difference in
code is which loop is on the outside:

```
dp[s] = number of ways to form sum s,   dp[0] = 1
```

**A) Count ordered sequences** (1+3 and 3+1 are different) — outer loop `s`:

```python
def count_ordered(coins, n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for s in range(1, n + 1):        # for each target sum...
        for coin in coins:           # ...try every coin as the LAST one added
            if s >= coin:
                dp[s] += dp[s - coin]
    return dp[n]
```

**B) Count unordered combinations** (1+3 same as 3+1) — outer loop `coin`:

```python
def count_combinations(coins, n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for coin in coins:               # fix a coin order once...
        for s in range(coin, n + 1): # ...only extend sums using coins seen so far
            dp[s] += dp[s - coin]
    return dp[n]
```

`★ Insight ─────────────────────────────────────`
- **Outer loop = sum** → each coin can be the "last" one at every step → counts **permutations** (ordered; CSES "Coin Combinations I"). **Outer loop = coin** → each coin is introduced once, globally → counts **combinations** (unordered; CSES "Coin Combinations II" / classic "Coin Change 2").
- Same three lines of code; the outer loop alone decides the meaning. This loop-order sensitivity is unique to *counting* — for *minimum coins* either order gives the same answer, because `min` doesn't care how many orderings reach a value, only the cheapest.
`─────────────────────────────────────────────────`

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
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    a, b = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        a, b = b, max(b, a + nums[i])
    return b
```

#### Walkthrough — LC 198 House Robber

**This template solves: LC 198 (House Robber), LC 213 (House Robber II — circular), LC 740 (Delete and Earn — bucket by value then rob).**

> You are a robber planning to rob houses along a street. Each house `nums[i]` holds some money. Adjacent houses have connected alarms — robbing two adjacent houses on the same night triggers the police. Return the maximum money you can rob without alerting police.

The whole family reduces to one binary choice **at each position**: take `nums[i]` (then you *cannot* have taken `i-1`), or skip it (keep whatever the best was through `i-1`). That's the take/skip archetype — the ancestor of every linear DP.

```
State   dp[i] = best loot considering houses 0..i
Choice  rob i  → nums[i] + dp[i-2]   (i-1 is off-limits)
        skip i → dp[i-1]
        dp[i] = max(skip, rob)
```

Only `dp[i-1]` and `dp[i-2]` are ever read, so we collapse the whole table into two rolling scalars: `b = dp[i-1]` (best so far) and `a = dp[i-2]` (best two back). Trace on `[2, 7, 9, 3, 1]`:

```
init          a=2   b=max(2,7)=7            (dp[0]=2, dp[1]=7)
i=2 (9)  rob=a+9=11, skip=b=7  → a=7,  b=11
i=3 (3)  rob=a+3=10, skip=b=11 → a=11, b=11   (skipping wins)
i=4 (1)  rob=a+1=12, skip=b=11 → a=11, b=12

answer b = 12   (rob houses 0, 2, 4:  2 + 9 + 1 = 12)
```

`★ Insight ─────────────────────────────────────`
- The rolling `a, b = b, max(b, a + nums[i])` line does the table swap *in place*: after the tuple-assignment, the old `b` (which was `dp[i-1]`) becomes the new `a` (`dp[i-2]` for the next step). Writing it as two separate lines is the classic bug — updating `b` first would clobber the value `a` still needs.
- **House Robber II (LC 213)** is the same code run twice: a circular street means house `0` and house `n-1` are adjacent, so the max is `max(rob(nums[:-1]), rob(nums[1:]))` — you forbid one endpoint or the other. Recognizing "this is just Robber with one house excluded" is the whole trick.
`─────────────────────────────────────────────────`

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

#### Walkthrough — LC 64 Minimum Path Sum

**This template solves: LC 64 (Minimum Path Sum), LC 62 (Unique Paths — count instead of min), LC 63 (Unique Paths II — obstacles zero out a cell), LC 931 (Minimum Falling Path Sum — three parents instead of two).**

> Given an `m × n` grid of non-negative numbers, find a path from the **top-left** to the **bottom-right** that minimizes the sum of numbers along the path. You can only move **right** or **down**.

The move restriction is the whole reason this is DP: since you only ever arrive at `(i,j)` from **above** `(i-1,j)` or from the **left** `(i,j-1)`, the best way to reach `(i,j)` is `grid[i][j]` plus the cheaper of those two already-solved cells. No cell depends on one below or to its right, so filling top-to-bottom, left-to-right guarantees both parents are ready.

```
grid            dp = min cost to reach each cell
1  3  1         1 →4 →5      row 0: only-left prefix sums
1  5  1         ↓            col 0: only-up prefix sums
4  2  1         2  7  6
                6  8  7      dp[2][2] = 1 + min(dp[1][2]=6, dp[2][1]=8) = 7

dp[1][1] = grid 5 + min(up 4, left 2) = 5 + 2 = 7
answer  dp[2][2] = 7   (path 1→3→1→1→1)
```

The first row and first column are special: a top-row cell has no cell above it, a left-column cell has none to its left — so each is just the running sum along the only path that reaches it. That's why the code seeds them in two separate loops before the main double loop.

`★ Insight ─────────────────────────────────────`
- Swapping `min` for `+` (sum) and the base cases for `1` turns this into **LC 62 Unique Paths** (count the paths) — the *shape* of the recurrence, "combine the cell above and the cell to the left," is identical across the whole grid family; only the combiner changes (`min`, `max`, `+`).
- The space optimization works because row `i` reads only row `i-1`. Rolling to a 1-D array, `dp[j]` still holds row `i-1`'s value at the moment you read it (as "up") and `dp[j-1]` already holds row `i`'s value (as "left") — the single line `dp[j] = grid[i][j] + min(dp[j], dp[j-1])` is both parents at once. Getting the read order wrong (updating `dp[j-1]` after `dp[j]`) silently corrupts the "left" term.
`─────────────────────────────────────────────────`

---

## 5. Knapsack Family

The most important DP family. Three major variants.

**Intuition**: you face a sequence of items and for each one make a yes/no (or how-many) choice under a shared budget (capacity, target sum). Brute force tries every subset — `2^N` combinations — which explodes past ~30 items. DP collapses this: instead of tracking *which* items were chosen, track only the *capacity used so far*, since two different subsets reaching the same capacity are interchangeable going forward. That merges the exponential tree into an `N × W` table.

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

#### Walkthrough — LC 416 Partition Equal Subset Sum

**This template solves: LC 416 (Partition Equal Subset Sum), LC 494 (Target Sum — assign +/- signs), LC 1049 (Last Stone Weight II — minimize |two-group difference|).**

> **Not LC 698.** "Partition to K Equal Sum Subsets" only collapses to this knapsack when `k = 2`
> (one target subset, everything else is the complement). For general `k` you must track *which*
> items each of the `k` buckets took, which is a mask state, not a capacity —
> see [Bitmask DP — Subset Partition](/pattern/bitmask-dp-subset-partition).

> Given an array of positive integers, determine whether it can be split into **two subsets with equal sum**.

The disguise: two equal halves means each half sums to `total/2`. So the question collapses to **"is there a subset summing to exactly `total/2`?"** — a boolean 0/1 knapsack where each number's *weight* and *value* are the number itself, capacity is `total/2`, and we only care whether we can *hit* the capacity exactly. (If `total` is odd, answer is instantly `False` — you can't halve an odd integer.)

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)   # dp[s] = can we form sum s?
    dp[0] = True                  # empty subset makes 0
    for x in nums:
        for s in range(target, x - 1, -1):   # REVERSE — each item once
            dp[s] = dp[s] or dp[s - x]
    return dp[target]
```

Trace on `[1, 5, 11, 5]`, `total = 22`, `target = 11`. `dp` starts with only sum `0` reachable; each item unlocks new reachable sums:

```
reachable sums after processing each item
start        {0}
after 1      {0, 1}
after 5      {0, 1, 5, 6}
after 11     {0, 1, 5, 6, 11}      ← 11 reachable! ({11})
after 5      {0, 1, 5, 6, 10, 11}

dp[11] = True   → {11} and {1,5,5} both sum to 11 → partitionable
```

`★ Insight ─────────────────────────────────────`
- **The reverse inner loop `range(target, x-1, -1)` is what makes it 0/1.** Iterating `s` downward means when we read `dp[s-x]` it still reflects the table *before* `x` was added — so `x` contributes to each sum at most once. Iterating *forward* would let `dp[s-x]` already include `x`, effectively reusing the item unlimited times — that's the **unbounded** knapsack (correct for Coin Change, wrong here). One loop direction is the entire difference between the two most common knapsack disguises.
- Booleans instead of a value-maximizing `max` is the tell for **feasibility** questions ("can we hit target?") versus **optimization** ("best value ≤ capacity"). LC 494 Target Sum wears an even better disguise: choosing `+`/`−` signs to reach `T` is the same as choosing a positive subset `P` with `P = (total + T)/2`, then it's *this exact code* counting subsets instead of testing one.
`─────────────────────────────────────────────────`

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

#### Walkthrough — LC 300 Longest Increasing Subsequence

**This template solves: LC 300 (Longest Increasing Subsequence), LC 673 (Number of LIS — carry a count per length), LC 354 (Russian Doll Envelopes — sort by width then LIS on height), LC 646 (Maximum Length of Pair Chain).**

> Given an integer array `nums`, return the length of the longest **strictly increasing subsequence** (elements need not be contiguous, but must keep their original order).

Two solutions, two mental models:

- **O(N²)** — `dp[i]` = length of the best increasing subsequence *ending exactly at* `i`. To extend, look back at every earlier `j` with a smaller value and take the longest chain you can append to. This is the honest, direct DP.
- **O(N log N)** — the patience-sorting trick. Keep `tails`, where `tails[k]` is the *smallest possible tail* of any increasing subsequence of length `k+1`. Each new `x` either extends the longest run (if it's bigger than every tail) or overwrites the first tail `≥ x`, keeping that length reachable with a smaller, more future-proof ending.

```python
from bisect import bisect_left

def lis_nlogn(arr):
    tails = []
    for x in arr:
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)     # x is bigger than all tails → new longest run
        else:
            tails[pos] = x      # x is a smaller ending for length pos+1
    return len(tails)
```

Trace on `[10, 9, 2, 5, 3, 7, 101, 18]` (same array as §Trace above): `tails` ends `[2, 3, 7, 18]`, length **4** — the LIS is `[2, 3, 7, 101]` or `[2, 3, 7, 18]`.

`★ Insight ─────────────────────────────────────`
- **`tails` is not the LIS itself** — its *length* is the answer, but its contents can be a mix of elements that never coexist in one subsequence (here `18` overwrote `101`, yet both give length-4 runs). Reading `tails` as the actual subsequence is the classic misconception. To recover the real LIS you track, for each `x`, the length it landed at, then stitch backward.
- **Why "smallest tail" is the right greedy invariant:** a shorter tail can be extended by strictly more future elements, so keeping tails minimal never forecloses a longer subsequence. `bisect_left` (strictly increasing) vs `bisect_right` (non-decreasing) is the single knob that toggles whether equal elements may chain — the same one-character swap that appears across the whole LIS variant family.
`─────────────────────────────────────────────────`

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

### Space Optimization for LCS

The full 2D table uses O(MN) space. Since each row `dp[i]` only depends on `dp[i-1]`, we can reduce to **O(min(M,N))** using two rows (or a single row with a saved variable):

```python
def lcs_optimized(s1, s2):
    # ensure s2 is shorter for minimal space
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)

    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev = curr

    return prev[n]
```

**Single-row trick** (saves one allocation, but trickier):

```python
def lcs_single_row(s1, s2):
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    m, n = len(s1), len(s2)
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev_diag = 0  # saves dp[i-1][j-1] before overwrite
        for j in range(1, n + 1):
            temp = dp[j]  # this is dp[i-1][j], save before overwrite
            if s1[i-1] == s2[j-1]:
                dp[j] = prev_diag + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev_diag = temp

    return dp[n]
```

**Caveat**: With O(N) space you can compute the LCS **length**, but **not reconstruct** the actual LCS string. Reconstruction requires the full 2D table (or Hirschberg's algorithm for O(N) space reconstruction in O(MN) time).

### LCS Family

| Problem | Relation to LCS |
|---------|----------------|
| Edit Distance | Similar DP table, different transition |
| Shortest Common Supersequence | `len(s1) + len(s2) - LCS` |
| Longest Palindromic Subsequence | LCS of string and its reverse |
| Diff (version control) | LCS = unchanged lines |

#### Walkthrough — LC 1143 Longest Common Subsequence

**This template solves: LC 1143 (Longest Common Subsequence), LC 72 (Edit Distance — same grid, insert/delete/replace transitions), LC 583 (Delete Operation for Two Strings — `m+n-2·LCS`), LC 516 (Longest Palindromic Subsequence — LCS of `s` with `reverse(s)`).**

> Given two strings `text1` and `text2`, return the length of their longest **common subsequence** (characters appearing in both, left-to-right, not necessarily contiguous). Return `0` if there is none.

Two-string alignment is the archetype for the whole 2-D grid-of-prefixes family. `dp[i][j]` answers one question: *"what's the LCS of the first `i` characters of `text1` and the first `j` of `text2`?"* At each cell you compare the two *current* characters:

- **They match** → that character joins the LCS; add `1` to the answer for the prefixes *without* it: `dp[i-1][j-1] + 1` (the diagonal).
- **They differ** → one of them can't be in the LCS ending here; drop a character from one string and take the better result: `max(dp[i-1][j], dp[i][j-1])` (up vs left).

Trace on `text1 = "abcde"`, `text2 = "ace"` — LC 1143's own example. Rows = prefixes of `abcde`, columns = prefixes of `ace`:

```
        ""  a   c   e
   ""    0  0   0   0
   a     0  1   1   1     'a'='a' → diag(0)+1 = 1
   b     0  1   1   1     no match → carry max
   c     0  1   2   2     'c'='c' → diag(1)+1 = 2
   d     0  1   2   2
   e     0  1   2   3     'e'='e' → diag(2)+1 = 3

answer dp[5][3] = 3   (LCS = "ace")
```

`★ Insight ─────────────────────────────────────`
- **The diagonal is "both strings advance"; up/left is "one string advances."** Every string-pair DP (edit distance, shortest common supersequence, regex/wildcard matching) is this same three-neighbor grid — only the transition formula in the match/no-match branches changes. Recognizing the `dp[i][j]` = *pair-of-prefixes* state is what lets you port the template between them.
- **Length is O(N) space, but reconstruction is not.** Because each row needs only the row above, you can shrink to two rows (or one row + a saved diagonal, as in `lcs_single_row`). But the *actual* subsequence string requires the full 2-D table to backtrack through, or Hirschberg's divide-and-conquer to get it in O(N) space at the cost of O(MN) time. Deciding "do I need the value or the witness?" up front picks your space budget.
`─────────────────────────────────────────────────`

---

## 8. Interval DP

### Pattern

Problems where the answer for a range `[i, j]` depends on sub-ranges.

**Intuition**: the shape is "combine adjacent pieces, and the *order* of combining changes the cost" — matrix-chain products, bursting balloons, merging stones. Brute force tries every order of combining (`~N!` / Catalan-many parenthesizations), which explodes fast. The key realization: any final combination has a *last* split point `k` that cuts `[i, j]` into `[i, k]` and `[k+1, j]`; try all `k` and reuse the already-solved sub-ranges. That turns `N!` into an `O(N^3)` table.

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

#### Walkthrough — LC 312 Burst Balloons

**This template solves: LC 312 (Burst Balloons), LC 1000 (Minimum Cost to Merge Stones), LC 1039 (Minimum Score Triangulation), LC 375 (Guess Number Higher or Lower II).**

> You have `n` balloons, each with a number `nums[i]`. Bursting balloon `i` earns `nums[i-1] * nums[i] * nums[i+1]` coins (treat out-of-range neighbors as `1`). After bursting, its neighbors become adjacent. Burst all balloons in some order to **maximize** total coins.

The trap: if you define `dp[i][j]` = best coins from *first* balloon burst in `(i,j)`, the recurrence breaks — bursting the first balloon changes who's adjacent to whom, so the two sides aren't independent. **The fix that defines interval DP: think about the balloon burst *last*.**

If balloon `k` is the **last** to burst inside the open interval `(i, j)`, then by the time it pops, everything strictly between `i..k` and `k..j` is already gone, so `k`'s neighbors are exactly the boundaries `i` and `j` — fixed and known. That makes the two sub-intervals `(i,k)` and `(k,j)` fully independent:

```
dp[i][j] = max coins from bursting all balloons strictly between i and j
         = max over k in (i,j) of
             dp[i][k]  +  dp[k][j]  +  nums[i]*nums[k]*nums[j]
               ↑ left       ↑ right      ↑ k bursts last, neighbors are the
               already      already        untouched boundaries i and j
               solved       solved
```

Pad the array with sentinel `1`s at both ends so every real balloon has a defined neighbor. Fill by **increasing interval length** so both sub-intervals are ready before the combining interval. On `[3,1,5,8]` this yields **167** (one optimal order: burst 1, then 5, then 3, then 8).

`★ Insight ─────────────────────────────────────`
- **"First to act" vs "last to act" is the pivot of interval DP.** Choosing the *last* operation makes the boundaries of each subproblem stable — the reason `nums[i] * nums[k] * nums[j]` uses the interval endpoints and not `k`'s original neighbors. Whenever an operation *mutates adjacency* (merging, bursting, removing), reframe around the final one.
- **Loop by length, not by `i,j` directly.** `dp[i][j]` reads strictly-smaller intervals `dp[i][k]` and `dp[k][j]`, so every shorter interval must be computed first — iterating `length = 2..n` guarantees that ordering. This length-outer / left-inner / split-innermost triple loop is the O(N³) skeleton shared by the entire family.
`─────────────────────────────────────────────────`

### Space Optimization for Interval DP

Interval DP generally **cannot** be space-optimized below O(N^2). Unlike linear or grid DP where each row depends only on the previous row, interval DP entries `dp[i][j]` depend on arbitrary sub-intervals `dp[i][k]` and `dp[k+1][j]` — you need the full table.

**Exception**: Some interval-like problems (e.g., palindrome partitioning) can be reformulated as linear DP, reducing space to O(N). See below.

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

#### Walkthrough — LC 309 Best Time to Buy and Sell Stock with Cooldown

**This template solves: LC 309 (with Cooldown), LC 122 (unlimited transactions — drop the cool state), LC 714 (with Transaction Fee — subtract fee on sell), LC 123 / LC 188 (at most 2 / k transactions — add a transaction-count dimension, see `max_profit_k`).**

> Given daily `prices`, maximize profit with unlimited transactions, but with one rule: **after you sell, you must skip one day** before buying again (a one-day cooldown). You can hold at most one share at a time.

State-machine DP applies when *"what you're allowed to do next depends on a mode you're currently in."* Here there are exactly three modes each day, and the answer is the best profit achievable while ending the day in each:

```
      buy (−price)         sell (+price)
REST ───────────────► HOLD ───────────────► COOL
 ▲   do nothing / cooldown done          │  must wait
 └─────────────────────────────────────  one day
```

- `rest` — not holding, free to buy. Reached by staying rest, or by finishing a cooldown: `max(rest, cool_prev)`.
- `hold` — holding a share. Reached by keeping it, or buying today *from rest* (never from cool — that's the cooldown): `max(hold, rest_prev - price)`.
- `cool` — just sold today: `hold_prev + price`.

Trace on `[1, 2, 3, 0, 2]`:

```
day  price  rest  hold  cool
 0     1      0    -1     0
 1     2      0    -1     1     (sell the day-0 share: -1+2 = 1)
 2     3      1    -1     2
 3     0      2     1    -1     (buy from rest(1): 1-0 = 1 held)
 4     2      2     1     3     (sell: hold(1)+2 = 3)

answer max(rest=2, cool=3) = 3   (buy@1 sell@2, cooldown, buy@0 sell@2)
```

`★ Insight ─────────────────────────────────────`
- **The whole family is one skeleton with different edges.** Remove the `cool` state and let `rest` follow `sell` immediately → LC 122 (unlimited). Subtract a fee inside the sell edge → LC 714. Add a "transactions used" axis → LC 123/188. Drawing the state diagram first, *then* transcribing one update per node, is far more reliable than reverse-engineering the recurrence.
- **All three states must update from the previous day's values simultaneously.** The array version reads `rest[i-1]/hold[i-1]/cool[i-1]` so it's naturally safe; the O(1) version *must* stage `new_rest/new_hold/new_cool` before committing — assigning `rest` first would feed a same-day value into `hold`'s update and quietly corrupt the answer. This "compute-then-commit" is the recurring state-machine footgun.
`─────────────────────────────────────────────────`

### Space Optimization for State Machine DP

Since each state at step `i` only depends on step `i-1`, replace arrays with variables — O(N) space → O(1):

```python
def max_profit_cooldown_optimized(prices):
    if not prices:
        return 0
    rest, hold, cool = 0, -prices[0], 0

    for i in range(1, len(prices)):
        new_rest = max(rest, cool)
        new_hold = max(hold, rest - prices[i])
        new_cool = hold + prices[i]
        rest, hold, cool = new_rest, new_hold, new_cool

    return max(rest, cool)
```

**Key**: Update all states simultaneously (use `new_` variables or tuple unpacking) to avoid using partially-updated values from the current step.

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

> **Who owns what.** This section is canonical for generic tree DP — select/skip, matching,
> colouring, and LC 337. [Tree Patterns §9](/pattern/tree) restates the same patterns in tree
> vocabulary and connects them to the tree-only machinery (Euler flattening, rerooting, virtual
> trees). For "the answer for every node as root", go straight to
> [Edge Contribution & Rerooting](/pattern/edge-contribution).

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

#### Walkthrough — LC 337 House Robber III

**This template solves: LC 337 (House Robber III), LC 124 (Binary Tree Maximum Path Sum — same two-value-per-node idea), LC 968 (Binary Tree Cameras — 3 states per node), and general weighted Maximum Independent Set on trees.**

> Houses form a **binary tree**. The robber can't rob two **directly-linked** houses (a parent and its child). Given the root, return the maximum money without alerting the police.

This is House Robber (§3) with the line bent into a tree. The take/skip choice is unchanged — but "adjacent" now means parent↔child, so the DP flows **bottom-up**: a node's answer needs its children's answers first. Each node returns a **pair**, not a scalar:

```
dfs(node) → (rob_node, skip_node)
   rob_node  = node.val + skip_left + skip_right   # rob here → children must be skipped
   skip_node = max(left) + max(right)              # skip here → each child free to choose its best
```

```python
def rob(root):
    def dfs(node):
        if not node:
            return (0, 0)                    # (rob_this, skip_this)
        lr, ls = dfs(node.left)
        rr, rs = dfs(node.right)
        rob_this  = node.val + ls + rs        # rob node → skip both children
        skip_this = max(lr, ls) + max(rr, rs) # skip node → children pick their best
        return (rob_this, skip_this)
    return max(dfs(root))
```

Trace on `[3,2,3,null,3,null,1]` (root 3, left-subtree {2→right 3}, right-subtree {3→right 1}):

```
leaf 3 (under 2)   → (3, 0)
node 2             → rob=2+0=2, skip=max(3,0)=3  → (2, 3)
leaf 1 (under 3)   → (1, 0)
node 3 (right)     → rob=3+0=3, skip=max(1,0)=1  → (3, 1)
root 3             → rob=3 + skip_left(3) + skip_right(1) = 7
                     skip=max(2,3) + max(3,1)  = 3 + 3 = 6
answer max(7, 6) = 7
```

`★ Insight ─────────────────────────────────────`
- **Returning a pair `(rob, skip)` is the crux.** A single "best for this subtree" number loses the information the parent needs — the parent must know the child's value *conditioned on the child being skipped* to decide whether robbing itself is legal. The #1 tree-DP bug is collapsing the state to one number too early; the fix is almost always "return a tuple of the answer under each local choice."
- **Tree DP is post-order recursion** — you compute children, then combine at the parent. That's the tree analogue of "fill the table in dependency order." The same shape powers LC 124 (each node returns best *downward* path, updates a global best through-node path) and rerooting DPs (a second top-down pass reuses the bottom-up values). Once you see "answer of a node = f(answers of its children)," you're in this family.
`─────────────────────────────────────────────────`

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

> **Who owns what.** This section owns bitmask DP's *place among the DP families* — the state
> shapes, the three cost classes, and the LC 847 walkthrough. The mechanics live elsewhere:
> [Bitmask Techniques](/pattern/bitmask) for bit operations, subset enumeration, and SOS DP;
> [Bitmask DP — Subset Partition](/pattern/bitmask-dp-subset-partition) for the O(3ⁿ) partition
> family (LC 1986, 2305, 698, 943, 1494). Read this to know *when*, read those to know *how*.

### Pattern

When you have a **small set** (N <= 20) and need to track which elements are used. Represent the set as a bitmask.

**Intuition**: the problem asks for the best way to *order* or *assign* a small set — visit all cities, match all workers to tasks. Brute force enumerates every permutation (`N!`), hopeless past ~11 items. The insight: for what comes next, the only thing that matters is *which* elements are already used (a subset), not the order they were used in. Encode that subset as the bits of an integer `mask`, and two paths reaching the same `mask` share the same future — so cache by `mask`. `N!` permutations collapse into `2^N` subsets.

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

**Trace on 3 cities** (symmetric distance matrix, start/end at city 0):

```
       0   1   2
  0 [  0  10  15 ]
  1 [ 10   0  20 ]
  2 [ 15  20   0 ]

Masks written as bits [city2 city1 city0].

Base:   dp[001][0] = 0                     (only city 0 visited, at 0)

From dp[001][0]=0:
  → visit 1: dp[011][1] = 0 + dist[0][1] = 10
  → visit 2: dp[101][2] = 0 + dist[0][2] = 15

From dp[011][1]=10:  (0,1 visited, at 1)
  → visit 2: dp[111][2] = 10 + dist[1][2] = 10 + 20 = 30

From dp[101][2]=15:  (0,2 visited, at 2)
  → visit 1: dp[111][1] = 15 + dist[2][1] = 15 + 20 = 35

Close the tour (add dist[i][0], full mask = 111):
  i=2: dp[111][2] + dist[2][0] = 30 + 15 = 45
  i=1: dp[111][1] + dist[1][0] = 35 + 10 = 45

Answer = min(45, 45) = 45
```

Check by hand: the only distinct cycle is `0→1→2→0` = 10+20+15 = **45** (its reverse `0→2→1→0` = 15+20+10 = 45 too). The dp reaches exactly 45.

### Example: Assignment Problem

**Problem**: N workers, N tasks. Assign each worker exactly one task to minimize total cost.

**Convention** (shared with [Bitmask Techniques](/pattern/bitmask), so the two guides read the
same): the **mask holds the workers already used**, and `popcount(mask)` is therefore the index of
the **next job to fill**. Assigning greedily in job order costs nothing — every worker still gets
considered for every job across the state space — and it removes a whole dimension from the table.

You will also see the dual convention in the wild (mask = jobs filled, `popcount` = next worker).
It is equally correct; just never mix the two halfway through a solution, because `cost[a][b]`
silently transposes on you.

```python
def min_assignment(cost):
    n = len(cost)
    INF = float('inf')
    dp = [INF] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        job = bin(mask).count('1')      # mask = workers used, so this is the next job
        if job >= n:
            continue
        for worker in range(n):
            if mask & (1 << worker):    # this worker is already assigned
                continue
            nxt = mask | (1 << worker)
            dp[nxt] = min(dp[nxt], dp[mask] + cost[worker][job])

    return dp[(1 << n) - 1]
```

Time O(2ⁿ · n), space O(2ⁿ). LC 1879 (Minimum XOR Sum of Two Arrays) is this template with
`cost[i][j] = nums1[i] ^ nums2[j]`.

#### Walkthrough — LC 847 Shortest Path Visiting All Nodes

**This template solves: LC 847 (Shortest Path Visiting All Nodes), LC 943 (Find the Shortest Superstring — overlap-cost TSP), LC 526 (Beautiful Arrangement — count over used-mask).**

> An undirected connected graph of `n` nodes (`0..n-1`) is given as an adjacency list. Return the length of the **shortest walk that visits every node**. You may start and end anywhere, and revisit nodes and edges.

The state that makes this tractable is `(mask, node)`: *"I've visited the set of nodes in `mask` and I'm currently standing on `node`."* With `n ≤ 12`, that's only `2ⁿ · n` states. Because every edge costs `1`, the shortest walk is a **BFS over the state graph** — each step moves to a neighbor and turns on that neighbor's bit. The first time any state reaches the full mask `2ⁿ−1`, its BFS depth is the answer.

```python
from collections import deque

def shortestPathLength(graph):
    n = len(graph)
    if n == 1:
        return 0
    full = (1 << n) - 1
    q = deque()
    seen = set()
    for i in range(n):                 # a walk may start at ANY node
        q.append((i, 1 << i, 0))       # (node, visited-mask, dist)
        seen.add((i, 1 << i))
    while q:
        node, mask, d = q.popleft()
        if mask == full:
            return d
        for nb in graph[node]:
            nm = mask | (1 << nb)      # mark neighbor visited
            if (nb, nm) not in seen:
                seen.add((nb, nm))
                q.append((nb, nm, d + 1))
    return -1
```

On `graph = [[1,2,3],[0],[0],[0]]` (a star: node 0 joined to 1, 2, 3) the answer is **4** — e.g. `1→0→2→0→3` visits all four nodes in 4 steps, and no shorter walk covers the three leaves that all hang off 0.

`★ Insight ─────────────────────────────────────`
- **The bitmask *is* the DP dimension; BFS supplies the ordering.** Because visiting-all can revisit nodes, this isn't a permutation search (`n!`) — it's a shortest-path over `2ⁿ·n` states, so BFS layers deliver optimal distance directly. Seeding the queue with *every* start node encodes "start anywhere" for free. Deduping on `(node, mask)` (not just `mask`) is essential — the same visited-set reached at a different current node is a genuinely different state.
- **`mask` shines exactly when a subproblem is "which of ≤ ~20 items are used."** TSP (each city once), assignment (each worker↔task), and this walk all share the "subset-of-used + where-am-I" state. The bit operations (`1<<i` test, `mask|(1<<j)` set) are the vocabulary; recognizing that the *set of used elements* — not their order — is the memoizable state is the pattern.
`─────────────────────────────────────────────────`

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

There are three distinct cost classes here, and picking the wrong one is how people mis-budget a
bitmask solution:

| Shape of the transition | Time | Example |
|-------------------------|------|---------|
| From each mask, pick one **unused element** | O(2^N · N) | assignment DP, count-arrangements |
| From each `(mask, last)`, move to one **next element** | O(2^N · N²) | TSP, LC 847, LC 943 |
| From each mask, iterate every **submask** of it | **O(3^N)** | k-way partition, set cover, LC 2305 |

The O(3^N) row surprises people. Summing `2^popcount(mask)` over all `2^N` masks gives `3^N`, not
`4^N` — see [Bitmask Techniques](/pattern/bitmask) for the derivation and
[Bitmask DP — Subset Partition](/pattern/bitmask-dp-subset-partition) for the partition family
that lives entirely in this row.

Space: O(2^N) or O(2^N · N). Only feasible for N <= ~20 (N <= ~16 if you are in the O(3^N) row).

---

## 12. Digit DP

> **Who owns what.** [Digit DP](/pattern/digit-dp) is canonical: seven worked problems, the
> `tight`/`started` flag discipline, and the pitfalls. This section covers the range trick and
> one walkthrough so you can recognise the family from inside the DP guide. Note the flag
> difference: the template below omits `started` because LC 233 counts from 0 and leading zeros
> are harmless there. Any problem where a leading zero would be *counted as a digit* needs the
> `started` flag — that is why the canonical guide carries it everywhere.

### Pattern

Count numbers in range [L, R] with some digit property. Use the trick: `count(R) - count(L-1)`.

**Intuition**: you must count integers up to `10^18` satisfying some digit rule — far too many to iterate one by one. Instead, *build the number digit by digit* left to right and count valid completions. Two partial numbers that have the same "position, property-so-far, and whether they're still hugging the upper bound" have the same number of valid completions, so memoize on that small state. Iterating `10^18` numbers becomes filling a tiny `positions × states` table.

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

**This template solves: LC 233 (Number of Digit One), LC 357 (Count Numbers with Unique Digits), LC 902 (Numbers At Most N Given Digit Set), LC 600 (Non-negative Integers without Consecutive Ones).**

#### Walkthrough — LC 233 Number of Digit One

> Given integer `n`, count total number of digit `1` appearing in all numbers from `0` to `n`. Example: `n = 13` → `1,10,11,12,13` contribute the digit `1` a total of **6** times (11 alone has two).

Note the target: not *how many numbers contain a 1*, but *how many `1`s appear* — 11 counts twice. So the accumulator carries the running count of 1s placed in the prefix, and the base case returns that count (not a boolean).

```python
from functools import lru_cache

def countDigitOne(n):
    if n < 0:
        return 0
    digits = [int(c) for c in str(n)]
    L = len(digits)

    @lru_cache(None)
    def solve(pos, cnt, tight):
        # cnt = number of 1s already placed in the prefix
        if pos == L:
            return cnt
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(limit + 1):
            total += solve(pos + 1, cnt + (1 if d == 1 else 0), tight and d == limit)
        return total

    return solve(0, 0, True)
```

Trace on `n = 13` (`digits = [1, 3]`, `L = 2`):

```
solve(0, 0, tight=True)  limit = digits[0] = 1
  d=0  solve(1, 0, tight=False)   ← d<limit releases tight: any second digit 0..9
         d=0..9, cnt stays 0 except d=1 adds 1 → contributes 1   (the "1" in 01)
  d=1  solve(1, 1, tight=True)    limit = digits[1] = 3
         d=0 solve(2,1,..)=1   d=1 solve(2,2,..)=2   d=2 solve(2,1,..)=1
         d=3 solve(2,1,tight)=1                       → contributes 5
                                                (10,11×2,12,13 = 1+2+1+1)
total = 1 + 5 = 6
```

The `tight` flag is the whole engine of digit DP. While `tight` is true, you are still hugging the upper bound `n`, so this digit may not exceed `digits[pos]`. The instant you pick a digit *strictly below* the limit (`d < limit`), every later position is free to run `0..9` — `tight` drops to false and the `@lru_cache` result for `(pos, cnt, False)` is shared across all such prefixes. That shared subtree is where the exponential blowup collapses into `O(L · 10 · states)`.

`★ Insight ─────────────────────────────────────`
- **`tight` is the bound-hugging bit.** True = prefix equals `n`'s prefix so far (digit capped at `digits[pos]`); false = prefix already went below, so the tail is unconstrained and memoizable. Only the `tight=False` states get cache hits — that's why the cache key *must* include `tight`.
- **Range `[L, R]` via prefix subtraction.** Digit DP naturally counts `[0, n]`. For a query on `[L, R]` (e.g. LC 902, LC 600), compute `f(R) - f(L-1)`. Same trick as prefix sums, one dimension up.
- **Accumulate vs. decide.** Here the base case returns the accumulated `cnt` (a sum of occurrences). Contrast the boolean/counting digit-DP variants above where the base case returns `1` for "this number qualifies" — the skeleton is identical; only what the leaf returns changes.
`─────────────────────────────────────────────────`

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

**This template solves: LC 688 (Knight Probability in Chessboard), LC 837 (New 21 Game), LC 808 (Soup Servings), LC 1223 (Dice Roll Simulation).**

#### Walkthrough — LC 688 Knight Probability in Chessboard

> An `n × n` board. A knight starts at `(row, col)` and makes exactly `k` moves, each move chosen **uniformly at random** from the 8 knight moves — even ones that fly off the board. Once it leaves the board it stops. Return the probability the knight is still **on the board** after `k` moves.

State: `solve(r, c, steps)` = probability of surviving `steps` more moves starting from `(r, c)`. Each move splits the current probability mass into 8 equal eighths, one per knight jump; jumps that land off-board contribute 0.

```python
from functools import lru_cache

def knightProbability(n, k, row, col):
    moves = [(1, 2), (1, -2), (-1, 2), (-1, -2),
             (2, 1), (2, -1), (-2, 1), (-2, -1)]

    @lru_cache(None)
    def solve(r, c, steps):
        if not (0 <= r < n and 0 <= c < n):
            return 0.0            # fell off — this branch contributes nothing
        if steps == 0:
            return 1.0            # survived all k moves
        return sum(solve(r + dr, c + dc, steps - 1)
                   for dr, dc in moves) / 8.0

    return solve(row, col, k)
```

Trace on `n = 3, k = 2, start = (0, 0)`:

```
solve(0,0,2): try all 8 jumps from corner (0,0)
  on-board landings: (1,2) and (2,1)   ← only 2 of 8 stay on a 3×3 board
  each recurses one more step:

  solve(1,2,1): jumps from (1,2), count on-board landings = 2  → 2/8 = 0.25
  solve(2,1,1): jumps from (2,1), count on-board landings = 2  → 2/8 = 0.25
  other 6 jumps → off-board → 0.0

  solve(0,0,2) = (0.25 + 0.25 + 0 + 0 + 0 + 0 + 0 + 0) / 8 = 0.5 / 8 = 0.0625
```

The recurrence works *forward* in probability: dividing by 8 at each level spreads the mass, and summing 8 children re-collects it. Equivalently you can push forward a full `dp[r][c]` probability grid `k` times — same math, iterative form. The memo key `(r, c, steps)` is essential: many jump sequences revisit the same square with the same moves left, and without the cache the branching is `8^k`.

`★ Insight ─────────────────────────────────────`
- **Probability DP = weighted counting.** Instead of *counting* paths and dividing at the end, you carry the `/8` at every transition so each `dp` value is already a probability. The two views are identical; the per-step division just keeps numbers bounded in `[0, 1]`.
- **Off-board = absorbing 0 state.** You don't prune the 8 moves to "legal" ones — you let all 8 fire and let out-of-bounds return `0.0`. That keeps the `/8` denominator honest (the knight *chooses* among 8, some are fatal), which is exactly what the problem states.
- **Forward vs. backward.** This memoized recursion pulls from children (top-down). The dice/sushi examples above push *backward from the goal* for expected steps. Prefer forward-probability when the horizon `k` is fixed; backward-expectation when you want "expected number of steps until an event."
`─────────────────────────────────────────────────`

---

## 14. DP on DAGs

> **Who owns what.** This section is canonical for the DP framing — memoized recursion over an
> *implicit* DAG (LC 329, where the DAG is "cell → strictly larger neighbour" and never gets
> built). [Graph Patterns §15](/pattern/graph) owns the graph-side pipeline: condense a cyclic
> graph into its SCC DAG first, then run this.

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
    # Precondition: nodes are processed in topological order (Kahn's below
    # guarantees this). dp[src]=1 seeds the source; every other dp[v] is
    # finalized only after all its predecessors are processed. Requires a
    # DAG — a cycle would loop forever (Kahn's would never enqueue those nodes).
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

**This template solves: LC 329 (Longest Increasing Path in a Matrix), LC 2050 (Parallel Courses III), LC 851 (Loud and Rich).**

> **LC 1494 (Parallel Courses II) is not one of these**, despite looking like a dependency-order
> problem. The `k`-courses-per-semester cap means you choose a *submask* of the currently
> available courses each step, so the state is a mask, not a topological position:
> [Bitmask DP — Subset Partition §9](/pattern/bitmask-dp-subset-partition).

#### Walkthrough — LC 329 Longest Increasing Path in a Matrix

> Given an `m × n` integer matrix, return the length of the **longest strictly increasing path**. From a cell you may move up/down/left/right (no diagonals, no wrap). Example: `[[9,9,4],[6,6,8],[2,1,1]]` → `4`, the path `1 → 2 → 6 → 9`.

The DAG is *implicit*: draw a directed edge `u → v` whenever `v` is an orthogonal neighbor with a strictly larger value. Strictly-increasing guarantees no cycles, so it's a genuine DAG — no explicit topo sort needed, because **memoized DFS visits nodes in an order that respects the edges automatically** (a cell's answer is only finalized after all its larger-neighbor answers are).

```python
from functools import lru_cache

def longestIncreasingPath(matrix):
    if not matrix or not matrix[0]:
        return 0
    R, C = len(matrix), len(matrix[0])

    @lru_cache(None)
    def dfs(r, c):
        best = 1                          # the cell itself, length 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))   # only climb to larger cells
        return best

    return max(dfs(r, c) for r in range(R) for c in range(C))
```

Trace on `[[9,9,4],[6,6,8],[2,1,1]]` (rows top→bottom):

```
dfs at each cell = longest increasing path STARTING there:

  9  9  4        1  1  1
  6  6  8   →    2  2  1        dfs(2,1)=1 (value 1, no larger neighbor up=2? 2>1 yes)
  2  1  1        3  4  1

follow the max: 1(2,1) → 2(1,0/1)? actual best chain:
  1 → 2 → 6 → 9   lengths  1 → 2 → 3 → 4

answer = max over all cells = 4
```

The memo is what turns exponential path enumeration into `O(R·C)`: each cell's longest-path-from-here is computed once and reused by every neighbor that flows into it. Because the guard `matrix[nr][nc] > matrix[r][c]` only ever recurses "uphill," the recursion depth is bounded and no visited-set is needed — the strict inequality *is* the acyclicity certificate.

`★ Insight ─────────────────────────────────────`
- **Memoized DFS = implicit topological order.** You never build in-degrees or a Kahn queue. Recursion bottoms out at local maxima (sinks of the DAG) and unwinds; each `dfs(u)` finalizes only after all `dfs(v)` for its out-edges return. That post-order unwind *is* reverse-topological processing.
- **The edge rule encodes the DAG.** No adjacency list is stored — "strictly larger orthogonal neighbor" generates edges on the fly. Whenever a grid problem says "move only if the next cell is bigger/smaller/valid," suspect DP-on-implicit-DAG.
- **No `visited` set, deliberately.** Ordinary grid DFS needs one to avoid revisiting; here the strict-increase constraint makes revisiting impossible, so the cache alone suffices. Add a visited set only if the relation can tie or cycle.
`─────────────────────────────────────────────────`

---

## 15. DP Optimizations

When the basic DP is too slow, apply these optimizations.

### 15.0 Space Optimization Principles

The most common DP optimization — reducing memory without changing time complexity. This is a **frequent interview follow-up**: "Can you do it in less space?"

#### The Core Rule

> **If `dp[i]` only depends on a bounded window of previous states, you only need to keep that window in memory.**

#### Decision Framework

| Dependency pattern | Reduction | Technique |
|-------------------|-----------|-----------|
| `dp[i]` depends only on `dp[i-1]` | O(N) → O(1) | Two variables |
| `dp[i]` depends on `dp[i-1]` and `dp[i-2]` | O(N) → O(1) | Three variables |
| `dp[i][j]` depends on row `i-1` only | O(MN) → O(N) | Two rows or single row |
| `dp[i][j]` depends on `dp[i-1][j-1]`, `dp[i-1][j]`, `dp[i][j-1]` | O(MN) → O(N) | Single row + saved diagonal |
| `dp[i][j]` depends on any `dp[i][k]`, `dp[k][j]` | **Cannot reduce** | Need full table (interval DP) |
| `dp[mask]` over subsets | **Cannot reduce** | Need full 2^N table |

#### The Reverse-Iteration Trick (Critical for Knapsack)

When flattening 2D → 1D, the **iteration direction** determines whether old or new values are read:

```
Forward iteration (left to right):
  dp[w - weight[i]] reads the ALREADY-UPDATED value from THIS iteration
  → item i can be reused → UNBOUNDED knapsack

Reverse iteration (right to left):
  dp[w - weight[i]] reads the NOT-YET-UPDATED value from PREVIOUS iteration
  → item i used at most once → 0/1 knapsack

Mnemonic: "Reverse = Restrict (to one use)"
```

#### The Diagonal-Save Trick (for LCS / Edit Distance)

When a single-row DP depends on `dp[i-1][j-1]` (the diagonal), that value gets overwritten as you process column `j`. Save it before overwriting:

```python
prev_diag = 0
for j in range(1, n + 1):
    temp = dp[j]           # save dp[i-1][j] before overwrite
    dp[j] = f(dp[j],       # dp[i-1][j]  (old value, still intact)
              dp[j-1],      # dp[i][j-1]  (already updated this row)
              prev_diag)    # dp[i-1][j-1] (saved from last iteration)
    prev_diag = temp        # carry forward for next column
```

#### The Simultaneous-Update Rule (State Machine DP)

When multiple states depend on each other at step `i-1`, update them **simultaneously** — otherwise you'll accidentally read a partially-updated current-step value:

```python
# WRONG: hold uses the just-updated rest value
rest = max(rest, cool)
hold = max(hold, rest - prices[i])  # bug: rest is already step i!

# CORRECT: compute all new values, then assign
new_rest = max(rest, cool)
new_hold = max(hold, rest - prices[i])
new_cool = hold + prices[i]
rest, hold, cool = new_rest, new_hold, new_cool

# ALSO CORRECT: Python tuple unpacking (idiomatic)
rest, hold, cool = max(rest, cool), max(hold, rest - prices[i]), hold + prices[i]
```

#### When Space Optimization Isn't Possible

- **Interval DP**: `dp[i][j]` depends on arbitrary sub-intervals — need full O(N^2) table
- **Bitmask DP**: `dp[mask]` over all 2^N subsets — need full table
- **When you need to reconstruct the solution**: Space optimization preserves the final answer but discards the path. To reconstruct, either keep the full table or use Hirschberg's divide-and-conquer trick (works for LCS in O(N) space)
- **Tree DP with rerooting**: Needs full dp_down[] and dp_up[] arrays

#### Space Optimization Summary by Pattern

| Pattern | Original space | Optimized space | How |
|---------|---------------|----------------|-----|
| Fibonacci / Linear (window) | O(N) | O(1) | Rolling variables |
| Grid DP | O(MN) | O(N) | Process row by row |
| 0/1 Knapsack | O(NW) | O(W) | 1D array, **reverse** iteration |
| Unbounded Knapsack | O(NW) | O(W) | 1D array, **forward** iteration |
| LCS / Edit Distance | O(MN) | O(min(M,N)) | Single row + diagonal save |
| State Machine DP | O(N × S) | O(S) | S variables, simultaneous update |
| Interval DP | O(N^2) | O(N^2) | Cannot reduce |
| Bitmask DP | O(2^N) | O(2^N) | Cannot reduce |

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

**This template solves: LC 1137 (N-th Tribonacci), LC 70 (Climbing Stairs, huge-N variant), LC 509 (Fibonacci Number), and any "linear recurrence, `n` up to 10^18" problem.**

#### Note — LC 1137 N-th Tribonacci

> `T(0)=0, T(1)=1, T(2)=1`, and `T(n) = T(n-1)+T(n-2)+T(n-3)`. Return `T(n)`.

At LeetCode's constraint (`n ≤ 37`) a two-line rolling window is the intended answer — this is an *Easy*:

```python
def tribonacci(n):
    a, b, c = 0, 1, 1
    if n == 0: return 0
    for _ in range(n - 2):
        a, b, c = b, c, a + b + c
    return c
```

The reason it lives under Optimizations is the **"huge N" hook**: the moment the same recurrence is asked for `n` up to `10^18` (a common interview escalation, or Codeforces/Project-Euler framing), the O(N) loop dies and you switch to matrix exponentiation. Tribonacci's transition matrix is the 3×3 companion matrix:

```
| T(n+1) |   | 1 1 1 |   | T(n)   |
| T(n)   | = | 1 0 0 | · | T(n-1) |
| T(n-1) |   | 0 1 0 |   | T(n-2) |
```

Raise that matrix to the `n`-th power with the same `mat_pow` binary-exponentiation skeleton shown above (swap the 2×2 for this 3×3) → `O(3³ log n)`.

`★ Insight ─────────────────────────────────────`
- **The recurrence *is* the matrix.** Any constant-coefficient linear recurrence of order `k` becomes a `k×k` companion matrix; the top-left row holds the coefficients, a sub-diagonal of `1`s shifts the window. Fibonacci is `k=2`, Tribonacci `k=3` — same machine.
- **The trigger is `n`, not the recurrence.** Rolling variables are correct and simpler until `n` is astronomically large. Recognize the escalation ("`n ≤ 10^18`") as the *only* signal to pay the matrix-power complexity — don't reach for it on the Easy version.
- **This is the DP cousin of fast exponentiation.** Same `while p: if p&1 ... M=M·M; p>>=1` loop as integer `pow(a, n)` — you're just multiplying matrices instead of scalars.
`─────────────────────────────────────────────────`

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
| Bitmask DP (pick next element) | O(2^N * N) | O(2^N) |
| Bitmask DP (TSP, `dp[mask][last]`) | O(2^N * N^2) | O(2^N * N) |
| Bitmask DP (submask enumeration) | O(3^N) | O(2^N) |
| Digit DP | O(D * S * 10) | O(D * S) |
| Matrix Exponent. | O(K^3 log N) | O(K^2) |

---

## 17. Practice Order

Climb this ladder — each rung introduces one new DP shape built on the last.

```
Start here
    │
    ▼
  LC 70   Climbing Stairs            (Easy)   ── the "hello world" of DP: dp[i]=dp[i-1]+dp[i-2]
    │
    ▼
  LC 198  House Robber               (Medium) ── add a choice: take-or-skip with an adjacency constraint
    │
    ▼
  LC 322  Coin Change                (Medium) ── unbounded knapsack: minimize count over a target sum
    │
    ▼
  LC 300  Longest Increasing Subseq. (Medium) ── dp[i] over subsequences; then the O(N log N) tails trick
    │
    ▼
  LC 72   Edit Distance              (Medium) ── 2D table: transition over two-string prefixes
    │
    ▼
  LC 188  Best Time Buy/Sell Stock IV (Hard)  ── state-machine DP with a transaction-count dimension
```

Once the main ladder feels solid, branch into the remaining families — each maps to one worked walkthrough above:

```
  LC 416  Partition Equal Subset Sum   (Medium) ── 0/1 knapsack disguise; reverse-loop feasibility   (§5)
  LC 1143 Longest Common Subsequence   (Medium) ── the 2D two-string namesake                        (§7)
  LC 312  Burst Balloons               (Hard)   ── interval DP, "last to burst" reframing            (§8)
  LC 337  House Robber III             (Medium) ── tree DP; return (rob, skip) pair — callback to 198 (§10)
  LC 847  Shortest Path Visiting Nodes (Hard)   ── bitmask state + BFS ordering                       (§11)
  LC 233  Number of Digit One          (Hard)   ── digit DP; tight flag, count(R)-count(L-1)          (§12)
  LC 688  Knight Probability           (Medium) ── probability DP; mass /8 per move                   (§13)
  LC 329  Longest Increasing Path      (Hard)   ── DP on implicit DAG; memo = topo order              (§14)
```

---

## The 13 Families at a Glance

```
LINEAR        1-D chain, dp[i] from dp[i-1..i-k]        LC 198  House Robber
GRID          2-D board, dp[i][j] from up/left          LC 64   Minimum Path Sum
KNAPSACK      pick items under a capacity/target         LC 416  Partition Equal Subset Sum
LIS           best subsequence, dp[i] or tails+bisect    LC 300  Longest Increasing Subsequence
LCS           two sequences, dp[i][j] on prefixes        LC 1143 Longest Common Subsequence
INTERVAL      range [i,j], split on last/first action    LC 312  Burst Balloons
STATE MACHINE fixed states + transitions each step       LC 309  Buy/Sell w/ Cooldown
TREE          post-order, child answers → parent (pair)  LC 337  House Robber III
BITMASK       subset in an int, N ≤ ~20                   LC 847  Shortest Path Visiting All Nodes
DIGIT         build number digit-by-digit, tight flag    LC 233  Number of Digit One
PROBABILITY   carry probability / expected value         LC 688  Knight Probability in Chessboard
DP ON DAG     topological / memoized order over a DAG    LC 329  Longest Increasing Path in a Matrix
OPTIMIZATION  CHT / Knuth / SOS / matrix-power speedups   LC 1137 N-th Tribonacci (huge-N → matrix expo)
```

---

## When This Fails

DP needs **optimal substructure** (the best solution is built from best solutions of
subproblems) and **overlapping subproblems** (the same subproblem recurs). Missing either one:

- **No overlap.** Distinct subproblems every time means memoization only adds bookkeeping — it is
  plain divide and conquer, or backtracking.
- **No optimal substructure.** If a globally best answer can require a locally suboptimal
  subsolution, the recurrence is wrong. This is the failure that produces a confidently incorrect
  answer.
- **The state is incomplete.** If two situations share a state key but have different futures,
  memoization returns the wrong cached value. The fix is always to add the missing dimension —
  which is why "what exactly does `dp[i]` mean?" must be answerable in one sentence.
- **Greedy actually works.** Coin change with arbitrary denominations needs DP; with canonical
  currency systems, greedy is correct and far faster. Prove it before assuming it.
- **The state space does not fit.** `2^n` with `n = 40` is not a table. Consider
  meet-in-the-middle, or a different formulation entirely.

## Self-Test

Answer these from memory, out loud or on paper, *before* looking. Recognition is not
recall: rereading an explanation feels like knowing, and it is not. A question you cannot answer
cold names the exact section to revisit — you do not need to reread the guide.


**1. What two properties must a problem have before DP applies?**

<details markdown="1">
<summary>Answer</summary>

Optimal substructure (an optimal solution is composed of optimal solutions to subproblems) and overlapping subproblems (the same subproblem is solved repeatedly). Without overlap it is divide and conquer; without optimal substructure the recurrence is simply wrong.

</details>

**2. What five questions define any DP, in order?**

<details markdown="1">
<summary>Answer</summary>

What does the state mean (in one sentence)? What is the recurrence? What are the base cases? Which cell holds the answer? In what iteration order must the table be filled so every dependency is ready? If you cannot answer the first, the rest cannot be right.

</details>

**3. 0/1 knapsack versus unbounded — what is the code difference and why?**

<details markdown="1">
<summary>Answer</summary>

The inner capacity loop direction. Descending for 0/1: reading `dp[w - weight]` from the *previous* item's row means each item is used at most once. Ascending for unbounded: it reads the current row, already updated with this item, allowing reuse. One character apart, completely different problems, no error message.

</details>

**4. LIS in O(n log n): what does the `tails` array hold?**

<details markdown="1">
<summary>Answer</summary>

`tails[i]` is the smallest possible tail of any increasing subsequence of length `i+1`. It is not itself a valid subsequence. Its *length* is the answer. Use `bisect_left` for strictly increasing, `bisect_right` for non-decreasing.

</details>

**5. Why must interval DP iterate by increasing interval length?**

<details markdown="1">
<summary>Answer</summary>

`dp[i][j]` depends on strictly shorter intervals inside `[i, j]`. Length-outer ordering guarantees every dependency is computed. Looping `i` and `j` directly reads uninitialised cells.

</details>

**6. Digit DP: why must the `tight` flag be part of the memo key?**

<details markdown="1">
<summary>Answer</summary>

`tight` means "the prefix so far exactly matches the bound's prefix", which restricts the digits still available. Two states identical except for `tight` have genuinely different completion counts, so sharing a cache entry between them is wrong.

</details>

**7. Name the three cost classes of bitmask DP.**

<details markdown="1">
<summary>Answer</summary>

Pick one unused element per mask: O(2^n · n). Track `(mask, last)` and move to a next element (TSP): O(2^n · n²). Enumerate every submask of every mask (partition): **O(3^n)**, because `Σ 2^popcount(mask)` over all masks equals `3^n`.

</details>

**8. Top-down or bottom-up — what actually decides it?**

<details markdown="1">
<summary>Answer</summary>

Top-down when the reachable state space is sparse (it only visits states you need) or when the recurrence is easier to express recursively. Bottom-up when you want to drop a dimension via rolling arrays, or to avoid Python's recursion limit. They compute the same table.

</details>

**9. When is greedy enough and DP wasted?**

<details markdown="1">
<summary>Answer</summary>

When a locally optimal choice is provably globally optimal — activity selection by earliest end time, Huffman coding, coin change in a canonical system. The word is *provably*: greedy that merely passes the samples is the classic wrong answer.

</details>

---

## See Also

The DP families that grew their own guides:

- [Digit DP](/pattern/digit-dp) — the full treatment of §12: seven worked problems, `tight`/`started` discipline, and the pitfalls.
- [Bitmask Techniques](/pattern/bitmask) — bit operations, subset enumeration, and SOS DP, the machinery §11 assumes.
- [Bitmask DP — Subset Partition](/pattern/bitmask-dp-subset-partition) — the O(3^n) partition family (LC 1986, 2305, 698, 943, 1494).
- [Tree Patterns](/pattern/tree) — tree DP in its natural habitat, plus rerooting, HLD, and centroid decomposition.
- [Edge Contribution & Rerooting](/pattern/edge-contribution) — "answer for every node as root" in O(n), the rerooting cousin of tree DP.
- [Graph Patterns §15](/pattern/graph) — DP on DAGs from the graph side, including the SCC-condensation pipeline that turns a cyclic graph into a DAG you can DP over.
- [Backtracking](/pattern/backtracking) — when you need the actual solutions, not just the count or the optimum.
- [Pattern Decision Map](/pattern/decision-map) — the router: which technique does a cold problem call for?
- [Pattern Mastery Program](/pattern/mastery) — the spaced-repetition schedule, mastery checklist, and drill formats that turn reading into recall.

---

*Pattern mastered — every DP is a choice at each step whose subproblems repeat. Name the state, name the transition, and the family names itself.*

