---
layout: simple
title: "Knight Moves Grid - Graph/BFS Problem"
permalink: /problem_soulutions/introductory_problems/knight_moves_grid_analysis
difficulty: Medium
tags: [BFS, graph-traversal, grid, shortest-path]
prerequisites: [basic_bfs, grid_traversal]
---

# Knight Moves Grid

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Graph / BFS |
| **Time Limit** | 1 second |
| **Key Technique** | Breadth-First Search |
| **CSES Link** | [Two Knights](https://cses.fi/problemset/task/1072) (related) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply BFS to find shortest paths on grids
- [ ] Handle non-standard movement patterns (L-shaped knight moves)
- [ ] Recognize when BFS guarantees optimal solutions in unweighted graphs
- [ ] Implement efficient visited tracking for grid problems

---

## Problem Statement

**Problem:** Find the minimum number of moves for a knight to reach a target position on an n x n chessboard from a starting position.

**Input:**
- n: size of the chessboard (n x n)
- start: starting position (row, col)
- target: target position (row, col)

**Output:**
- Minimum number of knight moves needed, or -1 if impossible

**Constraints:**
- 1 <= n <= 1000
- 0 <= row, col < n

### Example

```
Input:
n = 8
start = (0, 0)
target = (7, 7)

Output:
6
```

**Explanation:** The knight moves in an L-shape (2 squares in one direction + 1 square perpendicular). One optimal path:
`(0,0) -> (2,1) -> (4,2) -> (6,3) -> (4,4) -> (6,5) -> (7,7)` = 6 moves.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Why is BFS the right choice here?

In an unweighted graph where each edge has equal cost (1 move), BFS explores nodes level by level, guaranteeing that the first time we reach a node is via the shortest path. The chessboard is essentially a graph where each cell is a node, and knight moves define the edges.

### Breaking Down the Problem

1. **What are we looking for?** Minimum number of moves (shortest path).
2. **What information do we have?** Start position, target position, board size, knight movement rules.
3. **What's the relationship?** Each valid knight move adds 1 to the distance; BFS explores all positions at distance k before distance k+1.

### Analogies

Think of this like a maze where you can only move in L-shapes. BFS is like sending out scouts in waves - first wave checks all positions 1 move away, second wave checks all positions 2 moves away, and so on. The first scout to reach the target found the shortest path.

---

## Solution 1: Brute Force (DFS)

### Idea

Explore all possible paths using recursive DFS and track the minimum moves found.

### Algorithm

1. From current position, try all 8 knight moves
2. Recursively explore each valid move
3. Track visited positions to avoid cycles
4. Return minimum moves across all paths

### Code (Python)

```python
def brute_force_knight(n, start, target):
 """
 Brute force DFS solution - explores all paths.

 Time: O(8^d) where d is the solution depth
 Space: O(n^2) for visited set
 """
 def dfs(row, col, moves, visited):
  if (row, col) == target:
   return moves
  if moves > n * n:  # Pruning: max possible moves
   return float('inf')

  min_moves = float('inf')
  knight_moves = [
   (2, 1), (2, -1), (-2, 1), (-2, -1),
   (1, 2), (1, -2), (-1, 2), (-1, -2)
  ]

  for dr, dc in knight_moves:
   nr, nc = row + dr, col + dc
   if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
    visited.add((nr, nc))
    min_moves = min(min_moves, dfs(nr, nc, moves + 1, visited))
    visited.remove((nr, nc))

  return min_moves

 result = dfs(start[0], start[1], 0, {start})
 return result if result != float('inf') else -1
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(8^d) | Each position branches into up to 8 moves; d = solution depth |
| Space | O(n^2) | Visited set can hold all cells |

### Why This Works (But Is Slow)

DFS explores all possible paths, so it will find the minimum - but it explores many suboptimal paths before finding the shortest one.

---

## Solution 2: Optimal Solution (BFS)

### Key Insight

> **The Trick:** BFS explores all positions at distance k before any position at distance k+1, guaranteeing the first path found to target is shortest.

### Algorithm

1. Initialize queue with start position (distance 0)
2. While queue is not empty:
   - Dequeue current position
   - If target reached, return distance
   - For each valid knight move, if unvisited, enqueue with distance + 1
3. Return -1 if queue empties (target unreachable)

### Dry Run Example

Let's trace through with `n = 5, start = (0,0), target = (2,2)`:

```
Initial state:
  Queue: [(0,0,0)]    <- (row, col, moves)
  Visited: {(0,0)}

Level 0: Process (0,0,0)
  Valid moves from (0,0): (2,1), (1,2)
  Queue: [(2,1,1), (1,2,1)]
  Visited: {(0,0), (2,1), (1,2)}

Level 1: Process (2,1,1)
  Valid moves: (4,2), (4,0), (0,2), (0,0)*, (3,3), (1,3)
  * already visited
  Queue: [(1,2,1), (4,2,2), (4,0,2), (0,2,2), (3,3,2), (1,3,2)]

Level 1: Process (1,2,1)
  Valid moves: (3,3), (3,1), (0,4), (2,0), (0,0)*
  Queue: [..., (3,1,2), (0,4,2), (2,0,2)]

Level 2: Process (4,2,2)
  Valid moves include (2,3), (2,1)*...

Level 2: Process (0,2,2)
  Valid moves: (2,3), (2,1)*, (1,4), (1,0)

Level 2: Process (3,3,2)
  Valid moves: (4,1), (2,1)*, (1,4), (1,2)*...

Level 2: Process (3,1,2)
  Valid moves: (4,3), (2,3), (1,0), (1,2)*...

Level 2: Process (2,0,2)
  Valid moves: (4,1), (0,1), (3,2)...

...continuing BFS...

Eventually reach (2,2) at Level 4
Result: 4 moves
```

### Visual Diagram

```
Knight at (0,0), Target at (2,2) on 5x5 board:

  0   1   2   3   4
+---+---+---+---+---+

| K |   |   |   |   | 0   K = Start (Knight)
+---+---+---+---+---+

|   |   | * |   |   | 1   * = Reachable in 1 move
+---+---+---+---+---+

|   | * | T |   |   | 2   T = Target
+---+---+---+---+---+

|   |   |   |   |   | 3
+---+---+---+---+---+

|   |   |   |   |   | 4

Knight moves in L-shape:
    +---+   +---+
    | 1 |   | 2 |
+---+---+---+---+---+

| 8 |   | K |   | 3 |
+---+---+---+---+---+

| 7 |   |   |   | 4 |
+---+---+---+---+---+
    | 6 |   | 5 |
    +---+   +---+
```

### Code (Python)

```python
from collections import deque

def knight_moves_bfs(n, start, target):
 """
 Optimal BFS solution for shortest knight path.

 Time: O(n^2) - each cell visited at most once
 Space: O(n^2) - queue and visited set
 """
 if start == target:
  return 0

 # Knight move offsets: 8 L-shaped moves
 moves = [(2,1), (2,-1), (-2,1), (-2,-1),
   (1,2), (1,-2), (-1,2), (-1,-2)]

 queue = deque([(start[0], start[1], 0)])
 visited = {start}

 while queue:
  row, col, dist = queue.popleft()

  for dr, dc in moves:
   nr, nc = row + dr, col + dc

   # Check bounds
   if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
    # Check if target reached
    if (nr, nc) == target:
     return dist + 1

    visited.add((nr, nc))
    queue.append((nr, nc, dist + 1))

 return -1  # Target unreachable


# Main function with I/O
def main():
 import sys
 input_data = sys.stdin.read().split()
 idx = 0

 n = int(input_data[idx]); idx += 1
 sr, sc = int(input_data[idx]), int(input_data[idx+1]); idx += 2
 tr, tc = int(input_data[idx]), int(input_data[idx+1]); idx += 2

 print(knight_moves_bfs(n, (sr, sc), (tr, tc)))


if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Each cell visited at most once |
| Space | O(n^2) | Visited array + queue (worst case all cells) |

---

## Common Mistakes

### Mistake 1: Checking Target After Dequeue

```python
# SLOWER - checks target after dequeue
while queue:
 row, col, dist = queue.popleft()
 if (row, col) == target:  # Late check
  return dist
 # ... add neighbors
```

**Problem:** Wastes time by adding target to queue and processing it later.
**Fix:** Check if neighbor is target BEFORE adding to queue:

```python
if (nr, nc) == target:
 return dist + 1  # Return immediately
```

### Mistake 2: Not Marking Visited When Enqueueing

```python
# WRONG - marks visited when dequeuing
while queue:
 row, col, dist = queue.popleft()
 if (row, col) in visited:  # Too late!
  continue
 visited.add((row, col))
```

**Problem:** Same cell can be added to queue multiple times, causing TLE.
**Fix:** Mark visited immediately when adding to queue:

```python
if (nr, nc) not in visited:
 visited.add((nr, nc))  # Mark NOW
 queue.append((nr, nc, dist + 1))
```

### Mistake 3: Wrong Knight Move Offsets

```python
# WRONG - incomplete or wrong moves
moves = [(2,1), (1,2), (-2,-1), (-1,-2)]  # Only 4 moves!

# CORRECT - all 8 L-shaped moves
moves = [(2,1), (2,-1), (-2,1), (-2,-1),
  (1,2), (1,-2), (-1,2), (-1,-2)]
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Same position | start = target | 0 | No moves needed |
| Adjacent (non-reachable) | n=3, (0,0) to (0,1) | varies | Knight can't move 1 square |
| Small board | n=2 | often -1 | Knight can't move within 2x2 |
| Corner to corner | (0,0) to (n-1,n-1) | varies | Tests full board traversal |
| Single cell board | n=1 | 0 or -1 | Start must equal target |

---

## When to Use This Pattern

### Use BFS When:
- Finding shortest path in unweighted graphs
- All edges have equal cost
- Need to explore all nodes at distance k before k+1
- Grid problems with non-standard movement (knight, king, custom)

### Don't Use When:
- Edges have different weights (use Dijkstra's)
- Looking for all paths (use DFS or backtracking)
- Graph is weighted (use Dijkstra's or Bellman-Ford)

### Pattern Recognition Checklist:
- [ ] Shortest path in unweighted graph? -> **BFS**
- [ ] Grid with obstacles? -> **BFS with boundary checks**
- [ ] Non-standard movement pattern? -> **Define move offsets, then BFS**
- [ ] Weighted edges? -> **Dijkstra's instead**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Labyrinth (CSES)](https://cses.fi/problemset/task/1193) | Standard BFS on grid |
| [Shortest Path in Binary Matrix (LC)](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | 8-directional BFS |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Minimum Knight Moves (LC)](https://leetcode.com/problems/minimum-knight-moves/) | Infinite board, bidirectional BFS |
| [Two Knights (CSES)](https://cses.fi/problemset/task/1072) | Counting, not pathfinding |
| [Rotting Oranges (LC)](https://leetcode.com/problems/rotting-oranges/) | Multi-source BFS |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Word Ladder (LC)](https://leetcode.com/problems/word-ladder/) | BFS on implicit graph |
| [Monsters (CSES)](https://cses.fi/problemset/task/1194) | BFS with multiple entities |
| [Sliding Puzzle (LC)](https://leetcode.com/problems/sliding-puzzle/) | State-space BFS |

---

## Key Takeaways

1. **The Core Idea:** BFS guarantees shortest path in unweighted graphs by exploring level-by-level.
2. **Time Optimization:** From O(8^d) DFS to O(n^2) BFS by avoiding redundant path exploration.
3. **Space Trade-off:** O(n^2) space for visited tracking enables massive time savings.
4. **Pattern:** This belongs to the "Grid BFS with Custom Movement" pattern family.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why BFS finds the shortest path
- [ ] Implement knight move offsets correctly (all 8 moves)
- [ ] Handle edge cases (same position, small boards)
- [ ] Implement in both Python and C++ in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: BFS](https://cp-algorithms.com/graph/breadth-first-search.html)
- [Knight's Tour - Wikipedia](https://en.wikipedia.org/wiki/Knight%27s_tour)
- [CSES Labyrinth](https://cses.fi/problemset/task/1193) - BFS on grid
