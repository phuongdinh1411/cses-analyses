---
layout: simple
title: "MEX Grid Construction II - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/mex_grid_construction_ii_analysis
difficulty: Hard
tags: [mex, grid, construction, constraint-satisfaction, math, dual-constraints]
---

# MEX Grid Construction II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Construction / Math |
| **Time Limit** | 1 second |
| **Key Technique** | Dual Constraint Satisfaction + MEX Properties |
| **CSES Link** | [CSES Problem Set](https://cses.fi/problemset/) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply MEX constraints simultaneously to rows AND columns
- [ ] Analyze when dual MEX constraints are satisfiable
- [ ] Construct grids using careful value placement strategies
- [ ] Recognize impossibility conditions for multi-dimensional constraints

---

## Problem Statement

**Problem:** Construct an n x n grid where each row has MEX = r and each column has MEX = c.

**Input:** Three integers n, r, c (grid size, row MEX target, column MEX target)

**Output:** Print n lines with n space-separated integers, or "IMPOSSIBLE"

**Constraints:** 1 <= n <= 1000, 0 <= r, c <= n

### Example

```
Input: 3 2 2
Output:
0 1 3
1 3 0
3 0 1
```

**Explanation:** Each row and column contains {0, 1, 3}, so MEX = 2 for all.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When can we satisfy MEX constraints on both rows AND columns?

Unlike row-only constraints, placing values affects both dimensions simultaneously.

### Breaking Down the Problem

1. **Row requirement:** Contains {0, 1, ..., r-1}, must NOT contain r
2. **Column requirement:** Contains {0, 1, ..., c-1}, must NOT contain c
3. **The conflict:** Same cell counts for both row AND column

### Critical Case Analysis

| Condition | Result | Reason |
|-----------|--------|--------|
| r > n OR c > n | IMPOSSIBLE | Cannot fit required values |
| r == c | POSSIBLE | Symmetric cyclic construction |
| r != c AND min(r,c) < n | POSSIBLE | Asymmetric construction works |
| r != c AND (r == n OR c == n) | IMPOSSIBLE | Contradictory constraints |

---

## Solution: Case Analysis Construction

### Key Insight

> **The Trick:** Use cyclic Latin square-style patterns for symmetric cases, and careful value exclusion for asymmetric cases.

### Dry Run Example

With n = 3, r = 2, c = 2:

```
Cyclic construction with values {0, 1, 3}:

       +---+---+---+
Row 0: | 0 | 1 | 3 |  Row: {0,1,3} -> MEX = 2
Row 1: | 1 | 3 | 0 |  Row: {0,1,3} -> MEX = 2
Row 2: | 3 | 0 | 1 |  Row: {0,1,3} -> MEX = 2
       +---+---+---+

Col 0: {0,1,3} -> MEX = 2
Col 1: {1,3,0} -> MEX = 2
Col 2: {3,0,1} -> MEX = 2
```

### Code

#### Python

```python
def mex_grid_construction_ii(n: int, r: int, c: int) -> None:
    """
    Construct n x n grid where each row has MEX = r and each column has MEX = c.
    Time: O(n^2), Space: O(n^2)
    """
    # Impossibility checks
    if r > n or c > n:
        print("IMPOSSIBLE")
        return
    if r != c and (r == n or c == n):
        print("IMPOSSIBLE")
        return

    grid = [[0] * n for _ in range(n)]

    if r == c:
        # Symmetric case: cyclic construction
        filler = r + 1
        for i in range(n):
            for j in range(n):
                if j < r:
                    grid[i][j] = (i + j) % r
                else:
                    grid[i][j] = filler
                    filler += 1
    else:
        # Asymmetric case
        large = max(r, c)
        filler = large + 1
        for i in range(n):
            for j in range(n):
                val = (i + j) % (large + 1)
                if val == r or val == c:
                    val = filler
                    filler += 1
                grid[i][j] = val

    for row in grid:
        print(*row)


if __name__ == "__main__":
    n, r, c = map(int, input().split())
    mex_grid_construction_ii(n, r, c)
```

#### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, r, c;
    cin >> n >> r >> c;

    // Impossibility checks
    if (r > n || c > n) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }
    if (r != c && (r == n || c == n)) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }

    vector<vector<int>> grid(n, vector<int>(n));

    if (r == c) {
        // Symmetric case
        int filler = r + 1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (j < r) {
                    grid[i][j] = (i + j) % r;
                } else {
                    grid[i][j] = filler++;
                }
            }
        }
    } else {
        // Asymmetric case
        int large = max(r, c);
        int filler = large + 1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                int val = (i + j) % (large + 1);
                if (val == r || val == c) {
                    val = filler++;
                }
                grid[i][j] = val;
            }
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (j > 0) cout << " ";
            cout << grid[i][j];
        }
        cout << "\n";
    }
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Fill n x n grid cells |
| Space | O(n^2) | Store the grid |

---

## Common Mistakes

### Mistake 1: Missing Impossibility Cases

```python
# WRONG - only checks basic bounds
if r > n or c > n:
    return "IMPOSSIBLE"

# CORRECT - also check asymmetric edge case
if r != c and (r == n or c == n):
    return "IMPOSSIBLE"
```

### Mistake 2: Including Forbidden Values

```python
# WRONG - cyclic might produce r or c
val = (i + j) % (large + 1)
grid[i][j] = val  # Might be r or c!

# CORRECT - skip forbidden values
if val == r or val == c:
    val = filler
    filler += 1
```

### Mistake 3: Treating Rows and Columns Independently

Values placed for row MEX also count toward column MEX. Consider both constraints simultaneously.

---

## Edge Cases

| Case | Input (n, r, c) | Output | Reason |
|------|-----------------|--------|--------|
| Both zero | (3, 0, 0) | Grid with no zeros | MEX=0 means 0 absent |
| Equal targets | (3, 2, 2) | Valid grid | Symmetric case |
| r > n | (2, 3, 1) | IMPOSSIBLE | Cannot fit {0,1,2} in row |
| r = n, c < n | (3, 3, 2) | IMPOSSIBLE | Contradictory constraints |
| n = 1, r = c = 1 | (1, 1, 1) | 0 | Single cell = 0 |

---

## When to Use This Pattern

### Use This Approach When:
- Grid construction with multiple MEX constraints
- Constraints on both rows AND columns simultaneously
- Need to find any valid construction (not count them)

### Don't Use When:
- Need to count all valid configurations (use DP)
- Problem has additional constraints beyond MEX

### Pattern Recognition Checklist:
- [ ] MEX on multiple dimensions? -> Analyze constraint interactions
- [ ] r == c? -> Symmetric cyclic construction
- [ ] r != c? -> Case analysis for impossibility

---

## Related Problems

### Easier (Do First)
| Problem | Why It Helps |
|---------|--------------|
| [Missing Number](https://cses.fi/problemset/task/1083) | Basic MEX concept |
| [MEX Grid Construction](mex_grid_construction_analysis) | Single constraint version |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Chessboard and Queens](https://cses.fi/problemset/task/1624) | Grid constraints with conflicts |
| [Grid Paths](https://cses.fi/problemset/task/1638) | Grid traversal constraints |

### Harder (Do After)
| Problem | New Concept |
|---------|-------------|
| [Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) | Multiple constraint types |

---

## Key Takeaways

1. **Dual Constraints:** Row and column MEX constraints interact through shared cells
2. **Impossibility Detection:** Check bounds and asymmetric edge cases (r != c with one == n)
3. **Cyclic Construction:** Latin square patterns help satisfy symmetric constraints
4. **Case Analysis:** r == c vs r != c require different strategies

---

## Practice Checklist

- [ ] Explain why r != c with one equal to n is impossible
- [ ] Implement the symmetric (r == c) case from scratch
- [ ] Handle the r = 0 or c = 0 edge cases correctly
- [ ] Verify your solution satisfies both row AND column MEX
