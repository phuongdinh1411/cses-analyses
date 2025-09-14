---
layout: simple
title: "Tree Algorithms Summary"
permalink: /problem_soulutions/tree_algorithms/summary
---

# Tree Algorithms

Welcome to the Tree Algorithms section! This category covers algorithms and techniques for working with tree data structures.

## 🎯 Visual Example

### Tree Algorithm Techniques Overview
```
1. Tree Traversal:
   Tree:    1
          / \
         2   3
        / \
       4   5
   
   DFS: 1 → 2 → 4 → 5 → 3
   BFS: 1 → 2 → 3 → 4 → 5

2. Subtree Operations:
   Subtree of 2: {2, 4, 5}
   Size: 3 nodes
   Sum: 2 + 4 + 5 = 11

3. Path Queries:
   Path 1-4: 1 → 2 → 4
   Distance: 2 edges
   Sum: 1 + 2 + 4 = 7

4. LCA Queries:
   LCA(4,5) = 2
   LCA(2,3) = 1
```

### Algorithm Complexity Comparison
```
Algorithm          | Time    | Space   | Use Case
-------------------|---------|---------|------------------
DFS                | O(n)    | O(h)    | Tree traversal
BFS                | O(n)    | O(w)    | Level traversal
LCA (Binary Lift)  | O(log n)| O(n log n)| Ancestor queries
Euler Tour         | O(n)    | O(n)    | Subtree queries
Tree DP            | O(n)    | O(n)    | Tree optimization
Rerooting          | O(n)    | O(n)    | All-node queries
```

## Key Concepts & Techniques

### Tree Properties & Representation

#### Tree Structure
- **When to use**: Hierarchical data, parent-child relationships
- **Properties**: n nodes, n-1 edges, acyclic, connected
- **Applications**: File systems, organization charts, decision trees
- **Implementation**: Adjacency list or parent array

#### Rooted Trees
- **When to use**: When hierarchy matters, directed relationships
- **Properties**: One root node, directed edges from parent to child
- **Applications**: Family trees, company hierarchies, parse trees
- **Implementation**: Store parent for each node

#### Tree Paths
- **When to use**: Finding connections between nodes
- **Properties**: Unique path between any two nodes
- **Applications**: Network routing, game trees, decision paths
- **Implementation**: DFS or BFS to find path

#### Subtrees
- **When to use**: Operations on tree components
- **Properties**: Connected subgraph containing a node and descendants
- **Applications**: File system operations, tree queries
- **Implementation**: DFS to identify subtree nodes

### Basic Tree Algorithms

#### Depth-First Search (DFS)
- **When to use**: Tree traversal, path finding, subtree operations
- **Time**: O(n) where n is number of nodes
- **Space**: O(h) where h is tree height
- **Applications**: Tree traversal, path finding, subtree size calculation
- **Implementation**: Recursive or iterative with stack

#### Breadth-First Search (BFS)
- **When to use**: Level-order traversal, shortest path in trees
- **Time**: O(n)
- **Space**: O(w) where w is maximum width
- **Applications**: Level-order processing, shortest path
- **Implementation**: Queue-based iterative approach

#### Tree Dynamic Programming
- **When to use**: Optimization problems on trees
- **Time**: O(n) for most problems
- **Space**: O(n)
- **Applications**: Tree matching, tree coloring, tree optimization
- **Implementation**: Post-order traversal with state computation

#### Tree Diameter
- **When to use**: Finding longest path in tree
- **Time**: O(n)
- **Space**: O(n)
- **Applications**: Network analysis, tree metrics
- **Implementation**: Two DFS passes or tree DP

### Advanced Tree Techniques

#### Binary Lifting
- **When to use**: Fast ancestor queries, LCA finding
- **Time**: O(n log n) preprocessing, O(log n) per query
- **Space**: O(n log n)
- **Applications**: LCA queries, k-th ancestor, path queries
- **Implementation**: Precompute 2^i-th ancestors for each node

#### Heavy-Light Decomposition
- **When to use**: Path queries and updates in trees
- **Time**: O(log² n) per query/update
- **Space**: O(n)
- **Applications**: Path sum, path maximum, path updates
- **Implementation**: Decompose tree into heavy chains, use segment trees

#### Euler Tour
- **When to use**: Linear representation of tree, subtree queries
- **Time**: O(n) preprocessing, O(log n) per query
- **Space**: O(n)
- **Applications**: Subtree queries, path queries, tree flattening
- **Implementation**: DFS with entry/exit times

#### Centroid Decomposition
- **When to use**: Tree problems with divide-and-conquer
- **Time**: O(n log n) for decomposition
- **Space**: O(n)
- **Applications**: Tree distances, tree counting, tree optimization
- **Implementation**: Find centroid, solve recursively

### Tree Query Techniques

#### Lowest Common Ancestor (LCA)
- **Binary Lifting Method**: Fast LCA queries
  - *When to use*: Multiple LCA queries
  - *Time*: O(log n) per query
  - *Implementation*: Precompute ancestors, binary search
- **Euler Tour + RMQ**: LCA via range minimum
  - *When to use*: When you need Euler tour anyway
  - *Time*: O(1) per query with sparse table
  - *Implementation*: Euler tour with depth array, RMQ on depths

#### Path Queries
- **Path Sum**: Sum of values on path
  - *When to use*: When you need sum of path values
  - *Time*: O(log n) per query
  - *Implementation*: Use LCA and prefix sums
- **Path Minimum/Maximum**: Min/max on path
  - *When to use*: When you need extremal values on path
  - *Time*: O(log n) per query
  - *Implementation*: Use LCA and sparse table

#### Subtree Queries
- **Subtree Sum**: Sum of subtree values
  - *When to use*: When you need sum of subtree
  - *Time*: O(log n) per query
  - *Implementation*: Use Euler tour with segment tree
- **Subtree Update**: Update all nodes in subtree
  - *When to use*: When you need to update subtree
  - *Time*: O(log n) per update
  - *Implementation*: Use Euler tour with lazy propagation

### Specialized Tree Algorithms

#### Tree Matching
- **Maximum Matching**: Find maximum matching in tree
- **When to use**: Assignment problems, resource allocation
- **Time**: O(n)
- **Space**: O(n)
- **Applications**: Job assignment, resource allocation
- **Implementation**: Greedy algorithm or tree DP

#### Tree Coloring
- **Vertex Coloring**: Color vertices with constraints
- **When to use**: Resource allocation, scheduling
- **Time**: O(n)
- **Space**: O(n)
- **Applications**: Resource allocation, conflict resolution
- **Implementation**: Greedy coloring or tree DP

#### Tree Distances
- **All-Pairs Distances**: Distance between all pairs
- **When to use**: When you need all distances
- **Time**: O(n²)
- **Space**: O(n²)
- **Applications**: Network analysis, graph metrics
- **Implementation**: BFS from each node or tree DP

#### Tree Counting
- **Subtree Counting**: Count subtrees with properties
- **When to use**: When you need to count tree structures
- **Time**: O(n)
- **Space**: O(n)
- **Applications**: Graph enumeration, tree analysis
- **Implementation**: Tree DP with counting

### Tree Data Structures

#### Segment Tree on Trees
- **When to use**: Range queries on tree paths
- **Time**: O(log n) per query/update
- **Space**: O(n)
- **Applications**: Path queries, subtree queries
- **Implementation**: Use Euler tour to linearize tree

#### Fenwick Tree on Trees
- **When to use**: Point updates with range queries on trees
- **Time**: O(log n) per query/update
- **Space**: O(n)
- **Applications**: Point updates, range sums on trees
- **Implementation**: Use Euler tour with Fenwick tree

#### Persistent Data Structures
- **When to use**: Version control, time-travel queries
- **Time**: O(log n) per query/update
- **Space**: O(n log n)
- **Applications**: Version history, temporal queries
- **Implementation**: Create new nodes for each update

### Optimization Techniques

#### Space Optimization
- **In-place Updates**: Modify tree in place
  - *When to use*: When original tree not needed
  - *Example*: In-place tree transformation
- **Lazy Evaluation**: Compute on demand
  - *When to use*: When not all values needed
  - *Example*: Lazy tree construction

#### Time Optimization
- **Precomputation**: Compute values once
  - *When to use*: Multiple queries on same tree
  - *Example*: Precompute LCA for all pairs
- **Caching**: Store computed results
  - *When to use*: Repeated calculations
  - *Example*: Cache subtree sizes

#### Memory Optimization
- **Tree Compression**: Reduce memory usage
  - *When to use*: Large trees with patterns
  - *Example*: Compress repeated subtrees
- **Lazy Allocation**: Allocate memory on demand
  - *When to use*: Sparse trees
  - *Example*: Dynamic tree construction

## Problem Categories

### Basic Tree Operations
- [Subordinates](subordinates_analysis) - Count subtree sizes
- [Tree Matching](tree_matching_analysis) - Maximum matching in tree
- [Tree Diameter](tree_diameter_analysis) - Finding longest path

### Tree Queries
- [Company Queries I](company_queries_i_analysis) - Basic company hierarchy
- [Company Queries II](company_queries_ii_analysis) - LCA queries

### Distance Problems
- [Tree Distances I](tree_distances_i_analysis) - Distance calculation
- [Tree Distances II](tree_distances_ii_analysis) - Advanced distances
- [Distance Queries](distance_queries_analysis) - Path length queries

### Path Problems
- [Path Queries](path_queries_analysis) - Sum queries on paths
- [Path Queries II](path_queries_ii_analysis) - Advanced path operations
- [Counting Paths](counting_paths_analysis) - Count paths with sum

## Detailed Examples and Implementations

### Classic Tree Algorithms with Code

#### 1. Tree Traversal and Basic Operations
```python
class TreeNode:
    def __init__(self, val=0, children=None):
        self.val = val
        self.children = children or []

def dfs_preorder(root):
    """Preorder traversal: Root -> Left -> Right"""
    if not root:
        return []
    
    result = [root.val]
    for child in root.children:
        result.extend(dfs_preorder(child))
    return result

def dfs_postorder(root):
    """Postorder traversal: Left -> Right -> Root"""
    if not root:
        return []
    
    result = []
    for child in root.children:
        result.extend(dfs_postorder(child))
    result.append(root.val)
    return result

def bfs_level_order(root):
    """Level order traversal using BFS"""
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        level_size = len(queue)
        level_values = []
        
        for _ in range(level_size):
            node = queue.pop(0)
            level_values.append(node.val)
            queue.extend(node.children)
        
        result.append(level_values)
    
    return result

def calculate_subtree_sizes(root):
    """Calculate size of each subtree"""
    def dfs(node):
        if not node:
            return 0
        
        size = 1
        for child in node.children:
            size += dfs(child)
        
        node.subtree_size = size
        return size
    
    dfs(root)
    return root

def find_tree_diameter(root):
    """Find diameter of tree (longest path)"""
    def dfs(node):
        if not node:
            return 0, 0  # (height, diameter)
        
        max_height1 = max_height2 = 0
        max_diameter = 0
        
        for child in node.children:
            height, diameter = dfs(child)
            max_diameter = max(max_diameter, diameter)
            
            if height > max_height1:
                max_height2 = max_height1
                max_height1 = height
            elif height > max_height2:
                max_height2 = height
        
        current_diameter = max_height1 + max_height2
        max_diameter = max(max_diameter, current_diameter)
        
        return max_height1 + 1, max_diameter
    
    _, diameter = dfs(root)
    return diameter
```

#### 2. Lowest Common Ancestor (LCA) with Binary Lifting
```python
class LCABinaryLifting:
    def __init__(self, tree, root):
        self.n = len(tree)
        self.log = 0
        while (1 << self.log) <= self.n:
            self.log += 1
        
        self.up = [[-1] * self.n for _ in range(self.log)]
        self.depth = [0] * self.n
        
        self.dfs(root, -1)
        self.precompute()
    
    def dfs(self, node, parent):
        self.up[0][node] = parent
        for child in self.tree[node]:
            if child != parent:
                self.depth[child] = self.depth[node] + 1
                self.dfs(child, node)
    
    def precompute(self):
        for k in range(1, self.log):
            for v in range(self.n):
                if self.up[k-1][v] != -1:
                    self.up[k][v] = self.up[k-1][self.up[k-1][v]]
    
    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        
        # Bring u to same depth as v
        for k in range(self.log - 1, -1, -1):
            if self.depth[u] - (1 << k) >= self.depth[v]:
                u = self.up[k][u]
        
        if u == v:
            return u
        
        # Find LCA
        for k in range(self.log - 1, -1, -1):
            if self.up[k][u] != -1 and self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
        
        return self.up[0][u]
    
    def distance(self, u, v):
        lca_node = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[lca_node]

def lca_euler_tour(tree, root):
    """LCA using Euler Tour + RMQ"""
    euler_tour = []
    first_occurrence = {}
    depth = {}
    
    def dfs(node, parent, d):
        first_occurrence[node] = len(euler_tour)
        depth[node] = d
        euler_tour.append(node)
        
        for child in tree[node]:
            if child != parent:
                dfs(child, node, d + 1)
                euler_tour.append(node)
    
    dfs(root, -1, 0)
    
    # Build sparse table for RMQ
    n = len(euler_tour)
    log = [0] * (n + 1)
    for i in range(2, n + 1):
        log[i] = log[i // 2] + 1
    
    k = log[n] + 1
    st = [[0] * k for _ in range(n)]
    
    for i in range(n):
        st[i][0] = i
    
    for j in range(1, k):
        for i in range(n - (1 << j) + 1):
            if depth[euler_tour[st[i][j-1]]] < depth[euler_tour[st[i + (1 << (j-1))][j-1]]]:
                st[i][j] = st[i][j-1]
            else:
                st[i][j] = st[i + (1 << (j-1))][j-1]
    
    def lca_query(u, v):
        l = first_occurrence[u]
        r = first_occurrence[v]
        if l > r:
            l, r = r, l
        
        k = log[r - l + 1]
        if depth[euler_tour[st[l][k]]] < depth[euler_tour[st[r - (1 << k) + 1][k]]]:
            return euler_tour[st[l][k]]
        else:
            return euler_tour[st[r - (1 << k) + 1][k]]
    
    return lca_query
```

#### 3. Heavy-Light Decomposition
```python
class HeavyLightDecomposition:
    def __init__(self, tree, root):
        self.tree = tree
        self.n = len(tree)
        self.root = root
        
        self.parent = [-1] * self.n
        self.depth = [0] * self.n
        self.size = [0] * self.n
        self.heavy = [-1] * self.n
        self.head = [0] * self.n
        self.pos = [0] * self.n
        
        self.dfs1(root, -1)
        self.dfs2(root, root)
    
    def dfs1(self, node, parent):
        self.parent[node] = parent
        self.size[node] = 1
        self.depth[node] = self.depth[parent] + 1 if parent != -1 else 0
        
        max_size = 0
        for child in self.tree[node]:
            if child != parent:
                child_size = self.dfs1(child, node)
                self.size[node] += child_size
                if child_size > max_size:
                    max_size = child_size
                    self.heavy[node] = child
        
        return self.size[node]
    
    def dfs2(self, node, head):
        self.head[node] = head
        self.pos[node] = self.cur_pos
        self.cur_pos += 1
        
        if self.heavy[node] != -1:
            self.dfs2(self.heavy[node], head)
        
        for child in self.tree[node]:
            if child != self.parent[node] and child != self.heavy[node]:
                self.dfs2(child, child)
    
    def path_query(self, u, v, query_func):
        """Query on path from u to v"""
        result = None
        
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] > self.depth[self.head[v]]:
                u, v = v, u
            
            # Query from head[v] to v
            path_result = query_func(self.pos[self.head[v]], self.pos[v])
            result = self.merge_results(result, path_result)
            
            v = self.parent[self.head[v]]
        
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        
        # Query from u to v
        path_result = query_func(self.pos[u], self.pos[v])
        result = self.merge_results(result, path_result)
        
        return result
    
    def merge_results(self, result1, result2):
        """Merge two query results"""
        if result1 is None:
            return result2
        if result2 is None:
            return result1
        # Implement based on query type (sum, min, max, etc.)
        return result1 + result2  # Example for sum
```

#### 4. Centroid Decomposition
```python
class CentroidDecomposition:
    def __init__(self, tree):
        self.tree = tree
        self.n = len(tree)
        self.centroid_tree = [[] for _ in range(self.n)]
        self.centroid_parent = [-1] * self.n
        self.centroid_root = -1
        
        self.visited = [False] * self.n
        self.size = [0] * self.n
        
        self.centroid_root = self.decompose(0)
    
    def calculate_sizes(self, node, parent):
        self.size[node] = 1
        for child in self.tree[node]:
            if child != parent and not self.visited[child]:
                self.size[node] += self.calculate_sizes(child, node)
        return self.size[node]
    
    def find_centroid(self, node, parent, total_size):
        for child in self.tree[node]:
            if (child != parent and not self.visited[child] and 
                self.size[child] > total_size // 2):
                return self.find_centroid(child, node, total_size)
        return node
    
    def decompose(self, node):
        self.calculate_sizes(node, -1)
        centroid = self.find_centroid(node, -1, self.size[node])
        self.visited[centroid] = True
        
        for child in self.tree[centroid]:
            if not self.visited[child]:
                child_centroid = self.decompose(child)
                self.centroid_tree[centroid].append(child_centroid)
                self.centroid_parent[child_centroid] = centroid
        
        return centroid
    
    def query_distance(self, node, target, max_distance):
        """Query all nodes within max_distance from node"""
        result = []
        current = node
        
        while current != -1:
            distance = self.distance_in_original_tree(current, node)
            if distance <= max_distance:
                result.append(current)
            
            current = self.centroid_parent[current]
        
        return result
    
    def distance_in_original_tree(self, u, v):
        """Calculate distance between u and v in original tree"""
        # This would typically use BFS or other distance calculation
        # Implementation depends on specific requirements
        pass
```

### Advanced Tree Techniques

#### 1. Tree DP (Dynamic Programming on Trees)
```python
def tree_dp_maximum_independent_set(tree, root):
    """Maximum Independent Set on tree"""
    def dfs(node, parent):
        # dp[node][0] = max independent set not including node
        # dp[node][1] = max independent set including node
        dp = [0, 1]  # [not_include, include]
        
        for child in tree[node]:
            if child != parent:
                child_dp = dfs(child, node)
                # If we don't include current node, we can include or not include child
                dp[0] += max(child_dp[0], child_dp[1])
                # If we include current node, we cannot include child
                dp[1] += child_dp[0]
        
        return dp
    
    result = dfs(root, -1)
    return max(result[0], result[1])

def tree_dp_minimum_vertex_cover(tree, root):
    """Minimum Vertex Cover on tree"""
    def dfs(node, parent):
        # dp[node][0] = min vertex cover not including node
        # dp[node][1] = min vertex cover including node
        dp = [0, 1]  # [not_include, include]
        
        for child in tree[node]:
            if child != parent:
                child_dp = dfs(child, node)
                # If we don't include current node, we must include all children
                dp[0] += child_dp[1]
                # If we include current node, we can choose for each child
                dp[1] += min(child_dp[0], child_dp[1])
        
        return dp
    
    result = dfs(root, -1)
    return min(result[0], result[1])

def tree_dp_longest_path(tree, root):
    """Longest path in tree (diameter)"""
    def dfs(node, parent):
        max_depth = 0
        max_path = 0
        
        depths = []
        for child in tree[node]:
            if child != parent:
                child_depth, child_path = dfs(child, node)
                depths.append(child_depth)
                max_path = max(max_path, child_path)
        
        if len(depths) >= 2:
            depths.sort(reverse=True)
            max_path = max(max_path, depths[0] + depths[1])
        elif len(depths) == 1:
            max_path = max(max_path, depths[0])
        
        max_depth = max(depths) + 1 if depths else 1
        return max_depth, max_path
    
    _, max_path = dfs(root, -1)
    return max_path
```

#### 2. Euler Tour and Tree Linearization
```python
class EulerTour:
    def __init__(self, tree, root):
        self.tree = tree
        self.n = len(tree)
        self.euler_tour = []
        self.first_occurrence = {}
        self.last_occurrence = {}
        self.depth = {}
        
        self.build_euler_tour(root, -1, 0)
    
    def build_euler_tour(self, node, parent, d):
        self.first_occurrence[node] = len(self.euler_tour)
        self.depth[node] = d
        self.euler_tour.append(node)
        
        for child in self.tree[node]:
            if child != parent:
                self.build_euler_tour(child, node, d + 1)
                self.euler_tour.append(node)
        
        self.last_occurrence[node] = len(self.euler_tour) - 1
    
    def is_ancestor(self, u, v):
        """Check if u is ancestor of v"""
        return (self.first_occurrence[u] <= self.first_occurrence[v] and
                self.last_occurrence[u] >= self.last_occurrence[v])
    
    def lca(self, u, v):
        """Find LCA using Euler tour"""
        start = min(self.first_occurrence[u], self.first_occurrence[v])
        end = max(self.first_occurrence[u], self.first_occurrence[v])
        
        # Find node with minimum depth in range [start, end]
        min_depth = float('inf')
        lca_node = -1
        
        for i in range(start, end + 1):
            node = self.euler_tour[i]
            if self.depth[node] < min_depth:
                min_depth = self.depth[node]
                lca_node = node
        
        return lca_node
    
    def subtree_range(self, node):
        """Get range of subtree in Euler tour"""
        return (self.first_occurrence[node], self.last_occurrence[node])
```

#### 3. Tree with Segment Tree
```python
class TreeWithSegmentTree:
    def __init__(self, tree, values, root):
        self.tree = tree
        self.values = values
        self.n = len(tree)
        
        # Build Euler tour
        self.euler_tour = EulerTour(tree, root)
        self.tour = self.euler_tour.euler_tour
        self.tour_size = len(self.tour)
        
        # Build segment tree on Euler tour
        self.segment_tree = self.build_segment_tree()
    
    def build_segment_tree(self):
        """Build segment tree for range queries on Euler tour"""
        def build(node, start, end):
            if start == end:
                self.segment_tree[node] = self.values[self.tour[start]]
            else:
                mid = (start + end) // 2
                left = build(2 * node + 1, start, mid)
                right = build(2 * node + 2, mid + 1, end)
                self.segment_tree[node] = left + right  # Sum operation
            return self.segment_tree[node]
        
        self.segment_tree = [0] * (4 * self.tour_size)
        build(0, 0, self.tour_size - 1)
        return self.segment_tree
    
    def update_node(self, node, new_value):
        """Update value of a node"""
        self.values[node] = new_value
        
        # Update all occurrences in Euler tour
        first = self.euler_tour.first_occurrence[node]
        last = self.euler_tour.last_occurrence[node]
        
        for i in range(first, last + 1):
            self.update_segment_tree(0, 0, self.tour_size - 1, i, new_value)
    
    def update_segment_tree(self, node, start, end, index, value):
        if start == end:
            self.segment_tree[node] = value
        else:
            mid = (start + end) // 2
            if index <= mid:
                self.update_segment_tree(2 * node + 1, start, mid, index, value)
            else:
                self.update_segment_tree(2 * node + 2, mid + 1, end, index, value)
            self.segment_tree[node] = (self.segment_tree[2 * node + 1] + 
                                     self.segment_tree[2 * node + 2])
    
    def query_subtree(self, node):
        """Query sum of subtree"""
        first = self.euler_tour.first_occurrence[node]
        last = self.euler_tour.last_occurrence[node]
        return self.query_segment_tree(0, 0, self.tour_size - 1, first, last)
    
    def query_segment_tree(self, node, start, end, left, right):
        if right < start or end < left:
            return 0
        
        if left <= start and end <= right:
            return self.segment_tree[node]
        
        mid = (start + end) // 2
        left_result = self.query_segment_tree(2 * node + 1, start, mid, left, right)
        right_result = self.query_segment_tree(2 * node + 2, mid + 1, end, left, right)
        return left_result + right_result
```

## Tips for Success

1. **Master Tree Traversal**: Foundation for all algorithms
2. **Understand Tree Properties**: Basic concepts
3. **Learn Binary Lifting**: Essential for queries
4. **Practice Implementation**: Code common operations
5. **Study Advanced Techniques**: HLD, centroid decomposition
6. **Handle Edge Cases**: Single nodes, linear trees

## Common Pitfalls to Avoid

1. **Incorrect Traversal**: Missing nodes
2. **Memory Limits**: With large trees
3. **Time Limits**: With inefficient queries
4. **Edge Cases**: Leaf nodes, root handling

## Advanced Topics

### Tree Decomposition
- **Heavy-Light**: Path decomposition
- **Centroid**: Tree partitioning
- **Dynamic Trees**: Link-cut trees
- **Euler Tour**: Linear representation

### Query Optimization
- **Binary Lifting**: Ancestor finding
- **Sparse Table**: Static RMQ
- **Segment Tree**: Dynamic updates
- **Fenwick Tree**: Sum queries

### Special Cases
- **Path Queries**: Sum/min/max on paths
- **Subtree Queries**: Operations on subtrees
- **Distance Queries**: Path length finding
- **Value Queries**: Node value operations

## Algorithm Complexities

### Basic Operations
- **Tree Traversal**: O(n) time
- **Subtree Size**: O(n) preprocessing
- **Tree Diameter**: O(n) time
- **Distance Calculation**: O(n) time

### Advanced Operations
- **LCA Queries**: O(log n) per query
- **Path Queries**: O(log n) per query
- **Distance Queries**: O(log n) per query
- **Value Updates**: O(log n) per update

---

Ready to start? Begin with [Subordinates](subordinates_analysis) and work your way through the problems in order of difficulty!