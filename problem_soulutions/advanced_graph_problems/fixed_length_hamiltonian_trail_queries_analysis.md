---
layout: simple
title: "Hamiltonian Flights - Advanced Graph Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_hamiltonian_trail_queries_analysis
difficulty: Hard
tags: [bitmask-dp, hamiltonian-path, graph-theory, exponential-algorithms]
prerequisites: [dynamic_programming_basics, bitmask_operations]
---

# Hamiltonian Flights

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Graph Theory / Bitmask DP |
| **Time Limit** | 1 second |
| **Key Technique** | Bitmask Dynamic Programming |
| **CSES Link** | [Hamiltonian Flights](https://cses.fi/problemset/task/1690) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand Hamiltonian paths and their NP-complete nature
- [ ] Apply bitmask DP to represent subsets of visited vertices
- [ ] Use exponential-time algorithms optimally for small n
- [ ] Implement efficient state transitions using bit operations
- [ ] Precompute results for fast multi-query answering

---

## Problem Statement

**Problem:** Count the number of Hamiltonian paths from city 1 to city n in a directed graph.

**Input:**
- Line 1: n (cities) and m (flights)
- Next m lines: a b (flight from a to b)

**Output:**
- Number of routes from city 1 to city n visiting all cities exactly once (modulo 10^9 + 7)

**Constraints:**
- 2 <= n <= 20
- 1 <= m <= n^2
- 1 <= a, b <= n

### Example

```
Input:
4 6
1 2
1 3
2 3
2 4
3 2
3 4

Output:
2
```

**Explanation:** Two valid Hamiltonian paths exist:
- Path 1: 1 -> 2 -> 3 -> 4
- Path 2: 1 -> 3 -> 2 -> 4

Both visit all 4 cities exactly once and end at city n.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count paths that visit every vertex exactly once?

This is the Hamiltonian Path problem - an NP-complete problem with no known polynomial solution. However, with n <= 20, we can use **Bitmask DP** with O(2^n * n^2) complexity, which is feasible.

### Breaking Down the Problem

1. **What are we looking for?** Number of paths visiting ALL vertices exactly once
2. **What information do we have?** Directed edges and small n (n <= 20)
3. **What's the key constraint?** Each vertex visited exactly once -> track visited set

### The Bitmask Insight

With n = 20 vertices, we have 2^20 = ~1M possible subsets of visited vertices. We can represent any subset as a binary number (bitmask) where bit i is 1 if vertex i is visited.

```
Example: n = 4, visited = {0, 2, 3}
Bitmask: 1101 (binary) = 13 (decimal)
         ^^^^
         3210  (vertex indices)
```

---

## Solution 1: Brute Force (DFS)

### Idea

Try all possible paths starting from vertex 1, tracking visited vertices, and count those ending at vertex n with all vertices visited.

### Code

```python
def solve_brute_force(n, edges):
    """
    DFS brute force - explores all paths.
    Time: O(n!) - factorial, too slow
    Space: O(n)
    """
    MOD = 10**9 + 7
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a-1].append(b-1)  # 0-indexed

    def dfs(node, visited):
        if len(visited) == n:
            return 1 if node == n - 1 else 0

        count = 0
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                count = (count + dfs(neighbor, visited)) % MOD
                visited.remove(neighbor)
        return count

    return dfs(0, {0})
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n!) | Explores all permutations |
| Space | O(n) | Recursion depth |

**Why it's slow:** With n = 20, n! = 2.4 * 10^18 - completely infeasible.

---

## Solution 2: Bitmask DP (Optimal)

### Key Insight

> **The Trick:** Use a bitmask to represent the set of visited vertices, enabling memoization of subproblems.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[mask][v]` | Number of paths ending at vertex v, having visited exactly the vertices in mask |

**In plain English:** "How many ways can I reach vertex v after visiting exactly the cities represented by mask?"

### State Transition

```
dp[new_mask][u] += dp[mask][v]   for all edges v -> u where u is not in mask
```

**Where:** `new_mask = mask | (1 << u)` (add vertex u to visited set)

**Why?** If we have `dp[mask][v]` ways to reach v with visited set mask, and there's an edge v -> u where u is unvisited, we can extend each path.

### Base Case

| Case | Value | Reason |
|------|-------|--------|
| `dp[1][0]` | 1 | Start at vertex 0 (city 1), only vertex 0 visited |

### Dry Run Example

Input: n = 4, edges = [(1,2), (1,3), (2,3), (2,4), (3,2), (3,4)]

```
Graph (0-indexed): 0->1, 0->2, 1->2, 1->3, 2->1, 2->3

Initial: dp[0001][0] = 1  (at vertex 0, visited {0})

Iteration 1: From dp[0001][0] = 1
  Edge 0->1: dp[0011][1] += 1  (visited {0,1})
  Edge 0->2: dp[0101][2] += 1  (visited {0,2})

Iteration 2: From dp[0011][1] = 1
  Edge 1->2: dp[0111][2] += 1  (visited {0,1,2})
  Edge 1->3: dp[1011][3] += 1  (visited {0,1,3})

From dp[0101][2] = 1
  Edge 2->1: dp[0111][1] += 1  (visited {0,1,2})
  Edge 2->3: dp[1101][3] += 1  (visited {0,2,3})

Iteration 3: From dp[0111][2] = 1
  Edge 2->3: dp[1111][3] += 1  (visited {0,1,2,3})

From dp[0111][1] = 1
  Edge 1->3: dp[1111][3] += 1  (visited {0,1,2,3})

Final: dp[1111][3] = 2  (full mask, ending at vertex 3)

Answer: 2
```

### Visual Diagram

```
Vertices: 0(1) -> 1(2) -> 2(3) -> 3(4)
              \       X       /
               -------+-------

Path 1: 0 -> 1 -> 2 -> 3  (mask progression: 0001 -> 0011 -> 0111 -> 1111)
Path 2: 0 -> 2 -> 1 -> 3  (mask progression: 0001 -> 0101 -> 0111 -> 1111)
```

### Code

```python
def solve_bitmask_dp(n, edges):
    """
    Bitmask DP solution for Hamiltonian path counting.

    Time: O(2^n * n^2) - iterate all masks, all vertices, all edges
    Space: O(2^n * n) - DP table
    """
    MOD = 10**9 + 7

    # Build adjacency list (0-indexed)
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a-1].append(b-1)

    # dp[mask][v] = number of paths ending at v with visited set = mask
    dp = [[0] * n for _ in range(1 << n)]
    dp[1][0] = 1  # Start at vertex 0, mask = 1 (only bit 0 set)

    # Process all masks in increasing order of popcount
    for mask in range(1, 1 << n):
        for v in range(n):
            if dp[mask][v] == 0:
                continue
            if not (mask & (1 << v)):  # v must be in mask
                continue

            # Try extending to each neighbor
            for u in graph[v]:
                if mask & (1 << u):  # u already visited
                    continue
                new_mask = mask | (1 << u)
                dp[new_mask][u] = (dp[new_mask][u] + dp[mask][v]) % MOD

    # Answer: paths ending at vertex n-1 with all vertices visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n-1]


# Read input and solve
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    print(solve_bitmask_dp(n, edges))

if __name__ == "__main__":
    main()
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n * n * m) | 2^n masks, n vertices, up to m edges per vertex |
| Space | O(2^n * n) | DP table with 2^n masks and n endpoints |

For n = 20: 2^20 * 20 = ~20 million operations - feasible!

---

## Common Mistakes

### Mistake 1: Forgetting to Check Start/End Vertices

```python
# WRONG - doesn't ensure path starts at vertex 0
dp[1 << start][start] = 1 for all start

# CORRECT - path must start at vertex 0
dp[1][0] = 1  # Only vertex 0 as starting point
```

**Problem:** Problem requires starting from city 1 (vertex 0)
**Fix:** Initialize only `dp[1][0] = 1`

### Mistake 2: Wrong Mask Check

```python
# WRONG - checking if v is in mask incorrectly
if mask & v:  # This checks if ANY bits overlap

# CORRECT - check specific bit
if mask & (1 << v):  # Check if bit v is set
```

**Problem:** `mask & v` doesn't check if vertex v is visited
**Fix:** Use `mask & (1 << v)` to check bit at position v

**Problem:** Sum can overflow 32-bit integers
**Fix:** Use `long long` for DP array and apply modulo after each addition

### Mistake 4: 1-indexed vs 0-indexed Confusion

```python
# WRONG - mixing indices
graph[a].append(b)  # If a,b are 1-indexed from input
dp[1][1] = 1        # Wrong starting position

# CORRECT - convert to 0-indexed
graph[a-1].append(b-1)
dp[1][0] = 1  # Vertex 0 = City 1
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Minimum graph | n=2, edges=[(1,2)] | 1 | Single path 1->2 |
| No path | n=3, edges=[(1,2),(1,3)] | 0 | Can't visit all and end at 3 |
| Complete graph | n=3, all edges | 2 | 1->2->3 and 1->3->2 (if valid end) |
| Self loops | edge (1,1) | Ignore | Self loops don't help |
| Large n | n=20 | Compute | Tests algorithm efficiency |

---

## When to Use This Pattern

### Use Bitmask DP When:
- Problem involves visiting/selecting subsets of n elements
- n is small (typically n <= 20-25)
- Need to track "which elements have been used"
- Subproblem structure depends on the SET of elements processed

### Don't Use When:
- n is large (n > 25) - 2^n becomes too big
- Order within subset matters beyond just "what's included"
- Problem has polynomial-time solution

### Pattern Recognition Checklist:
- [ ] Small n (n <= 20)? -> Consider bitmask
- [ ] Need to track visited/used set? -> Bitmask represents this
- [ ] Counting paths visiting all vertices? -> **Classic bitmask DP**
- [ ] TSP-like problem? -> Bitmask DP is the standard approach

---

## Related Problems

### Easier (Do These First)

| Problem | Link | Why It Helps |
|---------|------|--------------|
| Counting Bits | [LeetCode 338](https://leetcode.com/problems/counting-bits/) | Basic bit manipulation |
| Subsets | [LeetCode 78](https://leetcode.com/problems/subsets/) | Bitmask enumeration |

### Similar Difficulty

| Problem | Link | Key Difference |
|---------|------|----------------|
| Grid Paths (CSES) | [CSES 1638](https://cses.fi/problemset/task/1638) | Path counting on grid |
| Counting Paths (CSES) | [CSES 1136](https://cses.fi/problemset/task/1136) | Path counting on tree |
| Round Trip (CSES) | [CSES 1669](https://cses.fi/problemset/task/1669) | Cycle detection |

### Harder (Do These After)

| Problem | Link | New Concept |
|---------|------|-------------|
| Travelling Salesman (CSES) | [CSES 1690](https://cses.fi/problemset/task/1690) | TSP with minimum cost |
| Elevator Rides (CSES) | [CSES 1653](https://cses.fi/problemset/task/1653) | Bitmask + optimization |
| SOS DP Problems | Various | Sum over subsets technique |

---

## Key Takeaways

1. **The Core Idea:** Use bitmask to encode "which vertices visited" as DP state
2. **Time Optimization:** From O(n!) brute force to O(2^n * n^2) with memoization
3. **Space Trade-off:** O(2^n * n) space for exponential speedup
4. **Pattern:** Classic example of exponential-time DP for NP-complete problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why Hamiltonian Path is NP-complete
- [ ] Convert between vertex sets and bitmasks fluently
- [ ] Implement bitmask DP without reference
- [ ] Analyze when 2^n complexity is acceptable
- [ ] Handle 1-indexed to 0-indexed conversion correctly

---

## Additional Resources

- [CP-Algorithms: Bitmask DP](https://cp-algorithms.com/algebra/all-submasks.html)
- [CSES Hamiltonian Flights](https://cses.fi/problemset/task/1690) - Bitmask DP on paths
- [Hamiltonian Path - Wikipedia](https://en.wikipedia.org/wiki/Hamiltonian_path)
