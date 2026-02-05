---
layout: simple
title: "Bridges (Cut Edges) - Graph Algorithm"
permalink: /problem_soulutions/graph_algorithms/bridges_analysis
difficulty: Hard
tags: [graph, dfs, bridges, tarjan, connectivity]
---

# Bridges (Cut Edges) in Graphs

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Graph / DFS |
| **Time Complexity** | O(V + E) |
| **Key Technique** | Tarjan's Algorithm with Low-Link Values |

### Concept Explanation

A **bridge** (or cut edge) is an edge in an undirected graph whose removal **disconnects** the graph (or increases the number of connected components). Bridges represent critical connections - single points of failure in a network.

**Real-world examples:**
- A single road connecting two cities (if destroyed, travel is impossible)
- A critical network link (if it fails, parts of the network become unreachable)
- A supply chain dependency (if removed, distribution breaks)

### Learning Goals

After studying this topic, you will be able to:
- [ ] Understand what makes an edge a bridge in a graph
- [ ] Implement Tarjan's algorithm for finding bridges
- [ ] Use discovery time and low-link values correctly
- [ ] Handle edge cases like multiple edges and self-loops
- [ ] Differentiate between bridges and articulation points

---

## Problem Statement

**Problem:** Given an undirected graph with `n` vertices and `m` edges, find all bridges (edges whose removal disconnects the graph).

**Input:**
- Line 1: `n m` (number of vertices and edges)
- Next `m` lines: `a b` (edge between vertices a and b)

**Output:**
- All bridge edges, one per line

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 * 10^5
- Graph may have multiple components

### Example

```
Input:
7 8
1 2
1 3
2 3
3 4
4 5
5 6
5 7
6 7

Output:
3 4
4 5
```

**Explanation:** Removing edge (3,4) or (4,5) disconnects vertex 4 (and beyond) from the rest. The triangles {1,2,3} and {5,6,7} have no bridges since alternate paths exist.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we determine if removing an edge disconnects the graph without actually removing it?

An edge (u, v) is a bridge if and only if there is **no back edge** from the subtree rooted at v (when DFS traverses from u to v) that connects to u or any ancestor of u. If such a back edge exists, removing (u, v) still leaves an alternate path.

### Tarjan's Algorithm Core Concepts

| Term | Definition |
|------|------------|
| **Discovery Time** (`disc[v]`) | The order in which node v is first visited during DFS |
| **Low-Link Value** (`low[v]`) | The minimum discovery time reachable from the subtree rooted at v |

### The Bridge Condition

```
Edge (u, v) is a bridge if and only if: low[v] > disc[u]
```

**Why?** If `low[v] > disc[u]`, then from v's subtree, we cannot reach u or any ancestor of u through a back edge. Thus, removing (u, v) cuts off v's subtree entirely.

### Visual Understanding

```
         1 (disc=1)
        /|\
       / | \
      2  |  3 (disc=3)
     /   |   \
    /   back   \
   4    edge    5 (disc=5)
  (disc=4)      |
                6 (disc=6)

If node 6 has low[6] = 6 and disc[5] = 5:
  low[6] > disc[5] --> Edge (5,6) is a bridge!

If node 4 has low[4] = 1 (via back edge to 1):
  low[4] < disc[2] --> Edge (2,4) is NOT a bridge
```

---

## Algorithm: Tarjan's Bridge Finding

### Step-by-Step Process

1. **Initialize:** Set `disc[]` and `low[]` to -1 for all vertices
2. **DFS Traversal:** For each unvisited vertex, run DFS
3. **On visiting vertex v:**
   - Set `disc[v] = low[v] = timer++`
4. **For each neighbor u of v:**
   - If u is parent: skip (don't go back on the same edge)
   - If u is visited: `low[v] = min(low[v], disc[u])` (back edge)
   - If u is unvisited: recurse, then `low[v] = min(low[v], low[u])`
5. **After processing child u:** If `low[u] > disc[v]`, edge (v, u) is a bridge

### Dry Run Example

**Graph:**
```
    1---2
    |\ /|
    | 3 |
    |   |
    4---5
```

Edges: (1,2), (1,3), (2,3), (1,4), (4,5), (2,5)

**DFS from vertex 1:**

```
Step 1: Visit 1
  disc[1] = 0, low[1] = 0

Step 2: Visit 2 (from 1)
  disc[2] = 1, low[2] = 1

Step 3: Visit 3 (from 2)
  disc[3] = 2, low[3] = 2
  Back edge to 1: low[3] = min(2, 0) = 0
  Return to 2: low[2] = min(1, 0) = 0
  Check: low[3]=0 > disc[2]=1? NO, (2,3) not a bridge

Step 4: Visit 5 (from 2)
  disc[5] = 3, low[5] = 3

Step 5: Visit 4 (from 5)
  disc[4] = 4, low[4] = 4
  Back edge to 1: low[4] = min(4, 0) = 0
  Return to 5: low[5] = min(3, 0) = 0
  Check: low[4]=0 > disc[5]=3? NO, (5,4) not a bridge

Return to 2: low[2] = min(0, 0) = 0
Check: low[5]=0 > disc[2]=1? NO, (2,5) not a bridge

Return to 1: low[1] = min(0, 0) = 0
Check: low[2]=0 > disc[1]=0? NO, (1,2) not a bridge

Continue from 1 to 4: Already visited
Continue from 1 to 3: Already visited

Final: No bridges found (graph is 2-edge-connected)
```

**Second Example with a Bridge:**

```
Graph: 1---2---3---4
              |   |
              +---+

Edges: (1,2), (2,3), (3,4), (4,3) -- wait, let's use:
       1---2---3---4
                  /|
                 5-+

Edges: (1,2), (2,3), (3,4), (4,5), (3,5)
```

```
DFS from 1:
  disc[1]=0, low[1]=0
  disc[2]=1, low[2]=1
  disc[3]=2, low[3]=2
  disc[4]=3, low[4]=3
  disc[5]=4, low[5]=4
  Back edge 5->3: low[5]=min(4,2)=2
  Return: low[4]=min(3,2)=2
  Check: low[5]=2 > disc[4]=3? NO
  Return: low[3]=min(2,2)=2
  Check: low[4]=2 > disc[3]=2? NO
  Return: low[2]=min(1,2)=1
  Check: low[3]=2 > disc[2]=1? YES! (2,3) is a bridge!
  Return: low[1]=min(0,1)=0
  Check: low[2]=1 > disc[1]=0? YES! (1,2) is a bridge!

Bridges: (1,2), (2,3)
```

---

## Solution: Python Implementation

```python
from collections import defaultdict

def find_bridges(n, edges):
 """
 Find all bridges in an undirected graph using Tarjan's algorithm.

 Time: O(V + E)
 Space: O(V + E)

 Args:
  n: number of vertices (1-indexed)
  edges: list of (u, v) tuples representing edges

 Returns:
  List of bridge edges as (u, v) tuples
 """
 graph = defaultdict(list)
 for u, v in edges:
  graph[u].append(v)
  graph[v].append(u)

 disc = [-1] * (n + 1)      # Discovery time
 low = [-1] * (n + 1)       # Low-link value
 timer = [0]                # Mutable timer for closure
 bridges = []

 def dfs(v, parent):
  disc[v] = low[v] = timer[0]
  timer[0] += 1

  for u in graph[v]:
   if u == parent:
    continue       # Skip the edge we came from

   if disc[u] == -1:  # Tree edge (unvisited)
    dfs(u, v)
    low[v] = min(low[v], low[u])

    # Bridge condition
    if low[u] > disc[v]:
     bridges.append((v, u))
   else:              # Back edge (already visited)
    low[v] = min(low[v], disc[u])

 # Handle disconnected components
 for v in range(1, n + 1):
  if disc[v] == -1:
   dfs(v, -1)

 return bridges


# Example usage
if __name__ == "__main__":
 n, m = map(int, input().split())
 edges = []
 for _ in range(m):
  a, b = map(int, input().split())
  edges.append((a, b))

 result = find_bridges(n, edges)
 for u, v in result:
  print(u, v)
```

---

---

## Common Mistakes

### Mistake 1: Incorrect Parent Edge Handling

```python
# WRONG: Using parent vertex check with multiple edges
def dfs(v, parent):
 for u in graph[v]:
  if u == parent:  # Skips ALL edges to parent!
   continue
```

**Problem:** If there are multiple edges between v and parent, we should only skip ONE of them. With the vertex-based check, we skip all.

**Fix:** Use edge index instead of vertex for parent tracking:

```python
# CORRECT: Track edge index for multigraphs
def dfs(v, parent_edge_idx):
 for idx, u in graph[v]:  # Store (neighbor, edge_idx)
  if idx == parent_edge_idx:
   continue
```

### Mistake 2: Using low[u] Instead of disc[u] for Back Edges

```python
# WRONG
if disc[u] != -1:  # Back edge
 low[v] = min(low[v], low[u])  # Should be disc[u]!
```

**Problem:** Using `low[u]` can propagate incorrect values. Back edges connect to already-visited nodes; we should use their discovery time.

**Fix:** Always use `disc[u]` for back edge updates.

### Mistake 3: Forgetting to Handle Disconnected Graphs

```python
# WRONG: Only starts DFS from vertex 1
dfs(1, -1)

# CORRECT: Start DFS from all unvisited vertices
for v in range(1, n + 1):
 if disc[v] == -1:
  dfs(v, -1)
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Single vertex | n=1, m=0 | No bridges | No edges exist |
| Single edge | n=2, edges=[(1,2)] | (1,2) is bridge | Only connection |
| Complete graph | K4 | No bridges | Multiple paths exist |
| Tree | Any tree | All edges are bridges | Trees have no cycles |
| Cycle | Simple cycle | No bridges | Every edge has alternate path |
| Multiple edges | Two edges between same nodes | Neither is bridge | Alternate path via other edge |
| Self-loop | Edge (v,v) | Not a bridge | Does not affect connectivity |
| Disconnected | Two components | Bridges within each | Treat independently |

---

## When to Use This Pattern

### Use Bridge Finding When:
- Network reliability analysis (finding single points of failure)
- Graph connectivity problems
- Finding 2-edge-connected components
- Critical path/edge identification
- Road/network infrastructure planning

### Related Patterns:
- **Articulation Points:** Same algorithm, different condition
- **2-Edge-Connected Components:** Contract bridges to find components
- **SCC (Strongly Connected Components):** For directed graphs

### Pattern Recognition Checklist:
- [ ] Need to find critical edges? --> **Bridge finding**
- [ ] Need to find critical vertices? --> **Articulation points**
- [ ] Working with directed graph? --> **Consider SCC instead**
- [ ] Need all edges that preserve connectivity? --> **Non-bridge edges**

---

## Comparison: Bridges vs Articulation Points

| Aspect | Bridges | Articulation Points |
|--------|---------|---------------------|
| **Definition** | Edge whose removal disconnects graph | Vertex whose removal disconnects graph |
| **Condition** | `low[v] > disc[u]` | `low[v] >= disc[u]` (non-root) |
| **Root special case** | No | Yes (root is AP if >1 child) |
| **In a tree** | All edges | All non-leaf vertices |
| **In a cycle** | None | None |
| **Algorithm** | Tarjan's (edge variant) | Tarjan's (vertex variant) |

### Code Difference

```python
# Bridge condition (strict inequality)
if low[u] > disc[v]:
 bridges.append((v, u))

# Articulation point condition (non-strict for non-root)
if parent != -1 and low[u] >= disc[v]:
 articulation_points.add(v)
# Special case: root is AP if it has more than one DFS child
if parent == -1 and children > 1:
 articulation_points.add(v)
```

---

## Related CSES Problems

### Direct Applications

| Problem | Description |
|---------|-------------|
| [Road Reparation](https://cses.fi/problemset/task/1675) | MST, but understanding bridges helps |
| [Flight Routes Check](https://cses.fi/problemset/task/1682) | Connectivity, SCC related |

### Prerequisite Problems

| Problem | Why It Helps |
|---------|--------------|
| [Building Roads](https://cses.fi/problemset/task/1666) | Basic connectivity concepts |
| [Counting Rooms](https://cses.fi/problemset/task/1192) | DFS traversal practice |

### Advanced Extensions

| Problem | New Concept |
|---------|-------------|
| [Planets and Kingdoms](https://cses.fi/problemset/task/1683) | SCC (directed analog) |
| [Giant Pizza](https://cses.fi/problemset/task/1684) | 2-SAT uses SCC |

---

## Complexity Analysis

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(V + E) | Single DFS traversal visits each vertex and edge once |
| Space | O(V + E) | Adjacency list + disc/low arrays |

---

## Key Takeaways

1. **Core Concept:** A bridge is an edge with no "bypass" through back edges
2. **Algorithm:** Tarjan's algorithm with discovery time and low-link values
3. **Condition:** Edge (u,v) is bridge iff `low[v] > disc[u]`
4. **Difference from AP:** Bridges use strict inequality, no root special case
5. **Time Complexity:** Linear O(V+E) - optimal for this problem

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain what discovery time and low-link values represent
- [ ] Derive the bridge condition from first principles
- [ ] Handle multiple edges between same vertices correctly
- [ ] Implement the algorithm without looking at reference
- [ ] Identify bridges visually in a graph drawing
- [ ] Explain the difference between bridges and articulation points

---

## Additional Resources

- [CP-Algorithms: Finding Bridges](https://cp-algorithms.com/graph/bridge-searching.html)
- [CP-Algorithms: Finding Articulation Points](https://cp-algorithms.com/graph/cutpoints.html)
- [Tarjan's Original Paper](https://doi.org/10.1137/0201010)
- [CSES Giant Pizza](https://cses.fi/problemset/task/1684) - SCC-based problem
