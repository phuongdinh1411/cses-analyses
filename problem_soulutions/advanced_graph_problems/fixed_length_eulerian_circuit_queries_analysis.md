---
layout: simple
title: "Mail Delivery - Graph Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_eulerian_circuit_queries_analysis
difficulty: Medium
tags: [graph, eulerian-circuit, hierholzer, dfs]
---

# Mail Delivery (Eulerian Circuit)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Graph Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Hierholzer's Algorithm, Degree Analysis |
| **CSES Link** | [Mail Delivery](https://cses.fi/problemset/task/1691) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Identify when an Eulerian circuit exists in a graph
- [ ] Apply degree conditions for Eulerian circuits (all vertices must have even degree)
- [ ] Implement Hierholzer's algorithm to find an Eulerian circuit
- [ ] Verify graph connectivity as a prerequisite for Eulerian circuits

---

## Problem Statement

**Problem:** Given an undirected graph with n nodes and m edges, find a route that starts and ends at node 1 and visits every edge exactly once. This is an Eulerian circuit.

**Input:**
- Line 1: n (nodes) and m (edges)
- Next m lines: a b (edge between nodes a and b)

**Output:**
- A route visiting every edge exactly once, or "IMPOSSIBLE"

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 * 10^5

### Example

```
Input:
5 6
1 2
1 3
2 3
2 4
3 4
4 5

Output:
IMPOSSIBLE

Input:
5 6
1 3
1 2
2 3
4 5
4 5
3 4

Output:
1 3 2 1 3 4 5 4 3
```

**Explanation:** In the second example, every edge is traversed exactly once, and the path starts and ends at node 1.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When can we traverse every edge exactly once and return to the start?

An Eulerian circuit exists if and only if:
1. **Every vertex has even degree** - When entering a vertex, you must be able to leave
2. **The graph is connected** - All edges must be reachable from the starting point

### Breaking Down the Problem

1. **What are we looking for?** A path that uses each edge exactly once and forms a cycle
2. **What information do we have?** The graph structure (nodes and edges)
3. **What's the relationship between input and output?** Degree parity determines existence; Hierholzer's algorithm finds the path

### Analogies

Think of this problem like a mail carrier who needs to deliver mail on every street exactly once and return home. If any intersection has an odd number of streets, the carrier gets "stuck" - they can enter but not leave (or vice versa).

---

## Solution 1: Condition Check Only

### Idea

Before attempting to find a circuit, verify that one exists by checking the necessary conditions.

### Algorithm

1. Build the adjacency list
2. Check if all vertices with edges have even degree
3. Check if the graph is connected (using DFS/BFS)
4. If conditions fail, output "IMPOSSIBLE"

### Code

```python
def check_eulerian_possible(n, edges):
    """
    Check if Eulerian circuit is possible.

    Time: O(n + m)
    Space: O(n + m)
    """
    from collections import defaultdict

    graph = defaultdict(list)
    degree = [0] * (n + 1)

    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
        degree[a] += 1
        degree[b] += 1

    # Check 1: All vertices must have even degree
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return False

    # Check 2: Graph must be connected (only check vertices with edges)
    start = -1
    for i in range(1, n + 1):
        if degree[i] > 0:
            start = i
            break

    if start == -1:
        return True  # No edges, trivially true

    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)

    # All vertices with edges must be visited
    for i in range(1, n + 1):
        if degree[i] > 0 and i not in visited:
            return False

    return True
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | DFS visits each node and edge once |
| Space | O(n + m) | Adjacency list storage |

---

## Solution 2: Hierholzer's Algorithm (Optimal)

### Key Insight

> **The Trick:** Start from any vertex, follow edges (removing them as you go), and when stuck, backtrack while building the circuit.

### Algorithm

1. Verify Eulerian conditions (even degrees, connectivity)
2. Start at node 1
3. Follow any available edge, marking it as used
4. When stuck (no outgoing edges), add current node to result and backtrack
5. Continue until all edges are used

### Dry Run Example

Let's trace through with a simple graph:

```
Graph: 1--2--3--1 (triangle)
Edges: (1,2), (2,3), (3,1)

Initial adjacency:
  1: [2, 3]
  2: [1, 3]
  3: [2, 1]

Step 1: Start at node 1
  Stack: [1]
  Path: []

Step 2: From 1, go to 2 (remove edge 1-2)
  Stack: [1, 2]
  Adjacency updates: 1: [3], 2: [3]

Step 3: From 2, go to 3 (remove edge 2-3)
  Stack: [1, 2, 3]
  Adjacency updates: 2: [], 3: [1]

Step 4: From 3, go to 1 (remove edge 3-1)
  Stack: [1, 2, 3, 1]
  Adjacency updates: 3: [], 1: []

Step 5: Node 1 has no edges, add to path
  Path: [1]
  Stack: [1, 2, 3]

Step 6-8: Continue backtracking
  Final Path: [1, 3, 2, 1]
```

### Visual Diagram

```
Initial Graph:          After finding circuit:
    1                       1
   / \                     / \
  2---3                   2---3

Circuit: 1 -> 2 -> 3 -> 1
         Uses each edge exactly once
```

### Code

```python
def find_eulerian_circuit(n, edges):
    """
    Find Eulerian circuit using Hierholzer's algorithm.

    Time: O(m) - each edge processed once
    Space: O(n + m) - adjacency list and stack
    """
    from collections import defaultdict

    if not edges:
        print(1)
        return

    graph = defaultdict(list)
    degree = [0] * (n + 1)

    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
        degree[a] += 1
        degree[b] += 1

    # Check even degree condition
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            print("IMPOSSIBLE")
            return

    # Check connectivity
    start = 1
    if degree[1] == 0:
        print("IMPOSSIBLE")
        return

    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)

    for i in range(1, n + 1):
        if degree[i] > 0 and i not in visited:
            print("IMPOSSIBLE")
            return

    # Hierholzer's algorithm
    # Use index-based adjacency for efficient edge removal
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    circuit = []
    stack = [1]

    while stack:
        v = stack[-1]
        if adj[v]:
            u = adj[v].pop()
            # Remove the reverse edge
            adj[u].remove(v)
            stack.append(u)
        else:
            circuit.append(stack.pop())

    # Check if all edges were used
    if len(circuit) != len(edges) + 1:
        print("IMPOSSIBLE")
        return

    print(" ".join(map(str, circuit)))

# Input handling
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))
find_eulerian_circuit(n, edges)
```

### C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<vector<pair<int, int>>> adj(n + 1);
    vector<int> degree(n + 1, 0);
    vector<bool> used(m, false);

    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back({b, i});
        adj[b].push_back({a, i});
        degree[a]++;
        degree[b]++;
    }

    // Check even degree condition
    for (int i = 1; i <= n; i++) {
        if (degree[i] % 2 != 0) {
            cout << "IMPOSSIBLE\n";
            return 0;
        }
    }

    // Check if node 1 has edges
    if (degree[1] == 0) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }

    // Connectivity check using DFS
    vector<bool> visited(n + 1, false);
    stack<int> dfs_stack;
    dfs_stack.push(1);
    while (!dfs_stack.empty()) {
        int node = dfs_stack.top();
        dfs_stack.pop();
        if (visited[node]) continue;
        visited[node] = true;
        for (auto& [neighbor, _] : adj[node]) {
            if (!visited[neighbor]) {
                dfs_stack.push(neighbor);
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        if (degree[i] > 0 && !visited[i]) {
            cout << "IMPOSSIBLE\n";
            return 0;
        }
    }

    // Hierholzer's algorithm
    vector<int> ptr(n + 1, 0);
    vector<int> circuit;
    stack<int> st;
    st.push(1);

    while (!st.empty()) {
        int v = st.top();
        while (ptr[v] < adj[v].size() && used[adj[v][ptr[v]].second]) {
            ptr[v]++;
        }
        if (ptr[v] < adj[v].size()) {
            auto [u, idx] = adj[v][ptr[v]];
            used[idx] = true;
            ptr[v]++;
            st.push(u);
        } else {
            circuit.push_back(v);
            st.pop();
        }
    }

    if (circuit.size() != m + 1) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }

    for (int i = 0; i < circuit.size(); i++) {
        cout << circuit[i] << " \n"[i == circuit.size() - 1];
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | Each edge and vertex processed once |
| Space | O(n + m) | Adjacency list, stack, and circuit storage |

---

## Common Mistakes

### Mistake 1: Forgetting Connectivity Check

```python
# WRONG - Only checks degrees
for i in range(1, n + 1):
    if degree[i] % 2 != 0:
        return "IMPOSSIBLE"
return find_circuit()  # May fail on disconnected graph!
```

**Problem:** A graph with even degrees but multiple components has no Eulerian circuit.
**Fix:** Always verify connectivity of vertices with edges.

### Mistake 2: Not Removing Both Edge Directions

```python
# WRONG - Only removes forward edge
adj[v].remove(u)
# Forgot: adj[u].remove(v)
```

**Problem:** Edge gets traversed twice (once in each direction).
**Fix:** Remove the edge from both adjacency lists.

### Mistake 3: Ignoring the Starting Node Requirement

```python
# WRONG - Starting from any node
start = next(node for node in range(1, n+1) if degree[node] > 0)
```

**Problem:** Problem requires starting from node 1 specifically.
**Fix:** Check that node 1 has edges; start from node 1.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No edges | n=1, m=0 | 1 | Trivially at node 1 |
| Single self-loop | 1-1 | 1 1 | Valid circuit |
| Odd degree vertex | Triangle with extra edge at one vertex | IMPOSSIBLE | Violates even degree condition |
| Disconnected components | Two separate triangles | IMPOSSIBLE | Not all edges reachable from node 1 |
| Node 1 isolated | Graph excludes node 1 | IMPOSSIBLE | Must start at node 1 |
| Multiple edges between same nodes | 1-2, 1-2 | 1 2 1 | Valid (multigraph) |

---

## When to Use This Pattern

### Use Hierholzer's Algorithm When:
- Finding an Eulerian path or circuit (traverse each edge exactly once)
- Graph has proper degree conditions (all even for circuit, 0 or 2 odd for path)
- Need linear time complexity O(n + m)

### Don't Use When:
- Looking for Hamiltonian path/circuit (visit each vertex once) - different problem
- Graph doesn't meet Eulerian conditions - no solution exists
- Need shortest path - use Dijkstra/BFS instead

### Pattern Recognition Checklist:
- [ ] "Traverse every edge exactly once" mentioned? -> **Eulerian problem**
- [ ] All degrees even? -> **Eulerian circuit exists**
- [ ] Exactly 2 odd degree vertices? -> **Eulerian path exists**
- [ ] Graph connected (considering only vertices with edges)? -> **Required condition**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Round Trip](https://cses.fi/problemset/task/1669) | Basic cycle detection |
| [Building Roads](https://cses.fi/problemset/task/1666) | Graph connectivity |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Teleporters Path](https://cses.fi/problemset/task/1693) | Directed graph, Eulerian path |
| [De Bruijn Sequence](https://cses.fi/problemset/task/1692) | Construct Eulerian path on implicit graph |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Hamiltonian Flights](https://cses.fi/problemset/task/1690) | Visit each node once (NP-hard, use DP) |
| [Knight's Tour](https://cses.fi/problemset/task/1689) | Hamiltonian path on chessboard |

---

## Key Takeaways

1. **The Core Idea:** An Eulerian circuit exists iff all vertices have even degree and the graph is connected
2. **Time Optimization:** Hierholzer's algorithm achieves O(n + m) by cleverly backtracking
3. **Space Trade-off:** We use O(n + m) space for adjacency list and result storage
4. **Pattern:** Graph theory - Eulerian circuits are fundamentally about edge traversal

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] State the two conditions for an Eulerian circuit to exist
- [ ] Explain why odd-degree vertices make circuits impossible
- [ ] Implement Hierholzer's algorithm from scratch
- [ ] Handle edge cases (no edges, disconnected, node 1 isolated)

---

## Additional Resources

- [CP-Algorithms: Eulerian Path](https://cp-algorithms.com/graph/euler_path.html)
- [CSES Mail Delivery](https://cses.fi/problemset/task/1691) - Find Eulerian circuit
- [Wikipedia: Eulerian Path](https://en.wikipedia.org/wiki/Eulerian_path)
