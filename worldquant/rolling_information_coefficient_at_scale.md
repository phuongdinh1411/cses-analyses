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

### In 60 seconds
- **Pattern:** Per-date correlation + rolling mean
- **Key insight:** Standard IC is the cross-sectional correlation per date, averaged over the window; pooling the whole W×N block also rewards market-wide co-movement.
- **Complexity:** O(T·N) time, O(W) extra space
- **Trap:** Reporting a pooled IC as if it were the standard one (Example 1: 0.5 vs 0.886).

> **Say this in the interview:** "IC measures ranking skill each day, so I compute it per date and smooth it, not pool across time."

---

## Problem Statement

The **Information Coefficient (IC)** at time `t` is the Pearson (or Spearman) correlation between a vector of factor predictions and a vector of realised forward returns across all assets.

Given:
- `factors`: a 2D array of shape `(T, N)` — factor values for `N` assets over `T` time steps
- `returns`: a 2D array of shape `(T, N)` — forward returns for `N` assets over `T` time steps
- `window`: rolling window size `W`

For each time step `t >= W - 1`, compute the **rolling IC** over the past `W` time steps. There are two definitions; be explicit about which one you implement:

```
Standard (per-date):  IC_t = corr(factors[t], returns[t])               # across N assets
                      rolling_IC[t] = mean(IC_{t-W+1} .. IC_t)
Pooled (this page's   rolling_IC[t] = corr(factors[t-W+1:t+1].flatten(),
 streaming exercise):                     returns[t-W+1:t+1].flatten())
```

The standard definition is what research teams report: it measures cross-sectional ranking skill each day. The pooled one also rewards the factor for tracking *market-wide* moves over time, which inflates it (see Example 1).

Return an array of length `T - W + 1`.

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

Standard: IC_0 = corr([1,2,3], [0.1,0.3,0.2]) = 0.5
          IC_1 = corr([4,5,6], [0.5,0.4,0.6]) = 0.5
          rolling_IC = mean(0.5, 0.5) = 0.5          → Output: [0.5]

Pooled:   corr([1,2,3,4,5,6], [0.1,0.3,0.2,0.5,0.4,0.6]) ≈ 0.886  → Output: [0.886]

The pooled value is higher only because day 2 has both higher factors
and higher returns overall — not because the ranking within each day is better.
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

## Approach (standard definition): per-date IC, then a rolling mean

1. For each date, compute the cross-sectional correlation over valid pairs: O(N).
2. Keep a running sum of the last `W` daily ICs (skipping NaN days) to get the rolling mean: O(1) per step.

Total O(T × N) time, O(W) extra space.

```python
import math
from collections import deque

def daily_ic(f_row: list[float], r_row: list[float]) -> float:
    pairs = [(f, r) for f, r in zip(f_row, r_row) if not (math.isnan(f) or math.isnan(r))]
    m = len(pairs)
    if m < 2:
        return float("nan")
    mf = sum(f for f, _ in pairs) / m
    mr = sum(r for _, r in pairs) / m
    cov = sum((f - mf) * (r - mr) for f, r in pairs)
    vf = sum((f - mf) ** 2 for f, _ in pairs)
    vr = sum((r - mr) ** 2 for _, r in pairs)
    return cov / math.sqrt(vf * vr) if vf > 0 and vr > 0 else float("nan")

def rolling_mean_ic(factors: list[list[float]], returns: list[list[float]], window: int) -> list[float]:
    ics: deque[float] = deque()
    total, valid, out = 0.0, 0, []
    for f_row, r_row in zip(factors, returns):
        ic = daily_ic(f_row, r_row)
        ics.append(ic)
        if not math.isnan(ic):
            total += ic; valid += 1
        if len(ics) > window:
            old = ics.popleft()
            if not math.isnan(old):
                total -= old; valid -= 1
        if len(ics) == window:
            out.append(total / valid if valid else float("nan"))
    return out
```

## Approach (pooled definition): sliding window with running sums

For each window of W rows, maintain running sums:
- `S_x`, `S_y`, `S_xx`, `S_yy`, `S_xy`, `count` (excluding NaN pairs)

When the window slides, **subtract the leaving row's contribution** and **add the entering row's contribution**.

The numerics need the same two guards as [Rolling Correlation](/worldquant/rolling_correlation_with_missing_values#numerical-stability). Raw sums crash `math.sqrt` on a variance that rounds to −2e-14 (`rolling_ic([[1,2,3],[1,2,3]], [[0.3]*3]*2, 2)`) and return junk such as 1.07 for constant windows. So the code centres on the first valid pair and detects constant windows exactly.

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
    result = []

    # Sliding window of rows
    win_f = deque()  # stores rows of factors
    win_r = deque()  # stores rows of returns

    def valid_pairs(f_row, r_row):
        return ((f, r) for f, r in zip(f_row, r_row) if not (math.isnan(f) or math.isnan(r)))

    # Centre on the first valid pair: correlation is shift-invariant, and centred
    # sums avoid catastrophic cancellation in count*S_xx - S_x**2
    cf, cr = next((p for f_row, r_row in zip(factors, returns)
                   for p in valid_pairs(f_row, r_row)), (0.0, 0.0))

    # Running sums (over valid, centred pairs only)
    S_x = S_y = S_xx = S_yy = S_xy = 0.0
    count = 0
    # Trailing run of equal factor (return) values in arrival order; a run covering
    # all `count` pairs means a constant window: IC is NaN, not rounding noise
    run_f = run_r = 0
    last_f = last_r = math.nan

    def add_row(f_row, r_row):
        nonlocal S_x, S_y, S_xx, S_yy, S_xy, count, run_f, run_r, last_f, last_r
        for f, r in valid_pairs(f_row, r_row):
            run_f = run_f + 1 if f == last_f else 1
            run_r = run_r + 1 if r == last_r else 1
            last_f, last_r = f, r
            f, r = f - cf, r - cr
            S_x  += f;  S_y  += r
            S_xx += f*f; S_yy += r*r; S_xy += f*r
            count += 1

    def remove_row(f_row, r_row):
        nonlocal S_x, S_y, S_xx, S_yy, S_xy, count
        for f, r in valid_pairs(f_row, r_row):
            f, r = f - cf, r - cr
            S_x  -= f;  S_y  -= r
            S_xx -= f*f; S_yy -= r*r; S_xy -= f*r
            count -= 1

    def pearson():
        if count < 2 or run_f >= count or run_r >= count:
            return float('nan')
        var_f = count * S_xx - S_x**2   # computed separately: rounding can make
        var_r = count * S_yy - S_y**2   # either one slightly negative
        if var_f <= 0 or var_r <= 0:
            return float('nan')
        return max(-1.0, min(1.0, (count * S_xy - S_x * S_y) / math.sqrt(var_f * var_r)))

    for f_row, r_row in zip(factors, returns):
        add_row(f_row, r_row)
        win_f.append(f_row)
        win_r.append(r_row)

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
import math
from scipy.stats import rankdata

def spearman_ic_row(f_row: list[float], r_row: list[float]) -> float:
    valid = [(f, r) for f, r in zip(f_row, r_row)
             if not math.isnan(f) and not math.isnan(r)]
    if len(valid) < 2:
        return float('nan')
    f_vals, r_vals = zip(*valid)
    return daily_ic(list(rankdata(f_vals)), list(rankdata(r_vals)))   # Pearson of ranks
```

With the standard definition, ranks are computed once per date: O(T × N log N) total, then the same O(1) rolling mean. A *pooled* rolling Spearman must re-rank all `W × N` values in every window, O(T × W·N log(W·N)), unless you use an order-statistics structure.

---

## IC Interpretation

| IC value | Meaning |
|---|---|
| 1.0 | Perfect positive prediction |
| 0.0 | No predictive power |
| -1.0 | Perfect inverse prediction |
| > 0.05 | Rule of thumb: useful for a daily cross-sectional IC |
| > 0.10 | Rule of thumb: very strong (check for look-ahead bias) |

These thresholds depend on horizon, universe breadth, and turnover; a small but *stable* IC across many assets can be valuable.

---

## Related Problems

| Problem | Note |
|---|---|
| Cross-Sectional Rank Transform with Ties and NaN | Input to Spearman IC |
| Rolling Correlation With Missing Values | Pairwise asset correlation version |
| Online EWMA Mean and Variance | Exponential weighting alternative to rolling window |
