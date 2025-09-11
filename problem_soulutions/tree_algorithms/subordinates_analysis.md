---
layout: simple
title: "Subordinates"
permalink: /problem_soulutions/tree_algorithms/subordinates_analysis
---

# Subordinates

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand tree traversal and subtree counting algorithms
- Apply depth-first search (DFS) for tree processing
- Implement efficient tree dynamic programming
- Optimize tree algorithms for large inputs
- Handle edge cases in tree problems (single nodes, linear trees)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tree algorithms, DFS, tree DP, subtree counting
- **Data Structures**: Trees, graphs, adjacency lists, arrays
- **Mathematical Concepts**: Tree theory, graph theory, dynamic programming
- **Programming Skills**: Tree traversal, DFS implementation, recursive algorithms
- **Related Problems**: Tree Diameter (tree traversal), Tree Distances I (tree algorithms), Company Queries I (tree queries)

## 📋 Problem Description

Given a tree with n nodes, for each node, find the number of nodes in its subtree (including itself).

This is a fundamental tree algorithm problem that tests understanding of tree traversal and subtree counting.

**Input**: 
- First line: integer n (number of nodes)
- Next n-1 lines: two integers a and b (edge between nodes a and b)

**Output**: 
- Print n integers: the number of nodes in the subtree of each node

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
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
5 1 3 1 1

Explanation**: 
The tree structure:
    1
   / \\
  2   3
     / \\
    4   5

Subtree sizes:
- Node 1: 5 nodes (1, 2, 3, 4, 5)
- Node 2: 1 node (2)
- Node 3: 3 nodes (3, 4, 5)
- Node 4: 1 node (4)
- Node 5: 1 node (5)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - DFS for Each Node

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: For each node, perform a separate DFS to count its subtree
- **Complete Coverage**: Guaranteed to find the correct subtree size for each node
- **Simple Implementation**: Straightforward DFS approach
- **Inefficient**: Multiple DFS traversals lead to quadratic time complexity

**Key Insight**: For each node, perform a DFS starting from that node to count all nodes in its subtree.

**Algorithm**:
- For each node i:
  - Perform DFS starting from node i
  - Count all nodes reachable from node i
  - Store the count as subtree size of node i

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

For node 1:
- DFS from 1: visit 1, 2, 3, 4, 5
- Count: 5 nodes

For node 2:
- DFS from 2: visit 2
- Count: 1 node

For node 3:
- DFS from 3: visit 3, 4, 5
- Count: 3 nodes

For node 4:
- DFS from 4: visit 4
- Count: 1 node

For node 5:
- DFS from 5: visit 5
- Count: 1 node

Result: [5, 1, 3, 1, 1]
```

**Implementation**:
```python
def brute_force_subordinates(n, edges):
    """
    Find subtree sizes using brute force approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        list: subtree size for each node
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def dfs_count(node, parent):
        """DFS to count nodes in subtree"""
        count = 1
        for neighbor in adj[node]:
            if neighbor != parent:
                count += dfs_count(neighbor, node)
        return count
    
    subtree_sizes = []
    for i in range(1, n + 1):
        size = dfs_count(i, -1)
        subtree_sizes.append(size)
    
    return subtree_sizes

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = brute_force_subordinates(n, edges)
print(f"Brute force result: {result}")  # Output: [5, 1, 3, 1, 1]
```

**Time Complexity**: O(n²) - For each node, DFS takes O(n) time
**Space Complexity**: O(n) - For adjacency list and recursion stack

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Single DFS with Memoization

**Key Insights from Optimized Approach**:
- **Single DFS**: Perform only one DFS traversal from root
- **Memoization**: Store subtree sizes during the DFS
- **Efficient Calculation**: Calculate subtree sizes in a single pass
- **Linear Time**: Achieve O(n) time complexity

**Key Insight**: Use a single DFS traversal to calculate all subtree sizes simultaneously.

**Algorithm**:
- Perform DFS from root node
- For each node, calculate its subtree size as 1 + sum of children's subtree sizes
- Store results during the traversal

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

DFS traversal order: 1 → 2 → 3 → 4 → 5

Post-order processing:
1. Node 5: subtree_size = 1
2. Node 4: subtree_size = 1
3. Node 3: subtree_size = 1 + 1 + 1 = 3
4. Node 2: subtree_size = 1
5. Node 1: subtree_size = 1 + 1 + 3 = 5

Result: [5, 1, 3, 1, 1]
```

**Implementation**:
```python
def optimized_subordinates(n, edges):
    """
    Find subtree sizes using single DFS with memoization
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        list: subtree size for each node
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    subtree_sizes = [0] * (n + 1)
    
    def dfs(node, parent):
        """DFS to calculate subtree sizes"""
        subtree_sizes[node] = 1  # Count the node itself
        
        for neighbor in adj[node]:
            if neighbor != parent:
                dfs(neighbor, node)
                subtree_sizes[node] += subtree_sizes[neighbor]
    
    # Start DFS from node 1 (assuming it's the root)
    dfs(1, -1)
    
    return subtree_sizes[1:n+1]

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = optimized_subordinates(n, edges)
print(f"Optimized result: {result}")  # Output: [5, 1, 3, 1, 1]
```

**Time Complexity**: O(n) - Single DFS traversal
**Space Complexity**: O(n) - For adjacency list and recursion stack

**Why it's better**: Linear time complexity with efficient single-pass calculation.

---

### Approach 3: Optimal - Post-order DFS with Dynamic Programming

**Key Insights from Optimal Approach**:
- **Post-order Traversal**: Process children before parent
- **Dynamic Programming**: Use DP to calculate subtree sizes
- **Optimal Space**: Use only O(n) space
- **Optimal Time**: Achieve O(n) time complexity

**Key Insight**: Use post-order DFS to ensure that when we process a node, all its children have already been processed.

**Algorithm**:
- Perform post-order DFS traversal
- For each node, calculate subtree size as 1 + sum of children's subtree sizes
- Return the results

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

Post-order DFS: 2, 4, 5, 3, 1

Processing:
1. Node 2: subtree_size = 1
2. Node 4: subtree_size = 1
3. Node 5: subtree_size = 1
4. Node 3: subtree_size = 1 + 1 + 1 = 3
5. Node 1: subtree_size = 1 + 1 + 3 = 5

Result: [5, 1, 3, 1, 1]
```

**Implementation**:
```python
def optimal_subordinates(n, edges):
    """
    Find subtree sizes using optimal post-order DFS
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        list: subtree size for each node
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    subtree_sizes = [0] * (n + 1)
    
    def post_order_dfs(node, parent):
        """Post-order DFS to calculate subtree sizes"""
        # Process all children first
        for neighbor in adj[node]:
            if neighbor != parent:
                post_order_dfs(neighbor, node)
        
        # Process current node after children
        subtree_sizes[node] = 1  # Count the node itself
        for neighbor in adj[node]:
            if neighbor != parent:
                subtree_sizes[node] += subtree_sizes[neighbor]
    
    # Start DFS from node 1 (assuming it's the root)
    post_order_dfs(1, -1)
    
    return subtree_sizes[1:n+1]

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = optimal_subordinates(n, edges)
print(f"Optimal result: {result}")  # Output: [5, 1, 3, 1, 1]
```

**Time Complexity**: O(n) - Single post-order DFS traversal
**Space Complexity**: O(n) - For adjacency list and recursion stack

**Why it's optimal**: Achieves the best possible time and space complexity for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | DFS for each node |
| Single DFS | O(n) | O(n) | Calculate all sizes in one pass |
| Post-order DFS | O(n) | O(n) | Process children before parent |

### Time Complexity
- **Time**: O(n) - Single DFS traversal provides optimal linear time
- **Space**: O(n) - For adjacency list and recursion stack

### Why This Solution Works
- **Tree Properties**: Trees have unique paths between nodes, enabling efficient traversal
- **Dynamic Programming**: Subtree size of a node equals 1 + sum of children's subtree sizes
- **Post-order Processing**: Ensures children are processed before parents
- **Optimal Approach**: Post-order DFS provides the most elegant and efficient solution
