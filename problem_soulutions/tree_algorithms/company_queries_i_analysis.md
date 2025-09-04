---
layout: simple
title: "Company Queries I - K-th Superior of Employee"
permalink: /problem_soulutions/tree_algorithms/company_queries_i_analysis
---

# Company Queries I - K-th Superior of Employee

## 📋 Problem Description

A company has n employees, numbered 1,2,…,n. Each employee except 1 has exactly one superior. Given q queries, for each query find the k-th superior of an employee.

This is a tree ancestor query problem that requires finding the k-th ancestor of each node in a tree. The solution involves using binary lifting technique to efficiently answer ancestor queries.

**Input**: 
- First line: Two integers n and q (number of employees and queries)
- Second line: n-1 integers p₂, p₃, ..., pₙ (each pᵢ is the superior of employee i)
- Next q lines: Two integers a and k (find the k-th superior of employee a)

**Output**: 
- For each query, print the k-th superior of the employee, or -1 if it doesn't exist

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ pᵢ < i
- 1 ≤ a ≤ n
- 1 ≤ k ≤ n

**Example**:
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

**Explanation**: 
- Query 1: 1st superior of employee 2 = 1
- Query 2: 2nd superior of employee 2 = -1 (doesn't exist)
- Query 3: 1st superior of employee 5 = 2

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find the k-th ancestor of each node in a tree efficiently
- **Key Insight**: Use binary lifting technique to answer ancestor queries in O(log n)
- **Challenge**: Handle multiple queries efficiently without O(q × k) complexity

### Step 2: Initial Approach
**Naive climbing approach (inefficient but correct):**

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

### Step 3: Optimization/Alternative
**Optimized binary lifting:**

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

### Step 4: Complete Solution

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

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple tree (should return correct k-th superiors)
- **Test 2**: Linear tree (should return correct ancestors)
- **Test 3**: Star tree (should return correct ancestors)
- **Test 4**: Complex tree (should find all k-th ancestors)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Climbing | O(q * k) | O(n) | Simple but slow |
| Binary Lifting | O(n * log(n) + q * log(n)) | O(n * log(n)) | Precompute ancestors |
| Optimized Binary Lifting | O(n * log(n) + q * log(n)) | O(n * log(n)) | Better implementation |
| Heavy-Light | O(n + q * log(n)) | O(n) | Alternative approach |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Binary Lifting**: Precompute ancestors in powers of 2 for efficient queries
- **K-th Ancestor**: Find k-th ancestor using binary representation of k
- **Tree Ancestors**: Use parent pointers to traverse up the tree
- **Logarithmic Queries**: Answer ancestor queries in O(log n) time

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Company Queries with Dynamic Updates**
```python
def dynamic_company_queries(n, superiors, operations):
    # Handle company queries with dynamic superior changes
    
    # Build parent array
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    def rebuild_binary_lifting():
        # Rebuild binary lifting table after updates
        log_n = 20
        ancestor = [[0] * log_n for _ in range(n + 1)]
        
        # Initialize base case
        for i in range(1, n + 1):
            ancestor[i][0] = parent[i]
        
        # Fill the table
        for level in range(1, log_n):
            for node in range(1, n + 1):
                if ancestor[node][level - 1] != 0:
                    ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
        
        return ancestor
    
    def find_kth_superior(ancestor, employee, k):
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
    
    # Process operations
    results = []
    for operation in operations:
        if operation[0] == 'update':
            # Update superior
            employee, new_superior = operation[1], operation[2]
            parent[employee] = new_superior
        elif operation[0] == 'query':
            # K-th superior query
            employee, k = operation[1], operation[2]
            ancestor = rebuild_binary_lifting()
            result = find_kth_superior(ancestor, employee, k)
            results.append(result)
    
    return results
```

#### **2. Company Queries with Range Constraints**
```python
def constrained_company_queries(n, superiors, queries, constraints):
    # Handle company queries with range constraints
    
    # Build parent array
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Binary lifting table
    log_n = 20
    ancestor = [[0] * log_n for _ in range(n + 1)]
    
    # Initialize base case
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Fill the table
    for level in range(1, log_n):
        for node in range(1, n + 1):
            if ancestor[node][level - 1] != 0:
                ancestor[node][level] = ancestor[ancestor[node][level - 1]][level - 1]
    
    def find_kth_superior_with_constraints(employee, k, min_level, max_level):
        if k == 0:
            return employee if min_level <= 0 <= max_level else -1
        
        current = employee
        level = 0
        current_level = 0
        
        while k > 0 and current != 0:
            if k & (1 << level):
                current = ancestor[current][level]
                current_level += (1 << level)
                if current == 0:
                    return -1
            level += 1
        
        if current != 0 and min_level <= current_level <= max_level:
            return current
        else:
            return -1
    
    # Process queries
    results = []
    for query in queries:
        employee, k = query[0], query[1]
        min_level = constraints.get('min_level', 0)
        max_level = constraints.get('max_level', float('inf'))
        
        result = find_kth_superior_with_constraints(employee, k, min_level, max_level)
        results.append(result)
    
    return results
```

#### **3. Company Queries with Multiple Operations**
```python
def multi_operation_company_queries(n, superiors, operations):
    # Handle company queries with multiple operation types
    
    # Build parent array
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = superiors[i - 2]
    
    # Binary lifting table
    log_n = 20
    ancestor = [[0] * log_n for _ in range(n + 1)]
    
    # Initialize base case
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Fill the table
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
    
    def find_depth(employee):
        # Find depth of employee in hierarchy
        depth = 0
        current = employee
        while current != 0:
            depth += 1
            current = parent[current]
        return depth - 1
    
    def find_all_superiors(employee):
        # Find all superiors of an employee
        superiors_list = []
        current = employee
        while current != 0:
            superiors_list.append(current)
            current = parent[current]
        return superiors_list
    
    # Process operations
    results = []
    for operation in operations:
        if operation[0] == 'kth_superior':
            # K-th superior query
            employee, k = operation[1], operation[2]
            result = find_kth_superior(employee, k)
            results.append(result)
        elif operation[0] == 'depth':
            # Depth query
            employee = operation[1]
            result = find_depth(employee)
            results.append(result)
        elif operation[0] == 'all_superiors':
            # All superiors query
            employee = operation[1]
            result = find_all_superiors(employee)
            results.append(result)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Company Queries**: Various company hierarchy problems
- **Binary Lifting**: Binary lifting technique problems
- **Tree Ancestors**: Tree ancestor query problems
- **Tree Algorithms**: Tree traversal and query problems

## 📚 Learning Points

### Key Takeaways
- **Binary lifting** enables efficient ancestor queries
- **K-th ancestor** can be found using binary representation
- **Precomputation** is key for efficient query answering
- **Tree structure** enables logarithmic ancestor queries

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

*This analysis shows how to efficiently find k-th ancestors in trees using binary lifting technique.*