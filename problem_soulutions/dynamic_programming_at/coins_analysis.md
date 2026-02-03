---
layout: simple
title: "Coins - Probability DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/coins_analysis
difficulty: Medium
tags: [dp, probability, expected-value]
prerequisites: []
---

# Coins

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [AtCoder DP Contest - Problem I](https://atcoder.jp/contests/dp/tasks/dp_i) |
| **Difficulty** | Medium |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | Probability DP |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how to model probability using dynamic programming
- [ ] Define DP states for counting outcomes with probabilities
- [ ] Apply the recurrence relation for independent events
- [ ] Optimize space complexity from O(N^2) to O(N) using rolling array

---

## Problem Statement

**Problem:** Given N coins where each coin i has probability p_i of landing heads, find the probability of getting more heads than tails when all coins are tossed.

**Input:**
- Line 1: N (number of coins)
- Line 2: p_1, p_2, ..., p_N (probability of heads for each coin)

**Output:**
- The probability that the number of heads exceeds the number of tails (absolute error at most 10^-9)

**Constraints:**
- 1 <= N <= 3000
- 0 < p_i < 1

### Example

```
Input:
3
0.30 0.60 0.80

Output:
0.612
```

**Explanation:** We need more heads than tails, meaning at least 2 heads out of 3 coins.

- P(exactly 2 heads) = P(HHT) + P(HTH) + P(THH)
  - HHT: 0.3 * 0.6 * 0.2 = 0.036
  - HTH: 0.3 * 0.4 * 0.8 = 0.096
  - THH: 0.7 * 0.6 * 0.8 = 0.336
  - Total: 0.468

- P(exactly 3 heads) = 0.3 * 0.6 * 0.8 = 0.144

- Answer: 0.468 + 0.144 = **0.612**

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently compute the probability of getting a specific number of heads?

The brute force approach would enumerate all 2^N possible outcomes, which is infeasible for N = 3000. Instead, we observe that the probability of j heads after considering i coins only depends on the probability of (j-1) or j heads after (i-1) coins.

### Breaking Down the Problem

1. **What are we looking for?** Probability of getting more than N/2 heads
2. **What information do we have?** Individual coin probabilities
3. **What's the relationship?** Each coin either adds a head (with probability p_i) or a tail (with probability 1-p_i)

### Analogies

Think of this problem like filling a probability distribution table. Each coin "expands" the possible outcomes: if you had probability X of having j heads, after one more coin, that probability splits into:
- Contributing to "j+1 heads" with weight p
- Contributing to "j heads" with weight (1-p)

---

## Solution 1: Brute Force (Exponential)

### Idea

Enumerate all 2^N outcomes and sum probabilities where heads > tails.

### Algorithm

1. Generate all binary sequences of length N
2. For each sequence, compute probability and count heads
3. Sum probabilities where heads > N/2

### Why This Does Not Work

With N up to 3000, we would need to enumerate 2^3000 outcomes, which is computationally impossible.

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^N) | All possible outcomes |
| Space | O(N) | Recursion stack |

---

## Solution 2: Optimal DP Solution

### Key Insight

> **The Trick:** Track the probability distribution of the number of heads as we process coins one by one.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Probability of getting exactly j heads from the first i coins |

**In plain English:** After tossing the first i coins, dp[i][j] tells us the probability that exactly j of them landed heads.

### State Transition

```
dp[i][j] = p[i] * dp[i-1][j-1] + (1 - p[i]) * dp[i-1][j]
```

**Why?** To have exactly j heads after i coins:
- Either we had (j-1) heads after (i-1) coins AND coin i landed heads (probability p[i])
- Or we had j heads after (i-1) coins AND coin i landed tails (probability 1-p[i])

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0][0]` | 1.0 | With 0 coins, probability of 0 heads is 1 |
| `dp[0][j]` for j > 0 | 0.0 | Cannot have heads with no coins |

### Algorithm

1. Initialize dp[0][0] = 1.0
2. For each coin i from 1 to N:
   - For each possible head count j from 0 to i:
     - Apply the transition formula
3. Sum dp[N][j] for all j > N/2

### Dry Run Example

Let's trace through with `N = 3, p = [0.30, 0.60, 0.80]`:

```
Initial: dp[0][0] = 1.0

After coin 1 (p = 0.3):
  dp[1][0] = (1-0.3) * dp[0][0] = 0.7 * 1.0 = 0.70
  dp[1][1] = 0.3 * dp[0][0] = 0.3 * 1.0 = 0.30

  State: [0.70, 0.30]

After coin 2 (p = 0.6):
  dp[2][0] = (1-0.6) * dp[1][0] = 0.4 * 0.70 = 0.28
  dp[2][1] = 0.6 * dp[1][0] + 0.4 * dp[1][1] = 0.42 + 0.12 = 0.54
  dp[2][2] = 0.6 * dp[1][1] = 0.6 * 0.30 = 0.18

  State: [0.28, 0.54, 0.18]

After coin 3 (p = 0.8):
  dp[3][0] = 0.2 * dp[2][0] = 0.2 * 0.28 = 0.056
  dp[3][1] = 0.8 * dp[2][0] + 0.2 * dp[2][1] = 0.224 + 0.108 = 0.332
  dp[3][2] = 0.8 * dp[2][1] + 0.2 * dp[2][2] = 0.432 + 0.036 = 0.468
  dp[3][3] = 0.8 * dp[2][2] = 0.8 * 0.18 = 0.144

  State: [0.056, 0.332, 0.468, 0.144]

More heads than tails means heads > 1.5, so heads >= 2
Answer = dp[3][2] + dp[3][3] = 0.468 + 0.144 = 0.612
```

### Visual Diagram

```
Coins:     1        2        3
Prob:    0.30     0.60     0.80

Heads Distribution Evolution:

         0 heads    1 head    2 heads   3 heads
i=0:     [1.00]
i=1:     [0.70,     0.30]
i=2:     [0.28,     0.54,     0.18]
i=3:     [0.056,    0.332,    0.468,    0.144]
                               ^^^^      ^^^^
                              Sum these: 0.612
```

### Code (Python)

```python
def solve():
    n = int(input())
    p = list(map(float, input().split()))

    # dp[j] = probability of exactly j heads
    dp = [0.0] * (n + 1)
    dp[0] = 1.0

    for i in range(n):
        # Process backwards to avoid overwriting values we need
        for j in range(i + 1, -1, -1):
            if j > 0:
                dp[j] = p[i] * dp[j - 1] + (1 - p[i]) * dp[j]
            else:
                dp[j] = (1 - p[i]) * dp[j]

    # Sum probabilities where heads > tails (heads > n/2)
    result = sum(dp[j] for j in range(n // 2 + 1, n + 1))
    print(f"{result:.10f}")

if __name__ == "__main__":
    solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<double> p(n);
    for (int i = 0; i < n; i++) {
        cin >> p[i];
    }

    // dp[j] = probability of exactly j heads
    vector<double> dp(n + 1, 0.0);
    dp[0] = 1.0;

    for (int i = 0; i < n; i++) {
        // Process backwards to avoid overwriting values we need
        for (int j = i + 1; j >= 0; j--) {
            if (j > 0) {
                dp[j] = p[i] * dp[j - 1] + (1 - p[i]) * dp[j];
            } else {
                dp[j] = (1 - p[i]) * dp[j];
            }
        }
    }

    // Sum probabilities where heads > tails (heads > n/2)
    double result = 0.0;
    for (int j = n / 2 + 1; j <= n; j++) {
        result += dp[j];
    }

    cout << fixed << setprecision(10) << result << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N^2) | For each of N coins, update up to N+1 states |
| Space | O(N) | Single array of size N+1 (space-optimized) |

---

## Common Mistakes

### Mistake 1: Forward Loop Instead of Backward

```python
# WRONG: Forward loop overwrites values before they're used
for j in range(i + 2):
    if j > 0:
        dp[j] = p[i] * dp[j - 1] + (1 - p[i]) * dp[j]
```

**Problem:** When updating dp[j], we need dp[j-1] from the PREVIOUS iteration. Forward loop overwrites dp[j-1] before we use it.
**Fix:** Iterate j in reverse order (from i+1 down to 0).

### Mistake 2: Wrong Threshold for "More Heads Than Tails"

```python
# WRONG: Using >= n/2 instead of > n/2
result = sum(dp[j] for j in range(n // 2, n + 1))
```

**Problem:** "More heads than tails" means heads > tails, so heads > n/2, not heads >= n/2.
**Fix:** Start summation from n // 2 + 1.

### Mistake 3: Floating Point Precision

```python
# WRONG: Printing with insufficient precision
print(result)

# CORRECT: Use sufficient decimal places
print(f"{result:.10f}")
```

**Problem:** Output requires absolute error at most 10^-9.
**Fix:** Print with at least 9-10 decimal places.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single coin (p > 0.5) | N=1, p=[0.7] | 0.7 | Need 1 head out of 1 |
| Single coin (p < 0.5) | N=1, p=[0.3] | 0.3 | Still need 1 head |
| All fair coins | N=2, p=[0.5, 0.5] | 0.25 | Only HH counts |
| Very likely heads | N=3, p=[0.99, 0.99, 0.99] | ~0.9997 | Almost certain to win |
| Very unlikely heads | N=3, p=[0.01, 0.01, 0.01] | ~0.000298 | Very unlikely to win |

---

## When to Use This Pattern

### Use This Approach When:
- Computing probability distributions over discrete outcomes
- Events are independent but have different probabilities
- You need to count outcomes satisfying a threshold condition
- The number of "successes" matters, not their order

### Don't Use When:
- Events are dependent (need different DP formulation)
- Exact enumeration is feasible (small N)
- You need expected value instead of probability (use different DP)

### Pattern Recognition Checklist:
- [ ] Independent trials with success/failure outcomes? -> **Probability DP**
- [ ] Need probability of exactly k successes? -> **dp[i][j] = prob of j successes in i trials**
- [ ] Different success probabilities per trial? -> **Cannot use binomial formula directly**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Knapsack 1](https://atcoder.jp/contests/dp/tasks/dp_d) | Basic counting DP with similar structure |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Sushi](https://atcoder.jp/contests/dp/tasks/dp_j) | Expected value instead of probability |
| [Dice Combinations (CSES)](https://cses.fi/problemset/task/1633) | Counting ways with equal probabilities |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Matching](https://atcoder.jp/contests/dp/tasks/dp_o) | Bitmask DP with probabilities |
| [Random Walk](https://codeforces.com/problemset/problem/1472/G) | Probability on graphs |

---

## Key Takeaways

1. **The Core Idea:** Track probability distribution of outcomes as you process events
2. **Time Optimization:** From O(2^N) enumeration to O(N^2) DP by reusing subproblem solutions
3. **Space Trade-off:** Use O(N) space with backward iteration instead of O(N^2) with 2D array
4. **Pattern:** Probability DP - model probability as a sum over mutually exclusive events

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why backward iteration is necessary for space optimization
- [ ] Identify the base case and transition formula
- [ ] Handle the "more than half" threshold correctly
- [ ] Implement in your preferred language in under 15 minutes

---

## Additional Resources

- [AtCoder DP Contest Editorial](https://atcoder.jp/contests/dp)
- [CP-Algorithms: Introduction to DP](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html)
- [Probability Theory Basics](https://en.wikipedia.org/wiki/Probability_theory)
