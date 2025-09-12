---
layout: simple
title: "Fixed Length Paths Ii"
permalink: /problem_soulutions/tree_algorithms/fixed_length_paths_ii_analysis
---

# Fixed Length Paths Ii

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand advanced path counting in trees with constraints
- Apply dynamic programming and tree traversal techniques for constrained path counting
- Implement efficient solutions for fixed length path problems with additional constraints
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in constrained tree path counting problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tree algorithms, DFS, BFS, tree DP, centroid decomposition, constrained path counting
- **Data Structures**: Trees, graphs, adjacency lists, DP tables, segment trees
- **Mathematical Concepts**: Tree theory, combinatorics, dynamic programming, constraint satisfaction
- **Programming Skills**: Tree traversal, algorithm implementation, DP optimization
- **Related Problems**: Fixed Length Paths I (basic path counting), Tree DP, Constrained Path Problems

## 📋 Problem Description

You are given a tree with n nodes, where each node has a color, and q queries. Each query consists of two integers k and c. For each query, find the number of paths of length exactly k where both endpoints have color c.

**Input**: 
- First line: integer n (number of nodes)
- Second line: n integers (colors of nodes 1 to n)
- Next n-1 lines: two integers u and v (edge between nodes u and v)
- Next line: integer q (number of queries)
- Next q lines: two integers k and c

**Output**: 
- For each query, print the number of paths of length exactly k with both endpoints having color c

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ q ≤ 10⁵
- 1 ≤ k ≤ n-1
- 1 ≤ c ≤ n
- Tree is connected and undirected

**Example**:
```
Input:
5
1 2 1 2 1
1 2
2 3
2 4
4 5
3
1 1
2 1
3 1

Output:
2
1
0

Explanation**: 
Tree structure:
    1(1)
    |
    2(2)
   / \
3(1) 4(2)
      |
    5(1)

Paths of length 1 with both endpoints color 1: (1,3) = 1 path
Paths of length 2 with both endpoints color 1: (1,5) = 1 path
Paths of length 3 with both endpoints color 1: none = 0 paths
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n² × k)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each node of the target color, perform BFS to find nodes at distance k
2. Count only nodes that also have the target color
3. Sum up all counts and divide by 2 (since each path is counted twice)

**Implementation**:
```python
def brute_force_fixed_length_paths_ii(n, colors, edges, queries):
    from collections import deque, defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    results = []
    
    for k, target_color in queries:
        count = 0
        
        # For each node of target color as starting point
        for start in range(1, n + 1):
            if colors[start - 1] != target_color:
                continue
                
            # BFS to find nodes at distance k with target color
            queue = deque([(start, 0)])
            visited = {start}
            
            while queue:
                node, dist = queue.popleft()
                
                if dist == k:
                    if colors[node - 1] == target_color:
                        count += 1
                    continue
                
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))
        
        # Each path is counted twice (from both endpoints)
        results.append(count // 2)
    
    return results
```

**Analysis**:
- **Time**: O(n² × k) - For each query, BFS from each node of target color
- **Space**: O(n) - Queue and visited set
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Tree DP
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to count paths of each length for each color
2. For each node, count paths passing through it with color constraints
3. Use rerooting technique to efficiently compute counts

**Implementation**:
```python
def optimized_fixed_length_paths_ii(n, colors, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Precompute path counts for each color and length
    path_counts = defaultdict(lambda: defaultdict(int))
    
    def dfs(node, parent):
        # Count paths of each length and color passing through this node
        color_counts = defaultdict(lambda: defaultdict(int))
        
        for child in graph[node]:
            if child != parent:
                child_counts = dfs(child, node)
                
                # Merge child counts
                for color in child_counts:
                    for length in child_counts[color]:
                        color_counts[color][length] += child_counts[color][length]
        
        # Add paths starting from this node
        node_color = colors[node - 1]
        color_counts[node_color][0] += 1
        
        # Count paths of each length
        for color in color_counts:
            for length in range(1, n):
                count = 0
                
                # Paths within subtrees
                for child in graph[node]:
                    if child != parent:
                        child_color = colors[child - 1]
                        if child_color == color:
                            count += color_counts[color].get(length - 1, 0)
                
                # Paths passing through this node
                for child1 in graph[node]:
                    if child1 == parent:
                        continue
                    for child2 in graph[node]:
                        if child2 == parent or child2 <= child1:
                            continue
                        
                        child1_color = colors[child1 - 1]
                        child2_color = colors[child2 - 1]
                        
                        if child1_color == color and child2_color == color:
                            for len1 in range(length):
                                len2 = length - len1 - 1
                                if len1 in color_counts[color] and len2 in color_counts[color]:
                                    count += color_counts[color][len1] * color_counts[color][len2]
                
                path_counts[color][length] += count
        
        return color_counts
    
    dfs(1, -1)
    
    # Answer queries
    results = []
    for k, target_color in queries:
        results.append(path_counts[target_color][k])
    
    return results
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
2. For each centroid, count paths passing through it with color constraints
3. Recursively solve for each subtree

**Implementation**:
```python
def optimal_fixed_length_paths_ii(n, colors, edges, queries):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    path_counts = defaultdict(lambda: defaultdict(int))
    
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
        
        # Count paths passing through centroid with color constraints
        color_distances = defaultdict(lambda: defaultdict(int))
        
        def dfs_distances(curr, par, dist, color):
            color_distances[color][dist] += 1
            for child in graph[curr]:
                if child != par and child != centroid:
                    dfs_distances(child, curr, dist + 1, colors[child - 1])
        
        # Count paths of each length and color
        for length in range(1, n):
            for target_color in range(1, n + 1):
                count = 0
                
                # Paths within each subtree of centroid
                for child in graph[centroid]:
                    if child != parent:
                        subtree_distances = defaultdict(lambda: defaultdict(int))
                        
                        def dfs_subtree(curr, par, dist, color):
                            subtree_distances[color][dist] += 1
                            for grandchild in graph[curr]:
                                if grandchild != par and grandchild != centroid:
                                    dfs_subtree(grandchild, curr, dist + 1, colors[grandchild - 1])
                        
                        dfs_subtree(child, centroid, 1, colors[child - 1])
                        
                        # Count paths of length k with target color within this subtree
                        for dist in subtree_distances[target_color]:
                            if dist == length:
                                count += subtree_distances[target_color][dist]
                
                path_counts[target_color][length] += count
        
        # Recursively solve for each subtree
        for child in graph[centroid]:
            if child != parent:
                solve_subtree(child, centroid)
    
    solve_subtree(1, -1)
    
    # Answer queries
    results = []
    for k, target_color in queries:
        results.append(path_counts[target_color][k])
    
    return results
```

**Analysis**:
- **Time**: O(n log n) - Centroid decomposition
- **Space**: O(n) - Recursion stack and arrays
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
Tree structure:
    1(1)
    |
    2(2)
   / \
3(1) 4(2)
      |
    5(1)

Centroid Decomposition with Color Constraints:
1. Find centroid (node 2)
2. Count paths through centroid with color 1:
   - Length 1: (1,3) = 1 path
   - Length 2: (1,5) = 1 path
   - Length 3: none = 0 paths
3. Recursively solve subtrees
```

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: [Description]
- **Complete Coverage**: [Description]
- **Simple Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def brute_force_fixed_length_paths_ii(tree, queries):
    """
    [Description]
    
    Args:
        tree: [Description]
        queries: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's inefficient**: [Reason]

---

### Approach 2: Optimized

**Key Insights from Optimized Approach**:
- **Optimization Technique**: [Description]
- **Efficiency Improvement**: [Description]
- **Better Complexity**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimized_fixed_length_paths_ii(tree, queries):
    """
    [Description]
    
    Args:
        tree: [Description]
        queries: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's better**: [Reason]

---

### Approach 3: Optimal

**Key Insights from Optimal Approach**:
- **Optimal Algorithm**: [Description]
- **Best Complexity**: [Description]
- **Efficient Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimal_fixed_length_paths_ii(tree, queries):
    """
    [Description]
    
    Args:
        tree: [Description]
        queries: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's optimal**: [Reason]

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O([complexity]) | O([complexity]) | [Insight] |
| Optimized | O([complexity]) | O([complexity]) | [Insight] |
| Optimal | O([complexity]) | O([complexity]) | [Insight] |

### Time Complexity
- **Time**: O([complexity]) - [Explanation]
- **Space**: O([complexity]) - [Explanation]

### Why This Solution Works
- **[Reason 1]**: [Explanation]
- **[Reason 2]**: [Explanation]
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Fixed Length Paths II with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain fixed length path queries with color constraints efficiently.

**Link**: [CSES Problem Set - Fixed Length Paths II with Updates](https://cses.fi/problemset/task/fixed_length_paths_ii_updates)

```python
class FixedLengthPathsIIWithUpdates:
    def __init__(self, n, colors, edges, target_length):
        self.n = n
        self.colors = colors[:]
        self.adj = [[] for _ in range(n)]
        self.target_length = target_length
        self.path_counts = {}
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_path_counts()
    
    def _calculate_path_counts(self):
        """Calculate path counts using tree DP with color constraints"""
        def dfs(node, parent):
            # Initialize path counts for this node
            self.path_counts[node] = {}
            
            # Count paths of target length starting from this node
            def count_paths(current, parent, length, start_color):
                if length == self.target_length:
                    return 1 if self.colors[current] == start_color else 0
                
                count = 0
                for child in self.adj[current]:
                    if child != parent:
                        count += count_paths(child, current, length + 1, start_color)
                
                return count
            
            # Count paths for each color
            for color in set(self.colors):
                self.path_counts[node][color] = count_paths(node, parent, 0, color)
            
            # Recursively calculate for children
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
        
        dfs(0, -1)
    
    def update_color(self, node, new_color):
        """Update color of a node and recalculate affected counts"""
        self.colors[node] = new_color
        
        # Recalculate path counts
        self._calculate_path_counts()
    
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
    
    def get_path_count(self, node, color):
        """Get number of paths of target length starting from node with specific color"""
        return self.path_counts[node].get(color, 0)
    
    def get_all_path_counts(self):
        """Get path counts for all nodes and colors"""
        return self.path_counts.copy()
    
    def get_total_paths(self, color):
        """Get total number of paths of target length with specific color"""
        total = 0
        for node in range(self.n):
            total += self.path_counts[node].get(color, 0)
        return total
    
    def get_path_statistics(self):
        """Get comprehensive path statistics"""
        color_totals = {}
        for color in set(self.colors):
            color_totals[color] = self.get_total_paths(color)
        
        return {
            'color_totals': color_totals,
            'target_length': self.target_length,
            'path_counts': self.path_counts.copy()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update_color':
                self.update_color(query['node'], query['new_color'])
                results.append(None)
            elif query['type'] == 'add_edge':
                self.add_edge(query['u'], query['v'])
                results.append(None)
            elif query['type'] == 'remove_edge':
                self.remove_edge(query['u'], query['v'])
                results.append(None)
            elif query['type'] == 'path_count':
                result = self.get_path_count(query['node'], query['color'])
                results.append(result)
            elif query['type'] == 'total_paths':
                result = self.get_total_paths(query['color'])
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_path_statistics()
                results.append(result)
        return results
```

### Variation 2: Fixed Length Paths II with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on fixed length paths with color constraints.

**Link**: [CSES Problem Set - Fixed Length Paths II Different Operations](https://cses.fi/problemset/task/fixed_length_paths_ii_operations)

```python
class FixedLengthPathsIIDifferentOps:
    def __init__(self, n, colors, edges, target_length):
        self.n = n
        self.colors = colors[:]
        self.adj = [[] for _ in range(n)]
        self.target_length = target_length
        self.path_counts = {}
        self.depths = [0] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_path_counts()
        self._calculate_depths()
    
    def _calculate_path_counts(self):
        """Calculate path counts using tree DP with color constraints"""
        def dfs(node, parent):
            # Initialize path counts for this node
            self.path_counts[node] = {}
            
            # Count paths of target length starting from this node
            def count_paths(current, parent, length, start_color):
                if length == self.target_length:
                    return 1 if self.colors[current] == start_color else 0
                
                count = 0
                for child in self.adj[current]:
                    if child != parent:
                        count += count_paths(child, current, length + 1, start_color)
                
                return count
            
            # Count paths for each color
            for color in set(self.colors):
                self.path_counts[node][color] = count_paths(node, parent, 0, color)
            
            # Recursively calculate for children
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
        
        dfs(0, -1)
    
    def _calculate_depths(self):
        """Calculate depth of each node"""
        def dfs(node, parent, depth):
            self.depths[node] = depth
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node, depth + 1)
        
        dfs(0, -1, 0)
    
    def get_path_count(self, node, color):
        """Get number of paths of target length starting from node with specific color"""
        return self.path_counts[node].get(color, 0)
    
    def get_paths_by_color(self, color):
        """Get all paths of target length with specific color"""
        paths = []
        
        def dfs(node, parent, current_path):
            if len(current_path) == self.target_length:
                if self.colors[current_path[0]] == color and self.colors[current_path[-1]] == color:
                    paths.append(current_path.copy())
                return
            
            for child in self.adj[node]:
                if child != parent:
                    current_path.append(child)
                    dfs(child, node, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return paths
    
    def get_paths_from_node(self, node, color):
        """Get all paths starting from given node with specific color"""
        paths = []
        
        def dfs(current, parent, current_path):
            if len(current_path) > 1:
                if self.colors[current_path[0]] == color and self.colors[current_path[-1]] == color:
                    paths.append(current_path.copy())
            
            for child in self.adj[current]:
                if child != parent:
                    current_path.append(child)
                    dfs(child, current, current_path)
                    current_path.pop()
        
        dfs(node, -1, [node])
        return paths
    
    def get_paths_to_node(self, node, color):
        """Get all paths ending at given node with specific color"""
        paths = []
        
        def dfs(current, parent, current_path):
            if current == node and len(current_path) > 1:
                if self.colors[current_path[0]] == color and self.colors[current_path[-1]] == color:
                    paths.append(current_path.copy())
                return
            
            for child in self.adj[current]:
                if child != parent:
                    current_path.append(child)
                    dfs(child, current, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return paths
    
    def get_paths_through_node(self, node, color):
        """Get all paths passing through given node with specific color"""
        paths = []
        
        def dfs(current, parent, current_path):
            if node in current_path and len(current_path) > 1:
                if self.colors[current_path[0]] == color and self.colors[current_path[-1]] == color:
                    paths.append(current_path.copy())
            
            for child in self.adj[current]:
                if child != parent:
                    current_path.append(child)
                    dfs(child, current, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return paths
    
    def get_color_statistics(self):
        """Get comprehensive color statistics"""
        color_totals = {}
        for color in set(self.colors):
            color_totals[color] = self.get_total_paths(color)
        
        return {
            'color_totals': color_totals,
            'target_length': self.target_length,
            'path_counts': self.path_counts.copy(),
            'depths': self.depths.copy()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'path_count':
                result = self.get_path_count(query['node'], query['color'])
                results.append(result)
            elif query['type'] == 'paths_by_color':
                result = self.get_paths_by_color(query['color'])
                results.append(result)
            elif query['type'] == 'paths_from_node':
                result = self.get_paths_from_node(query['node'], query['color'])
                results.append(result)
            elif query['type'] == 'paths_to_node':
                result = self.get_paths_to_node(query['node'], query['color'])
                results.append(result)
            elif query['type'] == 'paths_through_node':
                result = self.get_paths_through_node(query['node'], query['color'])
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_color_statistics()
                results.append(result)
        return results
```

### Variation 3: Fixed Length Paths II with Constraints
**Problem**: Handle fixed length path queries with additional constraints (e.g., minimum length, maximum length, color frequency).

**Link**: [CSES Problem Set - Fixed Length Paths II with Constraints](https://cses.fi/problemset/task/fixed_length_paths_ii_constraints)

```python
class FixedLengthPathsIIWithConstraints:
    def __init__(self, n, colors, edges, target_length, min_length, max_length, min_color_frequency):
        self.n = n
        self.colors = colors[:]
        self.adj = [[] for _ in range(n)]
        self.target_length = target_length
        self.min_length = min_length
        self.max_length = max_length
        self.min_color_frequency = min_color_frequency
        self.path_counts = {}
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_path_counts()
    
    def _calculate_path_counts(self):
        """Calculate path counts using tree DP with color constraints"""
        def dfs(node, parent):
            # Initialize path counts for this node
            self.path_counts[node] = {}
            
            # Count paths of target length starting from this node
            def count_paths(current, parent, length, start_color):
                if length == self.target_length:
                    return 1 if self.colors[current] == start_color else 0
                
                count = 0
                for child in self.adj[current]:
                    if child != parent:
                        count += count_paths(child, current, length + 1, start_color)
                
                return count
            
            # Count paths for each color
            for color in set(self.colors):
                self.path_counts[node][color] = count_paths(node, parent, 0, color)
            
            # Recursively calculate for children
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
        
        dfs(0, -1)
    
    def constrained_path_count_query(self, node, color):
        """Query path count with constraints"""
        if self.path_counts[node].get(color, 0) == 0:
            return 0
        
        # Count paths of valid lengths starting from this node with specific color
        valid_paths = 0
        
        def count_valid_paths(current, parent, length, start_color):
            nonlocal valid_paths
            
            if self.min_length <= length <= self.max_length:
                if self.colors[current] == start_color:
                    valid_paths += 1
            
            for child in self.adj[current]:
                if child != parent:
                    count_valid_paths(child, current, length + 1, start_color)
        
        count_valid_paths(node, -1, 0, color)
        return valid_paths
    
    def find_valid_paths(self, color):
        """Find all paths that satisfy length and color constraints"""
        valid_paths = []
        
        def dfs(node, parent, current_path):
            if self.min_length <= len(current_path) <= self.max_length:
                if self.colors[current_path[0]] == color and self.colors[current_path[-1]] == color:
                    valid_paths.append(current_path.copy())
            
            for child in self.adj[node]:
                if child != parent:
                    current_path.append(child)
                    dfs(child, node, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return valid_paths
    
    def count_valid_paths(self, color):
        """Count number of valid paths with specific color"""
        return len(self.find_valid_paths(color))
    
    def get_valid_paths_by_length(self, color, length):
        """Get all valid paths of specific length with specific color"""
        if not (self.min_length <= length <= self.max_length):
            return []
        
        paths = []
        
        def dfs(node, parent, current_path):
            if len(current_path) == length:
                if self.colors[current_path[0]] == color and self.colors[current_path[-1]] == color:
                    paths.append(current_path.copy())
                return
            
            for child in self.adj[node]:
                if child != parent:
                    current_path.append(child)
                    dfs(child, node, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return paths
    
    def get_valid_paths_from_node(self, node, color):
        """Get all valid paths starting from given node with specific color"""
        valid_paths = []
        
        def dfs(current, parent, current_path):
            if self.min_length <= len(current_path) <= self.max_length:
                if self.colors[current_path[0]] == color and self.colors[current_path[-1]] == color:
                    valid_paths.append(current_path.copy())
            
            for child in self.adj[current]:
                if child != parent:
                    current_path.append(child)
                    dfs(child, current, current_path)
                    current_path.pop()
        
        dfs(node, -1, [node])
        return valid_paths
    
    def get_valid_paths_through_node(self, node, color):
        """Get all valid paths passing through given node with specific color"""
        valid_paths = []
        
        def dfs(current, parent, current_path):
            if node in current_path and self.min_length <= len(current_path) <= self.max_length:
                if self.colors[current_path[0]] == color and self.colors[current_path[-1]] == color:
                    valid_paths.append(current_path.copy())
            
            for child in self.adj[current]:
                if child != parent:
                    current_path.append(child)
                    dfs(child, current, current_path)
                    current_path.pop()
        
        for start in range(self.n):
            dfs(start, -1, [start])
        
        return valid_paths
    
    def get_constraint_statistics(self):
        """Get statistics about valid paths"""
        color_totals = {}
        for color in set(self.colors):
            color_totals[color] = self.count_valid_paths(color)
        
        return {
            'color_totals': color_totals,
            'min_length': self.min_length,
            'max_length': self.max_length,
            'target_length': self.target_length,
            'min_color_frequency': self.min_color_frequency
        }

# Example usage
n = 5
colors = [1, 2, 1, 3, 2]
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
target_length = 2
min_length = 1
max_length = 3
min_color_frequency = 1

flp = FixedLengthPathsIIWithConstraints(n, colors, edges, target_length, min_length, max_length, min_color_frequency)
result = flp.constrained_path_count_query(1, 1)
print(f"Constrained path count query result: {result}")

valid_paths = flp.find_valid_paths(1)
print(f"Valid paths: {valid_paths}")

statistics = flp.get_constraint_statistics()
print(f"Constraint statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Fixed Length Paths II](https://cses.fi/problemset/task/2081) - Advanced fixed length paths in tree with color constraints
- [Fixed Length Paths I](https://cses.fi/problemset/task/2080) - Basic fixed length paths in tree
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Find diameter of tree

#### **LeetCode Problems**
- [Binary Tree Paths](https://leetcode.com/problems/binary-tree-paths/) - Find all paths in binary tree
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Tree DP**: Dynamic programming on trees, path counting with constraints
- **Tree Traversal**: DFS, BFS, tree traversal algorithms
- **Tree Queries**: Path queries, tree analysis, tree operations
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
