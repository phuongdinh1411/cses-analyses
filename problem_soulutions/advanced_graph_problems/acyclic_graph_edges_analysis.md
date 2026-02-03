---
layout: simple
title: "Acyclic Graph Edges - Orient Edges to Form DAG"
permalink: /problem_soulutions/advanced_graph_problems/acyclic_graph_edges_analysis
difficulty: Medium
tags: [graph, dfs, topological-order, dag, edge-orientation]
prerequisites: [graph_basics, dfs_bfs]
---

# Acyclic Graph Edges

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/1756](https://cses.fi/problemset/task/1756) |
| **Difficulty** | Medium |
| **Category** | Graph / DFS |
| **Time Limit** | 1 second |
| **Key Technique** | DFS Ordering / Edge Orientation |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Orient undirected edges to form a Directed Acyclic Graph (DAG)
- [ ] Use DFS discovery times to determine edge directions
- [ ] Understand the relationship between DFS trees and acyclic orientations
- [ ] Apply topological ordering concepts to edge orientation problems

---

## Problem Statement

**Problem:** Given an undirected graph with n nodes and m edges, orient each edge (assign a direction) so that the resulting directed graph is acyclic (a DAG).

**Input:**
- Line 1: Two integers n and m (number of nodes and edges)
- Next m lines: Two integers a and b describing an undirected edge

**Output:**
- m lines: For each edge, output the directed version (a b means edge goes from a to b)

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 x 10^5
- The graph is simple (no self-loops, no multiple edges)

### Example

```
Input:
3 3
1 2
2 3
1 3

Output:
1 2
2 3
1 3
```

**Explanation:** The original undirected triangle is oriented as 1->2, 2->3, 1->3. This forms a DAG since we can topologically sort as [1, 2, 3].

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we decide which direction to assign to each edge?

The key insight is that DFS naturally creates an ordering of nodes. When we perform DFS, we discover nodes in a specific order. If we orient all edges from "earlier discovered" to "later discovered" nodes, we guarantee no cycles.

### Breaking Down the Problem

1. **What are we looking for?** A direction for each edge such that no cycles exist.
2. **What information do we have?** The undirected edges of the graph.
3. **What's the relationship?** DFS discovery order provides a natural topological ordering.

### Why DFS Works

When performing DFS on an undirected graph:
- **Tree edges:** Go from parent to child (earlier to later discovery)
- **Back edges:** Go from descendant to ancestor (later to earlier discovery)

If we orient ALL edges from earlier-discovered to later-discovered node, back edges become forward edges, eliminating cycles.

---

## Solution: DFS-Based Edge Orientation

### Key Insight

> **The Trick:** Orient each edge from the node with smaller DFS discovery time to the node with larger discovery time.

### Algorithm

1. Run DFS on all connected components
2. Record discovery time for each node
3. For each edge (a, b), output it as (a, b) if disc[a] < disc[b], else output (b, a)

### Dry Run Example

Let's trace through with input: n=4, edges=[(1,2), (2,3), (3,1), (3,4)]

```
Graph (undirected):
    1 --- 2
    |     |
    +--3--+
       |
       4

DFS starting from node 1:

Step 1: Visit node 1
  disc[1] = 0
  Stack: [1]

Step 2: Visit neighbor 2 (unvisited)
  disc[2] = 1
  Stack: [1, 2]

Step 3: Visit neighbor 3 from node 2 (unvisited)
  disc[3] = 2
  Stack: [1, 2, 3]

Step 4: Neighbor 1 of node 3 already visited (skip)
        Visit neighbor 4 (unvisited)
  disc[4] = 3
  Stack: [1, 2, 3, 4]

Final discovery times:
  Node:  1  2  3  4
  Disc:  0  1  2  3

Orient edges (smaller disc -> larger disc):
  Edge (1,2): disc[1]=0 < disc[2]=1  =>  1 2
  Edge (2,3): disc[2]=1 < disc[3]=2  =>  2 3
  Edge (3,1): disc[3]=2 > disc[1]=0  =>  1 3  (reversed!)
  Edge (3,4): disc[3]=2 < disc[4]=3  =>  3 4

Result DAG:
    1 --> 2
    |     |
    v     v
    +-->3-+
        |
        v
        4
```

### Visual Diagram

```
UNDIRECTED GRAPH           DFS DISCOVERY         ORIENTED DAG

    1 --- 2                disc[1]=0             1 --> 2
    |     |                disc[2]=1             |     |
    +--3--+                disc[3]=2             v     v
       |                   disc[4]=3             +-->3<+
       4                                             |
                                                     v
                                                     4

Rule: For edge (u,v), orient u->v if disc[u] < disc[v]
```

### Code

**Python Solution:**

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    m = int(input_data[idx]); idx += 1

    # Build adjacency list
    adj = defaultdict(list)
    edges = []
    for _ in range(m):
        a = int(input_data[idx]); idx += 1
        b = int(input_data[idx]); idx += 1
        adj[a].append(b)
        adj[b].append(a)
        edges.append((a, b))

    # DFS to compute discovery times
    disc = [0] * (n + 1)
    visited = [False] * (n + 1)
    time = [0]  # Use list to allow modification in nested function

    def dfs(u):
        visited[u] = True
        disc[u] = time[0]
        time[0] += 1
        for v in adj[u]:
            if not visited[v]:
                dfs(v)

    # Run DFS on all components
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)

    # Orient edges based on discovery time
    result = []
    for a, b in edges:
        if disc[a] < disc[b]:
            result.append(f"{a} {b}")
        else:
            result.append(f"{b} {a}")

    print('\n'.join(result))

solve()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> adj[MAXN];
int disc[MAXN];
bool visited[MAXN];
int timer = 0;

void dfs(int u) {
    visited[u] = true;
    disc[u] = timer++;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(v);
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    cin >> n >> m;

    vector<pair<int,int>> edges(m);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
        edges[i] = {a, b};
    }

    // Run DFS on all components
    for (int i = 1; i <= n; i++) {
        if (!visited[i]) {
            dfs(i);
        }
    }

    // Orient edges based on discovery time
    for (auto& [a, b] : edges) {
        if (disc[a] < disc[b]) {
            cout << a << " " << b << "\n";
        } else {
            cout << b << " " << a << "\n";
        }
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | Single DFS traversal + linear edge processing |
| Space | O(n + m) | Adjacency list + discovery time array |

---

## Common Mistakes

### Mistake 1: Not Handling Disconnected Components

```python
# WRONG - Only runs DFS from node 1
dfs(1)

# CORRECT - Run DFS from all unvisited nodes
for i in range(1, n + 1):
    if not visited[i]:
        dfs(i)
```

**Problem:** Graph may have multiple connected components.
**Fix:** Start DFS from every unvisited node.

### Mistake 2: Using BFS Instead of DFS

```python
# WRONG - BFS doesn't guarantee proper back edge handling
# Can still work, but DFS is the standard approach

# CORRECT - Use DFS for cleaner discovery time ordering
def dfs(u):
    visited[u] = True
    disc[u] = time[0]
    time[0] += 1
    for v in adj[u]:
        if not visited[v]:
            dfs(v)
```

**Problem:** BFS also works but DFS is more intuitive for this problem.
**Note:** Both BFS and DFS work because any traversal order gives valid orientation.

### Mistake 3: Recursion Limit (Python)

```python
# WRONG - Default recursion limit is ~1000
def dfs(u):
    # May cause RecursionError for large graphs
    ...

# CORRECT - Increase recursion limit
import sys
sys.setrecursionlimit(300000)
```

**Problem:** Python's default recursion limit causes crashes on large inputs.
**Fix:** Increase limit or use iterative DFS.

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| Single node | n=1, m=0 | Empty output | No edges to orient |
| Two nodes, one edge | n=2, m=1 (1-2) | "1 2" or "2 1" | Either direction works |
| Linear chain | 1-2-3-4 | All edges point same direction | Natural ordering |
| Disconnected components | Two separate triangles | Each component oriented independently | DFS handles separately |
| Star graph | 1 connected to 2,3,4,5 | All edges from 1 outward (or inward) | Depends on DFS start |

---

## When to Use This Pattern

### Use DFS Ordering When:
- You need to orient edges to form a DAG
- You need to find a topological-like ordering on undirected graphs
- You're working with tree/back edge classification

### Don't Use When:
- Graph is already directed (different problem)
- You need a specific topological order (use directed graph algorithms)
- You need to minimize/maximize something about the orientation

### Pattern Recognition Checklist:
- [ ] Undirected graph that needs direction assignment? -> **DFS discovery times**
- [ ] Need acyclic orientation? -> **Earlier-to-later discovery ordering**
- [ ] Multiple components? -> **Run DFS from all unvisited nodes**

---

## Why This Works: Proof Sketch

**Claim:** Orienting edges from lower to higher discovery time creates a DAG.

**Proof:**
1. In DFS, a cycle would require a "back edge" from a node to its ancestor
2. An ancestor always has a smaller discovery time than its descendants
3. By orienting edges from smaller to larger discovery time, the "back edge" direction is reversed
4. The reversed edge goes from ancestor to descendant (same as tree edges)
5. All edges now point "forward" in DFS order, making cycles impossible

---

## Related Problems

### Easier (Do These First)
| Problem | Link | Why It Helps |
|---------|------|--------------|
| Course Schedule (detect cycle) | [CSES 1679](https://cses.fi/problemset/task/1679) | Basic cycle detection |
| Building Roads | [CSES 1666](https://cses.fi/problemset/task/1666) | Connected components |

### Similar Difficulty
| Problem | Link | Key Difference |
|---------|------|----------------|
| Round Trip | [CSES 1669](https://cses.fi/problemset/task/1669) | Find a cycle instead of avoiding |
| Course Schedule II | [CSES 1757](https://cses.fi/problemset/task/1757) | Topological sort on directed graph |

### Harder (Do These After)
| Problem | Link | New Concept |
|---------|------|-------------|
| Game Routes | [CSES 1681](https://cses.fi/problemset/task/1681) | DP on DAG |
| Longest Flight Route | [CSES 1680](https://cses.fi/problemset/task/1680) | Path finding on DAG |

---

## Key Takeaways

1. **The Core Idea:** DFS discovery times provide a natural ordering that guarantees acyclicity when used for edge orientation.

2. **Time Optimization:** Single O(n+m) DFS traversal is optimal - no need for complex algorithms.

3. **Space Trade-off:** O(n) extra space for discovery times, but no expensive data structures needed.

4. **Pattern:** This is a fundamental "DFS tree property" problem - understanding tree edges vs back edges.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why DFS discovery ordering creates a DAG
- [ ] Handle disconnected graph components
- [ ] Implement both iteratively and recursively
- [ ] Solve in under 10 minutes without looking at solution

---

## Implementation Summary

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| DFS Discovery Time | O(n+m) | O(n+m) | Optimal, simple to implement |
| BFS Level Order | O(n+m) | O(n+m) | Also works, less intuitive |

The DFS-based solution is the standard approach for this problem class.
