---
layout: simple
title: "Knapsack 1 - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming_at/knapsack_1_analysis
difficulty: Medium
tags: [dp, knapsack, optimization]
prerequisites: []
---

# Knapsack 1

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [AtCoder DP Contest - Problem D](https://atcoder.jp/contests/dp/tasks/dp_d) |
| **Difficulty** | Medium |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | 0/1 Knapsack DP |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement the classic 0/1 Knapsack algorithm
- [ ] Define DP states for optimization problems with capacity constraints
- [ ] Apply space optimization using 1D rolling arrays
- [ ] Recognize knapsack pattern variations in other problems

---

## Problem Statement

**Problem:** Given N items with weights and values, find the maximum total value you can carry in a knapsack with capacity W. Each item can only be taken once (0/1 property).

**Input:**
- Line 1: N W (number of items, knapsack capacity)
- Lines 2 to N+1: w_i v_i (weight and value of item i)

**Output:**
- Maximum possible sum of values

**Constraints:**
- 1 <= N <= 100
- 1 <= W <= 10^5
- 1 <= w_i <= W
- 1 <= v_i <= 10^9

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

**Explanation:**
- Items: (weight=3, value=30), (weight=4, value=50), (weight=5, value=60)
- Best selection: Item 1 + Item 3 = weight 8, value 90
- Item 1 + Item 2 = weight 7, value 80 (suboptimal)
- Item 2 + Item 3 = weight 9 (exceeds capacity)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** For each item, we have exactly two choices: take it or leave it. How do we make optimal decisions across all items?

This is the classic 0/1 Knapsack problem. The "0/1" means each item is either fully taken (1) or not taken (0) - no partial selections allowed.

### Breaking Down the Problem

1. **What are we looking for?** Maximum total value within weight limit W
2. **What information do we have?** Weight and value of each item
3. **What's the relationship?** Each item selection affects remaining capacity, creating subproblems

### Analogies

Think of packing for a trip with a weight limit on your luggage. You have valuable items of different weights - you want to maximize the total value of what you bring without exceeding the weight limit.

---

## Solution 1: Recursive Brute Force

### Idea

Try all possible combinations of items (take or skip each one) and track the maximum value achievable within capacity.

### Algorithm

1. For each item, recursively try both: skip it, or take it (if weight allows)
2. Return the maximum value from all valid combinations

### Code

```python
def knapsack_recursive(n, W, weights, values):
    """
    Brute force recursive solution.

    Time: O(2^n) - exponential
    Space: O(n) - recursion depth
    """
    def solve(i, remaining):
        if i == n:
            return 0

        # Option 1: Skip item i
        skip = solve(i + 1, remaining)

        # Option 2: Take item i (if possible)
        take = 0
        if weights[i] <= remaining:
            take = values[i] + solve(i + 1, remaining - weights[i])

        return max(skip, take)

    return solve(0, W)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n) | Each item has 2 choices, exponential combinations |
| Space | O(n) | Maximum recursion depth |

### Why This Works (But Is Slow)

It correctly explores all subsets but recalculates the same (item, capacity) states many times.

---

## Solution 2: Optimal DP Solution

### Key Insight

> **The Trick:** The maximum value achievable depends only on "which items remain" and "remaining capacity" - use DP to avoid recalculating these states.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Maximum value using first i items with capacity j |

**In plain English:** "What's the best value I can get if I can only consider items 0 to i-1, and my bag can hold weight j?"

### State Transition

```
dp[i][j] = max(
    dp[i-1][j],                              # Skip item i-1
    dp[i-1][j - w[i-1]] + v[i-1]             # Take item i-1 (if w[i-1] <= j)
)
```

**Why?** For each item, we choose the better option between skipping it (keep previous best) or taking it (add its value to the best achievable with reduced capacity).

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0][j]` | 0 | No items = no value |
| `dp[i][0]` | 0 | No capacity = no value |

### Algorithm

1. Initialize dp table with zeros
2. For each item i (1 to n):
   - For each capacity j (0 to W):
     - dp[i][j] = max(skip, take if possible)
3. Return dp[n][W]

### Dry Run Example

Let's trace through with `n=3, W=8, weights=[3,4,5], values=[30,50,60]`:

```
Initial: dp[0][*] = 0 (no items)

Processing Item 1 (w=3, v=30):
  dp[1][3] = max(dp[0][3], dp[0][0]+30) = max(0, 30) = 30
  dp[1][4] = max(dp[0][4], dp[0][1]+30) = max(0, 30) = 30
  ...
  dp[1][8] = 30

Processing Item 2 (w=4, v=50):
  dp[2][4] = max(dp[1][4], dp[1][0]+50) = max(30, 50) = 50
  dp[2][7] = max(dp[1][7], dp[1][3]+50) = max(30, 80) = 80
  dp[2][8] = max(dp[1][8], dp[1][4]+50) = max(30, 80) = 80

Processing Item 3 (w=5, v=60):
  dp[3][5] = max(dp[2][5], dp[2][0]+60) = max(50, 60) = 60
  dp[3][8] = max(dp[2][8], dp[2][3]+60) = max(80, 90) = 90

Answer: dp[3][8] = 90
```

### Visual Diagram

```
DP Table (rows=items, cols=capacity):

     j:  0   1   2   3   4   5   6   7   8
i=0      0   0   0   0   0   0   0   0   0   (no items)
i=1      0   0   0  30  30  30  30  30  30   (item 1: w=3, v=30)
i=2      0   0   0  30  50  50  50  80  80   (items 1-2)
i=3      0   0   0  30  50  60  60  80 [90]  (items 1-3)
                                        ^
                                    Answer
```

### Code

**Python Solution:**

```python
def knapsack_2d(n, W, weights, values):
    """
    2D DP solution for 0/1 Knapsack.

    Time: O(n * W)
    Space: O(n * W)
    """
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(W + 1):
            # Option 1: Skip item i-1
            dp[i][j] = dp[i - 1][j]

            # Option 2: Take item i-1 (if possible)
            if weights[i - 1] <= j:
                dp[i][j] = max(dp[i][j], dp[i - 1][j - weights[i - 1]] + values[i - 1])

    return dp[n][W]


def knapsack_1d(n, W, weights, values):
    """
    Space-optimized 1D DP solution.

    Time: O(n * W)
    Space: O(W)
    """
    dp = [0] * (W + 1)

    for i in range(n):
        # CRITICAL: Iterate backwards to avoid using updated values
        for j in range(W, weights[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])

    return dp[W]


# Main
if __name__ == "__main__":
    n, W = map(int, input().split())
    weights = []
    values = []
    for _ in range(n):
        w, v = map(int, input().split())
        weights.append(w)
        values.append(v)

    print(knapsack_1d(n, W, weights, values))
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, W;
    cin >> n >> W;

    vector<int> weight(n), value(n);
    for (int i = 0; i < n; i++) {
        cin >> weight[i] >> value[i];
    }

    // Space-optimized 1D DP
    vector<long long> dp(W + 1, 0);

    for (int i = 0; i < n; i++) {
        // Iterate backwards to maintain 0/1 property
        for (int j = W; j >= weight[i]; j--) {
            dp[j] = max(dp[j], dp[j - weight[i]] + (long long)value[i]);
        }
    }

    cout << dp[W] << endl;
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * W) | Process each item for each capacity |
| Space (2D) | O(n * W) | Full DP table |
| Space (1D) | O(W) | Single row with backward iteration |

---

## Common Mistakes

### Mistake 1: Forward Iteration in 1D DP

```python
# WRONG - counts same item multiple times
for j in range(weights[i], W + 1):  # Forward iteration
    dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
```

**Problem:** Forward iteration uses already-updated dp[j - w], effectively allowing unlimited copies of each item (unbounded knapsack).

**Fix:** Iterate backwards: `for j in range(W, weights[i] - 1, -1)`

### Mistake 2: Integer Overflow

```cpp
// WRONG - may overflow with large values
int dp[W + 1];  // v_i can be up to 10^9, sum can exceed int

// CORRECT
long long dp[W + 1];
```

**Problem:** Values up to 10^9, summed across items, can overflow 32-bit integers.

**Fix:** Use `long long` in C++ or Python's arbitrary precision.

### Mistake 3: Off-by-One Indexing

```python
# WRONG - accessing weights[i] when i goes from 1 to n
for i in range(1, n + 1):
    if weights[i] <= j:  # IndexError! weights is 0-indexed

# CORRECT
    if weights[i - 1] <= j:
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single item fits | N=1, W=5, w=[3], v=[100] | 100 | Take the only item |
| Single item too heavy | N=1, W=2, w=[3], v=[100] | 0 | Cannot take any item |
| Exact capacity | N=2, W=7, w=[3,4], v=[30,50] | 80 | Take both, exactly fills bag |
| All items fit | N=3, W=100, w=[1,2,3], v=[10,20,30] | 60 | Take everything |
| Large values | N=2, W=10, w=[5,5], v=[10^9, 10^9] | 2*10^9 | Handle large sums |

---

## When to Use This Pattern

### Use This Approach When:
- You have items with weight/cost and value/benefit
- There's a capacity/budget constraint
- Each item can be used at most once
- You want to maximize total value

### Don't Use When:
- Items can be taken multiple times -> Use **Unbounded Knapsack** (forward iteration)
- W is very large but values are small -> Use **Knapsack 2** approach (dp on values)
- Need to track exact items selected -> Add backtracking or use 2D DP

### Pattern Recognition Checklist:
- [ ] Fixed capacity/budget constraint? -> **Knapsack DP**
- [ ] Each item used at most once? -> **0/1 Knapsack** (backward iteration)
- [ ] Each item unlimited uses? -> **Unbounded Knapsack** (forward iteration)
- [ ] Minimize cost to reach target? -> **Knapsack variant**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Frog 1](https://atcoder.jp/contests/dp/tasks/dp_a) | Basic DP introduction |
| [Coin Combinations I](https://cses.fi/problemset/task/1635) | Simpler unbounded version |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Knapsack 2](https://atcoder.jp/contests/dp/tasks/dp_e) | DP on values when W is huge |
| [Book Shop](https://cses.fi/problemset/task/1158) | Same problem, different context |
| [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Target is sum/2 |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Money Sums](https://cses.fi/problemset/task/1745) | Track all achievable sums |
| [Target Sum](https://leetcode.com/problems/target-sum/) | +/- assignment variant |
| [LCS](https://atcoder.jp/contests/dp/tasks/dp_f) | 2D DP on two sequences |

---

## Key Takeaways

1. **The Core Idea:** For each item, choose max of (skip it, take it) based on remaining capacity
2. **Time Optimization:** DP reduces 2^n to n*W by caching (item, capacity) states
3. **Space Trade-off:** Backward iteration in 1D array achieves O(W) space
4. **Pattern:** 0/1 Knapsack is foundational for many subset/selection problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement 0/1 Knapsack from scratch in under 10 minutes
- [ ] Explain why backward iteration is needed for 1D optimization
- [ ] Recognize knapsack pattern in disguised problems
- [ ] Modify for item reconstruction when needed

---

## Additional Resources

- [AtCoder DP Contest](https://atcoder.jp/contests/dp) - Problem D and E
- [CSES Problem Set - DP Section](https://cses.fi/problemset/)
- [CP-Algorithms: Knapsack](https://cp-algorithms.com/dynamic_programming/knapsack.html)
