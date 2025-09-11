---
layout: simple
title: "Company Queries Ii"
permalink: /problem_soulutions/tree_algorithms/company_queries_ii_analysis
---

# Company Queries Ii

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

Given a company hierarchy tree with n employees, process q queries of the form "find the k-th ancestor of employee a".

**Input**: 
- First line: n (number of employees)
- Next n-1 lines: parent-child relationships (parent, child)
- Next line: q (number of queries)
- Next q lines: two integers a and k (employee and ancestor level)

**Output**: 
- q lines: k-th ancestor of employee a (or -1 if doesn't exist)

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 1 ≤ k ≤ n

**Example**:
```
Input:
5
1 2
1 3
2 4
2 5
3
4 1
4 2
4 3

Output:
2
1
-1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, traverse up the tree k levels
2. Follow parent pointers until reaching the k-th ancestor
3. Return the ancestor or -1 if it doesn't exist

**Implementation**:
```python
def brute_force_company_queries_ii(n, edges, queries):
    from collections import defaultdict
    
    # Build parent array
    parent = [0] * (n + 1)
    for u, v in edges:
        parent[v] = u
    
    results = []
    for a, k in queries:
        current = a
        for _ in range(k):
            if current == 0:
                break
            current = parent[current]
        
        if current == 0:
            results.append(-1)
        else:
            results.append(current)
    
    return results
```

**Analysis**:
- **Time**: O(q × n) - For each query, traverse up to n levels
- **Space**: O(n) - Parent array
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Binary Lifting
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute ancestors at powers of 2 using binary lifting
2. For each query, use binary representation of k to find ancestor
3. Jump in powers of 2 to reach the k-th ancestor

**Implementation**:
```python
def optimized_company_queries_ii(n, edges, queries):
    from collections import defaultdict
    
    # Build parent array
    parent = [0] * (n + 1)
    for u, v in edges:
        parent[v] = u
    
    # Binary lifting
    LOG = 20
    up = [[0] * (n + 1) for _ in range(LOG)]
    
    # Initialize first level
    for i in range(1, n + 1):
        up[0][i] = parent[i]
    
    # Fill up the table
    for k in range(1, LOG):
        for i in range(1, n + 1):
            up[k][i] = up[k-1][up[k-1][i]]
    
    def kth_ancestor(node, k):
        current = node
        for i in range(LOG):
            if k & (1 << i):
                current = up[i][current]
                if current == 0:
                    return -1
        return current
    
    results = []
    for a, k in queries:
        ancestor = kth_ancestor(a, k)
        results.append(ancestor)
    
    return results
```

**Analysis**:
- **Time**: O(n log n + q log n) - Preprocessing + query processing
- **Space**: O(n log n) - Binary lifting table
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Binary Lifting
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Use binary lifting to precompute ancestors at powers of 2
2. For each query, decompose k into powers of 2
3. Jump in powers of 2 to reach the k-th ancestor efficiently

**Implementation**:
```python
def optimal_company_queries_ii(n, edges, queries):
    from collections import defaultdict
    
    # Build parent array
    parent = [0] * (n + 1)
    for u, v in edges:
        parent[v] = u
    
    # Binary lifting
    LOG = 20
    up = [[0] * (n + 1) for _ in range(LOG)]
    
    # Initialize first level
    for i in range(1, n + 1):
        up[0][i] = parent[i]
    
    # Fill up the table
    for k in range(1, LOG):
        for i in range(1, n + 1):
            up[k][i] = up[k-1][up[k-1][i]]
    
    def kth_ancestor(node, k):
        current = node
        for i in range(LOG):
            if k & (1 << i):
                current = up[i][current]
                if current == 0:
                    return -1
        return current
    
    results = []
    for a, k in queries:
        ancestor = kth_ancestor(a, k)
        results.append(ancestor)
    
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

Binary Lifting Table:
up[0]: [0, 0, 1, 2, 2, 4]  # 1st ancestors
up[1]: [0, 0, 0, 1, 1, 2]  # 2nd ancestors
up[2]: [0, 0, 0, 0, 0, 1]  # 4th ancestors

Query: Find 3rd ancestor of node 5
k = 3 = 2^1 + 2^0
1. Jump 2^0 = 1 level: 5 → 4
2. Jump 2^1 = 2 levels: 4 → 1
Result: 1
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(n) | Traverse up k levels for each query |
| Optimized | O(n log n + q log n) | O(n log n) | Binary lifting with powers of 2 |
| Optimal | O(n log n + q log n) | O(n log n) | Binary lifting with powers of 2 |

### Time Complexity
- **Time**: O(n log n + q log n) - Preprocessing + query processing with binary lifting
- **Space**: O(n log n) - Binary lifting table

### Why This Solution Works
- **Binary Lifting**: Precompute ancestors at powers of 2 for efficient jumping
- **Binary Representation**: Decompose k into powers of 2 to find ancestor
- **Efficient Queries**: Each query takes O(log n) time instead of O(n)
- **Optimal Approach**: Binary lifting provides the best possible complexity for ancestor queries
