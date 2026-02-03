---
layout: simple
title: "Path Queries II - Tree Algorithms Problem"
permalink: /problem_soulutions/tree_algorithms/path_queries_ii_analysis
difficulty: Hard
tags: [heavy-light-decomposition, segment-tree, tree, path-queries, lca]
prerequisites: [tree_basics, segment_tree, lca]
---

# Path Queries II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Heavy-Light Decomposition + Segment Tree |
| **CSES Link** | [https://cses.fi/problemset/task/2134](https://cses.fi/problemset/task/2134) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement Heavy-Light Decomposition (HLD)
- [ ] Combine HLD with segment trees for efficient path queries
- [ ] Handle point updates and path maximum queries in O(log^2 n)
- [ ] Decompose a tree into chains for linearization
- [ ] Apply HLD pattern to other path query problems

---

## Problem Statement

**Problem:** Given a tree with n nodes where each node has a value, process two types of queries:
1. **Update (type 1):** Change the value of node s to x
2. **Query (type 2):** Find the maximum value on the path from node a to node b

**Input:**
- Line 1: Two integers n and q (number of nodes and queries)
- Line 2: n integers v1, v2, ..., vn (initial node values)
- Next n-1 lines: Two integers a, b describing an edge
- Next q lines: Either "1 s x" (update) or "2 a b" (query)

**Output:**
- For each type 2 query, print the maximum value on the path

**Constraints:**
- 1 <= n, q <= 2 * 10^5
- 1 <= vi, x <= 10^9

### Example

```
Input:
5 5
4 2 5 2 1
1 2
1 3
3 4
3 5
2 2 5
1 3 7
2 2 5
2 1 1
2 2 4

Output:
5
7
4
7
```

**Explanation:**
- Query 2 5: Path is 2->1->3->5, values are [2,4,5,1], max = 5
- Update node 3 to value 7
- Query 2 5: Path is 2->1->3->5, values are [2,4,7,1], max = 7
- Query 1 1: Path is just node 1, max = 4
- Query 2 4: Path is 2->1->3->4, values are [2,4,7,2], max = 7

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently answer path queries on a tree?

The challenge is that a tree path can go through any nodes, not just along a linear structure. We need to transform tree paths into contiguous segments that a segment tree can handle.

### Breaking Down the Problem

1. **What are we looking for?** Maximum value on arbitrary tree paths
2. **What information do we have?** Tree structure and node values
3. **What's the relationship?** Any path can be decomposed into O(log n) chains

### The Core Insight: Heavy-Light Decomposition

Think of HLD like organizing a company hierarchy:
- Each node has one "heavy" child (largest subtree) and possibly multiple "light" children
- Following heavy edges creates long "chains"
- Any path crosses at most O(log n) chains because each light edge at least halves the subtree size

```
Original Tree:         After HLD (chains shown):
      1                      [1-2-4-8] <- Heavy chain
     /|\                    /
    2 3 5                 [3]  [5-6]
   /|   |                 |
  4 7   6                [7]
  |
  8
```

---

## Solution 1: Brute Force with LCA

### Idea

For each query, find the path using LCA and traverse all nodes to find maximum.

### Algorithm

1. Build tree and precompute LCA using binary lifting
2. For each query, find LCA of a and b
3. Traverse from a to LCA and from b to LCA, tracking maximum

### Code

```python
def solve_brute_force(n, values, edges, queries):
    """
    Brute force: traverse path for each query.

    Time: O(q * n) - each query may traverse O(n) nodes
    Space: O(n log n) - for LCA preprocessing
    """
    from collections import defaultdict
    import sys
    sys.setrecursionlimit(300000)

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    LOG = 18
    parent = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)

    def dfs(node, par, d):
        parent[0][node] = par
        depth[node] = d
        for child in graph[node]:
            if child != par:
                dfs(child, node, d + 1)

    dfs(1, 0, 0)

    for k in range(1, LOG):
        for v in range(1, n + 1):
            parent[k][v] = parent[k-1][parent[k-1][v]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        for k in range(LOG):
            if diff & (1 << k):
                a = parent[k][a]
        if a == b:
            return a
        for k in range(LOG - 1, -1, -1):
            if parent[k][a] != parent[k][b]:
                a, b = parent[k][a], parent[k][b]
        return parent[0][a]

    def path_max(a, b):
        l = lca(a, b)
        max_val = values[l]
        # Traverse a to lca
        node = a
        while node != l:
            max_val = max(max_val, values[node])
            node = parent[0][node]
        # Traverse b to lca
        node = b
        while node != l:
            max_val = max(max_val, values[node])
            node = parent[0][node]
        return max_val

    results = []
    for query in queries:
        if query[0] == 1:  # Update
            s, x = query[1], query[2]
            values[s] = x
        else:  # Query
            a, b = query[1], query[2]
            results.append(path_max(a, b))

    return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query traverses up to n nodes |
| Space | O(n log n) | Binary lifting table for LCA |

### Why This Works (But Is Slow)

Correctness is guaranteed because we visit every node on the path. However, with n, q up to 2*10^5, this gives 4*10^10 operations - far too slow.

---

## Solution 2: Optimal with Heavy-Light Decomposition

### Key Insight

> **The Trick:** Decompose the tree into chains such that any path crosses O(log n) chains, then use a segment tree on the linearized nodes.

### Heavy-Light Decomposition Explained

**Step 1: Calculate subtree sizes and identify heavy edges**
- For each node, the "heavy child" is the one with the largest subtree
- Heavy edges form chains; light edges connect chains

**Step 2: Decompose into chains (DFS order)**
- Assign positions to nodes so each chain is contiguous
- Store chain head for each node

**Step 3: Build segment tree on the linearized array**
- Node values placed according to their HLD position
- Segment tree supports point update and range max query

**Step 4: Answer path queries**
- Climb from both endpoints toward LCA
- When nodes are in different chains, query the chain segment and jump to chain head's parent
- When in same chain, do one final segment query

### Visual Example: HLD Construction

```
Tree:                Values:
      1 (val=4)           4
     / \                 / \
    2   3               2   5
   (2) (5)
       / \                 / \
      4   5               2   1
     (2) (1)

Step 1: Subtree sizes
  Node 1: size=5 (heavy child = 3, size=3)
  Node 2: size=1
  Node 3: size=3 (heavy child = 4, size=1... tie, pick 4)
  Node 4: size=1
  Node 5: size=1

Step 2: Chains and positions
  Chain 1: 1 -> 3 -> 4  (positions 0, 1, 2)
  Chain 2: 2            (position 3)
  Chain 3: 5            (position 4)

  Linearized array: [4, 5, 2, 2, 1]  (by position)
                     ^  ^  ^  ^  ^
                     1  3  4  2  5

Step 3: Segment tree on [4, 5, 2, 2, 1]
```

### Dry Run: Query path from node 2 to node 5

```
Path: 2 -> 1 -> 3 -> 5
Values on path: [2, 4, 5, 1]
Expected max: 5

Step 1: Start with a=2, b=5
  head[2]=2, head[5]=5, depth[head[2]]=1, depth[head[5]]=2
  depth[head[5]] > depth[head[2]], so process node 5's chain first

Step 2: Process node 5
  Query segment tree [pos[5], pos[5]] = [4, 4] -> max = 1
  Move b = parent[head[5]] = parent[5] = 3

Step 3: Now a=2, b=3
  head[2]=2, head[3]=1
  Different chains, depth[head[2]]=1, depth[head[3]]=0
  depth[head[2]] > depth[head[3]], process node 2's chain

Step 4: Process node 2
  Query segment tree [pos[2], pos[2]] = [3, 3] -> max = 2
  Move a = parent[head[2]] = parent[2] = 1

Step 5: Now a=1, b=3
  head[1]=1, head[3]=1
  Same chain! Query segment tree [pos[1], pos[3]] = [0, 1] -> max = 5

Step 6: Combine all results: max(1, 2, 5) = 5
```

### Algorithm

1. Build adjacency list from edges
2. DFS to compute parent, depth, subtree size, heavy child
3. Decompose tree: assign chain heads and positions
4. Build segment tree on linearized values
5. For each query:
   - Update: modify segment tree at node's position
   - Path max: climb chains, querying segments, until same chain

### Code (Python)

```python
import sys
from collections import defaultdict

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n, q = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2

    values = [0] + [int(input_data[idx + i]) for i in range(n)]  # 1-indexed
    idx += n

    graph = defaultdict(list)
    for _ in range(n - 1):
        u, v = int(input_data[idx]), int(input_data[idx + 1])
        idx += 2
        graph[u].append(v)
        graph[v].append(u)

    # HLD arrays
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    size = [0] * (n + 1)
    heavy = [0] * (n + 1)  # heavy child (0 if leaf)
    head = [0] * (n + 1)   # chain head
    pos = [0] * (n + 1)    # position in segment tree

    # DFS to compute size and heavy child (iterative)
    stack = [(1, 0, False)]
    while stack:
        node, par, processed = stack.pop()
        if processed:
            size[node] = 1
            max_child_size = 0
            for child in graph[node]:
                if child != par:
                    size[node] += size[child]
                    if size[child] > max_child_size:
                        max_child_size = size[child]
                        heavy[node] = child
        else:
            parent[node] = par
            depth[node] = depth[par] + 1 if par else 0
            stack.append((node, par, True))
            for child in graph[node]:
                if child != par:
                    stack.append((child, node, False))

    # Decompose into chains (iterative)
    current_pos = 0
    stack = [(1, 1)]  # (node, chain_head)
    while stack:
        node, h = stack.pop()
        head[node] = h
        pos[node] = current_pos
        current_pos += 1

        # Add light children first (processed later)
        light_children = []
        for child in graph[node]:
            if child != parent[node] and child != heavy[node]:
                light_children.append(child)

        # Add light children - each starts new chain
        for child in reversed(light_children):
            stack.append((child, child))

        # Add heavy child (processed next, same chain)
        if heavy[node]:
            stack.append((heavy[node], h))

    # Build segment tree
    seg_tree = [0] * (4 * n)
    arr = [0] * n
    for i in range(1, n + 1):
        arr[pos[i]] = values[i]

    def build(node, start, end):
        if start == end:
            seg_tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            build(2 * node, start, mid)
            build(2 * node + 1, mid + 1, end)
            seg_tree[node] = max(seg_tree[2 * node], seg_tree[2 * node + 1])

    def update(node, start, end, idx, val):
        if start == end:
            seg_tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                update(2 * node, start, mid, idx, val)
            else:
                update(2 * node + 1, mid + 1, end, idx, val)
            seg_tree[node] = max(seg_tree[2 * node], seg_tree[2 * node + 1])

    def query(node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return seg_tree[node]
        mid = (start + end) // 2
        return max(query(2 * node, start, mid, l, r),
                   query(2 * node + 1, mid + 1, end, l, r))

    build(1, 0, n - 1)

    def path_max(a, b):
        result = 0
        while head[a] != head[b]:
            if depth[head[a]] < depth[head[b]]:
                a, b = b, a
            result = max(result, query(1, 0, n - 1, pos[head[a]], pos[a]))
            a = parent[head[a]]
        if depth[a] > depth[b]:
            a, b = b, a
        result = max(result, query(1, 0, n - 1, pos[a], pos[b]))
        return result

    results = []
    for _ in range(q):
        query_type = int(input_data[idx])
        if query_type == 1:
            s, x = int(input_data[idx + 1]), int(input_data[idx + 2])
            idx += 3
            update(1, 0, n - 1, pos[s], x)
        else:
            a, b = int(input_data[idx + 1]), int(input_data[idx + 2])
            idx += 3
            results.append(path_max(a, b))

    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;

vector<int> adj[MAXN];
int values[MAXN], parent_node[MAXN], depth[MAXN];
int subtree_size[MAXN], heavy[MAXN], head[MAXN], pos[MAXN];
int seg_tree[4 * MAXN];
int current_pos = 0;

void dfs_size(int node, int par) {
    parent_node[node] = par;
    subtree_size[node] = 1;
    heavy[node] = 0;
    int max_child = 0;
    for (int child : adj[node]) {
        if (child != par) {
            depth[child] = depth[node] + 1;
            dfs_size(child, node);
            subtree_size[node] += subtree_size[child];
            if (subtree_size[child] > max_child) {
                max_child = subtree_size[child];
                heavy[node] = child;
            }
        }
    }
}

void decompose(int node, int h) {
    head[node] = h;
    pos[node] = current_pos++;
    if (heavy[node]) {
        decompose(heavy[node], h);
    }
    for (int child : adj[node]) {
        if (child != parent_node[node] && child != heavy[node]) {
            decompose(child, child);
        }
    }
}

void build(int node, int start, int end, int arr[]) {
    if (start == end) {
        seg_tree[node] = arr[start];
    } else {
        int mid = (start + end) / 2;
        build(2 * node, start, mid, arr);
        build(2 * node + 1, mid + 1, end, arr);
        seg_tree[node] = max(seg_tree[2 * node], seg_tree[2 * node + 1]);
    }
}

void update(int node, int start, int end, int idx, int val) {
    if (start == end) {
        seg_tree[node] = val;
    } else {
        int mid = (start + end) / 2;
        if (idx <= mid) {
            update(2 * node, start, mid, idx, val);
        } else {
            update(2 * node + 1, mid + 1, end, idx, val);
        }
        seg_tree[node] = max(seg_tree[2 * node], seg_tree[2 * node + 1]);
    }
}

int query(int node, int start, int end, int l, int r) {
    if (r < start || end < l) return 0;
    if (l <= start && end <= r) return seg_tree[node];
    int mid = (start + end) / 2;
    return max(query(2 * node, start, mid, l, r),
               query(2 * node + 1, mid + 1, end, l, r));
}

int path_max(int a, int b, int n) {
    int result = 0;
    while (head[a] != head[b]) {
        if (depth[head[a]] < depth[head[b]]) swap(a, b);
        result = max(result, query(1, 0, n - 1, pos[head[a]], pos[a]));
        a = parent_node[head[a]];
    }
    if (depth[a] > depth[b]) swap(a, b);
    result = max(result, query(1, 0, n - 1, pos[a], pos[b]));
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;

    for (int i = 1; i <= n; i++) {
        cin >> values[i];
    }

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    depth[1] = 0;
    dfs_size(1, 0);
    decompose(1, 1);

    int arr[n];
    for (int i = 1; i <= n; i++) {
        arr[pos[i]] = values[i];
    }
    build(1, 0, n - 1, arr);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int s, x;
            cin >> s >> x;
            update(1, 0, n - 1, pos[s], x);
        } else {
            int a, b;
            cin >> a >> b;
            cout << path_max(a, b, n) << "\n";
        }
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log^2 n) | Each query crosses O(log n) chains, each segment query is O(log n) |
| Space | O(n) | Tree arrays and segment tree |

---

## Common Mistakes

### Mistake 1: Wrong Chain Traversal Order

```python
# WRONG - may skip nodes
while head[a] != head[b]:
    if depth[a] < depth[b]:  # Comparing node depth, not chain head depth
        a, b = b, a
    ...
```

**Problem:** We must compare depths of chain heads, not the nodes themselves.
**Fix:** Use `depth[head[a]] < depth[head[b]]` to decide which chain to process.

### Mistake 2: Forgetting Final Same-Chain Query

```python
# WRONG - missing the final segment
while head[a] != head[b]:
    # ... process chains
# Missing: query(pos[a], pos[b]) when same chain!
```

**Problem:** After the loop, a and b are in the same chain but we still need to query that segment.
**Fix:** Always do a final query from pos[a] to pos[b] after the loop.

### Mistake 3: Position Order in Segment Query

```python
# WRONG - positions may be reversed
result = max(result, query(1, 0, n-1, pos[a], pos[b]))
```

**Problem:** If a is deeper than b in the same chain, pos[a] > pos[b].
**Fix:** Ensure a is the shallower node before the final query:
```python
if depth[a] > depth[b]:
    a, b = b, a
result = max(result, query(1, 0, n-1, pos[a], pos[b]))
```

### Mistake 4: Stack Overflow in DFS

```python
# WRONG - recursive DFS on large trees
def dfs(node, par):
    for child in graph[node]:
        if child != par:
            dfs(child, node)  # Stack overflow for n=200000
```

**Problem:** Python's default recursion limit is 1000.
**Fix:** Use iterative DFS or increase recursion limit with `sys.setrecursionlimit()`.

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| Single node | n=1, query 2 1 1 | Return value of node 1 | Path is just one node |
| Linear tree | 1-2-3-...-n chain | All nodes in one chain | Degenerate case, still O(log n) per query |
| Star tree | 1 connected to all others | n-1 chains of length 1 | Many light edges |
| Query after update | Update then query same node | New value | Segment tree reflects update |
| Same node query | Query 2 a a | value[a] | Path contains only one node |

---

## When to Use This Pattern

### Use HLD When:
- You need path queries (max, min, sum, etc.) on a tree
- Point updates or path updates are required
- Query complexity needs to be better than O(n)
- The tree is static (structure doesn't change)

### Don't Use When:
- Only need LCA queries (binary lifting is simpler)
- Tree structure changes dynamically (consider Link-Cut Trees)
- Only querying subtrees (use Euler tour instead)
- Single path query without updates (simple DFS suffices)

### Pattern Recognition Checklist:
- [ ] Path queries on a tree? -> **Consider HLD**
- [ ] Need to support updates? -> **HLD + Segment Tree**
- [ ] Subtree queries only? -> **Euler Tour + Segment Tree**
- [ ] LCA queries only? -> **Binary Lifting**
- [ ] Dynamic tree connectivity? -> **Link-Cut Trees**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Path Queries](https://cses.fi/problemset/task/1138) | Subtree sums with Euler tour |
| [Company Queries I](https://cses.fi/problemset/task/1687) | Binary lifting basics |
| [Company Queries II](https://cses.fi/problemset/task/1688) | LCA with binary lifting |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Subtree Queries](https://cses.fi/problemset/task/1137) | Subtree updates instead of path |
| [Distance Queries](https://cses.fi/problemset/task/1135) | Path length using LCA |
| [Path Queries (SPOJ QTREE)](https://www.spoj.com/problems/QTREE/) | Classic HLD problem |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Vertex Set Path Composite](https://judge.yosupo.jp/problem/vertex_set_path_composite) | Non-commutative operations on paths |
| [Tree Isomorphism](https://cses.fi/problemset/task/1700) | Tree hashing |

---

## Key Takeaways

1. **The Core Idea:** HLD transforms tree paths into O(log n) contiguous segments
2. **Time Optimization:** From O(n) per query to O(log^2 n) per query
3. **Space Trade-off:** O(n) extra arrays for decomposition metadata
4. **Pattern:** Linearize tree structure to enable efficient range queries

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why any path crosses at most O(log n) chains
- [ ] Implement HLD decomposition from scratch
- [ ] Combine HLD with segment trees for path queries
- [ ] Handle both point updates and path queries
- [ ] Debug common issues (wrong chain comparison, missing final query)

---

## Additional Resources

- [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/data_structures/hld.html)
- [CSES Problem Set](https://cses.fi/problemset/)
- [Anudeep's Blog on HLD](https://blog.anudeep2011.com/heavy-light-decomposition/)
