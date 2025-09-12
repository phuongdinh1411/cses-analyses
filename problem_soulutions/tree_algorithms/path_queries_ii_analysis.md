---
layout: simple
title: "Path Queries Ii"
permalink: /problem_soulutions/tree_algorithms/path_queries_ii_analysis
---

# Path Queries Ii

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

Given a tree with n nodes, each node has a value. Process q queries of the form "find the minimum value on the path from node a to node b".

**Input**: 
- First line: n (number of nodes)
- Next n lines: values of nodes 1 to n
- Next n-1 lines: edges of the tree
- Next line: q (number of queries)
- Next q lines: two integers a and b (path endpoints)

**Output**: 
- q lines: minimum value on the path from a to b

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 1 ≤ value ≤ 10⁹

**Example**:
```
Input:
5
1 2 3 4 5
1 2
2 3
2 4
4 5
3
1 3
2 5
1 5

Output:
1
2
1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, find the path from a to b using DFS
2. Find the minimum value along the path
3. Return the minimum for each query

**Implementation**:
```python
def brute_force_path_queries_ii(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def find_path(a, b):
        # Find path from a to b using DFS
        path = []
        visited = set()
        
        def dfs(node, target, current_path):
            if node == target:
                return current_path + [node]
            
            visited.add(node)
            for child in graph[node]:
                if child not in visited:
                    result = dfs(child, target, current_path + [node])
                    if result:
                        return result
            return None
        
        return dfs(a, b, [])
    
    results = []
    for a, b in queries:
        path = find_path(a, b)
        min_value = min(values[node - 1] for node in path)
        results.append(min_value)
    
    return results
```

**Analysis**:
- **Time**: O(q × n) - For each query, DFS takes O(n) time
- **Space**: O(n) - Recursion stack and path storage
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with LCA
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute LCA using binary lifting
2. For each query, find LCA of a and b
3. Find minimum value from a to LCA and from b to LCA

**Implementation**:
```python
def optimized_path_queries_ii(n, values, edges, queries):
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
    min_path = [[float('inf')] * (n + 1) for _ in range(LOG)]
    
    def dfs(node, parent):
        up[0][node] = parent
        min_path[0][node] = values[node - 1]
        depth[node] = depth[parent] + 1
        
        for child in graph[node]:
            if child != parent:
                dfs(child, node)
    
    dfs(1, 0)
    
    # Binary lifting
    for k in range(1, LOG):
        for node in range(1, n + 1):
            up[k][node] = up[k-1][up[k-1][node]]
            min_path[k][node] = min(min_path[k-1][node], min_path[k-1][up[k-1][node]])
    
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
    
    def min_on_path(node, ancestor):
        min_val = float('inf')
        for k in range(LOG - 1, -1, -1):
            if depth[node] - (1 << k) >= depth[ancestor]:
                min_val = min(min_val, min_path[k][node])
                node = up[k][node]
        return min_val
    
    results = []
    for a, b in queries:
        lca_node = lca(a, b)
        min_a_to_lca = min_on_path(a, lca_node)
        min_b_to_lca = min_on_path(b, lca_node)
        total_min = min(min_a_to_lca, min_b_to_lca)
        results.append(total_min)
    
    return results
```

**Analysis**:
- **Time**: O(n log n + q log n) - Preprocessing + query processing
- **Space**: O(n log n) - Binary lifting table
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Heavy-Light Decomposition
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use heavy-light decomposition to break tree into chains
2. Use segment trees on each chain for efficient range minimum queries
3. For each query, break path into O(log n) segments

**Implementation**:
```python
def optimal_path_queries_ii(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Heavy-light decomposition
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    size = [0] * (n + 1)
    heavy = [0] * (n + 1)
    head = [0] * (n + 1)
    pos = [0] * (n + 1)
    
    def dfs_size(node, par):
        parent[node] = par
        size[node] = 1
        heavy[node] = 0
        
        for child in graph[node]:
            if child != par:
                depth[child] = depth[node] + 1
                size[node] += dfs_size(child, node)
                if size[child] > size[heavy[node]]:
                    heavy[node] = child
        
        return size[node]
    
    dfs_size(1, 0)
    
    # Decompose tree into chains
    current_pos = 0
    def decompose(node, h):
        nonlocal current_pos
        head[node] = h
        pos[node] = current_pos
        current_pos += 1
        
        if heavy[node]:
            decompose(heavy[node], h)
        
        for child in graph[node]:
            if child != parent[node] and child != heavy[node]:
                decompose(child, child)
    
    decompose(1, 1)
    
    # Build segment tree for each chain
    chain_values = [0] * n
    for node in range(1, n + 1):
        chain_values[pos[node]] = values[node - 1]
    
    # Simple segment tree for range minimum
    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [float('inf')] * (4 * self.n)
            self.build(arr, 1, 0, self.n - 1)
        
        def build(self, arr, node, start, end):
            if start == end:
                self.tree[node] = arr[start]
            else:
                mid = (start + end) // 2
                self.build(arr, 2 * node, start, mid)
                self.build(arr, 2 * node + 1, mid + 1, end)
                self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
        
        def query(self, node, start, end, l, r):
            if r < start or end < l:
                return float('inf')
            if l <= start and end <= r:
                return self.tree[node]
            mid = (start + end) // 2
            return min(self.query(2 * node, start, mid, l, r), 
                       self.query(2 * node + 1, mid + 1, end, l, r))
    
    st = SegmentTree(chain_values)
    
    def path_query(a, b):
        min_val = float('inf')
        
        while head[a] != head[b]:
            if depth[head[a]] > depth[head[b]]:
                a, b = b, a
            
            # Add minimum from b to head[b]
            min_val = min(min_val, st.query(1, 0, n - 1, pos[head[b]], pos[b]))
            b = parent[head[b]]
        
        # Add minimum from a to b (they're in same chain now)
        if depth[a] > depth[b]:
            a, b = b, a
        min_val = min(min_val, st.query(1, 0, n - 1, pos[a], pos[b]))
        
        return min_val
    
    results = []
    for a, b in queries:
        results.append(path_query(a, b))
    
    return results
```

**Analysis**:
- **Time**: O(n + q log n) - Preprocessing + query processing
- **Space**: O(n) - Heavy-light decomposition and segment tree
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
Tree structure:
    1(1)
    |
    2(2)
   / \
3(3) 4(4)
      |
    5(5)

Heavy-Light Decomposition:
Chain 1: 1-2-4-5 (heavy edges)
Chain 2: 3 (light edge)

Path Query (1, 5):
1. 1 → 2 (same chain): min = 1
2. 2 → 4 (same chain): min = 2
3. 4 → 5 (same chain): min = 4
Total minimum: 1
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(n) | DFS for each query |
| Optimized | O(n log n + q log n) | O(n log n) | LCA with binary lifting |
| Optimal | O(n + q log n) | O(n) | Heavy-light decomposition |

### Time Complexity
- **Time**: O(n + q log n) - Preprocessing + query processing with HLD
- **Space**: O(n) - Heavy-light decomposition and segment tree

### Why This Solution Works
- **LCA Technique**: Use lowest common ancestor to break path into two parts
- **Binary Lifting**: Efficiently find LCA and minimum values in O(log n) time
- **Heavy-Light Decomposition**: Break tree into chains for efficient range minimum queries
- **Optimal Approach**: Heavy-light decomposition provides the best possible complexity for path minimum queries

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Path Queries II with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain path minimum queries efficiently.

**Link**: [CSES Problem Set - Path Queries II with Updates](https://cses.fi/problemset/task/path_queries_ii_updates)

```python
class PathQueriesIIWithUpdates:
    def __init__(self, n, edges, values):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.values = values[:]
        self.depths = [0] * n
        self.log_n = 20  # Maximum log n for binary lifting
        self.up = [[-1] * self.log_n for _ in range(n)]
        self.min_up = [[float('inf')] * self.log_n for _ in range(n)]
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def _calculate_depths(self):
        """Calculate depth of each node using DFS"""
        def dfs(node, parent, d):
            self.depths[node] = d
            self.up[node][0] = parent
            self.min_up[node][0] = self.values[node]
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node, d + 1)
        
        dfs(0, -1, 0)
    
    def _preprocess_binary_lifting(self):
        """Preprocess binary lifting table with minimum values"""
        for j in range(1, self.log_n):
            for i in range(self.n):
                if self.up[i][j-1] != -1:
                    self.up[i][j] = self.up[self.up[i][j-1]][j-1]
                    self.min_up[i][j] = min(
                        self.min_up[i][j-1],
                        self.min_up[self.up[i][j-1]][j-1]
                    )
    
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
    
    def update_value(self, node, new_value):
        """Update value of a node and recalculate binary lifting table"""
        self.values[node] = new_value
        
        # Recalculate binary lifting table
        self._preprocess_binary_lifting()
    
    def get_lca(self, node1, node2):
        """Get lowest common ancestor of two nodes"""
        # Make sure node1 is deeper
        if self.depths[node1] < self.depths[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        diff = self.depths[node1] - self.depths[node2]
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
    
    def get_path_minimum(self, node1, node2):
        """Get minimum value on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Calculate minimum from node1 to LCA
        min1 = self.values[node1]
        current = node1
        while current != lca:
            min1 = min(min1, self.values[current])
            current = self.up[current][0]
        
        # Calculate minimum from node2 to LCA
        min2 = self.values[node2]
        current = node2
        while current != lca:
            min2 = min(min2, self.values[current])
            current = self.up[current][0]
        
        # Include LCA value
        return min(min1, min2, self.values[lca])
    
    def get_path_maximum(self, node1, node2):
        """Get maximum value on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Calculate maximum from node1 to LCA
        max1 = self.values[node1]
        current = node1
        while current != lca:
            max1 = max(max1, self.values[current])
            current = self.up[current][0]
        
        # Calculate maximum from node2 to LCA
        max2 = self.values[node2]
        current = node2
        while current != lca:
            max2 = max(max2, self.values[current])
            current = self.up[current][0]
        
        # Include LCA value
        return max(max1, max2, self.values[lca])
    
    def get_path_sum(self, node1, node2):
        """Get sum of values on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Calculate sum from node1 to LCA
        sum1 = 0
        current = node1
        while current != lca:
            sum1 += self.values[current]
            current = self.up[current][0]
        
        # Calculate sum from node2 to LCA
        sum2 = 0
        current = node2
        while current != lca:
            sum2 += self.values[current]
            current = self.up[current][0]
        
        # Add LCA value
        return sum1 + sum2 + self.values[lca]
    
    def get_path_values(self, node1, node2):
        """Get all values on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Get values from node1 to LCA
        values1 = []
        current = node1
        while current != lca:
            values1.append(self.values[current])
            current = self.up[current][0]
        
        # Get values from node2 to LCA
        values2 = []
        current = node2
        while current != lca:
            values2.append(self.values[current])
            current = self.up[current][0]
        
        # Combine values
        return values1 + [self.values[lca]] + values2[::-1]
    
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
            elif query['type'] == 'update_value':
                self.update_value(query['node'], query['new_value'])
                results.append(None)
            elif query['type'] == 'path_minimum':
                result = self.get_path_minimum(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path_maximum':
                result = self.get_path_maximum(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path_sum':
                result = self.get_path_sum(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path_values':
                result = self.get_path_values(query['u'], query['v'])
                results.append(result)
        return results
```

### Variation 2: Path Queries II with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on path queries.

**Link**: [CSES Problem Set - Path Queries II Different Operations](https://cses.fi/problemset/task/path_queries_ii_operations)

```python
class PathQueriesIIDifferentOps:
    def __init__(self, n, edges, values):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.values = values[:]
        self.depths = [0] * n
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
            self.depths[node] = d
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
        if self.depths[node1] < self.depths[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        diff = self.depths[node1] - self.depths[node2]
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
    
    def get_path_minimum(self, node1, node2):
        """Get minimum value on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Calculate minimum from node1 to LCA
        min1 = self.values[node1]
        current = node1
        while current != lca:
            min1 = min(min1, self.values[current])
            current = self.up[current][0]
        
        # Calculate minimum from node2 to LCA
        min2 = self.values[node2]
        current = node2
        while current != lca:
            min2 = min(min2, self.values[current])
            current = self.up[current][0]
        
        # Include LCA value
        return min(min1, min2, self.values[lca])
    
    def get_path_maximum(self, node1, node2):
        """Get maximum value on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Calculate maximum from node1 to LCA
        max1 = self.values[node1]
        current = node1
        while current != lca:
            max1 = max(max1, self.values[current])
            current = self.up[current][0]
        
        # Calculate maximum from node2 to LCA
        max2 = self.values[node2]
        current = node2
        while current != lca:
            max2 = max(max2, self.values[current])
            current = self.up[current][0]
        
        # Include LCA value
        return max(max1, max2, self.values[lca])
    
    def get_path_sum(self, node1, node2):
        """Get sum of values on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Calculate sum from node1 to LCA
        sum1 = 0
        current = node1
        while current != lca:
            sum1 += self.values[current]
            current = self.up[current][0]
        
        # Calculate sum from node2 to LCA
        sum2 = 0
        current = node2
        while current != lca:
            sum2 += self.values[current]
            current = self.up[current][0]
        
        # Add LCA value
        return sum1 + sum2 + self.values[lca]
    
    def get_path_values(self, node1, node2):
        """Get all values on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Get values from node1 to LCA
        values1 = []
        current = node1
        while current != lca:
            values1.append(self.values[current])
            current = self.up[current][0]
        
        # Get values from node2 to LCA
        values2 = []
        current = node2
        while current != lca:
            values2.append(self.values[current])
            current = self.up[current][0]
        
        # Combine values
        return values1 + [self.values[lca]] + values2[::-1]
    
    def get_path_length(self, node1, node2):
        """Get length of path between two nodes"""
        lca = self.get_lca(node1, node2)
        return self.depths[node1] + self.depths[node2] - 2 * self.depths[lca]
    
    def get_path_statistics(self, node1, node2):
        """Get comprehensive statistics for path between two nodes"""
        values = self.get_path_values(node1, node2)
        
        return {
            'sum': sum(values),
            'max': max(values),
            'min': min(values),
            'avg': sum(values) / len(values),
            'length': len(values),
            'values': values
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'path_minimum':
                result = self.get_path_minimum(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path_maximum':
                result = self.get_path_maximum(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path_sum':
                result = self.get_path_sum(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path_values':
                result = self.get_path_values(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path_length':
                result = self.get_path_length(query['u'], query['v'])
                results.append(result)
            elif query['type'] == 'path_statistics':
                result = self.get_path_statistics(query['u'], query['v'])
                results.append(result)
        return results
```

### Variation 3: Path Queries II with Constraints
**Problem**: Handle path queries with additional constraints (e.g., minimum value, maximum value, value range).

**Link**: [CSES Problem Set - Path Queries II with Constraints](https://cses.fi/problemset/task/path_queries_ii_constraints)

```python
class PathQueriesIIWithConstraints:
    def __init__(self, n, edges, values, min_value, max_value):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.values = values[:]
        self.depths = [0] * n
        self.log_n = 20  # Maximum log n for binary lifting
        self.up = [[-1] * self.log_n for _ in range(n)]
        self.min_value = min_value
        self.max_value = max_value
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_depths()
        self._preprocess_binary_lifting()
    
    def _calculate_depths(self):
        """Calculate depth of each node using DFS"""
        def dfs(node, parent, d):
            self.depths[node] = d
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
        if self.depths[node1] < self.depths[node2]:
            node1, node2 = node2, node1
        
        # Bring node1 to same depth as node2
        diff = self.depths[node1] - self.depths[node2]
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
    
    def get_path_minimum(self, node1, node2):
        """Get minimum value on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Calculate minimum from node1 to LCA
        min1 = self.values[node1]
        current = node1
        while current != lca:
            min1 = min(min1, self.values[current])
            current = self.up[current][0]
        
        # Calculate minimum from node2 to LCA
        min2 = self.values[node2]
        current = node2
        while current != lca:
            min2 = min(min2, self.values[current])
            current = self.up[current][0]
        
        # Include LCA value
        return min(min1, min2, self.values[lca])
    
    def get_path_maximum(self, node1, node2):
        """Get maximum value on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Calculate maximum from node1 to LCA
        max1 = self.values[node1]
        current = node1
        while current != lca:
            max1 = max(max1, self.values[current])
            current = self.up[current][0]
        
        # Calculate maximum from node2 to LCA
        max2 = self.values[node2]
        current = node2
        while current != lca:
            max2 = max(max2, self.values[current])
            current = self.up[current][0]
        
        # Include LCA value
        return max(max1, max2, self.values[lca])
    
    def get_path_values(self, node1, node2):
        """Get all values on path between two nodes"""
        lca = self.get_lca(node1, node2)
        
        # Get values from node1 to LCA
        values1 = []
        current = node1
        while current != lca:
            values1.append(self.values[current])
            current = self.up[current][0]
        
        # Get values from node2 to LCA
        values2 = []
        current = node2
        while current != lca:
            values2.append(self.values[current])
            current = self.up[current][0]
        
        # Combine values
        return values1 + [self.values[lca]] + values2[::-1]
    
    def constrained_path_minimum_query(self, node1, node2):
        """Query path minimum with constraints"""
        values = self.get_path_values(node1, node2)
        
        # Filter values that satisfy constraints
        valid_values = [v for v in values if self.min_value <= v <= self.max_value]
        
        return min(valid_values) if valid_values else -1
    
    def constrained_path_maximum_query(self, node1, node2):
        """Query path maximum with constraints"""
        values = self.get_path_values(node1, node2)
        
        # Filter values that satisfy constraints
        valid_values = [v for v in values if self.min_value <= v <= self.max_value]
        
        return max(valid_values) if valid_values else -1
    
    def find_valid_paths(self):
        """Find all paths that satisfy value constraints"""
        valid_paths = []
        
        for i in range(self.n):
            for j in range(i + 1, self.n):
                values = self.get_path_values(i, j)
                if all(self.min_value <= v <= self.max_value for v in values):
                    valid_paths.append((i, j, values))
        
        return valid_paths
    
    def count_valid_paths(self):
        """Count number of valid paths"""
        return len(self.find_valid_paths())
    
    def get_constraint_statistics(self):
        """Get statistics about valid paths"""
        valid_paths = self.find_valid_paths()
        
        if not valid_paths:
            return {
                'valid_paths_count': 0,
                'min_value': self.min_value,
                'max_value': self.max_value,
                'valid_paths': []
            }
        
        all_values = []
        for _, _, values in valid_paths:
            all_values.extend(values)
        
        return {
            'valid_paths_count': len(valid_paths),
            'min_value': self.min_value,
            'max_value': self.max_value,
            'min_valid_value': min(all_values),
            'max_valid_value': max(all_values),
            'avg_valid_value': sum(all_values) / len(all_values),
            'valid_paths': valid_paths
        }

# Example usage
n = 5
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
values = [1, 2, 3, 4, 5]
min_value = 2
max_value = 4

pq = PathQueriesIIWithConstraints(n, edges, values, min_value, max_value)
result = pq.constrained_path_minimum_query(0, 4)
print(f"Constrained path minimum query result: {result}")

valid_paths = pq.find_valid_paths()
print(f"Valid paths: {valid_paths}")

statistics = pq.get_constraint_statistics()
print(f"Constraint statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Path Queries](https://cses.fi/problemset/task/1138) - Basic path queries in tree
- [Path Queries II](https://cses.fi/problemset/task/2134) - Advanced path queries in tree
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Find diameter of tree

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Heavy-Light Decomposition**: Tree decomposition, path queries
- **LCA Algorithm**: Lowest common ancestor, binary lifting
- **Tree Queries**: Path queries, tree analysis, tree operations
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
