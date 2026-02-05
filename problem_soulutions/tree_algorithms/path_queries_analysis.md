---
layout: simple
title: "Path Queries - Tree Algorithms Problem"
permalink: /problem_soulutions/tree_algorithms/path_queries_analysis
difficulty: Medium
tags: [tree, euler-tour, segment-tree, dfs]
prerequisites: [tree_traversal, segment_tree_basics]
---

# Path Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [CSES 1138](https://cses.fi/problemset/task/1138) |
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Euler Tour + Segment Tree |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Transform tree path sums into range queries using Euler tour
- [ ] Apply segment trees to tree problems via linearization
- [ ] Understand how point updates on nodes affect subtree ranges
- [ ] Convert "root-to-node" queries into O(log n) operations

---

## Problem Statement

**Problem:** Given a rooted tree with n nodes where each node has a value, process two types of queries:
1. **Update:** Change the value of node s to x
2. **Query:** Find the sum of values on the path from root (node 1) to node s

**Input:**
- Line 1: n q (number of nodes, number of queries)
- Line 2: v1 v2 ... vn (initial values of nodes)
- Next n-1 lines: a b (edge between nodes a and b)
- Next q lines: Either "1 s x" (update) or "2 s" (query)

**Output:**
- For each type 2 query, print the sum of values on the path from root to node s

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- 1 <= vi, x <= 10^9
- 1 <= s <= n

### Example

```
Input:
5 3
4 2 5 2 1
1 2
1 3
3 4
3 5
2 4
1 3 2
2 4

Output:
11
8
```

**Explanation:**
- Query 1: Path 1->3->4 has sum 4+5+2 = 11
- Update: Node 3 value changes from 5 to 2
- Query 2: Path 1->3->4 now has sum 4+2+2 = 8

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we transform tree path queries into something a segment tree can handle?

The core insight is that **path sum from root to node u = prefix sum in DFS order**. If we flatten the tree using Euler tour (DFS traversal), each node's "entry time" gives us a position where we can use a segment tree for prefix sums.

### Breaking Down the Problem

1. **What are we looking for?** Sum of node values from root to any node
2. **What information do we have?** Tree structure, node values, update/query operations
3. **What's the relationship?** Path to node u includes all ancestors of u in DFS order

### The Key Transformation

```
Tree:           Euler Tour (entry times):
    1               Node: 1  2  3  4  5
   / \              Time: 0  1  2  3  4
  2   3
     / \
    4   5

Path sum(1->3->4) = value[1] + value[3] + value[4]
                  = Prefix sum up to node 4's entry time
                  = BUT only counting ancestors!
```

**The trick:** When we enter a node, add its value. When we exit, subtract it. Then prefix sum at entry time gives path sum!

---

## Solution 1: Brute Force (DFS per Query)

### Idea

For each query, traverse from root to the target node, summing values along the path.

### Algorithm

1. Build adjacency list from edges
2. For each query, run DFS to find path and sum values
3. For updates, simply modify the value array

### Code

```python
def solve_brute_force(n, values, edges, queries):
  """
  Brute force: DFS for each query.

  Time: O(q * n) - TLE for large inputs
  Space: O(n)
  """
  from collections import defaultdict

  adj = defaultdict(list)
  for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)

  def path_sum(target):
    """Find sum from root (1) to target using DFS."""
    def dfs(node, parent, current_sum):
      current_sum += values[node]
      if node == target:
        return current_sum
      for child in adj[node]:
        if child != parent:
          result = dfs(child, node, current_sum)
          if result is not None:
            return result
      return None
    return dfs(1, 0, 0)

  results = []
  for query in queries:
    if query[0] == 1:  # Update
      s, x = query[1], query[2]
      values[s] = x
    else:  # Query
      s = query[1]
      results.append(path_sum(s))

  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query traverses up to n nodes |
| Space | O(n) | Adjacency list and recursion stack |

### Why This Works (But Is Slow)

Correctness is guaranteed since we traverse the actual tree path. However, with q up to 2x10^5 queries and n up to 2x10^5 nodes, this gives 4x10^10 operations - far too slow.

---

## Solution 2: Optimal - Euler Tour + Segment Tree

### Key Insight

> **The Trick:** Flatten the tree with Euler tour. Add node value at entry, subtract at exit. Prefix sum at entry time = path sum from root!

### How Euler Tour Works for Path Sums

```
Tree:               Entry/Exit times:
      1             Node 1: entry=0, exit=9
     /|\            Node 2: entry=1, exit=2
    2 3 4           Node 3: entry=3, exit=8
     /|\            Node 4: entry=4, exit=5
    5 6 7           ...

Euler tour array (size 2n):
Position: 0   1   2   3   4   5   6   7   8   9
Event:   +1  +2  -2  +3  +4  -4  +5  -5  -3  -1
         ^entry    ^entry      ^entry
         1         3           5
```

**For query on node 5:**
- Entry time of node 5 = 6
- Prefix sum [0..6] = +1 -2 +2 +3 +4 -4 +5 = 1 + 3 + 5 = 9
- Wait, node 2 cancels out! Only ancestors remain!

### Why This Works

When computing prefix sum up to entry[u]:
- Ancestors of u: entered but NOT exited yet -> their +value counts
- Non-ancestors: either (not entered) or (entered AND exited) -> cancel out

### Algorithm

1. **Build tree and run DFS** to compute entry/exit times
2. **Initialize segment tree** with +value at entry, -value at exit
3. **For update(s, x):** Update both entry[s] and exit[s] positions
4. **For query(s):** Return prefix sum from 0 to entry[s]

### Dry Run Example

Input: n=5, values=[4,2,5,2,1], tree edges form: 1-2, 1-3, 3-4, 3-5

```
Tree structure:
      1(4)
     / \
   2(2) 3(5)
       / \
     4(2) 5(1)

Step 1: DFS to get entry/exit times
  DFS order: 1 -> 2 -> back -> 3 -> 4 -> back -> 5 -> back -> back

  Node:  1  2  3  4  5
  Entry: 0  1  3  4  6
  Exit:  9  2  8  5  7

Step 2: Build Euler array (size 2n = 10)
  Position: 0   1   2   3   4   5   6   7   8   9
  Value:   +4  +2  -2  +5  +2  -2  +1  -1  -5  -4
           ^1  ^2  ^2  ^3  ^4  ^4  ^5  ^5  ^3  ^1
          enter   exit

Step 3: Query - path sum to node 4 (entry time = 4)
  Prefix sum [0..4] = 4 + 2 + (-2) + 5 + 2 = 11
  Path: 1 -> 3 -> 4, values: 4 + 5 + 2 = 11  [Correct!]

Step 4: Update - change node 3 from 5 to 2
  Update position 3 (entry): +5 -> +2  (delta = -3)
  Update position 8 (exit):  -5 -> -2  (delta = +3)

Step 5: Query again - path sum to node 4
  Prefix sum [0..4] = 4 + 2 + (-2) + 2 + 2 = 8
  Path: 1 -> 3 -> 4, values: 4 + 2 + 2 = 8  [Correct!]
```

### Code (Python)

```python
import sys
from collections import defaultdict
input = sys.stdin.readline

def solve():
  n, q = map(int, input().split())
  values = [0] + list(map(int, input().split()))  # 1-indexed

  # Build adjacency list
  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  # Euler tour: compute entry and exit times
  entry = [0] * (n + 1)
  exit_time = [0] * (n + 1)
  euler = [0] * (2 * n)  # Euler tour array
  timer = [0]  # Use list for mutable reference in nested function

  def dfs(node, parent):
    entry[node] = timer[0]
    euler[timer[0]] = values[node]  # +value at entry
    timer[0] += 1

    for child in adj[node]:
      if child != parent:
        dfs(child, node)

    exit_time[node] = timer[0]
    euler[timer[0]] = -values[node]  # -value at exit
    timer[0] += 1

  dfs(1, 0)

  # Segment tree for range sum with point updates
  size = 2 * n
  tree = [0] * (4 * size)

  def build(node, start, end):
    if start == end:
      tree[node] = euler[start]
    else:
      mid = (start + end) // 2
      build(2 * node, start, mid)
      build(2 * node + 1, mid + 1, end)
      tree[node] = tree[2 * node] + tree[2 * node + 1]

  def update(node, start, end, idx, delta):
    if start == end:
      tree[node] += delta
    else:
      mid = (start + end) // 2
      if idx <= mid:
        update(2 * node, start, mid, idx, delta)
      else:
        update(2 * node + 1, mid + 1, end, idx, delta)
      tree[node] = tree[2 * node] + tree[2 * node + 1]

  def query(node, start, end, l, r):
    if r < start or end < l:
      return 0
    if l <= start and end <= r:
      return tree[node]
    mid = (start + end) // 2
    return query(2 * node, start, mid, l, r) + \
       query(2 * node + 1, mid + 1, end, l, r)

  build(1, 0, size - 1)

  # Process queries
  results = []
  for _ in range(q):
    query_line = list(map(int, input().split()))
    if query_line[0] == 1:  # Update
      s, x = query_line[1], query_line[2]
      old_val = values[s]
      delta = x - old_val
      values[s] = x
      # Update entry position (+delta) and exit position (-delta)
      update(1, 0, size - 1, entry[s], delta)
      update(1, 0, size - 1, exit_time[s], -delta)
    else:  # Query
      s = query_line[1]
      # Prefix sum from 0 to entry[s]
      results.append(query(1, 0, size - 1, 0, entry[s]))

  print('\n'.join(map(str, results)))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | Build O(n), each query/update O(log n) |
| Space | O(n) | Euler array and segment tree |

---

## Common Mistakes

### Mistake 1: Forgetting to Update Both Entry and Exit

**Problem:** The cancellation property breaks; non-ancestors will affect queries.
**Fix:** Always update both entry (+delta) and exit (-delta) positions.

### Mistake 2: Integer Overflow

**Problem:** Values up to 10^9, path up to 2x10^5 nodes -> sum can reach 2x10^14.
**Fix:** Use `long long` for all sum-related variables.

### Mistake 3: Off-by-One in Euler Array Size

**Problem:** Each node contributes two events (entry and exit).
**Fix:** Euler array must have size 2n.

### Mistake 4: Wrong Query Range

**Problem:** Including exit events of the target node and descendants.
**Fix:** Path sum = prefix sum ending at entry time.

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| Single node | n=1, query node 1 | Return value[1] | Trivial path |
| Root query | Query node 1 | Return value[1] | Path is just root |
| Deep tree (chain) | n nodes in a line | O(log n) per query | Euler tour handles any tree shape |
| Star graph | Root with n-1 leaves | Works correctly | Entry/exit times still valid |
| Large values | v[i] = 10^9 | Use long long | Sum can overflow int |
| Update to same value | Update v[s] = v[s] | No-op (delta=0) | Should handle gracefully |

---

## When to Use This Pattern

### Use Euler Tour + Segment Tree When:
- Path queries from root to any node (this problem)
- Subtree queries (sum/min/max of all nodes in subtree)
- Need both point updates and path/subtree queries
- Tree is static (edges don't change)

### Don't Use When:
- Path queries between arbitrary nodes u and v (use HLD or LCA + data structure)
- Tree structure changes dynamically (use Link-Cut Trees)
- Only need single path query without updates (simple DFS suffices)
- Memory is extremely constrained (Euler tour doubles space requirement)

### Pattern Recognition Checklist:
- [ ] Queries involve root-to-node paths? -> **Euler tour + prefix sums**
- [ ] Queries involve subtrees? -> **Euler tour + range queries**
- [ ] Queries involve arbitrary paths (u to v)? -> **HLD or LCA-based approach**
- [ ] Need updates on edges instead of nodes? -> **Map edges to child nodes**

---

## Visual Summary

```
Original Tree:          After Euler Tour:
      1
     / \                Position: 0  1  2  3  4  5  6  7  8  9
    2   3               Value:   +1 +2 -2 +3 +4 -4 +5 -5 -3 -1
       / \                       |  |     |  |     |
      4   5             entry:   1  2     3  4     5

Query(node 4) = prefix_sum[0..4] = 1 + 2 - 2 + 3 + 4 = 8
                                 = value[1] + value[3] + value[4]
                                 (node 2 cancels out!)
```

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subordinates (CSES 1674)](https://cses.fi/problemset/task/1674) | Basic subtree size with DFS |
| [Tree Diameter (CSES 1131)](https://cses.fi/problemset/task/1131) | Tree traversal fundamentals |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Path Queries II (CSES 2134)](https://cses.fi/problemset/task/2134) | Path between any two nodes (needs HLD) |
| [Subtree Queries (CSES 1137)](https://cses.fi/problemset/task/1137) | Subtree sums instead of path sums |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Path Queries II (CSES 2134)](https://cses.fi/problemset/task/2134) | Heavy-Light Decomposition |
| [Distance Queries (CSES 1135)](https://cses.fi/problemset/task/1135) | LCA for arbitrary path distances |

---

## Key Takeaways

1. **The Core Idea:** Euler tour linearizes the tree so path sums become prefix sums
2. **The Cancellation Trick:** +value at entry, -value at exit makes non-ancestors cancel
3. **Time Optimization:** O(n) per query -> O(log n) using segment tree
4. **Pattern:** This is the "Euler Tour Technique" for tree linearization

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why +value at entry and -value at exit gives correct path sums
- [ ] Implement Euler tour DFS to compute entry/exit times
- [ ] Build and query a segment tree for prefix sums
- [ ] Handle both update and query operations correctly
- [ ] Identify when Euler tour is applicable vs when HLD is needed

---

## Additional Resources

- [CP-Algorithms: Euler Tour Technique](https://cp-algorithms.com/graph/euler_path.html)
- [CSES Problem Set - Tree Algorithms](https://cses.fi/problemset/list/)
- [USACO Guide - Euler Tour Technique](https://usaco.guide/gold/tree-euler)
