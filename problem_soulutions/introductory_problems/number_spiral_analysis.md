---
layout: simple
title: "Number Spiral - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/number_spiral_analysis
difficulty: Easy
tags: [math, pattern, formula, spiral]
---

# Number Spiral

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Problem Link** | [CSES 1071 - Number Spiral](https://cses.fi/problemset/task/1071) |
| **Difficulty** | Easy |
| **Category** | Math / Pattern Recognition |
| **Time Limit** | 1 second |
| **Key Technique** | Layer-based O(1) formula |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize diagonal layer patterns in 2D grids
- [ ] Derive O(1) formulas for coordinate-based calculations
- [ ] Handle alternating direction patterns based on parity
- [ ] Convert between 1-indexed coordinates and mathematical formulas

---

## Problem Statement

**Problem:** A number spiral is an infinite grid where positive integers are written in diagonal layers. Given row `y` and column `x`, find the value at position `(y, x)`.

The spiral is constructed as follows:
```
 1   2   9  10  25 ...
 4   3   8  11  24
 5   6   7  12  23
16  15  14  13  22
17  18  19  20  21
...
```

**Input:**
- Line 1: Number of test cases `t` (1 <= t <= 10^5)
- Lines 2 to t+1: Two integers `y` and `x` (1 <= y, x <= 10^9)

**Output:**
- For each test case, print the value at position `(y, x)`

**Constraints:**
- 1 <= t <= 10^5
- 1 <= y, x <= 10^9

### Example

```
Input:
3
2 3
1 1
4 2

Output:
8
1
15
```

**Explanation:**
- Position (2, 3): Looking at the grid, row 2 column 3 has value 8
- Position (1, 1): Top-left corner is always 1
- Position (4, 2): Row 4 column 2 has value 15

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How are numbers arranged in this spiral? What determines the value at any position?

The spiral fills numbers along **diagonal layers**. Each layer `k` forms an L-shape starting from position `(k, 1)` or `(1, k)`. The crucial insight is that the layer number is determined by `max(y, x)`, and within each layer, numbers flow in **alternating directions** (down/right for odd layers, up/left for even layers).

### Breaking Down the Problem

1. **What layer is position (y, x) in?** Layer `k = max(y, x)`
2. **What's the starting number of layer k?** The corner value at the start of layer k
3. **Where in the layer is (y, x)?** Count steps from the layer's starting corner

### Analogies

Think of this like floors in a building where each floor has an L-shaped hallway. Floor `k` starts at room `(k-1)^2 + 1` and wraps around in alternating directions. To find a specific room, you determine which floor it's on, then count how far along the hallway it is.

### Visual: Layer Structure

```
Layer 1:  (1,1)                    Numbers: 1
Layer 2:  (1,2)-(2,2)-(2,1)        Numbers: 2,3,4
Layer 3:  (3,1)-(3,2)-(3,3)        Numbers: 5,6,7
          (2,3)-(1,3)                       8,9
Layer 4:  (1,4)-(2,4)-(3,4)-(4,4)  Numbers: 10,11,12,13
          (4,3)-(4,2)-(4,1)                 14,15,16
```

**Key Observation:** Layer `k` contains numbers from `(k-1)^2 + 1` to `k^2`.

---

## Solution: O(1) Mathematical Formula

### Key Insight

> **The Trick:** Every position (y, x) lies on layer `k = max(y, x)`. The layer's corner value and direction alternation (based on k's parity) let us compute the answer directly.

### Layer Properties

| Property | Formula | Explanation |
|----------|---------|-------------|
| Layer number | `k = max(y, x)` | The larger coordinate determines the layer |
| Layer start | `(k-1)^2 + 1` | First number in layer k |
| Layer end | `k^2` | Last number in layer k |
| Direction | Odd k: down then right; Even k: right then down | Alternates each layer |

### The Formula Derivation

**Step 1: Identify the layer**
```
k = max(y, x)
```

**Step 2: Determine if we're on the row part or column part of the L-shape**
- If `y >= x`: We're on the vertical part of the L
- If `x > y`: We're on the horizontal part of the L

**Step 3: Calculate position based on layer parity**

For **odd layers** (k is odd):
- Numbers go DOWN the column, then RIGHT along the row
- At (k, 1): value = (k-1)^2 + 1
- At (k, k): value = (k-1)^2 + k (the corner)
- At (1, k): value = k^2

For **even layers** (k is even):
- Numbers go RIGHT along the row, then DOWN the column
- At (1, k): value = (k-1)^2 + 1
- At (k, k): value = (k-1)^2 + k (the corner)
- At (k, 1): value = k^2

### Algorithm

1. Compute `k = max(y, x)` to identify the layer
2. If k is odd:
   - If `y >= x`: answer = `(k-1)^2 + y`
   - Else: answer = `k^2 - x + 1`
3. If k is even:
   - If `y >= x`: answer = `k^2 - y + 1`
   - Else: answer = `(k-1)^2 + x`

### Dry Run Example

**Example 1:** Input `(y=2, x=3)`

```
Step 1: Find the layer
  k = max(2, 3) = 3

Step 2: Determine parity
  k = 3 is ODD

Step 3: Determine position type
  x > y, so we're on the horizontal part (going up column k)

Step 4: Apply formula
  answer = k^2 - y + 1 = 9 - 2 + 1 = 8

Verify: Grid shows (2,3) = 8
```

**Example 2:** Input `(y=4, x=2)`

```
Step 1: k = max(4, 2) = 4

Step 2: k = 4 is EVEN

Step 3: y >= x, so we're on the horizontal part (row k, going left)

Step 4: Apply formula
  answer = k^2 - x + 1 = 16 - 2 + 1 = 15

Verify: Grid shows (4,2) = 15
```

**Example 3:** Input `(y=1, x=1)`

```
Step 1: k = max(1, 1) = 1

Step 2: k = 1 is ODD

Step 3: y >= x

Step 4: answer = (k-1)^2 + y = 0 + 1 = 1

Verify: Origin is always 1
```

**Summary of Formulas:**

```
k = max(y, x)

If k is ODD:
  - If y >= x: answer = (k-1)^2 + y     # vertical part
  - If x > y:  answer = k^2 - y + 1     # horizontal part

If k is EVEN:
  - If y >= x: answer = k^2 - x + 1     # horizontal part
  - If x > y:  answer = (k-1)^2 + x     # vertical part
```

### Visual Diagram

```
Layer k determines the "ring" of the spiral:

k=1     k=2       k=3         k=4
 1    | 2  9   | 2  9     | 2  9  10
      | 4  3   | 4  3  8  | 4  3   8  11
               | 5  6  7  | 5  6   7  12
                          |16 15  14  13

Odd layers (1,3,5...): Fill DOWN then UP
Even layers (2,4,6...): Fill RIGHT then DOWN
```

### Code

**Python Solution:**

```python
def solve(y: int, x: int) -> int:
    """
    Find value at position (y, x) in the number spiral.

    Time: O(1)
    Space: O(1)
    """
    k = max(y, x)  # Layer number

    if k % 2 == 1:  # Odd layer
        if y >= x:
            return (k - 1) * (k - 1) + y
        else:
            return k * k - y + 1
    else:  # Even layer
        if y >= x:
            return k * k - x + 1
        else:
            return (k - 1) * (k - 1) + x


def main():
    t = int(input())
    results = []
    for _ in range(t):
        y, x = map(int, input().split())
        results.append(solve(y, x))
    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(1) per query | Direct formula calculation |
| Space | O(1) | Only a few variables |
| Total Time | O(t) | t queries, each O(1) |

---

## Common Mistakes

### Mistake 1: Forgetting Direction Alternation

```python
# WRONG - Using same formula for all layers
def solve_wrong(y, x):
    k = max(y, x)
    if y >= x:
        return (k - 1) * (k - 1) + y  # Wrong for even layers!
    else:
        return k * k - y + 1
```

**Problem:** The spiral alternates direction between odd and even layers. Using the same formula ignores this.

**Fix:** Check `k % 2` and use the appropriate formula for each parity.

### Mistake 2: Using 0-indexed Coordinates

```python
# WRONG - Treating input as 0-indexed
def solve_wrong(y, x):
    y += 1  # DON'T do this!
    x += 1
    k = max(y, x)
    # ...
```

**Problem:** The problem uses 1-indexed coordinates. Adding 1 shifts all answers incorrectly.

**Fix:** Use the coordinates as given; they are already 1-indexed.

### Mistake 3: Integer Overflow

**Problem:** When y, x can be up to 10^9, k^2 can be up to 10^18, exceeding 32-bit int range.

**Fix:** Use `long long` for all calculations involving k^2.

### Mistake 4: Wrong Boundary Condition

```python
# WRONG - Using > instead of >=
if y > x:  # Should be y >= x
    return (k - 1) * (k - 1) + y
```

**Problem:** When y == x (diagonal), the position belongs to a specific part of the L-shape depending on direction.

**Fix:** The condition should be `y >= x` for odd layers and the same for even layers.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Origin | y=1, x=1 | 1 | Top-left corner is always 1 |
| First row | y=1, x=5 | 25 | k=5 (odd), x>y: k^2-y+1 = 25-1+1 = 25 |
| First column | y=5, x=1 | 21 | k=5 (odd), y>=x: (k-1)^2+y = 16+5 = 21 |
| Diagonal (odd) | y=3, x=3 | 7 | k=3 (odd), y>=x: (k-1)^2+y = 4+3 = 7 |
| Diagonal (even) | y=4, x=4 | 13 | k=4 (even), y>=x: k^2-x+1 = 16-4+1 = 13 |
| Large coordinates | y=10^9, x=1 | 999999999000000001 | k=10^9 (even), y>=x: k^2-x+1 |
| Equal large (odd) | y=10^9-1, x=10^9-1 | (10^9-2)^2+(10^9-1) | Diagonal on odd layer |

---

## When to Use This Pattern

### Use This Approach When:
- The problem involves a 2D grid with a predictable filling pattern
- You need O(1) lookup for coordinates in a spiral or diagonal pattern
- Layer-based decomposition reveals a mathematical structure
- Values follow a sequential ordering along some path

### Don't Use When:
- The spiral has irregular or input-dependent patterns
- You need to traverse or modify the actual grid
- The pattern doesn't have a closed-form mathematical description

### Pattern Recognition Checklist:
- [ ] Values arranged in concentric layers or rings? -> **Layer-based formula**
- [ ] Pattern alternates based on layer/ring number? -> **Check parity (odd/even)**
- [ ] Need value at arbitrary coordinate? -> **Derive O(1) closed-form formula**
- [ ] Sequential filling along a path? -> **Identify path direction and starting points**

---

## Related Problems

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES - Two Knights](https://cses.fi/problemset/task/1072) | Counting problem with formula derivation |
| [LeetCode 59 - Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) | Generate spiral, not query |
| [LeetCode 54 - Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Traverse spiral order |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [LeetCode 885 - Spiral Matrix III](https://leetcode.com/problems/spiral-matrix-iii/) | Bounded spiral with coordinates |
| [CSES - Chessboard and Queens](https://cses.fi/problemset/task/1624) | 2D grid with constraints |

---

## Key Takeaways

1. **The Core Idea:** The spiral can be decomposed into layers where `max(y, x)` determines the layer, and parity determines the direction.

2. **Mathematical Insight:** Each layer k contains numbers from `(k-1)^2 + 1` to `k^2`, with 2k-1 cells.

3. **Direction Matters:** Odd layers fill down-then-right; even layers fill right-then-down. Getting this wrong breaks the solution.

4. **Pattern:** This is a coordinate-to-value mapping problem solvable with O(1) formulas once you understand the structure.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Draw the first 5 layers of the spiral from memory
- [ ] Derive the formula for odd and even layers independently
- [ ] Explain why `max(y, x)` determines the layer
- [ ] Handle the test cases without running the code
- [ ] Implement in your preferred language in under 5 minutes

---

## Additional Resources

- [CSES Number Spiral](https://cses.fi/problemset/task/1071) - Spiral pattern queries
- [Spiral Matrix patterns on CP-Algorithms](https://cp-algorithms.com/)
