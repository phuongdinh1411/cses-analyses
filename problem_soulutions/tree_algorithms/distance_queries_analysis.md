---
layout: simple
title: "Distance Queries - Tree Algorithms Problem"
permalink: /problem_soulutions/tree_algorithms/distance_queries_analysis
difficulty: Medium
tags: [tree, lca, binary-lifting, dfs]
prerequisites: [tree_traversal, binary_lifting_basics]
---

# Distance Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | LCA with Binary Lifting |
| **CSES Link** | [Distance Queries](https://cses.fi/problemset/task/1135) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Use LCA (Lowest Common Ancestor) to compute distances in a tree
- [ ] Implement binary lifting for O(log n) ancestor queries
- [ ] Apply the distance formula: `dist(a,b) = depth[a] + depth[b] - 2*depth[LCA(a,b)]`
- [ ] Preprocess a tree to answer multiple path queries efficiently

---

## Problem Statement

**Problem:** Given a tree with n nodes, answer q queries of the form "what is the distance (number of edges) between nodes a and b?"

**Input:**
- Line 1: Two integers n and q (number of nodes and queries)
- Next n-1 lines: Two integers a and b describing an edge
- Next q lines: Two integers a and b (query nodes)

**Output:**
- For each query, print the distance between the two nodes

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- 1 <= a, b <= n

### Example

```
Input:
5 3
1 2
1 3
3 4
3 5
1 4
5 4
2 5

Output:
2
2
3
```

**Explanation:**
- Query 1: Path 1 -> 3 -> 4 has length 2
- Query 2: Path 5 -> 3 -> 4 has length 2
- Query 3: Path 2 -> 1 -> 3 -> 5 has length 3

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently compute the distance between any two nodes in a tree without traversing the path each time?

The core insight is that **every path between two nodes in a tree passes through their Lowest Common Ancestor (LCA)**. This lets us break the path into two parts and use precomputed depths.

### Breaking Down the Problem

1. **What are we looking for?** The number of edges between two nodes
2. **What information do we have?** The tree structure (edges)
3. **What is the relationship between input and output?** The distance equals the sum of distances from each node to their LCA

### The Distance Formula

```
For nodes a and b with LCA l:

distance(a, b) = depth[a] + depth[b] - 2 * depth[l]
```

**Why does this work?**
- `depth[a]` = distance from root to a
- `depth[b]` = distance from root to b
- The path from a to b goes: a -> ... -> LCA -> ... -> b
- We add both depths but count the root-to-LCA portion twice, so we subtract `2 * depth[LCA]`

### Visual Explanation

```
        1 (depth=0)
       / \
      2   3 (depth=1)
         / \
        4   5 (depth=2)

Query: distance(2, 4)
- depth[2] = 1
- depth[4] = 2
- LCA(2, 4) = 1, depth[1] = 0
- distance = 1 + 2 - 2*0 = 3

Path: 2 -> 1 -> 3 -> 4 (3 edges)
```

---

## Solution 1: Brute Force (BFS for Each Query)

### Idea

For each query, run BFS/DFS from node a to find the distance to node b.

### Algorithm

1. Build adjacency list from edges
2. For each query (a, b):
   - Run BFS from a
   - Return distance when b is reached

### Code

```python
from collections import deque, defaultdict

def solve_brute_force(n, edges, queries):
    """
    Brute force: BFS for each query.

    Time: O(q * n)
    Space: O(n)
    """
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    def bfs_distance(start, end):
        if start == end:
            return 0
        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            node, dist = queue.popleft()
            for neighbor in graph[node]:
                if neighbor == end:
                    return dist + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        return -1

    return [bfs_distance(a, b) for a, b in queries]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | BFS takes O(n) per query |
| Space | O(n) | Queue and visited set |

### Why This Works (But Is Slow)

Correctness is guaranteed since BFS finds shortest paths. However, with q = 2x10^5 queries and n = 2x10^5 nodes, this gives 4x10^10 operations - far too slow.

---

## Solution 2: Optimal Solution (LCA with Binary Lifting)

### Key Insight

> **The Trick:** Preprocess the tree to answer LCA queries in O(log n), then use the distance formula.

### Binary Lifting Concept

Binary lifting precomputes the 2^k-th ancestor of each node. To find LCA:
1. Bring both nodes to the same depth (using binary jumps)
2. Jump both nodes up together until they meet

| Array | Meaning |
|-------|---------|
| `depth[v]` | Distance from root to node v |
| `up[k][v]` | The 2^k-th ancestor of node v |

### Algorithm

1. **Preprocessing O(n log n):**
   - DFS to compute depths and direct parents
   - Build binary lifting table: `up[k][v] = up[k-1][up[k-1][v]]`

2. **Query O(log n):**
   - Find LCA of a and b using binary lifting
   - Return `depth[a] + depth[b] - 2 * depth[LCA]`

### Dry Run Example

Let us trace through with the example tree:

```
Tree:
        1
       / \
      2   3
         / \
        4   5

Query: distance(2, 5)
```

**Step 1: Preprocessing**
```
DFS from node 1:
  depth = [_, 0, 1, 1, 2, 2]  (1-indexed, _ is placeholder)

Binary lifting table (up[k][v] = 2^k ancestor):
  up[0] = [_, 0, 1, 1, 3, 3]  (direct parents, 0 means no parent)
  up[1] = [_, 0, 0, 0, 1, 1]  (2^1 = 2nd ancestors)
```

**Step 2: Query distance(2, 5)**
```
Finding LCA(2, 5):
  depth[2] = 1, depth[5] = 2

  Node 5 is deeper, so lift it:
  - Difference = 2 - 1 = 1
  - Jump 5 up by 1: 5 -> up[0][5] = 3

  Now both at depth 1: nodes 2 and 3

  They are different, so jump both:
  - up[0][2] = 1, up[0][3] = 1  (same!)
  - LCA = 1

Computing distance:
  distance = depth[2] + depth[5] - 2*depth[1]
           = 1 + 2 - 2*0
           = 3

Path: 2 -> 1 -> 3 -> 5 (verified: 3 edges)
```

### Code (Python)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n, q = int(input_data[idx]), int(input_data[idx+1])
    idx += 2

    # Build adjacency list
    graph = defaultdict(list)
    for _ in range(n - 1):
        u, v = int(input_data[idx]), int(input_data[idx+1])
        idx += 2
        graph[u].append(v)
        graph[v].append(u)

    # Binary lifting setup
    LOG = 18  # ceil(log2(2*10^5)) = 18
    up = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)

    # DFS to compute depths and direct parents
    def dfs(node, parent):
        up[0][node] = parent
        for child in graph[node]:
            if child != parent:
                depth[child] = depth[node] + 1
                dfs(child, node)

    dfs(1, 0)  # Root at node 1

    # Build binary lifting table
    for k in range(1, LOG):
        for v in range(1, n + 1):
            up[k][v] = up[k-1][up[k-1][v]]

    def lca(a, b):
        # Ensure a is deeper
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]

        # Lift a to same depth as b
        for k in range(LOG):
            if diff & (1 << k):
                a = up[k][a]

        if a == b:
            return a

        # Binary search for LCA
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]

        return up[0][a]

    def distance(a, b):
        l = lca(a, b)
        return depth[a] + depth[b] - 2 * depth[l]

    # Process queries
    results = []
    for _ in range(q):
        a, b = int(input_data[idx]), int(input_data[idx+1])
        idx += 2
        results.append(str(distance(a, b)))

    print('\n'.join(results))

if __name__ == "__main__":
    solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
const int LOG = 18;

vector<int> adj[MAXN];
int up[LOG][MAXN];
int depth[MAXN];
int n, q;

void dfs(int v, int parent) {
    up[0][v] = parent;
    for (int child : adj[v]) {
        if (child != parent) {
            depth[child] = depth[v] + 1;
            dfs(child, v);
        }
    }
}

int lca(int a, int b) {
    if (depth[a] < depth[b]) swap(a, b);

    int diff = depth[a] - depth[b];
    for (int k = 0; k < LOG; k++) {
        if (diff & (1 << k)) {
            a = up[k][a];
        }
    }

    if (a == b) return a;

    for (int k = LOG - 1; k >= 0; k--) {
        if (up[k][a] != up[k][b]) {
            a = up[k][a];
            b = up[k][b];
        }
    }

    return up[0][a];
}

int distance(int a, int b) {
    int l = lca(a, b);
    return depth[a] + depth[b] - 2 * depth[l];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> n >> q;

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // DFS from root (node 1)
    depth[1] = 0;
    dfs(1, 0);

    // Build binary lifting table
    for (int k = 1; k < LOG; k++) {
        for (int v = 1; v <= n; v++) {
            up[k][v] = up[k-1][up[k-1][v]];
        }
    }

    // Process queries
    while (q--) {
        int a, b;
        cin >> a >> b;
        cout << distance(a, b) << "\n";
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | O(n log n) preprocessing + O(q log n) queries |
| Space | O(n log n) | Binary lifting table has LOG rows of n elements |

---

## Common Mistakes

### Mistake 1: Wrong Depth Initialization

```python
# WRONG - depth[root] should be 0, not undefined
depth = [0] * (n + 1)
def dfs(node, parent):
    depth[node] = depth[parent] + 1  # Root's parent is 0, so depth[1] = 1
```

**Problem:** If root's depth starts at 1 instead of 0, the distance formula gives wrong results.
**Fix:** Either set `depth[root] = 0` explicitly or handle root specially in DFS.

### Mistake 2: Insufficient LOG Value

```python
# WRONG for n = 2*10^5
LOG = 10  # 2^10 = 1024, way too small!

# CORRECT
LOG = 18  # 2^18 = 262144 > 2*10^5
```

**Problem:** If LOG is too small, binary lifting cannot reach distant ancestors.
**Fix:** Use `LOG = ceil(log2(n)) + 1` or just 18-20 for n up to 2x10^5.

### Mistake 3: Not Handling Same Node Query

```python
# WRONG - may cause issues if not handled
def lca(a, b):
    if depth[a] < depth[b]:
        a, b = b, a
    # ... rest of code
```

**Problem:** Query for distance(a, a) should return 0.
**Fix:** The code actually handles this correctly since LCA(a, a) = a, giving distance = 0. But it is good to verify.

### Mistake 4: 0-indexed vs 1-indexed Confusion

```python
# WRONG - mixing indices
up = [[0] * n for _ in range(LOG)]  # 0-indexed
dfs(1, 0)  # 1-indexed call!
```

**Problem:** Accessing out-of-bounds or wrong nodes.
**Fix:** Be consistent - use 1-indexed throughout for tree problems.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Same node | `distance(3, 3)` | 0 | Node to itself has distance 0 |
| Adjacent nodes | `distance(1, 2)` where 1-2 is edge | 1 | Direct edge = distance 1 |
| Root query | `distance(1, n)` | depth[n] | Path to root is just depth |
| Linear tree | 1-2-3-...-n | n-1 for distance(1,n) | Worst case path length |
| Star tree | All nodes connect to 1 | 2 for any non-root pair | All paths go through center |

---

## When to Use This Pattern

### Use This Approach When:
- Multiple queries about paths/distances in a static tree
- Need to find LCA of node pairs efficiently
- Computing path properties (distance, sum, min, max on path)
- Problems involving tree paths passing through ancestors

### Do Not Use When:
- Tree changes dynamically (consider Link-Cut Trees)
- Only a single query (BFS is simpler)
- Graph is not a tree (use Dijkstra/BFS)

### Pattern Recognition Checklist:
- [ ] Is the graph a tree (n nodes, n-1 edges, connected)?
- [ ] Are there multiple queries about paths?
- [ ] Does the solution involve finding common ancestors?
- [ ] Can path problems be split at LCA?

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subordinates](https://cses.fi/problemset/task/1674) | Basic tree DFS, computing subtree properties |
| [Tree Diameter](https://cses.fi/problemset/task/1131) | Understanding tree paths |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Company Queries I](https://cses.fi/problemset/task/1687) | Find k-th ancestor (uses binary lifting directly) |
| [Company Queries II](https://cses.fi/problemset/task/1688) | LCA queries without distance |
| [Counting Paths](https://cses.fi/problemset/task/1136) | Path counting using LCA + difference arrays |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Path Queries](https://cses.fi/problemset/task/1138) | Path sums with updates (Euler tour + segment tree) |
| [Path Queries II](https://cses.fi/problemset/task/2134) | Path min/max with updates (HLD) |
| [Distinct Colors](https://cses.fi/problemset/task/1139) | Small-to-large merging on tree |

---

## Key Takeaways

1. **The Core Idea:** Distance in a tree can be computed using LCA: `dist(a,b) = depth[a] + depth[b] - 2*depth[LCA]`
2. **Time Optimization:** Binary lifting reduces LCA queries from O(n) to O(log n)
3. **Space Trade-off:** We use O(n log n) space for the lifting table to enable fast queries
4. **Pattern:** This is a fundamental technique for all tree path problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why the distance formula works with a diagram
- [ ] Implement binary lifting from scratch
- [ ] Trace through LCA computation step by step
- [ ] Identify when a problem can use LCA-based solutions
- [ ] Implement in your preferred language in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: LCA with Binary Lifting](https://cp-algorithms.com/graph/lca_binary_lifting.html)
- [CSES Problem Set - Tree Algorithms](https://cses.fi/problemset/)
- [USACO Guide: Binary Lifting](https://usaco.guide/plat/binary-lifting)
