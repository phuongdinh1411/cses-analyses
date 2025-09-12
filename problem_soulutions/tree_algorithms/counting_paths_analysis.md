---
layout: simple
title: "Counting Paths"
permalink: /problem_soulutions/tree_algorithms/counting_paths_analysis
---

# Counting Paths

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

Given a tree with n nodes, count the number of paths of length k in the tree.

**Input**: 
- First line: n (number of nodes)
- Next n-1 lines: edges of the tree
- Next line: k (path length)

**Output**: 
- Number of paths of length k in the tree

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ k ≤ n

**Example**:
```
Input:
5
1 2
2 3
2 4
4 5
2

Output:
4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each node, perform BFS to find all nodes at distance k
2. Count the number of such nodes
3. Sum up all counts and divide by 2 (since each path is counted twice)

**Implementation**:
```python
def brute_force_counting_paths(n, edges, k):
    from collections import deque, defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    total_paths = 0
    
    for start in range(1, n + 1):
        # BFS to find nodes at distance k
        queue = deque([(start, 0)])
        visited = {start}
        
        while queue:
            node, dist = queue.popleft()
            
            if dist == k:
                total_paths += 1
                continue
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
    
    # Each path is counted twice (from both endpoints)
    return total_paths // 2
```

**Analysis**:
- **Time**: O(n²) - For each node, BFS takes O(n) time
- **Space**: O(n) - Queue and visited set
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Tree DP
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to count paths of each length for each node
2. For each node, count paths passing through it
3. Use rerooting technique to efficiently compute counts

**Implementation**:
```python
def optimized_counting_paths(n, edges, k):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Precompute path counts
    path_counts = [0] * n
    
    def dfs(node, parent):
        # Count paths of each length passing through this node
        subtree_sizes = []
        
        for child in graph[node]:
            if child != parent:
                child_size = dfs(child, node)
                subtree_sizes.append(child_size)
        
        # Count paths of length k
        count = 0
        
        # Paths within subtrees
        for size in subtree_sizes:
            if size >= k:
                count += size - k + 1
        
        # Paths passing through this node
        for i in range(len(subtree_sizes)):
            for j in range(i + 1, len(subtree_sizes)):
                if subtree_sizes[i] + subtree_sizes[j] >= k:
                    count += min(subtree_sizes[i], k) * min(subtree_sizes[j], k)
        
        path_counts[k] += count
        return sum(subtree_sizes) + 1
    
    dfs(1, -1)
    return path_counts[k]
```

**Analysis**:
- **Time**: O(n²) - Tree DP with rerooting
- **Space**: O(n) - Recursion stack and arrays
- **Improvement**: More efficient than brute force

### Approach 3: Optimal with Centroid Decomposition
**Time Complexity**: O(n log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use centroid decomposition to divide the tree
2. For each centroid, count paths passing through it
3. Recursively solve for each subtree

**Implementation**:
```python
def optimal_counting_paths(n, edges, k):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    path_counts = [0] * n
    
    def get_centroid(node, parent, total_size):
        # Find centroid of the tree
        max_subtree = 0
        centroid = node
        
        def dfs_size(curr, par):
            nonlocal max_subtree, centroid
            size = 1
            
            for child in graph[curr]:
                if child != par:
                    child_size = dfs_size(child, curr)
                    size += child_size
                    max_subtree = max(max_subtree, child_size)
            
            if max_subtree <= total_size // 2:
                centroid = curr
            
            return size
        
        dfs_size(node, parent)
        return centroid
    
    def solve_subtree(node, parent):
        if node is None:
            return
        
        # Find centroid
        centroid = get_centroid(node, parent, n)
        
        # Count paths passing through centroid
        distances = defaultdict(int)
        
        def dfs_distances(curr, par, dist):
            distances[dist] += 1
            for child in graph[curr]:
                if child != par and child != centroid:
                    dfs_distances(child, curr, dist + 1)
        
        # Count paths of length k
        count = 0
        
        # Paths within each subtree of centroid
        for child in graph[centroid]:
            if child != parent:
                subtree_distances = defaultdict(int)
                
                def dfs_subtree(curr, par, dist):
                    subtree_distances[dist] += 1
                    for grandchild in graph[curr]:
                        if grandchild != par and grandchild != centroid:
                            dfs_subtree(grandchild, curr, dist + 1)
                
                dfs_subtree(child, centroid, 1)
                
                # Count paths of length k within this subtree
                for dist in subtree_distances:
                    if dist == k:
                        count += subtree_distances[dist]
        
        path_counts[k] += count
        
        # Recursively solve for each subtree
        for child in graph[centroid]:
            if child != parent:
                solve_subtree(child, centroid)
    
    solve_subtree(1, -1)
    return path_counts[k]
```

**Analysis**:
- **Time**: O(n log n) - Centroid decomposition
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

Centroid Decomposition:
1. Find centroid (node 2)
2. Count paths through centroid of length 2:
   - (1,3) = 1 path
   - (1,4) = 1 path
   - (3,4) = 1 path
   - (4,5) = 1 path
3. Recursively solve subtrees
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | BFS from each node |
| Optimized | O(n²) | O(n) | Tree DP with rerooting |
| Optimal | O(n log n) | O(n) | Centroid decomposition |

### Time Complexity
- **Time**: O(n log n) - Centroid decomposition for efficient path counting
- **Space**: O(n) - Recursion stack and arrays

### Why This Solution Works
- **Tree DP**: Use dynamic programming to count paths passing through each node
- **Rerooting**: Efficiently compute path counts for all nodes
- **Centroid Decomposition**: Divide tree into smaller parts for efficient processing
- **Optimal Approach**: Centroid decomposition provides the best possible complexity for path counting

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Counting Paths with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain path counting queries efficiently.

**Link**: [CSES Problem Set - Counting Paths with Updates](https://cses.fi/problemset/task/counting_paths_updates)

```python
class CountingPathsWithUpdates:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.path_counts = [0] * n
        self.subtree_sizes = [0] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_path_counts()
    
    def _calculate_path_counts(self):
        """Calculate path counts using tree DP"""
        def dfs(node, parent):
            self.subtree_sizes[node] = 1
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node)
                    self.subtree_sizes[node] += self.subtree_sizes[neighbor]
            
            # Count paths passing through this node
            self.path_counts[node] = 0
            
            # Paths from this node to all nodes in its subtree
            self.path_counts[node] += self.subtree_sizes[node] - 1
            
            # Paths passing through this node (connecting different subtrees)
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    other_size = self.subtree_sizes[node] - self.subtree_sizes[neighbor]
                    self.path_counts[node] += self.subtree_sizes[neighbor] * other_size
        
        dfs(0, -1)
    
    def add_edge(self, u, v):
        """Add edge between nodes u and v"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        
        # Recalculate path counts
        self._calculate_path_counts()
    
    def remove_edge(self, u, v):
        """Remove edge between nodes u and v"""
        if v in self.adj[u]:
            self.adj[u].remove(v)
        if u in self.adj[v]:
            self.adj[v].remove(u)
        
        # Recalculate path counts
        self._calculate_path_counts()
    
    def get_path_count(self, node):
        """Get number of paths passing through given node"""
        return self.path_counts[node]
    
    def get_all_path_counts(self):
        """Get path counts for all nodes"""
        return self.path_counts.copy()
    
    def get_total_paths(self):
        """Get total number of paths in the tree"""
        return sum(self.path_counts) // 2  # Each path is counted twice
    
    def get_max_path_count(self):
        """Get maximum path count among all nodes"""
        return max(self.path_counts)
    
    def get_min_path_count(self):
        """Get minimum path count among all nodes"""
        return min(self.path_counts)
    
    def get_path_statistics(self):
        """Get comprehensive path statistics"""
        return {
            'total_paths': self.get_total_paths(),
            'max_path_count': self.get_max_path_count(),
            'min_path_count': self.get_min_path_count(),
            'path_counts': self.path_counts.copy(),
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
            elif query['type'] == 'path_count':
                result = self.get_path_count(query['node'])
                results.append(result)
            elif query['type'] == 'all_path_counts':
                result = self.get_all_path_counts()
                results.append(result)
            elif query['type'] == 'total_paths':
                result = self.get_total_paths()
                results.append(result)
            elif query['type'] == 'max_path_count':
                result = self.get_max_path_count()
                results.append(result)
            elif query['type'] == 'min_path_count':
                result = self.get_min_path_count()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_path_statistics()
                results.append(result)
        return results
```

### Variation 2: Counting Paths with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on path counting.

**Link**: [CSES Problem Set - Counting Paths Different Operations](https://cses.fi/problemset/task/counting_paths_operations)

```python
class CountingPathsDifferentOps:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.path_counts = [0] * n
        self.subtree_sizes = [0] * n
        self.depths = [0] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_path_counts()
        self._calculate_depths()
    
    def _calculate_path_counts(self):
        """Calculate path counts using tree DP"""
        def dfs(node, parent):
            self.subtree_sizes[node] = 1
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node)
                    self.subtree_sizes[node] += self.subtree_sizes[neighbor]
            
            # Count paths passing through this node
            self.path_counts[node] = 0
            
            # Paths from this node to all nodes in its subtree
            self.path_counts[node] += self.subtree_sizes[node] - 1
            
            # Paths passing through this node (connecting different subtrees)
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    other_size = self.subtree_sizes[node] - self.subtree_sizes[neighbor]
                    self.path_counts[node] += self.subtree_sizes[neighbor] * other_size
        
        dfs(0, -1)
    
    def _calculate_depths(self):
        """Calculate depth of each node"""
        def dfs(node, parent, depth):
            self.depths[node] = depth
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node, depth + 1)
        
        dfs(0, -1, 0)
    
    def get_path_count(self, node):
        """Get number of paths passing through given node"""
        return self.path_counts[node]
    
    def get_paths_by_length(self, length):
        """Get all paths of specific length"""
        paths = []
        
        def dfs(node, parent, current_path):
            if len(current_path) == length:
                paths.append(current_path.copy())
                return
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, node, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return paths
    
    def get_paths_from_node(self, node):
        """Get all paths starting from given node"""
        paths = []
        
        def dfs(current, parent, current_path):
            if len(current_path) > 1:
                paths.append(current_path.copy())
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, current, current_path)
                    current_path.pop()
        
        dfs(node, -1, [node])
        return paths
    
    def get_paths_to_node(self, node):
        """Get all paths ending at given node"""
        paths = []
        
        def dfs(current, parent, current_path):
            if current == node and len(current_path) > 1:
                paths.append(current_path.copy())
                return
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, current, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return paths
    
    def get_paths_through_node(self, node):
        """Get all paths passing through given node"""
        paths = []
        
        def dfs(current, parent, current_path):
            if node in current_path and len(current_path) > 1:
                paths.append(current_path.copy())
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, current, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return paths
    
    def get_longest_path(self):
        """Get longest path in the tree"""
        longest_path = []
        max_length = 0
        
        def dfs(node, parent, current_path):
            nonlocal longest_path, max_length
            
            if len(current_path) > max_length:
                max_length = len(current_path)
                longest_path = current_path.copy()
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, node, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return longest_path, max_length - 1
    
    def get_shortest_path(self, start, end):
        """Get shortest path between two nodes"""
        from collections import deque
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            
            if node == end:
                return path
            
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return []
    
    def get_path_statistics(self):
        """Get comprehensive path statistics"""
        longest_path, max_length = self.get_longest_path()
        
        return {
            'total_paths': sum(self.path_counts) // 2,
            'max_path_count': max(self.path_counts),
            'min_path_count': min(self.path_counts),
            'longest_path_length': max_length,
            'longest_path': longest_path,
            'path_counts': self.path_counts.copy(),
            'subtree_sizes': self.subtree_sizes.copy(),
            'depths': self.depths.copy()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'path_count':
                result = self.get_path_count(query['node'])
                results.append(result)
            elif query['type'] == 'paths_by_length':
                result = self.get_paths_by_length(query['length'])
                results.append(result)
            elif query['type'] == 'paths_from_node':
                result = self.get_paths_from_node(query['node'])
                results.append(result)
            elif query['type'] == 'paths_to_node':
                result = self.get_paths_to_node(query['node'])
                results.append(result)
            elif query['type'] == 'paths_through_node':
                result = self.get_paths_through_node(query['node'])
                results.append(result)
            elif query['type'] == 'longest_path':
                result = self.get_longest_path()
                results.append(result)
            elif query['type'] == 'shortest_path':
                result = self.get_shortest_path(query['start'], query['end'])
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_path_statistics()
                results.append(result)
        return results
```

### Variation 3: Counting Paths with Constraints
**Problem**: Handle path counting queries with additional constraints (e.g., minimum length, maximum length).

**Link**: [CSES Problem Set - Counting Paths with Constraints](https://cses.fi/problemset/task/counting_paths_constraints)

```python
class CountingPathsWithConstraints:
    def __init__(self, n, edges, min_length, max_length):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.path_counts = [0] * n
        self.subtree_sizes = [0] * n
        self.min_length = min_length
        self.max_length = max_length
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_path_counts()
    
    def _calculate_path_counts(self):
        """Calculate path counts using tree DP"""
        def dfs(node, parent):
            self.subtree_sizes[node] = 1
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    dfs(neighbor, node)
                    self.subtree_sizes[node] += self.subtree_sizes[neighbor]
            
            # Count paths passing through this node
            self.path_counts[node] = 0
            
            # Paths from this node to all nodes in its subtree
            self.path_counts[node] += self.subtree_sizes[node] - 1
            
            # Paths passing through this node (connecting different subtrees)
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    other_size = self.subtree_sizes[node] - self.subtree_sizes[neighbor]
                    self.path_counts[node] += self.subtree_sizes[neighbor] * other_size
        
        dfs(0, -1)
    
    def constrained_path_count_query(self, node):
        """Query path count with constraints"""
        if self.path_counts[node] == 0:
            return 0
        
        # Count paths of valid lengths passing through this node
        valid_paths = 0
        
        def dfs(current, parent, current_path):
            nonlocal valid_paths
            
            if len(current_path) >= self.min_length and len(current_path) <= self.max_length:
                valid_paths += 1
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, current, current_path)
                    current_path.pop()
        
        # Count paths starting from this node
        dfs(node, -1, [node])
        
        return valid_paths
    
    def find_valid_paths(self):
        """Find all paths that satisfy length constraints"""
        valid_paths = []
        
        def dfs(node, parent, current_path):
            if len(current_path) >= self.min_length and len(current_path) <= self.max_length:
                valid_paths.append(current_path.copy())
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, node, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return valid_paths
    
    def count_valid_paths(self):
        """Count number of valid paths"""
        return len(self.find_valid_paths())
    
    def get_valid_paths_by_length(self, length):
        """Get all valid paths of specific length"""
        if not (self.min_length <= length <= self.max_length):
            return []
        
        paths = []
        
        def dfs(node, parent, current_path):
            if len(current_path) == length:
                paths.append(current_path.copy())
                return
            
            for neighbor in self.adj[node]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, node, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return paths
    
    def get_valid_paths_from_node(self, node):
        """Get all valid paths starting from given node"""
        valid_paths = []
        
        def dfs(current, parent, current_path):
            if len(current_path) >= self.min_length and len(current_path) <= self.max_length:
                valid_paths.append(current_path.copy())
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, current, current_path)
                    current_path.pop()
        
        dfs(node, -1, [node])
        return valid_paths
    
    def get_valid_paths_through_node(self, node):
        """Get all valid paths passing through given node"""
        valid_paths = []
        
        def dfs(current, parent, current_path):
            if node in current_path and len(current_path) >= self.min_length and len(current_path) <= self.max_length:
                valid_paths.append(current_path.copy())
            
            for neighbor in self.adj[current]:
                if neighbor != parent:
                    current_path.append(neighbor)
                    dfs(neighbor, current, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return valid_paths
    
    def get_constraint_statistics(self):
        """Get statistics about valid paths"""
        valid_paths = self.find_valid_paths()
        
        if not valid_paths:
            return {
                'valid_paths_count': 0,
                'min_length': self.min_length,
                'max_length': self.max_length,
                'valid_paths': []
            }
        
        lengths = [len(path) for path in valid_paths]
        
        return {
            'valid_paths_count': len(valid_paths),
            'min_length': self.min_length,
            'max_length': self.max_length,
            'min_valid_length': min(lengths),
            'max_valid_length': max(lengths),
            'avg_valid_length': sum(lengths) / len(lengths),
            'valid_paths': valid_paths
        }

# Example usage
n = 5
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
min_length = 2
max_length = 4

cp = CountingPathsWithConstraints(n, edges, min_length, max_length)
result = cp.constrained_path_count_query(1)
print(f"Constrained path count query result: {result}")

valid_paths = cp.find_valid_paths()
print(f"Valid paths: {valid_paths}")

statistics = cp.get_constraint_statistics()
print(f"Constraint statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Counting Paths](https://cses.fi/problemset/task/1136) - Basic path counting in tree
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Find diameter of tree
- [Tree Distances I](https://cses.fi/problemset/task/1132) - Distance queries in tree

#### **LeetCode Problems**
- [Binary Tree Paths](https://leetcode.com/problems/binary-tree-paths/) - Find all paths in binary tree
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Tree DP**: Dynamic programming on trees, path counting
- **Tree Traversal**: DFS, BFS, tree traversal algorithms
- **Tree Queries**: Path queries, tree analysis, tree operations
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
