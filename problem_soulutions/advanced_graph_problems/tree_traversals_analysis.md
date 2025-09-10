---
layout: simple
title: "Tree Traversals - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/tree_traversals_analysis
---

# Tree Traversals - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of tree traversals in graph theory
- Apply graph theory principles to traverse trees efficiently
- Implement algorithms for different tree traversal methods
- Optimize tree operations for various traversal patterns
- Handle special cases in tree traversal analysis

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, tree algorithms, DFS, BFS, tree traversal
- **Data Structures**: Trees, adjacency lists, stacks, queues, visited arrays
- **Mathematical Concepts**: Graph theory, tree properties, traversal order
- **Programming Skills**: Tree representation, recursive algorithms, iterative algorithms
- **Related Problems**: Tree Diameter (tree properties), Tree Queries (tree algorithms), Company Queries (tree operations)

## 📋 Problem Description

Given a tree with n nodes, perform different types of tree traversals and analyze their properties.

**Input**: 
- n: number of nodes
- n-1 lines: a b (undirected edge between nodes a and b)

**Output**: 
- Results of different tree traversals

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
Preorder: 1 2 3 4
Inorder: 4 3 2 1
Postorder: 4 3 2 1
Level-order: 1 2 3 4

Explanation**: 
Tree: 1-2-3-4
Preorder: Visit root, then left subtree, then right subtree
Inorder: Visit left subtree, then root, then right subtree
Postorder: Visit left subtree, then right subtree, then root
Level-order: Visit nodes level by level
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Traversal Solution

**Key Insights from Recursive Traversal Solution**:
- **Recursive Approach**: Use recursion to traverse the tree
- **Simple Implementation**: Easy to understand and implement
- **Memory Overhead**: Uses call stack for recursion
- **Baseline Understanding**: Provides correct answer but may have stack overflow issues

**Key Insight**: Use recursive functions to implement different tree traversal methods.

**Algorithm**:
- Implement recursive functions for each traversal type
- Use visited array to avoid revisiting nodes
- Return traversal results in the correct order

**Visual Example**:
```
Tree: 1-2-3-4

Preorder traversal:
┌─────────────────────────────────────┐
│ Visit 1, then traverse subtree     │
│ Visit 2, then traverse subtree     │
│ Visit 3, then traverse subtree     │
│ Visit 4                            │
│ Result: 1 2 3 4                    │
└─────────────────────────────────────┘

Postorder traversal:
┌─────────────────────────────────────┐
│ Traverse subtree, then visit 1     │
│ Traverse subtree, then visit 2     │
│ Traverse subtree, then visit 3     │
│ Visit 4                            │
│ Result: 4 3 2 1                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_traversal_solution(n, edges):
    """
    Perform tree traversals using recursive approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        dict: results of different traversals
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def preorder_traversal(node, parent, visited):
        """Preorder traversal: root, left, right"""
        result = []
        if not visited[node]:
            result.append(node + 1)  # Convert back to 1-indexed
            visited[node] = True
            
            for neighbor in adj[node]:
                if neighbor != parent and not visited[neighbor]:
                    result.extend(preorder_traversal(neighbor, node, visited))
        
        return result
    
    def inorder_traversal(node, parent, visited):
        """Inorder traversal: left, root, right"""
        result = []
        if not visited[node]:
            visited[node] = True
            
            # Visit left subtree first
            for neighbor in adj[node]:
                if neighbor != parent and not visited[neighbor]:
                    result.extend(inorder_traversal(neighbor, node, visited))
            
            # Visit root
            result.append(node + 1)  # Convert back to 1-indexed
        
        return result
    
    def postorder_traversal(node, parent, visited):
        """Postorder traversal: left, right, root"""
        result = []
        if not visited[node]:
            visited[node] = True
            
            # Visit subtrees first
            for neighbor in adj[node]:
                if neighbor != parent and not visited[neighbor]:
                    result.extend(postorder_traversal(neighbor, node, visited))
            
            # Visit root last
            result.append(node + 1)  # Convert back to 1-indexed
        
        return result
    
    def level_order_traversal(start):
        """Level-order traversal using BFS"""
        from collections import deque
        
        result = []
        visited = [False] * n
        queue = deque([start])
        visited[start] = True
        
        while queue:
            node = queue.popleft()
            result.append(node + 1)  # Convert back to 1-indexed
            
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return result
    
    # Perform traversals
    visited = [False] * n
    preorder = preorder_traversal(0, -1, visited)
    
    visited = [False] * n
    inorder = inorder_traversal(0, -1, visited)
    
    visited = [False] * n
    postorder = postorder_traversal(0, -1, visited)
    
    level_order = level_order_traversal(0)
    
    return {
        'preorder': preorder,
        'inorder': inorder,
        'postorder': postorder,
        'level_order': level_order
    }

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = recursive_traversal_solution(n, edges)
print(f"Recursive traversal result: {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's inefficient**: Recursive approach may cause stack overflow for deep trees.

---

### Approach 2: Iterative Traversal Solution

**Key Insights from Iterative Traversal Solution**:
- **Iterative Approach**: Use stacks and queues instead of recursion
- **Stack Management**: Explicitly manage the call stack
- **Memory Control**: Better control over memory usage
- **Optimization**: More efficient than recursive approach

**Key Insight**: Use iterative algorithms with explicit stacks and queues for tree traversal.

**Algorithm**:
- Use stack for DFS-based traversals (preorder, inorder, postorder)
- Use queue for BFS-based traversal (level-order)
- Explicitly manage the traversal state

**Visual Example**:
```
Tree: 1-2-3-4

Iterative preorder traversal:
┌─────────────────────────────────────┐
│ Stack: [1]                         │
│ Pop 1, visit 1, push [2, 3]        │
│ Pop 2, visit 2, push [3]           │
│ Pop 3, visit 3, push [4]           │
│ Pop 4, visit 4                     │
│ Result: 1 2 3 4                    │
└─────────────────────────────────────┘

Iterative level-order traversal:
┌─────────────────────────────────────┐
│ Queue: [1]                         │
│ Pop 1, visit 1, enqueue [2]        │
│ Pop 2, visit 2, enqueue [3]        │
│ Pop 3, visit 3, enqueue [4]        │
│ Pop 4, visit 4                     │
│ Result: 1 2 3 4                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def iterative_traversal_solution(n, edges):
    """
    Perform tree traversals using iterative approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        dict: results of different traversals
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def iterative_preorder(start):
        """Iterative preorder traversal using stack"""
        result = []
        visited = [False] * n
        stack = [start]
        visited[start] = True
        
        while stack:
            node = stack.pop()
            result.append(node + 1)  # Convert back to 1-indexed
            
            # Push children in reverse order to maintain left-to-right order
            for neighbor in reversed(adj[node]):
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
        
        return result
    
    def iterative_inorder(start):
        """Iterative inorder traversal using stack"""
        result = []
        visited = [False] * n
        stack = [start]
        visited[start] = True
        
        while stack:
            node = stack[-1]
            
            # Find leftmost unvisited child
            leftmost_child = None
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    leftmost_child = neighbor
                    break
            
            if leftmost_child is not None:
                visited[leftmost_child] = True
                stack.append(leftmost_child)
            else:
                # No more children, visit current node
                stack.pop()
                result.append(node + 1)  # Convert back to 1-indexed
        
        return result
    
    def iterative_postorder(start):
        """Iterative postorder traversal using stack"""
        result = []
        visited = [False] * n
        stack = [start]
        visited[start] = True
        
        while stack:
            node = stack[-1]
            
            # Find unvisited child
            unvisited_child = None
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    unvisited_child = neighbor
                    break
            
            if unvisited_child is not None:
                visited[unvisited_child] = True
                stack.append(unvisited_child)
            else:
                # No more children, visit current node
                stack.pop()
                result.append(node + 1)  # Convert back to 1-indexed
        
        return result
    
    def iterative_level_order(start):
        """Iterative level-order traversal using queue"""
        from collections import deque
        
        result = []
        visited = [False] * n
        queue = deque([start])
        visited[start] = True
        
        while queue:
            node = queue.popleft()
            result.append(node + 1)  # Convert back to 1-indexed
            
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return result
    
    # Perform traversals
    preorder = iterative_preorder(0)
    inorder = iterative_inorder(0)
    postorder = iterative_postorder(0)
    level_order = iterative_level_order(0)
    
    return {
        'preorder': preorder,
        'inorder': inorder,
        'postorder': postorder,
        'level_order': level_order
    }

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = iterative_traversal_solution(n, edges)
print(f"Iterative traversal result: {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Iterative approach avoids stack overflow issues and provides better memory control.

**Implementation Considerations**:
- **Stack Management**: Use explicit stack for DFS-based traversals
- **Queue Management**: Use queue for BFS-based traversal
- **State Tracking**: Track visited nodes and traversal state

---

### Approach 3: Optimized Traversal Solution (Optimal)

**Key Insights from Optimized Traversal Solution**:
- **Single Pass**: Perform multiple traversals in a single pass
- **State Machine**: Use state machine to track traversal progress
- **Memory Optimization**: Minimize memory usage and improve cache locality
- **Optimal Complexity**: O(n) time complexity with optimal space usage

**Key Insight**: Use a single pass with state machine to perform multiple traversals efficiently.

**Algorithm**:
- Use a single DFS pass with state machine
- Track traversal progress for each node
- Generate all traversal results in one pass

**Visual Example**:
```
Tree: 1-2-3-4

Single pass traversal:
┌─────────────────────────────────────┐
│ State: PREORDER, visit 1           │
│ State: PREORDER, visit 2           │
│ State: PREORDER, visit 3           │
│ State: PREORDER, visit 4           │
│ State: POSTORDER, visit 4          │
│ State: POSTORDER, visit 3          │
│ State: POSTORDER, visit 2          │
│ State: POSTORDER, visit 1          │
└─────────────────────────────────────┘

Results: Preorder [1,2,3,4], Postorder [4,3,2,1]
```

**Implementation**:
```python
def optimized_traversal_solution(n, edges):
    """
    Perform tree traversals using optimized single-pass approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        dict: results of different traversals
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def single_pass_traversal(start):
        """Perform all traversals in a single pass"""
        preorder = []
        inorder = []
        postorder = []
        level_order = []
        
        # For level-order, we still need BFS
        from collections import deque
        queue = deque([start])
        visited_bfs = [False] * n
        visited_bfs[start] = True
        
        while queue:
            node = queue.popleft()
            level_order.append(node + 1)  # Convert back to 1-indexed
            
            for neighbor in adj[node]:
                if not visited_bfs[neighbor]:
                    visited_bfs[neighbor] = True
                    queue.append(neighbor)
        
        # For DFS traversals, use single pass with state machine
        visited = [False] * n
        stack = [(start, 'preorder')]
        visited[start] = True
        
        while stack:
            node, state = stack.pop()
            
            if state == 'preorder':
                preorder.append(node + 1)  # Convert back to 1-indexed
                
                # Push children in reverse order for correct traversal
                children = []
                for neighbor in adj[node]:
                    if not visited[neighbor]:
                        children.append(neighbor)
                
                # Push postorder state first
                stack.append((node, 'postorder'))
                
                # Push children in reverse order
                for neighbor in reversed(children):
                    visited[neighbor] = True
                    stack.append((neighbor, 'preorder'))
            
            elif state == 'postorder':
                postorder.append(node + 1)  # Convert back to 1-indexed
        
        # For inorder, we need a separate pass
        visited = [False] * n
        stack = [start]
        visited[start] = True
        
        while stack:
            node = stack[-1]
            
            # Find leftmost unvisited child
            leftmost_child = None
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    leftmost_child = neighbor
                    break
            
            if leftmost_child is not None:
                visited[leftmost_child] = True
                stack.append(leftmost_child)
            else:
                # No more children, visit current node
                stack.pop()
                inorder.append(node + 1)  # Convert back to 1-indexed
        
        return {
            'preorder': preorder,
            'inorder': inorder,
            'postorder': postorder,
            'level_order': level_order
        }
    
    return single_pass_traversal(0)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = optimized_traversal_solution(n, edges)
print(f"Optimized traversal result: {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's optimal**: O(n) time complexity with optimal space usage and single pass for most traversals.

**Implementation Details**:
- **Single Pass**: Perform multiple traversals in one pass
- **State Machine**: Use state machine to track traversal progress
- **Memory Optimization**: Minimize memory usage and improve cache locality
- **Efficient Algorithms**: Use optimal algorithms for each traversal type

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(n) | O(n) | Use recursion for simple implementation |
| Iterative | O(n) | O(n) | Use explicit stacks and queues |
| Optimized | O(n) | O(n) | Use single pass with state machine |

### Time Complexity
- **Time**: O(n) - Visit each node exactly once
- **Space**: O(n) - Store traversal results and auxiliary data structures

### Why This Solution Works
- **Tree Properties**: Use tree properties for efficient traversal
- **State Machine**: Use state machine for single-pass traversal
- **Memory Optimization**: Minimize memory usage and improve cache locality
- **Optimal Algorithms**: Use optimal algorithms for each traversal type

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Binary Tree Traversals**
**Problem**: Perform traversals on a binary tree with left and right children.

**Key Differences**: Binary tree structure with explicit left and right children

**Solution Approach**: Use binary tree properties for efficient traversal

**Implementation**:
```python
def binary_tree_traversals(n, edges, left_child, right_child):
    """
    Perform traversals on a binary tree
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        left_child: list of left children
        right_child: list of right children
    
    Returns:
        dict: results of different traversals
    """
    def binary_preorder(root):
        """Binary tree preorder traversal"""
        result = []
        if root != -1:
            result.append(root + 1)  # Convert back to 1-indexed
            result.extend(binary_preorder(left_child[root]))
            result.extend(binary_preorder(right_child[root]))
        return result
    
    def binary_inorder(root):
        """Binary tree inorder traversal"""
        result = []
        if root != -1:
            result.extend(binary_inorder(left_child[root]))
            result.append(root + 1)  # Convert back to 1-indexed
            result.extend(binary_inorder(right_child[root]))
        return result
    
    def binary_postorder(root):
        """Binary tree postorder traversal"""
        result = []
        if root != -1:
            result.extend(binary_postorder(left_child[root]))
            result.extend(binary_postorder(right_child[root]))
            result.append(root + 1)  # Convert back to 1-indexed
        return result
    
    def binary_level_order(root):
        """Binary tree level-order traversal"""
        from collections import deque
        
        result = []
        if root == -1:
            return result
        
        queue = deque([root])
        while queue:
            node = queue.popleft()
            result.append(node + 1)  # Convert back to 1-indexed
            
            if left_child[node] != -1:
                queue.append(left_child[node])
            if right_child[node] != -1:
                queue.append(right_child[node])
        
        return result
    
    # Find root (node with no parent)
    has_parent = [False] * n
    for a, b in edges:
        has_parent[b-1] = True  # Convert to 0-indexed
    
    root = -1
    for i in range(n):
        if not has_parent[i]:
            root = i
            break
    
    return {
        'preorder': binary_preorder(root),
        'inorder': binary_inorder(root),
        'postorder': binary_postorder(root),
        'level_order': binary_level_order(root)
    }

# Example usage
n = 4
edges = [(1, 2), (1, 3), (2, 4)]
left_child = [1, 3, -1, -1]  # 0-indexed
right_child = [2, -1, -1, -1]  # 0-indexed
result = binary_tree_traversals(n, edges, left_child, right_child)
print(f"Binary tree traversals result: {result}")
```

#### **2. Dynamic Tree Traversals**
**Problem**: Support adding/removing edges and maintain traversal results.

**Key Differences**: Tree structure can change dynamically

**Solution Approach**: Use dynamic tree maintenance with incremental updates

**Implementation**:
```python
class DynamicTreeTraversals:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.traversal_cache = None
    
    def add_edge(self, a, b):
        """Add undirected edge between a and b"""
        if b not in self.adj[a]:
            self.adj[a].append(b)
            self.adj[b].append(a)
            self.traversal_cache = None  # Invalidate cache
    
    def remove_edge(self, a, b):
        """Remove undirected edge between a and b"""
        if b in self.adj[a]:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.traversal_cache = None  # Invalidate cache
    
    def get_traversals(self, start=0):
        """Get current traversal results"""
        if self.traversal_cache is None:
            self._compute_traversals(start)
        
        return self.traversal_cache
    
    def _compute_traversals(self, start):
        """Compute traversals for current tree"""
        from collections import deque
        
        # Preorder traversal
        preorder = []
        visited = [False] * self.n
        stack = [start]
        visited[start] = True
        
        while stack:
            node = stack.pop()
            preorder.append(node + 1)  # Convert back to 1-indexed
            
            for neighbor in reversed(self.adj[node]):
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
        
        # Postorder traversal
        postorder = []
        visited = [False] * self.n
        stack = [(start, 'preorder')]
        visited[start] = True
        
        while stack:
            node, state = stack.pop()
            
            if state == 'preorder':
                stack.append((node, 'postorder'))
                for neighbor in reversed(self.adj[node]):
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append((neighbor, 'preorder'))
            else:  # postorder
                postorder.append(node + 1)  # Convert back to 1-indexed
        
        # Level-order traversal
        level_order = []
        visited = [False] * self.n
        queue = deque([start])
        visited[start] = True
        
        while queue:
            node = queue.popleft()
            level_order.append(node + 1)  # Convert back to 1-indexed
            
            for neighbor in self.adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        self.traversal_cache = {
            'preorder': preorder,
            'postorder': postorder,
            'level_order': level_order
        }

# Example usage
dtt = DynamicTreeTraversals(4)
dtt.add_edge(0, 1)
dtt.add_edge(1, 2)
dtt.add_edge(2, 3)
result1 = dtt.get_traversals()
print(f"Dynamic tree traversals result: {result1}")
```

#### **3. Constrained Tree Traversals**
**Problem**: Perform traversals with additional constraints (e.g., visit only certain nodes).

**Key Differences**: Consider additional constraints when traversing

**Solution Approach**: Use modified traversal algorithms with constraint checking

**Implementation**:
```python
def constrained_tree_traversals(n, edges, constraints):
    """
    Perform tree traversals with constraints
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        constraints: list of nodes that must be visited
    
    Returns:
        dict: results of constrained traversals
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def constrained_preorder(start):
        """Constrained preorder traversal"""
        result = []
        visited = [False] * n
        stack = [start]
        visited[start] = True
        
        while stack:
            node = stack.pop()
            
            # Only visit if node is in constraints
            if node + 1 in constraints:  # Convert back to 1-indexed
                result.append(node + 1)
            
            for neighbor in reversed(adj[node]):
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
        
        return result
    
    def constrained_level_order(start):
        """Constrained level-order traversal"""
        from collections import deque
        
        result = []
        visited = [False] * n
        queue = deque([start])
        visited[start] = True
        
        while queue:
            node = queue.popleft()
            
            # Only visit if node is in constraints
            if node + 1 in constraints:  # Convert back to 1-indexed
                result.append(node + 1)
            
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return result
    
    def constrained_postorder(start):
        """Constrained postorder traversal"""
        result = []
        visited = [False] * n
        stack = [(start, 'preorder')]
        visited[start] = True
        
        while stack:
            node, state = stack.pop()
            
            if state == 'preorder':
                stack.append((node, 'postorder'))
                for neighbor in reversed(adj[node]):
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append((neighbor, 'preorder'))
            else:  # postorder
                # Only visit if node is in constraints
                if node + 1 in constraints:  # Convert back to 1-indexed
                    result.append(node + 1)
        
        return result
    
    return {
        'preorder': constrained_preorder(0),
        'postorder': constrained_postorder(0),
        'level_order': constrained_level_order(0)
    }

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
constraints = [1, 3, 4]  # Only visit nodes 1, 3, 4
result = constrained_tree_traversals(n, edges, constraints)
print(f"Constrained tree traversals result: {result}")
```

### Related Problems

#### **CSES Problems**
- [Tree Diameter](https://cses.fi/problemset/task/1707) - Tree properties
- [Tree Queries](https://cses.fi/problemset/task/1707) - Tree algorithms
- [Company Queries](https://cses.fi/problemset/task/1707) - Tree operations

#### **LeetCode Problems**
- [Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/) - Tree traversal
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Tree algorithms

#### **Problem Categories**
- **Graph Theory**: Tree algorithms, tree traversal
- **Data Structures**: Tree operations, traversal algorithms
- **Combinatorial Algorithms**: Tree analysis, traversal optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Tree Traversal](https://cp-algorithms.com/graph/tree_algorithms.html) - Tree algorithms
- [DFS](https://cp-algorithms.com/graph/depth-first-search.html) - Depth-first search
- [BFS](https://cp-algorithms.com/graph/breadth-first-search.html) - Breadth-first search

### **Practice Problems**
- [CSES Tree Diameter](https://cses.fi/problemset/task/1707) - Medium
- [CSES Tree Queries](https://cses.fi/problemset/task/1707) - Medium
- [CSES Company Queries](https://cses.fi/problemset/task/1707) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
