---
layout: simple
title: "Hamiltonian Flights - Graph DP Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_hamiltonian_path_queries_analysis
difficulty: Hard
tags: [bitmask-dp, graph, hamiltonian-path, dynamic-programming]
---

# Hamiltonian Flights

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Graph / Bitmask DP |
| **Time Limit** | 1 second |
| **Key Technique** | Bitmask DP |
| **CSES Link** | [Hamiltonian Flights](https://cses.fi/problemset/task/1690) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand Hamiltonian paths and their properties
- [ ] Use bitmasks to represent subsets of vertices
- [ ] Design DP states for path-counting problems
- [ ] Apply state transitions for visiting new vertices
- [ ] Optimize exponential algorithms using memoization

---

## Problem Statement

**Problem:** Count the number of Hamiltonian paths from city 1 to city n in a directed graph. A Hamiltonian path visits every vertex exactly once.

**Input:**
- Line 1: n m (number of cities, number of flights)
- Next m lines: a b (flight from city a to city b)

**Output:**
- Number of Hamiltonian paths from 1 to n, modulo 10^9 + 7

**Constraints:**
- 2 <= n <= 20
- 1 <= m <= n(n-1)
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

**Explanation:** The two Hamiltonian paths from 1 to 4 are:
- Path 1: 1 -> 2 -> 3 -> 4
- Path 2: 1 -> 3 -> 2 -> 4

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count paths that visit every vertex exactly once?

The constraint n <= 20 is a huge hint. When n is small (typically <= 20), we can use **bitmask DP** to track which vertices have been visited. Each subset of vertices can be represented as an integer where bit i indicates whether vertex i is visited.

### Breaking Down the Problem

1. **What are we looking for?** Count of paths visiting all n vertices, starting at 1, ending at n
2. **What information do we need to track?** Which vertices we have visited AND where we currently are
3. **Why bitmask?** With n <= 20, there are 2^20 = ~10^6 possible subsets, which is manageable

### Analogies

Think of this like a traveling salesman who must visit every city exactly once. Instead of minimizing distance, we are counting all possible valid routes from city 1 to city n.

---

## Solution 1: Brute Force (Backtracking)

### Idea

Generate all possible paths starting from vertex 1, tracking visited vertices, and count paths that end at vertex n after visiting all vertices.

### Algorithm

1. Start DFS from vertex 1
2. Track visited vertices in a set
3. If all vertices visited and current vertex is n, increment count
4. Recurse to all unvisited neighbors

### Code

```python
def solve_brute_force(n, adj):
    """
    Brute force backtracking solution.

    Time: O(n! * n) - generates all permutations
    Space: O(n) - recursion stack
    """
    MOD = 10**9 + 7
    count = 0

    def dfs(node, visited):
        nonlocal count
        if len(visited) == n:
            if node == n - 1:  # 0-indexed, so n-1 is the target
                count = (count + 1) % MOD
            return

        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor, visited)
                visited.remove(neighbor)

    visited = {0}  # Start from vertex 0 (1 in 1-indexed)
    dfs(0, visited)
    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n!) | Explores all permutations of vertices |
| Space | O(n) | Recursion depth |

### Why This Works (But Is Slow)

Correctness is guaranteed since we explore all possible orderings. However, factorial time makes it impractical even for n = 15.

---

## Solution 2: Bitmask DP (Optimal)

### Key Insight

> **The Trick:** Use a bitmask to represent the set of visited vertices, and DP to count paths reaching each (mask, vertex) state.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[mask][v]` | Number of paths that visit exactly the vertices in `mask` and end at vertex `v` |

**In plain English:** "How many ways can I arrive at vertex v, having visited exactly the cities represented by the bits in mask?"

### State Transition

```
dp[new_mask][u] += dp[mask][v]
    where new_mask = mask | (1 << u)
    and there is an edge from v to u
    and u is not already in mask
```

**Why?** If we can reach vertex v with visited set `mask`, and there is an edge v -> u where u is unvisited, we can extend the path to u.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[1][0]` | 1 | One way to be at vertex 0 (city 1) with only vertex 0 visited |

### Algorithm

1. Initialize dp[1][0] = 1 (start at vertex 0)
2. Iterate through all masks from 1 to 2^n - 1
3. For each mask and vertex v in mask, extend to unvisited neighbors
4. Answer is dp[(1 << n) - 1][n - 1]

### Dry Run Example

Let's trace with n = 3, edges: 1->2, 1->3, 2->3 (0-indexed: 0->1, 0->2, 1->2):

```
Initial:
  dp[001][0] = 1  (at vertex 0, visited {0})

mask = 001 (binary), v = 0:
  Neighbors of 0: {1, 2}

  Extend to 1: new_mask = 001 | 010 = 011
    dp[011][1] += dp[001][0] = 1

  Extend to 2: new_mask = 001 | 100 = 101
    dp[101][2] += dp[001][0] = 1

mask = 011, v = 1:
  Neighbors of 1: {2}

  Extend to 2: new_mask = 011 | 100 = 111
    dp[111][2] += dp[011][1] = 1

mask = 101, v = 2:
  No unvisited neighbors reachable

Final: dp[111][2] = 1 (one Hamiltonian path: 0 -> 1 -> 2)
```

### Visual Diagram

```
Graph:         Bitmask States:
  1 ──→ 2        001 (only 1 visited)
  │     │          ↓
  ↓     ↓        011 (1,2 visited) → 111 (all visited, at 3) ✓
  └──→ 3         101 (1,3 visited) → no path to 2 then 3

Answer: dp[111][2] = number of Hamiltonian paths ending at n
```

### Code

```python
def solve_optimal(n, m, edges):
    """
    Bitmask DP solution for counting Hamiltonian paths.

    Time: O(2^n * n^2)
    Space: O(2^n * n)
    """
    MOD = 10**9 + 7

    # Build adjacency list (0-indexed)
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a - 1].append(b - 1)  # Convert to 0-indexed

    # dp[mask][v] = number of paths visiting vertices in mask, ending at v
    dp = [[0] * n for _ in range(1 << n)]
    dp[1][0] = 1  # Start at vertex 0

    # Iterate through all subsets
    for mask in range(1, 1 << n):
        for v in range(n):
            if dp[mask][v] == 0:
                continue
            if not (mask & (1 << v)):  # v must be in mask
                continue

            # Extend to unvisited neighbors
            for u in adj[v]:
                if mask & (1 << u):  # Skip if already visited
                    continue
                new_mask = mask | (1 << u)
                dp[new_mask][u] = (dp[new_mask][u] + dp[mask][v]) % MOD

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

    print(solve_optimal(n, m, edges))


if __name__ == "__main__":
    main()
```

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<vector<int>> adj(n);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a - 1].push_back(b - 1);  // 0-indexed
    }

    // dp[mask][v] = number of paths visiting vertices in mask, ending at v
    vector<vector<long long>> dp(1 << n, vector<long long>(n, 0));
    dp[1][0] = 1;  // Start at vertex 0

    for (int mask = 1; mask < (1 << n); mask++) {
        for (int v = 0; v < n; v++) {
            if (dp[mask][v] == 0) continue;
            if (!(mask & (1 << v))) continue;

            for (int u : adj[v]) {
                if (mask & (1 << u)) continue;  // Already visited
                int new_mask = mask | (1 << u);
                dp[new_mask][u] = (dp[new_mask][u] + dp[mask][v]) % MOD;
            }
        }
    }

    int full_mask = (1 << n) - 1;
    cout << dp[full_mask][n - 1] << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n * n^2) | 2^n masks, n vertices per mask, n neighbors max |
| Space | O(2^n * n) | DP table size |

---

## Common Mistakes

### Mistake 1: Wrong Base Case

```python
# WRONG - Starting with empty mask
dp[0][0] = 1

# CORRECT - Vertex 0 is already visited when we start there
dp[1][0] = 1  # mask = 1 means vertex 0 is visited
```

**Problem:** The starting vertex must be marked as visited in the initial mask.

### Mistake 2: Forgetting Modular Arithmetic

```python
# WRONG - Integer overflow for large counts
dp[new_mask][u] += dp[mask][v]

# CORRECT - Always take modulo
dp[new_mask][u] = (dp[new_mask][u] + dp[mask][v]) % MOD
```

**Problem:** Path counts can exceed 10^9, causing overflow or wrong answers.

### Mistake 3: 0-indexing vs 1-indexing

```python
# WRONG - Using 1-indexed vertices with bit operations
dp[1 << 1][1] = 1  # Starts at wrong position

# CORRECT - Convert to 0-indexed
dp[1 << 0][0] = 1  # Vertex 1 becomes index 0
```

**Problem:** Bit operations naturally use 0-indexing; mixing causes off-by-one errors.

### Mistake 4: Not Checking Vertex in Mask

```python
# WRONG - Processing vertices not in mask
for v in range(n):
    for u in adj[v]:
        ...

# CORRECT - Only process if v is actually in the current mask
for v in range(n):
    if not (mask & (1 << v)):
        continue
    for u in adj[v]:
        ...
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum n | n=2, edge 1->2 | 1 | Single direct path |
| No path | n=3, edges 1->2, 2->1 | 0 | Cannot reach vertex 3 |
| Complete graph | n=3, all edges | 2 | 1->2->3 and 1->3->2 (if 3->2 exists) |
| Self-loop | n=2, edges 1->1, 1->2 | 1 | Self-loops don't affect Hamiltonian paths |
| Maximum n | n=20 | Varies | Tests time/space limits |

---

## When to Use This Pattern

### Use Bitmask DP When:
- n <= 20 (or sometimes up to 25 with optimizations)
- You need to track subsets of elements
- Problems involve "visiting all" or "selecting subset"
- State depends on which elements are chosen, not their order

### Don't Use When:
- n > 25 (2^n becomes too large)
- Subset information is not needed
- A greedy or simpler DP works

### Pattern Recognition Checklist:
- [ ] Small n constraint (n <= 20)? --> **Consider bitmask DP**
- [ ] Need to track visited/selected elements? --> **Bitmask representation**
- [ ] Counting paths through all vertices? --> **Hamiltonian path DP**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Counting Bits](https://leetcode.com/problems/counting-bits/) | Practice bit manipulation |
| [Subsets](https://leetcode.com/problems/subsets/) | Understand subset enumeration |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES - Hamiltonian Flights](https://cses.fi/problemset/task/1690) | This problem |
| [CSES - Counting Paths](https://cses.fi/problemset/task/1638) | General path counting without Hamiltonian constraint |
| [TSP with DP](https://cses.fi/problemset/task/1690) | Minimize cost instead of counting |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [CSES - Elevator Rides](https://cses.fi/problemset/task/1653) | Bitmask DP with optimization |
| [LeetCode - Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | BFS + bitmask |
| [CSES - Counting Tilings](https://cses.fi/problemset/task/2181) | Profile DP (advanced bitmask) |

---

## Key Takeaways

1. **The Core Idea:** Use bitmask to represent visited vertices; DP state is (visited_set, current_vertex)
2. **Time Optimization:** From O(n!) backtracking to O(2^n * n^2) bitmask DP
3. **Space Trade-off:** O(2^n * n) space enables polynomial-per-state transitions
4. **Pattern:** Classic bitmask DP for subset-based path problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why bitmask DP works for n <= 20
- [ ] Write the state transition from memory
- [ ] Handle 0-indexing correctly with bit operations
- [ ] Identify Hamiltonian path problems in disguise
- [ ] Implement in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Bitmask DP](https://cp-algorithms.com/dynamic_programming/profile-dynamics.html)
- [CSES Hamiltonian Flights](https://cses.fi/problemset/task/1690) - Count Hamiltonian paths
- [TopCoder: Bitmask Tutorial](https://www.topcoder.com/thrive/articles/A%20bit%20of%20fun:%20fun%20with%20bits)
