---
layout: simple
title: "Stones - Game Theory DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/stones_analysis
difficulty: Medium
tags: [game-theory, dp, nim, combinatorial-games]
---

# Stones

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Dynamic Programming / Game Theory |
| **Time Limit** | 2 seconds |
| **Key Technique** | Win/Lose Position DP |
| **Link** | [AtCoder DP Contest - K Stones](https://atcoder.jp/contests/dp/tasks/dp_k) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Identify impartial games where DP determines the winner
- [ ] Understand winning (W) and losing (L) position concepts
- [ ] Apply the key game theory principle: a position is winning if any move leads to a losing position
- [ ] Build DP solutions for turn-based games with optimal play

---

## Problem Statement

**Problem:** Two players play a game with N stones. They take turns, and on each turn, a player must remove exactly a_1, a_2, ..., or a_K stones (choosing one value from the given set). The player who cannot make a move (no valid moves available) loses. Determine who wins if both players play optimally.

**Input:**
- Line 1: N K (number of stones, number of move options)
- Line 2: a_1, a_2, ..., a_K (the allowed move values)

**Output:**
- Print "First" if the first player wins, "Second" otherwise

**Constraints:**
- 1 <= N <= 10^5
- 1 <= K <= 100
- 1 <= a_i <= N

### Example

```
Input:
4 2
2 3

Output:
First
```

**Explanation:** With 4 stones and moves {2, 3}:
- First player takes 3 stones, leaving 1 stone
- Second player cannot take 2 or 3 stones (only 1 remains)
- Second player loses, so First wins

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we determine who wins a two-player game with optimal play?

This is a classic **impartial game** where:
1. Both players have the same available moves
2. The game state depends only on the number of stones remaining
3. The player unable to move loses (normal play convention)

The core insight is that every game position is either a **Winning (W)** or **Losing (L)** position:
- **Losing Position (L):** ALL moves lead to winning positions for the opponent
- **Winning Position (W):** At least ONE move leads to a losing position for the opponent

### Breaking Down the Problem

1. **What are we looking for?** Whether position N is a winning or losing position for the first player
2. **What information do we have?** The set of valid moves and the starting stone count
3. **What's the relationship?** A position depends on the positions reachable by one move

### Analogies

Think of this problem like a chess endgame analysis. In chess, you work backwards from checkmate positions to determine which positions are winning. Here, we work forward from 0 stones (a losing position) to determine all positions up to N.

---

## Solution: Game Theory DP

### Key Insight

> **The Trick:** Position 0 is always a Losing position (can't move). For each subsequent position, check if any move leads to a Losing position - if yes, it's Winning; if all moves lead to Winning positions, it's Losing.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i]` | True if position with i stones is a Winning position for the player to move |

**In plain English:** `dp[i]` answers "Can the player whose turn it is win if there are i stones?"

### State Transition

```
dp[i] = True   if EXISTS move m in moves where dp[i - m] = False
dp[i] = False  if FOR ALL moves m in moves, dp[i - m] = True
```

**Why?** If you can move to ANY losing position, your opponent will be in a losing position and you win. If ALL your moves lead to winning positions, your opponent will always be in a winning position and you lose.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | False (L) | No stones means no valid move - you lose |

### Algorithm

1. Initialize `dp[0] = False` (losing position - can't move)
2. For each position i from 1 to N:
   - Check each move m in the allowed moves
   - If m <= i and dp[i - m] is False, set dp[i] = True and break
3. Return "First" if dp[N] is True, else "Second"

### Dry Run Example

Let's trace through with input `N = 4, moves = [2, 3]`:

```
Initial state:
  dp = [F, ?, ?, ?, ?]  (F = False/Lose, T = True/Win)
  moves = [2, 3]

Position 0: Base case
  dp[0] = False (no moves possible = Lose)
  dp = [F, ?, ?, ?, ?]

Position 1: Check moves {2, 3}
  move=2: 2 > 1, skip (can't remove 2 from 1 stone)
  move=3: 3 > 1, skip
  No valid moves lead to L position
  dp[1] = False (Lose)
  dp = [F, F, ?, ?, ?]

Position 2: Check moves {2, 3}
  move=2: 2 <= 2, check dp[2-2] = dp[0] = False (L)
  Found move to losing position!
  dp[2] = True (Win)
  dp = [F, F, T, ?, ?]

Position 3: Check moves {2, 3}
  move=2: 2 <= 3, check dp[3-2] = dp[1] = False (L)
  Found move to losing position!
  dp[3] = True (Win)
  dp = [F, F, T, T, ?]

Position 4: Check moves {2, 3}
  move=2: 2 <= 4, check dp[4-2] = dp[2] = True (W)
  move=3: 3 <= 4, check dp[4-3] = dp[1] = False (L)
  Found move to losing position!
  dp[4] = True (Win)
  dp = [F, F, T, T, T]

Result: dp[4] = True -> "First" wins
```

### Visual Diagram

```
Stones:    0     1     2     3     4
           |     |     |     |     |
Position:  L     L     W     W     W
           ^     ^     |     |     |
           |     |     |     |     |
           no    no   take  take  take
          move  move   2     2     3
                       |     |     |
                       v     v     v
                       0(L)  1(L)  1(L)

Legend: L = Losing position, W = Winning position
Arrow shows optimal move to force opponent into L position
```

### Code (Python)

```python
def solve():
 """
 Game Theory DP solution for Stones problem.

 Time: O(N * K) - check K moves for each of N positions
 Space: O(N) - dp array
 """
 line1 = input().split()
 n, k = int(line1[0]), int(line1[1])
 moves = list(map(int, input().split()))

 # dp[i] = True if position i is winning for player to move
 dp = [False] * (n + 1)

 # Base case: dp[0] = False (no moves = lose)
 # Already initialized to False

 for i in range(1, n + 1):
  for move in moves:
   if move <= i and not dp[i - move]:
    # Found a move to losing position -> this is winning
    dp[i] = True
    break

 print("First" if dp[n] else "Second")

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N * K) | For each of N positions, check up to K moves |
| Space | O(N) | DP array of size N+1 |

---

## Common Mistakes

### Mistake 1: Wrong Base Case

```python
# WRONG
dp[0] = True  # Thinking "0 stones means I already won"

# CORRECT
dp[0] = False  # 0 stones = can't move = you LOSE
```

**Problem:** The player who cannot move loses, not wins. Position 0 means it's your turn but you can't do anything.

**Fix:** Remember the rule: "Player who cannot make a move loses."

### Mistake 2: Checking All Moves Instead of Early Break

```python
# INEFFICIENT (still correct, but slower)
for move in moves:
 if move <= i and not dp[i - move]:
  dp[i] = True
  # Missing break - continues checking unnecessarily

# CORRECT
for move in moves:
 if move <= i and not dp[i - move]:
  dp[i] = True
  break  # One losing successor is enough
```

**Problem:** Once we find ONE move to a losing position, we know this is winning - no need to check more.

**Fix:** Add `break` after setting dp[i] = True.

### Mistake 3: Confusing Who Wins

```python
# WRONG
print("First" if not dp[n] else "Second")

# CORRECT
print("First" if dp[n] else "Second")
```

**Problem:** dp[n] = True means position N is winning for the player to move (First player).

**Fix:** First player wins when dp[n] is True.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single move covers all | N=6, moves=[2] | Second | 6->4->2->0, First can't escape |
| Smallest losing | N=1, moves=[2,3] | Second | Can't remove 2 or 3 from 1 stone |
| Immediate win | N=3, moves=[3] | First | Take all 3, opponent has 0 (loses) |
| All moves available | N=5, moves=[1,2,3,4,5] | First | Take all 5 and win |
| Large N, small moves | N=100000, moves=[1] | First | Nim with single pile, first wins |

---

## When to Use This Pattern

### Use This Approach When:
- Two players alternate turns with optimal play
- Game state can be described by a single integer (or small state space)
- Player who cannot move loses (or wins - adjust accordingly)
- Both players have the same available moves (impartial game)

### Don't Use When:
- Game state is too large (consider Sprague-Grundy / Nim values)
- Players have different move sets (partisan games)
- Need to find the actual winning strategy, not just who wins

### Pattern Recognition Checklist:
- [ ] Is this a two-player, perfect information game? -> **Consider game theory DP**
- [ ] Can game state be represented as small integer? -> **Direct W/L DP feasible**
- [ ] Multiple independent games combined? -> **Use XOR of Grundy numbers**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Nim Game (LeetCode 292)](https://leetcode.com/problems/nim-game/) | Simplest game theory pattern |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Divisor Game (LeetCode 1025)](https://leetcode.com/problems/divisor-game/) | Different move rules, same W/L concept |
| [Can I Win (LeetCode 464)](https://leetcode.com/problems/can-i-win/) | Bitmask DP for game state |
| [Stone Game (LeetCode 877)](https://leetcode.com/problems/stone-game/) | Two-ended selection |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Grundy's Game](https://atcoder.jp/contests/dp/tasks/dp_l) | Sprague-Grundy theorem |
| [Cat vs Dog](https://www.spoj.com/problems/CATDOG/) | Advanced game theory |
| [Nim (CSES)](https://cses.fi/problemset/task/1730) | XOR of Grundy numbers |

---

## Key Takeaways

1. **The Core Idea:** Position is Winning if you can move to ANY Losing position; Losing if ALL moves lead to Winning positions
2. **Time Optimization:** DP avoids exponential recursion by building from base cases
3. **Space Trade-off:** O(N) space to store all position states
4. **Pattern:** Classic impartial game theory - foundation for Sprague-Grundy theorem

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why position 0 is a Losing position
- [ ] Draw the W/L diagram for a small example by hand
- [ ] Identify similar game theory problems in contests

---

## Additional Resources

- [AtCoder DP Contest - Problem K](https://atcoder.jp/contests/dp/tasks/dp_k) - Original problem
- [CP-Algorithms: Game Theory](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html) - Sprague-Grundy theorem
- [TopCoder: Algorithm Games](https://www.topcoder.com/thrive/articles/Algorithm%20Games) - Comprehensive game theory tutorial
