# CSES Tree Traversals - Problem Analysis

## Problem Statement
Given a tree with n nodes, find the preorder, inorder, and postorder traversals of the tree.

### Input
The first input line has one integer n: the number of nodes.
Then there are n-1 lines describing the tree edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print three lines: the preorder, inorder, and postorder traversals.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
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
```

## Solution Progression

### Approach 1: DFS Traversals - O(n)
**Description**: Use DFS to perform the three tree traversals.

```python
def tree_traversals_naive(n, edges):
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
        
        # Inorder: visit node between children (for binary trees)
        # For general trees, we can visit after all children
        inorder.append(node)
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    return preorder, inorder, postorder
```

**Why this is inefficient**: The inorder traversal for general trees is not well-defined, and we need to handle the tree structure properly.

### Improvement 1: Proper Tree Traversals - O(n)
**Description**: Implement proper tree traversals with correct handling of general trees.

```python
def tree_traversals_proper(n, edges):
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
```

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