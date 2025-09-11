---
layout: simple
title: "Distance Queries"
permalink: /problem_soulutions/tree_algorithms/distance_queries_analysis
---

# Distance Queries

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

Given a tree with n nodes, process q queries of the form "find the distance between nodes a and b".

**Input**: 
- First line: n (number of nodes)
- Next n-1 lines: edges of the tree
- Next line: q (number of queries)
- Next q lines: two integers a and b (query nodes)

**Output**: 
- q lines: distance between nodes a and b

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵

**Example**:
```
Input:
5
1 2
2 3
2 4
4 5
3
1 3
2 5
1 5

Output:
2
3
4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, perform BFS from node a to find distance to node b
2. Return the distance for each query
3. Use BFS to find shortest path in unweighted tree

**Implementation**:
```python
def brute_force_distance_queries(n, edges, queries):
    from collections import deque, defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def find_distance(a, b):
        if a == b:
            return 0
        
        # BFS to find distance from a to b
        queue = deque([(a, 0)])
        visited = {a}
        
        while queue:
            node, dist = queue.popleft()
            
            if node == b:
                return dist
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return -1  # Should not happen in a tree
    
    results = []
    for a, b in queries:
        distance = find_distance(a, b)
        results.append(distance)
    
    return results
```

**Analysis**:
- **Time**: O(q × n) - For each query, BFS takes O(n) time
- **Space**: O(n) - Queue and visited set
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with LCA
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute LCA using binary lifting
2. For each query, find LCA of a and b
3. Calculate distance as depth[a] + depth[b] - 2 * depth[LCA]

**Implementation**:
```python
def optimized_distance_queries(n, edges, queries):
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
    
    def dfs(node, parent):
        up[0][node] = parent
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
        distance = depth[a] + depth[b] - 2 * depth[lca_node]
        results.append(distance)
    
    return results
```

**Analysis**:
- **Time**: O(n log n + q log n) - Preprocessing + query processing
- **Space**: O(n log n) - Binary lifting table
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with LCA
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Use binary lifting to precompute LCA efficiently
2. For each query, find LCA and calculate distance using depth formula
3. Distance = depth[a] + depth[b] - 2 * depth[LCA]

**Implementation**:
```python
def optimal_distance_queries(n, edges, queries):
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
    
    def dfs(node, parent):
        up[0][node] = parent
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
        distance = depth[a] + depth[b] - 2 * depth[lca_node]
        results.append(distance)
    
    return results
```

**Analysis**:
- **Time**: O(n log n + q log n) - Preprocessing + query processing
- **Space**: O(n log n) - Binary lifting table
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
Tree structure:
    1
    |
    2
   / \
3   4
    |
    5

Depth array: [0, 1, 2, 2, 3, 4]

Query: Distance between nodes 1 and 5
1. LCA(1, 5) = 1
2. Distance = depth[1] + depth[5] - 2 * depth[1]
3. Distance = 1 + 4 - 2 * 1 = 3
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(n) | BFS for each query |
| Optimized | O(n log n + q log n) | O(n log n) | LCA with binary lifting |
| Optimal | O(n log n + q log n) | O(n log n) | LCA with binary lifting |

### Time Complexity
- **Time**: O(n log n + q log n) - Preprocessing + query processing with LCA
- **Space**: O(n log n) - Binary lifting table

### Why This Solution Works
- **LCA Technique**: Use lowest common ancestor to break path into two parts
- **Binary Lifting**: Efficiently find LCA in O(log n) time
- **Depth Formula**: Calculate distance using depth[a] + depth[b] - 2 * depth[LCA]
- **Optimal Approach**: LCA with binary lifting provides the best possible complexity for distance queries
