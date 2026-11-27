---
layout: simple
title: "Biological Hazards"
permalink: /worldquant/biological_hazards
difficulty: Medium
tags: [array, two-pointers, sliding-window, intervals, worldquant]
---

# Biological Hazards

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Array / Two Pointers |
| **Key Technique** | Count valid windows ending at each index |

### Learning Goals
- [ ] Count "good" contiguous subarrays in O(n + m) instead of O(n²)
- [ ] Turn pairwise constraints into a per-index left boundary
- [ ] Recognize the "for each right end, how many valid left ends?" pattern

### In 60 seconds
- A window `[l, r]` is bad if it contains both members of some forbidden pair `(a, b)`, i.e. `l <= min(a, b)` and `max(a, b) <= r`.
- For a fixed right end `r`, the window is good exactly when `l > left`, where `left` is the largest `min(a, b)` over all pairs with `max(a, b) <= r`.
- `left` only grows as `r` grows, so add `r - left` good windows for each `r`.

> **Say this in the interview:** "For each right end I keep the closest left boundary any forbidden pair imposes; every start after it is valid, so I add `r − left`. One pass, O(n + m)."

---

## Problem Statement

There are `n` bacteria labelled `1..n` placed in a row. You are given two arrays `allergic` and `poisonous` of length `m`: bacterium `allergic[i]` and bacterium `poisonous[i]` must never be in the same group.

A group is a **contiguous** interval `[l, r]` (`1 <= l <= r <= n`). Count the intervals that contain no forbidden pair.

This is the commonly reported HackerRank-style problem `bioHazard(n, allergic, poisonous)`.

**Input:**
- `n`: number of bacteria
- `allergic`, `poisonous`: arrays of length `m`; pair `i` is `(allergic[i], poisonous[i])`

**Output:**
- The number of valid intervals (can reach about `n²/2`, so use a 64-bit integer in typed languages)

**Constraints:**
- `1 <= n <= 10^5`
- `0 <= m <= 10^5`
- `1 <= allergic[i], poisonous[i] <= n`

---

## Examples

### Example 1
```
Input:  n = 3, allergic = [2, 1, 3], poisonous = [3, 3, 1]
Output: 4

Forbidden pairs: {2,3}, {1,3}, {1,3}
Valid intervals: [1], [2], [3], [1,2]
Invalid: [2,3], [1,3] (contain 2 and 3, or 1 and 3)
```

### Example 2
```
Input:  n = 4, allergic = [1], poisonous = [2]
Output: 7

All 10 intervals minus the 3 that contain both 1 and 2: [1,2], [1,3], [1,4]
```

### Example 3
```
Input:  n = 5, allergic = [], poisonous = []
Output: 15   (every interval: 5·6/2)
```

---

## Approach

### Brute force — O(n² · m)
Check every interval against every pair. Too slow for `n = 10^5`.

### Optimal — one pass, O(n + m)

1. For every pair, record `bound[max(a, b)] = max(bound[max(a, b)], min(a, b))`: once the window reaches `max(a, b)`, it must start after `min(a, b)`.
2. Sweep `r = 1..n`, keeping `left = max(left, bound[r])`. Valid starts for this `r` are `left + 1 .. r`, so add `r - left`.

`left` never decreases: a constraint that applies to right end `r` also applies to every larger `r`.

---

## Implementation

```python
def bio_hazard(n: int, allergic: list[int], poisonous: list[int]) -> int:
    bound = [0] * (n + 1)          # bound[r]: windows ending at >= r must start after this
    for a, b in zip(allergic, poisonous):
        lo, hi = min(a, b), max(a, b)
        bound[hi] = max(bound[hi], lo)

    left = 0
    total = 0
    for r in range(1, n + 1):
        left = max(left, bound[r])
        total += r - left          # starts left+1 .. r are all valid
    return total
```

---

## Dry Run — Example 1

`bound[3] = max(2, 1, 1) = 2`, all other bounds are 0.

| r | bound[r] | left | r − left | total |
|---|---|---|---|---|
| 1 | 0 | 0 | 1 | 1 |
| 2 | 0 | 0 | 2 | 3 |
| 3 | 2 | 2 | 1 | 4 |

Answer: **4** ✅

---

## Complexity

| | Complexity |
|---|---|
| **Time** | O(n + m) |
| **Space** | O(n) |

---

## Common Mistakes

- Forgetting that a pair may be given as `(larger, smaller)`; always use `min`/`max`.
- Resetting `left` per `r` instead of carrying the maximum forward.
- Overflow in typed languages: the count is up to ~5·10⁹ for `n = 10^5`.

---

## Variant: Minimum Number of Containment Zones (graph coloring)

Some versions instead ask for the minimum number of zones (not necessarily contiguous) so that no forbidden pair shares a zone. That is the graph's **chromatic number**:

- No edges → 1 zone.
- Edges and **bipartite** (no odd cycle) → exactly 2; check with BFS 2-coloring in O(n + m).
- Not bipartite → at least 3, and computing the exact minimum is **NP-hard** for general graphs. Say so in the interview; offer greedy/DSatur for an upper bound, or backtracking for small `n`.

```python
from collections import deque

def two_zones_suffice(n: int, pairs: list[tuple[int, int]]) -> bool:
    adj = [[] for _ in range(n + 1)]
    for u, v in pairs:
        adj[u].append(v)
        adj[v].append(u)
    color = [-1] * (n + 1)
    for start in range(1, n + 1):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nei in adj[node]:
                if color[nei] == -1:
                    color[nei] = 1 - color[node]
                    queue.append(nei)
                elif color[nei] == color[node]:
                    return False       # odd cycle
    return True
```

---

## Related Problems

| Problem | Note |
|---|---|
| Count Subarrays With Fixed Bounds (LeetCode 2444) | Same "valid starts for each end" counting |
| Possible Bipartition (LeetCode 886) | The zone variant with 2 zones |
| [Counting Pairs](/worldquant/counting_pairs) | Another pair-constraint counting problem |
