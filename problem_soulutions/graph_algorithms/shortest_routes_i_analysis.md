---
layout: analysis
title: "Shortest Routes I"
difficulty: Medium
tags: [graph, dijkstra, shortest-path, priority-queue, weighted-graph]
cses_link: https://cses.fi/problemset/task/1671
---

# Shortest Routes I - Dijkstra's Algorithm

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find shortest paths from city 1 to all cities |
| Input | n cities, m one-way flights with costs |
| Output | Minimum cost to reach each city from city 1 |
| Constraints | n <= 10^5, m <= 2*10^5, costs up to 10^9 |
| Core Algorithm | Dijkstra's Algorithm with Priority Queue |

## Learning Goals

After solving this problem, you will understand:
1. **Dijkstra's Algorithm** - The fundamental single-source shortest path algorithm
2. **Priority Queue (Min-Heap)** - Efficient selection of the next node to process
3. **Weighted Graph Traversal** - Why BFS fails and how Dijkstra handles weights
4. **Edge Relaxation** - The key operation that updates shortest distances

## Problem Statement

There are n cities and m flight connections. Each flight has a cost.
Find the minimum cost to travel from city 1 to every other city.

```
Input:
3 4           # 3 cities, 4 flights
1 2 6         # flight from 1 to 2, cost 6
1 3 2         # flight from 1 to 3, cost 2
3 2 3         # flight from 3 to 2, cost 3
1 2 4         # flight from 1 to 2, cost 4

Output:
0 5 2         # cost to reach city 1, 2, 3 from city 1
```

## Why BFS Doesn't Work Here

BFS finds shortest paths in **unweighted** graphs (or graphs where all edges have equal weight).

```
BFS assumes: All edges have equal cost (1 step = 1 cost)

Example where BFS fails:
    1 ---(10)--- 2
    |
   (1)
    |
    3 ---(1)---- 2

BFS path: 1 -> 2 (1 edge, cost 10)
Optimal:  1 -> 3 -> 2 (2 edges, cost 2)
```

**Key Insight**: With weighted edges, fewer edges does NOT mean shorter distance!

## Dijkstra's Key Insight

> Always process the closest unvisited node first.

This greedy choice works because:
- Once we process a node, we've found its shortest path
- We can never find a shorter path later (all remaining paths are longer)

**Requirement**: All edge weights must be NON-NEGATIVE.

## Algorithm: Dijkstra with Priority Queue

### Step-by-Step Process

```
1. Initialize:
   - dist[1] = 0 (start node)
   - dist[all others] = infinity
   - priority_queue = [(0, 1)]  # (distance, node)

2. While priority queue not empty:
   a. Pop node with SMALLEST distance
   b. If already processed, skip it
   c. Mark as processed
   d. For each neighbor:
      - Calculate new_dist = current_dist + edge_weight
      - If new_dist < dist[neighbor]:
        - Update dist[neighbor] = new_dist
        - Push (new_dist, neighbor) to queue

3. Return dist array
```

## Visual Diagram: Algorithm Progression

```
Example Graph:
    1 -----(6)-----> 2
    |                ^
   (2)              (3)
    |                |
    v                |
    3 ---------------+

Step 0: Initialize
+-------+-------+-------+

| Node  |   1   |   2   |   3   |
+-------+-------+-------+-------+

| dist  |   0   |  INF  |  INF  |
+-------+-------+-------+-------+
Priority Queue: [(0, 1)]

Step 1: Process node 1 (dist=0)
- Relax edge 1->2: dist[2] = min(INF, 0+6) = 6
- Relax edge 1->3: dist[3] = min(INF, 0+2) = 2
+-------+-------+-------+-------+

| dist  |   0   |   6   |   2   |
+-------+-------+-------+-------+
Priority Queue: [(2, 3), (6, 2)]

Step 2: Process node 3 (dist=2) <- smallest!
- Relax edge 3->2: dist[2] = min(6, 2+3) = 5  <- improved!
+-------+-------+-------+-------+

| dist  |   0   |   5   |   2   |
+-------+-------+-------+-------+
Priority Queue: [(5, 2), (6, 2)]

Step 3: Process node 2 (dist=5)
- No outgoing edges
+-------+-------+-------+-------+

| dist  |   0   |   5   |   2   |  <- FINAL
+-------+-------+-------+-------+

Step 4: Pop (6, 2) - already processed, skip!

Final Answer: [0, 5, 2]
```

## Detailed Dry Run

```
Input:
n=4, m=5
Edges: 1->2(2), 1->3(5), 2->3(1), 2->4(7), 3->4(3)

Graph visualization:
       (2)
    1 -----> 2
    |        | \
   (5)      (1) (7)
    |        |   \
    v        v    v
    3 <------+    4
    |             ^
    +----(3)------+

Initial State:
dist = [-, 0, INF, INF, INF]  (index 0 unused)
pq = [(0, 1)]
processed = {}

Iteration 1:
- Pop (0, 1)
- Process node 1
- Relax 1->2: dist[2] = 0+2 = 2, push (2, 2)
- Relax 1->3: dist[3] = 0+5 = 5, push (5, 3)
- dist = [-, 0, 2, 5, INF]
- pq = [(2, 2), (5, 3)]

Iteration 2:
- Pop (2, 2)
- Process node 2
- Relax 2->3: dist[3] = min(5, 2+1) = 3, push (3, 3)
- Relax 2->4: dist[4] = 2+7 = 9, push (9, 4)
- dist = [-, 0, 2, 3, 9]
- pq = [(3, 3), (5, 3), (9, 4)]

Iteration 3:
- Pop (3, 3)
- Process node 3
- Relax 3->4: dist[4] = min(9, 3+3) = 6, push (6, 4)
- dist = [-, 0, 2, 3, 6]
- pq = [(5, 3), (6, 4), (9, 4)]

Iteration 4:
- Pop (5, 3) - node 3 already processed, SKIP

Iteration 5:
- Pop (6, 4)
- Process node 4
- No outgoing edges
- dist = [-, 0, 2, 3, 6]

Iteration 6:
- Pop (9, 4) - node 4 already processed, SKIP

Final: dist = [0, 2, 3, 6]
```

## Python Implementation

```python
import heapq

def dijkstra(n, edges):
    """
    Dijkstra's algorithm for single-source shortest paths.

    Args:
        n: number of nodes (1-indexed)
        edges: list of (from, to, cost) tuples

    Returns:
        list of shortest distances from node 1 to all nodes
    """
    # Build adjacency list
    INF = float('inf')
    graph = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        graph[u].append((v, w))

    # Initialize distances
    dist = [INF] * (n + 1)
    dist[1] = 0

    # Min-heap: (distance, node)
    pq = [(0, 1)]
    processed = [False] * (n + 1)

    while pq:
        d, u = heapq.heappop(pq)

        # Skip if already processed
        if processed[u]:
            continue
        processed[u] = True

        # Relax all neighbors
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist[1:]  # Return distances for nodes 1 to n


def solve():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a, b, c))

    result = dijkstra(n, edges)
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    solve()
```

## Common Mistakes

### 1. Not Skipping Processed Nodes

```python
# WRONG - processes same node multiple times
while pq:
    d, u = heapq.heappop(pq)
    for v, w in graph[u]:  # Bug: may relax from outdated distance
        ...

# CORRECT - skip already processed nodes
while pq:
    d, u = heapq.heappop(pq)
    if processed[u]:  # Critical check!
        continue
    processed[u] = True
    ...
```

### 2. Using Max-Heap Instead of Min-Heap

```python
# Python's heapq is already a min-heap - no issue here
# But be careful with custom comparisons!
```

### 3. Integer Overflow

### 4. Forgetting to Handle Unreachable Nodes

```python
# If a node is unreachable, dist remains INF
# Make sure to handle this in output if needed
```

## Complexity Analysis

| Operation | Count | Cost | Total |
|-----------|-------|------|-------|
| Push to heap | O(m) | O(log n) | O(m log n) |
| Pop from heap | O(m) | O(log n) | O(m log n) |
| Process each node | O(n) | O(1) | O(n) |

**Time Complexity**: O((n + m) log n)
- Each edge causes at most one push operation
- Each pop takes O(log n)

**Space Complexity**: O(n + m)
- Adjacency list: O(m)
- Distance array: O(n)
- Priority queue: O(m) in worst case

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| Network Delay Time | LeetCode 743 | Same algorithm, find max of all distances |
| Cheapest Flights Within K Stops | LeetCode 787 | Limited number of edges allowed |
| Shortest Routes II | CSES | All-pairs shortest path (Floyd-Warshall) |
| Flight Discount | CSES | One edge can be halved |

## Key Takeaways

1. **Dijkstra = BFS with Priority Queue** for weighted graphs
2. **Greedy Choice**: Always process the closest unvisited node
3. **Min-Heap is Essential**: Pop smallest distance, not largest
4. **Skip Processed Nodes**: Critical for correctness and efficiency
5. **Non-negative Weights Only**: Use Bellman-Ford for negative weights
