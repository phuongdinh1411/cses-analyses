---
layout: simple
title: "Hamiltonian Flights - Bitmask DP Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_hamiltonian_circuit_queries_analysis
difficulty: Hard
tags: [bitmask-dp, hamiltonian-path, graph, combinatorics]
prerequisites: [grid_paths, counting_paths]
---

# Hamiltonian Flights

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Bitmask DP / Graph |
| **Time Limit** | 1 second |
| **Key Technique** | Bitmask DP for subset enumeration |
| **CSES Link** | [Hamiltonian Flights](https://cses.fi/problemset/task/1690) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand when to apply Bitmask DP for subset problems
- [ ] Represent visited vertices as a bitmask
- [ ] Define DP states combining bitmask and current position
- [ ] Implement efficient state transitions using bitwise operations
- [ ] Handle counting problems modulo a prime

---

## Problem Statement

**Problem:** Count the number of Hamiltonian paths from city 1 to city n in a directed graph.

A Hamiltonian path visits every vertex exactly once.

**Input:**
- Line 1: n (cities) and m (flights)
- Next m lines: a b (flight from city a to city b)

**Output:**
- Number of Hamiltonian paths from 1 to n, modulo 10^9 + 7

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
3 2
2 4
3 4

Output:
2
```

**Explanation:** Two Hamiltonian paths exist:
- Path 1: 1 -> 2 -> 3 -> 4
- Path 2: 1 -> 3 -> 2 -> 4

Both visit all 4 cities exactly once.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently track which cities have been visited?

When n <= 20, we can represent the set of visited cities as a **bitmask**. Each bit position corresponds to a city: bit i is 1 if city i has been visited.

### Breaking Down the Problem

1. **What are we counting?** Paths visiting all n cities exactly once, starting at 1 and ending at n.
2. **What state do we need?** The set of visited cities AND the current city.
3. **Why bitmask?** With n <= 20, there are at most 2^20 = ~10^6 possible subsets, which is manageable.

### Analogies

Think of this like a delivery driver who must visit all customers exactly once. The bitmask is like a checklist tracking which customers have been served, and we need to count all valid orderings.

---

## Solution 1: Brute Force (DFS)

### Idea

Try all possible orderings of cities using depth-first search with backtracking.

### Algorithm

1. Start DFS from city 1
2. For each unvisited neighbor, mark it visited and recurse
3. If we reach city n with all cities visited, increment count
4. Backtrack by unmarking the city

### Code

```python
def solve_brute_force(n, adj):
    """
    Brute force using DFS backtracking.

    Time: O(n! * n) - factorial paths, n edges each
    Space: O(n) - recursion stack
    """
    MOD = 10**9 + 7
    count = 0

    def dfs(city, visited_count, visited):
        nonlocal count
        if city == n:
            if visited_count == n:
                count = (count + 1) % MOD
            return

        for next_city in adj[city]:
            if not visited[next_city]:
                visited[next_city] = True
                dfs(next_city, visited_count + 1, visited)
                visited[next_city] = False

    visited = [False] * (n + 1)
    visited[1] = True
    dfs(1, 1, visited)
    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n! * n) | At most n! paths, each path has n transitions |
| Space | O(n) | Visited array and recursion stack |

### Why This Works (But Is Slow)

This explores every possible path. For n=20, there could be up to 20! paths - far too many to enumerate.

---

## Solution 2: Optimal Solution (Bitmask DP)

### Key Insight

> **The Trick:** Use a bitmask to represent visited cities, converting the exponential backtracking into polynomial DP.

Instead of exploring paths one by one, we count paths to each (mask, city) state.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[mask][v]` | Number of paths that visit exactly the cities in `mask` and end at city `v` |

**In plain English:** dp[mask][v] counts how many ways we can arrive at city v having visited precisely the cities whose bits are set in mask.

### State Transition

```
dp[new_mask][u] += dp[mask][v]   for each edge v -> u
where new_mask = mask | (1 << u)
```

**Why?** If we have `dp[mask][v]` paths ending at v, and there's an edge v -> u where u is unvisited (bit not set), we can extend all those paths to u.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[1][1]` | 1 | Start at city 1, only city 1 visited |
| All other | 0 | No paths initially |

### Algorithm

1. Initialize dp[1][1] = 1 (city 1 visited, at city 1)
2. Iterate through all masks from 1 to 2^n - 1
3. For each valid (mask, v) state, extend to neighbors
4. Answer is dp[(1 << n) - 1][n] (all visited, at city n)

### Dry Run Example

Let's trace with `n=4, edges: 1->2, 1->3, 2->3, 3->2, 2->4, 3->4`:

```
Initial: dp[0001][1] = 1  (binary 0001 = city 1 visited)

Process mask=0001 (city 1):
  From city 1:
    Edge 1->2: dp[0011][2] += dp[0001][1] = 1
    Edge 1->3: dp[0101][3] += dp[0001][1] = 1

Process mask=0011 (cities 1,2):
  From city 2:
    Edge 2->3: dp[0111][3] += dp[0011][2] = 1
    Edge 2->4: dp[1011][4] += dp[0011][2] = 1

Process mask=0101 (cities 1,3):
  From city 3:
    Edge 3->2: dp[0111][2] += dp[0101][3] = 1
    Edge 3->4: dp[1101][4] += dp[0101][3] = 1

Process mask=0111 (cities 1,2,3):
  From city 2: dp[1111][4] += dp[0111][2] = 1
  From city 3: dp[1111][4] += dp[0111][3] = 1

Final: dp[1111][4] = 2 (all cities visited, at city 4)
```

### Visual Diagram

```
State Space:

  mask=0001   mask=0011   mask=0111   mask=1111
  city 1      city 2      city 3      city 4
    (1) ------> (1) ------> (1) ------> (1)
        \                 /          /
         \-> city 3     \/          /
             (1) ------> (1) ------+
                        city 2      \
                                     -> (2) Total

Bitmask meaning:
  0001 = {1}
  0011 = {1,2}
  0101 = {1,3}
  0111 = {1,2,3}
  1111 = {1,2,3,4}
```

### Code

```python
def solve(n, m, edges):
    """
    Bitmask DP solution for counting Hamiltonian paths.

    Time: O(2^n * n^2)
    Space: O(2^n * n)
    """
    MOD = 10**9 + 7

    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)

    # dp[mask][v] = number of paths visiting cities in mask, ending at v
    dp = [[0] * (n + 1) for _ in range(1 << n)]

    # Base case: start at city 1
    dp[1][1] = 1

    # Process all masks in order
    for mask in range(1, 1 << n):
        for v in range(1, n + 1):
            # Skip if v is not in current mask
            if not (mask & (1 << (v - 1))):
                continue
            if dp[mask][v] == 0:
                continue

            # Try extending to each neighbor
            for u in adj[v]:
                # Skip if u already visited
                if mask & (1 << (u - 1)):
                    continue
                new_mask = mask | (1 << (u - 1))
                dp[new_mask][u] = (dp[new_mask][u] + dp[mask][v]) % MOD

    # Answer: all cities visited, ending at city n
    full_mask = (1 << n) - 1
    return dp[full_mask][n]


# Input handling
def main():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    m = int(input_data[idx]); idx += 1

    edges = []
    for _ in range(m):
        a = int(input_data[idx]); idx += 1
        b = int(input_data[idx]); idx += 1
        edges.append((a, b))

    print(solve(n, m, edges))

if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n * n^2) | 2^n masks, n cities per mask, n edges per city |
| Space | O(2^n * n) | DP table size |

---

## Common Mistakes

### Mistake 1: Wrong Bit Indexing

```python
# WRONG: Using 0-indexed cities with 1-indexed bit positions
if mask & (1 << v):  # If cities are 1-indexed, this is off by one

# CORRECT: Adjust for 1-indexed cities
if mask & (1 << (v - 1)):
```

**Problem:** Mismatch between city numbering and bit positions.
**Fix:** Be consistent. If cities are 1 to n, use bits 0 to n-1.

### Mistake 2: Checking Visited After Adding

```python
# WRONG: Update then check
new_mask = mask | (1 << (u - 1))
if new_mask & (1 << (u - 1)):  # Always true!

# CORRECT: Check before updating
if mask & (1 << (u - 1)):  # Skip if already visited
    continue
new_mask = mask | (1 << (u - 1))
```

### Mistake 3: Forgetting Modular Arithmetic

```python
# WRONG: Overflow for large counts
dp[new_mask][u] += dp[mask][v]

# CORRECT: Apply modulo
dp[new_mask][u] = (dp[new_mask][u] + dp[mask][v]) % MOD
```

### Mistake 4: Wrong Initial State

```python
# WRONG: Empty mask or wrong city
dp[0][1] = 1  # mask=0 means no cities visited

# CORRECT: City 1 visited, at city 1
dp[1][1] = 1  # mask=1 means city 1 is visited
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| n=2, direct path | `2 1`, `1 2` | 1 | Only path is 1->2 |
| n=2, no path | `2 0` | 0 | No edges at all |
| No path to n | `3 2`, `1 2`, `2 1` | 0 | City 3 unreachable |
| Must visit middle | `3 2`, `1 3`, `2 3` | 0 | Cannot visit city 2 |
| Multiple paths | `3 4`, `1 2`, `1 3`, `2 3`, `3 2` | 1 | Only 1->2->3 works |

---

## When to Use This Pattern

### Use Bitmask DP When:
- **Small n (<= 20-25):** Bitmask has 2^n states
- **Subset tracking needed:** Need to know which elements are "used"
- **Order matters:** DP state includes both subset and position
- **Counting or optimization:** Finding count/min/max over all orderings

### Don't Use When:
- **n is large (> 25):** 2^n becomes too big
- **Simple linear DP suffices:** No need for subset tracking
- **Polynomial solution exists:** Always prefer lower complexity

### Pattern Recognition Checklist:
- [ ] n <= 20-25? -> Consider bitmask
- [ ] Need to track visited/used elements? -> Bitmask
- [ ] Asking for paths visiting all vertices? -> Hamiltonian path, use bitmask DP
- [ ] Asking for circuits returning to start? -> Hamiltonian circuit variant

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Grid Paths](https://cses.fi/problemset/task/1638) | Basic DP counting paths |
| [Counting Paths](https://cses.fi/problemset/task/1643) | DP on DAG |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Round Trip](https://cses.fi/problemset/task/1669) | Find any cycle, not count |
| [Round Trip II](https://cses.fi/problemset/task/1678) | Directed graph cycle |
| [Graph Girth](https://cses.fi/problemset/task/1707) | Shortest cycle length |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Elevator Rides](https://cses.fi/problemset/task/1653) | Bitmask DP with optimization |
| [Counting Tilings](https://cses.fi/problemset/task/2181) | Profile DP (bitmask on grid) |
| [General Graph Matching](https://cses.fi/problemset/task/1696) | Bitmask with complex state |

---

## Key Takeaways

1. **The Core Idea:** Represent visited vertices as bits in an integer; DP state = (visited set, current position).
2. **Time Optimization:** From O(n!) backtracking to O(2^n * n^2) DP by memoizing states.
3. **Space Trade-off:** O(2^n * n) space to avoid redundant computation.
4. **Pattern:** Bitmask DP - classic technique for small n with subset requirements.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why bitmask works here but not for n=100
- [ ] Convert between city numbers and bit positions correctly
- [ ] Trace through the DP table for a small example
- [ ] Implement in your preferred language in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Bitmask DP](https://cp-algorithms.com/algebra/all-submasks.html)
- [CP-Algorithms: Hamiltonian Path](https://cp-algorithms.com/graph/hamiltonian-path.html)
- [CSES Hamiltonian Flights](https://cses.fi/problemset/task/1690) - Bitmask DP application
