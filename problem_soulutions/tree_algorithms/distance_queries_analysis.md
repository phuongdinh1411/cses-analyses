---
layout: simple
title: "Distance Queries"
permalink: /problem_soulutions/tree_algorithms/distance_queries_analysis
---

# Distance Queries

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

Given a tree with n nodes, process q queries of the form "find the distance between nodes a and b".

**Input**: 
- First line: n (number of nodes)
- Next n-1 lines: edges of the tree
- Next line: q (number of queries)
- Next q lines: two integers a and b (query nodes)

**Output**: 
- q lines: distance between nodes a and b

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵

**Example**:
```
Input:
5
1 2
2 3
2 4
4 5
3
1 3
2 5
1 5

Output:
2
3
4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, perform BFS from node a to find distance to node b
2. Return the distance for each query
3. Use BFS to find shortest path in unweighted tree

**Implementation**:
```python
def brute_force_distance_queries(n, edges, queries):
    from collections import deque, defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def find_distance(a, b):
        if a == b:
            return 0
        
        # BFS to find distance from a to b
        queue = deque([(a, 0)])
        visited = {a}
        
        while queue:
            node, dist = queue.popleft()
            
            if node == b:
                return dist
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return -1  # Should not happen in a tree
    
    results = []
    for a, b in queries:
        distance = find_distance(a, b)
        results.append(distance)
    
    return results
```

**Analysis**:
- **Time**: O(q × n) - For each query, BFS takes O(n) time
- **Space**: O(n) - Queue and visited set
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with LCA
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute LCA using binary lifting
2. For each query, find LCA of a and b
3. Calculate distance as depth[a] + depth[b] - 2 * depth[LCA]

**Implementation**:
```python
def optimized_distance_queries(n, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Precompute LCA using binary lifting
    LOG = 20
    up = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    
    def dfs(node, parent):
        up[0][node] = parent
        depth[node] = depth[parent] + 1
        
        for child in graph[node]:
            if child != parent:
                dfs(child, node)
    
    dfs(1, 0)
    
    # Binary lifting
    for k in range(1, LOG):
        for node in range(1, n + 1):
            up[k][node] = up[k-1][up[k-1][node]]
    
    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        for k in range(LOG - 1, -1, -1):
            if depth[a] - (1 << k) >= depth[b]:
                a = up[k][a]
        
        if a == b:
            return a
        
        # Find LCA
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        
        return up[0][a]
    
    results = []
    for a, b in queries:
        lca_node = lca(a, b)
        distance = depth[a] + depth[b] - 2 * depth[lca_node]
        results.append(distance)
    
    return results
```

**Analysis**:
- **Time**: O(n log n + q log n) - Preprocessing + query processing
- **Space**: O(n log n) - Binary lifting table
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with LCA
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Use binary lifting to precompute LCA efficiently
2. For each query, find LCA and calculate distance using depth formula
3. Distance = depth[a] + depth[b] - 2 * depth[LCA]

**Implementation**:
```python
def optimal_distance_queries(n, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Precompute LCA using binary lifting
    LOG = 20
    up = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    
    def dfs(node, parent):
        up[0][node] = parent
        depth[node] = depth[parent] + 1
        
        for child in graph[node]:
            if child != parent:
                dfs(child, node)
    
    dfs(1, 0)
    
    # Binary lifting
    for k in range(1, LOG):
        for node in range(1, n + 1):
            up[k][node] = up[k-1][up[k-1][node]]
    
    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        
        # Bring a to same depth as b
        for k in range(LOG - 1, -1, -1):
            if depth[a] - (1 << k) >= depth[b]:
                a = up[k][a]
        
        if a == b:
            return a
        
        # Find LCA
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        
        return up[0][a]
    
    results = []
    for a, b in queries:
        lca_node = lca(a, b)
        distance = depth[a] + depth[b] - 2 * depth[lca_node]
        results.append(distance)
    
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

Depth array: [0, 1, 2, 2, 3, 4]

Query: Distance between nodes 1 and 5
1. LCA(1, 5) = 1
2. Distance = depth[1] + depth[5] - 2 * depth[1]
3. Distance = 1 + 4 - 2 * 1 = 3
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(n) | BFS for each query |
| Optimized | O(n log n + q log n) | O(n log n) | LCA with binary lifting |
| Optimal | O(n log n + q log n) | O(n log n) | LCA with binary lifting |

### Time Complexity
- **Time**: O(n log n + q log n) - Preprocessing + query processing with LCA
- **Space**: O(n log n) - Binary lifting table

### Why This Solution Works
- **LCA Technique**: Use lowest common ancestor to break path into two parts
- **Binary Lifting**: Efficiently find LCA in O(log n) time
- **Depth Formula**: Calculate distance using depth[a] + depth[b] - 2 * depth[LCA]
- **Optimal Approach**: LCA with binary lifting provides the best possible complexity for distance queries

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Distance Queries with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain distance queries efficiently.

**Link**: [CSES Problem Set - Distance Queries with Updates](https://cses.fi/problemset/task/distance_queries_updates)

```python
class DistanceQueriesWithUpdates:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.depth = [0] * n
        self.log_n = 20  # Maximum log n for binary lifting
        self.up = [[-1] * self.log_n for _ in range(n)]
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def _calculate_depths(self):
        """Calculate depth of each node using DFS"""
        def dfs(node, parent, d):
            self.depth[node] = d
            self.up[node][0] = parent
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node, d + 1)
        
        dfs(0, -1, 0)
    
    def _preprocess_binary_lifting(self):
        """Preprocess binary lifting table"""
        for j in range(1, self.log_n):
            for i in range(self.n):
                if self.up[i][j-1] != -1:
                    self.up[i][j] = self.up[self.up[i][j-1]][j-1]
    
    def add_edge(self, u, v):
        """Add edge between nodes u and v"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        
        # Recalculate depths and binary lifting table
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def remove_edge(self, u, v):
        """Remove edge between nodes u and v"""
        if v in self.adj[u]:
            self.adj[u].remove(v)
        if u in self.adj[v]:
            self.adj[v].remove(u)
        
        # Recalculate depths and binary lifting table
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def get_lca(self, node1, node2):
        """Get lowest common ancestor of two nodes"""
        # Make sure node1 is deeper
        if self.depth[node1] < self.depth[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        diff = self.depth[node1] - self.depth[node2]
        for j in range(self.log_n):
            if diff & (1 << j):
                node1 = self.up[node1][j]
        
        if node1 == node2:
            return node1
        
        # Binary search for LCA
        for j in range(self.log_n - 1, -1, -1):
            if self.up[node1][j] != self.up[node2][j]:
                node1 = self.up[node1][j]
                node2 = self.up[node2][j]
        
        return self.up[node1][0]
    
    def get_distance(self, node1, node2):
        """Get distance between two nodes"""
        lca = self.get_lca(node1, node2)
        return self.depth[node1] + self.depth[node2] - 2 * self.depth[lca]
    
    def get_path_between_nodes(self, node1, node2):
        """Get path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Path from node1 to LCA
        path1 = []
        current = node1
        while current != lca:
            path1.append(current)
            current = self.up[current][0]
        
        # Path from node2 to LCA
        path2 = []
        current = node2
        while current != lca:
            path2.append(current)
            current = self.up[current][0]
        
        # Combine paths
        return path1 + [lca] + path2[::-1]
    
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
            elif query['type'] == 'distance':
                result = self.get_distance(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'lca':
                result = self.get_lca(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path':
                result = self.get_path_between_nodes(query['u'], query['v'])
                results.append(result)
        return results
```

### Variation 2: Distance Queries with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on distance queries.

**Link**: [CSES Problem Set - Distance Queries Different Operations](https://cses.fi/problemset/task/distance_queries_operations)

```python
class DistanceQueriesDifferentOps:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.depth = [0] * n
        self.log_n = 20  # Maximum log n for binary lifting
        self.up = [[-1] * self.log_n for _ in range(n)]
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def _calculate_depths(self):
        """Calculate depth of each node using DFS"""
        def dfs(node, parent, d):
            self.depth[node] = d
            self.up[node][0] = parent
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node, d + 1)
        
        dfs(0, -1, 0)
    
    def _preprocess_binary_lifting(self):
        """Preprocess binary lifting table"""
        for j in range(1, self.log_n):
            for i in range(self.n):
                if self.up[i][j-1] != -1:
                    self.up[i][j] = self.up[self.up[i][j-1]][j-1]
    
    def get_lca(self, node1, node2):
        """Get lowest common ancestor of two nodes"""
        # Make sure node1 is deeper
        if self.depth[node1] < self.depth[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        diff = self.depth[node1] - self.depth[node2]
        for j in range(self.log_n):
            if diff & (1 << j):
                node1 = self.up[node1][j]
        
        if node1 == node2:
            return node1
        
        # Binary search for LCA
        for j in range(self.log_n - 1, -1, -1):
            if self.up[node1][j] != self.up[node2][j]:
                node1 = self.up[node1][j]
                node2 = self.up[node2][j]
        
        return self.up[node1][0]
    
    def get_distance(self, node1, node2):
        """Get distance between two nodes"""
        lca = self.get_lca(node1, node2)
        return self.depth[node1] + self.depth[node2] - 2 * self.depth[lca]
    
    def get_path_between_nodes(self, node1, node2):
        """Get path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Path from node1 to LCA
        path1 = []
        current = node1
        while current != lca:
            path1.append(current)
            current = self.up[current][0]
        
        # Path from node2 to LCA
        path2 = []
        current = node2
        while current != lca:
            path2.append(current)
            current = self.up[current][0]
        
        # Combine paths
        return path1 + [lca] + path2[::-1]
    
    def get_nodes_at_distance(self, node, distance):
        """Get all nodes at specific distance from given node"""
        nodes = []
        
        def dfs(current, parent, current_distance):
            if current_distance == distance:
                nodes.append(current)
                return
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    dfs(neighbor, current, current_distance + 1)
        
        dfs(node, -1, 0)
        return nodes
    
    def get_farthest_node(self, node):
        """Get farthest node from given node"""
        farthest_node = node
        max_distance = 0
        
        def dfs(current, parent, current_distance):
            nonlocal farthest_node, max_distance
            
            if current_distance > max_distance:
                max_distance = current_distance
                farthest_node = current
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    dfs(neighbor, current, current_distance + 1)
        
        dfs(node, -1, 0)
        return farthest_node, max_distance
    
    def get_diameter(self):
        """Get diameter of the tree"""
        # Find farthest node from any node (e.g., node 0)
        farthest1, _ = self.get_farthest_node(0)
        
        # Find farthest node from farthest1
        farthest2, diameter = self.get_farthest_node(farthest1)
        
        return diameter, farthest1, farthest2
    
    def get_center(self):
        """Get center(s) of the tree"""
        diameter, end1, end2 = self.get_diameter()
        
        # Find middle node(s) of the diameter
        path = self.get_path_between_nodes(end1, end2)
        
        if diameter % 2 == 0:
            # Single center
            return [path[diameter // 2]]
        else:
            # Two centers
            return [path[diameter // 2], path[diameter // 2 + 1]]
    
    def get_all_distances_from_node(self, node):
        """Get distances from given node to all other nodes"""
        distances = [0] * self.n
        
        def dfs(current, parent, current_distance):
            distances[current] = current_distance
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    dfs(neighbor, current, current_distance + 1)
        
        dfs(node, -1, 0)
        return distances
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        diameter, end1, end2 = self.get_diameter()
        center = self.get_center()
        max_depth = max(self.depth)
        
        return {
            'diameter': diameter,
            'diameter_endpoints': (end1, end2),
            'center': center,
            'max_depth': max_depth,
            'total_nodes': self.n
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'distance':
                result = self.get_distance(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'lca':
                result = self.get_lca(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path':
                result = self.get_path_between_nodes(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'nodes_at_distance':
                result = self.get_nodes_at_distance(query['node'], query['distance'])
                results.append(result)
            elif query['type'] == 'farthest_node':
                result = self.get_farthest_node(query['node'])
                results.append(result)
            elif query['type'] == 'diameter':
                result = self.get_diameter()
                results.append(result)
            elif query['type'] == 'center':
                result = self.get_center()
                results.append(result)
            elif query['type'] == 'all_distances':
                result = self.get_all_distances_from_node(query['node'])
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_tree_statistics()
                results.append(result)
        return results
```

### Variation 3: Distance Queries with Constraints
**Problem**: Handle distance queries with additional constraints (e.g., minimum distance, maximum distance).

**Link**: [CSES Problem Set - Distance Queries with Constraints](https://cses.fi/problemset/task/distance_queries_constraints)

```python
class DistanceQueriesWithConstraints:
    def __init__(self, n, edges, min_distance, max_distance):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.depth = [0] * n
        self.log_n = 20  # Maximum log n for binary lifting
        self.up = [[-1] * self.log_n for _ in range(n)]
        self.min_distance = min_distance
        self.max_distance = max_distance
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def _calculate_depths(self):
        """Calculate depth of each node using DFS"""
        def dfs(node, parent, d):
            self.depth[node] = d
            self.up[node][0] = parent
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node, d + 1)
        
        dfs(0, -1, 0)
    
    def _preprocess_binary_lifting(self):
        """Preprocess binary lifting table"""
        for j in range(1, self.log_n):
            for i in range(self.n):
                if self.up[i][j-1] != -1:
                    self.up[i][j] = self.up[self.up[i][j-1]][j-1]
    
    def get_lca(self, node1, node2):
        """Get lowest common ancestor of two nodes"""
        # Make sure node1 is deeper
        if self.depth[node1] < self.depth[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        diff = self.depth[node1] - self.depth[node2]
        for j in range(self.log_n):
            if diff & (1 << j):
                node1 = self.up[node1][j]
        
        if node1 == node2:
            return node1
        
        # Binary search for LCA
        for j in range(self.log_n - 1, -1, -1):
            if self.up[node1][j] != self.up[node2][j]:
                node1 = self.up[node1][j]
                node2 = self.up[node2][j]
        
        return self.up[node1][0]
    
    def get_distance(self, node1, node2):
        """Get distance between two nodes"""
        lca = self.get_lca(node1, node2)
        return self.depth[node1] + self.depth[node2] - 2 * self.depth[lca]
    
    def constrained_distance_query(self, node1, node2):
        """Query distance with constraints"""
        distance = self.get_distance(node1, node2)
        
        # Check if distance satisfies constraints
        if self.min_distance <= distance <= self.max_distance:
            return distance
        
        return -1
    
    def find_valid_pairs(self):
        """Find all pairs of nodes with valid distances"""
        valid_pairs = []
        
        for i in range(self.n):
            for j in range(i + 1, self.n):
                distance = self.get_distance(i, j)
                if self.min_distance <= distance <= self.max_distance:
                    valid_pairs.append((i, j, distance))
        
        return valid_pairs
    
    def count_valid_pairs(self):
        """Count number of valid pairs"""
        return len(self.find_valid_pairs())
    
    def get_valid_nodes_at_distance(self, node, distance):
        """Get all nodes at specific distance from given node that satisfy constraints"""
        if not (self.min_distance <= distance <= self.max_distance):
            return []
        
        nodes = []
        
        def dfs(current, parent, current_distance):
            if current_distance == distance:
                nodes.append(current)
                return
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    dfs(neighbor, current, current_distance + 1)
        
        dfs(node, -1, 0)
        return nodes
    
    def get_valid_distances_from_node(self, node):
        """Get all valid distances from given node to other nodes"""
        valid_distances = []
        
        def dfs(current, parent, current_distance):
            if current_distance > 0 and self.min_distance <= current_distance <= self.max_distance:
                valid_distances.append((current, current_distance))
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    dfs(neighbor, current, current_distance + 1)
        
        dfs(node, -1, 0)
        return valid_distances
    
    def get_constraint_statistics(self):
        """Get statistics about valid distances"""
        valid_pairs = self.find_valid_pairs()
        
        if not valid_pairs:
            return {
                'valid_pairs_count': 0,
                'min_distance': self.min_distance,
                'max_distance': self.max_distance,
                'valid_pairs': []
            }
        
        distances = [pair[2] for pair in valid_pairs]
        
        return {
            'valid_pairs_count': len(valid_pairs),
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'min_valid_distance': min(distances),
            'max_valid_distance': max(distances),
            'avg_valid_distance': sum(distances) / len(distances),
            'valid_pairs': valid_pairs
        }

# Example usage
n = 5
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
min_distance = 2
max_distance = 4

dq = DistanceQueriesWithConstraints(n, edges, min_distance, max_distance)
result = dq.constrained_distance_query(0, 4)
print(f"Constrained distance query result: {result}")

valid_pairs = dq.find_valid_pairs()
print(f"Valid pairs: {valid_pairs}")

statistics = dq.get_constraint_statistics()
print(f"Constraint statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Distance Queries](https://cses.fi/problemset/task/1135) - Basic distance queries in tree
- [Company Queries II](https://cses.fi/problemset/task/1688) - LCA queries in company hierarchy
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Find diameter of tree

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **LCA Algorithm**: Lowest common ancestor, binary lifting
- **Tree Queries**: Distance queries, path queries, tree analysis
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
- **Tree Traversal**: DFS, BFS, tree traversal algorithms
