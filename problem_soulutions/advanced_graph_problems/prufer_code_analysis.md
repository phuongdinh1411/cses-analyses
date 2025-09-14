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

## Problem Variations

### **Variation 1: Prufer Code with Dynamic Updates**
**Problem**: Handle dynamic tree updates (add/remove/update vertices) while maintaining Prufer code calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic tree management with Prufer code generation.

```python
from collections import defaultdict, deque
import heapq

class DynamicPruferCode:
    def __init__(self, n=None, edges=None):
        self.n = n or 0
        self.edges = edges or []
        self.graph = defaultdict(list)
        self._update_prufer_info()
    
    def _update_prufer_info(self):
        """Update Prufer code information."""
        self.prufer_code = self._calculate_prufer_code()
    
    def _calculate_prufer_code(self):
        """Calculate Prufer code from tree edges."""
        if self.n <= 2:
            return []
        
        # Build adjacency list
        adj = defaultdict(list)
        degree = defaultdict(int)
        
        for u, v in self.edges:
            adj[u].append(v)
            adj[v].append(u)
            degree[u] += 1
            degree[v] += 1
        
        # Find leaves (vertices with degree 1)
        leaves = []
        for i in range(self.n):
            if degree[i] == 1:
                leaves.append(i)
        
        prufer_code = []
        
        # Process n-2 times
        for _ in range(self.n - 2):
            # Get the smallest leaf
            leaf = min(leaves)
            leaves.remove(leaf)
            
            # Find its neighbor
            neighbor = adj[leaf][0]
            prufer_code.append(neighbor)
            
            # Update degree and add new leaf if needed
            degree[neighbor] -= 1
            if degree[neighbor] == 1:
                leaves.append(neighbor)
        
        return prufer_code
    
    def update_tree(self, new_n, new_edges):
        """Update the tree with new vertices and edges."""
        self.n = new_n
        self.edges = new_edges
        self._build_graph()
        self._update_prufer_info()
    
    def add_edge(self, u, v):
        """Add an edge to the tree."""
        if 0 <= u < self.n and 0 <= v < self.n and (u, v) not in self.edges and (v, u) not in self.edges:
            self.edges.append((u, v))
            self.graph[u].append(v)
            self.graph[v].append(u)
            self._update_prufer_info()
    
    def remove_edge(self, u, v):
        """Remove an edge from the tree."""
        if (u, v) in self.edges:
            self.edges.remove((u, v))
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            self._update_prufer_info()
        elif (v, u) in self.edges:
            self.edges.remove((v, u))
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            self._update_prufer_info()
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def get_prufer_code(self):
        """Get the current Prufer code."""
        return self.prufer_code
    
    def get_prufer_code_with_priorities(self, priorities):
        """Get Prufer code considering vertex priorities."""
        if not self.prufer_code:
            return []
        
        # Calculate weighted Prufer code based on priorities
        weighted_prufer = []
        for vertex in self.prufer_code:
            priority = priorities.get(vertex, 1)
            weighted_prufer.append((vertex, priority))
        
        return weighted_prufer
    
    def get_prufer_code_with_constraints(self, constraint_func):
        """Get Prufer code that satisfies custom constraints."""
        if not self.prufer_code:
            return []
        
        if constraint_func(self.n, self.edges, self.prufer_code):
            return self.prufer_code
        else:
            return []
    
    def get_prufer_code_in_range(self, min_length, max_length):
        """Get Prufer code within specified length range."""
        if not self.prufer_code:
            return []
        
        if min_length <= len(self.prufer_code) <= max_length:
            return self.prufer_code
        else:
            return []
    
    def get_prufer_code_with_pattern(self, pattern_func):
        """Get Prufer code matching specified pattern."""
        if not self.prufer_code:
            return []
        
        if pattern_func(self.n, self.edges, self.prufer_code):
            return self.prufer_code
        else:
            return []
    
    def get_prufer_statistics(self):
        """Get statistics about the Prufer code."""
        return {
            'n': self.n,
            'edge_count': len(self.edges),
            'prufer_length': len(self.prufer_code),
            'expected_length': max(0, self.n - 2),
            'is_valid_tree': len(self.edges) == self.n - 1
        }
    
    def get_prufer_patterns(self):
        """Get patterns in Prufer code."""
        patterns = {
            'has_edges': 0,
            'has_valid_tree': 0,
            'optimal_prufer_possible': 0,
            'has_large_tree': 0
        }
        
        # Check if has edges
        if len(self.edges) > 0:
            patterns['has_edges'] = 1
        
        # Check if has valid tree
        if len(self.edges) == self.n - 1:
            patterns['has_valid_tree'] = 1
        
        # Check if optimal Prufer is possible
        if len(self.prufer_code) == self.n - 2:
            patterns['optimal_prufer_possible'] = 1
        
        # Check if has large tree
        if self.n > 100:
            patterns['has_large_tree'] = 1
        
        return patterns
    
    def get_optimal_prufer_strategy(self):
        """Get optimal strategy for Prufer code management."""
        if not self.prufer_code:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'prufer_length': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = len(self.prufer_code) / max(1, self.n - 2)
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'greedy_prufer'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_prufer'
        else:
            recommended_strategy = 'advanced_prufer_generation'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'prufer_length': len(self.prufer_code)
        }

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
dynamic_prufer = DynamicPruferCode(n, edges)
print(f"Prufer code: {dynamic_prufer.prufer_code}")

# Update tree
dynamic_prufer.update_tree(6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
print(f"After updating tree: n={dynamic_prufer.n}, prufer_code={dynamic_prufer.prufer_code}")

# Add edge
dynamic_prufer.add_edge(5, 0)
print(f"After adding edge (5,0): {dynamic_prufer.edges}")

# Remove edge
dynamic_prufer.remove_edge(5, 0)
print(f"After removing edge (5,0): {dynamic_prufer.edges}")

# Get Prufer code
prufer = dynamic_prufer.get_prufer_code()
print(f"Prufer code: {prufer}")

# Get Prufer code with priorities
priorities = {i: i for i in range(n)}
priority_prufer = dynamic_prufer.get_prufer_code_with_priorities(priorities)
print(f"Prufer code with priorities: {priority_prufer}")

# Get Prufer code with constraints
def constraint_func(n, edges, prufer_code):
    return len(prufer_code) > 0 and n > 0

print(f"Prufer code with constraints: {dynamic_prufer.get_prufer_code_with_constraints(constraint_func)}")

# Get Prufer code in range
print(f"Prufer code in range 1-5: {dynamic_prufer.get_prufer_code_in_range(1, 5)}")

# Get Prufer code with pattern
def pattern_func(n, edges, prufer_code):
    return len(prufer_code) > 0 and n > 0

print(f"Prufer code with pattern: {dynamic_prufer.get_prufer_code_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_prufer.get_prufer_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_prufer.get_prufer_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_prufer.get_optimal_prufer_strategy()}")
```

### **Variation 2: Prufer Code with Different Operations**
**Problem**: Handle different types of Prufer code operations (weighted codes, priority-based selection, advanced code analysis).

**Approach**: Use advanced data structures for efficient different types of Prufer code operations.

```python
class AdvancedPruferCode:
    def __init__(self, n=None, edges=None, weights=None, priorities=None):
        self.n = n or 0
        self.edges = edges or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.graph = defaultdict(list)
        self._update_prufer_info()
    
    def _update_prufer_info(self):
        """Update Prufer code information."""
        self.prufer_code = self._calculate_prufer_code()
    
    def _calculate_prufer_code(self):
        """Calculate Prufer code from tree edges."""
        if self.n <= 2:
            return []
        
        # Build adjacency list
        adj = defaultdict(list)
        degree = defaultdict(int)
        
        for u, v in self.edges:
            adj[u].append(v)
            adj[v].append(u)
            degree[u] += 1
            degree[v] += 1
        
        # Find leaves (vertices with degree 1)
        leaves = []
        for i in range(self.n):
            if degree[i] == 1:
                leaves.append(i)
        
        prufer_code = []
        
        # Process n-2 times
        for _ in range(self.n - 2):
            # Get the smallest leaf
            leaf = min(leaves)
            leaves.remove(leaf)
            
            # Find its neighbor
            neighbor = adj[leaf][0]
            prufer_code.append(neighbor)
            
            # Update degree and add new leaf if needed
            degree[neighbor] -= 1
            if degree[neighbor] == 1:
                leaves.append(neighbor)
        
        return prufer_code
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def get_prufer_code(self):
        """Get the current Prufer code."""
        return self.prufer_code
    
    def get_weighted_prufer_code(self):
        """Get Prufer code with weights and priorities applied."""
        if not self.prufer_code:
            return []
        
        # Calculate weighted Prufer code based on vertex weights and priorities
        weighted_prufer = []
        for vertex in self.prufer_code:
            vertex_weight = self.weights.get(vertex, 1)
            vertex_priority = self.priorities.get(vertex, 1)
            weighted_score = vertex_weight * vertex_priority
            weighted_prufer.append((vertex, weighted_score))
        
        return weighted_prufer
    
    def get_prufer_code_with_priority(self, priority_func):
        """Get Prufer code considering priority."""
        if not self.prufer_code:
            return []
        
        # Calculate priority-based Prufer code
        priority_prufer = []
        for vertex in self.prufer_code:
            priority = priority_func(vertex, self.weights, self.priorities)
            priority_prufer.append((vertex, priority))
        
        return priority_prufer
    
    def get_prufer_code_with_optimization(self, optimization_func):
        """Get Prufer code using custom optimization function."""
        if not self.prufer_code:
            return []
        
        # Calculate optimization-based Prufer code
        optimized_prufer = []
        for vertex in self.prufer_code:
            score = optimization_func(vertex, self.weights, self.priorities)
            optimized_prufer.append((vertex, score))
        
        return optimized_prufer
    
    def get_prufer_code_with_constraints(self, constraint_func):
        """Get Prufer code that satisfies custom constraints."""
        if not self.prufer_code:
            return []
        
        if constraint_func(self.n, self.edges, self.weights, self.priorities, self.prufer_code):
            return self.get_weighted_prufer_code()
        else:
            return []
    
    def get_prufer_code_with_multiple_criteria(self, criteria_list):
        """Get Prufer code that satisfies multiple criteria."""
        if not self.prufer_code:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.n, self.edges, self.weights, self.priorities, self.prufer_code):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_prufer_code()
        else:
            return []
    
    def get_prufer_code_with_alternatives(self, alternatives):
        """Get Prufer code considering alternative weights/priorities."""
        result = []
        
        # Check original Prufer code
        original_prufer = self.get_weighted_prufer_code()
        result.append((original_prufer, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedPruferCode(self.n, self.edges, alt_weights, alt_priorities)
            temp_prufer = temp_instance.get_weighted_prufer_code()
            result.append((temp_prufer, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_prufer_code_with_adaptive_criteria(self, adaptive_func):
        """Get Prufer code using adaptive criteria."""
        if not self.prufer_code:
            return []
        
        if adaptive_func(self.n, self.edges, self.weights, self.priorities, self.prufer_code, []):
            return self.get_weighted_prufer_code()
        else:
            return []
    
    def get_prufer_code_optimization(self):
        """Get optimal Prufer code configuration."""
        strategies = [
            ('weighted_prufer', lambda: len(self.get_weighted_prufer_code())),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
weights = {i: i + 1 for i in range(n)}  # Weight based on vertex number
priorities = {i: i for i in range(n)}  # Priority based on vertex number
advanced_prufer = AdvancedPruferCode(n, edges, weights, priorities)

print(f"Weighted Prufer code: {advanced_prufer.get_weighted_prufer_code()}")

# Get Prufer code with priority
def priority_func(vertex, weights, priorities):
    return priorities.get(vertex, 1) + weights.get(vertex, 1)

print(f"Prufer code with priority: {advanced_prufer.get_prufer_code_with_priority(priority_func)}")

# Get Prufer code with optimization
def optimization_func(vertex, weights, priorities):
    return weights.get(vertex, 1) + priorities.get(vertex, 1)

print(f"Prufer code with optimization: {advanced_prufer.get_prufer_code_with_optimization(optimization_func)}")

# Get Prufer code with constraints
def constraint_func(n, edges, weights, priorities, prufer_code):
    return len(prufer_code) > 0 and n > 0

print(f"Prufer code with constraints: {advanced_prufer.get_prufer_code_with_constraints(constraint_func)}")

# Get Prufer code with multiple criteria
def criterion1(n, edges, weights, priorities, prufer_code):
    return len(edges) > 0

def criterion2(n, edges, weights, priorities, prufer_code):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Prufer code with multiple criteria: {advanced_prufer.get_prufer_code_with_multiple_criteria(criteria_list)}")

# Get Prufer code with alternatives
alternatives = [({i: 1 for i in range(n)}, {i: 1 for i in range(n)}), ({i: (i + 1)*3 for i in range(n)}, {i: 2 for i in range(n)})]
print(f"Prufer code with alternatives: {advanced_prufer.get_prufer_code_with_alternatives(alternatives)}")

# Get Prufer code with adaptive criteria
def adaptive_func(n, edges, weights, priorities, prufer_code, current_result):
    return len(edges) > 0 and len(current_result) < 10

print(f"Prufer code with adaptive criteria: {advanced_prufer.get_prufer_code_with_adaptive_criteria(adaptive_func)}")

# Get Prufer code optimization
print(f"Prufer code optimization: {advanced_prufer.get_prufer_code_optimization()}")
```

### **Variation 3: Prufer Code with Constraints**
**Problem**: Handle Prufer code calculation with additional constraints (length limits, code constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedPruferCode:
    def __init__(self, n=None, edges=None, constraints=None):
        self.n = n or 0
        self.edges = edges or []
        self.constraints = constraints or {}
        self.graph = defaultdict(list)
        self._update_prufer_info()
    
    def _update_prufer_info(self):
        """Update Prufer code information."""
        self.prufer_code = self._calculate_prufer_code()
    
    def _calculate_prufer_code(self):
        """Calculate Prufer code from tree edges."""
        if self.n <= 2:
            return []
        
        # Build adjacency list
        adj = defaultdict(list)
        degree = defaultdict(int)
        
        for u, v in self.edges:
            adj[u].append(v)
            adj[v].append(u)
            degree[u] += 1
            degree[v] += 1
        
        # Find leaves (vertices with degree 1)
        leaves = []
        for i in range(self.n):
            if degree[i] == 1:
                leaves.append(i)
        
        prufer_code = []
        
        # Process n-2 times
        for _ in range(self.n - 2):
            # Get the smallest leaf
            leaf = min(leaves)
            leaves.remove(leaf)
            
            # Find its neighbor
            neighbor = adj[leaf][0]
            prufer_code.append(neighbor)
            
            # Update degree and add new leaf if needed
            degree[neighbor] -= 1
            if degree[neighbor] == 1:
                leaves.append(neighbor)
        
        return prufer_code
    
    def _is_valid_edge(self, u, v):
        """Check if edge is valid considering constraints."""
        # Edge constraints
        if 'allowed_edges' in self.constraints:
            if (u, v) not in self.constraints['allowed_edges'] and (v, u) not in self.constraints['allowed_edges']:
                return False
        
        if 'forbidden_edges' in self.constraints:
            if (u, v) in self.constraints['forbidden_edges'] or (v, u) in self.constraints['forbidden_edges']:
                return False
        
        # Vertex constraints
        if 'max_vertex' in self.constraints:
            if u > self.constraints['max_vertex'] or v > self.constraints['max_vertex']:
                return False
        
        if 'min_vertex' in self.constraints:
            if u < self.constraints['min_vertex'] or v < self.constraints['min_vertex']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(u, v, self.n, self.edges, self.prufer_code):
                    return False
        
        return True
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            if self._is_valid_edge(u, v):
                self.graph[u].append(v)
                self.graph[v].append(u)
    
    def get_prufer_code(self):
        """Get the current Prufer code."""
        return self.prufer_code
    
    def get_prufer_code_with_length_constraints(self, min_length, max_length):
        """Get Prufer code considering length constraints."""
        if not self.prufer_code:
            return []
        
        if min_length <= len(self.prufer_code) <= max_length:
            return self.prufer_code
        else:
            return []
    
    def get_prufer_code_with_code_constraints(self, code_constraints):
        """Get Prufer code considering code constraints."""
        if not self.prufer_code:
            return []
        
        satisfies_constraints = True
        for constraint in code_constraints:
            if not constraint(self.n, self.edges, self.prufer_code):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self.prufer_code
        else:
            return []
    
    def get_prufer_code_with_pattern_constraints(self, pattern_constraints):
        """Get Prufer code considering pattern constraints."""
        if not self.prufer_code:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.n, self.edges, self.prufer_code):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self.prufer_code
        else:
            return []
    
    def get_prufer_code_with_mathematical_constraints(self, constraint_func):
        """Get Prufer code that satisfies custom mathematical constraints."""
        if not self.prufer_code:
            return []
        
        if constraint_func(self.n, self.edges, self.prufer_code):
            return self.prufer_code
        else:
            return []
    
    def get_prufer_code_with_optimization_constraints(self, optimization_func):
        """Get Prufer code using custom optimization constraints."""
        if not self.prufer_code:
            return []
        
        # Calculate optimization score for Prufer code
        score = optimization_func(self.n, self.edges, self.prufer_code)
        
        if score > 0:
            return self.prufer_code
        else:
            return []
    
    def get_prufer_code_with_multiple_constraints(self, constraints_list):
        """Get Prufer code that satisfies multiple constraints."""
        if not self.prufer_code:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.n, self.edges, self.prufer_code):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self.prufer_code
        else:
            return []
    
    def get_prufer_code_with_priority_constraints(self, priority_func):
        """Get Prufer code with priority-based constraints."""
        if not self.prufer_code:
            return []
        
        # Calculate priority for Prufer code
        priority = priority_func(self.n, self.edges, self.prufer_code)
        
        if priority > 0:
            return self.prufer_code
        else:
            return []
    
    def get_prufer_code_with_adaptive_constraints(self, adaptive_func):
        """Get Prufer code with adaptive constraints."""
        if not self.prufer_code:
            return []
        
        if adaptive_func(self.n, self.edges, self.prufer_code, []):
            return self.prufer_code
        else:
            return []
    
    def get_optimal_prufer_code_strategy(self):
        """Get optimal Prufer code strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_prufer_code_with_length_constraints),
            ('code_constraints', self.get_prufer_code_with_code_constraints),
            ('pattern_constraints', self.get_prufer_code_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'code_constraints':
                    code_constraints = [lambda n, edges, prufer_code: len(edges) > 0]
                    result = strategy_func(code_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda n, edges, prufer_code: len(edges) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_edges': [(0, 1), (1, 2), (2, 3), (3, 4)],
    'forbidden_edges': [(0, 2), (1, 3)],
    'max_vertex': 10,
    'min_vertex': 0,
    'pattern_constraints': [lambda u, v, n, edges, prufer_code: u >= 0 and v >= 0 and u < n and v < n]
}

n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
constrained_prufer = ConstrainedPruferCode(n, edges, constraints)

print("Length-constrained Prufer code:", constrained_prufer.get_prufer_code_with_length_constraints(1, 5))

print("Code-constrained Prufer code:", constrained_prufer.get_prufer_code_with_code_constraints([lambda n, edges, prufer_code: len(edges) > 0]))

print("Pattern-constrained Prufer code:", constrained_prufer.get_prufer_code_with_pattern_constraints([lambda n, edges, prufer_code: len(edges) > 0]))

# Mathematical constraints
def custom_constraint(n, edges, prufer_code):
    return len(prufer_code) > 0 and n > 0

print("Mathematical constraint Prufer code:", constrained_prufer.get_prufer_code_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(n, edges, prufer_code):
    return 1 <= len(prufer_code) <= 20

range_constraints = [range_constraint]
print("Range-constrained Prufer code:", constrained_prufer.get_prufer_code_with_length_constraints(1, 20))

# Multiple constraints
def constraint1(n, edges, prufer_code):
    return len(edges) > 0

def constraint2(n, edges, prufer_code):
    return len(prufer_code) > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints Prufer code:", constrained_prufer.get_prufer_code_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(n, edges, prufer_code):
    return n + len(edges) + len(prufer_code)

print("Priority-constrained Prufer code:", constrained_prufer.get_prufer_code_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(n, edges, prufer_code, current_result):
    return len(edges) > 0 and len(current_result) < 10

print("Adaptive constraint Prufer code:", constrained_prufer.get_prufer_code_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_prufer.get_optimal_prufer_code_strategy()
print(f"Optimal Prufer code strategy: {optimal}")
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
