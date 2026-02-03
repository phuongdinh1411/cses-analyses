---
layout: simple
title: "Rerooting Technique (All-Root DP) - Tree Algorithms"
permalink: /problem_soulutions/tree_algorithms/rerooting_dp_analysis
difficulty: Hard
tags: [tree-dp, rerooting, all-roots, dfs, dynamic-programming]
---

# Rerooting Technique (All-Root DP)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Tree DP |
| **Time Complexity** | O(n) |
| **Key Technique** | Two-Pass DFS (Down then Up) |

### Concept Explanation

The **Rerooting Technique** solves a class of tree problems where we need to compute an answer for **every node as if it were the root**. The naive approach would run a separate DFS from each node, giving O(n^2) complexity. Rerooting reduces this to O(n) by cleverly reusing computations.

The core idea: When we "move" the root from node `u` to its child `v`, we can compute the new answer by:
1. **Removing** v's contribution from u's answer
2. **Adding** u's modified answer as a contribution to v

### Learning Goals

After studying this technique, you will be able to:
- [ ] Recognize problems requiring answers for all nodes as root
- [ ] Implement the two-pass DFS pattern (down pass + up pass)
- [ ] Define combine and uncombine operations for different problem types
- [ ] Solve "Tree Distances II" and similar CSES problems efficiently
- [ ] Transform O(n^2) tree solutions into O(n) solutions

---

## Problem Statement

**Generic Problem:** Given a tree with n nodes, compute f(v) for every node v, where f(v) is some function that depends on the tree structure when v is considered the root.

**Classic Example - Tree Distances II:**
- Compute the sum of distances from each node to all other nodes
- Output n values: dist_sum[1], dist_sum[2], ..., dist_sum[n]

**Constraints:**
- 1 <= n <= 2 * 10^5
- Tree is connected and undirected

---

## Intuition: The Two-Pass Approach

### Pattern Recognition

> **Key Question:** How can we efficiently "re-root" the tree without recomputing everything?

When moving the root from parent `p` to child `c`:
- All nodes in c's subtree get **1 closer** to the new root
- All nodes outside c's subtree get **1 farther** from the new root

### The Two-Pass Strategy

```
Pass 1 (DOWN): Root at node 1, compute dp_down[v] for all nodes
               dp_down[v] = answer considering only v's subtree

Pass 2 (UP):   Propagate answers from parent to children
               dp_up[v] = answer considering nodes outside v's subtree

Final Answer:  answer[v] = combine(dp_down[v], dp_up[v])
```

### Visual Intuition

```
Original Tree (rooted at 1):          After rerooting at 3:

        1                                     3
       /|\                                   /|\
      2 3 4                                 1 5 6
        |                                   |
       /|\                                 / \
      5 6 7                               2   4
```

When we reroot from 1 to 3:
- Subtree of 3 (nodes 3,5,6,7) stays below
- Rest of tree (nodes 1,2,4) becomes a new "child" of 3

---

## The Combine/Uncombine Pattern

### Core Operations

For rerooting to work, we need two operations:

| Operation | Purpose | Example (Distance Sum) |
|-----------|---------|------------------------|
| `combine(a, b)` | Merge contributions | `a + b + subtree_size` |
| `uncombine(total, part)` | Remove a contribution | `total - part - subtree_size` |

### Why Uncombine is Needed

```
answer[parent] = combine(child1, child2, child3, ...)

To get answer for child1 as root:
  contribution_from_parent = uncombine(answer[parent], contribution_of_child1)
  answer[child1] = combine(dp_down[child1], contribution_from_parent)
```

---

## Dry Run Example: Tree Distances II

### Input Tree

```
n = 5
Edges: 1-2, 1-3, 3-4, 3-5

Tree structure:
        1
       / \
      2   3
         / \
        4   5
```

### Pass 1: Down DFS (compute subtree info)

Starting DFS from node 1:

```
Node 2 (leaf):
  subtree_size[2] = 1
  dist_sum_down[2] = 0  (no nodes below)

Node 4 (leaf):
  subtree_size[4] = 1
  dist_sum_down[4] = 0

Node 5 (leaf):
  subtree_size[5] = 1
  dist_sum_down[5] = 0

Node 3:
  subtree_size[3] = 1 + 1 + 1 = 3  (self + children)
  dist_sum_down[3] = (0 + 1) + (0 + 1) = 2
                     [from 4]   [from 5]
  (Each child contributes: its dist_sum + 1 edge * its subtree_size)

Node 1 (root):
  subtree_size[1] = 1 + 1 + 3 = 5
  dist_sum_down[1] = (0 + 1) + (2 + 3) = 6
                     [from 2]   [from 3]
```

### Pass 2: Up DFS (propagate to children)

```
Node 1: answer[1] = dist_sum_down[1] = 6 (it's the root)

Moving to Node 2:
  Nodes outside subtree of 2: {1, 3, 4, 5} = 4 nodes
  contribution_from_1 = answer[1] - (dist_sum_down[2] + subtree_size[2])
                      = 6 - (0 + 1) = 5
  answer[2] = dist_sum_down[2] + (contribution_from_1 + 4)
            = 0 + (5 + 4) = 9

  Verify: From node 2, distances are: 1->1, 1->3, 2->4, 2->5, 3->... wait
  Actually: d(2,1)=1, d(2,3)=2, d(2,4)=3, d(2,5)=3 => 1+2+3+3 = 9 [Correct!]

Moving to Node 3:
  Nodes outside subtree of 3: {1, 2} = 2 nodes
  contribution_from_1 = answer[1] - (dist_sum_down[3] + subtree_size[3])
                      = 6 - (2 + 3) = 1
  answer[3] = dist_sum_down[3] + (contribution_from_1 + 2)
            = 2 + (1 + 2) = 5

  Verify: d(3,1)=1, d(3,2)=2, d(3,4)=1, d(3,5)=1 => 1+2+1+1 = 5 [Correct!]

Moving to Node 4 (from 3):
  contribution_from_3 = answer[3] - (dist_sum_down[4] + subtree_size[4])
                      = 5 - (0 + 1) = 4
  answer[4] = 0 + (4 + 4) = 8

  Verify: d(4,1)=2, d(4,2)=3, d(4,3)=1, d(4,5)=2 => 2+3+1+2 = 8 [Correct!]

Moving to Node 5 (from 3):
  contribution_from_3 = answer[3] - (dist_sum_down[5] + subtree_size[5])
                      = 5 - (0 + 1) = 4
  answer[5] = 0 + (4 + 4) = 8

  Verify: d(5,1)=2, d(5,2)=3, d(5,3)=1, d(5,4)=2 => 2+3+1+2 = 8 [Correct!]
```

### Final Answers

```
answer = [6, 9, 5, 8, 8]  (for nodes 1, 2, 3, 4, 5)
```

---

## Solution: Optimal O(n)

### DP State Definition

| State | Meaning |
|-------|---------|
| `subtree_size[v]` | Number of nodes in subtree rooted at v |
| `dp_down[v]` | Answer contribution from v's subtree |
| `answer[v]` | Final answer when v is the root |

### Algorithm

1. **Build adjacency list** from edges
2. **DFS Down (Pass 1):** Compute subtree_size and dp_down for all nodes
3. **DFS Up (Pass 2):** Propagate answers from parent to children
4. **Output:** answer[1], answer[2], ..., answer[n]

### Python Solution

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1

    if n == 1:
        print(0)
        return

    # Build adjacency list
    adj = defaultdict(list)
    for _ in range(n - 1):
        a = int(input_data[idx]); idx += 1
        b = int(input_data[idx]); idx += 1
        adj[a].append(b)
        adj[b].append(a)

    subtree_size = [0] * (n + 1)
    dp_down = [0] * (n + 1)
    answer = [0] * (n + 1)

    # Pass 1: DFS down - compute subtree info
    def dfs_down(node, parent):
        subtree_size[node] = 1
        dp_down[node] = 0

        for child in adj[node]:
            if child != parent:
                dfs_down(child, node)
                subtree_size[node] += subtree_size[child]
                # Add child's contribution: distances in subtree + 1 edge per node
                dp_down[node] += dp_down[child] + subtree_size[child]

    # Pass 2: DFS up - propagate answers
    def dfs_up(node, parent, contribution_from_above):
        # Total answer for this node as root
        answer[node] = dp_down[node] + contribution_from_above

        for child in adj[node]:
            if child != parent:
                # Remove child's contribution from current answer
                # Then add 1 edge per node outside child's subtree
                nodes_outside = n - subtree_size[child]
                child_contribution = dp_down[child] + subtree_size[child]
                new_contribution = (answer[node] - child_contribution) + nodes_outside
                dfs_up(child, node, new_contribution)

    dfs_down(1, 0)
    dfs_up(1, 0, 0)

    print(' '.join(map(str, answer[1:n+1])))

solve()
```

### C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
vector<int> adj[MAXN];
long long subtree_size[MAXN], dp_down[MAXN], answer[MAXN];
int n;

void dfs_down(int node, int parent) {
    subtree_size[node] = 1;
    dp_down[node] = 0;

    for (int child : adj[node]) {
        if (child != parent) {
            dfs_down(child, node);
            subtree_size[node] += subtree_size[child];
            dp_down[node] += dp_down[child] + subtree_size[child];
        }
    }
}

void dfs_up(int node, int parent, long long contribution_from_above) {
    answer[node] = dp_down[node] + contribution_from_above;

    for (int child : adj[node]) {
        if (child != parent) {
            long long nodes_outside = n - subtree_size[child];
            long long child_contribution = dp_down[child] + subtree_size[child];
            long long new_contribution = (answer[node] - child_contribution) + nodes_outside;
            dfs_up(child, node, new_contribution);
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;

    if (n == 1) {
        cout << 0 << "\n";
        return 0;
    }

    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    dfs_down(1, 0);
    dfs_up(1, 0, 0);

    for (int i = 1; i <= n; i++) {
        cout << answer[i] << " \n"[i == n];
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Two DFS passes, each visiting every node once |
| Space | O(n) | Adjacency list + DP arrays |

---

## Common Mistakes

### Mistake 1: Forgetting to Handle Single Node

```python
# WRONG - crashes or gives wrong answer for n=1
dfs_down(1, 0)  # Works but answer needs special case

# CORRECT
if n == 1:
    print(0)
    return
```

**Problem:** A single node has distance sum of 0, and DFS may behave unexpectedly.

### Mistake 2: Wrong Combine/Uncombine Formula

```python
# WRONG - forgetting to add nodes_outside when rerooting
new_contribution = answer[node] - child_contribution  # Missing term!

# CORRECT
nodes_outside = n - subtree_size[child]
new_contribution = (answer[node] - child_contribution) + nodes_outside
```

**Problem:** When we move root to child, all nodes outside get 1 farther.

### Mistake 3: Using Wrong Data Types

```cpp
// WRONG - integer overflow for large trees
int dp_down[MAXN];  // Sum of distances can exceed 2^31

// CORRECT
long long dp_down[MAXN];
```

**Problem:** With n = 2*10^5 nodes, distance sums can reach ~10^10.

### Mistake 4: Modifying dp_down During Up Pass

```python
# WRONG - corrupts data needed for sibling calculations
def dfs_up(node, parent, contrib):
    dp_down[node] += contrib  # NEVER modify dp_down!
    ...

# CORRECT - use separate answer array
def dfs_up(node, parent, contrib):
    answer[node] = dp_down[node] + contrib
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Single node | n=1, no edges | `0` | No other nodes to measure distance to |
| Linear tree (path) | 1-2-3-4-5 | `10 7 6 7 10` | Endpoints have max distance |
| Star graph | 1 connected to 2,3,4,5 | `4 7 7 7 7` | Center has minimum distance |
| Two nodes | 1-2 | `1 1` | Each at distance 1 from the other |
| Large linear | n=200000 path | Check overflow | Distances sum to ~n^2/2 |

---

## When to Use Rerooting

### Use This Technique When:

- Computing a value for **every node** as if it were the root
- The answer can be expressed in terms of subtree aggregates
- You can define **combine** and **uncombine** operations
- The brute force would be O(n^2) with n separate DFS calls

### Common Problem Types:

| Problem Type | Combine | Uncombine |
|--------------|---------|-----------|
| Sum of distances | add + size | subtract + size |
| Max depth | max + 1 | requires prefix/suffix |
| Subtree sums | add | subtract |
| Tree diameter queries | complex | needs auxiliary data |

### Pattern Recognition Checklist:

- [ ] "For each node, compute..." -> Consider rerooting
- [ ] Can define subtree contribution? -> Rerooting likely works
- [ ] Combine is associative/commutative? -> Simpler implementation
- [ ] Need uncombine for non-invertible ops? -> Use prefix/suffix arrays

---

## Related CSES Problems

### Direct Applications

| Problem | Description | Rerooting Aspect |
|---------|-------------|------------------|
| [Tree Distances II](https://cses.fi/problemset/task/1133) | Sum of distances from each node | Classic rerooting |
| [Tree Distances I](https://cses.fi/problemset/task/1132) | Max distance from each node | Rerooting with max |

### Related Tree DP Problems

| Problem | Technique |
|---------|-----------|
| Tree Diameter | Two BFS or DP on tree |
| Tree Matching | Standard tree DP |
| Subordinates | Basic subtree counting |

### Harder Extensions

| Problem | New Challenge |
|---------|---------------|
| Finding Centroid | Minimize max subtree |
| Weighted Tree Distances | Edge weights in formula |

---

## Key Takeaways

1. **Core Idea:** Reuse subtree computations when changing root by tracking what to add/remove
2. **Two-Pass Pattern:** Down pass computes subtree info, Up pass propagates to children
3. **Combine/Uncombine:** Define how contributions merge and split for your specific problem
4. **Complexity Win:** Transform O(n^2) brute force into O(n) with clever bookkeeping

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement rerooting for Tree Distances II without reference
- [ ] Explain why two passes are sufficient
- [ ] Derive the combine/uncombine formulas for distance sums
- [ ] Handle edge cases (n=1, overflow)
- [ ] Recognize rerooting opportunities in new problems

---

## Additional Resources

- [CP-Algorithms: Rerooting Technique](https://cp-algorithms.com/graph/reroot.html)
- [CSES Problem Set - Tree Algorithms](https://cses.fi/problemset/list/)
- [Codeforces Blog on Tree DP](https://codeforces.com/blog/entry/20935)
