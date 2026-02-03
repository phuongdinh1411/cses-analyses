---
layout: simple
title: "Knapsack 2 - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming_at/knapsack_2_analysis
difficulty: Medium
tags: [dp, knapsack, value-based-dp, state-inversion]
prerequisites: [knapsack_1]
---

# Knapsack 2

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [AtCoder DP Contest - Problem E](https://atcoder.jp/contests/dp/tasks/dp_e) |
| **Difficulty** | Medium |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | Value-Based DP (State Inversion) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when standard capacity-based knapsack DP is infeasible
- [ ] Apply state inversion: DP on value instead of weight
- [ ] Understand the trade-off between different DP state definitions
- [ ] Choose the right DP formulation based on constraint analysis

---

## Problem Statement

**Problem:** Given N items with weights and values, find the maximum total value that can fit in a knapsack of capacity W.

**Input:**
- Line 1: N W (number of items and knapsack capacity)
- Lines 2 to N+1: w_i v_i (weight and value of item i)

**Output:**
- Maximum possible sum of values

**Constraints:**
- 1 <= N <= 100
- 1 <= W <= 10^9 (huge!)
- 1 <= w_i <= 10^9 (huge!)
- 1 <= v_i <= 10^3 (small!)

**Critical Observation:**
| Constraint | Knapsack 1 | Knapsack 2 |
|------------|------------|------------|
| W (capacity) | <= 10^5 (small) | <= 10^9 (huge) |
| v_i (values) | <= 10^9 (large) | <= 10^3 (small) |

### Example

```
Input:
3 8
3 30
4 50
5 60

Output:
90
```

**Explanation:** Take items 1 and 3 (weights 3+5=8, values 30+60=90). This exactly fills the knapsack with maximum value.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Why can't we use the standard knapsack DP from Knapsack 1?

Standard knapsack uses `dp[i][w]` = max value using first i items with capacity w. This requires O(N * W) space/time. With W up to 10^9, this is impossible.

### The Key Insight

> **State Inversion:** When one dimension is too large, swap the DP state definition.

Instead of asking "What's the maximum value for a given weight?"
Ask: "What's the minimum weight needed to achieve a given value?"

| Standard DP | Inverted DP |
|-------------|-------------|
| `dp[v]` = max value with capacity v | `dp[v]` = min weight to achieve value v |
| Iterate over capacities (up to W) | Iterate over values (up to N * max_v) |
| Infeasible when W is huge | Feasible since sum of values <= 100 * 1000 = 10^5 |

### Why This Works

- Maximum possible total value = N * max(v_i) = 100 * 1000 = 100,000
- We can create an array of size 10^5 (feasible!)
- For each possible value v, track the minimum weight needed
- Answer: Find the largest v where min_weight[v] <= W

---

## Solution 1: Standard DP (Infeasible)

### Why It Fails

```python
# This would require O(N * W) = O(100 * 10^9) operations
# Memory: 10^9 integers = ~4GB - impossible!
dp = [[0] * (W + 1) for _ in range(N + 1)]  # Cannot allocate!
```

**Verdict:** With W up to 10^9, standard approach is not viable.

---

## Solution 2: Value-Based DP (Optimal)

### Key Insight

> **The Trick:** Since values are small (max 10^3) and N <= 100, total achievable value is at most 10^5. DP on value instead of capacity.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[v]` | Minimum weight needed to achieve exactly value v |

**In plain English:** For each possible total value, what's the lightest way to achieve it?

### State Transition

```
dp[v] = min(dp[v], dp[v - value[i]] + weight[i])
```

**Why?** To achieve value v, either:
1. Don't take item i: dp[v] stays the same
2. Take item i: Need dp[v - value[i]] weight for remaining value, plus weight[i]

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 0 | Zero value requires zero weight |
| `dp[v]` for v > 0 | INF | Initially impossible without items |

### Algorithm

1. Calculate max_value = sum of all item values
2. Initialize dp[0] = 0, dp[v] = INF for v > 0
3. For each item, update dp in reverse order (to avoid reusing items)
4. Find largest v where dp[v] <= W

### Dry Run Example

Let's trace through with `N=3, W=8, items=[(3,30), (4,50), (5,60)]`:

```
Initial:
  dp[0] = 0
  dp[1..140] = INF

After Item 1 (weight=3, value=30):
  dp[30] = min(INF, dp[0] + 3) = 3

  State: dp[0]=0, dp[30]=3, rest=INF

After Item 2 (weight=4, value=50):
  dp[80] = min(INF, dp[30] + 4) = 7   (take both)
  dp[50] = min(INF, dp[0] + 4) = 4    (take only item 2)

  State: dp[0]=0, dp[30]=3, dp[50]=4, dp[80]=7, rest=INF

After Item 3 (weight=5, value=60):
  dp[140] = min(INF, dp[80] + 5) = 12  (all three items)
  dp[110] = min(INF, dp[50] + 5) = 9   (items 2 and 3)
  dp[90]  = min(INF, dp[30] + 5) = 8   (items 1 and 3)
  dp[60]  = min(INF, dp[0] + 5) = 5    (only item 3)

Final State:
  v   |  dp[v] (min weight)
  ----|--------------------
  0   |  0
  30  |  3
  50  |  4
  60  |  5
  80  |  7
  90  |  8   <-- largest v where dp[v] <= W=8
  110 |  9   (exceeds W)
  140 |  12  (exceeds W)

Answer: 90
```

### Visual Diagram

```
Items: [(w=3,v=30), (w=4,v=50), (w=5,v=60)]  Capacity: W=8

Achievable combinations:
  Item 1 only:     w=3, v=30
  Item 2 only:     w=4, v=50
  Item 3 only:     w=5, v=60
  Items 1+2:       w=7, v=80
  Items 1+3:       w=8, v=90  <-- Best! (exactly fits)
  Items 2+3:       w=9, v=110 (exceeds capacity)
  Items 1+2+3:     w=12, v=140 (exceeds capacity)
```

### Code (Python)

```python
def solve():
    N, W = map(int, input().split())
    items = []
    for _ in range(N):
        w, v = map(int, input().split())
        items.append((w, v))

    # Maximum possible value
    max_value = sum(v for w, v in items)

    # dp[v] = minimum weight to achieve value v
    INF = float('inf')
    dp = [INF] * (max_value + 1)
    dp[0] = 0

    # Process each item
    for weight, value in items:
        # Iterate backwards to ensure each item used at most once
        for v in range(max_value, value - 1, -1):
            if dp[v - value] + weight < dp[v]:
                dp[v] = dp[v - value] + weight

    # Find maximum value achievable within capacity W
    for v in range(max_value, -1, -1):
        if dp[v] <= W:
            print(v)
            return

    print(0)

solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    long long W;
    cin >> N >> W;

    vector<long long> weight(N), value(N);
    long long max_value = 0;

    for (int i = 0; i < N; i++) {
        cin >> weight[i] >> value[i];
        max_value += value[i];
    }

    // dp[v] = minimum weight to achieve value v
    const long long INF = 1e18;
    vector<long long> dp(max_value + 1, INF);
    dp[0] = 0;

    // Process each item
    for (int i = 0; i < N; i++) {
        // Iterate backwards
        for (long long v = max_value; v >= value[i]; v--) {
            if (dp[v - value[i]] + weight[i] < dp[v]) {
                dp[v] = dp[v - value[i]] + weight[i];
            }
        }
    }

    // Find maximum achievable value
    for (long long v = max_value; v >= 0; v--) {
        if (dp[v] <= W) {
            cout << v << "\n";
            return 0;
        }
    }

    cout << 0 << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N * V) | V = sum of values <= 10^5 |
| Space | O(V) | Single array of size V |

---

## Common Mistakes

### Mistake 1: Using Capacity-Based DP

```python
# WRONG - Will exceed memory/time limits
dp = [[0] * (W + 1) for _ in range(N + 1)]  # W can be 10^9!
```

**Problem:** Standard knapsack fails when W is too large.
**Fix:** Use value-based DP when sum of values is small.

### Mistake 2: Forward Iteration (Allows Item Reuse)

```python
# WRONG - Items can be used multiple times
for v in range(value, max_value + 1):  # Forward iteration
    dp[v] = min(dp[v], dp[v - value] + weight)
```

**Problem:** Forward iteration uses updated dp values, allowing items to be picked multiple times.
**Fix:** Iterate backwards from max_value down to value.

### Mistake 3: Integer Overflow

```cpp
// WRONG - int may overflow with large weights
int dp[MAX_VALUE];  // Weights can be up to 10^9

// CORRECT
long long dp[MAX_VALUE];  // Use long long for weights
```

**Problem:** Sum of weights can exceed 32-bit integer range.
**Fix:** Use `long long` for weight calculations.

### Mistake 4: Wrong INF Value

```python
# WRONG - INF too small, could be reached legitimately
INF = 10**6

# CORRECT - INF must exceed any possible sum of weights
INF = float('inf')  # or 10**18 in C++
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single item fits | N=1, W=5, item=(3,100) | 100 | Take the only item |
| Single item too heavy | N=1, W=2, item=(3,100) | 0 | Cannot take any item |
| All items fit | N=3, W=100, items heavy 1 each | sum of values | Take everything |
| Exact fit | N=2, W=5, items=(2,10),(3,20) | 30 | Both items fit exactly |
| Large W, small items | W=10^9, small weights | sum of values | Capacity not limiting |
| Large weights | weights near 10^9 | Handle carefully | Use long long |

---

## When to Use This Pattern

### Use Value-Based DP When:
- Capacity/weight limits are huge (10^9+)
- Individual values are small (allowing bounded total value)
- Standard knapsack DP would exceed memory/time limits

### Use Standard Knapsack DP When:
- Capacity W is small (10^5 or less)
- Values can be arbitrarily large
- Memory O(W) or O(N*W) is acceptable

### Pattern Recognition Checklist:
- [ ] Is W too large for O(N*W) complexity? --> Consider value-based DP
- [ ] Is sum of values bounded and small? --> Value-based DP is feasible
- [ ] Are values small but capacity huge? --> Classic sign for state inversion

### Decision Framework

```
If W <= 10^5 and values unbounded:
    Use standard dp[capacity] = max_value

If W > 10^5 but sum(values) <= 10^5:
    Use inverted dp[value] = min_weight

If both are huge:
    Consider meet-in-the-middle or other techniques
```

---

## Related Problems

### Prerequisites (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Knapsack 1 (AtCoder E)](https://atcoder.jp/contests/dp/tasks/dp_d) | Standard capacity-based knapsack |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [CSES Book Shop](https://cses.fi/problemset/task/1158) | Standard knapsack with moderate W |
| [LeetCode 416 - Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Boolean DP, can we achieve target sum? |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [AtCoder DP F - LCS](https://atcoder.jp/contests/dp/tasks/dp_f) | Different DP state design |
| [CSES Money Sums](https://cses.fi/problemset/task/1745) | All achievable sums |
| [LeetCode 518 - Coin Change 2](https://leetcode.com/problems/coin-change-2/) | Unbounded knapsack variant |

---

## Key Takeaways

1. **The Core Idea:** When capacity is too large, DP on value instead - track minimum weight for each possible value.

2. **Constraint Analysis:** Always check constraints first. The key insight here is v_i <= 10^3 makes value-based DP feasible.

3. **State Inversion:** A powerful technique - when one dimension explodes, swap to another dimension that stays bounded.

4. **Pattern:** This is the "bounded value knapsack" pattern, commonly appearing when weights are huge but values are small.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why standard knapsack DP fails for this problem
- [ ] Derive the value-based DP formulation from scratch
- [ ] Implement in both Python and C++ without looking at solution
- [ ] Identify this pattern in new problems based on constraints
- [ ] Handle edge cases (empty knapsack, single item, exact fit)

---

## Additional Resources

- [AtCoder DP Contest Editorial](https://atcoder.jp/contests/dp/editorial)
- [CP-Algorithms: Knapsack Problems](https://cp-algorithms.com/dynamic_programming/knapsack.html)
- [CSES Problem Set](https://cses.fi/problemset/)
