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

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tree algorithms, DFS, BFS, tree DP, centroid decomposition
- **Data Structures**: Trees, graphs, segment trees, binary indexed trees
- **Mathematical Concepts**: Tree theory, graph theory, dynamic programming
- **Programming Skills**: Tree traversal, algorithm implementation
- **Related Problems**: Other tree algorithm problems in this section

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
