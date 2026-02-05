---
layout: simple
title: "Ternary Search - Finding Extrema of Unimodal Functions"
permalink: /problem_soulutions/sorting_and_searching/ternary_search_analysis
difficulty: Medium
tags: [ternary-search, binary-search, optimization, unimodal-functions]
---

# Ternary Search

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Key Technique** | Divide and Conquer on Unimodal Functions |
| **Time Complexity** | O(log n) or O(log((R-L)/epsilon)) |

### What is a Unimodal Function?

A **unimodal function** is a function that has exactly one local extremum (maximum or minimum) in a given interval:

- **Unimodal with maximum:** Function strictly increases, reaches peak, then strictly decreases
- **Unimodal with minimum:** Function strictly decreases, reaches trough, then strictly increases

```
Maximum Case:           Minimum Case:
      *                       \     /
     / \                       \   /
    /   \                       \ /
   /     \                       *
```

### Learning Goals

After studying this topic, you will be able to:
- [ ] Identify unimodal functions and determine when ternary search applies
- [ ] Implement ternary search for both integer and floating-point domains
- [ ] Choose between ternary search and binary search on derivative
- [ ] Apply search-on-answer technique to optimization problems

---

## Problem Statement

**Problem:** Given a unimodal function f(x) defined on interval [L, R], find the value x that maximizes (or minimizes) f(x).

**Input:**
- Function f(x) that can be evaluated at any point
- Search bounds L and R
- Required precision epsilon (for floating-point) or exact answer (for integers)

**Output:**
- The value x* where f(x*) is maximum/minimum
- Optionally, the optimal value f(x*)

**Constraints:**
- Function must be unimodal in [L, R]
- For integers: L, R can be up to 10^18
- For floats: typically need precision of 10^-9

### Example

```
Function: f(x) = -(x-3)^2 + 10  (parabola with maximum at x=3)
Interval: [0, 6]

Output: x* = 3, f(x*) = 10
```

**Explanation:** The function increases from x=0 to x=3, then decreases from x=3 to x=6.

---

## Intuition: How to Think About This Problem

### Comparing to Binary Search

| Aspect | Binary Search | Ternary Search |
|--------|---------------|----------------|
| **Problem Type** | Find target in sorted array | Find extremum of unimodal function |
| **Decision Criterion** | Compare with target | Compare two probe points |
| **Elimination** | Half the search space | One-third of search space |
| **Convergence** | O(log2 n) | O(log1.5 n) ~ O(1.71 log2 n) |

### The Key Insight

> **Core Idea:** In a unimodal function, if we probe two points m1 < m2, we can eliminate one-third of the search space based on which point has a better value.

**For finding maximum:**
- If f(m1) < f(m2): maximum is in [m1, R] - discard [L, m1)
- If f(m1) > f(m2): maximum is in [L, m2] - discard (m2, R]
- If f(m1) = f(m2): maximum is in [m1, m2] - discard both ends

### Why This Works

```
Case: f(m1) < f(m2) when finding MAXIMUM

    Peak somewhere here
          v
          *
         /|\
        / | \
       /  |  \
      /   |   \
   --m1---+---m2--
     ^         ^
   lower     higher

Since m2 > m1 and f(m2) > f(m1), the peak must be to the RIGHT of m1.
Why? If peak were left of m1, then m1 would be in the decreasing region,
and since m2 is further right, f(m2) < f(m1). Contradiction!
```

---

## Dry Run: Finding Peak

### Example Function: f(x) = -(x-5)^2 + 25 on [0, 10]

This parabola has maximum at x=5 with f(5)=25.

```
Initial: L=0, R=10

Iteration 1:
  m1 = L + (R-L)/3 = 0 + 10/3 = 3.33
  m2 = R - (R-L)/3 = 10 - 10/3 = 6.67
  f(m1) = -(3.33-5)^2 + 25 = 22.21
  f(m2) = -(6.67-5)^2 + 25 = 22.21
  f(m1) = f(m2), but let's use f(m1) < f(m2) logic (they're close)
  Actually f(m1) ~ f(m2), narrow from both sides
  New: L=3.33, R=6.67

Iteration 2:
  m1 = 3.33 + (6.67-3.33)/3 = 4.44
  m2 = 6.67 - (6.67-3.33)/3 = 5.56
  f(m1) = -(4.44-5)^2 + 25 = 24.69
  f(m2) = -(5.56-5)^2 + 25 = 24.69
  New: L=4.44, R=5.56

Iteration 3:
  m1 = 4.44 + 0.37 = 4.81
  m2 = 5.56 - 0.37 = 5.19
  f(m1) = 24.96
  f(m2) = 24.96
  New: L=4.81, R=5.19

... continue until |R - L| < epsilon
Final answer: x* ~ 5.0
```

### Visual Progress

```
Iteration 0: [===================] L=0, R=10
Iteration 1:    [=========]        L=3.33, R=6.67
Iteration 2:      [===]            L=4.44, R=5.56
Iteration 3:       [=]             L=4.81, R=5.19
                    *              x* = 5.0
```

---

## Solution: Integer Domain

### Algorithm

1. Set search bounds [lo, hi]
2. While hi - lo > 2:
   - Calculate m1 = lo + (hi - lo) / 3
   - Calculate m2 = hi - (hi - lo) / 3
   - Compare f(m1) and f(m2)
   - Narrow search space accordingly
3. Check remaining candidates and return best

### Code (Python)

```python
def ternary_search_max_int(lo: int, hi: int, f) -> int:
  """
  Find x in [lo, hi] that maximizes f(x).

  Time: O(log(hi - lo)) function evaluations
  Space: O(1)
  """
  while hi - lo > 2:
    m1 = lo + (hi - lo) // 3
    m2 = hi - (hi - lo) // 3

    if f(m1) < f(m2):
      lo = m1  # Discard left third
    else:
      hi = m2  # Discard right third

  # Check remaining candidates (at most 3)
  best_x = lo
  best_val = f(lo)
  for x in range(lo + 1, hi + 1):
    val = f(x)
    if val > best_val:
      best_val = val
      best_x = x

  return best_x


def ternary_search_min_int(lo: int, hi: int, f) -> int:
  """Find x in [lo, hi] that minimizes f(x)."""
  while hi - lo > 2:
    m1 = lo + (hi - lo) // 3
    m2 = hi - (hi - lo) // 3

    if f(m1) > f(m2):
      lo = m1  # Discard left third
    else:
      hi = m2  # Discard right third

  best_x = lo
  best_val = f(lo)
  for x in range(lo + 1, hi + 1):
    val = f(x)
    if val < best_val:
      best_val = val
      best_x = x

  return best_x
```

---

## Solution: Floating-Point Domain

### Algorithm

1. Set search bounds [lo, hi] and precision epsilon
2. While hi - lo > epsilon:
   - Calculate m1 = lo + (hi - lo) / 3
   - Calculate m2 = hi - (hi - lo) / 3
   - Compare and narrow
3. Return midpoint (lo + hi) / 2

### Code (Python)

```python
def ternary_search_max_float(lo: float, hi: float, f,
               eps: float = 1e-9) -> float:
  """
  Find x in [lo, hi] that maximizes f(x).

  Time: O(log((hi-lo)/eps)) function evaluations
  Space: O(1)
  """
  while hi - lo > eps:
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3

    if f(m1) < f(m2):
      lo = m1
    else:
      hi = m2

  return (lo + hi) / 2


def ternary_search_min_float(lo: float, hi: float, f,
               eps: float = 1e-9) -> float:
  """Find x in [lo, hi] that minimizes f(x)."""
  while hi - lo > eps:
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3

    if f(m1) > f(m2):
      lo = m1
    else:
      hi = m2

  return (lo + hi) / 2


# Alternative: Fixed iterations (more robust for floating-point)
def ternary_search_max_iterations(lo: float, hi: float, f,
                 iterations: int = 200) -> float:
  """Fixed iteration version - avoids floating-point comparison issues."""
  for _ in range(iterations):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3

    if f(m1) < f(m2):
      lo = m1
    else:
      hi = m2

  return (lo + hi) / 2
```

---

## Common Mistakes

### Mistake 1: Wrong Termination Condition (Integers)

```python
# WRONG - May infinite loop or miss candidates
while lo < hi:
  m1 = lo + (hi - lo) // 3
  m2 = hi - (hi - lo) // 3
  # When hi - lo = 2, m1 = m2, stuck!

# CORRECT - Stop when range is small enough
while hi - lo > 2:
  # ...
# Then check remaining candidates manually
```

**Problem:** When `hi - lo <= 2`, the trisection points may overlap.
**Fix:** Use `hi - lo > 2` and enumerate remaining candidates.

### Mistake 2: Integer Overflow in Midpoint Calculation

### Mistake 3: Floating-Point Precision Issues

```python
# WRONG - May never terminate due to floating-point errors
while lo != hi:
  # ...

# CORRECT - Use epsilon or fixed iterations
while hi - lo > 1e-9:
  # ...
# OR
for _ in range(200):
  # ...
```

### Mistake 4: Wrong Comparison Direction

```python
# For MAXIMUM: eliminate the LOWER value's side
if f(m1) < f(m2):
  lo = m1  # Correct: peak is toward higher value

# For MINIMUM: eliminate the HIGHER value's side
if f(m1) > f(m2):
  lo = m1  # Correct: trough is toward lower value
```

---

## Edge Cases

| Case | Description | Handling |
|------|-------------|----------|
| Single point | `lo == hi` | Return `lo` directly |
| Two points | `hi - lo == 1` | Compare both, return better |
| Extremum at boundary | Peak/trough at `lo` or `hi` | Algorithm handles correctly |
| Flat region | `f(m1) == f(m2)` | Any consistent rule works |
| Very large range | `hi - lo > 10^18` | Use proper integer arithmetic |
| Steep function | Large value differences | No special handling needed |
| Flat function | `f(x) = constant` | Returns any valid point |

---

## When to Use This Pattern

### Use Ternary Search When:
- Function is strictly unimodal (one peak or one trough)
- You need to find the extremum, not a specific value
- Function evaluations are expensive (minimize calls)
- Binary search is not directly applicable

### Use Binary Search Instead When:
- Function is monotonic (no extremum in interior)
- You can binary search on the derivative
- Problem is "search on answer" type with monotonic check function

### Decision Flowchart

```
Is function monotonic?
    |
    +-- Yes --> Use Binary Search
    |
    +-- No --> Is function unimodal?
                   |
                   +-- Yes --> Use Ternary Search
                   |
                   +-- No --> Different approach needed
                              (possibly divide into unimodal segments)
```

---

## Comparison: Ternary Search vs Binary Search on Derivative

### The Two Approaches

| Aspect | Ternary Search | Binary Search on Derivative |
|--------|----------------|----------------------------|
| **Evaluations/iter** | 2 (f(m1), f(m2)) | 1 or 2 (f'(m) or f(m-1), f(m+1)) |
| **Space eliminated** | 1/3 per iteration | 1/2 per iteration |
| **Total evaluations** | ~2 log1.5(n) | ~2 log2(n) |
| **Iterations** | ~1.71 log2(n) | ~log2(n) |
| **When applicable** | Any unimodal function | When derivative sign computable |

### Binary Search on Derivative (Integer Example)

For integers, "derivative" means: is f(x) < f(x+1)? (increasing at x)

```python
def binary_search_peak(lo: int, hi: int, f) -> int:
  """
  Find peak of unimodal function using binary search.
  Checks if function is increasing at midpoint.
  """
  while lo < hi:
    mid = lo + (hi - lo) // 2
    if f(mid) < f(mid + 1):
      # Still increasing, peak is to the right
      lo = mid + 1
    else:
      # Decreasing or at peak, peak is at mid or left
      hi = mid
  return lo
```

### Which to Choose?

- **Ternary Search:** Simpler to implement, works for any unimodal function
- **Binary Search on Derivative:** Fewer function evaluations overall, but requires checking derivative
- **Practical Note:** For most problems, the difference is negligible; choose based on clarity

---

## Related CSES Problems

### Problems Using Binary Search on Answer

| Problem | Description | Connection |
|---------|-------------|------------|
| [Factory Machines](https://cses.fi/problemset/task/1620) | Minimize time to produce t products | Binary search on time; check function is monotonic |
| [Array Division](https://cses.fi/problemset/task/1085) | Minimize maximum subarray sum | Binary search on answer |
| [Stick Lengths](https://cses.fi/problemset/task/1074) | Minimize total modification cost | Optimal point is median (special case) |

### Factory Machines Example

```python
def factory_machines(n: int, t: int, times: list) -> int:
  """
  Find minimum time to produce t products.
  Uses binary search on answer (time), not ternary search.
  """
  def can_produce(time_limit: int) -> bool:
    """Can we produce >= t products in given time?"""
    total = sum(time_limit // machine_time for machine_time in times)
    return total >= t

  lo, hi = 0, min(times) * t

  while lo < hi:
    mid = lo + (hi - lo) // 2
    if can_produce(mid):
      hi = mid  # Try to find smaller time
    else:
      lo = mid + 1  # Need more time

  return lo
```

**Why not ternary search?** The function "products produced in time T" is monotonically increasing, not unimodal. We want the minimum T satisfying a threshold, which is binary search territory.

---

## Key Takeaways

1. **Core Idea:** Ternary search finds extrema of unimodal functions by eliminating one-third of the search space per iteration.

2. **Integer vs Float:** For integers, stop when range is small (2-3 elements) and enumerate. For floats, use epsilon or fixed iterations.

3. **Comparison Direction:** For maximum, move toward higher values. For minimum, move toward lower values.

4. **Alternative:** Binary search on derivative is often more efficient but requires computing whether function is increasing/decreasing at a point.

5. **Application:** Many CSES problems use "binary search on answer" (monotonic check), not ternary search (unimodal optimization).

---

## Complexity Analysis

| Version | Time Complexity | Space Complexity |
|---------|-----------------|------------------|
| Integer | O(log(R-L)) evals | O(1) |
| Float (epsilon) | O(log((R-L)/eps)) evals | O(1) |
| Float (iterations) | O(iterations) evals | O(1) |

Each iteration reduces search space by factor of 2/3, so:
- After k iterations: range = (2/3)^k * (R-L)
- Iterations needed for precision eps: k = log1.5((R-L)/eps)

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why ternary search works on unimodal functions
- [ ] Implement both integer and floating-point versions from memory
- [ ] Identify whether a problem needs ternary search or binary search
- [ ] Handle edge cases (small ranges, boundary extrema)
- [ ] Choose appropriate termination conditions
