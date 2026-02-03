---
layout: simple
title: "Graph Girth - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/graph_girth_analysis
difficulty: Medium
tags: [graph, bfs, cycle-detection, shortest-path]
---

# Graph Girth

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Graph Girth](https://cses.fi/problemset/task/1707) |
| **Difficulty** | Medium |
| **Category** | Graph Theory |
| **Time Limit** | 1 second |
| **Key Technique** | BFS from each node |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the concept of graph girth (shortest cycle length)
- [ ] Apply BFS to find shortest paths back to a starting node
- [ ] Handle cycle detection in undirected graphs
- [ ] Recognize when to use BFS vs DFS for shortest path problems

---

## Problem Statement

**Problem:** Given an undirected graph, find the length of the shortest cycle. If the graph has no cycles, output -1.

**Input:**
- Line 1: n m (number of nodes and edges)
- Next m lines: a b (undirected edge between nodes a and b)

**Output:**
- The length of the shortest cycle, or -1 if no cycle exists

**Constraints:**
- 1 <= n <= 2500
- 1 <= m <= 5000
- 1 <= a, b <= n

### Example

```
Input:
4 5
1 2
2 3
3 4
4 1
2 4

Output:
3
```

**Explanation:** The shortest cycle is 2 -> 3 -> 4 -> 2 with length 3. Another cycle 1 -> 2 -> 3 -> 4 -> 1 has length 4.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we find the shortest cycle in an undirected graph?

The girth of a graph is the length of its shortest cycle. In an undirected graph, we can detect a cycle when BFS from a node discovers an already-visited node through a different path.

### Breaking Down the Problem

1. **What are we looking for?** The minimum cycle length across all cycles in the graph.
2. **What information do we have?** The graph structure (nodes and edges).
3. **What's the relationship between input and output?** We need to explore all possible cycles and find the shortest one.

### The Key Insight

When doing BFS from a node, if we reach an already-visited node (that is not our immediate parent), we have found a cycle. The cycle length is `dist[u] + dist[v] + 1` where u and v are the two endpoints of the edge that closes the cycle.

---

## Solution 1: Brute Force (DFS)

### Idea

For each node, use DFS to find all cycles containing that node and track the minimum length.

### Algorithm

1. For each node, run DFS tracking the path depth
2. When we revisit a node, calculate cycle length
3. Track the minimum cycle length found

### Code

```python
def solve_brute_force(n, edges):
    """
    Brute force: DFS from each node.

    Time: O(n * m) - exponential in worst case
    Space: O(n)
    """
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    min_girth = float('inf')

    for start in range(1, n + 1):
        visited = [False] * (n + 1)

        def dfs(node, parent, depth):
            nonlocal min_girth
            if visited[node]:
                return depth
            visited[node] = True

            for neighbor in adj[node]:
                if neighbor != parent:
                    cycle_len = dfs(neighbor, node, depth + 1)
                    if cycle_len > 0:
                        min_girth = min(min_girth, cycle_len)

            visited[node] = False
            return -1

        dfs(start, -1, 0)

    return min_girth if min_girth != float('inf') else -1
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * 2^n) | Exponential due to path enumeration |
| Space | O(n) | Recursion stack |

### Why This Works (But Is Slow)

DFS explores all paths, which leads to exponential time complexity. It does not efficiently find the shortest cycle.

---

## Solution 2: Optimal Solution (BFS from Each Node)

### Key Insight

> **The Trick:** BFS finds shortest paths. When BFS discovers a node that is already visited (via a different path), we have found a cycle, and its length is the sum of the two distances plus one.

### Why BFS Works for Girth

In an undirected graph, when BFS from node `s` reaches a node `v` through node `u`, and `v` is already visited with a different parent, we have found a cycle:
- Path 1: s -> ... -> v (length dist[v])
- Path 2: s -> ... -> u -> v (length dist[u] + 1)
- Cycle length: dist[u] + dist[v] + 1

### Algorithm

1. For each node `s`, run BFS
2. Track distance and parent for each visited node
3. When we find an edge (u, v) where v is already visited and v != parent[u], we found a cycle
4. Cycle length = dist[u] + dist[v] + 1
5. Return minimum cycle length across all BFS runs

### Dry Run Example

Input: `n=4, edges=[(1,2), (2,3), (3,4), (4,1), (2,4)]`

```
Graph visualization:
    1 --- 2
    |     |\
    |     | \
    4 --- 3  |
     \-------/

BFS from node 1:
  Start: dist[1] = 0, parent[1] = -1
  Queue: [1]

  Step 1: Process node 1
    Neighbors: 2, 4
    dist[2] = 1, parent[2] = 1
    dist[4] = 1, parent[4] = 1
    Queue: [2, 4]

  Step 2: Process node 2
    Neighbors: 1, 3, 4
    Skip 1 (parent)
    dist[3] = 2, parent[3] = 2
    Check 4: already visited, parent[2]=1 != 4
      Cycle found! Length = dist[2] + dist[4] + 1 = 1 + 1 + 1 = 3
    Queue: [4, 3]

BFS from node 2:
  Start: dist[2] = 0

  Step 1: Process node 2
    dist[1] = 1, dist[3] = 1, dist[4] = 1
    Queue: [1, 3, 4]

  Step 2: Process node 1
    Check 4: already visited, parent[1]=2 != 4
      Cycle found! Length = dist[1] + dist[4] + 1 = 1 + 1 + 1 = 3

Minimum girth = 3
```

### Visual Diagram

```
Finding cycle through BFS from node 2:

       1 (dist=1)
      / \
     /   \
    2-----4 (dist=1)  <-- Edge 1-4 closes the cycle!
   (start)

Cycle: 2 -> 1 -> 4 -> 2
Length: dist[1] + dist[4] + 1 = 1 + 1 + 1 = 3
```

### Code

```python
from collections import deque

def solve(n, m, edges):
    """
    Optimal solution: BFS from each node.

    Time: O(n * (n + m))
    Space: O(n + m)
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    min_girth = float('inf')

    # BFS from each node
    for start in range(1, n + 1):
        dist = [-1] * (n + 1)
        parent = [-1] * (n + 1)

        dist[start] = 0
        queue = deque([start])

        while queue:
            u = queue.popleft()

            for v in adj[u]:
                if dist[v] == -1:
                    # Not visited yet
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    queue.append(v)
                elif parent[u] != v:
                    # Found a cycle (v already visited via different path)
                    cycle_length = dist[u] + dist[v] + 1
                    min_girth = min(min_girth, cycle_length)

    return min_girth if min_girth != float('inf') else -1


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

### C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    int minGirth = INT_MAX;

    // BFS from each node
    for (int start = 1; start <= n; start++) {
        vector<int> dist(n + 1, -1);
        vector<int> parent(n + 1, -1);

        dist[start] = 0;
        queue<int> q;
        q.push(start);

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int v : adj[u]) {
                if (dist[v] == -1) {
                    dist[v] = dist[u] + 1;
                    parent[v] = u;
                    q.push(v);
                } else if (parent[u] != v) {
                    // Found a cycle
                    int cycleLength = dist[u] + dist[v] + 1;
                    minGirth = min(minGirth, cycleLength);
                }
            }
        }
    }

    cout << (minGirth == INT_MAX ? -1 : minGirth) << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * (n + m)) | BFS is O(n + m), run n times |
| Space | O(n + m) | Adjacency list + BFS arrays |

---

## Common Mistakes

### Mistake 1: Counting Parent Edge as Cycle

```python
# WRONG
for v in adj[u]:
    if dist[v] != -1:
        # This includes the edge we came from!
        cycle_length = dist[u] + dist[v] + 1
```

**Problem:** In undirected graphs, the edge (u, parent[u]) should not be counted as forming a cycle.

**Fix:** Check that `v != parent[u]` before considering it a cycle:

```python
# CORRECT
for v in adj[u]:
    if dist[v] != -1 and parent[u] != v:
        cycle_length = dist[u] + dist[v] + 1
```

### Mistake 2: Only Running BFS from One Node

```python
# WRONG
dist[1] = 0
queue = deque([1])
# Only finds cycles reachable from node 1
```

**Problem:** A single BFS might not find the shortest cycle if it starts from a node far from the shortest cycle.

**Fix:** Run BFS from every node to ensure we find the global minimum.

### Mistake 3: Wrong Cycle Length Calculation

```python
# WRONG
cycle_length = dist[u] + dist[v]  # Missing +1 for the edge (u,v)

# WRONG
cycle_length = dist[u] + 1  # Only counting one path
```

**Problem:** The cycle consists of two paths (start to u, start to v) plus the edge (u, v).

**Fix:** `cycle_length = dist[u] + dist[v] + 1`

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No edges | `n=5, m=0` | -1 | No edges means no cycles |
| Tree (no cycles) | `n=4, m=3` (tree edges) | -1 | Trees have no cycles |
| Self-loop | `n=2, m=1, edge=(1,1)` | 1 | Cycle of length 1 |
| Triangle | `n=3, m=3` (triangle) | 3 | Smallest possible cycle (without self-loops) |
| Multiple components | Graph with multiple components | Shortest cycle in any component | May exist in any component |
| Large cycle only | `n=1000`, single cycle | 1000 | BFS still finds it |

---

## When to Use This Pattern

### Use This Approach When:
- Finding the shortest cycle in an unweighted graph
- Graph is undirected
- Need exact minimum cycle length

### Don't Use When:
- Graph is weighted (use Dijkstra-based approach)
- Only need to detect if a cycle exists (use Union-Find or simple DFS)
- Graph is directed (use different cycle detection methods)

### Pattern Recognition Checklist:
- [ ] Finding shortest cycle? -> **BFS from each node**
- [ ] Detecting any cycle? -> **Union-Find or DFS**
- [ ] Weighted graph cycle? -> **Dijkstra-based approach**
- [ ] Directed graph cycle? -> **DFS with coloring**

---

## Related Problems

### Easier (Do These First)

| Problem | Link | Why It Helps |
|---------|------|--------------|
| Round Trip | [CSES 1669](https://cses.fi/problemset/task/1669) | Basic cycle detection and path finding |
| Building Roads | [CSES 1666](https://cses.fi/problemset/task/1666) | Graph connectivity fundamentals |

### Similar Difficulty

| Problem | Link | Key Difference |
|---------|------|----------------|
| Round Trip II | [CSES 1678](https://cses.fi/problemset/task/1678) | Directed graph cycle detection |
| Shortest Routes I | [CSES 1671](https://cses.fi/problemset/task/1671) | BFS/Dijkstra for shortest paths |

### Harder (Do These After)

| Problem | Link | New Concept |
|---------|------|-------------|
| Cycle Finding | [CSES 1197](https://cses.fi/problemset/task/1197) | Finding negative cycles (Bellman-Ford) |
| Flight Routes | [CSES 1196](https://cses.fi/problemset/task/1196) | K shortest paths |

---

## Key Takeaways

1. **The Core Idea:** BFS from each node to find when we reach an already-visited node via a different path.
2. **Time Optimization:** BFS guarantees shortest paths, so the first cycle found from each start is the shortest containing that start.
3. **Space Trade-off:** O(n) extra space per BFS run for distance and parent arrays.
4. **Pattern:** "BFS from each node" is a common technique for finding shortest cycles in unweighted graphs.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why BFS finds the shortest cycle
- [ ] Implement the solution without looking at the code
- [ ] Handle the parent edge case correctly
- [ ] Calculate the cycle length formula correctly
- [ ] Identify graph girth problems in contests

---

## Additional Resources

- [CP-Algorithms: Finding Cycle](https://cp-algorithms.com/graph/finding-cycle.html)
- [CP-Algorithms: BFS](https://cp-algorithms.com/graph/breadth-first-search.html)
- [CSES Shortest Routes I](https://cses.fi/problemset/task/1671) - BFS-based shortest path
