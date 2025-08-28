---
layout: simple
title: "Distance Queries"permalink: /problem_soulutions/tree_algorithms/distance_queries_analysis
---


# Distance Queries

## Problem Statement
Given a tree with n nodes, answer q queries about the distance between two nodes.

### Input
The first input line has two integers n and q: the number of nodes and queries.
Then, there are n−1 lines describing the edges. Each line has two integers a and b: there is an edge between nodes a and b.
Finally, there are q lines describing the queries. Each line has two integers a and b: find the distance between nodes a and b.

### Output
Print q integers: the answers to the queries.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
5 3
1 2
1 3
3 4
3 5
2 4
1 5
2 5

Output:
3
2
3
```

## Solution Progression

### Approach 1: BFS for Each Query - O(q * n)
**Description**: Use BFS from one node to find the distance to the other node for each query.

```python
from collections import deque

def distance_queries_bfs(n, q, edges, queries):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    def bfs_distance(start, end):
        # BFS to find distance from start to end
        distances = [-1] * (n + 1)
        queue = deque([start])
        distances[start] = 0
        
        while queue:
            node = queue.popleft()
            if node == end:
                return distances[node]
            
            for neighbor in tree[node]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        
        return -1
    
    # Process queries
    result = []
    for a, b in queries:
        result.append(bfs_distance(a, b))
    
    return result
```

**Why this is inefficient**: Multiple BFS queries become slow for large numbers of queries.

### Improvement 1: LCA-based Distance - O(n * log(n) + q * log(n))
**Description**: Use LCA to calculate distances efficiently using the formula: distance(a,b) = depth(a) + depth(b) - 2*depth(lca(a,b)).

```python
def distance_queries_lca(n, q, edges, queries):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Binary lifting for LCA
    log_n = 20
    ancestor = [[0] * log_n for _ in range(n + 1)]
    depth = [0] * (n + 1)
    
    # Calculate depths and build ancestor table
    def dfs(node, parent, current_depth):
        depth[node] = current_depth
        ancestor[node][0] = parent
        
        for child in tree[node]:
            if child != parent:
                dfs(child, node, current_depth + 1)
    
    dfs(1, 0, 0)
    
    # Fill ancestor table
    for level in range(1, log_n):
        for node in range(1, n + 1):
            if ancestor[node][level - 1] != 0:
                ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
    
    def get_kth_ancestor(node, k):
        current = node
        level = 0
        while k > 0 and current != 0:
            if k & (1 << level):
                current = ancestor[current][level]
                if current == 0:
                    return 0
            level += 1
        return current
    
    def find_lca(a, b):
        # Bring both nodes to same depth
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        diff = depth[a] - depth[b]
        a = get_kth_ancestor(a, diff)
        
        if a == b:
            return a
        
        # Find LCA by binary search
        for level in range(log_n - 1, -1, -1):
            if ancestor[a][level] != ancestor[b][level]:
                a = ancestor[a][level]
                b = ancestor[b][level]
        
        return ancestor[a][0]
    
    def calculate_distance(a, b):
        lca_node = find_lca(a, b)
        return depth[a] + depth[b] - 2 * depth[lca_node]
    
    # Process queries
    result = []
    for a, b in queries:
        result.append(calculate_distance(a, b))
    
    return result
```

**Why this improvement works**: LCA-based approach uses the formula distance(a,b) = depth(a) + depth(b) - 2*depth(lca(a,b)) for efficient distance calculation.

### Improvement 2: Optimized LCA with Better Setup - O(n * log(n) + q * log(n))
**Description**: Optimize the LCA setup with better depth calculation and ancestor table building.

```python
def distance_queries_optimized_lca(n, q, edges, queries):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Calculate log base 2 of n
    log_n = 0
    temp = n
    while temp > 0:
        log_n += 1
        temp >>= 1
    
    # Binary lifting table and depths
    ancestor = [[0] * log_n for _ in range(n + 1)]
    depth = [0] * (n + 1)
    
    # Calculate depths using DFS
    def calculate_depths_dfs(node, parent, current_depth):
        depth[node] = current_depth
        ancestor[node][0] = parent
        
        for child in tree[node]:
            if child != parent:
                calculate_depths_dfs(child, node, current_depth + 1)
    
    calculate_depths_dfs(1, 0, 0)
    
    # Fill ancestor table
    for level in range(1, log_n):
        for node in range(1, n + 1):
            if ancestor[node][level - 1] != 0:
                ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
    
    def get_kth_ancestor(node, k):
        if k == 0:
            return node
        
        current = node
        level = 0
        while k > 0 and current != 0:
            if k & (1 << level):
                current = ancestor[current][level]
                if current == 0:
                    return 0
            level += 1
        return current
    
    def find_lca(a, b):
        # Bring both nodes to same depth
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        diff = depth[a] - depth[b]
        a = get_kth_ancestor(a, diff)
        
        if a == b:
            return a
        
        # Find LCA by binary search
        for level in range(log_n - 1, -1, -1):
            if ancestor[a][level] != ancestor[b][level]:
                a = ancestor[a][level]
                b = ancestor[b][level]
        
        return ancestor[a][0]
    
    def calculate_distance(a, b):
        lca_node = find_lca(a, b)
        return depth[a] + depth[b] - 2 * depth[lca_node]
    
    # Process queries
    result = []
    for a, b in queries:
        result.append(calculate_distance(a, b))
    
    return result
```

**Why this improvement works**: Optimized implementation with better log calculation and depth computation.

### Alternative: Euler Tour with RMQ - O(n + q * log(n))
**Description**: Use Euler Tour technique with Range Minimum Query for LCA-based distance calculation.

```python
def distance_queries_euler_tour(n, q, edges, queries):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Euler Tour arrays
    euler_tour = []
    first_occurrence = [0] * (n + 1)
    depth = [0] * (n + 1)
    
    def dfs(node, parent, current_depth):
        first_occurrence[node] = len(euler_tour)
        euler_tour.append(node)
        depth[node] = current_depth
        
        for child in tree[node]:
            if child != parent:
                dfs(child, node, current_depth + 1)
                euler_tour.append(node)
    
    dfs(1, 0, 0)
    
    # Build sparse table for RMQ
    m = len(euler_tour)
    log_m = 0
    temp = m
    while temp > 0:
        log_m += 1
        temp >>= 1
    
    sparse_table = [[0] * log_m for _ in range(m)]
    
    # Initialize sparse table
    for i in range(m):
        sparse_table[i][0] = i
    
    # Fill sparse table
    for level in range(1, log_m):
        for i in range(m - (1 << level) + 1):
            left = sparse_table[i][level - 1]
            right = sparse_table[i + (1 << (level - 1))][level - 1]
            if depth[euler_tour[left]] < depth[euler_tour[right]]:
                sparse_table[i][level] = left
            else:
                sparse_table[i][level] = right
    
    def rmq(left, right):
        length = right - left + 1
        level = 0
        while (1 << (level + 1)) <= length:
            level += 1
        
        left_idx = sparse_table[left][level]
        right_idx = sparse_table[right - (1 << level) + 1][level]
        
        if depth[euler_tour[left_idx]] < depth[euler_tour[right_idx]]:
            return euler_tour[left_idx]
        else:
            return euler_tour[right_idx]
    
    def find_lca(a, b):
        left = first_occurrence[a]
        right = first_occurrence[b]
        
        if left > right:
            left, right = right, left
        
        return rmq(left, right)
    
    def calculate_distance(a, b):
        lca_node = find_lca(a, b)
        return depth[a] + depth[b] - 2 * depth[lca_node]
    
    # Process queries
    result = []
    for a, b in queries:
        result.append(calculate_distance(a, b))
    
    return result
```

**Why this works**: Euler Tour technique reduces LCA to RMQ problem for distance calculation.

## Final Optimal Solution

```python
n, q = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(n - 1)]
queries = [tuple(map(int, input().split())) for _ in range(q)]

# Build adjacency list
tree = [[] for _ in range(n + 1)]
for a, b in edges:
    tree[a].append(b)
    tree[b].append(a)

# Calculate log base 2 of n
log_n = 0
temp = n
while temp > 0:
    log_n += 1
    temp >>= 1

# Binary lifting table and depths
ancestor = [[0] * log_n for _ in range(n + 1)]
depth = [0] * (n + 1)

# Calculate depths using DFS
def calculate_depths_dfs(node, parent, current_depth):
    depth[node] = current_depth
    ancestor[node][0] = parent
    
    for child in tree[node]:
        if child != parent:
            calculate_depths_dfs(child, node, current_depth + 1)

calculate_depths_dfs(1, 0, 0)

# Fill ancestor table
for level in range(1, log_n):
    for node in range(1, n + 1):
        if ancestor[node][level - 1] != 0:
            ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]

def get_kth_ancestor(node, k):
    if k == 0:
        return node
    
    current = node
    level = 0
    while k > 0 and current != 0:
        if k & (1 << level):
            current = ancestor[current][level]
            if current == 0:
                return 0
        level += 1
    return current

def find_lca(a, b):
    # Bring both nodes to same depth
    if depth[a] < depth[b]:
        a, b = b, a
    
    # Bring a to same depth as b
    diff = depth[a] - depth[b]
    a = get_kth_ancestor(a, diff)
    
    if a == b:
        return a
    
    # Find LCA by binary search
    for level in range(log_n - 1, -1, -1):
        if ancestor[a][level] != ancestor[b][level]:
            a = ancestor[a][level]
            b = ancestor[b][level]
    
    return ancestor[a][0]

def calculate_distance(a, b):
    lca_node = find_lca(a, b)
    return depth[a] + depth[b] - 2 * depth[lca_node]

# Process queries
for a, b in queries:
    print(calculate_distance(a, b))
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| BFS for Each Query | O(q * n) | O(n) | Simple but slow |
| LCA-based | O(n * log(n) + q * log(n)) | O(n * log(n)) | Use LCA formula |
| Optimized LCA | O(n * log(n) + q * log(n)) | O(n * log(n)) | Better implementation |
| Euler Tour | O(n + q * log(n)) | O(n * log(n)) | RMQ-based approach |

## Key Insights for Other Problems

### 1. **Distance Query Problems**
**Principle**: Use LCA to calculate distances efficiently using the formula distance(a,b) = depth(a) + depth(b) - 2*depth(lca(a,b)).
**Applicable to**:
- Distance query problems
- Tree algorithms
- Graph algorithms
- Algorithm design

**Example Problems**:
- Distance query problems
- Tree algorithms
- Graph algorithms
- Algorithm design

### 2. **LCA-based Distance Formula**
**Principle**: The distance between two nodes in a tree is the sum of their depths minus twice the depth of their LCA.
**Applicable to**:
- Tree algorithms
- Graph algorithms
- Algorithm design
- Problem solving

**Example Problems**:
- Tree algorithms
- Graph algorithms
- Algorithm design
- Problem solving

### 3. **Binary Lifting for Distance**
**Principle**: Use binary lifting to find LCA efficiently for distance calculations.
**Applicable to**:
- Tree algorithms
- Graph algorithms
- Algorithm design
- Problem solving

**Example Problems**:
- Tree algorithms
- Graph algorithms
- Algorithm design
- Problem solving

### 4. **Query Optimization**
**Principle**: Preprocess tree information to answer multiple queries efficiently.
**Applicable to**:
- Query optimization
- Algorithm design
- Problem solving
- System design

**Example Problems**:
- Query optimization
- Algorithm design
- Problem solving
- System design

## Notable Techniques

### 1. **LCA-based Distance Pattern**
```python
def lca_based_distance_setup(tree, n):
    log_n = 20
    ancestor = [[0] * log_n for _ in range(n + 1)]
    depth = [0] * (n + 1)
    
    def dfs(node, parent, current_depth):
        depth[node] = current_depth
        ancestor[node][0] = parent
        
        for child in tree[node]:
            if child != parent:
                dfs(child, node, current_depth + 1)
    
    dfs(1, 0, 0)
    
    # Fill ancestor table
    for level in range(1, log_n):
        for node in range(1, n + 1):
            if ancestor[node][level - 1] != 0:
                ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
    
    return ancestor, depth

def calculate_distance(ancestor, depth, a, b, log_n):
    lca_node = find_lca(ancestor, depth, a, b, log_n)
    return depth[a] + depth[b] - 2 * depth[lca_node]
```

### 2. **Distance Formula Pattern**
```python
def distance_formula(depth_a, depth_b, depth_lca):
    return depth_a + depth_b - 2 * depth_lca
```

### 3. **Query Processing Pattern**
```python
def process_distance_queries(ancestor, depth, queries, log_n):
    results = []
    for a, b in queries:
        distance = calculate_distance(ancestor, depth, a, b, log_n)
        results.append(distance)
    return results
```

## Edge Cases to Remember

1. **Same node**: Distance between a node and itself is 0
2. **Adjacent nodes**: Distance between adjacent nodes is 1
3. **Root node**: Distance involving root node
4. **Deep trees**: Handle deep trees efficiently
5. **Multiple queries**: Preprocess for efficiency

## Problem-Solving Framework

1. **Identify distance nature**: This is a distance query problem
2. **Use LCA formula**: distance(a,b) = depth(a) + depth(b) - 2*depth(lca(a,b))
3. **Choose approach**: Use binary lifting for LCA
4. **Preprocess data**: Build ancestor table and calculate depths
5. **Handle queries**: Use LCA to calculate distances efficiently

---

*This analysis shows how to efficiently calculate distances in trees using LCA-based formulas.*