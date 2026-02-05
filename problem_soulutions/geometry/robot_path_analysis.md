---
layout: simple
title: "Robot Path - Geometry Problem"
permalink: /problem_soulutions/geometry/robot_path_analysis
difficulty: Easy
tags: [simulation, coordinate-geometry, cycle-detection, hash-set]
prerequisites: []
---

# Robot Path

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Geometry / Simulation |
| **Time Limit** | 1 second |
| **Key Technique** | Coordinate Simulation + Cycle Detection |
| **CSES Link** | [Point Location Test](https://cses.fi/problemset/task/2189) (related) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Simulate movement on a 2D coordinate plane using direction vectors
- [ ] Use a hash set to detect when a position is revisited (cycle detection)
- [ ] Map character commands to coordinate transformations
- [ ] Understand when a robot's path forms a cycle

---

## Problem Statement

**Problem:** A robot starts at the origin (0, 0) on a 2D grid. Given a string of movement commands, determine if the robot ever returns to a previously visited position.

**Input:**
- Line 1: A string of commands where each character is one of: U (up), D (down), L (left), R (right)

**Output:**
- The number of moves before the robot first revisits a position, or the total path length if no cycle occurs

**Constraints:**
- 1 <= |commands| <= 2 * 10^5
- Commands consist only of characters U, D, L, R

### Example

```
Input:
URDL

Output:
4

Explanation:
  Position trace:
  (0,0) -> U -> (0,1) -> R -> (1,1) -> D -> (1,0) -> L -> (0,0)
  Robot returns to (0,0) after 4 moves.
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently detect when the robot revisits a position?

This is a classic **cycle detection** problem disguised as geometry. We track every position the robot visits using a hash set. If we try to add a position that already exists, we have found a cycle.

### Breaking Down the Problem

1. **What are we looking for?** The first time the robot revisits any position.
2. **What information do we have?** Starting position (0,0) and a sequence of moves.
3. **What's the relationship between input and output?** Each move transforms coordinates; we detect when coordinates repeat.

### Direction Mapping

```
Direction   Delta (dx, dy)
---------   --------------
U (Up)      (0, +1)
D (Down)    (0, -1)
L (Left)    (-1, 0)
R (Right)   (+1, 0)
```

---

## Solution 1: Brute Force (Check All Previous Positions)

### Idea

After each move, linearly scan all previous positions to check for a match.

### Algorithm

1. Start at (0, 0), store in a list
2. For each command, compute new position
3. Linear search the list for the new position
4. If found, return current step count

### Code

```python
def robot_path_brute_force(commands: str) -> int:
 """
 Brute force: O(n^2) time checking all previous positions.
 """
 x, y = 0, 0
 visited = [(0, 0)]

 directions = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}

 for i, cmd in enumerate(commands):
  dx, dy = directions[cmd]
  x, y = x + dx, y + dy

  # Linear search for cycle
  if (x, y) in visited:  # O(n) search in list
   return i + 1
  visited.append((x, y))

 return len(commands)  # No cycle found
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | For each of n moves, linear search through up to n positions |
| Space | O(n) | Store all visited positions |

---

## Solution 2: Optimal Solution (Hash Set)

### Key Insight

> **The Trick:** Use a hash set for O(1) position lookup instead of O(n) linear search.

### Algorithm

1. Initialize position (0, 0) and add to hash set
2. For each command:
   - Compute new position using direction mapping
   - Check if position exists in hash set (O(1))
   - If yes, return step count (cycle found)
   - If no, add position to hash set
3. Return total length if no cycle

### Dry Run Example

Let's trace through with input `URDL`:

```
Initial state:
  position = (0, 0)
  visited = {(0, 0)}

Step 1: Command 'U'
  new_position = (0, 0+1) = (0, 1)
  (0, 1) not in visited
  visited = {(0, 0), (0, 1)}

Step 2: Command 'R'
  new_position = (0+1, 1) = (1, 1)
  (1, 1) not in visited
  visited = {(0, 0), (0, 1), (1, 1)}

Step 3: Command 'D'
  new_position = (1, 1-1) = (1, 0)
  (1, 0) not in visited
  visited = {(0, 0), (0, 1), (1, 1), (1, 0)}

Step 4: Command 'L'
  new_position = (1-1, 0) = (0, 0)
  (0, 0) IS in visited!
  Return 4 (cycle detected at step 4)
```

### Visual Diagram

```
    Y
    ^
    |
  1 +   *-------*
    |   |       |
    |   | cycle |
    |   |       |
  0 +   *-------*-----> X
    0       1

Path: (0,0) -> (0,1) -> (1,1) -> (1,0) -> (0,0)
                                          ^
                                     CYCLE DETECTED
```

### Code

**Python Solution:**

```python
def robot_path(commands: str) -> int:
 """
 Optimal solution using hash set for O(1) lookup.

 Time: O(n) - single pass through commands
 Space: O(n) - hash set stores visited positions
 """
 x, y = 0, 0
 visited = {(0, 0)}

 directions = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}

 for i, cmd in enumerate(commands):
  dx, dy = directions[cmd]
  x, y = x + dx, y + dy

  if (x, y) in visited:
   return i + 1  # Cycle found at step i+1
  visited.add((x, y))

 return len(commands)  # No cycle
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass, O(1) hash operations |
| Space | O(n) | Hash set stores up to n+1 positions |

---

## Common Mistakes

### Mistake 1: Forgetting to Include Starting Position

```python
# WRONG - starting position not tracked
visited = set()  # Empty!
for cmd in commands:
 # ...
 if (x, y) in visited:  # Will miss returning to origin
  return steps
```

**Problem:** The robot starts at (0,0). If it returns to origin, we miss the cycle.
**Fix:** Initialize `visited = {(0, 0)}` before processing.

### Mistake 2: Off-by-One in Step Count

```python
# WRONG
for i, cmd in enumerate(commands):
 # process move
 if (x, y) in visited:
  return i  # Should be i + 1
```

**Problem:** Step count should be 1-indexed (after 1st move, 2nd move, etc.).
**Fix:** Return `i + 1` since enumerate starts at 0.

### Mistake 3: Using List Instead of Set

```python
# WRONG - O(n) lookup
visited = [(0, 0)]  # List, not set
if (x, y) in visited:  # Linear search!
```

**Problem:** Checking membership in a list is O(n), making total time O(n^2).
**Fix:** Use `set()` or `unordered_set` for O(1) lookup.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single move, no cycle | `U` | 1 | Robot moves once, no revisit |
| Immediate return | `UD` | 2 | Up then down returns to origin |
| Long path, late cycle | `UUURRRDDDLLL` | 12 | Returns to origin at end |
| No cycle | `UUUU` | 4 | Never revisits any position |
| Zigzag | `RLRL` | 2 | Returns to origin after RL |

---

## When to Use This Pattern

### Use This Approach When:
- Simulating movement on a grid or coordinate plane
- Need to detect cycles or revisited states
- State can be represented as a hashable tuple (x, y)
- Each operation is a deterministic state transition

### Don't Use When:
- State space is continuous (not discrete grid)
- You need the shortest path (use BFS instead)
- State has too many dimensions to hash efficiently

### Pattern Recognition Checklist:
- [ ] Movement commands on a grid? --> **Coordinate simulation**
- [ ] Need to detect revisited position? --> **Hash set for visited states**
- [ ] Commands are U/D/L/R? --> **Direction mapping dictionary**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Walking on a Grid](https://cses.fi/problemset/task/1638) | Basic grid traversal concepts |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Robot Bounded In Circle](https://leetcode.com/problems/robot-bounded-in-circle/) | Cycle detection after repeating commands |
| [Point Location Test](https://cses.fi/problemset/task/2189) | Point and line geometry basics |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Polygon Area](https://cses.fi/problemset/task/2191) | Using coordinates for area calculation |
| [Convex Hull](https://cses.fi/problemset/task/2195) | Advanced coordinate geometry |
| [Line Segment Intersection](https://cses.fi/problemset/task/2190) | Line intersection detection |

---

## Key Takeaways

1. **The Core Idea:** Track all visited positions in a hash set for O(1) cycle detection.
2. **Time Optimization:** Hash set lookup reduces O(n^2) brute force to O(n).
3. **Space Trade-off:** We use O(n) space for the hash set to gain time efficiency.
4. **Pattern:** This is the "visited state tracking" pattern common in simulation problems.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement coordinate simulation with direction mapping
- [ ] Use a hash set to detect cycles efficiently
- [ ] Handle edge cases (immediate cycle, no cycle, return to origin)
- [ ] Explain why hash set gives O(1) lookup vs O(n) for list

---

## Additional Resources

- [CP-Algorithms: Computational Geometry](https://cp-algorithms.com/geometry/basic-geometry.html)
- [CSES Geometry Problems](https://cses.fi/problemset/list/)
