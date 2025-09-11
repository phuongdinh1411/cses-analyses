---
layout: simple
title: "Tree Diameter - Longest Path in Tree"
permalink: /problem_soulutions/tree_algorithms/tree_diameter_analysis
---

# Tree Diameter - Longest Path in Tree

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of tree diameter and its properties
- Apply DFS-based algorithms for finding tree diameter
- Implement efficient tree traversal techniques
- Optimize tree algorithms for large inputs
- Handle edge cases in tree problems (single node, linear trees)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tree algorithms, DFS, BFS, tree traversal, dynamic programming
- **Data Structures**: Trees, graphs, adjacency lists
- **Mathematical Concepts**: Tree theory, graph theory, longest path problem
- **Programming Skills**: Tree traversal implementation, DFS, algorithm optimization
- **Related Problems**: Tree Distances I (tree distances), Subordinates (tree traversal), Tree Matching (tree algorithms)

## 📋 Problem Description

Given a tree with n nodes, find the diameter of the tree. The diameter is the length of the longest path between any two nodes in the tree.

This is a fundamental tree algorithm problem that tests understanding of tree properties and efficient traversal techniques.

**Input**: 
- First line: integer n (number of nodes)
- Next n-1 lines: two integers a and b (edge between nodes a and b)

**Output**: 
- Print one integer: the diameter of the tree

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a, b ≤ n

**Example**:
```
Input:
5
1 2
1 3
3 4
3 5

Output:
3

Explanation**: 
The tree structure:
    1
   / \\
  2   3
     / \\
    4   5

The longest path is from node 2 to node 4 (or 5): 2 → 1 → 3 → 4
The diameter is 3 (length of this path).
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Pairs

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible pairs of nodes
- **Path Finding**: For each pair, find the shortest path (which is unique in trees)
- **Complete Coverage**: Guaranteed to find the longest path
- **Simple Implementation**: BFS/DFS for each pair

**Key Insight**: For each pair of nodes, find the path between them and keep track of the longest path found.

**Algorithm**:
- For each pair of nodes (i, j):
  - Find the path from i to j using BFS/DFS
  - Calculate the length of this path
  - Update maximum diameter if this path is longer

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

All possible paths:
1. (1,2): 1 → 2, length = 1
2. (1,3): 1 → 3, length = 1
3. (1,4): 1 → 3 → 4, length = 2
4. (1,5): 1 → 3 → 5, length = 2
5. (2,3): 2 → 1 → 3, length = 2
6. (2,4): 2 → 1 → 3 → 4, length = 3 ← Maximum
7. (2,5): 2 → 1 → 3 → 5, length = 3 ← Maximum
8. (3,4): 3 → 4, length = 1
9. (3,5): 3 → 5, length = 1
10. (4,5): 4 → 3 → 5, length = 2

Diameter: 3
```

**Implementation**:
```python
def brute_force_tree_diameter(n, edges):
    """
    Find tree diameter using brute force approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        int: diameter of the tree
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def bfs(start, end):
        """Find shortest path between start and end using BFS"""
        from collections import deque
        
        queue = deque([(start, 0)])
        visited = [False] * (n + 1)
        visited[start] = True
        
        while queue:
            node, distance = queue.popleft()
            
            if node == end:
                return distance
            
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, distance + 1))
        
        return 0
    
    max_diameter = 0
    
    # Check all pairs of nodes
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            path_length = bfs(i, j)
            max_diameter = max(max_diameter, path_length)
    
    return max_diameter

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = brute_force_tree_diameter(n, edges)
print(f"Brute force result: {result}")  # Output: 3
```

**Time Complexity**: O(n³) - For each pair, BFS takes O(n) time
**Space Complexity**: O(n) - For adjacency list and BFS queue

**Why it's inefficient**: Cubic time complexity makes it very slow for large inputs.

---

### Approach 2: Optimized - Two DFS Approach

**Key Insights from Optimized Approach**:
- **Two DFS Strategy**: Use two DFS traversals to find diameter
- **Farthest Node**: First DFS finds the farthest node from any starting node
- **Diameter Endpoint**: Second DFS finds the farthest node from the first farthest node
- **Linear Time**: Achieve O(n) time complexity

**Key Insight**: The diameter of a tree can be found by performing two DFS traversals: first to find one endpoint of the diameter, then to find the other endpoint.

**Algorithm**:
- Perform DFS from any node to find the farthest node
- Perform DFS from the farthest node to find the diameter
- The distance found in the second DFS is the diameter

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

Step 1: DFS from node 1
- Distance to node 2: 1
- Distance to node 3: 1
- Distance to node 4: 2
- Distance to node 5: 2
- Farthest node: 4 or 5 (distance 2)

Step 2: DFS from node 4
- Distance to node 1: 2
- Distance to node 2: 3
- Distance to node 3: 1
- Distance to node 5: 2
- Farthest node: 2 (distance 3)

Diameter: 3
```

**Implementation**:
```python
def optimized_tree_diameter(n, edges):
    """
    Find tree diameter using two DFS approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        int: diameter of the tree
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def dfs(node, parent, distance):
        """DFS to find farthest node and its distance"""
        farthest_node = node
        max_distance = distance
        
        for neighbor in adj[node]:
            if neighbor != parent:
                far_node, far_dist = dfs(neighbor, node, distance + 1)
                if far_dist > max_distance:
                    max_distance = far_dist
                    farthest_node = far_node
        
        return farthest_node, max_distance
    
    # First DFS: find farthest node from node 1
    farthest_node, _ = dfs(1, -1, 0)
    
    # Second DFS: find diameter from the farthest node
    _, diameter = dfs(farthest_node, -1, 0)
    
    return diameter

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = optimized_tree_diameter(n, edges)
print(f"Optimized result: {result}")  # Output: 3
```

**Time Complexity**: O(n) - Two DFS traversals
**Space Complexity**: O(n) - For adjacency list and recursion stack

**Why it's better**: Linear time complexity with efficient tree traversal.

---

### Approach 3: Optimal - Single DFS with Dynamic Programming

**Key Insights from Optimal Approach**:
- **Tree DP**: Use dynamic programming on trees
- **Subtree Diameter**: Calculate diameter for each subtree
- **Path Through Root**: Consider paths that go through the current node
- **Single Traversal**: Find diameter in a single DFS pass

**Key Insight**: For each node, calculate the diameter of its subtree and the longest path through that node.

**Algorithm**:
- For each node, calculate:
  - Longest path in subtree (not through current node)
  - Longest path through current node
- Return the maximum diameter found

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

DFS with DP:
Node 4: diameter = 0, max_depth = 0
Node 5: diameter = 0, max_depth = 0
Node 3: 
  - max_depth = 1 (to nodes 4, 5)
  - diameter = 2 (path 4-3-5)
Node 2: diameter = 0, max_depth = 0
Node 1:
  - max_depth = 2 (to nodes 4, 5 through node 3)
  - diameter = 3 (path 2-1-3-4 or 2-1-3-5)

Maximum diameter: 3
```

**Implementation**:
```python
def optimal_tree_diameter(n, edges):
    """
    Find tree diameter using single DFS with DP
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        int: diameter of the tree
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    max_diameter = 0
    
    def dfs(node, parent):
        """DFS with dynamic programming"""
        nonlocal max_diameter
        
        # Longest and second longest paths from this node
        max_depth1 = max_depth2 = 0
        
        for neighbor in adj[node]:
            if neighbor != parent:
                depth = dfs(neighbor, node) + 1
                
                if depth > max_depth1:
                    max_depth2 = max_depth1
                    max_depth1 = depth
                elif depth > max_depth2:
                    max_depth2 = depth
        
        # Diameter through this node
        diameter_through_node = max_depth1 + max_depth2
        max_diameter = max(max_diameter, diameter_through_node)
        
        # Return longest path from this node
        return max_depth1
    
    dfs(1, -1)
    return max_diameter

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = optimal_tree_diameter(n, edges)
print(f"Optimal result: {result}")  # Output: 3
```

**Time Complexity**: O(n) - Single DFS traversal
**Space Complexity**: O(n) - For adjacency list and recursion stack

**Why it's optimal**: Single traversal with optimal time and space complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all pairs |
| Two DFS | O(n) | O(n) | Find endpoints of diameter |
| Single DFS with DP | O(n) | O(n) | Dynamic programming on trees |

### Time Complexity
- **Time**: O(n) - Single DFS traversal with dynamic programming
- **Space**: O(n) - For adjacency list and recursion stack

### Why This Solution Works
- **Tree Properties**: Leverage unique properties of trees (unique paths)
- **Dynamic Programming**: Use DP to calculate subtree diameters efficiently
- **Single Traversal**: Find diameter in one pass through the tree
- **Optimal Approach**: Single DFS with DP provides the most elegant solution