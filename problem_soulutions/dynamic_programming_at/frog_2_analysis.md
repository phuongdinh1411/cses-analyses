---
layout: simple
title: "Frog 2 - 1D DP with K Jumps"
permalink: /problem_soulutions/dynamic_programming_at/frog_2_analysis
difficulty: Easy
tags: [dp, 1d-dp, linear-dp, k-transitions]
prerequisites: [frog_1]
---

# Frog 2

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | 1D DP with K Transitions |
| **Problem Link** | [AtCoder DP Contest - Problem B](https://atcoder.jp/contests/dp/tasks/dp_b) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Extend 1D DP from fixed transitions (k=2) to variable transitions (k steps)
- [ ] Define DP states for minimum cost path problems
- [ ] Implement efficient O(N*K) transition loops
- [ ] Recognize when to generalize DP recurrence relations

---

## Problem Statement

**Problem:** A frog starts on stone 1 and wants to reach stone N. From stone i, it can jump to any stone from i+1 to i+K. Each jump costs |h[i] - h[j]| where j is the landing stone. Find the minimum total cost.

**Input:**
- Line 1: N (number of stones), K (maximum jump distance)
- Line 2: h[1], h[2], ..., h[N] (heights of stones)

**Output:**
- Minimum total cost to reach stone N

**Constraints:**
- 2 <= N <= 10^5
- 1 <= K <= 100
- 1 <= h[i] <= 10^4

### Example

```
Input:
5 3
10 30 40 50 20

Output:
30
```

**Explanation:** Optimal path is 1 -> 2 -> 5 with cost |10-30| + |30-20| = 20 + 10 = 30.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** This is an extension of Frog 1. Instead of only jumping 1 or 2 stones, we can now jump up to K stones.

The core insight is that at each position, we need to consider K possible previous positions instead of just 2. The optimal cost to reach position i is the minimum of (cost to reach any valid previous position + jump cost).

### Breaking Down the Problem

1. **What are we looking for?** Minimum cost to reach stone N from stone 1.
2. **What information do we have?** Heights of all stones, maximum jump distance K.
3. **What's the relationship?** dp[i] depends on dp[i-1], dp[i-2], ..., dp[i-K].

### Analogy

Think of this like finding the cheapest flight path where you can have up to K layovers between airports, and each flight's cost depends on the altitude difference between airports.

---

## Solution 1: Brute Force (Recursion)

### Idea

Try all possible jump sequences from stone 1 to stone N, computing the cost for each path.

### Code

```python
def solve_brute_force(n, k, h):
    """
    Brute force recursive solution.
    Time: O(K^N) - exponential
    Space: O(N) - recursion stack
    """
    def min_cost(i):
        if i == 0:
            return 0
        result = float('inf')
        for j in range(1, min(k, i) + 1):
            result = min(result, min_cost(i - j) + abs(h[i] - h[i - j]))
        return result

    return min_cost(n - 1)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(K^N) | Each position branches into K recursive calls |
| Space | O(N) | Maximum recursion depth |

---

## Solution 2: Optimal (Bottom-Up DP)

### Key Insight

> **The Trick:** For each stone i, the minimum cost is the best choice among all K possible previous stones.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i]` | Minimum cost to reach stone i from stone 0 |

**In plain English:** dp[i] stores the cheapest way to get to stone i.

### State Transition

```
dp[i] = min(dp[j] + |h[i] - h[j]|) for all j in [max(0, i-K), i-1]
```

**Why?** To reach stone i, we must have jumped from some stone j where i-K <= j < i. We pick the j that minimizes total cost.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 0 | Starting position, no cost to be here |

### Dry Run Example

Input: `n=5, k=3, h=[10, 30, 40, 50, 20]`

```
Initial: dp = [0, inf, inf, inf, inf]

Step 1: i=1, check j in [0, 0]
  dp[1] = dp[0] + |30-10| = 0 + 20 = 20
  dp = [0, 20, inf, inf, inf]

Step 2: i=2, check j in [0, 1]
  from j=0: dp[0] + |40-10| = 0 + 30 = 30
  from j=1: dp[1] + |40-30| = 20 + 10 = 30
  dp[2] = 30
  dp = [0, 20, 30, inf, inf]

Step 3: i=3, check j in [0, 2]
  from j=0: dp[0] + |50-10| = 0 + 40 = 40
  from j=1: dp[1] + |50-30| = 20 + 20 = 40
  from j=2: dp[2] + |50-40| = 30 + 10 = 40
  dp[3] = 40
  dp = [0, 20, 30, 40, inf]

Step 4: i=4, check j in [1, 3]
  from j=1: dp[1] + |20-30| = 20 + 10 = 30  <-- minimum
  from j=2: dp[2] + |20-40| = 30 + 20 = 50
  from j=3: dp[3] + |20-50| = 40 + 30 = 70
  dp[4] = 30
  dp = [0, 20, 30, 40, 30]

Answer: dp[4] = 30
```

### Visual Diagram

```
Stones:  0    1    2    3    4
Heights: 10   30   40   50   20
         |    |              ^
         |    +---> jump --->|  cost = 10
         +--> jump --------->   cost = 20
                                --------
                                Total: 30
```

### Code (Python)

```python
def solve_optimal(n, k, h):
    """
    Bottom-up DP solution.
    Time: O(N*K)
    Space: O(N)
    """
    dp = [float('inf')] * n
    dp[0] = 0

    for i in range(1, n):
        for j in range(1, min(k, i) + 1):
            dp[i] = min(dp[i], dp[i - j] + abs(h[i] - h[i - j]))

    return dp[n - 1]

# Read input and solve
n, k = map(int, input().split())
h = list(map(int, input().split()))
print(solve_optimal(n, k, h))
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, k;
    cin >> n >> k;

    vector<int> h(n);
    for (int i = 0; i < n; i++) {
        cin >> h[i];
    }

    vector<long long> dp(n, LLONG_MAX);
    dp[0] = 0;

    for (int i = 1; i < n; i++) {
        for (int j = 1; j <= min(k, i); j++) {
            dp[i] = min(dp[i], dp[i - j] + abs(h[i] - h[i - j]));
        }
    }

    cout << dp[n - 1] << endl;
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N*K) | For each of N stones, check up to K previous stones |
| Space | O(N) | DP array of size N |

---

## Common Mistakes

### Mistake 1: Wrong Loop Bounds for K

```python
# WRONG - may access negative indices
for j in range(1, k + 1):
    dp[i] = min(dp[i], dp[i - j] + ...)

# CORRECT - limit j to valid range
for j in range(1, min(k, i) + 1):
    dp[i] = min(dp[i], dp[i - j] + ...)
```

**Problem:** When i < k, accessing dp[i-k] goes out of bounds.
**Fix:** Use `min(k, i)` to limit the jump distance.

### Mistake 2: Forgetting Absolute Value

```python
# WRONG
cost = h[i] - h[j]

# CORRECT
cost = abs(h[i] - h[j])
```

**Problem:** Height differences can be negative; cost must be positive.

### Mistake 3: 1-indexed vs 0-indexed Confusion

```python
# WRONG (if using 1-indexed input directly)
dp[1] = 0  # but h array might be 0-indexed

# CORRECT - be consistent with indexing
dp[0] = 0  # 0-indexed throughout
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| K=1 (only adjacent jumps) | `n=3, k=1, h=[1,2,3]` | 2 | Must visit every stone |
| K >= N-1 (can reach end directly) | `n=3, k=5, h=[10,100,10]` | 0 | Jump directly from 0 to N-1 |
| All same heights | `n=4, k=2, h=[5,5,5,5]` | 0 | All jumps cost 0 |
| Strictly increasing heights | `n=4, k=1, h=[1,2,3,4]` | 3 | Total = sum of differences |
| N=2 (minimum stones) | `n=2, k=1, h=[1,5]` | 4 | Single jump required |

---

## When to Use This Pattern

### Use This Approach When:
- Problem involves reaching a destination with variable step sizes
- Cost depends on state transitions (not just position)
- Need to find minimum/maximum over multiple previous states

### Don't Use When:
- K is very large (consider segment tree/deque optimization)
- Transitions don't have overlapping subproblems
- Problem requires tracking path (add parent pointer array)

### Pattern Recognition Checklist:
- [ ] Linear sequence of positions? -> **Consider 1D DP**
- [ ] Multiple choices at each step? -> **Loop over K transitions**
- [ ] Minimize/maximize cost? -> **Use min/max in transition**

---

## Related Problems

### Easier (Do First)
| Problem | Why It Helps |
|---------|--------------|
| [Frog 1 (AtCoder DP-A)](https://atcoder.jp/contests/dp/tasks/dp_a) | Same problem with K=2 |
| [Min Cost Climbing Stairs (LC 746)](https://leetcode.com/problems/min-cost-climbing-stairs/) | Similar 1D DP structure |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [House Robber (LC 198)](https://leetcode.com/problems/house-robber/) | Can't take adjacent, maximize |
| [Jump Game II (LC 45)](https://leetcode.com/problems/jump-game-ii/) | Minimize jumps, not cost |

### Harder (Do After)
| Problem | New Concept |
|---------|-------------|
| [Frog 3 (AtCoder DP-Z)](https://atcoder.jp/contests/dp/tasks/dp_z) | Convex hull trick optimization |
| [CSES - Minimizing Coins](https://cses.fi/problemset/task/1634) | Unbounded transitions |

---

## Key Takeaways

1. **Core Idea:** Extend fixed-step DP to variable-step by looping over K possible transitions
2. **Time Optimization:** Memoization/tabulation reduces O(K^N) to O(N*K)
3. **Space Trade-off:** O(N) space for DP array
4. **Pattern:** Linear DP with multiple transition sources

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why O(N*K) is optimal for this constraint
- [ ] Modify the solution to reconstruct the actual path
- [ ] Implement in under 10 minutes
