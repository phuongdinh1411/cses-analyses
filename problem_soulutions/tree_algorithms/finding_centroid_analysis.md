---
layout: simple
title: "Finding Centroid"
permalink: /problem_soulutions/tree_algorithms/finding_centroid_analysis
---

# Finding Centroid

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

Given a tree with n nodes, find the centroid of the tree. A centroid is a node such that when removed, the tree breaks into components of size at most n/2.

**Input**: 
- First line: n (number of nodes)
- Next n-1 lines: edges of the tree

**Output**: 
- The centroid node (if multiple centroids exist, output any one)

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- Tree is connected

**Example**:
```
Input:
5
1 2
2 3
2 4
4 5

Output:
2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each node, remove it and check if all remaining components have size ≤ n/2
2. Use DFS to find component sizes after removal
3. Return the first node that satisfies the centroid condition

**Implementation**:
```python
def brute_force_finding_centroid(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def get_component_sizes(node_to_remove):
        visited = set()
        component_sizes = []
        
        def dfs(node, parent):
            if node in visited or node == node_to_remove:
                return 0
            visited.add(node)
            size = 1
            for child in graph[node]:
                if child != parent:
                    size += dfs(child, node)
            return size
        
        for node in range(1, n + 1):
            if node not in visited and node != node_to_remove:
                size = dfs(node, -1)
                component_sizes.append(size)
        
        return component_sizes
    
    for node in range(1, n + 1):
        component_sizes = get_component_sizes(node)
        if all(size <= n // 2 for size in component_sizes):
            return node
    
    return -1
```

**Analysis**:
- **Time**: O(n²) - For each node, DFS takes O(n) time
- **Space**: O(n) - Recursion stack and visited set
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Tree DP
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to compute subtree sizes for each node
2. For each node, check if removing it creates components of size ≤ n/2
3. Use the subtree size information to efficiently check centroid condition

**Implementation**:
```python
def optimized_finding_centroid(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    subtree_sizes = [0] * (n + 1)
    
    def dfs(node, parent):
        subtree_sizes[node] = 1
        for child in graph[node]:
            if child != parent:
                subtree_sizes[node] += dfs(child, node)
        return subtree_sizes[node]
    
    dfs(1, -1)
    
    def is_centroid(node):
        for child in graph[node]:
            if subtree_sizes[child] < subtree_sizes[node]:
                if subtree_sizes[child] > n // 2:
                    return False
        return subtree_sizes[node] <= n // 2
    
    for node in range(1, n + 1):
        if is_centroid(node):
            return node
    
    return -1
```

**Analysis**:
- **Time**: O(n) - Single DFS pass
- **Space**: O(n) - Recursion stack and subtree sizes array
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Centroid Finding Algorithm
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use the standard centroid finding algorithm
2. Start from any node and move towards the largest subtree
3. Continue until we find a node where all subtrees have size ≤ n/2

**Implementation**:
```python
def optimal_finding_centroid(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def find_centroid():
        # Start from node 1
        current = 1
        parent = -1
        
        while True:
            # Find the largest subtree
            max_subtree_size = 0
            max_subtree_node = -1
            
            for child in graph[current]:
                if child != parent:
                    # Calculate subtree size
                    subtree_size = 0
                    def dfs_size(node, par):
                        nonlocal subtree_size
                        subtree_size = 1
                        for grandchild in graph[node]:
                            if grandchild != par:
                                subtree_size += dfs_size(grandchild, node)
                        return subtree_size
                    
                    size = dfs_size(child, current)
                    if size > max_subtree_size:
                        max_subtree_size = size
                        max_subtree_node = child
            
            # If largest subtree has size ≤ n/2, current is centroid
            if max_subtree_size <= n // 2:
                return current
            
            # Move towards the largest subtree
            parent = current
            current = max_subtree_node
    
    return find_centroid()
```

**Analysis**:
- **Time**: O(n) - At most O(n) moves, each move takes O(degree) time
- **Space**: O(n) - Recursion stack
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

Centroid Finding Process:
1. Start at node 1
2. Largest subtree: {2,3,4,5} (size 4 > 5/2)
3. Move to node 2
4. Largest subtree: {4,5} (size 2 ≤ 5/2)
5. Node 2 is the centroid
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check each node by removing it |
| Optimized | O(n) | O(n) | Tree DP with subtree sizes |
| Optimal | O(n) | O(n) | Centroid finding algorithm |

### Time Complexity
- **Time**: O(n) - Single DFS pass to find centroid
- **Space**: O(n) - Recursion stack and subtree sizes array

### Why This Solution Works
- **Centroid Property**: A centroid always exists in any tree
- **Tree DP**: Use dynamic programming to compute subtree sizes efficiently
- **Centroid Finding**: Move towards the largest subtree until centroid is found
- **Optimal Approach**: The centroid finding algorithm provides the most efficient solution

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Finding Centroid with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain centroid queries efficiently.

**Link**: [CSES Problem Set - Finding Centroid with Updates](https://cses.fi/problemset/task/finding_centroid_updates)

```python
class FindingCentroidWithUpdates:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_sizes = [0] * n
        self.centroid = -1
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._find_centroid()
    
    def _calculate_subtree_sizes(self, node, parent):
        """Calculate subtree sizes using DFS"""
        self.subtree_sizes[node] = 1
        
        for child in self.adj[node]:
            if child != parent:
                self._calculate_subtree_sizes(child, node)
                self.subtree_sizes[node] += self.subtree_sizes[child]
    
    def _find_centroid(self):
        """Find centroid of the tree"""
        # Calculate subtree sizes
        self._calculate_subtree_sizes(0, -1)
        
        # Find centroid
        current = 0
        while True:
            found = False
            for child in self.adj[current]:
                if self.subtree_sizes[child] > self.n // 2:
                    current = child
                    found = True
                    break
            
            if not found:
                break
        
        self.centroid = current
    
    def add_edge(self, u, v):
        """Add edge between nodes u and v"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        
        # Recalculate centroid
        self._find_centroid()
    
    def remove_edge(self, u, v):
        """Remove edge between nodes u and v"""
        if v in self.adj[u]:
            self.adj[u].remove(v)
        if u in self.adj[v]:
            self.adj[v].remove(u)
        
        # Recalculate centroid
        self._find_centroid()
    
    def get_centroid(self):
        """Get current centroid of the tree"""
        return self.centroid
    
    def get_subtree_size(self, node):
        """Get subtree size of a node"""
        return self.subtree_sizes[node]
    
    def get_all_subtree_sizes(self):
        """Get all subtree sizes"""
        return self.subtree_sizes.copy()
    
    def get_centroid_properties(self):
        """Get properties of the centroid"""
        if self.centroid == -1:
            return None
        
        max_subtree_size = 0
        for child in self.adj[self.centroid]:
            if self.subtree_sizes[child] > max_subtree_size:
                max_subtree_size = self.subtree_sizes[child]
        
        return {
            'centroid': self.centroid,
            'max_subtree_size': max_subtree_size,
            'is_valid_centroid': max_subtree_size <= self.n // 2
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
            elif query['type'] == 'centroid':
                result = self.get_centroid()
                results.append(result)
            elif query['type'] == 'subtree_size':
                result = self.get_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'all_subtree_sizes':
                result = self.get_all_subtree_sizes()
                results.append(result)
            elif query['type'] == 'centroid_properties':
                result = self.get_centroid_properties()
                results.append(result)
        return results
```

### Variation 2: Finding Centroid with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on centroid finding.

**Link**: [CSES Problem Set - Finding Centroid Different Operations](https://cses.fi/problemset/task/finding_centroid_operations)

```python
class FindingCentroidDifferentOps:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_sizes = [0] * n
        self.centroid = -1
        self.depths = [0] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._find_centroid()
        self._calculate_depths()
    
    def _calculate_subtree_sizes(self, node, parent):
        """Calculate subtree sizes using DFS"""
        self.subtree_sizes[node] = 1
        
        for child in self.adj[node]:
            if child != parent:
                self._calculate_subtree_sizes(child, node)
                self.subtree_sizes[node] += self.subtree_sizes[child]
    
    def _calculate_depths(self):
        """Calculate depth of each node"""
        def dfs(node, parent, depth):
            self.depths[node] = depth
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node, depth + 1)
        
        dfs(0, -1, 0)
    
    def _find_centroid(self):
        """Find centroid of the tree"""
        # Calculate subtree sizes
        self._calculate_subtree_sizes(0, -1)
        
        # Find centroid
        current = 0
        while True:
            found = False
            for child in self.adj[current]:
                if self.subtree_sizes[child] > self.n // 2:
                    current = child
                    found = True
                    break
            
            if not found:
                break
        
        self.centroid = current
    
    def get_centroid(self):
        """Get current centroid of the tree"""
        return self.centroid
    
    def get_centroid_depth(self):
        """Get depth of the centroid"""
        return self.depths[self.centroid]
    
    def get_centroid_children(self):
        """Get children of the centroid"""
        return self.adj[self.centroid].copy()
    
    def get_centroid_subtree_sizes(self):
        """Get subtree sizes of centroid's children"""
        subtree_sizes = []
        for child in self.adj[self.centroid]:
            subtree_sizes.append(self.subtree_sizes[child])
        return subtree_sizes
    
    def get_centroid_balance(self):
        """Get balance of the centroid (max subtree size / total size)"""
        if self.centroid == -1:
            return 0
        
        max_subtree_size = max(self.get_centroid_subtree_sizes()) if self.get_centroid_subtree_sizes() else 0
        return max_subtree_size / self.n
    
    def get_centroid_distance_to_root(self):
        """Get distance from centroid to root"""
        return self.depths[self.centroid]
    
    def get_centroid_statistics(self):
        """Get comprehensive centroid statistics"""
        if self.centroid == -1:
            return None
        
        return {
            'centroid': self.centroid,
            'depth': self.depths[self.centroid],
            'children_count': len(self.adj[self.centroid]),
            'subtree_sizes': self.get_centroid_subtree_sizes(),
            'balance': self.get_centroid_balance(),
            'is_valid_centroid': self.get_centroid_balance() <= 0.5
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'centroid':
                result = self.get_centroid()
                results.append(result)
            elif query['type'] == 'centroid_depth':
                result = self.get_centroid_depth()
                results.append(result)
            elif query['type'] == 'centroid_children':
                result = self.get_centroid_children()
                results.append(result)
            elif query['type'] == 'centroid_subtree_sizes':
                result = self.get_centroid_subtree_sizes()
                results.append(result)
            elif query['type'] == 'centroid_balance':
                result = self.get_centroid_balance()
                results.append(result)
            elif query['type'] == 'centroid_distance_to_root':
                result = self.get_centroid_distance_to_root()
                results.append(result)
            elif query['type'] == 'centroid_statistics':
                result = self.get_centroid_statistics()
                results.append(result)
        return results
```

### Variation 3: Finding Centroid with Constraints
**Problem**: Handle centroid finding queries with additional constraints (e.g., minimum balance, maximum depth).

**Link**: [CSES Problem Set - Finding Centroid with Constraints](https://cses.fi/problemset/task/finding_centroid_constraints)

```python
class FindingCentroidWithConstraints:
    def __init__(self, n, edges, min_balance, max_depth):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_sizes = [0] * n
        self.centroid = -1
        self.depths = [0] * n
        self.min_balance = min_balance
        self.max_depth = max_depth
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._find_centroid()
        self._calculate_depths()
    
    def _calculate_subtree_sizes(self, node, parent):
        """Calculate subtree sizes using DFS"""
        self.subtree_sizes[node] = 1
        
        for child in self.adj[node]:
            if child != parent:
                self._calculate_subtree_sizes(child, node)
                self.subtree_sizes[node] += self.subtree_sizes[child]
    
    def _calculate_depths(self):
        """Calculate depth of each node"""
        def dfs(node, parent, depth):
            self.depths[node] = depth
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node, depth + 1)
        
        dfs(0, -1, 0)
    
    def _find_centroid(self):
        """Find centroid of the tree"""
        # Calculate subtree sizes
        self._calculate_subtree_sizes(0, -1)
        
        # Find centroid
        current = 0
        while True:
            found = False
            for child in self.adj[current]:
                if self.subtree_sizes[child] > self.n // 2:
                    current = child
                    found = True
                    break
            
            if not found:
                break
        
        self.centroid = current
    
    def get_centroid(self):
        """Get current centroid of the tree"""
        return self.centroid
    
    def get_centroid_balance(self):
        """Get balance of the centroid"""
        if self.centroid == -1:
            return 0
        
        max_subtree_size = 0
        for child in self.adj[self.centroid]:
            if self.subtree_sizes[child] > max_subtree_size:
                max_subtree_size = self.subtree_sizes[child]
        
        return max_subtree_size / self.n
    
    def constrained_centroid_query(self):
        """Query centroid with constraints"""
        if self.centroid == -1:
            return -1
        
        balance = self.get_centroid_balance()
        depth = self.depths[self.centroid]
        
        # Check if centroid satisfies constraints
        if self.min_balance <= balance <= 0.5 and depth <= self.max_depth:
            return self.centroid
        
        return -1
    
    def find_valid_centroids(self):
        """Find all nodes that could be valid centroids with constraints"""
        valid_centroids = []
        
        for node in range(self.n):
            # Calculate balance for this node
            max_subtree_size = 0
            for child in self.adj[node]:
                if self.subtree_sizes[child] > max_subtree_size:
                    max_subtree_size = self.subtree_sizes[child]
            
            balance = max_subtree_size / self.n
            depth = self.depths[node]
            
            # Check constraints
            if self.min_balance <= balance <= 0.5 and depth <= self.max_depth:
                valid_centroids.append(node)
        
        return valid_centroids
    
    def count_valid_centroids(self):
        """Count number of valid centroids"""
        return len(self.find_valid_centroids())
    
    def get_best_centroid(self):
        """Get best centroid among valid ones (lowest balance)"""
        valid_centroids = self.find_valid_centroids()
        
        if not valid_centroids:
            return -1
        
        best_centroid = valid_centroids[0]
        best_balance = self.get_centroid_balance()
        
        for centroid in valid_centroids:
            # Calculate balance for this centroid
            max_subtree_size = 0
            for child in self.adj[centroid]:
                if self.subtree_sizes[child] > max_subtree_size:
                    max_subtree_size = self.subtree_sizes[child]
            
            balance = max_subtree_size / self.n
            
            if balance < best_balance:
                best_balance = balance
                best_centroid = centroid
        
        return best_centroid
    
    def get_constraint_statistics(self):
        """Get statistics about valid centroids"""
        valid_centroids = self.find_valid_centroids()
        
        if not valid_centroids:
            return {
                'valid_centroids_count': 0,
                'min_balance': self.min_balance,
                'max_depth': self.max_depth,
                'valid_centroids': []
            }
        
        balances = []
        depths = []
        
        for centroid in valid_centroids:
            # Calculate balance for this centroid
            max_subtree_size = 0
            for child in self.adj[centroid]:
                if self.subtree_sizes[child] > max_subtree_size:
                    max_subtree_size = self.subtree_sizes[child]
            
            balance = max_subtree_size / self.n
            balances.append(balance)
            depths.append(self.depths[centroid])
        
        return {
            'valid_centroids_count': len(valid_centroids),
            'min_balance': self.min_balance,
            'max_depth': self.max_depth,
            'min_balance_found': min(balances),
            'max_balance_found': max(balances),
            'min_depth_found': min(depths),
            'max_depth_found': max(depths),
            'valid_centroids': valid_centroids
        }

# Example usage
n = 5
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
min_balance = 0.3
max_depth = 2

fc = FindingCentroidWithConstraints(n, edges, min_balance, max_depth)
result = fc.constrained_centroid_query()
print(f"Constrained centroid query result: {result}")

valid_centroids = fc.find_valid_centroids()
print(f"Valid centroids: {valid_centroids}")

statistics = fc.get_constraint_statistics()
print(f"Constraint statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Finding Centroid](https://cses.fi/problemset/task/2079) - Basic centroid finding in tree
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Find diameter of tree
- [Tree Distances I](https://cses.fi/problemset/task/1132) - Distance queries in tree

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Centroid Decomposition**: Tree decomposition, centroid finding
- **Tree DP**: Dynamic programming on trees, subtree calculations
- **Tree Queries**: Tree analysis, tree operations, tree properties
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
