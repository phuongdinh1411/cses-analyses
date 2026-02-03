---
layout: simple
title: "Chessboard and Queens - Backtracking Problem"
permalink: /problem_soulutions/introductory_problems/chessboard_and_queens_analysis
difficulty: Medium
tags: [backtracking, pruning, constraint-satisfaction, recursion]
---

# Chessboard and Queens

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Backtracking |
| **Time Limit** | 1 second |
| **Key Technique** | Backtracking with Pruning |
| **CSES Link** | [Chessboard and Queens](https://cses.fi/problemset/task/1624) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement backtracking with constraint checking
- [ ] Use diagonal indexing to detect queen attacks in O(1) time
- [ ] Handle reserved/blocked squares in constraint satisfaction problems
- [ ] Recognize when to prune search branches early for efficiency

---

## Problem Statement

**Problem:** Place 8 queens on an 8x8 chessboard so that no two queens attack each other. Some squares are reserved and cannot have a queen. Count all valid arrangements.

**Input:**
- 8 lines, each with 8 characters
- `.` represents an empty square (queen can be placed)
- `*` represents a reserved square (queen cannot be placed)

**Output:**
- Number of valid ways to place 8 non-attacking queens

**Constraints:**
- Board is always 8x8
- Queens attack horizontally, vertically, and diagonally

### Example

```
Input:
........
........
..*.....
........
........
.....**.
...*....
........

Output:
65
```

**Explanation:** With some squares reserved (`*`), there are 65 valid configurations where 8 queens can be placed without attacking each other.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we systematically explore all queen placements while efficiently detecting conflicts?

This is a classic **constraint satisfaction problem** solved with **backtracking**. We place queens row by row, and at each step, we check if the placement is valid. If we reach a dead end (no valid column for current row), we backtrack.

### Breaking Down the Problem

1. **What are we looking for?** All configurations of 8 queens with no attacks
2. **What constraints exist?** No two queens on same row, column, or diagonal; no queen on reserved squares
3. **Why backtracking?** We can prune entire branches when we detect a conflict early

### The Key Insight: Diagonal Indexing

For an 8x8 board, there are:
- **15 main diagonals** (top-left to bottom-right): indexed by `row - col + 7` (range 0-14)
- **15 anti-diagonals** (top-right to bottom-left): indexed by `row + col` (range 0-14)

```
Main Diagonal (row - col + 7):     Anti-Diagonal (row + col):
  0  1  2  3  4  5  6  7            0  1  2  3  4  5  6  7
+--+--+--+--+--+--+--+--+         +--+--+--+--+--+--+--+--+
| 7| 8| 9|10|11|12|13|14|  0     | 0| 1| 2| 3| 4| 5| 6| 7|  0
| 6| 7| 8| 9|10|11|12|13|  1     | 1| 2| 3| 4| 5| 6| 7| 8|  1
| 5| 6| 7| 8| 9|10|11|12|  2     | 2| 3| 4| 5| 6| 7| 8| 9|  2
| 4| 5| 6| 7| 8| 9|10|11|  3     | 3| 4| 5| 6| 7| 8| 9|10|  3
| 3| 4| 5| 6| 7| 8| 9|10|  4     | 4| 5| 6| 7| 8| 9|10|11|  4
| 2| 3| 4| 5| 6| 7| 8| 9|  5     | 5| 6| 7| 8| 9|10|11|12|  5
| 1| 2| 3| 4| 5| 6| 7| 8|  6     | 6| 7| 8| 9|10|11|12|13|  6
| 0| 1| 2| 3| 4| 5| 6| 7|  7     | 7| 8| 9|10|11|12|13|14|  7
+--+--+--+--+--+--+--+--+         +--+--+--+--+--+--+--+--+
```

Two queens at `(r1, c1)` and `(r2, c2)` are on the **same diagonal** if:
- Main: `r1 - c1 == r2 - c2`
- Anti: `r1 + c1 == r2 + c2`

---

## Solution: Backtracking with Pruning

### Idea

Place exactly one queen in each row. For each row, try all 8 columns. Skip if:
1. The square is reserved (`*`)
2. The column already has a queen
3. Either diagonal already has a queen

Track occupied columns and diagonals with boolean arrays for O(1) lookup.

### Algorithm

1. Read the board and mark reserved squares
2. Initialize tracking arrays: `col_used[8]`, `diag1_used[15]`, `diag2_used[15]`
3. Recursively place queens row by row:
   - Base case: row == 8, found valid configuration, count++
   - For each column in current row:
     - Skip if reserved, column used, or diagonal used
     - Mark column and diagonals as used
     - Recurse to next row
     - Unmark (backtrack)
4. Return total count

### Dry Run Example

Let's trace through a small portion with an empty 8x8 board:

```
Row 0: Try each column
  col=0: Place queen at (0,0)
    Mark: col_used[0]=true, diag1[7]=true, diag2[0]=true

Row 1: Try each column
  col=0: Skip (col_used[0] is true)
  col=1: Skip (diag1[7] - same main diagonal as (0,0))
  col=2: Place queen at (1,2)
    Mark: col_used[2]=true, diag1[6]=true, diag2[3]=true

Row 2: Try each column
  col=0: Skip (col_used[0] is true)
  col=1: Skip (diag2[3] - same anti-diagonal as (1,2))
  col=2: Skip (col_used[2] is true)
  col=3: Skip (diag1[6] - same main diagonal as (1,2))
  col=4: Place queen at (2,4)
    ...continue recursion...

If all 8 rows placed successfully -> count++
Backtrack and try next column configurations
```

### Visual: One Valid Configuration

```
    0   1   2   3   4   5   6   7
  +---+---+---+---+---+---+---+---+
0 | Q |   |   |   |   |   |   |   |  Queen at col 0
  +---+---+---+---+---+---+---+---+
1 |   |   |   |   | Q |   |   |   |  Queen at col 4
  +---+---+---+---+---+---+---+---+
2 |   |   |   |   |   |   |   | Q |  Queen at col 7
  +---+---+---+---+---+---+---+---+
3 |   |   |   |   |   | Q |   |   |  Queen at col 5
  +---+---+---+---+---+---+---+---+
4 |   |   | Q |   |   |   |   |   |  Queen at col 2
  +---+---+---+---+---+---+---+---+
5 |   |   |   |   |   |   | Q |   |  Queen at col 6
  +---+---+---+---+---+---+---+---+
6 |   | Q |   |   |   |   |   |   |  Queen at col 1
  +---+---+---+---+---+---+---+---+
7 |   |   |   | Q |   |   |   |   |  Queen at col 3
  +---+---+---+---+---+---+---+---+

No two queens share a row, column, or diagonal!
```

### Code (Python)

```python
def solve():
    """
    CSES Chessboard and Queens - Backtracking Solution

    Time: O(8!) worst case, much less with pruning
    Space: O(8) for recursion stack and tracking arrays
    """
    # Read the 8x8 board
    board = []
    for _ in range(8):
        board.append(input().strip())

    # Tracking arrays for O(1) conflict detection
    col_used = [False] * 8      # col_used[c] = True if column c has a queen
    diag1 = [False] * 15        # Main diagonal: row - col + 7
    diag2 = [False] * 15        # Anti diagonal: row + col

    count = 0

    def backtrack(row):
        nonlocal count

        # Base case: all 8 queens placed successfully
        if row == 8:
            count += 1
            return

        # Try each column in current row
        for col in range(8):
            # Skip if square is reserved
            if board[row][col] == '*':
                continue

            # Calculate diagonal indices
            d1 = row - col + 7  # Main diagonal index
            d2 = row + col      # Anti diagonal index

            # Skip if column or diagonal is already used
            if col_used[col] or diag1[d1] or diag2[d2]:
                continue

            # Place queen: mark column and diagonals
            col_used[col] = True
            diag1[d1] = True
            diag2[d2] = True

            # Recurse to next row
            backtrack(row + 1)

            # Backtrack: unmark column and diagonals
            col_used[col] = False
            diag1[d1] = False
            diag2[d2] = False

    backtrack(0)
    print(count)

# Run solution
solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

/*
 * CSES Chessboard and Queens - Backtracking Solution
 *
 * Time: O(8!) worst case, much less with pruning
 * Space: O(8) for recursion stack and tracking arrays
 */

string board[8];
bool col_used[8];     // Column tracking
bool diag1[15];       // Main diagonal (row - col + 7)
bool diag2[15];       // Anti diagonal (row + col)
int count_solutions = 0;

void backtrack(int row) {
    // Base case: all 8 queens placed
    if (row == 8) {
        count_solutions++;
        return;
    }

    // Try each column in current row
    for (int col = 0; col < 8; col++) {
        // Skip reserved squares
        if (board[row][col] == '*') continue;

        // Calculate diagonal indices
        int d1 = row - col + 7;  // Main diagonal
        int d2 = row + col;      // Anti diagonal

        // Skip if column or diagonal is used
        if (col_used[col] || diag1[d1] || diag2[d2]) continue;

        // Place queen
        col_used[col] = diag1[d1] = diag2[d2] = true;

        // Recurse
        backtrack(row + 1);

        // Backtrack
        col_used[col] = diag1[d1] = diag2[d2] = false;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    // Read board
    for (int i = 0; i < 8; i++) {
        cin >> board[i];
    }

    // Initialize tracking arrays
    memset(col_used, false, sizeof(col_used));
    memset(diag1, false, sizeof(diag1));
    memset(diag2, false, sizeof(diag2));

    // Solve
    backtrack(0);

    cout << count_solutions << endl;

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(8!) | At most 8! = 40,320 configurations; pruning reduces this significantly |
| Space | O(1) | Fixed-size arrays (8 + 15 + 15); O(8) recursion depth |

---

## Common Mistakes

### Mistake 1: Wrong Diagonal Index Calculation

```python
# WRONG - can produce negative indices
d1 = row - col  # Range: -7 to 7

# CORRECT - shift to non-negative range
d1 = row - col + 7  # Range: 0 to 14
```

**Problem:** Negative array indices cause bugs or wrap-around errors.
**Fix:** Add offset (N-1 = 7) to ensure all indices are non-negative.

### Mistake 2: Forgetting to Check Reserved Squares

```python
# WRONG - ignores reserved squares
for col in range(8):
    if col_used[col] or diag1[d1] or diag2[d2]:
        continue
    # ... place queen

# CORRECT - check reserved squares first
for col in range(8):
    if board[row][col] == '*':  # Check reserved first!
        continue
    if col_used[col] or diag1[d1] or diag2[d2]:
        continue
    # ... place queen
```

**Problem:** Queens placed on reserved squares, giving wrong count.
**Fix:** Check reserved status before any other validation.

### Mistake 3: Off-by-One in Diagonal Array Size

```python
# WRONG - array too small
diag1 = [False] * 8  # Only 8 elements

# CORRECT - need 2*N - 1 = 15 elements
diag1 = [False] * 15
```

**Problem:** For an NxN board, there are 2N-1 diagonals in each direction.
**Fix:** Use array size of 15 (= 2*8 - 1) for both diagonal arrays.

### Mistake 4: Not Backtracking Properly

```python
# WRONG - forgetting to unmark
col_used[col] = True
backtrack(row + 1)
# Missing: col_used[col] = False

# CORRECT - always unmark after recursion
col_used[col] = True
backtrack(row + 1)
col_used[col] = False  # Backtrack!
```

**Problem:** State "leaks" between branches, causing incorrect counts.
**Fix:** Always restore state after recursive call returns.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No reserved squares | All `.` | 92 | Classic N-Queens answer |
| All squares reserved | All `*` | 0 | No valid placement possible |
| First row blocked | Row 0 all `*` | 0 | Cannot place queen in row 0 |
| Single path | Strategic `*` placement | 1 | Only one configuration works |
| Diagonal blocked | Main diagonal all `*` | Still valid | Other placements exist |

---

## When to Use This Pattern

### Use Backtracking When:
- You need to find ALL solutions (not just one)
- Problem has constraints that can prune the search space
- Solution is built incrementally (e.g., row by row)
- You can detect invalid partial solutions early

### Optimization Tips:
- Use arrays instead of sets for O(1) lookup (as shown)
- Prune as early as possible (check constraints before recursing)
- Consider symmetry to reduce search space (not needed for CSES)

### Pattern Recognition Checklist:
- [ ] Need to place items with mutual constraints? -> **Backtracking**
- [ ] Chess-related attacks? -> **Diagonal indexing with row +/- col**
- [ ] Counting configurations? -> **DFS with backtracking**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Permutations](https://cses.fi/problemset/task/1070) | Basic backtracking pattern |
| [Creating Strings](https://cses.fi/problemset/task/1622) | Generating all permutations |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [N-Queens (LeetCode 51)](https://leetcode.com/problems/n-queens/) | Return actual configurations, not just count |
| [N-Queens II (LeetCode 52)](https://leetcode.com/problems/n-queens-ii/) | Same as this problem but without reserved squares |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Sudoku Solver (LeetCode 37)](https://leetcode.com/problems/sudoku-solver/) | More complex constraints, 2D placement |
| [Grid Paths (CSES)](https://cses.fi/problemset/task/1625) | Backtracking with path constraints |

---

## Key Takeaways

1. **The Core Idea:** Place queens row-by-row, using tracking arrays to detect conflicts in O(1)
2. **Time Optimization:** Pruning invalid branches early avoids exploring dead ends
3. **Space Trade-off:** O(1) extra space for tracking arrays enables O(1) conflict detection
4. **Pattern:** Classic constraint satisfaction with backtracking and diagonal indexing

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why `row - col + 7` and `row + col` identify diagonals
- [ ] Handle reserved squares correctly
- [ ] Implement backtracking with proper state restoration
- [ ] Write the solution in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Backtracking](https://cp-algorithms.com/others/backtracking.html)
- [Wikipedia: Eight Queens Puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle)
- [CSES Chessboard and Queens](https://cses.fi/problemset/task/1624) - Backtracking puzzle
