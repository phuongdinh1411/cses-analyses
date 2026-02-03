---
layout: simple
title: "Creating Offices - Tree Coverage Problem"
permalink: /problem_soulutions/advanced_graph_problems/creating_offices_analysis
difficulty: Medium
tags: [trees, greedy, bfs, dfs, graph-algorithms]
---

# Creating Offices

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Creating Offices](https://cses.fi/problemset/task/1752) |
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Greedy BFS/DFS Selection |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply greedy selection on trees to minimize facility placement
- [ ] Use BFS to find farthest uncovered nodes efficiently
- [ ] Understand distance-based coverage constraints in tree structures
- [ ] Implement the "farthest-first" greedy strategy for optimal placement

---

## Problem Statement

**Problem:** Given a tree with n nodes, place offices at some nodes so that every node is within distance d of at least one office. Find the minimum number of offices needed.

**Input:**
- Line 1: Two integers n (nodes) and d (max distance)
- Lines 2 to n: Two integers a and b (edge between nodes a and b)

**Output:**
- Minimum number of offices needed

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= d <= n
- 1 <= a, b <= n

### Example

```
Input:
7 2
1 2
1 3
2 4
2 5
3 6
3 7

Output:
1
```

**Explanation:** Place one office at node 1. All nodes are within distance 2:
- Node 1: distance 0 (office location)
- Nodes 2, 3: distance 1
- Nodes 4, 5, 6, 7: distance 2

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we minimize the number of offices while ensuring every node is covered?

The critical insight is that we should **start from the farthest uncovered nodes**. If we greedily place offices to cover the deepest/farthest nodes first, we ensure maximum coverage efficiency.

### Breaking Down the Problem

1. **What are we looking for?** Minimum number of office placements
2. **What constraint must be satisfied?** Every node within distance d of some office
3. **What's the greedy strategy?** Find farthest uncovered node, place office at distance d from it (toward center)

---

## Solution 1: Brute Force (Greedy by Coverage Count)

### Idea

Try placing an office at each node, pick the one that covers the most uncovered nodes, and repeat until all nodes are covered.

### Algorithm

1. Build adjacency list from edges
2. While uncovered nodes exist:
   - For each node, compute how many uncovered nodes it would cover
   - Place office at the node with maximum coverage
   - Mark all nodes within distance d as covered

### Code

```python
from collections import deque

def solve_brute_force(n, d, edges):
    """
    Greedy solution - place office at node covering most uncovered nodes.

    Time: O(n^2) per office placement
    Space: O(n)
    """
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    def get_coverage(start, max_dist):
        """BFS to find all nodes within max_dist from start."""
        covered = set()
        queue = deque([(start, 0)])
        visited = {start}

        while queue:
            node, dist = queue.popleft()
            covered.add(node)

            if dist < max_dist:
                for neighbor in adj[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))
        return covered

    uncovered = set(range(1, n + 1))
    offices = 0

    while uncovered:
        best_node, best_count = 1, 0
        for node in range(1, n + 1):
            coverage = get_coverage(node, d)
            count = len(coverage & uncovered)
            if count > best_count:
                best_count = count
                best_node = node

        uncovered -= get_coverage(best_node, d)
        offices += 1

    return offices
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 * k) | k offices, each requires O(n^2) to find best |
| Space | O(n) | Adjacency list and visited sets |

### Why This Works (But Is Slow)

This guarantees coverage but may not give the minimum number of offices. The greedy-by-coverage approach is a heuristic that works well in practice but isn't provably optimal for all cases.

---

## Solution 2: Optimal Greedy (Farthest-First Strategy)

### Key Insight

> **The Trick:** Always find the farthest uncovered node from any office, then place a new office exactly d steps toward the root from that node. This ensures maximum "reach" for each office.

### Algorithm

1. Root the tree at any node (e.g., node 1)
2. Process nodes in decreasing order of depth (deepest first)
3. For each uncovered node at depth h:
   - Walk d steps toward root to find office location
   - Mark all nodes within distance d of new office as covered
4. Count total offices placed

### Dry Run Example

Let's trace through with the example tree:

```
Tree structure (rooted at 1):
         1
        / \
       2   3
      / \ / \
     4  5 6  7

n = 7, d = 2
```

```
Initial: All nodes uncovered
Depth order: [4,5,6,7] at depth 2, [2,3] at depth 1, [1] at depth 0

Step 1: Process node 4 (depth 2, uncovered)
  Walk d=2 steps toward root: 4 -> 2 -> 1
  Place office at node 1
  Coverage from node 1 (distance <= 2): {1, 2, 3, 4, 5, 6, 7}
  All nodes now covered!

Result: 1 office at node 1
```

### Code

```python
from collections import deque

def solve_optimal(n, d, edges):
    """
    Optimal greedy: process deepest uncovered nodes first.

    Time: O(n)
    Space: O(n)
    """
    if n == 1:
        return 1

    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    # Root tree at node 1, compute depths and parents
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    order = []  # Nodes in BFS order

    queue = deque([1])
    visited = {1}

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                depth[neighbor] = depth[node] + 1
                queue.append(neighbor)

    # Process nodes from deepest to shallowest
    order.sort(key=lambda x: -depth[x])

    covered_dist = [-1] * (n + 1)  # Distance to nearest office (-1 = uncovered)
    offices = 0

    for node in order:
        if covered_dist[node] >= 0:
            continue  # Already covered

        # Find office location: walk d steps toward root
        office = node
        for _ in range(d):
            if parent[office] != 0:
                office = parent[office]

        # BFS to mark all nodes within distance d of office
        offices += 1
        q = deque([(office, 0)])
        vis = {office}

        while q:
            curr, dist = q.popleft()
            covered_dist[curr] = dist

            if dist < d:
                for neighbor in adj[curr]:
                    if neighbor not in vis:
                        vis.add(neighbor)
                        q.append((neighbor, dist + 1))

    return offices


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().split()
    n, d = int(data[0]), int(data[1])
    edges = [(int(data[i]), int(data[i+1])) for i in range(2, len(data), 2)]
    print(solve_optimal(n, d, edges))
```

### C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, d;
    cin >> n >> d;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    if (n == 1) {
        cout << 1 << "\n";
        return 0;
    }

    // Root tree at node 1
    vector<int> parent(n + 1, 0);
    vector<int> depth(n + 1, 0);
    vector<int> order;
    vector<bool> visited(n + 1, false);

    queue<int> bfs;
    bfs.push(1);
    visited[1] = true;

    while (!bfs.empty()) {
        int node = bfs.front();
        bfs.pop();
        order.push_back(node);

        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                parent[neighbor] = node;
                depth[neighbor] = depth[node] + 1;
                bfs.push(neighbor);
            }
        }
    }

    // Sort by depth descending
    sort(order.begin(), order.end(), [&](int a, int b) {
        return depth[a] > depth[b];
    });

    vector<int> covered_dist(n + 1, -1);
    int offices = 0;

    for (int node : order) {
        if (covered_dist[node] >= 0) continue;

        // Walk d steps toward root
        int office = node;
        for (int i = 0; i < d && parent[office] != 0; i++) {
            office = parent[office];
        }

        // BFS to mark coverage
        offices++;
        queue<pair<int, int>> q;
        q.push({office, 0});
        vector<bool> vis(n + 1, false);
        vis[office] = true;

        while (!q.empty()) {
            auto [curr, dist] = q.front();
            q.pop();
            covered_dist[curr] = dist;

            if (dist < d) {
                for (int neighbor : adj[curr]) {
                    if (!vis[neighbor]) {
                        vis[neighbor] = true;
                        q.push({neighbor, dist + 1});
                    }
                }
            }
        }
    }

    cout << offices << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | BFS is O(n), sorting is O(n log n) |
| Space | O(n) | Adjacency list, parent/depth arrays |

---

## Common Mistakes

### Mistake 1: Not Walking Far Enough Toward Root

```python
# WRONG: Place office at the uncovered node itself
office = node  # Office at leaf node

# CORRECT: Walk d steps toward root for better coverage
office = node
for _ in range(d):
    if parent[office] != 0:
        office = parent[office]
```

**Problem:** Placing office at a leaf wastes coverage - half the radius extends into empty space.
**Fix:** Walk toward the center of the tree to maximize coverage area.

### Mistake 2: Processing Nodes in Wrong Order

```python
# WRONG: Process nodes in BFS order (shallow first)
for node in order:  # If order is BFS order
    ...

# CORRECT: Process deepest nodes first
order.sort(key=lambda x: -depth[x])
for node in order:
    ...
```

**Problem:** Processing shallow nodes first may place offices inefficiently, leaving deep nodes uncovered.
**Fix:** Always process deepest uncovered nodes first.

### Mistake 3: Forgetting Single Node Case

```python
# WRONG: Assumes tree has at least 2 nodes
parent = [0] * (n + 1)
# ... BFS that expects edges

# CORRECT: Handle n=1 explicitly
if n == 1:
    return 1
```

**Problem:** A single node tree still needs one office.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n=1, d=1 | 1 | Need one office for the only node |
| Line graph, d covers all | n=5, d=4 (1-2-3-4-5) | 1 | One central office covers everything |
| Line graph, d=1 | n=5, d=1 (1-2-3-4-5) | 2 | Offices at nodes 2 and 4 |
| Star graph | n=5, d=1 (center=1) | 1 | Office at center covers all |
| d=0 | n=3, d=0 | 3 | Each node needs its own office |

---

## When to Use This Pattern

### Use This Approach When:
- You need to place facilities to cover all nodes in a tree
- There's a distance constraint for coverage
- You want to minimize the number of facilities

### Don't Use When:
- Graph has cycles (need different algorithms)
- Weighted edges with variable costs (need weighted BFS/Dijkstra)
- You need to find ALL possible optimal placements

### Pattern Recognition Checklist:
- [ ] Tree structure with coverage requirement? -> **Greedy farthest-first**
- [ ] Need minimum facilities? -> **Process deepest/farthest nodes first**
- [ ] Distance-based constraint? -> **BFS for coverage calculation**

---

## Related Problems

| Difficulty | Problem | Key Concept |
|------------|---------|-------------|
| Easier | [Tree Diameter](https://cses.fi/problemset/task/1131) | BFS on trees, farthest nodes |
| Easier | [Tree Distances I](https://cses.fi/problemset/task/1132) | Computing distances |
| Similar | [Tree Distances II](https://cses.fi/problemset/task/1133) | Sum of distances |
| Similar | [Company Queries I](https://cses.fi/problemset/task/1687) | Ancestor queries |
| Harder | [Path Queries](https://cses.fi/problemset/task/1138) | Path operations |

---

## Key Takeaways

1. **The Core Idea:** Process uncovered nodes from farthest to nearest, placing offices optimally toward the tree center
2. **Time Optimization:** Single BFS pass with proper ordering gives O(n log n) vs O(n^2) brute force
3. **Greedy Correctness:** Farthest-first ensures each office covers maximum previously uncovered territory
4. **Pattern:** This is a classic "facility location" problem on trees

---

## Practice Checklist

- [ ] Solve this problem without looking at the solution
- [ ] Explain why processing deepest nodes first is optimal
- [ ] Implement the parent/depth computation via BFS
- [ ] Handle edge cases (n=1, d=0, star graphs, line graphs)