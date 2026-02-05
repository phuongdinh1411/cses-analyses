---
layout: simple
title: "Longest Path - Graph DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/longest_path_analysis
difficulty: Medium
tags: [dp, dag, graph, topological-sort, memoization]
prerequisites: []
---

# Longest Path

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Graph DP / DAG |
| **Time Limit** | 2 seconds |
| **Key Technique** | DP on DAG with Topological Order |
| **Problem Link** | [AtCoder DP Contest - G](https://atcoder.jp/contests/dp/tasks/dp_g) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how to apply DP on Directed Acyclic Graphs (DAGs)
- [ ] Implement DFS with memoization for graph problems
- [ ] Use topological sorting to determine DP computation order
- [ ] Recognize the optimal substructure in path problems

---

## Problem Statement

**Problem:** Given a directed acyclic graph (DAG) with N vertices and M edges, find the length of the longest directed path. The length of a path is defined as the number of edges in it.

**Input:**
- Line 1: Two integers N and M (number of vertices and edges)
- Lines 2 to M+1: Two integers x_i and y_i representing a directed edge from x_i to y_i

**Output:**
- A single integer: the length of the longest path

**Constraints:**
- 2 <= N <= 10^5
- 1 <= M <= 10^5
- 1 <= x_i < y_i <= N (this guarantees the graph is a DAG)

### Example

```
Input:
4 5
1 2
1 3
2 3
2 4
3 4

Output:
3
```

**Explanation:** The graph has the structure:
```
1 --> 2 --> 3 --> 4
 \         /
  \-> 3 --/
```
The longest path is 1 -> 2 -> 3 -> 4 with 3 edges.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Why can we use DP on this graph?

A DAG has no cycles, which means there is a natural ordering of vertices (topological order). This ordering guarantees that if we process vertices correctly, all dependencies (neighbors) are resolved before we need them. This is the essence of DP on DAGs.

### Breaking Down the Problem

1. **What are we looking for?** The maximum number of edges in any path.
2. **What information do we have?** The graph structure (vertices and directed edges).
3. **What is the relationship?** The longest path from vertex v depends on the longest paths from its neighbors.

### Analogies

Think of this like finding the longest route through a one-way street system where you can only go "forward" (no U-turns allowed). From any intersection, your best route is 1 + the best route from whichever next intersection leads farthest.

---

## Solution 1: DFS with Memoization (Recommended)

### Key Insight

> **The Trick:** Use DFS to explore paths lazily, caching results to avoid recomputation. The DAG property ensures no infinite loops.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[v]` | Length of the longest path **starting from** vertex v |

**In plain English:** For each vertex, we store how far we can travel starting from that vertex.

### State Transition

```
dp[v] = max(1 + dp[u]) for all neighbors u of v
dp[v] = 0 if v has no outgoing edges (sink vertex)
```

**Why?** From vertex v, we can go to any neighbor u. Taking that edge adds 1 to the path length, plus however far we can go from u.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[v]` for sink | 0 | No outgoing edges means path ends here |

### Algorithm

1. Build adjacency list from input edges
2. Initialize dp array with -1 (unvisited marker)
3. For each vertex, run DFS to compute longest path from it
4. Return the maximum value in dp array

### Dry Run Example

Let's trace through with input `N=4, M=5, edges: (1,2), (1,3), (2,3), (2,4), (3,4)`:

```
Graph adjacency list:
  1 -> [2, 3]
  2 -> [3, 4]
  3 -> [4]
  4 -> []

Initial state: dp = [-1, -1, -1, -1, -1] (index 0 unused)

DFS(1):
  |-- DFS(2):
  |     |-- DFS(3):
  |     |     |-- DFS(4):
  |     |     |     No neighbors, dp[4] = 0
  |     |     dp[3] = 1 + dp[4] = 1 + 0 = 1
  |     |-- DFS(4): already computed, dp[4] = 0
  |     dp[2] = max(1 + dp[3], 1 + dp[4]) = max(2, 1) = 2
  |-- DFS(3): already computed, dp[3] = 1
  dp[1] = max(1 + dp[2], 1 + dp[3]) = max(3, 2) = 3

Final: dp = [-1, 3, 2, 1, 0]
Answer: max(dp[1..4]) = 3
```

### Visual Diagram

```
Vertex:    1       2       3       4
           |       |       |       |
           v       v       v       v
dp value:  3       2       1       0

Path:      1 ----> 2 ----> 3 ----> 4
           (longest path, length = 3)
```

### Code (Python)

```python
import sys
from typing import List, Tuple
sys.setrecursionlimit(200005)

def solve(n: int, edges: List[Tuple[int, int]]) -> int:
    """
    Find longest path in DAG using DFS with memoization.

    Time: O(V + E) - each vertex and edge visited once
    Space: O(V + E) - adjacency list and recursion stack
    """
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)

    # dp[v] = longest path starting from v, -1 means unvisited
    dp = [-1] * (n + 1)

    def dfs(v: int) -> int:
        if dp[v] != -1:
            return dp[v]

        # Base case: sink vertex
        if not graph[v]:
            dp[v] = 0
            return 0

        # Recurrence: try all neighbors
        dp[v] = max(1 + dfs(u) for u in graph[v])
        return dp[v]

    # Compute for all vertices, return maximum
    return max(dfs(v) for v in range(1, n + 1))


def main():
    input_data = sys.stdin.read().split()
    idx = 0
    n, m = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2

    edges = []
    for _ in range(m):
        u, v = int(input_data[idx]), int(input_data[idx + 1])
        edges.append((u, v))
        idx += 2

    print(solve(n, edges))


if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(V + E) | Each vertex computed once, each edge traversed once |
| Space | O(V + E) | Adjacency list + dp array + recursion stack |

---

## Solution 2: Topological Sort + Iterative DP

### Key Insight

> **The Trick:** Process vertices in reverse topological order. This ensures that when computing dp[v], all dp[u] values for neighbors u are already computed.

### Algorithm

1. Compute topological order using Kahn's algorithm (BFS with in-degree)
2. Process vertices in **reverse** topological order
3. For each vertex, compute dp using already-computed neighbor values

### Code (Python)

```python
from collections import deque
from typing import List, Tuple

def solve_topological(n: int, edges: List[Tuple[int, int]]) -> int:
    """
    Find longest path using topological sort + DP.

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Kahn's algorithm for topological sort
    queue = deque(v for v in range(1, n + 1) if in_degree[v] == 0)
    topo_order = []

    while queue:
        v = queue.popleft()
        topo_order.append(v)
        for u in graph[v]:
            in_degree[u] -= 1
            if in_degree[u] == 0:
                queue.append(u)

    # DP in reverse topological order
    dp = [0] * (n + 1)
    for v in reversed(topo_order):
        for u in graph[v]:
            dp[v] = max(dp[v], 1 + dp[u])

    return max(dp)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(V + E) | Topological sort + single DP pass |
| Space | O(V + E) | Adjacency list + in-degree array + dp array |

---

## Common Mistakes

### Mistake 1: Forgetting Base Case

```python
# WRONG - infinite recursion for sink vertices
def dfs(v):
    dp[v] = max(1 + dfs(u) for u in graph[v])  # crashes if graph[v] is empty
    return dp[v]

# CORRECT
def dfs(v):
    if not graph[v]:
        dp[v] = 0
        return 0
    dp[v] = max(1 + dfs(u) for u in graph[v])
    return dp[v]
```

**Problem:** Empty max() raises ValueError in Python; undefined behavior in C++.
**Fix:** Handle sink vertices explicitly.

### Mistake 2: Processing Topological Order in Wrong Direction

```python
# WRONG - neighbors not computed yet
for v in topo_order:
    for u in graph[v]:
        dp[v] = max(dp[v], 1 + dp[u])  # dp[u] is still 0!

# CORRECT - reverse order so neighbors are computed first
for v in reversed(topo_order):
    for u in graph[v]:
        dp[v] = max(dp[v], 1 + dp[u])
```

**Problem:** In forward order, dp[u] for neighbors hasn't been computed.
**Fix:** Process in reverse topological order.

### Mistake 3: Recursion Limit in Python

```python
# WRONG - default recursion limit is ~1000
def dfs(v):
    # ... may hit RecursionError for large graphs

# CORRECT - increase limit before running
import sys
sys.setrecursionlimit(200005)
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No edges | N=3, M=0 | 0 | All isolated vertices, no path |
| Single edge | N=2, M=1, (1,2) | 1 | Only one edge to traverse |
| Linear chain | N=4, edges: (1,2),(2,3),(3,4) | 3 | Full path through all vertices |
| Star graph | N=4, edges: (1,2),(1,3),(1,4) | 1 | All paths have length 1 |
| Dense DAG | Complete DAG with all i->j where i<j | N-1 | Longest path visits all vertices |

---

## When to Use This Pattern

### Use This Approach When:
- The graph is a **DAG** (no cycles)
- You need to find **longest/shortest path** in terms of edge count or weight
- The problem has **optimal substructure** (answer at v depends on answers at neighbors)
- You need to **count paths** or compute path-related quantities

### Don't Use When:
- The graph has **cycles** (use BFS/DFS or detect cycle first)
- You need **shortest path with non-negative weights** (use Dijkstra)
- You need **shortest path with negative weights** (use Bellman-Ford)
- The graph is **undirected** and you need longest path (NP-hard in general)

### Pattern Recognition Checklist:
- [ ] Is the graph guaranteed to be a DAG? --> **DP on DAG is applicable**
- [ ] Does the answer at a vertex depend on answers at reachable vertices? --> **Use DFS + memoization**
- [ ] Need to process vertices in dependency order? --> **Topological sort**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [AtCoder DP - A: Frog 1](https://atcoder.jp/contests/dp/tasks/dp_a) | Basic 1D DP warm-up |
| [AtCoder DP - B: Frog 2](https://atcoder.jp/contests/dp/tasks/dp_b) | Variable transitions in DP |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES - Longest Flight Route](https://cses.fi/problemset/task/1680) | Same concept, requires path reconstruction |
| [CSES - Game Routes](https://cses.fi/problemset/task/1681) | Count number of paths instead of max length |
| [AtCoder DP - H: Grid 1](https://atcoder.jp/contests/dp/tasks/dp_h) | DP on implicit DAG (grid) |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [LeetCode - Longest Increasing Path in Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | Implicit DAG on 2D grid |
| [CSES - Shortest Routes I](https://cses.fi/problemset/task/1671) | Shortest path with Dijkstra |
| [LeetCode - Longest Path With Different Adjacent Characters](https://leetcode.com/problems/longest-path-with-different-adjacent-characters/) | Longest path on tree with constraints |

---

## Key Takeaways

1. **The Core Idea:** In a DAG, longest path from v = 1 + max(longest path from neighbors).
2. **Time Optimization:** Memoization prevents recomputing paths from the same vertex.
3. **Space Trade-off:** O(V) dp array enables O(V+E) time instead of exponential.
4. **Pattern:** This is the fundamental "DP on DAG" pattern - applicable whenever you have a DAG with optimal substructure.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why DP works on DAGs but not general graphs
- [ ] Implement both DFS+memoization and topological sort approaches
- [ ] Identify when a problem can be modeled as longest/shortest path on DAG

---

## Additional Resources

- [CP-Algorithms: Topological Sorting](https://cp-algorithms.com/graph/topological-sort.html)
- [CP-Algorithms: Longest Path in DAG](https://cp-algorithms.com/graph/longest_path_in_dag.html)
- [CSES Longest Flight Route](https://cses.fi/problemset/task/1680) - Find longest path in DAG
