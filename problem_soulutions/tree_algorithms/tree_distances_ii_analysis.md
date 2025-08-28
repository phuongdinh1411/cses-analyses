---
layout: simple
title: "Tree Distances II
permalink: /problem_soulutions/tree_algorithms/tree_distances_ii_analysis/
---

# Tree Distances II

## Problem Statement
Given a tree with n nodes, find for each node the sum of distances to all other nodes.

### Input
The first input line has an integer n: the number of nodes. The nodes are numbered 1,2,…,n.
Then, there are n−1 lines describing the edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print n integers: the sum of distances from each node to all other nodes.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
5
1 2
1 3
3 4
3 5

Output:
6 9 5 8 8
```

## Solution Progression

### Approach 1: Multiple BFS - O(n²)
**Description**: Use BFS from each node to find the sum of distances to all other nodes.

```python
from collections import deque

def tree_distances_multiple_bfs(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    def bfs(start):
        # BFS to find distances from start node
        distances = [-1] * (n + 1)
        queue = deque([start])
        distances[start] = 0
        
        while queue:
            node = queue.popleft()
            for neighbor in tree[node]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        
        # Return sum of distances
        return sum(distances[1:])
    
    # Calculate sum of distances for each node
    result = []
    for i in range(1, n + 1):
        result.append(bfs(i))
    
    return result
```

**Why this is inefficient**: Multiple BFS approach has quadratic time complexity.

### Improvement 1: Rerooting with Subtree Sizes - O(n)
**Description**: Use rerooting technique with subtree sizes to calculate distance sums efficiently.

```python
def tree_distances_rerooting(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Arrays to store subtree sizes and distance sums
    subtree_sizes = [0] * (n + 1)
    distance_sums = [0] * (n + 1)
    
    def dfs1(node, parent):
        # First DFS: calculate subtree sizes
        subtree_sizes[node] = 1
        for child in tree[node]:
            if child != parent:
                subtree_sizes[node] += dfs1(child, node)
        return subtree_sizes[node]
    
    def dfs2(node, parent, dist_sum):
        # Second DFS: calculate distance sums using rerooting
        distance_sums[node] = dist_sum
        
        for child in tree[node]:
            if child != parent:
                # When moving root from node to child:"
                # - Nodes in child's subtree get closer by 1
                # - Nodes outside child's subtree get farther by 1
                nodes_in_subtree = subtree_sizes[child]
                nodes_outside_subtree = n - nodes_in_subtree
                
                new_dist_sum = dist_sum - nodes_in_subtree + nodes_outside_subtree
                dfs2(child, node, new_dist_sum)
    
    # Calculate initial distance sum from root
    def calculate_initial_sum(node, parent, depth):
        total = depth
        for child in tree[node]:
            if child != parent:
                total += calculate_initial_sum(child, node, depth + 1)
        return total
    
    # Start rerooting from root
    dfs1(1, -1)
    initial_sum = calculate_initial_sum(1, -1, 0)
    dfs2(1, -1, initial_sum)
    
    return distance_sums[1:n + 1]
```

**Why this improvement works**: Rerooting technique efficiently calculates distance sums for all nodes using subtree sizes.

### Improvement 2: Single DFS with Height and Count - O(n)
**Description**: Use a single DFS to calculate heights and node counts for efficient distance calculation.

```python
def tree_distances_single_dfs(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Arrays to store subtree information
    subtree_sizes = [0] * (n + 1)
    distance_sums = [0] * (n + 1)
    
    def dfs(node, parent, depth):
        # Calculate subtree size and initial distance sum
        subtree_sizes[node] = 1
        total_distance = depth
        
        for child in tree[node]:
            if child != parent:
                child_distance = dfs(child, node, depth + 1)
                subtree_sizes[node] += subtree_sizes[child]
                total_distance += child_distance
        
        return total_distance
    
    def reroot(node, parent, current_sum):
        # Reroot the tree and update distance sums
        distance_sums[node] = current_sum
        
        for child in tree[node]:
            if child != parent:
                # Calculate new sum when moving root to child
                nodes_in_child = subtree_sizes[child]
                nodes_outside_child = n - nodes_in_child
                new_sum = current_sum - nodes_in_child + nodes_outside_child
                
                # Update subtree sizes for rerooting
                subtree_sizes[node] -= subtree_sizes[child]
                subtree_sizes[child] += subtree_sizes[node]
                
                reroot(child, node, new_sum)
                
                # Restore subtree sizes
                subtree_sizes[child] -= subtree_sizes[node]
                subtree_sizes[node] += subtree_sizes[child]
    
    # Calculate initial distance sum from root
    initial_sum = dfs(1, -1, 0)
    
    # Reroot to calculate sums for all nodes
    reroot(1, -1, initial_sum)
    
    return distance_sums[1:n + 1]
```

**Why this improvement works**: Single DFS with rerooting calculates all distance sums efficiently.

### Alternative: Dynamic Programming with Parent Tracking - O(n)
**Description**: Use dynamic programming with parent tracking for educational purposes.

```python
def tree_distances_dp(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Arrays to store DP results
    dp = [0] * (n + 1)
    subtree_sizes = [0] * (n + 1)
    
    def dfs1(node, parent):
        # First DFS: calculate subtree sizes and initial distances
        subtree_sizes[node] = 1
        dp[node] = 0
        
        for child in tree[node]:
            if child != parent:
                child_dist = dfs1(child, node)
                subtree_sizes[node] += subtree_sizes[child]
                dp[node] += child_dist + subtree_sizes[child]
        
        return dp[node]
    
    def dfs2(node, parent, parent_sum):
        # Second DFS: calculate distance sums for all nodes
        if parent != -1:
            # Calculate distance sum for current node
            nodes_in_subtree = subtree_sizes[node]
            nodes_outside_subtree = n - nodes_in_subtree
            
            # Distance sum = parent's sum - nodes in subtree + nodes outside subtree
            dp[node] = parent_sum - nodes_in_subtree + nodes_outside_subtree
        
        for child in tree[node]:
            if child != parent:
                dfs2(child, node, dp[node])
    
    # Calculate initial distances
    dfs1(1, -1)
    
    # Calculate distance sums for all nodes
    dfs2(1, -1, dp[1])
    
    return dp[1:n + 1]
```

**Why this works**: DP approach uses parent information to calculate distance sums efficiently.

## Final Optimal Solution

```python
n = int(input())
edges = [tuple(map(int, input().split())) for _ in range(n - 1)]

# Build adjacency list
tree = [[] for _ in range(n + 1)]
for a, b in edges:
    tree[a].append(b)
    tree[b].append(a)

# Arrays to store subtree sizes and distance sums
subtree_sizes = [0] * (n + 1)
distance_sums = [0] * (n + 1)

def dfs1(node, parent):
    # First DFS: calculate subtree sizes
    subtree_sizes[node] = 1
    for child in tree[node]:
        if child != parent:
            subtree_sizes[node] += dfs1(child, node)
    return subtree_sizes[node]

def dfs2(node, parent, dist_sum):
    # Second DFS: calculate distance sums using rerooting
    distance_sums[node] = dist_sum
    
    for child in tree[node]:
        if child != parent:
            # When moving root from node to child:
            # - Nodes in child's subtree get closer by 1
            # - Nodes outside child's subtree get farther by 1
            nodes_in_subtree = subtree_sizes[child]
            nodes_outside_subtree = n - nodes_in_subtree
            
            new_dist_sum = dist_sum - nodes_in_subtree + nodes_outside_subtree
            dfs2(child, node, new_dist_sum)

# Calculate initial distance sum from root
def calculate_initial_sum(node, parent, depth):
    total = depth
    for child in tree[node]:
        if child != parent:
            total += calculate_initial_sum(child, node, depth + 1)
    return total

# Start rerooting from root
dfs1(1, -1)
initial_sum = calculate_initial_sum(1, -1, 0)
dfs2(1, -1, initial_sum)

print(*distance_sums[1:n + 1])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Multiple BFS | O(n²) | O(n) | Brute force approach |
| Rerooting | O(n) | O(n) | Use subtree sizes |
| Single DFS | O(n) | O(n) | Efficient rerooting |
| Dynamic Programming | O(n) | O(n) | Parent-based calculation |

## Key Insights for Other Problems

### 1. **Tree Distance Sum Problems**
**Principle**: Use rerooting technique with subtree sizes to calculate distance sums efficiently.
**Applicable to**:
- Tree distance sum problems
- Graph algorithms
- Tree algorithms
- Algorithm design

**Example Problems**:
- Tree distance sum problems
- Graph algorithms
- Tree algorithms
- Algorithm design

### 2. **Rerooting Technique**
**Principle**: Use rerooting to calculate properties for all nodes efficiently.
**Applicable to**:
- Tree algorithms
- Dynamic programming on trees
- Algorithm design
- Problem solving

**Example Problems**:
- Tree algorithms
- Dynamic programming on trees
- Algorithm design
- Problem solving

### 3. **Subtree Size Calculations**
**Principle**: Use subtree sizes to calculate distance changes during rerooting.
**Applicable to**:
- Tree algorithms
- Dynamic programming on trees
- Algorithm design
- Problem solving

**Example Problems**:
- Tree algorithms
- Dynamic programming on trees
- Algorithm design
- Problem solving

### 4. **Two-Pass Algorithms**
**Principle**: Use two passes to calculate initial values and then update for all nodes.
**Applicable to**:
- Tree algorithms
- Graph algorithms
- Algorithm design
- Problem solving

**Example Problems**:
- Tree algorithms
- Graph algorithms
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **Rerooting Pattern**
```python
def rerooting_distances(tree, n):
    subtree_sizes = [0] * (n + 1)
    distance_sums = [0] * (n + 1)
    
    def dfs1(node, parent):
        subtree_sizes[node] = 1
        for child in tree[node]:
            if child != parent:
                subtree_sizes[node] += dfs1(child, node)
        return subtree_sizes[node]
    
    def dfs2(node, parent, dist_sum):
        distance_sums[node] = dist_sum
        
        for child in tree[node]:
            if child != parent:
                nodes_in_subtree = subtree_sizes[child]
                nodes_outside_subtree = n - nodes_in_subtree
                new_dist_sum = dist_sum - nodes_in_subtree + nodes_outside_subtree
                dfs2(child, node, new_dist_sum)
    
    dfs1(1, -1)
    initial_sum = calculate_initial_sum(1, -1, 0)
    dfs2(1, -1, initial_sum)
    return distance_sums[1:n + 1]
```

### 2. **Subtree Size Pattern**
```python
def subtree_size_calculation(tree, n):
    subtree_sizes = [0] * (n + 1)
    
    def dfs(node, parent):
        subtree_sizes[node] = 1
        for child in tree[node]:
            if child != parent:
                subtree_sizes[node] += dfs(child, node)
        return subtree_sizes[node]
    
    dfs(1, -1)
    return subtree_sizes
```

### 3. **Distance Sum Pattern**
```python
def distance_sum_calculation(tree, n):
    def calculate_initial_sum(node, parent, depth):
        total = depth
        for child in tree[node]:
            if child != parent:
                total += calculate_initial_sum(child, node, depth + 1)
        return total
    
    return calculate_initial_sum(1, -1, 0)
```

## Edge Cases to Remember

1. **Single node**: Tree with only one node (sum = 0)
2. **Linear tree**: Tree with no branching
3. **Star tree**: Tree with one central node
4. **Perfect binary tree**: Balanced tree structure
5. **Large trees**: Handle deep recursion properly

## Problem-Solving Framework

1. **Identify distance sum nature**: This is a tree distance sum problem
2. **Use rerooting technique**: Calculate sums for all nodes efficiently
3. **Calculate subtree sizes**: Use subtree sizes for distance updates
4. **Apply rerooting formula**: Update distances when moving root
5. **Return result**: Return distance sums for all nodes

---

*This analysis shows how to efficiently calculate distance sums in trees using rerooting technique.* 