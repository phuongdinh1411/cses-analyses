---
layout: simple
title: "Distance Queries - Tree Distance Between Two Nodes"
permalink: /problem_soulutions/tree_algorithms/distance_queries_analysis
---

# Distance Queries - Tree Distance Between Two Nodes

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand tree distance query problems and distance calculation algorithms
- [ ] **Objective 2**: Apply Lowest Common Ancestor (LCA) technique to efficiently calculate tree distances
- [ ] **Objective 3**: Implement efficient distance query algorithms with O(log n) query time complexity
- [ ] **Objective 4**: Optimize distance queries using LCA, binary lifting, and tree distance analysis
- [ ] **Objective 5**: Handle edge cases in distance queries (same node, adjacent nodes, root node, large trees)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Lowest Common Ancestor (LCA), binary lifting, tree traversal, distance calculation, tree algorithms
- **Data Structures**: Trees, LCA tables, binary lifting tables, distance tracking, tree representation
- **Mathematical Concepts**: Tree theory, LCA mathematics, distance mathematics, binary lifting theory
- **Programming Skills**: LCA implementation, binary lifting implementation, tree traversal, algorithm implementation
- **Related Problems**: Path Queries (path operations), Company Queries (ancestor queries), Tree algorithms

## 📋 Problem Description

Given a tree with n nodes, answer q queries about the distance between two nodes.

This is a tree distance query problem that requires finding the distance between any two nodes in a tree. The solution involves using Lowest Common Ancestor (LCA) to efficiently calculate distances.

**Input**: 
- First line: Two integers n and q (number of nodes and queries)
- Next n-1 lines: Two integers a and b (edge between nodes a and b)
- Next q lines: Two integers a and b (find distance between nodes a and b)

**Output**: 
- For each query, print the distance between the two nodes

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n

**Example**:
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

**Explanation**: 
- Query 1: Distance between nodes 2 and 4 = 3 (path: 2-1-3-4)
- Query 2: Distance between nodes 1 and 5 = 2 (path: 1-3-5)
- Query 3: Distance between nodes 2 and 5 = 3 (path: 2-1-3-5)

## 🎯 Visual Example

### Input
```
n = 5, q = 3
Edges: [(1,2), (1,3), (3,4), (3,5)]
Queries: [(2,4), (1,5), (2,5)]
```

### Tree Structure
```
Node 1
├── Node 2
└── Node 3
    ├── Node 4
    └── Node 5

Tree representation:
    1
   / \
  2   3
     / \
    4   5
```

### Distance Query Processing
```
Query 1: Distance between nodes 2 and 4
- Path: 2 → 1 → 3 → 4
- Distance: 3
- Result: 3

Query 2: Distance between nodes 1 and 5
- Path: 1 → 3 → 5
- Distance: 2
- Result: 2

Query 3: Distance between nodes 2 and 5
- Path: 2 → 1 → 3 → 5
- Distance: 3
- Result: 3
```

### LCA-based Distance Calculation
```
Distance formula: dist(a,b) = depth[a] + depth[b] - 2*depth[LCA(a,b)]

Query 1: dist(2,4)
- depth[2] = 1, depth[4] = 2
- LCA(2,4) = 1, depth[1] = 0
- dist(2,4) = 1 + 2 - 2*0 = 3

Query 2: dist(1,5)
- depth[1] = 0, depth[5] = 2
- LCA(1,5) = 1, depth[1] = 0
- dist(1,5) = 0 + 2 - 2*0 = 2

Query 3: dist(2,5)
- depth[2] = 1, depth[5] = 2
- LCA(2,5) = 1, depth[1] = 0
- dist(2,5) = 1 + 2 - 2*0 = 3
```

### Key Insight
Tree distance calculation works by:
1. Using LCA to find the lowest common ancestor
2. Calculating distance using depth information
3. Formula: dist(a,b) = depth[a] + depth[b] - 2*depth[LCA(a,b)]
4. Time complexity: O(log n) per query after O(n log n) preprocessing
5. Space complexity: O(n log n) for binary lifting table

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find distance between any two nodes in a tree efficiently
- **Key Insight**: Use LCA (Lowest Common Ancestor) to calculate distances
- **Challenge**: Handle multiple queries efficiently without O(q × n) complexity

### Step 2: Initial Approach
**BFS for each query (inefficient but correct):**

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

### Step 3: Optimization/Alternative
**Optimized LCA with better setup:**

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

### Step 4: Complete Solution

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

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple tree (should return correct distances)
- **Test 2**: Linear tree (should return correct distances)
- **Test 3**: Star tree (should return correct distances)
- **Test 4**: Complex tree (should find all distances)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| BFS for Each Query | O(q * n) | O(n) | Simple but slow |
| LCA-based | O(n * log(n) + q * log(n)) | O(n * log(n)) | Use LCA formula |
| Optimized LCA | O(n * log(n) + q * log(n)) | O(n * log(n)) | Better implementation |
| Euler Tour | O(n + q * log(n)) | O(n * log(n)) | RMQ-based approach |

## 🎯 Key Insights

### Important Concepts and Patterns
- **LCA (Lowest Common Ancestor)**: Find common ancestors for distance calculation
- **Distance Formula**: distance(a,b) = depth(a) + depth(b) - 2*depth(lca(a,b))
- **Binary Lifting**: Efficient LCA computation using binary lifting
- **Tree Traversal**: Use DFS to calculate depths and build ancestor tables

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Distance Queries with Edge Weights**
```python
def weighted_distance_queries(n, q, edges, weights, queries):
    # Handle distance queries with edge weights
    
    # Build adjacency list with weights
    tree = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        tree[a].append((b, weights[i]))
        tree[b].append((a, weights[i]))
    
    # Binary lifting for LCA with weighted distances
    log_n = 20
    ancestor = [[0] * log_n for _ in range(n + 1)]
    depth = [0] * (n + 1)
    distance_from_root = [0] * (n + 1)
    
    def dfs(node, parent, current_depth, current_distance):
        depth[node] = current_depth
        distance_from_root[node] = current_distance
        ancestor[node][0] = parent
        
        for child, weight in tree[node]:
            if child != parent:
                dfs(child, node, current_depth + 1, current_distance + weight)
    
    dfs(1, 0, 0, 0)
    
    # Fill ancestor table
    for level in range(1, log_n):
        for node in range(1, n + 1):
            if ancestor[node][level - 1] != 0:
                ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
    
    def find_lca(a, b):
        # Bring both nodes to same depth
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        diff = depth[a] - depth[b]
        for level in range(log_n):
            if diff & (1 << level):
                a = ancestor[a][level]
        
        if a == b:
            return a
        
        # Find LCA by binary search
        for level in range(log_n - 1, -1, -1):
            if ancestor[a][level] != ancestor[b][level]:
                a = ancestor[a][level]
                b = ancestor[b][level]
        
        return ancestor[a][0]
    
    def calculate_weighted_distance(a, b):
        lca_node = find_lca(a, b)
        return distance_from_root[a] + distance_from_root[b] - 2 * distance_from_root[lca_node]
    
    # Process queries
    result = []
    for a, b in queries:
        result.append(calculate_weighted_distance(a, b))
    
    return result
```

#### **2. Distance Queries with Updates**
```python
def dynamic_distance_queries(n, q, edges, operations):
    # Handle distance queries with dynamic tree updates
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    def rebuild_lca():
        # Rebuild LCA tables after updates
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
    
    def find_lca(ancestor, depth, a, b):
        # Bring both nodes to same depth
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        diff = depth[a] - depth[b]
        for level in range(20):
            if diff & (1 << level):
                a = ancestor[a][level]
        
        if a == b:
            return a
        
        # Find LCA by binary search
        for level in range(19, -1, -1):
            if ancestor[a][level] != ancestor[b][level]:
                a = ancestor[a][level]
                b = ancestor[b][level]
        
        return ancestor[a][0]
    
    def calculate_distance(ancestor, depth, a, b):
        lca_node = find_lca(ancestor, depth, a, b)
        return depth[a] + depth[b] - 2 * depth[lca_node]
    
    # Process operations
    result = []
    for operation in operations:
        if operation[0] == 'add':
            # Add edge
            a, b = operation[1], operation[2]
            tree[a].append(b)
            tree[b].append(a)
        elif operation[0] == 'remove':
            # Remove edge
            a, b = operation[1], operation[2]
            tree[a].remove(b)
            tree[b].remove(a)
        elif operation[0] == 'query':
            # Distance query
            a, b = operation[1], operation[2]
            ancestor, depth = rebuild_lca()
            distance = calculate_distance(ancestor, depth, a, b)
            result.append(distance)
    
    return result
```

#### **3. Distance Queries with Path Information**
```python
def distance_queries_with_path(n, q, edges, queries):
    # Handle distance queries with path reconstruction
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Binary lifting for LCA
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
    
    def find_lca(a, b):
        # Bring both nodes to same depth
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        diff = depth[a] - depth[b]
        for level in range(log_n):
            if diff & (1 << level):
                a = ancestor[a][level]
        
        if a == b:
            return a
        
        # Find LCA by binary search
        for level in range(log_n - 1, -1, -1):
            if ancestor[a][level] != ancestor[b][level]:
                a = ancestor[a][level]
                b = ancestor[b][level]
        
        return ancestor[a][0]
    
    def get_path(a, b):
        # Get the path from a to b
        lca_node = find_lca(a, b)
        path = []
        
        # Add nodes from a to LCA
        current = a
        while current != lca_node:
            path.append(current)
            current = ancestor[current][0]
        path.append(lca_node)
        
        # Add nodes from b to LCA (in reverse)
        current = b
        temp_path = []
        while current != lca_node:
            temp_path.append(current)
            current = ancestor[current][0]
        
        # Combine paths
        path.extend(reversed(temp_path))
        return path
    
    def calculate_distance_with_path(a, b):
        lca_node = find_lca(a, b)
        distance = depth[a] + depth[b] - 2 * depth[lca_node]
        path = get_path(a, b)
        return distance, path
    
    # Process queries
    result = []
    for a, b in queries:
        distance, path = calculate_distance_with_path(a, b)
        result.append((distance, path))
    
    return result
```

## 🔗 Related Problems

### Links to Similar Problems
- **Distance Queries**: Various tree distance query problems
- **LCA**: Lowest Common Ancestor problems
- **Tree Algorithms**: Tree traversal and distance problems
- **Binary Lifting**: Binary lifting technique problems

## 📚 Learning Points

### Key Takeaways
- **LCA formula** efficiently calculates tree distances
- **Binary lifting** provides fast LCA computation
- **Distance formula** works for both weighted and unweighted trees
- **Tree structure** enables efficient distance calculations

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