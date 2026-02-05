---
layout: simple
title: "Factory Machines - Binary Search on Answer"
permalink: /problem_soulutions/sorting_and_searching/factory_machines_analysis
difficulty: Medium
tags: [binary-search, optimization, monotonic-function]
prerequisites: []
---

# Factory Machines

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Binary Search on Answer |
| **CSES Link** | [Factory Machines](https://cses.fi/problemset/task/1620) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when to apply "binary search on the answer" pattern
- [ ] Implement a feasibility check function for optimization problems
- [ ] Handle integer overflow when computing products in the check function
- [ ] Set correct search bounds for binary search problems

---

## Problem Statement

**Problem:** A factory has n machines. Each machine i produces one product in t[i] seconds. All machines can work in parallel. Find the minimum time needed to produce exactly k products.

**Input:**
- Line 1: Two integers n and t (number of machines and products needed)
- Line 2: n integers describing each machine's production time

**Output:**
- The minimum time to produce t products

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= t <= 10^9
- 1 <= k[i] <= 10^9

### Example

```
Input:
3 7
3 2 5

Output:
8
```

**Explanation:**
- Machine 1 (time=3): In 8 seconds, produces 8/3 = 2 products
- Machine 2 (time=2): In 8 seconds, produces 8/2 = 4 products
- Machine 3 (time=5): In 8 seconds, produces 8/5 = 1 product
- Total: 2 + 4 + 1 = 7 products (exactly what we need)

In 7 seconds: 7/3 + 7/2 + 7/5 = 2 + 3 + 1 = 6 products (not enough)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** We need to minimize time T such that all machines together produce at least t products. Given a time T, can we quickly check if it is sufficient?

Yes! If we fix a time T, machine i produces floor(T / k[i]) products. The total is the sum across all machines. This check is O(n).

### Breaking Down the Problem

1. **What are we looking for?** The minimum time T to produce t products.
2. **What information do we have?** Each machine's production time and target count.
3. **What's the relationship?** More time = more products (monotonic!).

### Why Binary Search Works

The key insight is **monotonicity**:
- If time T is enough to produce t products, then T+1 is also enough.
- If time T is NOT enough, then T-1 is also NOT enough.

This "threshold" property is exactly what binary search exploits. We search for the smallest T where the check returns true.

```
Time:     1   2   3   4   5   6   7   8   9   10  ...
Enough?   N   N   N   N   N   N   N   Y   Y   Y   ...
                                      ^
                              Answer: First "Yes"
```

---

## Solution 1: Brute Force (Linear Search)

### Idea

Try every possible time from 1 upward until we find one that produces enough products.

### Algorithm

1. Start with time = 1
2. Calculate total products produced at this time
3. If total >= target, return time
4. Otherwise, increment time and repeat

### Code

```python
def solve_brute_force(machines, target):
  """
  Brute force: try each time linearly.

  Time: O(answer * n)
  Space: O(1)
  """
  time = 1
  while True:
    total = sum(time // m for m in machines)
    if total >= target:
      return time
    time += 1
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(answer * n) | Linear search up to answer, O(n) check each |
| Space | O(1) | No extra space |

### Why This Is Too Slow

With t up to 10^9 and machine times up to 10^9, the answer could be as large as 10^18. Linear search is infeasible.

---

## Solution 2: Binary Search on Answer

### Key Insight

> **The Trick:** Instead of searching linearly, binary search on the answer space. For each candidate time, check in O(n) if it suffices.

### Feasibility Check Function

```
can_produce(T) = sum(T // k[i] for all i) >= target
```

This function is monotonic: once true, stays true for larger T.

### Search Bounds

| Bound | Value | Reason |
|-------|-------|--------|
| `lo` | 1 | Minimum possible time |
| `hi` | min(machines) * target | Slowest case: only fastest machine works |

Note: A tighter upper bound is `min(machines) * target` since the fastest machine alone could produce all products.

### Algorithm

1. Set lo = 1, hi = min(machines) * target
2. While lo < hi:
   - mid = (lo + hi) / 2
   - If can_produce(mid): hi = mid (search left for smaller time)
   - Else: lo = mid + 1 (need more time)
3. Return lo

### Dry Run Example

Input: machines = [3, 2, 5], target = 7

```
Initial: lo = 1, hi = 2 * 7 = 14

Iteration 1:
  mid = (1 + 14) / 2 = 7
  Products at time 7: 7/3 + 7/2 + 7/5 = 2 + 3 + 1 = 6
  6 < 7, NOT enough
  lo = 8

Iteration 2:
  mid = (8 + 14) / 2 = 11
  Products at time 11: 11/3 + 11/2 + 11/5 = 3 + 5 + 2 = 10
  10 >= 7, enough!
  hi = 11

Iteration 3:
  mid = (8 + 11) / 2 = 9
  Products at time 9: 9/3 + 9/2 + 9/5 = 3 + 4 + 1 = 8
  8 >= 7, enough!
  hi = 9

Iteration 4:
  mid = (8 + 9) / 2 = 8
  Products at time 8: 8/3 + 8/2 + 8/5 = 2 + 4 + 1 = 7
  7 >= 7, enough!
  hi = 8

Iteration 5:
  lo = 8, hi = 8
  Loop ends

Answer: 8
```

### Visual Diagram

```
Time:        1   2   3   4   5   6   7   8   9  10  11  12  13  14
Products:    0   1   2   3   4   5   6   7   8   9  10  11  12  13
                                         ^
                                     Answer: 8
                                   First time >= 7 products

Binary search path:
  [1 -------------------- 14]
              7 (6 products, need more)
  [8 ----------- 14]
         11 (10 products, try less)
  [8 ---- 11]
      9 (8 products, try less)
  [8 - 9]
    8 (7 products, try less)
  [8]
   Done! Answer = 8
```

### Code (Python)

```python
def solve(n, target, machines):
  """
  Binary search on answer.

  Time: O(n log(answer))
  Space: O(1)
  """
  def can_produce(time):
    """Check if we can produce target products in given time."""
    total = 0
    for m in machines:
      total += time // m
      # Early exit optimization
      if total >= target:
        return True
    return False

  lo = 1
  hi = min(machines) * target

  while lo < hi:
    mid = (lo + hi) // 2
    if can_produce(mid):
      hi = mid
    else:
      lo = mid + 1

  return lo


# Read input and solve
n, t = map(int, input().split())
machines = list(map(int, input().split()))
print(solve(n, t, machines))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log(answer)) | log(answer) iterations, O(n) check each |
| Space | O(n) | Only store machine times |

---

## Common Mistakes

### Mistake 1: Integer Overflow in Check Function

**Problem:** If time is large and machines are fast, total can overflow.

**Fix:** Early exit when total >= target, or check for overflow:

### Mistake 2: Wrong Upper Bound

**Problem:** If machines are slow, we need more time than just target.

**Fix:** Use `min(machines) * target` - the fastest machine alone takes this long.

### Mistake 3: Using Wrong Mid Calculation

### Mistake 4: Off-by-One in Binary Search

**Fix:** Use the `lo < hi` pattern with `hi = mid` and `lo = mid + 1`.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single machine | n=1, t=5, [3] | 15 | 5 * 3 = 15 |
| Target is 1 | n=3, t=1, [5,3,7] | 3 | Fastest machine time |
| All same speed | n=3, t=6, [2,2,2] | 4 | 4/2 * 3 = 6 |
| Large values | n=1, t=10^9, [10^9] | 10^18 | Maximum possible answer |
| Very fast machine | n=2, t=10, [1,1000] | 5 | Fast machine dominates |

---

## When to Use This Pattern

### Use Binary Search on Answer When:
- You need to minimize/maximize a value
- There is a monotonic feasibility function
- The check function is efficient (O(n) or O(n log n))
- Linear search would be too slow

### Pattern Recognition Checklist:
- [ ] "Find minimum time/cost/size such that..." -> Consider binary search
- [ ] Can you write a yes/no check for a given answer? -> Binary search candidate
- [ ] Is the check monotonic (if X works, X+1 works)? -> Binary search applies

### Template for Binary Search on Answer

```python
def binary_search_on_answer(lo, hi, is_feasible):
  """
  Find minimum value where is_feasible returns True.
  Assumes: is_feasible is monotonic (False...False, True...True)
  """
  while lo < hi:
    mid = (lo + hi) // 2
    if is_feasible(mid):
      hi = mid
    else:
      lo = mid + 1
  return lo
```

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Apartments](https://cses.fi/problemset/task/1084) | Basic sorting and searching |

### Similar Difficulty (Binary Search on Answer)

| Problem | Key Similarity |
|---------|----------------|
| [Array Division](https://cses.fi/problemset/task/1085) | Binary search on max subarray sum |
| [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Same pattern: minimize rate to finish in time |
| [Capacity To Ship Packages](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Minimize capacity to ship in D days |
| [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Binary search on answer |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Minimize Max Distance to Gas Station](https://leetcode.com/problems/minimize-max-distance-to-gas-station/) | Binary search with floating point |
| [Nth Magical Number](https://leetcode.com/problems/nth-magical-number/) | Binary search with LCM |

---

## Key Takeaways

1. **The Core Idea:** Transform "minimize X" into "find smallest X where check(X) is true"
2. **Time Optimization:** O(answer) -> O(log(answer)) by exploiting monotonicity
3. **Common Pitfalls:** Overflow in check function, wrong bounds, off-by-one errors
4. **Pattern:** "Binary search on answer" - one of the most common CP techniques

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem in under 15 minutes
- [ ] Explain why binary search works (monotonicity)
- [ ] Handle overflow correctly in the check function
- [ ] Set appropriate bounds for the binary search
- [ ] Apply this pattern to similar problems (Koko, Capacity to Ship)
