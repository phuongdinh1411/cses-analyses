---
layout: simple
title: "Tree Distances I"
permalink: /problem_soulutions/tree_algorithms/tree_distances_i_analysis
---

# Tree Distances I

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

Given a tree with n nodes, for each node, find the maximum distance to any other node in the tree.

**Input**: 
- First line: n (number of nodes)
- Next n-1 lines: edges of the tree

**Output**: 
- n lines: maximum distance from each node to any other node

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
3
2
3
2
3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each node, perform BFS to find the maximum distance to any other node
2. Return the maximum distance for each node
3. Use BFS to find shortest path to all other nodes

**Implementation**:
```python
def brute_force_tree_distances_i(n, edges):
    from collections import deque, defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    results = []
    
    for start in range(1, n + 1):
        # BFS to find maximum distance from start
        queue = deque([(start, 0)])
        visited = {start}
        max_distance = 0
        
        while queue:
            node, dist = queue.popleft()
            max_distance = max(max_distance, dist)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        results.append(max_distance)
    
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
1. Use tree DP to find the diameter of the tree
2. For each node, the maximum distance is either to one end of the diameter or the other
3. Use two DFS passes to find the diameter endpoints

**Implementation**:
```python
def optimized_tree_distances_i(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Find diameter endpoints
    def dfs(node, parent, dist):
        max_dist = dist
        farthest_node = node
        
        for child in graph[node]:
            if child != parent:
                child_dist, child_node = dfs(child, node, dist + 1)
                if child_dist > max_dist:
                    max_dist = child_dist
                    farthest_node = child_node
        
        return max_dist, farthest_node
    
    # First DFS to find one end of diameter
    _, end1 = dfs(1, -1, 0)
    
    # Second DFS to find the other end and distances from end1
    distances_from_end1 = [0] * (n + 1)
    def dfs_distances(node, parent, dist):
        distances_from_end1[node] = dist
        for child in graph[node]:
            if child != parent:
                dfs_distances(child, node, dist + 1)
    
    dfs_distances(end1, -1, 0)
    
    # Find the other end of diameter
    max_dist = 0
    end2 = end1
    for i in range(1, n + 1):
        if distances_from_end1[i] > max_dist:
            max_dist = distances_from_end1[i]
            end2 = i
    
    # Calculate distances from end2
    distances_from_end2 = [0] * (n + 1)
    def dfs_distances2(node, parent, dist):
        distances_from_end2[node] = dist
        for child in graph[node]:
            if child != parent:
                dfs_distances2(child, node, dist + 1)
    
    dfs_distances2(end2, -1, 0)
    
    # For each node, maximum distance is max of distances to both ends
    results = []
    for i in range(1, n + 1):
        max_distance = max(distances_from_end1[i], distances_from_end2[i])
        results.append(max_distance)
    
    return results
```

**Analysis**:
- **Time**: O(n) - Three DFS passes
- **Space**: O(n) - Recursion stack and distance arrays
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Tree DP
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to find the diameter of the tree
2. For each node, the maximum distance is either to one end of the diameter or the other
3. Use two DFS passes to find the diameter endpoints

**Implementation**:
```python
def optimal_tree_distances_i(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Find diameter endpoints
    def dfs(node, parent, dist):
        max_dist = dist
        farthest_node = node
        
        for child in graph[node]:
            if child != parent:
                child_dist, child_node = dfs(child, node, dist + 1)
                if child_dist > max_dist:
                    max_dist = child_dist
                    farthest_node = child_node
        
        return max_dist, farthest_node
    
    # First DFS to find one end of diameter
    _, end1 = dfs(1, -1, 0)
    
    # Second DFS to find the other end and distances from end1
    distances_from_end1 = [0] * (n + 1)
    def dfs_distances(node, parent, dist):
        distances_from_end1[node] = dist
        for child in graph[node]:
            if child != parent:
                dfs_distances(child, node, dist + 1)
    
    dfs_distances(end1, -1, 0)
    
    # Find the other end of diameter
    max_dist = 0
    end2 = end1
    for i in range(1, n + 1):
        if distances_from_end1[i] > max_dist:
            max_dist = distances_from_end1[i]
            end2 = i
    
    # Calculate distances from end2
    distances_from_end2 = [0] * (n + 1)
    def dfs_distances2(node, parent, dist):
        distances_from_end2[node] = dist
        for child in graph[node]:
            if child != parent:
                dfs_distances2(child, node, dist + 1)
    
    dfs_distances2(end2, -1, 0)
    
    # For each node, maximum distance is max of distances to both ends
    results = []
    for i in range(1, n + 1):
        max_distance = max(distances_from_end1[i], distances_from_end2[i])
        results.append(max_distance)
    
    return results
```

**Analysis**:
- **Time**: O(n) - Three DFS passes
- **Space**: O(n) - Recursion stack and distance arrays
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

Diameter: 1-2-4-5 (length 3)

Distances from end1 (1):
Node 1: 0
Node 2: 1
Node 3: 2
Node 4: 2
Node 5: 3

Distances from end2 (5):
Node 1: 3
Node 2: 2
Node 3: 3
Node 4: 1
Node 5: 0

Maximum distances:
Node 1: max(0, 3) = 3
Node 2: max(1, 2) = 2
Node 3: max(2, 3) = 3
Node 4: max(2, 1) = 2
Node 5: max(3, 0) = 3
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Use BFS from each node to find maximum distance |
| Optimized | O(n) | O(n) | Use tree diameter to find maximum distances efficiently |
| Optimal | O(n) | O(n) | Use tree diameter to find maximum distances efficiently |

### Time Complexity
- **Time**: O(n) - Three DFS passes to find diameter and calculate distances
- **Space**: O(n) - Recursion stack and distance arrays

### Why This Solution Works
- **Diameter Property**: The maximum distance from any node is always to one of the diameter endpoints
- **Efficient Calculation**: We can find the diameter in O(n) time using two DFS passes
- **Distance Calculation**: Once we have the diameter endpoints, we can calculate distances from each endpoint in O(n) time
- **Optimal Approach**: O(n) time complexity is optimal for this problem
