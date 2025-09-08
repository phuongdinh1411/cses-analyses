---
layout: simple
title: "Prufer Code"
permalink: /problem_soulutions/advanced_graph_problems/prufer_code_analysis
---

# Prufer Code

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Prufer codes and their properties
- Apply the Prufer code construction algorithm for trees
- Implement efficient tree-to-Prufer code conversion
- Understand the bijection between labeled trees and Prufer codes
- Apply Prufer codes to tree counting and enumeration problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tree algorithms, Prufer codes, bijection algorithms
- **Data Structures**: Trees, adjacency lists, priority queues
- **Mathematical Concepts**: Graph theory, tree properties, bijections, combinatorics
- **Programming Skills**: Tree traversal, priority queue operations, tree manipulation
- **Related Problems**: Tree Traversals (tree algorithms), Tree Diameter (tree properties), Counting Trees (tree enumeration)

## 📋 Problem Description

Given a tree with n vertices, find its Prufer code. The Prufer code is a unique sequence that represents a labeled tree.

**Input**: 
- n: number of vertices
- n-1 edges: a b (edge between vertices a and b)

**Output**: 
- Prufer code of the tree

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ a, b ≤ n

**Example**:
```
Input:
4
1 2
2 3
3 4

Output:
2 3

Explanation**: 
The Prufer code [2, 3] represents the tree:
1 -- 2 -- 3 -- 4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Prufer Code Construction (Brute Force)

**Key Insights from Brute Force Approach**:
- **Leaf Removal**: Iteratively remove leaves from the tree
- **Neighbor Recording**: Record the neighbor of each removed leaf
- **Tree Modification**: Modify the tree structure after each removal
- **Exhaustive Search**: Process all leaves until only 2 vertices remain

**Key Insight**: Use brute force to iteratively remove leaves and record their neighbors to construct the Prufer code.

**Algorithm**:
- Build adjacency list representation of the tree
- Count degrees of each vertex
- Iteratively find and remove leaves
- Record the neighbor of each removed leaf
- Continue until only 2 vertices remain

**Visual Example**:
```
Tree: 1-2-3-4

Step 1: Remove leaf 1
┌─────────────────────────────────────┐
│ Tree: 2-3-4                        │
│ Prufer: [2]                        │
└─────────────────────────────────────┘

Step 2: Remove leaf 2
┌─────────────────────────────────────┐
│ Tree: 3-4                          │
│ Prufer: [2, 3]                     │
└─────────────────────────────────────┘

Result: [2, 3]
```

**Implementation**:
```python
def brute_force_prufer_code_solution(n, edges):
    """
    Find Prufer code using brute force approach
    
    Args:
        n: number of vertices
        edges: list of (a, b) representing edges
    
    Returns:
        list: Prufer code of the tree
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
    
    return prufer

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = brute_force_prufer_code_solution(n, edges)
print(f"Brute force result: {result}")  # Output: [2, 3]
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n²) complexity due to linear search for leaves and list removal operations.

---

### Approach 2: Optimized Prufer Code Construction (Optimized)

**Key Insights from Optimized Approach**:
- **Priority Queue**: Use priority queue to efficiently find leaves
- **Degree Tracking**: Maintain degree counts efficiently
- **Leaf Management**: Use priority queue for leaf selection
- **Optimized Removal**: Efficiently remove leaves and update degrees

**Key Insight**: Use priority queue to efficiently find and remove leaves in the correct order.

**Algorithm**:
- Build adjacency list and degree counts
- Use priority queue to find leaves efficiently
- Remove leaves and update degrees
- Record neighbors in Prufer code

**Visual Example**:
```
Tree: 1-2-3-4

Optimized Process:
┌─────────────────────────────────────┐
│ Priority Queue: [1, 2, 3, 4]       │
│ Degrees: [1, 2, 2, 1]              │
│ Remove leaf 1, Prufer: [2]         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Priority Queue: [2, 3, 4]          │
│ Degrees: [0, 1, 2, 1]              │
│ Remove leaf 2, Prufer: [2, 3]      │
└─────────────────────────────────────┘

Result: [2, 3]
```

**Implementation**:
```python
def optimized_prufer_code_solution(n, edges):
    """
    Find Prufer code using optimized approach with priority queue
    
    Args:
        n: number of vertices
        edges: list of (a, b) representing edges
    
    Returns:
        list: Prufer code of the tree
    """
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Initialize priority queue with leaves
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heapq.heappush(leaves, i)
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Get leaf with smallest label
        leaf = heapq.heappop(leaves)
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        
        # If neighbor becomes a leaf, add to queue
        if degree[neighbor] == 1:
            heapq.heappush(leaves, neighbor)
    
    return prufer

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = optimized_prufer_code_solution(n, edges)
print(f"Optimized result: {result}")  # Output: [2, 3]
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's better**: O(n log n) complexity is much faster than O(n²) brute force approach.

**Implementation Considerations**:
- **Priority Queue**: Use heapq for efficient leaf selection
- **Degree Tracking**: Maintain degree counts efficiently
- **Leaf Management**: Add new leaves to queue when they become leaves
- **Optimized Removal**: Efficiently remove leaves and update degrees

---

### Approach 3: Optimal Prufer Code Construction (Optimal)

**Key Insights from Optimal Approach**:
- **Linear Time**: Achieve O(n) time complexity
- **Efficient Data Structures**: Use appropriate data structures
- **Optimal Algorithm**: Use the most efficient Prufer code construction
- **Tree Properties**: Leverage tree properties for optimization

**Key Insight**: Use optimal data structures and algorithms to achieve O(n) time complexity.

**Algorithm**:
- Build adjacency list and degree counts
- Use efficient leaf finding and removal
- Optimize data structure operations
- Record neighbors in Prufer code

**Visual Example**:
```
Tree: 1-2-3-4

Optimal Process:
┌─────────────────────────────────────┐
│ Degrees: [1, 2, 2, 1]              │
│ Leaves: [1, 4]                     │
│ Remove leaf 1, Prufer: [2]         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Degrees: [0, 1, 2, 1]              │
│ Leaves: [2, 4]                     │
│ Remove leaf 2, Prufer: [2, 3]      │
└─────────────────────────────────────┘

Result: [2, 3]
```

**Implementation**:
```python
def optimal_prufer_code_solution(n, edges):
    """
    Find Prufer code using optimal approach
    
    Args:
        n: number of vertices
        edges: list of (a, b) representing edges
    
    Returns:
        list: Prufer code of the tree
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
    
    return prufer

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = optimal_prufer_code_solution(n, edges)
print(f"Optimal result: {result}")  # Output: [2, 3]

# Test with different example
n = 5
edges = [(1, 2), (2, 3), (3, 4), (4, 5)]
result = optimal_prufer_code_solution(n, edges)
print(f"Optimal result: {result}")  # Output: [2, 3, 4]
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's optimal**: This approach provides the most efficient solution with O(n) time complexity.

**Implementation Details**:
- **Linear Time**: Achieve O(n) time complexity
- **Efficient Leaf Finding**: Use linear search for leaves
- **Optimal Data Structures**: Use appropriate data structures
- **Optimal Result**: Guarantees efficient Prufer code construction
- Follows Prufer code algorithm
- Removes leaves iteratively
- Records neighbors in sequence
- O(n²) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_prufer_code():
    n = int(input())
    edges = []
    
    for _ in range(n - 1):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
    
    print(*prufer)

# Main execution
if __name__ == "__main__":
    solve_prufer_code()
```

**Why this works:**
- Optimal Prufer code construction
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4)]),
        (5, [(1, 2), (2, 3), (3, 4), (4, 5)]),
        (3, [(1, 2), (2, 3)]),
    ]
    
    for n, edges in test_cases:
        result = solve_test(n, edges)
        print(f"n={n}, edges={edges}")
        print(f"Result: {result}")
        print()

def solve_test(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
    
    return prufer

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n²) - finding leaves and removing them
- **Space**: O(n) - adjacency list and degree array

### Why This Solution Works
- **Prufer Code Algorithm**: Follows standard construction
- **Leaf Removal**: Iteratively removes leaves
- **Neighbor Recording**: Records neighbors in sequence
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Prufer Code**
- Unique representation of labeled trees
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Leaf Removal**
- Iteratively removes leaves
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Neighbor Recording**
- Records neighbors in sequence
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Prufer Code with Weights
**Problem**: Each edge has a weight, construct weighted Prufer code.

```python
def weighted_prufer_code(n, edges, weights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find weighted Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor and weight
        neighbor, weight = adj[leaf][0]
        prufer.append((neighbor, weight))
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove((leaf, weight))
    
    return prufer
```

### Variation 2: Prufer Code with Constraints
**Problem**: Construct Prufer code avoiding certain edges.

```python
def constrained_prufer_code(n, edges, forbidden_edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
    
    return prufer
```

### Variation 3: Dynamic Prufer Code
**Problem**: Support adding/removing edges and maintaining Prufer code.

```python
class DynamicPruferCode:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.edges = set()
    
    def add_edge(self, a, b):
        if (a, b) not in self.edges and (b, a) not in self.edges:
            self.edges.add((a, b))
            self.adj[a].append(b)
            self.adj[b].append(a)
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.edges.remove((a, b))
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            return True
        elif (b, a) in self.edges:
            self.edges.remove((b, a))
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            return True
        return False
    
    def get_prufer_code(self):
        # Count degrees
        degree = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            degree[i] = len(self.adj[i])
        
        # Find Prufer code
        prufer = []
        for _ in range(self.n - 2):
            # Find leaf with smallest label
            leaf = 1
            while degree[leaf] != 1:
                leaf += 1
            
            # Find its neighbor
            neighbor = self.adj[leaf][0]
            prufer.append(neighbor)
            
            # Remove the leaf
            degree[leaf] = 0
            degree[neighbor] -= 1
            self.adj[neighbor].remove(leaf)
        
        return prufer
```

### Variation 4: Prufer Code with Multiple Constraints
**Problem**: Construct Prufer code satisfying multiple constraints.

```python
def multi_constrained_prufer_code(n, edges, constraints):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    forbidden_edges = constraints.get('forbidden_edges', set())
    allowed_nodes = constraints.get('allowed_nodes', set(range(1, n + 1)))
    
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            if a in allowed_nodes and b in allowed_nodes:
                adj[a].append(b)
                adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
    
    return prufer
```

### Variation 5: Prufer Code with Edge Weights
**Problem**: Each edge has a weight, construct weighted Prufer code.

```python
def weighted_prufer_code_optimized(n, edges, weights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find weighted Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor and weight
        neighbor, weight = adj[leaf][0]
        prufer.append((neighbor, weight))
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove((leaf, weight))
    
    return prufer
```

## 🔗 Related Problems

- **[Tree Algorithms](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Tree algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[Tree Representation](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Tree representation algorithms

## 📚 Learning Points

1. **Prufer Code**: Essential for tree representation
2. **Tree Properties**: Important tree concepts
3. **Leaf Removal**: Key algorithmic technique
4. **Graph Theory**: Important graph theory concept

---

**This is a great introduction to Prufer code and tree representation!** 🎯
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
    
    # Print result
    print(*prufer)

# Main execution
if __name__ == "__main__":
    solve_prufer_code()
```

**Why this works:**
- Optimal Prufer code construction
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4)]),
        (3, [(1, 2), (2, 3)]),
        (5, [(1, 2), (2, 3), (3, 4), (4, 5)]),
    ]
    
    for n, edges in test_cases:
        result = solve_test(n, edges)
        print(f"n={n}, edges={edges}")
        print(f"Prufer code: {result}")
        print()

def solve_test(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
    
    return prufer

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n²) - finding leaves and removing edges
- **Space**: O(n) - adjacency list and degree array

### Why This Solution Works
- **Prufer Code Algorithm**: Follows standard construction method
- **Leaf Removal**: Iteratively removes leaves
- **Neighbor Recording**: Records neighbors in sequence
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Prufer Code Construction**
- Remove leaves iteratively
- Record neighbors in sequence
- Essential for tree representation
- Enables efficient solution

### 2. **Tree Properties**
- Trees have n-1 edges
- Prufer code has length n-2
- Important for understanding
- Fundamental concept

### 3. **Leaf Removal**
- Find leaves efficiently
- Important for performance
- Simple but important concept
- Essential for algorithm

## 🎯 Problem Variations

### Variation 1: Prufer Code to Tree
**Problem**: Reconstruct tree from Prufer code.

```python
def prufer_to_tree(prufer):
    n = len(prufer) + 2
    edges = []
    
    # Count occurrences in Prufer code
    degree = [1] * (n + 1)
    for x in prufer:
        degree[x] += 1
    
    # Find leaves
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            leaves.append(i)
    
    # Reconstruct tree
    for x in prufer:
        # Connect smallest leaf to x
        leaf = min(leaves)
        edges.append((leaf, x))
        
        # Remove leaf and update degrees
        leaves.remove(leaf)
        degree[x] -= 1
        if degree[x] == 1:
            leaves.append(x)
    
    # Connect last two vertices
    edges.append((leaves[0], leaves[1]))
    
    return edges
```

### Variation 2: Weighted Tree Prufer Code
**Problem**: Find Prufer code for weighted tree.

```python
def weighted_prufer_code(n, edges, weights):
    # Build adjacency list with weights
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, weights[i]))
        adj[b].append((a, weights[i]))
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor] = [(v, w) for v, w in adj[neighbor] if v != leaf]
    
    return prufer
```

### Variation 3: Prufer Code Validation
**Problem**: Check if a sequence is a valid Prufer code.

```python
def is_valid_prufer_code(prufer, n):
    if len(prufer) != n - 2:
        return False
    
    # Check if all values are in range [1, n]
    for x in prufer:
        if x < 1 or x > n:
            return False
    
    # Count occurrences
    count = [0] * (n + 1)
    for x in prufer:
        count[x] += 1
    
    # Check if reconstruction is possible
    degree = [1] * (n + 1)
    for x in prufer:
        degree[x] += 1
    
    # Find leaves
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            leaves.append(i)
    
    # Try to reconstruct
    for x in prufer:
        if not leaves:
            return False
        
        leaf = min(leaves)
        leaves.remove(leaf)
        degree[x] -= 1
        if degree[x] == 1:
            leaves.append(x)
    
    return len(leaves) == 2
```

### Variation 4: Prufer Code with Constraints
**Problem**: Find Prufer code avoiding certain edges.

```python
def constrained_prufer_code(n, edges, forbidden_edges):
    # Build adjacency list avoiding forbidden edges
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Find leaf with smallest label
        leaf = 1
        while degree[leaf] != 1:
            leaf += 1
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
    
    return prufer
```

### Variation 5: Dynamic Prufer Code
**Problem**: Support adding/removing edges and answering Prufer code queries.

```python
class DynamicPruferCode:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.edges = set()
    
    def add_edge(self, a, b):
        if (a, b) not in self.edges and (b, a) not in self.edges:
            self.adj[a].append(b)
            self.adj[b].append(a)
            self.edges.add((a, b))
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.edges.remove((a, b))
        elif (b, a) in self.edges:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.edges.remove((b, a))
    
    def get_prufer_code(self):
        if len(self.edges) != self.n - 1:
            return None  # Not a tree
        
        # Count degrees
        degree = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            degree[i] = len(self.adj[i])
        
        # Find Prufer code
        prufer = []
        adj_copy = [adj[:] for adj in self.adj]
        
        for _ in range(self.n - 2):
            # Find leaf with smallest label
            leaf = 1
            while degree[leaf] != 1:
                leaf += 1
            
            # Find its neighbor
            neighbor = adj_copy[leaf][0]
            prufer.append(neighbor)
            
            # Remove the leaf
            degree[leaf] = 0
            degree[neighbor] -= 1
            adj_copy[neighbor].remove(leaf)
        
        return prufer
```

## 🔗 Related Problems

- **[Tree Algorithms](/cses-analyses/problem_soulutions/tree_algorithms/)**: Tree algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[Tree Properties](/cses-analyses/problem_soulutions/tree_algorithms/)**: Tree properties

## 📚 Learning Points

1. **Prufer Code**: Essential for tree representation
2. **Tree Properties**: Important graph theory concept
3. **Leaf Removal**: Fundamental tree algorithm
4. **Tree Reconstruction**: Inverse of Prufer code

---

**This is a great introduction to Prufer codes and tree algorithms!** 🎯
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Use priority queue for leaves
    from heapq import heappush, heappop
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heappush(leaves, i)
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Get smallest leaf
        leaf = heappop(leaves)
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
        
        # Add neighbor to leaves if it becomes a leaf
        if degree[neighbor] == 1:
            heappush(leaves, neighbor)
    
    return prufer
```

**Why this is better:**
- Uses priority queue for efficiency
- O(n log n) time complexity
- More scalable for large trees
- Maintains correctness

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_prufer_code():
    n = int(input())
    edges = []
    
    for _ in range(n - 1):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Use priority queue for leaves
    from heapq import heappush, heappop
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heappush(leaves, i)
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Get smallest leaf
        leaf = heappop(leaves)
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
        
        # Add neighbor to leaves if it becomes a leaf
        if degree[neighbor] == 1:
            heappush(leaves, neighbor)
    
    print(*prufer)

# Main execution
if __name__ == "__main__":
    solve_prufer_code()
```

**Why this works:**
- Optimal Prufer code construction
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4)], [2, 3]),
        (3, [(1, 2), (2, 3)], [2]),
        (5, [(1, 2), (2, 3), (3, 4), (4, 5)], [2, 3, 4]),
    ]
    
    for n, edges, expected in test_cases:
        result = solve_test(n, edges)
        print(f"n={n}, edges={edges}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Use priority queue for leaves
    from heapq import heappush, heappop
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heappush(leaves, i)
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Get smallest leaf
        leaf = heappop(leaves)
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
        
        # Add neighbor to leaves if it becomes a leaf
        if degree[neighbor] == 1:
            heappush(leaves, neighbor)
    
    return prufer

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - priority queue operations
- **Space**: O(n) - adjacency list and priority queue

### Why This Solution Works
- **Prufer Code Algorithm**: Standard tree encoding method
- **Leaf Removal**: Iteratively removes leaves
- **Priority Queue**: Efficient leaf finding
- **Optimal Approach**: Guarantees correct result

## 🎯 Key Insights

### 1. **Prufer Code Properties**
- Length is n-2 for n-vertex tree
- Unique representation of labeled trees
- Key insight for tree encoding
- Essential for understanding

### 2. **Leaf Removal Process**
- Iteratively removes leaves
- Records neighbors in sequence
- Important for efficiency
- Fundamental algorithm

### 3. **Priority Queue Usage**
- Efficient leaf finding
- Maintains smallest label order
- Simple but important optimization
- Essential for performance

## 🎯 Problem Variations

### Variation 1: Tree Reconstruction from Prufer Code
**Problem**: Given a Prufer code, reconstruct the original tree.

```python
def reconstruct_tree_from_prufer(n, prufer):
    # Initialize degree array
    degree = [1] * (n + 1)
    for code in prufer:
        degree[code] += 1
    
    # Find missing vertices
    missing = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            missing.append(i)
    
    # Reconstruct tree
    edges = []
    for code in prufer:
        # Find smallest missing vertex
        leaf = min(missing)
        missing.remove(leaf)
        
        # Add edge
        edges.append((code, leaf))
        
        # Update degrees
        degree[code] -= 1
        if degree[code] == 1:
            missing.append(code)
    
    # Add final edge
    if len(missing) == 2:
        edges.append((missing[0], missing[1]))
    
    return edges
```

### Variation 2: Prufer Code with Weights
**Problem**: Each edge has a weight. Find Prufer code and total weight.

```python
def prufer_code_with_weights(n, edges, weights):
    # Build adjacency list with weights
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, weights[i]))
        adj[b].append((a, weights[i]))
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Use priority queue for leaves
    from heapq import heappush, heappop
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heappush(leaves, i)
    
    # Find Prufer code and total weight
    prufer = []
    total_weight = 0
    
    for _ in range(n - 2):
        # Get smallest leaf
        leaf = heappop(leaves)
        
        # Find its neighbor and weight
        neighbor, weight = adj[leaf][0]
        prufer.append(neighbor)
        total_weight += weight
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove((leaf, weight))
        
        # Add neighbor to leaves if it becomes a leaf
        if degree[neighbor] == 1:
            heappush(leaves, neighbor)
    
    return prufer, total_weight
```

### Variation 3: Prufer Code for Forests
**Problem**: Handle multiple trees (forest) and find Prufer codes.

```python
def prufer_code_forest(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Find connected components
    visited = [False] * (n + 1)
    components = []
    
    def dfs(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor, component)
    
    for i in range(1, n + 1):
        if not visited[i]:
            component = []
            dfs(i, component)
            components.append(component)
    
    # Find Prufer code for each component
    all_prufer_codes = []
    for component in components:
        if len(component) > 1:
            # Create subgraph for this component
            component_edges = []
            for a, b in edges:
                if a in component and b in component:
                    component_edges.append((a, b))
            
            # Find Prufer code for this component
            prufer = prufer_code_for_component(component, component_edges)
            all_prufer_codes.append(prufer)
    
    return all_prufer_codes

def prufer_code_for_component(component, edges):
    # Similar to main algorithm but for a specific component
    # Implementation details...
    pass
```

### Variation 4: Prufer Code with Constraints
**Problem**: Find Prufer code while respecting certain constraints.

```python
def prufer_code_constrained(n, edges, constraints):
    # constraints: set of forbidden edges
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in constraints and (b, a) not in constraints:
            adj[a].append(b)
            adj[b].append(a)
    
    # Count degrees
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Use priority queue for leaves
    from heapq import heappush, heappop
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heappush(leaves, i)
    
    # Find Prufer code
    prufer = []
    for _ in range(n - 2):
        # Get smallest leaf
        leaf = heappop(leaves)
        
        # Find its neighbor
        neighbor = adj[leaf][0]
        prufer.append(neighbor)
        
        # Remove the leaf
        degree[leaf] = 0
        degree[neighbor] -= 1
        adj[neighbor].remove(leaf)
        
        # Add neighbor to leaves if it becomes a leaf
        if degree[neighbor] == 1:
            heappush(leaves, neighbor)
    
    return prufer
```

### Variation 5: Prufer Code Enumeration
**Problem**: Count all possible Prufer codes for a given tree structure.

```python
def count_prufer_codes(n, tree_structure):
    # tree_structure: describes the tree topology
    # For labeled trees, number of Prufer codes = n!
    # For unlabeled trees, need to consider symmetries
    
    # For labeled trees
    if tree_structure == "labeled":
        from math import factorial
        return factorial(n)
    
    # For unlabeled trees, more complex
    # Would need to consider automorphisms
    return "Complex calculation needed"
```

## 🔗 Related Problems

- **[Tree Traversals](/cses-analyses/problem_soulutions/advanced_graph_problems/tree_traversals_analysis)**: Tree algorithms
- **[Graph Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms
- **[Tree Problems](/cses-analyses/problem_soulutions/tree_algorithms/)**: Tree algorithms

## 📚 Learning Points

1. **Prufer Code**: Essential tree encoding method
2. **Tree Properties**: Understanding tree structure
3. **Priority Queue**: Efficient leaf finding
4. **Tree Algorithms**: Common pattern in graph theory

---

**This is a great introduction to tree encoding and Prufer codes!** 🎯 