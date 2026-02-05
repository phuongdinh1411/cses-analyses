---
layout: simple
title: "Strongly Connected Components"
permalink: /problem_soulutions/graph_algorithms/strongly_connected_components_analysis
difficulty: Hard
tags: [graph, scc, kosaraju, tarjan, dfs]
cses_link: https://cses.fi/problemset/task/1682
---

# Strongly Connected Components

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find all SCCs in a directed graph and label each node |
| Input | n nodes, m directed edges |
| Output | Number of SCCs and component ID for each node |
| Constraints | 1 <= n <= 100,000 and 1 <= m <= 200,000 |
| Time Limit | 1 second |
| Difficulty | Hard |

## Learning Goals

By completing this problem, you will understand:
1. **SCC Definition**: What makes a strongly connected component
2. **Kosaraju's Algorithm**: Two-pass DFS approach for finding SCCs
3. **Graph Reversal**: Why reversing edges helps identify components
4. **Finish Time Ordering**: How DFS finish times reveal SCC structure

## Problem Statement

Given a directed graph with n nodes and m edges, find:
1. The number of strongly connected components
2. For each node, which component it belongs to

**Example Input:**
```
n=7, m=8
Edges: 1->2, 2->3, 3->1, 3->4, 4->5, 5->6, 6->4, 7->6
```

**Example Output:**
```
3 components
Node labels: [1, 1, 1, 2, 2, 2, 3]
```

## What is a Strongly Connected Component?

A **Strongly Connected Component (SCC)** is a maximal set of vertices where every vertex is reachable from every other vertex within that set.

**Key properties:**
- For any two nodes u and v in the same SCC: u can reach v AND v can reach u
- "Maximal" means we cannot add any more nodes while maintaining this property
- Every directed graph can be uniquely partitioned into SCCs

```
Example: Which nodes form SCCs?

    1 --> 2
    ^     |
    |     v
    +---- 3 --> 4 --> 5
              ^     |
              |     v
              +---- 6 <-- 7

SCC 1: {1, 2, 3}  - All nodes can reach each other via the cycle
SCC 2: {4, 5, 6}  - All nodes can reach each other via the cycle
SCC 3: {7}        - Single node (can only reach itself trivially)
```

## Kosaraju's Algorithm

Kosaraju's algorithm finds all SCCs in O(V + E) time using two DFS passes.

### Algorithm Overview

```
KOSARAJU'S ALGORITHM:

Pass 1: DFS on original graph
        Record finish times (use a stack)

Pass 2: DFS on REVERSED graph
        Process nodes in decreasing finish time order
        Each DFS tree = one SCC
```

### Step-by-Step Explanation

**Pass 1: Record Finish Times**
- Run DFS on the original graph
- When a node finishes (all descendants explored), push it to a stack
- The stack now contains nodes in order of decreasing finish time (top = latest finish)

**Pass 2: Find SCCs on Reversed Graph**
- Reverse all edges in the graph
- Pop nodes from stack (decreasing finish time order)
- Run DFS from each unvisited node on the reversed graph
- All nodes reached in one DFS form one SCC

### Why Does Kosaraju's Algorithm Work?

The key insight is about **finish times** and **reachability**.

```
INTUITION:

If node A finishes after node B in Pass 1:
  - Either A can reach B (A started before B and explored B)
  - Or A and B are in different parts of the graph

In the REVERSED graph:
  - If B could reach A in original, now A can reach B
  - Nodes in same SCC can still reach each other (cycles reverse to cycles)

Processing by decreasing finish time ensures:
  - We start DFS from a "root" of an SCC
  - We cannot escape to another SCC (edges going out become edges coming in)
```

**Formal reasoning:**
1. If u and v are in the same SCC, they remain connected in the reversed graph
2. If u finishes after v and they are in different SCCs, then in the reversed graph, v cannot reach u
3. Therefore, starting from nodes with highest finish times isolates each SCC

## Visual Diagram: Original vs Reversed Graph

```
ORIGINAL GRAPH:                    REVERSED GRAPH:

    1 -----> 2                         1 <----- 2
    ^        |                         |        ^
    |        v                         v        |
    +------- 3 -----> 4                +------- 3 <----- 4
                      |                                  ^
                      v                                  |
                      5 -----> 6                         5 <----- 6
                      ^        |                         |        ^
                      |        v                         v        |
                      +------- 7                         +------- 7

Pass 1 on Original:                Pass 2 on Reversed:
DFS order fills stack              Pop from stack, DFS on reversed

Finish order (bottom to top):      Processing order:
Stack: [7, 6, 5, 4, 3, 2, 1]      1 -> finds {1,2,3}
       (1 finishes last)          4 -> finds {4,5,7}
                                  6 -> finds {6}

Result: 3 SCCs: {1,2,3}, {4,5,7}, {6}
```

## Dry Run Example

Let us trace through with a concrete example:

```
Graph: n=6, edges: 1->2, 2->3, 3->1, 2->4, 4->5, 5->6, 6->4

Adjacency list (original):
1: [2]
2: [3, 4]
3: [1]
4: [5]
5: [6]
6: [4]

PASS 1: DFS on original, record finish times
----------------------------------------
Start DFS from node 1:
  Visit 1 -> Visit 2 -> Visit 3 -> (1 already visited)
           -> Visit 4 -> Visit 5 -> Visit 6 -> (4 already visited)
                         Finish 6, push to stack
                       Finish 5, push to stack
                     Finish 4, push to stack
           Finish 3, push to stack
         Finish 2, push to stack
       Finish 1, push to stack

Stack (top to bottom): [1, 2, 3, 4, 5, 6]

PASS 2: DFS on reversed graph in stack order
--------------------------------------------
Reversed adjacency list:
1: [3]
2: [1]
3: [2]
4: [6, 2]
5: [4]
6: [5]

Pop 1: DFS from 1 on reversed graph
  Visit 1 -> Visit 3 -> Visit 2 -> (1 already visited)
  SCC #1 = {1, 2, 3}

Pop 2: Already visited, skip
Pop 3: Already visited, skip

Pop 4: DFS from 4 on reversed graph
  Visit 4 -> Visit 6 -> Visit 5 -> (4 already visited)
  SCC #2 = {4, 5, 6}

Pop 5: Already visited, skip
Pop 6: Already visited, skip

RESULT: 2 SCCs
  Component 1: {1, 2, 3}
  Component 2: {4, 5, 6}
```

## Python Implementation

```python
import sys
from collections import defaultdict

sys.setrecursionlimit(200001)

def find_sccs(n: int, edges: list) -> tuple:
 """
 Find strongly connected components using Kosaraju's algorithm.

 Args:
  n: Number of nodes (1-indexed)
  edges: List of (u, v) directed edges

 Returns:
  (num_sccs, component_id) where component_id[i] is the SCC of node i
 """
 # Build adjacency lists
 graph = defaultdict(list)      # Original graph
 reversed_graph = defaultdict(list)  # Reversed graph

 for u, v in edges:
  graph[u].append(v)
  reversed_graph[v].append(u)

 # Pass 1: DFS on original graph, record finish order
 visited = [False] * (n + 1)
 finish_stack = []

 def dfs_pass1(node):
  visited[node] = True
  for neighbor in graph[node]:
   if not visited[neighbor]:
    dfs_pass1(neighbor)
  finish_stack.append(node)

 for node in range(1, n + 1):
  if not visited[node]:
   dfs_pass1(node)

 # Pass 2: DFS on reversed graph in decreasing finish time order
 visited = [False] * (n + 1)
 component_id = [0] * (n + 1)
 current_scc = 0

 def dfs_pass2(node, scc_id):
  visited[node] = True
  component_id[node] = scc_id
  for neighbor in reversed_graph[node]:
   if not visited[neighbor]:
    dfs_pass2(neighbor, scc_id)

 while finish_stack:
  node = finish_stack.pop()
  if not visited[node]:
   current_scc += 1
   dfs_pass2(node, current_scc)

 return current_scc, component_id

# Read input
n, m = map(int, input().split())
edges = []
for _ in range(m):
 u, v = map(int, input().split())
 edges.append((u, v))

# Find SCCs
num_sccs, component_id = find_sccs(n, edges)

# Output
print(num_sccs)
print(' '.join(map(str, component_id[1:])))
```

## Brief Overview: Tarjan's Algorithm

Tarjan's algorithm finds SCCs in a single DFS pass using **low-link values**.

```
TARJAN'S ALGORITHM (Single Pass):

For each node, track:
  - discovery_time[v]: When v was first visited
  - low_link[v]: Smallest discovery time reachable from v's subtree

Key idea:
  - A node v is the "root" of an SCC if low_link[v] == discovery_time[v]
  - Use a stack to track current SCC candidates
  - When we find a root, pop all nodes until v from stack -> one SCC

Advantage: Single pass O(V + E)
Disadvantage: More complex to understand and implement
```

**When to use which:**
- Kosaraju's: Easier to understand, good for learning
- Tarjan's: Slightly more efficient (single pass), preferred in competitions

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Forgetting to reverse the graph | Pass 2 runs on original graph, gives wrong SCCs | Build reversed adjacency list explicitly |
| Wrong order in Pass 2 | Processing nodes in wrong order breaks the algorithm | Use stack from Pass 1, pop in order |
| 0-indexed vs 1-indexed confusion | Off-by-one errors, missing nodes | Be consistent, CSES uses 1-indexed |
| Stack overflow on large graphs | Recursion limit exceeded | Increase recursion limit or use iterative DFS |
| Not handling disconnected graphs | Missing some nodes entirely | Start DFS from all unvisited nodes in Pass 1 |

## Applications of SCCs

**1. 2-SAT (Boolean Satisfiability)**
- Model implications as directed graph
- Variables in same SCC must have same truth value
- If x and NOT x in same SCC, no solution exists

**2. DAG of SCCs (Condensation Graph)**
- Contract each SCC to a single node
- Result is a DAG (no cycles between SCCs)
- Useful for problems requiring topological ordering

**3. Reachability Queries**
- Nodes in same SCC can all reach each other
- Condense to DAG, then answer reachability on DAG

**4. Finding Bridges and Articulation Points**
- Related concepts in connectivity analysis
- SCC algorithms share ideas with bridge-finding

## Complexity Analysis

| Aspect | Kosaraju's | Tarjan's |
|--------|-----------|----------|
| Time | O(V + E) | O(V + E) |
| Space | O(V + E) | O(V) |
| DFS Passes | 2 | 1 |
| Extra Space | Reversed graph | Stack + arrays |

Both algorithms are optimal for finding SCCs. Choose based on implementation preference.

## Summary

1. **SCC** = Maximal set where every node reaches every other node
2. **Kosaraju's Algorithm**: Two-pass DFS approach
   - Pass 1: Record finish times on original graph
   - Pass 2: DFS on reversed graph in decreasing finish time order
3. **Key insight**: Finish time ordering + graph reversal isolates SCCs
4. **Complexity**: O(V + E) time and space
5. **Applications**: 2-SAT, condensation graphs, reachability analysis
