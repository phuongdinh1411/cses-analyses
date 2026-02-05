---
layout: simple
title: "Array Description"
permalink: /problem_soulutions/dynamic_programming/array_description_analysis
difficulty: Medium
tags: [dp, 2d-dp, counting, state-machine]
prerequisites: [dice_combinations]
cses_link: https://cses.fi/problemset/task/1746
---

# Array Description

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Fill unknown array elements (marked as 0) with values 1 to m |
| Constraint | Adjacent elements must differ by at most 1 |
| Goal | Count valid ways to fill the array (mod 10^9+7) |
| Input | n (length), m (max value), array of n integers |
| Output | Number of valid fillings |

## Learning Goals

- Implement 2D DP where state tracks both position and value
- Handle constraints between adjacent elements in DP transitions
- Optimize space from O(n*m) to O(m) using rolling arrays

## Problem Statement

Given an array of n integers where each element is either:
- A known value between 1 and m (inclusive)
- Unknown, represented by 0

Count the number of ways to replace all zeros with values from 1 to m such that the absolute difference between any two adjacent elements is at most 1.

### Example

**Input:**
```
n = 3, m = 2
array = [0, 1, 0]
```

**Output:** `4`

**Explanation:**
Valid arrays after filling zeros:
1. `[1, 1, 1]` - differences: |1-1|=0, |1-1|=0
2. `[1, 1, 2]` - differences: |1-1|=0, |1-2|=1
3. `[2, 1, 1]` - differences: |2-1|=1, |1-1|=0
4. `[2, 1, 2]` - differences: |2-1|=1, |1-2|=1

Position 0 can be 1 or 2 (both differ from fixed value 1 by at most 1).
Position 2 can be 1 or 2 (both differ from fixed value 1 by at most 1).
Total: 2 x 2 = 4 valid ways.

## Intuition

We need to track:
1. Which position we're at in the array
2. What value we assign to that position

This leads to: **dp[i][v] = number of ways to fill positions 0 to i such that position i has value v**

The key insight is that the value at position i only depends on the value at position i-1 (adjacent constraint), making this a classic 2D DP problem.

## DP State Definition

```
dp[i][v] = number of valid ways to fill array[0..i] where array[i] = v
```

Where:
- `i` ranges from 0 to n-1 (array positions)
- `v` ranges from 1 to m (possible values)

## State Transition

### Case 1: array[i] is known (not 0)
Only one value is allowed at position i:
```
dp[i][array[i]] = dp[i-1][array[i]-1] + dp[i-1][array[i]] + dp[i-1][array[i]+1]
```
All other dp[i][v] = 0 for v != array[i]

### Case 2: array[i] is unknown (0)
Any value from 1 to m is allowed:
```
for v in 1..m:
    dp[i][v] = dp[i-1][v-1] + dp[i-1][v] + dp[i-1][v+1]
```

**Important:** Handle boundary cases where v-1 < 1 or v+1 > m (those terms are 0).

## Base Case

For position 0:
- If `array[0] == 0`: `dp[0][v] = 1` for all v from 1 to m
- If `array[0] != 0`: `dp[0][array[0]] = 1`, all others are 0

## Answer

```
answer = sum(dp[n-1][v]) for v from 1 to m
```

## Detailed Dry Run

**Input:** n=4, m=3, array=[1, 0, 2, 0]

### Initialization (i=0, array[0]=1)

| v | dp[0][v] |
|---|----------|
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |

### i=1 (array[1]=0, unknown)
For each v, sum adjacent values from previous row:

| v | dp[0][v-1] | dp[0][v] | dp[0][v+1] | dp[1][v] |
|---|------------|----------|------------|----------|
| 1 | 0 | 1 | 0 | 1 |
| 2 | 1 | 0 | 0 | 1 |
| 3 | 0 | 0 | 0 | 0 |

### i=2 (array[2]=2, known)
Only v=2 can be filled:

| v | dp[1][v-1] | dp[1][v] | dp[1][v+1] | dp[2][v] |
|---|------------|----------|------------|----------|
| 1 | - | - | - | 0 |
| 2 | 1 | 1 | 0 | 2 |
| 3 | - | - | - | 0 |

### i=3 (array[3]=0, unknown)

| v | dp[2][v-1] | dp[2][v] | dp[2][v+1] | dp[3][v] |
|---|------------|----------|------------|----------|
| 1 | 0 | 0 | 2 | 2 |
| 2 | 0 | 2 | 0 | 2 |
| 3 | 2 | 0 | 0 | 2 |

**Answer:** dp[3][1] + dp[3][2] + dp[3][3] = 2 + 2 + 2 = **6**

## Python Implementation

```python
def array_description(n: int, m: int, array: list) -> int:
  MOD = 10**9 + 7

  # dp[v] = ways to reach current position with value v
  dp = [0] * (m + 2)  # Extra space for boundary handling

  # Base case: first position
  if array[0] == 0:
    for v in range(1, m + 1):
      dp[v] = 1
  else:
    dp[array[0]] = 1

  # Fill remaining positions
  for i in range(1, n):
    new_dp = [0] * (m + 2)

    if array[i] == 0:
      # Unknown: try all values
      for v in range(1, m + 1):
        new_dp[v] = (dp[v-1] + dp[v] + dp[v+1]) % MOD
    else:
      # Known: only one value allowed
      v = array[i]
      new_dp[v] = (dp[v-1] + dp[v] + dp[v+1]) % MOD

    dp = new_dp

  # Sum all ways for final position
  return sum(dp[1:m+1]) % MOD


# Example usage
if __name__ == "__main__":
  print(array_description(3, 2, [0, 1, 0]))  # Output: 4
  print(array_description(4, 3, [1, 0, 2, 0]))  # Output: 6
```

## Space Optimization

The standard 2D DP uses O(n*m) space. Since each row only depends on the previous row, we optimize to O(m):

**Before (2D):**
```python
dp = [[0] * (m + 1) for _ in range(n)]
```

**After (1D with rolling):**
```python
dp = [0] * (m + 2)      # Current row
new_dp = [0] * (m + 2)  # Next row
```

This reduces memory from O(n*m) to O(m), which is crucial when n can be up to 10^5.

## Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O(n * m) |
| Space | O(m) with optimization |

- For each position (n), we compute at most m values
- Each value computation is O(1) - just sum three adjacent values

## Common Mistakes

### 1. Boundary Handling for v=1 and v=m
**Wrong:**
```python
dp[i][v] = dp[i-1][v-1] + dp[i-1][v] + dp[i-1][v+1]  # Index out of bounds!
```

**Correct:** Use padding or explicit checks:
```python
# Padding approach (recommended)
dp = [0] * (m + 2)  # dp[0] and dp[m+1] are always 0

# Or explicit check
for delta in [-1, 0, 1]:
  if 1 <= v + delta <= m:
    new_dp[v] += dp[v + delta]
```

### 2. Forgetting Modulo in Intermediate Sums
```python
# Wrong: overflow before modulo
new_dp[v] = (dp[v-1] + dp[v] + dp[v+1]) % MOD

# Better for C++ (use long long)
new_dp[v] = ((long long)dp[v-1] + dp[v] + dp[v+1]) % MOD
```

### 3. Not Handling Fixed Values Correctly
When array[i] != 0, only dp[i][array[i]] should be updated:
```python
# Wrong: updating all values when position is fixed
if array[i] != 0:
  for v in range(1, m + 1):  # Should only update array[i]
    ...
```

### 4. Edge Case: First Element is Fixed
If array[0] is a known value that's invalid (> m), the answer should be 0.

## Related Problems

| Problem | Similarity | Key Difference |
|---------|------------|----------------|
| [Dice Combinations](https://cses.fi/problemset/task/1633) | 1D counting DP | No adjacency constraint |
| [Edit Distance](https://cses.fi/problemset/task/1639) | 2D DP with transitions | Different transition rules |
| [Longest Increasing Subsequence](https://cses.fi/problemset/task/1145) | 1D DP with constraints | Subsequence, not adjacent |
| [Rectangle Cutting](https://cses.fi/problemset/task/1744) | 2D state DP | Different state meaning |

### LeetCode Similar Problems
- [House Robber](https://leetcode.com/problems/house-robber/) - Adjacent constraints
- [Paint House](https://leetcode.com/problems/paint-house/) - State-based transitions
- [Decode Ways](https://leetcode.com/problems/decode-ways/) - Counting with constraints
