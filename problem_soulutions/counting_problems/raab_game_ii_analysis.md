---
layout: simple
title: "Raab Game II - Combinatorics Problem"
permalink: /problem_soulutions/counting_problems/raab_game_ii_analysis
difficulty: Medium
tags: [combinatorics, modular-arithmetic, counting, game-theory]
prerequisites: [modular_exponentiation]
---

# Raab Game II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Combinatorics / Counting |
| **Time Limit** | 1 second |
| **Key Technique** | Modular Exponentiation |
| **CSES Link** | - |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Derive counting formulas for sequence enumeration problems
- [ ] Apply modular exponentiation for efficient power computation
- [ ] Recognize when brute force enumeration can be replaced by closed-form formulas
- [ ] Handle large number computations with modular arithmetic

---

## Problem Statement

**Problem:** Count the number of ways to make k moves on a game board with n positions, where each move must go to a different position.

**Input:**
- Line 1: Two integers n (number of positions) and k (number of moves)

**Output:**
- The number of valid move sequences modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 10^6
- 0 <= k <= 10^6

### Example

```
Input:
3 2

Output:
6
```

**Explanation:** Starting from any of 3 positions, we make 2 moves where each move goes to a different position.
- From position 1: can go to 2 then 1 or 3, OR to 3 then 1 or 2 (4 paths, but wait...)

Actually, let us count more carefully:
- Start at 1, move to 2, move to 1 or 3 = 2 paths
- Start at 1, move to 3, move to 1 or 2 = 2 paths
- ... but we need to count ALL starting positions.

Formula: n starting positions x (n-1) choices per move x k moves = n x (n-1)^k = 3 x 2^2 = 3 x 4 = 12?

Wait, re-reading: if we just count SEQUENCES of k moves (not paths), then:
- n choices for start
- (n-1) choices for each of k moves
- Total = n x (n-1)^k

For n=3, k=2: 3 x 2^2 = 12. But output is 6...

The problem likely counts just the k-move SEQUENCES (without counting start position separately):
- Total = n x (n-1)^(k-1) with k moves means (k-1) transitions? Or just (n-1)^k for k transitions from a fixed start?

Given output 6 = 3 x 2 = n x (n-1)^1, it seems k=2 means 1 move/transition, giving n x (n-1) = 6.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count sequences where consecutive elements must differ?

This is a classic counting problem. Each position in our sequence has a fixed number of valid choices based on what came before. When choices are independent of history (except the immediate predecessor), we can use the multiplication principle.

### Breaking Down the Problem

1. **What are we counting?** Sequences of positions where adjacent positions differ
2. **What constraints exist?** Cannot stay in the same position (must move)
3. **What is the structure?** Each move has exactly (n-1) valid destinations

### The Key Insight

Think of this like a "no-repeat-adjacent" sequence:
- First position: n choices
- Each subsequent position: (n-1) choices (anything except current position)

This gives us the formula: **n x (n-1)^k** for a sequence of length (k+1) positions with k moves.

---

## Solution 1: Brute Force (Recursive Enumeration)

### Idea

Generate all possible sequences recursively and count valid ones.

### Algorithm

1. Start from each of n positions
2. For each position, recursively explore all (n-1) next positions
3. Count all complete sequences of k moves

### Code

```python
def count_sequences_brute(n, k):
 """
 Brute force: enumerate all sequences.

 Time: O(n * (n-1)^k) - exponential
 Space: O(k) - recursion depth
 """
 MOD = 10**9 + 7

 def dfs(current_pos, moves_left):
  if moves_left == 0:
   return 1

  count = 0
  for next_pos in range(1, n + 1):
   if next_pos != current_pos:
    count = (count + dfs(next_pos, moves_left - 1)) % MOD
  return count

 total = 0
 for start in range(1, n + 1):
  total = (total + dfs(start, k)) % MOD
 return total
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^k) | Exponential branching factor |
| Space | O(k) | Recursion stack depth |

### Why This Is Too Slow

For n = 10^6 and k = 10^6, we would need to enumerate 10^6,000,000 sequences - completely infeasible.

---

## Solution 2: Optimal (Closed-Form Formula)

### Key Insight

> **The Trick:** Each position independently has (n-1) choices, so total = n x (n-1)^k

Since the number of choices at each step is constant (always n-1), we can directly compute the count using exponentiation.

### Formula Derivation

```
Position 0 (start): n choices
Position 1: (n-1) choices (anything except position 0)
Position 2: (n-1) choices (anything except position 1)
...
Position k: (n-1) choices (anything except position k-1)

Total = n * (n-1) * (n-1) * ... * (n-1)
      = n * (n-1)^k
```

### Algorithm

1. Handle edge case: if n = 1 and k > 0, return 0 (no valid moves)
2. Compute (n-1)^k using fast modular exponentiation
3. Multiply by n and return result mod 10^9 + 7

### Dry Run Example

Let us trace through with n = 3, k = 2:

```
Step 1: Identify the formula
  Total sequences = n * (n-1)^k

Step 2: Substitute values
  = 3 * (3-1)^2
  = 3 * 2^2
  = 3 * 4
  = 12

Wait - but expected output is 6. Let me reconsider...

If k represents the LENGTH of sequence (not number of moves):
  k = 2 means sequence of 2 positions with 1 move
  Total = n * (n-1)^(k-1) = 3 * 2^1 = 6  [Matches!]

So the formula depends on problem interpretation:
  - If k = number of moves: n * (n-1)^k
  - If k = sequence length: n * (n-1)^(k-1)
```

### Visual Diagram

```
n = 3 positions: {1, 2, 3}
k = 2 (sequence length)

All valid sequences of length 2:
  Start=1: [1,2], [1,3]       -> 2 sequences
  Start=2: [2,1], [2,3]       -> 2 sequences
  Start=3: [3,1], [3,2]       -> 2 sequences
                              ---------------
                              Total: 6 sequences

Formula: 3 * 2^(2-1) = 3 * 2 = 6
```

### Code

```python
def count_sequences(n, k):
 """
 Optimal: use closed-form formula with modular exponentiation.

 Time: O(log k) - binary exponentiation
 Space: O(1)
 """
 MOD = 10**9 + 7

 # Edge case: single position, cannot make any moves
 if n == 1:
  return 1 if k <= 1 else 0

 # Formula: n * (n-1)^(k-1) for sequence length k
 # Or: n * (n-1)^k for k moves
 # Using built-in pow with modular arithmetic
 if k == 0:
  return 0  # No sequence of length 0

 return (n * pow(n - 1, k - 1, MOD)) % MOD


def count_moves(n, k):
 """
 Alternative: count sequences with exactly k moves.

 Time: O(log k)
 Space: O(1)
 """
 MOD = 10**9 + 7

 if n == 1:
  return 0 if k > 0 else n

 return (n * pow(n - 1, k, MOD)) % MOD
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(log k) | Binary exponentiation |
| Space | O(1) | Only scalar variables |

---

## Common Mistakes

### Mistake 1: Integer Overflow

```python
# WRONG - overflow for large n, k
def count_wrong(n, k):
 return n * (n - 1) ** k  # Overflow!

# CORRECT - use modular arithmetic throughout
def count_correct(n, k):
 MOD = 10**9 + 7
 return (n * pow(n - 1, k, MOD)) % MOD
```

**Problem:** Python handles big integers, but the result must be modulo 10^9 + 7.
**Fix:** Use `pow(base, exp, mod)` for modular exponentiation.

### Mistake 2: Wrong Base Case for n = 1

```python
# WRONG - returns non-zero for impossible case
def count_wrong(n, k):
 return n * pow(n - 1, k, MOD)  # When n=1, this gives 1 * 0^k

# CORRECT - explicitly handle edge case
def count_correct(n, k):
 if n == 1 and k > 0:
  return 0  # Cannot move anywhere
 return (n * pow(n - 1, k, MOD)) % MOD
```

**Problem:** With only one position, you cannot make any moves.
**Fix:** Return 0 when n = 1 and k > 0.

### Mistake 3: Confusing Moves vs Sequence Length

```python
# Different interpretations!
# If k = number of moves (transitions):
result = n * pow(n - 1, k, MOD)

# If k = sequence length (number of positions):
result = n * pow(n - 1, k - 1, MOD)
```

**Problem:** The formula changes based on what k represents.
**Fix:** Read the problem carefully to determine the correct interpretation.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single position, no moves | n=1, k=0 | 1 | One valid "empty" sequence |
| Single position, with moves | n=1, k=5 | 0 | Cannot move anywhere |
| Zero moves | n=5, k=0 | 0 or 5 | Depends on interpretation |
| Large values | n=10^6, k=10^6 | Compute | Must use mod arithmetic |
| Two positions | n=2, k=3 | 2 | Alternates: 121, 212 |

---

## When to Use This Pattern

### Use Closed-Form Counting When:
- Each step has a fixed number of independent choices
- The total count follows a simple product formula
- Direct enumeration would be exponential

### Recognize This Pattern When You See:
- "Count the number of ways..."
- "How many sequences..."
- Constraints like "adjacent elements must differ"
- Large constraints (n, k up to 10^6) requiring O(log n) solution

### Pattern Recognition Checklist:
- [ ] Fixed number of choices at each step? Consider **multiplication principle**
- [ ] Need to compute a^b mod m efficiently? Use **binary exponentiation**
- [ ] Counting sequences with constraints? Look for **closed-form formulas**

---

## Related Problems

### Prerequisites (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Exponentiation](https://cses.fi/problemset/task/1095) | Learn modular exponentiation |
| [Exponentiation II](https://cses.fi/problemset/task/1712) | Advanced modular arithmetic |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Counting Rooms](https://cses.fi/problemset/task/1192) | Grid-based counting |
| [Creating Strings](https://cses.fi/problemset/task/1622) | Permutation counting |
| [Distributing Apples](https://cses.fi/problemset/task/1716) | Stars and bars technique |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Bracket Sequences I](https://cses.fi/problemset/task/2064) | Catalan numbers |
| [Graph Paths I](https://cses.fi/problemset/task/1723) | Matrix exponentiation |
| [Dice Combinations](https://cses.fi/problemset/task/1633) | DP counting |

---

## Key Takeaways

1. **The Core Formula:** Sequences where adjacent elements differ: n * (n-1)^(moves)
2. **Time Optimization:** O(n^k) enumeration reduced to O(log k) via closed-form + fast exponentiation
3. **Space Optimization:** O(k) recursion stack eliminated entirely
4. **Pattern:** When choices are constant and independent, use the multiplication principle

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the formula n * (n-1)^k from first principles
- [ ] Implement binary exponentiation from scratch
- [ ] Explain why modular arithmetic is necessary
- [ ] Solve this problem in under 5 minutes

---

## Additional Resources

- [CP-Algorithms: Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [CP-Algorithms: Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html)
- [CSES Exponentiation](https://cses.fi/problemset/task/1095) - Modular power computation
