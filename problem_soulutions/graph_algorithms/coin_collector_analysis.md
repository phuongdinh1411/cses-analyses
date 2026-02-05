---
layout: simple
title: "Coin Collector - SCC Condensation + DP on DAG"
permalink: /problem_soulutions/graph_algorithms/coin_collector_analysis
difficulty: Hard
tags: [graph, scc, dag, dp, topological-sort]
cses_link: https://cses.fi/problemset/task/1686
---

# Coin Collector

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Maximum coin collection on directed graph |
| Technique | SCC Condensation + DP on DAG |
| Time Complexity | O(n + m) |
| Space Complexity | O(n + m) |
| Key Insight | Condense SCCs, then DP in reverse topological order |

## Learning Goals

After solving this problem, you will understand:

1. **SCC Condensation**: How to collapse strongly connected components into single nodes
2. **DP on DAG**: Running dynamic programming on directed acyclic graphs
3. **Combining Graph Algorithms**: Using Kosaraju's/Tarjan's with topological sort and DP
4. **Graph Transformation**: Converting cyclic graphs to DAGs for easier processing

## Problem Statement

You have `n` rooms and `m` one-way tunnels. Each room contains a certain number of coins. You can start from any room and travel through tunnels, collecting coins from each room you visit (each room counted only once). Find the maximum number of coins you can collect.

**Input:**
- First line: n (rooms), m (tunnels)
- Second line: coins in each room (k1, k2, ..., kn)
- Next m lines: tunnel from room a to room b

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 x 10^5
- 1 <= ki <= 10^9

**Example:**
```
Input:
4 4
4 5 2 7
1 2
2 1
2 3
3 4

Output:
18
```

## Key Insight: SCC Condensation

**Critical Observation:** Within a Strongly Connected Component (SCC), you can reach ANY node from ANY other node. This means if you enter an SCC, you can collect ALL coins in that SCC.

This insight transforms the problem:
1. Find all SCCs
2. Treat each SCC as a single "super-node" with total coins = sum of all coins in SCC
3. The condensed graph is a DAG (no cycles between SCCs)
4. Find maximum path sum on this DAG

## Algorithm

### Step 1: Find SCCs using Kosaraju's Algorithm

Kosaraju's algorithm uses two DFS passes:
1. First DFS: Record finish times (add to stack when done)
2. Second DFS: Process nodes in reverse finish order on transposed graph

### Step 2: Condense the Graph

- Assign each node to its SCC ID
- For each SCC, compute total coins
- Build DAG: for each original edge (u, v), if scc[u] != scc[v], add edge scc[u] -> scc[v]

### Step 3: DP on DAG

Process SCCs in reverse topological order:

```
dp[scc] = coins[scc] + max(dp[child] for all children in DAG)
```

If no children: `dp[scc] = coins[scc]`

### Step 4: Answer

```
Answer = max(dp[scc]) for all SCCs
```

## Visual Diagram

### Original Graph
```
    [4]         [5]
     1 --------> 2
     ^           |
     |           |
     +-----------+
           |
           v
          [2]         [7]
           3 --------> 4
```
Nodes 1 and 2 form an SCC (can go 1->2->1).

### SCC Identification
```
SCC A: {1, 2}  coins = 4 + 5 = 9
SCC B: {3}     coins = 2
SCC C: {4}     coins = 7
```

### Condensed DAG
```
    [9]         [2]         [7]
     A --------> B --------> C
```

### DP Calculation (reverse topological order: C, B, A)
```
dp[C] = 7                    (no outgoing edges)
dp[B] = 2 + dp[C] = 2 + 7 = 9
dp[A] = 9 + dp[B] = 9 + 9 = 18

Answer = max(18, 9, 7) = 18
```

## Dry Run

**Input:**
```
n=4, m=4
coins = [4, 5, 2, 7]  (1-indexed: room 1 has 4 coins, etc.)
edges: 1->2, 2->1, 2->3, 3->4
```

**Step 1: First DFS (record finish order)**
```
Start DFS from node 1:
  Visit 1 -> Visit 2 -> Visit 3 -> Visit 4
  Finish 4, push to stack
  Finish 3, push to stack
  Back to 2: try 1 (already visiting, skip)
  Finish 2, push to stack
  Finish 1, push to stack

Stack (top to bottom): [1, 2, 3, 4]
```

**Step 2: Build transpose graph**
```
Original: 1->2, 2->1, 2->3, 3->4
Transpose: 2->1, 1->2, 3->2, 4->3
```

**Step 3: Second DFS (process in stack order on transpose)**
```
Pop 1: DFS on transpose
  Visit 1 -> Visit 2 -> (2's neighbor is 1, already visited)
  SCC 0: {1, 2}

Pop 2: already visited, skip

Pop 3: DFS on transpose
  Visit 3 -> (3's neighbor is 2, already visited)
  SCC 1: {3}

Pop 4: DFS on transpose
  Visit 4 -> (4's neighbor is 3, already visited)
  SCC 2: {4}
```

**Step 4: Build condensed graph**
```
scc_coins[0] = 4 + 5 = 9
scc_coins[1] = 2
scc_coins[2] = 7

Original edges -> DAG edges:
  1->2: same SCC, skip
  2->1: same SCC, skip
  2->3: SCC 0 -> SCC 1
  3->4: SCC 1 -> SCC 2

DAG: 0 -> 1 -> 2
```

**Step 5: DP in reverse topological order**
```
Topological order: [0, 1, 2]
Reverse: [2, 1, 0]

dp[2] = 7 (no outgoing)
dp[1] = 2 + max(dp[2]) = 2 + 7 = 9
dp[0] = 9 + max(dp[1]) = 9 + 9 = 18

Answer = max(dp[0], dp[1], dp[2]) = 18
```

## Python Implementation

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(200005)

def solve():
  input_data = sys.stdin.read().split()
  idx = 0
  n = int(input_data[idx]); idx += 1
  m = int(input_data[idx]); idx += 1

  coins = [0] * (n + 1)
  for i in range(1, n + 1):
    coins[i] = int(input_data[idx]); idx += 1

  # Build graph and transpose
  graph = defaultdict(list)
  transpose = defaultdict(list)

  for _ in range(m):
    a = int(input_data[idx]); idx += 1
    b = int(input_data[idx]); idx += 1
    graph[a].append(b)
    transpose[b].append(a)

  # Step 1: First DFS - get finish order
  visited = [False] * (n + 1)
  finish_stack = []

  def dfs1(node):
    visited[node] = True
    for neighbor in graph[node]:
      if not visited[neighbor]:
        dfs1(neighbor)
    finish_stack.append(node)

  for i in range(1, n + 1):
    if not visited[i]:
      dfs1(i)

  # Step 2: Second DFS on transpose - find SCCs
  visited = [False] * (n + 1)
  scc_id = [0] * (n + 1)
  scc_count = 0

  def dfs2(node, scc):
    visited[node] = True
    scc_id[node] = scc
    for neighbor in transpose[node]:
      if not visited[neighbor]:
        dfs2(neighbor, scc)

  while finish_stack:
    node = finish_stack.pop()
    if not visited[node]:
      dfs2(node, scc_count)
      scc_count += 1

  # Step 3: Build condensed DAG
  scc_coins = [0] * scc_count
  for i in range(1, n + 1):
    scc_coins[scc_id[i]] += coins[i]

  # Build DAG edges (use set to avoid duplicates)
  dag = defaultdict(set)
  for u in range(1, n + 1):
    for v in graph[u]:
      if scc_id[u] != scc_id[v]:
        dag[scc_id[u]].add(scc_id[v])

  # Step 4: DP on DAG
  # SCCs are numbered in reverse topological order by Kosaraju's
  # So process from scc_count-1 down to 0
  dp = [0] * scc_count

  for scc in range(scc_count - 1, -1, -1):
    dp[scc] = scc_coins[scc]
    for child in dag[scc]:
      dp[scc] = max(dp[scc], scc_coins[scc] + dp[child])

  print(max(dp))

solve()
```

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Not processing in reverse topological order | DP depends on children being computed first | Process from sinks to sources |
| Integer overflow | Coins up to 10^9, sum can exceed 32-bit | Use `long long` in C++ |
| Duplicate edges in DAG | Multiple edges between same SCCs waste time | Use set to deduplicate |
| Forgetting self-loops | A node can have edge to itself (still same SCC) | Check `scc[u] != scc[v]` |
| Wrong topological order | Kosaraju gives reverse topo order naturally | Process SCCs from highest ID to lowest |

## Why Kosaraju's Order Works

Kosaraju's algorithm assigns SCC IDs in reverse topological order:
- SCCs discovered first (higher IDs) have no outgoing edges to undiscovered SCCs
- This means if there's an edge from SCC A to SCC B in the DAG, then ID(A) < ID(B)
- Processing from highest to lowest ID = processing sinks before sources = correct DP order

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build graph | O(m) | O(n + m) |
| First DFS | O(n + m) | O(n) |
| Second DFS | O(n + m) | O(n) |
| Build DAG | O(m) | O(m) |
| DP on DAG | O(n + m) | O(n) |
| **Total** | **O(n + m)** | **O(n + m)** |

## Related Problems

- [CSES: Giant Pizza](https://cses.fi/problemset/task/1684) - 2-SAT with SCC
- [CSES: Planets and Kingdoms](https://cses.fi/problemset/task/1683) - Finding SCCs
- [CSES: Longest Flight Route](https://cses.fi/problemset/task/1680) - DP on DAG
