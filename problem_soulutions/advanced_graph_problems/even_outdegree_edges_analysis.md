---
layout: simple
title: "Even Outdegree Edges - Graph Orientation Problem"
permalink: /problem_soulutions/advanced_graph_problems/even_outdegree_edges_analysis
difficulty: Medium
tags: [graph, dfs, tree, parity, edge-orientation]
---

# Even Outdegree Edges

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Even Outdegree Edges](https://cses.fi/problemset/task/2179) |
| **Difficulty** | Medium |
| **Category** | Graph / DFS Tree |
| **Time Limit** | 1 second |
| **Key Technique** | DFS Tree + Parity-Based Edge Orientation |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how DFS trees partition edges into tree edges and back edges
- [ ] Use parity arguments to determine edge orientations
- [ ] Recognize when graph connectivity affects solution existence
- [ ] Apply bottom-up tree processing for degree constraints

---

## Problem Statement

**Problem:** Given an undirected graph, orient each edge (assign a direction) so that every vertex has an even outdegree. If this is impossible, report "IMPOSSIBLE".

**Input:**
- Line 1: Two integers n (vertices) and m (edges)
- Next m lines: Two integers a and b representing an undirected edge

**Output:**
- If possible: m lines, each showing an edge as "a b" where the edge is directed from a to b
- If impossible: Print "IMPOSSIBLE"

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 * 10^5
- The graph may have multiple edges and self-loops

### Example

```
Input:
4 4
1 2
2 3
3 4
4 1

Output:
1 2
3 2
3 4
1 4
```

**Explanation:** After orientation, outdegrees are: vertex 1 has outdegree 2, vertex 2 has outdegree 0, vertex 3 has outdegree 2, vertex 4 has outdegree 0. All are even.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When can we orient edges so all outdegrees are even?

The sum of all outdegrees equals m (total edges). For all outdegrees to be even, their sum must be even. Therefore, **m must be even** for a solution to exist.

But that is not sufficient - we also need the graph to be **connected** (or each component must have an even number of edges).

### Breaking Down the Problem

1. **What are we looking for?** An orientation of each edge such that every vertex has even outdegree.
2. **What information do we have?** An undirected graph with n vertices and m edges.
3. **What is the key insight?** Build a DFS tree and use parity to decide edge directions bottom-up.

### The DFS Tree Approach

When we run DFS on a connected graph:
- **Tree edges**: Edges used to discover new vertices
- **Back edges**: Edges connecting to already-visited ancestors

For each vertex v (processed bottom-up):
1. Count how many edges going "downward" (from children) are directed toward v
2. If this count is odd, orient the edge to v's parent away from v (v -> parent)
3. If this count is even, orient the edge to v's parent toward v (parent -> v)

This ensures every non-root vertex ends up with even outdegree. The root will also have even outdegree because m is even.

---

## Solution: DFS Tree with Parity

### Key Insight

> **The Trick:** Process the DFS tree bottom-up. At each vertex, use parity to decide whether to point the parent edge up or down, ensuring even outdegree.

### Algorithm

1. Check if m is even. If not, output "IMPOSSIBLE".
2. Build the adjacency list for the undirected graph.
3. For each connected component, run DFS:
   - For each vertex, track how many oriented edges point outward
   - Process children first (post-order)
   - Orient the parent edge based on current parity
4. Output all edge orientations.

### Dry Run Example

Let's trace through with the example input:

```
Graph: 4 vertices, 4 edges
Edges: (1,2), (2,3), (3,4), (4,1)

Step 1: m = 4 is even, so solution may exist.

Step 2: Build adjacency list
  1: [2, 4]
  2: [1, 3]
  3: [2, 4]
  4: [3, 1]

Step 3: DFS from vertex 1
  Visit 1 (root)
    Visit 2 (parent=1)
      Visit 3 (parent=2)
        Visit 4 (parent=3)
          Edge (4,1) is back edge to ancestor 1
          Orient as 1->4 (toward descendant)
          Return: outdegree[4] = 0 (even)
          Orient parent edge: 3->4 (current parity is 0, so parent points down)
        Return: outdegree[3] = 2 (3->4, 3->2? No, let's recalculate)

Let me redo with clearer tracking:

DFS from 1:
  Process vertex 4 (leaf in DFS tree, has back edge to 1):
    - Back edge (4,1): we defer this
    - outdegree[4] currently = 0
    - Parent edge (3,4): orient based on parity

Bottom-up processing:
  At 4: subtree_out = 0 (even), orient parent edge INTO 4: 3->4, outdegree[3]++
  At 3: subtree_out = 1 (from 3->4), need odd more, orient parent edge OUT: 3->2
        Now outdegree[3] = 2 (even)
  At 2: subtree_out = 1 (from incoming 3->2 doesn't count, outgoing does)
        ...

Final orientation achieving all even outdegrees:
  1->2: outdegree[1]++
  3->2: outdegree[3]++
  3->4: outdegree[3]++
  1->4: outdegree[1]++

Result: outdegree = [2, 0, 2, 0] - all even!
```

### Visual Diagram

```
Original undirected graph:        DFS Tree:

    1 --- 2                           1
    |     |                          /
    |     |                         2
    4 --- 3                        /
                                  3
                                 /
                                4
                                |
                             (back to 1)

After orientation:
    1 --> 2
    |     ^
    v     |
    4 <-- 3

Outdegrees: 1:2, 2:0, 3:2, 4:0 (all even)
```

### Code

**Python Solution:**

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
  input_data = sys.stdin.read().split()
  idx = 0
  n = int(input_data[idx]); idx += 1
  m = int(input_data[idx]); idx += 1

  # Check if solution is possible
  if m % 2 == 1:
    print("IMPOSSIBLE")
    return

  # Build adjacency list with edge indices
  # Each edge stored as (neighbor, edge_index, is_first)
  adj = defaultdict(list)
  edges = []

  for i in range(m):
    a = int(input_data[idx]); idx += 1
    b = int(input_data[idx]); idx += 1
    edges.append([a, b])
    adj[a].append((b, i, True))   # True = this is the "a" side
    adj[b].append((a, i, False))  # False = this is the "b" side

  visited = [False] * (n + 1)
  result = [None] * m  # result[i] = (from, to) for edge i

  def dfs(v, parent_edge_idx):
    visited[v] = True
    out_count = 0  # count of edges oriented outward from v

    for neighbor, edge_idx, is_a_side in adj[v]:
      if result[edge_idx] is not None:
        # Edge already oriented
        if result[edge_idx][0] == v:
          out_count += 1
        continue

      if not visited[neighbor]:
        # Tree edge - recurse first
        child_out = dfs(neighbor, edge_idx)

        # Orient based on child's parity
        if child_out % 2 == 1:
          # Child has odd out-count, point edge toward child
          result[edge_idx] = (v, neighbor)
          out_count += 1
        else:
          # Child has even out-count, point edge toward v
          result[edge_idx] = (neighbor, v)
      else:
        # Back edge to ancestor - orient toward ancestor (v -> neighbor)
        result[edge_idx] = (v, neighbor)
        out_count += 1

    return out_count

  # Process all components
  for v in range(1, n + 1):
    if not visited[v] and adj[v]:
      dfs(v, -1)

  # Output results
  for i in range(m):
    if result[i]:
      print(result[i][0], result[i][1])
    else:
      # Self-loop or isolated edge
      print(edges[i][0], edges[i][1])

if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | Single DFS traversal |
| Space | O(n + m) | Adjacency list and result storage |

---

## Common Mistakes

### Mistake 1: Forgetting the Parity Check

```python
# WRONG - missing initial check
def solve(n, m, edges):
  # Directly try to orient without checking m
  ...

# CORRECT
def solve(n, m, edges):
  if m % 2 == 1:
    print("IMPOSSIBLE")
    return
  ...
```

**Problem:** If m is odd, no valid orientation exists.
**Fix:** Always check if m is even before attempting to solve.

### Mistake 2: Processing Edges Multiple Times

```python
# WRONG
for neighbor, edge_idx in adj[v]:
  result[edge_idx] = (v, neighbor)  # May overwrite previous orientation!
```

**Problem:** Each undirected edge appears twice in the adjacency list.
**Fix:** Track which edges have been oriented to avoid processing twice.

### Mistake 3: Incorrect Parity Logic

```python
# WRONG - inverted logic
if child_out % 2 == 0:  # Should be == 1
  result[edge_idx] = (v, neighbor)
```

**Problem:** Inverted parity check leads to odd outdegrees.
**Fix:** Orient away from v when child has ODD outcount (to make it even).

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Odd edges | `n=2, m=1, edge=(1,2)` | IMPOSSIBLE | m must be even |
| No edges | `n=3, m=0` | (empty output) | All outdegrees are 0 (even) |
| Self-loop | `n=1, m=2, edges=(1,1),(1,1)` | `1 1` (twice) | Self-loops count as outdegree |
| Disconnected | `n=4, m=2, (1,2),(3,4)` | Valid orientation | Each component handled separately |
| Single vertex | `n=1, m=0` | (empty output) | Trivially satisfied |

---

## When to Use This Pattern

### Use This Approach When:
- You need to orient undirected edges to satisfy degree constraints
- The problem involves parity conditions on vertices
- You can use DFS tree structure to propagate constraints bottom-up

### Don't Use When:
- The graph is already directed
- Constraints involve specific edge weights (not just parity)
- You need to find minimum cost orientation (use flow algorithms)

### Pattern Recognition Checklist:
- [ ] Need to assign directions to undirected edges? --> **Consider DFS tree orientation**
- [ ] Parity constraint on vertex degrees? --> **Use bottom-up parity propagation**
- [ ] Connected graph with degree constraints? --> **Check necessary conditions first (like m even)**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Building Roads](https://cses.fi/problemset/task/1666) | Basic graph connectivity |
| [Round Trip](https://cses.fi/problemset/task/1669) | DFS cycle detection |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Strongly Connected Edges](https://cses.fi/problemset/task/2177) | Orient for strong connectivity |
| [Acyclic Graph Edges](https://cses.fi/problemset/task/2178) | Orient to make DAG |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Eulerian Path](https://cses.fi/problemset/task/1691) | Finding path using all edges |
| [New Flight Routes](https://cses.fi/problemset/task/1685) | SCC-based edge addition |

---

## Key Takeaways

1. **The Core Idea:** Use DFS tree structure to orient edges bottom-up, using parity to decide each edge's direction.
2. **Necessary Condition:** m must be even for any solution to exist.
3. **Why DFS Works:** Each vertex (except root) has exactly one parent edge, which we can orient to fix its parity.
4. **Pattern:** Parity-based graph orientation using tree decomposition.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why m must be even
- [ ] Draw the DFS tree for a sample graph
- [ ] Trace through the bottom-up parity propagation
- [ ] Implement the solution in under 15 minutes
- [ ] Handle edge cases (no edges, disconnected components)

---

## Additional Resources

- [CP-Algorithms: DFS and Tree Decomposition](https://cp-algorithms.com/graph/depth-first-search.html)
- [CSES Even Outdegree Edges](https://cses.fi/problemset/task/2179) - Graph orientation problem
- [Graph Orientation Problems - TopCoder](https://www.topcoder.com/community/competitive-programming/tutorials/)
