---
layout: simple
title: "Backtracking Patterns"
permalink: /pattern/backtracking
---

# Backtracking Patterns — Comprehensive Guide

Backtracking is **brute force with early termination**. You explore a decision tree, and whenever a partial solution can't possibly lead to a valid complete solution, you **prune** that branch and backtrack. The power of backtracking comes not from what it explores, but from what it **doesn't** explore.

---

## Quick Navigation: "I need to..."

| I need to... | Technique | Section |
|--------------|-----------|---------|
| Generate all **permutations** | Swap-based / used-array backtracking | [2](#2-permutations) |
| Generate all **combinations** (choose k from n) | Index-based backtracking | [3](#3-combinations) |
| Generate all **subsets** (power set) | Include/exclude at each step | [4](#4-subsets) |
| Handle **duplicates** in generation | Sort + skip adjacent duplicates | [5](#5-handling-duplicates) |
| Solve **N-Queens** / board placement | Row-by-row with column/diagonal tracking | [6](#6-grid-and-board-problems) |
| Solve **Sudoku** | Cell-by-cell with constraint checking | [6](#6-grid-and-board-problems) |
| **Partition** array into k equal subsets | Bucket-filling backtracking | [7](#7-partitioning-problems) |
| Generate **parentheses** / valid sequences | Count-based constraints | [8](#8-string-backtracking) |
| Search for **word in grid** | DFS with visited tracking | [6](#6-grid-and-board-problems) |
| Optimize with **pruning** | Feasibility + bound + symmetry pruning | [9](#9-pruning-techniques) |
| Use **bitmask** for state | Bitmask replaces boolean arrays | [10](#10-backtracking--bitmask) |

---

## Table of Contents

1. [The Backtracking Framework](#1-the-backtracking-framework)
2. [Permutations](#2-permutations)
3. [Combinations](#3-combinations)
4. [Subsets](#4-subsets)
5. [Handling Duplicates](#5-handling-duplicates)
6. [Grid and Board Problems](#6-grid-and-board-problems)
7. [Partitioning Problems](#7-partitioning-problems)
8. [String Backtracking](#8-string-backtracking)
9. [Pruning Techniques](#9-pruning-techniques)
10. [Backtracking + Bitmask](#10-backtracking--bitmask)
11. [Constraint Satisfaction Problems](#11-constraint-satisfaction-problems)
12. [Common Patterns Collection](#12-common-patterns-collection)
13. [Pattern Recognition Cheat Sheet](#13-pattern-recognition-cheat-sheet)

---

## 1. The Backtracking Framework

### The Idea

Every backtracking problem follows the same skeleton:

```
1. Choose   — pick a candidate for the current position
2. Explore  — recurse with that choice
3. Unchoose — undo the choice (backtrack)
```

### The Universal Template

```python
def backtrack(state, choices):
    if is_complete(state):
        process_solution(state)
        return

    for candidate in choices:
        if is_valid(state, candidate):
            # 1. Choose
            apply(state, candidate)

            # 2. Explore
            backtrack(state, next_choices)

            # 3. Unchoose
            undo(state, candidate)
```

### The Decision Tree

Every backtracking algorithm implicitly explores a **tree**. Each node is a partial solution, each edge is a decision, and leaves are complete (or pruned) solutions.

```
Generate all 3-bit binary strings:

                       ""
                   /        \
                 "0"        "1"          ← choose bit 0
               /    \      /    \
            "00"   "01"  "10"   "11"     ← choose bit 1
            / \    / \   / \    / \
         000 001 010 011 100 101 110 111  ← choose bit 2

Without pruning: visits all 2^3 = 8 leaves
With constraint "no two consecutive 1s":
                       ""
                   /        \
                 "0"        "1"
               /    \      /    ╲
            "00"   "01"  "10"   "11" ← PRUNE (consecutive 1s)
            / \    / \   / \
         000 001 010 011 100 101      ← only 5 leaves!
                      ↑
                     PRUNE (011→0110/0111 both have "11")
Wait — 011 is 3 bits, it's a leaf. Let me redo:

Actually for 3-bit, leaves ARE the 3-bit strings.
Pruning "11" prefix means we skip "110" and "111".
Result: 000, 001, 010, 100, 101 — 5 valid strings.
```

### Recursion vs State Space

Think of each recursive call as **one level** of the decision tree:

| Level | Decision | State changes |
|-------|----------|---------------|
| 0 | Which element goes first? | Add to `path[0]` |
| 1 | Which element goes second? | Add to `path[1]` |
| ... | ... | ... |
| n-1 | Which element goes last? | Add to `path[n-1]` |

### Implementation — Basic Template

```python
def solve(n):
    result = []

    def backtrack(path):
        # Base case: solution is complete
        if len(path) == n:
            result.append(path[:])  # copy!
            return

        for candidate in get_candidates(path):
            path.append(candidate)       # choose
            backtrack(path)              # explore
            path.pop()                   # unchoose

    backtrack([])
    return result
```

### ⚠️ Critical: Copy the Path!

```python
# WRONG — all entries point to the same list
result.append(path)

# CORRECT — snapshot the current state
result.append(path[:])
result.append(list(path))
result.append(tuple(path))
```

Since `path` is mutated during backtracking, you must copy it when recording a solution.

---

## 2. Permutations

### Problem: Generate All Permutations of [1..n]

Each position chooses from the remaining unused elements.

### Approach A: Used-Array

Track which elements are used with a boolean array.

```
Tree for [1, 2, 3]:

Level 0 (pick 1st):     1           2           3
Level 1 (pick 2nd):   2   3       1   3       1   2
Level 2 (pick 3rd):  3     2     3     1     2     1

Permutations: [1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1]
```

```python
def permutations_used_array(nums):
    n = len(nums)
    result = []
    used = [False] * n

    def backtrack(path):
        if len(path) == n:
            result.append(path[:])
            return
        for i in range(n):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                backtrack(path)
                path.pop()
                used[i] = False

    backtrack([])
    return result
```

### Approach B: Swap-Based

Instead of a separate `used` array, swap elements into position. More memory efficient.

```
[1, 2, 3]
 ^  fix position 0: swap with 0, 1, 2

pos=0: [1, 2, 3]  →  recurse on [_, 2, 3]
       [2, 1, 3]  →  recurse on [_, 1, 3]
       [3, 2, 1]  →  recurse on [_, 2, 1]
```

```python
def permutations_swap(nums):
    result = []

    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]  # choose
            backtrack(start + 1)                          # explore
            nums[start], nums[i] = nums[i], nums[start]  # unchoose

    backtrack(0)
    return result
```

### Complexity

- **Number of permutations**: n!
- **Time**: O(n × n!) — n! permutations, each takes O(n) to copy
- **Space**: O(n) recursion depth (excluding output)

---

## 3. Combinations

### Problem: Choose k Elements from [1..n]

The key difference from permutations: **order doesn't matter**, so we enforce an ordering (e.g., always pick in increasing order) to avoid duplicates.

### The Trick: Start Index

```
C(4, 2) — choose 2 from [1, 2, 3, 4]:

          start=1
        /    |    \    \
       1     2     3    4
      /|\   /\     |
     2 3 4  3  4   4

Combinations: [1,2] [1,3] [1,4] [2,3] [2,4] [3,4]

Notice: we never go backward (e.g., no [2,1]).
```

```python
def combinations(n, k):
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return

        # Pruning: need (k - len(path)) more elements,
        # and only (n - start + 1) are available
        for i in range(start, n + 1):
            if n - i + 1 < k - len(path):  # not enough remaining
                break
            path.append(i)
            backtrack(i + 1, path)  # i+1 to avoid reuse
            path.pop()

    backtrack(1, [])
    return result
```

### Why `i + 1` and Not `i`?

- `backtrack(i + 1, ...)` → each element used **at most once** (combinations)
- `backtrack(i, ...)` → elements can repeat (combinations with repetition)
- `backtrack(start, ...)` → ERROR: would repeat same combinations

### Combination with Repetition

```python
def combinations_with_repetition(candidates, k):
    """Choose k elements, each can be used multiple times."""
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path)     # i, NOT i+1 — allow reuse
            path.pop()

    backtrack(0, [])
    return result
```

### Complexity

- **Number of combinations**: C(n, k) = n! / (k!(n-k)!)
- **Time**: O(k × C(n, k))
- **Space**: O(k) recursion depth

---

## 4. Subsets

### Problem: Generate All Subsets (Power Set)

Two classic approaches:

### Approach A: Include/Exclude (Binary Decision)

At each element, make a binary choice: include it or skip it.

```
Array: [1, 2, 3]

                      {}
                   /      \
               {1}         {}           ← include/exclude 1
              /    \      /    \
          {1,2}   {1}  {2}    {}        ← include/exclude 2
          / \     / \   / \   / \
      {1,2,3}{1,2}{1,3}{1}{2,3}{2}{3}{} ← include/exclude 3
```

```python
def subsets_include_exclude(nums):
    result = []

    def backtrack(index, path):
        if index == len(nums):
            result.append(path[:])
            return

        # Include nums[index]
        path.append(nums[index])
        backtrack(index + 1, path)
        path.pop()

        # Exclude nums[index]
        backtrack(index + 1, path)

    backtrack(0, [])
    return result
```

### Approach B: Iterative Growth

At each level, choose any element with index ≥ start.

```python
def subsets_iterative_growth(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])  # every partial path is a valid subset

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

### Approach C: Bitmask (Non-Recursive)

```python
def subsets_bitmask(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    return result
```

### Complexity

- **Number of subsets**: 2^n
- **Time**: O(n × 2^n)
- **Space**: O(n) recursion depth

---

## 5. Handling Duplicates

### The Problem

If the input has duplicates, naive backtracking generates duplicate solutions:

```
Input: [1, 1, 2]
Naive subsets: {}, {1}, {1}, {2}, {1,1}, {1,2}, {1,2}, {1,1,2}
                         ^                        ^
                     duplicate!               duplicate!
```

### The Fix: Sort + Skip Adjacent

**Sort** the array first. Then at each decision level, **skip a candidate if it equals the previous candidate at the same level**.

```
Sorted: [1, 1, 2]

Level decision for "which element next?":
  candidates at start=0: [1, 1, 2]
    - pick 1 (index 0) ✓
    - pick 1 (index 1) ✗ SKIP (same as previous candidate at this level)
    - pick 2 (index 2) ✓
```

### Subsets with Duplicates

```python
def subsets_with_dup(nums):
    nums.sort()  # critical!
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            # Skip duplicates at the same decision level
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

### Permutations with Duplicates

```python
def permutations_with_dup(nums):
    nums.sort()  # critical!
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicate: if nums[i] == nums[i-1] and nums[i-1] was NOT used
            # at this level, then we'd generate the same subtree
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result
```

### Why `not used[i-1]`?

This is the tricky part. Consider `[1a, 1b, 2]`:

```
Without the check, both subtrees are identical:
  1a → 1b → 2   and   1b → 1a → 2

Rule: among equal elements, only pick them in the original order.
  - 1a before 1b: OK (original order)
  - 1b before 1a: SKIP

"not used[i-1]" means: the previous equal element was already returned
(not currently in the path), so we're trying to start a new branch with
this duplicate — skip it.
```

### Combination Sum with Duplicates

```python
def combination_sum_with_dup(candidates, target):
    """Each number used at most once; duplicates in input."""
    candidates.sort()
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # pruning: sorted, so all future too big
            if i > start and candidates[i] == candidates[i - 1]:
                continue  # skip duplicate at same level
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return result
```

### The Duplicate-Handling Rules

| Problem Type | Sort? | Skip Condition |
|-------------|-------|----------------|
| Subsets with dups | Yes | `i > start and nums[i] == nums[i-1]` |
| Permutations with dups | Yes | `i > 0 and nums[i] == nums[i-1] and not used[i-1]` |
| Combinations with dups | Yes | `i > start and nums[i] == nums[i-1]` |

---

## 6. Grid and Board Problems

### N-Queens

Place N queens on an N×N board so no two attack each other.

```
N = 4 solution:

  . Q . .      . . Q .
  . . . Q      Q . . .
  Q . . .      . . . Q
  . . Q .      . Q . .
```

**Key insight**: Place one queen per row. Track which columns and diagonals are occupied.

```
Diagonals encoding:
  - Main diagonal (↘): row - col is constant
  - Anti-diagonal (↙): row + col is constant

Board for N=4, showing (row-col) values:
   0   -1   -2   -3       ← main diagonal IDs
   1    0   -1   -2
   2    1    0   -1
   3    2    1    0

Board showing (row+col) values:
   0    1    2    3       ← anti-diagonal IDs
   1    2    3    4
   2    3    4    5
   3    4    5    6
```

```python
def solve_n_queens(n):
    result = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row, queens):
        if row == n:
            # Build board representation
            board = []
            for r, c in sorted(queens):
                board.append('.' * c + 'Q' + '.' * (n - c - 1))
            result.append(board)
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            queens.append((row, col))

            backtrack(row + 1, queens)

            queens.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0, [])
    return result
```

### Sudoku Solver

Fill empty cells so every row, column, and 3×3 box contains 1–9.

```python
def solve_sudoku(board):
    """board: 9x9 list of lists, 0 = empty."""
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    # Initialize constraint sets
    empty = []
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                val = board[r][c]
                rows[r].add(val)
                cols[c].add(val)
                boxes[(r // 3) * 3 + c // 3].add(val)
            else:
                empty.append((r, c))

    def backtrack(idx):
        if idx == len(empty):
            return True  # all cells filled

        r, c = empty[idx]
        box_id = (r // 3) * 3 + c // 3

        for val in range(1, 10):
            if val in rows[r] or val in cols[c] or val in boxes[box_id]:
                continue

            # Choose
            board[r][c] = val
            rows[r].add(val)
            cols[c].add(val)
            boxes[box_id].add(val)

            # Explore
            if backtrack(idx + 1):
                return True

            # Unchoose
            board[r][c] = 0
            rows[r].remove(val)
            cols[c].remove(val)
            boxes[box_id].remove(val)

        return False  # no valid digit for this cell

    backtrack(0)
    return board
```

### Word Search in Grid

Find if a word exists in a grid by moving to adjacent cells (no revisiting).

```python
def word_search(board, word):
    R, C = len(board), len(board[0])

    def backtrack(r, c, k):
        if k == len(word):
            return True
        if r < 0 or r >= R or c < 0 or c >= C:
            return False
        if board[r][c] != word[k]:
            return False

        # Mark visited (in-place trick)
        tmp = board[r][c]
        board[r][c] = '#'

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if backtrack(r + dr, c + dc, k + 1):
                return True

        board[r][c] = tmp  # unchoose
        return False

    for r in range(R):
        for c in range(C):
            if backtrack(r, c, 0):
                return True
    return False
```

**In-place visited trick**: Temporarily replace `board[r][c]` with a sentinel character (`'#'`), then restore it when backtracking. Saves allocating a separate `visited` array.

---

## 7. Partitioning Problems

### Partition into k Equal-Sum Subsets

Given an array and integer k, can you partition the array into k subsets with equal sum?

```
Input: [4, 3, 2, 3, 5, 2, 1], k = 4
Total = 20, target per bucket = 5

Solution: {5}, {4,1}, {3,2}, {3,2}  ✓
```

```python
def can_partition_k(nums, k):
    total = sum(nums)
    if total % k != 0:
        return False
    target = total // k

    nums.sort(reverse=True)  # pruning: try big elements first
    if nums[0] > target:
        return False

    buckets = [0] * k

    def backtrack(index):
        if index == len(nums):
            return all(b == target for b in buckets)

        seen = set()  # avoid putting same value in equivalent empty buckets
        for i in range(k):
            if buckets[i] + nums[index] > target:
                continue
            if buckets[i] in seen:  # symmetry pruning
                continue
            seen.add(buckets[i])

            buckets[i] += nums[index]
            if backtrack(index + 1):
                return True
            buckets[i] -= nums[index]

        return False

    return backtrack(0)
```

### Palindrome Partitioning

Split a string so every part is a palindrome.

```
Input: "aab"
Output: [["a","a","b"], ["aa","b"]]
```

```python
def palindrome_partition(s):
    result = []

    def is_palindrome(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return

        for end in range(start, len(s)):
            if is_palindrome(start, end):
                path.append(s[start:end + 1])
                backtrack(end + 1, path)
                path.pop()

    backtrack(0, [])
    return result
```

### Optimization: Precompute Palindromes with DP

```python
def palindrome_partition_optimized(s):
    n = len(s)
    # is_pal[i][j] = True if s[i..j] is palindrome
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j] and is_pal[i + 1][j - 1])

    result = []

    def backtrack(start, path):
        if start == n:
            result.append(path[:])
            return
        for end in range(start, n):
            if is_pal[start][end]:
                path.append(s[start:end + 1])
                backtrack(end + 1, path)
                path.pop()

    backtrack(0, [])
    return result
```

---

## 8. String Backtracking

### Generate Parentheses

Generate all combinations of n pairs of well-formed parentheses.

```
n = 3:
((()))  (()())  (())()  ()(())  ()()()

Key constraint: at every prefix, #open ≥ #close
```

```python
def generate_parentheses(n):
    result = []

    def backtrack(path, open_count, close_count):
        if len(path) == 2 * n:
            result.append(''.join(path))
            return

        if open_count < n:
            path.append('(')
            backtrack(path, open_count + 1, close_count)
            path.pop()

        if close_count < open_count:
            path.append(')')
            backtrack(path, open_count, close_count + 1)
            path.pop()

    backtrack([], 0, 0)
    return result
```

### Letter Combinations of Phone Number

```
2 → "abc", 3 → "def", ..., 9 → "wxyz"
Input: "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

```python
def letter_combinations(digits):
    if not digits:
        return []

    mapping = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    result = []

    def backtrack(index, path):
        if index == len(digits):
            result.append(''.join(path))
            return
        for ch in mapping[digits[index]]:
            path.append(ch)
            backtrack(index + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

### Restore IP Addresses

```
Input: "25525511135"
Output: ["255.255.11.135", "255.255.111.35"]
```

```python
def restore_ip_addresses(s):
    result = []

    def backtrack(start, parts):
        if len(parts) == 4:
            if start == len(s):
                result.append('.'.join(parts))
            return

        remaining_digits = len(s) - start
        remaining_parts = 4 - len(parts)

        # Pruning: each remaining part needs 1-3 digits
        if remaining_digits < remaining_parts or remaining_digits > remaining_parts * 3:
            return

        for length in range(1, 4):
            if start + length > len(s):
                break
            segment = s[start:start + length]
            # No leading zeros (except "0" itself)
            if len(segment) > 1 and segment[0] == '0':
                break
            if int(segment) > 255:
                break
            parts.append(segment)
            backtrack(start + length, parts)
            parts.pop()

    backtrack(0, [])
    return result
```

### Expression: Add Operators

Insert `+`, `-`, `*` between digits to reach a target.

```python
def add_operators(num, target):
    result = []

    def backtrack(index, path, value, prev_operand):
        if index == len(num):
            if value == target:
                result.append(path)
            return

        for i in range(index, len(num)):
            # No leading zeros
            if i > index and num[index] == '0':
                break

            substr = num[index:i + 1]
            curr = int(substr)

            if index == 0:
                # First number, no operator
                backtrack(i + 1, substr, curr, curr)
            else:
                # Addition
                backtrack(i + 1, path + '+' + substr,
                         value + curr, curr)
                # Subtraction
                backtrack(i + 1, path + '-' + substr,
                         value - curr, -curr)
                # Multiplication (need to undo previous addition/subtraction)
                backtrack(i + 1, path + '*' + substr,
                         value - prev_operand + prev_operand * curr,
                         prev_operand * curr)

    backtrack(0, '', 0, 0)
    return result
```

**Why track `prev_operand`?** Multiplication has higher precedence. If the expression so far evaluates to `2 + 3` and we multiply by `4`, the result should be `2 + 3*4 = 14`, not `(2+3)*4 = 20`. So we undo `+3` and redo `+3*4`.

---

## 9. Pruning Techniques

Pruning is what makes backtracking practical. Without it, you're just doing brute force.

### Type 1: Feasibility Pruning

**Stop early when the current path can't possibly lead to a solution.**

```python
# Combination Sum: if remaining < 0, stop
def backtrack(start, path, remaining):
    if remaining < 0:
        return  # PRUNE — overshot the target
    if remaining == 0:
        result.append(path[:])
        return
    ...
```

### Type 2: Bound Pruning (Branch and Bound)

**Estimate the best possible outcome from the current state. If it's worse than the best known solution, prune.**

```python
# Traveling Salesman: prune if current_cost + estimated_remaining > best_known
def backtrack(current_city, visited, cost):
    lower_bound = cost + estimate_remaining(visited)
    if lower_bound >= best_known:
        return  # PRUNE — can't beat current best

    if len(visited) == n:
        best_known = min(best_known, cost + dist[current_city][0])
        return
    ...
```

### Type 3: Symmetry Pruning

**If multiple choices lead to equivalent states, try only one.**

```python
# N-Queens: the board has vertical symmetry
# Only place first queen in columns 0..n//2, mirror the rest
def backtrack(row, queens):
    if row == 0:
        end = (n + 1) // 2  # only half the columns
    else:
        end = n
    for col in range(end):
        ...
```

```python
# Partition into k subsets: identical empty buckets are interchangeable
seen = set()
for i in range(k):
    if buckets[i] in seen:
        continue  # this bucket state already tried
    seen.add(buckets[i])
    ...
```

### Type 4: Ordering Pruning

**Process elements in a smart order to trigger other pruning earlier.**

```python
# Sort in decreasing order: large elements fail faster, pruning more branches
nums.sort(reverse=True)

# Sudoku: pick the cell with fewest candidates (MRV heuristic)
def find_best_cell(board):
    min_options = 10
    best = None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                options = count_valid_digits(r, c)
                if options < min_options:
                    min_options = options
                    best = (r, c)
    return best
```

### Type 5: Memoization (When Subproblems Repeat)

If the same state can be reached via different paths, cache the result. This turns backtracking into **dynamic programming**.

```python
# Word Break: can we segment string into dictionary words?
from functools import lru_cache

@lru_cache(maxsize=None)
def can_break(start):
    if start == len(s):
        return True
    for end in range(start + 1, len(s) + 1):
        if s[start:end] in word_set and can_break(end):
            return True
    return False
```

### Pruning Impact Summary

```
Without pruning:     O(n!)   or  O(2^n)   or  O(k^n)
With pruning:        Often orders of magnitude faster

Example — N-Queens:
  n=8:  Without pruning: 8^8 = 16M states
        With col/diag pruning: ~15K states
        Speedup: ~1000x
```

---

## 10. Backtracking + Bitmask

### Why Bitmask?

A bitmask compresses a set of boolean flags into a single integer. Instead of `used = [False, True, True, False]`, use `used = 0b0110 = 6`.

### Benefits

| Boolean Array | Bitmask |
|---------------|---------|
| O(n) to copy | O(1) to copy |
| O(n) to compare | O(1) to compare |
| Can't hash easily | Hash as integer |
| Mutable (must undo) | Immutable operations |

### Permutations with Bitmask

```python
def permutations_bitmask(nums):
    n = len(nums)
    result = []

    def backtrack(mask, path):
        if mask == (1 << n) - 1:  # all bits set
            result.append(path[:])
            return
        for i in range(n):
            if mask & (1 << i):  # already used
                continue
            path.append(nums[i])
            backtrack(mask | (1 << i), path)
            path.pop()

    backtrack(0, [])
    return result
```

### Bitmask DP on Permutations (TSP-Style)

When you need to count or optimize over permutations, combine bitmask with memoization:

```python
from functools import lru_cache

def shortest_hamiltonian_path(dist, n):
    """Find shortest path visiting all n cities."""
    @lru_cache(maxsize=None)
    def dp(mask, last):
        if mask == (1 << n) - 1:
            return 0  # or dist[last][0] for cycle

        best = float('inf')
        for nxt in range(n):
            if mask & (1 << nxt):
                continue
            best = min(best, dist[last][nxt] + dp(mask | (1 << nxt), nxt))
        return best

    return min(dp(1 << i, i) for i in range(n))
```

### N-Queens with Bitmask

Track column and diagonal conflicts as bitmasks — checking and updating all three in O(1).

```python
def n_queens_bitmask(n):
    count = 0

    def backtrack(row, cols, diag1, diag2):
        nonlocal count
        if row == n:
            count += 1
            return

        # Available positions: bits NOT set in any conflict mask
        available = ((1 << n) - 1) & ~(cols | diag1 | diag2)

        while available:
            # Pick lowest set bit
            pos = available & (-available)
            available &= available - 1

            backtrack(
                row + 1,
                cols | pos,
                (diag1 | pos) << 1,    # shift left: row-col increases
                (diag2 | pos) >> 1     # shift right: row+col decreases
            )

    backtrack(0, 0, 0, 0)
    return count
```

**Why shift the diagonal masks?** When moving to the next row:
- A queen's main diagonal (↘) threat shifts one column right (`<< 1`)
- A queen's anti-diagonal (↙) threat shifts one column left (`>> 1`)

This is faster than using sets because all operations are bitwise O(1).

---

## 11. Constraint Satisfaction Problems

### Graph Coloring

Color a graph with at most `m` colors such that no two adjacent nodes share a color.

```python
def graph_coloring(adj, n, m):
    """Can we color graph with m colors? adj = adjacency list."""
    colors = [0] * n  # 0 = uncolored

    def is_safe(node, color):
        for neighbor in adj[node]:
            if colors[neighbor] == color:
                return False
        return True

    def backtrack(node):
        if node == n:
            return True

        for color in range(1, m + 1):
            if is_safe(node, color):
                colors[node] = color
                if backtrack(node + 1):
                    return True
                colors[node] = 0

        return False

    return backtrack(0)
```

### Hamiltonian Path

Find a path that visits every vertex exactly once.

```python
def hamiltonian_path(adj, n):
    """Find a Hamiltonian path if one exists."""
    path = []
    visited = [False] * n

    def backtrack(node):
        path.append(node)
        if len(path) == n:
            return True

        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                if backtrack(neighbor):
                    return True
        visited[node] = False
        path.pop()
        return False

    for start in range(n):
        if backtrack(start):
            return path
    return None
```

### Cryptarithmetic (SEND + MORE = MONEY)

```python
def solve_cryptarithmetic():
    """Solve SEND + MORE = MONEY."""
    letters = 'SENDMORY'  # 8 unique letters
    leading = {'S', 'M'}  # can't be 0

    def backtrack(idx, assignment, used_digits):
        if idx == len(letters):
            # Check the equation
            s = lambda w: int(''.join(str(assignment[c]) for c in w))
            return s('SEND') + s('MORE') == s('MONEY')

        letter = letters[idx]
        start = 1 if letter in leading else 0

        for digit in range(start, 10):
            if digit in used_digits:
                continue
            assignment[letter] = digit
            used_digits.add(digit)
            if backtrack(idx + 1, assignment, used_digits):
                return True
            del assignment[letter]
            used_digits.discard(digit)

        return False

    assignment = {}
    if backtrack(0, assignment, set()):
        return assignment
    return None
```

---

## 12. Common Patterns Collection

### Pattern A: "Generate All X" → Backtracking

Whenever a problem asks to **generate all** valid configurations:

```
Generate all:
  - Permutations       → Section 2
  - Combinations       → Section 3
  - Subsets            → Section 4
  - Palindrome splits  → Section 7
  - Valid parentheses  → Section 8
  - IP addresses       → Section 8
```

### Pattern B: "Can We Achieve X?" → Backtracking with Early Return

When the answer is True/False, return as soon as you find one solution:

```python
def can_achieve(state):
    if is_solution(state):
        return True  # found one!
    for choice in candidates:
        if is_valid(state, choice):
            apply(state, choice)
            if can_achieve(state):  # propagate True immediately
                return True
            undo(state, choice)
    return False  # exhausted all options
```

### Pattern C: "Find Optimal X" → Backtracking with Bound

Track the best solution found so far and prune branches that can't improve it:

```python
best = float('inf')

def find_optimal(state, cost):
    global best
    if is_complete(state):
        best = min(best, cost)
        return
    if cost + lower_bound(state) >= best:
        return  # PRUNE
    for choice in candidates:
        apply(state, choice)
        find_optimal(state, cost + choice_cost)
        undo(state, choice)
```

### Pattern D: Counting Solutions → Backtracking with Counter

```python
def count_solutions(state):
    if is_complete(state):
        return 1
    total = 0
    for choice in candidates:
        if is_valid(state, choice):
            apply(state, choice)
            total += count_solutions(state)
            undo(state, choice)
    return total
```

### Pattern E: Incremental Constraint Checking

Don't re-validate the entire state from scratch. Instead, maintain constraint data structures and update them incrementally:

```
N-Queens:
  BAD:  for each new queen, scan entire board for conflicts → O(n) per check
  GOOD: maintain sets for cols, diag1, diag2 → O(1) per check

Sudoku:
  BAD:  for each digit, scan row + col + box → O(n) per check
  GOOD: maintain sets for each row, col, box → O(1) per check
```

---

## 13. Pattern Recognition Cheat Sheet

### Decision Flowchart

```
Problem asks to...
   │
   ├── "Generate ALL valid ___"
   │     │
   │     ├── Order matters? → Permutations (Section 2)
   │     ├── Order doesn't matter, fixed size? → Combinations (Section 3)
   │     ├── Order doesn't matter, any size? → Subsets (Section 4)
   │     ├── Split/partition something? → Partitioning (Section 7)
   │     └── Build a string char by char? → String backtracking (Section 8)
   │
   ├── "Can we ___?" (yes/no)
   │     → Backtracking with early return (Pattern B)
   │
   ├── "Find the best ___"
   │     → Branch and bound (Pattern C)
   │
   ├── "Count how many ___"
   │     │
   │     ├── State space small? → Backtracking with counter
   │     └── Overlapping subproblems? → DP (memoized backtracking)
   │
   └── "Place items on grid with constraints"
         → Grid backtracking (Section 6)
```

### Complexity Summary

| Problem | # Solutions | Time |
|---------|-------------|------|
| Permutations of n | n! | O(n × n!) |
| Permutations with dups | n! / (k₁! × k₂! × ...) | O(n × result) |
| Combinations C(n,k) | C(n,k) | O(k × C(n,k)) |
| Subsets of n | 2^n | O(n × 2^n) |
| N-Queens | varies (~n!/nᵏ) | O(n!) worst |
| Sudoku (9×9) | 1 | O(9^empty) worst |
| Graph coloring (m colors) | varies | O(m^n) worst |
| Hamiltonian path | varies | O(n!) worst |

### When Backtracking vs DP

| Use Backtracking | Use DP |
|-----------------|--------|
| Need **all** solutions | Need **count** or **optimal** |
| State space has **no overlap** | Subproblems **overlap** |
| Constraints are **complex** (hard to encode as DP state) | State can be encoded as **tuple/mask** |
| Small input (n ≤ ~20) | Larger input (n ≤ ~1000+) |

### When Backtracking vs Greedy

| Use Backtracking | Use Greedy |
|-----------------|------------|
| Need to explore **multiple paths** | Locally optimal = globally optimal |
| No greedy property exists | Matroid / exchange argument works |
| Need **exact** answer | Need **approximate** or provably optimal |

### Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Forgetting to copy `path` when saving | Use `path[:]` or `list(path)` |
| Not undoing the choice (backtrack step) | Always pair `choose` with `unchoose` |
| Generating duplicate solutions | Sort + skip (Section 5) |
| Not pruning → TLE | Add feasibility / bound / symmetry pruning |
| Infinite recursion | Ensure state progresses (index increases, mask grows) |
| Modifying iteration variable | Use index-based loop, not iterator over mutable collection |

### Template Quick Reference

```python
# Permutations
def perms(nums):
    backtrack with used[] or swap

# Combinations
def combs(n, k):
    backtrack(start, path)  # start ensures no duplicates

# Subsets
def subs(nums):
    backtrack(start, path)  # record at every node, not just leaves

# With duplicates
nums.sort()
if i > start and nums[i] == nums[i-1]: continue

# Grid placement
for col in range(n):
    if valid(row, col): place and recurse on row+1

# String building
for candidate_char in options:
    if constraints_met: append and recurse on index+1
```

---

**Backtracking is systematic trial-and-error.** The "trial" part is choosing a candidate; the "error" part is recognizing dead ends and undoing the choice. Master the template, learn the pruning tricks, and know when to switch to DP — that covers 90% of backtracking problems.
