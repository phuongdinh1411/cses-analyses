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
