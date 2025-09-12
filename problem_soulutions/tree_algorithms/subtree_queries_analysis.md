---
layout: simple
title: "Subtree Queries"
permalink: /problem_soulutions/tree_algorithms/subtree_queries_analysis
---

# Subtree Queries

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

Given a tree with n nodes, each node has a value. Process q queries of the form "find the sum of values in the subtree rooted at node a".

**Input**: 
- First line: n (number of nodes)
- Next n lines: values of nodes 1 to n
- Next n-1 lines: edges of the tree
- Next line: q (number of queries)
- Next q lines: integer a (subtree root)

**Output**: 
- q lines: sum of values in subtree rooted at a

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
1
2
3

Output:
15
14
3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, perform DFS from the given node
2. Sum all values in the subtree
3. Return the sum for each query

**Implementation**:
```python
def brute_force_subtree_queries(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def subtree_sum(node):
        # DFS to find sum of subtree rooted at node
        total_sum = values[node - 1]
        visited = set()
        
        def dfs(curr):
            visited.add(curr)
            for child in graph[curr]:
                if child not in visited:
                    total_sum += values[child - 1]
                    dfs(child)
        
        dfs(node)
        return total_sum
    
    results = []
    for a in queries:
        sum_val = subtree_sum(a)
        results.append(sum_val)
    
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
1. Use tree DP to precompute subtree sums for all nodes
2. For each query, return the precomputed sum
3. Use DFS to compute subtree sums in a single pass

**Implementation**:
```python
def optimized_subtree_queries(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Precompute subtree sums
    subtree_sums = [0] * (n + 1)
    
    def dfs(node, parent):
        subtree_sums[node] = values[node - 1]
        
        for child in graph[node]:
            if child != parent:
                subtree_sums[node] += dfs(child, node)
        
        return subtree_sums[node]
    
    dfs(1, -1)
    
    # Answer queries
    results = []
    for a in queries:
        results.append(subtree_sums[a])
    
    return results
```

**Analysis**:
- **Time**: O(n + q) - Single DFS pass + O(1) per query
- **Space**: O(n) - Recursion stack and subtree sums array
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Euler Tour
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use Euler tour to flatten the tree into an array
2. Each subtree corresponds to a contiguous range in the array
3. Use prefix sums for efficient range sum queries

**Implementation**:
```python
def optimal_subtree_queries(n, values, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Euler tour
    euler_tour = []
    in_time = [0] * (n + 1)
    out_time = [0] * (n + 1)
    time_counter = 0
    
    def dfs(node, parent):
        nonlocal time_counter
        in_time[node] = time_counter
        euler_tour.append(values[node - 1])
        time_counter += 1
        
        for child in graph[node]:
            if child != parent:
                dfs(child, node)
        
        out_time[node] = time_counter - 1
    
    dfs(1, -1)
    
    # Build prefix sums
    prefix_sums = [0] * (n + 1)
    for i in range(n):
        prefix_sums[i + 1] = prefix_sums[i] + euler_tour[i]
    
    # Answer queries
    results = []
    for a in queries:
        start = in_time[a]
        end = out_time[a]
        sum_val = prefix_sums[end + 1] - prefix_sums[start]
        results.append(sum_val)
    
    return results
```

**Analysis**:
- **Time**: O(n + q) - Euler tour + O(1) per query
- **Space**: O(n) - Euler tour array and prefix sums
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

Euler Tour:
[1, 2, 3, 4, 5]
 0  1  2  3  4

Subtree ranges:
Node 1: [0, 4] → sum = 15
Node 2: [1, 4] → sum = 14
Node 3: [2, 2] → sum = 3
Node 4: [3, 4] → sum = 9
Node 5: [4, 4] → sum = 5
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(n) | DFS for each query |
| Optimized | O(n + q) | O(n) | Tree DP with precomputation |
| Optimal | O(n + q) | O(n) | Euler tour with prefix sums |

### Time Complexity
- **Time**: O(n + q) - Single DFS pass + O(1) per query
- **Space**: O(n) - Euler tour array and prefix sums

### Why This Solution Works
- **Tree DP**: Use dynamic programming to precompute subtree sums
- **Euler Tour**: Flatten tree into array for efficient range queries
- **Prefix Sums**: Enable O(1) range sum queries on the flattened array
- **Optimal Approach**: Euler tour provides the most efficient solution for subtree queries

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Subtree Queries with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain subtree queries efficiently.

**Link**: [CSES Problem Set - Subtree Queries with Updates](https://cses.fi/problemset/task/subtree_queries_updates)

```python
class SubtreeQueriesWithUpdates:
    def __init__(self, n, edges, values):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.values = values[:]
        self.subtree_sums = [0] * n
        self.subtree_sizes = [0] * n
        self.parent = [-1] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_subtree_info()
    
    def _calculate_subtree_info(self):
        """Calculate subtree sums and sizes using DFS"""
        def dfs(node, parent):
            self.parent[node] = parent
            self.subtree_sums[node] = self.values[node]
            self.subtree_sizes[node] = 1
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    self.subtree_sums[node] += self.subtree_sums[child]
                    self.subtree_sizes[node] += self.subtree_sizes[child]
        
        dfs(0, -1)
    
    def add_edge(self, u, v):
        """Add edge between nodes u and v"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        
        # Recalculate subtree info
        self._calculate_subtree_info()
    
    def remove_edge(self, u, v):
        """Remove edge between nodes u and v"""
        if v in self.adj[u]:
            self.adj[u].remove(v)
        if u in self.adj[v]:
            self.adj[v].remove(u)
        
        # Recalculate subtree info
        self._calculate_subtree_info()
    
    def update_value(self, node, new_value):
        """Update value of a node and recalculate affected subtree sums"""
        old_value = self.values[node]
        self.values[node] = new_value
        
        # Update subtree sums for all ancestors
        current = node
        while current != -1:
            self.subtree_sums[current] += (new_value - old_value)
            current = self.parent[current]
    
    def get_subtree_sum(self, node):
        """Get sum of values in subtree rooted at node"""
        return self.subtree_sums[node]
    
    def get_subtree_size(self, node):
        """Get size of subtree rooted at node"""
        return self.subtree_sizes[node]
    
    def get_all_subtree_sums(self):
        """Get subtree sums for all nodes"""
        return self.subtree_sums.copy()
    
    def get_all_subtree_sizes(self):
        """Get subtree sizes for all nodes"""
        return self.subtree_sizes.copy()
    
    def get_subtree_statistics(self):
        """Get comprehensive subtree statistics"""
        return {
            'total_sum': sum(self.subtree_sums),
            'max_subtree_sum': max(self.subtree_sums),
            'min_subtree_sum': min(self.subtree_sums),
            'max_subtree_size': max(self.subtree_sizes),
            'min_subtree_size': min(self.subtree_sizes),
            'subtree_sums': self.subtree_sums.copy(),
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
            elif query['type'] == 'update_value':
                self.update_value(query['node'], query['new_value'])
                results.append(None)
            elif query['type'] == 'subtree_sum':
                result = self.get_subtree_sum(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_size':
                result = self.get_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'all_subtree_sums':
                result = self.get_all_subtree_sums()
                results.append(result)
            elif query['type'] == 'all_subtree_sizes':
                result = self.get_all_subtree_sizes()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_subtree_statistics()
                results.append(result)
        return results
```

### Variation 2: Subtree Queries with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on subtree queries.

**Link**: [CSES Problem Set - Subtree Queries Different Operations](https://cses.fi/problemset/task/subtree_queries_operations)

```python
class SubtreeQueriesDifferentOps:
    def __init__(self, n, edges, values):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.values = values[:]
        self.subtree_sums = [0] * n
        self.subtree_sizes = [0] * n
        self.subtree_maxs = [0] * n
        self.subtree_mins = [0] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_subtree_info()
    
    def _calculate_subtree_info(self):
        """Calculate subtree information using DFS"""
        def dfs(node, parent):
            self.subtree_sums[node] = self.values[node]
            self.subtree_sizes[node] = 1
            self.subtree_maxs[node] = self.values[node]
            self.subtree_mins[node] = self.values[node]
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    self.subtree_sums[node] += self.subtree_sums[child]
                    self.subtree_sizes[node] += self.subtree_sizes[child]
                    self.subtree_maxs[node] = max(self.subtree_maxs[node], self.subtree_maxs[child])
                    self.subtree_mins[node] = min(self.subtree_mins[node], self.subtree_mins[child])
        
        dfs(0, -1)
    
    def get_subtree_sum(self, node):
        """Get sum of values in subtree rooted at node"""
        return self.subtree_sums[node]
    
    def get_subtree_size(self, node):
        """Get size of subtree rooted at node"""
        return self.subtree_sizes[node]
    
    def get_subtree_max(self, node):
        """Get maximum value in subtree rooted at node"""
        return self.subtree_maxs[node]
    
    def get_subtree_min(self, node):
        """Get minimum value in subtree rooted at node"""
        return self.subtree_mins[node]
    
    def get_subtree_avg(self, node):
        """Get average value in subtree rooted at node"""
        return self.subtree_sums[node] / self.subtree_sizes[node]
    
    def get_subtree_statistics(self, node):
        """Get comprehensive statistics for subtree rooted at node"""
        return {
            'sum': self.subtree_sums[node],
            'size': self.subtree_sizes[node],
            'max': self.subtree_maxs[node],
            'min': self.subtree_mins[node],
            'avg': self.subtree_sums[node] / self.subtree_sizes[node]
        }
    
    def get_all_subtree_sums(self):
        """Get subtree sums for all nodes"""
        return self.subtree_sums.copy()
    
    def get_all_subtree_sizes(self):
        """Get subtree sizes for all nodes"""
        return self.subtree_sizes.copy()
    
    def get_all_subtree_maxs(self):
        """Get subtree maximums for all nodes"""
        return self.subtree_maxs.copy()
    
    def get_all_subtree_mins(self):
        """Get subtree minimums for all nodes"""
        return self.subtree_mins.copy()
    
    def get_global_statistics(self):
        """Get global statistics for all subtrees"""
        return {
            'total_sum': sum(self.subtree_sums),
            'max_subtree_sum': max(self.subtree_sums),
            'min_subtree_sum': min(self.subtree_sums),
            'max_subtree_size': max(self.subtree_sizes),
            'min_subtree_size': min(self.subtree_sizes),
            'max_subtree_max': max(self.subtree_maxs),
            'min_subtree_min': min(self.subtree_mins)
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'subtree_sum':
                result = self.get_subtree_sum(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_size':
                result = self.get_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_max':
                result = self.get_subtree_max(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_min':
                result = self.get_subtree_min(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_avg':
                result = self.get_subtree_avg(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_statistics':
                result = self.get_subtree_statistics(query['node'])
                results.append(result)
            elif query['type'] == 'all_subtree_sums':
                result = self.get_all_subtree_sums()
                results.append(result)
            elif query['type'] == 'all_subtree_sizes':
                result = self.get_all_subtree_sizes()
                results.append(result)
            elif query['type'] == 'all_subtree_maxs':
                result = self.get_all_subtree_maxs()
                results.append(result)
            elif query['type'] == 'all_subtree_mins':
                result = self.get_all_subtree_mins()
                results.append(result)
            elif query['type'] == 'global_statistics':
                result = self.get_global_statistics()
                results.append(result)
        return results
```

### Variation 3: Subtree Queries with Constraints
**Problem**: Handle subtree queries with additional constraints (e.g., minimum value, maximum value, value range).

**Link**: [CSES Problem Set - Subtree Queries with Constraints](https://cses.fi/problemset/task/subtree_queries_constraints)

```python
class SubtreeQueriesWithConstraints:
    def __init__(self, n, edges, values, min_value, max_value):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.values = values[:]
        self.subtree_sums = [0] * n
        self.subtree_sizes = [0] * n
        self.subtree_valid_counts = [0] * n
        self.min_value = min_value
        self.max_value = max_value
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_subtree_info()
    
    def _calculate_subtree_info(self):
        """Calculate subtree information using DFS"""
        def dfs(node, parent):
            self.subtree_sums[node] = self.values[node]
            self.subtree_sizes[node] = 1
            self.subtree_valid_counts[node] = 1 if self.min_value <= self.values[node] <= self.max_value else 0
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    self.subtree_sums[node] += self.subtree_sums[child]
                    self.subtree_sizes[node] += self.subtree_sizes[child]
                    self.subtree_valid_counts[node] += self.subtree_valid_counts[child]
        
        dfs(0, -1)
    
    def get_subtree_sum(self, node):
        """Get sum of values in subtree rooted at node"""
        return self.subtree_sums[node]
    
    def get_subtree_size(self, node):
        """Get size of subtree rooted at node"""
        return self.subtree_sizes[node]
    
    def get_subtree_valid_count(self, node):
        """Get count of valid values in subtree rooted at node"""
        return self.subtree_valid_counts[node]
    
    def get_subtree_valid_sum(self, node):
        """Get sum of valid values in subtree rooted at node"""
        # This would require a more complex implementation
        # For now, we'll use a simple approach
        valid_sum = 0
        if self.min_value <= self.values[node] <= self.max_value:
            valid_sum += self.values[node]
        
        for child in self.adj[node]:
            if child != self.parent[node]:
                valid_sum += self.get_subtree_valid_sum(child)
        
        return valid_sum
    
    def get_subtree_valid_values(self, node):
        """Get all valid values in subtree rooted at node"""
        valid_values = []
        
        def dfs_collect(node, parent):
            if self.min_value <= self.values[node] <= self.max_value:
                valid_values.append(self.values[node])
            
            for child in self.adj[node]:
                if child != parent:
                    dfs_collect(child, node)
        
        dfs_collect(node, -1)
        return valid_values
    
    def get_subtree_statistics(self, node):
        """Get comprehensive statistics for subtree rooted at node"""
        valid_values = self.get_subtree_valid_values(node)
        
        return {
            'total_sum': self.subtree_sums[node],
            'size': self.subtree_sizes[node],
            'valid_count': self.subtree_valid_counts[node],
            'valid_sum': sum(valid_values),
            'valid_avg': sum(valid_values) / len(valid_values) if valid_values else 0,
            'valid_values': valid_values
        }
    
    def get_all_subtree_sums(self):
        """Get subtree sums for all nodes"""
        return self.subtree_sums.copy()
    
    def get_all_subtree_sizes(self):
        """Get subtree sizes for all nodes"""
        return self.subtree_sizes.copy()
    
    def get_all_subtree_valid_counts(self):
        """Get subtree valid counts for all nodes"""
        return self.subtree_valid_counts.copy()
    
    def get_global_statistics(self):
        """Get global statistics for all subtrees"""
        return {
            'total_sum': sum(self.subtree_sums),
            'max_subtree_sum': max(self.subtree_sums),
            'min_subtree_sum': min(self.subtree_sums),
            'max_subtree_size': max(self.subtree_sizes),
            'min_subtree_size': min(self.subtree_sizes),
            'max_valid_count': max(self.subtree_valid_counts),
            'min_valid_count': min(self.subtree_valid_counts),
            'min_value': self.min_value,
            'max_value': self.max_value
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'subtree_sum':
                result = self.get_subtree_sum(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_size':
                result = self.get_subtree_size(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_valid_count':
                result = self.get_subtree_valid_count(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_valid_sum':
                result = self.get_subtree_valid_sum(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_valid_values':
                result = self.get_subtree_valid_values(query['node'])
                results.append(result)
            elif query['type'] == 'subtree_statistics':
                result = self.get_subtree_statistics(query['node'])
                results.append(result)
            elif query['type'] == 'all_subtree_sums':
                result = self.get_all_subtree_sums()
                results.append(result)
            elif query['type'] == 'all_subtree_sizes':
                result = self.get_all_subtree_sizes()
                results.append(result)
            elif query['type'] == 'all_subtree_valid_counts':
                result = self.get_all_subtree_valid_counts()
                results.append(result)
            elif query['type'] == 'global_statistics':
                result = self.get_global_statistics()
                results.append(result)
        return results

# Example usage
n = 5
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
values = [1, 2, 3, 4, 5]
min_value = 2
max_value = 4

sq = SubtreeQueriesWithConstraints(n, edges, values, min_value, max_value)
result = sq.get_subtree_valid_count(1)
print(f"Subtree valid count result: {result}")

valid_values = sq.get_subtree_valid_values(1)
print(f"Valid values: {valid_values}")

statistics = sq.get_global_statistics()
print(f"Global statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Subtree Queries](https://cses.fi/problemset/task/1137) - Basic subtree queries in tree
- [Path Queries](https://cses.fi/problemset/task/1138) - Path queries in tree
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Find diameter of tree

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Tree DP**: Dynamic programming on trees, subtree analysis
- **Euler Tour**: Tree flattening, range queries
- **Tree Queries**: Subtree queries, tree analysis, tree operations
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
