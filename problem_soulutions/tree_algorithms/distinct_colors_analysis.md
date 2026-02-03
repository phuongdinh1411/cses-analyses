---
layout: simple
title: "Distinct Colors - Tree Algorithms Problem"
permalink: /problem_soulutions/tree_algorithms/distinct_colors_analysis
difficulty: Medium
tags: [tree, dfs, small-to-large-merging, dsu-on-tree, set]
prerequisites: [tree_traversal, dfs_basics]
---

# Distinct Colors

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Small-to-Large Merging (DSU on Tree) |
| **CSES Link** | [Distinct Colors](https://cses.fi/problemset/task/1139) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply small-to-large merging technique for efficient set operations on trees
- [ ] Understand why merging smaller sets into larger sets gives O(n log n) complexity
- [ ] Implement DSU on tree pattern for subtree aggregation problems
- [ ] Recognize when set merging problems can be optimized with this technique

---

## Problem Statement

**Problem:** Given a tree with n nodes where each node has a color, find the number of distinct colors in each node's subtree (including the node itself).

**Input:**
- Line 1: n (number of nodes)
- Line 2: n space-separated integers - colors of nodes 1 to n
- Next n-1 lines: edges (u, v) defining the tree

**Output:**
- n space-separated integers: distinct color count for each node's subtree

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= color[i] <= 10^9

### Example

```
Input:
5
2 3 2 5 3
1 2
1 3
3 4
3 5

Output:
3 1 3 1 1
```

**Explanation:**

```
Tree Structure (node: color):
       1(2)
      /    \
    2(3)   3(2)
          /    \
        4(5)   5(3)

Subtree Analysis:
- Node 1: subtree contains all 5 nodes
  colors = {2, 3, 2, 5, 3} -> distinct = {2, 3, 5} -> count = 3
- Node 2: subtree = {2} only (leaf node)
  colors = {3} -> distinct = {3} -> count = 1
- Node 3: subtree = {3, 4, 5}
  colors = {2, 5, 3} -> distinct = {2, 3, 5} -> count = 3
- Node 4: subtree = {4} only (leaf node)
  colors = {5} -> distinct = {5} -> count = 1
- Node 5: subtree = {5} only (leaf node)
  colors = {3} -> distinct = {3} -> count = 1
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently count distinct colors in every subtree without recomputing from scratch?

The naive approach of running DFS from each node takes O(n^2) time. The key insight is that when we finish processing a subtree, we already have all its colors collected - we should reuse this information for the parent.

### Breaking Down the Problem

1. **What are we looking for?** Distinct color count in each subtree
2. **What information do we have?** Tree structure and node colors
3. **What's the relationship?** Parent's distinct colors = union of all children's distinct colors + parent's own color

### The Small-to-Large Insight

When merging sets, always merge the **smaller set into the larger set**. This ensures each element is moved at most O(log n) times across all operations.

**Why O(log n)?** Each time an element is moved, the set it joins is at least twice as large as its previous set. So an element can be moved at most log2(n) times before the set has size n.

---

## Solution 1: Brute Force

### Idea

For each node, perform DFS to collect all colors in its subtree and count distinct colors.

### Algorithm

1. Build adjacency list from edges
2. For each node, run DFS to collect all colors in subtree
3. Use a set to count distinct colors

### Code

```python
def solve_brute_force(n, colors, edges):
    """
    Brute force: DFS from each node.

    Time: O(n^2)
    Space: O(n)
    """
    from collections import defaultdict

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    def collect_colors(node, parent):
        result = {colors[node - 1]}
        for child in graph[node]:
            if child != parent:
                result.update(collect_colors(child, node))
        return result

    # For each node, collect subtree colors
    result = []
    for node in range(1, n + 1):
        subtree_colors = collect_colors(node, -1)
        result.append(len(subtree_colors))

    return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | DFS from each of n nodes, each DFS is O(n) |
| Space | O(n) | Recursion stack and color set |

### Why This Works (But Is Slow)

Each DFS correctly collects all colors but we're redoing work. The subtree of node 1 includes all other subtrees - we're computing overlapping information repeatedly.

---

## Solution 2: Optimal - Small-to-Large Merging

### Key Insight

> **The Trick:** Process children first, then merge their color sets into the parent. Always merge smaller sets into larger sets to minimize total operations.

### Why Small-to-Large Works

Consider what happens when we merge sets:
- If we always merge smaller into larger, each element can only be in a set that doubles in size
- An element starts in a set of size 1, and the maximum size is n
- So each element is moved at most log2(n) times
- Total operations: O(n log n)

### Algorithm

1. Build adjacency list
2. DFS from root (node 1), processing children before parent (post-order)
3. For each node:
   - Start with a set containing only its own color
   - Get color sets from all children
   - Merge all sets, always merging smaller into larger
   - Record the distinct count
4. Return the color set to parent for further merging

### Dry Run Example

```
Input: n=5, colors=[2,3,2,5,3], edges=[(1,2),(1,3),(3,4),(3,5)]

Tree:
       1(2)
      /    \
    2(3)   3(2)
          /    \
        4(5)   5(3)

DFS Execution (post-order):

Step 1: Visit node 2 (leaf)
  - Initialize: set_2 = {3}
  - No children to merge
  - result[2] = 1
  - Return {3} to parent

Step 2: Visit node 4 (leaf)
  - Initialize: set_4 = {5}
  - No children to merge
  - result[4] = 1
  - Return {5} to parent

Step 3: Visit node 5 (leaf)
  - Initialize: set_5 = {3}
  - No children to merge
  - result[5] = 1
  - Return {3} to parent

Step 4: Visit node 3
  - Initialize: set_3 = {2}
  - Children: 4 returns {5}, 5 returns {3}
  - Merge {5} into {2}: set_3 = {2,5}
  - Merge {3} into {2,5}: set_3 = {2,5,3}
  - result[3] = 3
  - Return {2,5,3} to parent

Step 5: Visit node 1
  - Initialize: set_1 = {2}
  - Children: 2 returns {3}, 3 returns {2,5,3}
  - Compare sizes: |{3}|=1, |{2}|=1, |{2,5,3}|=3
  - Merge {2} into {2,5,3}: set_1 = {2,5,3} (2 already present)
  - Merge {3} into {2,5,3}: set_1 = {2,5,3} (3 already present)
  - result[1] = 3
  - Done!

Final answer: [3, 1, 3, 1, 1]
```

### Visual Diagram

```
Processing Order (bottom-up):

       1(2)          Step 5: Merge all -> {2,3,5} = 3
      /    \
    2(3)   3(2)      Step 1: {3}=1    Step 4: {2,3,5}=3
          /    \
        4(5)   5(3)  Step 2: {5}=1    Step 3: {3}=1

Merging at Node 3:
  {2} <- {5} <- {3}

  {2}     : size 1
  + {5}   : {2,5}, size 2
  + {3}   : {2,5,3}, size 3
```

### Code (Python)

```python
import sys
from collections import defaultdict

def solve(n, colors, edges):
    """
    Small-to-large merging solution.

    Time: O(n log n)
    Space: O(n)
    """
    sys.setrecursionlimit(300000)

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    result = [0] * (n + 1)

    def dfs(node, parent):
        # Start with current node's color
        color_set = {colors[node - 1]}

        for child in graph[node]:
            if child != parent:
                child_set = dfs(child, node)

                # Small-to-large: always merge smaller into larger
                if len(color_set) < len(child_set):
                    color_set, child_set = child_set, color_set

                color_set.update(child_set)

        result[node] = len(color_set)
        return color_set

    dfs(1, -1)
    return result[1:]


def main():
    input_data = sys.stdin.read().split()
    idx = 0

    n = int(input_data[idx])
    idx += 1

    colors = []
    for i in range(n):
        colors.append(int(input_data[idx]))
        idx += 1

    edges = []
    for _ in range(n - 1):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        edges.append((u, v))
        idx += 2

    result = solve(n, colors, edges)
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    main()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> colors;
vector<vector<int>> adj;
vector<int> result;

// Each node owns a set, we track which set belongs to which node
vector<set<int>> color_sets;

void dfs(int node, int parent) {
    color_sets[node].insert(colors[node]);

    for (int child : adj[node]) {
        if (child != parent) {
            dfs(child, node);

            // Small-to-large merging
            if (color_sets[node].size() < color_sets[child].size()) {
                swap(color_sets[node], color_sets[child]);
            }

            // Merge smaller into larger
            for (int color : color_sets[child]) {
                color_sets[node].insert(color);
            }
            color_sets[child].clear();  // Free memory
        }
    }

    result[node] = color_sets[node].size();
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;

    colors.resize(n + 1);
    adj.resize(n + 1);
    result.resize(n + 1);
    color_sets.resize(n + 1);

    for (int i = 1; i <= n; i++) {
        cin >> colors[i];
    }

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    dfs(1, 0);

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
| Time | O(n log n) | Each element moved O(log n) times during merges |
| Space | O(n) | Total elements across all sets is O(n) |

---

## Common Mistakes

### Mistake 1: Merging Large into Small

```python
# WRONG - O(n^2) in worst case
for child in children:
    child_set = dfs(child, node)
    child_set.update(color_set)  # Merging large into small!
    color_set = child_set
```

**Problem:** If we merge the parent's (larger) set into child's (smaller) set, we lose the O(n log n) guarantee.

**Fix:** Always check sizes and merge the smaller set into the larger one.

### Mistake 2: Not Handling 1-indexed vs 0-indexed

```python
# WRONG - colors array is 0-indexed
color_set = {colors[node]}  # node is 1-indexed!

# CORRECT
color_set = {colors[node - 1]}  # Adjust for 0-indexed array
```

### Mistake 3: Stack Overflow on Deep Trees

```python
# WRONG - default recursion limit is ~1000 in Python
def dfs(node, parent):
    ...

# CORRECT - increase limit for large inputs
import sys
sys.setrecursionlimit(300000)
```

### Mistake 4: Not Clearing Child Sets (C++)

```cpp
// WRONG - memory builds up
for (int color : color_sets[child]) {
    color_sets[node].insert(color);
}
// Child set still holds data

// CORRECT - free memory after merge
for (int color : color_sets[child]) {
    color_sets[node].insert(color);
}
color_sets[child].clear();  // Release memory
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n=1, colors=[5] | 1 | Only one node with one color |
| All same color | n=3, colors=[1,1,1] | 1 1 1 | Every subtree has just color 1 |
| All different colors | n=3, colors=[1,2,3] | 3 1 1 | Root sees all, leaves see 1 |
| Linear tree (chain) | 1-2-3-4-5 | n n-1 ... 1 | Each node sees colors below |
| Star graph | Center connected to all | n 1 1 ... 1 | Center sees all, leaves see 1 |
| Large color values | colors up to 10^9 | - | Use set, not array for counting |

---

## When to Use This Pattern

### Use Small-to-Large Merging When:
- You need to aggregate information from subtrees to parents
- The aggregation involves set union or similar merge operations
- Naive merging would be O(n^2) due to repeated insertions

### Don't Use When:
- You can use Euler tour + data structures (sometimes faster in practice)
- The problem asks for specific queries (consider Heavy-Light Decomposition)
- Simple DFS with counting suffices (no set operations needed)

### Pattern Recognition Checklist:
- [ ] Computing something for each subtree? -> Consider tree DP
- [ ] Merging sets or collections from children? -> Consider small-to-large
- [ ] Need O(n log n) instead of O(n^2)? -> Small-to-large is the key
- [ ] Each element appears in exactly one set at any time? -> Good fit

### Related Techniques
- **DSU on Tree (Sack)**: Similar idea, but keeps heavy child's data structure
- **Heavy-Light Decomposition**: For path queries
- **Centroid Decomposition**: For distance-related queries

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subordinates (CSES)](https://cses.fi/problemset/task/1674) | Basic subtree counting without merging |
| [Tree Diameter (CSES)](https://cses.fi/problemset/task/1131) | DFS on trees fundamentals |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Lomsat gelral (Codeforces)](https://codeforces.com/problemset/problem/600/E) | Find most frequent color (uses same technique) |
| [Tree Distances I (CSES)](https://cses.fi/problemset/task/1132) | Different aggregation (max distance) |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Path Queries II (CSES)](https://cses.fi/problemset/task/2134) | Heavy-Light Decomposition |
| [Tree Queries (CSES)](https://cses.fi/problemset/task/1137) | Euler tour + segment tree |

---

## Key Takeaways

1. **The Core Idea:** Always merge smaller sets into larger sets to ensure O(n log n) total operations
2. **Time Optimization:** From O(n^2) naive merging to O(n log n) by tracking set sizes
3. **Space Trade-off:** O(n) total space - elements exist in exactly one set at a time
4. **Pattern:** DSU on Tree / Small-to-Large Merging for subtree aggregation problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why small-to-large gives O(n log n) complexity
- [ ] Implement the solution without looking at code
- [ ] Handle both 0-indexed and 1-indexed variants
- [ ] Recognize this pattern in new tree problems
- [ ] Implement in both Python and C++ within 15 minutes

---

## Additional Resources

- [CP-Algorithms: Small-to-Large](https://cp-algorithms.com/data_structures/dsu.html)
- [CF Blog: DSU on Tree](https://codeforces.com/blog/entry/44351)
- [CSES Distinct Colors](https://cses.fi/problemset/task/1139) - Small-to-large merging
