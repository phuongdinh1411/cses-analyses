---
layout: simple
title: "Longest Path"
permalink: /problem_soulutions/dynamic_programming_at/longest_path_analysis
---

# Longest Path

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand DP on Directed Acyclic Graphs (DAGs)
- Apply topological sorting for DP computation
- Recognize when to use DP on graphs
- Implement longest path algorithms using DP
- Handle graph-based DP problems efficiently

## 📋 Problem Description

There is a directed graph G with N vertices and M edges. The vertices are numbered 1, 2, ..., N, and each edge is directed from a vertex with a smaller number to a vertex with a larger number. G is a DAG (Directed Acyclic Graph). Find the length of the longest path in G. Here, the length of a path is the number of edges in it.

**Input**: 
- First line: N, M (2 ≤ N ≤ 10^5, 1 ≤ M ≤ 10^5)
- Next M lines: x_i, y_i (1 ≤ x_i < y_i ≤ N) - edge from x_i to y_i

**Output**: 
- Print the length of the longest path

**Constraints**:
- 2 ≤ N ≤ 10^5
- 1 ≤ M ≤ 10^5
- 1 ≤ x_i < y_i ≤ N
- G is a DAG (guaranteed by x_i < y_i)

**Example**:
```
Input:
4 5
1 2
1 3
2 3
2 4
3 4

Output:
3

Explanation**: 
Graph structure:
1 → 2 → 3 → 4
1 → 3 → 4
1 → 2 → 4

Longest path: 1 → 2 → 3 → 4 (length 3)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: DFS with Memoization (Optimal)

**Key Insights from DFS Solution**:
- **DFS Approach**: Use DFS to explore all paths from each vertex
- **Memoization**: Cache results to avoid recomputation
- **DAG Property**: Since graph is acyclic, DFS is safe
- **Efficient**: O(V + E) time complexity

**Key Insight**: For a DAG, we can use DFS with memoization to compute longest path from each vertex. The longest path overall is the maximum over all starting vertices.

#### 📌 **DP State Definition**

**What does `dp[v]` represent?**
- `dp[v]` = **length of longest path** starting from vertex v
- This is a 1D DP array where index v represents the vertex
- `dp[v]` stores the maximum number of edges in any path starting from v
- Final answer = max(dp[v]) over all vertices v

**In plain language:**
- For each vertex, we store the length of the longest path that starts from that vertex
- We can compute dp[v] by considering all neighbors u of v and taking the maximum

#### 🎯 **DP Thinking Process**

**Step 1: Identify the Subproblem**
- What are we trying to maximize? The length of the longest path in the graph
- What information do we need? For each vertex, the longest path starting from it

**Step 2: Define the DP State** (See DP State Definition section above)

**Step 3: Find the Recurrence Relation (State Transition)**
- How do we compute `dp[v]`?
- From vertex v, we can go to any neighbor u
- If we go to u, the path length becomes 1 + dp[u]
- Therefore: `dp[v] = max(1 + dp[u])` for all neighbors u of v
- Base case: If v has no outgoing edges, `dp[v] = 0`

**Step 4: Determine Base Cases**
- `dp[v] = 0` if v has no outgoing edges (sink vertex)

**Step 5: Identify the Answer**
- The answer is `max(dp[v])` over all vertices v

#### 📊 **Visual DP Table Construction**

For the example graph:
```
Vertices: 1, 2, 3, 4
Edges: 1→2, 1→3, 2→3, 2→4, 3→4

Graph structure:
1 → 2 → 3 → 4
  ↘   ↗
   3 → 4

DFS with memoization:
┌─────────────────────────────────────┐
│ dp[4] = 0 (no outgoing edges)       │
│                                     │
│ dp[3] = 1 + dp[4] = 1 + 0 = 1      │
│                                     │
│ dp[2] = max(1 + dp[3], 1 + dp[4]) │
│      = max(1 + 1, 1 + 0) = 2       │
│                                     │
│ dp[1] = max(1 + dp[2], 1 + dp[3]) │
│      = max(1 + 2, 1 + 1) = 3       │
│                                     │
│ Final answer: max(dp) = 3          │
└─────────────────────────────────────┘
```

**Algorithm**:
- Build adjacency list representation of graph
- Initialize `dp[v] = -1` (unvisited) for all vertices
- For each vertex v:
  - If `dp[v] == -1`, compute it using DFS
  - `dp[v] = max(1 + dp[u])` for all neighbors u
- Return `max(dp[v])` over all vertices

**Visual Example**:
```
DP computation order (topological order):
Vertex 4: dp[4] = 0 (sink)
Vertex 3: dp[3] = 1 + dp[4] = 1
Vertex 2: dp[2] = max(1 + dp[3], 1 + dp[4]) = max(2, 1) = 2
Vertex 1: dp[1] = max(1 + dp[2], 1 + dp[3]) = max(3, 2) = 3

Longest path: 1 → 2 → 3 → 4 (length 3)
```

**Implementation**:
```python
def longest_path_dfs(n, m, edges):
    """
    DFS with memoization solution for Longest Path problem
    
    Args:
        n: number of vertices
        m: number of edges
        edges: list of (u, v) tuples representing edges
    
    Returns:
        int: length of longest path
    """
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
    
    # dp[v] = longest path starting from vertex v
    dp = [-1] * (n + 1)
    
    def dfs(v):
        """Compute longest path from vertex v"""
        # If already computed, return cached value
        if dp[v] != -1:
            return dp[v]
        
        # Base case: no outgoing edges
        if len(graph[v]) == 0:
            dp[v] = 0
            return 0
        
        # Try all neighbors
        max_path = 0
        for u in graph[v]:
            max_path = max(max_path, 1 + dfs(u))
        
        dp[v] = max_path
        return max_path
    
    # Compute longest path from each vertex
    max_length = 0
    for v in range(1, n + 1):
        if dp[v] == -1:
            dfs(v)
        max_length = max(max_length, dp[v])
    
    return max_length

# Example usage
n, m = 4, 5
edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
result = longest_path_dfs(n, m, edges)
print(f"Longest path length: {result}")  # Output: 3
```

**Time Complexity**: O(V + E)
**Space Complexity**: O(V + E)

**Why it's optimal**: Uses DFS with memoization for O(V + E) time complexity, which is optimal for this problem.

---

### Approach 2: Topological Sort + DP

**Key Insights from Topological Sort Solution**:
- **Topological Order**: Process vertices in topological order
- **DAG Property**: Guaranteed topological ordering exists
- **Iterative DP**: Fill DP table in topological order
- **Efficient**: O(V + E) time complexity

**Key Insight**: Since the graph is a DAG, we can process vertices in topological order. This ensures that when we compute dp[v], all neighbors u have already been processed.

**Algorithm**:
- Compute topological ordering of vertices
- Process vertices in topological order
- For each vertex v, compute dp[v] using already computed neighbors

**Implementation**:
```python
def longest_path_topological(n, m, edges):
    """
    Topological sort + DP solution for Longest Path problem
    
    Args:
        n: number of vertices
        m: number of edges
        edges: list of (u, v) tuples representing edges
    
    Returns:
        int: length of longest path
    """
    # Build graph and in-degree array
    graph = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    # Topological sort using Kahn's algorithm
    queue = []
    for v in range(1, n + 1):
        if in_degree[v] == 0:
            queue.append(v)
    
    topo_order = []
    while queue:
        v = queue.pop(0)
        topo_order.append(v)
        for u in graph[v]:
            in_degree[u] -= 1
            if in_degree[u] == 0:
                queue.append(u)
    
    # DP: dp[v] = longest path starting from v
    dp = [0] * (n + 1)
    
    # Process vertices in reverse topological order
    # (so we process sinks first, then sources)
    for v in reversed(topo_order):
        for u in graph[v]:
            dp[v] = max(dp[v], 1 + dp[u])
    
    return max(dp[1:])

# Example usage
n, m = 4, 5
edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
result = longest_path_topological(n, m, edges)
print(f"Longest path length: {result}")  # Output: 3
```

**Time Complexity**: O(V + E)
**Space Complexity**: O(V + E)

**Why it's equivalent**: Both approaches achieve O(V + E) complexity, choose based on preference.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS with Memoization | O(V + E) | O(V + E) | Cache results during DFS |
| Topological Sort + DP | O(V + E) | O(V + E) | Process in topological order |

### Time Complexity
- **Time**: O(V + E) - Visit each vertex and edge once
- **Space**: O(V + E) - Graph representation and DP array

### Why This Solution Works
- **DAG Property**: Graph is acyclic, so longest path is well-defined
- **Optimal Substructure**: Longest path from v depends on longest paths from neighbors
- **Memoization**: Cache results to avoid recomputation
- **Topological Order**: Ensures dependencies are resolved before computation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Longest Path - Path Reconstruction**
**Problem**: Find longest path and reconstruct the actual path.

**Implementation**:
```python
def longest_path_with_path(n, m, edges):
    """
    Longest path with path reconstruction
    
    Args:
        n: number of vertices
        m: number of edges
        edges: list of (u, v) tuples
    
    Returns:
        tuple: (longest path length, actual path)
    """
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
    
    dp = [-1] * (n + 1)
    next_vertex = [-1] * (n + 1)
    
    def dfs(v):
        if dp[v] != -1:
            return dp[v]
        
        if len(graph[v]) == 0:
            dp[v] = 0
            return 0
        
        max_path = 0
        best_next = -1
        for u in graph[v]:
            path_len = 1 + dfs(u)
            if path_len > max_path:
                max_path = path_len
                best_next = u
        
        dp[v] = max_path
        next_vertex[v] = best_next
        return max_path
    
    # Find starting vertex with longest path
    max_length = 0
    start_vertex = 1
    for v in range(1, n + 1):
        if dp[v] == -1:
            dfs(v)
        if dp[v] > max_length:
            max_length = dp[v]
            start_vertex = v
    
    # Reconstruct path
    path = [start_vertex]
    current = start_vertex
    while next_vertex[current] != -1:
        current = next_vertex[current]
        path.append(current)
    
    return max_length, path

# Example usage
n, m = 4, 5
edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
length, path = longest_path_with_path(n, m, edges)
print(f"Longest path length: {length}")
print(f"Path: {path}")
```

#### **2. Longest Path - Weighted Edges**
**Problem**: Find longest path when edges have weights.

**Implementation**:
```python
def longest_path_weighted(n, m, weighted_edges):
    """
    Longest path with weighted edges
    
    Args:
        n: number of vertices
        m: number of edges
        weighted_edges: list of (u, v, weight) tuples
    
    Returns:
        int: maximum total weight of a path
    """
    graph = [[] for _ in range(n + 1)]
    for u, v, w in weighted_edges:
        graph[u].append((v, w))
    
    dp = [-1] * (n + 1)
    
    def dfs(v):
        if dp[v] != -1:
            return dp[v]
        
        if len(graph[v]) == 0:
            dp[v] = 0
            return 0
        
        max_weight = 0
        for u, w in graph[v]:
            max_weight = max(max_weight, w + dfs(u))
        
        dp[v] = max_weight
        return max_weight
    
    max_total = 0
    for v in range(1, n + 1):
        if dp[v] == -1:
            dfs(v)
        max_total = max(max_total, dp[v])
    
    return max_total

# Example usage
n, m = 4, 5
weighted_edges = [(1, 2, 5), (1, 3, 3), (2, 3, 2), (2, 4, 4), (3, 4, 1)]
result = longest_path_weighted(n, m, weighted_edges)
print(f"Maximum path weight: {result}")
```

### Related Problems

#### **AtCoder Problems**
- [Grid 1](https://atcoder.jp/contests/dp/tasks/dp_h) - Similar DP pattern on grid
- [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) - Similar concept

#### **LeetCode Problems**
- [Longest Increasing Path in Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) - Similar on grid
- [Longest Path With Different Adjacent Characters](https://leetcode.com/problems/longest-path-with-different-adjacent-characters/) - Tree version

#### **CSES Problems**
- [Longest Flight Route](https://cses.fi/problemset/task/1680) - Similar problem
- [Game Routes](https://cses.fi/problemset/task/1681) - Counting paths

#### **Problem Categories**
- **DP on DAGs**: Dynamic programming on directed acyclic graphs
- **Graph DP**: Applying DP to graph problems
- **Longest Path**: Finding maximum length paths

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming on DAGs](https://cp-algorithms.com/graph/longest_path_in_dag.html) - DAG DP algorithms
- [Topological Sorting](https://cp-algorithms.com/graph/topological-sort.html) - Topological sort algorithms

### **Practice Problems**
- [AtCoder DP Contest Problem G](https://atcoder.jp/contests/dp/tasks/dp_g) - Original problem
- [CSES Longest Flight Route](https://cses.fi/problemset/task/1680) - Similar problem

### **Further Reading**
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms) - Graph algorithms chapter
- [Competitive Programming Handbook](https://cses.fi/book/book.pdf) - DP and graphs section

