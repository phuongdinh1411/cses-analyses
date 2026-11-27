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

### In 60 seconds
- **Pattern:** Greedy pairwise swaps with an exchange argument
- **Key insight:** Pair the i-th best outsider with the i-th worst holding; gains only shrink, so swap while the gain is positive, up to `t` times.
- **Complexity:** O(n log n) time, O(n) space
- **Trap:** Swapping when the gain is zero or negative.

> **Say this in the interview:** "Swap gains are non-increasing, so taking the best swaps first is optimal under a turnover cap."

---

## Problem Statement

You manage a portfolio of `k` assets selected from a universe of `n` assets. Each asset has a predicted **expected return** `returns[i]`.

Each day you may rebalance: select a new set of `k` assets. However, to minimise transaction costs, you have a **stability constraint**: you may **replace at most `t` assets** from the previous portfolio (turnover limit).

Given the current portfolio `prev` (set of `k` asset indices) and the new expected returns array `returns`, select `k` assets that:
1. Maximise total expected return
2. Replace **at most `t` assets** from `prev`

Return the selected asset indices (any optimal set if there are ties).

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

Output: [0, 1, 3]

Explanation:
Unconstrained top-3 is {1, 3, 5}, but reaching it from {0, 1, 2} needs 2 swaps > t = 1.
One swap: drop the worst holding (index 2, return 3), add the best outsider (index 3, return 9).
New portfolio {0, 1, 3}, total 5 + 8 + 9 = 22.
```

---

## Approach: Greedy pairwise swaps

Brute force tries every set reachable with ≤ t swaps: O(C(k, t) · C(n-k, t)), which is hopeless.

### Algorithm

```
held      = prev sorted by return ascending    (worst first)
outsiders = non-prev sorted by return descending (best first)
for i in 0 .. t-1:
    if returns[outsiders[i]] > returns[held[i]]: swap them
    else: stop
```

### Why greedy is optimal

The gain of the i-th swap, `returns[outsiders[i]] - returns[held[i]]`, is non-increasing in `i`: outsiders get worse and holdings get better. Any optimal answer that makes `s` swaps can be exchanged, one pair at a time, into "the `s` best outsiders for the `s` worst holdings" without lowering the total. So the best plan is to take the first `s` swaps while their gain is positive.

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n log n) — or O(n + t log n) with `heapq.nlargest`/`nsmallest(t, ...)` |
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
