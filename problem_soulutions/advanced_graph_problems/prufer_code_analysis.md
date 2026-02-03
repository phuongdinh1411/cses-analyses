---
layout: simple
title: "Prufer Code - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/prufer_code_analysis
difficulty: Medium
tags: [graph-theory, tree, encoding, combinatorics]
---

# Prufer Code

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Prufer Code](https://cses.fi/problemset/task/1134) |
| **Difficulty** | Medium |
| **Category** | Graph Theory / Tree Encoding |
| **Time Limit** | 1 second |
| **Key Technique** | Degree Tracking, Leaf Removal |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the bijection between labeled trees and Prufer sequences
- [ ] Encode a tree into its unique Prufer sequence
- [ ] Decode a Prufer sequence back into the original tree
- [ ] Apply Cayley's formula: n^(n-2) labeled trees on n vertices

---

## Problem Statement

**Problem:** Given a labeled tree with n nodes, construct its Prufer code (encoding). Given a Prufer code, reconstruct the original tree (decoding).

**Input (Encoding):**
- Line 1: n (number of nodes)
- Lines 2 to n: Two integers a, b representing an edge

**Output (Encoding):**
- n-2 integers: The Prufer code sequence

**Constraints:**
- 3 <= n <= 10^5
- Tree is connected with exactly n-1 edges
- Nodes are labeled 1 to n

### Example

```
Input:
5
1 2
2 3
3 4
3 5

Output:
2 3 3

Explanation:
Tree structure:
    1 - 2 - 3 - 4
            |
            5

Step 1: Smallest leaf is 1, parent is 2. Code: [2]. Remove node 1.
Step 2: Smallest leaf is 4, parent is 3. Code: [2, 3]. Remove node 4.
Step 3: Smallest leaf is 5, parent is 3. Code: [2, 3, 3]. Remove node 5.
Stop when 2 nodes remain (nodes 2 and 3).
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Insight:** A Prufer sequence uniquely encodes a labeled tree. Each node's frequency in the sequence equals (degree - 1).

The Prufer code establishes a bijection between labeled trees on n vertices and sequences of length n-2 where each element is in [1, n]. This proves Cayley's formula: there are exactly n^(n-2) labeled trees.

### Breaking Down the Problem

1. **What are we looking for?** A sequence that uniquely represents the tree structure.
2. **What information do we have?** The tree edges (adjacency).
3. **What's the relationship?** Repeatedly remove the smallest leaf and record its neighbor.

### The Core Algorithm

**Encoding:** Remove leaves in order, recording their parent.
**Decoding:** Reconstruct edges using degree information from the sequence.

---

## Solution 1: Brute Force - O(n^2)

### Idea

Repeatedly find the smallest leaf, record its parent, and remove it from the tree.

### Code

```python
def encode_brute_force(n, edges):
    """
    Generate Prufer code by repeatedly finding smallest leaf.
    Time: O(n^2), Space: O(n)
    """
    adj = [set() for _ in range(n + 1)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    prufer = []
    for _ in range(n - 2):
        # Find smallest leaf (node with degree 1)
        for v in range(1, n + 1):
            if len(adj[v]) == 1:
                parent = next(iter(adj[v]))
                prufer.append(parent)
                adj[v].remove(parent)
                adj[parent].remove(v)
                break

    return prufer
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | n iterations, each scanning up to n nodes |
| Space | O(n) | Adjacency storage |

---

## Solution 2: Optimal - O(n) Linear Time

### Key Insight

> **The Trick:** Track node degrees and use a pointer to find the next smallest leaf efficiently.

Instead of scanning for leaves each time, maintain degree counts and process leaves in order.

### Algorithm

1. Compute degree of each node
2. Find smallest leaf (degree = 1)
3. Remove leaf, add its parent to code, update degrees
4. If parent becomes a leaf AND is smaller than current pointer, process it immediately
5. Otherwise, continue to next smallest unprocessed leaf

### Dry Run Example

```
Tree: 1-2-3-4, 3-5
Edges: (1,2), (2,3), (3,4), (3,5)

Initial degrees: [-, 1, 2, 3, 1, 1]  (1-indexed, node 3 has degree 3)

Step 1: ptr=1, degree[1]=1 (leaf)
  Parent = 2, Code = [2]
  degree[2] = 2-1 = 1 (becomes leaf, but 2 > ptr)

Step 2: ptr=2, degree[2]=1 (leaf)
  But wait - we already have ptr at 1, continue scan
  ptr=4, degree[4]=1 (leaf)
  Parent = 3, Code = [2, 3]
  degree[3] = 3-1 = 2

Step 3: ptr=5, degree[5]=1 (leaf)
  Parent = 3, Code = [2, 3, 3]
  degree[3] = 2-1 = 1

Stop: Only 2 nodes remain (2 and 3)
Final Prufer Code: [2, 3, 3]
```

### Code

**Python:**

```python
def encode_optimal(n, edges):
    """
    Generate Prufer code in O(n) time.
    Time: O(n), Space: O(n)
    """
    adj = [[] for _ in range(n + 1)]
    degree = [0] * (n + 1)

    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        degree[a] += 1
        degree[b] += 1

    # Find first parent of each node (for leaf removal)
    parent = [0] * (n + 1)
    for v in range(1, n + 1):
        if adj[v]:
            parent[v] = adj[v][0]

    prufer = []
    ptr = 1
    leaf = 0

    # Find first leaf
    while ptr <= n and degree[ptr] != 1:
        ptr += 1
    leaf = ptr

    for _ in range(n - 2):
        # Find parent of current leaf
        p = 0
        for neighbor in adj[leaf]:
            if degree[neighbor] > 0:
                p = neighbor
                break

        prufer.append(p)
        degree[leaf] = 0
        degree[p] -= 1

        # Check if parent became a smaller leaf
        if degree[p] == 1 and p < ptr:
            leaf = p
        else:
            ptr += 1
            while ptr <= n and degree[ptr] != 1:
                ptr += 1
            leaf = ptr

    return prufer


def decode_optimal(n, prufer):
    """
    Reconstruct tree from Prufer code in O(n) time.
    Time: O(n), Space: O(n)
    """
    # Count occurrences (degree - 1 for each node)
    degree = [1] * (n + 1)
    degree[0] = 0
    for p in prufer:
        degree[p] += 1

    edges = []
    ptr = 1
    leaf = 0

    # Find first leaf (degree = 1)
    while ptr <= n and degree[ptr] != 1:
        ptr += 1
    leaf = ptr

    for p in prufer:
        edges.append((leaf, p))
        degree[leaf] -= 1
        degree[p] -= 1

        if degree[p] == 1 and p < ptr:
            leaf = p
        else:
            ptr += 1
            while ptr <= n and degree[ptr] != 1:
                ptr += 1
            leaf = ptr

    # Add final edge between remaining two nodes
    remaining = [v for v in range(1, n + 1) if degree[v] == 1]
    if len(remaining) == 2:
        edges.append((remaining[0], remaining[1]))

    return edges
```

**C++:**

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> encode(int n, vector<pair<int,int>>& edges) {
    vector<vector<int>> adj(n + 1);
    vector<int> degree(n + 1, 0);

    for (auto& [a, b] : edges) {
        adj[a].push_back(b);
        adj[b].push_back(a);
        degree[a]++;
        degree[b]++;
    }

    vector<int> prufer;
    int ptr = 1;
    while (ptr <= n && degree[ptr] != 1) ptr++;
    int leaf = ptr;

    for (int i = 0; i < n - 2; i++) {
        int p = 0;
        for (int neighbor : adj[leaf]) {
            if (degree[neighbor] > 0) {
                p = neighbor;
                break;
            }
        }

        prufer.push_back(p);
        degree[leaf] = 0;
        degree[p]--;

        if (degree[p] == 1 && p < ptr) {
            leaf = p;
        } else {
            ptr++;
            while (ptr <= n && degree[ptr] != 1) ptr++;
            leaf = ptr;
        }
    }
    return prufer;
}

vector<pair<int,int>> decode(int n, vector<int>& prufer) {
    vector<int> degree(n + 1, 1);
    for (int p : prufer) degree[p]++;

    vector<pair<int,int>> edges;
    int ptr = 1;
    while (ptr <= n && degree[ptr] != 1) ptr++;
    int leaf = ptr;

    for (int p : prufer) {
        edges.push_back({leaf, p});
        degree[leaf]--;
        degree[p]--;

        if (degree[p] == 1 && p < ptr) {
            leaf = p;
        } else {
            ptr++;
            while (ptr <= n && degree[ptr] != 1) ptr++;
            leaf = ptr;
        }
    }

    // Add final edge
    vector<int> remaining;
    for (int v = 1; v <= n; v++) {
        if (degree[v] == 1) remaining.push_back(v);
    }
    if (remaining.size() == 2) {
        edges.push_back({remaining[0], remaining[1]});
    }
    return edges;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each node processed exactly once |
| Space | O(n) | Degree array and adjacency list |

---

## Common Mistakes

### Mistake 1: Wrong Leaf Selection Order

```python
# WRONG - Using heap adds O(log n) overhead
import heapq
leaves = [v for v in range(1, n+1) if degree[v] == 1]
heapq.heapify(leaves)  # Unnecessary!
```

**Problem:** Using a priority queue makes this O(n log n).
**Fix:** Use the pointer technique shown above for O(n).

### Mistake 2: Not Handling Immediate Leaf Creation

```python
# WRONG - Always incrementing pointer
degree[p] -= 1
ptr += 1  # Wrong! Parent might be smaller leaf
```

**Problem:** When a parent becomes a leaf, it might be smaller than current pointer.
**Fix:** Check `if degree[p] == 1 and p < ptr: leaf = p`

### Mistake 3: Forgetting Final Edge in Decoding

```python
# WRONG - Missing final edge
for p in prufer:
    edges.append((leaf, p))
    # ... update degrees
return edges  # Missing one edge!
```

**Problem:** Prufer code has n-2 elements but tree has n-1 edges.
**Fix:** After processing, add edge between the two remaining degree-1 nodes.

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| n = 3 (minimum) | Line: 1-2-3 | Code: [2] | Smallest valid tree for Prufer |
| Star graph | 1 connected to 2,3,4,5 | Code: [1,1,1] | Center appears n-2 times |
| Path graph | 1-2-3-4-5 | Code: [2,3,4] | Each internal node once |
| Node n is leaf | Any tree with n as leaf | n never in code | Leaves don't appear |

---

## When to Use This Pattern

### Use Prufer Codes When:
- Counting labeled trees (Cayley's formula applications)
- Generating random labeled trees uniformly
- Encoding tree structures compactly
- Proving bijective results in combinatorics

### Don't Use When:
- Working with unlabeled/rooted trees (use different encodings)
- Need to preserve parent-child relationships (use parent arrays)
- Tree has additional attributes (weights, colors)

### Pattern Recognition Checklist:
- [ ] Need to count labeled trees? -> **Cayley's formula via Prufer**
- [ ] Need unique tree encoding? -> **Prufer sequence**
- [ ] Need to generate random tree? -> **Random Prufer code + decode**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Tree Diameter](https://cses.fi/problemset/task/1131) | Basic tree traversal |
| [Tree Distances I](https://cses.fi/problemset/task/1132) | Tree DFS/BFS fundamentals |

### Similar Difficulty

| Problem | Key Concept |
|---------|-------------|
| [Counting Trees](https://cses.fi/problemset/task/1693) | Cayley's formula application |
| [New Roads Queries](https://cses.fi/problemset/task/1160) | Tree construction |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Tree Isomorphism I](https://cses.fi/problemset/task/1700) | Tree hashing, canonical forms |
| [Tree Isomorphism II](https://cses.fi/problemset/task/1701) | Rooted tree isomorphism |

---

## Key Takeaways

1. **The Core Idea:** Prufer codes create a bijection between labeled trees and (n-2)-length sequences.
2. **Time Optimization:** Pointer technique avoids repeated scanning for O(n) complexity.
3. **Mathematical Significance:** Proves Cayley's formula: n^(n-2) labeled trees exist.
4. **Pattern:** Degree tracking + ordered leaf removal = efficient tree encoding.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Encode a tree to Prufer code without looking at solution
- [ ] Decode a Prufer code back to tree edges
- [ ] Explain why the bijection works (node appears degree-1 times)
- [ ] Derive Cayley's formula from Prufer code properties

---

## Additional Resources

- [CP-Algorithms: Prufer Code](https://cp-algorithms.com/graph/pruefer_code.html)
- [Wikipedia: Cayley's Formula](https://en.wikipedia.org/wiki/Cayley%27s_formula)
- [CSES Problem Set](https://cses.fi/problemset/)
