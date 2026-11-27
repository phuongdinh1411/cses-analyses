---
layout: simple
title: "Grid Completion - Combinatorics Problem"
permalink: /problem_soulutions/counting_problems/grid_completion_analysis
difficulty: Hard
tags: [combinatorics, inclusion-exclusion, permutations, grid, counting]
---

# Grid Completion

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Grid Completion](https://cses.fi/problemset/task/2429) |
| **Difficulty** | Hard |
| **Category** | Combinatorics |
| **Time Limit** | 1 second |
| **Key Technique** | Two permutations + inclusion–exclusion over collision cells |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Model "one A per row and column" as a permutation (a perfect matching of free rows to free columns)
- [ ] Count pairs of permutations that must not share a cell with inclusion–exclusion
- [ ] Split forbidden cells into independent groups so the sum factorises
- [ ] Count permutations that avoid a set of non-attacking forbidden cells

---

## Problem Statement

**Problem:** Build an n × n grid where every row and every column contains exactly one `A` and exactly one `B` (all other cells empty). Some `A`s and `B`s are already placed. Count the completions.

**Input:**
- Line 1: integer n
- Next n lines: n characters each, `.` (empty), `A`, or `B`
- Every row and column has at most one `A` and at most one `B`

**Output:**
- The number of completions modulo 10^9 + 7

**Constraints:**
- 2 <= n <= 500

### Example

```
Input:
5
.....
..AB.
.....
B....
...A.

Output:
16
```

**Explanation:** 3 `A`s and 3 `B`s are still missing. Without the "one letter per cell" rule there would be 3! · 3! = 36 pairs of placements; 20 of them put two letters in one cell (including an `A` on the prefilled `B` at row 3, column 0), leaving 16.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** If A and B were placed on separate transparent sheets, each sheet would be just a permutation. What goes wrong when we overlay them?

Only one thing: two letters landing in the same cell. Counting placements that avoid every such collision is a classic inclusion–exclusion.

### Breaking Down the Problem

Let `a` = number of A's still to place (rows without an A; the same number of columns lack an A). Define `b` the same way for B. A completion is a bijection σ for A's and τ for B's. A cell (i, j) is a **bad cell** when a letter could land on it illegally. There are three kinds:

| Kind | Cell | Row condition | Column condition | Count |
|------|------|---------------|------------------|-------|
| New A on prefilled B | holds `B` | row lacks A | column lacks A | p |
| New B on prefilled A | holds `A` | row lacks B | column lacks B | q |
| New A meets new B | empty | row lacks both | column lacks both | any of r × c cells |

Here r = rows lacking both letters, c = columns lacking both letters.

The three kinds live in **disjoint sets of rows and columns** (a kind-1 row has a B, a kind-3 row has neither, a kind-2 row has an A but no B), so a chosen set of bad cells splits into independent parts.

### The Formula

Choose k collision cells of kind 3 (C(r,k) · C(c,k) · k! ways to pick k rows, k columns and match them). Each forces one A and one B. The remaining A's must avoid the p kind-1 cells, and the remaining B's must avoid the q kind-2 cells:

```
avoid(P, R) = Σ_x (-1)^x · C(P, x) · (R - x)!          # permutations of R avoiding P non-attacking cells

answer = Σ_k (-1)^k · C(r,k) · C(c,k) · k! · avoid(p, a - k) · avoid(q, b - k)
```

### Analogy

Two people independently seat guests (A-team and B-team) in a theatre where each row and column gets one guest per team. Inclusion–exclusion subtracts the seatings where two guests share a seat, adds back double-subtractions, and so on.

---

## Solution 1: Brute Force (Enumerate Both Permutations)

### Idea

Try every permutation for A's and every permutation for B's; keep pairs that respect the prefilled cells and never share a cell.

### Code

```python
from itertools import permutations


def grid_completion_brute(grid):
    """Time: O((n!)^2 * n), only for n <= 6."""
    n = len(grid)
    count = 0
    for pa in permutations(range(n)):            # A in row i goes to column pa[i]
        if any(grid[i][pa[i]] == 'B' for i in range(n)):
            continue
        if any(grid[i][j] == 'A' and pa[i] != j for i in range(n) for j in range(n)):
            continue
        for pb in permutations(range(n)):        # B in row i goes to column pb[i]
            if any(pa[i] == pb[i] or grid[i][pb[i]] == 'A' for i in range(n)):
                continue
            if any(grid[i][j] == 'B' and pb[i] != j for i in range(n) for j in range(n)):
                continue
            count += 1
    return count


print(grid_completion_brute([".....", "..AB.", ".....", "B....", "...A."]))  # 16
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n!)² · n²) | Every pair of permutations is checked |
| Space | O(n) | Current permutations |

### Why This Is Slow

n = 10 already means (10!)² ≈ 1.3 · 10^13 pairs; n = 500 is hopeless.

---

## Solution 2: Optimal (Inclusion–Exclusion)

### Key Insight

> **The Trick:** Treat A's and B's as two independent permutations, then subtract collisions. Because the three kinds of bad cells never share a row or column, the inclusion–exclusion sum factorises into one outer sum over k and two simple inner sums.

### Algorithm

1. Scan the grid; mark rows/columns that already have an A or a B. If any row or column has two A's or two B's, the answer is 0.
2. Compute a, b, r, c, p, q as defined above.
3. Precompute factorials and inverse factorials up to n.
4. Sum over k = 0..min(r, c) with alternating signs, using `avoid(p, a−k)` and `avoid(q, b−k)`.

### Dry Run Example

Official sample:

```
row 0  .....      rows lacking A: 0, 2, 3        -> a = 3
row 1  ..AB.      rows lacking B: 0, 2, 4        -> b = 3
row 2  .....      rows lacking both: 0, 2        -> r = 2
row 3  B....      cols lacking both: 1, 4        -> c = 2
row 4  ...A.      prefilled B at (3,0): row 3 and col 0 lack A -> p = 1
                  prefilled A's: (1,2) row has B, (4,3) col has B -> q = 0

avoid(1, 3) = 3! - 2! = 4     avoid(0, 3) = 6
avoid(1, 2) = 2! - 1! = 1     avoid(0, 2) = 2
avoid(1, 1) = 1! - 0! = 0

k = 0:  + C(2,0)·C(2,0)·0! · 4 · 6 = +24
k = 1:  - C(2,1)·C(2,1)·1! · 1 · 2 = -8
k = 2:  + C(2,2)·C(2,2)·2! · 0 · 1 =  0

answer = 24 - 8 + 0 = 16
```

### Visual Diagram

```
          free A columns          free B columns
              |                       |
   A sheet: permutation σ    B sheet: permutation τ
              \                     /
               overlay: forbidden if σ and τ hit the same cell
                        or σ hits a prefilled B, or τ hits a prefilled A
```

### Code (Python)

```python
import sys

MOD = 10**9 + 7


def grid_completion(grid):
    n = len(grid)
    row_a = [False] * n; row_b = [False] * n
    col_a = [False] * n; col_b = [False] * n
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch == 'A':
                if row_a[i] or col_a[j]:
                    return 0
                row_a[i] = col_a[j] = True
            elif ch == 'B':
                if row_b[i] or col_b[j]:
                    return 0
                row_b[i] = col_b[j] = True

    a = row_a.count(False)  # A's still to place
    b = row_b.count(False)  # B's still to place
    r = sum(1 for i in range(n) if not row_a[i] and not row_b[i])  # rows missing both letters
    c = sum(1 for j in range(n) if not col_a[j] and not col_b[j])  # columns missing both letters
    # prefilled B cells a new A could wrongly land on (its row and column still need an A), and vice versa
    p = sum(1 for i in range(n) for j in range(n) if grid[i][j] == 'B' and not row_a[i] and not col_a[j])
    q = sum(1 for i in range(n) for j in range(n) if grid[i][j] == 'A' and not row_b[i] and not col_b[j])

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (n + 1)
    inv[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD

    def comb(x, y):
        return fact[x] * inv[y] % MOD * inv[x - y] % MOD

    def avoid(prefilled, remaining):
        # ways to place `remaining` letters avoiding the bad prefilled cells (inclusion-exclusion)
        return sum((-1) ** x * comb(prefilled, x) * fact[remaining - x]
                   for x in range(min(prefilled, remaining) + 1)) % MOD

    # The three kinds of bad cells use disjoint rows and columns, so inclusion-exclusion factorises:
    # choose k empty cells where the new A and new B collide, then place the rest avoiding prefilled cells.
    total = 0
    for k in range(min(r, c) + 1):
        ways = comb(r, k) * comb(c, k) % MOD * fact[k] % MOD
        ways = ways * avoid(p, a - k) % MOD * avoid(q, b - k) % MOD
        total = (total + ways if k % 2 == 0 else total - ways) % MOD
    return total


if __name__ == "__main__":
    data = sys.stdin.read().split()
    n = int(data[0])
    print(grid_completion(data[1:1 + n]))
```

Checked against the brute force on 600 random grids (n ≤ 5) and on the official sample.

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n²) | Grid scan, plus up to n values of k each with O(n) `avoid` sums |
| Space | O(n) | Row/column flags and factorial tables |

---

## Common Mistakes

### Mistake 1: Ignoring Prefilled Cells of the Other Letter

**Problem:** Counting only new-A/new-B collisions (Σ (−1)^k C(r,k) C(c,k) k! (a−k)! (b−k)!) lets a new A sit on a prefilled B. On the grid `..B / ... / ...` it returns 6 instead of 4.

**Fix:** Add the `avoid(p, ·)` and `avoid(q, ·)` factors.

### Mistake 2: Counting Collisions in Rows That Already Have a Letter

**Problem:** A new A and a new B can only meet in a row and column that lack *both* letters; using all free rows overcounts the subtraction.

**Fix:** r and c count rows/columns missing both A and B.

### Mistake 3: Treating It as a Latin Square

**Problem:** Each row needs one A and one B, and the remaining n−2 cells stay empty. Backtracking over Latin squares solves a different problem and cannot reach n = 500.

### Mistake 4: Negative Values Under the Modulus

```python
total = (total - ways) % MOD   # Python's % is always non-negative; in C++ add MOD first
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Empty 2×2 | `..` / `..` | 2 | A on a diagonal, B on the other |
| A sits on B's only spot | `A.` / `..` | 1 | A's forced to the main diagonal, B's to the other |
| Prefilled B blocks an A | `..B` / `...` / `...` | 4 | 3! A-placements minus 2 that use (0,2), times B's |
| Fully determined | complete valid grid | 1 | Nothing left to place |
| n = 500, empty | — | — | O(n²) is instant |

---

## When to Use This Pattern

### Use This Approach When:
- Two (or more) independent permutations must not overlap
- Forbidden cells form non-attacking groups (distinct rows and columns)
- The count of "at least these k conflicts" has a closed form

### Don't Use When:
- Forbidden cells share rows/columns arbitrarily (you need a rook polynomial or DP)
- Values per row are more than two letters with complex interaction

### Pattern Recognition Checklist:
- [ ] "Exactly one X per row and column"? --> **Permutation**
- [ ] Two permutations that must not share a cell? --> **Inclusion–exclusion on shared cells**
- [ ] Forbidden cells in distinct rows/cols? --> **Σ (−1)^x C(P,x) (R−x)!**

---

## Related Problems

### Easier (Do These First)

| Problem | Link | Why It Helps |
|---------|------|--------------|
| Christmas Party | [CSES 1717](https://cses.fi/problemset/task/1717) | Derangements: one permutation avoiding the diagonal |
| Binomial Coefficients | [CSES 1079](https://cses.fi/problemset/task/1079) | Factorials and inverse factorials mod p |

### Similar Difficulty

| Problem | Link | Key Difference |
|---------|------|----------------|
| Counting Reorders | [CSES 2421](https://cses.fi/problemset/task/2421) | Inclusion–exclusion over glued equal neighbours |

---

## Key Takeaways

1. **The Core Idea:** A's form one permutation, B's another; the only conflict is sharing a cell.
2. **Three kinds of bad cells** (A on B, B on A, A meets B) use disjoint rows and columns, so the sum factorises.
3. **Formula:** Σ_k (−1)^k C(r,k) C(c,k) k! · avoid(p, a−k) · avoid(q, b−k).
4. **Cost:** O(n²) with precomputed factorials.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Compute a, b, r, c, p, q for the sample by hand
- [ ] Reproduce 24 − 8 + 0 = 16
- [ ] Explain why kind-1, kind-2 and kind-3 cells never share a row
- [ ] Derive avoid(P, R) from inclusion–exclusion

---

## Additional Resources

- [CP-Algorithms: Inclusion–Exclusion Principle](https://cp-algorithms.com/combinatorics/inclusion-exclusion.html)
- [CP-Algorithms: Binomial Coefficients](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
