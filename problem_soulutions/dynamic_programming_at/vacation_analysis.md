---
layout: simple
title: "Vacation - State Machine DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/vacation_analysis
difficulty: Easy
tags: [dp, state-machine, optimization]
prerequisites: [frog_1, frog_2]
---

# Vacation

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | State Machine DP |
| **Link** | [AtCoder DP Contest - Problem C](https://atcoder.jp/contests/dp/tasks/dp_c) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when to track "which choice was made last" as DP state
- [ ] Implement state machine DP with multiple states per position
- [ ] Optimize space from O(n) to O(1) using rolling variables
- [ ] Apply this pattern to problems with "no consecutive same choice" constraints

---

## Problem Statement

**Problem:** Taro has N vacation days. Each day he chooses one activity from {A, B, C} and gains happiness points. He cannot do the same activity on consecutive days. Find the maximum total happiness.

**Input:**
- Line 1: N (number of days)
- Lines 2 to N+1: Three integers a_i, b_i, c_i (happiness for activities A, B, C on day i)

**Output:**
- Maximum total happiness achievable

**Constraints:**
- 1 <= N <= 10^5
- 1 <= a_i, b_i, c_i <= 10^4

### Example

```
Input:
3
10 40 70
20 50 80
30 60 90

Output:
210
```

**Explanation:**
- Day 1: Choose C (70 points)
- Day 2: Choose B (50 points) - cannot repeat C
- Day 3: Choose C (90 points) - cannot repeat B
- Total: 70 + 50 + 90 = 210

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** What information do we need to make optimal decisions?

To decide what activity to do on day i, we need to know what we did on day i-1 (to avoid repetition). This is the hallmark of **state machine DP**: the state includes not just "where we are" (day i) but "what state we're in" (last activity chosen).

### Breaking Down the Problem

1. **What are we looking for?** Maximum sum of happiness values across N days
2. **What information do we have?** Happiness values for each activity on each day
3. **What's the constraint?** Cannot choose the same activity on consecutive days

### Analogies

Think of this like choosing meals at a buffet where you get tired of eating the same thing twice in a row. Each day you pick a different station than yesterday to maximize your enjoyment.

---

## Solution 1: Brute Force (Recursion)

### Idea

Try all valid activity sequences and track the maximum happiness.

### Algorithm

1. For each day, try all three activities
2. Skip any activity that matches the previous day's choice
3. Recursively solve for remaining days
4. Return maximum total happiness

### Code

```python
def solve_brute_force(n, activities):
 """
 Brute force recursive solution.

 Time: O(3 * 2^(n-1)) - exponential
 Space: O(n) - recursion stack
 """
 def helper(day, last):
  if day == n:
   return 0

  best = 0
  for act in range(3):
   if act != last:
    best = max(best, activities[day][act] + helper(day + 1, act))
  return best

 return helper(0, -1)  # -1 means no previous activity
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n) | Each day has 2 valid choices (avoiding previous) |
| Space | O(n) | Recursion depth equals number of days |

### Why This Works (But Is Slow)

Correctness is guaranteed by exploring all valid paths. However, we recalculate the same subproblems many times. For example, "max happiness from day 5 onward when day 4 was activity A" is computed multiple times.

---

## Solution 2: Optimal DP Solution

### Key Insight

> **The Trick:** Track maximum happiness ending with each activity. To compute day i, we only need day i-1's values.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Maximum happiness through day i, ending with activity j |

Where j = 0 (A), j = 1 (B), j = 2 (C).

**In plain English:** "What's the best total happiness I can get up to day i if I do activity j on day i?"

### State Transition

```
dp[i][j] = activities[i][j] + max(dp[i-1][k]) for all k != j
```

**Why?** On day i, choosing activity j gives `activities[i][j]` happiness. We must have done a different activity on day i-1, so we take the best among all other activities.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0][0]` | a_0 | Day 0, activity A |
| `dp[0][1]` | b_0 | Day 0, activity B |
| `dp[0][2]` | c_0 | Day 0, activity C |

### Algorithm

1. Initialize dp[0][j] = activities[0][j] for j in {0, 1, 2}
2. For each day i from 1 to n-1:
   - For each activity j: dp[i][j] = activities[i][j] + max(dp[i-1][k] for k != j)
3. Return max(dp[n-1])

### Dry Run Example

Let's trace through with input `n=3, activities=[(10,40,70), (20,50,80), (30,60,90)]`:

```
Initial state (Day 0):
  dp[0][A] = 10, dp[0][B] = 40, dp[0][C] = 70

Day 1:
  dp[1][A] = 20 + max(dp[0][B], dp[0][C]) = 20 + max(40, 70) = 90
  dp[1][B] = 50 + max(dp[0][A], dp[0][C]) = 50 + max(10, 70) = 120
  dp[1][C] = 80 + max(dp[0][A], dp[0][B]) = 80 + max(10, 40) = 120

Day 2:
  dp[2][A] = 30 + max(dp[1][B], dp[1][C]) = 30 + max(120, 120) = 150
  dp[2][B] = 60 + max(dp[1][A], dp[1][C]) = 60 + max(90, 120) = 180
  dp[2][C] = 90 + max(dp[1][A], dp[1][B]) = 90 + max(90, 120) = 210

Answer: max(150, 180, 210) = 210
```

### Visual Diagram

```
Day:        0           1           2
         ------      ------      ------
Act A:     10    ->    90    ->   150
              \      /    \      /
Act B:     40    ->   120   ->   180
              \      /    \      /
Act C:     70    ->   120   ->   210  <-- ANSWER

Optimal path: C(70) -> B(50) -> C(90) = 210
```

### Code (Python)

```python
def solve_optimal(n, activities):
 """
 Bottom-up DP solution.

 Time: O(n) - single pass through days
 Space: O(n) - dp table with n rows
 """
 dp = [[0] * 3 for _ in range(n)]

 # Base case: day 0
 for j in range(3):
  dp[0][j] = activities[0][j]

 # Fill DP table
 for i in range(1, n):
  dp[i][0] = activities[i][0] + max(dp[i-1][1], dp[i-1][2])
  dp[i][1] = activities[i][1] + max(dp[i-1][0], dp[i-1][2])
  dp[i][2] = activities[i][2] + max(dp[i-1][0], dp[i-1][1])

 return max(dp[n-1])

# Read input and solve
n = int(input())
activities = [tuple(map(int, input().split())) for _ in range(n)]
print(solve_optimal(n, activities))
```

### Space-Optimized Version

Since we only need the previous day's values, we can reduce space to O(1):

```python
def solve_space_optimized(n, activities):
 """
 Space-optimized DP using rolling variables.

 Time: O(n)
 Space: O(1)
 """
 prev_a, prev_b, prev_c = activities[0]

 for i in range(1, n):
  a, b, c = activities[i]
  curr_a = a + max(prev_b, prev_c)
  curr_b = b + max(prev_a, prev_c)
  curr_c = c + max(prev_a, prev_b)
  prev_a, prev_b, prev_c = curr_a, curr_b, curr_c

 return max(prev_a, prev_b, prev_c)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through n days |
| Space | O(1) | Only 3 variables needed (optimized version) |

---

## Common Mistakes

### Mistake 1: Forgetting Base Case

```python
# WRONG - dp[0] is uninitialized
for i in range(1, n):
 dp[i][0] = activities[i][0] + max(dp[i-1][1], dp[i-1][2])
```

**Problem:** First day's values are never set, causing wrong answers.
**Fix:** Initialize `dp[0][j] = activities[0][j]` before the loop.

### Mistake 2: Including Same Activity in Max

```python
# WRONG
dp[i][0] = activities[i][0] + max(dp[i-1])  # Includes dp[i-1][0]!
```

**Problem:** This allows choosing activity A on both day i-1 and day i.
**Fix:** Explicitly exclude the same activity: `max(dp[i-1][1], dp[i-1][2])`

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single day | n=1, (5,10,3) | 10 | Choose max of first day |
| All same values | n=3, (5,5,5) each day | 15 | Any non-repeating path works |
| Greedy fails | n=2, (100,1,1), (1,100,1) | 200 | Must alternate: A then B |
| Large n | n=10^5 | Check overflow | Use long long in C++ |

---

## When to Use This Pattern

### Use This Approach When:
- Choices have "no consecutive repeat" constraints
- You need to track "what was the last choice" as part of state
- The number of possible states (choices) is small and fixed

### Don't Use When:
- Constraint is "no repeat in last K days" for large K (state space explodes)
- Choices have complex interdependencies beyond just the previous step
- Problem can be solved greedily (no need for DP)

### Pattern Recognition Checklist:
- [ ] Cannot repeat same choice consecutively? -> **State Machine DP**
- [ ] Fixed number of states (like 3 activities)? -> **Track each state separately**
- [ ] Only previous decision matters? -> **Space optimization possible**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Frog 1](https://atcoder.jp/contests/dp/tasks/dp_a) | Basic 1D DP introduction |
| [Frog 2](https://atcoder.jp/contests/dp/tasks/dp_b) | DP with k choices |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Paint House](https://leetcode.com/problems/paint-house/) | Nearly identical - minimize cost instead |
| [House Robber](https://leetcode.com/problems/house-robber/) | Binary choice (rob or skip) |
| [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | State machine with hold/sold/cooldown |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Paint House II](https://leetcode.com/problems/paint-house-ii/) | K colors instead of 3, requires O(n*k) optimization |
| [House Robber II](https://leetcode.com/problems/house-robber-ii/) | Circular constraint adds complexity |

---

## Key Takeaways

1. **The Core Idea:** Track maximum achievable value for each possible ending state
2. **Time Optimization:** From O(2^n) brute force to O(n) by storing subproblem solutions
3. **Space Trade-off:** Can reduce from O(n) to O(1) since only previous row needed
4. **Pattern:** State Machine DP - when "last choice" affects current valid options

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why we need 3 DP states per day (not just 1)
- [ ] Implement the space-optimized O(1) version
- [ ] Recognize similar patterns in problems like House Robber and Paint House

---

## Additional Resources

- [AtCoder DP Contest Editorial](https://atcoder.jp/contests/dp)
- [CP-Algorithms: Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html)
- [CSES Grid Paths](https://cses.fi/problemset/task/1638) - Similar DP on sequential choices
