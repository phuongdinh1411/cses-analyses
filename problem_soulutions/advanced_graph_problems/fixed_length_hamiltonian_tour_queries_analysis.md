---
layout: simple
title: "Hamiltonian Flights - Advanced Graph Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_hamiltonian_tour_queries_analysis
difficulty: Hard
tags: [bitmask-dp, hamiltonian-path, graph-theory, counting]
prerequisites: [counting_paths, longest_flight_route]
---

# Hamiltonian Flights

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Graph / Bitmask DP |
| **Time Limit** | 1 second |
| **Key Technique** | Bitmask Dynamic Programming |
| **CSES Link** | [Hamiltonian Flights](https://cses.fi/problemset/task/1690) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand when to apply Bitmask DP for path counting
- [ ] Represent visited vertex sets using bitmasks
- [ ] Implement efficient state transitions for Hamiltonian paths
- [ ] Handle modular arithmetic in counting problems

---

## Problem Statement

**Problem:** Count the number of routes from city 1 to city n that visit each city exactly once.

**Input:**
- Line 1: n m (n cities, m flights)
- Next m lines: a b (one-way flight from city a to city b)

**Output:**
- Number of valid routes modulo 10^9 + 7

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

**Explanation:** The two valid Hamiltonian paths from city 1 to city 4 are:
- Path 1: 1 -> 2 -> 3 -> 4
- Path 2: 1 -> 3 -> 2 -> 4

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count paths that visit ALL vertices exactly once?

This is the classic **Hamiltonian Path** counting problem. The constraint `n <= 20` is a strong hint for **Bitmask DP** because 2^20 = ~10^6 is manageable.

### Breaking Down the Problem

1. **What are we counting?** Paths from vertex 1 to vertex n visiting all vertices exactly once
2. **What information do we need to track?** Which vertices have been visited AND current position
3. **Why Bitmask?** We need to track subsets of visited vertices efficiently

### The Key Insight

We can represent the set of visited vertices as a **bitmask**. For n=4:
- `0001` (binary) = {vertex 1} visited
- `1111` (binary) = {all vertices} visited

This allows O(1) set operations:
- Check if vertex i is visited: `mask & (1 << i)`
- Add vertex i to set: `mask | (1 << i)`

---

## Solution 1: Brute Force (DFS)

### Idea

Try all possible paths from vertex 1, backtracking when we revisit a vertex.

### Code

```python
def count_hamiltonian_paths_brute(n, adj):
    """
    Brute force DFS solution.

    Time: O(n! * n) - all permutations
    Space: O(n) - recursion stack
    """
    MOD = 10**9 + 7
    count = 0

    def dfs(curr, visited):
        nonlocal count
        if len(visited) == n:
            if curr == n - 1:  # 0-indexed, so n-1 is city n
                count = (count + 1) % MOD
            return

        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor, visited)
                visited.remove(neighbor)

    visited = {0}  # Start from vertex 0 (city 1)
    dfs(0, visited)
    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n!) | Explores all permutations |
| Space | O(n) | Recursion depth |

### Why This Is Too Slow

For n=20, we'd need to explore up to 20! = 2.4 * 10^18 paths - impossible within time limits.

---

## Solution 2: Bitmask DP (Optimal)

### Key Insight

> **The Trick:** Use bitmask to represent visited vertices and memoize states

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[mask][i]` | Number of paths that have visited exactly the vertices in `mask` and currently end at vertex `i` |

**In plain English:** "How many ways can I reach vertex i having visited exactly the vertices represented by mask?"

### State Transition

```
For each vertex j where:
  - j is NOT in mask (not yet visited)
  - There's an edge from i to j

dp[mask | (1 << j)][j] += dp[mask][i]
```

**Why?** If we're at vertex i with visited set `mask`, and we can go to j, then the new state has j added to the visited set.

### Base Case

| Case | Value | Reason |
|------|-------|--------|
| `dp[1][0]` | 1 | Start at vertex 0 (city 1) with only vertex 0 visited |

### Dry Run Example

Let's trace with n=4, edges: 1->2, 1->3, 2->3, 2->4, 3->2, 3->4

```
Initial: dp[0001][0] = 1 (at vertex 0, visited {0})

Step 1: From dp[0001][0] = 1
  Can go to vertex 1 (edge 0->1): dp[0011][1] += 1
  Can go to vertex 2 (edge 0->2): dp[0101][2] += 1

  State: dp[0011][1] = 1, dp[0101][2] = 1

Step 2: From dp[0011][1] = 1
  Can go to vertex 2 (edge 1->2): dp[0111][2] += 1
  Can go to vertex 3 (edge 1->3): dp[1011][3] += 1

From dp[0101][2] = 1
  Can go to vertex 1 (edge 2->1): dp[0111][1] += 1
  Can go to vertex 3 (edge 2->3): dp[1101][3] += 1

Step 3: Continue transitions...
  dp[0111][2] -> dp[1111][3] += 1  (via edge 2->3)
  dp[0111][1] -> dp[1111][3] += 1  (via edge 1->3)

Final: dp[1111][3] = 2 (mask=all visited, end at vertex 3)
```

### Visual Diagram

```
Vertices: 0, 1, 2, 3 (cities 1, 2, 3, 4)

        1 -----> 2
        |  \   / |
        |   \ /  |
        v    X   v
        3 -----> 4

Bitmask States:
0001 -> 0011 -> 0111 -> 1111
 (1)    (1,2)  (1,2,3)  (all)
     \
      -> 0101 -> 0111 -> 1111
         (1,3)  (1,2,3)  (all)

Answer = dp[1111][3] (all visited, at vertex 3/city 4)
```

### Code

**Python:**
```python
def count_hamiltonian_paths(n, edges):
    """
    Optimal Bitmask DP solution.

    Time: O(2^n * n^2)
    Space: O(2^n * n)
    """
    MOD = 10**9 + 7

    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a - 1].append(b - 1)  # Convert to 0-indexed

    # dp[mask][i] = count of paths with visited set 'mask' ending at vertex i
    dp = [[0] * n for _ in range(1 << n)]

    # Base case: start at vertex 0 with only vertex 0 visited
    dp[1][0] = 1

    # Process all masks in increasing order
    for mask in range(1 << n):
        for i in range(n):
            if dp[mask][i] == 0:
                continue
            if not (mask & (1 << i)):  # Vertex i must be in mask
                continue

            # Try extending to each neighbor
            for j in adj[i]:
                if not (mask & (1 << j)):  # j must not be visited
                    new_mask = mask | (1 << j)
                    dp[new_mask][j] = (dp[new_mask][j] + dp[mask][i]) % MOD

    # Answer: all vertices visited, ending at vertex n-1
    full_mask = (1 << n) - 1
    return dp[full_mask][n - 1]


# Read input and solve
def main():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0
    n, m = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2

    edges = []
    for _ in range(m):
        a, b = int(input_data[idx]), int(input_data[idx + 1])
        edges.append((a, b))
        idx += 2

    print(count_hamiltonian_paths(n, edges))


if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n * n^2) | 2^n masks, n vertices per mask, n neighbors |
| Space | O(2^n * n) | DP table size |

For n=20: 2^20 * 20^2 = ~4 * 10^8 operations (tight but feasible)

---

## Common Mistakes

### Mistake 1: Forgetting 0-indexing

```python
# WRONG - cities are 1-indexed in input
dp[1 << a][a] = 1

# CORRECT - convert to 0-indexed
dp[1 << (a-1)][a-1] = 1
```

**Problem:** Off-by-one errors cause wrong mask calculations.

### Mistake 2: Wrong Base Case

```python
# WRONG - starting with empty mask
dp[0][0] = 1

# CORRECT - vertex 0 is already visited at start
dp[1][0] = 1  # mask = 0001 means vertex 0 is visited
```

**Problem:** The path must START from vertex 1, so it's already in our visited set.

### Mistake 3: Not Checking Vertex in Mask

```python
# WRONG - processing dp[mask][i] even if i not in mask
for i in range(n):
    if dp[mask][i] > 0:
        # process...

# CORRECT - must verify i is in the visited set
for i in range(n):
    if dp[mask][i] > 0 and (mask & (1 << i)):
        # process...
```

### Mistake 4: Modular Arithmetic Overflow

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| n = 2, direct edge | `2 1, 1 2` | 1 | Single direct path |
| n = 2, no edge | `2 0` | 0 | No valid path |
| No path to n | disconnected graph | 0 | Can't reach destination |
| Multiple edges | parallel edges | Sum counts | Each edge is separate route |
| Self-loops | edge a a | 0 | Can't use (vertex already visited) |

---

## When to Use This Pattern

### Use Bitmask DP When:
- Problem involves subsets of elements (n <= 20-25)
- Need to track "which elements have been used"
- Counting paths/permutations with constraints
- State depends on a SET of items, not just count

### Don't Use When:
- n > 25 (2^n becomes too large)
- Only need to track count of used items (use regular DP)
- Problem has polynomial solution

### Pattern Recognition Checklist:
- [ ] Constraint n <= 20? -> **Strong hint for Bitmask DP**
- [ ] Need to track "visited" or "used" items? -> **Use bitmask**
- [ ] Counting permutations/paths? -> **Bitmask DP candidate**
- [ ] Asking for Hamiltonian path/cycle? -> **Classic Bitmask DP**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Counting Paths (CSES)](https://cses.fi/problemset/task/1638) | Basic path counting DP |
| [Grid Paths (CSES)](https://cses.fi/problemset/task/1639) | DP on grids |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Round Trip II (CSES)](https://cses.fi/problemset/task/1678) | Finding one cycle, not counting |
| [Elevator Rides (CSES)](https://cses.fi/problemset/task/1653) | Bitmask DP for optimization |
| [Elevator Rides (CSES)](https://cses.fi/problemset/task/1653) | Sum over subsets technique |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Counting Tilings (CSES)](https://cses.fi/problemset/task/2181) | Profile/broken profile DP |
| [TSP (Traveling Salesman)](https://cses.fi/problemset/task/1690) | Minimum cost variant |

---

## Key Takeaways

1. **The Core Idea:** Use bitmask to represent visited vertices, enabling O(1) set operations
2. **Time Optimization:** From O(n!) brute force to O(2^n * n^2) with memoization
3. **Space Trade-off:** O(2^n * n) space for exponential time improvement
4. **Pattern:** Bitmask DP is the go-to for small n (<=20) subset-based counting

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why n <= 20 suggests Bitmask DP
- [ ] Convert between vertex sets and bitmasks
- [ ] Write the DP transition from scratch
- [ ] Handle 0-indexing vs 1-indexing correctly
- [ ] Apply modular arithmetic properly

---

## Additional Resources

- [CP-Algorithms: Bitmask DP](https://cp-algorithms.com/algebra/profile-dynamics.html)
- [CSES Hamiltonian Flights](https://cses.fi/problemset/task/1690) - Hamiltonian path counting
- [Hamiltonian Path - Wikipedia](https://en.wikipedia.org/wiki/Hamiltonian_path)
