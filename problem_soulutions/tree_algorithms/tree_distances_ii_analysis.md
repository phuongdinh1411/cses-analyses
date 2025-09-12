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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Tree Distances II with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain distance calculations efficiently.

**Link**: [CSES Problem Set - Tree Distances II with Updates](https://cses.fi/problemset/task/tree_distances_ii_updates)

```python
class TreeDistancesIIWithUpdates:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_sizes = [0] * n
        self.distances = [0] * n
        self.parent = [-1] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_distances()
    
    def _calculate_distances(self):
        """Calculate distances using tree DP with rerooting"""
        # First DFS: calculate subtree sizes and distances from root
        self._dfs1(0, -1)
        
        # Second DFS: calculate distances from each node using rerooting
        self._dfs2(0, -1)
    
    def _dfs1(self, node, parent):
        """First DFS to calculate subtree sizes and distances from root"""
        self.parent[node] = parent
        self.subtree_sizes[node] = 1
        self.distances[node] = 0
        
        for child in self.adj[node]:
            if child != parent:
                self._dfs1(child, node)
                self.subtree_sizes[node] += self.subtree_sizes[child]
                self.distances[node] += self.distances[child] + self.subtree_sizes[child]
    
    def _dfs2(self, node, parent):
        """Second DFS to calculate distances from each node using rerooting"""
        if parent != -1:
            # Reroot from parent to current node
            self.distances[node] = self.distances[parent] - self.subtree_sizes[node] + (self.n - self.subtree_sizes[node])
        
        for child in self.adj[node]:
            if child != parent:
                self._dfs2(child, node)
    
    def add_edge(self, u, v):
        """Add edge between nodes u and v"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        
        # Recalculate distances
        self._calculate_distances()
    
    def remove_edge(self, u, v):
        """Remove edge between nodes u and v"""
        if v in self.adj[u]:
            self.adj[u].remove(v)
        if u in self.adj[v]:
            self.adj[v].remove(u)
        
        # Recalculate distances
        self._calculate_distances()
    
    def get_distance_sum(self, node):
        """Get sum of distances from node to all other nodes"""
        return self.distances[node]
    
    def get_all_distance_sums(self):
        """Get distance sums for all nodes"""
        return self.distances.copy()
    
    def get_subtree_size(self, node):
        """Get subtree size of a node"""
        return self.subtree_sizes[node]
    
    def get_all_subtree_sizes(self):
        """Get subtree sizes for all nodes"""
        return self.subtree_sizes.copy()
    
    def get_distance_statistics(self):
        """Get comprehensive distance statistics"""
        return {
            'total_distance_sum': sum(self.distances),
            'max_distance_sum': max(self.distances),
            'min_distance_sum': min(self.distances),
            'avg_distance_sum': sum(self.distances) / self.n,
            'distance_sums': self.distances.copy(),
            'subtree_sizes': self.subtree_sizes.copy()
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
            elif query['type'] == 'distance_sum':
                result = self.get_distance_sum(query['node'])
                results.append(result)
            elif query['type'] == 'all_distance_sums':
                result = self.get_all_distance_sums()
                results.append(result)
            elif query['type'] == 'subtree_size':
                result = self.get_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'all_subtree_sizes':
                result = self.get_all_subtree_sizes()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_distance_statistics()
                results.append(result)
        return results
```

### Variation 2: Tree Distances II with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on tree distance calculations.

**Link**: [CSES Problem Set - Tree Distances II Different Operations](https://cses.fi/problemset/task/tree_distances_ii_operations)

```python
class TreeDistancesIIDifferentOps:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_sizes = [0] * n
        self.distances = [0] * n
        self.parent = [-1] * n
        self.depths = [0] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_distances()
    
    def _calculate_distances(self):
        """Calculate distances using tree DP with rerooting"""
        # First DFS: calculate subtree sizes and distances from root
        self._dfs1(0, -1, 0)
        
        # Second DFS: calculate distances from each node using rerooting
        self._dfs2(0, -1)
    
    def _dfs1(self, node, parent, depth):
        """First DFS to calculate subtree sizes and distances from root"""
        self.parent[node] = parent
        self.depths[node] = depth
        self.subtree_sizes[node] = 1
        self.distances[node] = 0
        
        for child in self.adj[node]:
            if child != parent:
                self._dfs1(child, node, depth + 1)
                self.subtree_sizes[node] += self.subtree_sizes[child]
                self.distances[node] += self.distances[child] + self.subtree_sizes[child]
    
    def _dfs2(self, node, parent):
        """Second DFS to calculate distances from each node using rerooting"""
        if parent != -1:
            # Reroot from parent to current node
            self.distances[node] = self.distances[parent] - self.subtree_sizes[node] + (self.n - self.subtree_sizes[node])
        
        for child in self.adj[node]:
            if child != parent:
                self._dfs2(child, node)
    
    def get_distance_sum(self, node):
        """Get sum of distances from node to all other nodes"""
        return self.distances[node]
    
    def get_all_distance_sums(self):
        """Get distance sums for all nodes"""
        return self.distances.copy()
    
    def get_subtree_size(self, node):
        """Get subtree size of a node"""
        return self.subtree_sizes[node]
    
    def get_all_subtree_sizes(self):
        """Get subtree sizes for all nodes"""
        return self.subtree_sizes.copy()
    
    def get_depth(self, node):
        """Get depth of a node"""
        return self.depths[node]
    
    def get_all_depths(self):
        """Get depths for all nodes"""
        return self.depths.copy()
    
    def get_distance_by_depth(self):
        """Get distance sums grouped by depth"""
        depth_groups = {}
        for i in range(self.n):
            depth = self.depths[i]
            if depth not in depth_groups:
                depth_groups[depth] = []
            depth_groups[depth].append(self.distances[i])
        
        return depth_groups
    
    def get_distance_statistics(self):
        """Get comprehensive distance statistics"""
        return {
            'total_distance_sum': sum(self.distances),
            'max_distance_sum': max(self.distances),
            'min_distance_sum': min(self.distances),
            'avg_distance_sum': sum(self.distances) / self.n,
            'distance_sums': self.distances.copy(),
            'subtree_sizes': self.subtree_sizes.copy(),
            'depths': self.depths.copy(),
            'distance_by_depth': self.get_distance_by_depth()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'distance_sum':
                result = self.get_distance_sum(query['node'])
                results.append(result)
            elif query['type'] == 'all_distance_sums':
                result = self.get_all_distance_sums()
                results.append(result)
            elif query['type'] == 'subtree_size':
                result = self.get_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'all_subtree_sizes':
                result = self.get_all_subtree_sizes()
                results.append(result)
            elif query['type'] == 'depth':
                result = self.get_depth(query['node'])
                results.append(result)
            elif query['type'] == 'all_depths':
                result = self.get_all_depths()
                results.append(result)
            elif query['type'] == 'distance_by_depth':
                result = self.get_distance_by_depth()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_distance_statistics()
                results.append(result)
        return results
```

### Variation 3: Tree Distances II with Constraints
**Problem**: Handle tree distance calculations with additional constraints (e.g., minimum depth, maximum depth, depth range).

**Link**: [CSES Problem Set - Tree Distances II with Constraints](https://cses.fi/problemset/task/tree_distances_ii_constraints)

```python
class TreeDistancesIIWithConstraints:
    def __init__(self, n, edges, min_depth, max_depth):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_sizes = [0] * n
        self.distances = [0] * n
        self.parent = [-1] * n
        self.depths = [0] * n
        self.min_depth = min_depth
        self.max_depth = max_depth
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_distances()
    
    def _calculate_distances(self):
        """Calculate distances using tree DP with rerooting"""
        # First DFS: calculate subtree sizes and distances from root
        self._dfs1(0, -1, 0)
        
        # Second DFS: calculate distances from each node using rerooting
        self._dfs2(0, -1)
    
    def _dfs1(self, node, parent, depth):
        """First DFS to calculate subtree sizes and distances from root"""
        self.parent[node] = parent
        self.depths[node] = depth
        self.subtree_sizes[node] = 1
        self.distances[node] = 0
        
        for child in self.adj[node]:
            if child != parent:
                self._dfs1(child, node, depth + 1)
                self.subtree_sizes[node] += self.subtree_sizes[child]
                self.distances[node] += self.distances[child] + self.subtree_sizes[child]
    
    def _dfs2(self, node, parent):
        """Second DFS to calculate distances from each node using rerooting"""
        if parent != -1:
            # Reroot from parent to current node
            self.distances[node] = self.distances[parent] - self.subtree_sizes[node] + (self.n - self.subtree_sizes[node])
        
        for child in self.adj[node]:
            if child != parent:
                self._dfs2(child, node)
    
    def get_distance_sum(self, node):
        """Get sum of distances from node to all other nodes"""
        return self.distances[node]
    
    def get_all_distance_sums(self):
        """Get distance sums for all nodes"""
        return self.distances.copy()
    
    def get_constrained_distance_sum(self, node):
        """Get sum of distances from node to nodes within depth constraints"""
        if not (self.min_depth <= self.depths[node] <= self.max_depth):
            return 0
        
        constrained_sum = 0
        for i in range(self.n):
            if self.min_depth <= self.depths[i] <= self.max_depth:
                # Calculate distance between node and i
                distance = self._get_distance(node, i)
                constrained_sum += distance
        
        return constrained_sum
    
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
    
    def get_all_constrained_distance_sums(self):
        """Get constrained distance sums for all nodes"""
        constrained_sums = []
        for i in range(self.n):
            constrained_sums.append(self.get_constrained_distance_sum(i))
        return constrained_sums
    
    def get_constrained_statistics(self):
        """Get comprehensive statistics considering depth constraints"""
        valid_nodes = self.get_valid_nodes()
        constrained_sums = self.get_all_constrained_distance_sums()
        
        return {
            'total_distance_sum': sum(self.distances),
            'constrained_distance_sum': sum(constrained_sums),
            'valid_nodes_count': len(valid_nodes),
            'max_constrained_sum': max(constrained_sums),
            'min_constrained_sum': min(constrained_sums),
            'avg_constrained_sum': sum(constrained_sums) / len(constrained_sums) if constrained_sums else 0,
            'min_depth': self.min_depth,
            'max_depth': self.max_depth,
            'valid_nodes': valid_nodes,
            'constrained_sums': constrained_sums
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'distance_sum':
                result = self.get_distance_sum(query['node'])
                results.append(result)
            elif query['type'] == 'all_distance_sums':
                result = self.get_all_distance_sums()
                results.append(result)
            elif query['type'] == 'constrained_distance_sum':
                result = self.get_constrained_distance_sum(query['node'])
                results.append(result)
            elif query['type'] == 'valid_nodes':
                result = self.get_valid_nodes()
                results.append(result)
            elif query['type'] == 'all_constrained_sums':
                result = self.get_all_constrained_distance_sums()
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

td = TreeDistancesIIWithConstraints(n, edges, min_depth, max_depth)
result = td.get_constrained_distance_sum(1)
print(f"Constrained distance sum result: {result}")

valid_nodes = td.get_valid_nodes()
print(f"Valid nodes: {valid_nodes}")

statistics = td.get_constrained_statistics()
print(f"Constrained statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Tree Distances II](https://cses.fi/problemset/task/1133) - Basic tree distance calculations
- [Tree Distances I](https://cses.fi/problemset/task/1132) - Tree distance calculations
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Tree diameter calculation

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Tree DP**: Dynamic programming on trees, distance calculations
- **Tree Traversal**: DFS, BFS, tree processing
- **Tree Queries**: Tree analysis, tree operations
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
