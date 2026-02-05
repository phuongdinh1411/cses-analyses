---
layout: simple
title: "Two Knights - Combinatorics Problem"
permalink: /problem_soulutions/introductory_problems/two_knights_analysis
difficulty: Medium
tags: [combinatorics, math, chess, counting]
---

# Two Knights

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Combinatorics / Mathematics |
| **Time Limit** | 1 second |
| **Key Technique** | Combinatorial Counting (Total - Invalid) |
| **CSES Link** | [https://cses.fi/problemset/task/1072](https://cses.fi/problemset/task/1072) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the complementary counting technique (total - invalid = valid)
- [ ] Calculate combinations C(n,k) for placement problems
- [ ] Analyze chess piece movement patterns mathematically
- [ ] Derive closed-form formulas for counting problems
- [ ] Handle large numbers and integer overflow in combinatorics

---

## Problem Statement

**Problem:** Given an n x n chessboard, count the number of ways to place two knights so that they do not attack each other. Output this count for all board sizes from 1 to n.

**Input:**
- A single integer n (1 <= n <= 10000)

**Output:**
- n lines, where line k contains the number of valid placements for a k x k board

**Constraints:**
- 1 <= n <= 10000

### Example

```
Input:
8

Output:
0
6
28
96
252
550
1056
1848
```

**Explanation:**
- For k=1: A 1x1 board has only 1 square, impossible to place 2 knights. Answer: 0
- For k=2: A 2x2 board has 4 squares, C(4,2)=6 ways to place knights, and no two squares are a knight's move apart. Answer: 6
- For k=3: A 3x3 board has 9 squares. C(9,2)=36 total ways, but 8 pairs attack each other. Answer: 36-8=28

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Instead of counting valid placements directly, what if we count all placements and subtract the invalid ones?

This is the **complementary counting** technique. Counting non-attacking pairs directly is complex because we'd need to consider many different relative positions. But counting attacking pairs is simpler because knights have a fixed attack pattern.

### Breaking Down the Problem

1. **What are we looking for?** Number of ways to place 2 knights that don't attack each other
2. **What information do we have?** Board size k x k
3. **What's the relationship between input and output?**
   - Total ways to place 2 knights = C(k^2, 2) = k^2 * (k^2 - 1) / 2
   - Attacking pairs = positions where knights can capture each other
   - Answer = Total - Attacking

### The Knight's Attack Pattern

A knight attacks in an "L" shape: 2 squares in one direction, 1 square perpendicular.

```
  . . X . X . .
  . X . . . X .
  . . . K . . .
  . X . . . X .
  . . X . X . .
```

Key insight: Two knights attack each other if and only if they occupy opposite corners of a 2x3 or 3x2 rectangle.

---

## Solution: Mathematical Formula

### Key Insight

> **The Trick:** Count 2x3 and 3x2 rectangles on the board. Each rectangle contains exactly 2 pairs of squares where knights attack each other.

### Formula Derivation

**Step 1: Total placements**
```
Total = C(k^2, 2) = k^2 * (k^2 - 1) / 2
```

**Step 2: Count attacking pairs**

For a 2x3 rectangle, the attacking pairs are the diagonal corners:
```
A . B      Knights at A attack B
. . .      Knights at C attack D
C . D      (2 attacking pairs per 2x3 rectangle)
```

Number of 2x3 rectangles that fit on a k x k board:
- Width 3, height 2: can place at (k-2) horizontal positions, (k-1) vertical positions
- Count: (k-2) * (k-1)

Number of 3x2 rectangles:
- Width 2, height 3: can place at (k-1) horizontal positions, (k-2) vertical positions
- Count: (k-1) * (k-2)

Each rectangle contributes 2 attacking pairs, so:
```
Attacking = 2 * (k-2)(k-1) + 2 * (k-1)(k-2) = 4 * (k-1) * (k-2)
```

**Step 3: Final formula**
```
Answer(k) = k^2 * (k^2 - 1) / 2  -  4 * (k-1) * (k-2)
```

### Why This Formula Works

The formula counts:
1. All possible ways to choose 2 squares from k^2 squares
2. Subtracts exactly those pairs where the squares form attacking positions
3. Knights attack from corners of 2x3/3x2 rectangles, each contributing 2 pairs

### Dry Run Example

Let's trace through for k = 4 (4x4 board):

```
Step 1: Calculate total placements
  Total squares = 4^2 = 16
  Total ways = C(16, 2) = 16 * 15 / 2 = 120

Step 2: Count attacking pairs
  2x3 rectangles: (4-2) * (4-1) = 2 * 3 = 6 rectangles
  3x2 rectangles: (4-1) * (4-2) = 3 * 2 = 6 rectangles
  Total rectangles = 12
  Attacking pairs = 12 * 2 = 24

Step 3: Calculate answer
  Answer = 120 - 24 = 96

Verification for small k values:
  k=1: Total = 0,   Attacking = 0,  Answer = 0
  k=2: Total = 6,   Attacking = 0,  Answer = 6
  k=3: Total = 36,  Attacking = 8,  Answer = 28
  k=4: Total = 120, Attacking = 24, Answer = 96
```

### Visual Diagram: Attacking Positions

```
2x3 Rectangle with attacking pairs marked:

  +---+---+---+        Knights at opposite corners attack:
  | A |   | B |        - A attacks B (diagonal)
  +---+---+---+        - C attacks D (diagonal)
  | C |   | D |        Total: 2 attacking pairs
  +---+---+---+

3x2 Rectangle rotated:

  +---+---+
  | A |   |
  +---+---+          Same logic: A-B and C-D
  |   |   |          attack each other
  +---+---+
  | C | B |
  +---+---+
```

---

## Code Solutions

### Python Solution

```python
def two_knights(n: int) -> list[int]:
 """
 Calculate non-attacking knight placements for boards 1x1 to nxn.

 Formula: k^2 * (k^2 - 1) / 2 - 4 * (k-1) * (k-2)

 Time: O(n) - single pass through board sizes
 Space: O(1) - constant space (excluding output)
 """
 results = []

 for k in range(1, n + 1):
  total_squares = k * k

  # Total ways to place 2 knights on k^2 squares
  total_placements = total_squares * (total_squares - 1) // 2

  # Attacking pairs: 4 * (k-1) * (k-2)
  # Each 2x3 or 3x2 rectangle contributes 2 attacking pairs
  attacking_pairs = 4 * (k - 1) * (k - 2)

  # Non-attacking = Total - Attacking
  answer = total_placements - attacking_pairs
  results.append(answer)

 return results


def main():
 n = int(input())
 results = two_knights(n)
 for result in results:
  print(result)


if __name__ == "__main__":
 main()
```

#### Complexity Analysis

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single loop from 1 to n |
| Space | O(1) | Only using constant extra variables |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** For k = 10000, k^4 exceeds int range (10^16 > 2^31).
**Fix:** Use `long long` and cast before multiplication.

### Mistake 2: Wrong Attacking Pair Count

```python
# WRONG - counting rectangles, not pairs
attacking = (k-2)*(k-1) + (k-1)*(k-2)  # Missing *2

# CORRECT - each rectangle has 2 attacking pairs
attacking = 4 * (k-1) * (k-2)
```

**Problem:** Each 2x3 rectangle has 2 diagonal attacking pairs, not 1.
**Fix:** Multiply by 2 for each rectangle type (total factor of 4).

### Mistake 3: Off-by-One in Rectangle Count

```python
# WRONG - incorrect bounds
rectangles_2x3 = (k-1) * (k-2)  # Should be (k-2) * (k-1)
        # Order matters for understanding

# CORRECT - think about it as:
# - A 2x3 rectangle needs 3 columns: fits (k-2) times horizontally
# - A 2x3 rectangle needs 2 rows: fits (k-1) times vertically
rectangles_2x3 = (k - 2) * (k - 1)  # width-fit * height-fit
```

**Problem:** Confusing which dimension subtracts 1 vs 2.
**Fix:** Remember: subtract (dimension_size - 1) from board dimension.

### Mistake 4: Starting Loop from Wrong Index

```python
# WRONG - missing k=1 case or wrong indexing
for k in range(n):  # 0 to n-1 instead of 1 to n
 ...

# CORRECT
for k in range(1, n + 1):
 ...
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single square | k=1 | 0 | Cannot place 2 knights on 1 square |
| 2x2 board | k=2 | 6 | C(4,2)=6, no attacks possible (too small for L-shape) |
| 3x3 board | k=3 | 28 | First board where attacks are possible |
| Large board | k=10000 | ~4.99*10^15 | Tests integer overflow handling |

---

## When to Use This Pattern

### Use Complementary Counting When:
- Direct counting of valid cases is complex
- Invalid cases follow a clear, countable pattern
- Total count is easy to calculate (combinations/permutations)

### Don't Use When:
- Invalid cases are harder to count than valid cases
- There's no clean formula for total possibilities
- The problem requires enumeration (not just counting)

### Pattern Recognition Checklist:
- [ ] Can I easily count total possibilities? (Yes: C(n,k))
- [ ] Do invalid cases have a geometric/pattern structure? (Yes: L-shape attack)
- [ ] Is it easier to count what I DON'T want? (Yes: attacking positions)
- [ ] Can I derive a closed-form formula? (Yes: 4*(k-1)*(k-2))

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Chessboard and Queens](https://cses.fi/problemset/task/1624) | Basic chess piece placement |
| [Apple Division](https://cses.fi/problemset/task/1623) | Combinatorial counting basics |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Grid Paths](https://cses.fi/problemset/task/1625) | Counting paths on a grid |
| [Counting Tilings](https://cses.fi/problemset/task/2181) | More complex combinatorics |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Two Bishops](https://codeforces.com/problemset/problem/1466/E) | Different piece, different pattern |
| [Counting Necklaces](https://cses.fi/problemset/task/2209) | Burnside's lemma for symmetry |

---

## Key Takeaways

1. **The Core Idea:** Use complementary counting: Total placements - Attacking placements = Valid placements

2. **Time Optimization:** Derive a closed-form O(1) formula per board size instead of enumerating positions

3. **Space Trade-off:** No extra space needed; pure mathematical calculation

4. **Pattern:** This is a classic "total minus invalid" combinatorics problem, common in competitive programming

5. **Chess Insight:** Two knights attack if and only if they are diagonal corners of a 2x3 or 3x2 rectangle

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the formula from scratch without looking at notes
- [ ] Explain why each 2x3 rectangle contributes exactly 2 attacking pairs
- [ ] Handle integer overflow in your implementation
- [ ] Recognize when to apply complementary counting in new problems

---

## Additional Resources

- [CP-Algorithms: Combinatorics](https://cp-algorithms.com/combinatorics/catalan-numbers.html)
- [CSES Two Knights](https://cses.fi/problemset/task/1072) - Chess combinatorics
- [Knight's Tour Problem](https://en.wikipedia.org/wiki/Knight%27s_tour) - Related chess combinatorics
