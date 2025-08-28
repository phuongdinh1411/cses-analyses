---
layout: simple
title: "Company Queries III"
permalink: /problem_soulutions/tree_algorithms/company_queries_iii_analysis
---


# Company Queries III

## Problem Statement
A company has n employees, numbered 1,2,…,n. Each employee except 1 has exactly one superior. Given q queries, for each query find the number of employees in the subtree of an employee.

### Input
The first input line has two integers n and q: the number of employees and queries.
The second line has n−1 integers p2,p3,…,pn: each pi is the superior of employee i.
Then, there are q lines describing the queries. Each line has one integer a: find the number of employees in the subtree of employee a.

### Output
Print q integers: the answers to the queries.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ pi < i
- 1 ≤ a ≤ n

### Example
```
Input:
5 3
1 1 2 2
1
2
3

Output:
5
3
1
```

## Solution Progression

### Approach 1: DFS for Each Query - O(q * n)
**Description**: For each query, perform DFS to count the number of employees in the subtree.

```python
def company_queries_dfs_each(n, q, superiors, queries):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    def count_subtree_size(node):
        count = 1  # Count the node itself
        for child in tree[node]:
            count += count_subtree_size(child)
        return count
    
    # Process queries
    result = []
    for a in queries:
        result.append(count_subtree_size(a))
    
    return result
```

**Why this is inefficient**: Multiple DFS traversals become slow for large numbers of queries.

### Improvement 1: Precompute Subtree Sizes - O(n + q)
**Description**: Precompute subtree sizes using a single DFS and answer queries in O(1).

```python
def company_queries_precompute(n, q, superiors, queries):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store subtree sizes
    subtree_sizes = [0] * (n + 1)
    
    def calculate_subtree_sizes(node):
        subtree_sizes[node] = 1  # Count the node itself
        for child in tree[node]:
            subtree_sizes[node] += calculate_subtree_sizes(child)
        return subtree_sizes[node]
    
    # Calculate all subtree sizes
    calculate_subtree_sizes(1)
    
    # Process queries
    result = []
    for a in queries:
        result.append(subtree_sizes[a])
    
    return result
```

**Why this improvement works**: Single DFS precomputes all subtree sizes, making queries O(1).

### Improvement 2: Iterative DFS - O(n + q)
**Description**: Use iterative DFS to avoid recursion stack issues for deep trees.

```python
def company_queries_iterative_dfs(n, q, superiors, queries):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store subtree sizes
    subtree_sizes = [0] * (n + 1)
    
    def calculate_subtree_sizes_iterative():
        # Use stack for iterative DFS
        stack = [(1, False)]
        
        while stack:
            node, processed = stack.pop()
            
            if processed:
                # Post-order processing
                subtree_sizes[node] = 1
                for child in tree[node]:
                    subtree_sizes[node] += subtree_sizes[child]
            else:
                # Push back with processed flag
                stack.append((node, True))
                # Push children in reverse order for correct processing
                for child in reversed(tree[node]):
                    stack.append((child, False))
    
    # Calculate all subtree sizes
    calculate_subtree_sizes_iterative()
    
    # Process queries
    result = []
    for a in queries:
        result.append(subtree_sizes[a])
    
    return result
```

**Why this improvement works**: Iterative DFS avoids recursion stack overflow for very deep trees.

### Alternative: BFS with Level Order - O(n + q)
**Description**: Use BFS with level order traversal for educational purposes.

```python
from collections import deque

def company_queries_bfs(n, q, superiors, queries):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store subtree sizes
    subtree_sizes = [0] * (n + 1)
    
    def calculate_subtree_sizes_bfs():
        # Calculate subtree sizes using BFS
        # We need to process nodes in reverse topological order
        # First, calculate in-degrees
        in_degree = [0] * (n + 1)
        for i in range(2, n + 1):
            superior = superiors[i - 2]
            in_degree[superior] += 1
        
        # Use queue for processing
        queue = deque()
        for i in range(1, n + 1):
            if in_degree[i] == 0:
                queue.append(i)
        
        while queue:
            node = queue.popleft()
            subtree_sizes[node] = 1  # Count the node itself
            # Add children's subtree sizes
            for child in tree[node]:
                subtree_sizes[node] += subtree_sizes[child]
            
            # Update in-degree of parent
            if node > 1:
                parent = superiors[node - 2]
                in_degree[parent] -= 1
                if in_degree[parent] == 0:
                    queue.append(parent)
    
    # Calculate all subtree sizes
    calculate_subtree_sizes_bfs()
    
    # Process queries
    result = []
    for a in queries:
        result.append(subtree_sizes[a])
    
    return result
```

**Why this works**: BFS approach processes nodes in topological order, ensuring parent nodes are processed after their children.

## Final Optimal Solution

```python
n, q = map(int, input().split())
superiors = list(map(int, input().split()))
queries = [int(input()) for _ in range(q)]

# Build adjacency list (tree)
tree = [[] for _ in range(n + 1)]
for i in range(2, n + 1):
    superior = superiors[i - 2]
    tree[superior].append(i)

# Array to store subtree sizes
subtree_sizes = [0] * (n + 1)

def calculate_subtree_sizes(node):
    subtree_sizes[node] = 1  # Count the node itself
    for child in tree[node]:
        subtree_sizes[node] += calculate_subtree_sizes(child)
    return subtree_sizes[node]

# Calculate all subtree sizes
calculate_subtree_sizes(1)

# Process queries
for a in queries:
    print(subtree_sizes[a])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS for Each Query | O(q * n) | O(n) | Simple but slow |
| Precompute Subtree Sizes | O(n + q) | O(n) | Single DFS preprocessing |
| Iterative DFS | O(n + q) | O(n) | Avoid recursion stack |
| BFS | O(n + q) | O(n) | Topological order processing |

## Key Insights for Other Problems

### 1. **Subtree Size Problems**
**Principle**: Precompute subtree sizes using post-order traversal for efficient queries.
**Applicable to**:
- Subtree size problems
- Tree algorithms
- Graph algorithms
- Algorithm design

**Example Problems**:
- Subtree size problems
- Tree algorithms
- Graph algorithms
- Algorithm design

### 2. **Post-order Traversal**
**Principle**: Use post-order traversal when you need to process children before parents.
**Applicable to**:
- Subtree calculations
- Tree algorithms
- Dynamic programming on trees
- Algorithm design

**Example Problems**:
- Subtree calculations
- Tree algorithms
- Dynamic programming on trees
- Algorithm design

### 3. **Preprocessing vs Query Trade-off**
**Principle**: Balance preprocessing time with query time based on problem constraints.
**Applicable to**:
- Algorithm design
- Problem solving
- Performance optimization
- System design

**Example Problems**:
- Algorithm design
- Problem solving
- Performance optimization
- System design

### 4. **Iterative vs Recursive DFS**
**Principle**: Choose between iterative and recursive DFS based on tree depth and stack limitations.
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

### 1. **Subtree Size Calculation Pattern**
```python
def calculate_subtree_sizes(tree, n):
    subtree_sizes = [0] * (n + 1)
    
    def dfs(node):
        subtree_sizes[node] = 1
        for child in tree[node]:
            subtree_sizes[node] += dfs(child)
        return subtree_sizes[node]
    
    dfs(1)
    return subtree_sizes
```

### 2. **Iterative DFS Pattern**
```python
def iterative_dfs_subtree_sizes(tree, n):
    subtree_sizes = [0] * (n + 1)
    stack = [(1, False)]
    
    while stack:
        node, processed = stack.pop()
        
        if processed:
            subtree_sizes[node] = 1
            for child in tree[node]:
                subtree_sizes[node] += subtree_sizes[child]
        else:
            stack.append((node, True))
            for child in reversed(tree[node]):
                stack.append((child, False))
    
    return subtree_sizes
```

### 3. **BFS Topological Pattern**
```python
def bfs_subtree_sizes(tree, superiors, n):
    subtree_sizes = [0] * (n + 1)
    in_degree = [0] * (n + 1)
    
    # Calculate in-degrees
    for i in range(2, n + 1):
        parent = superiors[i - 2]
        in_degree[parent] += 1
    
    # Process in topological order
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    while queue:
        node = queue.popleft()
        subtree_sizes[node] = 1
        
        for child in tree[node]:
            subtree_sizes[node] += subtree_sizes[child]
        
        if node > 1:
            parent = superiors[node - 2]
            in_degree[parent] -= 1
            if in_degree[parent] == 0:
                queue.append(parent)
    
    return subtree_sizes
```

## Edge Cases to Remember

1. **Root node**: Subtree of root contains all nodes
2. **Leaf nodes**: Subtree of leaf contains only the leaf itself
3. **Single child**: Nodes with only one child
4. **Deep trees**: Handle recursion stack properly
5. **Large queries**: Preprocess for efficiency

## Problem-Solving Framework

1. **Identify subtree nature**: This is a subtree size problem
2. **Choose approach**: Use post-order traversal for preprocessing
3. **Preprocess data**: Calculate all subtree sizes in one pass
4. **Handle queries**: Answer queries in O(1) using precomputed values
5. **Return result**: Return subtree sizes for all queries

---

*This analysis shows how to efficiently calculate subtree sizes using post-order traversal and preprocessing.* 