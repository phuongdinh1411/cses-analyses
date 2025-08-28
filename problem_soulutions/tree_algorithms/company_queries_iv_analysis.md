---
layout: simple
title: "Company Queries IV
permalink: /problem_soulutions/tree_algorithms/company_queries_iv_analysis/"
---


# Company Queries IV

## Problem Statement
A company has n employees, numbered 1,2,…,n. Each employee except 1 has exactly one superior. Given q queries, for each query find the number of employees that are exactly k levels below an employee.

### Input
The first input line has two integers n and q: the number of employees and queries.
The second line has n−1 integers p2,p3,…,pn: each pi is the superior of employee i.
Then, there are q lines describing the queries. Each line has two integers a and k: find the number of employees exactly k levels below employee a.

### Output
Print q integers: the answers to the queries.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ pi < i
- 1 ≤ a ≤ n
- 0 ≤ k ≤ n

### Example
```
Input:
5 3
1 1 2 2
1 1
1 2
2 1

Output:
2
2
2
```

## Solution Progression

### Approach 1: BFS for Each Query - O(q * n)
**Description**: For each query, use BFS to find employees at exactly k levels below the given employee.

```python
from collections import deque

def company_queries_bfs_each(n, q, superiors, queries):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    def count_at_level(start, target_level):
        if target_level == 0:
            return 1 if start == 1 else 0
        
        # BFS to find nodes at target level
        queue = deque([(start, 0)])
        count = 0
        
        while queue:
            node, level = queue.popleft()
            
            if level == target_level:
                count += 1
                continue
            
            for child in tree[node]:
                queue.append((child, level + 1))
        
        return count
    
    # Process queries
    result = []
    for a, k in queries:
        result.append(count_at_level(a, k))
    
    return result
```

**Why this is inefficient**: Multiple BFS traversals become slow for large numbers of queries.

### Improvement 1: Precompute Levels - O(n + q)
**Description**: Precompute the level of each employee and count employees at each level for each node.

```python
def company_queries_precompute_levels(n, q, superiors, queries):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Arrays to store levels and level counts
    levels = [0] * (n + 1)
    level_counts = {}  # level_counts[node][level] = count
    
    def calculate_levels_and_counts(node, current_level):
        levels[node] = current_level
        
        # Initialize level counts for this node
        if node not in level_counts:
            level_counts[node] = {}
        
        # Count this node at its level
        level_counts[node][0] = 1
        
        for child in tree[node]:
            # Recursively calculate for children
            calculate_levels_and_counts(child, current_level + 1)
            
            # Merge level counts from children
            for child_level, child_count in level_counts[child].items():
                new_level = child_level + 1
                if new_level not in level_counts[node]:
                    level_counts[node][new_level] = 0
                level_counts[node][new_level] += child_count
    
    # Calculate levels and counts
    calculate_levels_and_counts(1, 0)
    
    # Process queries
    result = []
    for a, k in queries:
        if a in level_counts and k in level_counts[a]:
            result.append(level_counts[a][k])
        else:
            result.append(0)
    
    return result
```

**Why this improvement works**: Single DFS precomputes level information for all nodes, making queries O(1).

### Improvement 2: Optimized Level Counting - O(n + q)
**Description**: Optimize level counting with better data structures and memory usage.

```python
def company_queries_optimized_levels(n, q, superiors, queries):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store level counts for each node
    # level_counts[node][level] = number of employees at that level
    level_counts = [[0] * (n + 1) for _ in range(n + 1)]
    
    def calculate_level_counts(node):
        # Initialize: this node is at level 0
        level_counts[node][0] = 1
        
        for child in tree[node]:
            # Recursively calculate for children
            calculate_level_counts(child)
            
            # Merge level counts from children
            for level in range(n):
                if level_counts[child][level] > 0:
                    level_counts[node][level + 1] += level_counts[child][level]
    
    # Calculate level counts for all nodes
    calculate_level_counts(1)
    
    # Process queries
    result = []
    for a, k in queries:
        if k <= n:
            result.append(level_counts[a][k])
        else:
            result.append(0)
    
    return result
```

**Why this improvement works**: Optimized implementation with better memory usage and simpler data structures.

### Alternative: BFS with Level Tracking - O(n + q)
**Description**: Use BFS with level tracking for educational purposes.

```python
from collections import deque

def company_queries_bfs_levels(n, q, superiors, queries):
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store level counts
    level_counts = [[0] * (n + 1) for _ in range(n + 1)]
    
    def calculate_level_counts_bfs(start):
        # BFS to calculate level counts for start node
        queue = deque([(start, 0)])
        counts = [0] * (n + 1)
        counts[0] = 1  # Start node is at level 0
        
        while queue:
            node, level = queue.popleft()
            
            for child in tree[node]:
                new_level = level + 1
                counts[new_level] += 1
                queue.append((child, new_level))
        
        # Store counts for start node
        for level in range(n + 1):
            level_counts[start][level] = counts[level]
    
    # Calculate level counts for all nodes
    for node in range(1, n + 1):
        calculate_level_counts_bfs(node)
    
    # Process queries
    result = []
    for a, k in queries:
        if k <= n:
            result.append(level_counts[a][k])
        else:
            result.append(0)
    
    return result
```

**Why this works**: BFS approach processes nodes level by level, which can be useful for understanding.

## Final Optimal Solution

```python
n, q = map(int, input().split())
superiors = list(map(int, input().split()))
queries = [tuple(map(int, input().split())) for _ in range(q)]

# Build adjacency list (tree)
tree = [[] for _ in range(n + 1)]
for i in range(2, n + 1):
    superior = superiors[i - 2]
    tree[superior].append(i)

# Array to store level counts for each node
level_counts = [[0] * (n + 1) for _ in range(n + 1)]

def calculate_level_counts(node):
    # Initialize: this node is at level 0
    level_counts[node][0] = 1
    
    for child in tree[node]:
        # Recursively calculate for children
        calculate_level_counts(child)
        
        # Merge level counts from children
        for level in range(n):
            if level_counts[child][level] > 0:
                level_counts[node][level + 1] += level_counts[child][level]

# Calculate level counts for all nodes
calculate_level_counts(1)

# Process queries
for a, k in queries:
    if k <= n:
        print(level_counts[a][k])
    else:
        print(0)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| BFS for Each Query | O(q * n) | O(n) | Simple but slow |
| Precompute Levels | O(n + q) | O(n²) | Single DFS preprocessing |
| Optimized Levels | O(n + q) | O(n²) | Better implementation |
| BFS Levels | O(n² + q) | O(n²) | Level-by-level processing |

## Key Insights for Other Problems

### 1. **Level-based Query Problems**
**Principle**: Precompute level information using tree traversal for efficient level-based queries.
**Applicable to**:
- Level-based query problems
- Tree algorithms
- Graph algorithms
- Algorithm design

**Example Problems**:
- Level-based query problems
- Tree algorithms
- Graph algorithms
- Algorithm design

### 2. **Tree Level Calculations**
**Principle**: Use post-order traversal to calculate level information for all nodes efficiently.
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

### 3. **Level Count Merging**
**Principle**: Merge level counts from children to calculate level counts for parent nodes.
**Applicable to**:
- Tree algorithms
- Dynamic programming on trees
- Algorithm design
- Problem solving

**Example Problems**:
- Tree algorithms
- Dynamic programming on trees
- Algorithm design
- Problem solving

### 4. **Preprocessing for Level Queries**
**Principle**: Preprocess tree information to answer level-based queries efficiently.
**Applicable to**:
- Query optimization
- Algorithm design
- Problem solving
- System design

**Example Problems**:
- Query optimization
- Algorithm design
- Problem solving
- System design

## Notable Techniques

### 1. **Level Count Calculation Pattern**
```python
def calculate_level_counts(tree, n):
    level_counts = [[0] * (n + 1) for _ in range(n + 1)]
    
    def dfs(node):
        level_counts[node][0] = 1
        
        for child in tree[node]:
            dfs(child)
            
            for level in range(n):
                if level_counts[child][level] > 0:
                    level_counts[node][level + 1] += level_counts[child][level]
    
    dfs(1)
    return level_counts
```

### 2. **Level Count Merging Pattern**
```python
def merge_level_counts(parent_counts, child_counts, max_level):
    for level in range(max_level):
        if child_counts[level] > 0:
            parent_counts[level + 1] += child_counts[level]
```

### 3. **BFS Level Tracking Pattern**
```python
def bfs_level_tracking(tree, start, n):
    queue = deque([(start, 0)])
    counts = [0] * (n + 1)
    counts[0] = 1
    
    while queue:
        node, level = queue.popleft()
        
        for child in tree[node]:
            new_level = level + 1
            counts[new_level] += 1
            queue.append((child, new_level))
    
    return counts
```

## Edge Cases to Remember

1. **k = 0**: Count the node itself
2. **k > tree height**: Return 0 (no employees at that level)
3. **Leaf nodes**: No employees at levels > 0
4. **Root node**: All employees are at some level below root
5. **Large k values**: Handle efficiently with preprocessing

## Problem-Solving Framework

1. **Identify level nature**: This is a level-based query problem
2. **Choose approach**: Use post-order traversal for preprocessing
3. **Preprocess data**: Calculate level counts for all nodes
4. **Handle queries**: Answer queries in O(1) using precomputed values
5. **Return result**: Return level counts for all queries

---

*This analysis shows how to efficiently calculate level-based information in trees using post-order traversal and preprocessing.*"