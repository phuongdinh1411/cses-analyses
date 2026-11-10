---
layout: simple
title: "Rolling Correlation With Missing Values"
permalink: /worldquant/rolling_correlation_with_missing_values
difficulty: Hard
tags: [statistics, rolling-window, correlation, nan-handling, worldquant, finance]
---

# Rolling Correlation With Missing Values

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Statistics / Rolling Window / Data Processing |
| **Key Technique** | Sliding window running sums, skipping NaN pairs |

### Learning Goals
- [ ] Compute rolling Pearson correlation between two time series
- [ ] Handle NaN values by excluding them from each window's computation
- [ ] Use running sums to make each step O(N) instead of O(W)
- [ ] Return NaN when fewer than 2 valid pairs exist in a window

---

## Problem Statement

Given two time series `x` and `y` of length `n` (both may contain NaN), and a window size `W`, compute the **rolling Pearson correlation** between `x` and `y` for each position `t >= W - 1`.

At each position `t`, the correlation is computed using only the **valid (non-NaN) pairs** within `x[t-W+1 .. t]` and `y[t-W+1 .. t]`. A pair `(x[i], y[i])` is valid only if **both** `x[i]` and `y[i]` are non-NaN.

If fewer than 2 valid pairs exist in the window, return NaN for that position.

**Input:**
- Two float arrays `x` and `y` of length `n` (may contain NaN)
- An integer `W` (window size)

**Output:**
- An array of length `n - W + 1`: rolling correlations (NaN where insufficient data)

**Constraints:**
- `1 <= W <= n <= 10^6`
- `-10^9 <= x[i], y[i] <= 10^9` (or NaN)

---

## Examples

### Example 1 — No Missing Values
```
Input:  x = [1, 2, 3, 4, 5], y = [5, 4, 3, 2, 1], W = 3
Output: [-1.0, -1.0, -1.0]

All windows have perfect negative correlation.
```

### Example 2 — With NaN
```
Input:
x = [1.0, NaN, 3.0, 4.0, 5.0]
y = [2.0, 3.0, NaN, 5.0, 6.0]
W = 3

Window t=2 [0..2]: pairs (1,2), (NaN,3→skip), (3,NaN→skip) → only 1 valid pair → NaN
Window t=3 [1..3]: pairs (NaN,3→skip), (3,NaN→skip), (4,5) → only 1 valid pair → NaN
Window t=4 [2..4]: pairs (3,NaN→skip), (4,5), (5,6) → 2 valid pairs: (4,5),(5,6)
  corr([4,5],[5,6]) = 1.0

Output: [NaN, NaN, 1.0]
```

### Example 3 — Constant series in window
```
x_window = [2, 2, 2], y_window = [1, 3, 5]
Correlation = NaN (std_x = 0, division by zero)
```

---

## Approach: Sliding Window with Running Sums

Maintain 6 running sums for valid pairs only:
`S1` (count), `Sx`, `Sy`, `Sxx`, `Syy`, `Sxy`

When the window slides:
- **Add** the entering pair `(x[t], y[t])` if both are non-NaN
- **Remove** the leaving pair `(x[t-W], y[t-W])` if both were non-NaN

Pearson correlation from sums:
```
corr = (S1*Sxy - Sx*Sy) / sqrt((S1*Sxx - Sx^2) * (S1*Syy - Sy^2))
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n) — each element added/removed once |
| **Space** | O(1) extra (beyond input storage) |

---

## Implementation

```python
import math

def rolling_corr(x: list[float], y: list[float], W: int) -> list[float]:
    n = len(x)
    result = []

    # Running sums
    S1 = Sx = Sy = Sxx = Syy = Sxy = 0.0

    def is_valid(xi, yi):
        return not math.isnan(xi) and not math.isnan(yi)

    def add(xi, yi):
        nonlocal S1, Sx, Sy, Sxx, Syy, Sxy
        if is_valid(xi, yi):
            S1  += 1;  Sx  += xi;  Sy  += yi
            Sxx += xi*xi; Syy += yi*yi; Sxy += xi*yi

    def remove(xi, yi):
        nonlocal S1, Sx, Sy, Sxx, Syy, Sxy
        if is_valid(xi, yi):
            S1  -= 1;  Sx  -= xi;  Sy  -= yi
            Sxx -= xi*xi; Syy -= yi*yi; Sxy -= xi*yi

    def pearson():
        if S1 < 2:
            return float('nan')
        num = S1 * Sxy - Sx * Sy
        den_sq = (S1 * Sxx - Sx**2) * (S1 * Syy - Sy**2)
        if den_sq <= 0:
            return float('nan')  # constant series
        return num / math.sqrt(den_sq)

    for t in range(n):
        add(x[t], y[t])
        if t >= W:
            remove(x[t - W], y[t - W])
        if t >= W - 1:
            result.append(pearson())

    return result
```

---

## Numerical Stability

The one-pass formula `S1*Sxy - Sx*Sy` can suffer from **catastrophic cancellation** for large values with small variance. For production use, prefer a two-pass or compensated approach:

```python
def stable_pearson(xs, ys):
    """Two-pass Pearson on a small list."""
    n = len(xs)
    if n < 2:
        return float('nan')
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(xs, ys))
    vx  = sum((xi - mx)**2 for xi in xs)
    vy  = sum((yi - my)**2 for yi in ys)
    den = math.sqrt(vx * vy)
    return cov / den if den > 0 else float('nan')
```

For very large windows, consider using `numpy` or `pandas` which implement numerically stable rolling correlation.

---

## NaN Handling Strategies

| Strategy | When to use |
|---|---|
| Skip pair if either is NaN | Default — most common in finance |
| Skip window if ANY NaN | Stricter — guarantees full-data windows |
| Interpolate NaN before | When data is sparse but smooth |
| Return NaN if < min_periods valid pairs | Pandas `min_periods` parameter |

---

## Pandas Equivalent

```python
import pandas as pd

corr = pd.Series(x).rolling(W, min_periods=2).corr(pd.Series(y))
```

Understanding the underlying algorithm makes it possible to replicate this in environments without pandas (e.g., C++, SQL, streaming systems).

---

## Finance Context

Rolling correlation between two assets is used for:
- **Pairs trading**: detect regime changes in correlation
- **Factor attribution**: how correlated is the portfolio to a factor over time?
- **Correlation breakdown detection**: identify when historically stable correlations collapse (e.g., during market stress)

---

## Related Problems

| Problem | Note |
|---|---|
| Rolling Information Coefficient at Scale | Correlation between factor and returns |
| Online EWMA Mean and Variance | Exponential weighting alternative |
| Cross-Sectional Rank Transform | Pre-processing step for Spearman correlation |
