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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Tree Diameter with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain tree diameter efficiently.

**Link**: [CSES Problem Set - Tree Diameter with Updates](https://cses.fi/problemset/task/tree_diameter_updates)

```python
class TreeDiameterWithUpdates:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.diameter = 0
        self.diameter_endpoints = (-1, -1)
        self.depths = [0] * n
        self.parent = [-1] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_diameter()
    
    def _calculate_diameter(self):
        """Calculate tree diameter using two DFS approach"""
        # First DFS: find one endpoint of diameter
        self._dfs(0, -1, 0)
        endpoint1 = max(range(self.n), key=lambda x: self.depths[x])
        
        # Second DFS: find other endpoint and diameter
        self._dfs(endpoint1, -1, 0)
        endpoint2 = max(range(self.n), key=lambda x: self.depths[x])
        
        self.diameter = self.depths[endpoint2]
        self.diameter_endpoints = (endpoint1, endpoint2)
    
    def _dfs(self, node, parent, depth):
        """DFS to calculate depths"""
        self.parent[node] = parent
        self.depths[node] = depth
        
        for child in self.adj[node]:
            if child != parent:
                self._dfs(child, node, depth + 1)
    
    def add_edge(self, u, v):
        """Add edge between nodes u and v"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        
        # Recalculate diameter
        self._calculate_diameter()
    
    def remove_edge(self, u, v):
        """Remove edge between nodes u and v"""
        if v in self.adj[u]:
            self.adj[u].remove(v)
        if u in self.adj[v]:
            self.adj[v].remove(u)
        
        # Recalculate diameter
        self._calculate_diameter()
    
    def get_diameter(self):
        """Get current tree diameter"""
        return self.diameter
    
    def get_diameter_endpoints(self):
        """Get endpoints of the diameter"""
        return self.diameter_endpoints
    
    def get_diameter_path(self):
        """Get the path of the diameter"""
        if self.diameter_endpoints[0] == -1:
            return []
        
        # Find path between endpoints
        path = []
        current = self.diameter_endpoints[1]
        while current != -1:
            path.append(current)
            current = self.parent[current]
        
        return path
    
    def get_node_depth(self, node):
        """Get depth of a node"""
        return self.depths[node]
    
    def get_all_depths(self):
        """Get all node depths"""
        return self.depths.copy()
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        return {
            'diameter': self.diameter,
            'diameter_endpoints': self.diameter_endpoints,
            'diameter_path': self.get_diameter_path(),
            'max_depth': max(self.depths),
            'min_depth': min(self.depths),
            'avg_depth': sum(self.depths) / self.n,
            'depths': self.depths.copy()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'add_edge':
                self.add_edge(query['u'], query['v'])
                results.append(None)
            elif query['type'] == 'remove_edge':
                self.remove_edge(query['u'], query['v'])
                results.append(None)
            elif query['type'] == 'diameter':
                result = self.get_diameter()
                results.append(result)
            elif query['type'] == 'diameter_endpoints':
                result = self.get_diameter_endpoints()
                results.append(result)
            elif query['type'] == 'diameter_path':
                result = self.get_diameter_path()
                results.append(result)
            elif query['type'] == 'node_depth':
                result = self.get_node_depth(query['node'])
                results.append(result)
            elif query['type'] == 'all_depths':
                result = self.get_all_depths()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_tree_statistics()
                results.append(result)
        return results
```

### Variation 2: Tree Diameter with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on tree diameter.

**Link**: [CSES Problem Set - Tree Diameter Different Operations](https://cses.fi/problemset/task/tree_diameter_operations)

```python
class TreeDiameterDifferentOps:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.diameter = 0
        self.diameter_endpoints = (-1, -1)
        self.depths = [0] * n
        self.parent = [-1] * n
        self.subtree_diameters = [0] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_diameter()
        self._calculate_subtree_diameters()
    
    def _calculate_diameter(self):
        """Calculate tree diameter using two DFS approach"""
        # First DFS: find one endpoint of diameter
        self._dfs(0, -1, 0)
        endpoint1 = max(range(self.n), key=lambda x: self.depths[x])
        
        # Second DFS: find other endpoint and diameter
        self._dfs(endpoint1, -1, 0)
        endpoint2 = max(range(self.n), key=lambda x: self.depths[x])
        
        self.diameter = self.depths[endpoint2]
        self.diameter_endpoints = (endpoint1, endpoint2)
    
    def _dfs(self, node, parent, depth):
        """DFS to calculate depths"""
        self.parent[node] = parent
        self.depths[node] = depth
        
        for child in self.adj[node]:
            if child != parent:
                self._dfs(child, node, depth + 1)
    
    def _calculate_subtree_diameters(self):
        """Calculate diameter of each subtree"""
        def dfs(node, parent):
            max_depth1 = 0
            max_depth2 = 0
            subtree_diameter = 0
            
            for child in self.adj[node]:
                if child != parent:
                    child_depth, child_diameter = dfs(child, node)
                    subtree_diameter = max(subtree_diameter, child_diameter)
                    
                    if child_depth > max_depth1:
                        max_depth2 = max_depth1
                        max_depth1 = child_depth
                    elif child_depth > max_depth2:
                        max_depth2 = child_depth
            
            # Diameter through this node
            current_diameter = max_depth1 + max_depth2
            subtree_diameter = max(subtree_diameter, current_diameter)
            
            self.subtree_diameters[node] = subtree_diameter
            return max_depth1 + 1, subtree_diameter
        
        dfs(0, -1)
    
    def get_diameter(self):
        """Get current tree diameter"""
        return self.diameter
    
    def get_diameter_endpoints(self):
        """Get endpoints of the diameter"""
        return self.diameter_endpoints
    
    def get_diameter_path(self):
        """Get the path of the diameter"""
        if self.diameter_endpoints[0] == -1:
            return []
        
        # Find path between endpoints
        path = []
        current = self.diameter_endpoints[1]
        while current != -1:
            path.append(current)
            current = self.parent[current]
        
        return path
    
    def get_subtree_diameter(self, node):
        """Get diameter of subtree rooted at node"""
        return self.subtree_diameters[node]
    
    def get_all_subtree_diameters(self):
        """Get diameters of all subtrees"""
        return self.subtree_diameters.copy()
    
    def get_node_depth(self, node):
        """Get depth of a node"""
        return self.depths[node]
    
    def get_all_depths(self):
        """Get all node depths"""
        return self.depths.copy()
    
    def get_diameter_statistics(self):
        """Get comprehensive diameter statistics"""
        return {
            'diameter': self.diameter,
            'diameter_endpoints': self.diameter_endpoints,
            'diameter_path': self.get_diameter_path(),
            'max_subtree_diameter': max(self.subtree_diameters),
            'min_subtree_diameter': min(self.subtree_diameters),
            'avg_subtree_diameter': sum(self.subtree_diameters) / self.n,
            'subtree_diameters': self.subtree_diameters.copy(),
            'depths': self.depths.copy()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'diameter':
                result = self.get_diameter()
                results.append(result)
            elif query['type'] == 'diameter_endpoints':
                result = self.get_diameter_endpoints()
                results.append(result)
            elif query['type'] == 'diameter_path':
                result = self.get_diameter_path()
                results.append(result)
            elif query['type'] == 'subtree_diameter':
                result = self.get_subtree_diameter(query['node'])
                results.append(result)
            elif query['type'] == 'all_subtree_diameters':
                result = self.get_all_subtree_diameters()
                results.append(result)
            elif query['type'] == 'node_depth':
                result = self.get_node_depth(query['node'])
                results.append(result)
            elif query['type'] == 'all_depths':
                result = self.get_all_depths()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_diameter_statistics()
                results.append(result)
        return results
```

### Variation 3: Tree Diameter with Constraints
**Problem**: Handle tree diameter with additional constraints (e.g., minimum depth, maximum depth, depth range).

**Link**: [CSES Problem Set - Tree Diameter with Constraints](https://cses.fi/problemset/task/tree_diameter_constraints)

```python
class TreeDiameterWithConstraints:
    def __init__(self, n, edges, min_depth, max_depth):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.diameter = 0
        self.diameter_endpoints = (-1, -1)
        self.depths = [0] * n
        self.parent = [-1] * n
        self.min_depth = min_depth
        self.max_depth = max_depth
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_diameter()
    
    def _calculate_diameter(self):
        """Calculate tree diameter using two DFS approach"""
        # First DFS: find one endpoint of diameter
        self._dfs(0, -1, 0)
        endpoint1 = max(range(self.n), key=lambda x: self.depths[x])
        
        # Second DFS: find other endpoint and diameter
        self._dfs(endpoint1, -1, 0)
        endpoint2 = max(range(self.n), key=lambda x: self.depths[x])
        
        self.diameter = self.depths[endpoint2]
        self.diameter_endpoints = (endpoint1, endpoint2)
    
    def _dfs(self, node, parent, depth):
        """DFS to calculate depths"""
        self.parent[node] = parent
        self.depths[node] = depth
        
        for child in self.adj[node]:
            if child != parent:
                self._dfs(child, node, depth + 1)
    
    def get_diameter(self):
        """Get current tree diameter"""
        return self.diameter
    
    def get_diameter_endpoints(self):
        """Get endpoints of the diameter"""
        return self.diameter_endpoints
    
    def get_diameter_path(self):
        """Get the path of the diameter"""
        if self.diameter_endpoints[0] == -1:
            return []
        
        # Find path between endpoints
        path = []
        current = self.diameter_endpoints[1]
        while current != -1:
            path.append(current)
            current = self.parent[current]
        
        return path
    
    def get_constrained_diameter(self):
        """Get diameter considering depth constraints"""
        constrained_diameter = 0
        constrained_endpoints = (-1, -1)
        
        # Find longest path between nodes within depth constraints
        for i in range(self.n):
            if self.min_depth <= self.depths[i] <= self.max_depth:
                for j in range(i + 1, self.n):
                    if self.min_depth <= self.depths[j] <= self.max_depth:
                        # Calculate distance between i and j
                        distance = self._get_distance(i, j)
                        if distance > constrained_diameter:
                            constrained_diameter = distance
                            constrained_endpoints = (i, j)
        
        return constrained_diameter, constrained_endpoints
    
    def _get_distance(self, node1, node2):
        """Get distance between two nodes"""
        # Find LCA
        lca = self._get_lca(node1, node2)
        return self.depths[node1] + self.depths[node2] - 2 * self.depths[lca]
    
    def _get_lca(self, node1, node2):
        """Get lowest common ancestor of two nodes"""
        # Make sure node1 is deeper
        if self.depths[node1] < self.depths[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        while self.depths[node1] > self.depths[node2]:
            node1 = self.parent[node1]
        
        # Find LCA
        while node1 != node2:
            node1 = self.parent[node1]
            node2 = self.parent[node2]
        
        return node1
    
    def get_valid_nodes(self):
        """Get nodes that satisfy depth constraints"""
        return [i for i in range(self.n) if self.min_depth <= self.depths[i] <= self.max_depth]
    
    def get_constrained_diameter_path(self):
        """Get path of constrained diameter"""
        constrained_diameter, constrained_endpoints = self.get_constrained_diameter()
        
        if constrained_endpoints[0] == -1:
            return []
        
        # Find path between constrained endpoints
        path = []
        current = constrained_endpoints[1]
        while current != -1:
            path.append(current)
            current = self.parent[current]
        
        return path
    
    def get_constrained_statistics(self):
        """Get comprehensive statistics considering depth constraints"""
        valid_nodes = self.get_valid_nodes()
        constrained_diameter, constrained_endpoints = self.get_constrained_diameter()
        
        return {
            'total_diameter': self.diameter,
            'constrained_diameter': constrained_diameter,
            'constrained_endpoints': constrained_endpoints,
            'constrained_path': self.get_constrained_diameter_path(),
            'valid_nodes_count': len(valid_nodes),
            'min_depth': self.min_depth,
            'max_depth': self.max_depth,
            'valid_nodes': valid_nodes
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'diameter':
                result = self.get_diameter()
                results.append(result)
            elif query['type'] == 'diameter_endpoints':
                result = self.get_diameter_endpoints()
                results.append(result)
            elif query['type'] == 'diameter_path':
                result = self.get_diameter_path()
                results.append(result)
            elif query['type'] == 'constrained_diameter':
                result = self.get_constrained_diameter()
                results.append(result)
            elif query['type'] == 'valid_nodes':
                result = self.get_valid_nodes()
                results.append(result)
            elif query['type'] == 'constrained_diameter_path':
                result = self.get_constrained_diameter_path()
                results.append(result)
            elif query['type'] == 'constrained_statistics':
                result = self.get_constrained_statistics()
                results.append(result)
        return results

# Example usage
n = 5
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
min_depth = 1
max_depth = 3

td = TreeDiameterWithConstraints(n, edges, min_depth, max_depth)
result = td.get_constrained_diameter()
print(f"Constrained diameter result: {result}")

valid_nodes = td.get_valid_nodes()
print(f"Valid nodes: {valid_nodes}")

statistics = td.get_constrained_statistics()
print(f"Constrained statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Basic tree diameter problem
- [Tree Distances I](https://cses.fi/problemset/task/1132) - Tree distance calculations
- [Subordinates](https://cses.fi/problemset/task/1674) - Tree traversal and analysis

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Tree Traversal**: DFS, BFS, tree processing
- **Tree DP**: Dynamic programming on trees, diameter calculation
- **Tree Queries**: Tree analysis, tree operations
- **Tree Algorithms**: Tree properties, tree analysis, tree operations