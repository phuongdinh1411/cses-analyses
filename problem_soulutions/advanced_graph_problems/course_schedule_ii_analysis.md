---
layout: simple
title: "Course Schedule II - Topological Sorting"
permalink: /problem_soulutions/advanced_graph_problems/course_schedule_ii_analysis
difficulty: Medium
tags: [topological-sort, graph, bfs, dfs, kahn-algorithm]
prerequisites: [graph_basics, bfs_dfs]
---

# Course Schedule II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Course Schedule](https://cses.fi/problemset/task/1757) |
| **Difficulty** | Medium |
| **Category** | Graph / Topological Sort |
| **Time Limit** | 1 second |
| **Key Technique** | Kahn's Algorithm / DFS |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand topological sorting and when it applies
- [ ] Implement Kahn's algorithm (BFS-based topological sort)
- [ ] Implement DFS-based topological sort with cycle detection
- [ ] Detect cycles in directed graphs
- [ ] Solve dependency resolution problems

---

## Problem Statement

**Problem:** Given n courses labeled 1 to n and m prerequisite requirements, find a valid order to complete all courses. If no valid order exists (due to cycles), output "IMPOSSIBLE".

**Input:**
- Line 1: Two integers n and m (number of courses and prerequisites)
- Lines 2 to m+1: Two integers a and b, meaning course a requires course b

**Output:**
- A valid order to complete all courses, or "IMPOSSIBLE" if a cycle exists

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 * 10^5

### Example

```
Input:
5 3
3 1
4 1
5 4

Output:
1 2 3 4 5
```

**Explanation:** Course 1 has no prerequisites, so we take it first. Course 3 requires 1 (done). Course 4 requires 1 (done). Course 5 requires 4 (done). Course 2 is independent.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** We have items with dependencies - in what order can we process them?

This is the classic **topological sorting** problem. Whenever you see:
- Tasks with prerequisites
- Dependencies between items
- "Valid ordering" with constraints

Think **topological sort**.

### Breaking Down the Problem

1. **What are we looking for?** An ordering where every prerequisite comes before the course that needs it.
2. **What information do we have?** Directed edges showing dependencies (b -> a means "take b before a").
3. **What makes it impossible?** A cycle - if A requires B and B requires A, neither can go first.

### Analogy

Think of getting dressed. You must put on underwear before pants, socks before shoes. If there was a rule "put on shoes before socks," you'd have a cycle - impossible to satisfy!

---

## Solution 1: Brute Force (Conceptual)

### Idea

Try all n! permutations and check if each one satisfies all prerequisites.

### Why It's Impractical

With n up to 10^5, we cannot enumerate all permutations. This is purely for understanding - we need a smarter approach.

**Time:** O(n! * m) - completely infeasible

---

## Solution 2: Kahn's Algorithm (BFS)

### Key Insight

> **The Trick:** Start with courses that have no prerequisites (in-degree = 0). After "taking" them, reduce the in-degree of dependent courses. Repeat.

### Algorithm

1. Build adjacency list and compute in-degree for each node
2. Add all nodes with in-degree 0 to a queue
3. Process queue: remove node, add to result, decrease in-degree of neighbors
4. If any neighbor's in-degree becomes 0, add it to queue
5. If result has all n nodes, we succeeded; otherwise, there's a cycle

### Dry Run Example

```
Input: n=5, edges: 3->1, 4->1, 5->4

Step 1: Build graph and in-degrees
  Adjacency: 1->[3,4], 4->[5]
  In-degree: [0, 0, 0, 1, 1, 1]  (1-indexed: nodes 1,2 have 0)

Step 2: Queue = [1, 2] (in-degree 0)

Step 3: Process node 1
  Result: [1]
  Decrease in-degree of 3: 1->0, add to queue
  Decrease in-degree of 4: 1->0, add to queue
  Queue: [2, 3, 4]

Step 4: Process node 2
  Result: [1, 2]
  No neighbors
  Queue: [3, 4]

Step 5: Process node 3
  Result: [1, 2, 3]
  No neighbors
  Queue: [4]

Step 6: Process node 4
  Result: [1, 2, 3, 4]
  Decrease in-degree of 5: 1->0, add to queue
  Queue: [5]

Step 7: Process node 5
  Result: [1, 2, 3, 4, 5]
  Queue: []

Final: [1, 2, 3, 4, 5] - all 5 nodes processed, valid order!
```

### Visual Diagram

```
    1 -----> 3
    |
    +------> 4 -----> 5

    2 (independent)

In-degree:  1:0  2:0  3:1  4:1  5:1
            ^    ^
            |____|___ Start here (in-degree 0)
```

### Code (Python)

```python
from collections import deque

def solve():
    n, m = map(int, input().split())

    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)

    for _ in range(m):
        a, b = map(int, input().split())
        adj[b].append(a)  # b must come before a
        in_degree[a] += 1

    # Kahn's algorithm
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)

    result = []
    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) == n:
        print(*result)
    else:
        print("IMPOSSIBLE")

solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<vector<int>> adj(n + 1);
    vector<int> in_degree(n + 1, 0);

    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[b].push_back(a);  // b must come before a
        in_degree[a]++;
    }

    // Kahn's algorithm
    queue<int> q;
    for (int i = 1; i <= n; i++) {
        if (in_degree[i] == 0) {
            q.push(i);
        }
    }

    vector<int> result;
    while (!q.empty()) {
        int node = q.front();
        q.pop();
        result.push_back(node);

        for (int neighbor : adj[node]) {
            in_degree[neighbor]--;
            if (in_degree[neighbor] == 0) {
                q.push(neighbor);
            }
        }
    }

    if ((int)result.size() == n) {
        for (int i = 0; i < n; i++) {
            cout << result[i] << " \n"[i == n - 1];
        }
    } else {
        cout << "IMPOSSIBLE\n";
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | Visit each node and edge once |
| Space | O(n + m) | Adjacency list and queue |

---

## Solution 3: DFS-Based Topological Sort

### Key Insight

> **The Trick:** Use DFS with three states: unvisited, visiting (in current path), visited. Add nodes to result in post-order (after all descendants processed). Reverse at the end.

### Algorithm

1. Mark all nodes as unvisited (state = 0)
2. For each unvisited node, run DFS
3. During DFS: mark as visiting (state = 1), recurse on neighbors
4. If we encounter a "visiting" node, we found a cycle
5. After recursion, mark as visited (state = 2), add to result
6. Reverse result at the end

### Dry Run Example

```
Input: n=4, edges: 2->1, 3->1, 4->2, 4->3

DFS from node 1:
  Visit 1 (state: visiting)
  No unvisited neighbors
  Mark 1 visited, add to result: [1]

DFS from node 2:
  Visit 2 (state: visiting)
  Neighbor 4: visit 4 (state: visiting)
    Neighbor of 4: none unvisited
    Mark 4 visited, add to result: [1, 4]
  Back to 2: mark visited, add to result: [1, 4, 2]

DFS from node 3:
  Visit 3 (state: visiting)
  Neighbor 4: already visited, skip
  Mark 3 visited, add to result: [1, 4, 2, 3]

Reverse: [3, 2, 4, 1] - valid topological order!
```

### Code (Python)

```python
import sys
sys.setrecursionlimit(200005)

def solve():
    n, m = map(int, input().split())

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, input().split())
        adj[b].append(a)  # b must come before a

    state = [0] * (n + 1)  # 0: unvisited, 1: visiting, 2: visited
    result = []
    has_cycle = False

    def dfs(node):
        nonlocal has_cycle
        if has_cycle:
            return

        state[node] = 1  # visiting

        for neighbor in adj[node]:
            if state[neighbor] == 1:  # cycle detected
                has_cycle = True
                return
            if state[neighbor] == 0:
                dfs(neighbor)

        state[node] = 2  # visited
        result.append(node)

    for i in range(1, n + 1):
        if state[i] == 0:
            dfs(i)

    if has_cycle:
        print("IMPOSSIBLE")
    else:
        print(*result[::-1])

solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> adj;
vector<int> state;  // 0: unvisited, 1: visiting, 2: visited
vector<int> result;
bool has_cycle = false;

void dfs(int node) {
    if (has_cycle) return;

    state[node] = 1;  // visiting

    for (int neighbor : adj[node]) {
        if (state[neighbor] == 1) {
            has_cycle = true;
            return;
        }
        if (state[neighbor] == 0) {
            dfs(neighbor);
        }
    }

    state[node] = 2;  // visited
    result.push_back(node);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    adj.resize(n + 1);
    state.resize(n + 1, 0);

    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[b].push_back(a);
    }

    for (int i = 1; i <= n; i++) {
        if (state[i] == 0) {
            dfs(i);
        }
    }

    if (has_cycle) {
        cout << "IMPOSSIBLE\n";
    } else {
        reverse(result.begin(), result.end());
        for (int i = 0; i < n; i++) {
            cout << result[i] << " \n"[i == n - 1];
        }
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | Visit each node and edge once |
| Space | O(n + m) | Adjacency list and recursion stack |

---

## Common Mistakes

### Mistake 1: Wrong Edge Direction

```python
# WRONG - edge direction reversed
adj[a].append(b)  # a points to b

# CORRECT - b must come before a, so b points to a
adj[b].append(a)
```

**Problem:** The edge direction determines the order. "a requires b" means b -> a.

### Mistake 2: Forgetting to Reverse DFS Result

```python
# WRONG
return result  # Post-order gives reverse topological order

# CORRECT
return result[::-1]  # Reverse to get correct order
```

### Mistake 3: Not Handling Disconnected Components

```python
# WRONG - only starts from node 1
dfs(1)

# CORRECT - check all nodes
for i in range(1, n + 1):
    if state[i] == 0:
        dfs(i)
```

### Mistake 4: Using Only Two States for Cycle Detection

```python
# WRONG - can't distinguish "in current path" from "fully processed"
visited = [False] * n

# CORRECT - three states needed
state = [0] * n  # 0: unvisited, 1: visiting, 2: visited
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| No edges | n=3, m=0 | Any order like "1 2 3" | All orderings valid |
| Self-loop | n=2, 1->1 | IMPOSSIBLE | Node depends on itself |
| Simple cycle | n=2, 1->2, 2->1 | IMPOSSIBLE | Circular dependency |
| Linear chain | n=3, 2->1, 3->2 | 1 2 3 | Simple dependency chain |
| Single node | n=1, m=0 | 1 | Trivial case |

---

## When to Use This Pattern

### Use Topological Sort When:
- Tasks have dependencies/prerequisites
- Need to find valid execution order
- Checking if dependencies have cycles
- Build systems, task scheduling, course planning

### Kahn's vs DFS:
- **Kahn's (BFS):** Iterative, easier to understand, directly produces order
- **DFS:** Recursive, useful when also need to find the actual cycle path

### Pattern Recognition Checklist:
- [ ] Directed graph with dependencies? -> **Topological Sort**
- [ ] Need to detect cycles? -> **Either approach works**
- [ ] Need lexicographically smallest order? -> **Use Kahn's with priority queue**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Building Roads](https://cses.fi/problemset/task/1666) | Basic graph connectivity |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Game Routes](https://cses.fi/problemset/task/1681) | Count paths in DAG |
| [Longest Flight Route](https://cses.fi/problemset/task/1680) | Longest path in DAG |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Strongly Connected Components](https://cses.fi/problemset/task/1682) | Kosaraju's/Tarjan's algorithm |
| [Cycle Finding](https://cses.fi/problemset/task/1669) | Find actual cycle path |

---

## Key Takeaways

1. **Core Idea:** Process nodes with no remaining dependencies first
2. **Cycle Detection:** If we can't process all nodes, a cycle exists
3. **Two Approaches:** Kahn's (BFS with in-degree) or DFS (three-state coloring)
4. **Pattern:** Classic dependency resolution - very common in real systems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement Kahn's algorithm from memory
- [ ] Implement DFS-based topological sort from memory
- [ ] Explain why three states are needed for DFS cycle detection
- [ ] Recognize topological sort problems in disguise
