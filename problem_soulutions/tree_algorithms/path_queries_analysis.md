---
layout: simple
title: "Path Queries"
permalink: /problem_soulutions/tree_algorithms/path_queries_analysis
---

# Path Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand tree algorithms and tree traversal techniques
- Apply efficient tree processing algorithms
- Implement advanced tree data structures and algorithms
- Optimize tree operations for large inputs
- Handle edge cases in tree problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tree algorithms, DFS, BFS, tree DP, centroid decomposition
- **Data Structures**: Trees, graphs, segment trees, binary indexed trees
- **Mathematical Concepts**: Tree theory, graph theory, dynamic programming
- **Programming Skills**: Tree traversal, algorithm implementation
- **Related Problems**: Other tree algorithm problems in this section

## 📋 Problem Description

Given a tree with n nodes, each node has a value. Process q queries of the form "find the sum of values on the path from node a to node b".

**Input**: 
- First line: n (number of nodes)
- Next n lines: values of nodes 1 to n
- Next n-1 lines: edges of the tree
- Next line: q (number of queries)
- Next q lines: two integers a and b (path endpoints)

**Output**: 
- q lines: sum of values on the path from a to b

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 1 ≤ value ≤ 10⁹

**Example**:
```
Input:
5
1 2 3 4 5
1 2
2 3
2 4
4 5
3
1 3
2 5
1 5

Output:
6
11
15
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, find the path from a to b using DFS
2. Sum the values along the path
3. Return the sum for each query

**Implementation**:
```python
def brute_force_path_queries(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def find_path(a, b):
        # Find path from a to b using DFS
        path = []
        visited = set()
        
        def dfs(node, target, current_path):
            if node == target:
                return current_path + [node]
            
            visited.add(node)
            for child in graph[node]:
                if child not in visited:
                    result = dfs(child, target, current_path + [node])
                    if result:
                        return result
            return None
        
        return dfs(a, b, [])
    
    results = []
    for a, b in queries:
        path = find_path(a, b)
        path_sum = sum(values[node - 1] for node in path)
        results.append(path_sum)
    
    return results
```

**Analysis**:
- **Time**: O(q × n) - For each query, DFS takes O(n) time
- **Space**: O(n) - Recursion stack and path storage
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with LCA
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute LCA using binary lifting
2. For each query, find LCA of a and b
3. Sum values from a to LCA and from b to LCA

**Implementation**:
```python
def optimized_path_queries(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Precompute LCA using binary lifting
    LOG = 20
    up = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    path_sum = [0] * (n + 1)
    
    def dfs(node, parent):
        up[0][node] = parent
        path_sum[node] = path_sum[parent] + values[node - 1]
        depth[node] = depth[parent] + 1
        
        for child in graph[node]:
            if child != parent:
                dfs(child, node)
    
    dfs(1, 0)
    
    # Binary lifting
    for k in range(1, LOG):
        for node in range(1, n + 1):
            up[k][node] = up[k-1][up[k-1][node]]
    
    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        for k in range(LOG - 1, -1, -1):
            if depth[a] - (1 << k) >= depth[b]:
                a = up[k][a]
        
        if a == b:
            return a
        
        # Find LCA
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        
        return up[0][a]
    
    results = []
    for a, b in queries:
        lca_node = lca(a, b)
        # Sum from a to LCA + sum from b to LCA - LCA value (counted twice)
        sum_a_to_lca = path_sum[a] - path_sum[lca_node] + values[lca_node - 1]
        sum_b_to_lca = path_sum[b] - path_sum[lca_node] + values[lca_node - 1]
        total_sum = sum_a_to_lca + sum_b_to_lca - values[lca_node - 1]
        results.append(total_sum)
    
    return results
```

**Analysis**:
- **Time**: O(n log n + q log n) - Preprocessing + query processing
- **Space**: O(n log n) - Binary lifting table
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Heavy-Light Decomposition
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use heavy-light decomposition to break tree into chains
2. Use segment trees on each chain for efficient range queries
3. For each query, break path into O(log n) segments

**Implementation**:
```python
def optimal_path_queries(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Heavy-light decomposition
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    size = [0] * (n + 1)
    heavy = [0] * (n + 1)
    head = [0] * (n + 1)
    pos = [0] * (n + 1)
    
    def dfs_size(node, par):
        parent[node] = par
        size[node] = 1
        heavy[node] = 0
        
        for child in graph[node]:
            if child != par:
                depth[child] = depth[node] + 1
                size[node] += dfs_size(child, node)
                if size[child] > size[heavy[node]]:
                    heavy[node] = child
        
        return size[node]
    
    dfs_size(1, 0)
    
    # Decompose tree into chains
    current_pos = 0
    def decompose(node, h):
        nonlocal current_pos
        head[node] = h
        pos[node] = current_pos
        current_pos += 1
        
        if heavy[node]:
            decompose(heavy[node], h)
        
        for child in graph[node]:
            if child != parent[node] and child != heavy[node]:
                decompose(child, child)
    
    decompose(1, 1)
    
    # Build segment tree for each chain
    chain_values = [0] * n
    for node in range(1, n + 1):
        chain_values[pos[node]] = values[node - 1]
    
    # Simple segment tree for range sum
    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [0] * (4 * self.n)
            self.build(arr, 1, 0, self.n - 1)
        
        def build(self, arr, node, start, end):
            if start == end:
                self.tree[node] = arr[start]
            else:
                mid = (start + end) // 2
                self.build(arr, 2 * node, start, mid)
                self.build(arr, 2 * node + 1, mid + 1, end)
                self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
        
        def query(self, node, start, end, l, r):
            if r < start or end < l:
                return 0
            if l <= start and end <= r:
                return self.tree[node]
            mid = (start + end) // 2
            return (self.query(2 * node, start, mid, l, r) + 
                    self.query(2 * node + 1, mid + 1, end, l, r))
    
    st = SegmentTree(chain_values)
    
    def path_query(a, b):
        total_sum = 0
        
        while head[a] != head[b]:
            if depth[head[a]] > depth[head[b]]:
                a, b = b, a
            
            # Add sum from b to head[b]
            total_sum += st.query(1, 0, n - 1, pos[head[b]], pos[b])
            b = parent[head[b]]
        
        # Add sum from a to b (they're in same chain now)
        if depth[a] > depth[b]:
            a, b = b, a
        total_sum += st.query(1, 0, n - 1, pos[a], pos[b])
        
        return total_sum
    
    results = []
    for a, b in queries:
        results.append(path_query(a, b))
    
    return results
```

**Analysis**:
- **Time**: O(n + q log n) - Preprocessing + query processing
- **Space**: O(n) - Heavy-light decomposition and segment tree
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
Tree structure:
    1(1)
    |
    2(2)
   / \
3(3) 4(4)
      |
    5(5)

Heavy-Light Decomposition:
Chain 1: 1-2-4-5 (heavy edges)
Chain 2: 3 (light edge)

Path Query (1, 5):
1. 1 → 2 (same chain)
2. 2 → 4 (same chain)
3. 4 → 5 (same chain)
Total: 1 + 2 + 4 + 5 = 12
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(n) | DFS for each query |
| Optimized | O(n log n + q log n) | O(n log n) | LCA with binary lifting |
| Optimal | O(n + q log n) | O(n) | Heavy-light decomposition |

### Time Complexity
- **Time**: O(n + q log n) - Preprocessing + query processing with HLD
- **Space**: O(n) - Heavy-light decomposition and segment tree

### Why This Solution Works
- **LCA Technique**: Use lowest common ancestor to break path into two parts
- **Binary Lifting**: Efficiently find LCA in O(log n) time
- **Heavy-Light Decomposition**: Break tree into chains for efficient range queries
- **Optimal Approach**: Heavy-light decomposition provides the best possible complexity for path queries
