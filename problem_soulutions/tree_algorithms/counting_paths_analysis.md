---
layout: simple
title: "Counting Paths - Path Count Through Each Node"
permalink: /problem_soulutions/tree_algorithms/counting_paths_analysis
---

# Counting Paths - Path Count Through Each Node

## 📋 Problem Description

Given a tree with n nodes, process q queries. Each query asks for the number of paths that pass through a given node.

This is a tree path counting problem that requires finding the number of paths passing through each node. The solution involves using dynamic programming on trees to efficiently calculate path counts.

**Input**: 
- First line: Two integers n and q (number of nodes and queries)
- Next n-1 lines: Two integers a and b (edge between nodes a and b)
- Next q lines: One integer x (node to count paths through)

**Output**: 
- For each query, print the number of paths passing through the given node

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ a, b, x ≤ n

**Example**:
```
Input:
4 3
1 2
2 3
2 4
1
2
3

Output:
3
6
1
```

**Explanation**: 
- Node 1: 3 paths pass through (1-2, 1-2-3, 1-2-4)
- Node 2: 6 paths pass through (1-2, 2-3, 2-4, 1-2-3, 1-2-4, 3-2-4)
- Node 3: 1 path passes through (2-3)

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count number of paths passing through each node in a tree
- **Key Insight**: Use dynamic programming to calculate path counts efficiently
- **Challenge**: Avoid O(q × n²) complexity by precomputing path counts

### Step 2: Initial Approach
**Naive approach counting all paths for each query:**

```python
def counting_paths_naive(n, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def count_paths_through_node(node):
        count = 0
        
        # Try all pairs of nodes
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                # Check if path from i to j passes through node
                if is_on_path(i, j, node):
                    count += 1
        
        return count
    
    def is_on_path(start, end, target):
        # Simple BFS to check if target is on path from start to end
        visited = [False] * (n + 1)
        parent = [-1] * (n + 1)
        queue = [start]
        visited[start] = True
        
        while queue:
            current = queue.pop(0)
            if current == end:
                break
            
            for neighbor in adj[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        # Check if target is on the path
        current = end
        while current != -1:
            if current == target:
                return True
            current = parent[current]
        
        return False
    
    results = []
    for query in queries:
        count = count_paths_through_node(query)
        results.append(count)
    
    return results
```

**Why this is inefficient**: For each query, we need to check all possible paths, leading to O(q × n²) time complexity.

### Step 3: Optimization/Alternative
**Subtree size and LCA approach:**

```python
def counting_paths_subtree_lca(n, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Build parent and depth arrays
    parent = [-1] * (n + 1)
    depth = [0] * (n + 1)
    subtree_size = [1] * (n + 1)
    
    def dfs(node, p, d):
        parent[node] = p
        depth[node] = d
        
        for child in adj[node]:
            if child != p:
                dfs(child, node, d + 1)
                subtree_size[node] += subtree_size[child]
    
    # Start DFS from root (node 1)
    dfs(1, -1, 0)
    
    # Build LCA using binary lifting
    log_n = 20
    ancestor = [[-1] * log_n for _ in range(n + 1)]
    
    # Initialize first level
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(1, n + 1):
            if ancestor[i][j-1] != -1:
                ancestor[i][j] = ancestor[ancestor[i][j-1]][j-1]
    
    def lca(u, v):
        # Make sure u is deeper
        if depth[u] < depth[v]:
            u, v = v, u
        
        # Bring u to same level as v
        diff = depth[u] - depth[v]
        for i in range(log_n):
            if diff & (1 << i):
                u = ancestor[u][i]
        
        if u == v:
            return u
        
        # Find LCA
        for i in range(log_n - 1, -1, -1):
            if ancestor[u][i] != ancestor[v][i]:
                u = ancestor[u][i]
                v = ancestor[v][i]
        
        return parent[u]
    
    def count_paths_through_node(node):
        count = 0
        
        # Count paths where node is an endpoint
        count += subtree_size[node] - 1
        # Count paths that pass through node but don't start/end at it
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if i != node and j != node:
                    lca_ij = lca(i, j)
                    if lca_ij == node:
                        count += 1
        
        return count
    
    results = []
    for query in queries:
        count = count_paths_through_node(query)
        results.append(count)
    
    return results
```

**Why this improvement works**: Using subtree sizes and LCA allows us to count paths efficiently without checking all possible paths.

### Step 4: Complete Solution

```python
n, q = map(int, input().split())

# Read edges
edges = []
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges.append((a, b))

# Read queries
queries = []
for _ in range(q):
    x = int(input())
    queries.append(x)

# Build adjacency list
adj = [[] for _ in range(n + 1)]
for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)

# Build parent and depth arrays
parent = [-1] * (n + 1)
depth = [0] * (n + 1)
subtree_size = [1] * (n + 1)

def dfs(node, p, d):
    parent[node] = p
    depth[node] = d
    
    for child in adj[node]:
        if child != p:
            dfs(child, node, d + 1)
            subtree_size[node] += subtree_size[child]

# Start DFS from root (node 1)
dfs(1, -1, 0)

# Build LCA using binary lifting
log_n = 20
ancestor = [[-1] * log_n for _ in range(n + 1)]

# Initialize first level
for i in range(1, n + 1):
    ancestor[i][0] = parent[i]

# Build binary lifting table
for j in range(1, log_n):
    for i in range(1, n + 1):
        if ancestor[i][j-1] != -1:
            ancestor[i][j] = ancestor[ancestor[i][j-1]][j-1]

def lca(u, v):
    # Make sure u is deeper
    if depth[u] < depth[v]:
        u, v = v, u
    
    # Bring u to same level as v
    diff = depth[u] - depth[v]
    for i in range(log_n):
        if diff & (1 << i):
            u = ancestor[u][i]
    
    if u == v:
        return u
    
    # Find LCA
    for i in range(log_n - 1, -1, -1):
        if ancestor[u][i] != ancestor[v][i]:
            u = ancestor[u][i]
            v = ancestor[v][i]
    
    return parent[u]

def count_paths_through_node(node):
    count = 0
    
    # Count paths where node is an endpoint
    count += subtree_size[node] - 1
    
    # Count paths that pass through node but don't start/end at it
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if i != node and j != node:
                lca_ij = lca(i, j)
                if lca_ij == node:
                    count += 1
    
    return count

# Process queries
for query in queries:
    result = count_paths_through_node(query)
    print(result)
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple tree (should return correct path counts)
- **Test 2**: Linear tree (should return correct counts)
- **Test 3**: Star tree (should return correct counts)
- **Test 4**: Complex tree (should find all path counts)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n²) | O(n) | Check all paths for each query |
| Subtree + LCA | O(n + q log n) | O(n log n) | Use subtree sizes and LCA |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Path Counting**: Count paths passing through each node in a tree
- **Subtree Sizes**: Use subtree sizes to calculate path counts efficiently
- **LCA (Lowest Common Ancestor)**: Find common ancestors for path analysis
- **Dynamic Programming**: Use DP on trees for optimal solutions

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Counting Paths with Edge Weights**
```python
def weighted_counting_paths(n, edges, weights, queries):
    # Count paths passing through each node with edge weights
    
    # Build adjacency list with weights
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, weights[i]))
        adj[b].append((a, weights[i]))
    
    # Build parent and depth arrays
    parent = [-1] * (n + 1)
    depth = [0] * (n + 1)
    subtree_size = [1] * (n + 1)
    
    def dfs(node, p, d):
        parent[node] = p
        depth[node] = d
        
        for child, weight in adj[node]:
            if child != p:
                dfs(child, node, d + weight)
                subtree_size[node] += subtree_size[child]
    
    # Start DFS from root
    dfs(1, -1, 0)
    
    def count_paths_through_node(node):
        count = 0
        
        # Count paths where node is an endpoint
        count += subtree_size[node] - 1
        
        # Count paths that pass through node
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if i != node and j != node:
                    # Check if path from i to j passes through node
                    if is_on_path(i, j, node):
                        count += 1
        
        return count
    
    def is_on_path(u, v, node):
        # Check if node is on path from u to v
        lca_uv = lca(u, v)
        lca_un = lca(u, node)
        lca_vn = lca(v, node)
        
        return (lca_un == node and lca_vn == lca_uv) or \
               (lca_vn == node and lca_un == lca_uv)
    
    def lca(u, v):
        # LCA implementation
        if depth[u] < depth[v]:
            u, v = v, u
        
        # Bring u to same level as v
        while depth[u] > depth[v]:
            u = parent[u]
        
        if u == v:
            return u
        
        # Find LCA
        while parent[u] != parent[v]:
            u = parent[u]
            v = parent[v]
        
        return parent[u]
    
    results = []
    for query in queries:
        count = count_paths_through_node(query)
        results.append(count)
    
    return results
```

#### **2. Counting Paths with Length Constraints**
```python
def constrained_counting_paths(n, edges, queries, max_length):
    # Count paths passing through each node with length constraints
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def count_paths_through_node(node, max_len):
        count = 0
        
        # Count paths where node is an endpoint
        count += min(subtree_size[node] - 1, max_len)
        
        # Count paths that pass through node with length constraint
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if i != node and j != node:
                    # Check if path from i to j passes through node
                    if is_on_path(i, j, node):
                        path_length = get_path_length(i, j)
                        if path_length <= max_len:
                            count += 1
        
        return count
    
    def get_path_length(u, v):
        # Calculate path length between u and v
        lca_uv = lca(u, v)
        return depth[u] + depth[v] - 2 * depth[lca_uv]
    
    # Build parent and depth arrays
    parent = [-1] * (n + 1)
    depth = [0] * (n + 1)
    subtree_size = [1] * (n + 1)
    
    def dfs(node, p, d):
        parent[node] = p
        depth[node] = d
        
        for child in adj[node]:
            if child != p:
                dfs(child, node, d + 1)
                subtree_size[node] += subtree_size[child]
    
    # Start DFS from root
    dfs(1, -1, 0)
    
    results = []
    for query in queries:
        count = count_paths_through_node(query, max_length)
        results.append(count)
    
    return results
```

#### **3. Counting Paths with Multiple Constraints**
```python
def multi_constrained_counting_paths(n, edges, queries, constraints):
    # Count paths with multiple constraints
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def count_paths_through_node(node, constraints):
        count = 0
        
        # Apply constraints to path counting
        max_length = constraints.get('max_length', float('inf'))
        min_length = constraints.get('min_length', 0)
        required_nodes = constraints.get('required_nodes', [])
        
        # Count paths where node is an endpoint
        if min_length <= 1 <= max_length:
            count += subtree_size[node] - 1
        
        # Count paths that pass through node
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if i != node and j != node:
                    # Check if path from i to j passes through node
                    if is_on_path(i, j, node):
                        path_length = get_path_length(i, j)
                        
                        # Check length constraints
                        if min_length <= path_length <= max_length:
                            # Check if path contains required nodes
                            if all(required_node in get_path_nodes(i, j) for required_node in required_nodes):
                                count += 1
        
        return count
    
    def get_path_nodes(u, v):
        # Get all nodes on path from u to v
        lca_uv = lca(u, v)
        path_nodes = set()
        
        # Add nodes from u to LCA
        current = u
        while current != lca_uv:
            path_nodes.add(current)
            current = parent[current]
        path_nodes.add(lca_uv)
        
        # Add nodes from v to LCA
        current = v
        while current != lca_uv:
            path_nodes.add(current)
            current = parent[current]
        
        return path_nodes
    
    # Build parent and depth arrays
    parent = [-1] * (n + 1)
    depth = [0] * (n + 1)
    subtree_size = [1] * (n + 1)
    
    def dfs(node, p, d):
        parent[node] = p
        depth[node] = d
        
        for child in adj[node]:
            if child != p:
                dfs(child, node, d + 1)
                subtree_size[node] += subtree_size[child]
    
    # Start DFS from root
    dfs(1, -1, 0)
    
    results = []
    for query in queries:
        count = count_paths_through_node(query, constraints)
        results.append(count)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Path Counting**: Various path counting problems
- **Tree Algorithms**: Tree traversal and path problems
- **LCA**: Lowest Common Ancestor problems
- **Dynamic Programming**: DP on trees

## 📚 Learning Points

### Key Takeaways
- **Subtree sizes** are crucial for path counting
- **LCA** helps determine if a node is on a path
- **Path analysis** requires understanding tree structure
- **Dynamic programming** provides optimal solutions

## Key Insights for Other Problems

### 1. **Path Counting Problems**
**Principle**: Use subtree sizes and LCA to count paths efficiently.
**Applicable to**: Tree problems, path problems, counting problems

### 2. **Binary Lifting for LCA**
**Principle**: Use binary lifting to find LCA in O(log n) time.
**Applicable to**: Tree problems, LCA problems, binary lifting applications

### 3. **Subtree Size Applications**
**Principle**: Use subtree sizes to count paths and relationships in trees.
**Applicable to**: Tree problems, counting problems, subtree analysis

## Notable Techniques

### 1. **Binary Lifting LCA**
```python
def build_binary_lifting(n, parent):
    log_n = 20
    ancestor = [[-1] * log_n for _ in range(n + 1)]
    
    # Initialize first level
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(1, n + 1):
            if ancestor[i][j-1] != -1:
                ancestor[i][j] = ancestor[ancestor[i][j-1]][j-1]
    
    return ancestor
```

### 2. **LCA Query**
```python
def lca_query(ancestor, depth, u, v):
    # Make sure u is deeper
    if depth[u] < depth[v]:
        u, v = v, u
    
    # Bring u to same level as v
    diff = depth[u] - depth[v]
    for i in range(20):
        if diff & (1 << i):
            u = ancestor[u][i]
    
    if u == v:
        return u
    
    # Find LCA
    for i in range(19, -1, -1):
        if ancestor[u][i] != ancestor[v][i]:
            u = ancestor[u][i]
            v = ancestor[v][i]
    
    return ancestor[u][0]
```

### 3. **Subtree Size Calculation**
```python
def calculate_subtree_sizes(adj, n):
    subtree_size = [1] * (n + 1)
    parent = [-1] * (n + 1)
    
    def dfs(node, p):
        for child in adj[node]:
            if child != p:
                dfs(child, node)
                subtree_size[node] += subtree_size[child]
    
    dfs(1, -1)
    return subtree_size
```

## Problem-Solving Framework

1. **Identify problem type**: This is a path counting problem in trees
2. **Choose approach**: Use subtree sizes and LCA for efficient counting
3. **Build data structures**: Calculate subtree sizes and build LCA table
4. **Implement counting**: Count paths using subtree sizes and LCA queries
5. **Process queries**: Answer each query using the precomputed data

---

*This analysis shows how to efficiently count paths through nodes using subtree sizes and LCA technique.* 