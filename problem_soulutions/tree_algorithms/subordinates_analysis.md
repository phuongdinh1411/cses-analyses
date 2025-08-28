---
layout: simple
title: CSES Subordinates - Problem Analysis
permalink: /problem_soulutions/tree_algorithms/subordinates_analysis/
---

# CSES Subordinates - Problem Analysis

## Problem Statement
You are given a company hierarchy with a tree structure. The company has n employees, numbered 1,2,…,n. Each employee except 1 has exactly one superior. Your task is to find for each employee the number of subordinates.

### Input
The first input line has an integer n: the number of employees.
The second line has n−1 integers p2,p3,…,pn: each pi is the superior of employee i.

### Output
Print n integers: the number of subordinates for each employee.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ pi < i

### Example
```
Input:
5
1 1 2 2

Output:
4 2 0 0 0
```

## Solution Progression

### Approach 1: DFS with Recursion - O(n)
**Description**: Use depth-first search to count subordinates for each node recursively.

```python
def subordinates_dfs(n, superiors):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]  # Convert to 0-indexed
        tree[superior].append(i)
    
    def count_subordinates(node):
        count = 0
        for child in tree[node]:
            count += 1 + count_subordinates(child)
        return count
    
    # Calculate subordinates for each employee
    result = []
    for i in range(1, n + 1):
        result.append(count_subordinates(i))
    
    return result
```

**Why this is efficient**: DFS naturally traverses the tree structure and counts subordinates recursively.

### Improvement 1: DFS with Memoization - O(n)
**Description**: Use DFS with memoization to avoid recalculating the same subtrees.

```python
def subordinates_dfs_memoized(n, superiors):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Memoization cache
    memo = {}
    
    def count_subordinates(node):
        if node in memo:
            return memo[node]
        
        count = 0
        for child in tree[node]:
            count += 1 + count_subordinates(child)
        
        memo[node] = count
        return count
    
    # Calculate subordinates for each employee
    result = []
    for i in range(1, n + 1):
        result.append(count_subordinates(i))
    
    return result
```

**Why this improvement works**: Memoization prevents redundant calculations for overlapping subtrees.

### Improvement 2: Single DFS with Post-order Traversal - O(n)
**Description**: Use a single DFS with post-order traversal to calculate all counts efficiently.

```python
def subordinates_single_dfs(n, superiors):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store subordinate counts
    subordinates = [0] * (n + 1)
    
    def dfs(node):
        count = 0
        for child in tree[node]:
            count += 1 + dfs(child)
        subordinates[node] = count
        return count
    
    # Start DFS from root (employee 1)
    dfs(1)
    
    # Return results for all employees
    return subordinates[1:n + 1]
```

**Why this improvement works**: Single DFS is more efficient and uses less memory than multiple recursive calls.

### Alternative: BFS with Level Order - O(n)
**Description**: Use BFS with level order traversal for educational purposes.

```python
from collections import deque

def subordinates_bfs(n, superiors):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store subordinate counts
    subordinates = [0] * (n + 1)
    
    # BFS with level order traversal
    queue = deque([1])
    visited = [False] * (n + 1)
    visited[1] = True
    
    while queue:
        node = queue.popleft()
        
        for child in tree[node]:
            if not visited[child]:
                visited[child] = True
                queue.append(child)
                # Count this child and all its descendants
                subordinates[node] += 1 + count_descendants(child, tree)
    
    return subordinates[1:n + 1]

def count_descendants(node, tree):
    count = 0
    for child in tree[node]:
        count += 1 + count_descendants(child, tree)
    return count
```

**Why this works**: BFS approach can be useful for understanding level-based tree traversal.

## Final Optimal Solution

```python
n = int(input())
superiors = list(map(int, input().split()))

# Build adjacency list (tree)
tree = [[] for _ in range(n + 1)]
for i in range(2, n + 1):
    superior = superiors[i - 2]
    tree[superior].append(i)

# Array to store subordinate counts
subordinates = [0] * (n + 1)

def dfs(node):
    count = 0
    for child in tree[node]:
        count += 1 + dfs(child)
    subordinates[node] = count
    return count

# Start DFS from root (employee 1)
dfs(1)

# Print results for all employees
print(*subordinates[1:n + 1])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS with Recursion | O(n) | O(n) | Natural tree traversal |
| DFS with Memoization | O(n) | O(n) | Avoid redundant calculations |
| Single DFS | O(n) | O(n) | Most efficient approach |
| BFS | O(n) | O(n) | Level-based traversal |

## Key Insights for Other Problems

### 1. **Tree Traversal Patterns**
**Principle**: Use appropriate tree traversal patterns based on problem requirements.
**Applicable to**:
- Tree algorithms
- Graph algorithms
- Hierarchical data structures
- Algorithm design

**Example Problems**:
- Tree algorithms
- Graph algorithms
- Hierarchical data structures
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

### 3. **Memoization in Trees**
**Principle**: Use memoization to avoid recalculating subtree properties.
**Applicable to**:
- Tree algorithms
- Dynamic programming
- Algorithm optimization
- Performance improvement

**Example Problems**:
- Tree algorithms
- Dynamic programming
- Algorithm optimization
- Performance improvement

### 4. **Single Pass Algorithms**
**Principle**: Design algorithms that compute all required information in a single traversal.
**Applicable to**:
- Algorithm design
- Performance optimization
- Tree algorithms
- Graph algorithms

**Example Problems**:
- Algorithm design
- Performance optimization
- Tree algorithms
- Graph algorithms

## Notable Techniques

### 1. **DFS Post-order Pattern**
```python
def dfs_post_order(tree, node, result):
    count = 0
    for child in tree[node]:
        count += 1 + dfs_post_order(tree, child, result)
    result[node] = count
    return count
```

### 2. **Tree Building Pattern**
```python
def build_tree_from_parents(n, parents):
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        parent = parents[i - 2]
        tree[parent].append(i)
    return tree
```

### 3. **Subtree Counting Pattern**
```python
def count_subtree_sizes(tree, n):
    sizes = [0] * (n + 1)
    
    def dfs(node):
        size = 1
        for child in tree[node]:
            size += dfs(child)
        sizes[node] = size
        return size
    
    dfs(1)
    return sizes
```

## Edge Cases to Remember

1. **Root node**: Employee 1 has no superior
2. **Leaf nodes**: Employees with no subordinates
3. **Single child**: Employees with exactly one subordinate
4. **Large trees**: Handle deep recursion properly
5. **Empty subtrees**: Handle nodes with no children

## Problem-Solving Framework

1. **Identify tree structure**: This is a tree with parent-child relationships
2. **Choose traversal**: Use post-order DFS for subtree calculations
3. **Handle recursion**: Ensure proper base cases and recursion
4. **Optimize performance**: Use single pass algorithm
5. **Format output**: Return counts for all nodes

---

*This analysis shows how to efficiently calculate subtree sizes using tree traversal algorithms.* 