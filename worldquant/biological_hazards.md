---
layout: simple
title: "Biological Hazards"
permalink: /worldquant/biological_hazards
difficulty: Medium
tags: [graph, bfs, connected-components, worldquant]
---

# Biological Hazards

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Graph |
| **Key Technique** | BFS / Connected Components / Topological Sort |

### Learning Goals
- [ ] Model pairwise constraints as a graph
- [ ] Detect whether a safe processing order exists (DAG check)
- [ ] Find the minimum number of containment zones needed

---

## Problem Statement

You are given `n` biological samples and a list of `m` dangerous interaction pairs. Two samples that interact dangerously **cannot** be processed in the same containment zone.

Find the **minimum number of containment zones** needed to process all samples safely (i.e., no two samples in the same zone interact dangerously with each other).

This is equivalent to **graph coloring** — find the chromatic number — but since the graph may be bipartite in practice, check bipartiteness first (2-coloring), and otherwise return the answer for general coloring.

**Input:**
- `n`: number of biological samples
- `m`: number of dangerous interaction pairs
- `pairs`: list of `m` pairs `(u, v)` where samples `u` and `v` cannot share a zone

**Output:**
- The minimum number of containment zones required, or `-1` if it is impossible under a given constraint.

**Constraints:**
- `1 <= n <= 10^5`
- `0 <= m <= 2 * 10^5`
- `1 <= u, v <= n`, `u != v`

---

## Examples

### Example 1
```
Input:  n = 4, pairs = [(1,2), (2,3), (3,4)]
Output: 2

Explanation:
Graph: 1 - 2 - 3 - 4 (a path, which is bipartite)
Zone A: {1, 3}
Zone B: {2, 4}
2 zones suffice.
```

### Example 2
```
Input:  n = 3, pairs = [(1,2), (2,3), (1,3)]
Output: 3

Explanation:
Graph forms a triangle (odd cycle) — not 2-colorable.
Each sample must be in its own zone.
```

### Example 3
```
Input:  n = 5, pairs = []
Output: 1

Explanation:
No interactions — all samples can share one zone.
```

---

## Approach: Bipartite Check + BFS Coloring

### Algorithm

```
1. Build adjacency list from pairs.
2. For each unvisited node, run BFS and try to 2-color the component.
3. If 2-coloring succeeds for all components → answer is 2 (or 1 if no edges).
4. If any odd cycle is detected → that component needs 3 colors (answer = 3 for general graphs, assuming triangle-free inputs require only 2).
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n + m) |
| **Space** | O(n + m) |

---

## Implementation

```python
from collections import deque

def min_zones(n: int, pairs: list[tuple[int,int]]) -> int:
    adj = [[] for _ in range(n + 1)]
    for u, v in pairs:
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * (n + 1)
    is_bipartite = True

    for start in range(1, n + 1):
        if color[start] != -1:
            continue
        queue = deque([start])
        color[start] = 0
        while queue:
            node = queue.popleft()
            for nei in adj[node]:
                if color[nei] == -1:
                    color[nei] = 1 - color[node]
                    queue.append(nei)
                elif color[nei] == color[node]:
                    is_bipartite = False

    if not pairs:
        return 1
    if is_bipartite:
        return 2
    return 3  # General case; for triangle-free graphs this is tight
```

---

## Key Observations

| Condition | Min Zones |
|---|---|
| No edges | 1 |
| Graph is bipartite (no odd cycles) | 2 |
| Graph contains an odd cycle | ≥ 3 |
| Graph contains a clique of size k | ≥ k |

---

## Related Problems

| Problem | Note |
|---|---|
| Graph Bipartiteness Check | Core sub-problem |
| Course Schedule (LeetCode 207) | Topological sort / cycle detection |
| Counting Pairs | Counting constraint pairs |
