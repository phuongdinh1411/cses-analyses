---
layout: simple
title: "Deque - Interval DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/deque_analysis
difficulty: Medium
tags: [interval-dp, game-theory, two-player-game, dynamic-programming]
prerequisites: []
---

# Deque (AtCoder DP Contest L)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Dynamic Programming / Game Theory |
| **Time Limit** | 2 seconds |
| **Key Technique** | Interval DP |
| **Problem Link** | [AtCoder DP Contest - L](https://atcoder.jp/contests/dp/tasks/dp_l) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when interval DP applies to game theory problems
- [ ] Model optimal two-player games using DP on intervals
- [ ] Track score differences instead of individual scores for symmetric games
- [ ] Implement interval DP with correct iteration order (by interval length)

---

## Problem Statement

**Problem:** Two players, Taro and Jiro, play a game with a deque (double-ended queue) containing N integers. Players alternate turns, with Taro going first. On each turn, a player removes either the leftmost or rightmost element and adds its value to their score. Both players play optimally to maximize their own score. Find Taro's score minus Jiro's score.

**Input:**
- Line 1: N (number of elements)
- Line 2: a_1, a_2, ..., a_N (the elements)

**Output:**
- Maximum score difference (Taro's score - Jiro's score) when both play optimally

**Constraints:**
- 1 <= N <= 3000
- 1 <= a_i <= 10^9

### Example

```
Input:
4
10 80 90 30

Output:
10
```

**Explanation:**
- Taro takes 10 (left), score: Taro=10, Jiro=0
- Jiro takes 30 (right), score: Taro=10, Jiro=30
- Taro takes 90 (right), score: Taro=100, Jiro=30
- Jiro takes 80 (remaining), score: Taro=100, Jiro=110
- Final difference: 100 - 110 = -10?

Wait, let's reconsider with optimal play:
- Taro takes 90 (right), score: Taro=90
- Jiro takes 80 (right), score: Jiro=80
- Taro takes 30 (right), score: Taro=120
- Jiro takes 10 (remaining), score: Jiro=90
- Final difference: 120 - 90 = 30?

Actually optimal: Taro=90, Jiro=80, Taro=30, Jiro=10 gives 120-90=30, but answer is 10. Let me trace correctly with minimax:
The answer 10 comes from optimal play where Jiro also plays to maximize their score.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we model a two-player game where both players play optimally?

This is a classic **interval DP** problem combined with **game theory**. The key insight is that after any move, the remaining elements form a contiguous subarray (interval). By computing optimal results for all possible intervals, we can determine the game outcome.

### Breaking Down the Problem

1. **What are we looking for?** The score difference when both players play optimally.
2. **What information do we have?** The array elements and their positions.
3. **What's the relationship?** Each move reduces the interval by 1 from either end, creating a subproblem.

### The Minimax Insight

In two-player zero-sum games:
- When it's my turn, I want to **maximize** my advantage
- When it's opponent's turn, they want to **maximize** their advantage (minimize mine)

The brilliant trick: Instead of tracking two scores, track the **score difference from the current player's perspective**. When players alternate, we subtract the subproblem result because the next player's gain is our loss.

---

## Solution: Interval DP

### Key Insight

> **The Trick:** Define `dp[i][j]` as the maximum score difference achievable by the **current player** for the interval [i, j]. After taking an element, subtract the opponent's optimal result because their gain reduces our relative advantage.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Maximum (current player's score - opponent's score) for interval [i, j] |

**In plain English:** If you're the player about to move on interval [i, j], dp[i][j] tells you the best score advantage you can achieve.

### State Transition

```
dp[i][j] = max(
    a[i] - dp[i+1][j],   // Take left element
    a[j] - dp[i][j-1]    // Take right element
)
```

**Why subtract?** After taking element `a[i]`, the opponent plays optimally on [i+1, j]. The opponent's advantage in that subgame becomes our disadvantage, so we subtract `dp[i+1][j]`.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[i][i]` | a[i] | Single element: current player takes it, gains a[i] |

### Algorithm

1. Initialize dp[i][i] = a[i] for all single-element intervals
2. Iterate by increasing interval length (2 to N)
3. For each interval [i, j], compute optimal choice
4. Return dp[0][n-1] (Taro's advantage on full array)

### Dry Run Example

Let's trace through with input `N = 4, a = [10, 80, 90, 30]`:

```
Array indices: 0   1   2   3
Values:       10  80  90  30

Step 1: Base cases (length = 1)
  dp[0][0] = 10   (take 10)
  dp[1][1] = 80   (take 80)
  dp[2][2] = 90   (take 90)
  dp[3][3] = 30   (take 30)

Step 2: Length = 2
  dp[0][1]: interval [10, 80]
    Take left:  10 - dp[1][1] = 10 - 80 = -70
    Take right: 80 - dp[0][0] = 80 - 10 = 70
    dp[0][1] = max(-70, 70) = 70

  dp[1][2]: interval [80, 90]
    Take left:  80 - dp[2][2] = 80 - 90 = -10
    Take right: 90 - dp[1][1] = 90 - 80 = 10
    dp[1][2] = max(-10, 10) = 10

  dp[2][3]: interval [90, 30]
    Take left:  90 - dp[3][3] = 90 - 30 = 60
    Take right: 30 - dp[2][2] = 30 - 90 = -60
    dp[2][3] = max(60, -60) = 60

Step 3: Length = 3
  dp[0][2]: interval [10, 80, 90]
    Take left:  10 - dp[1][2] = 10 - 10 = 0
    Take right: 90 - dp[0][1] = 90 - 70 = 20
    dp[0][2] = max(0, 20) = 20

  dp[1][3]: interval [80, 90, 30]
    Take left:  80 - dp[2][3] = 80 - 60 = 20
    Take right: 30 - dp[1][2] = 30 - 10 = 20
    dp[1][3] = max(20, 20) = 20

Step 4: Length = 4
  dp[0][3]: interval [10, 80, 90, 30]
    Take left:  10 - dp[1][3] = 10 - 20 = -10
    Take right: 30 - dp[0][2] = 30 - 20 = 10
    dp[0][3] = max(-10, 10) = 10

Answer: dp[0][3] = 10
```

### Visual Diagram

```
DP Table (dp[i][j] for interval [i,j]):

     j=0   j=1   j=2   j=3
i=0  [10]  [70]  [20]  [10] <- Answer
i=1        [80]  [10]  [20]
i=2              [90]  [60]
i=3                    [30]

Fill order: diagonal by diagonal (increasing interval length)
```

### Code

#### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # dp[i][j] = max score difference for current player on interval [i, j]
    dp = [[0] * n for _ in range(n)]

    # Base case: single elements
    for i in range(n):
        dp[i][i] = a[i]

    # Fill by increasing interval length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            take_left = a[i] - dp[i + 1][j]
            take_right = a[j] - dp[i][j - 1]
            dp[i][j] = max(take_left, take_right)

    print(dp[0][n - 1])

if __name__ == "__main__":
    solve()
```

##### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N^2) | Fill N^2/2 states, O(1) per state |
| Space | O(N^2) | 2D DP table |

---

## Common Mistakes

### Mistake 1: Tracking Individual Scores

```python
# WRONG - Overcomplicates the problem
dp[i][j] = (taro_score, jiro_score)
```

**Problem:** Tracking two separate scores makes transitions complex and requires knowing whose turn it is.
**Fix:** Track only the score difference from the current player's perspective.

### Mistake 2: Wrong Sign in Transition

```python
# WRONG - Adding instead of subtracting
dp[i][j] = max(a[i] + dp[i+1][j], a[j] + dp[i][j-1])
```

**Problem:** This assumes both players contribute to the same score.
**Fix:** Subtract the subproblem result because opponent's gain is your loss.

### Mistake 3: Wrong Iteration Order

```python
# WRONG - Iterating by i, j directly
for i in range(n):
    for j in range(i, n):
        # dp[i+1][j] may not be computed yet!
```

**Problem:** When computing dp[i][j], we need dp[i+1][j] and dp[i][j-1] to be ready.
**Fix:** Iterate by interval length, from smallest to largest.

**Problem:** With a_i up to 10^9 and N up to 3000, differences can exceed int range.
**Fix:** Use `long long` for the DP table and intermediate calculations.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `N=1, a=[5]` | 5 | Taro takes the only element |
| Two elements | `N=2, a=[3, 7]` | 4 | Taro takes 7, Jiro takes 3: 7-3=4 |
| All equal | `N=4, a=[5,5,5,5]` | 0 | Symmetric game, tied |
| Strictly increasing | `N=3, a=[1,2,3]` | 2 | Taro: 3, Jiro: 2, Taro: 1 -> 4-2=2 |
| Large values | `N=2, a=[10^9, 10^9]` | 0 | Test overflow handling |

---

## When to Use This Pattern

### Use Interval DP for Games When:
- Players take from endpoints of a sequence
- Remaining elements always form a contiguous interval
- Both players play optimally (minimax scenario)
- The game has perfect information (no hidden state)

### Don't Use When:
- Players can take from anywhere (not just endpoints)
- The game has randomness or hidden information
- State space is too large (N > 5000 for O(N^2))

### Pattern Recognition Checklist:
- [ ] Two-player alternating game? -> **Consider game theory DP**
- [ ] Taking from ends of array? -> **Interval DP likely applies**
- [ ] Need optimal play for both sides? -> **Use minimax (subtract subproblem)**
- [ ] Score difference matters? -> **Track difference, not individual scores**

---

## Related Problems

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES - Removal Game](https://cses.fi/problemset/task/1097) | Identical problem |
| [LeetCode 486 - Predict the Winner](https://leetcode.com/problems/predict-the-winner/) | Return true/false instead of difference |
| [LeetCode 877 - Stone Game](https://leetcode.com/problems/stone-game/) | Even length, alternating parity trick |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [LeetCode 1140 - Stone Game II](https://leetcode.com/problems/stone-game-ii/) | Variable number of piles per turn |
| [LeetCode 1406 - Stone Game III](https://leetcode.com/problems/stone-game-iii/) | Take 1-3 elements from front |
| [AtCoder DP - K Stones](https://atcoder.jp/contests/dp/tasks/dp_k) | Grundy numbers / Sprague-Grundy |

---

## Key Takeaways

1. **The Core Idea:** Model optimal two-player games using interval DP where dp[i][j] represents the current player's advantage on interval [i,j].

2. **The Subtraction Trick:** After making a move, subtract the opponent's optimal result from the subproblem because their gain is your loss.

3. **Iteration Order:** Always fill the DP table by increasing interval length to ensure dependencies are computed first.

4. **Pattern:** This is the fundamental template for "two-player game on array endpoints" problems.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why we subtract dp[i+1][j] instead of adding it
- [ ] Derive the recurrence relation from scratch
- [ ] Implement the solution in under 15 minutes
- [ ] Recognize this pattern in new game theory problems

---

## Additional Resources

- [AtCoder DP Contest - Problem L](https://atcoder.jp/contests/dp/tasks/dp_l) - Original problem
- [CSES Removal Game](https://cses.fi/problemset/task/1097) - Similar interval game theory problem
- [CP-Algorithms - Game Theory](https://cp-algorithms.com/game_theory/) - Advanced game theory concepts
