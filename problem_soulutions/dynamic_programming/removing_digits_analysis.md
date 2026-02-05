---
layout: simple
title: "Removing Digits"
permalink: /problem_soulutions/dynamic_programming/removing_digits_analysis
difficulty: Easy
tags: [dp, optimization, digit-dp]
prerequisites: []
cses_link: https://cses.fi/problemset/task/1637
---

# Removing Digits

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Given n, subtract one of its digits at each step. Find minimum steps to reach 0. |
| Input | A single integer n (1 <= n <= 10^6) |
| Output | Minimum number of operations to reduce n to 0 |
| Time Complexity | O(n * d) where d is the number of digits (~10) |
| Space Complexity | O(n) |
| Key Technique | Dynamic Programming / BFS |

## Learning Goals

After completing this problem, you will understand:
- **Digit extraction**: How to extract digits from a number using modulo and division
- **Optimization DP**: Finding minimum operations using bottom-up DP
- **BFS vs DP**: When to use BFS (unweighted shortest path) vs DP for optimization

## Problem Statement

Given an integer `n`, you want to reduce it to `0`. At each step, you may subtract one of the digits that appears in the current number.

**What is the minimum number of steps required?**

### Example

```
Input: n = 27

Output: 5

One optimal path:
27 -> 20 -> 18 -> 10 -> 9 -> 0

Steps breakdown:
1. 27 - 7 = 20  (subtract digit 7)
2. 20 - 2 = 18  (subtract digit 2)
3. 18 - 8 = 10  (subtract digit 8)
4. 10 - 1 = 9   (subtract digit 1)
5. 9 - 9 = 0    (subtract digit 9)

Total: 5 steps
```

## Intuition

Think of each number as a node in a graph. From any number, you can move to another number by subtracting one of its digits.

**Key insight**: At each number, we have multiple choices (subtract any non-zero digit). We want to find the minimum steps to reach 0.

This is a classic optimization problem that can be solved with:
1. **Dynamic Programming**: Build solutions from smaller subproblems
2. **BFS**: Treat as shortest path in an unweighted graph

**Greedy does NOT work**: Always subtracting the largest digit is not optimal.
- Example: For n=32, greedy gives 32->29->22->20->18->10->9->0 (7 steps)
- Optimal: 32->30->27->20->18->10->9->0 (7 steps) or other paths

## DP State Definition

```
dp[i] = minimum number of steps to reduce i to 0
```

**In plain language**: For each value from 0 to n, we compute the minimum operations needed to reach 0.

## State Transition

For each number `i`, try subtracting each of its non-zero digits `d`:

```
dp[i] = min(dp[i - d] + 1) for each digit d in i where d > 0
```

**Why this works**: If we subtract digit `d` from `i`, we reach `i - d`. The cost is `dp[i - d]` (already computed) plus 1 for this step.

## Base Case

```
dp[0] = 0  (we're already at 0, no steps needed)
```

## How to Extract Digits

```python
def get_digits(n):
    digits = []
    while n > 0:
        d = n % 10      # get last digit
        if d > 0:       # skip zeros
            digits.append(d)
        n //= 10        # remove last digit
    return digits
```

**Alternative using string conversion**:
```python
digits = [int(c) for c in str(n) if c != '0']
```

## Detailed Dry Run for n = 27

Building the DP table from 0 to 27:

```
i=0:  dp[0] = 0 (base case)

i=1:  digits = [1]
      dp[1] = dp[1-1] + 1 = dp[0] + 1 = 1

i=2:  digits = [2]
      dp[2] = dp[2-2] + 1 = dp[0] + 1 = 1

...

i=9:  digits = [9]
      dp[9] = dp[9-9] + 1 = dp[0] + 1 = 1

i=10: digits = [1] (0 is skipped)
      dp[10] = dp[10-1] + 1 = dp[9] + 1 = 2

i=11: digits = [1, 1]
      dp[11] = dp[11-1] + 1 = dp[10] + 1 = 3

i=18: digits = [1, 8]
      dp[18] = min(dp[18-1] + 1, dp[18-8] + 1)
             = min(dp[17] + 1, dp[10] + 1)
             = min(3, 3) = 3

i=20: digits = [2]
      dp[20] = dp[20-2] + 1 = dp[18] + 1 = 4

i=27: digits = [2, 7]
      dp[27] = min(dp[27-2] + 1, dp[27-7] + 1)
             = min(dp[25] + 1, dp[20] + 1)
             = min(5, 5) = 5
```

**Final answer**: dp[27] = 5

## Implementation

### Python Solution

```python
def removing_digits(n):
    """
    Find minimum steps to reduce n to 0 by subtracting its digits.

    Args:
        n: positive integer to reduce

    Returns:
        minimum number of steps
    """
    # dp[i] = minimum steps to reduce i to 0
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        dp[i] = float('inf')

        # Extract and try each digit
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit > 0:  # Skip zero digits
                dp[i] = min(dp[i], dp[i - digit] + 1)
            temp //= 10

    return dp[n]


# Read input and solve
n = int(input())
print(removing_digits(n))
```

#### Python (Alternative with String Conversion)

```python
def removing_digits_alt(n):
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        # Get non-zero digits using string conversion
        digits = [int(c) for c in str(i) if c != '0']
        dp[i] = min(dp[i - d] + 1 for d in digits)

    return dp[n]

n = int(input())
print(removing_digits_alt(n))
```

## Common Mistakes

### 1. Forgetting to Skip Digit 0
```python
# WRONG: includes 0 as a valid digit
digit = temp % 10
dp[i] = min(dp[i], dp[i - digit] + 1)  # Subtracting 0 is useless!

# CORRECT: skip zero digits
digit = temp % 10
if digit > 0:
    dp[i] = min(dp[i], dp[i - digit] + 1)
```

### 2. Not Initializing dp[i] Properly
```python
# WRONG: missing initialization
dp[i] = dp[i - digit] + 1  # First iteration has undefined dp[i]

# CORRECT: initialize to infinity first
dp[i] = float('inf')
dp[i] = min(dp[i], dp[i - digit] + 1)
```

### 3. Single Digit Edge Case
Single digit numbers (1-9) always need exactly 1 step (subtract themselves).
The solution handles this automatically since dp[d-d] = dp[0] = 0, so dp[d] = 1.

### 4. Off-by-One in Loop Range
```python
# WRONG: misses computing dp[n]
for i in range(1, n):

# CORRECT: include n
for i in range(1, n + 1):
```

## Alternative Approach: BFS

Since each operation has cost 1 (unweighted edges), BFS finds the shortest path:

```python
from collections import deque

def removing_digits_bfs(n):
    if n == 0:
        return 0

    visited = [False] * (n + 1)
    queue = deque([(n, 0)])  # (current number, steps)
    visited[n] = True

    while queue:
        curr, steps = queue.popleft()

        # Try each digit
        temp = curr
        while temp > 0:
            digit = temp % 10
            if digit > 0:
                next_num = curr - digit
                if next_num == 0:
                    return steps + 1
                if not visited[next_num]:
                    visited[next_num] = True
                    queue.append((next_num, steps + 1))
            temp //= 10

    return -1  # Should never reach here for valid input
```

**BFS vs DP Comparison**:
- Both have O(n * d) time complexity
- DP is simpler and more natural for this problem
- BFS is useful when you need to track the actual path

## Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n * d) where d = number of digits in i (at most 7 for n <= 10^6) |
| Space | O(n) for the DP array |

**Why O(n * d)?** For each number from 1 to n, we extract its digits (at most log10(n) digits).

## Related Problems

| Problem | Platform | Similarity |
|---------|----------|------------|
| [Coin Change](https://leetcode.com/problems/coin-change/) | LeetCode | Same DP pattern, different "coins" |
| [Perfect Squares](https://leetcode.com/problems/perfect-squares/) | LeetCode | Minimize steps, different choices |
| [Dice Combinations](https://cses.fi/problemset/task/1633) | CSES | Similar DP with fixed choices |
| [Minimizing Coins](https://cses.fi/problemset/task/1634) | CSES | Same pattern with coin denominations |

## Key Takeaways

1. **State definition is crucial**: dp[i] represents the minimum steps to reach 0 from i
2. **Build from smaller to larger**: We need dp[i-d] before computing dp[i]
3. **Skip invalid choices**: Zero digits don't help reduce the number
4. **Greedy fails**: Always taking the maximum digit is not optimal
5. **BFS alternative**: Unweighted shortest path problems can use BFS
