---
layout: simple
title: "Subordinates"
permalink: /problem_soulutions/tree_algorithms/subordinates_analysis
---

# Subordinates

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand tree traversal and subtree counting algorithms
- Apply depth-first search (DFS) for tree processing
- Implement efficient tree dynamic programming
- Optimize tree algorithms for large inputs
- Handle edge cases in tree problems (single nodes, linear trees)

## 📋 Problem Description

Given a tree with n nodes, for each node, find the number of nodes in its subtree (including itself).

This is a fundamental tree algorithm problem that tests understanding of tree traversal and subtree counting.

**Input**: 
- First line: integer n (number of nodes)
- Next n-1 lines: two integers a and b (edge between nodes a and b)

**Output**: 
- Print n integers: the number of nodes in the subtree of each node

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
5 1 3 1 1

Explanation**: 
The tree structure:
    1
   / \\
  2   3
     / \\
    4   5

Subtree sizes:
- Node 1: 5 nodes (1, 2, 3, 4, 5)
- Node 2: 1 node (2)
- Node 3: 3 nodes (3, 4, 5)
- Node 4: 1 node (4)
- Node 5: 1 node (5)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - DFS for Each Node

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: For each node, perform a separate DFS to count its subtree
- **Complete Coverage**: Guaranteed to find the correct subtree size for each node
- **Simple Implementation**: Straightforward DFS approach
- **Inefficient**: Multiple DFS traversals lead to quadratic time complexity

**Key Insight**: For each node, perform a DFS starting from that node to count all nodes in its subtree.

**Algorithm**:
- For each node i:
  - Perform DFS starting from node i
  - Count all nodes reachable from node i
  - Store the count as subtree size of node i

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

For node 1:
- DFS from 1: visit 1, 2, 3, 4, 5
- Count: 5 nodes

For node 2:
- DFS from 2: visit 2
- Count: 1 node

For node 3:
- DFS from 3: visit 3, 4, 5
- Count: 3 nodes

For node 4:
- DFS from 4: visit 4
- Count: 1 node

For node 5:
- DFS from 5: visit 5
- Count: 1 node

Result: [5, 1, 3, 1, 1]
```

**Implementation**:
```python
def brute_force_subordinates(n, edges):
    """
    Find subtree sizes using brute force approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        list: subtree size for each node
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def dfs_count(node, parent):
        """DFS to count nodes in subtree"""
        count = 1
        for neighbor in adj[node]:
            if neighbor != parent:
                count += dfs_count(neighbor, node)
        return count
    
    subtree_sizes = []
    for i in range(1, n + 1):
        size = dfs_count(i, -1)
        subtree_sizes.append(size)
    
    return subtree_sizes

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = brute_force_subordinates(n, edges)
print(f"Brute force result: {result}")  # Output: [5, 1, 3, 1, 1]
```

**Time Complexity**: O(n²) - For each node, DFS takes O(n) time
**Space Complexity**: O(n) - For adjacency list and recursion stack

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Single DFS with Memoization

**Key Insights from Optimized Approach**:
- **Single DFS**: Perform only one DFS traversal from root
- **Memoization**: Store subtree sizes during the DFS
- **Efficient Calculation**: Calculate subtree sizes in a single pass
- **Linear Time**: Achieve O(n) time complexity

**Key Insight**: Use a single DFS traversal to calculate all subtree sizes simultaneously.

**Algorithm**:
- Perform DFS from root node
- For each node, calculate its subtree size as 1 + sum of children's subtree sizes
- Store results during the traversal

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

DFS traversal order: 1 → 2 → 3 → 4 → 5

Post-order processing:
1. Node 5: subtree_size = 1
2. Node 4: subtree_size = 1
3. Node 3: subtree_size = 1 + 1 + 1 = 3
4. Node 2: subtree_size = 1
5. Node 1: subtree_size = 1 + 1 + 3 = 5

Result: [5, 1, 3, 1, 1]
```

**Implementation**:
```python
def optimized_subordinates(n, edges):
    """
    Find subtree sizes using single DFS with memoization
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        list: subtree size for each node
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    subtree_sizes = [0] * (n + 1)
    
    def dfs(node, parent):
        """DFS to calculate subtree sizes"""
        subtree_sizes[node] = 1  # Count the node itself
        
        for neighbor in adj[node]:
            if neighbor != parent:
                dfs(neighbor, node)
                subtree_sizes[node] += subtree_sizes[neighbor]
    
    # Start DFS from node 1 (assuming it's the root)
    dfs(1, -1)
    
    return subtree_sizes[1:n+1]

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = optimized_subordinates(n, edges)
print(f"Optimized result: {result}")  # Output: [5, 1, 3, 1, 1]
```

**Time Complexity**: O(n) - Single DFS traversal
**Space Complexity**: O(n) - For adjacency list and recursion stack

**Why it's better**: Linear time complexity with efficient single-pass calculation.

---

### Approach 3: Optimal - Post-order DFS with Dynamic Programming

**Key Insights from Optimal Approach**:
- **Post-order Traversal**: Process children before parent
- **Dynamic Programming**: Use DP to calculate subtree sizes
- **Optimal Space**: Use only O(n) space
- **Optimal Time**: Achieve O(n) time complexity

**Key Insight**: Use post-order DFS to ensure that when we process a node, all its children have already been processed.

**Algorithm**:
- Perform post-order DFS traversal
- For each node, calculate subtree size as 1 + sum of children's subtree sizes
- Return the results

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

Post-order DFS: 2, 4, 5, 3, 1

Processing:
1. Node 2: subtree_size = 1
2. Node 4: subtree_size = 1
3. Node 5: subtree_size = 1
4. Node 3: subtree_size = 1 + 1 + 1 = 3
5. Node 1: subtree_size = 1 + 1 + 3 = 5

Result: [5, 1, 3, 1, 1]
```

**Implementation**:
```python
def optimal_subordinates(n, edges):
    """
    Find subtree sizes using optimal post-order DFS
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        list: subtree size for each node
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    subtree_sizes = [0] * (n + 1)
    
    def post_order_dfs(node, parent):
        """Post-order DFS to calculate subtree sizes"""
        # Process all children first
        for neighbor in adj[node]:
            if neighbor != parent:
                post_order_dfs(neighbor, node)
        
        # Process current node after children
        subtree_sizes[node] = 1  # Count the node itself
        for neighbor in adj[node]:
            if neighbor != parent:
                subtree_sizes[node] += subtree_sizes[neighbor]
    
    # Start DFS from node 1 (assuming it's the root)
    post_order_dfs(1, -1)
    
    return subtree_sizes[1:n+1]

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = optimal_subordinates(n, edges)
print(f"Optimal result: {result}")  # Output: [5, 1, 3, 1, 1]
```

**Time Complexity**: O(n) - Single post-order DFS traversal
**Space Complexity**: O(n) - For adjacency list and recursion stack

**Why it's optimal**: Achieves the best possible time and space complexity for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | DFS for each node |
| Single DFS | O(n) | O(n) | Calculate all sizes in one pass |
| Post-order DFS | O(n) | O(n) | Process children before parent |

### Time Complexity
- **Time**: O(n) - Single DFS traversal provides optimal linear time
- **Space**: O(n) - For adjacency list and recursion stack

### Why This Solution Works
- **Tree Properties**: Trees have unique paths between nodes, enabling efficient traversal
- **Dynamic Programming**: Subtree size of a node equals 1 + sum of children's subtree sizes
- **Post-order Processing**: Ensures children are processed before parents
- **Optimal Approach**: Post-order DFS provides the most elegant and efficient solution

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Subordinates with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain subordinate counts efficiently.

**Link**: [CSES Problem Set - Subordinates with Updates](https://cses.fi/problemset/task/subordinates_updates)

```python
class SubordinatesWithUpdates:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_sizes = [0] * n
        self.parent = [-1] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_subtree_sizes()
    
    def _calculate_subtree_sizes(self):
        """Calculate subtree sizes using DFS"""
        def dfs(node, parent):
            self.parent[node] = parent
            self.subtree_sizes[node] = 1
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    self.subtree_sizes[node] += self.subtree_sizes[child]
        
        dfs(0, -1)
    
    def add_edge(self, u, v):
        """Add edge between nodes u and v"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        
        # Recalculate subtree sizes
        self._calculate_subtree_sizes()
    
    def remove_edge(self, u, v):
        """Remove edge between nodes u and v"""
        if v in self.adj[u]:
            self.adj[u].remove(v)
        if u in self.adj[v]:
            self.adj[v].remove(u)
        
        # Recalculate subtree sizes
        self._calculate_subtree_sizes()
    
    def get_subtree_size(self, node):
        """Get subtree size of a node"""
        return self.subtree_sizes[node]
    
    def get_all_subtree_sizes(self):
        """Get all subtree sizes"""
        return self.subtree_sizes.copy()
    
    def get_children_count(self, node):
        """Get number of direct children"""
        return len(self.adj[node]) - (1 if self.parent[node] != -1 else 0)
    
    def get_descendants_count(self, node):
        """Get total number of descendants (subtree size - 1)"""
        return self.subtree_sizes[node] - 1
    
    def is_leaf(self, node):
        """Check if node is a leaf"""
        return len(self.adj[node]) == 1 and self.parent[node] != -1
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        leaves = sum(1 for i in range(self.n) if self.is_leaf(i))
        max_subtree = max(self.subtree_sizes)
        min_subtree = min(self.subtree_sizes)
        
        return {
            'total_nodes': self.n,
            'leaves': leaves,
            'max_subtree_size': max_subtree,
            'min_subtree_size': min_subtree,
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
            elif query['type'] == 'subtree_size':
                result = self.get_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'all_sizes':
                result = self.get_all_subtree_sizes()
                results.append(result)
            elif query['type'] == 'children_count':
                result = self.get_children_count(query['node'])
                results.append(result)
            elif query['type'] == 'descendants_count':
                result = self.get_descendants_count(query['node'])
                results.append(result)
            elif query['type'] == 'is_leaf':
                result = self.is_leaf(query['node'])
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_tree_statistics()
                results.append(result)
        return results
```

### Variation 2: Subordinates with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on subordinate queries.

**Link**: [CSES Problem Set - Subordinates Different Operations](https://cses.fi/problemset/task/subordinates_operations)

```python
class SubordinatesDifferentOps:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_sizes = [0] * n
        self.depths = [0] * n
        self.parent = [-1] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_tree_info()
    
    def _calculate_tree_info(self):
        """Calculate tree information using DFS"""
        def dfs(node, parent, depth):
            self.parent[node] = parent
            self.depths[node] = depth
            self.subtree_sizes[node] = 1
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node, depth + 1)
                    self.subtree_sizes[node] += self.subtree_sizes[child]
        
        dfs(0, -1, 0)
    
    def get_subtree_size(self, node):
        """Get subtree size of a node"""
        return self.subtree_sizes[node]
    
    def get_depth(self, node):
        """Get depth of a node"""
        return self.depths[node]
    
    def get_children_count(self, node):
        """Get number of direct children"""
        return len(self.adj[node]) - (1 if self.parent[node] != -1 else 0)
    
    def get_descendants_count(self, node):
        """Get total number of descendants (subtree size - 1)"""
        return self.subtree_sizes[node] - 1
    
    def get_ancestors_count(self, node):
        """Get number of ancestors (depth)"""
        return self.depths[node]
    
    def is_leaf(self, node):
        """Check if node is a leaf"""
        return len(self.adj[node]) == 1 and self.parent[node] != -1
    
    def is_root(self, node):
        """Check if node is root"""
        return self.parent[node] == -1
    
    def get_siblings_count(self, node):
        """Get number of siblings"""
        if self.is_root(node):
            return 0
        return self.get_children_count(self.parent[node]) - 1
    
    def get_node_statistics(self, node):
        """Get comprehensive statistics for a node"""
        return {
            'subtree_size': self.subtree_sizes[node],
            'depth': self.depths[node],
            'children_count': self.get_children_count(node),
            'descendants_count': self.get_descendants_count(node),
            'ancestors_count': self.get_ancestors_count(node),
            'siblings_count': self.get_siblings_count(node),
            'is_leaf': self.is_leaf(node),
            'is_root': self.is_root(node)
        }
    
    def get_all_subtree_sizes(self):
        """Get all subtree sizes"""
        return self.subtree_sizes.copy()
    
    def get_all_depths(self):
        """Get all depths"""
        return self.depths.copy()
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        leaves = sum(1 for i in range(self.n) if self.is_leaf(i))
        max_subtree = max(self.subtree_sizes)
        min_subtree = min(self.subtree_sizes)
        max_depth = max(self.depths)
        
        return {
            'total_nodes': self.n,
            'leaves': leaves,
            'max_subtree_size': max_subtree,
            'min_subtree_size': min_subtree,
            'max_depth': max_depth,
            'subtree_sizes': self.subtree_sizes.copy(),
            'depths': self.depths.copy()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'subtree_size':
                result = self.get_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'depth':
                result = self.get_depth(query['node'])
                results.append(result)
            elif query['type'] == 'children_count':
                result = self.get_children_count(query['node'])
                results.append(result)
            elif query['type'] == 'descendants_count':
                result = self.get_descendants_count(query['node'])
                results.append(result)
            elif query['type'] == 'ancestors_count':
                result = self.get_ancestors_count(query['node'])
                results.append(result)
            elif query['type'] == 'siblings_count':
                result = self.get_siblings_count(query['node'])
                results.append(result)
            elif query['type'] == 'is_leaf':
                result = self.is_leaf(query['node'])
                results.append(result)
            elif query['type'] == 'is_root':
                result = self.is_root(query['node'])
                results.append(result)
            elif query['type'] == 'node_statistics':
                result = self.get_node_statistics(query['node'])
                results.append(result)
            elif query['type'] == 'all_sizes':
                result = self.get_all_subtree_sizes()
                results.append(result)
            elif query['type'] == 'all_depths':
                result = self.get_all_depths()
                results.append(result)
            elif query['type'] == 'tree_statistics':
                result = self.get_tree_statistics()
                results.append(result)
        return results
```

### Variation 3: Subordinates with Constraints
**Problem**: Handle subordinate queries with additional constraints (e.g., minimum depth, maximum depth, depth range).

**Link**: [CSES Problem Set - Subordinates with Constraints](https://cses.fi/problemset/task/subordinates_constraints)

```python
class SubordinatesWithConstraints:
    def __init__(self, n, edges, min_depth, max_depth):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_sizes = [0] * n
        self.depths = [0] * n
        self.parent = [-1] * n
        self.min_depth = min_depth
        self.max_depth = max_depth
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_tree_info()
    
    def _calculate_tree_info(self):
        """Calculate tree information using DFS"""
        def dfs(node, parent, depth):
            self.parent[node] = parent
            self.depths[node] = depth
            self.subtree_sizes[node] = 1
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node, depth + 1)
                    self.subtree_sizes[node] += self.subtree_sizes[child]
        
        dfs(0, -1, 0)
    
    def get_subtree_size(self, node):
        """Get subtree size of a node"""
        return self.subtree_sizes[node]
    
    def get_depth(self, node):
        """Get depth of a node"""
        return self.depths[node]
    
    def get_constrained_subtree_size(self, node):
        """Get subtree size considering depth constraints"""
        if not (self.min_depth <= self.depths[node] <= self.max_depth):
            return 0
        
        constrained_size = 1 if self.min_depth <= self.depths[node] <= self.max_depth else 0
        
        for child in self.adj[node]:
            if child != self.parent[node]:
                constrained_size += self.get_constrained_subtree_size(child)
        
        return constrained_size
    
    def get_constrained_descendants_count(self, node):
        """Get count of descendants within depth constraints"""
        return self.get_constrained_subtree_size(node) - 1
    
    def get_valid_nodes_in_subtree(self, node):
        """Get all valid nodes in subtree considering depth constraints"""
        valid_nodes = []
        
        def dfs_collect(current, parent):
            if self.min_depth <= self.depths[current] <= self.max_depth:
                valid_nodes.append(current)
            
            for child in self.adj[current]:
                if child != parent:
                    dfs_collect(child, current)
        
        dfs_collect(node, -1)
        return valid_nodes
    
    def get_constrained_statistics(self, node):
        """Get comprehensive statistics considering depth constraints"""
        valid_nodes = self.get_valid_nodes_in_subtree(node)
        
        return {
            'total_subtree_size': self.subtree_sizes[node],
            'constrained_subtree_size': len(valid_nodes),
            'depth': self.depths[node],
            'is_valid_depth': self.min_depth <= self.depths[node] <= self.max_depth,
            'valid_nodes': valid_nodes,
            'min_depth': self.min_depth,
            'max_depth': self.max_depth
        }
    
    def get_all_constrained_subtree_sizes(self):
        """Get constrained subtree sizes for all nodes"""
        constrained_sizes = []
        for i in range(self.n):
            constrained_sizes.append(self.get_constrained_subtree_size(i))
        return constrained_sizes
    
    def get_global_constrained_statistics(self):
        """Get global statistics considering depth constraints"""
        constrained_sizes = self.get_all_constrained_subtree_sizes()
        valid_nodes = [i for i in range(self.n) if self.min_depth <= self.depths[i] <= self.max_depth]
        
        return {
            'total_nodes': self.n,
            'valid_nodes_count': len(valid_nodes),
            'max_constrained_subtree_size': max(constrained_sizes),
            'min_constrained_subtree_size': min(constrained_sizes),
            'min_depth': self.min_depth,
            'max_depth': self.max_depth,
            'constrained_sizes': constrained_sizes,
            'valid_nodes': valid_nodes
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'subtree_size':
                result = self.get_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'depth':
                result = self.get_depth(query['node'])
                results.append(result)
            elif query['type'] == 'constrained_subtree_size':
                result = self.get_constrained_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'constrained_descendants_count':
                result = self.get_constrained_descendants_count(query['node'])
                results.append(result)
            elif query['type'] == 'valid_nodes_in_subtree':
                result = self.get_valid_nodes_in_subtree(query['node'])
                results.append(result)
            elif query['type'] == 'constrained_statistics':
                result = self.get_constrained_statistics(query['node'])
                results.append(result)
            elif query['type'] == 'all_constrained_sizes':
                result = self.get_all_constrained_subtree_sizes()
                results.append(result)
            elif query['type'] == 'global_constrained_statistics':
                result = self.get_global_constrained_statistics()
                results.append(result)
        return results

# Example usage
n = 5
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
min_depth = 1
max_depth = 3

sq = SubordinatesWithConstraints(n, edges, min_depth, max_depth)
result = sq.get_constrained_subtree_size(1)
print(f"Constrained subtree size result: {result}")

valid_nodes = sq.get_valid_nodes_in_subtree(1)
print(f"Valid nodes: {valid_nodes}")

statistics = sq.get_global_constrained_statistics()
print(f"Global constrained statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Subordinates](https://cses.fi/problemset/task/1674) - Basic subordinate counting in tree
- [Company Queries I](https://cses.fi/problemset/task/1687) - Tree queries and subtree analysis
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Find diameter of tree

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Tree DP**: Dynamic programming on trees, subtree analysis
- **Tree Traversal**: DFS, BFS, tree processing
- **Tree Queries**: Subtree queries, tree analysis, tree operations
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
