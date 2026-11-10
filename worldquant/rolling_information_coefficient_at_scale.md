---
layout: simple
title: "Rolling Information Coefficient at Scale"
permalink: /worldquant/rolling_information_coefficient_at_scale
difficulty: Hard
tags: [statistics, rolling-window, correlation, worldquant, finance]
---

# Rolling Information Coefficient at Scale

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Statistics / Rolling Window / Data Processing |
| **Key Technique** | Incremental Pearson/Spearman correlation with O(1) per step |

### Learning Goals
- [ ] Understand what the Information Coefficient (IC) measures in finance
- [ ] Compute Pearson IC efficiently using running statistics
- [ ] Understand why Spearman IC requires rank transformation first
- [ ] Handle NaN values in rolling correlation

---

## Problem Statement

The **Information Coefficient (IC)** at time `t` is the Pearson (or Spearman) correlation between a vector of factor predictions and a vector of realised forward returns across all assets.

Given:
- `factors`: a 2D array of shape `(T, N)` — factor values for `N` assets over `T` time steps
- `returns`: a 2D array of shape `(T, N)` — forward returns for `N` assets over `T` time steps
- `window`: rolling window size `W`

For each time step `t >= W - 1`, compute the **rolling IC** over the past `W` time steps:

```
IC[t] = pearson_corr(factors[t-W+1:t+1].flatten(), returns[t-W+1:t+1].flatten())
```

Return the array `IC` of length `T - W + 1`.

**Constraints:**
- `1 <= W <= T <= 10^4`
- `1 <= N <= 10^3`
- Values may contain NaN (exclude those pairs from correlation)
- `-10^6 <= factors[t][i], returns[t][i] <= 10^6`

---

## Examples

### Example 1
```
Input:
factors = [[1, 2, 3], [4, 5, 6]]
returns = [[0.1, 0.3, 0.2], [0.5, 0.4, 0.6]]
window  = 2

Step t=1 uses all 6 paired values:
  f = [1,2,3,4,5,6], r = [0.1,0.3,0.2,0.5,0.4,0.6]
  IC[0] = pearson_corr(f, r) ≈ 0.828

Output: [0.828]
```

### Example 2 — With NaN
```
factors = [[1, NaN, 3]]
returns = [[0.1, 0.2, 0.3]]
window  = 1

Valid pairs: (1, 0.1), (3, 0.3)
IC[0] = pearson_corr([1,3], [0.1,0.3]) = 1.0
```

---

## Pearson Correlation Formula

For paired vectors `(x, y)` of length `m`:

```
mean_x = sum(x) / m
mean_y = sum(y) / m
cov     = sum((xi - mean_x)(yi - mean_y)) / m
std_x   = sqrt(sum((xi - mean_x)^2) / m)
std_y   = sqrt(sum((yi - mean_y)^2) / m)
r       = cov / (std_x * std_y)
```

Or equivalently:
```
r = (m·Σxy - Σx·Σy) / sqrt((m·Σx² - (Σx)²)(m·Σy² - (Σy)²))
```

This form is useful for incremental updates.

---

## Approach: Sliding Window with Running Sums

For each window of W rows, maintain running sums:
- `S_x`, `S_y`, `S_xx`, `S_yy`, `S_xy`, `count` (excluding NaN pairs)

When the window slides, **subtract the leaving row's contribution** and **add the entering row's contribution**.

### Complexity

| | Complexity |
|---|---|
| **Time** | O(T × N) — one pass over all data |
| **Space** | O(W × N) for the window buffer |

---

## Implementation

```python
import math
from collections import deque

def rolling_ic(
    factors: list[list[float]],
    returns: list[list[float]],
    window: int
) -> list[float]:
    T = len(factors)
    N = len(factors[0])
    result = []

    # Sliding window of rows
    win_f = deque()  # stores rows of factors
    win_r = deque()  # stores rows of returns

    # Running sums (over valid pairs only)
    S_x = S_y = S_xx = S_yy = S_xy = 0.0
    count = 0

    def add_row(f_row, r_row):
        nonlocal S_x, S_y, S_xx, S_yy, S_xy, count
        for f, r in zip(f_row, r_row):
            if math.isnan(f) or math.isnan(r):
                continue
            S_x  += f;  S_y  += r
            S_xx += f*f; S_yy += r*r; S_xy += f*r
            count += 1

    def remove_row(f_row, r_row):
        nonlocal S_x, S_y, S_xx, S_yy, S_xy, count
        for f, r in zip(f_row, r_row):
            if math.isnan(f) or math.isnan(r):
                continue
            S_x  -= f;  S_y  -= r
            S_xx -= f*f; S_yy -= r*r; S_xy -= f*r
            count -= 1

    def pearson():
        if count < 2:
            return float('nan')
        num = count * S_xy - S_x * S_y
        den = math.sqrt(
            (count * S_xx - S_x**2) *
            (count * S_yy - S_y**2)
        )
        return num / den if den != 0 else float('nan')

    for t in range(T):
        add_row(factors[t], returns[t])
        win_f.append(factors[t])
        win_r.append(returns[t])

        if len(win_f) > window:
            remove_row(win_f.popleft(), win_r.popleft())

        if len(win_f) == window:
            result.append(pearson())

    return result
```

---

## Spearman IC Variant

Spearman IC = Pearson correlation of the **ranks** rather than raw values.

```python
from scipy.stats import rankdata

def spearman_ic_row(f_row, r_row):
    valid = [(f, r) for f, r in zip(f_row, r_row)
             if not math.isnan(f) and not math.isnan(r)]
    if len(valid) < 2:
        return float('nan')
    f_vals, r_vals = zip(*valid)
    f_ranks = rankdata(f_vals)
    r_ranks = rankdata(r_vals)
    return pearson(f_ranks, r_ranks)
```

For rolling Spearman IC, the rank transformation must be recomputed each window slide (no simple O(1) update), making it O(T × W × N log N).

---

## IC Interpretation

| IC value | Meaning |
|---|---|
| 1.0 | Perfect positive prediction |
| 0.0 | No predictive power |
| -1.0 | Perfect inverse prediction |
| > 0.05 | Considered "good" in practice |
| > 0.10 | Considered "excellent" in practice |

---

## Related Problems

| Problem | Note |
|---|---|
| Cross-Sectional Rank Transform with Ties and NaN | Input to Spearman IC |
| Rolling Correlation With Missing Values | Pairwise asset correlation version |
| Online EWMA Mean and Variance | Exponential weighting alternative to rolling window |
