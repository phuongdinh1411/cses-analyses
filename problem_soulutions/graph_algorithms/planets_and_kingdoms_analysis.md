---
layout: simple
title: "Planets and Kingdoms"
difficulty: Hard
tags: [graph, scc, kosaraju]
cses_link: https://cses.fi/problemset/task/1683
permalink: /problem_soulutions/graph_algorithms/planets_and_kingdoms_analysis
---

# Planets and Kingdoms

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Assign each planet to a kingdom (SCC) |
| Input | n planets, m one-way teleporters |
| Output | Number of kingdoms + kingdom ID for each planet |
| Constraints | 1 <= n <= 10^5, 1 <= m <= 2*10^5 |
| Core Algorithm | Kosaraju's Algorithm (SCC) |
| Time Complexity | O(n + m) |
| Space Complexity | O(n + m) |

## Learning Goals

After solving this problem, you will understand:
1. **Practical SCC Application**: How SCC theory translates to real problem solving
2. **Component Labeling**: How to assign unique IDs to each component
3. **Output Formatting**: Returning per-node component membership

## Problem Statement

A game has n planets (numbered 1 to n) and m one-way teleporters. You need to divide the planets into kingdoms such that:
- You can travel between any two planets in the same kingdom (using teleporters)
- This is the **definition of a Strongly Connected Component (SCC)**

**Output Format**:
1. First line: k = number of kingdoms
2. Second line: n integers where the i-th integer is the kingdom number of planet i

**Example**:
```
Input:
5 6
1 2
2 3
3 1
1 4
4 5
5 4

Output:
2
1 1 1 2 2
```

**Explanation**: Planets {1,2,3} form one kingdom (they have a cycle 1->2->3->1), and planets {4,5} form another kingdom (cycle 4->5->4). Total: 2 kingdoms.

## Key Insight: Direct SCC Application

This problem is a **direct application** of finding Strongly Connected Components:

```
Kingdom = Strongly Connected Component

Why? A kingdom groups planets where you can travel between ANY two planets.
This is exactly the definition of an SCC in a directed graph.
```

**The Algorithm**:
1. Run Kosaraju's algorithm to find all SCCs
2. During pass 2, assign each node its component number
3. Output: count of components + component ID for each node

## Algorithm: Kosaraju's with Component Labeling

For a detailed explanation of Kosaraju's algorithm, see [Strongly Connected Components Analysis](strongly_connected_components_analysis).

**Key Modification**: We need to track which component each node belongs to.

```
Standard Kosaraju:           This Problem:
- Find all SCCs              - Find all SCCs
- Return list of SCCs        - Return component[i] for each node i
```

### Visual Diagram

```
Original Graph:                  Kingdoms Found:
    1 --> 2                      Kingdom 1: {1, 2, 3}
    ^     |                      Kingdom 2: {4, 5}
    |     v
    3 <---+                      Component Assignment:
    |                            Planet 1 -> Kingdom 1
    v                            Planet 2 -> Kingdom 1
    4 <--> 5                     Planet 3 -> Kingdom 1
                                 Planet 4 -> Kingdom 2
                                 Planet 5 -> Kingdom 2
```

## Dry Run

**Input**: n=5, m=6, Edges: (1,2), (2,3), (3,1), (3,4), (4,5), (5,4)

```
Step 1: Build graphs
Original adj[]:          Reversed adj[]:
1: [2]                   1: [3]
2: [3]                   2: [1]
3: [1, 4]                3: [2]
4: [5]                   4: [3, 5]
5: [4]                   5: [4]

Step 2: First DFS (finish order)
Visit: 1 -> 2 -> 3 -> 4 -> 5
Finish order: [5, 4, 3, 2, 1]

Step 3: Second DFS on reversed graph (reverse finish order)
Process 1: DFS finds {1, 3, 2} -> Kingdom 1
Process 4: DFS finds {4, 5}    -> Kingdom 2

Result: 2 kingdoms, assignments: [1, 1, 1, 2, 2]
```

## Python Implementation

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(200001)

def solve():
    n, m = map(int, input().split())

    # Build adjacency lists (1-indexed)
    adj = defaultdict(list)      # Original graph
    radj = defaultdict(list)     # Reversed graph

    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        radj[b].append(a)

    # Pass 1: DFS on original graph to get finish order
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

    # Pass 2: DFS on reversed graph, assign component IDs
    visited = [False] * (n + 1)
    component = [0] * (n + 1)
    comp_id = 0

    def dfs2(u, cid):
        visited[u] = True
        component[u] = cid
        for v in radj[u]:
            if not visited[v]:
                dfs2(v, cid)

    # Process in reverse finish order
    for u in reversed(order):
        if not visited[u]:
            comp_id += 1
            dfs2(u, comp_id)

    # Output
    print(comp_id)
    print(' '.join(map(str, component[1:])))

solve()
```

## C++ Implementation

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100001;
vector<int> adj[MAXN];    // Original graph
vector<int> radj[MAXN];   // Reversed graph
bool visited[MAXN];
int component[MAXN];
vector<int> order;

void dfs1(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs1(v);
        }
    }
    order.push_back(u);
}

void dfs2(int u, int compId) {
    visited[u] = true;
    component[u] = compId;
    for (int v : radj[u]) {
        if (!visited[v]) {
            dfs2(v, compId);
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    // Build both graphs
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        radj[b].push_back(a);
    }

    // Pass 1: Get finish order
    fill(visited, visited + n + 1, false);
    for (int i = 1; i <= n; i++) {
        if (!visited[i]) {
            dfs1(i);
        }
    }

    // Pass 2: Assign components
    fill(visited, visited + n + 1, false);
    int compId = 0;

    for (int i = n - 1; i >= 0; i--) {
        int u = order[i];
        if (!visited[u]) {
            compId++;
            dfs2(u, compId);
        }
    }

    // Output
    cout << compId << "\n";
    for (int i = 1; i <= n; i++) {
        cout << component[i] << " \n"[i == n];
    }

    return 0;
}
```

## Connection to SCC Problem

| Aspect | SCC Problem | Planets and Kingdoms |
|--------|-------------|---------------------|
| Goal | Find all SCCs | Find all SCCs |
| Output | List of components | Component ID per node |
| Algorithm | Kosaraju/Tarjan | Kosaraju/Tarjan |
| Key Difference | Return component lists | Return `component[i]` array |

**What's Different?**
- SCC problem: Return `[[1,2,3], [4,5]]`
- This problem: Return `k=2` and `[1,1,1,2,2]`

The modification is minimal - just track the component ID during pass 2.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Wrong output order | Output component[1..n], not discovery order |
| Missing reversed graph | Build radj[] separately for pass 2 |
| 0-indexed vs 1-indexed | Allocate size n+1, read planets as 1 to n |
| Recursion limit (Python) | sys.setrecursionlimit(200001) or iterative DFS |
| Component numbering | Start comp_id from 1, not 0 |

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build graphs | O(m) | O(n + m) |
| Pass 1 DFS | O(n + m) | O(n) stack |
| Pass 2 DFS | O(n + m) | O(n) stack |
| **Total** | **O(n + m)** | **O(n + m)** |

## Related Problems

- [CSES: Strongly Connected Components](https://cses.fi/problemset/task/1682) - Find SCCs
- [CSES: Giant Pizza](https://cses.fi/problemset/task/1684) - 2-SAT using SCCs
- [CSES: Coin Collector](https://cses.fi/problemset/task/1686) - DP on SCC DAG
