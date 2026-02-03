---
difficulty: Easy
tags: [dp, 2d-dp, grid, counting]
prerequisites: [dice_combinations]
cses_link: https://cses.fi/problemset/task/1638
---

# Grid Paths

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Count paths from top-left to bottom-right in a grid with obstacles |
| Input | n x n grid where '.' is empty and '*' is a trap |
| Output | Number of valid paths modulo 10^9 + 7 |
| Constraints | 1 <= n <= 1000 |
| Movements | Only right or down |

## Learning Goals

After solving this problem, you will understand:
- **2D Dynamic Programming**: Building solutions on a grid structure
- **Handling Obstacles**: Incorporating blocked cells into DP transitions
- **Grid Traversal Counting**: Counting paths with restricted movements

## Problem Statement

Given an n x n grid, count the number of paths from the top-left corner (1,1) to the bottom-right corner (n,n). You can only move right or down. Some cells contain traps marked with '*' which cannot be visited. Print the answer modulo 10^9 + 7.

**Example Input:**
```
4
....
.*..
..*.
....
```

**Example Output:**
```
3
```

## Intuition

The key insight is that to reach any cell (i,j), you must come from either:
- The cell above: (i-1, j)
- The cell to the left: (i, j-1)

Therefore, the number of ways to reach (i,j) is the sum of ways to reach both neighboring cells - **unless** (i,j) is a trap, in which case there are 0 ways to reach it.

```
dp[i][j] = dp[i-1][j] + dp[i][j-1]  (if not a trap)
dp[i][j] = 0                         (if trap '*')
```

## DP State Definition

**`dp[i][j]`** = Number of distinct paths from (0,0) to cell (i,j)

- `i` represents the row index (0 to n-1)
- `j` represents the column index (0 to n-1)
- Final answer is `dp[n-1][n-1]`

## State Transition

```
if grid[i][j] == '*':
    dp[i][j] = 0
else:
    dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

Handle boundaries:
- If `i == 0`: can only come from left, so `dp[0][j] = dp[0][j-1]`
- If `j == 0`: can only come from above, so `dp[i][0] = dp[i-1][0]`

## Base Case

```
dp[0][0] = 1  if grid[0][0] != '*'
dp[0][0] = 0  if grid[0][0] == '*'
```

## Visual Diagram

For a 4x4 grid with traps at (1,1) and (2,2):

```
Grid:               DP Table:
. . . .             1  1  1  1
. * . .             1  0  1  2
. . * .             1  1  0  2
. . . .             1  2  2  4

Legend: '*' = trap (0 paths)
```

How DP values are computed:
```
dp[0][0] = 1 (start)
dp[0][1] = dp[0][0] = 1
dp[0][2] = dp[0][1] = 1
dp[0][3] = dp[0][2] = 1

dp[1][0] = dp[0][0] = 1
dp[1][1] = 0 (trap!)
dp[1][2] = dp[0][2] + dp[1][1] = 1 + 0 = 1
dp[1][3] = dp[0][3] + dp[1][2] = 1 + 1 = 2

dp[2][0] = dp[1][0] = 1
dp[2][1] = dp[1][1] + dp[2][0] = 0 + 1 = 1
dp[2][2] = 0 (trap!)
dp[2][3] = dp[1][3] + dp[2][2] = 2 + 0 = 2

dp[3][0] = dp[2][0] = 1
dp[3][1] = dp[2][1] + dp[3][0] = 1 + 1 = 2
dp[3][2] = dp[2][2] + dp[3][1] = 0 + 2 = 2
dp[3][3] = dp[2][3] + dp[3][2] = 2 + 2 = 4
```

## Detailed Dry Run (3x3 Example)

**Input:**
```
3
.*.
...
...
```

**Step-by-step execution:**

| Step | Cell | Grid Value | Calculation | dp[i][j] |
|------|------|------------|-------------|----------|
| 1 | (0,0) | '.' | Base case | 1 |
| 2 | (0,1) | '*' | Trap | 0 |
| 3 | (0,2) | '.' | dp[0][1] = 0 | 0 |
| 4 | (1,0) | '.' | dp[0][0] = 1 | 1 |
| 5 | (1,1) | '.' | dp[0][1] + dp[1][0] = 0 + 1 | 1 |
| 6 | (1,2) | '.' | dp[0][2] + dp[1][1] = 0 + 1 | 1 |
| 7 | (2,0) | '.' | dp[1][0] = 1 | 1 |
| 8 | (2,1) | '.' | dp[1][1] + dp[2][0] = 1 + 1 | 2 |
| 9 | (2,2) | '.' | dp[1][2] + dp[2][1] = 1 + 2 | 3 |

**Answer: 3 paths**

## Python Solution

```python
def solve():
    MOD = 10**9 + 7
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    # Edge case: start or end is a trap
    if grid[0][0] == '*' or grid[n-1][n-1] == '*':
        print(0)
        return

    # Initialize DP table
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1

    # Fill DP table row by row
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '*':
                dp[i][j] = 0
            elif i == 0 and j == 0:
                continue  # Already initialized
            else:
                from_top = dp[i-1][j] if i > 0 else 0
                from_left = dp[i][j-1] if j > 0 else 0
                dp[i][j] = (from_top + from_left) % MOD

    print(dp[n-1][n-1])

solve()
```

## C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    vector<string> grid(n);
    for (int i = 0; i < n; i++) {
        cin >> grid[i];
    }

    // Edge case: start or end is a trap
    if (grid[0][0] == '*' || grid[n-1][n-1] == '*') {
        cout << 0 << endl;
        return 0;
    }

    // Initialize DP table
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    dp[0][0] = 1;

    // Fill DP table
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == '*') {
                dp[i][j] = 0;
            } else if (i == 0 && j == 0) {
                continue;  // Already initialized
            } else {
                long long from_top = (i > 0) ? dp[i-1][j] : 0;
                long long from_left = (j > 0) ? dp[i][j-1] : 0;
                dp[i][j] = (from_top + from_left) % MOD;
            }
        }
    }

    cout << dp[n-1][n-1] << endl;
    return 0;
}
```

## Space Optimization

The 2D solution uses O(n^2) space. Since we only need the previous row to compute the current row, we can optimize to O(n) space using a 1D array:

```python
def solve_optimized():
    MOD = 10**9 + 7
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    if grid[0][0] == '*' or grid[n-1][n-1] == '*':
        print(0)
        return

    # 1D DP array
    dp = [0] * n
    dp[0] = 1

    for i in range(n):
        for j in range(n):
            if grid[i][j] == '*':
                dp[j] = 0
            elif j > 0:
                dp[j] = (dp[j] + dp[j-1]) % MOD

    print(dp[n-1])
```

**Space optimization explanation:**
- `dp[j]` stores the value from the previous row (from_top)
- `dp[j-1]` stores the already-updated value from current row (from_left)
- We update in-place from left to right

## Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| 2D DP | O(n^2) | O(n^2) |
| 1D DP (optimized) | O(n^2) | O(n) |

## Common Mistakes

1. **Forgetting modulo operation**: Always apply `% MOD` after each addition to prevent overflow.

2. **Not checking start/end for traps**: If `grid[0][0]` or `grid[n-1][n-1]` is a trap, the answer is 0 immediately.

3. **0-indexed vs 1-indexed confusion**: The problem states (1,1) to (n,n), but arrays are 0-indexed. Be consistent.

4. **Integer overflow in C++**: Use `long long` for the DP table, not `int`.

5. **Incorrect boundary handling**: First row can only receive paths from the left; first column only from above.

```cpp
// Wrong: forgetting to check if trap blocks the entire row/column
dp[0][j] = dp[0][j-1];  // Should be 0 if any previous cell was a trap

// Correct approach: let the main loop handle it naturally
```

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| [Unique Paths](https://leetcode.com/problems/unique-paths/) | LeetCode | No obstacles, pure counting |
| [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | LeetCode | Same as this problem |
| [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | LeetCode | Minimize sum instead of counting |
| [Dungeon Game](https://leetcode.com/problems/dungeon-game/) | LeetCode | DP from end to start |

## Summary

Grid Paths is a foundational 2D DP problem that teaches:
- Building DP solutions on grid structures
- Handling obstacles by setting blocked states to 0
- The importance of modular arithmetic for counting problems
- Space optimization from 2D to 1D arrays

The core recurrence `dp[i][j] = dp[i-1][j] + dp[i][j-1]` appears in many grid-based DP problems, making this an essential pattern to master.
