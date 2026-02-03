---
layout: simple
title: "Strongly Connected Edges - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/strongly_connected_edges_analysis
difficulty: Hard
tags: [graph, dfs, bridges, edge-orientation, strongly-connected]
prerequisites: [graph-dfs, bridge-finding]
---

# Strongly Connected Edges

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/2177](https://cses.fi/problemset/task/2177) |
| **Difficulty** | Hard |
| **Category** | Graph Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Bridge Finding + DFS Edge Orientation |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Find bridges in an undirected graph using Tarjan's algorithm
- [ ] Understand when an undirected graph can be oriented to be strongly connected
- [ ] Orient edges using DFS tree traversal (tree edges down, back edges up)
- [ ] Apply low-link values to detect bridges

---

## Problem Statement

**Problem:** Given an undirected graph, orient each edge to create a directed graph that is strongly connected. If impossible, print "IMPOSSIBLE".

**Input:**
- Line 1: Two integers n and m (number of nodes and edges)
- Next m lines: Two integers a and b (undirected edge between a and b)

**Output:**
- If possible: m lines, each with directed edge "a b" meaning edge from a to b
- If impossible: "IMPOSSIBLE"

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 x 10^5
- Graph is connected

### Example

```
Input:
3 3
1 2
1 3
2 3

Output:
1 2
3 1
2 3
```

**Explanation:** The triangle can be oriented as a cycle: 1->2->3->1. Every node can reach every other node.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When can we orient an undirected graph to make it strongly connected?

The answer lies in **bridges**. A bridge is an edge whose removal disconnects the graph. If we orient a bridge edge, one side can never reach the other.

### Breaking Down the Problem

1. **What are we looking for?** Direction for each edge so all nodes can reach all other nodes.
2. **What makes it impossible?** If there is a bridge, we cannot make it strongly connected.
3. **How do we orient?** Use DFS - tree edges go down (parent to child), back edges go up (descendant to ancestor).

### The Key Insight

```
A graph can be oriented to be strongly connected
       if and only if
    it has NO BRIDGES (is 2-edge-connected)
```

### Why DFS Orientation Works

When we run DFS on a graph with no bridges:
- **Tree edges**: Orient from parent to child (going down)
- **Back edges**: Orient from descendant to ancestor (going up)

This creates cycles because every tree edge is "covered" by some back edge (no bridges means every tree edge has a back edge that bypasses it).

---

## Solution: Bridge Detection + DFS Orientation

### Algorithm Overview

1. Run DFS to find all bridges using low-link values
2. If any bridge exists, output "IMPOSSIBLE"
3. Otherwise, orient edges: tree edges go down, back edges go up

### Understanding Low-Link Values

```
disc[u] = Discovery time of node u
low[u]  = Minimum discovery time reachable from subtree of u
          (using one back edge)

Bridge condition: For edge (u, v) where u is parent of v,
                  if low[v] > disc[u], then (u,v) is a bridge
```

### Visual Example

```
Graph:           DFS Tree:        Oriented:
  1---2            1                1-->2
  |\ /|            |                |   |
  | X |            2                v   v
  |/ \|            |                3<--+
  3---4            3                |   |
                   |                v   v
                   4                4<--+

Back edges: 1-3, 2-3, 2-4, 3-4 (all go UP in DFS tree)
Result: Every node reachable from every other node
```

### Dry Run Example

Let's trace through with the triangle graph (n=3, m=3):

```
Graph: 1-2, 1-3, 2-3

DFS from node 1:
-----------------
Visit 1: disc[1]=0, low[1]=0
  -> Explore edge 1-2 (tree edge)
     Visit 2: disc[2]=1, low[2]=1
       -> Explore edge 2-3 (tree edge)
          Visit 3: disc[3]=2, low[3]=2
            -> Explore edge 3-1 (back edge to ancestor)
               Update: low[3] = min(low[3], disc[1]) = 0
            -> Edge 3-2 is to parent, skip
          Return to 2: low[2] = min(low[2], low[3]) = 0
       -> Edge 2-1 is to parent, skip
     Return to 1: low[1] = min(low[1], low[2]) = 0

Bridge check for each tree edge:
  Edge 1-2: low[2]=0, disc[1]=0, low[2] <= disc[1] -> NOT a bridge
  Edge 2-3: low[3]=0, disc[2]=1, low[3] <= disc[2] -> NOT a bridge

No bridges! Can orient successfully.

Edge orientations:
  1-2: Tree edge, orient as 1->2
  2-3: Tree edge, orient as 2->3
  1-3: Back edge from 3 to 1, orient as 3->1

Result: 1->2, 2->3, 3->1 (forms a cycle!)
```

### Code (Python)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    m = int(input_data[idx]); idx += 1

    # Build adjacency list with edge indices
    adj = defaultdict(list)
    edges = []
    for i in range(m):
        a = int(input_data[idx]); idx += 1
        b = int(input_data[idx]); idx += 1
        adj[a].append((b, i))
        adj[b].append((a, i))
        edges.append([a, b])

    # DFS arrays
    disc = [0] * (n + 1)
    low = [0] * (n + 1)
    visited = [False] * (n + 1)
    timer = [1]
    has_bridge = [False]

    # Result: direction[i] = True means edge[i] keeps original direction
    direction = [True] * m

    def dfs(u, parent_edge_idx):
        visited[u] = True
        disc[u] = low[u] = timer[0]
        timer[0] += 1

        for v, edge_idx in adj[u]:
            if edge_idx == parent_edge_idx:
                continue

            if visited[v]:
                # Back edge: orient toward ancestor (v has smaller disc)
                low[u] = min(low[u], disc[v])
                if disc[v] < disc[u]:
                    # v is ancestor, orient u -> v
                    if edges[edge_idx][0] == u:
                        direction[edge_idx] = True  # u->v
                    else:
                        direction[edge_idx] = False  # flip to u->v
            else:
                # Tree edge: orient toward child (u -> v)
                if edges[edge_idx][0] == u:
                    direction[edge_idx] = True
                else:
                    direction[edge_idx] = False

                dfs(v, edge_idx)
                low[u] = min(low[u], low[v])

                # Check for bridge
                if low[v] > disc[u]:
                    has_bridge[0] = True

    # Run DFS from node 1
    dfs(1, -1)

    if has_bridge[0]:
        print("IMPOSSIBLE")
        return

    # Output oriented edges
    result = []
    for i in range(m):
        a, b = edges[i]
        if direction[i]:
            result.append(f"{a} {b}")
        else:
            result.append(f"{b} {a}")
    print('\n'.join(result))

solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<pair<int,int>> adj[MAXN];  // {neighbor, edge_index}
pair<int,int> edges[200005];      // original edges
int disc[MAXN], low[MAXN];
bool visited[MAXN];
bool direction[200005];  // true = keep original direction
int timer_val = 1;
bool has_bridge = false;
int n, m;

void dfs(int u, int parent_edge) {
    visited[u] = true;
    disc[u] = low[u] = timer_val++;

    for (auto& [v, edge_idx] : adj[u]) {
        if (edge_idx == parent_edge) continue;

        if (visited[v]) {
            // Back edge
            low[u] = min(low[u], disc[v]);
            if (disc[v] < disc[u]) {
                // v is ancestor, orient u -> v
                direction[edge_idx] = (edges[edge_idx].first == u);
            }
        } else {
            // Tree edge: orient u -> v
            direction[edge_idx] = (edges[edge_idx].first == u);

            dfs(v, edge_idx);
            low[u] = min(low[u], low[v]);

            if (low[v] > disc[u]) {
                has_bridge = true;
            }
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;

    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back({b, i});
        adj[b].push_back({a, i});
        edges[i] = {a, b};
        direction[i] = true;
    }

    dfs(1, -1);

    if (has_bridge) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }

    for (int i = 0; i < m; i++) {
        if (direction[i]) {
            cout << edges[i].first << " " << edges[i].second << "\n";
        } else {
            cout << edges[i].second << " " << edges[i].first << "\n";
        }
    }

    return 0;
}
```

### Complexity Analysis

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | Single DFS traversal |
| Space | O(n + m) | Adjacency list and DFS arrays |

---

## Common Mistakes

### Mistake 1: Not Handling Multi-edges Correctly

```cpp
// WRONG: Using parent node instead of parent edge
void dfs(int u, int parent) {
    for (auto [v, idx] : adj[u]) {
        if (v == parent) continue;  // WRONG for multi-edges!
        // ...
    }
}

// CORRECT: Track parent edge index
void dfs(int u, int parent_edge_idx) {
    for (auto [v, idx] : adj[u]) {
        if (idx == parent_edge_idx) continue;  // Correct!
        // ...
    }
}
```

**Problem:** If there are multiple edges between same nodes, skipping by parent node skips all of them.
**Fix:** Track and skip by edge index, not by node.

### Mistake 2: Wrong Bridge Condition

```cpp
// WRONG
if (low[v] >= disc[u])  // This detects articulation points!

// CORRECT (for bridges)
if (low[v] > disc[u])   // Strictly greater for bridges
```

**Problem:** `>=` detects articulation points, not bridges.
**Fix:** Use strict inequality `>` for bridge detection.

### Mistake 3: Forgetting Back Edge Orientation

```cpp
// WRONG: Only orienting tree edges
if (!visited[v]) {
    direction[edge_idx] = (edges[edge_idx].first == u);
    dfs(v, edge_idx);
}
// Missing back edge orientation!

// CORRECT: Also orient back edges
if (visited[v]) {
    if (disc[v] < disc[u]) {
        direction[edge_idx] = (edges[edge_idx].first == u);
    }
}
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single edge | n=2, edge: 1-2 | IMPOSSIBLE | Single edge is always a bridge |
| Triangle | n=3, edges: triangle | Valid orientation | No bridges, forms cycle |
| Two triangles sharing edge | n=4, 5 edges | Valid orientation | 2-edge-connected |
| Path graph | n=3, edges: 1-2, 2-3 | IMPOSSIBLE | All edges are bridges |
| Complete graph | K_n | Valid orientation | Highly connected |

---

## When to Use This Pattern

### Use This Approach When:
- Need to orient edges to achieve strong connectivity
- Need to detect bridges (critical edges) in undirected graphs
- Working with 2-edge-connectivity problems

### Pattern Recognition Checklist:
- [ ] Given undirected graph, need to direct edges? -> **Consider DFS orientation**
- [ ] Need strong connectivity? -> **Check for bridges first**
- [ ] Bridges = impossible? -> **Use low-link bridge detection**

### Related Concepts:
- **Bridges**: Edges whose removal disconnects graph
- **2-edge-connected**: Graph with no bridges
- **DFS Tree**: Tree edges (going down) vs back edges (going up)

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Building Roads](https://cses.fi/problemset/task/1666) | Basic connectivity |
| [Finding Bridges](https://cp-algorithms.com/graph/bridge-searching.html) | Bridge detection practice |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Critical Connections](https://leetcode.com/problems/critical-connections-in-a-network/) | Only find bridges, no orientation |
| [Flight Routes Check](https://cses.fi/problemset/task/1682) | Check if directed graph is strongly connected |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Planets and Kingdoms](https://cses.fi/problemset/task/1683) | SCC decomposition |
| [Coin Collector](https://cses.fi/problemset/task/1686) | DP on SCC DAG |

---

## Key Takeaways

1. **The Core Idea:** A graph can be oriented to be strongly connected if and only if it has no bridges.

2. **Bridge Detection:** Use low-link values - edge (u,v) is bridge if `low[v] > disc[u]` where u is parent of v.

3. **Orientation Rule:** Tree edges go down (parent to child), back edges go up (descendant to ancestor).

4. **Why It Works:** No bridges means every tree edge has a bypassing back edge, creating cycles that enable bidirectional reachability.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement bridge finding with low-link values
- [ ] Explain why bridges make strong connectivity impossible
- [ ] Orient a graph using DFS tree structure
- [ ] Handle multi-edges correctly using edge indices

---

## Additional Resources

- [CP-Algorithms: Bridge Finding](https://cp-algorithms.com/graph/bridge-searching.html)
- [CP-Algorithms: Strongly Connected Components](https://cp-algorithms.com/graph/strongly-connected-components.html)
- [CSES Strongly Connected Edges](https://cses.fi/problemset/task/2177) - Make graph strongly connected
