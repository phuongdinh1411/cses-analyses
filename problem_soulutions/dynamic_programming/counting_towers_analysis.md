---
layout: simple
title: "Counting Towers - State-Based Dynamic Programming"
permalink: /problem_soulutions/dynamic_programming/counting_towers_analysis
difficulty: Hard
tags: [dp, grid-dp, state-compression, counting]
prerequisites: [grid_paths]
cses_link: https://cses.fi/problemset/task/2413
---

# Counting Towers

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Count ways to fill a 2xN grid with blocks |
| Technique | State-based DP with transition counting |
| Key Insight | Track whether current row is "split" or "merged" |
| Time Complexity | O(N) per query |
| Space Complexity | O(N) for precomputation |
| Difficulty | Hard |

## Learning Goals

By completing this problem, you will learn:
- **State-based DP**: Defining states based on structural properties
- **Transition Analysis**: Systematically counting all valid transitions
- **State Compression**: Reducing complex configurations to simple states
- **Precomputation**: Handling multiple queries efficiently

## Problem Statement

Given a 2xN grid, count the number of ways to fill it with blocks. Each block can be:
- A 1x1 square
- A 1x2 horizontal rectangle
- A 2x1 vertical rectangle
- Or extend vertically across multiple rows

The key constraint: **blocks can span multiple rows vertically**, creating "towers" of varying heights.

**Input**: Number of test cases T, followed by T values of N
**Output**: For each N, the number of valid tower configurations modulo 10^9+7

**Constraints**:
- 1 <= T <= 10^5
- 1 <= N <= 10^6

### Example

```
Input:
3
1
2
6

Output:
2
8
2864
```

**For N = 1**:
```
Two configurations:

Config 1: Split      Config 2: Merged
+---+---+            +-------+
| A | B |            |   A   |
+---+---+            +-------+
(two 1x1 blocks)     (one 1x2 block)
```

**For N = 2**:
```
Eight configurations exist (see transition diagrams below)
```

## Key Insight: The Split/Merged State Model

The crucial insight is recognizing that at any row, only TWO states matter:

```
SPLIT STATE:                    MERGED STATE:
Two independent towers          One unified tower
+---+---+                       +-------+
| A | B |  <- separate         |   A   |  <- connected
+---+---+                       +-------+
```

**Why only these two states?**
- At each row boundary, the grid has width 2
- Either both columns are part of the SAME block (merged)
- Or each column belongs to a DIFFERENT block (split)

This dramatically simplifies the problem from exponential possibilities to just 2 states!

## DP States Definition

```
dp[i][0] = Number of ways to build towers of height i where row i is in SPLIT state
dp[i][1] = Number of ways to build towers of height i where row i is in MERGED state
```

**Visual representation**:
```
Row i in SPLIT state:           Row i in MERGED state:
       +---+---+                       +-------+
Row i  | ? | ? |                Row i  |   ?   |
       +---+---+                       +-------+
       (two separate                   (one connected
        blocks at top)                  block at top)
```

## State Transitions: The Core Logic

### From SPLIT State (4 ways to stay SPLIT, 1 way to go MERGED)

**SPLIT -> SPLIT (4 ways)**:

```
Way 1: Both columns extend up independently
       +---+---+
Row i  | | | | |  (vertical lines = same block as below)
       +---+---+
       | A | B |
       +---+---+
Row i-1

Way 2: Left extends, right starts new
       +---+---+
Row i  | | |   |
       +---+---+
       | A | B |
       +---+---+
Row i-1

Way 3: Right extends, left starts new
       +---+---+
Row i  |   | | |
       +---+---+
       | A | B |
       +---+---+
Row i-1

Way 4: Both start new blocks
       +---+---+
Row i  |   |   |
       +---+---+
       | A | B |
       +---+---+
Row i-1
```

**SPLIT -> MERGED (1 way)**:

```
Both columns merge into one horizontal block
       +-------+
Row i  |       |
       +---+---+
       | A | B |
       +---+---+
Row i-1

(Previous blocks A and B must terminate,
 new horizontal block spans both columns)
```

### From MERGED State (1 way to go SPLIT, 2 ways to stay MERGED)

**MERGED -> SPLIT (1 way)**:

```
Split the merged block into two separate blocks
       +---+---+
Row i  |   |   |
       +-------+
       |   A   |
       +-------+
Row i-1

(Previous merged block A terminates,
 two new blocks start)
```

**MERGED -> MERGED (2 ways)**:

```
Way 1: Merged block extends up
       +-------+
Row i  |   |   |  (single block continues)
       +-------+
       |   A   |
       +-------+
Row i-1

Way 2: New horizontal block starts
       +-------+
Row i  |       |
       +-------+
       |   A   |
       +-------+
Row i-1

(Previous block terminates,
 new horizontal block starts)
```

## Complete Transition Diagram

```
                    +-----+
                    | ROW |
                    |  i  |
                    +-----+
                   /       \
                  /         \
           SPLIT              MERGED
           STATE              STATE
          dp[i][0]           dp[i][1]
              |                   |
              |                   |
    +---------+---------+    +----+----+
    |         |         |    |         |
    v         v         v    v         v
  +---+     +---+     +---+ +---+     +---+
  |x4 |     |x1 |     |x1 | |x2 |     |x1 |
  +---+     +---+     +---+ +---+     +---+
    |         |         |    |         |
    v         v         v    v         v
 SPLIT     MERGED    SPLIT MERGED    SPLIT
dp[i-1][0] dp[i-1][0] dp[i-1][1] dp[i-1][1]


TRANSITIONS SUMMARY:
====================
SPLIT[i-1] --> SPLIT[i]:  4 ways
SPLIT[i-1] --> MERGED[i]: 1 way
MERGED[i-1] --> SPLIT[i]: 1 way
MERGED[i-1] --> MERGED[i]: 2 ways
```

## Recurrence Relations

Based on the transition analysis:

```
dp[i][0] = 4 * dp[i-1][0] + 1 * dp[i-1][1]
           ^^^^^^^^^^^^     ^^^^^^^^^^^^^
           SPLIT->SPLIT     MERGED->SPLIT
           (4 ways)         (1 way)

dp[i][1] = 1 * dp[i-1][0] + 2 * dp[i-1][1]
           ^^^^^^^^^^^^     ^^^^^^^^^^^^^
           SPLIT->MERGED    MERGED->MERGED
           (1 way)          (2 ways)
```

**In matrix form**:
```
[ dp[i][0] ]   [ 4  1 ]   [ dp[i-1][0] ]
[          ] = [      ] * [            ]
[ dp[i][1] ]   [ 1  2 ]   [ dp[i-1][1] ]
```

## Base Case

For N = 1 (single row):
```
dp[1][0] = 1    (one way: two separate 1x1 blocks)
dp[1][1] = 1    (one way: one horizontal 1x2 block)
```

**Verification**:
```
SPLIT (dp[1][0] = 1):        MERGED (dp[1][1] = 1):
+---+---+                    +-------+
| A | B |                    |   A   |
+---+---+                    +-------+
```

## Final Answer

```
Answer(N) = dp[N][0] + dp[N][1]
```

We sum both states because the topmost row can end in either configuration.

**Verification for N = 2**:
```
dp[2][0] = 4 * dp[1][0] + 1 * dp[1][1] = 4 * 1 + 1 * 1 = 5
dp[2][1] = 1 * dp[1][0] + 2 * dp[1][1] = 1 * 1 + 2 * 1 = 3
Answer(2) = 5 + 3 = 8  (matches expected output)
```

## Visual: All 8 Configurations for N = 2

```
SPLIT configurations (5 total):

1. Both extend    2. Left ext     3. Right ext    4. Both new     5. From merged
+---+---+         +---+---+       +---+---+       +---+---+       +---+---+
| | | | |         | | |   |       |   | | |       |   |   |       |   |   |
+---+---+         +---+---+       +---+---+       +---+---+       +-------+
| | | | |         | | |   |       |   | | |       |   |   |       |       |
+---+---+         +---+---+       +---+---+       +---+---+       +-------+


MERGED configurations (3 total):

6. From split     7. Extend       8. New horiz
+-------+         +-------+       +-------+
|       |         |   |   |       |       |
+---+---+         +-------+       +-------+
|   |   |         |       |       |       |
+---+---+         +-------+       +-------+
```

## Implementation

### Python Solution (with precomputation)

```python
def solve():
    MOD = 10**9 + 7
    MAX_N = 10**6 + 1

    # Precompute dp values for all N up to MAX_N
    # dp[i][0] = split state, dp[i][1] = merged state
    dp = [[0, 0] for _ in range(MAX_N)]

    # Base case: N = 1
    dp[1][0] = 1  # Two separate blocks
    dp[1][1] = 1  # One horizontal block

    # Fill DP table using recurrence
    for i in range(2, MAX_N):
        dp[i][0] = (4 * dp[i-1][0] + dp[i-1][1]) % MOD
        dp[i][1] = (dp[i-1][0] + 2 * dp[i-1][1]) % MOD

    # Process queries
    t = int(input())
    for _ in range(t):
        n = int(input())
        print((dp[n][0] + dp[n][1]) % MOD)

if __name__ == "__main__":
    solve()
```

### C++ Solution (Optimized)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;
const int MAXN = 1e6 + 1;

long long dp[MAXN][2];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    // Base case
    dp[1][0] = 1;  // split
    dp[1][1] = 1;  // merged

    // Precompute
    for (int i = 2; i < MAXN; i++) {
        dp[i][0] = (4 * dp[i-1][0] + dp[i-1][1]) % MOD;
        dp[i][1] = (dp[i-1][0] + 2 * dp[i-1][1]) % MOD;
    }

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;
        cout << (dp[n][0] + dp[n][1]) % MOD << "\n";
    }

    return 0;
}
```

### Space-Optimized Version (O(1) Space per Query)

```python
def count_towers(n):
    MOD = 10**9 + 7

    if n == 1:
        return 2

    # Only need previous row values
    split_prev = 1  # dp[1][0]
    merged_prev = 1  # dp[1][1]

    for i in range(2, n + 1):
        split_curr = (4 * split_prev + merged_prev) % MOD
        merged_curr = (split_prev + 2 * merged_prev) % MOD
        split_prev = split_curr
        merged_prev = merged_curr

    return (split_prev + merged_prev) % MOD
```

## Complexity Analysis

| Aspect | Precomputation | Per Query |
|--------|----------------|-----------|
| Time | O(N) | O(1) |
| Space | O(N) | O(1) |

**Why O(N) precomputation is optimal**:
- We have T queries (up to 10^5)
- Each N can be up to 10^6
- Precomputing all values once: O(10^6)
- Answering all queries: O(10^5)
- Total: O(10^6) instead of O(T * N) without precomputation

## Common Mistakes

### 1. Incorrect Transition Counts
```python
# WRONG: Forgetting some transitions
dp[i][0] = 2 * dp[i-1][0] + dp[i-1][1]  # Only counted 2 SPLIT->SPLIT

# CORRECT: All 4 SPLIT->SPLIT transitions
dp[i][0] = 4 * dp[i-1][0] + dp[i-1][1]
```

### 2. Missing Modulo Operation
```python
# WRONG: Overflow for large N
dp[i][0] = 4 * dp[i-1][0] + dp[i-1][1]

# CORRECT: Apply modulo at each step
dp[i][0] = (4 * dp[i-1][0] + dp[i-1][1]) % MOD
```

### 3. Wrong Base Case
```python
# WRONG: Starting from N = 0
dp[0][0] = 1
dp[0][1] = 0

# CORRECT: Start from N = 1 (minimum valid grid)
dp[1][0] = 1
dp[1][1] = 1
```

### 4. Confusing States
```python
# WRONG: Defining states by "number of blocks" instead of structure
# This leads to exponential states

# CORRECT: States are STRUCTURAL (split vs merged)
# Only 2 states needed regardless of N
```

### 5. Not Precomputing for Multiple Queries
```python
# WRONG: Computing for each query separately O(T*N)
for _ in range(t):
    n = int(input())
    # compute dp[1] to dp[n]...

# CORRECT: Precompute once, answer queries in O(1)
# Precompute dp[1] to dp[MAX_N]
for _ in range(t):
    n = int(input())
    print((dp[n][0] + dp[n][1]) % MOD)
```

## Related Problems

| Problem | Similarity | Key Difference |
|---------|------------|----------------|
| [Grid Paths](https://cses.fi/problemset/task/1638) | Grid DP | Fixed path, no state |
| [Rectangle Cutting](https://cses.fi/problemset/task/1744) | 2D DP | Minimization, not counting |
| [Domino Tiling](https://leetcode.com/problems/domino-and-tromino-tiling/) | Tile counting | Different tile shapes |

## Key Takeaways

1. **State Reduction**: Complex problems can often be reduced to few essential states
2. **Transition Analysis**: Systematically enumerate ALL ways to move between states
3. **Visual Verification**: Draw out small cases to verify transition counts
4. **Precomputation**: For multiple queries, precompute rather than recompute
5. **Matrix Form**: Linear recurrences can be expressed as matrix multiplication (useful for matrix exponentiation if needed)
