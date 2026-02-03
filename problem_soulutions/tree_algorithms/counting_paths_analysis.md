---
layout: simple
title: "Counting Paths - Tree Algorithms Problem"
permalink: /problem_soulutions/tree_algorithms/counting_paths_analysis
difficulty: Medium
tags: [tree, lca, difference-array, dfs]
---

# Counting Paths

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Difference Array on Tree + LCA |
| **CSES Link** | [https://cses.fi/problemset/task/1136](https://cses.fi/problemset/task/1136) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply difference array technique on trees (not just arrays)
- [ ] Use LCA to decompose tree paths into two segments
- [ ] Efficiently count contributions using subtree aggregation
- [ ] Understand when to use +1/-1 marking instead of direct counting

---

## Problem Statement

**Problem:** Given a tree of n nodes and m paths, count how many paths pass through each node.

**Input:**
- Line 1: Two integers n and m (number of nodes and paths)
- Lines 2 to n: Each line has two integers a and b describing an edge
- Lines n+1 to n+m: Each line has two integers a and b describing a path from a to b

**Output:**
- Print n integers: for each node 1, 2, ..., n, the number of paths containing that node

**Constraints:**
- 1 <= n, m <= 2 x 10^5

### Example

```
Input:
5 3
1 2
2 3
3 4
3 5
1 3
2 5
1 4

Output:
2 3 3 1 1
```

**Explanation:**
- Path 1-3: Goes through nodes 1, 2, 3
- Path 2-5: Goes through nodes 2, 3, 5
- Path 1-4: Goes through nodes 1, 2, 3, 4

Node counts: 1 appears in 2 paths, 2 appears in 3 paths, 3 appears in 3 paths, 4 appears in 1 path, 5 appears in 1 path.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently count path coverage for all nodes without iterating through each path?

The naive approach of marking every node on each path takes O(n) per path, giving O(nm) total, which is too slow. The key insight is that **a tree path can be decomposed using LCA**, and we can use a **difference array technique** to mark paths efficiently.

### Breaking Down the Problem

1. **What are we looking for?** For each node, count how many of the m paths include it.
2. **What information do we have?** Tree structure and m (start, end) path pairs.
3. **What's the relationship between input and output?** Each path from a to b passes through LCA(a,b) and all nodes on both branches.

### The Difference Array Insight

On a 1D array, if we want to add 1 to range [l, r], we do:
- `diff[l] += 1`
- `diff[r+1] -= 1`
- Then prefix sum gives us the actual values

On a tree, for path a -> b with LCA = c and parent of c = p:
- `diff[a] += 1`
- `diff[b] += 1`
- `diff[c] -= 1`
- `diff[p] -= 1` (to cancel the double-counting at LCA)
- Then **subtree sum** (DFS sum from leaves to root) gives us the actual values

---

## Solution 1: Brute Force

### Idea

For each path, traverse from source to destination and increment counters.

### Algorithm

1. Build adjacency list
2. For each path (a, b), find all nodes on the path using DFS/BFS
3. Increment counter for each node on the path

### Code

```python
def solve_brute_force(n, m, edges, paths):
    """
    Brute force: traverse each path and mark nodes.

    Time: O(m * n)
    Space: O(n)
    """
    from collections import defaultdict

    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    count = [0] * (n + 1)

    def find_path(start, end):
        """Find path from start to end using DFS."""
        parent = {start: None}
        stack = [start]

        while stack:
            node = stack.pop()
            if node == end:
                break
            for neighbor in adj[node]:
                if neighbor not in parent:
                    parent[neighbor] = node
                    stack.append(neighbor)

        # Reconstruct path
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        return path

    for a, b in paths:
        path_nodes = find_path(a, b)
        for node in path_nodes:
            count[node] += 1

    return count[1:]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(m * n) | Each path traversal can visit up to n nodes |
| Space | O(n) | Parent dictionary for path finding |

### Why This Works (But Is Slow)

Correctness is guaranteed because we explicitly visit each node on each path. However, with n, m up to 2 x 10^5, this gives up to 4 x 10^10 operations, which is far too slow.

---

## Solution 2: Optimal - Difference Array on Tree

### Key Insight

> **The Trick:** Instead of marking all nodes on a path, mark only the endpoints with +1 and LCA with -1/-1, then aggregate with DFS.

### How Difference Array Works on Trees

For path from `a` to `b` with `LCA(a,b) = c`:

```
       c (LCA)
      / \
     /   \
    ...  ...
   /       \
  a         b
```

The path goes: a -> ... -> c -> ... -> b

We mark:
- `diff[a] += 1` (path starts here)
- `diff[b] += 1` (path ends here)
- `diff[c] -= 1` (LCA counted twice, subtract once)
- `diff[parent[c]] -= 1` (cancel propagation above LCA)

When we DFS and sum up subtrees (bottom-up), each node gets exactly:
- +1 for each path endpoint in its subtree
- -1 for each LCA and parent-of-LCA in its subtree
- Net result = number of paths passing through this node

### Algorithm

1. Build tree and precompute LCA using binary lifting
2. For each path (a, b):
   - Find c = LCA(a, b)
   - Mark: diff[a]++, diff[b]++, diff[c]--, diff[parent[c]]--
3. DFS to compute subtree sums (this gives final answer)

### Dry Run Example

Let's trace through with the example:
```
Tree:     1
          |
          2
          |
          3
         / \
        4   5

Paths: (1,3), (2,5), (1,4)
```

**Step 1: Build LCA structure**
- parent[1] = 0 (root, use 0 as sentinel)
- parent[2] = 1
- parent[3] = 2
- parent[4] = 3
- parent[5] = 3

**Step 2: Process each path**

Path (1, 3): LCA = 1
```
diff[1] += 1 -> diff[1] = 1
diff[3] += 1 -> diff[3] = 1
diff[1] -= 1 -> diff[1] = 0
diff[0] -= 1 -> (sentinel, ignored)
```

Path (2, 5): LCA = 2
```
diff[2] += 1 -> diff[2] = 1
diff[5] += 1 -> diff[5] = 1
diff[2] -= 1 -> diff[2] = 0
diff[1] -= 1 -> diff[1] = -1
```

Path (1, 4): LCA = 1
```
diff[1] += 1 -> diff[1] = 0
diff[4] += 1 -> diff[4] = 1
diff[1] -= 1 -> diff[1] = -1
diff[0] -= 1 -> (sentinel, ignored)
```

**After all paths:**
```
diff = [_, -1, 0, 1, 1, 1]  (index 0 is sentinel)
       node: 1  2  3  4  5
```

**Step 3: DFS to compute subtree sums (post-order)**

Process leaves first, then propagate up:
```
Node 4: sum[4] = diff[4] = 1
Node 5: sum[5] = diff[5] = 1
Node 3: sum[3] = diff[3] + sum[4] + sum[5] = 1 + 1 + 1 = 3
Node 2: sum[2] = diff[2] + sum[3] = 0 + 3 = 3
Node 1: sum[1] = diff[1] + sum[2] = -1 + 3 = 2
```

**Final answer:** `[2, 3, 3, 1, 1]`

### Visual Diagram

```
Path 1-3:     Path 2-5:     Path 1-4:
    1*            1             1*
    |             |             |
    2*            2*            2*
    |             |             |
    3*            3*            3*
   / \           / \           / \
  4   5         4   5*        4*  5

* = nodes on path

After DFS aggregation:
    1(2)          <- 2 paths pass through
    |
    2(3)          <- 3 paths pass through
    |
    3(3)          <- 3 paths pass through
   / \
4(1)  5(1)        <- 1 path each
```

### Code

**Python Solution:**

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve(n, m, edges, paths):
    """
    Optimal solution using difference array on tree.

    Time: O((n + m) log n)
    Space: O(n log n) for LCA preprocessing
    """
    # Build adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # LCA preprocessing with binary lifting
    LOG = 18  # log2(2 * 10^5) ~ 18
    parent = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)

    # DFS to compute parent and depth
    def dfs_init(node, par, d):
        parent[0][node] = par
        depth[node] = d
        for neighbor in adj[node]:
            if neighbor != par:
                dfs_init(neighbor, node, d + 1)

    dfs_init(1, 0, 0)

    # Build sparse table for LCA
    for k in range(1, LOG):
        for v in range(1, n + 1):
            parent[k][v] = parent[k-1][parent[k-1][v]]

    def lca(u, v):
        # Bring u and v to same depth
        if depth[u] < depth[v]:
            u, v = v, u

        diff = depth[u] - depth[v]
        for k in range(LOG):
            if (diff >> k) & 1:
                u = parent[k][u]

        if u == v:
            return u

        # Binary search for LCA
        for k in range(LOG - 1, -1, -1):
            if parent[k][u] != parent[k][v]:
                u = parent[k][u]
                v = parent[k][v]

        return parent[0][u]

    # Difference array
    diff = [0] * (n + 1)

    for a, b in paths:
        c = lca(a, b)
        diff[a] += 1
        diff[b] += 1
        diff[c] -= 1
        if parent[0][c] != 0:
            diff[parent[0][c]] -= 1

    # DFS to compute subtree sums
    result = [0] * (n + 1)

    def dfs_sum(node, par):
        result[node] = diff[node]
        for neighbor in adj[node]:
            if neighbor != par:
                dfs_sum(neighbor, node)
                result[node] += result[neighbor]

    dfs_sum(1, 0)

    return result[1:]


def main():
    input_data = sys.stdin.read().split()
    idx = 0

    n, m = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2

    edges = []
    for _ in range(n - 1):
        u, v = int(input_data[idx]), int(input_data[idx + 1])
        edges.append((u, v))
        idx += 2

    paths = []
    for _ in range(m):
        a, b = int(input_data[idx]), int(input_data[idx + 1])
        paths.append((a, b))
        idx += 2

    result = solve(n, m, edges, paths)
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    main()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
const int LOG = 18;

vector<int> adj[MAXN];
int parent[LOG][MAXN];
int depth[MAXN];
int diff[MAXN];
long long result[MAXN];
int n, m;

void dfs_init(int node, int par, int d) {
    parent[0][node] = par;
    depth[node] = d;
    for (int neighbor : adj[node]) {
        if (neighbor != par) {
            dfs_init(neighbor, node, d + 1);
        }
    }
}

void build_lca() {
    for (int k = 1; k < LOG; k++) {
        for (int v = 1; v <= n; v++) {
            parent[k][v] = parent[k-1][parent[k-1][v]];
        }
    }
}

int lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v);

    int diff_depth = depth[u] - depth[v];
    for (int k = 0; k < LOG; k++) {
        if ((diff_depth >> k) & 1) {
            u = parent[k][u];
        }
    }

    if (u == v) return u;

    for (int k = LOG - 1; k >= 0; k--) {
        if (parent[k][u] != parent[k][v]) {
            u = parent[k][u];
            v = parent[k][v];
        }
    }

    return parent[0][u];
}

void dfs_sum(int node, int par) {
    result[node] = diff[node];
    for (int neighbor : adj[node]) {
        if (neighbor != par) {
            dfs_sum(neighbor, node);
            result[node] += result[neighbor];
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> n >> m;

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // Initialize LCA
    dfs_init(1, 0, 0);
    build_lca();

    // Process paths
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        int c = lca(a, b);

        diff[a]++;
        diff[b]++;
        diff[c]--;
        if (parent[0][c] != 0) {
            diff[parent[0][c]]--;
        }
    }

    // Compute subtree sums
    dfs_sum(1, 0);

    // Output
    for (int i = 1; i <= n; i++) {
        cout << result[i];
        if (i < n) cout << " ";
    }
    cout << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + m) log n) | LCA preprocessing O(n log n), each query O(log n) |
| Space | O(n log n) | Binary lifting table |

---

## Common Mistakes

### Mistake 1: Forgetting to subtract at parent of LCA

```python
# WRONG - Double counts nodes above LCA
diff[a] += 1
diff[b] += 1
diff[c] -= 1
# Missing: diff[parent[c]] -= 1
```

**Problem:** Without subtracting at parent of LCA, the contribution propagates incorrectly above the LCA.

**Fix:** Always subtract 1 at parent[LCA], handling the root case (parent = 0).

### Mistake 2: Wrong LCA for same-node query

```python
# WRONG - If a == b, LCA logic might fail
def lca(u, v):
    if u == v:
        return u  # Must handle this case!
    # ... rest of LCA logic
```

**Problem:** When start and end are the same node, the path is just that node.

**Fix:** Check if u == v before the main LCA computation.

### Mistake 3: Incorrect subtree sum direction

```python
# WRONG - Top-down traversal
def dfs_wrong(node, par):
    for neighbor in adj[node]:
        if neighbor != par:
            result[neighbor] += result[node]  # Wrong direction!
            dfs_wrong(neighbor, node)
```

**Problem:** Difference array on tree requires bottom-up aggregation.

**Fix:** Sum children's results into parent (post-order).

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| Single node | n=1, m=1, path (1,1) | Output: 1 | Path through same node |
| Linear tree | Chain 1-2-3-...-n | Works correctly | Tests deep recursion |
| Star tree | All edges from node 1 | Center has all paths | Tests high-degree node |
| No paths | m=0 | All zeros | No paths to count |
| All paths same | m paths all (a,b) | Counts multiply | Same path adds up |

---

## When to Use This Pattern

### Use This Approach When:
- You need to count/sum contributions along tree paths
- Multiple queries on the same tree structure
- Path operations that can be decomposed at LCA
- Problems involving "add X to path from a to b"

### Don't Use When:
- Tree structure changes between queries (use Link-Cut Tree)
- You need actual path enumeration (use explicit traversal)
- Single query on small tree (brute force is simpler)

### Pattern Recognition Checklist:
- [ ] "Count paths through each node" -> **Difference array on tree**
- [ ] "Add value to all nodes on path" -> **Difference array on tree**
- [ ] "Sum of values on path from a to b" -> **LCA + prefix sums**
- [ ] Tree + batch path operations -> **Consider difference array**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Subordinates](https://cses.fi/problemset/task/1674) | Basic subtree counting with DFS |
| [Tree Distances I](https://cses.fi/problemset/task/1132) | DFS on trees, max depth |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Path Queries](https://cses.fi/problemset/task/1138) | Uses similar path decomposition |
| [Distance Queries](https://cses.fi/problemset/task/1135) | LCA for path length |
| [Path Queries II](https://cses.fi/problemset/task/2134) | Path queries with updates |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Tree Isomorphism I](https://cses.fi/problemset/task/1700) | Tree hashing |
| [Centroid Decomposition](https://cses.fi/problemset/task/2079) | Advanced tree decomposition |

---

## Key Takeaways

1. **The Core Idea:** Decompose tree paths at LCA and use difference array with subtree aggregation.
2. **Time Optimization:** From O(nm) brute force to O((n+m) log n) with LCA preprocessing.
3. **Space Trade-off:** O(n log n) space for binary lifting enables O(log n) LCA queries.
4. **Pattern:** This is the "difference array on tree" pattern, analogous to range updates on arrays.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement LCA using binary lifting from scratch
- [ ] Explain why we subtract at both LCA and parent of LCA
- [ ] Trace through the difference array + DFS sum process
- [ ] Identify similar problems that use this technique

---

## Additional Resources

- [CP-Algorithms: LCA with Binary Lifting](https://cp-algorithms.com/graph/lca_binary_lifting.html)
- [CSES Counting Paths](https://cses.fi/problemset/task/1136) - Count paths through edges
- [USACO Guide: Tree Algorithms](https://usaco.guide/gold/tree-euler)
