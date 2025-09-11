---
layout: simple
title: "Company Queries I"
permalink: /problem_soulutions/tree_algorithms/company_queries_i_analysis
---

# Company Queries I

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

Given a company hierarchy tree with n employees, process q queries of the form "find the number of subordinates of employee a".

**Input**: 
- First line: n (number of employees)
- Next n-1 lines: parent-child relationships (parent, child)
- Next line: q (number of queries)
- Next q lines: integer a (employee)

**Output**: 
- q lines: number of subordinates of employee a

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵

**Example**:
```
Input:
5
1 2
1 3
2 4
2 5
3
1
2
3

Output:
4
2
0
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, perform DFS from the given employee
2. Count all nodes in the subtree
3. Return the count minus 1 (excluding the employee themselves)

**Implementation**:
```python
def brute_force_company_queries_i(n, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def count_subordinates(employee):
        # DFS to count all nodes in subtree
        count = 0
        visited = set()
        
        def dfs(node):
            nonlocal count
            visited.add(node)
            count += 1
            
            for child in graph[node]:
                if child not in visited:
                    dfs(child)
        
        dfs(employee)
        return count - 1  # Exclude the employee themselves
    
    results = []
    for a in queries:
        subordinates = count_subordinates(a)
        results.append(subordinates)
    
    return results
```

**Analysis**:
- **Time**: O(q × n) - For each query, DFS takes O(n) time
- **Space**: O(n) - Recursion stack and visited set
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Tree DP
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to precompute subtree sizes for all employees
2. For each query, return the precomputed size minus 1
3. Use DFS to compute subtree sizes in a single pass

**Implementation**:
```python
def optimized_company_queries_i(n, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Precompute subtree sizes
    subtree_sizes = [0] * (n + 1)
    
    def dfs(node, parent):
        subtree_sizes[node] = 1
        
        for child in graph[node]:
            if child != parent:
                subtree_sizes[node] += dfs(child, node)
        
        return subtree_sizes[node]
    
    dfs(1, -1)
    
    # Answer queries
    results = []
    for a in queries:
        subordinates = subtree_sizes[a] - 1  # Exclude the employee themselves
        results.append(subordinates)
    
    return results
```

**Analysis**:
- **Time**: O(n + q) - Single DFS pass + O(1) per query
- **Space**: O(n) - Recursion stack and subtree sizes array
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Tree DP
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to precompute subtree sizes for all employees
2. For each query, return the precomputed size minus 1
3. Use DFS to compute subtree sizes in a single pass

**Implementation**:
```python
def optimal_company_queries_i(n, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Precompute subtree sizes
    subtree_sizes = [0] * (n + 1)
    
    def dfs(node, parent):
        subtree_sizes[node] = 1
        
        for child in graph[node]:
            if child != parent:
                subtree_sizes[node] += dfs(child, node)
        
        return subtree_sizes[node]
    
    dfs(1, -1)
    
    # Answer queries
    results = []
    for a in queries:
        subordinates = subtree_sizes[a] - 1  # Exclude the employee themselves
        results.append(subordinates)
    
    return results
```

**Analysis**:
- **Time**: O(n + q) - Single DFS pass + O(1) per query
- **Space**: O(n) - Recursion stack and subtree sizes array
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
Company hierarchy:
    1 (CEO)
    |
    2 (Manager)
   / \
3   4 (Team Lead)
    |
    5 (Employee)

Subtree sizes:
Node 1: 5 (total employees)
Node 2: 3 (2, 4, 5)
Node 3: 1 (just 3)
Node 4: 2 (4, 5)
Node 5: 1 (just 5)

Subordinates count:
Employee 1: 4 subordinates
Employee 2: 2 subordinates
Employee 3: 0 subordinates
Employee 4: 1 subordinate
Employee 5: 0 subordinates
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(n) | DFS for each query |
| Optimized | O(n + q) | O(n) | Tree DP with precomputation |
| Optimal | O(n + q) | O(n) | Tree DP with precomputation |

### Time Complexity
- **Time**: O(n + q) - Single DFS pass + O(1) per query
- **Space**: O(n) - Recursion stack and subtree sizes array

### Why This Solution Works
- **Tree DP**: Use dynamic programming to precompute subtree sizes
- **Precomputation**: Compute all subtree sizes in a single DFS pass
- **Efficient Queries**: Each query takes O(1) time after preprocessing
- **Optimal Approach**: Tree DP provides the best possible complexity for subtree size queries
