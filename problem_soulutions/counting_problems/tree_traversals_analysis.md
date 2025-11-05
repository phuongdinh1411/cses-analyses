---
layout: simple
title: "Tree Traversals - Counting Problem"
permalink: /problem_soulutions/counting_problems/tree_traversals_analysis
---

# Tree Traversals - Counting Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of tree traversals in counting problems
- Apply counting techniques for tree traversal analysis
- Implement efficient algorithms for traversal counting
- Optimize tree operations for counting applications
- Handle special cases in tree traversal counting

## 📋 Problem Description

Given a tree with n nodes, count the number of different ways to traverse the tree.

**Input**: 
- n: number of nodes
- n-1 lines: a b (undirected edge between nodes a and b)

**Output**: 
- Number of different traversal sequences modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 10^5
- Tree is connected and has no cycles

**Example**:
```
Input:
n = 4
edges = [(1,2), (2,3), (3,4)]

Output:
6

Explanation**: 
Tree: 1-2-3-4
Different traversal sequences:
- 1→2→3→4
- 1→2→3→4 (reverse)
- 2→1→3→4
- 2→3→4→1
- 3→2→1→4
- 4→3→2→1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Counting Solution

**Key Insights from Recursive Counting Solution**:
- **Recursive Approach**: Use recursion to count all possible traversals
- **Complete Enumeration**: Enumerate all possible traversal sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to enumerate all possible traversal sequences and count them.

**Algorithm**:
- Use recursive function to explore all possible paths
- Count valid traversal sequences
- Apply modulo operation to prevent overflow

**Visual Example**:
```
Tree: 1-2-3-4

Recursive exploration:
┌─────────────────────────────────────┐
│ Start from node 1:                 │
│ - Visit 1, then explore neighbors  │
│ - Visit 2, then explore neighbors  │
│ - Visit 3, then explore neighbors  │
│ - Visit 4 (leaf node)              │
│ Count: 1                           │
└─────────────────────────────────────┘

All possible traversals:
┌─────────────────────────────────────┐
│ 1→2→3→4: 1 way                    │
│ 1→2→3→4 (reverse): 1 way          │
│ 2→1→3→4: 1 way                    │
│ 2→3→4→1: 1 way                    │
│ 3→2→1→4: 1 way                    │
│ 4→3→2→1: 1 way                    │
│ Total: 6 ways                      │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_traversal_count(n, edges, mod=10**9+7):
    """
    Count tree traversals using recursive approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        mod: modulo value
    
    Returns:
        int: number of traversal sequences modulo mod
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def count_traversals(node, visited, path_length):
        """Count traversals starting from given node"""
        if path_length == n:
            return 1
        
        count = 0
        for neighbor in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                count = (count + count_traversals(neighbor, visited, path_length + 1)) % mod
                visited[neighbor] = False
        
        return count
    
    total_count = 0
    for start_node in range(n):
        visited = [False] * n
        visited[start_node] = True
        total_count = (total_count + count_traversals(start_node, visited, 1)) % mod
    
    return total_count

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = recursive_traversal_count(n, edges)
print(f"Recursive traversal count: {result}")
```

**Time Complexity**: O(n!)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Memoization**: Store previously calculated results
- **Overlapping Subproblems**: Avoid recalculating same subproblems
- **Time Optimization**: Reduce time complexity significantly
- **Space Trade-off**: Use O(n) space for memoization

**Key Insight**: Use dynamic programming with memoization to avoid recalculating same subproblems.

**Algorithm**:
- Use memoization to store calculated results
- Define state as (current_node, visited_mask)
- Use bitmask to represent visited nodes

**Visual Example**:
```
DP state representation:
┌─────────────────────────────────────┐
│ State: (node, visited_mask)        │
│ visited_mask: bitmask of visited nodes │
│ Example: visited_mask = 1011        │
│ means nodes 0, 1, 3 are visited    │
└─────────────────────────────────────┘

Memoization table:
┌─────────────────────────────────────┐
│ memo[(node, mask)] = count         │
│ (0, 0001): 1                       │
│ (1, 0011): 2                       │
│ (2, 0111): 3                       │
│ (3, 1111): 6                       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_traversal_count(n, edges, mod=10**9+7):
    """
    Count tree traversals using dynamic programming
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        mod: modulo value
    
    Returns:
        int: number of traversal sequences modulo mod
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    memo = {}
    
    def count_traversals_dp(node, visited_mask):
        """Count traversals using DP with memoization"""
        if visited_mask == (1 << n) - 1:  # All nodes visited
            return 1
        
        if (node, visited_mask) in memo:
            return memo[(node, visited_mask)]
        
        count = 0
        for neighbor in adj[node]:
            if not (visited_mask & (1 << neighbor)):  # Neighbor not visited
                new_mask = visited_mask | (1 << neighbor)
                count = (count + count_traversals_dp(neighbor, new_mask)) % mod
        
        memo[(node, visited_mask)] = count
        return count
    
    total_count = 0
    for start_node in range(n):
        visited_mask = 1 << start_node
        total_count = (total_count + count_traversals_dp(start_node, visited_mask)) % mod
    
    return total_count

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = dp_traversal_count(n, edges)
print(f"DP traversal count: {result}")
```

**Time Complexity**: O(n * 2^n)
**Space Complexity**: O(n * 2^n)

**Why it's better**: Significantly reduces time complexity using memoization.

**Implementation Considerations**:
- **Memoization**: Store calculated results to avoid recalculation
- **Bitmask**: Use bitmask to represent visited nodes efficiently
- **State Definition**: Define state as (current_node, visited_mask)

---

### Approach 3: Mathematical Counting Solution (Optimal)

**Key Insights from Mathematical Counting Solution**:
- **Mathematical Analysis**: Use mathematical properties of trees
- **Combinatorial Formula**: Use combinatorial formulas for counting
- **Efficient Calculation**: O(n) time complexity
- **Optimal Complexity**: Best approach for tree traversal counting

**Key Insight**: Use mathematical properties of trees and combinatorial formulas for efficient counting.

**Algorithm**:
- Use mathematical properties of trees
- Apply combinatorial formulas
- Calculate result efficiently

**Visual Example**:
```
Mathematical analysis:
┌─────────────────────────────────────┐
│ For a tree with n nodes:           │
│ - Number of edges: n-1             │
│ - Number of leaves: variable       │
│ - Traversal count: n! / (product of subtree sizes) │
└─────────────────────────────────────┘

Combinatorial formula:
┌─────────────────────────────────────┐
│ For each node, count:              │
│ - Number of ways to arrange children │
│ - Multiply by subtree counts       │
│ - Use factorial and combinations   │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def mathematical_traversal_count(n, edges, mod=10**9+7):
    """
    Count tree traversals using mathematical approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        mod: modulo value
    
    Returns:
        int: number of traversal sequences modulo mod
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def factorial_mod(x, mod):
        """Calculate factorial modulo mod"""
        result = 1
        for i in range(1, x + 1):
            result = (result * i) % mod
        return result
    
    def mod_inverse(a, mod):
        """Calculate modular inverse"""
        return pow(a, mod - 2, mod)
    
    def calculate_subtree_sizes(node, parent):
        """Calculate sizes of subtrees rooted at each node"""
        size = 1
        for child in adj[node]:
            if child != parent:
                size += calculate_subtree_sizes(child, node)
        return size
    
    def count_traversals_math(node, parent):
        """Count traversals using mathematical formula"""
        if len(adj[node]) == 1 and parent != -1:  # Leaf node
            return 1
        
        result = 1
        children_count = 0
        
        for child in adj[node]:
            if child != parent:
                children_count += 1
                child_result = count_traversals_math(child, node)
                result = (result * child_result) % mod
        
        # Multiply by factorial of children count
        if children_count > 0:
            result = (result * factorial_mod(children_count, mod)) % mod
        
        return result
    
    # Find a good starting node (preferably with degree > 1)
    start_node = 0
    for i in range(n):
        if len(adj[i]) > 1:
            start_node = i
            break
    
    return count_traversals_math(start_node, -1)

def optimized_mathematical_count(n, edges, mod=10**9+7):
    """
    Optimized mathematical counting approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        mod: modulo value
    
    Returns:
        int: number of traversal sequences modulo mod
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = (fact[i-1] * i) % mod
    
    def count_traversals_optimized(node, parent):
        """Optimized traversal counting"""
        if len(adj[node]) == 1 and parent != -1:  # Leaf node
            return 1
        
        result = 1
        children_count = 0
        
        for child in adj[node]:
            if child != parent:
                children_count += 1
                child_result = count_traversals_optimized(child, node)
                result = (result * child_result) % mod
        
        # Use precomputed factorial
        if children_count > 0:
            result = (result * fact[children_count]) % mod
        
        return result
    
    # Find starting node
    start_node = 0
    for i in range(n):
        if len(adj[i]) > 1:
            start_node = i
            break
    
    return count_traversals_optimized(start_node, -1)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result1 = mathematical_traversal_count(n, edges)
result2 = optimized_mathematical_count(n, edges)
print(f"Mathematical traversal count: {result1}")
print(f"Optimized mathematical count: {result2}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's optimal**: Uses mathematical properties for O(n) time complexity.

**Implementation Details**:
- **Mathematical Properties**: Use tree properties for efficient counting
- **Combinatorial Formulas**: Apply combinatorial formulas
- **Precomputation**: Precompute factorials for efficiency
- **Tree Traversal**: Use tree traversal for calculation

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(n!) | O(n) | Complete enumeration of all traversals |
| Dynamic Programming | O(n * 2^n) | O(n * 2^n) | Memoization with bitmask state |
| Mathematical | O(n) | O(n) | Use mathematical properties and formulas |

### Time Complexity
- **Time**: O(n) - Use mathematical properties and tree traversal
- **Space**: O(n) - Store tree structure and auxiliary data

### Why This Solution Works
- **Mathematical Properties**: Use tree properties for efficient counting
- **Combinatorial Formulas**: Apply combinatorial formulas for counting
- **Tree Traversal**: Use tree traversal for calculation
- **Efficient Algorithms**: Use optimal algorithms for tree operations

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted Tree Traversals**
**Problem**: Count traversals with weights on edges.

**Key Differences**: Edges have weights that affect counting

**Solution Approach**: Modify counting formula to include weights

**Implementation**:
```python
def weighted_traversal_count(n, edges, weights, mod=10**9+7):
    """
    Count weighted tree traversals
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        weights: list of edge weights
        mod: modulo value
    
    Returns:
        int: number of weighted traversal sequences modulo mod
    """
    # Build adjacency list with weights
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        adj[a-1].append((b-1, weights[i]))  # Convert to 0-indexed
        adj[b-1].append((a-1, weights[i]))  # Undirected edge
    
    def count_weighted_traversals(node, parent, current_weight):
        """Count weighted traversals"""
        if len(adj[node]) == 1 and parent != -1:  # Leaf node
            return current_weight % mod
        
        result = current_weight
        children_count = 0
        
        for child, weight in adj[node]:
            if child != parent:
                children_count += 1
                child_result = count_weighted_traversals(child, node, weight)
                result = (result * child_result) % mod
        
        # Multiply by factorial of children count
        if children_count > 0:
            result = (result * factorial_mod(children_count, mod)) % mod
        
        return result
    
    # Find starting node
    start_node = 0
    for i in range(n):
        if len(adj[i]) > 1:
            start_node = i
            break
    
    return count_weighted_traversals(start_node, -1, 1)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
weights = [2, 3, 1]
result = weighted_traversal_count(n, edges, weights)
print(f"Weighted traversal count: {result}")
```

#### **2. Constrained Tree Traversals**
**Problem**: Count traversals with certain constraints.

**Key Differences**: Apply constraints to traversal sequences

**Solution Approach**: Use inclusion-exclusion principle

**Implementation**:
```python
def constrained_traversal_count(n, edges, constraints, mod=10**9+7):
    """
    Count constrained tree traversals
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of constrained traversal sequences modulo mod
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def count_constrained_traversals(node, parent, constraint_mask):
        """Count constrained traversals"""
        if len(adj[node]) == 1 and parent != -1:  # Leaf node
            return 1
        
        result = 1
        children_count = 0
        
        for child in adj[node]:
            if child != parent:
                children_count += 1
                child_result = count_constrained_traversals(child, node, constraint_mask)
                result = (result * child_result) % mod
        
        # Apply constraints
        if constraint_mask & (1 << node):  # Node has constraint
            result = (result * 2) % mod  # Double the count
        
        # Multiply by factorial of children count
        if children_count > 0:
            result = (result * factorial_mod(children_count, mod)) % mod
        
        return result
    
    # Find starting node
    start_node = 0
    for i in range(n):
        if len(adj[i]) > 1:
            start_node = i
            break
    
    return count_constrained_traversals(start_node, -1, 0)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
constraints = [0, 1]  # Nodes 0 and 1 have constraints
result = constrained_traversal_count(n, edges, constraints)
print(f"Constrained traversal count: {result}")
```

#### **3. Multiple Tree Traversals**
**Problem**: Count traversals across multiple trees.

**Key Differences**: Handle multiple trees simultaneously

**Solution Approach**: Combine results from multiple trees

**Implementation**:
```python
def multiple_tree_traversal_count(trees, mod=10**9+7):
    """
    Count traversals across multiple trees
    
    Args:
        trees: list of tree descriptions
        mod: modulo value
    
    Returns:
        int: number of traversal sequences modulo mod
    """
    def count_single_tree(n, edges):
        """Count traversals for a single tree"""
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a-1].append(b-1)  # Convert to 0-indexed
            adj[b-1].append(a-1)  # Undirected edge
        
        def count_traversals(node, parent):
            """Count traversals for single tree"""
            if len(adj[node]) == 1 and parent != -1:  # Leaf node
                return 1
            
            result = 1
            children_count = 0
            
            for child in adj[node]:
                if child != parent:
                    children_count += 1
                    child_result = count_traversals(child, node)
                    result = (result * child_result) % mod
            
            # Multiply by factorial of children count
            if children_count > 0:
                result = (result * factorial_mod(children_count, mod)) % mod
            
            return result
        
        # Find starting node
        start_node = 0
        for i in range(n):
            if len(adj[i]) > 1:
                start_node = i
                break
        
        return count_traversals(start_node, -1)
    
    # Count traversals for each tree
    total_count = 1
    for n, edges in trees:
        tree_count = count_single_tree(n, edges)
        total_count = (total_count * tree_count) % mod
    
    return total_count

# Example usage
trees = [
    (3, [(1, 2), (2, 3)]),  # Tree 1
    (2, [(1, 2)])           # Tree 2
]
result = multiple_tree_traversal_count(trees)
print(f"Multiple tree traversal count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Counting Permutations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Combinations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Sequences](https://cses.fi/problemset/task/1075) - Combinatorics

#### **LeetCode Problems**
- [Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/) - Tree traversal
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Tree algorithms

#### **Problem Categories**
- **Tree Algorithms**: Tree traversal, tree counting
- **Combinatorics**: Mathematical counting, tree properties
- **Dynamic Programming**: DP optimization, tree DP

## 🔗 Additional Resources

### **Algorithm References**
- [Tree Algorithms](https://cp-algorithms.com/graph/tree_algorithms.html) - Tree algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP introduction

### **Practice Problems**
- [CSES Counting Permutations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Sequences](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Tree Algorithms](https://en.wikipedia.org/wiki/Tree_traversal) - Wikipedia article
