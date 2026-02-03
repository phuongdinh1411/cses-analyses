---
layout: simple
title: "DSU on Trees (Small-to-Large Merging) - Tree Algorithms"
permalink: /problem_soulutions/tree_algorithms/dsu_on_tree_analysis
difficulty: Hard
tags: [tree, dsu, small-to-large, sack, subtree-queries]
---

# DSU on Trees (Small-to-Large Merging / Sack)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Tree Algorithms |
| **Time Complexity** | O(n log n) |
| **Key Technique** | Small-to-Large Merging (Heavy-Light Decomposition insight) |

### Concept Explanation

**DSU on Trees** (also called **Sack** - Small-to-large Algorithm for Counting on Trees) is a technique for efficiently answering subtree queries. The core idea is to process subtrees by keeping the data from the "heavy child" (largest subtree) and re-inserting data from smaller children.

This achieves O(n log n) total time because each node is inserted at most O(log n) times - once for each ancestor where it belongs to a light (non-heavy) subtree.

### Learning Goals

After studying this technique, you will be able to:
- [ ] Identify problems solvable with small-to-large merging on trees
- [ ] Implement heavy child selection and subtree size calculation
- [ ] Apply DSU on Trees to count distinct values in subtrees
- [ ] Understand why the technique achieves O(n log n) complexity
- [ ] Choose between DSU on Trees vs. other techniques (Mo's, Euler tour)

---

## Problem Statement (Distinct Colors - CSES)

**Problem:** Given a rooted tree where each node has a color, for each node, find the number of distinct colors in its subtree.

**Input:**
- Line 1: n (number of nodes)
- Line 2: c_1, c_2, ..., c_n (color of each node)
- Lines 3 to n: edges (parent-child relationships)

**Output:**
- n integers: the count of distinct colors in each node's subtree

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= c_i <= 10^9

### Example

```
Input:
5
2 3 2 3 1
1 2
1 3
3 4
3 5

Output:
3 1 3 1 1
```

**Tree Structure:**
```
        1(color=2)
       / \
      2   3(color=2)
     (3)  /\
         4  5
        (3)(1)
```

---

## Intuition: The "Keep Heavy Child" Optimization

### Pattern Recognition

> **Key Question:** Why can't we just merge all children's data naively?

Naive merging would give O(n^2) in the worst case (e.g., a chain). The insight is that if we always keep the largest child's data and only re-insert smaller children, each node gets re-inserted at most O(log n) times.

### Why O(n log n)?

Consider any node v. It gets "cleared and re-added" only when it's in a light subtree of some ancestor. Since the heavy child always has > half the subtree size, the light subtrees decrease by at least half at each level. Thus, each node is in at most O(log n) light subtrees.

### The Algorithm in Three Sentences

1. **DFS bottom-up**: Process children before parent
2. **Keep heavy child data**: Don't clear the data from the largest subtree
3. **Re-add light children**: Insert all nodes from smaller subtrees

---

## Solution: DSU on Trees

### Algorithm Steps

1. **Calculate subtree sizes** with a DFS
2. **Identify heavy child** for each node (child with largest subtree)
3. **DFS with merging**:
   - Recursively solve for light children (clear their data after)
   - Recursively solve for heavy child (keep its data)
   - Add current node to the data structure
   - Add all light children's subtrees back
   - Record answer for current node

### Dry Run Example

Using the tree from the example:

```
Tree:       1(c=2)
           / \
          2   3(c=2)
         (c=3) /\
              4  5
             (3)(1)

Step 1: Calculate subtree sizes
  Node 1: size = 5 (heavy child = 3, size 3)
  Node 2: size = 1
  Node 3: size = 3 (heavy child = 4 or 5, both size 1)
  Node 4: size = 1
  Node 5: size = 1

Step 2: DFS from node 1

Process node 2 (leaf):
  cnt = {3: 1}, distinct = 1
  Answer[2] = 1
  Clear (light child of 1)

Process node 4 (leaf):
  cnt = {3: 1}, distinct = 1
  Answer[4] = 1
  Clear (light child of 3)

Process node 5 (leaf):
  cnt = {1: 1}, distinct = 1
  Answer[5] = 1
  [Keep - heavy child of 3]

Process node 3:
  Keep data from heavy child (5): cnt = {1: 1}
  Add node 3's color (2): cnt = {1: 1, 2: 1}, distinct = 2
  Re-add light child 4: cnt = {1: 1, 2: 1, 3: 1}, distinct = 3
  Answer[3] = 3
  [Keep - heavy child of 1]

Process node 1:
  Keep data from heavy child (3): cnt = {1: 1, 2: 1, 3: 1}
  Add node 1's color (2): cnt = {1: 1, 2: 2, 3: 1}, distinct = 3
  Re-add light child 2's subtree: cnt = {1: 1, 2: 2, 3: 2}, distinct = 3
  Answer[1] = 3

Final Answer: [3, 1, 3, 1, 1]
```

### Visual Diagram

```
Processing Order (Heavy edges shown with =):
        1
       / \\
      2   3    (3 is heavy child of 1)
         //\
        4  5   (5 is heavy child of 3, arbitrary tie-break)

Legend: // = heavy edge, / = light edge

Nodes visited multiple times:
  Node 2: 2 times (own + re-add to 1)
  Node 4: 2 times (own + re-add to 3)
  Node 5: 1 time  (heavy path to root)
  Node 3: 1 time  (heavy path to root)
  Node 1: 1 time  (root)
```

---

## Code Solutions

### Python Solution

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
    n = int(input())
    colors = [0] + list(map(int, input().split()))  # 1-indexed

    adj = defaultdict(list)
    for _ in range(n - 1):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)

    # Build rooted tree and calculate subtree sizes
    subtree_size = [0] * (n + 1)
    parent = [0] * (n + 1)
    order = []  # post-order for bottom-up processing

    # BFS to establish parent relationships and order
    from collections import deque
    visited = [False] * (n + 1)
    queue = deque([1])
    visited[1] = True
    bfs_order = []

    while queue:
        node = queue.popleft()
        bfs_order.append(node)
        for child in adj[node]:
            if not visited[child]:
                visited[child] = True
                parent[child] = node
                queue.append(child)

    # Calculate subtree sizes (reverse BFS order)
    children = defaultdict(list)
    for node in bfs_order[1:]:
        children[parent[node]].append(node)

    for node in reversed(bfs_order):
        subtree_size[node] = 1
        for child in children[node]:
            subtree_size[node] += subtree_size[child]

    # Find heavy child for each node
    heavy = [0] * (n + 1)
    for node in range(1, n + 1):
        if children[node]:
            heavy[node] = max(children[node], key=lambda x: subtree_size[x])

    # DSU on tree
    cnt = defaultdict(int)  # color -> count
    distinct = [0]  # mutable counter
    answer = [0] * (n + 1)

    def add(node):
        """Add a node's color to the count."""
        if cnt[colors[node]] == 0:
            distinct[0] += 1
        cnt[colors[node]] += 1

    def remove(node):
        """Remove a node's color from the count."""
        cnt[colors[node]] -= 1
        if cnt[colors[node]] == 0:
            distinct[0] -= 1

    def add_subtree(node):
        """Add all nodes in subtree to count."""
        add(node)
        for child in children[node]:
            add_subtree(child)

    def remove_subtree(node):
        """Remove all nodes in subtree from count."""
        remove(node)
        for child in children[node]:
            remove_subtree(child)

    def dfs(node, keep):
        """
        Process node's subtree.
        keep: whether to keep this subtree's data after processing
        """
        # Process light children first (clear after)
        for child in children[node]:
            if child != heavy[node]:
                dfs(child, keep=False)

        # Process heavy child (keep its data)
        if heavy[node]:
            dfs(heavy[node], keep=True)

        # Add current node
        add(node)

        # Re-add light children's subtrees
        for child in children[node]:
            if child != heavy[node]:
                add_subtree(child)

        # Record answer
        answer[node] = distinct[0]

        # Clear if not keeping
        if not keep:
            remove_subtree(node)

    dfs(1, keep=False)
    print(' '.join(map(str, answer[1:])))

solve()
```

### C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
vector<int> adj[MAXN];
int color[MAXN], subtree_size[MAXN], heavy[MAXN];
int answer[MAXN];
map<int, int> cnt;  // color -> count
int distinct_count = 0;

void calc_size(int u, int p) {
    subtree_size[u] = 1;
    int max_child_size = 0;
    for (int v : adj[u]) {
        if (v != p) {
            calc_size(v, u);
            subtree_size[u] += subtree_size[v];
            if (subtree_size[v] > max_child_size) {
                max_child_size = subtree_size[v];
                heavy[u] = v;
            }
        }
    }
}

void add(int c) {
    if (cnt[c] == 0) distinct_count++;
    cnt[c]++;
}

void remove(int c) {
    cnt[c]--;
    if (cnt[c] == 0) distinct_count--;
}

void add_subtree(int u, int p) {
    add(color[u]);
    for (int v : adj[u]) {
        if (v != p) add_subtree(v, u);
    }
}

void remove_subtree(int u, int p) {
    remove(color[u]);
    for (int v : adj[u]) {
        if (v != p) remove_subtree(v, u);
    }
}

void dfs(int u, int p, bool keep) {
    // Process light children first
    for (int v : adj[u]) {
        if (v != p && v != heavy[u]) {
            dfs(v, u, false);
        }
    }

    // Process heavy child (keep data)
    if (heavy[u]) {
        dfs(heavy[u], u, true);
    }

    // Add current node
    add(color[u]);

    // Re-add light children
    for (int v : adj[u]) {
        if (v != p && v != heavy[u]) {
            add_subtree(v, u);
        }
    }

    answer[u] = distinct_count;

    // Clear if not keeping
    if (!keep) {
        remove_subtree(u, p);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    for (int i = 1; i <= n; i++) {
        cin >> color[i];
    }

    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    calc_size(1, 0);
    dfs(1, 0, false);

    for (int i = 1; i <= n; i++) {
        cout << answer[i] << " \n"[i == n];
    }

    return 0;
}
```

### Complexity Analysis

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Each node added/removed O(log n) times |
| Space | O(n) | Tree structure + color count map |

---

## Common Mistakes

### Mistake 1: Clearing Heavy Child Data

```cpp
// WRONG: Clearing all children after processing
for (int v : children[u]) {
    dfs(v, u, false);  // Clears ALL children!
}
```

**Problem:** Defeats the purpose - we need to KEEP heavy child data.
**Fix:** Only pass `keep=false` to light children.

### Mistake 2: Wrong Heavy Child Selection

```cpp
// WRONG: Selecting heavy child BEFORE calculating subtree sizes
heavy[u] = adj[u][0];  // Arbitrary, not based on size

// CORRECT: Select after size calculation
for (int v : adj[u]) {
    if (subtree_size[v] > subtree_size[heavy[u]]) {
        heavy[u] = v;
    }
}
```

### Mistake 3: Forgetting to Add Current Node

```cpp
// WRONG: Missing add(color[u])
void dfs(int u, int p, bool keep) {
    // Process children...
    answer[u] = distinct_count;  // Current node not counted!
}
```

### Mistake 4: Adding Heavy Child Twice

```cpp
// WRONG: Re-adding heavy child in the loop
for (int v : adj[u]) {
    if (v != p) {  // Should also exclude heavy[u]!
        add_subtree(v, u);
    }
}
```

---

## Edge Cases

| Case | Input | Consideration |
|------|-------|---------------|
| Single node | n=1 | Answer is 1 |
| Chain tree | Linear path | Tests O(n log n) vs O(n^2) |
| Star tree | All nodes connected to root | All children are light except one |
| All same color | c_i = c for all i | Distinct count = 1 for all nodes |
| All different colors | c_i unique | Distinct = subtree_size |
| Large color values | c_i up to 10^9 | Use map, not array |

---

## When to Use DSU on Trees

### Use This Approach When:
- You need to answer queries about subtrees
- The query involves counting/aggregating over subtree elements
- Updates are not required (offline queries)
- Each query is independent (no path queries)

**Classic Applications:**
- Count distinct values in subtree
- Find most frequent element in subtree
- Sum of elements matching criteria in subtree

### Don't Use When:
- Queries involve paths (use HLD or LCA techniques)
- Online updates required (use Euler tour + segment tree)
- Need to answer queries in specific order (use Mo's algorithm)

### Decision Flowchart

```
Subtree query problem?
    |
    +-- Yes --> Updates needed?
    |               |
    |               +-- Yes --> Euler Tour + Segment Tree
    |               |
    |               +-- No --> DSU on Trees (O(n log n))
    |
    +-- No (Path query) --> Heavy-Light Decomposition
```

---

## Comparison with Other Techniques

| Technique | Time | Space | Updates | Best For |
|-----------|------|-------|---------|----------|
| **DSU on Trees** | O(n log n) | O(n) | No | Subtree aggregation queries |
| **Euler Tour + Seg Tree** | O(n log n) | O(n) | Yes | Subtree with updates |
| **Mo's on Trees** | O((n+q) sqrt(n)) | O(n) | No | Path queries, offline |
| **HLD** | O(n log^2 n) | O(n) | Yes | Path queries with updates |

### When Each Excels

**DSU on Trees:** Simple subtree queries, no updates, memory-efficient
**Euler Tour:** Need point updates or range sum on subtrees
**Mo's Algorithm:** Path queries with add/remove operations
**HLD:** Path updates and queries, online processing

---

## Related CSES Problems

### Direct Applications
| Problem | Technique Used |
|---------|----------------|
| [Distinct Colors](https://cses.fi/problemset/task/1139) | DSU on Trees (this analysis) |

### Related Tree Problems
| Problem | Key Difference |
|---------|----------------|
| [Subtree Queries](https://cses.fi/problemset/task/1137) | Euler tour + BIT (with updates) |
| [Path Queries](https://cses.fi/problemset/task/1138) | Euler tour + segment tree |
| [Tree Distances I](https://cses.fi/problemset/task/1132) | Two DFS for diameter |

---

## Key Takeaways

1. **Core Idea:** Keep data from the largest (heavy) child subtree; only re-add smaller subtrees
2. **Complexity Insight:** Each node is in O(log n) light subtrees, giving O(n log n) total
3. **Implementation Key:** Process light children first (clearing), then heavy child (keeping)
4. **Pattern:** Useful for subtree aggregation queries without updates

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why each node is added at most O(log n) times
- [ ] Implement subtree size calculation and heavy child selection
- [ ] Solve Distinct Colors without looking at the solution
- [ ] Identify when DSU on Trees is better than Euler Tour approach
- [ ] Adapt the technique for different subtree query types

---

## Additional Resources

- [CP-Algorithms: DSU on Trees](https://cp-algorithms.com/data_structures/dsu_on_tree.html)
- [Codeforces Blog: Sack (DSU on Trees)](https://codeforces.com/blog/entry/44351)
- [CSES Distinct Colors](https://cses.fi/problemset/task/1139) - DSU on tree application
