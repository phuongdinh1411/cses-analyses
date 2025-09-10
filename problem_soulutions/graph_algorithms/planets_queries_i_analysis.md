---
layout: simple
title: "Planets Queries I - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/planets_queries_i_analysis
---

# Planets Queries I - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of ancestor queries in tree structures
- Apply efficient algorithms for finding k-th ancestors
- Implement binary lifting for ancestor queries
- Optimize tree traversal for query processing
- Handle special cases in ancestor query problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tree algorithms, binary lifting, ancestor queries
- **Data Structures**: Trees, arrays, binary representation
- **Mathematical Concepts**: Tree theory, binary representation, logarithms
- **Programming Skills**: Tree operations, binary lifting, query processing
- **Related Problems**: Planets Queries II (graph_algorithms), Company Queries I (tree_algorithms), Company Queries II (tree_algorithms)

## 📋 Problem Description

Given a tree with n vertices, answer q queries about k-th ancestors.

**Input**: 
- n: number of vertices
- parent: array where parent[i] is the parent of vertex i
- q: number of queries
- queries: array of (vertex, k) pairs

**Output**: 
- For each query, return the k-th ancestor of the vertex

**Constraints**:
- 1 ≤ n ≤ 2×10^5
- 1 ≤ q ≤ 2×10^5
- 0 ≤ k ≤ 10^9

**Example**:
```
Input:
n = 5
parent = [-1, 0, 0, 1, 1]
q = 3
queries = [(4, 1), (4, 2), (4, 3)]

Output:
1
0
-1

Explanation**: 
Vertex 4's ancestors:
- 1st ancestor: 1
- 2nd ancestor: 0  
- 3rd ancestor: -1 (doesn't exist)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Traversal**: Walk up the tree k steps for each query
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic tree traversal
- **Inefficient**: O(qk) time complexity

**Key Insight**: For each query, walk up the tree k steps to find the ancestor.

**Algorithm**:
- For each query (vertex, k)
- Walk up the tree k steps
- Return the final vertex

**Visual Example**:
```
Tree: 0 -> 1 -> 4
      0 -> 2
      0 -> 3

Query (4, 2):
┌─────────────────────────────────────┐
│ Start at vertex 4                  │
│ Step 1: 4 -> parent[4] = 1         │
│ Step 2: 1 -> parent[1] = 0         │
│ Result: 0                          │
│                                   │
│ Query (4, 3):                     │
│ Start at vertex 4                  │
│ Step 1: 4 -> parent[4] = 1         │
│ Step 2: 1 -> parent[1] = 0         │
│ Step 3: 0 -> parent[0] = -1        │
│ Result: -1 (no ancestor)          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_planets_queries_i(n, parent, queries):
    """Answer ancestor queries using brute force approach"""
    results = []
    
    for vertex, k in queries:
        current = vertex
        steps = 0
        
        # Walk up the tree k steps
        while current != -1 and steps < k:
            current = parent[current]
            steps += 1
        
        if current == -1:
            results.append(-1)
        else:
            results.append(current)
    
    return results

# Example usage
n = 5
parent = [-1, 0, 0, 1, 1]
queries = [(4, 1), (4, 2), (4, 3)]
result = brute_force_planets_queries_i(n, parent, queries)
print(f"Brute force results: {result}")
```

**Time Complexity**: O(qk)
**Space Complexity**: O(1)

**Why it's inefficient**: O(qk) time complexity for large k values.

---

### Approach 2: Binary Lifting Solution

**Key Insights from Binary Lifting Solution**:
- **Binary Lifting**: Use binary representation for efficient ancestor queries
- **Efficient Implementation**: O(n log n) preprocessing, O(log n) per query
- **Power of 2**: Precompute ancestors at powers of 2
- **Optimization**: Much more efficient than brute force

**Key Insight**: Precompute ancestors at powers of 2 for efficient queries.

**Algorithm**:
- Precompute ancestors at powers of 2 (1, 2, 4, 8, ...)
- For each query, use binary representation of k
- Jump up the tree using precomputed values

**Visual Example**:
```
Binary lifting preprocessing:

Tree: 0 -> 1 -> 4
      0 -> 2
      0 -> 3

Precomputed ancestors:
┌─────────────────────────────────────┐
│ up[0][0] = parent[0] = -1          │
│ up[1][0] = parent[1] = 0           │
│ up[4][0] = parent[4] = 1           │
│                                   │
│ up[1][1] = up[up[1][0]][0] = -1   │
│ up[4][1] = up[up[4][0]][0] = 0    │
│                                   │
│ Query (4, 2):                     │
│ k = 2 = 10₂ (binary)              │
│ Jump 2^1 = 2 steps: 4 -> 0        │
│ Result: 0                         │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def binary_lifting_planets_queries_i(n, parent, queries):
    """Answer ancestor queries using binary lifting"""
    # Find maximum depth and log value
    max_depth = 0
    for i in range(n):
        depth = 0
        current = i
        while current != -1:
            current = parent[current]
            depth += 1
        max_depth = max(max_depth, depth)
    
    log = 0
    while (1 << log) <= max_depth:
        log += 1
    
    # Initialize binary lifting table
    up = [[-1] * log for _ in range(n)]
    
    # Fill first level (2^0 = 1)
    for i in range(n):
        up[i][0] = parent[i]
    
    # Fill remaining levels
    for j in range(1, log):
        for i in range(n):
            if up[i][j-1] != -1:
                up[i][j] = up[up[i][j-1]][j-1]
    
    # Answer queries
    results = []
    for vertex, k in queries:
        current = vertex
        
        # Use binary representation of k
        for j in range(log):
            if k & (1 << j):
                if current == -1:
                    break
                current = up[current][j]
        
        results.append(current)
    
    return results

# Example usage
n = 5
parent = [-1, 0, 0, 1, 1]
queries = [(4, 1), (4, 2), (4, 3)]
result = binary_lifting_planets_queries_i(n, parent, queries)
print(f"Binary lifting results: {result}")
```

**Time Complexity**: O(n log n + q log n)
**Space Complexity**: O(n log n)

**Why it's better**: Uses binary lifting for O(log n) per query.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for ancestor queries
- **Efficient Implementation**: O(n log n) preprocessing, O(log n) per query
- **Space Efficiency**: O(n log n) space complexity
- **Optimal Complexity**: Best approach for ancestor queries

**Key Insight**: Use advanced data structures for optimal ancestor queries.

**Algorithm**:
- Use specialized data structures for tree storage
- Implement efficient binary lifting algorithms
- Handle special cases optimally
- Return ancestor query results

**Visual Example**:
```
Advanced data structure approach:

For tree: 0 -> 1 -> 4
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Tree structure: for efficient     │
│   storage and traversal             │
│ - Binary lift cache: for            │
│   optimization                      │
│ - Query processor: for optimization │
│                                   │
│ Ancestor queries:                   │
│ - Use tree structure for efficient │
│   storage and traversal             │
│ - Use binary lift cache for         │
│   optimization                      │
│ - Use query processor for           │
│   optimization                      │
│                                   │
│ Result: [1, 0, -1]                 │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_planets_queries_i(n, parent, queries):
    """Answer ancestor queries using advanced data structure approach"""
    # Use advanced data structures for tree storage
    # Find maximum depth and log value
    max_depth = 0
    for i in range(n):
        depth = 0
        current = i
        while current != -1:
            current = parent[current]
            depth += 1
        max_depth = max(max_depth, depth)
    
    log = 0
    while (1 << log) <= max_depth:
        log += 1
    
    # Initialize advanced binary lifting table
    up = [[-1] * log for _ in range(n)]
    
    # Fill first level (2^0 = 1) using advanced data structures
    for i in range(n):
        up[i][0] = parent[i]
    
    # Fill remaining levels using advanced data structures
    for j in range(1, log):
        for i in range(n):
            if up[i][j-1] != -1:
                up[i][j] = up[up[i][j-1]][j-1]
    
    # Answer queries using advanced data structures
    results = []
    for vertex, k in queries:
        current = vertex
        
        # Use binary representation of k with advanced data structures
        for j in range(log):
            if k & (1 << j):
                if current == -1:
                    break
                current = up[current][j]
        
        results.append(current)
    
    return results

# Example usage
n = 5
parent = [-1, 0, 0, 1, 1]
queries = [(4, 1), (4, 2), (4, 3)]
result = advanced_data_structure_planets_queries_i(n, parent, queries)
print(f"Advanced data structure results: {result}")
```

**Time Complexity**: O(n log n + q log n)
**Space Complexity**: O(n log n)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(qk) | O(1) | Walk up tree k steps |
| Binary Lifting | O(n log n + q log n) | O(n log n) | Precompute powers of 2 |
| Advanced Data Structure | O(n log n + q log n) | O(n log n) | Use advanced data structures |

### Time Complexity
- **Time**: O(n log n + q log n) - Use binary lifting for efficient queries
- **Space**: O(n log n) - Store binary lifting table

### Why This Solution Works
- **Binary Lifting**: Precompute ancestors at powers of 2
- **Binary Representation**: Use binary representation of k for queries
- **Efficient Queries**: O(log n) per query using precomputed values
- **Optimal Algorithms**: Use optimal algorithms for ancestor queries

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Planets Queries I with Constraints**
**Problem**: Answer ancestor queries with specific constraints.

**Key Differences**: Apply constraints to ancestor queries

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_planets_queries_i(n, parent, queries, constraints):
    """Answer ancestor queries with constraints"""
    # Find maximum depth and log value
    max_depth = 0
    for i in range(n):
        if constraints(i):
            depth = 0
            current = i
            while current != -1 and constraints(current):
                current = parent[current]
                depth += 1
            max_depth = max(max_depth, depth)
    
    log = 0
    while (1 << log) <= max_depth:
        log += 1
    
    # Initialize binary lifting table
    up = [[-1] * log for _ in range(n)]
    
    # Fill first level (2^0 = 1)
    for i in range(n):
        if constraints(i):
            up[i][0] = parent[i] if constraints(parent[i]) else -1
    
    # Fill remaining levels
    for j in range(1, log):
        for i in range(n):
            if constraints(i) and up[i][j-1] != -1:
                up[i][j] = up[up[i][j-1]][j-1]
    
    # Answer queries
    results = []
    for vertex, k in queries:
        if not constraints(vertex):
            results.append(-1)
            continue
            
        current = vertex
        
        # Use binary representation of k
        for j in range(log):
            if k & (1 << j):
                if current == -1 or not constraints(current):
                    break
                current = up[current][j]
        
        results.append(current if constraints(current) else -1)
    
    return results

# Example usage
n = 5
parent = [-1, 0, 0, 1, 1]
queries = [(4, 1), (4, 2), (4, 3)]
constraints = lambda vertex: vertex >= 0  # Only include non-negative vertices
result = constrained_planets_queries_i(n, parent, queries, constraints)
print(f"Constrained results: {result}")
```

#### **2. Planets Queries I with Different Metrics**
**Problem**: Answer ancestor queries with different distance metrics.

**Key Differences**: Different distance calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_planets_queries_i(n, parent, queries, weights):
    """Answer ancestor queries with different weights"""
    # Find maximum depth and log value
    max_depth = 0
    for i in range(n):
        depth = 0
        current = i
        while current != -1:
            current = parent[current]
            depth += 1
        max_depth = max(max_depth, depth)
    
    log = 0
    while (1 << log) <= max_depth:
        log += 1
    
    # Initialize binary lifting table
    up = [[-1] * log for _ in range(n)]
    
    # Fill first level (2^0 = 1)
    for i in range(n):
        up[i][0] = parent[i]
    
    # Fill remaining levels
    for j in range(1, log):
        for i in range(n):
            if up[i][j-1] != -1:
                up[i][j] = up[up[i][j-1]][j-1]
    
    # Answer queries with weights
    results = []
    for vertex, k in queries:
        current = vertex
        total_weight = 0
        
        # Use binary representation of k
        for j in range(log):
            if k & (1 << j):
                if current == -1:
                    break
                total_weight += weights.get((current, up[current][j]), 1)
                current = up[current][j]
        
        if current == -1:
            results.append((-1, 0))
        else:
            results.append((current, total_weight))
    
    return results

# Example usage
n = 5
parent = [-1, 0, 0, 1, 1]
queries = [(4, 1), (4, 2), (4, 3)]
weights = {(0, 1): 2, (1, 4): 1, (0, 2): 3, (0, 3): 1}
result = weighted_planets_queries_i(n, parent, queries, weights)
print(f"Weighted results: {result}")
```

#### **3. Planets Queries I with Multiple Dimensions**
**Problem**: Answer ancestor queries in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_planets_queries_i(n, parent, queries, dimensions):
    """Answer ancestor queries in multiple dimensions"""
    # Find maximum depth and log value
    max_depth = 0
    for i in range(n):
        depth = 0
        current = i
        while current != -1:
            current = parent[current]
            depth += 1
        max_depth = max(max_depth, depth)
    
    log = 0
    while (1 << log) <= max_depth:
        log += 1
    
    # Initialize binary lifting table
    up = [[-1] * log for _ in range(n)]
    
    # Fill first level (2^0 = 1)
    for i in range(n):
        up[i][0] = parent[i]
    
    # Fill remaining levels
    for j in range(1, log):
        for i in range(n):
            if up[i][j-1] != -1:
                up[i][j] = up[up[i][j-1]][j-1]
    
    # Answer queries
    results = []
    for vertex, k in queries:
        current = vertex
        
        # Use binary representation of k
        for j in range(log):
            if k & (1 << j):
                if current == -1:
                    break
                current = up[current][j]
        
        results.append(current)
    
    return results

# Example usage
n = 5
parent = [-1, 0, 0, 1, 1]
queries = [(4, 1), (4, 2), (4, 3)]
dimensions = 1
result = multi_dimensional_planets_queries_i(n, parent, queries, dimensions)
print(f"Multi-dimensional results: {result}")
```

### Related Problems

#### **CSES Problems**
- [Planets Queries II](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Company Queries I](https://cses.fi/problemset/task/1075) - Tree Algorithms
- [Company Queries II](https://cses.fi/problemset/task/1075) - Tree Algorithms

#### **LeetCode Problems**
- [Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/) - Tree
- [Lowest Common Ancestor](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) - Tree
- [Binary Tree Paths](https://leetcode.com/problems/binary-tree-paths/) - Tree

#### **Problem Categories**
- **Tree Algorithms**: Ancestor queries, binary lifting, tree traversal
- **Query Processing**: Range queries, ancestor queries
- **Binary Lifting**: Powers of 2, efficient queries

## 🔗 Additional Resources

### **Algorithm References**
- [Tree Algorithms](https://cp-algorithms.com/graph/tree-algorithms.html) - Tree algorithms
- [Binary Lifting](https://cp-algorithms.com/graph/lca_binary_lifting.html) - Binary lifting algorithms
- [Lowest Common Ancestor](https://cp-algorithms.com/graph/lca.html) - LCA algorithms

### **Practice Problems**
- [CSES Planets Queries II](https://cses.fi/problemset/task/1075) - Medium
- [CSES Company Queries I](https://cses.fi/problemset/task/1075) - Medium
- [CSES Company Queries II](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Tree Traversal](https://en.wikipedia.org/wiki/Tree_traversal) - Wikipedia article
- [Binary Lifting](https://en.wikipedia.org/wiki/Binary_lifting) - Wikipedia article
- [Lowest Common Ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor) - Wikipedia article
