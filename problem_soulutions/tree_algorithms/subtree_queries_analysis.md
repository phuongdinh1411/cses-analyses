---
layout: simple
title: "Subtree Queries"
permalink: /problem_soulutions/tree_algorithms/subtree_queries_analysis
---

# Subtree Queries

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

Given a tree with n nodes, each node has a value. Process q queries of the form "find the sum of values in the subtree rooted at node a".

**Input**: 
- First line: n (number of nodes)
- Next n lines: values of nodes 1 to n
- Next n-1 lines: edges of the tree
- Next line: q (number of queries)
- Next q lines: integer a (subtree root)

**Output**: 
- q lines: sum of values in subtree rooted at a

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
1
2
3

Output:
15
14
3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, perform DFS from the given node
2. Sum all values in the subtree
3. Return the sum for each query

**Implementation**:
```python
def brute_force_subtree_queries(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def subtree_sum(node):
        # DFS to find sum of subtree rooted at node
        total_sum = values[node - 1]
        visited = set()
        
        def dfs(curr):
            visited.add(curr)
            for child in graph[curr]:
                if child not in visited:
                    total_sum += values[child - 1]
                    dfs(child)
        
        dfs(node)
        return total_sum
    
    results = []
    for a in queries:
        sum_val = subtree_sum(a)
        results.append(sum_val)
    
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
1. Use tree DP to precompute subtree sums for all nodes
2. For each query, return the precomputed sum
3. Use DFS to compute subtree sums in a single pass

**Implementation**:
```python
def optimized_subtree_queries(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Precompute subtree sums
    subtree_sums = [0] * (n + 1)
    
    def dfs(node, parent):
        subtree_sums[node] = values[node - 1]
        
        for child in graph[node]:
            if child != parent:
                subtree_sums[node] += dfs(child, node)
        
        return subtree_sums[node]
    
    dfs(1, -1)
    
    # Answer queries
    results = []
    for a in queries:
        results.append(subtree_sums[a])
    
    return results
```

**Analysis**:
- **Time**: O(n + q) - Single DFS pass + O(1) per query
- **Space**: O(n) - Recursion stack and subtree sums array
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Euler Tour
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use Euler tour to flatten the tree into an array
2. Each subtree corresponds to a contiguous range in the array
3. Use prefix sums for efficient range sum queries

**Implementation**:
```python
def optimal_subtree_queries(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Euler tour
    euler_tour = []
    in_time = [0] * (n + 1)
    out_time = [0] * (n + 1)
    time_counter = 0
    
    def dfs(node, parent):
        nonlocal time_counter
        in_time[node] = time_counter
        euler_tour.append(values[node - 1])
        time_counter += 1
        
        for child in graph[node]:
            if child != parent:
                dfs(child, node)
        
        out_time[node] = time_counter - 1
    
    dfs(1, -1)
    
    # Build prefix sums
    prefix_sums = [0] * (n + 1)
    for i in range(n):
        prefix_sums[i + 1] = prefix_sums[i] + euler_tour[i]
    
    # Answer queries
    results = []
    for a in queries:
        start = in_time[a]
        end = out_time[a]
        sum_val = prefix_sums[end + 1] - prefix_sums[start]
        results.append(sum_val)
    
    return results
```

**Analysis**:
- **Time**: O(n + q) - Euler tour + O(1) per query
- **Space**: O(n) - Euler tour array and prefix sums
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

Euler Tour:
[1, 2, 3, 4, 5]
 0  1  2  3  4

Subtree ranges:
Node 1: [0, 4] → sum = 15
Node 2: [1, 4] → sum = 14
Node 3: [2, 2] → sum = 3
Node 4: [3, 4] → sum = 9
Node 5: [4, 4] → sum = 5
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(n) | DFS for each query |
| Optimized | O(n + q) | O(n) | Tree DP with precomputation |
| Optimal | O(n + q) | O(n) | Euler tour with prefix sums |

### Time Complexity
- **Time**: O(n + q) - Single DFS pass + O(1) per query
- **Space**: O(n) - Euler tour array and prefix sums

### Why This Solution Works
- **Tree DP**: Use dynamic programming to precompute subtree sums
- **Euler Tour**: Flatten tree into array for efficient range queries
- **Prefix Sums**: Enable O(1) range sum queries on the flattened array
- **Optimal Approach**: Euler tour provides the most efficient solution for subtree queries
