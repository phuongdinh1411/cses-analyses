---
layout: simple
title: "Distinct Colors"
permalink: /problem_soulutions/tree_algorithms/distinct_colors_analysis
---

# Distinct Colors

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand tree algorithms and tree traversal techniques
- Apply efficient tree processing algorithms
- Implement advanced tree data structures and algorithms
- Optimize tree operations for large inputs
- Handle edge cases in tree problems

## 📋 Problem Description

Given a tree with n nodes, each node has a color. For each node, find the number of distinct colors in its subtree.

**Input**: 
- First line: n (number of nodes)
- Next n lines: colors of nodes 1 to n
- Next n-1 lines: edges of the tree

**Output**: 
- n lines: number of distinct colors in subtree of each node

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ color ≤ n

**Example**:
```
Input:
5
1 2 1 2 3
1 2
2 3
2 4
4 5

Output:
3
3
1
2
1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each node, perform DFS to collect all colors in its subtree
2. Count distinct colors using a set
3. Return the count for each node

**Implementation**:
```python
def brute_force_distinct_colors(n, colors, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    results = []
    
    def dfs_collect_colors(node, parent):
        color_set = set()
        color_set.add(colors[node - 1])
        
        for child in graph[node]:
            if child != parent:
                child_colors = dfs_collect_colors(child, node)
                color_set.update(child_colors)
        
        return color_set
    
    for node in range(1, n + 1):
        subtree_colors = dfs_collect_colors(node, -1)
        results.append(len(subtree_colors))
    
    return results
```

**Analysis**:
- **Time**: O(n²) - For each node, DFS takes O(n) time
- **Space**: O(n) - Recursion stack and color sets
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Tree DP
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to merge color sets from children
2. For each node, combine its color with children's color sets
3. Use set union operations to merge efficiently

**Implementation**:
```python
def optimized_distinct_colors(n, colors, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    results = [0] * (n + 1)
    
    def dfs(node, parent):
        color_set = {colors[node - 1]}
        
        for child in graph[node]:
            if child != parent:
                child_colors = dfs(child, node)
                color_set.update(child_colors)
        
        results[node] = len(color_set)
        return color_set
    
    dfs(1, -1)
    return results[1:]
```

**Analysis**:
- **Time**: O(n²) - Still O(n²) due to set operations
- **Space**: O(n) - Recursion stack and color sets
- **Improvement**: More efficient than brute force

### Approach 3: Optimal with Small-to-Large Merging
**Time Complexity**: O(n log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use small-to-large merging technique
2. Always merge smaller set into larger set
3. This ensures each element is moved at most O(log n) times

**Implementation**:
```python
def optimal_distinct_colors(n, colors, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    results = [0] * (n + 1)
    
    def dfs(node, parent):
        # Start with current node's color
        color_set = {colors[node - 1]}
        
        for child in graph[node]:
            if child != parent:
                child_colors = dfs(child, node)
                
                # Small-to-large merging
                if len(color_set) < len(child_colors):
                    color_set, child_colors = child_colors, color_set
                
                color_set.update(child_colors)
        
        results[node] = len(color_set)
        return color_set
    
    dfs(1, -1)
    return results[1:]
```

**Analysis**:
- **Time**: O(n log n) - Small-to-large merging ensures O(log n) moves per element
- **Space**: O(n) - Recursion stack and color sets
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
    5(3)

Small-to-Large Merging:
1. Node 5: {3} → size 1
2. Node 4: {2} + {3} → {2,3} → size 2
3. Node 3: {1} → size 1
4. Node 2: {2} + {1} + {2,3} → {1,2,3} → size 3
5. Node 1: {1} + {1,2,3} → {1,2,3} → size 3
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | DFS from each node |
| Optimized | O(n²) | O(n) | Tree DP with set merging |
| Optimal | O(n log n) | O(n) | Small-to-large merging |

### Time Complexity
- **Time**: O(n log n) - Small-to-large merging ensures each element is moved at most O(log n) times
- **Space**: O(n) - Recursion stack and color sets

### Why This Solution Works
- **Small-to-Large Merging**: Always merge smaller set into larger set to minimize operations
- **Tree DP**: Use dynamic programming to avoid recomputing subtree information
- **Set Operations**: Efficiently merge color sets using set union operations
- **Optimal Approach**: Small-to-large merging provides the best possible complexity for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Distinct Colors with Dynamic Updates
**Problem**: Handle dynamic updates to node colors and maintain distinct color queries efficiently.

**Link**: [CSES Problem Set - Distinct Colors with Updates](https://cses.fi/problemset/task/distinct_colors_updates)

```python
class DistinctColorsWithUpdates:
    def __init__(self, n, colors, edges):
        self.n = n
        self.colors = colors[:]
        self.adj = [[] for _ in range(n)]
        self.distinct_counts = [0] * n
        self.color_sets = [set() for _ in range(n)]
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_distinct_counts()
    
    def _calculate_distinct_counts(self):
        """Calculate distinct color counts using small-to-large merging"""
        def dfs(node, parent):
            # Initialize with current node's color
            self.color_sets[node].add(self.colors[node])
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    
                    # Small-to-large merging
                    if len(self.color_sets[child]) > len(self.color_sets[node]):
                        self.color_sets[node], self.color_sets[child] = self.color_sets[child], self.color_sets[node]
                    
                    # Merge smaller set into larger set
                    self.color_sets[node].update(self.color_sets[child])
            
            self.distinct_counts[node] = len(self.color_sets[node])
        
        dfs(0, -1)
    
    def update_color(self, node, new_color):
        """Update color of a node and recalculate affected counts"""
        old_color = self.colors[node]
        self.colors[node] = new_color
        
        # Recalculate distinct counts
        self._calculate_distinct_counts()
    
    def get_distinct_count(self, node):
        """Get number of distinct colors in subtree rooted at node"""
        return self.distinct_counts[node]
    
    def get_all_distinct_counts(self):
        """Get distinct color counts for all nodes"""
        return self.distinct_counts.copy()
    
    def get_color_set(self, node):
        """Get set of distinct colors in subtree rooted at node"""
        return self.color_sets[node].copy()
    
    def get_max_distinct_count(self):
        """Get maximum distinct color count among all nodes"""
        return max(self.distinct_counts)
    
    def get_min_distinct_count(self):
        """Get minimum distinct color count among all nodes"""
        return min(self.distinct_counts)
    
    def get_color_statistics(self):
        """Get comprehensive color statistics"""
        return {
            'max_distinct_count': self.get_max_distinct_count(),
            'min_distinct_count': self.get_min_distinct_count(),
            'distinct_counts': self.distinct_counts.copy(),
            'total_colors': len(set(self.colors))
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update_color':
                self.update_color(query['node'], query['new_color'])
                results.append(None)
            elif query['type'] == 'distinct_count':
                result = self.get_distinct_count(query['node'])
                results.append(result)
            elif query['type'] == 'all_distinct_counts':
                result = self.get_all_distinct_counts()
                results.append(result)
            elif query['type'] == 'color_set':
                result = self.get_color_set(query['node'])
                results.append(result)
            elif query['type'] == 'max_distinct_count':
                result = self.get_max_distinct_count()
                results.append(result)
            elif query['type'] == 'min_distinct_count':
                result = self.get_min_distinct_count()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_color_statistics()
                results.append(result)
        return results
```

### Variation 2: Distinct Colors with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on distinct colors.

**Link**: [CSES Problem Set - Distinct Colors Different Operations](https://cses.fi/problemset/task/distinct_colors_operations)

```python
class DistinctColorsDifferentOps:
    def __init__(self, n, colors, edges):
        self.n = n
        self.colors = colors[:]
        self.adj = [[] for _ in range(n)]
        self.distinct_counts = [0] * n
        self.color_sets = [set() for _ in range(n)]
        self.color_frequencies = [{} for _ in range(n)]
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_distinct_counts()
        self._calculate_color_frequencies()
    
    def _calculate_distinct_counts(self):
        """Calculate distinct color counts using small-to-large merging"""
        def dfs(node, parent):
            # Initialize with current node's color
            self.color_sets[node].add(self.colors[node])
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    
                    # Small-to-large merging
                    if len(self.color_sets[child]) > len(self.color_sets[node]):
                        self.color_sets[node], self.color_sets[child] = self.color_sets[child], self.color_sets[node]
                    
                    # Merge smaller set into larger set
                    self.color_sets[node].update(self.color_sets[child])
            
            self.distinct_counts[node] = len(self.color_sets[node])
        
        dfs(0, -1)
    
    def _calculate_color_frequencies(self):
        """Calculate color frequencies in each subtree"""
        def dfs(node, parent):
            # Initialize with current node's color
            self.color_frequencies[node][self.colors[node]] = 1
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    
                    # Merge color frequencies
                    for color, freq in self.color_frequencies[child].items():
                        self.color_frequencies[node][color] = self.color_frequencies[node].get(color, 0) + freq
        
        dfs(0, -1)
    
    def get_distinct_count(self, node):
        """Get number of distinct colors in subtree rooted at node"""
        return self.distinct_counts[node]
    
    def get_color_set(self, node):
        """Get set of distinct colors in subtree rooted at node"""
        return self.color_sets[node].copy()
    
    def get_color_frequency(self, node, color):
        """Get frequency of specific color in subtree rooted at node"""
        return self.color_frequencies[node].get(color, 0)
    
    def get_most_frequent_color(self, node):
        """Get most frequent color in subtree rooted at node"""
        if not self.color_frequencies[node]:
            return None
        
        return max(self.color_frequencies[node], key=self.color_frequencies[node].get)
    
    def get_least_frequent_color(self, node):
        """Get least frequent color in subtree rooted at node"""
        if not self.color_frequencies[node]:
            return None
        
        return min(self.color_frequencies[node], key=self.color_frequencies[node].get)
    
    def get_color_distribution(self, node):
        """Get color distribution in subtree rooted at node"""
        return self.color_frequencies[node].copy()
    
    def get_nodes_with_color(self, color):
        """Get all nodes that have specific color"""
        nodes = []
        for i in range(self.n):
            if self.colors[i] == color:
                nodes.append(i)
        return nodes
    
    def get_subtrees_with_color(self, color):
        """Get all subtrees that contain specific color"""
        subtrees = []
        for i in range(self.n):
            if color in self.color_sets[i]:
                subtrees.append(i)
        return subtrees
    
    def get_color_statistics(self):
        """Get comprehensive color statistics"""
        total_colors = len(set(self.colors))
        color_counts = {}
        for color in self.colors:
            color_counts[color] = color_counts.get(color, 0) + 1
        
        return {
            'total_colors': total_colors,
            'max_distinct_count': max(self.distinct_counts),
            'min_distinct_count': min(self.distinct_counts),
            'color_counts': color_counts,
            'distinct_counts': self.distinct_counts.copy()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'distinct_count':
                result = self.get_distinct_count(query['node'])
                results.append(result)
            elif query['type'] == 'color_set':
                result = self.get_color_set(query['node'])
                results.append(result)
            elif query['type'] == 'color_frequency':
                result = self.get_color_frequency(query['node'], query['color'])
                results.append(result)
            elif query['type'] == 'most_frequent_color':
                result = self.get_most_frequent_color(query['node'])
                results.append(result)
            elif query['type'] == 'least_frequent_color':
                result = self.get_least_frequent_color(query['node'])
                results.append(result)
            elif query['type'] == 'color_distribution':
                result = self.get_color_distribution(query['node'])
                results.append(result)
            elif query['type'] == 'nodes_with_color':
                result = self.get_nodes_with_color(query['color'])
                results.append(result)
            elif query['type'] == 'subtrees_with_color':
                result = self.get_subtrees_with_color(query['color'])
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_color_statistics()
                results.append(result)
        return results
```

### Variation 3: Distinct Colors with Constraints
**Problem**: Handle distinct color queries with additional constraints (e.g., minimum frequency, maximum frequency).

**Link**: [CSES Problem Set - Distinct Colors with Constraints](https://cses.fi/problemset/task/distinct_colors_constraints)

```python
class DistinctColorsWithConstraints:
    def __init__(self, n, colors, edges, min_frequency, max_frequency):
        self.n = n
        self.colors = colors[:]
        self.adj = [[] for _ in range(n)]
        self.distinct_counts = [0] * n
        self.color_sets = [set() for _ in range(n)]
        self.color_frequencies = [{} for _ in range(n)]
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_distinct_counts()
        self._calculate_color_frequencies()
    
    def _calculate_distinct_counts(self):
        """Calculate distinct color counts using small-to-large merging"""
        def dfs(node, parent):
            # Initialize with current node's color
            self.color_sets[node].add(self.colors[node])
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    
                    # Small-to-large merging
                    if len(self.color_sets[child]) > len(self.color_sets[node]):
                        self.color_sets[node], self.color_sets[child] = self.color_sets[child], self.color_sets[node]
                    
                    # Merge smaller set into larger set
                    self.color_sets[node].update(self.color_sets[child])
            
            self.distinct_counts[node] = len(self.color_sets[node])
        
        dfs(0, -1)
    
    def _calculate_color_frequencies(self):
        """Calculate color frequencies in each subtree"""
        def dfs(node, parent):
            # Initialize with current node's color
            self.color_frequencies[node][self.colors[node]] = 1
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    
                    # Merge color frequencies
                    for color, freq in self.color_frequencies[child].items():
                        self.color_frequencies[node][color] = self.color_frequencies[node].get(color, 0) + freq
        
        dfs(0, -1)
    
    def constrained_distinct_count_query(self, node):
        """Query distinct count with constraints"""
        if self.distinct_counts[node] == 0:
            return 0
        
        # Count colors that satisfy frequency constraints
        valid_colors = 0
        for color, freq in self.color_frequencies[node].items():
            if self.min_frequency <= freq <= self.max_frequency:
                valid_colors += 1
        
        return valid_colors
    
    def find_valid_colors(self, node):
        """Find all colors that satisfy frequency constraints in subtree"""
        valid_colors = []
        for color, freq in self.color_frequencies[node].items():
            if self.min_frequency <= freq <= self.max_frequency:
                valid_colors.append((color, freq))
        
        return valid_colors
    
    def get_valid_color_sets(self):
        """Get valid color sets for all nodes"""
        valid_sets = []
        for i in range(self.n):
            valid_colors = self.find_valid_colors(i)
            valid_sets.append([color for color, _ in valid_colors])
        
        return valid_sets
    
    def count_valid_colors(self, node):
        """Count number of valid colors in subtree"""
        return len(self.find_valid_colors(node))
    
    def get_nodes_with_valid_colors(self):
        """Get all nodes that have valid colors"""
        valid_nodes = []
        for i in range(self.n):
            if self.count_valid_colors(i) > 0:
                valid_nodes.append(i)
        
        return valid_nodes
    
    def get_subtrees_with_color_frequency(self, color, frequency):
        """Get all subtrees with specific color frequency"""
        subtrees = []
        for i in range(self.n):
            if (color in self.color_frequencies[i] and 
                self.color_frequencies[i][color] == frequency):
                subtrees.append(i)
        
        return subtrees
    
    def get_constraint_statistics(self):
        """Get statistics about valid colors"""
        valid_nodes = self.get_nodes_with_valid_colors()
        valid_sets = self.get_valid_color_sets()
        
        return {
            'valid_nodes_count': len(valid_nodes),
            'min_frequency': self.min_frequency,
            'max_frequency': self.max_frequency,
            'valid_nodes': valid_nodes,
            'valid_sets': valid_sets
        }

# Example usage
n = 5
colors = [1, 2, 1, 3, 2]
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
min_frequency = 1
max_frequency = 2

dc = DistinctColorsWithConstraints(n, colors, edges, min_frequency, max_frequency)
result = dc.constrained_distinct_count_query(1)
print(f"Constrained distinct count query result: {result}")

valid_colors = dc.find_valid_colors(1)
print(f"Valid colors: {valid_colors}")

statistics = dc.get_constraint_statistics()
print(f"Constraint statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Distinct Colors](https://cses.fi/problemset/task/1139) - Basic distinct colors in tree
- [Tree Distances I](https://cses.fi/problemset/task/1132) - Distance queries in tree
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Find diameter of tree

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Small-to-Large Merging**: Efficient set merging, tree DP optimization
- **Tree DP**: Dynamic programming on trees, subtree calculations
- **Tree Queries**: Subtree queries, tree analysis, tree operations
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
