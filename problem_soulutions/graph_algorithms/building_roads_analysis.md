---
layout: problem
title: "Building Roads"
difficulty: Easy
tags: [graph, union-find, dsu, connected-components]
cses_link: https://cses.fi/problemset/task/1666
---

# Building Roads

## Problem Overview

| Aspect | Details |
|--------|---------|
| Source | CSES Problem Set |
| Category | Graph Algorithms |
| Difficulty | Easy |
| Key Technique | Union-Find (Disjoint Set Union) |
| Time Complexity | O(n + m * alpha(n)) where alpha is inverse Ackermann |
| Space Complexity | O(n) |

## Learning Goals

By the end of this problem, you will understand:

1. **Union-Find Data Structure**: How to efficiently track and merge disjoint sets
2. **Counting Connected Components**: Using Union-Find to count separate groups in a graph
3. **Path Compression**: Optimization technique that flattens the tree structure during find operations
4. **Union by Rank**: Optimization technique that attaches smaller trees under larger trees

## Problem Statement

Byteland has `n` cities and `m` roads between them. Unfortunately, the roads do not currently connect all cities. Your task is to determine the minimum number of new roads required to connect all cities.

**Input:**
- First line: two integers `n` and `m` (number of cities and roads)
- Next `m` lines: two integers `a` and `b` describing a road between cities `a` and `b`

**Output:**
- First line: minimum number of new roads `k`
- Next `k` lines: description of new roads (any valid solution)

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 * 10^5
- Cities are numbered 1 to n

**Example:**

```
Input:
4 2
1 2
3 4

Output:
1
2 3
```

**Explanation:** Cities {1, 2} form one component and {3, 4} form another. We need exactly 1 road to connect them. Road (2, 3) is one valid solution; (1, 3), (1, 4), or (2, 4) would also work.

## Key Insight

The minimum number of roads needed equals **(number of connected components - 1)**.

Why? Each new road can connect at most two previously disconnected components. To merge `k` components into one, we need exactly `k - 1` connections (like linking `k` islands with `k - 1` bridges).

To build the roads, simply pick one representative city from each component and chain them together.

## Union-Find Explained

Union-Find (also called Disjoint Set Union or DSU) is a data structure that tracks elements partitioned into disjoint sets. It supports two operations:

### find(x): Find the root of x's component

```
find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])   # Path compression
    return parent[x]
```

Path compression flattens the tree by making every node point directly to the root during traversal.

### union(x, y): Merge two components

```
union(x, y):
    root_x = find(x)
    root_y = find(y)
    if root_x == root_y:
        return  # Already in same component

    # Union by rank: attach smaller tree under larger
    if rank[root_x] < rank[root_y]:
        parent[root_x] = root_y
    elif rank[root_x] > rank[root_y]:
        parent[root_y] = root_x
    else:
        parent[root_y] = root_x
        rank[root_x] += 1
```

## Algorithm

1. Initialize Union-Find with n cities (each city is its own component)
2. For each existing road (a, b), call union(a, b)
3. Count distinct components by finding unique roots
4. Output (components - 1) roads, connecting representative cities

## Union-Find Implementation

```
class UnionFind:
    def __init__(self, n):
        # parent[i] = parent of node i (initially itself)
        self.parent = [i for i in range(n + 1)]
        # rank[i] = upper bound on height of subtree rooted at i
        self.rank = [0] * (n + 1)

    def find(self, x):
        # Find root with path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # Merge components containing x and y
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already connected

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True  # Successfully merged
```

## Visual Diagram: Union Operations

```
Initial State (4 cities, no roads):
  parent: [_, 1, 2, 3, 4]   (1-indexed, ignore index 0)

  1     2     3     4       <- Each city is its own root
  |     |     |     |

After union(1, 2) - Road between city 1 and 2:
  parent: [_, 1, 1, 3, 4]

    1         3     4
   /
  2

After union(3, 4) - Road between city 3 and 4:
  parent: [_, 1, 1, 3, 3]

    1           3
   /           /
  2           4

Components: {1, 2} and {3, 4}
Component count: 2
Roads needed: 2 - 1 = 1

After adding road (2, 3):
  find(2) = 1, find(3) = 3
  union(1, 3)
  parent: [_, 1, 1, 1, 3]

      1
     / \
    2   3
        |
        4

Path compression on find(4):
  find(4) -> find(3) -> find(1) = 1
  parent[4] = 1, parent[3] = 1

      1
    / | \
   2  3  4     <- Flattened tree!
```

## Dry Run

**Input:** n=4, m=2, roads=[(1,2), (3,4)]

| Step | Operation | parent[] | Components | Notes |
|------|-----------|----------|------------|-------|
| 0 | Initialize | [_, 1, 2, 3, 4] | 4 | Each city is own root |
| 1 | union(1, 2) | [_, 1, 1, 3, 4] | 3 | City 2 joins city 1 |
| 2 | union(3, 4) | [_, 1, 1, 3, 3] | 2 | City 4 joins city 3 |
| 3 | Count roots | - | 2 | Roots: {1, 3} |
| 4 | Roads needed | - | - | 2 - 1 = 1 |

**Output:** Need 1 road. Connect representative cities: (1, 3) or (2, 3) etc.

## Python Solution

```python
import sys
from sys import stdin

def solve():
 input = stdin.readline
 n, m = map(int, input().split())

 # Union-Find with path compression and union by rank
 parent = list(range(n + 1))
 rank = [0] * (n + 1)

 def find(x):
  if parent[x] != x:
   parent[x] = find(parent[x])
  return parent[x]

 def union(x, y):
  rx, ry = find(x), find(y)
  if rx == ry:
   return
  if rank[rx] < rank[ry]:
   rx, ry = ry, rx
  parent[ry] = rx
  if rank[rx] == rank[ry]:
   rank[rx] += 1

 # Process existing roads
 for _ in range(m):
  a, b = map(int, input().split())
  union(a, b)

 # Find all component representatives
 components = []
 for i in range(1, n + 1):
  if find(i) == i:
   components.append(i)

 # Output roads connecting components
 k = len(components) - 1
 print(k)
 for i in range(k):
  print(components[i], components[i + 1])

if __name__ == "__main__":
 sys.setrecursionlimit(200005)
 solve()
```

## Why Union-Find vs DFS?

| Aspect | Union-Find | DFS/BFS |
|--------|------------|---------|
| **Time Complexity** | O(n + m * alpha(n)) ~ O(n + m) | O(n + m) |
| **Space Complexity** | O(n) | O(n + m) for adjacency list |
| **Implementation** | Slightly more code | Simpler |
| **Dynamic Updates** | Excellent - can add edges incrementally | Poor - need full recomputation |
| **Query "Are x,y connected?"** | O(alpha(n)) after preprocessing | O(n + m) each time |

**When to use Union-Find:**
- Need to answer many connectivity queries
- Edges arrive dynamically (online)
- Need to count/track components as edges are added

**When to use DFS:**
- One-time component counting
- Need to enumerate all nodes in each component
- Simpler implementation is preferred

For this problem, both approaches work well. Union-Find shines if we need to handle dynamic road construction queries.

## Common Mistakes

1. **Forgetting Path Compression**
   - Without it, find() can be O(n) in worst case
   - Always update parent during find: `parent[x] = find(parent[x])`

2. **1-indexed vs 0-indexed Arrays**
   - CSES uses 1-indexed cities
   - Make sure parent array has size n+1, not n
   - Loop from 1 to n, not 0 to n-1

3. **Not Handling Single City Case**
   - If n=1, output should be 0 roads (already connected)
   - Formula still works: 1 component - 1 = 0 roads

4. **Incorrect Union by Rank**
   - Only increment rank when merging equal-rank trees
   - Rank is upper bound on height, not exact count

5. **Stack Overflow with Recursion**
   - For large n, recursive find() may overflow
   - Use iterative version or increase recursion limit

## Related Problems

| Problem | Platform | Similarity |
|---------|----------|------------|
| [Number of Connected Components in an Undirected Graph](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | LeetCode | Direct application of Union-Find |
| [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | LeetCode | Find edge that creates a cycle |
| [Road Construction](https://cses.fi/problemset/task/1676) | CSES | Track component count dynamically |
| [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) | LeetCode | Check if graph forms a valid tree |
