---
layout: simple
title: "Finding Centroid - Tree Algorithm Problem"
permalink: /problem_soulutions/tree_algorithms/finding_centroid_analysis
difficulty: Medium
tags: [tree, centroid, dfs, tree-dp]
prerequisites: [tree_traversal, subtree_size]
---

# Finding Centroid

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Tree DP / Subtree Size Calculation |
| **CSES Link** | [Finding Centroid](https://cses.fi/problemset/task/2079) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand what a tree centroid is and its properties
- [ ] Calculate subtree sizes using DFS
- [ ] Identify the centroid by checking the max subtree size constraint
- [ ] Apply centroid concepts as a foundation for centroid decomposition

---

## Problem Statement

**Problem:** Given a tree of n nodes, find the centroid of the tree. A centroid is a node such that when removed, no remaining component has more than n/2 nodes.

**Input:**
- Line 1: n (number of nodes)
- Next n-1 lines: Two integers a and b representing an edge between nodes a and b

**Output:**
- A single integer: the centroid node (1-indexed)

**Constraints:**
- 1 <= n <= 2 x 10^5
- The graph is a connected tree

### Example

```
Input:
5
1 2
2 3
2 4
4 5

Output:
2
```

**Explanation:** When node 2 is removed, the tree splits into components: {1}, {3}, and {4,5}. The largest component has size 2, which is <= 5/2 = 2. Node 2 is the centroid.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** What makes a node the "center" of a tree?

A centroid is the most balanced node in a tree. When you remove it, no single subtree dominates - all resulting components have size at most n/2. This is the defining property of a centroid.

### Breaking Down the Problem

1. **What are we looking for?** A node where ALL neighboring subtrees have size <= n/2
2. **What information do we need?** The size of each subtree when rooted at any node
3. **What's the key insight?** For a node rooted at r, we need to check:
   - Size of each child's subtree
   - Size of the "parent's subtree" = n - subtree_size[current_node]

### Centroid Properties

```
Important Properties:
1. Every tree has at least one centroid
2. A tree has at most two centroids (if two exist, they are adjacent)
3. For the centroid, max(all_component_sizes) <= n/2
4. The centroid minimizes the maximum subtree size
```

### Analogies

Think of the centroid like finding the balance point of a mobile. If you hang the tree from the centroid, no branch would significantly outweigh the others.

---

## Solution 1: Brute Force

### Idea

For each node, remove it and check if all resulting components have size <= n/2.

### Algorithm

1. For each node v from 1 to n:
2. Remove node v and find all connected components
3. Check if all component sizes are <= n/2
4. Return the first node satisfying this condition

### Code

```python
def brute_force_centroid(n, edges):
    """
    Brute force: try removing each node and check component sizes.

    Time: O(n^2)
    Space: O(n)
    """
    from collections import defaultdict

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    def get_component_sizes(removed):
        visited = set([removed])
        sizes = []

        for start in range(1, n + 1):
            if start not in visited:
                # BFS/DFS to find component size
                size = 0
                stack = [start]
                while stack:
                    node = stack.pop()
                    if node in visited:
                        continue
                    visited.add(node)
                    size += 1
                    for neighbor in graph[node]:
                        if neighbor not in visited:
                            stack.append(neighbor)
                sizes.append(size)

        return sizes

    for node in range(1, n + 1):
        sizes = get_component_sizes(node)
        if all(s <= n // 2 for s in sizes):
            return node

    return -1
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | For each of n nodes, we do O(n) traversal |
| Space | O(n) | Graph storage and visited set |

### Why This Works (But Is Slow)

This correctly finds the centroid by definition checking, but we repeat O(n) work for each candidate node.

---

## Solution 2: Optimal Solution (Single DFS)

### Key Insight

> **The Trick:** Root the tree at any node, compute subtree sizes once, then find the node where max(child subtree sizes, n - subtree_size[node]) <= n/2.

### Understanding the Components

When we root the tree at node 1 and consider removing node v:
- **Child subtrees:** Direct subtrees below v (we know their sizes from DFS)
- **Parent subtree:** Everything above v = n - subtree_size[v]

```
         1
        / \
       2   3     If we remove node 2:
      / \        - Child subtrees: {4}, {5}
     4   5       - Parent subtree: {1, 3} = n - subtree_size[2]
```

### Algorithm

1. Build adjacency list from edges
2. DFS from node 1 to compute subtree sizes
3. For each node, check if it's a centroid:
   - Max child subtree size <= n/2
   - Parent subtree size (n - subtree_size[node]) <= n/2
4. Return the first centroid found

### Dry Run Example

Let's trace through with the example tree:

```
Tree structure (n=5):
    1
    |
    2
   /|\
  3 4
    |
    5

Edges: (1,2), (2,3), (2,4), (4,5)
```

**Step 1: Compute subtree sizes (root at node 1)**

```
DFS traversal order: 1 -> 2 -> 3 -> 4 -> 5

After DFS:
  subtree_size[5] = 1
  subtree_size[4] = 1 + 1 = 2  (4 + subtree of 5)
  subtree_size[3] = 1
  subtree_size[2] = 1 + 1 + 2 = 4  (2 + subtrees of 3,4)
  subtree_size[1] = 1 + 4 = 5  (1 + subtree of 2)
```

**Step 2: Check each node for centroid condition**

```
n/2 = 5/2 = 2

Node 1:
  Child subtree: {2,3,4,5} size=4 > 2  FAIL

Node 2:
  Child subtrees: {3} size=1 <= 2  OK
                  {4,5} size=2 <= 2  OK
  Parent subtree: n - 4 = 1 <= 2  OK
  ALL <= 2, so node 2 is CENTROID

Answer: 2
```

### Visual Diagram

```
Checking node 2 as centroid:

       [1]          <- Parent component (size = 1)
        |
  -----[2]-----     <- Remove this node
  |     |     |
 [3]   [4]         <- Child components
        |
       [5]

Component sizes: 1, 1, 2
All <= n/2 = 2?  YES -> Node 2 is centroid
```

### Code (Python)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def find_centroid(n, edges):
    """
    Find tree centroid using single DFS.

    Time: O(n) - one DFS pass
    Space: O(n) - adjacency list and subtree sizes
    """
    if n == 1:
        return 1

    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    subtree_size = [0] * (n + 1)

    # DFS to compute subtree sizes
    def dfs(node, parent):
        subtree_size[node] = 1
        for child in graph[node]:
            if child != parent:
                dfs(child, node)
                subtree_size[node] += subtree_size[child]

    dfs(1, -1)

    # Find centroid
    def find(node, parent):
        for child in graph[node]:
            if child != parent:
                # Check child subtree
                if subtree_size[child] > n // 2:
                    return find(child, node)
        # Check parent subtree
        if n - subtree_size[node] > n // 2:
            return find(parent, node)
        return node

    return find(1, -1)


# Main input handling
def main():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1

    edges = []
    for _ in range(n - 1):
        u = int(input_data[idx]); idx += 1
        v = int(input_data[idx]); idx += 1
        edges.append((u, v))

    print(find_centroid(n, edges))

if __name__ == "__main__":
    main()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
vector<int> adj[MAXN];
int subtree_size[MAXN];
int n;

void dfs(int node, int parent) {
    subtree_size[node] = 1;
    for (int child : adj[node]) {
        if (child != parent) {
            dfs(child, node);
            subtree_size[node] += subtree_size[child];
        }
    }
}

int find_centroid(int node, int parent) {
    for (int child : adj[node]) {
        if (child != parent) {
            // Child subtree too large -> move toward it
            if (subtree_size[child] > n / 2) {
                return find_centroid(child, node);
            }
        }
    }
    // Parent subtree too large -> move toward parent
    if (n - subtree_size[node] > n / 2) {
        return find_centroid(parent, node);
    }
    return node;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> n;

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    dfs(1, -1);
    cout << find_centroid(1, -1) << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single DFS to compute sizes + single traversal to find centroid |
| Space | O(n) | Adjacency list + subtree size array + recursion stack |

---

## Common Mistakes

### Mistake 1: Forgetting the Parent Subtree

```python
# WRONG - Only checking child subtrees
def is_centroid(node):
    for child in graph[node]:
        if subtree_size[child] > n // 2:
            return False
    return True  # Missing parent subtree check!
```

**Problem:** When we root the tree, the "parent direction" also forms a component.
**Fix:** Also check `n - subtree_size[node] <= n // 2`

### Mistake 2: Wrong Subtree Size After Re-rooting

```python
# WRONG - Using child's subtree size directly when node is not root
if subtree_size[child] > n // 2:  # This is wrong if child was computed as descendant
```

**Problem:** subtree_size[child] is computed relative to the root, not relative to current node.
**Fix:** When moving from node to child, the "subtree" in child's direction has size `subtree_size[child]`, which is correct. The confusion arises when checking the parent direction.

### Mistake 3: Integer Division Edge Case

```python
# Be careful with n // 2 vs n / 2
# For n = 5: n // 2 = 2
# Centroid condition: component_size <= n // 2
```

**Fix:** Use integer division consistently. The condition is `<= n/2` which means `<= floor(n/2)`.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n=1, no edges | 1 | Only node is trivially the centroid |
| Two nodes | n=2, edge (1,2) | 1 or 2 | Both are centroids (component size = 1 <= 1) |
| Line graph | 1-2-3-4-5 | 3 | Middle node is centroid |
| Star graph | 1 connected to 2,3,4,5 | 1 | Center node is centroid |
| Two centroids | Certain even trees | Either one | Both valid answers |

---

## When to Use This Pattern

### Use This Approach When:
- Finding the "balanced center" of a tree
- Preprocessing for centroid decomposition
- Solving tree problems that benefit from divide-and-conquer on trees
- Finding a node that minimizes maximum distance to all other nodes

### Don't Use When:
- Looking for tree diameter endpoints (different problem)
- Need all possible centroids (modify to return both if two exist)
- Working with forests (apply to each tree separately)

### Pattern Recognition Checklist:
- [ ] Need to split tree into balanced parts? -> **Centroid**
- [ ] Divide and conquer on trees? -> **Centroid Decomposition**
- [ ] Find most central node? -> **Consider centroid**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Subordinates (CSES)](https://cses.fi/problemset/task/1674) | Practice computing subtree sizes |
| [Tree Diameter (CSES)](https://cses.fi/problemset/task/1131) | Basic tree DFS traversal |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Tree Distances I (CSES)](https://cses.fi/problemset/task/1132) | Uses similar subtree size technique |
| [Tree Distances II (CSES)](https://cses.fi/problemset/task/1133) | Re-rooting technique on trees |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Centroid Decomposition Problems](https://cses.fi/problemset/) | Uses centroid as building block |
| [Fixed-Length Paths I (CSES)](https://cses.fi/problemset/task/2080) | Centroid decomposition application |

---

## Key Takeaways

1. **The Core Idea:** A centroid balances the tree - no component exceeds n/2 when removed
2. **Time Optimization:** Single DFS computes all subtree sizes; then one traversal finds centroid
3. **Space Trade-off:** O(n) extra space for subtree sizes enables O(n) time
4. **Pattern:** Foundation for centroid decomposition - a powerful divide-and-conquer technique on trees

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain what a tree centroid is and its properties
- [ ] Compute subtree sizes with a single DFS
- [ ] Check both child subtrees AND parent subtree for centroid condition
- [ ] Implement the solution in under 10 minutes

---

## Additional Resources

- [CP-Algorithms: Centroid Decomposition](https://cp-algorithms.com/graph/centroid-decomposition.html)
- [CSES Problem Set](https://cses.fi/problemset/)
- [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)
