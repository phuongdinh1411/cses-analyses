---
layout: simple
title: "Filled Subgrid Count I - Grid Counting Problem"
permalink: /problem_soulutions/counting_problems/filled_subgrid_count_i_analysis
difficulty: Medium
tags: [grid, 2d-prefix-sum, counting, subgrid]
prerequisites: [prefix_sums, 2d_arrays]
---

# Filled Subgrid Count I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Grid / Counting |
| **Time Limit** | 1 second |
| **Key Technique** | 2D Prefix Sums / Early Termination |
| **CSES Link** | [Filled Subgrid Count I](https://cses.fi/problemset/task/2101) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how to enumerate all k x k subgrids in a 2D grid
- [ ] Apply early termination optimization for uniformity checking
- [ ] Use 2D prefix sums to accelerate subgrid queries
- [ ] Recognize when brute force with pruning is acceptable

---

## Problem Statement

**Problem:** Given an n x m grid of integers, count the number of k x k subgrids where all cells contain the same value (filled subgrids).

**Input:**
- Line 1: Three integers n, m, k (grid dimensions and subgrid size)
- Next n lines: m integers each (grid values)

**Output:**
- One integer: the count of filled k x k subgrids

**Constraints:**
- 1 <= n, m <= 100
- 1 <= k <= min(n, m)
- 1 <= grid[i][j] <= 10^9

### Example

```
Input:
3 4 2
1 1 2 2
1 1 2 2
3 3 3 3

Output:
4
```

**Explanation:** The four filled 2x2 subgrids are:
- (0,0): all 1s
- (0,2): all 2s
- (1,0): values [1,1,3,3] - NOT filled
- (1,2): all 2s and 3s mixed - NOT filled
- Actually: positions (0,0), (0,2), (1,2) have uniform values, plus bottom-right corner.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently check if all cells in a subgrid have the same value?

The naive approach checks all k^2 cells for each subgrid. The insight is that we can:
1. **Early terminate** when we find a mismatched value
2. **Use prefix sums** to check if sum equals k^2 times the first element

### Breaking Down the Problem

1. **What are we looking for?** Count of k x k subgrids with uniform values
2. **What information do we have?** Grid dimensions, subgrid size, cell values
3. **What's the relationship?** A subgrid is "filled" iff all k^2 cells equal the top-left cell

### Analogies

Think of this like checking if a patch of tiles on a floor all have the same color. You can either check each tile one-by-one (stopping early if you find a different color), or use a clever counting method.

---

## Solution 1: Brute Force with Early Termination

### Idea

For each possible k x k subgrid position, check if all cells match the top-left value. Stop immediately when a mismatch is found.

### Algorithm

1. Iterate through all valid top-left corners: (i, j) where i <= n-k and j <= m-k
2. For each position, get the reference value at (i, j)
3. Check all k^2 cells; return false immediately on mismatch
4. Count subgrids that pass the check

### Code

**Python:**
```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    grid = []
    for _ in range(n):
        grid.append(list(map(int, input().split())))

    count = 0
    for i in range(n - k + 1):
        for j in range(m - k + 1):
            if is_filled(grid, i, j, k):
                count += 1

    print(count)

def is_filled(grid, r, c, k):
    """Check if k x k subgrid starting at (r,c) is uniform."""
    val = grid[r][c]
    for i in range(r, r + k):
        for j in range(c, c + k):
            if grid[i][j] != val:
                return False
    return True

solve()
```

**C++:**
```cpp
#include <bits/stdc++.h>
using namespace std;

int n, m, k;
vector<vector<int>> grid;

bool isFilled(int r, int c) {
    int val = grid[r][c];
    for (int i = r; i < r + k; i++) {
        for (int j = c; j < c + k; j++) {
            if (grid[i][j] != val) return false;
        }
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m >> k;
    grid.assign(n, vector<int>(m));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> grid[i][j];
        }
    }

    int count = 0;
    for (int i = 0; i <= n - k; i++) {
        for (int j = 0; j <= m - k; j++) {
            if (isFilled(i, j)) count++;
        }
    }

    cout << count << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n-k+1) * (m-k+1) * k^2) | Check each subgrid, each cell |
| Space | O(1) | No extra space beyond input |

### Why This Works (But Can Be Slow)

Early termination helps in practice - mixed subgrids are rejected quickly. However, worst case (all uniform grid) still checks all cells.

---

## Solution 2: Optimal with 2D Prefix Sums

### Key Insight

> **The Trick:** If all k^2 cells have value v, then sum of subgrid = k^2 * v. Use 2D prefix sums for O(1) subgrid sum queries.

### Why Prefix Sums Help

Instead of checking k^2 cells, we:
1. Compute the subgrid sum in O(1) using prefix sums
2. Compare: `sum == k * k * grid[r][c]`

**Caveat:** This only works when values are non-negative and the equality is mathematically sound. For large values, we must be careful about overflow.

### 2D Prefix Sum Formula

For prefix sum array `P`:
```
P[i][j] = sum of grid[0..i-1][0..j-1]

Sum of subgrid (r1,c1) to (r2,c2):
= P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]
```

### Dry Run Example

Let's trace with:
```
Grid (3x3, k=2):
1 1 2
1 1 2
3 3 3

Prefix Sum Array P (4x4, 1-indexed for convenience):
  0 0 0 0
  0 1 2 4
  0 2 4 8
  0 5 10 18
```

```
Check subgrid at (0,0):
  Reference value = grid[0][0] = 1
  Expected sum = 2 * 2 * 1 = 4
  Actual sum = P[2][2] - P[0][2] - P[2][0] + P[0][0]
             = 4 - 0 - 0 + 0 = 4
  4 == 4? YES -> filled!

Check subgrid at (0,1):
  Reference value = grid[0][1] = 1
  Expected sum = 4 * 1 = 4
  Actual sum = P[2][3] - P[0][3] - P[2][1] + P[0][1]
             = 8 - 0 - 2 + 0 = 6
  6 == 4? NO -> not filled

Check subgrid at (1,0):
  Reference value = grid[1][0] = 1
  Expected sum = 4 * 1 = 4
  Actual sum = P[3][2] - P[1][2] - P[3][0] + P[1][0]
             = 10 - 2 - 0 + 0 = 8
  8 == 4? NO -> not filled

Check subgrid at (1,1):
  Reference value = grid[1][1] = 1
  Expected sum = 4
  Actual sum = P[3][3] - P[1][3] - P[3][1] + P[1][1]
             = 18 - 4 - 5 + 1 = 10
  10 == 4? NO -> not filled

Result: 1 filled subgrid
```

### Code

**Python:**
```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    grid = []
    for _ in range(n):
        grid.append(list(map(int, input().split())))

    # Build 2D prefix sum
    prefix = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            prefix[i+1][j+1] = (grid[i][j] + prefix[i][j+1]
                               + prefix[i+1][j] - prefix[i][j])

    def subgrid_sum(r1, c1, r2, c2):
        """Sum of subgrid from (r1,c1) to (r2,c2) inclusive."""
        return (prefix[r2+1][c2+1] - prefix[r1][c2+1]
                - prefix[r2+1][c1] + prefix[r1][c1])

    count = 0
    target_cells = k * k

    for i in range(n - k + 1):
        for j in range(m - k + 1):
            val = grid[i][j]
            actual_sum = subgrid_sum(i, j, i + k - 1, j + k - 1)
            if actual_sum == target_cells * val:
                # Verify with early-termination check (handles collision cases)
                if is_truly_filled(grid, i, j, k):
                    count += 1

    print(count)

def is_truly_filled(grid, r, c, k):
    """Double-check uniformity (handles hash collision-like cases)."""
    val = grid[r][c]
    for i in range(r, r + k):
        for j in range(c, c + k):
            if grid[i][j] != val:
                return False
    return True

solve()
```

**C++:**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, k;
    cin >> n >> m >> k;

    vector<vector<long long>> grid(n, vector<long long>(m));
    vector<vector<long long>> prefix(n + 1, vector<long long>(m + 1, 0));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> grid[i][j];
        }
    }

    // Build prefix sum
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            prefix[i+1][j+1] = grid[i][j] + prefix[i][j+1]
                              + prefix[i+1][j] - prefix[i][j];
        }
    }

    auto subgridSum = [&](int r1, int c1, int r2, int c2) -> long long {
        return prefix[r2+1][c2+1] - prefix[r1][c2+1]
               - prefix[r2+1][c1] + prefix[r1][c1];
    };

    auto isFilled = [&](int r, int c) -> bool {
        long long val = grid[r][c];
        for (int i = r; i < r + k; i++) {
            for (int j = c; j < c + k; j++) {
                if (grid[i][j] != val) return false;
            }
        }
        return true;
    };

    int count = 0;
    long long targetCells = (long long)k * k;

    for (int i = 0; i <= n - k; i++) {
        for (int j = 0; j <= m - k; j++) {
            long long val = grid[i][j];
            long long actualSum = subgridSum(i, j, i + k - 1, j + k - 1);
            if (actualSum == targetCells * val) {
                if (isFilled(i, j)) count++;
            }
        }
    }

    cout << count << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * m) average | Prefix sum filters most candidates |
| Space | O(n * m) | Prefix sum array |

---

## Common Mistakes

### Mistake 1: Off-by-One in Subgrid Boundaries

```python
# WRONG - goes out of bounds
for i in range(n - k):  # Should be n - k + 1
    for j in range(m - k):
        ...
```

**Problem:** Misses the last valid row/column of subgrids.
**Fix:** Use `range(n - k + 1)` to include all valid positions.

### Mistake 2: Integer Overflow in Sum Calculation

```cpp
// WRONG - may overflow with large values
int sum = k * k * grid[i][j];  // grid values up to 10^9!

// CORRECT
long long sum = (long long)k * k * grid[i][j];
```

**Problem:** With k=100 and value=10^9, product exceeds 32-bit range.
**Fix:** Use `long long` for sum calculations.

### Mistake 3: Trusting Prefix Sum Alone

```python
# WRONG - assumes sum equality means uniformity
if subgrid_sum == k * k * grid[r][c]:
    count += 1  # False positive possible!
```

**Problem:** Different values can sum to same total (e.g., [1,3] vs [2,2]).
**Fix:** Either verify with direct check, or use additional constraints.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| k equals grid size | n=2, m=2, k=2, uniform grid | 1 | Only one possible subgrid |
| k = 1 | Any grid, k=1 | n * m | Every cell is a trivial filled subgrid |
| All different values | No two cells match | 0 (if k>1) | No uniform subgrids exist |
| All same value | Entire grid is uniform | (n-k+1) * (m-k+1) | Every subgrid is filled |
| Single row/column | n=1 or m=1 | Depends on k | Linear subgrid counting |

---

## When to Use This Pattern

### Use This Approach When:
- Counting uniform/homogeneous subregions in 2D grids
- Subgrid size k is fixed and given
- Need to verify a property across all cells of a subregion

### Don't Use When:
- Looking for the largest uniform subgrid (use DP instead)
- Subgrid sizes vary (different approach needed)
- Grid is sparse (consider coordinate compression)

### Pattern Recognition Checklist:
- [ ] Fixed-size subgrid queries? -> **Consider 2D prefix sums**
- [ ] Checking uniformity? -> **Early termination helps**
- [ ] Counting subregions? -> **Enumerate all top-left corners**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | 1D prefix sums foundation |
| [Forest Queries](https://cses.fi/problemset/task/1652) | 2D prefix sums basics |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Maximal Square (LeetCode)](https://leetcode.com/problems/maximal-square/) | Find largest uniform square |
| [Count Square Submatrices (LeetCode)](https://leetcode.com/problems/count-square-submatrices-with-all-ones/) | Count all sizes, DP approach |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Filled Subgrid Count II](https://cses.fi/problemset/task/2102) | Larger constraints, optimization needed |
| [Maximal Rectangle (LeetCode)](https://leetcode.com/problems/maximal-rectangle/) | Histogram-based approach |

---

## Key Takeaways

1. **The Core Idea:** Enumerate all k x k positions and verify uniformity efficiently
2. **Time Optimization:** Early termination on first mismatch; prefix sums for O(1) range queries
3. **Space Trade-off:** O(n*m) prefix array enables faster filtering
4. **Pattern:** Fixed-size 2D subgrid counting with uniformity constraint

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a 2D prefix sum array correctly
- [ ] Query any rectangular subgrid sum in O(1)
- [ ] Handle off-by-one errors in grid boundary iteration
- [ ] Implement early termination for uniformity checking
- [ ] Analyze when prefix sums provide benefit vs. overhead

---

## Additional Resources

- [CP-Algorithms: 2D Prefix Sums](https://cp-algorithms.com/data_structures/prefix-sum.html)
- [CSES Forest Queries](https://cses.fi/problemset/task/1652) - 2D prefix sum application
- [LeetCode Grid Problems](https://leetcode.com/tag/matrix/)
