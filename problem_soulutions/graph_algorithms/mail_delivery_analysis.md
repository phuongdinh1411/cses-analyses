---
layout: analysis
title: "Mail Delivery"
difficulty: Medium
tags: [graph, eulerian-circuit, hierholzer, undirected]
cses_link: https://cses.fi/problemset/task/1691
---

# Mail Delivery

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find a route using each street exactly once, returning to start |
| Type | Eulerian Circuit in Undirected Graph |
| Key Technique | Hierholzer's Algorithm |
| Time Complexity | O(n + m) |
| Space Complexity | O(n + m) |

## Learning Goals

After solving this problem, you will understand:
1. **Eulerian Circuit**: A path that visits every edge exactly once and returns to the starting vertex
2. **Existence Conditions**: When an Eulerian circuit exists in an undirected graph
3. **Hierholzer's Algorithm**: Efficient algorithm to construct Eulerian circuits
4. **Undirected Edge Handling**: Properly marking edges as used from both endpoints

## Problem Statement

Syrjala's mail carrier needs to deliver mail to n crossings connected by m streets. The carrier must:
- Start at the post office (crossing 1)
- Use each street exactly once
- Return to the post office

**Input**: First line has n and m. Next m lines each contain two integers a and b (a street between crossings a and b).

**Output**: Print any valid route as a sequence of crossings, or "IMPOSSIBLE" if no such route exists.

**Constraints**: 1 <= n <= 10^5, 1 <= m <= 2 x 10^5

## Eulerian Circuit: Existence Conditions

For an **undirected graph**, an Eulerian circuit exists if and only if:

1. **All vertices with edges have even degree**: Every vertex must have an even number of edges
2. **Connectivity**: All vertices with at least one edge must be in the same connected component

```
Why even degree?
- When entering a vertex, you must also leave it
- Each visit uses 2 edges (one in, one out)
- The start vertex: leave once initially, return once finally = 2 edges

Odd degree vertex = dead end (you get stuck or can't return)
```

## Undirected vs Directed: Key Difference

In an **undirected** graph:
- Each edge can be traversed in either direction
- But each edge can only be used **once total**
- When you use edge (u,v), it's consumed from both u's and v's perspective

```
Edge (A)-----(B)

Can traverse: A -> B  OR  B -> A
But NOT both! Once used, the edge is gone.
```

## Hierholzer's Algorithm for Undirected Graphs

**Core Idea**: Build the circuit by following edges until stuck, then backtrack and insert sub-circuits.

**Key for Undirected Graphs**: When using edge (u,v), mark it as used from BOTH endpoints.

```
Algorithm:
1. Check existence conditions
2. Start DFS from vertex 1
3. For each vertex, follow any unused edge
4. Mark edge as used (remove from both endpoints)
5. When stuck (no unused edges), add vertex to result
6. Backtrack and continue
7. Reverse the result
```

## Visual Diagram

```
Example: n=5, m=6
Streets: (1,2), (1,3), (2,3), (2,4), (3,4), (4,5), (5,1)
Wait, that's 7 edges. Let's use: (1,2), (1,3), (2,3), (3,4), (4,5), (5,1)

Initial Graph:
        1
       /|\
      / | \
     2--3  5
        |  |
        4--+

Degree check:
- Vertex 1: degree 3 (edges to 2, 3, 5) - ODD!
- This graph has NO Eulerian circuit

Let's fix it - add edge (1,4):
Streets: (1,2), (1,3), (1,4), (2,3), (3,4), (4,5), (5,1)

        1
       /|\\
      / | \\
     2--3  5
        |  |
        4--+

Degrees: 1->4, 2->2, 3->3, 4->3, 5->2
Still odd degrees! Need even simpler example.

Simple Example: n=4, m=4
Streets: (1,2), (2,3), (3,4), (4,1)

    1 --- 2
    |     |
    4 --- 3

Degrees: 1->2, 2->2, 3->2, 4->2 (all even!)
Connected: Yes

Hierholzer's execution:
Step 1: Start at 1, stack=[1]
Step 2: Go to 2 (use edge 1-2), stack=[1,2]
Step 3: Go to 3 (use edge 2-3), stack=[1,2,3]
Step 4: Go to 4 (use edge 3-4), stack=[1,2,3,4]
Step 5: Go to 1 (use edge 4-1), stack=[1,2,3,4,1]
Step 6: No edges from 1, pop -> result=[1]
Step 7: No edges from 4, pop -> result=[1,4]
Step 8: No edges from 3, pop -> result=[1,4,3]
Step 9: No edges from 2, pop -> result=[1,4,3,2]
Step 10: No edges from 1, pop -> result=[1,4,3,2,1]

Reverse: [1,2,3,4,1]
Output: 1 2 3 4 1
```

## Dry Run: Complex Example

```
n=5, m=6
Edges: (1,2), (1,3), (2,3), (2,4), (3,4), (1,4)

Graph:
      1
     /|\
    / | \
   2--+--3
    \ | /
     \|/
      4

Degrees: 1->3, 2->3, 3->3, 4->3
All ODD! No Eulerian circuit exists.
Output: IMPOSSIBLE

---

n=4, m=6 (with multi-edges)
Edges: (1,2), (1,2), (2,3), (3,4), (4,1), (4,1)

Degrees: 1->4, 2->3, 3->2, 4->3
Vertices 2,4 have odd degree -> IMPOSSIBLE

---

Valid example: n=3, m=4
Edges: (1,2), (1,2), (2,3), (3,1)

     1
    /|\\
   / | \\
  3--+--2
  (two edges between 1-2)

Degrees: 1->4, 2->3, 3->2
Vertex 2 odd -> IMPOSSIBLE

Actually valid: n=3, m=6
Edges: (1,2), (1,2), (2,3), (2,3), (3,1), (3,1)

Degrees: 1->4, 2->4, 3->4 (all even!)

Hierholzer's:
adj[1] = [2,2,3,3], adj[2] = [1,1,3,3], adj[3] = [2,2,1,1]

stack=[1], result=[]
Go 1->2: adj[1]=[2,3,3], adj[2]=[1,3,3], stack=[1,2]
Go 2->1: adj[2]=[3,3], adj[1]=[3,3], stack=[1,2,1]
Go 1->3: adj[1]=[3], adj[3]=[2,2,1], stack=[1,2,1,3]
Go 3->2: adj[3]=[2,1], adj[2]=[3], stack=[1,2,1,3,2]
Go 2->3: adj[2]=[], adj[3]=[1], stack=[1,2,1,3,2,3]
Go 3->1: adj[3]=[], adj[1]=[], stack=[1,2,1,3,2,3,1]

Pop all (no remaining edges): result=[1,3,2,3,1,2,1]
Reverse: [1,2,1,3,2,3,1]

Output: 1 2 1 3 2 3 1
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

    if m == 0:
        print(1)
        return

    # Adjacency list storing (neighbor, edge_index)
    adj = defaultdict(list)
    degree = [0] * (n + 1)

    for i in range(m):
        a = int(input_data[idx]); idx += 1
        b = int(input_data[idx]); idx += 1
        adj[a].append([b, i])
        adj[b].append([a, i])
        degree[a] += 1
        degree[b] += 1

    # Check 1: All vertices must have even degree
    for v in range(1, n + 1):
        if degree[v] % 2 == 1:
            print("IMPOSSIBLE")
            return

    # Check 2: All edges must be in same component (containing vertex 1)
    # We'll verify this by checking if we use all m edges

    used = [False] * m  # Track which edges are used
    result = []

    def dfs(u):
        while adj[u]:
            v, edge_idx = adj[u].pop()
            if not used[edge_idx]:
                used[edge_idx] = True
                dfs(v)
        result.append(u)

    dfs(1)

    # Check if all edges were used
    if len(result) != m + 1:
        print("IMPOSSIBLE")
        return

    result.reverse()
    print(' '.join(map(str, result)))

solve()
```

## C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXM = 200005;
vector<pair<int,int>> adj[100005];  // {neighbor, edge_index}
bool used[MAXM];
vector<int> result;
int degree[100005];

void dfs(int u) {
    while (!adj[u].empty()) {
        auto [v, idx] = adj[u].back();
        adj[u].pop_back();
        if (!used[idx]) {
            used[idx] = true;
            dfs(v);
        }
    }
    result.push_back(u);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    if (m == 0) {
        cout << 1 << "\n";
        return 0;
    }

    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back({b, i});
        adj[b].push_back({a, i});
        degree[a]++;
        degree[b]++;
    }

    // Check: all vertices must have even degree
    for (int v = 1; v <= n; v++) {
        if (degree[v] % 2 == 1) {
            cout << "IMPOSSIBLE\n";
            return 0;
        }
    }

    dfs(1);

    // Check: all edges must be used (connectivity check)
    if ((int)result.size() != m + 1) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }

    reverse(result.begin(), result.end());
    for (int i = 0; i < (int)result.size(); i++) {
        cout << result[i] << " \n"[i == (int)result.size() - 1];
    }

    return 0;
}
```

## Algorithm Walkthrough

```
Why we use edge indices:

In undirected graphs, edge (u,v) appears in both adj[u] and adj[v].
When we traverse from u to v, we must mark it used for BOTH.

Using edge index:
- Edge 0: (1,2) -> adj[1] has {2,0}, adj[2] has {1,0}
- When we use edge 0 going 1->2:
  - Set used[0] = true
  - When we later see {1,0} in adj[2], used[0] is already true
  - So we skip it (edge already consumed)

This prevents using the same street twice!
```

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Not marking edge as used from both endpoints | Same edge traversed twice | Use edge index to track globally |
| Checking only degree condition | Disconnected components with even degrees still fail | Verify all edges are used |
| Using recursion without increasing stack limit | Stack overflow for large graphs | Use iterative version or increase limit |
| Forgetting to check m=0 case | Empty graph is valid (just output "1") | Handle edge case explicitly |
| Not reversing final result | Hierholzer builds path backwards | Reverse at the end |

## Key Insights

1. **Undirected = bidirectional but single-use**: Each street can be walked either way, but only once total

2. **Even degree = balanced flow**: Every time you enter a vertex, you can leave it

3. **Edge tracking is crucial**: Must track each edge individually, not just adjacency

4. **Connectivity via edge count**: If result has m+1 vertices, all edges were used and graph was connected

## Related Problems

| Problem | Type | Key Difference |
|---------|------|----------------|
| [Teleporters Path](https://cses.fi/problemset/task/1693) | Eulerian Path (Directed) | Directed edges, path not circuit |
| [De Bruijn Sequence](https://cses.fi/problemset/task/1692) | Eulerian Path | Construct specific sequence |
| [LeetCode 332: Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) | Eulerian Path | Lexicographically smallest |

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build adjacency list | O(m) | O(m) |
| Degree check | O(n) | O(n) |
| Hierholzer's DFS | O(m) | O(m) stack |
| **Total** | **O(n + m)** | **O(n + m)** |
