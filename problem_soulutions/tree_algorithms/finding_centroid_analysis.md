---
layout: simple
title: "Finding Centroid"
permalink: /problem_soulutions/tree_algorithms/finding_centroid_analysis
---

# Finding Centroid

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

Given a tree with n nodes, find the centroid of the tree. A centroid is a node such that when removed, the tree breaks into components of size at most n/2.

**Input**: 
- First line: n (number of nodes)
- Next n-1 lines: edges of the tree

**Output**: 
- The centroid node (if multiple centroids exist, output any one)

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- Tree is connected

**Example**:
```
Input:
5
1 2
2 3
2 4
4 5

Output:
2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each node, remove it and check if all remaining components have size ≤ n/2
2. Use DFS to find component sizes after removal
3. Return the first node that satisfies the centroid condition

**Implementation**:
```python
def brute_force_finding_centroid(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def get_component_sizes(node_to_remove):
        visited = set()
        component_sizes = []
        
        def dfs(node, parent):
            if node in visited or node == node_to_remove:
                return 0
            visited.add(node)
            size = 1
            for child in graph[node]:
                if child != parent:
                    size += dfs(child, node)
            return size
        
        for node in range(1, n + 1):
            if node not in visited and node != node_to_remove:
                size = dfs(node, -1)
                component_sizes.append(size)
        
        return component_sizes
    
    for node in range(1, n + 1):
        component_sizes = get_component_sizes(node)
        if all(size <= n // 2 for size in component_sizes):
            return node
    
    return -1
```

**Analysis**:
- **Time**: O(n²) - For each node, DFS takes O(n) time
- **Space**: O(n) - Recursion stack and visited set
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Tree DP
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use tree DP to compute subtree sizes for each node
2. For each node, check if removing it creates components of size ≤ n/2
3. Use the subtree size information to efficiently check centroid condition

**Implementation**:
```python
def optimized_finding_centroid(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    subtree_sizes = [0] * (n + 1)
    
    def dfs(node, parent):
        subtree_sizes[node] = 1
        for child in graph[node]:
            if child != parent:
                subtree_sizes[node] += dfs(child, node)
        return subtree_sizes[node]
    
    dfs(1, -1)
    
    def is_centroid(node):
        for child in graph[node]:
            if subtree_sizes[child] < subtree_sizes[node]:
                if subtree_sizes[child] > n // 2:
                    return False
        return subtree_sizes[node] <= n // 2
    
    for node in range(1, n + 1):
        if is_centroid(node):
            return node
    
    return -1
```

**Analysis**:
- **Time**: O(n) - Single DFS pass
- **Space**: O(n) - Recursion stack and subtree sizes array
- **Improvement**: Much more efficient than brute force

### Approach 3: Optimal with Centroid Finding Algorithm
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use the standard centroid finding algorithm
2. Start from any node and move towards the largest subtree
3. Continue until we find a node where all subtrees have size ≤ n/2

**Implementation**:
```python
def optimal_finding_centroid(n, edges):
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def find_centroid():
        # Start from node 1
        current = 1
        parent = -1
        
        while True:
            # Find the largest subtree
            max_subtree_size = 0
            max_subtree_node = -1
            
            for child in graph[current]:
                if child != parent:
                    # Calculate subtree size
                    subtree_size = 0
                    def dfs_size(node, par):
                        nonlocal subtree_size
                        subtree_size = 1
                        for grandchild in graph[node]:
                            if grandchild != par:
                                subtree_size += dfs_size(grandchild, node)
                        return subtree_size
                    
                    size = dfs_size(child, current)
                    if size > max_subtree_size:
                        max_subtree_size = size
                        max_subtree_node = child
            
            # If largest subtree has size ≤ n/2, current is centroid
            if max_subtree_size <= n // 2:
                return current
            
            # Move towards the largest subtree
            parent = current
            current = max_subtree_node
    
    return find_centroid()
```

**Analysis**:
- **Time**: O(n) - At most O(n) moves, each move takes O(degree) time
- **Space**: O(n) - Recursion stack
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

Centroid Finding Process:
1. Start at node 1
2. Largest subtree: {2,3,4,5} (size 4 > 5/2)
3. Move to node 2
4. Largest subtree: {4,5} (size 2 ≤ 5/2)
5. Node 2 is the centroid
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check each node by removing it |
| Optimized | O(n) | O(n) | Tree DP with subtree sizes |
| Optimal | O(n) | O(n) | Centroid finding algorithm |

### Time Complexity
- **Time**: O(n) - Single DFS pass to find centroid
- **Space**: O(n) - Recursion stack and subtree sizes array

### Why This Solution Works
- **Centroid Property**: A centroid always exists in any tree
- **Tree DP**: Use dynamic programming to compute subtree sizes efficiently
- **Centroid Finding**: Move towards the largest subtree until centroid is found
- **Optimal Approach**: The centroid finding algorithm provides the most efficient solution
