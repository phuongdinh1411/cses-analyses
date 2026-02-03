---
layout: problem
title: "Articulation Points (Cut Vertices)"
difficulty: Medium
tags: [graph, dfs, tarjan, low-link, connectivity, critical-nodes]
cses_link: https://cses.fi/problemset/
---

# Articulation Points (Cut Vertices)

## Problem Overview

| Aspect | Details |
|--------|---------|
| Source | Classic Graph Algorithm |
| Category | Graph Algorithms |
| Difficulty | Medium |
| Key Technique | Tarjan's Algorithm with Low-Link Values |
| Time Complexity | O(V + E) |
| Space Complexity | O(V) |

## Learning Goals

After completing this analysis, you will be able to:

- [ ] Understand what articulation points are and why they matter in network analysis
- [ ] Implement Tarjan's algorithm using DFS discovery times and low-link values
- [ ] Correctly handle the special case for the root node of DFS
- [ ] Identify articulation points in both connected and disconnected graphs
- [ ] Apply this concept to solve network reliability and connectivity problems

---

## Concept Explanation

### What is an Articulation Point?

An **articulation point** (also called a **cut vertex**) is a vertex in an undirected graph whose removal disconnects the graph (or increases the number of connected components).

```
Original Graph:          After removing vertex 2:
    1---2---3                 1     3
        |
        4                         4

Vertex 2 is an articulation point because removing it
disconnects {1} from {3, 4}.
```

### Why Are Articulation Points Important?

- **Network Reliability**: Identify single points of failure in networks
- **Infrastructure Planning**: Find critical routers, servers, or connections
- **Social Network Analysis**: Identify key individuals whose removal fragments communities
- **Circuit Design**: Detect vulnerable components in electrical circuits

---

## Problem Statement

**Problem:** Given an undirected graph with `n` vertices and `m` edges, find all articulation points.

**Input:**
- First line: two integers `n` and `m`
- Next `m` lines: two integers `u` and `v` describing an edge

**Output:**
- All vertices that are articulation points

**Constraints:**
- 1 <= n <= 10^5
- 0 <= m <= 2 * 10^5

### Example

```
Input:
5 5
1 2
2 3
2 4
3 4
4 5

Output:
2 4
```

**Explanation:**
- Removing vertex 2 disconnects vertex 1 from the rest
- Removing vertex 4 disconnects vertex 5 from the rest
- Vertices 1, 3, 5 are not articulation points (removing any leaves the graph connected minus that vertex)

---

## Intuition: Tarjan's Low-Link Concept

### The Core Idea

During DFS traversal, we assign each vertex two values:

1. **Discovery Time (`disc[v]`)**: When vertex `v` was first visited
2. **Low-Link Value (`low[v]`)**: The minimum discovery time reachable from the subtree rooted at `v`

### What Low-Link Tells Us

```
If low[child] >= disc[current]:
    "child" cannot reach any ancestor of "current" without going through "current"
    Therefore, "current" is an articulation point
```

### Visual Intuition

```
DFS Tree:                   Discovery & Low-Link Values:

    1 (root)                disc: [1, 2, 3, 4, 5]
    |                       low:  [1, 2, 2, 2, 5]  (after propagation)
    2
   / \                      At vertex 2:
  3---4                       - Child 4 has low[4] = 2 >= disc[2] = 2
      |                       - But there's a back edge 3-4, so low[3] = low[4] = 2
      5
                            At vertex 4:
Back edge 3-4 allows          - Child 5 has low[5] = 5 >= disc[4] = 4
low values to propagate       - Vertex 4 is an articulation point
upward through the cycle
```

### Two Conditions for Articulation Points

**Condition 1 (Non-root vertex):**
A non-root vertex `u` is an articulation point if it has a child `v` where:
```
low[v] >= disc[u]
```
This means `v` cannot reach any ancestor of `u` without passing through `u`.

**Condition 2 (Root vertex):**
The DFS root is an articulation point if and only if it has **two or more children** in the DFS tree.

---

## Algorithm

### Tarjan's Algorithm Steps

1. Initialize `disc[]` and `low[]` arrays to -1 (unvisited)
2. Maintain a global timer for discovery times
3. For each unvisited vertex, start a DFS
4. During DFS at vertex `u`:
   - Set `disc[u] = low[u] = timer++`
   - For each neighbor `v`:
     - If `v` is unvisited: recurse, then `low[u] = min(low[u], low[v])`
     - If `v` is visited and not parent: `low[u] = min(low[u], disc[v])`
   - Check articulation point conditions

### Pseudocode

```
function findArticulationPoints(graph):
    timer = 0
    disc = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    isArticulation = [false] * n

    function dfs(u):
        children = 0
        disc[u] = low[u] = timer++

        for each neighbor v of u:
            if disc[v] == -1:        # v not visited
                children++
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])

                # Condition 1: non-root with no back edge from subtree
                if parent[u] != -1 and low[v] >= disc[u]:
                    isArticulation[u] = true

            elif v != parent[u]:     # Back edge
                low[u] = min(low[u], disc[v])

        # Condition 2: root with multiple children
        if parent[u] == -1 and children > 1:
            isArticulation[u] = true

    for each vertex u:
        if disc[u] == -1:
            dfs(u)

    return all u where isArticulation[u] is true
```

---

## Dry Run Example

**Graph:**
```
    1---2---3
        |  /|
        | / |
        4---5
```

**Edges:** (1,2), (2,3), (2,4), (3,4), (3,5), (4,5)

### DFS Traversal (starting from vertex 1)

| Step | Current | Action | disc[] | low[] | Notes |
|------|---------|--------|--------|-------|-------|
| 1 | 1 | Visit | [0,-,-,-,-] | [0,-,-,-,-] | Start DFS, timer=1 |
| 2 | 2 | Visit | [0,1,-,-,-] | [0,1,-,-,-] | From 1, timer=2 |
| 3 | 3 | Visit | [0,1,2,-,-] | [0,1,2,-,-] | From 2, timer=3 |
| 4 | 4 | Visit | [0,1,2,3,-] | [0,1,2,3,-] | From 3, timer=4 |
| 5 | 5 | Visit | [0,1,2,3,4] | [0,1,2,3,4] | From 4, timer=5 |
| 6 | 5 | Back edge to 3 | - | [0,1,2,3,2] | low[5]=min(4,disc[3])=2 |
| 7 | 5 | Back edge to 4 | - | [0,1,2,3,2] | low[5]=min(2,disc[4])=2 (no change) |
| 8 | 4 | Return from 5 | - | [0,1,2,2,2] | low[4]=min(3,low[5])=2 |
| 9 | 4 | Back edge to 2 | - | [0,1,2,1,2] | low[4]=min(2,disc[2])=1 |
| 10 | 3 | Return from 4 | - | [0,1,1,1,2] | low[3]=min(2,low[4])=1 |
| 11 | 2 | Return from 3 | - | [0,1,1,1,2] | low[2]=min(1,low[3])=1 |
| 12 | 2 | Check child 4 | - | - | Already visited, skip |
| 13 | 1 | Return from 2 | - | [0,0,1,1,2] | low[1]=min(0,low[2])=0 (no change) |

### Articulation Point Analysis

| Vertex | parent | children | Condition | Result |
|--------|--------|----------|-----------|--------|
| 1 | -1 (root) | 1 | Root needs 2+ children | Not AP |
| 2 | 1 | 2 (3,4 in DFS tree) | low[3]=1 >= disc[2]=1? Yes | **AP** |
| 3 | 2 | 1 (4) | low[4]=1 >= disc[3]=2? No | Not AP |
| 4 | 3 | 1 (5) | low[5]=2 >= disc[4]=3? No | Not AP |
| 5 | 4 | 0 | Leaf node | Not AP |

**Result:** Vertex 2 is the only articulation point.

Wait - let me recheck. In the DFS tree I traced:
- From 2, we visit 3 first (child)
- From 3, we visit 4 (child)
- From 4, we visit 5 (child)
- 4 also connects to 2, but 2 is already visited

Actually with the back edges 4-2, 5-3, 5-4, the low values propagate up allowing nodes below 2 to reach 2's ancestors. But vertex 1 can only be reached through vertex 2.

Checking vertex 2:
- low[child] >= disc[2] for any child?
- For child 3: low[3] = 1, disc[2] = 1, so 1 >= 1 is true

Actually, the result depends on graph structure. In this particular fully connected subgraph {2,3,4,5}, removing vertex 2 would disconnect vertex 1. So **vertex 2 is an articulation point**.

---

## Common Mistakes

### Mistake 1: Wrong Low-Link Update for Back Edges

```python
# WRONG: Using low[v] instead of disc[v] for back edges
if v != parent[u]:
    low[u] = min(low[u], low[v])  # INCORRECT!

# CORRECT: Use disc[v] for back edges (visited non-parent neighbors)
if v != parent[u]:
    low[u] = min(low[u], disc[v])  # CORRECT!
```

**Problem:** Using `low[v]` can propagate incorrect values across back edges that don't represent actual reachability.

### Mistake 2: Forgetting Root Node Special Case

```python
# WRONG: Treating root the same as other nodes
if low[v] >= disc[u]:
    is_articulation[u] = True  # Wrong for root!

# CORRECT: Root is AP only if it has 2+ DFS children
if parent[u] == -1:
    if children > 1:
        is_articulation[u] = True
else:
    if low[v] >= disc[u]:
        is_articulation[u] = True
```

**Problem:** The root always satisfies `low[v] >= disc[u]` for its children, but it's only an AP if removing it creates multiple disconnected subtrees.

### Mistake 3: Counting Parent as Back Edge

```python
# WRONG: Not excluding parent from back edge check
for v in graph[u]:
    if disc[v] != -1:
        low[u] = min(low[u], disc[v])  # Includes parent!

# CORRECT: Explicitly exclude parent
for v in graph[u]:
    if disc[v] != -1 and v != parent[u]:
        low[u] = min(low[u], disc[v])
```

**Problem:** The edge to parent is a tree edge, not a back edge. Including it gives incorrect low values.

### Mistake 4: Handling Multiple Edges (Multigraphs)

```python
# WRONG for multigraphs: Using simple parent check
if v != parent[u]:
    ...

# CORRECT for multigraphs: Track edge index or use edge count
# If there are multiple edges between u and parent,
# one can be a tree edge while others are back edges
```

---

## Edge Cases

| Case | Description | Handling |
|------|-------------|----------|
| Single vertex | n=1, m=0 | No articulation points |
| Single edge | n=2, m=1 | Both vertices are articulation points |
| Complete graph | All vertices connected | No articulation points (except n<=2) |
| Linear chain | 1-2-3-4-5 | All middle vertices are articulation points |
| Star graph | Center connected to all | Only center is articulation point |
| Disconnected graph | Multiple components | Find APs in each component separately |
| Self-loops | Edge (u, u) | Ignore self-loops |
| Multiple edges | Parallel edges u-v | May affect AP status |
| Tree | n vertices, n-1 edges | All non-leaf vertices are APs |

---

## When to Use This Pattern

### Use Articulation Points When:
- Finding single points of failure in networks
- Identifying critical nodes in infrastructure
- Analyzing network reliability and redundancy
- Detecting vulnerabilities in communication systems
- Solving biconnected component problems

### Related Concepts:
- **Bridges (Cut Edges)**: Similar concept for edges instead of vertices
- **Biconnected Components**: Maximal subgraphs with no articulation points
- **2-Edge-Connected Components**: Maximal subgraphs with no bridges

### Pattern Recognition Checklist:
- [ ] Need to find critical/vulnerable nodes? -> **Articulation Points**
- [ ] Need to find critical edges? -> **Bridges**
- [ ] Need maximal 2-connected subgraphs? -> **Biconnected Components**
- [ ] Working with directed graphs? -> **Consider SCCs instead**

---

## Python Solution

```python
import sys
from collections import defaultdict

def find_articulation_points(n, edges):
    """
    Find all articulation points in an undirected graph.

    Time: O(V + E)
    Space: O(V + E) for adjacency list, O(V) for arrays
    """
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Initialize arrays
    disc = [-1] * (n + 1)      # Discovery time
    low = [-1] * (n + 1)       # Low-link value
    parent = [-1] * (n + 1)    # Parent in DFS tree
    is_ap = [False] * (n + 1)  # Is articulation point?
    timer = [0]                # Use list for mutable closure

    def dfs(u):
        children = 0
        disc[u] = low[u] = timer[0]
        timer[0] += 1

        for v in graph[u]:
            if disc[v] == -1:  # Not visited
                children += 1
                parent[v] = u
                dfs(v)

                # Update low-link from child
                low[u] = min(low[u], low[v])

                # Articulation point conditions
                # Condition 1: u is root with 2+ children
                if parent[u] == -1 and children > 1:
                    is_ap[u] = True

                # Condition 2: u is not root and no back edge from v's subtree
                if parent[u] != -1 and low[v] >= disc[u]:
                    is_ap[u] = True

            elif v != parent[u]:  # Back edge (not to parent)
                low[u] = min(low[u], disc[v])

    # Run DFS from each unvisited vertex (handles disconnected graphs)
    for i in range(1, n + 1):
        if disc[i] == -1:
            dfs(i)

    # Collect articulation points
    return [i for i in range(1, n + 1) if is_ap[i]]


def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())

    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))

    result = find_articulation_points(n, edges)

    if result:
        print(len(result))
        print(' '.join(map(str, sorted(result))))
    else:
        print(0)


if __name__ == "__main__":
    sys.setrecursionlimit(200005)
    solve()
```

---

## C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

class ArticulationPointsFinder {
private:
    int n, timer;
    vector<vector<int>> adj;
    vector<int> disc, low, parent;
    vector<bool> isAP;

    void dfs(int u) {
        int children = 0;
        disc[u] = low[u] = timer++;

        for (int v : adj[u]) {
            if (disc[v] == -1) {  // Not visited
                children++;
                parent[v] = u;
                dfs(v);

                // Update low-link from child
                low[u] = min(low[u], low[v]);

                // Condition 1: Root with 2+ children
                if (parent[u] == -1 && children > 1) {
                    isAP[u] = true;
                }

                // Condition 2: Non-root with no back edge from subtree
                if (parent[u] != -1 && low[v] >= disc[u]) {
                    isAP[u] = true;
                }
            }
            else if (v != parent[u]) {  // Back edge
                low[u] = min(low[u], disc[v]);
            }
        }
    }

public:
    ArticulationPointsFinder(int n) : n(n), timer(0) {
        adj.resize(n + 1);
        disc.assign(n + 1, -1);
        low.assign(n + 1, -1);
        parent.assign(n + 1, -1);
        isAP.assign(n + 1, false);
    }

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> findArticulationPoints() {
        // Run DFS from each component
        for (int i = 1; i <= n; i++) {
            if (disc[i] == -1) {
                dfs(i);
            }
        }

        // Collect results
        vector<int> result;
        for (int i = 1; i <= n; i++) {
            if (isAP[i]) {
                result.push_back(i);
            }
        }
        return result;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    ArticulationPointsFinder finder(n);

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        finder.addEdge(u, v);
    }

    vector<int> aps = finder.findArticulationPoints();

    cout << aps.size() << "\n";
    for (int i = 0; i < (int)aps.size(); i++) {
        if (i > 0) cout << " ";
        cout << aps[i];
    }
    if (!aps.empty()) cout << "\n";

    return 0;
}
```

---

## Complexity Analysis

### Time Complexity: O(V + E)

| Operation | Complexity | Reason |
|-----------|------------|--------|
| Building adjacency list | O(E) | Process each edge once |
| DFS traversal | O(V + E) | Visit each vertex and edge once |
| Collecting results | O(V) | Check each vertex |
| **Total** | **O(V + E)** | Linear in graph size |

### Space Complexity: O(V + E)

| Data Structure | Space | Purpose |
|----------------|-------|---------|
| Adjacency list | O(V + E) | Store graph |
| disc[] array | O(V) | Discovery times |
| low[] array | O(V) | Low-link values |
| parent[] array | O(V) | DFS tree parent |
| isAP[] array | O(V) | Result flags |
| Recursion stack | O(V) | DFS call stack |
| **Total** | **O(V + E)** | Dominated by adjacency list |

---

## Related CSES Problems

| Problem | Link | Connection |
|---------|------|------------|
| Building Roads | [CSES 1666](https://cses.fi/problemset/task/1666) | Finding connected components (prerequisite concept) |
| Flight Routes Check | [CSES 1682](https://cses.fi/problemset/task/1682) | Strong connectivity (directed graph variant) |
| Road Reparation | [CSES 1675](https://cses.fi/problemset/task/1675) | MST with connectivity (related infrastructure problem) |
| Road Construction | [CSES 1676](https://cses.fi/problemset/task/1676) | Dynamic connectivity tracking |

### Progression Path

1. **Building Roads** - Understand connected components with Union-Find
2. **Road Construction** - Track components dynamically
3. **Articulation Points** - Find critical vertices (this topic)
4. **Flight Routes Check** - Extend to directed graphs and SCCs

---

## Key Takeaways

1. **Core Concept:** An articulation point is a vertex whose removal disconnects the graph
2. **Algorithm:** Tarjan's algorithm uses DFS with discovery times and low-link values
3. **Two Cases:** Root nodes need 2+ children; non-root nodes need `low[child] >= disc[node]`
4. **Low-Link Meaning:** Minimum discovery time reachable from subtree via back edges
5. **Complexity:** Linear O(V + E) time, making it efficient for large graphs

---

## Practice Checklist

Before moving on, ensure you can:

- [ ] Explain what articulation points are and give real-world examples
- [ ] Trace through Tarjan's algorithm on a small graph by hand
- [ ] Implement the algorithm without looking at the solution
- [ ] Handle edge cases: root nodes, disconnected graphs, trees
- [ ] Explain why the root node requires special handling
- [ ] Extend the concept to find bridges (cut edges)
