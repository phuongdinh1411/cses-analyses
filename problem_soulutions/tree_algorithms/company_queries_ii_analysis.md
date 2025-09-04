---
layout: simple
title: "Company Queries II - Lowest Common Ancestor of Two Employees"
permalink: /problem_soulutions/tree_algorithms/company_queries_ii_analysis
---

# Company Queries II - Lowest Common Ancestor of Two Employees

## 📋 Problem Description

A company has n employees, numbered 1,2,…,n. Each employee except 1 has exactly one superior. Given q queries, for each query find the lowest common ancestor (LCA) of two employees.

This is a tree LCA query problem that requires finding the lowest common ancestor of any two nodes in a tree. The solution involves using binary lifting technique to efficiently answer LCA queries.

**Input**: 
- First line: Two integers n and q (number of employees and queries)
- Second line: n-1 integers p₂, p₃, ..., pₙ (each pᵢ is the superior of employee i)
- Next q lines: Two integers a and b (find the LCA of employees a and b)

**Output**: 
- For each query, print the LCA of the two employees

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ pᵢ < i
- 1 ≤ a, b ≤ n

**Example**:
```
Input:
5 3
1 1 2 2
2 3
2 4
4 5

Output:
1
2
2
```

**Explanation**: 
- Query 1: LCA of employees 2 and 3 = 1
- Query 2: LCA of employees 2 and 4 = 2
- Query 3: LCA of employees 4 and 5 = 2

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find the lowest common ancestor of any two nodes in a tree efficiently
- **Key Insight**: Use binary lifting technique to answer LCA queries in O(log n)
- **Challenge**: Handle multiple queries efficiently without O(q × h) complexity

### Step 2: Initial Approach
**Naive LCA approach (inefficient but correct):**

```python
def company_queries_naive_lca(n, q, superiors, queries):
    # Build parent array (1-indexed)
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    def get_depth(node):
        depth = 0
        current = node
        while current != 0:
            current = parent[current]
            depth += 1
        return depth
    
    def find_lca(a, b):
        # Get depths of both nodes
        depth_a = get_depth(a)
        depth_b = get_depth(b)
        
        # Bring both nodes to same depth
        while depth_a > depth_b:
            a = parent[a]
            depth_a -= 1
        while depth_b > depth_a:
            b = parent[b]
            depth_b -= 1
        
        # Now climb up together until we find LCA
        while a != b:
            a = parent[a]
            b = parent[b]
        
        return a
    
    # Process queries
    result = []
    for a, b in queries:
        result.append(find_lca(a, b))
    
    return result
```

**Why this is inefficient**: For deep trees, this approach becomes slow.

### Step 3: Optimization/Alternative
**Binary lifting for LCA:**

```python
def company_queries_binary_lifting_lca(n, q, superiors, queries):
    # Build parent array (1-indexed)
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Binary lifting table
    log_n = 20  # Sufficient for n up to 10^6
    ancestor = [[0] * log_n for _ in range(n + 1)]
    depth = [0] * (n + 1)
    
    # Calculate depths and initialize ancestor table
    def calculate_depths():
        for i in range(1, n + 1):
            current = i
            d = 0
            while current != 0:
                current = parent[current]
                d += 1
            depth[i] = d
    
    calculate_depths()
    
    # Initialize ancestor table
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
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
        
        # Now find LCA by binary search
        for level in range(log_n - 1, -1, -1):
            if ancestor[a][level] != ancestor[b][level]:
                a = ancestor[a][level]
                b = ancestor[b][level]
        
        return ancestor[a][0]
    
    # Process queries
    result = []
    for a, b in queries:
        result.append(find_lca(a, b))
    
    return result
```

**Why this improvement works**: Binary lifting allows efficient LCA queries in logarithmic time.

### Improvement 2: Optimized Binary Lifting - O(n * log(n) + q * log(n))
**Description**: Optimize binary lifting with better depth calculation and LCA finding.

```python
def company_queries_optimized_lca(n, q, superiors, queries):
    # Build parent array (1-indexed)
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
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
    def calculate_depths_dfs(node, current_depth):
        depth[node] = current_depth
        for child in range(2, n + 1):
            if parent[child] == node:
                calculate_depths_dfs(child, current_depth + 1)
    
    calculate_depths_dfs(1, 0)
    
    # Initialize ancestor table
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
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
    
    # Process queries
    result = []
    for a, b in queries:
        result.append(find_lca(a, b))
    
    return result
```

**Why this improvement works**: Optimized implementation with better depth calculation using DFS.

### Alternative: Euler Tour with RMQ - O(n + q * log(n))
**Description**: Use Euler Tour technique with Range Minimum Query for LCA.

```python
def company_queries_euler_tour(n, q, superiors, queries):
    # Build parent array
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Euler Tour arrays
    euler_tour = []
    first_occurrence = [0] * (n + 1)
    depth = [0] * (n + 1)
    
    def dfs(node, current_depth):
        first_occurrence[node] = len(euler_tour)
        euler_tour.append(node)
        depth[node] = current_depth
        
        for child in range(2, n + 1):
            if parent[child] == node:
                dfs(child, current_depth + 1)
                euler_tour.append(node)
    
    dfs(1, 0)
    
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
    
    # Process queries
    result = []
    for a, b in queries:
        result.append(find_lca(a, b))
    
    return result
```

**Why this works**: Euler Tour technique reduces LCA to RMQ problem.

### Step 4: Complete Solution

```python
n, q = map(int, input().split())
superiors = list(map(int, input().split()))
queries = [tuple(map(int, input().split())) for _ in range(q)]

# Build parent array (1-indexed)
parent = [0] * (n + 1)
for i in range(2, n + 1):
    parent[i] = superiors[i - 2]

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
def calculate_depths_dfs(node, current_depth):
    depth[node] = current_depth
    for child in range(2, n + 1):
        if parent[child] == node:
            calculate_depths_dfs(child, current_depth + 1)

calculate_depths_dfs(1, 0)

# Initialize ancestor table
for i in range(1, n + 1):
    ancestor[i][0] = parent[i]

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

# Process queries
for a, b in queries:
    print(find_lca(a, b))
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple tree (should return correct LCAs)
- **Test 2**: Linear tree (should return correct LCAs)
- **Test 3**: Star tree (should return correct LCAs)
- **Test 4**: Complex tree (should find all LCAs)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive LCA | O(q * h) | O(n) | Simple but slow |
| Binary Lifting | O(n * log(n) + q * log(n)) | O(n * log(n)) | Precompute ancestors |
| Optimized Binary Lifting | O(n * log(n) + q * log(n)) | O(n * log(n)) | Better implementation |
| Euler Tour | O(n + q * log(n)) | O(n * log(n)) | RMQ-based approach |

## 🎯 Key Insights

### Important Concepts and Patterns
- **LCA (Lowest Common Ancestor)**: Find common ancestors of two nodes efficiently
- **Binary Lifting**: Precompute ancestors in powers of 2 for efficient queries
- **Depth Calculation**: Use depths to bring nodes to same level before finding LCA
- **Tree Traversal**: Use parent pointers to traverse up the tree

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Company Queries with Distance Calculation**
```python
def lca_with_distance(n, superiors, queries):
    # Handle LCA queries with distance calculation
    
    # Build parent array
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Binary lifting table
    log_n = 20
    ancestor = [[0] * log_n for _ in range(n + 1)]
    depth = [0] * (n + 1)
    
    # Calculate depths
    def calculate_depths():
        for i in range(1, n + 1):
            current = i
            d = 0
            while current != 0:
                current = parent[current]
                d += 1
            depth[i] = d
    
    calculate_depths()
    
    # Initialize ancestor table
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
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
    
    def find_lca_with_distance(a, b):
        # Calculate distance between a and b
        original_a, original_b = a, b
        
        # Bring both nodes to same depth
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        diff = depth[a] - depth[b]
        a = get_kth_ancestor(a, diff)
        
        if a == b:
            lca_node = a
        else:
            # Find LCA by binary search
            for level in range(log_n - 1, -1, -1):
                if ancestor[a][level] != ancestor[b][level]:
                    a = ancestor[a][level]
                    b = ancestor[b][level]
            lca_node = ancestor[a][0]
        
        # Calculate distance
        distance = depth[original_a] + depth[original_b] - 2 * depth[lca_node]
        
        return lca_node, distance
    
    # Process queries
    results = []
    for a, b in queries:
        lca_node, distance = find_lca_with_distance(a, b)
        results.append((lca_node, distance))
    
    return results
```

#### **2. Company Queries with Path Information**
```python
def lca_with_path(n, superiors, queries):
    # Handle LCA queries with path reconstruction
    
    # Build parent array
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Binary lifting table
    log_n = 20
    ancestor = [[0] * log_n for _ in range(n + 1)]
    depth = [0] * (n + 1)
    
    # Calculate depths
    def calculate_depths():
        for i in range(1, n + 1):
            current = i
            d = 0
            while current != 0:
                current = parent[current]
                d += 1
            depth[i] = d
    
    calculate_depths()
    
    # Initialize ancestor table
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
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
    
    def find_lca_with_path(a, b):
        # Find LCA
        original_a, original_b = a, b
        
        # Bring both nodes to same depth
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        diff = depth[a] - depth[b]
        a = get_kth_ancestor(a, diff)
        
        if a == b:
            lca_node = a
        else:
            # Find LCA by binary search
            for level in range(log_n - 1, -1, -1):
                if ancestor[a][level] != ancestor[b][level]:
                    a = ancestor[a][level]
                    b = ancestor[b][level]
            lca_node = ancestor[a][0]
        
        # Reconstruct path from a to b
        path = []
        
        # Path from original_a to LCA
        current = original_a
        while current != lca_node:
            path.append(current)
            current = parent[current]
        path.append(lca_node)
        
        # Path from LCA to original_b (in reverse)
        temp_path = []
        current = original_b
        while current != lca_node:
            temp_path.append(current)
            current = parent[current]
        
        # Combine paths
        path.extend(reversed(temp_path))
        
        return lca_node, path
    
    # Process queries
    results = []
    for a, b in queries:
        lca_node, path = find_lca_with_path(a, b)
        results.append((lca_node, path))
    
    return results
```

#### **3. Company Queries with Multiple LCAs**
```python
def multiple_lca_queries(n, superiors, queries):
    # Handle multiple LCA queries efficiently
    
    # Build parent array
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Binary lifting table
    log_n = 20
    ancestor = [[0] * log_n for _ in range(n + 1)]
    depth = [0] * (n + 1)
    
    # Calculate depths
    def calculate_depths():
        for i in range(1, n + 1):
            current = i
            d = 0
            while current != 0:
                current = parent[current]
                d += 1
            depth[i] = d
    
    calculate_depths()
    
    # Initialize ancestor table
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
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
    
    def find_multiple_lcas(nodes):
        # Find LCA of multiple nodes
        if len(nodes) == 0:
            return -1
        if len(nodes) == 1:
            return nodes[0]
        
        result = nodes[0]
        for i in range(1, len(nodes)):
            result = find_lca(result, nodes[i])
        
        return result
    
    # Process queries
    results = []
    for query in queries:
        if query[0] == 'lca':
            # Single LCA query
            a, b = query[1], query[2]
            result = find_lca(a, b)
            results.append(result)
        elif query[0] == 'multiple_lca':
            # Multiple LCA query
            nodes = query[1]
            result = find_multiple_lcas(nodes)
            results.append(result)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Company Queries**: Various company hierarchy problems
- **LCA**: Lowest Common Ancestor problems
- **Binary Lifting**: Binary lifting technique problems
- **Tree Algorithms**: Tree traversal and query problems

## 📚 Learning Points

### Key Takeaways
- **Binary lifting** enables efficient LCA queries
- **Depth calculation** is crucial for LCA algorithms
- **LCA formula** works for distance calculations
- **Tree structure** enables efficient ancestor queries

## Key Insights for Other Problems

### 1. **LCA Problems**
**Principle**: Use binary lifting or Euler Tour to find lowest common ancestors efficiently.
**Applicable to**:
- LCA problems
- Tree algorithms
- Graph algorithms
- Algorithm design

**Example Problems**:
- LCA problems
- Tree algorithms
- Graph algorithms
- Algorithm design

### 2. **Binary Lifting for LCA**
**Principle**: Use binary lifting to bring nodes to same depth and then find LCA.
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

### 3. **Euler Tour Technique**
**Principle**: Use Euler Tour to reduce LCA to Range Minimum Query problem.
**Applicable to**:
- Tree algorithms
- Range queries
- Algorithm design
- Problem solving

**Example Problems**:
- Tree algorithms
- Range queries
- Algorithm design
- Problem solving

### 4. **Depth-based Algorithms**
**Principle**: Use node depths to optimize tree algorithms.
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

## Notable Techniques

### 1. **Binary Lifting LCA Pattern**
```python
def binary_lifting_lca_setup(parent, n):
    log_n = 20
    ancestor = [[0] * log_n for _ in range(n + 1)]
    depth = [0] * (n + 1)
    
    # Calculate depths
    def calculate_depths(node, current_depth):
        depth[node] = current_depth
        for child in range(2, n + 1):
            if parent[child] == node:
                calculate_depths(child, current_depth + 1)
    
    calculate_depths(1, 0)
    
    # Initialize ancestor table
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Fill ancestor table
    for level in range(1, log_n):
        for node in range(1, n + 1):
            if ancestor[node][level - 1] != 0:
                ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
    
    return ancestor, depth

def find_lca(ancestor, depth, a, b, log_n):
    # Bring both nodes to same depth
    if depth[a] < depth[b]:
        a, b = b, a
    
    # Bring a to same depth as b
    diff = depth[a] - depth[b]
    a = get_kth_ancestor(ancestor, a, diff)
    
    if a == b:
        return a
    
    # Find LCA by binary search
    for level in range(log_n - 1, -1, -1):
        if ancestor[a][level] != ancestor[b][level]:
            a = ancestor[a][level]
            b = ancestor[b][level]
    
    return ancestor[a][0]
```

### 2. **Euler Tour Pattern**
```python
def euler_tour_setup(parent, n):
    euler_tour = []
    first_occurrence = [0] * (n + 1)
    depth = [0] * (n + 1)
    
    def dfs(node, current_depth):
        first_occurrence[node] = len(euler_tour)
        euler_tour.append(node)
        depth[node] = current_depth
        
        for child in range(2, n + 1):
            if parent[child] == node:
                dfs(child, current_depth + 1)
                euler_tour.append(node)
    
    dfs(1, 0)
    return euler_tour, first_occurrence, depth
```

### 3. **RMQ-based LCA Pattern**
```python
def rmq_lca(euler_tour, first_occurrence, depth, a, b):
    left = first_occurrence[a]
    right = first_occurrence[b]
    
    if left > right:
        left, right = right, left
    
    # Find minimum depth in range [left, right]
    min_depth = float('inf')
    lca_node = 0
    
    for i in range(left, right + 1):
        if depth[euler_tour[i]] < min_depth:
            min_depth = depth[euler_tour[i]]
            lca_node = euler_tour[i]
    
    return lca_node
```

## Edge Cases to Remember

1. **Same node**: LCA of a node with itself is the node itself
2. **Parent-child**: LCA of parent and child is the parent
3. **Root node**: LCA involving root is always root
4. **Different depths**: Handle nodes at different depths properly
5. **Large trees**: Handle deep trees efficiently

## Problem-Solving Framework

1. **Identify LCA nature**: This is a lowest common ancestor problem
2. **Choose approach**: Use binary lifting for efficiency
3. **Calculate depths**: Use DFS to calculate node depths
4. **Build ancestor table**: Use dynamic programming
5. **Handle queries**: Use binary lifting for logarithmic time

---

*This analysis shows how to efficiently find lowest common ancestors in trees using binary lifting technique.* 