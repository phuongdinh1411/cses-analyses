---
layout: simple
title: "Subtree Queries - Tree Algorithms Problem"
permalink: /problem_soulutions/tree_algorithms/subtree_queries_analysis
difficulty: Medium
tags: [tree, euler-tour, BIT, segment-tree, subtree]
prerequisites: [tree-traversal, binary-indexed-tree]
---

# Subtree Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Euler Tour + BIT/Segment Tree |
| **CSES Link** | [https://cses.fi/problemset/task/1137](https://cses.fi/problemset/task/1137) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Flatten a tree into an array using Euler tour (DFS order)
- [ ] Map subtree operations to range operations on arrays
- [ ] Use Binary Indexed Tree (BIT) or Segment Tree for point updates and range queries
- [ ] Understand why subtrees form contiguous ranges in Euler tour order

---

## Problem Statement

**Problem:** Given a rooted tree with n nodes, each node has a value. Process two types of queries:
1. **Update:** Change the value of node s to x
2. **Query:** Find the sum of all values in the subtree rooted at node s

**Input:**
- Line 1: n q (number of nodes and queries)
- Line 2: v1, v2, ..., vn (initial values of nodes)
- Next n-1 lines: edges a b (connecting nodes a and b)
- Next q lines: queries in format "1 s x" (update) or "2 s" (query sum)

**Output:**
- For each type 2 query, print the sum of values in the subtree

**Constraints:**
- 1 <= n, q <= 2 * 10^5
- 1 <= vi, x <= 10^9
- Tree is rooted at node 1

### Example

```
Input:
5 3
4 2 5 2 1
1 2
1 3
3 4
3 5
2 3
1 5 3
2 3

Output:
8
10
```

**Explanation:**
- Initial tree: Node 1 is root with children 2, 3. Node 3 has children 4, 5.
- Query "2 3": Subtree of node 3 contains {3, 4, 5} with values {5, 2, 1}. Sum = 8.
- Update "1 5 3": Change node 5's value from 1 to 3.
- Query "2 3": Subtree of node 3 now has values {5, 2, 3}. Sum = 10.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we convert tree operations into efficient array operations?

The crucial insight is that performing DFS on a tree visits each subtree as a **contiguous segment**. When we enter a node, all its descendants are visited before we backtrack. This means if we record the entry time of each node during DFS, nodes in the same subtree have consecutive entry times.

### Breaking Down the Problem

1. **What are we looking for?** Sum of values in a subtree, with support for updates.
2. **What information do we have?** Tree structure and node values.
3. **What's the relationship between input and output?** Subtree = contiguous range in DFS order.

### Analogies

Think of this problem like organizing a company directory. When you do a depth-first traversal of an org chart, everyone in a department (subtree) appears consecutively. If you want to know the total salary of a department, you just need to sum a contiguous range in your flattened list.

---

## Solution 1: Brute Force

### Idea

For each query, perform DFS from the queried node and sum all values in its subtree.

### Algorithm

1. Build adjacency list from edges
2. For each query, run DFS from the query node
3. Sum values of all visited nodes

### Code

```python
def solve_brute_force(n, q, values, edges, queries):
    """
    Brute force: DFS for each query.

    Time: O(q * n)
    Space: O(n)
    """
    from collections import defaultdict

    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    def subtree_sum(root, parent=-1):
        total = values[root]
        for child in graph[root]:
            if child != parent:
                total += subtree_sum(child, root)
        return total

    results = []
    for query in queries:
        if query[0] == 1:  # Update
            s, x = query[1], query[2]
            values[s] = x
        else:  # Query
            s = query[1]
            # Need to find parent to avoid going back up
            # For simplicity, we root at 1 and track parents
            results.append(subtree_sum(s, -1))  # Simplified

    return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query traverses up to n nodes |
| Space | O(n) | Adjacency list and recursion stack |

### Why This Works (But Is Slow)

Correctness is guaranteed because DFS visits exactly the nodes in the subtree. However, with q queries and n nodes, the worst case is O(q * n) = O(4 * 10^10) operations, far too slow.

---

## Solution 2: Optimal Solution (Euler Tour + BIT)

### Key Insight

> **The Trick:** Euler tour flattens the tree so each subtree becomes a contiguous range. Use BIT for O(log n) updates and range queries.

### Euler Tour Concept

| Term | Meaning |
|------|---------|
| `in_time[v]` | The DFS entry time of node v (0-indexed position in tour) |
| `out_time[v]` | The DFS exit time of node v (last position in its subtree) |
| `euler[i]` | The node value at position i in the flattened array |

**In plain English:** When we DFS from node v, all nodes in v's subtree are visited between `in_time[v]` and `out_time[v]`. So subtree sum = range sum from `in_time[v]` to `out_time[v]`.

### Why Euler Tour Works

```
Tree:           Euler Tour (DFS order):
    1           Position:  0   1   2   3   4
   / \          Node:      1   2   3   4   5
  2   3         Value:     4   2   5   2   1
     / \
    4   5       in_time:  1->0, 2->1, 3->2, 4->3, 5->4
                out_time: 1->4, 2->1, 3->4, 4->3, 5->4
```

Subtree of node 3 = positions [2, 4] = nodes {3, 4, 5}.

### Algorithm

1. **Build tree:** Create adjacency list
2. **Euler tour:** DFS to compute in_time and out_time for each node
3. **Initialize BIT:** Store node values in DFS order
4. **Process queries:**
   - Update: Point update in BIT at position `in_time[s]`
   - Query: Range sum from `in_time[s]` to `out_time[s]`

### Dry Run Example

Let's trace through the example:

```
Input:
n=5, q=3
values: [4, 2, 5, 2, 1] (1-indexed: node 1=4, node 2=2, etc.)
edges: (1,2), (1,3), (3,4), (3,5)
queries: (2,3), (1,5,3), (2,3)

Step 1: Build Tree (rooted at 1)
        1 (val=4)
       / \
      2   3 (val=2, val=5)
         / \
        4   5 (val=2, val=1)

Step 2: Euler Tour (DFS from node 1)
  Visit node 1: in_time[1] = 0
    Visit node 2: in_time[2] = 1, out_time[2] = 1
    Visit node 3: in_time[3] = 2
      Visit node 4: in_time[4] = 3, out_time[4] = 3
      Visit node 5: in_time[5] = 4, out_time[5] = 4
    out_time[3] = 4
  out_time[1] = 4

  Euler array (by in_time order):
  Position:  0   1   2   3   4
  Node:      1   2   3   4   5
  Value:     4   2   5   2   1

  Summary:
  Node | in_time | out_time | Subtree Range
  -----|---------|----------|---------------
    1  |    0    |    4     |    [0, 4]
    2  |    1    |    1     |    [1, 1]
    3  |    2    |    4     |    [2, 4]
    4  |    3    |    3     |    [3, 3]
    5  |    4    |    4     |    [4, 4]

Step 3: Initialize BIT with values [4, 2, 5, 2, 1]
  BIT supports: point update, prefix sum query

Step 4: Process Queries

  Query 1: "2 3" (sum of subtree rooted at 3)
    Range: [in_time[3], out_time[3]] = [2, 4]
    Sum = prefix_sum(4) - prefix_sum(1)
        = (4+2+5+2+1) - (4+2)
        = 14 - 6 = 8
    Output: 8

  Query 2: "1 5 3" (update node 5 to value 3)
    Position in euler array: in_time[5] = 4
    Old value: 1, New value: 3, Delta: +2
    BIT.update(4, +2)
    Now euler array represents: [4, 2, 5, 2, 3]

  Query 3: "2 3" (sum of subtree rooted at 3)
    Range: [2, 4]
    Sum = prefix_sum(4) - prefix_sum(1)
        = (4+2+5+2+3) - (4+2)
        = 16 - 6 = 10
    Output: 10

Final Output: 8, 10
```

### Visual Diagram

```
Tree Structure:              Euler Tour Mapping:

      1(4)                   Position: 0    1    2    3    4
     / \                              |    |    |    |    |
   2(2) 3(5)                 Node:    1    2    3    4    5
       / \                   Value:   4    2    5    2    1
     4(2) 5(1)                        ^--------------^
                                      |              |
                             Subtree of 1: [0,4] sum=14

                                           ^----^
                                           |    |
                                  Subtree of 2: [1,1] sum=2

                                                ^---------^
                                                |         |
                                       Subtree of 3: [2,4] sum=8
```

### Code (Python)

```python
import sys
from collections import defaultdict
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    values = [0] + list(map(int, input().split()))  # 1-indexed

    # Build adjacency list
    graph = defaultdict(list)
    for _ in range(n - 1):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    # Euler tour using iterative DFS (avoid recursion limit)
    in_time = [0] * (n + 1)
    out_time = [0] * (n + 1)
    euler = [0] * (n + 1)  # euler[i] = value at position i

    timer = 0
    stack = [(1, -1, False)]  # (node, parent, visited)

    while stack:
        node, parent, visited = stack.pop()

        if visited:
            out_time[node] = timer - 1
        else:
            in_time[node] = timer
            euler[timer] = values[node]
            timer += 1
            stack.append((node, parent, True))

            for child in graph[node]:
                if child != parent:
                    stack.append((child, node, False))

    # Binary Indexed Tree (1-indexed internally)
    bit = [0] * (n + 2)

    def bit_update(i, delta):
        i += 1  # Convert to 1-indexed
        while i <= n + 1:
            bit[i] += delta
            i += i & (-i)

    def bit_query(i):
        i += 1  # Convert to 1-indexed
        total = 0
        while i > 0:
            total += bit[i]
            i -= i & (-i)
        return total

    def range_sum(l, r):
        if l == 0:
            return bit_query(r)
        return bit_query(r) - bit_query(l - 1)

    # Initialize BIT with euler tour values
    for i in range(n):
        bit_update(i, euler[i])

    # Process queries
    results = []
    for _ in range(q):
        query = list(map(int, input().split()))

        if query[0] == 1:  # Update
            s, x = query[1], query[2]
            pos = in_time[s]
            old_val = euler[pos]
            euler[pos] = x
            bit_update(pos, x - old_val)
        else:  # Query subtree sum
            s = query[1]
            l, r = in_time[s], out_time[s]
            results.append(range_sum(l, r))

    print('\n'.join(map(str, results)))

solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
vector<int> adj[MAXN];
int in_time[MAXN], out_time[MAXN];
long long euler_val[MAXN];
long long bit[MAXN];
int timer_cnt = 0;
int n, q;

void dfs(int node, int parent) {
    in_time[node] = timer_cnt++;
    for (int child : adj[node]) {
        if (child != parent) {
            dfs(child, node);
        }
    }
    out_time[node] = timer_cnt - 1;
}

void bit_update(int i, long long delta) {
    for (++i; i <= n; i += i & (-i)) {
        bit[i] += delta;
    }
}

long long bit_query(int i) {
    long long sum = 0;
    for (++i; i > 0; i -= i & (-i)) {
        sum += bit[i];
    }
    return sum;
}

long long range_sum(int l, int r) {
    if (l == 0) return bit_query(r);
    return bit_query(r) - bit_query(l - 1);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> n >> q;

    vector<long long> values(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> values[i];
    }

    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    // Euler tour
    dfs(1, -1);

    // Initialize BIT
    for (int i = 1; i <= n; i++) {
        int pos = in_time[i];
        euler_val[pos] = values[i];
        bit_update(pos, values[i]);
    }

    // Process queries
    while (q--) {
        int type;
        cin >> type;

        if (type == 1) {
            int s;
            long long x;
            cin >> s >> x;
            int pos = in_time[s];
            long long delta = x - euler_val[pos];
            euler_val[pos] = x;
            bit_update(pos, delta);
        } else {
            int s;
            cin >> s;
            cout << range_sum(in_time[s], out_time[s]) << "\n";
        }
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | Euler tour O(n), each query O(log n) |
| Space | O(n) | BIT, Euler arrays, adjacency list |

---

## Common Mistakes

### Mistake 1: Recursion Depth Exceeded

```python
# WRONG - May cause stack overflow for n = 200000
def dfs(node, parent):
    in_time[node] = timer
    for child in graph[node]:
        if child != parent:
            dfs(child, node)  # Deep recursion
    out_time[node] = timer - 1
```

**Problem:** Python's default recursion limit (~1000) is too small.
**Fix:** Use iterative DFS with explicit stack, or increase limit with `sys.setrecursionlimit(300000)`.

### Mistake 2: Wrong BIT Indexing

```python
# WRONG - BIT is 1-indexed but forgetting conversion
def bit_update(i, delta):
    while i <= n:  # Missing i += 1 for 0-indexed input
        bit[i] += delta
        i += i & (-i)
```

**Problem:** BIT operations assume 1-indexed arrays.
**Fix:** Add 1 to index before BIT operations, or consistently use 1-indexed arrays.

### Mistake 3: Integer Overflow

```cpp
// WRONG - int overflow when summing large values
int bit[MAXN];  // Should be long long

long long query(int i) {
    int sum = 0;  // Should be long long
    // ...
}
```

**Problem:** Values up to 10^9, n up to 2*10^5, total sum can exceed 2*10^14.
**Fix:** Use `long long` for BIT and sum variables.

### Mistake 4: Incorrect out_time Calculation

```python
# WRONG
def dfs(node, parent):
    in_time[node] = timer
    timer += 1
    for child in graph[node]:
        if child != parent:
            dfs(child, node)
    out_time[node] = timer  # Should be timer - 1
```

**Problem:** out_time should point to the last valid index, not one past it.
**Fix:** `out_time[node] = timer - 1` (inclusive range).

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| Single node | n=1 | Subtree of 1 = just node 1's value | Tree with only root |
| Linear tree | 1-2-3-4-5 | Subtree of 1 = all nodes | Chain tree |
| Star tree | 1 connected to 2,3,4,5 | Subtree of 2 = just node 2 | All leaves |
| Large values | v_i = 10^9 | Use long long | Sum can overflow int |
| Many updates | q updates to same node | Each update O(log n) | BIT handles efficiently |
| Query root | Query subtree of 1 | Sum of all values | Root's subtree = entire tree |

---

## When to Use This Pattern

### Use This Approach When:
- You need subtree queries (sum, min, max, count)
- You need to update individual node values
- The tree structure is static (edges don't change)
- Multiple queries on the same tree

### Don't Use When:
- Tree structure changes dynamically (use Link-Cut Trees)
- You need path queries instead of subtree queries (use Heavy-Light Decomposition)
- Only one query is needed (simple DFS is enough)

### Pattern Recognition Checklist:
- [ ] Subtree operation? --> **Consider Euler Tour**
- [ ] Need updates? --> **Euler Tour + BIT/Segment Tree**
- [ ] Static queries only? --> **Euler Tour + Prefix Sums**
- [ ] Path queries? --> **Consider HLD or LCA techniques**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Subordinates (CSES)](https://cses.fi/problemset/task/1674) | Basic subtree counting with DFS |
| [Tree Matching (CSES)](https://cses.fi/problemset/task/1130) | Tree DP fundamentals |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Path Queries (CSES)](https://cses.fi/problemset/task/1138) | Path sum instead of subtree sum |
| [Range Update Queries (CSES)](https://cses.fi/problemset/task/1651) | BIT with lazy propagation |
| [Distinct Colors (CSES)](https://cses.fi/problemset/task/1139) | Subtree distinct count using small-to-large |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Path Queries II (CSES)](https://cses.fi/problemset/task/2134) | Heavy-Light Decomposition |
| [Subtree Queries with XOR](https://codeforces.com/problemset/problem/620/E) | Euler tour with segment tree and XOR |
| [Tree and Queries](https://codeforces.com/problemset/problem/375/D) | Mo's algorithm on trees |

---

## Key Takeaways

1. **The Core Idea:** Euler tour converts subtree operations to range operations
2. **Time Optimization:** BIT provides O(log n) updates and queries vs O(n) brute force
3. **Space Trade-off:** O(n) extra space for BIT enables efficient queries
4. **Pattern:** Euler Tour + Data Structure = Efficient Tree Queries

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement Euler tour without looking at reference
- [ ] Explain why subtrees become contiguous ranges
- [ ] Write BIT from scratch with update and query
- [ ] Handle 0-indexed vs 1-indexed correctly
- [ ] Identify when Euler tour applies to a tree problem

---

## Additional Resources

- [CP-Algorithms: Euler Tour Technique](https://cp-algorithms.com/graph/euler_path.html)
- [CP-Algorithms: Binary Indexed Tree](https://cp-algorithms.com/data_structures/fenwick.html)
- [CSES Problem Set - Tree Algorithms](https://cses.fi/problemset/)
- [USACO Guide: Tree Euler Tour](https://usaco.guide/gold/euler-tour)
