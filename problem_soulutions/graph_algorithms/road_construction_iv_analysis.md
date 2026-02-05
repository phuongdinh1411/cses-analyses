---
title: "Road Construction IV - Connectivity Queries"
cses_link: https://cses.fi/problemset/task/1678
category: Graph Algorithms
difficulty: Medium
---

# Road Construction IV - Connectivity Queries

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Answer queries about whether two cities are connected |
| Input | n cities, m roads, q connectivity queries |
| Output | For each query: "YES" if connected, "NO" otherwise |
| Constraints | 1 <= n, m, q <= 2*10^5 |
| Key Technique | Union-Find for connectivity queries |

## Problem Description

Given n cities, m roads connecting them, and q queries asking if two cities are in the same connected component.

**Example:**
```
Input:
5 3 3
1 2
3 4
1 3
1 4
2 5
1 5

Output:
YES
NO
NO

Explanation:
Roads create components: {1,2,3,4} and {5}
Query (1,4): Both in {1,2,3,4} -> YES
Query (2,5): 2 in {1,2,3,4}, 5 in {5} -> NO
Query (1,5): 1 in {1,2,3,4}, 5 in {5} -> NO
```

## Algorithm: Union-Find for Connectivity

**Key Insight:** After building all roads, connectivity queries reduce to checking if two nodes have the same root in Union-Find.

**Two-Phase Approach:**
1. **Build Phase:** Process all roads, building the Union-Find structure
2. **Query Phase:** For each query (a, b), check if find(a) == find(b)

```
Phase 1 - Build Union-Find:
Roads: (1,2), (3,4), (1,3)

Step 1: union(1,2) -> {1,2}
Step 2: union(3,4) -> {3,4}
Step 3: union(1,3) -> {1,2,3,4}

Phase 2 - Answer Queries:
Query (1,4): find(1)=1, find(4)=1 -> YES
Query (2,5): find(2)=1, find(5)=5 -> NO
```

## Implementation

### Python Solution
```python
import sys
from sys import stdin

def solve():
  input = stdin.readline
  n, m, q = map(int, input().split())

  parent = list(range(n + 1))
  rank = [0] * (n + 1)

  def find(x):
    if parent[x] != x:
      parent[x] = find(parent[x])
    return parent[x]

  def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
      return

    if rank[ra] < rank[rb]:
      ra, rb = rb, ra
    parent[rb] = ra
    if rank[ra] == rank[rb]:
      rank[ra] += 1

  # Build phase: process all roads
  for _ in range(m):
    a, b = map(int, input().split())
    union(a, b)

  # Query phase: answer connectivity queries
  result = []
  for _ in range(q):
    a, b = map(int, input().split())
    if find(a) == find(b):
      result.append("YES")
    else:
      result.append("NO")

  print('\n'.join(result))

solve()
```

### Complexity Analysis

| Phase | Time | Space |
|-------|------|-------|
| Initialization | O(n) | O(n) |
| Building (m roads) | O(m * alpha(n)) | - |
| Queries (q queries) | O(q * alpha(n)) | - |
| **Total** | **O(n + (m+q) * alpha(n))** | **O(n)** |

## Comparison with Other Approaches

| Approach | Build Time | Query Time | Space |
|----------|-----------|------------|-------|
| Union-Find | O(m * alpha(n)) | O(alpha(n)) | O(n) |
| BFS/DFS per query | O(m) | O(n + m) | O(n) |
| Precompute all pairs | O(n^2) | O(1) | O(n^2) |

Union-Find is optimal when queries are many.

## Visual Example

```
Graph with 6 nodes and roads: (1,2), (2,3), (4,5)

Initial:
[1] [2] [3] [4] [5] [6]

After (1,2):
    2
   /
  1    [3] [4] [5] [6]

After (2,3):
    2
   / \
  1   3   [4] [5] [6]

After (4,5):
    2         5
   / \        |
  1   3       4    [6]

Final components: {1,2,3}, {4,5}, {6}

Queries:
- (1,3): find(1)=2, find(3)=2 -> YES
- (1,4): find(1)=2, find(4)=5 -> NO
- (4,5): find(4)=5, find(5)=5 -> YES
- (1,6): find(1)=2, find(6)=6 -> NO
```

## Common Mistakes

1. **Querying before building:** Must process all roads before answering queries
2. **Not using path compression:** Leads to TLE on large inputs
3. **Wrong indexing:** Nodes are typically 1-indexed
4. **Output format:** "YES"/"NO" vs "yes"/"no" vs "1"/"0"
5. **Self-loops:** A node is always connected to itself (find(a) == find(a))

## Variations

### Online vs Offline

This problem is **offline** (all roads known before queries). For **online** problems where roads and queries are interleaved, Union-Find still works perfectly.

### With Edge Deletions

If roads can be deleted, Union-Find doesn't support efficient deletion. Consider:
- Link-Cut Trees for dynamic connectivity
- Offline processing with time-based segments

## Key Takeaways

- Union-Find is the standard tool for connectivity queries
- Path compression makes queries nearly O(1)
- Separate build and query phases for clarity
- Connected means same root in Union-Find structure
- This pattern appears frequently: build a structure, then answer queries
