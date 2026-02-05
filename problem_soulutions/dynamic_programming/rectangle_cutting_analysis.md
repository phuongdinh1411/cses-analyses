---
layout: simple
title: "Rectangle Cutting"
permalink: /problem_soulutions/dynamic_programming/rectangle_cutting_analysis
difficulty: Medium
tags: [dp, 2d-dp, interval-dp, optimization]
prerequisites: [minimizing_coins]
cses_link: https://cses.fi/problemset/task/1744
---

# Rectangle Cutting

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Divide an a x b rectangle into squares using minimum cuts |
| Input | Two integers a, b (dimensions of rectangle) |
| Output | Minimum number of cuts needed |
| Constraints | 1 <= a, b <= 500 |
| Core Technique | 2D Dynamic Programming |

## Learning Goals

By solving this problem, you will learn:
- **2D Optimization DP**: Building a DP table indexed by two dimensions (width and height)
- **Trying All Split Points**: Systematically evaluating all possible horizontal and vertical cut positions
- **Interval DP Pattern**: Recognizing problems where you split a structure and combine subproblem results

## Problem Statement

Given an a x b rectangle, find the minimum number of cuts needed to divide it into squares.

### Example: 2 x 3 Rectangle

```
Initial 2x3 rectangle:
+---+---+---+

|           |
+---+---+---+

Cut 1: Vertical cut after column 2 -> creates 2x2 and 2x1
+---+---+   +---+

|       |   |   |
+---+---+   +---+

Cut 2: Horizontal cut on 2x1 -> creates two 1x1 squares
+---+---+   +---+

|       |   |   |
+---+---+   +---+
            +---+
            |   |
            +---+

Total: 2 cuts
```

## Key Insight

**If a == b, the rectangle is already a square - 0 cuts needed.**

For non-square rectangles, we must make at least one cut. Each cut divides the rectangle into two smaller rectangles, which we then solve recursively.

### Cut Options

1. **Horizontal cut at row i**: Divides a x b into a x i and a x (b-i)
2. **Vertical cut at column j**: Divides a x b into j x b and (a-j) x b

We try all possible cut positions and take the minimum.

## DP State Definition

```
dp[a][b] = minimum number of cuts to divide an a x b rectangle into squares
```

### State Transition

For each rectangle of size a x b (where a != b):

```
dp[a][b] = min(
    // Try all horizontal cuts at row i (1 <= i < b)
    min(dp[a][i] + dp[a][b-i] + 1) for i in range(1, b),

    // Try all vertical cuts at column j (1 <= j < a)
    min(dp[j][b] + dp[a-j][b] + 1) for j in range(1, a)
)
```

**Important**: The `+1` accounts for the cut itself!

### Base Case

```
dp[k][k] = 0  for all k (a square needs no cuts)
```

## Detailed Dry Run: 2 x 3 Rectangle

### Building the DP Table

| (a,b) | Calculation | Result |
|-------|-------------|--------|
| dp[1][1] | Base case (square) | 0 |
| dp[1][2] | Horizontal cut: dp[1][1] + dp[1][1] + 1 = 0 + 0 + 1 | 1 |
| dp[1][3] | min(dp[1][1]+dp[1][2]+1, dp[1][2]+dp[1][1]+1) = min(2, 2) | 2 |
| dp[2][1] | Vertical cut: dp[1][1] + dp[1][1] + 1 = 0 + 0 + 1 | 1 |
| dp[2][2] | Base case (square) | 0 |
| dp[2][3] | See detailed calculation below | 2 |
| dp[3][3] | Base case (square) | 0 |

### Calculating dp[2][3]

**Horizontal cuts (cut at row i):**
- i=1: dp[2][1] + dp[2][2] + 1 = 1 + 0 + 1 = 2
- i=2: dp[2][2] + dp[2][1] + 1 = 0 + 1 + 1 = 2

**Vertical cut (cut at column j):**
- j=1: dp[1][3] + dp[1][3] + 1 = 2 + 2 + 1 = 5

**Minimum: dp[2][3] = 2**

## Solution Code

### Python

```python
def rectangle_cutting(a: int, b: int) -> int:
  """
  Find minimum cuts to divide an a x b rectangle into squares.

  Args:
    a: width of rectangle
    b: height of rectangle

  Returns:
    Minimum number of cuts needed
  """
  # Initialize DP table with infinity
  INF = float('inf')
  dp = [[INF] * (b + 1) for _ in range(a + 1)]

  # Fill DP table
  for i in range(1, a + 1):
    for j in range(1, b + 1):
      # Base case: square needs no cuts
      if i == j:
        dp[i][j] = 0
        continue

      # Try all horizontal cuts (cut at row k)
      for k in range(1, j):
        dp[i][j] = min(dp[i][j], dp[i][k] + dp[i][j - k] + 1)

      # Try all vertical cuts (cut at column k)
      for k in range(1, i):
        dp[i][j] = min(dp[i][j], dp[k][j] + dp[i - k][j] + 1)

  return dp[a][b]


# Read input and solve
if __name__ == "__main__":
  a, b = map(int, input().split())
  print(rectangle_cutting(a, b))
```

## Common Mistakes

### 1. Forgetting the +1 for the Cut Itself

**Wrong:**
```python
dp[i][j] = min(dp[i][j], dp[i][k] + dp[i][j - k])  # Missing +1!
```

**Correct:**
```python
dp[i][j] = min(dp[i][j], dp[i][k] + dp[i][j - k] + 1)
```

Each cut operation must be counted!

### 2. Not Handling the Square Base Case

**Wrong:**
```python
# Treating all rectangles the same, even squares
for k in range(1, j):
  dp[i][j] = min(dp[i][j], dp[i][k] + dp[i][j - k] + 1)
```

**Correct:**
```python
if i == j:
  dp[i][j] = 0
  continue  # Skip to next iteration
```

Squares require 0 cuts - they're already the goal state!

### 3. Wrong Loop Bounds

**Wrong:**
```python
for k in range(j):  # Includes k=0 which is invalid
```

**Correct:**
```python
for k in range(1, j):  # k from 1 to j-1
```

Cut position must be strictly between 0 and the dimension.

## Complexity Analysis

| Metric | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(a * b * (a + b)) | For each of O(a*b) states, we try O(a+b) cut positions |
| Space | O(a * b) | DP table storing results for all rectangle sizes |

### Why O(a * b * (a + b))?

- **States**: a * b different rectangle dimensions
- **Transitions per state**: (a - 1) vertical cuts + (b - 1) horizontal cuts = O(a + b)
- **Total**: O(a * b * (a + b))

For the maximum constraints (a = b = 500):
- Operations: 500 * 500 * 1000 = 250,000,000
- This is tight but acceptable for most judges

## Related Problems

| Problem | Platform | Key Similarity |
|---------|----------|----------------|
| [Minimizing Coins](https://cses.fi/problemset/task/1634) | CSES | Minimization DP, trying all options |
| [Coin Combinations I](https://cses.fi/problemset/task/1635) | CSES | DP with optimization |
| [Minimum Cost to Cut a Stick](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/) | LeetCode | Interval DP, optimal cutting |
| [Matrix Chain Multiplication](https://www.geeksforgeeks.org/matrix-chain-multiplication-dp-8/) | Classic | 2D interval DP pattern |

## Summary

The Rectangle Cutting problem teaches a fundamental 2D DP pattern:

1. **Define state** by the rectangle dimensions dp[a][b]
2. **Identify base case** - squares need 0 cuts
3. **Try all split points** - both horizontal and vertical
4. **Combine subproblems** and add 1 for the cut itself
5. **Take minimum** over all options

This pattern extends to many optimization problems where you split a structure and combine solutions to subproblems.
