---
layout: simple
title: "New Flight Routes - Advanced Graph Problem"
permalink: /problem_soulutions/advanced_graph_problems/new_flight_routes_analysis
difficulty: Hard
tags: [SCC, Tarjan, Kosaraju, DAG, graph-connectivity]
---

# New Flight Routes

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/1685](https://cses.fi/problemset/task/1685) |
| **Difficulty** | Hard |
| **Category** | Graph Theory / SCC |
| **Time Limit** | 1 second |
| **Key Technique** | SCC Condensation + Source/Sink Counting |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Find Strongly Connected Components using Kosaraju's or Tarjan's algorithm
- [ ] Build a condensation graph (DAG of SCCs)
- [ ] Identify sources and sinks in a DAG
- [ ] Apply the formula: edges needed = max(sources, sinks) for strong connectivity

---

## Problem Statement

**Problem:** Given a directed graph with n cities and m flight routes, find the minimum number of new flight routes needed to make it possible to travel from any city to any other city.

**Input:**
- Line 1: Two integers n and m (number of cities and flight routes)
- Lines 2 to m+1: Two integers a and b (flight from city a to city b)

**Output:**
- A single integer: the minimum number of new routes needed

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 x 10^5

### Example

```
Input:
4 5
1 2
2 3
3 1
1 4
2 4

Output:
1
```

**Explanation:** Cities 1, 2, 3 form an SCC. City 4 can be reached from this SCC but cannot reach back. Adding one edge 4 -> 1 (or 4 -> 2 or 4 -> 3) makes the entire graph strongly connected.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** What does "travel from any city to any other" mean in graph terms?

The graph must become **strongly connected** - every vertex must be reachable from every other vertex. Instead of thinking about individual nodes, we should think about **Strongly Connected Components (SCCs)**.

### Breaking Down the Problem

1. **What are we looking for?** Minimum edges to make the graph strongly connected.
2. **What information do we have?** Current directed edges between cities.
3. **What's the relationship?** After condensing SCCs into a DAG, we need to connect all components into one cycle.

### The Key Insight

Once we condense SCCs, we get a DAG (Directed Acyclic Graph). To make a DAG strongly connected:
- Every **source** (in-degree = 0) needs an incoming edge
- Every **sink** (out-degree = 0) needs an outgoing edge
- **Answer = max(sources, sinks)** (we can pair them optimally)

```
Original Graph:              Condensation DAG:
  +---> 2 --+                    [SCC1] ---> [SCC2]
  |    /|   |                       |
  1 <-+ |   v                       v
  ^     +-> 4               [SCC3] ---> [SCC4]
  |
  3 <-------+                Sources: SCC1, SCC3 (count = 2)
                             Sinks:   SCC2, SCC4 (count = 2)
                             Answer:  max(2, 2) = 2
```

---

## Solution: SCC Condensation

### Algorithm Overview

1. **Find all SCCs** using Kosaraju's or Tarjan's algorithm
2. **Build condensation graph** - each SCC becomes a single node
3. **Count sources and sinks** in the condensation DAG
4. **Return max(sources, sinks)** (special case: if only 1 SCC, return 0)

### Dry Run Example

Input: n=4, edges: 1->2, 2->3, 3->1, 1->4

```
Step 1: Find SCCs using Kosaraju's Algorithm

  First DFS (fill stack by finish time):
    Start at 1: visit 1 -> 2 -> 3 -> 1(visited) -> 4
    Finish order stack: [4, 3, 2, 1] (top is 1)

  Build reverse graph:
    2->1, 3->2, 1->3, 4->1

  Second DFS (process stack order on reverse graph):
    Pop 1: DFS finds {1, 3, 2} -> SCC_0 = {1, 2, 3}
    Pop 4: DFS finds {4}      -> SCC_1 = {4}

Step 2: Build condensation graph
  Node mapping: 1,2,3 -> SCC_0,  4 -> SCC_1

  Check original edges:
    1->2: same SCC (skip)
    2->3: same SCC (skip)
    3->1: same SCC (skip)
    1->4: SCC_0 -> SCC_1 (add edge)

  Condensation DAG: SCC_0 ---> SCC_1

Step 3: Count sources and sinks
  SCC_0: in-degree=0 (SOURCE), out-degree=1
  SCC_1: in-degree=1, out-degree=0 (SINK)

  Sources = 1, Sinks = 1

Step 4: Answer = max(1, 1) = 1
```

### Visual Diagram

```
Original Graph:                  Condensation:
    +-------+
    v       |                    +-------+     +-------+
   [1] --> [2]                   | SCC_0 | --> | SCC_1 |
    |       |                    | {1,2,3}|    |  {4}  |
    v       v                    +-------+     +-------+
   [4] <-- [3]                    SOURCE         SINK

To make strongly connected: Add edge from SINK back to SOURCE
    SCC_1 --> SCC_0  (e.g., add 4 -> 1)
```

---

## Code Solutions

### Python Solution (Kosaraju's Algorithm)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(200005)

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    m = int(input_data[idx]); idx += 1

    adj = defaultdict(list)
    radj = defaultdict(list)

    for _ in range(m):
        a = int(input_data[idx]); idx += 1
        b = int(input_data[idx]); idx += 1
        adj[a].append(b)
        radj[b].append(a)

    # Step 1: First DFS to get finish order
    visited = [False] * (n + 1)
    order = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(1, n + 1):
        if not visited[i]:
            dfs1(i)

    # Step 2: Second DFS on reverse graph to find SCCs
    visited = [False] * (n + 1)
    comp = [0] * (n + 1)  # comp[node] = SCC id
    num_scc = 0

    def dfs2(u, scc_id):
        visited[u] = True
        comp[u] = scc_id
        for v in radj[u]:
            if not visited[v]:
                dfs2(v, scc_id)

    for u in reversed(order):
        if not visited[u]:
            dfs2(u, num_scc)
            num_scc += 1

    # Special case: already strongly connected
    if num_scc == 1:
        print(0)
        return

    # Step 3: Count in-degree and out-degree in condensation DAG
    in_deg = [0] * num_scc
    out_deg = [0] * num_scc

    for u in range(1, n + 1):
        for v in adj[u]:
            if comp[u] != comp[v]:
                out_deg[comp[u]] += 1
                in_deg[comp[v]] += 1

    # Count sources and sinks (use sets to avoid counting duplicates)
    has_in = [False] * num_scc
    has_out = [False] * num_scc

    for u in range(1, n + 1):
        for v in adj[u]:
            if comp[u] != comp[v]:
                has_out[comp[u]] = True
                has_in[comp[v]] = True

    sources = sum(1 for i in range(num_scc) if not has_in[i])
    sinks = sum(1 for i in range(num_scc) if not has_out[i])

    print(max(sources, sinks))

solve()
```

### C++ Solution (Kosaraju's Algorithm)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> adj[MAXN], radj[MAXN];
bool visited[MAXN];
int comp[MAXN];
vector<int> order;
int n, m;

void dfs1(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs1(v);
    }
    order.push_back(u);
}

void dfs2(int u, int scc_id) {
    visited[u] = true;
    comp[u] = scc_id;
    for (int v : radj[u]) {
        if (!visited[v]) dfs2(v, scc_id);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;

    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        radj[b].push_back(a);
    }

    // First DFS: get finish order
    memset(visited, false, sizeof(visited));
    for (int i = 1; i <= n; i++) {
        if (!visited[i]) dfs1(i);
    }

    // Second DFS: find SCCs on reverse graph
    memset(visited, false, sizeof(visited));
    int num_scc = 0;
    for (int i = n - 1; i >= 0; i--) {
        int u = order[i];
        if (!visited[u]) {
            dfs2(u, num_scc);
            num_scc++;
        }
    }

    // Special case: already strongly connected
    if (num_scc == 1) {
        cout << 0 << "\n";
        return 0;
    }

    // Count sources and sinks in condensation DAG
    vector<bool> has_in(num_scc, false), has_out(num_scc, false);

    for (int u = 1; u <= n; u++) {
        for (int v : adj[u]) {
            if (comp[u] != comp[v]) {
                has_out[comp[u]] = true;
                has_in[comp[v]] = true;
            }
        }
    }

    int sources = 0, sinks = 0;
    for (int i = 0; i < num_scc; i++) {
        if (!has_in[i]) sources++;
        if (!has_out[i]) sinks++;
    }

    cout << max(sources, sinks) << "\n";
    return 0;
}
```

### Complexity Analysis

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | Two DFS passes through the graph |
| Space | O(n + m) | Store graph, reverse graph, and component info |

---

## Common Mistakes

### Mistake 1: Forgetting the Single SCC Case

```cpp
// WRONG: Missing special case
int sources = count(...);
int sinks = count(...);
cout << max(sources, sinks);  // Wrong when num_scc == 1!

// CORRECT: Handle single SCC
if (num_scc == 1) {
    cout << 0 << "\n";
    return 0;
}
cout << max(sources, sinks) << "\n";
```

**Problem:** When the graph is already strongly connected (1 SCC), the formula gives max(0, 0) = 0, but forgetting to check can cause issues with edge cases.

### Mistake 2: Counting Duplicate Edges in Condensation

```cpp
// WRONG: Counting edges instead of just existence
for (int u = 1; u <= n; u++) {
    for (int v : adj[u]) {
        if (comp[u] != comp[v]) {
            in_degree[comp[v]]++;  // May count same edge multiple times!
        }
    }
}

// CORRECT: Use boolean flags
for (int u = 1; u <= n; u++) {
    for (int v : adj[u]) {
        if (comp[u] != comp[v]) {
            has_in[comp[v]] = true;
            has_out[comp[u]] = true;
        }
    }
}
```

### Mistake 3: Wrong Order in Kosaraju's Second DFS

```cpp
// WRONG: Processing in forward order
for (int i = 0; i < n; i++) {
    int u = order[i];  // Should be reversed!
    if (!visited[u]) dfs2(u, num_scc++);
}

// CORRECT: Process in reverse finish order
for (int i = n - 1; i >= 0; i--) {
    int u = order[i];
    if (!visited[u]) dfs2(u, num_scc++);
}
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Already connected | Single SCC | 0 | No edges needed |
| No edges | n nodes, 0 edges | n | Each node is its own SCC, need n-1+1=n edges |
| Linear chain | 1->2->3->...->n | 1 | One sink, one source, add n->1 |
| Two SCCs, connected | SCC1 -> SCC2 | 1 | Add edge from SCC2 back to SCC1 |
| Isolated nodes | n=2, no edges | 2 | 2 sources, 2 sinks, need 2 edges |

---

## When to Use This Pattern

### Use SCC Condensation When:
- Problem involves making a directed graph strongly connected
- Need to analyze reachability between groups of nodes
- Problem reduces to properties of the condensation DAG

### Key Formula to Remember:
> **Edges to make DAG strongly connected = max(sources, sinks)**

This works because:
- Each source needs at least one incoming edge
- Each sink needs at least one outgoing edge
- We can optimally pair sources and sinks with single edges

### Pattern Recognition Checklist:
- [ ] Directed graph + strong connectivity? Consider SCC
- [ ] Multiple components that need connecting? Build condensation DAG
- [ ] Counting sources/sinks? Use in-degree/out-degree analysis

---

## Related Problems

### Prerequisite Problems (Do These First)
| Problem | Link | Why It Helps |
|---------|------|--------------|
| Planets and Kingdoms | [CSES 1683](https://cses.fi/problemset/task/1683) | Basic SCC detection |
| Kosaraju's Algorithm | Practice | Master the two-DFS approach |

### Similar Difficulty
| Problem | Link | Key Difference |
|---------|------|----------------|
| Coin Collector | [CSES 1686](https://cses.fi/problemset/task/1686) | DP on condensation DAG |
| Giant Pizza | [CSES 1684](https://cses.fi/problemset/task/1684) | 2-SAT using SCC |

### Harder Extensions
| Problem | Link | New Concept |
|---------|------|-------------|
| School Dance | [CSES 1696](https://cses.fi/problemset/task/1696) | Bipartite matching |
| Flight Routes Check | [CSES 1682](https://cses.fi/problemset/task/1682) | Check if strongly connected |

---

## Key Takeaways

1. **The Core Idea:** Condense SCCs into a DAG, then count sources and sinks
2. **Time Optimization:** Single O(n+m) pass with Kosaraju's/Tarjan's algorithm
3. **The Formula:** Answer = max(sources, sinks) in the condensation DAG
4. **Pattern:** SCC problems often reduce to DAG problems after condensation

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement Kosaraju's algorithm from scratch
- [ ] Explain why max(sources, sinks) gives the answer
- [ ] Handle the special case of a single SCC
- [ ] Identify SCC problems in contest settings
- [ ] Solve this problem in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Strongly Connected Components](https://cp-algorithms.com/graph/strongly-connected-components.html)
- [Kosaraju's Algorithm Visualization](https://www.cs.usfca.edu/~galles/visualization/ConnectedComponent.html)
- [CSES Graph Section](https://cses.fi/problemset/)
