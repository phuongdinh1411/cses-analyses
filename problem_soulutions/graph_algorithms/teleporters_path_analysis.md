---
difficulty: Medium
tags: [graph, eulerian-path, hierholzer, dfs]
cses_link: https://cses.fi/problemset/task/1693
---

# Teleporters Path

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find path using each teleporter exactly once |
| Algorithm | Hierholzer's Algorithm for Eulerian Path |
| Time Complexity | O(n + m) |
| Space Complexity | O(n + m) |
| Key Insight | DFS with path construction on backtracking |

## Learning Goals

After completing this problem, you should understand:

1. **Eulerian Path vs Eulerian Circuit**
   - Eulerian Path: visits every edge exactly once
   - Eulerian Circuit: Eulerian path that starts and ends at the same vertex

2. **Existence Conditions for Directed Graphs**
   - When an Eulerian path exists based on vertex degrees

3. **Hierholzer's Algorithm**
   - Efficient O(m) algorithm to construct the path

## Problem Statement

A game has `n` levels (numbered 1 to n) and `m` teleporters. Each teleporter is a one-way connection from level `a` to level `b`.

**Task**: Find a route from level 1 to level n that uses each teleporter exactly once.

**Input**:
- First line: integers n and m
- Next m lines: teleporter connections (a, b)

**Output**:
- The path as space-separated level numbers, or "IMPOSSIBLE"

**Constraints**:
- 2 <= n <= 10^5
- 1 <= m <= 2 * 10^5

## Eulerian Path Existence Conditions

For a directed graph, an Eulerian path exists if and only if:

```
Condition 1: At most ONE vertex has out_degree - in_degree = 1
             (This vertex must be the START)

Condition 2: At most ONE vertex has in_degree - out_degree = 1
             (This vertex must be the END)

Condition 3: All OTHER vertices have in_degree = out_degree

Condition 4: The graph is weakly connected
             (All vertices with edges are reachable)
```

### Special Requirements for This Problem

Since we must start at vertex 1 and end at vertex n:

| Vertex | Required Condition |
|--------|-------------------|
| Vertex 1 | out_degree - in_degree = 1 (start vertex) |
| Vertex n | in_degree - out_degree = 1 (end vertex) |
| Others | in_degree = out_degree |

If the graph has an Eulerian circuit instead (all vertices balanced), we cannot use it because it would require start = end, but we need start = 1, end = n.

## Hierholzer's Algorithm

The key insight is to build the path during DFS backtracking:

```
Algorithm Hierholzer(start):
    1. Initialize empty path
    2. DFS from start vertex:
       - While current vertex has unused edges:
           - Pick any unused edge (u, v)
           - Mark edge as used
           - Recursively DFS from v
       - When no more edges: ADD current vertex to path
    3. Reverse the path (built backwards during backtracking)
```

**Why add on backtracking?** A vertex is added to the path only when all its outgoing edges have been used, ensuring we don't get stuck.

## Visual Diagram

```
Example: n=5, m=6
Teleporters: 1->2, 2->3, 3->1, 1->4, 4->5, 5->3

Graph:
          +---+
          | 1 |----+
          +---+    |
         /    \    |
        v      v   |
      +---+  +---+ |
      | 2 |  | 4 | |
      +---+  +---+ |
        |      |   |
        v      v   |
      +---+  +---+ |
      | 3 |<-| 5 | |
      +---+  +---+ |
        |          |
        +----------+

Degree Analysis:
Vertex | in_degree | out_degree | difference
-------|-----------|------------|------------
   1   |     1     |     2      |    +1 (START)
   2   |     1     |     1      |     0
   3   |     2     |     1      |    -1 (END... but we need n=5!)
   4   |     1     |     1      |     0
   5   |     1     |     1      |     0

This example has NO valid path (end should be vertex 5, not 3)
```

**Valid Example**: n=4, m=4, edges: 1->2, 2->3, 3->4, 1->3

```
      +---+
      | 1 |
      +---+
      /   \
     v     v
   +---+  +---+
   | 2 |->| 3 |
   +---+  +---+
            |
            v
          +---+
          | 4 |
          +---+

Vertex | in | out | diff
-------|----|----|-----
   1   |  0 |  2 | +1 (START - correct!)
   2   |  1 |  1 |  0
   3   |  2 |  1 | -1 (... but end should be 4)

Still invalid! Let's use: 1->2, 2->3, 3->4, 2->4

Vertex | in | out | diff
-------|----|----|-----
   1   |  0 |  1 | +1 (START)
   2   |  1 |  2 | +1 (INVALID - two starts!)
```

**Correct Valid Example**: n=4, m=3, edges: 1->2, 2->3, 3->4
```
Path: 1 -> 2 -> 3 -> 4
```

## Dry Run

```
Input: n=4, m=3
Edges: (1,2), (2,3), (3,4)

Step 1: Build adjacency list (using indices for edges)
adj[1] = [2]
adj[2] = [3]
adj[3] = [4]
adj[4] = []

Step 2: Check degrees
Vertex 1: out=1, in=0  -> diff = +1 (start candidate)
Vertex 2: out=1, in=1  -> diff = 0
Vertex 3: out=1, in=1  -> diff = 0
Vertex 4: out=0, in=1  -> diff = -1 (end candidate)

Start=1, End=4 matches requirements!

Step 3: Hierholzer's Algorithm (iterative with stack)

Stack: [1]     Path: []
  Current=1, has edges -> push 2
Stack: [1,2]   Path: []
  Current=2, has edges -> push 3
Stack: [1,2,3] Path: []
  Current=3, has edges -> push 4
Stack: [1,2,3,4] Path: []
  Current=4, no edges -> pop to path
Stack: [1,2,3]   Path: [4]
  Current=3, no edges -> pop to path
Stack: [1,2]     Path: [4,3]
  Current=2, no edges -> pop to path
Stack: [1]       Path: [4,3,2]
  Current=1, no edges -> pop to path
Stack: []        Path: [4,3,2,1]

Step 4: Reverse path
Final: [1,2,3,4]

Step 5: Validate
- Length = 4 = m + 1? 3 + 1 = 4 YES
- Starts at 1? YES
- Ends at 4 (=n)? YES

Output: 1 2 3 4
```

## Python Solution

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    m = int(input_data[idx]); idx += 1

    adj = defaultdict(list)
    in_deg = [0] * (n + 1)
    out_deg = [0] * (n + 1)

    for _ in range(m):
        a = int(input_data[idx]); idx += 1
        b = int(input_data[idx]); idx += 1
        adj[a].append(b)
        out_deg[a] += 1
        in_deg[b] += 1

    # Check Eulerian path conditions for this problem
    # Vertex 1 must be start: out_deg[1] - in_deg[1] = 1
    # Vertex n must be end: in_deg[n] - out_deg[n] = 1
    # All others: in_deg = out_deg

    if out_deg[1] - in_deg[1] != 1:
        print("IMPOSSIBLE")
        return

    if in_deg[n] - out_deg[n] != 1:
        print("IMPOSSIBLE")
        return

    for v in range(2, n):
        if in_deg[v] != out_deg[v]:
            print("IMPOSSIBLE")
            return

    # Hierholzer's algorithm (iterative to avoid stack overflow)
    path = []
    stack = [1]

    while stack:
        u = stack[-1]
        if adj[u]:
            v = adj[u].pop()
            stack.append(v)
        else:
            path.append(stack.pop())

    path.reverse()

    # Validate: path length should be m+1 and end at n
    if len(path) != m + 1 or path[-1] != n:
        print("IMPOSSIBLE")
        return

    print(' '.join(map(str, path)))

solve()
```

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build graph | O(m) | O(n + m) |
| Degree check | O(n) | O(n) |
| Hierholzer DFS | O(m) | O(m) stack |
| **Total** | **O(n + m)** | **O(n + m)** |

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Wrong degree check | General Eulerian path allows any start/end | Must verify vertex 1 is start, vertex n is end |
| Not reversing path | Hierholzer builds path backwards | Always reverse at the end |
| Using recursion | Stack overflow for large m | Use iterative version with explicit stack |
| Missing connectivity check | Disconnected components | Validate path length = m + 1 |
| Checking all vertices equally | Vertex 1 and n have special roles | Separate checks for 1, n, and others |

## Related Problems

| Problem | Type | Key Difference |
|---------|------|----------------|
| [Mail Delivery](https://cses.fi/problemset/task/1691) | Eulerian Circuit | Undirected graph, start = end |
| [De Bruijn Sequence](https://cses.fi/problemset/task/1692) | Eulerian Path | Implicit graph from string patterns |
| LeetCode 332: Reconstruct Itinerary | Eulerian Path | Lexicographically smallest path |
| LeetCode 2097: Valid Arrangement of Pairs | Eulerian Path | Generic start/end |
