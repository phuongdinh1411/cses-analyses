---
layout: simple
title: "Company Queries Ii"
permalink: /problem_soulutions/tree_algorithms/company_queries_ii_analysis
---

# Company Queries Ii

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand tree algorithms and tree traversal techniques
- Apply efficient tree processing algorithms
- Implement advanced tree data structures and algorithms
- Optimize tree operations for large inputs
- Handle edge cases in tree problems

## 📋 Problem Description

Given a company hierarchy tree with n employees, process q queries of the form "find the k-th ancestor of employee a".

**Input**: 
- First line: n (number of employees)
- Next n-1 lines: parent-child relationships (parent, child)
- Next line: q (number of queries)
- Next q lines: two integers a and k (employee and ancestor level)

**Output**: 
- q lines: k-th ancestor of employee a (or -1 if doesn't exist)

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 1 ≤ k ≤ n

**Example**:
```
Input:
5
1 2
1 3
2 4
2 5
3
4 1
4 2
4 3

Output:
2
1
-1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, traverse up the tree k levels
2. Follow parent pointers until reaching the k-th ancestor
3. Return the ancestor or -1 if it doesn't exist

**Implementation**:
```python
def brute_force_company_queries_ii(n, edges, queries):
    from collections import defaultdict
    
    # Build parent array
    parent = [0] * (n + 1)
    for u, v in edges:
        parent[v] = u
    
    results = []
    for a, k in queries:
        current = a
        for _ in range(k):
            if current == 0:
                break
            current = parent[current]
        
        if current == 0:
            results.append(-1)
        else:
            results.append(current)
    
    return results
```

**Analysis**:
- **Time**: O(q × n) - For each query, traverse up to n levels
- **Space**: O(n) - Parent array
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Binary Lifting
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute ancestors at powers of 2 using binary lifting
2. For each query, use binary representation of k to find ancestor
3. Jump in powers of 2 to reach the k-th ancestor

**Implementation**:
```python
def optimized_company_queries_ii(n, edges, queries):
    from collections import defaultdict
    
    # Build parent array
    parent = [0] * (n + 1)
    for u, v in edges:
        parent[v] = u
    
    # Binary lifting
    LOG = 20
    up = [[0] * (n + 1) for _ in range(LOG)]
    
    # Initialize first level
    for i in range(1, n + 1):
        up[0][i] = parent[i]
    
    # Fill up the table
    for k in range(1, LOG):
        for i in range(1, n + 1):
            up[k][i] = up[k-1][up[k-1][i]]
    
    def kth_ancestor(node, k):
        current = node
        for i in range(LOG):
            if k & (1 << i):
                current = up[i][current]
                if current == 0:
                    return -1
        return current
    
    results = []
    for a, k in queries:
        ancestor = kth_ancestor(a, k)
        results.append(ancestor)
    
    return results
```

**Analysis**:
- **Time**: O(n log n + q log n) - Preprocessing + query processing
- **Space**: O(n log n) - Binary lifting table
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Binary Lifting
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Use binary lifting to precompute ancestors at powers of 2
2. For each query, decompose k into powers of 2
3. Jump in powers of 2 to reach the k-th ancestor efficiently

**Implementation**:
```python
def optimal_company_queries_ii(n, edges, queries):
    from collections import defaultdict
    
    # Build parent array
    parent = [0] * (n + 1)
    for u, v in edges:
        parent[v] = u
    
    # Binary lifting
    LOG = 20
    up = [[0] * (n + 1) for _ in range(LOG)]
    
    # Initialize first level
    for i in range(1, n + 1):
        up[0][i] = parent[i]
    
    # Fill up the table
    for k in range(1, LOG):
        for i in range(1, n + 1):
            up[k][i] = up[k-1][up[k-1][i]]
    
    def kth_ancestor(node, k):
        current = node
        for i in range(LOG):
            if k & (1 << i):
                current = up[i][current]
                if current == 0:
                    return -1
        return current
    
    results = []
    for a, k in queries:
        ancestor = kth_ancestor(a, k)
        results.append(ancestor)
    
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

Binary Lifting Table:
up[0]: [0, 0, 1, 2, 2, 4]  # 1st ancestors
up[1]: [0, 0, 0, 1, 1, 2]  # 2nd ancestors
up[2]: [0, 0, 0, 0, 0, 1]  # 4th ancestors

Query: Find 3rd ancestor of node 5
k = 3 = 2^1 + 2^0
1. Jump 2^0 = 1 level: 5 → 4
2. Jump 2^1 = 2 levels: 4 → 1
Result: 1
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(n) | Traverse up k levels for each query |
| Optimized | O(n log n + q log n) | O(n log n) | Binary lifting with powers of 2 |
| Optimal | O(n log n + q log n) | O(n log n) | Binary lifting with powers of 2 |

### Time Complexity
- **Time**: O(n log n + q log n) - Preprocessing + query processing with binary lifting
- **Space**: O(n log n) - Binary lifting table

### Why This Solution Works
- **Binary Lifting**: Precompute ancestors at powers of 2 for efficient jumping
- **Binary Representation**: Decompose k into powers of 2 to find ancestor
- **Efficient Queries**: Each query takes O(log n) time instead of O(n)
- **Optimal Approach**: Binary lifting provides the best possible complexity for ancestor queries

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Company Queries II with Dynamic Updates
**Problem**: Handle dynamic updates to the company hierarchy and maintain ancestor queries efficiently.

**Link**: [CSES Problem Set - Company Queries II with Updates](https://cses.fi/problemset/task/company_queries_ii_updates)

```python
class CompanyQueriesIIWithUpdates:
    def __init__(self, n, parent):
        self.n = n
        self.parent = parent[:]
        self.children = [[] for _ in range(n)]
        self.depth = [0] * n
        self.log_n = 20  # Maximum log n for binary lifting
        self.up = [[-1] * self.log_n for _ in range(n)]
        
        # Build children array and calculate depth
        for i in range(1, n):
            self.children[parent[i]].append(i)
        
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def _calculate_depths(self):
        """Calculate depth of each node"""
        def dfs(node, d):
            self.depth[node] = d
            for child in self.children[node]:
                dfs(child, d + 1)
        
        dfs(0, 0)
    
    def _preprocess_binary_lifting(self):
        """Preprocess binary lifting table"""
        # Initialize first level (direct parents)
        for i in range(self.n):
            self.up[i][0] = self.parent[i]
        
        # Fill binary lifting table
        for j in range(1, self.log_n):
            for i in range(self.n):
                if self.up[i][j-1] != -1:
                    self.up[i][j] = self.up[self.up[i][j-1]][j-1]
    
    def update_parent(self, node, new_parent):
        """Update parent of a node and recalculate binary lifting table"""
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
        
        # Recalculate depth and binary lifting table
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def get_kth_ancestor(self, node, k):
        """Get k-th ancestor of a node using binary lifting"""
        if k > self.depth[node]:
            return -1
        
        current = node
        for j in range(self.log_n):
            if k & (1 << j):
                current = self.up[current][j]
                if current == -1:
                    return -1
        
        return current
    
    def get_lca(self, node1, node2):
        """Get lowest common ancestor of two nodes"""
        # Make sure node1 is deeper
        if self.depth[node1] < self.depth[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        diff = self.depth[node1] - self.depth[node2]
        node1 = self.get_kth_ancestor(node1, diff)
        
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
    
    def get_path_to_root(self, node):
        """Get path from node to root"""
        path = []
        current = node
        while current != -1:
            path.append(current)
            current = self.parent[current]
        return path
    
    def get_path_between_nodes(self, node1, node2):
        """Get path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Path from node1 to LCA
        path1 = []
        current = node1
        while current != lca:
            path1.append(current)
            current = self.parent[current]
        
        # Path from node2 to LCA
        path2 = []
        current = node2
        while current != lca:
            path2.append(current)
            current = self.parent[current]
        
        # Combine paths
        return path1 + [lca] + path2[::-1]
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update_parent':
                self.update_parent(query['node'], query['new_parent'])
                results.append(None)
            elif query['type'] == 'kth_ancestor':
                result = self.get_kth_ancestor(query['node'], query['k'])
                results.append(result)
            elif query['type'] == 'lca':
                result = self.get_lca(query['node1'], query['node2'])
                results.append(result)
            elif query['type'] == 'distance':
                result = self.get_distance(query['node1'], query['node2'])
                results.append(result)
            elif query['type'] == 'path_to_root':
                result = self.get_path_to_root(query['node'])
                results.append(result)
            elif query['type'] == 'path_between':
                result = self.get_path_between_nodes(query['node1'], query['node2'])
                results.append(result)
        return results
```

### Variation 2: Company Queries II with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on company hierarchy.

**Link**: [CSES Problem Set - Company Queries II Different Operations](https://cses.fi/problemset/task/company_queries_ii_operations)

```python
class CompanyQueriesIIDifferentOps:
    def __init__(self, n, parent):
        self.n = n
        self.parent = parent[:]
        self.children = [[] for _ in range(n)]
        self.depth = [0] * n
        self.log_n = 20  # Maximum log n for binary lifting
        self.up = [[-1] * self.log_n for _ in range(n)]
        
        # Build children array and calculate depth
        for i in range(1, n):
            self.children[parent[i]].append(i)
        
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def _calculate_depths(self):
        """Calculate depth of each node"""
        def dfs(node, d):
            self.depth[node] = d
            for child in self.children[node]:
                dfs(child, d + 1)
        
        dfs(0, 0)
    
    def _preprocess_binary_lifting(self):
        """Preprocess binary lifting table"""
        # Initialize first level (direct parents)
        for i in range(self.n):
            self.up[i][0] = self.parent[i]
        
        # Fill binary lifting table
        for j in range(1, self.log_n):
            for i in range(self.n):
                if self.up[i][j-1] != -1:
                    self.up[i][j] = self.up[self.up[i][j-1]][j-1]
    
    def get_kth_ancestor(self, node, k):
        """Get k-th ancestor of a node using binary lifting"""
        if k > self.depth[node]:
            return -1
        
        current = node
        for j in range(self.log_n):
            if k & (1 << j):
                current = self.up[current][j]
                if current == -1:
                    return -1
        
        return current
    
    def get_lca(self, node1, node2):
        """Get lowest common ancestor of two nodes"""
        # Make sure node1 is deeper
        if self.depth[node1] < self.depth[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        diff = self.depth[node1] - self.depth[node2]
        node1 = self.get_kth_ancestor(node1, diff)
        
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
    
    def get_ancestors_at_depth(self, node, target_depth):
        """Get all ancestors of a node at specific depth"""
        if target_depth > self.depth[node]:
            return []
        
        k = self.depth[node] - target_depth
        ancestor = self.get_kth_ancestor(node, k)
        return [ancestor] if ancestor != -1 else []
    
    def get_common_ancestors(self, node1, node2):
        """Get all common ancestors of two nodes"""
        lca = self.get_lca(node1, node2)
        if lca == -1:
            return []
        
        # Get all ancestors of LCA
        ancestors = []
        current = lca
        while current != -1:
            ancestors.append(current)
            current = self.parent[current]
        
        return ancestors
    
    def get_nodes_at_same_level(self, node):
        """Get all nodes at the same depth as given node"""
        nodes = []
        target_depth = self.depth[node]
        
        for i in range(self.n):
            if self.depth[i] == target_depth:
                nodes.append(i)
        
        return nodes
    
    def get_subtree_at_depth(self, root, target_depth):
        """Get all nodes in subtree rooted at root at specific depth"""
        if target_depth < self.depth[root]:
            return []
        
        nodes = []
        def dfs(current, current_depth):
            if current_depth == target_depth:
                nodes.append(current)
                return
            
            for child in self.children[current]:
                dfs(child, current_depth + 1)
        
        dfs(root, self.depth[root])
        return nodes
    
    def get_path_length(self, node1, node2):
        """Get length of path between two nodes"""
        return self.get_distance(node1, node2) + 1
    
    def is_ancestor(self, ancestor, descendant):
        """Check if ancestor is ancestor of descendant"""
        if self.depth[ancestor] > self.depth[descendant]:
            return False
        
        k = self.depth[descendant] - self.depth[ancestor]
        return self.get_kth_ancestor(descendant, k) == ancestor
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        max_depth = max(self.depth)
        leaves = sum(1 for i in range(self.n) if len(self.children[i]) == 0)
        
        return {
            'total_nodes': self.n,
            'max_depth': max_depth,
            'leaves': leaves,
            'depths': self.depth.copy()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'kth_ancestor':
                result = self.get_kth_ancestor(query['node'], query['k'])
                results.append(result)
            elif query['type'] == 'lca':
                result = self.get_lca(query['node1'], query['node2'])
                results.append(result)
            elif query['type'] == 'distance':
                result = self.get_distance(query['node1'], query['node2'])
                results.append(result)
            elif query['type'] == 'ancestors_at_depth':
                result = self.get_ancestors_at_depth(query['node'], query['depth'])
                results.append(result)
            elif query['type'] == 'common_ancestors':
                result = self.get_common_ancestors(query['node1'], query['node2'])
                results.append(result)
            elif query['type'] == 'nodes_at_same_level':
                result = self.get_nodes_at_same_level(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_at_depth':
                result = self.get_subtree_at_depth(query['root'], query['depth'])
                results.append(result)
            elif query['type'] == 'path_length':
                result = self.get_path_length(query['node1'], query['node2'])
                results.append(result)
            elif query['type'] == 'is_ancestor':
                result = self.is_ancestor(query['ancestor'], query['descendant'])
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_tree_statistics()
                results.append(result)
        return results
```

### Variation 3: Company Queries II with Constraints
**Problem**: Handle company hierarchy queries with additional constraints (e.g., minimum depth, maximum distance).

**Link**: [CSES Problem Set - Company Queries II with Constraints](https://cses.fi/problemset/task/company_queries_ii_constraints)

```python
class CompanyQueriesIIWithConstraints:
    def __init__(self, n, parent, min_depth, max_distance):
        self.n = n
        self.parent = parent[:]
        self.children = [[] for _ in range(n)]
        self.depth = [0] * n
        self.log_n = 20  # Maximum log n for binary lifting
        self.up = [[-1] * self.log_n for _ in range(n)]
        self.min_depth = min_depth
        self.max_distance = max_distance
        
        # Build children array and calculate depth
        for i in range(1, n):
            self.children[parent[i]].append(i)
        
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def _calculate_depths(self):
        """Calculate depth of each node"""
        def dfs(node, d):
            self.depth[node] = d
            for child in self.children[node]:
                dfs(child, d + 1)
        
        dfs(0, 0)
    
    def _preprocess_binary_lifting(self):
        """Preprocess binary lifting table"""
        # Initialize first level (direct parents)
        for i in range(self.n):
            self.up[i][0] = self.parent[i]
        
        # Fill binary lifting table
        for j in range(1, self.log_n):
            for i in range(self.n):
                if self.up[i][j-1] != -1:
                    self.up[i][j] = self.up[self.up[i][j-1]][j-1]
    
    def get_kth_ancestor(self, node, k):
        """Get k-th ancestor of a node using binary lifting"""
        if k > self.depth[node]:
            return -1
        
        current = node
        for j in range(self.log_n):
            if k & (1 << j):
                current = self.up[current][j]
                if current == -1:
                    return -1
        
        return current
    
    def get_lca(self, node1, node2):
        """Get lowest common ancestor of two nodes"""
        # Make sure node1 is deeper
        if self.depth[node1] < self.depth[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        diff = self.depth[node1] - self.depth[node2]
        node1 = self.get_kth_ancestor(node1, diff)
        
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
    
    def constrained_kth_ancestor_query(self, node, k):
        """Query k-th ancestor with constraints"""
        if self.depth[node] < self.min_depth:
            return -1
        
        ancestor = self.get_kth_ancestor(node, k)
        if ancestor == -1:
            return -1
        
        # Check if ancestor satisfies depth constraint
        if self.depth[ancestor] < self.min_depth:
            return -1
        
        return ancestor
    
    def constrained_lca_query(self, node1, node2):
        """Query LCA with constraints"""
        if (self.depth[node1] < self.min_depth or 
            self.depth[node2] < self.min_depth):
            return -1
        
        lca = self.get_lca(node1, node2)
        if lca == -1:
            return -1
        
        # Check if LCA satisfies depth constraint
        if self.depth[lca] < self.min_depth:
            return -1
        
        return lca
    
    def constrained_distance_query(self, node1, node2):
        """Query distance with constraints"""
        if (self.depth[node1] < self.min_depth or 
            self.depth[node2] < self.min_depth):
            return -1
        
        distance = self.get_distance(node1, node2)
        
        # Check if distance satisfies constraint
        if distance > self.max_distance:
            return -1
        
        return distance
    
    def find_valid_nodes(self):
        """Find all nodes that satisfy depth constraint"""
        valid_nodes = []
        
        for node in range(self.n):
            if self.depth[node] >= self.min_depth:
                valid_nodes.append(node)
        
        return valid_nodes
    
    def get_valid_ancestors(self, node, k):
        """Get valid k-th ancestors"""
        valid_ancestors = []
        
        if self.depth[node] < self.min_depth:
            return valid_ancestors
        
        ancestor = self.get_kth_ancestor(node, k)
        if ancestor != -1 and self.depth[ancestor] >= self.min_depth:
            valid_ancestors.append(ancestor)
        
        return valid_ancestors
    
    def get_valid_pairs(self):
        """Get all valid pairs of nodes within distance constraint"""
        valid_pairs = []
        valid_nodes = self.find_valid_nodes()
        
        for i in range(len(valid_nodes)):
            for j in range(i + 1, len(valid_nodes)):
                node1, node2 = valid_nodes[i], valid_nodes[j]
                distance = self.get_distance(node1, node2)
                
                if distance <= self.max_distance:
                    valid_pairs.append((node1, node2, distance))
        
        return valid_pairs
    
    def count_valid_pairs(self):
        """Count number of valid pairs"""
        return len(self.get_valid_pairs())
    
    def get_constraint_statistics(self):
        """Get statistics about valid nodes and pairs"""
        valid_nodes = self.find_valid_nodes()
        valid_pairs = self.get_valid_pairs()
        
        return {
            'valid_nodes_count': len(valid_nodes),
            'valid_pairs_count': len(valid_pairs),
            'min_depth': self.min_depth,
            'max_distance': self.max_distance,
            'valid_nodes': valid_nodes,
            'valid_pairs': valid_pairs
        }

# Example usage
n = 5
parent = [-1, 0, 0, 1, 1]
min_depth = 1
max_distance = 3

cq = CompanyQueriesIIWithConstraints(n, parent, min_depth, max_distance)
result = cq.constrained_kth_ancestor_query(3, 1)
print(f"Constrained k-th ancestor query result: {result}")

valid_pairs = cq.get_valid_pairs()
print(f"Valid pairs: {valid_pairs}")

statistics = cq.get_constraint_statistics()
print(f"Constraint statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Company Queries II](https://cses.fi/problemset/task/1688) - LCA queries in company hierarchy
- [Company Queries I](https://cses.fi/problemset/task/1687) - Basic company hierarchy queries
- [Distance Queries](https://cses.fi/problemset/task/1135) - Distance queries in tree

#### **LeetCode Problems**
- [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) - Find LCA in binary tree
- [Binary Tree Level Order Traversal II](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree

#### **Problem Categories**
- **Binary Lifting**: Efficient ancestor queries, LCA computation
- **Tree Queries**: Ancestor queries, distance queries, path queries
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
- **Tree Traversal**: DFS, BFS, tree traversal algorithms
