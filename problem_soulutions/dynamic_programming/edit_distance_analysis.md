---
layout: simple
title: "Edit Distance - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/edit_distance_analysis
difficulty: Medium
tags: [dp, string-dp, 2d-dp, edit-distance]
prerequisites: [grid_paths]
cses_link: https://cses.fi/problemset/task/1639
---

# Edit Distance (Levenshtein Distance)

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Convert string s1 to string s2 using minimum operations |
| Operations | Insert, Delete, Replace (each costs 1) |
| Input | Two strings s1 and s2 |
| Output | Minimum number of operations |
| Constraints | 1 <= |s1|, |s2| <= 5000 |
| Time Complexity | O(n * m) |
| Space Complexity | O(n * m), optimizable to O(min(n, m)) |

## Learning Goals

By solving this problem, you will learn:
- **String DP**: How to apply dynamic programming to string transformation problems
- **2D DP on Strings**: Building a DP table indexed by positions in two strings
- **Three Operations Pattern**: Handling insert, delete, and replace in a unified framework
- **Space Optimization**: Reducing 2D DP to 1D using rolling arrays

## Problem Statement

Given two strings, find the minimum number of operations needed to transform the first string into the second. The allowed operations are:
1. **Insert** a character
2. **Delete** a character
3. **Replace** a character

### Example

Transform "LOVE" to "MOVIE":

```
LOVE -> MOVIE

Step 1: Insert 'M' at beginning -> MLOVE
Step 2: Replace 'L' with 'O'    -> MOOVE
Step 3: Replace 'O' with 'V'    -> MOVVE
Step 4: Replace 'V' with 'I'    -> MOVIE

Answer: 4 operations
```

Alternative transformation:
```
LOVE -> MOVIE

Step 1: Insert 'M' at beginning -> MLOVE
Step 2: Insert 'O' after 'M'    -> MOLOVE
Step 3: Delete 'L'              -> MOOVE
Step 4: Replace second 'O' with 'I' -> MOIVE
Step 5: Replace 'E' with 'E'    -> MOVIE

This takes 4 operations (same minimum)
```

## Intuition

At each position when comparing characters from both strings, we have the following choices:

1. **Characters Match**: If s1[i-1] == s2[j-1], no operation needed - move diagonally
2. **Characters Differ**: Choose the minimum cost among:
   - **Replace**: Change s1[i-1] to s2[j-1] (cost 1)
   - **Delete**: Remove s1[i-1] from s1 (cost 1)
   - **Insert**: Add s2[j-1] to s1 (cost 1)

The key insight is that we can solve this optimally by building up solutions to smaller subproblems.

## DP State Definition

```
dp[i][j] = minimum number of operations to convert s1[0..i-1] to s2[0..j-1]
```

Where:
- `i` ranges from 0 to len(s1)
- `j` ranges from 0 to len(s2)
- `dp[0][0]` = 0 (empty string to empty string)
- `dp[len(s1)][len(s2)]` = our answer

## State Transition

```
If s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1]           # Match: no cost, move diagonal

Else:
    dp[i][j] = 1 + min(
        dp[i-1][j-1],                  # Replace s1[i-1] with s2[j-1]
        dp[i-1][j],                    # Delete s1[i-1]
        dp[i][j-1]                     # Insert s2[j-1] into s1
    )
```

### Understanding Each Transition

| Operation | From State | Meaning |
|-----------|------------|---------|
| Replace | dp[i-1][j-1] + 1 | Convert s1[0..i-2] to s2[0..j-2], then replace s1[i-1] |
| Delete | dp[i-1][j] + 1 | Convert s1[0..i-2] to s2[0..j-1], then delete s1[i-1] |
| Insert | dp[i][j-1] + 1 | Convert s1[0..i-1] to s2[0..j-2], then insert s2[j-1] |

## Base Cases

```
dp[i][0] = i    # Delete all i characters from s1 to get empty string
dp[0][j] = j    # Insert all j characters to get s2 from empty string
```

## Visual DP Table

For s1 = "LOVE" and s2 = "MOVIE":

```
        ""   M    O    V    I    E
    +----+----+----+----+----+----+
 "" |  0 |  1 |  2 |  3 |  4 |  5 |
    +----+----+----+----+----+----+
  L |  1 |  1 |  2 |  3 |  4 |  5 |
    +----+----+----+----+----+----+
  O |  2 |  2 |  1 |  2 |  3 |  4 |
    +----+----+----+----+----+----+
  V |  3 |  3 |  2 |  1 |  2 |  3 |
    +----+----+----+----+----+----+
  E |  4 |  4 |  3 |  2 |  2 |  2 |
    +----+----+----+----+----+----+

Answer: dp[4][5] = 2
```

Wait, let me recalculate more carefully:

```
s1 = "LOVE" (length 4)
s2 = "MOVIE" (length 5)

        ""   M    O    V    I    E
    +----+----+----+----+----+----+
 "" |  0 |  1 |  2 |  3 |  4 |  5 |  <- Insert j chars
    +----+----+----+----+----+----+
  L |  1 |  1 |  2 |  3 |  4 |  5 |
    +----+----+----+----+----+----+
  O |  2 |  2 |  1 |  2 |  3 |  4 |  <- O matches O
    +----+----+----+----+----+----+
  V |  3 |  3 |  2 |  1 |  2 |  3 |  <- V matches V
    +----+----+----+----+----+----+
  E |  4 |  4 |  3 |  2 |  2 |  2 |  <- E matches E
    +----+----+----+----+----+----+
     ^
     Delete i chars

Answer: dp[4][5] = 2
```

## Detailed Dry Run

Let's trace through a smaller example: s1 = "CAT", s2 = "CUT"

**Initialization:**
```
        ""   C    U    T
    +----+----+----+----+
 "" |  0 |  1 |  2 |  3 |
    +----+----+----+----+
  C |  1 |    |    |    |
    +----+----+----+----+
  A |  2 |    |    |    |
    +----+----+----+----+
  T |  3 |    |    |    |
    +----+----+----+----+
```

**Step-by-step filling:**

dp[1][1]: s1[0]='C', s2[0]='C' -> Match! dp[1][1] = dp[0][0] = 0

dp[1][2]: s1[0]='C', s2[1]='U' -> Different
  - Replace: dp[0][1] + 1 = 2
  - Delete:  dp[0][2] + 1 = 3
  - Insert:  dp[1][1] + 1 = 1
  - dp[1][2] = min(2,3,1) = 1

dp[1][3]: s1[0]='C', s2[2]='T' -> Different
  - Replace: dp[0][2] + 1 = 3
  - Delete:  dp[0][3] + 1 = 4
  - Insert:  dp[1][2] + 1 = 2
  - dp[1][3] = min(3,4,2) = 2

dp[2][1]: s1[1]='A', s2[0]='C' -> Different
  - Replace: dp[1][0] + 1 = 2
  - Delete:  dp[1][1] + 1 = 1
  - Insert:  dp[2][0] + 1 = 3
  - dp[2][1] = min(2,1,3) = 1

dp[2][2]: s1[1]='A', s2[1]='U' -> Different
  - Replace: dp[1][1] + 1 = 1
  - Delete:  dp[1][2] + 1 = 2
  - Insert:  dp[2][1] + 1 = 2
  - dp[2][2] = min(1,2,2) = 1

dp[2][3]: s1[1]='A', s2[2]='T' -> Different
  - Replace: dp[1][2] + 1 = 2
  - Delete:  dp[1][3] + 1 = 3
  - Insert:  dp[2][2] + 1 = 2
  - dp[2][3] = min(2,3,2) = 2

dp[3][1]: s1[2]='T', s2[0]='C' -> Different
  - Replace: dp[2][0] + 1 = 3
  - Delete:  dp[2][1] + 1 = 2
  - Insert:  dp[3][0] + 1 = 4
  - dp[3][1] = min(3,2,4) = 2

dp[3][2]: s1[2]='T', s2[1]='U' -> Different
  - Replace: dp[2][1] + 1 = 2
  - Delete:  dp[2][2] + 1 = 2
  - Insert:  dp[3][1] + 1 = 3
  - dp[3][2] = min(2,2,3) = 2

dp[3][3]: s1[2]='T', s2[2]='T' -> Match! dp[3][3] = dp[2][2] = 1

**Final Table:**
```
        ""   C    U    T
    +----+----+----+----+
 "" |  0 |  1 |  2 |  3 |
    +----+----+----+----+
  C |  1 |  0 |  1 |  2 |
    +----+----+----+----+
  A |  2 |  1 |  1 |  2 |
    +----+----+----+----+
  T |  3 |  2 |  2 |  1 |
    +----+----+----+----+

Answer: 1 (Replace 'A' with 'U')
```

## Implementation

### Python Solution

```python
def edit_distance(s1: str, s2: str) -> int:
  """
  Calculate minimum edit distance between two strings.

  Args:
    s1: Source string
    s2: Target string

  Returns:
    Minimum number of operations (insert, delete, replace)
  """
  m, n = len(s1), len(s2)

  # Create DP table
  dp = [[0] * (n + 1) for _ in range(m + 1)]

  # Base cases
  for i in range(m + 1):
    dp[i][0] = i  # Delete all chars from s1
  for j in range(n + 1):
    dp[0][j] = j  # Insert all chars to make s2

  # Fill DP table
  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if s1[i-1] == s2[j-1]:
        dp[i][j] = dp[i-1][j-1]  # Match: no cost
      else:
        dp[i][j] = 1 + min(
          dp[i-1][j-1],  # Replace
          dp[i-1][j],    # Delete
          dp[i][j-1]     # Insert
        )

  return dp[m][n]


# Example usage
if __name__ == "__main__":
  s1 = input()
  s2 = input()
  print(edit_distance(s1, s2))
```

### Space Optimization

We can reduce space from O(m * n) to O(min(m, n)) by using two rows instead of the full table.

### Optimized Python Solution

```python
def edit_distance_optimized(s1: str, s2: str) -> int:
  """
  Space-optimized edit distance using O(min(m, n)) space.
  """
  # Ensure s2 is the shorter string for space optimization
  if len(s1) < len(s2):
    s1, s2 = s2, s1

  m, n = len(s1), len(s2)

  # Use two rows instead of full table
  prev = list(range(n + 1))
  curr = [0] * (n + 1)

  for i in range(1, m + 1):
    curr[0] = i  # Base case: delete i chars

    for j in range(1, n + 1):
      if s1[i-1] == s2[j-1]:
        curr[j] = prev[j-1]  # Match
      else:
        curr[j] = 1 + min(
          prev[j-1],  # Replace
          prev[j],    # Delete
          curr[j-1]   # Insert
        )

    prev, curr = curr, prev

  return prev[n]
```

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| 0-indexed confusion | Accessing s1[i] instead of s1[i-1] | Remember dp indices are 1-based, string indices are 0-based |
| Wrong base cases | Starting dp[0][0] = 1 or missing initialization | dp[i][0] = i, dp[0][j] = j |
| Incorrect transition order | Mixing up which operation is which | Draw the table and trace carefully |
| Space optimization bug | Not saving diagonal value before overwriting | Use temporary variable or two-row approach |
| Off-by-one errors | Wrong loop bounds | Loop from 1 to length inclusive |

## Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Basic DP | O(m * n) | O(m * n) |
| Space Optimized | O(m * n) | O(min(m, n)) |

## Related Problems

### CSES Problems
- [Longest Common Subsequence](https://cses.fi/problemset/task/1639) - Similar 2D string DP
- [Grid Paths](https://cses.fi/problemset/task/1638) - 2D DP foundation

### LeetCode Problems
- [72. Edit Distance](https://leetcode.com/problems/edit-distance/) - Same problem
- [583. Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) - Variant with only delete
- [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) - Related string DP
- [161. One Edit Distance](https://leetcode.com/problems/one-edit-distance/) - Check if exactly one edit apart

## Key Takeaways

1. **State Design**: dp[i][j] represents converting prefix of s1 to prefix of s2
2. **Three Operations**: Insert, Delete, Replace each come from different previous states
3. **Base Cases**: Converting to/from empty string requires length operations
4. **Space Optimization**: Only need previous row to compute current row
5. **Pattern Recognition**: Many string DP problems follow similar 2D table structure
