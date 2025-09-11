---
layout: simple
title: "Tree Distances Ii"
permalink: /problem_soulutions/tree_algorithms/tree_distances_ii_analysis
---

# Tree Distances Ii

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

Given a tree with n nodes, for each node, find the sum of distances to all other nodes in the tree.

**Input**: 
- First line: n (number of nodes)
- Next n-1 lines: edges of the tree

**Output**: 
- n lines: sum of distances from each node to all other nodes

**Constraints**:
- 1 ≤ n ≤ 2×10⁵

**Example**:
```
Input:
5
1 2
2 3
2 4
4 5

Output:
6
4
6
4
6
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each node, perform BFS to find distances to all other nodes
2. Sum up all distances for each node
3. Return the sum of distances for each node

**Implementation**:
```python
def brute_force_tree_distances_ii(n, edges):
    from collections import deque, defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    results = []
    
    for start in range(1, n + 1):
        # BFS to find distances from start to all other nodes
        queue = deque([(start, 0)])
        visited = {start}
        total_distance = 0
        
        while queue:
            node, dist = queue.popleft()
            if node != start:  # Don't count distance to itself
                total_distance += dist
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        results.append(total_distance)
    
    return results
```

**Analysis**:
- **Time**: O(n²) - For each node, BFS takes O(n) time
- **Space**: O(n) - Queue and visited set
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Tree DP
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to calculate subtree sizes and distances
2. Use rerooting technique to calculate distances from each node
3. For each node, calculate sum of distances using DP

**Implementation**:
```python
def optimized_tree_distances_ii(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # First pass: calculate subtree sizes and distances from root
    subtree_size = [0] * (n + 1)
    distances_from_root = [0] * (n + 1)
    
    def dfs1(node, parent):
        subtree_size[node] = 1
        for child in graph[node]:
            if child != parent:
                dfs1(child, node)
                subtree_size[node] += subtree_size[child]
                distances_from_root[node] += distances_from_root[child] + subtree_size[child]
    
    dfs1(1, -1)
    
    # Second pass: calculate distances from each node using rerooting
    total_distances = [0] * (n + 1)
    total_distances[1] = distances_from_root[1]
    
    def dfs2(node, parent):
        for child in graph[node]:
            if child != parent:
                # Reroot from node to child
                total_distances[child] = (total_distances[node] - 
                                        distances_from_root[child] - subtree_size[child] + 
                                        (n - subtree_size[child]))
                dfs2(child, node)
    
    dfs2(1, -1)
    
    return total_distances[1:]
```

**Analysis**:
- **Time**: O(n) - Two DFS passes
- **Space**: O(n) - Recursion stack and arrays
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Tree DP
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to calculate subtree sizes and distances
2. Use rerooting technique to calculate distances from each node
3. For each node, calculate sum of distances using DP

**Implementation**:
```python
def optimal_tree_distances_ii(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # First pass: calculate subtree sizes and distances from root
    subtree_size = [0] * (n + 1)
    distances_from_root = [0] * (n + 1)
    
    def dfs1(node, parent):
        subtree_size[node] = 1
        for child in graph[node]:
            if child != parent:
                dfs1(child, node)
                subtree_size[node] += subtree_size[child]
                distances_from_root[node] += distances_from_root[child] + subtree_size[child]
    
    dfs1(1, -1)
    
    # Second pass: calculate distances from each node using rerooting
    total_distances = [0] * (n + 1)
    total_distances[1] = distances_from_root[1]
    
    def dfs2(node, parent):
        for child in graph[node]:
            if child != parent:
                # Reroot from node to child
                total_distances[child] = (total_distances[node] - 
                                        distances_from_root[child] - subtree_size[child] + 
                                        (n - subtree_size[child]))
                dfs2(child, node)
    
    dfs2(1, -1)
    
    return total_distances[1:]
```

**Analysis**:
- **Time**: O(n) - Two DFS passes
- **Space**: O(n) - Recursion stack and arrays
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

Subtree sizes:
Node 1: 5
Node 2: 4
Node 3: 1
Node 4: 2
Node 5: 1

Distances from root (1):
Node 1: 0
Node 2: 1
Node 3: 2
Node 4: 2
Node 5: 3

Total distances:
Node 1: 0 + 1 + 2 + 2 + 3 = 8
Node 2: 1 + 0 + 1 + 1 + 2 = 5
Node 3: 2 + 1 + 0 + 2 + 3 = 8
Node 4: 2 + 1 + 2 + 0 + 1 = 6
Node 5: 3 + 2 + 3 + 1 + 0 = 9
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Use BFS from each node to find distances to all other nodes |
| Optimized | O(n) | O(n) | Use tree DP with rerooting to calculate distances efficiently |
| Optimal | O(n) | O(n) | Use tree DP with rerooting to calculate distances efficiently |

### Time Complexity
- **Time**: O(n) - Two DFS passes to calculate subtree sizes and distances
- **Space**: O(n) - Recursion stack and arrays for subtree sizes and distances

### Why This Solution Works
- **Tree DP**: Use dynamic programming to calculate subtree sizes and distances from root
- **Rerooting**: Use rerooting technique to calculate distances from each node efficiently
- **Efficient Calculation**: Calculate distances from each node in O(1) time using precomputed values
- **Optimal Approach**: O(n) time complexity is optimal for this problem
