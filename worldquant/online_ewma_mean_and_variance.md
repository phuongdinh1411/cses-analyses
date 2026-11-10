---
layout: simple
title: "Online EWMA Mean and Variance"
permalink: /worldquant/online_ewma_mean_and_variance
difficulty: Medium
tags: [statistics, streaming, ewma, worldquant, finance]
---

# Online EWMA Mean and Variance

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Statistics / Streaming / Signal Processing |
| **Key Technique** | Exponentially Weighted Moving Average — Welford-style online update |

### Learning Goals
- [ ] Implement EWMA mean with decay factor alpha in O(1) per update
- [ ] Implement EWMA variance using the online update formula
- [ ] Understand the difference between EWMA and simple rolling average
- [ ] Handle the warm-up period and bias correction

---

## Problem Statement

Given a stream of numbers `x_1, x_2, ..., x_n` and a smoothing parameter `alpha` (0 < alpha < 1), compute the **EWMA mean** and **EWMA variance** after each new observation.

The EWMA (Exponentially Weighted Moving Average) assigns **exponentially decreasing weights** to older observations:

```
mean_t = alpha * x_t + (1 - alpha) * mean_{t-1}
```

For **EWMA variance** (using Welford-style update):
```
delta  = x_t - mean_{t-1}
mean_t = mean_{t-1} + alpha * delta
var_t  = (1 - alpha) * (var_{t-1} + alpha * delta^2)
```

**Input:**
- A list `stream` of `n` floats
- A float `alpha` ∈ (0, 1) — the smoothing factor (higher = more weight to recent values)

**Output:**
- Two lists of length `n`: EWMA means and EWMA variances at each step

**Constraints:**
- `1 <= n <= 10^6`
- `0 < alpha < 1`
- `-10^9 <= stream[i] <= 10^9`

---

## Examples

### Example 1
```
Input:  stream = [2.0, 4.0, 6.0, 8.0], alpha = 0.5
Output:
  means:     [2.0, 3.0, 4.5, 6.25]
  variances: [0.0, 0.5, 1.375, 2.359]

Step 1: mean=2.0 (first value), var=0.0
Step 2: delta=4-2=2, mean=2+0.5*2=3.0, var=0.5*(0+0.5*4)=1.0
  Actually: var = (1-0.5)*(0 + 0.5*2^2) = 0.5*(0 + 2) = 1.0
Step 3: delta=6-3=3, mean=3+0.5*3=4.5, var=0.5*(1+0.5*9)=0.5*5.5=2.75
Step 4: delta=8-4.5=3.5, mean=4.5+0.5*3.5=6.25, var=0.5*(2.75+0.5*12.25)=0.5*8.875=4.4375
```

### Example 2 — High alpha (fast decay)
```
Input:  stream = [1.0, 100.0, 1.0], alpha = 0.9
Output:
  means: [1.0, 90.1, 9.91]  (heavily weighted toward most recent)
```

---

## Approach: Welford-Style Online Update

### Initialisation
- Set `mean = stream[0]`, `var = 0.0`

### Update (for each new value x)
```
delta   = x - mean
mean    += alpha * delta
var      = (1 - alpha) * (var + alpha * delta^2)
std      = sqrt(var)
```

This is a single-pass O(1) update — no need to store the window.

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n) total, O(1) per update |
| **Space** | O(1) — only two scalars maintained |

---

## Implementation

```python
import math

def online_ewma(stream: list[float], alpha: float):
    if not stream:
        return [], []

    means = []
    variances = []

    mean = stream[0]
    var = 0.0
    means.append(mean)
    variances.append(var)

    for x in stream[1:]:
        delta = x - mean
        mean  = mean + alpha * delta
        var   = (1 - alpha) * (var + alpha * delta ** 2)
        means.append(mean)
        variances.append(var)

    return means, variances


def online_ewma_std(stream: list[float], alpha: float):
    means, variances = online_ewma(stream, alpha)
    stds = [math.sqrt(v) for v in variances]
    return means, stds
```

---

## Alpha — The Smoothing Factor

`alpha` is often expressed in terms of a **half-life** or **span**:

| Parameterisation | Formula |
|---|---|
| Given span `s` | `alpha = 2 / (s + 1)` |
| Given half-life `h` | `alpha = 1 - exp(-ln(2) / h)` |
| Given com (center of mass) `c` | `alpha = 1 / (1 + c)` |

```python
def alpha_from_halflife(halflife: float) -> float:
    return 1 - math.exp(-math.log(2) / halflife)

def alpha_from_span(span: float) -> float:
    return 2 / (span + 1)
```

---

## Bias Correction (Pandas-style)

Early estimates are biased because the weight hasn't "summed to 1" yet. Pandas `ewm(adjust=True)` corrects this:

```
effective_weight_t = sum of alpha*(1-alpha)^k for k=0..t-1
mean_corrected_t   = raw_ewma_t / effective_weight_t
```

For most production use with `n >> 1/alpha`, the bias is negligible.

---

## Finance Context

EWMA is used for:
- **Volatility estimation**: `ewma_std(returns, alpha)` gives a rolling vol estimate that reacts faster to recent shocks than a simple window
- **Signal smoothing**: smooth noisy factor values before computing IC
- **Risk models**: JP Morgan's RiskMetrics model uses EWMA with `alpha = 0.94` for daily returns

---

## Comparison: Simple Rolling vs EWMA

| Property | Simple Rolling (window W) | EWMA (alpha) |
|---|---|---|
| Memory | O(W) | O(1) |
| Reacts to outliers | Equally until window | Decays — recent weighted more |
| Discontinuity | Yes (when old value leaves window) | No — smooth |
| Tuning parameter | W | alpha (or half-life) |

---

## Related Problems

| Problem | Note |
|---|---|
| Rolling Correlation With Missing Values | Uses similar running sums |
| Rolling Information Coefficient at Scale | Uses rolling mean/std |
| Online EWMA can replace rolling window | For signal generation at lower memory cost |
