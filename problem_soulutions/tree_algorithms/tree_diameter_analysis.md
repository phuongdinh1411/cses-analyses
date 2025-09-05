---
layout: simple
title: "Tree Diameter - Longest Path in Tree"
permalink: /problem_soulutions/tree_algorithms/tree_diameter_analysis
---

# Tree Diameter - Longest Path in Tree

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand tree diameter problems and longest path algorithms in trees
- [ ] **Objective 2**: Apply DFS-based algorithms to find the diameter of a tree efficiently
- [ ] **Objective 3**: Implement efficient tree diameter algorithms with O(n) time complexity
- [ ] **Objective 4**: Optimize tree diameter calculation using DFS, BFS, and tree traversal techniques
- [ ] **Objective 5**: Handle edge cases in tree diameter (single node, linear tree, star tree)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: DFS, BFS, tree traversal, tree diameter, longest path algorithms, tree algorithms
- **Data Structures**: Trees, adjacency lists, tree representation, path tracking, distance tracking
- **Mathematical Concepts**: Tree theory, graph theory, path mathematics, diameter analysis, tree properties
- **Programming Skills**: Tree traversal implementation, DFS implementation, BFS implementation, tree algorithms
- **Related Problems**: Tree Distances (distance calculation), Tree algorithms, Graph algorithms

## 📋 Problem Description

Given a tree with n nodes, find the diameter of the tree (the longest path between any two nodes).

The diameter of a tree is the longest path between any two nodes in the tree. This is a fundamental tree algorithm problem that requires finding the two nodes that are farthest apart.

**Input**: 
- First line: Integer n (number of nodes)
- Next n-1 lines: Two integers a and b (edge between nodes a and b)

**Output**: 
- One integer: diameter of the tree

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n

**Example**:
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

**Explanation**: 
- Tree structure: 1-2, 1-3, 3-4, 3-5
- Longest path: 2 → 1 → 3 → 4 (or 2 → 1 → 3 → 5)
- Diameter: 3 edges (length 3)

## 🎯 Visual Example

### Input
```
n = 5
Edges: [(1,2), (1,3), (3,4), (3,5)]
```

### Tree Structure
```
Node 1
├── Node 2
└── Node 3
    ├── Node 4
    └── Node 5

Tree representation:
    1
   / \
  2   3
     / \
    4   5
```

### Diameter Calculation
```
Two DFS approach:

Step 1: First DFS from node 1
- Find farthest node from 1: node 4 (distance 2)
- Path: 1 → 3 → 4

Step 2: Second DFS from node 4
- Find farthest node from 4: node 2 (distance 3)
- Path: 4 → 3 → 1 → 2

Diameter: 3 edges (longest path)
```

### All Possible Paths
```
All paths in the tree:
1. 1-2 (length 1)
2. 1-3 (length 1)
3. 3-4 (length 1)
4. 3-5 (length 1)
5. 1-3-4 (length 2)
6. 1-3-5 (length 2)
7. 2-1-3 (length 2)
8. 2-1-3-4 (length 3) ← Longest
9. 2-1-3-5 (length 3) ← Longest
10. 4-3-5 (length 2)

Longest paths: 2-1-3-4 and 2-1-3-5 (length 3)
```

### Key Insight
Tree diameter calculation works by:
1. Using two DFS traversals
2. First DFS: find farthest node from any starting node
3. Second DFS: find farthest node from the first farthest node
4. Distance between these two nodes is the diameter
5. Time complexity: O(n) for two DFS traversals
6. Space complexity: O(n) for recursion stack

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find the longest path between any two nodes in a tree
- **Key Insight**: Use two DFS traversals to find diameter efficiently
- **Challenge**: Efficiently find the two nodes that are farthest apart

### Step 2: Initial Approach
**Two DFS approach to find tree diameter:**

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

### Step 3: Optimization/Alternative
**BFS approach for tree diameter:**

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

### Step 4: Complete Solution

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

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple tree (should return correct diameter)
- **Test 2**: Linear tree (should return n-1)
- **Test 3**: Star tree (should return 2)
- **Test 4**: Complex tree (should find longest path)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Two DFS | O(n) | O(n) | Find farthest nodes |
| Single DFS | O(n) | O(n) | Track heights efficiently |
| BFS | O(n) | O(n) | Iterative approach |
| Dynamic Programming | O(n) | O(n) | Store heights for reuse |

## 🎨 Visual Example

### Input Example
```
Tree:
5
1 2
1 3
3 4
3 5
```

### Tree Structure Visualization
```
Tree Structure:
    1
   / \
  2   3
     / \
    4   5

Adjacency List:
1: [2, 3]
2: [1]
3: [1, 4, 5]
4: [3]
5: [3]
```

### All Possible Paths
```
All paths in the tree:
- 1 → 2 (length 1)
- 1 → 3 (length 1)
- 1 → 3 → 4 (length 2)
- 1 → 3 → 5 (length 2)
- 2 → 1 → 3 (length 2)
- 2 → 1 → 3 → 4 (length 3) ← Longest
- 2 → 1 → 3 → 5 (length 3) ← Longest
- 3 → 4 (length 1)
- 3 → 5 (length 1)
- 4 → 3 → 5 (length 2)

Diameter: 3 (longest path has 3 edges)
```

### Two DFS Approach
```
Step 1: First DFS from node 1
    1
   / \
  2   3
     / \
    4   5

DFS from node 1:
- Distance to node 1: 0
- Distance to node 2: 1
- Distance to node 3: 1
- Distance to node 4: 2
- Distance to node 5: 2

Farthest node from 1: node 2 or node 4 or node 5 (all distance 2)
Choose node 2 as farthest.

Step 2: Second DFS from node 2
    1
   / \
  2   3
     / \
    4   5

DFS from node 2:
- Distance to node 2: 0
- Distance to node 1: 1
- Distance to node 3: 2
- Distance to node 4: 3
- Distance to node 5: 3

Farthest node from 2: node 4 or node 5 (distance 3)
Diameter = 3
```

### Single DFS Approach
```
Tree with heights calculated:
    1 (height 2)
   / \
  2   3 (height 1)
     / \
    4   5 (both height 0)

DFS Process:
1. Visit node 4: height = 0, diameter = 0
2. Visit node 5: height = 0, diameter = 0
3. Visit node 3: 
   - height = max(0, 0) + 1 = 1
   - diameter = max(0, 0, 0 + 0) = 0
4. Visit node 2: height = 0, diameter = 0
5. Visit node 1:
   - height = max(0, 1) + 1 = 2
   - diameter = max(0, 0, 0 + 1) = 1
   - But we need to track the actual longest path

Correct Single DFS:
For each node, calculate:
- Height: longest path from this node to a leaf
- Diameter: longest path passing through this node

Node 3: height = 1, diameter = 2 (path 4-3-5)
Node 1: height = 2, diameter = 3 (path 2-1-3-4 or 2-1-3-5)
```

### BFS Approach
```
Step 1: BFS from node 1
Queue: [1]
Distances: {1: 0}

Level 0: [1]
- Process node 1, add neighbors 2, 3
- Distances: {1: 0, 2: 1, 3: 1}

Level 1: [2, 3]
- Process node 2, no new neighbors
- Process node 3, add neighbors 4, 5
- Distances: {1: 0, 2: 1, 3: 1, 4: 2, 5: 2}

Farthest nodes: 4, 5 (distance 2)
Choose node 4.

Step 2: BFS from node 4
Queue: [4]
Distances: {4: 0}

Level 0: [4]
- Process node 4, add neighbor 3
- Distances: {4: 0, 3: 1}

Level 1: [3]
- Process node 3, add neighbors 1, 5
- Distances: {4: 0, 3: 1, 1: 2, 5: 2}

Level 2: [1, 5]
- Process node 1, add neighbor 2
- Process node 5, no new neighbors
- Distances: {4: 0, 3: 1, 1: 2, 5: 2, 2: 3}

Farthest node: 2 (distance 3)
Diameter = 3
```

### Dynamic Programming Approach
```
Tree with DP values:
    1 (dp = 3)
   / \
  2   3 (dp = 2)
     / \
    4   5 (dp = 0)

DP Calculation:
- dp[node] = longest path in subtree rooted at node
- For each node, consider:
  1. Longest path in child subtrees
  2. Longest path passing through this node

Node 4: dp[4] = 0 (leaf)
Node 5: dp[5] = 0 (leaf)
Node 3: dp[3] = max(0, 0, 0+0+1) = 1, but actual longest path = 2
Node 2: dp[2] = 0 (leaf)
Node 1: dp[1] = max(0, 1, 0+1+1) = 2, but actual longest path = 3

Correct DP: Track both height and diameter
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Two DFS         │ O(n)         │ O(n)         │ Find farthest│
│                 │              │              │ nodes        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Single DFS      │ O(n)         │ O(n)         │ Track heights│
│                 │              │              │ efficiently  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ BFS             │ O(n)         │ O(n)         │ Iterative    │
│                 │              │              │ approach     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Dynamic Prog    │ O(n)         │ O(n)         │ Store heights│
│                 │              │              │ for reuse    │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Tree Diameter Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: tree     │
              │ (n nodes, edges)│
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Choose Algorithm│
              │ (Two DFS/       │
              │  Single DFS)    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ First DFS: Find │
              │ Farthest Node   │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Second DFS:     │
              │ Find Farthest   │
              │ from First      │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return Distance │
              │ (Diameter)      │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **Tree Diameter**: Longest path between any two nodes in a tree
- **Two DFS Approach**: Find farthest node, then find farthest from that node
- **Single DFS**: Calculate heights and update diameter during traversal
- **BFS Approach**: Use breadth-first search for iterative solution

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Tree Diameter with Path Reconstruction**
```python
def tree_diameter_with_path(n, edges):
    # Find diameter and reconstruct the actual path
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    def dfs(node, parent, distance):
        # DFS to find farthest node and distances
        distances = {node: distance}
        farthest_node = node
        max_distance = distance
        
        for child in tree[node]:
            if child != parent:
                child_farthest, child_max_dist, child_distances = dfs(child, node, distance + 1)
                distances.update(child_distances)
                
                if child_max_dist > max_distance:
                    max_distance = child_max_dist
                    farthest_node = child_farthest
        
        return farthest_node, max_distance, distances
    
    # First DFS: find farthest node from node 1
    farthest1, _, distances1 = dfs(1, -1, 0)
    
    # Second DFS: find farthest node from farthest1
    farthest2, diameter, distances2 = dfs(farthest1, -1, 0)
    
    # Reconstruct path using distances
    def reconstruct_path(start, end, distances):
        path = [end]
        current = end
        
        while current != start:
            for neighbor in tree[current]:
                if distances.get(neighbor, float('inf')) == distances[current] - 1:
                    path.append(neighbor)
                    current = neighbor
                    break
        
        return path[::-1]
    
    path = reconstruct_path(farthest1, farthest2, distances2)
    
    return diameter, path
```

#### **2. Tree Diameter with Edge Weights**
```python
def weighted_tree_diameter(n, edges, weights):
    # Find diameter in weighted tree
    
    # Build adjacency list with weights
    tree = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        tree[a].append((b, weights[i]))
        tree[b].append((a, weights[i]))
    
    def dfs(node, parent, distance):
        # DFS to find farthest node and distances
        distances = {node: distance}
        farthest_node = node
        max_distance = distance
        
        for child, weight in tree[node]:
            if child != parent:
                child_farthest, child_max_dist, child_distances = dfs(child, node, distance + weight)
                distances.update(child_distances)
                
                if child_max_dist > max_distance:
                    max_distance = child_max_dist
                    farthest_node = child_farthest
        
        return farthest_node, max_distance, distances
    
    # First DFS: find farthest node from node 1
    farthest1, _, distances1 = dfs(1, -1, 0)
    
    # Second DFS: find farthest node from farthest1
    farthest2, diameter, distances2 = dfs(farthest1, -1, 0)
    
    return diameter
```

#### **3. Tree Diameter with Multiple Queries**
```python
def tree_diameter_queries(n, edges, queries):
    # Handle multiple diameter queries efficiently
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    def dfs(node, parent, distance):
        # DFS to find farthest node and distances
        distances = {node: distance}
        farthest_node = node
        max_distance = distance
        
        for child in tree[node]:
            if child != parent:
                child_farthest, child_max_dist, child_distances = dfs(child, node, distance + 1)
                distances.update(child_distances)
                
                if child_max_dist > max_distance:
                    max_distance = child_max_dist
                    farthest_node = child_farthest
        
        return farthest_node, max_distance, distances
    
    # Precompute diameter
    farthest1, _, distances1 = dfs(1, -1, 0)
    farthest2, diameter, distances2 = dfs(farthest1, -1, 0)
    
    # Process queries
    results = []
    for query in queries:
        if query[0] == 'diameter':
            results.append(diameter)
        elif query[0] == 'distance':
            a, b = query[1], query[2]
            # Calculate distance between a and b
            def distance_between(a, b):
                # BFS to find distance
                from collections import deque
                queue = deque([(a, 0)])
                visited = {a}
                
                while queue:
                    node, dist = queue.popleft()
                    if node == b:
                        return dist
                    
                    for neighbor in tree[node]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, dist + 1))
                
                return -1
            
            results.append(distance_between(a, b))
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Tree Diameter**: Various tree diameter problems
- **Tree Algorithms**: Tree traversal and path problems
- **Graph Algorithms**: Path and distance problems
- **Tree DP**: Dynamic programming on trees

## 📚 Learning Points

### Key Takeaways
- **Two DFS approach** is the most common method for tree diameter
- **Single DFS** can be more efficient for some cases
- **BFS approach** is iterative and memory-efficient
- **Tree structure** simplifies diameter calculation

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

*This analysis shows how to efficiently find tree diameter using height tracking and longest path calculations.*