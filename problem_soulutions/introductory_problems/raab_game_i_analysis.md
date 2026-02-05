---
layout: simple
title: "Raab Game I - Game Theory Problem"
permalink: /problem_soulutions/introductory_problems/raab_game_i_analysis
difficulty: Easy
tags: [game-theory, nim, dp, winning-losing-positions]
---

# Raab Game I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Stick Game](https://cses.fi/problemset/task/1729) |
| **Difficulty** | Easy |
| **Category** | Game Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Winning/Losing Position Analysis |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Identify winning and losing positions in impartial games
- [ ] Apply backward induction to determine optimal play
- [ ] Implement game theory DP with O(n * k) complexity
- [ ] Recognize the pattern: a position is winning if any reachable position is losing

---

## Problem Statement

**Problem:** There is a pile of `n` sticks. Two players take turns removing sticks. On each turn, a player must remove exactly `p` sticks, where `p` is one of the allowed values from set `{a1, a2, ..., ak}`. The player who cannot make a move loses. Determine the winner assuming both players play optimally.

**Input:**
- Line 1: Two integers `n` and `k` (number of sticks and number of allowed moves)
- Line 2: `k` integers `a1, a2, ..., ak` (allowed moves)

**Output:**
- Print "W" if the first player wins, "L" if the first player loses

**Constraints:**
- 1 <= n <= 10^6
- 1 <= k <= 100
- 1 <= ai <= n

### Example

```
Input:
10 3
1 2 5

Output:
WLWWWWWWWL
```

**Explanation:** The output shows the result for each pile size from 1 to n:
- n=1: First player removes 1, wins (W)
- n=2: First player removes 1 or 2, wins (W)
- n=3: Any move leaves opponent in winning position, loses (L)
- ... and so on

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** What determines if a position is winning or losing?

A position is a **winning position (W)** if there exists at least one move to a losing position. A position is a **losing position (L)** if all moves lead to winning positions (for the opponent).

### Breaking Down the Problem

1. **What are we looking for?** Whether position n is W or L
2. **What information do we have?** All allowed moves and the starting position
3. **What's the relationship?** If I can move to ANY losing position, I win; if ALL my moves lead to winning positions, I lose

### Analogies

Think of it like a game where you want to "pass the hot potato" to your opponent. A losing position is like being stuck with the hot potato with no way to pass it. A winning position means you have at least one way to pass it and force your opponent into a bad spot.

---

## Solution 1: Brute Force (Recursion with Memoization)

### Idea

Recursively determine if each position is winning or losing by checking all possible moves.

### Algorithm

1. Base case: Position 0 is losing (no moves available)
2. For position i, try all valid moves
3. If any move leads to a losing position, current position is winning
4. Use memoization to avoid recomputation

### Code

```python
def solve_recursive(n: int, moves: list) -> str:
 """
 Recursive solution with memoization.

 Time: O(n * k)
 Space: O(n)
 """
 memo = {}

 def is_winning(pos: int) -> bool:
  if pos in memo:
   return memo[pos]
  if pos == 0:
   return False  # No moves = lose

  # Check if any move leads to losing position
  for move in moves:
   if move <= pos and not is_winning(pos - move):
    memo[pos] = True
    return True

  memo[pos] = False
  return False

 return "W" if is_winning(n) else "L"
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * k) | Each position computed once, k moves checked |
| Space | O(n) | Recursion stack + memoization |

### Why This Works (But Is Slow)

The recursion explores all positions but can hit stack limits for large n.

---

## Solution 2: Bottom-Up DP (Optimal)

### Key Insight

> **The Trick:** Build the solution from position 0 upward. Position 0 is always losing. For each position, check if any valid move leads to a losing position.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i]` | True if position i is winning, False if losing |

**In plain English:** `dp[i]` tells us whether the player whose turn it is with i sticks will win.

### State Transition

```
dp[i] = True   if exists move m where dp[i-m] = False
dp[i] = False  if for all moves m, dp[i-m] = True
```

**Why?** If you can reach ANY losing position, you win. If ALL reachable positions are winning (for opponent), you lose.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | False | No sticks = cannot move = lose |

### Algorithm

1. Initialize dp[0] = False (losing position)
2. For each position i from 1 to n:
   - For each allowed move m:
     - If m <= i and dp[i-m] is False, then dp[i] = True
3. Return dp[n]

### Dry Run Example

Let's trace through with `n = 10, moves = [1, 2, 5]`:

```
Initial: dp[0] = False (L)

Position 1:
  Try move 1: dp[1-1] = dp[0] = False (L)
  Found losing position! dp[1] = True (W)

Position 2:
  Try move 1: dp[2-1] = dp[1] = True (W) - no help
  Try move 2: dp[2-2] = dp[0] = False (L)
  Found losing position! dp[2] = True (W)

Position 3:
  Try move 1: dp[3-1] = dp[2] = True (W) - no help
  Try move 2: dp[3-2] = dp[1] = True (W) - no help
  (move 5 > 3, skip)
  All moves lead to W! dp[3] = False (L)

Position 4:
  Try move 1: dp[4-1] = dp[3] = False (L)
  Found losing position! dp[4] = True (W)

Position 5:
  Try move 1: dp[5-1] = dp[4] = True (W) - no help
  Try move 2: dp[5-2] = dp[3] = False (L)
  Found losing position! dp[5] = True (W)

...continuing this pattern...

Final dp array (1-indexed output):
Position:  1  2  3  4  5  6  7  8  9  10
Result:    W  W  L  W  W  W  W  W  W  L
```

### Visual Diagram

```
Position:    0   1   2   3   4   5   6   7   8   9   10
             L   W   W   L   W   W   W   W   W   W   L
             ^
           base
             |
             +-- dp[1]: can reach dp[0]=L, so W
             +-- dp[2]: can reach dp[0]=L, so W
             +-- dp[3]: reaches dp[2]=W, dp[1]=W only, so L
             +-- dp[4]: can reach dp[3]=L, so W
             ...
             +-- dp[10]: reaches dp[9]=W, dp[8]=W, dp[5]=W, so L

Transition arrows for position 10:
  10 --(-1)--> 9 (W)
  10 --(-2)--> 8 (W)
  10 --(-5)--> 5 (W)
  All paths lead to W, so position 10 is L
```

### Code (Python)

```python
def solve(n: int, k: int, moves: list) -> str:
 """
 Bottom-up DP solution for stick game.

 Time: O(n * k)
 Space: O(n)
 """
 # dp[i] = True if position i is winning
 dp = [False] * (n + 1)

 # Base case: dp[0] = False (no moves = lose)

 for i in range(1, n + 1):
  for move in moves:
   if move <= i and not dp[i - move]:
    dp[i] = True
    break  # Found winning move, no need to check others

 # Build result string for all positions 1 to n
 result = ''.join('W' if dp[i] else 'L' for i in range(1, n + 1))
 return result


def main():
 n, k = map(int, input().split())
 moves = list(map(int, input().split()))
 print(solve(n, k, moves))


if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * k) | For each of n positions, check up to k moves |
| Space | O(n) | DP array of size n+1 |

---

## Common Mistakes

### Mistake 1: Wrong Base Case

```python
# WRONG - dp[0] should be False, not True
dp = [True] * (n + 1)
```

**Problem:** Position 0 means no sticks left; the current player cannot move and loses.
**Fix:** Initialize `dp[0] = False`.

### Mistake 2: Checking dp[i-move] = True Instead of False

```python
# WRONG - looking for winning positions to move to
if move <= i and dp[i - move]:
 dp[i] = True

# CORRECT - looking for LOSING positions to move to
if move <= i and not dp[i - move]:
 dp[i] = True
```

**Problem:** You want to leave your opponent in a LOSING position, not a winning one.
**Fix:** Check for `not dp[i - move]`.

### Mistake 3: Forgetting to Check Move Validity

```python
# WRONG - may access negative index
if not dp[i - move]:
 dp[i] = True

# CORRECT - check if move is valid
if move <= i and not dp[i - move]:
 dp[i] = True
```

**Problem:** If move > i, accessing dp[i - move] accesses negative indices.
**Fix:** Always check `move <= i` first.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single stick, single move | n=1, moves=[1] | W | Can remove 1, win |
| No valid move from start | n=1, moves=[2] | L | Cannot make any move |
| Move equals n | n=5, moves=[5] | W | Can take all sticks immediately |
| All moves > n | n=3, moves=[4,5] | L | No valid moves possible |
| Classic Nim (remove 1-3) | n=4, moves=[1,2,3] | L | Position 4 is losing in Nim |

---

## When to Use This Pattern

### Use This Approach When:
- Two players take turns in a game
- The game has perfect information (both players see everything)
- You need to determine who wins with optimal play
- The game state can be represented by a single number or small tuple

### Don't Use When:
- Multiple piles exist (use Sprague-Grundy theorem instead)
- Game has randomness or hidden information
- State space is too large for DP (consider game tree search)

### Pattern Recognition Checklist:
- [ ] Two-player alternating game? -> **Consider W/L analysis**
- [ ] One pile/counter? -> **Use simple DP**
- [ ] Multiple piles? -> **Learn Sprague-Grundy / XOR**
- [ ] Need to count ways to win? -> **Different problem type**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Nim Game (LeetCode)](https://leetcode.com/problems/nim-game/) | Simplest game theory problem |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Stick Game (CSES)](https://cses.fi/problemset/task/1729) | Same problem, different name |
| [Can I Win (LeetCode)](https://leetcode.com/problems/can-i-win/) | Bitmask DP for state |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Nim Game II (CSES)](https://cses.fi/problemset/task/1730) | Multiple piles, XOR |
| [Grundy's Game (CSES)](https://cses.fi/problemset/task/2207) | Sprague-Grundy numbers |
| [Staircase Nim](https://cses.fi/problemset/task/1099) | Modified Nim rules |

---

## Key Takeaways

1. **The Core Idea:** A position is winning if you can move to ANY losing position; losing if ALL moves lead to winning positions
2. **Time Optimization:** Bottom-up DP avoids recursion overhead and stack limits
3. **Space Trade-off:** O(n) space for DP array
4. **Pattern:** Backward induction from base case (position 0 = lose)

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why dp[0] = False
- [ ] Trace through a small example by hand
- [ ] Identify winning and losing positions without code
- [ ] Implement the DP solution in under 10 minutes
- [ ] Extend the solution to print the actual winning move (not just W/L)

---

## Additional Resources

- [CP-Algorithms: Game Theory](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- [CSES Nim Game I](https://cses.fi/problemset/task/1730) - Classic game theory
- [TopCoder: Algorithm Games](https://www.topcoder.com/thrive/articles/Algorithm%20Games)
