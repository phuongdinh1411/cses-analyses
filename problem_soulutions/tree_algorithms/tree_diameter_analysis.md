---
layout: simple
title: "Tree Diameter
permalink: /problem_soulutions/tree_algorithms/tree_diameter_analysis/
---

# Tree Diameter

## Problem Statement
Given a tree with n nodes, find the diameter of the tree (the longest path between any two nodes).

### Input
The first input line has an integer n: the number of nodes. The nodes are numbered 1,2,…,n.
Then, there are n−1 lines describing the edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print one integer: the diameter of the tree.

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
3
```

## Solution Progression

### Approach 1: Two DFS Approach - O(n)
**Description**: Use two DFS traversals to find the diameter by finding the longest path from any node to its farthest node, then from that node to its farthest node.

```python
def tree_diameter_two_dfs(n, edges):
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
    
    # First DFS: find the farthest node from node 1
    _, farthest = dfs(1, -1, 0)
    
    # Second DFS: find the farthest node from the farthest node
    diameter, _ = dfs(farthest, -1, 0)
    
    return diameter
```

**Why this is efficient**: Two DFS approach finds the diameter by finding the longest path in the tree.

### Improvement 1: Single DFS with Height Tracking - O(n)
**Description**: Use a single DFS to track heights and calculate diameter simultaneously.

```python
def tree_diameter_single_dfs(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    diameter = 0
    
    def dfs(node, parent):
        nonlocal diameter
        
        # Heights of all children
        heights = []
        
        for child in tree[node]:
            if child != parent:
                height = dfs(child, node)
                heights.append(height)
        
        if not heights:
            return 0
        
        # Sort heights in descending order
        heights.sort(reverse=True)
        
        # Update diameter: longest path through current node
        if len(heights) >= 2:
            diameter = max(diameter, heights[0] + heights[1])
        else:
            diameter = max(diameter, heights[0])
        
        # Return height of current node
        return heights[0] + 1
    
    # Start DFS from root (node 1)
    dfs(1, -1)
    
    return diameter
```

**Why this improvement works**: Single DFS calculates diameter more efficiently by tracking heights and updating diameter during traversal.

### Improvement 2: BFS Approach - O(n)
**Description**: Use BFS to find the diameter by finding the longest shortest path.

```python
from collections import deque

def tree_diameter_bfs(n, edges):
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
        
        # Find the node with maximum distance
        max_dist = 0
        farthest_node = start
        for i in range(1, n + 1):
            if distances[i] > max_dist:
                max_dist = distances[i]
                farthest_node = i
        
        return max_dist, farthest_node
    
    # First BFS: find the farthest node from node 1
    _, farthest = bfs(1)
    
    # Second BFS: find the distance from farthest node
    diameter, _ = bfs(farthest)
    
    return diameter
```

**Why this improvement works**: BFS approach is iterative and can be more memory-efficient for very deep trees.

### Alternative: Dynamic Programming on Trees - O(n)
**Description**: Use dynamic programming to calculate heights and diameter simultaneously.

```python
def tree_diameter_dp(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # DP array to store heights
    heights = [0] * (n + 1)
    diameter = 0
    
    def dfs(node, parent):
        nonlocal diameter
        
        # Calculate heights of all children
        child_heights = []
        for child in tree[node]:
            if child != parent:
                child_height = dfs(child, node)
                child_heights.append(child_height)
        
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
    
    # Start DFS from root (node 1)
    dfs(1, -1)
    
    return diameter
```

**Why this works**: DP approach stores heights for reuse and calculates diameter efficiently.

## Final Optimal Solution

```python
n = int(input())
edges = [tuple(map(int, input().split())) for _ in range(n - 1)]

# Build adjacency list
tree = [[] for _ in range(n + 1)]
for a, b in edges:
    tree[a].append(b)
    tree[b].append(a)

diameter = 0

def dfs(node, parent):
    global diameter
    
    # Heights of all children
    heights = []
    
    for child in tree[node]:
        if child != parent:
            height = dfs(child, node)
            heights.append(height)
    
    if not heights:
        return 0
    
    # Sort heights in descending order
    heights.sort(reverse=True)
    
    # Update diameter: longest path through current node
    if len(heights) >= 2:
        diameter = max(diameter, heights[0] + heights[1])
    else:
        diameter = max(diameter, heights[0])
    
    # Return height of current node
    return heights[0] + 1

# Start DFS from root (node 1)
dfs(1, -1)

print(diameter)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Two DFS | O(n) | O(n) | Find farthest nodes |
| Single DFS | O(n) | O(n) | Track heights efficiently |
| BFS | O(n) | O(n) | Iterative approach |
| Dynamic Programming | O(n) | O(n) | Store heights for reuse |

## Key Insights for Other Problems

### 1. **Tree Diameter Problems**
**Principle**: Use height tracking and longest path calculation to find tree diameter.
**Applicable to**:
- Tree diameter problems
- Graph algorithms
- Tree algorithms
- Algorithm design

**Example Problems**:
- Tree diameter problems
- Graph algorithms
- Tree algorithms
- Algorithm design

### 2. **Height-based Calculations**
**Principle**: Use subtree heights to calculate global tree properties.
**Applicable to**:
- Tree algorithms
- Dynamic programming on trees
- Graph algorithms
- Algorithm design

**Example Problems**:
- Tree algorithms
- Dynamic programming on trees
- Graph algorithms
- Algorithm design

### 3. **Two-Pass Algorithms**
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

### 4. **Longest Path Problems**
**Principle**: Find longest paths by combining heights of subtrees.
**Applicable to**:
- Longest path problems
- Tree algorithms
- Graph algorithms
- Algorithm design

**Example Problems**:
- Longest path problems
- Tree algorithms
- Graph algorithms
- Algorithm design

## Notable Techniques

### 1. **Two DFS Pattern**
```python
def two_dfs_diameter(tree, n):
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
    
    _, farthest = dfs(1, -1, 0)
    diameter, _ = dfs(farthest, -1, 0)
    return diameter
```

### 2. **Height Tracking Pattern**
```python
def height_tracking_diameter(tree, n):
    diameter = 0
    
    def dfs(node, parent):
        nonlocal diameter
        heights = []
        
        for child in tree[node]:
            if child != parent:
                height = dfs(child, node)
                heights.append(height)
        
        if not heights:
            return 0
        
        heights.sort(reverse=True)
        
        if len(heights) >= 2:
            diameter = max(diameter, heights[0] + heights[1])
        else:
            diameter = max(diameter, heights[0])
        
        return heights[0] + 1
    
    dfs(1, -1)
    return diameter
```

### 3. **BFS Diameter Pattern**
```python
def bfs_diameter(tree, n):
    def bfs(start):
        distances = [-1] * (n + 1)
        queue = deque([start])
        distances[start] = 0
        
        while queue:
            node = queue.popleft()
            for neighbor in tree[node]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        
        max_dist = max(distances[1:])
        farthest = distances.index(max_dist)
        return max_dist, farthest
    
    _, farthest = bfs(1)
    diameter, _ = bfs(farthest)
    return diameter
```

## Edge Cases to Remember

1. **Single node**: Tree with only one node (diameter = 0)
2. **Linear tree**: Tree with no branching (diameter = n-1)
3. **Star tree**: Tree with one central node (diameter = 2)
4. **Perfect binary tree**: Balanced tree structure
5. **Large trees**: Handle deep recursion properly

## Problem-Solving Framework

1. **Identify diameter nature**: This is a tree diameter problem
2. **Choose approach**: Use height tracking with single DFS
3. **Track heights**: Calculate heights of all subtrees
4. **Update diameter**: Combine heights to find longest path
5. **Return result**: Return the maximum diameter found

---

*This analysis shows how to efficiently find tree diameter using height tracking and longest path calculations.*"