---
layout: simple
title: "Company Queries I
permalink: /problem_soulutions/tree_algorithms/company_queries_i_analysis/"
---


# Company Queries I

## Problem Statement
A company has n employees, numbered 1,2,…,n. Each employee except 1 has exactly one superior. Given q queries, for each query find the k-th superior of an employee.

### Input
The first input line has two integers n and q: the number of employees and queries.
The second line has n−1 integers p2,p3,…,pn: each pi is the superior of employee i.
Then, there are q lines describing the queries. Each line has two integers a and k: find the k-th superior of employee a.

### Output
Print q integers: the answers to the queries. If there is no k-th superior, print -1.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ pi < i
- 1 ≤ a ≤ n
- 1 ≤ k ≤ n

### Example
```
Input:
5 3
1 1 2 2
2 1
2 2
5 1

Output:
1
-1
2
```

## Solution Progression

### Approach 1: Naive Climbing - O(q * k)
**Description**: For each query, climb up the tree k times to find the k-th superior.

```python
def company_queries_naive(n, q, superiors, queries):
    # Build parent array (1-indexed)
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    def find_kth_superior(employee, k):
        current = employee
        for _ in range(k):
            if current == 0:  # No more superiors
                return -1
            current = parent[current]
        return current
    
    # Process queries
    result = []
    for a, k in queries:
        result.append(find_kth_superior(a, k))
    
    return result
```

**Why this is inefficient**: For large k values, this approach becomes very slow.

### Improvement 1: Binary Lifting - O(n * log(n) + q * log(n))
**Description**: Use binary lifting to precompute ancestors at powers of 2 for efficient queries.

```python
def company_queries_binary_lifting(n, q, superiors, queries):
    # Build parent array (1-indexed)
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Binary lifting table: ancestor[node][level] = 2^level ancestor of node
    log_n = 20  # Sufficient for n up to 10^6
    ancestor = [[0] * log_n for _ in range(n + 1)]
    
    # Initialize: ancestor[node][0] = parent[node]
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Fill the binary lifting table
    for level in range(1, log_n):
        for node in range(1, n + 1):
            if ancestor[node][level - 1] != 0:
                ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
    
    def find_kth_superior(employee, k):
        current = employee
        level = 0
        
        while k > 0 and current != 0:
            if k & (1 << level):
                current = ancestor[current][level]
                if current == 0:
                    return -1
            level += 1
        
        return current if current != 0 else -1
    
    # Process queries
    result = []
    for a, k in queries:
        result.append(find_kth_superior(a, k))
    
    return result
```

**Why this improvement works**: Binary lifting allows us to jump up the tree in powers of 2, making queries logarithmic.

### Improvement 2: Optimized Binary Lifting - O(n * log(n) + q * log(n))
**Description**: Optimize binary lifting with better implementation and early termination.

```python
def company_queries_optimized_binary_lifting(n, q, superiors, queries):
    # Build parent array (1-indexed)
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Calculate log base 2 of n
    log_n = 0
    temp = n
    while temp > 0:
        log_n += 1
        temp >>= 1
    
    # Binary lifting table
    ancestor = [[0] * log_n for _ in range(n + 1)]
    
    # Initialize base case
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Fill the table using dynamic programming
    for level in range(1, log_n):
        for node in range(1, n + 1):
            if ancestor[node][level - 1] != 0:
                ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
    
    def find_kth_superior(employee, k):
        if k == 0:
            return employee
        
        current = employee
        level = 0
        
        while k > 0 and current != 0:
            if k & (1 << level):
                current = ancestor[current][level]
                if current == 0:
                    return -1
            level += 1
        
        return current if current != 0 else -1
    
    # Process queries
    result = []
    for a, k in queries:
        result.append(find_kth_superior(a, k))
    
    return result
```

**Why this improvement works**: Optimized implementation with better log calculation and early termination.

### Alternative: Heavy-Light Decomposition - O(n + q * log(n))
**Description**: Use heavy-light decomposition for educational purposes.

```python
def company_queries_heavy_light(n, q, superiors, queries):
    # Build parent array
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Calculate subtree sizes
    subtree_size = [1] * (n + 1)
    
    def calculate_subtree_sizes():
        # Calculate sizes using post-order traversal
        stack = [(1, False)]
        while stack:
            node, processed = stack.pop()
            if processed:
                for child in range(2, n + 1):
                    if parent[child] == node:
                        subtree_size[node] += subtree_size[child]
            else:
                stack.append((node, True))
                for child in range(2, n + 1):
                    if parent[child] == node:
                        stack.append((child, False))
    
    calculate_subtree_sizes()
    
    # Heavy-light decomposition
    heavy = [0] * (n + 1)
    
    def find_heavy_children():
        for node in range(1, n + 1):
            max_size = 0
            heavy_child = 0
            for child in range(2, n + 1):
                if parent[child] == node and subtree_size[child] > max_size:
                    max_size = subtree_size[child]
                    heavy_child = child
            heavy[node] = heavy_child
    
    find_heavy_children()
    
    def find_kth_superior(employee, k):
        current = employee
        remaining = k
        
        while remaining > 0 and current != 0:
            # Find the highest ancestor we can reach
            level = 0
            temp = current
            while temp != 0 and level < remaining:
                temp = parent[temp]
                level += 1
            
            if temp == 0:
                return -1
            
            current = temp
            remaining -= level
        
        return current if remaining == 0 else -1
    
    # Process queries
    result = []
    for a, k in queries:
        result.append(find_kth_superior(a, k))
    
    return result
```

**Why this works**: Heavy-light decomposition can be used for path queries, though binary lifting is more efficient for this problem.

## Final Optimal Solution

```python
n, q = map(int, input().split())
superiors = list(map(int, input().split()))
queries = [tuple(map(int, input().split())) for _ in range(q)]

# Build parent array (1-indexed)
parent = [0] * (n + 1)
for i in range(2, n + 1):
    parent[i] = superiors[i - 2]

# Calculate log base 2 of n
log_n = 0
temp = n
while temp > 0:
    log_n += 1
    temp >>= 1

# Binary lifting table
ancestor = [[0] * log_n for _ in range(n + 1)]

# Initialize base case
for i in range(1, n + 1):
    ancestor[i][0] = parent[i]

# Fill the table using dynamic programming
for level in range(1, log_n):
    for node in range(1, n + 1):
        if ancestor[node][level - 1] != 0:
            ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]

def find_kth_superior(employee, k):
    if k == 0:
        return employee
    
    current = employee
    level = 0
    
    while k > 0 and current != 0:
        if k & (1 << level):
            current = ancestor[current][level]
            if current == 0:
                return -1
        level += 1
    
    return current if current != 0 else -1

# Process queries
for a, k in queries:
    print(find_kth_superior(a, k))
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Climbing | O(q * k) | O(n) | Simple but slow |
| Binary Lifting | O(n * log(n) + q * log(n)) | O(n * log(n)) | Precompute ancestors |
| Optimized Binary Lifting | O(n * log(n) + q * log(n)) | O(n * log(n)) | Better implementation |
| Heavy-Light | O(n + q * log(n)) | O(n) | Alternative approach |

## Key Insights for Other Problems

### 1. **Ancestor Query Problems**
**Principle**: Use binary lifting to efficiently find k-th ancestors in trees.
**Applicable to**:
- Ancestor query problems
- Tree algorithms
- Graph algorithms
- Algorithm design

**Example Problems**:
- Ancestor query problems
- Tree algorithms
- Graph algorithms
- Algorithm design

### 2. **Binary Lifting Technique**
**Principle**: Precompute ancestors at powers of 2 for logarithmic query time.
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

### 3. **Sparse Table Applications**
**Principle**: Use sparse table techniques for range queries and ancestor finding.
**Applicable to**:
- Range queries
- Tree algorithms
- Algorithm design
- Problem solving

**Example Problems**:
- Range queries
- Tree algorithms
- Algorithm design
- Problem solving

### 4. **Preprocessing vs Query Trade-off**
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

## Notable Techniques

### 1. **Binary Lifting Pattern**
```python
def binary_lifting_setup(parent, n):
    log_n = 20  # Adjust based on n
    ancestor = [[0] * log_n for _ in range(n + 1)]
    
    # Initialize
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Fill table
    for level in range(1, log_n):
        for node in range(1, n + 1):
            if ancestor[node][level - 1] != 0:
                ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
    
    return ancestor

def find_kth_ancestor(ancestor, node, k):
    current = node
    level = 0
    
    while k > 0 and current != 0:
        if k & (1 << level):
            current = ancestor[current][level]
            if current == 0:
                return -1
        level += 1
    
    return current if current != 0 else -1
```

### 2. **Log Calculation Pattern**
```python
def calculate_log_n(n):
    log_n = 0
    temp = n
    while temp > 0:
        log_n += 1
        temp >>= 1
    return log_n
```

### 3. **Ancestor Query Pattern**
```python
def ancestor_query(ancestor, node, k):
    if k == 0:
        return node
    
    current = node
    level = 0
    
    while k > 0 and current != 0:
        if k & (1 << level):
            current = ancestor[current][level]
            if current == 0:
                return -1
        level += 1
    
    return current if current != 0 else -1
```

## Edge Cases to Remember

1. **k = 0**: Return the node itself
2. **k > depth**: Return -1 (no k-th ancestor)
3. **Root node**: Node 1 has no superiors
4. **Large k values**: Handle efficiently with binary lifting
5. **Multiple queries**: Preprocess for efficiency

## Problem-Solving Framework

1. **Identify ancestor nature**: This is an ancestor query problem
2. **Choose approach**: Use binary lifting for efficiency
3. **Preprocess data**: Build ancestor table
4. **Handle queries**: Use binary lifting for logarithmic time
5. **Return result**: Return k-th ancestor or -1

---

*This analysis shows how to efficiently find k-th ancestors in trees using binary lifting technique.*"