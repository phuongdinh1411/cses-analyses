---
layout: simple
title: "Top-K Portfolio Selection with Stability Constraint"
permalink: /worldquant/top_k_portfolio_selection_with_stability_constraint
difficulty: Medium
tags: [greedy, sets, sorting, worldquant, finance]
---

# Top-K Portfolio Selection with Stability Constraint

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Greedy / Sets |
| **Key Technique** | Sorted selection with turnover budget |

### Learning Goals
- [ ] Model portfolio rebalancing as a constrained selection problem
- [ ] Minimise turnover (number of trades) while maximising signal
- [ ] Understand the stability-return tradeoff in quantitative strategies

---

## Problem Statement

You manage a portfolio of `k` assets selected from a universe of `n` assets. Each asset has a predicted **expected return** `returns[i]`.

Each day you may rebalance: select a new set of `k` assets. However, to minimise transaction costs, you have a **stability constraint**: you may **replace at most `t` assets** from the previous portfolio (turnover limit).

Given the current portfolio `prev` (set of `k` asset indices) and the new expected returns array `returns`, select `k` assets that:
1. Maximise total expected return
2. Replace **at most `t` assets** from `prev`

Return the set of selected asset indices. If multiple optimal sets exist, prefer lower indices.

**Input:**
- `n`: total number of assets
- `k`: portfolio size
- `t`: maximum allowed replacements (turnover budget)
- `returns`: array of length `n` with expected returns
- `prev`: list of `k` indices representing the current portfolio

**Output:**
- A sorted list of `k` asset indices forming the new portfolio

**Constraints:**
- `1 <= k <= n <= 10^5`
- `0 <= t <= k`
- `-10^9 <= returns[i] <= 10^9`

---

## Examples

### Example 1
```
Input:
n=6, k=3, t=1
returns = [5, 8, 3, 9, 1, 7]
prev    = [1, 3, 5]   (0-indexed: returns = [8, 9, 7])

Output: [1, 3, 5]  (no change needed — already top-3 by return)

Explanation:
Top-3 globally: indices [3,1,5] with returns [9,8,7].
prev = {1,3,5}, which is the same set. Turnover = 0 ≤ 1. ✅
```

### Example 2
```
Input:
n=6, k=3, t=1
returns = [5, 8, 3, 9, 1, 7]
prev    = [0, 1, 2]   (returns = [5, 8, 3])

Output: [1, 3, 5]

Explanation:
Top-3 globally: {1, 3, 5}. Diff from prev {0,1,2}: remove {0,2}, add {3,5} = 2 changes > t=1.
With t=1 we can make only 1 swap. Best single swap: drop index 2 (return 3), add index 3 (return 9).
New portfolio: {0, 1, 3} with total return 5+8+9=22. 
Or drop index 0 (return 5), add index 3: {1, 2, 3} total = 8+3+9=20.
Best single swap → {0,1,3} with total 22.
Output: [0, 1, 3]
```

---

## Approach: Greedy with Turnover Budget

### Algorithm

```
1. Keep all prev assets that are in the global top-(k+t) by return.
   (These are "safe" to retain — they won't be wastefully held.)
2. Sort non-prev assets by return descending.
3. Greedily add the best non-prev assets until we've made t additions.
4. Drop the t worst assets from prev to make room.
```

More precisely:

```
prev_set = set(prev)
all_sorted = sorted(range(n), key=lambda i: -returns[i])

# Assets already in prev, sorted by return ascending (worst first)
prev_by_return_asc = sorted(prev_set, key=lambda i: returns[i])

# Best assets NOT in prev
candidates = [i for i in all_sorted if i not in prev_set]

# Greedily swap: replace worst prev with best candidate, up to t times
swaps = 0
result = set(prev_set)
for cand in candidates:
    if swaps >= t:
        break
    worst = prev_by_return_asc[swaps]
    if returns[cand] > returns[worst]:
        result.remove(worst)
        result.add(cand)
        swaps += 1
    else:
        break  # No more beneficial swaps

return sorted(result)
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n log n) |
| **Space** | O(n) |

---

## Implementation

```python
def top_k_with_stability(
    n: int, k: int, t: int,
    returns: list[float],
    prev: list[int]
) -> list[int]:
    prev_set = set(prev)

    # Worst assets in current portfolio (candidates to drop)
    prev_sorted_asc = sorted(prev_set, key=lambda i: returns[i])

    # Best assets outside current portfolio (candidates to add)
    outside_sorted_desc = sorted(
        (i for i in range(n) if i not in prev_set),
        key=lambda i: -returns[i]
    )

    result = set(prev_set)
    swaps = 0

    for cand in outside_sorted_desc:
        if swaps >= t:
            break
        worst_in = prev_sorted_asc[swaps]
        if returns[cand] > returns[worst_in]:
            result.remove(worst_in)
            result.add(cand)
            swaps += 1
        else:
            break  # All remaining candidates are worse than worst held

    return sorted(result)
```

---

## Key Insight: Stability-Return Tradeoff

| t (turnover budget) | Behaviour |
|---|---|
| 0 | Portfolio unchanged — maximum stability |
| k | Unconstrained — choose globally optimal top-k |
| 1..k-1 | Partial rebalance — balance between signal and cost |

In practice, transaction costs make `t << k` optimal even when signal says to fully rebalance.

---

## Related Problems

| Problem | Note |
|---|---|
| Minimum Swaps to Sort by Popularity | Counting required swaps |
| LeetCode 1090 — Largest Values from Labels | Constrained selection |
| Rolling Rank in a Sliding Window | Ranking inputs to this problem |
