---
layout: simple
title: "Tree Distances II - Sum of Distances from Each Node"
permalink: /problem_soulutions/tree_algorithms/tree_distances_ii_analysis
---

# Tree Distances II - Sum of Distances from Each Node

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand tree distance problems and sum of distances calculation algorithms
- Apply dynamic programming with rerooting technique to calculate sum of distances efficiently
- Implement efficient tree distance algorithms with O(n) time complexity using rerooting
- Optimize tree distance calculation using dynamic programming, rerooting, and tree properties
- Handle edge cases in tree distances (single node, linear tree, star tree, large trees)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming on trees, rerooting technique, tree traversal, distance calculation, tree algorithms
- **Data Structures**: Trees, adjacency lists, DP tables, distance tracking, subtree tracking, tree representation
- **Mathematical Concepts**: Tree theory, distance mathematics, rerooting theory, dynamic programming mathematics
- **Programming Skills**: Dynamic programming implementation, tree traversal, rerooting implementation, algorithm implementation
- **Related Problems**: Tree Distances I (maximum distance), Tree algorithms, Dynamic programming problems

## 📋 Problem Description

Given a tree with n nodes, find for each node the sum of distances to all other nodes.

This is a tree distance problem that requires finding the sum of distances from each node to all other nodes in the tree. The solution involves using dynamic programming on trees with rerooting technique.

**Input**: 
- First line: Integer n (number of nodes)
- Next n-1 lines: Two integers a and b (edge between nodes a and b)

**Output**: 
- n integers: sum of distances from each node to all other nodes

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
6 9 5 8 8
```

**Explanation**: 
- Node 1: sum = 0+1+1+2+2 = 6
- Node 2: sum = 1+0+2+3+3 = 9
- Node 3: sum = 1+2+0+1+1 = 5
- Node 4: sum = 2+3+1+0+2 = 8
- Node 5: sum = 2+3+1+2+0 = 8

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

### Sum of Distances Calculation
```
For each node, sum distances to all other nodes:

Node 1: Sum = 0 + 1 + 1 + 2 + 2 = 6
- Distance to 1: 0
- Distance to 2: 1
- Distance to 3: 1
- Distance to 4: 2 (path: 1 → 3 → 4)
- Distance to 5: 2 (path: 1 → 3 → 5)

Node 2: Sum = 1 + 0 + 2 + 3 + 3 = 9
- Distance to 1: 1
- Distance to 2: 0
- Distance to 3: 2 (path: 2 → 1 → 3)
- Distance to 4: 3 (path: 2 → 1 → 3 → 4)
- Distance to 5: 3 (path: 2 → 1 → 3 → 5)

Node 3: Sum = 1 + 2 + 0 + 1 + 1 = 5
- Distance to 1: 1
- Distance to 2: 2 (path: 3 → 1 → 2)
- Distance to 3: 0
- Distance to 4: 1
- Distance to 5: 1

Node 4: Sum = 2 + 3 + 1 + 0 + 2 = 8
- Distance to 1: 2 (path: 4 → 3 → 1)
- Distance to 2: 3 (path: 4 → 3 → 1 → 2)
- Distance to 3: 1
- Distance to 4: 0
- Distance to 5: 2 (path: 4 → 3 → 5)

Node 5: Sum = 2 + 3 + 1 + 2 + 0 = 8
- Distance to 1: 2 (path: 5 → 3 → 1)
- Distance to 2: 3 (path: 5 → 3 → 1 → 2)
- Distance to 3: 1
- Distance to 4: 2 (path: 5 → 3 → 4)
- Distance to 5: 0
```

### Rerooting Technique
```
Start with one node (e.g., node 1) and calculate sum of distances.
Then use rerooting to calculate for other nodes:

When moving from parent to child:
- Subtract contribution of child's subtree
- Add contribution of parent's subtree
- Update distances accordingly
```

### Key Insight
Sum of distances calculation works by:
1. Using rerooting technique
2. Start with one node and calculate sum of distances
3. Move to adjacent nodes and update distances
4. Use dynamic programming to avoid recalculating
5. Time complexity: O(n) for rerooting
6. Space complexity: O(n) for storing distances

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find sum of distances from each node to all other nodes
- **Key Insight**: Use dynamic programming on trees with rerooting technique
- **Challenge**: Efficiently calculate distances without O(n²) complexity

### Step 2: Initial Approach
**Multiple BFS approach (inefficient but correct):**

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
            if child != parent: # When moving root from node to 
child: # - Nodes in child's subtree get closer by 1
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

### Step 3: Optimization/Alternative
**Single DFS with height and count calculation:**

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

### Step 4: Complete Solution

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
        if child != parent: # When moving root from node to 
child: # - Nodes in child's subtree get closer by 1
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

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple tree (should return correct distance sums)
- **Test 2**: Linear tree (should return correct sums)
- **Test 3**: Star tree (should return correct sums)
- **Test 4**: Complex tree (should find all distance sums)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Multiple BFS | O(n²) | O(n) | Brute force approach |
| Rerooting | O(n) | O(n) | Use subtree sizes |
| Single DFS | O(n) | O(n) | Efficient rerooting |
| Dynamic Programming | O(n) | O(n) | Parent-based calculation |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Rerooting Technique**: Change root and recalculate distances efficiently
- **Subtree Sizes**: Use subtree sizes to calculate distance changes
- **Dynamic Programming**: Use DP on trees for optimal solutions
- **Distance Sum Formula**: sum_new = sum_old - nodes_in_subtree + nodes_outside_subtree

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Tree Distances with Edge Weights**
```python
def weighted_tree_distances_ii(n, edges, weights):
    # Find sum of weighted distances from each node
    
    # Build adjacency list with weights
    tree = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        tree[a].append((b, weights[i]))
        tree[b].append((a, weights[i]))
    
    # Arrays to store subtree sizes and distance sums
    subtree_sizes = [0] * (n + 1)
    distance_sums = [0] * (n + 1)
    
    def dfs1(node, parent):
        # First DFS: calculate subtree sizes
        subtree_sizes[node] = 1
        for child, weight in tree[node]:
            if child != parent:
                subtree_sizes[node] += dfs1(child, node)
        return subtree_sizes[node]
    
    def dfs2(node, parent, dist_sum):
        # Second DFS: calculate distance sums using rerooting
        distance_sums[node] = dist_sum
        
        for child, weight in tree[node]:
            if child != parent:
                # When moving root from node to child:
                # - Nodes in child's subtree get closer by weight
                # - Nodes outside child's subtree get farther by weight
                nodes_in_subtree = subtree_sizes[child]
                nodes_outside_subtree = n - nodes_in_subtree
                
                new_dist_sum = dist_sum - nodes_in_subtree * weight + nodes_outside_subtree * weight
                dfs2(child, node, new_dist_sum)
    
    # Calculate initial distance sum from root
    def calculate_initial_sum(node, parent, depth):
        total = depth
        for child, weight in tree[node]:
            if child != parent:
                total += calculate_initial_sum(child, node, depth + weight)
        return total
    
    # Start rerooting from root
    dfs1(1, -1)
    initial_sum = calculate_initial_sum(1, -1, 0)
    dfs2(1, -1, initial_sum)
    
    return distance_sums[1:n + 1]
```

#### **2. Tree Distances with Multiple Queries**
```python
def tree_distances_ii_queries(n, edges, queries):
    # Handle multiple distance sum queries efficiently
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Precompute all distance sums using rerooting
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
    
    def calculate_initial_sum(node, parent, depth):
        total = depth
        for child in tree[node]:
            if child != parent:
                total += calculate_initial_sum(child, node, depth + 1)
        return total
    
    # Precompute all distance sums
    dfs1(1, -1)
    initial_sum = calculate_initial_sum(1, -1, 0)
    dfs2(1, -1, initial_sum)
    
    # Process queries
    results = []
    for query in queries:
        if query[0] == 'sum':
            node = query[1]
            results.append(distance_sums[node])
        elif query[0] == 'distance':
            a, b = query[1], query[2]
            # Calculate distance between a and b
            def distance_between(a, b):
                from collections import deque
                queue = deque([(a, 0)])
                visited = {a}
                
                while queue:
                    node, dist = queue.popleft()
                    if node == b:
                        return dist
                    
                    for child in tree[node]:
                        if child not in visited:
                            visited.add(child)
                            queue.append((child, dist + 1))
                
                return -1
            
            results.append(distance_between(a, b))
    
    return results
```

#### **3. Tree Distances with Updates**
```python
def tree_distances_ii_updates(n, edges, updates):
    # Handle dynamic updates to tree structure
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    def compute_distance_sums():
        # Recompute distance sums after updates
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
        
        def calculate_initial_sum(node, parent, depth):
            total = depth
            for child in tree[node]:
                if child != parent:
                    total += calculate_initial_sum(child, node, depth + 1)
            return total
        
        dfs1(1, -1)
        initial_sum = calculate_initial_sum(1, -1, 0)
        dfs2(1, -1, initial_sum)
        
        return distance_sums[1:n + 1]
    
    # Process updates
    results = []
    for update in updates:
        if update[0] == 'add':
            # Add edge
            a, b = update[1], update[2]
            tree[a].append(b)
            tree[b].append(a)
        elif update[0] == 'remove':
            # Remove edge
            a, b = update[1], update[2]
            tree[a].remove(b)
            tree[b].remove(a)
        
        # Recompute distance sums
        result = compute_distance_sums()
        results.append(result)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Tree Distances**: Various tree distance problems
- **Rerooting**: Rerooting technique problems
- **Tree Algorithms**: Tree traversal and distance problems
- **Dynamic Programming**: DP on trees

## 📚 Learning Points

### Key Takeaways
- **Rerooting technique** efficiently calculates distance sums for all nodes
- **Subtree sizes** are crucial for distance sum calculations
- **Distance sum formula** simplifies rerooting calculations
- **Tree DP** provides optimal solutions for tree problems

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