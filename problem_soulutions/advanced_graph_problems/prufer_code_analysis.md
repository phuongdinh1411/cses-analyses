---
layout: simple
title: "Prufer Code - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/prufer_code_analysis
---

# Prufer Code - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Prufer codes for tree representation
- Apply graph theory principles to encode and decode trees
- Implement algorithms for Prufer code generation and reconstruction
- Optimize tree operations using Prufer codes
- Handle special cases in tree encoding and decoding

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, tree algorithms, Prufer codes, tree traversal
- **Data Structures**: Trees, adjacency lists, priority queues, arrays
- **Mathematical Concepts**: Graph theory, tree properties, combinatorial encoding
- **Programming Skills**: Tree representation, DFS, BFS, array operations
- **Related Problems**: Tree Traversals (tree operations), Tree Diameter (tree properties), Tree Queries (tree algorithms)

## 📋 Problem Description

Given a tree with n nodes, generate its Prufer code and reconstruct the tree from a Prufer code.

**Input**: 
- n: number of nodes
- n-1 lines: a b (undirected edge between nodes a and b)

**Output**: 
- Prufer code of the tree

**Constraints**:
- 1 ≤ n ≤ 10^5
- Tree is connected and has no cycles

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
Tree: 1-2-3-4
Prufer code: [2, 3]
Process: Remove leaf 1, add 2 to code; remove leaf 2, add 3 to code; stop
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Sequential Removal**: Remove leaves one by one in order
- **Code Generation**: Add parent of removed leaf to Prufer code
- **Tree Reconstruction**: Build tree by adding edges in reverse order
- **Baseline Understanding**: Provides correct answer but inefficient for large trees

**Key Insight**: Remove leaves sequentially and add their parents to the Prufer code.

**Algorithm**:
- Find all leaves in the tree
- Remove the smallest leaf and add its parent to the code
- Repeat until only 2 nodes remain
- Return the Prufer code

**Visual Example**:
```
Tree: 1-2-3-4

Step 1: Remove leaf 1, add parent 2 to code
┌─────────────────────────────────────┐
│ Tree: 2-3-4                        │
│ Code: [2]                          │
└─────────────────────────────────────┘

Step 2: Remove leaf 2, add parent 3 to code
┌─────────────────────────────────────┐
│ Tree: 3-4                          │
│ Code: [2, 3]                       │
└─────────────────────────────────────┘

Step 3: Stop (only 2 nodes remain)
Final Prufer code: [2, 3]
```

**Implementation**:
```python
def brute_force_solution(n, edges):
    """
    Generate Prufer code using brute force approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        list: Prufer code
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def generate_prufer_code():
        """Generate Prufer code by removing leaves sequentially"""
        # Create a copy of adjacency list
        temp_adj = [list(neighbors) for neighbors in adj]
        
        prufer_code = []
        
        # Repeat until only 2 nodes remain
        while len(prufer_code) < n - 2:
            # Find all leaves
            leaves = []
            for i in range(n):
                if len(temp_adj[i]) == 1:
                    leaves.append(i)
            
            # Find the smallest leaf
            smallest_leaf = min(leaves)
            
            # Get its parent
            parent = temp_adj[smallest_leaf][0]
            
            # Add parent to Prufer code
            prufer_code.append(parent + 1)  # Convert back to 1-indexed
            
            # Remove the leaf
            temp_adj[smallest_leaf].remove(parent)
            temp_adj[parent].remove(smallest_leaf)
        
        return prufer_code
    
    return generate_prufer_code()

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = brute_force_solution(n, edges)
print(f"Brute force result: {result}")  # Output: [2, 3]
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n²) time complexity due to repeated leaf finding.

---

### Approach 2: Optimized Leaf Removal Solution

**Key Insights from Optimized Leaf Removal Solution**:
- **Leaf Tracking**: Maintain a set of current leaves
- **Efficient Updates**: Update leaf set when removing nodes
- **Priority Queue**: Use priority queue for efficient smallest leaf finding
- **Optimization**: Much more efficient than brute force

**Key Insight**: Maintain a set of current leaves and use a priority queue for efficient smallest leaf finding.

**Algorithm**:
- Initialize leaf set with all leaves
- Use priority queue to find smallest leaf efficiently
- Update leaf set when removing nodes
- Generate Prufer code efficiently

**Visual Example**:
```
Tree: 1-2-3-4

Initial leaves: {1, 4}
Priority queue: [1, 4]

Step 1: Remove leaf 1, add parent 2 to code
┌─────────────────────────────────────┐
│ Tree: 2-3-4                        │
│ Code: [2]                          │
│ Leaves: {2, 4}                     │
└─────────────────────────────────────┘

Step 2: Remove leaf 2, add parent 3 to code
┌─────────────────────────────────────┐
│ Tree: 3-4                          │
│ Code: [2, 3]                       │
│ Leaves: {3, 4}                     │
└─────────────────────────────────────┘

Final Prufer code: [2, 3]
```

**Implementation**:
```python
def optimized_leaf_removal_solution(n, edges):
    """
    Generate Prufer code using optimized leaf removal
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        list: Prufer code
    """
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def generate_prufer_code():
        """Generate Prufer code using optimized leaf removal"""
        # Create a copy of adjacency list
        temp_adj = [list(neighbors) for neighbors in adj]
        
        # Find all leaves and add to priority queue
        leaves = []
        for i in range(n):
            if len(temp_adj[i]) == 1:
                leaves.append(i)
        
        heapq.heapify(leaves)
        
        prufer_code = []
        
        # Repeat until only 2 nodes remain
        while len(prufer_code) < n - 2:
            # Get the smallest leaf
            smallest_leaf = heapq.heappop(leaves)
            
            # Get its parent
            parent = temp_adj[smallest_leaf][0]
            
            # Add parent to Prufer code
            prufer_code.append(parent + 1)  # Convert back to 1-indexed
            
            # Remove the leaf
            temp_adj[smallest_leaf].remove(parent)
            temp_adj[parent].remove(smallest_leaf)
            
            # Check if parent became a leaf
            if len(temp_adj[parent]) == 1:
                heapq.heappush(leaves, parent)
        
        return prufer_code
    
    return generate_prufer_code()

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = optimized_leaf_removal_solution(n, edges)
print(f"Optimized leaf removal result: {result}")  # Output: [2, 3]
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's better**: O(n log n) time complexity, much more efficient than brute force.

**Implementation Considerations**:
- **Priority Queue**: Use heapq for efficient smallest leaf finding
- **Leaf Updates**: Update leaf set when removing nodes
- **Memory Management**: Use efficient data structures

---

### Approach 3: Linear Time Solution (Optimal)

**Key Insights from Linear Time Solution**:
- **Degree Tracking**: Track degrees of all nodes
- **Leaf Queue**: Maintain queue of current leaves
- **Efficient Updates**: Update degrees and leaf queue efficiently
- **Optimal Complexity**: O(n) time complexity

**Key Insight**: Use degree tracking and a simple queue for efficient leaf removal.

**Algorithm**:
- Track degrees of all nodes
- Maintain queue of current leaves
- Remove leaves and update degrees efficiently
- Generate Prufer code in linear time

**Visual Example**:
```
Tree: 1-2-3-4

Initial degrees: [1, 2, 2, 1]
Leaf queue: [0, 3] (nodes 1 and 4)

Step 1: Remove leaf 0, add parent 1 to code
┌─────────────────────────────────────┐
│ Tree: 2-3-4                        │
│ Code: [2]                          │
│ Degrees: [0, 1, 2, 1]              │
│ Leaf queue: [1, 3]                 │
└─────────────────────────────────────┘

Step 2: Remove leaf 1, add parent 2 to code
┌─────────────────────────────────────┐
│ Tree: 3-4                          │
│ Code: [2, 3]                       │
│ Degrees: [0, 0, 1, 1]              │
│ Leaf queue: [2, 3]                 │
└─────────────────────────────────────┘

Final Prufer code: [2, 3]
```

**Implementation**:
```python
def linear_time_solution(n, edges):
    """
    Generate Prufer code using linear time algorithm
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        list: Prufer code
    """
    from collections import deque
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def generate_prufer_code():
        """Generate Prufer code using linear time algorithm"""
        # Track degrees of all nodes
        degrees = [len(neighbors) for neighbors in adj]
        
        # Find all leaves and add to queue
        leaf_queue = deque()
        for i in range(n):
            if degrees[i] == 1:
                leaf_queue.append(i)
        
        prufer_code = []
        
        # Repeat until only 2 nodes remain
        while len(prufer_code) < n - 2:
            # Get the smallest leaf
            smallest_leaf = leaf_queue.popleft()
            
            # Get its parent
            parent = adj[smallest_leaf][0]
            
            # Add parent to Prufer code
            prufer_code.append(parent + 1)  # Convert back to 1-indexed
            
            # Update degrees
            degrees[smallest_leaf] -= 1
            degrees[parent] -= 1
            
            # Check if parent became a leaf
            if degrees[parent] == 1:
                leaf_queue.append(parent)
        
        return prufer_code
    
    return generate_prufer_code()

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = linear_time_solution(n, edges)
print(f"Linear time result: {result}")  # Output: [2, 3]
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's optimal**: O(n) time complexity is optimal for this problem.

**Implementation Details**:
- **Degree Tracking**: Track degrees of all nodes efficiently
- **Leaf Queue**: Use deque for efficient leaf management
- **Linear Updates**: Update degrees and leaf queue in constant time
- **Memory Efficiency**: Use optimal data structures

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Remove leaves sequentially |
| Optimized Leaf Removal | O(n log n) | O(n) | Use priority queue for leaves |
| Linear Time | O(n) | O(n) | Use degree tracking and queue |

### Time Complexity
- **Time**: O(n) - Generate Prufer code in linear time
- **Space**: O(n) - Store graph and degree information

### Why This Solution Works
- **Degree Tracking**: Track degrees of all nodes efficiently
- **Leaf Management**: Use queue for efficient leaf removal
- **Linear Updates**: Update degrees and leaf queue in constant time
- **Optimal Algorithm**: Use linear time algorithm for efficiency

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Prufer Code to Tree Reconstruction**
**Problem**: Reconstruct a tree from its Prufer code.

**Key Differences**: Reverse process - build tree from code

**Solution Approach**: Use Prufer code to reconstruct tree edges

**Implementation**:
```python
def prufer_to_tree(n, prufer_code):
    """
    Reconstruct tree from Prufer code
    
    Args:
        n: number of nodes
        prufer_code: list of Prufer code values
    
    Returns:
        list: list of edges in the reconstructed tree
    """
    # Convert to 0-indexed
    code = [x - 1 for x in prufer_code]
    
    # Track degrees of all nodes
    degrees = [1] * n  # All nodes start with degree 1
    
    # Count occurrences in Prufer code
    for node in code:
        degrees[node] += 1
    
    # Find all leaves
    leaves = []
    for i in range(n):
        if degrees[i] == 1:
            leaves.append(i)
    
    # Build tree edges
    edges = []
    
    for i in range(len(code)):
        # Get the smallest leaf
        smallest_leaf = min(leaves)
        
        # Add edge from leaf to current code element
        edges.append((smallest_leaf + 1, code[i] + 1))  # Convert back to 1-indexed
        
        # Remove leaf from leaves
        leaves.remove(smallest_leaf)
        
        # Update degree of current code element
        degrees[code[i]] -= 1
        
        # Check if it became a leaf
        if degrees[code[i]] == 1:
            leaves.append(code[i])
    
    # Add final edge between remaining two leaves
    if len(leaves) == 2:
        edges.append((leaves[0] + 1, leaves[1] + 1))  # Convert back to 1-indexed
    
    return edges

# Example usage
n = 4
prufer_code = [2, 3]
result = prufer_to_tree(n, prufer_code)
print(f"Prufer to tree result: {result}")
```

#### **2. Weighted Tree Prufer Code**
**Problem**: Generate Prufer code for weighted trees.

**Key Differences**: Consider edge weights in the encoding

**Solution Approach**: Use weighted tree properties for Prufer code generation

**Implementation**:
```python
def weighted_tree_prufer_code(n, edges, weights):
    """
    Generate Prufer code for weighted tree
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        weights: list of edge weights
    
    Returns:
        list: Prufer code with weight information
    """
    # Build adjacency list with weights
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        adj[a-1].append((b-1, weights[i]))  # Convert to 0-indexed
        adj[b-1].append((a-1, weights[i]))  # Undirected edge
    
    def generate_weighted_prufer_code():
        """Generate Prufer code with weight information"""
        from collections import deque
        
        # Track degrees of all nodes
        degrees = [len(neighbors) for neighbors in adj]
        
        # Find all leaves and add to queue
        leaf_queue = deque()
        for i in range(n):
            if degrees[i] == 1:
                leaf_queue.append(i)
        
        prufer_code = []
        
        # Repeat until only 2 nodes remain
        while len(prufer_code) < n - 2:
            # Get the smallest leaf
            smallest_leaf = leaf_queue.popleft()
            
            # Get its parent and weight
            parent, weight = adj[smallest_leaf][0]
            
            # Add parent and weight to Prufer code
            prufer_code.append((parent + 1, weight))  # Convert back to 1-indexed
            
            # Update degrees
            degrees[smallest_leaf] -= 1
            degrees[parent] -= 1
            
            # Check if parent became a leaf
            if degrees[parent] == 1:
                leaf_queue.append(parent)
        
        return prufer_code
    
    return generate_weighted_prufer_code()

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
weights = [1, 2, 3]
result = weighted_tree_prufer_code(n, edges, weights)
print(f"Weighted tree Prufer code result: {result}")
```

#### **3. Dynamic Tree Prufer Code**
**Problem**: Support adding/removing edges and maintain Prufer code.

**Key Differences**: Tree structure can change dynamically

**Solution Approach**: Use dynamic tree maintenance with incremental updates

**Implementation**:
```python
class DynamicTreePruferCode:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.prufer_cache = None
    
    def add_edge(self, a, b):
        """Add undirected edge between a and b"""
        if b not in self.adj[a]:
            self.adj[a].append(b)
            self.adj[b].append(a)
            self.prufer_cache = None  # Invalidate cache
    
    def remove_edge(self, a, b):
        """Remove undirected edge between a and b"""
        if b in self.adj[a]:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.prufer_cache = None  # Invalidate cache
    
    def get_prufer_code(self):
        """Get current Prufer code"""
        if self.prufer_cache is None:
            self._compute_prufer_code()
        
        return self.prufer_cache
    
    def _compute_prufer_code(self):
        """Compute Prufer code for current tree"""
        from collections import deque
        
        # Track degrees of all nodes
        degrees = [len(neighbors) for neighbors in self.adj]
        
        # Find all leaves and add to queue
        leaf_queue = deque()
        for i in range(self.n):
            if degrees[i] == 1:
                leaf_queue.append(i)
        
        prufer_code = []
        
        # Repeat until only 2 nodes remain
        while len(prufer_code) < self.n - 2:
            # Get the smallest leaf
            smallest_leaf = leaf_queue.popleft()
            
            # Get its parent
            parent = self.adj[smallest_leaf][0]
            
            # Add parent to Prufer code
            prufer_code.append(parent + 1)  # Convert back to 1-indexed
            
            # Update degrees
            degrees[smallest_leaf] -= 1
            degrees[parent] -= 1
            
            # Check if parent became a leaf
            if degrees[parent] == 1:
                leaf_queue.append(parent)
        
        self.prufer_cache = prufer_code

# Example usage
dtpc = DynamicTreePruferCode(4)
dtpc.add_edge(0, 1)
dtpc.add_edge(1, 2)
dtpc.add_edge(2, 3)
result1 = dtpc.get_prufer_code()
print(f"Dynamic tree Prufer code result: {result1}")
```

### Related Problems

#### **CSES Problems**
- [Tree Traversals](https://cses.fi/problemset/task/1707) - Tree operations
- [Tree Diameter](https://cses.fi/problemset/task/1707) - Tree properties
- [Tree Queries](https://cses.fi/problemset/task/1707) - Tree algorithms

#### **LeetCode Problems**
- [Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/) - Tree traversal
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Tree algorithms

#### **Problem Categories**
- **Graph Theory**: Tree algorithms, Prufer codes
- **Combinatorial Encoding**: Tree representation, encoding algorithms
- **Data Structures**: Tree operations, efficient algorithms

## 🔗 Additional Resources

### **Algorithm References**
- [Prufer Code](https://cp-algorithms.com/graph/pruefer_code.html) - Prufer code algorithms
- [Tree Algorithms](https://cp-algorithms.com/graph/tree_algorithms.html) - Tree algorithms
- [Combinatorial Encoding](https://cp-algorithms.com/combinatorics/) - Encoding techniques

### **Practice Problems**
- [CSES Tree Traversals](https://cses.fi/problemset/task/1707) - Medium
- [CSES Tree Diameter](https://cses.fi/problemset/task/1707) - Medium
- [CSES Tree Queries](https://cses.fi/problemset/task/1707) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
