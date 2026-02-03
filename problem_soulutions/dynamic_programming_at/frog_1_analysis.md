---
layout: simple
title: "Frog 1 - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming_at/frog_1_analysis
difficulty: Easy
tags: [dp, 1d-dp, linear-dp, minimum-cost]
prerequisites: []
---

# Frog 1

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [AtCoder DP Contest - Problem A](https://atcoder.jp/contests/dp/tasks/dp_a) |
| **Difficulty** | Easy |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | 1D DP with Linear Transitions |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize problems that require simple 1D dynamic programming
- [ ] Define DP states that represent "minimum cost to reach position i"
- [ ] Write recurrence relations with multiple transition options
- [ ] Implement both forward and backward DP approaches
- [ ] Optimize space from O(n) to O(1) using rolling variables

---

## Problem Statement

**Problem:** A frog starts on stone 1 and wants to reach stone N. From stone i, it can jump to stone i+1 or i+2. Each jump costs |h[i] - h[j]| where h is the height of each stone. Find the minimum total cost to reach stone N.

**Input:**
- Line 1: N (number of stones)
- Line 2: h[1], h[2], ..., h[N] (heights of stones)

**Output:**
- Single integer: minimum total cost

**Constraints:**
- 2 <= N <= 10^5
- 1 <= h[i] <= 10^4

### Example

```
Input:
6
30 10 60 10 60 50

Output:
40
```

**Explanation:** The optimal path is Stone 1 -> Stone 3 -> Stone 5 -> Stone 6 (1-indexed).
Using 0-indexed: 0 -> 2 -> 4 -> 5
- Jump 0->2: |30-60| = 30
- Jump 2->4: |60-60| = 0
- Jump 4->5: |60-50| = 10
- Total: 30 + 0 + 10 = 40

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** This is a classic "minimum cost path" problem where we need to find the cheapest way to reach a destination with limited movement options.

The frog has only two choices at each stone: jump 1 step or jump 2 steps. This limited choice structure with overlapping subproblems screams dynamic programming.

### Breaking Down the Problem

1. **What are we looking for?** Minimum total cost to reach stone N from stone 1.
2. **What information do we have?** Heights of all stones, and the cost formula |h[i] - h[j]|.
3. **What's the relationship between input and output?** The minimum cost to reach stone i depends on the minimum costs to reach stones i-1 and i-2.

### Analogies

Think of this problem like climbing stairs where each step has a different "energy cost" based on height difference. You want to reach the top floor spending the least energy, and you can take either 1 or 2 steps at a time.

---

## Solution 1: Brute Force (Recursion)

### Idea

Try all possible paths from stone 1 to stone N using recursion. At each stone, branch into two choices (jump +1 or +2) and return the minimum cost.

### Algorithm

1. Start at stone 0 (0-indexed)
2. If at destination, return 0
3. Try jumping to i+1 and i+2, recursively compute costs
4. Return minimum of the two options

### Code

```python
def frog_brute_force(n, heights):
    """
    Brute force recursive solution.

    Time: O(2^n) - exponential branching
    Space: O(n) - recursion stack
    """
    def solve(i):
        if i == n - 1:
            return 0

        # Jump to i+1
        cost1 = abs(heights[i] - heights[i + 1]) + solve(i + 1)

        # Jump to i+2 (if possible)
        if i + 2 < n:
            cost2 = abs(heights[i] - heights[i + 2]) + solve(i + 2)
            return min(cost1, cost2)

        return cost1

    return solve(0)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n) | Each position branches into 2 choices |
| Space | O(n) | Maximum recursion depth |

### Why This Works (But Is Slow)

The recursion correctly explores all paths, but it recalculates the same subproblems exponentially many times. For example, solve(3) is called multiple times from different paths.

---

## Solution 2: Optimal Solution (Bottom-Up DP)

### Key Insight

> **The Trick:** The minimum cost to reach stone i only depends on the costs to reach stones i-1 and i-2. We can build the solution iteratively from the start.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i]` | Minimum cost to reach stone i from stone 0 |

**In plain English:** For each stone, we store the cheapest way to get there from the starting stone.

### State Transition

```
dp[i] = min(dp[i-1] + |h[i] - h[i-1]|, dp[i-2] + |h[i] - h[i-2]|)
```

**Why?** To reach stone i, we must have come from either stone i-1 or stone i-2. We pick whichever path gives the minimum total cost.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 0 | Starting position, no cost to be here |
| `dp[1]` | \|h[1] - h[0]\| | Only one way to reach stone 1 |

### Algorithm

1. Initialize dp[0] = 0, dp[1] = |h[1] - h[0]|
2. For each stone i from 2 to n-1:
   - Compute cost coming from i-1 and i-2
   - Take minimum
3. Return dp[n-1]

### Dry Run Example

Let's trace through with `n = 6, heights = [30, 10, 60, 10, 60, 50]`:

```
Initial state:
  dp = [0, _, _, _, _, _]
  heights = [30, 10, 60, 10, 60, 50]

Step 1: Compute dp[1]
  dp[1] = |10 - 30| = 20
  dp = [0, 20, _, _, _, _]

Step 2: Compute dp[2]
  From dp[1]: 20 + |60 - 10| = 20 + 50 = 70
  From dp[0]: 0 + |60 - 30| = 0 + 30 = 30
  dp[2] = min(70, 30) = 30
  dp = [0, 20, 30, _, _, _]

Step 3: Compute dp[3]
  From dp[2]: 30 + |10 - 60| = 30 + 50 = 80
  From dp[1]: 20 + |10 - 10| = 20 + 0 = 20
  dp[3] = min(80, 20) = 20
  dp = [0, 20, 30, 20, _, _]

Step 4: Compute dp[4]
  From dp[3]: 20 + |60 - 10| = 20 + 50 = 70
  From dp[2]: 30 + |60 - 60| = 30 + 0 = 30
  dp[4] = min(70, 30) = 30
  dp = [0, 20, 30, 20, 30, _]

Step 5: Compute dp[5]
  From dp[4]: 30 + |50 - 60| = 30 + 10 = 40
  From dp[3]: 20 + |50 - 10| = 20 + 40 = 60
  dp[5] = min(40, 60) = 40
  dp = [0, 20, 30, 20, 30, 40]

Answer: dp[5] = 40
```

### Visual Diagram

```
Heights: [30, 10, 60, 10, 60, 50]
Index:     0   1   2   3   4   5

DP Table Construction:
  dp[0] = 0 (start)
  dp[1] = 20 (only from 0)
  dp[2] = min(70, 30) = 30 (from 1 or 0)
  dp[3] = min(80, 20) = 20 (from 2 or 1)
  dp[4] = min(70, 30) = 30 (from 3 or 2)
  dp[5] = min(40, 60) = 40 (from 4 or 3)

Optimal path reconstruction: 0 -> 2 -> 4 -> 5
  Cost: |30-60| + |60-60| + |60-50| = 30 + 0 + 10 = 40
```

### Code

**Python:**

```python
def frog_dp(n, heights):
    """
    Bottom-up DP solution.

    Time: O(n) - single pass
    Space: O(n) - dp array
    """
    if n == 1:
        return 0

    dp = [0] * n
    dp[0] = 0
    dp[1] = abs(heights[1] - heights[0])

    for i in range(2, n):
        from_prev = dp[i - 1] + abs(heights[i] - heights[i - 1])
        from_prev2 = dp[i - 2] + abs(heights[i] - heights[i - 2])
        dp[i] = min(from_prev, from_prev2)

    return dp[n - 1]


# Read input and solve
def main():
    n = int(input())
    heights = list(map(int, input().split()))
    print(frog_dp(n, heights))


if __name__ == "__main__":
    main()
```

**C++:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    vector<int> h(n);
    for (int i = 0; i < n; i++) {
        cin >> h[i];
    }

    vector<int> dp(n);
    dp[0] = 0;
    if (n > 1) dp[1] = abs(h[1] - h[0]);

    for (int i = 2; i < n; i++) {
        int from_prev = dp[i - 1] + abs(h[i] - h[i - 1]);
        int from_prev2 = dp[i - 2] + abs(h[i] - h[i - 2]);
        dp[i] = min(from_prev, from_prev2);
    }

    cout << dp[n - 1] << endl;
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through all stones |
| Space | O(n) | DP array of size n |

---

## Solution 3: Space-Optimized DP

### Key Insight

> **The Trick:** Since dp[i] only depends on dp[i-1] and dp[i-2], we only need two variables instead of an entire array.

### Code

**Python:**

```python
def frog_optimized(n, heights):
    """
    Space-optimized DP using rolling variables.

    Time: O(n) - single pass
    Space: O(1) - only two variables
    """
    if n == 1:
        return 0

    prev2 = 0  # dp[i-2]
    prev1 = abs(heights[1] - heights[0])  # dp[i-1]

    for i in range(2, n):
        curr = min(
            prev1 + abs(heights[i] - heights[i - 1]),
            prev2 + abs(heights[i] - heights[i - 2])
        )
        prev2, prev1 = prev1, curr

    return prev1


def main():
    n = int(input())
    heights = list(map(int, input().split()))
    print(frog_optimized(n, heights))


if __name__ == "__main__":
    main()
```

**C++:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    vector<int> h(n);
    for (int i = 0; i < n; i++) {
        cin >> h[i];
    }

    if (n == 1) {
        cout << 0 << endl;
        return 0;
    }

    int prev2 = 0;
    int prev1 = abs(h[1] - h[0]);

    for (int i = 2; i < n; i++) {
        int curr = min(
            prev1 + abs(h[i] - h[i - 1]),
            prev2 + abs(h[i] - h[i - 2])
        );
        prev2 = prev1;
        prev1 = curr;
    }

    cout << prev1 << endl;
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through all stones |
| Space | O(1) | Only two rolling variables |

---

## Common Mistakes

### Mistake 1: Forgetting the i-2 Bound Check

```python
# WRONG (in brute force)
cost2 = abs(heights[i] - heights[i + 2]) + solve(i + 2)
return min(cost1, cost2)  # Crashes when i+2 >= n

# CORRECT
if i + 2 < n:
    cost2 = abs(heights[i] - heights[i + 2]) + solve(i + 2)
    return min(cost1, cost2)
return cost1
```

**Problem:** Index out of bounds when near the last stone.
**Fix:** Always check bounds before accessing i+2 or i-2.

### Mistake 2: Wrong Initial State

```python
# WRONG
dp[0] = heights[0]  # This is height, not cost!

# CORRECT
dp[0] = 0  # Cost to reach starting position is 0
```

**Problem:** Confusing height values with cost values.
**Fix:** dp[0] should be 0 because there's no cost to start at the first stone.

### Mistake 3: Off-by-One in Loop Range

```python
# WRONG
for i in range(2, n - 1):  # Misses the last stone!

# CORRECT
for i in range(2, n):  # Process all stones including the last
```

**Problem:** Not processing the destination stone.
**Fix:** Loop should go up to n (exclusive) to include index n-1.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum N | n=2, h=[10, 20] | 10 | Only one jump possible |
| All same height | n=5, h=[5, 5, 5, 5, 5] | 0 | All jumps cost 0 |
| Strictly increasing | n=4, h=[1, 2, 3, 4] | 3 | Always jump +1 (cost=1 each) |
| Alternating heights | n=4, h=[1, 100, 1, 100] | 99 | Better to jump +2 when possible |
| Large heights | n=3, h=[1, 10000, 1] | 2 | Jump +2 to avoid peak |

---

## When to Use This Pattern

### Use This Approach When:
- Problem asks for minimum/maximum cost to reach a destination
- Movement is restricted to a fixed number of options (e.g., +1 or +2 steps)
- Current state only depends on a small number of previous states
- Problem has optimal substructure (optimal solution contains optimal sub-solutions)

### Don't Use When:
- Movement options depend on current position in complex ways
- State depends on entire history, not just recent states
- Problem requires finding all paths, not just the optimal one

### Pattern Recognition Checklist:
- [ ] Is there a clear "start" and "end" state? -> **Consider DP**
- [ ] Limited movement options at each step? -> **Consider 1D DP**
- [ ] Cost/value accumulates along the path? -> **Consider min/max DP**
- [ ] Only need last few states? -> **Consider space optimization**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Climbing Stairs (LC 70)](https://leetcode.com/problems/climbing-stairs/) | Same structure, counts paths instead of min cost |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Min Cost Climbing Stairs (LC 746)](https://leetcode.com/problems/min-cost-climbing-stairs/) | Can start from step 0 or 1 |
| [Frog 2 (AtCoder)](https://atcoder.jp/contests/dp/tasks/dp_b) | Can jump up to K steps instead of just 2 |
| [House Robber (LC 198)](https://leetcode.com/problems/house-robber/) | Similar recurrence, different problem context |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Jump Game II (LC 45)](https://leetcode.com/problems/jump-game-ii/) | Variable jump lengths |
| [Frog 3 (AtCoder)](https://atcoder.jp/contests/dp/tasks/dp_z) | Requires Convex Hull Trick optimization |

---

## Key Takeaways

1. **The Core Idea:** DP state represents minimum cost to reach each position; each position considers all incoming transitions.
2. **Time Optimization:** From O(2^n) brute force to O(n) by storing and reusing subproblem solutions.
3. **Space Trade-off:** O(n) array can be reduced to O(1) since we only need the last two states.
4. **Pattern:** This is the canonical "Linear DP with Limited Transitions" pattern.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why dp[i] only needs dp[i-1] and dp[i-2]
- [ ] Implement both O(n) space and O(1) space versions
- [ ] Identify similar problems in contests within 2 minutes

---

## Additional Resources

- [AtCoder DP Contest](https://atcoder.jp/contests/dp) - Full problem set (A-Z)
- [CP-Algorithms: Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html)
- [CSES Dice Combinations](https://cses.fi/problemset/task/1633) - Introductory DP problem
