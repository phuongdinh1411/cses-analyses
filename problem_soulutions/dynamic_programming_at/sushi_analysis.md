---
layout: simple
title: "Sushi - Expected Value DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/sushi_analysis
difficulty: Hard
tags: [expected-value, dp, state-compression, probability, memoization]
prerequisites: [coins_dp, basic_probability]
---

# Sushi

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Dynamic Programming (Expected Value) |
| **Time Limit** | 2 seconds |
| **Key Technique** | Expected Value DP with State Compression |
| **Problem Link** | [AtCoder DP Contest - Problem J](https://atcoder.jp/contests/dp/tasks/dp_j) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand expected value DP and the linearity of expectation
- [ ] Apply state compression to reduce exponential state space to polynomial
- [ ] Derive and rearrange recurrence relations with self-referencing terms
- [ ] Handle floating-point precision in probability/expectation problems

---

## Problem Statement

**Problem:** There are N plates of sushi. Each plate initially has 0, 1, 2, or 3 pieces of sushi. Taro repeatedly performs the following operation: choose a plate uniformly at random. If it has at least one piece of sushi, eat one piece from it. Otherwise, do nothing (but the operation still counts). Continue until all plates are empty. Find the expected number of operations.

**Input:**
- Line 1: N (number of plates)
- Line 2: a_1, a_2, ..., a_N (initial sushi counts)

**Output:**
- Expected number of operations (absolute or relative error at most 10^-9)

**Constraints:**
- 1 <= N <= 300
- 0 <= a_i <= 3

### Example

```
Input:
3
1 1 1

Output:
5.500000000000000
```

**Explanation:** With 3 plates each having 1 sushi, on average it takes 5.5 operations. The first plate requires E[1] = 3 operations on average (geometric distribution), but plates share the random selection, making the calculation more complex.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we compute expected value when the state space seems exponentially large?

The naive approach would track each plate individually, giving O(4^N) states. The key insight is that the identity of plates does not matter - only the counts of plates with 1, 2, or 3 sushi pieces matter. This state compression reduces the state space to O(N^3).

### Breaking Down the Problem

1. **What are we looking for?** Expected number of operations until all plates are empty.
2. **What information do we have?** The count of plates with each sushi amount (0, 1, 2, or 3).
3. **What's the relationship between input and output?** Each operation transitions us to a new state with some probability, and we need to sum expected values.

### Analogies

Think of this problem like a weighted random walk on a 3D grid where coordinates (i, j, k) represent counts of plates with 1, 2, and 3 sushi. Each step moves us toward the origin (0, 0, 0), and we need to count expected steps.

---

## Solution 1: Naive Recursive (TLE)

### Idea

Track all N plates individually and compute expected value by considering all possible transitions.

### Why It Fails

With N plates and up to 4 states per plate (0-3 sushi), the state space is O(4^N), which is far too large for N = 300.

---

## Solution 2: Expected Value DP with State Compression

### Key Insight

> **The Trick:** Individual plate identities do not matter. Only track how many plates have 1, 2, or 3 pieces of sushi.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j][k]` | Expected operations when there are i plates with 1 sushi, j with 2, k with 3 |

**In plain English:** dp[i][j][k] answers "Starting from a configuration with i one-sushi plates, j two-sushi plates, and k three-sushi plates, how many operations do we expect until all are empty?"

### State Transition

The raw recurrence (before rearranging):

```
dp[i][j][k] = 1 + (i/N) * dp[i-1][j][k]      # pick 1-sushi plate
                + (j/N) * dp[i+1][j-1][k]    # pick 2-sushi plate
                + (k/N) * dp[i][j+1][k-1]    # pick 3-sushi plate
                + ((N-i-j-k)/N) * dp[i][j][k] # pick empty plate (no change)
```

**Problem:** The recurrence has `dp[i][j][k]` on both sides!

**Solution:** Rearrange to isolate `dp[i][j][k]`:

```
dp[i][j][k] - ((N-i-j-k)/N) * dp[i][j][k] = 1 + (i/N)*dp[i-1][j][k] + (j/N)*dp[i+1][j-1][k] + (k/N)*dp[i][j+1][k-1]
((i+j+k)/N) * dp[i][j][k] = 1 + (i/N)*dp[i-1][j][k] + (j/N)*dp[i+1][j-1][k] + (k/N)*dp[i][j+1][k-1]
dp[i][j][k] = (N + i*dp[i-1][j][k] + j*dp[i+1][j-1][k] + k*dp[i][j+1][k-1]) / (i+j+k)
```

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0][0][0]` | 0 | No sushi left, we are done |

### Algorithm

1. Count initial plates with 1, 2, and 3 sushi pieces
2. Use memoization to compute dp[c1][c2][c3] recursively
3. At each state, use the rearranged recurrence to avoid infinite recursion
4. Return the expected value for the initial state

### Dry Run Example

Let's trace through with input `N = 2, plates = [1, 2]`:

Initial state: c1=1, c2=1, c3=0 (one plate with 1 sushi, one with 2)

```
Call dp(1, 1, 0):
  Need: dp(0, 1, 0), dp(2, 0, 0)

  Call dp(0, 1, 0):   # 0 one-plates, 1 two-plate
    Need: dp(1, 0, 0)

    Call dp(1, 0, 0): # 1 one-plate, 0 two-plates
      Need: dp(0, 0, 0) = 0
      dp(1,0,0) = (N + 1*dp(0,0,0)) / 1 = (2 + 0) / 1 = 2.0

    dp(0,1,0) = (N + 1*dp(1,0,0)) / 1 = (2 + 2.0) / 1 = 4.0

  Call dp(2, 0, 0):   # 2 one-plates
    Need: dp(1, 0, 0) = 2.0 (already computed)
    dp(2,0,0) = (N + 2*dp(1,0,0)) / 2 = (2 + 4.0) / 2 = 3.0

  dp(1,1,0) = (N + 1*dp(0,1,0) + 1*dp(2,0,0)) / 2
           = (2 + 4.0 + 3.0) / 2 = 4.5

Answer: 4.5
```

### Visual Diagram

```
State Space (i, j, k) where i+j+k <= N:

         k (3-sushi plates)
        /
       /
      +--------> j (2-sushi plates)
      |
      |
      v
      i (1-sushi plates)

Transitions from state (i, j, k):
  - Pick 1-sushi plate (prob i/N): go to (i-1, j, k)
  - Pick 2-sushi plate (prob j/N): go to (i+1, j-1, k)
  - Pick 3-sushi plate (prob k/N): go to (i, j+1, k-1)
  - Pick empty plate (prob (N-i-j-k)/N): stay at (i, j, k)

Goal: Reach (0, 0, 0)
```

### Code (Python)

```python
import sys
sys.setrecursionlimit(1000000)

def solve():
    n = int(input())
    plates = list(map(int, input().split()))

    # Count plates with 1, 2, 3 pieces
    c1 = sum(1 for a in plates if a == 1)
    c2 = sum(1 for a in plates if a == 2)
    c3 = sum(1 for a in plates if a == 3)

    memo = {}

    def dp(i, j, k):
        """Expected operations with i 1-plates, j 2-plates, k 3-plates."""
        if i == 0 and j == 0 and k == 0:
            return 0.0

        if (i, j, k) in memo:
            return memo[(i, j, k)]

        total = i + j + k
        result = n  # Numerator starts with N

        if i > 0:
            result += i * dp(i - 1, j, k)
        if j > 0:
            result += j * dp(i + 1, j - 1, k)
        if k > 0:
            result += k * dp(i, j + 1, k - 1)

        result /= total
        memo[(i, j, k)] = result
        return result

    print(f"{dp(c1, c2, c3):.15f}")

if __name__ == "__main__":
    solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N^3) | State space is O(N^3), each state computed once |
| Space | O(N^3) | Memoization table for all states |

---

## Common Mistakes

### Mistake 1: Not Rearranging the Recurrence

```python
# WRONG - Infinite recursion
def dp(i, j, k):
    result = 1
    result += (n - i - j - k) / n * dp(i, j, k)  # Self-reference!
    result += i / n * dp(i - 1, j, k)
    # ...
    return result
```

**Problem:** The recurrence references dp[i][j][k] on the right side, causing infinite recursion.
**Fix:** Algebraically rearrange to isolate dp[i][j][k] on the left side.

### Mistake 2: Division by Zero

```python
# WRONG - Division by zero when i + j + k = 0
result /= (i + j + k)
```

**Problem:** When all plates are empty, we divide by zero.
**Fix:** Handle the base case (i == j == k == 0) before the division.

### Mistake 3: Incorrect State Transitions

```python
# WRONG - Forgetting that 2->1 increases 1-count
if j > 0:
    result += j * dp(i, j - 1, k)  # Should be dp(i + 1, j - 1, k)
```

**Problem:** When a 2-sushi plate loses one sushi, it becomes a 1-sushi plate, so i should increase.
**Fix:** When j decreases, i should increase by 1.

### Mistake 4: Integer Division

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| All empty | `N=3, plates=[0,0,0]` | 0.0 | No operations needed |
| Single plate | `N=1, plates=[3]` | 3.0 | Must hit same plate 3 times, each costs 1 |
| All ones | `N=3, plates=[1,1,1]` | 5.5 | Classic case |
| Maximum state | `N=300, all 3s` | Large value | Tests complexity |
| Mixed zeros | `N=5, plates=[0,1,0,2,0]` | Varies | Empty plates increase expected ops |

---

## When to Use This Pattern

### Use This Approach When:
- Computing expected value over a random process
- State space can be compressed by grouping equivalent states
- Recurrence has self-referencing terms that can be algebraically eliminated
- Linearity of expectation applies

### Don't Use When:
- Need exact probability distribution, not just expected value
- State transitions are not memoryless (depend on history)
- Cannot find meaningful state compression

### Pattern Recognition Checklist:
- [ ] Computing expected value or probability? -> **Consider expectation DP**
- [ ] Many equivalent states (order doesn't matter)? -> **Apply state compression**
- [ ] Recurrence references itself? -> **Algebraically rearrange**
- [ ] Process involves random choices? -> **Use probability-weighted transitions**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Coins (AtCoder DP I)](https://atcoder.jp/contests/dp/tasks/dp_i) | Basic probability DP |
| [Dice Probability](https://cses.fi/problemset/task/1725) | Expected value basics |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Candies (AtCoder DP M)](https://atcoder.jp/contests/dp/tasks/dp_m) | Distribution counting |
| [Grouping (AtCoder DP U)](https://atcoder.jp/contests/dp/tasks/dp_u) | Bitmask DP |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Stones (AtCoder DP K)](https://atcoder.jp/contests/dp/tasks/dp_k) | Game theory + DP |
| [Walk (AtCoder DP R)](https://atcoder.jp/contests/dp/tasks/dp_r) | Matrix exponentiation |

---

## Key Takeaways

1. **The Core Idea:** Use state compression to track counts instead of individual elements when order does not matter.
2. **Time Optimization:** Reduced from O(4^N) to O(N^3) by observing that plate identities are irrelevant.
3. **Mathematical Trick:** Rearrange self-referencing recurrences algebraically before implementing.
4. **Pattern:** Expected value DP with state compression - applicable to many probability problems.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the recurrence relation from first principles
- [ ] Rearrange self-referencing recurrences algebraically
- [ ] Explain why state compression works (plate identity irrelevance)
- [ ] Implement in under 15 minutes without looking at solution

---

## Additional Resources

- [AtCoder DP Contest Editorial](https://atcoder.jp/contests/dp)
- [CP-Algorithms: Probability DP](https://cp-algorithms.com/algebra/expected_value.html)
- [Expectation and Linearity of Expectation](https://brilliant.org/wiki/linearity-of-expectation/)
