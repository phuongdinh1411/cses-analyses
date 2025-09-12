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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Company Queries I with Dynamic Updates
**Problem**: Handle dynamic updates to the company hierarchy and maintain subtree size queries efficiently.

**Link**: [CSES Problem Set - Company Queries I with Updates](https://cses.fi/problemset/task/company_queries_i_updates)

```python
class CompanyQueriesIWithUpdates:
    def __init__(self, n, parent):
        self.n = n
        self.parent = parent[:]
        self.children = [[] for _ in range(n)]
        self.subtree_size = [0] * n
        
        # Build children array
        for i in range(1, n):
            self.children[parent[i]].append(i)
        
        self._calculate_subtree_sizes()
    
    def _calculate_subtree_sizes(self):
        """Calculate subtree sizes using DFS"""
        def dfs(node):
            self.subtree_size[node] = 1
            for child in self.children[node]:
                self.subtree_size[node] += dfs(child)
            return self.subtree_size[node]
        
        dfs(0)
    
    def update_parent(self, node, new_parent):
        """Update parent of a node and recalculate affected subtree sizes"""
        if node == 0:  # Root cannot have parent
            return
        
        old_parent = self.parent[node]
        
        # Remove from old parent's children
        if old_parent != -1:
            self.children[old_parent].remove(node)
        
        # Add to new parent's children
        self.parent[node] = new_parent
        if new_parent != -1:
            self.children[new_parent].append(node)
        
        # Recalculate subtree sizes for affected nodes
        self._recalculate_affected_sizes(node, old_parent, new_parent)
    
    def _recalculate_affected_sizes(self, moved_node, old_parent, new_parent):
        """Recalculate subtree sizes for affected nodes"""
        # Update sizes for old parent path
        current = old_parent
        while current != -1:
            self.subtree_size[current] -= self.subtree_size[moved_node]
            current = self.parent[current]
        
        # Update sizes for new parent path
        current = new_parent
        while current != -1:
            self.subtree_size[current] += self.subtree_size[moved_node]
            current = self.parent[current]
    
    def get_subtree_size(self, node):
        """Get subtree size of a node"""
        return self.subtree_size[node]
    
    def get_all_subtree_sizes(self):
        """Get all subtree sizes"""
        return self.subtree_size.copy()
    
    def get_children_count(self, node):
        """Get number of direct children"""
        return len(self.children[node])
    
    def get_descendants_count(self, node):
        """Get total number of descendants (subtree size - 1)"""
        return self.subtree_size[node] - 1
    
    def is_leaf(self, node):
        """Check if node is a leaf"""
        return len(self.children[node]) == 0
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        leaves = sum(1 for i in range(self.n) if self.is_leaf(i))
        max_subtree = max(self.subtree_size)
        min_subtree = min(self.subtree_size)
        
        return {
            'total_nodes': self.n,
            'leaves': leaves,
            'max_subtree_size': max_subtree,
            'min_subtree_size': min_subtree,
            'subtree_sizes': self.subtree_size.copy()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update_parent':
                self.update_parent(query['node'], query['new_parent'])
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

### Variation 2: Company Queries I with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on company hierarchy.

**Link**: [CSES Problem Set - Company Queries I Different Operations](https://cses.fi/problemset/task/company_queries_i_operations)

```python
class CompanyQueriesIDifferentOps:
    def __init__(self, n, parent):
        self.n = n
        self.parent = parent[:]
        self.children = [[] for _ in range(n)]
        self.subtree_size = [0] * n
        self.depth = [0] * n
        
        # Build children array and calculate depth
        for i in range(1, n):
            self.children[parent[i]].append(i)
        
        self._calculate_subtree_sizes()
        self._calculate_depths()
    
    def _calculate_subtree_sizes(self):
        """Calculate subtree sizes using DFS"""
        def dfs(node):
            self.subtree_size[node] = 1
            for child in self.children[node]:
                self.subtree_size[node] += dfs(child)
            return self.subtree_size[node]
        
        dfs(0)
    
    def _calculate_depths(self):
        """Calculate depth of each node"""
        def dfs(node, d):
            self.depth[node] = d
            for child in self.children[node]:
                dfs(child, d + 1)
        
        dfs(0, 0)
    
    def get_subtree_size(self, node):
        """Get subtree size of a node"""
        return self.subtree_size[node]
    
    def get_depth(self, node):
        """Get depth of a node"""
        return self.depth[node]
    
    def get_height(self, node):
        """Get height of subtree rooted at node"""
        if self.is_leaf(node):
            return 0
        
        max_child_height = 0
        for child in self.children[node]:
            max_child_height = max(max_child_height, self.get_height(child))
        
        return max_child_height + 1
    
    def get_ancestors(self, node):
        """Get all ancestors of a node"""
        ancestors = []
        current = self.parent[node]
        while current != -1:
            ancestors.append(current)
            current = self.parent[current]
        return ancestors
    
    def get_descendants(self, node):
        """Get all descendants of a node"""
        descendants = []
        def dfs(current):
            for child in self.children[current]:
                descendants.append(child)
                dfs(child)
        dfs(node)
        return descendants
    
    def get_siblings(self, node):
        """Get all siblings of a node"""
        if node == 0:  # Root has no siblings
            return []
        
        parent = self.parent[node]
        siblings = []
        for child in self.children[parent]:
            if child != node:
                siblings.append(child)
        return siblings
    
    def get_cousins(self, node):
        """Get all cousins of a node (nodes at same depth)"""
        cousins = []
        node_depth = self.depth[node]
        
        for i in range(self.n):
            if i != node and self.depth[i] == node_depth:
                # Check if they have different parents
                if self.parent[i] != self.parent[node]:
                    cousins.append(i)
        
        return cousins
    
    def find_common_ancestor(self, node1, node2):
        """Find lowest common ancestor of two nodes"""
        # Get ancestors of both nodes
        ancestors1 = set(self.get_ancestors(node1))
        ancestors1.add(node1)
        
        ancestors2 = set(self.get_ancestors(node2))
        ancestors2.add(node2)
        
        # Find common ancestors
        common = ancestors1.intersection(ancestors2)
        
        # Return the one with maximum depth
        if not common:
            return -1
        
        return max(common, key=lambda x: self.depth[x])
    
    def get_distance(self, node1, node2):
        """Get distance between two nodes"""
        lca = self.find_common_ancestor(node1, node2)
        if lca == -1:
            return -1
        
        return self.depth[node1] + self.depth[node2] - 2 * self.depth[lca]
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        leaves = sum(1 for i in range(self.n) if self.is_leaf(i))
        max_depth = max(self.depth)
        max_subtree = max(self.subtree_size)
        
        return {
            'total_nodes': self.n,
            'leaves': leaves,
            'max_depth': max_depth,
            'max_subtree_size': max_subtree,
            'subtree_sizes': self.subtree_size.copy(),
            'depths': self.depth.copy()
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
            elif query['type'] == 'height':
                result = self.get_height(query['node'])
                results.append(result)
            elif query['type'] == 'ancestors':
                result = self.get_ancestors(query['node'])
                results.append(result)
            elif query['type'] == 'descendants':
                result = self.get_descendants(query['node'])
                results.append(result)
            elif query['type'] == 'siblings':
                result = self.get_siblings(query['node'])
                results.append(result)
            elif query['type'] == 'cousins':
                result = self.get_cousins(query['node'])
                results.append(result)
            elif query['type'] == 'common_ancestor':
                result = self.find_common_ancestor(query['node1'], query['node2'])
                results.append(result)
            elif query['type'] == 'distance':
                result = self.get_distance(query['node1'], query['node2'])
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_tree_statistics()
                results.append(result)
        return results
```

### Variation 3: Company Queries I with Constraints
**Problem**: Handle company hierarchy queries with additional constraints (e.g., minimum depth, maximum subtree size).

**Link**: [CSES Problem Set - Company Queries I with Constraints](https://cses.fi/problemset/task/company_queries_i_constraints)

```python
class CompanyQueriesIWithConstraints:
    def __init__(self, n, parent, min_depth, max_subtree_size):
        self.n = n
        self.parent = parent[:]
        self.children = [[] for _ in range(n)]
        self.subtree_size = [0] * n
        self.depth = [0] * n
        self.min_depth = min_depth
        self.max_subtree_size = max_subtree_size
        
        # Build children array and calculate depth
        for i in range(1, n):
            self.children[parent[i]].append(i)
        
        self._calculate_subtree_sizes()
        self._calculate_depths()
    
    def _calculate_subtree_sizes(self):
        """Calculate subtree sizes using DFS"""
        def dfs(node):
            self.subtree_size[node] = 1
            for child in self.children[node]:
                self.subtree_size[node] += dfs(child)
            return self.subtree_size[node]
        
        dfs(0)
    
    def _calculate_depths(self):
        """Calculate depth of each node"""
        def dfs(node, d):
            self.depth[node] = d
            for child in self.children[node]:
                dfs(child, d + 1)
        
        dfs(0, 0)
    
    def constrained_subtree_size_query(self, node):
        """Query subtree size with constraints"""
        if self.depth[node] < self.min_depth:
            return 0
        
        if self.subtree_size[node] > self.max_subtree_size:
            return 0
        
        return self.subtree_size[node]
    
    def find_valid_nodes(self):
        """Find all nodes that satisfy constraints"""
        valid_nodes = []
        
        for node in range(self.n):
            if (self.depth[node] >= self.min_depth and 
                self.subtree_size[node] <= self.max_subtree_size):
                valid_nodes.append(node)
        
        return valid_nodes
    
    def get_valid_subtree_sizes(self):
        """Get subtree sizes of all valid nodes"""
        valid_nodes = self.find_valid_nodes()
        return [(node, self.subtree_size[node]) for node in valid_nodes]
    
    def count_valid_nodes(self):
        """Count number of valid nodes"""
        return len(self.find_valid_nodes())
    
    def get_largest_valid_subtree(self):
        """Get node with largest valid subtree size"""
        valid_nodes = self.find_valid_nodes()
        
        if not valid_nodes:
            return -1, 0
        
        max_node = max(valid_nodes, key=lambda x: self.subtree_size[x])
        return max_node, self.subtree_size[max_node]
    
    def get_smallest_valid_subtree(self):
        """Get node with smallest valid subtree size"""
        valid_nodes = self.find_valid_nodes()
        
        if not valid_nodes:
            return -1, 0
        
        min_node = min(valid_nodes, key=lambda x: self.subtree_size[x])
        return min_node, self.subtree_size[min_node]
    
    def get_valid_nodes_by_depth(self, target_depth):
        """Get all valid nodes at specific depth"""
        valid_nodes = []
        
        for node in range(self.n):
            if (self.depth[node] == target_depth and 
                self.subtree_size[node] <= self.max_subtree_size):
                valid_nodes.append(node)
        
        return valid_nodes
    
    def get_valid_nodes_by_subtree_size(self, min_size, max_size):
        """Get all valid nodes with subtree size in range"""
        valid_nodes = []
        
        for node in range(self.n):
            if (self.depth[node] >= self.min_depth and 
                min_size <= self.subtree_size[node] <= max_size):
                valid_nodes.append(node)
        
        return valid_nodes
    
    def get_constraint_statistics(self):
        """Get statistics about valid nodes"""
        valid_nodes = self.find_valid_nodes()
        
        if not valid_nodes:
            return {
                'count': 0,
                'min_subtree_size': 0,
                'max_subtree_size': 0,
                'avg_subtree_size': 0,
                'min_depth': 0,
                'max_depth': 0
            }
        
        subtree_sizes = [self.subtree_size[node] for node in valid_nodes]
        depths = [self.depth[node] for node in valid_nodes]
        
        return {
            'count': len(valid_nodes),
            'min_subtree_size': min(subtree_sizes),
            'max_subtree_size': max(subtree_sizes),
            'avg_subtree_size': sum(subtree_sizes) / len(subtree_sizes),
            'min_depth': min(depths),
            'max_depth': max(depths)
        }

# Example usage
n = 5
parent = [-1, 0, 0, 1, 1]
min_depth = 1
max_subtree_size = 3

cq = CompanyQueriesIWithConstraints(n, parent, min_depth, max_subtree_size)
result = cq.constrained_subtree_size_query(1)
print(f"Constrained subtree size query result: {result}")

valid_nodes = cq.find_valid_nodes()
print(f"Valid nodes: {valid_nodes}")

largest_subtree = cq.get_largest_valid_subtree()
print(f"Largest valid subtree: {largest_subtree}")
```

### Related Problems

#### **CSES Problems**
- [Company Queries I](https://cses.fi/problemset/task/1687) - Basic company hierarchy queries
- [Company Queries II](https://cses.fi/problemset/task/1688) - LCA queries in company hierarchy
- [Subordinates](https://cses.fi/problemset/task/1674) - Count subordinates in company hierarchy

#### **LeetCode Problems**
- [Count Complete Tree Nodes](https://leetcode.com/problems/count-complete-tree-nodes/) - Count nodes in complete binary tree
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) - Find maximum depth of tree

#### **Problem Categories**
- **Tree DP**: Dynamic programming on trees, subtree calculations
- **Tree Traversal**: DFS, BFS, tree traversal algorithms
- **Tree Queries**: Subtree queries, tree statistics, hierarchy queries
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
