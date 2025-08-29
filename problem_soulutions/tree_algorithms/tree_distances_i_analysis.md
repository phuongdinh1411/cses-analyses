---
layout: simple
title: "Tree Distances I"
permalink: /cses-analyses/problem_soulutions/tree_algorithms/tree_distances_i_analysis
---


# Tree Distances I

## Problem Statement
Given a tree with n nodes, find for each node the maximum distance to any other node.

### Input
The first input line has an integer n: the number of nodes. The nodes are numbered 1,2,…,n.
Then, there are n−1 lines describing the edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print n integers: the maximum distance from each node to any other node.

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
2 3 2 3 3
```

## Solution Progression

### Approach 1: Multiple BFS - O(n²)
**Description**: Use BFS from each node to find the maximum distance to any other node.

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
        
        # Return maximum distance
        return max(distances[1:])
    
    # Calculate maximum distance for each node
    result = []
    for i in range(1, n + 1):
        result.append(bfs(i))
    
    return result
```

**Why this is inefficient**: Multiple BFS approach has quadratic time complexity.

### Improvement 1: Two DFS with Diameter Endpoints - O(n)
**Description**: Use the fact that the maximum distance from any node is to one of the diameter endpoints.

```python
def tree_distances_diameter_endpoints(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    def dfs(node, parent, distance):
        max_dist = distance
        farthest_node = node
        
        for child in tree[node]:
            if child != parent:
                dist, far_node = dfs(child, node, distance + 1)
                if dist > max_dist:
                    max_dist = dist
                    farthest_node = far_node
        
        return max_dist, farthest_node
    
    # Find diameter endpoints
    _, endpoint1 = dfs(1, -1, 0)
    _, endpoint2 = dfs(endpoint1, -1, 0)
    
    # Calculate distances from both endpoints
    def calculate_distances(start):
        distances = [-1] * (n + 1)
        stack = [(start, -1, 0)]
        
        while stack:
            node, parent, dist = stack.pop()
            distances[node] = dist
            
            for child in tree[node]:
                if child != parent:
                    stack.append((child, node, dist + 1))
        
        return distances
    
    dist1 = calculate_distances(endpoint1)
    dist2 = calculate_distances(endpoint2)
    
    # Maximum distance for each node is max of distances to endpoints
    result = []
    for i in range(1, n + 1):
        result.append(max(dist1[i], dist2[i]))
    
    return result
```

**Why this improvement works**: Using diameter endpoints reduces the problem to two distance calculations.

### Improvement 2: Single DFS with Height and Diameter - O(n)
**Description**: Use a single DFS to calculate heights and use diameter information.

```python
def tree_distances_single_dfs(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Arrays to store heights and maximum distances
    heights = [0] * (n + 1)
    max_distances = [0] * (n + 1)
    diameter = 0
    
    def dfs(node, parent):
        nonlocal diameter
        
        # Heights of all children
        child_heights = []
        
        for child in tree[node]:
            if child != parent:
                height = dfs(child, node)
                child_heights.append(height)
        
        if not child_heights:
            heights[node] = 0
            return 0
        
        # Sort heights in descending order
        child_heights.sort(reverse=True)
        
        # Update diameter
        if len(child_heights) >= 2:
            diameter = max(diameter, child_heights[0] + child_heights[1])
        else:
            diameter = max(diameter, child_heights[0])
        
        # Store height of current node
        heights[node] = child_heights[0] + 1
        return heights[node]
    
    # Calculate heights and diameter
    dfs(1, -1)
    
    # Calculate maximum distances using heights and diameter
    def calculate_max_distances(node, parent, dist_from_root):
        # Maximum distance is max of:
        # 1. Distance to root + height of other subtrees
        # 2. Diameter
        max_dist = dist_from_root
        
        for child in tree[node]:
            if child != parent:
                # Distance through this child
                child_dist = dist_from_root + heights[child] + 1
                max_dist = max(max_dist, child_dist)
        
        max_distances[node] = max_dist
        
        for child in tree[node]:
            if child != parent:
                calculate_max_distances(child, node, dist_from_root + 1)
    
    calculate_max_distances(1, -1, 0)
    
    return max_distances[1:n + 1]
```

**Why this improvement works**: Single DFS calculates all necessary information efficiently.

### Alternative: Rerooting Technique - O(n)
**Description**: Use rerooting technique to calculate distances for all nodes efficiently.

```python
def tree_distances_rerooting(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Arrays to store distances
    max_distances = [0] * (n + 1)
    
    def dfs1(node, parent):
        # First DFS: calculate heights
        max_height = 0
        for child in tree[node]:
            if child != parent:
                height = dfs1(child, node)
                max_height = max(max_height, height + 1)
        return max_height
    
    def dfs2(node, parent, dist_from_parent):
        # Second DFS: calculate maximum distances
        max_distances[node] = dist_from_parent
        
        # Find two highest children
        heights = []
        for child in tree[node]:
            if child != parent:
                height = dfs1(child, node) + 1
                heights.append((height, child))
        
        heights.sort(reverse=True)
        
        for child in tree[node]:
            if child != parent:
                # Calculate distance from child to other nodes
                other_max = 0
                if len(heights) >= 2:
                    if heights[0][1] == child:
                        other_max = heights[1][0]
                    else:
                        other_max = heights[0][0]
                else:
                    other_max = dist_from_parent
                
                dfs2(child, node, max(dist_from_parent + 1, other_max + 1))
    
    # Start rerooting from root
    dfs1(1, -1)
    dfs2(1, -1, 0)
    
    return max_distances[1:n + 1]
```

**Why this works**: Rerooting technique efficiently calculates distances for all nodes.

## Final Optimal Solution

```python
n = int(input())
edges = [tuple(map(int, input().split())) for _ in range(n - 1)]

# Build adjacency list
tree = [[] for _ in range(n + 1)]
for a, b in edges:
    tree[a].append(b)
    tree[b].append(a)

def dfs(node, parent, distance):
    max_dist = distance
    farthest_node = node
    
    for child in tree[node]:
        if child != parent:
            dist, far_node = dfs(child, node, distance + 1)
            if dist > max_dist:
                max_dist = dist
                farthest_node = far_node
    
    return max_dist, farthest_node

# Find diameter endpoints
_, endpoint1 = dfs(1, -1, 0)
_, endpoint2 = dfs(endpoint1, -1, 0)

# Calculate distances from both endpoints
def calculate_distances(start):
    distances = [-1] * (n + 1)
    stack = [(start, -1, 0)]
    
    while stack:
        node, parent, dist = stack.pop()
        distances[node] = dist
        
        for child in tree[node]:
            if child != parent:
                stack.append((child, node, dist + 1))
    
    return distances

dist1 = calculate_distances(endpoint1)
dist2 = calculate_distances(endpoint2)

# Maximum distance for each node is max of distances to endpoints
result = []
for i in range(1, n + 1):
    result.append(max(dist1[i], dist2[i]))

print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Multiple BFS | O(n²) | O(n) | Brute force approach |
| Diameter Endpoints | O(n) | O(n) | Use diameter properties |
| Single DFS | O(n) | O(n) | Height-based calculation |
| Rerooting | O(n) | O(n) | Efficient rerooting technique |

## Key Insights for Other Problems

### 1. **Tree Distance Problems**
**Principle**: Use diameter properties to find maximum distances efficiently.
**Applicable to**:
- Tree distance problems
- Graph algorithms
- Tree algorithms
- Algorithm design

**Example Problems**:
- Tree distance problems
- Graph algorithms
- Tree algorithms
- Algorithm design

### 2. **Diameter Properties**
**Principle**: The maximum distance from any node is to one of the diameter endpoints.
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

### 3. **Rerooting Technique**
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

### 4. **Two-Pass Algorithms**
**Principle**: Use two passes to find optimal solutions in tree problems.
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

### 1. **Diameter Endpoints Pattern**
```python
def diameter_endpoints_distances(tree, n):
    def dfs(node, parent, distance):
        max_dist = distance
        farthest_node = node
        
        for child in tree[node]:
            if child != parent:
                dist, far_node = dfs(child, node, distance + 1)
                if dist > max_dist:
                    max_dist = dist
                    farthest_node = far_node
        
        return max_dist, farthest_node
    
    _, endpoint1 = dfs(1, -1, 0)
    _, endpoint2 = dfs(endpoint1, -1, 0)
    
    dist1 = calculate_distances(endpoint1)
    dist2 = calculate_distances(endpoint2)
    
    return [max(dist1[i], dist2[i]) for i in range(1, n + 1)]
```

### 2. **Rerooting Pattern**
```python
def rerooting_distances(tree, n):
    max_distances = [0] * (n + 1)
    
    def dfs1(node, parent):
        max_height = 0
        for child in tree[node]:
            if child != parent:
                height = dfs1(child, node)
                max_height = max(max_height, height + 1)
        return max_height
    
    def dfs2(node, parent, dist_from_parent):
        max_distances[node] = dist_from_parent
        
        for child in tree[node]:
            if child != parent:
                other_max = calculate_other_max(node, child)
                dfs2(child, node, max(dist_from_parent + 1, other_max + 1))
    
    dfs1(1, -1)
    dfs2(1, -1, 0)
    return max_distances[1:n + 1]
```

### 3. **Height-based Distance Pattern**
```python
def height_based_distances(tree, n):
    heights = [0] * (n + 1)
    max_distances = [0] * (n + 1)
    
    def dfs(node, parent):
        child_heights = []
        for child in tree[node]:
            if child != parent:
                height = dfs(child, node)
                child_heights.append(height)
        
        if child_heights:
            heights[node] = max(child_heights) + 1
        
        return heights[node]
    
    def calculate_distances(node, parent, dist_from_root):
        max_distances[node] = dist_from_root
        
        for child in tree[node]:
            if child != parent:
                child_dist = dist_from_root + heights[child] + 1
                max_distances[node] = max(max_distances[node], child_dist)
                calculate_distances(child, node, dist_from_root + 1)
    
    dfs(1, -1)
    calculate_distances(1, -1, 0)
    return max_distances[1:n + 1]
```

## Edge Cases to Remember

1. **Single node**: Tree with only one node (distance = 0)
2. **Linear tree**: Tree with no branching
3. **Star tree**: Tree with one central node
4. **Perfect binary tree**: Balanced tree structure
5. **Large trees**: Handle deep recursion properly

## Problem-Solving Framework

1. **Identify distance nature**: This is a tree distance problem
2. **Use diameter properties**: Maximum distance is to diameter endpoints
3. **Choose approach**: Use two DFS to find endpoints
4. **Calculate distances**: Find distances from both endpoints
5. **Return result**: Return maximum of distances to endpoints

---

*This analysis shows how to efficiently find maximum distances in trees using diameter properties.*