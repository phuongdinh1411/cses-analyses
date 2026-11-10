---
layout: simple
title: "Cross-Sectional Rank Transform with Ties and NaN"
permalink: /worldquant/cross_sectional_rank_transform
difficulty: Medium
tags: [array, sorting, ranking, nan-handling, worldquant, finance]
---

# Cross-Sectional Rank Transform with Ties and NaN

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Array / Sorting / Data Processing |
| **Key Technique** | Rank transform with tie-breaking and missing value handling |

### Learning Goals
- [ ] Implement cross-sectional ranking (rank across assets at one point in time)
- [ ] Handle multiple tie-breaking strategies: min, max, average, dense
- [ ] Correctly exclude or assign NaN values during ranking
- [ ] Normalise ranks to [-1, 1] or [0, 1] as used in alpha research

---

## Problem Statement

Given a 1D array `values` representing a cross-section of factor scores across `n` assets (e.g., P/E ratios, momentum scores), transform each non-NaN value into its **rank** among all non-NaN values.

Ties must be handled according to a specified `method`: `"average"`, `"min"`, `"max"`, or `"dense"`.

NaN values in the input must remain NaN in the output (they are excluded from ranking).

Optionally, **normalise** the ranks to the range `[-1, 1]` (zero-centred, commonly used in alpha research).

**Input:**
- `values`: array of floats (may contain NaN)
- `method`: one of `"average"`, `"min"`, `"max"`, `"dense"`
- `normalize`: boolean (if True, map ranks to [-1, 1])

**Output:**
- Array of the same length: ranked values (NaN where input was NaN)

**Constraints:**
- `1 <= n <= 10^6`
- At least one non-NaN value

---

## Examples

### Example 1 — Average Rank, No Normalisation
```
Input:  values = [3.0, NaN, 1.0, 3.0, 2.0], method = "average"
Output: [3.5, NaN, 1.0, 3.5, 2.0]

Explanation:
Non-NaN values: [3.0, 1.0, 3.0, 2.0]
Sorted:         [1.0, 2.0, 3.0, 3.0]
Ranks:          1.0 → 1, 2.0 → 2, 3.0 → average(3,4) = 3.5
```

### Example 2 — Dense Rank, Normalised
```
Input:  values = [5.0, 2.0, NaN, 2.0, 8.0], method = "dense", normalize = True
Output: [0.0, -1.0, NaN, -1.0, 1.0]

Dense ranks: 2.0→1, 5.0→2, 8.0→3 (max dense rank = 3)
Normalised to [-1,1]: rank_norm = 2*(rank-1)/(max_rank-1) - 1
  1 → -1.0, 2 → 0.0, 3 → 1.0
```

### Example 3 — Min Rank
```
Input:  values = [4.0, 4.0, 4.0], method = "min"
Output: [1.0, 1.0, 1.0]  (all ties get the minimum rank = 1)
```

---

## Approach

```
1. Identify non-NaN indices.
2. Extract and sort the non-NaN values while tracking original positions.
3. Assign ranks based on the chosen method.
4. Place ranks back into a result array of the same shape (NaN elsewhere).
5. If normalize=True, apply: rank_norm = 2*(rank - r_min)/(r_max - r_min) - 1
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n log n) |
| **Space** | O(n) |

---

## Implementation

```python
import math

def cross_sectional_rank(
    values: list[float],
    method: str = "average",
    normalize: bool = False
) -> list[float]:
    n = len(values)
    result = [float('nan')] * n

    # Collect non-NaN (value, original_index) pairs
    valid = [(v, i) for i, v in enumerate(values) if not math.isnan(v)]
    if not valid:
        return result

    valid_sorted = sorted(valid, key=lambda x: x[0])
    m = len(valid_sorted)

    # Compute ranks
    ranks = [0.0] * m
    i = 0
    while i < m:
        j = i
        # Find all tied elements
        while j < m and valid_sorted[j][0] == valid_sorted[i][0]:
            j += 1
        # i..j-1 are tied (1-indexed positions: i+1 .. j)
        if method == "min":
            r = i + 1
        elif method == "max":
            r = j
        elif method == "average":
            r = (i + 1 + j) / 2
        elif method == "dense":
            r = len(set(v for v, _ in valid_sorted[:j]))
        else:
            raise ValueError(f"Unknown method: {method}")
        for k in range(i, j):
            ranks[k] = r
        i = j

    # Place back
    for rank, (_, orig_idx) in zip(ranks, valid_sorted):
        result[orig_idx] = rank

    if normalize:
        r_min = min(ranks)
        r_max = max(ranks)
        if r_max == r_min:
            for idx, v in enumerate(result):
                if not math.isnan(v):
                    result[idx] = 0.0
        else:
            for idx, v in enumerate(result):
                if not math.isnan(v):
                    result[idx] = 2 * (v - r_min) / (r_max - r_min) - 1

    return result
```

---

## Rank Method Comparison

| Method | Tie handling | Example [3,3,3] in [1,3,3,3,5] |
|---|---|---|
| `min` | All ties get the lowest rank | 2, 2, 2 |
| `max` | All ties get the highest rank | 4, 4, 4 |
| `average` | All ties get the average rank | 3, 3, 3 |
| `dense` | Ranks increment by 1 per unique value | 2, 2, 2 (dense: 1→1, 3→2, 5→3) |

---

## Finance Context

Cross-sectional ranking is fundamental in **alpha research**:

```
alpha_rank[t, i] = rank of factor[t, i] among all assets at time t
```

Normalised rank `∈ [-1, 1]` removes the effect of factor magnitude, making the signal comparable across different factors and time periods. This is the core of the **rank-IC** computation.

---

## Related Problems

| Problem | Note |
|---|---|
| Rolling Rank in a Sliding Window | Time-series (rolling) version |
| Rolling Information Coefficient at Scale | Uses this as input |
| LeetCode 1331 — Rank Transform of an Array | Simplified (no NaN, dense rank only) |
