---
layout: simple
title: "Tree Traversals"
permalink: /problem_soulutions/advanced_graph_problems/tree_traversals_analysis
---

# Tree Traversals

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the three fundamental tree traversal orders (preorder, inorder, postorder)
- Implement recursive and iterative tree traversal algorithms
- Apply tree traversal techniques to different tree structures
- Optimize tree traversal algorithms for large trees
- Handle special cases in tree traversal (empty trees, single nodes)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tree traversal, DFS, recursion, iterative algorithms
- **Data Structures**: Trees, adjacency lists, stacks, recursion stacks
- **Mathematical Concepts**: Graph theory, tree properties, traversal orders
- **Programming Skills**: Recursion, stack operations, tree representation
- **Related Problems**: Tree Diameter (tree algorithms), Subordinates (tree traversal), Tree Distances I (tree properties)

## 📋 Problem Description

Given a tree with n nodes, find the preorder, inorder, and postorder traversals of the tree.

**Input**: 
- n: number of nodes
- n-1 lines: a b (edge between nodes a and b)

**Output**: 
- Three lines containing preorder, inorder, and postorder traversals

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
1 2 3 4
4 3 2 1
4 3 2 1

Explanation**: 
Tree structure: 1 -- 2 -- 3 -- 4
Preorder: Visit root, then children (1, 2, 3, 4)
Inorder: Visit left subtree, root, right subtree (4, 3, 2, 1)
Postorder: Visit children, then root (4, 3, 2, 1)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Tree Traversal (Brute Force)

**Key Insights from Brute Force Approach**:
- **Recursive DFS**: Use recursive depth-first search
- **Traversal Order**: Implement three different traversal orders
- **Tree Structure**: Handle general tree structures
- **Exhaustive Search**: Visit all nodes in the tree

**Key Insight**: Use recursive DFS to perform all three tree traversals in a straightforward manner.

**Algorithm**:
- Build adjacency list representation of the tree
- Use recursive DFS for each traversal type
- Visit nodes in the correct order for each traversal
- Collect results in separate lists

**Visual Example**:
```
Tree: 1-2-3-4

Recursive DFS Traversal:
┌─────────────────────────────────────┐
│ Preorder: 1 → 2 → 3 → 4            │
│ (Visit root before children)        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Inorder: 4 → 3 → 2 → 1             │
│ (Visit children before root)        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Postorder: 4 → 3 → 2 → 1           │
│ (Visit children, then root)         │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_tree_traversals_solution(n, edges):
    """
    Find tree traversals using brute force recursive DFS
    
    Args:
        n: number of nodes
        edges: list of (a, b) representing edges
    
    Returns:
        tuple: (preorder, inorder, postorder) traversals
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    # DFS traversal
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Inorder: visit node after all children (for general trees)
        inorder.append(node)
        
        # Postorder: visit node after all children
        postorder.append(node)
    
    # Start DFS from node 1 (assuming it's the root)
    dfs(1, -1)
    
    return preorder, inorder, postorder

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
preorder, inorder, postorder = brute_force_tree_traversals_solution(n, edges)
print(f"Preorder: {preorder}")  # Output: [1, 2, 3, 4]
print(f"Inorder: {inorder}")    # Output: [4, 3, 2, 1]
print(f"Postorder: {postorder}")  # Output: [4, 3, 2, 1]
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's inefficient**: While O(n) is optimal, this approach uses recursion which can cause stack overflow for very deep trees.

---

### Approach 2: Iterative Tree Traversal (Optimized)

**Key Insights from Iterative Approach**:
- **Stack-based DFS**: Use explicit stack instead of recursion
- **Traversal Order**: Implement three different traversal orders iteratively
- **Memory Control**: Avoid recursion stack overflow
- **Efficient Implementation**: Use iterative approach for better memory control

**Key Insight**: Use iterative DFS with explicit stack to avoid recursion stack overflow.

**Algorithm**:
- Build adjacency list representation of the tree
- Use iterative DFS with explicit stack
- Implement three different traversal orders
- Collect results in separate lists

**Visual Example**:
```
Tree: 1-2-3-4

Iterative DFS Traversal:
┌─────────────────────────────────────┐
│ Stack: [1]                         │
│ Preorder: [1]                      │
│ Stack: [2]                         │
│ Preorder: [1, 2]                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Stack: [3]                         │
│ Preorder: [1, 2, 3]                │
│ Stack: [4]                         │
│ Preorder: [1, 2, 3, 4]            │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def iterative_tree_traversals_solution(n, edges):
    """
    Find tree traversals using iterative DFS with stack
    
    Args:
        n: number of nodes
        edges: list of (a, b) representing edges
    
    Returns:
        tuple: (preorder, inorder, postorder) traversals
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    # Iterative DFS traversal
    def iterative_dfs(start):
        stack = [(start, -1, False)]  # (node, parent, visited)
        
        while stack:
            node, parent, visited = stack.pop()
            
            if not visited:
                # Preorder: visit node before children
                preorder.append(node)
                
                # Push back with visited=True
                stack.append((node, parent, True))
                
                # Push children in reverse order
                for child in reversed(adj[node]):
                    if child != parent:
                        stack.append((child, node, False))
            else:
                # Inorder: visit node after all children
                inorder.append(node)
                
                # Postorder: visit node after all children
                postorder.append(node)
    
    # Start iterative DFS from node 1
    iterative_dfs(1)
    
    return preorder, inorder, postorder

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
preorder, inorder, postorder = iterative_tree_traversals_solution(n, edges)
print(f"Preorder: {preorder}")  # Output: [1, 2, 3, 4]
print(f"Inorder: {inorder}")    # Output: [4, 3, 2, 1]
print(f"Postorder: {postorder}")  # Output: [4, 3, 2, 1]
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Avoids recursion stack overflow and provides better memory control.

**Implementation Considerations**:
- **Explicit Stack**: Use explicit stack instead of recursion
- **Visited Flag**: Use visited flag to handle preorder and postorder
- **Child Order**: Push children in reverse order for correct traversal
- **Memory Control**: Better memory control than recursion

---

### Approach 3: Optimal Tree Traversal (Optimal)

**Key Insights from Optimal Approach**:
- **Single Pass**: Perform all three traversals in a single pass
- **Efficient Implementation**: Use optimal data structures
- **Memory Optimization**: Minimize memory usage
- **Optimal Algorithm**: Use the most efficient tree traversal

**Key Insight**: Use a single DFS pass to perform all three traversals efficiently.

**Algorithm**:
- Build adjacency list representation of the tree
- Use single DFS pass for all traversals
- Optimize data structure operations
- Collect results efficiently

**Visual Example**:
```
Tree: 1-2-3-4

Optimal Single Pass:
┌─────────────────────────────────────┐
│ DFS: 1 → 2 → 3 → 4                │
│ Preorder: [1, 2, 3, 4]            │
│ Inorder: [4, 3, 2, 1]             │
│ Postorder: [4, 3, 2, 1]           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def optimal_tree_traversals_solution(n, edges):
    """
    Find tree traversals using optimal single-pass approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) representing edges
    
    Returns:
        tuple: (preorder, inorder, postorder) traversals
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    # Optimal single-pass DFS
    def optimal_dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                optimal_dfs(child, node)
        
        # Inorder: visit node after all children
        inorder.append(node)
        
        # Postorder: visit node after all children
        postorder.append(node)
    
    # Start optimal DFS from node 1
    optimal_dfs(1, -1)
    
    return preorder, inorder, postorder

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
preorder, inorder, postorder = optimal_tree_traversals_solution(n, edges)
print(f"Preorder: {preorder}")  # Output: [1, 2, 3, 4]
print(f"Inorder: {inorder}")    # Output: [4, 3, 2, 1]
print(f"Postorder: {postorder}")  # Output: [4, 3, 2, 1]

# Test with different example
n = 5
edges = [(1, 2), (1, 3), (2, 4), (2, 5)]
preorder, inorder, postorder = optimal_tree_traversals_solution(n, edges)
print(f"Preorder: {preorder}")  # Output: [1, 2, 4, 5, 3]
print(f"Inorder: {inorder}")    # Output: [4, 5, 2, 3, 1]
print(f"Postorder: {postorder}")  # Output: [4, 5, 2, 3, 1]
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's optimal**: This approach provides the most efficient solution with O(n) time complexity and optimal memory usage.

**Implementation Details**:
- **Single Pass**: Perform all traversals in one DFS pass
- **Optimal Memory**: Minimize memory usage
- **Efficient Implementation**: Use optimal data structures
- **Optimal Result**: Guarantees efficient tree traversal
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    return preorder, inorder, postorder
```

**Why this works:**
- Uses DFS for tree traversal
- Handles general tree structures
- Simple and efficient implementation
- O(n) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_tree_traversals():
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
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    # DFS traversal
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Inorder: visit node after all children (for general trees)
        inorder.append(node)
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    # Print results
    print(*preorder)
    print(*inorder)
    print(*postorder)

# Main execution
if __name__ == "__main__":
    solve_tree_traversals()
```

**Why this works:**
- Optimal DFS-based approach
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
        (5, [(1, 2), (1, 3), (2, 4), (2, 5)]),
    ]
    
    for n, edges in test_cases:
        preorder, inorder, postorder = solve_test(n, edges)
        print(f"n={n}, edges={edges}")
        print(f"Preorder: {preorder}")
        print(f"Inorder: {inorder}")
        print(f"Postorder: {postorder}")
        print()

def solve_test(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    # DFS traversal
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Inorder: visit node after all children (for general trees)
        inorder.append(node)
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    return preorder, inorder, postorder

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - DFS traversal of the tree
- **Space**: O(n) - adjacency list and recursion stack

### Why This Solution Works
- **DFS Traversal**: Efficient tree traversal algorithm
- **Parent Tracking**: Avoids revisiting parent nodes
- **Traversal Order**: Correctly implements all three orders
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Tree Traversals**
- Different ways to visit tree nodes
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **DFS Algorithm**
- Efficient tree traversal
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Traversal Order**
- Preorder: Root → Left → Right
- Inorder: Left → Root → Right
- Postorder: Left → Right → Root
- Important for understanding

## 🎯 Problem Variations

### Variation 1: Tree Traversals with Weights
**Problem**: Each node has a weight, find weighted traversals.

```python
def weighted_tree_traversals(n, edges, weights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    # DFS traversal with weights
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append((node, weights[node]))
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Inorder: visit node after all children
        inorder.append((node, weights[node]))
        
        # Postorder: visit node after children
        postorder.append((node, weights[node]))
    
    # Start from root
    dfs(1, -1)
    
    return preorder, inorder, postorder
```

### Variation 2: Tree Traversals with Constraints
**Problem**: Perform traversals avoiding certain nodes.

```python
def constrained_tree_traversals(n, edges, forbidden_nodes):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    # DFS traversal with constraints
    def dfs(node, parent):
        if node in forbidden_nodes:
            return
        
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent and child not in forbidden_nodes:
                dfs(child, node)
        
        # Inorder: visit node after all children
        inorder.append(node)
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # Start from root
    dfs(1, -1)
    
    return preorder, inorder, postorder
```

### Variation 3: Dynamic Tree Traversals
**Problem**: Support adding/removing edges and maintaining traversals.

```python
class DynamicTreeTraversals:
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
    
    def get_traversals(self):
        # Initialize traversal lists
        preorder = []
        inorder = []
        postorder = []
        
        # DFS traversal
        def dfs(node, parent):
            # Preorder: visit node before children
            preorder.append(node)
            
            # Visit children
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
            
            # Inorder: visit node after all children
            inorder.append(node)
            
            # Postorder: visit node after children
            postorder.append(node)
        
        # Start from root
        dfs(1, -1)
        
        return preorder, inorder, postorder
```

### Variation 4: Tree Traversals with Multiple Constraints
**Problem**: Perform traversals satisfying multiple constraints.

```python
def multi_constrained_tree_traversals(n, edges, constraints):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    forbidden_nodes = constraints.get('forbidden_nodes', set())
    allowed_nodes = constraints.get('allowed_nodes', set(range(1, n + 1)))
    
    for a, b in edges:
        if a in allowed_nodes and b in allowed_nodes:
            adj[a].append(b)
            adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    # DFS traversal with multiple constraints
    def dfs(node, parent):
        if node in forbidden_nodes:
            return
        
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent and child not in forbidden_nodes:
                dfs(child, node)
        
        # Inorder: visit node after all children
        inorder.append(node)
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # Start from root
    dfs(1, -1)
    
    return preorder, inorder, postorder
```

### Variation 5: Tree Traversals with Level Order
**Problem**: Also perform level-order (BFS) traversal.

```python
def level_order_tree_traversals(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    level_order = []
    
    # DFS traversal
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Inorder: visit node after all children
        inorder.append(node)
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # BFS for level order
    def bfs():
        from collections import deque
        queue = deque([(1, -1, 0)])  # (node, parent, level)
        visited = {1}
        
        while queue:
            node, parent, level = queue.popleft()
            level_order.append((node, level))
            
            for child in adj[node]:
                if child != parent and child not in visited:
                    visited.add(child)
                    queue.append((child, node, level + 1))
    
    # Start traversals
    dfs(1, -1)
    bfs()
    
    return preorder, inorder, postorder, level_order
```

## 🔗 Related Problems

- **[Tree Algorithms](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Tree algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[DFS/BFS](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Depth-first and breadth-first search

## 📚 Learning Points

1. **Tree Traversals**: Essential for tree processing
2. **DFS Algorithm**: Efficient tree traversal
3. **Traversal Order**: Important algorithmic concept
4. **Tree Properties**: Important tree theory concept

---

**This is a great introduction to tree traversals and tree algorithms!** 🎯python
def solve_tree_traversals():
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
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Inorder: visit node after all children (for general trees)
        inorder.append(node)
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    # Print results
    print(*preorder)
    print(*inorder)
    print(*postorder)

# Main execution
if __name__ == "__main__":
    solve_tree_traversals()
```

**Why this works:**
- Optimal tree traversal approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4)], ([1, 2, 3, 4], [4, 3, 2, 1], [4, 3, 2, 1])),
        (3, [(1, 2), (2, 3)], ([1, 2, 3], [3, 2, 1], [3, 2, 1])),
        (5, [(1, 2), (1, 3), (2, 4), (2, 5)], ([1, 2, 4, 5, 3], [4, 5, 2, 3, 1], [4, 5, 2, 3, 1])),
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
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Inorder: visit node after all children (for general trees)
        inorder.append(node)
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    return preorder, inorder, postorder

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single DFS traversal
- **Space**: O(n) - adjacency list and traversal lists

### Why This Solution Works
- **DFS Traversal**: Efficient tree exploration
- **Three Orders**: Preorder, inorder, postorder
- **General Trees**: Handles arbitrary tree structures
- **Optimal Approach**: Single pass through the tree

## 🎯 Key Insights

### 1. **Tree Traversal Orders**
- Preorder: Root → Left → Right
- Inorder: Left → Root → Right (for binary trees)
- Postorder: Left → Right → Root
- Key insight for understanding

### 2. **DFS Implementation**
- Single DFS pass for all three traversals
- Efficient and elegant solution
- Important for performance
- Essential for understanding

### 3. **General Tree Handling**
- Extends binary tree concepts to general trees
- Inorder for general trees: visit after all children
- Simple but important observation
- Essential for correctness

## 🎯 Problem Variations

### Variation 1: Binary Tree Traversals
**Problem**: Handle binary trees with left/right children.

```python
def binary_tree_traversals(n, edges):
    # Build binary tree structure
    left_child = [0] * (n + 1)
    right_child = [0] * (n + 1)
    
    for a, b in edges:
        if left_child[a] == 0:
            left_child[a] = b
        else:
            right_child[a] = b
    
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node):
        if node == 0:
            return
        
        # Preorder: Root → Left → Right
        preorder.append(node)
        dfs(left_child[node])
        dfs(right_child[node])
        
        # Inorder: Left → Root → Right
        inorder.append(node)
        
        # Postorder: Left → Right → Root
        postorder.append(node)
    
    dfs(1)
    return preorder, inorder, postorder
```

### Variation 2: Iterative Traversals
**Problem**: Implement traversals without recursion.

```python
def iterative_tree_traversals(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Iterative preorder
    def iterative_preorder():
        stack = [(1, -1, False)]
        preorder = []
        
        while stack:
            node, parent, processed = stack.pop()
            
            if not processed:
                preorder.append(node)
                stack.append((node, parent, True))
                
                # Add children in reverse order
                for child in reversed(adj[node]):
                    if child != parent:
                        stack.append((child, node, False))
        
        return preorder
    
    # Iterative postorder
    def iterative_postorder():
        stack = [(1, -1, False)]
        postorder = []
        
        while stack:
            node, parent, processed = stack.pop()
            
            if processed:
                postorder.append(node)
            else:
                stack.append((node, parent, True))
                
                # Add children in reverse order
                for child in reversed(adj[node]):
                    if child != parent:
                        stack.append((child, node, False))
        
        return postorder
    
    return iterative_preorder(), iterative_postorder()
```

### Variation 3: Level Order Traversal
**Problem**: Add level order (breadth-first) traversal.

```python
def level_order_traversal(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Level order traversal
    from collections import deque
    queue = deque([(1, -1)])
    level_order = []
    
    while queue:
        node, parent = queue.popleft()
        level_order.append(node)
        
        for child in adj[node]:
            if child != parent:
                queue.append((child, node))
    
    return level_order
```

### Variation 4: Traversal with Node Values
**Problem**: Each node has a value, traverse and collect values.

```python
def tree_traversals_with_values(n, edges, values):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    preorder_values = []
    inorder_values = []
    postorder_values = []
    
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder_values.append(values[node])
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Inorder: visit node after all children
        inorder_values.append(values[node])
        
        # Postorder: visit node after children
        postorder_values.append(values[node])
    
    dfs(1, -1)
    return preorder_values, inorder_values, postorder_values
```

### Variation 5: Traversal Paths
**Problem**: Find the path from root to each node in each traversal.

```python
def tree_traversal_paths(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    preorder_paths = {}
    inorder_paths = {}
    postorder_paths = {}
    
    def dfs(node, parent, path):
        # Preorder path
        preorder_paths[node] = path + [node]
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node, path + [node])
        
        # Inorder path
        inorder_paths[node] = path + [node]
        
        # Postorder path
        postorder_paths[node] = path + [node]
    
    dfs(1, -1, [])
    return preorder_paths, inorder_paths, postorder_paths
```

## 🔗 Related Problems

- **[Tree Algorithms](/cses-analyses/problem_soulutions/tree_algorithms/)**: Tree problems
- **[Graph Traversal](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms
- **[Binary Tree Problems](/cses-analyses/problem_soulutions/tree_algorithms/)**: Binary tree algorithms

## 📚 Learning Points

1. **Tree Traversals**: Essential for tree algorithms
2. **DFS Implementation**: Efficient tree exploration
3. **Traversal Orders**: Understanding different visit patterns
4. **General Trees**: Extending binary tree concepts

**Why this improvement works**: Properly handles general trees by defining inorder traversal as visiting the node after the first half of children.

## Final Optimal Solution

```python
n = int(input())
edges = []
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_tree_traversals(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Get children (excluding parent)
        children = [child for child in adj[node] if child != parent]
        
        # For inorder in general trees, visit node after first half of children
        if children:
            # Visit first half of children
            for i in range(len(children) // 2):
                dfs(children[i], node)
            
            # Visit node (inorder)
            inorder.append(node)
            
            # Visit second half of children
            for i in range(len(children) // 2, len(children)):
                dfs(children[i], node)
        else:
            # Leaf node
            inorder.append(node)
        
        # Postorder: visit node after all children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    return preorder, inorder, postorder

preorder, inorder, postorder = find_tree_traversals(n, edges)
print(*preorder)
print(*inorder)
print(*postorder)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS Traversals | O(n) | O(n) | Simple tree traversal |
| Proper Traversals | O(n) | O(n) | Correct handling of general trees |

## Key Insights for Other Problems

### 1. **Tree Traversal Properties**
**Principle**: Different traversal orders provide different views of the tree structure.
**Applicable to**: Tree problems, traversal problems, tree reconstruction problems

### 2. **DFS for Tree Traversals**
**Principle**: Use DFS to implement different traversal orders by controlling when to visit nodes.
**Applicable to**: Tree traversal problems, graph traversal problems, tree problems

### 3. **General Tree Handling**
**Principle**: General trees (not binary) require special handling for inorder traversal.
**Applicable to**: Tree problems, traversal problems, tree structure problems

## Notable Techniques

### 1. **DFS Tree Traversal**
```python
def dfs_traversal(adj, root):
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node, parent):
        # Preorder
        preorder.append(node)
        
        children = [child for child in adj[node] if child != parent]
        
        if children:
            # Visit first half
            for i in range(len(children) // 2):
                dfs(children[i], node)
            
            # Inorder
            inorder.append(node)
            
            # Visit second half
            for i in range(len(children) // 2, len(children)):
                dfs(children[i], node)
        else:
            inorder.append(node)
        
        # Postorder
        postorder.append(node)
    
    dfs(root, -1)
    return preorder, inorder, postorder
```

### 2. **Binary Tree Traversal**
```python
def binary_tree_traversal(root):
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node):
        if not node:
            return
        
        # Preorder: node -> left -> right
        preorder.append(node.val)
        dfs(node.left)
        
        # Inorder: left -> node -> right
        inorder.append(node.val)
        dfs(node.right)
        
        # Postorder: left -> right -> node
        postorder.append(node.val)
    
    dfs(root)
    return preorder, inorder, postorder
```

### 3. **Iterative Traversals**
```python
def iterative_preorder(root):
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Push children in reverse order
        for child in reversed(node.children):
            stack.append(child)
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a tree traversal problem
2. **Choose approach**: Use DFS with proper traversal order control
3. **Initialize data structure**: Build adjacency list from edges
4. **Implement traversals**: Use DFS with different visit timings
5. **Handle general trees**: Define inorder for non-binary trees
6. **Process children**: Visit children in appropriate order
7. **Return result**: Output all three traversal sequences

---

*This analysis shows how to efficiently perform tree traversals using DFS with proper order control.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Tree Traversals with Costs**
**Variation**: Each edge has a cost, find minimum cost traversal paths.
**Approach**: Use weighted tree traversal with cost optimization.
```python
def cost_based_tree_traversals(n, edges, edge_costs):
    # Build weighted adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        cost = edge_costs.get((a, b), 1)
        adj[a].append((b, cost))
        adj[b].append((a, cost))
    
    # Initialize traversal lists and costs
    preorder = []
    inorder = []
    postorder = []
    preorder_cost = 0
    inorder_cost = 0
    postorder_cost = 0
    
    def dfs(node, parent, current_cost):
        nonlocal preorder_cost, inorder_cost, postorder_cost
        
        # Preorder: visit node before children
        preorder.append(node)
        preorder_cost += current_cost
        
        # Get children with costs
        children = [(child, cost) for child, cost in adj[node] if child != parent]
        
        if children:
            # Visit first half of children
            for i in range(len(children) // 2):
                child, cost = children[i]
                dfs(child, node, current_cost + cost)
            
            # Inorder: visit node between children
            inorder.append(node)
            inorder_cost += current_cost
            
            # Visit second half of children
            for i in range(len(children) // 2, len(children)):
                child, cost = children[i]
                dfs(child, node, current_cost + cost)
        else:
            inorder.append(node)
            inorder_cost += current_cost
        
        # Postorder: visit node after children
        postorder.append(node)
        postorder_cost += current_cost
    
    # Start from root
    dfs(1, -1, 0)
    
    return (preorder, inorder, postorder), (preorder_cost, inorder_cost, postorder_cost)
```

#### 2. **Tree Traversals with Constraints**
**Variation**: Limited budget, restricted paths, or specific traversal requirements.
**Approach**: Use constraint satisfaction with traversal optimization.
```python
def constrained_tree_traversals(n, edges, budget, restricted_edges):
    # Build adjacency list excluding restricted edges
    adj = [[] for _ in range(n + 1)]
    for a, b in edges: if (a, b) not in restricted_edges and (b, a) not in 
restricted_edges: adj[a].append(b)
            adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    current_cost = 0
    
    def dfs(node, parent):
        nonlocal current_cost
        
        if current_cost >= budget:
            return
        
        # Preorder
        preorder.append(node)
        current_cost += 1
        
        # Get available children
        children = [child for child in adj[node] if child != parent]
        
        if children and current_cost < budget:
            # Visit first half
            for i in range(len(children) // 2):
                if current_cost < budget:
                    dfs(children[i], node)
            
            # Inorder
            if current_cost < budget:
                inorder.append(node)
                current_cost += 1
            
            # Visit second half
            for i in range(len(children) // 2, len(children)):
                if current_cost < budget:
                    dfs(children[i], node)
        else:
            inorder.append(node)
            current_cost += 1
        
        # Postorder
        if current_cost < budget:
            postorder.append(node)
            current_cost += 1
    
    # Start from root
    dfs(1, -1)
    
    return preorder, inorder, postorder, current_cost
```

#### 3. **Tree Traversals with Probabilities**
**Variation**: Each node has a probability of being visited, find expected traversal.
**Approach**: Use probabilistic traversal or Monte Carlo simulation.
```python
def probabilistic_tree_traversals(n, edges, node_probabilities, num_samples=1000):
    import random
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
---

**This is a great introduction to tree traversals and DFS algorithms!** 🎯
    
    def dfs(node, parent):
        # Preorder
        preorder.append(node)
        
        children = [child for child in adj[node] if child != parent]
        
        if children:
            # Visit first half
            for i in range(len(children) // 2):
                dfs(children[i], node)
            
            # Inorder
            inorder.append(node)
            
            # Visit second half
            for i in range(len(children) // 2, len(children)):
                dfs(children[i], node)
        else:
            inorder.append(node)
        
        # Postorder
        postorder.append(node)
    
    # Start from root
    dfs(1, -1)
    
    # Calculate traversal attributes
    def get_traversal_attributes(traversal):
        return {
            'visit_count': len(traversal),
            'cost': len(traversal),  # Simplified cost
            'probability': 0.5  # Simplified probability
        }
    
    preorder_attrs = get_traversal_attributes(preorder)
    inorder_attrs = get_traversal_attributes(inorder)
    postorder_attrs = get_traversal_attributes(postorder)
    
    preorder_score = calculate_traversal_score(preorder_attrs)
    inorder_score = calculate_traversal_score(inorder_attrs)
    postorder_score = calculate_traversal_score(postorder_attrs)
    
    return (preorder, inorder, postorder), (preorder_score, inorder_score, postorder_score)
```

#### 5. **Tree Traversals with Dynamic Updates**
**Variation**: Tree structure can be modified dynamically.
**Approach**: Use dynamic tree algorithms or incremental updates.
```python
class DynamicTreeTraversals:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.traversal_cache = None
    
    def add_edge(self, a, b):
        self.adj[a].append(b)
        self.adj[b].append(a)
        self.invalidate_cache()
    
    def remove_edge(self, a, b):
        self.adj[a].remove(b)
        self.adj[b].remove(a)
        self.invalidate_cache()
    
    def invalidate_cache(self):
        self.traversal_cache = None
    
    def get_traversals(self):
        if self.traversal_cache is None:
            self.traversal_cache = self.compute_traversals()
        return self.traversal_cache
    
    def compute_traversals(self):
        preorder = []
        inorder = []
        postorder = []
        
        def dfs(node, parent):
            # Preorder
            preorder.append(node)
            
            children = [child for child in self.adj[node] if child != parent]
            
            if children:
                # Visit first half
                for i in range(len(children) // 2):
                    dfs(children[i], node)
                
                # Inorder
                inorder.append(node)
                
                # Visit second half
                for i in range(len(children) // 2, len(children)):
                    dfs(children[i], node)
            else:
                inorder.append(node)
            
            # Postorder
            postorder.append(node)
        
        # Start from root
        dfs(1, -1)
        
        return preorder, inorder, postorder
```

### Related Problems & Concepts

#### 1. **Tree Traversal Problems**
- **Preorder Traversal**: Visit node before children
- **Inorder Traversal**: Visit node between children
- **Postorder Traversal**: Visit node after children
- **Level Order Traversal**: Visit nodes level by level

#### 2. **Tree Structure Problems**
- **Tree Construction**: Build trees from traversals
- **Tree Reconstruction**: Reconstruct tree from traversal data
- **Tree Properties**: Tree height, diameter, size
- **Tree Operations**: Insert, delete, search operations

#### 3. **Graph Traversal Problems**
- **DFS**: Depth-first search on graphs
- **BFS**: Breadth-first search on graphs
- **Graph Traversal**: Traverse graph structures
- **Path Finding**: Find paths in graphs

#### 4. **Algorithm Problems**
- **Recursive Algorithms**: Recursive tree traversal
- **Iterative Algorithms**: Iterative tree traversal
- **Stack/Queue Usage**: Using data structures for traversal
- **Tree Algorithms**: Tree-specific algorithms

#### 5. **Data Structure Problems**
- **Tree Data Structures**: Binary trees, general trees
- **Graph Representations**: Adjacency list, adjacency matrix
- **Stack Operations**: Push, pop, peek operations
- **Queue Operations**: Enqueue, dequeue operations

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large trees
- **Edge Cases**: Robust tree operations

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient tree traversal
- **Sliding Window**: Optimal subtree problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Tree Theory**
- **Tree Properties**: Height, diameter, size, degree
- **Tree Types**: Binary trees, general trees, rooted trees
- **Tree Operations**: Insertion, deletion, searching
- **Tree Analysis**: Analyzing tree structure

#### 2. **Graph Theory**
- **Graph Traversal**: DFS, BFS, and variations
- **Graph Properties**: Connectivity, cycles, paths
- **Graph Algorithms**: Traversal algorithms
- **Graph Analysis**: Analyzing graph structure

#### 3. **Combinatorics**
- **Tree Counting**: Count different tree structures
- **Traversal Counting**: Count different traversal orders
- **Permutation Problems**: Ordering of tree nodes
- **Enumeration**: Listing all possible traversals

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Tree and graph problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Tree Problems**: Tree traversal, tree construction
- **Graph Problems**: Graph traversal, path finding
- **Algorithm Problems**: DFS, BFS, recursive algorithms
- **Data Structure Problems**: Trees, graphs, stacks, queues 