---
layout: simple
title: "Company Queries III - Number of Employees in Subtree"
permalink: /problem_soulutions/tree_algorithms/company_queries_iii_analysis
---

# Company Queries III - Number of Employees in Subtree

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand tree subtree size query problems and subtree counting algorithms
- Apply DFS to calculate subtree sizes efficiently for all nodes
- Implement efficient subtree size algorithms with O(n) preprocessing and O(1) query time complexity
- Optimize subtree size calculation using DFS, tree traversal, and tree properties
- Handle edge cases in subtree size queries (single node, linear tree, star tree, large trees)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: DFS, tree traversal, subtree size calculation, tree algorithms, recursive algorithms
- **Data Structures**: Trees, adjacency lists, subtree tracking, size tracking, tree representation
- **Mathematical Concepts**: Tree theory, subtree mathematics, size calculation, tree properties
- **Programming Skills**: DFS implementation, tree traversal, recursive algorithms, subtree counting, algorithm implementation
- **Related Problems**: Company Queries I (ancestor queries), Tree algorithms, Subtree problems

## 📋 Problem Description

A company has n employees, numbered 1,2,…,n. Each employee except 1 has exactly one superior. Given q queries, for each query find the number of employees in the subtree of an employee.

This is a tree subtree size query problem that requires finding the number of nodes in each subtree. The solution involves using DFS to calculate subtree sizes efficiently.

**Input**: 
- First line: Two integers n and q (number of employees and queries)
- Second line: n-1 integers p₂, p₃, ..., pₙ (each pᵢ is the superior of employee i)
- Next q lines: One integer a (find the number of employees in the subtree of employee a)

**Output**: 
- For each query, print the number of employees in the subtree

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ pᵢ < i
- 1 ≤ a ≤ n

**Example**:
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

**Explanation**: 
- Query 1: Subtree of employee 1 contains all 5 employees
- Query 2: Subtree of employee 2 contains employees 2, 4, 5 (3 employees)
- Query 3: Subtree of employee 3 contains only employee 3 (1 employee)

## 🎯 Visual Example

### Input
```
n = 5, q = 3
Superiors: [1, 1, 2, 2]
Queries: [1, 2, 3]
```

### Tree Structure
```
Employee 1 (CEO)
├── Employee 2
│   ├── Employee 3
│   └── Employee 4
└── Employee 5

Tree representation:
    1
   / \
  2   5
 / \
3   4
```

### Subtree Size Queries
```
Query 1: Subtree size of employee 1
- Subtree of 1: {1, 2, 3, 4, 5}
- Size: 5
- Result: 5

Query 2: Subtree size of employee 2
- Subtree of 2: {2, 3, 4}
- Size: 3
- Result: 3

Query 3: Subtree size of employee 3
- Subtree of 3: {3}
- Size: 1
- Result: 1
```

### DFS Subtree Size Calculation
```
DFS Traversal Order: 3, 4, 2, 5, 1

Step 1: Process leaf nodes
- Employee 3: subtree_size = 1
- Employee 4: subtree_size = 1
- Employee 5: subtree_size = 1

Step 2: Process internal nodes
- Employee 2: subtree_size = 1 + 1 + 1 = 3
- Employee 1: subtree_size = 3 + 1 + 1 = 5

Final subtree sizes: [5, 3, 1, 1, 1]
```

### Key Insight
Subtree size calculation works by:
1. Using DFS to traverse the tree
2. For each node, sum up subtree sizes of children
3. Add 1 for the node itself
4. Time complexity: O(n) for single DFS traversal
5. Space complexity: O(n) for recursion stack

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find the number of nodes in each subtree efficiently
- **Key Insight**: Use DFS to calculate subtree sizes in O(n) time
- **Challenge**: Handle multiple queries efficiently without O(q × n) complexity

### Step 2: Initial Approach
**DFS for each query (inefficient but correct):**

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

### Step 3: Optimization/Alternative
**Iterative DFS:**

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

### Step 4: Complete Solution

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

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple tree (should return correct subtree sizes)
- **Test 2**: Linear tree (should return correct sizes)
- **Test 3**: Star tree (should return correct sizes)
- **Test 4**: Complex tree (should find all subtree sizes)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS for Each Query | O(q * n) | O(n) | Simple but slow |
| Precompute Subtree Sizes | O(n + q) | O(n) | Single DFS preprocessing |
| Iterative DFS | O(n + q) | O(n) | Avoid recursion stack |
| BFS | O(n + q) | O(n) | Topological order processing |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Subtree Size Calculation**: Use DFS to calculate subtree sizes efficiently
- **Post-order Traversal**: Process children before parent for subtree calculations
- **Precomputation**: Calculate all subtree sizes in O(n) time for O(1) queries
- **Tree Traversal**: Use DFS or BFS to traverse tree structure

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Company Queries with Dynamic Updates**
```python
def dynamic_subtree_queries(n, superiors, operations):
    # Handle subtree queries with dynamic tree updates
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    def calculate_subtree_sizes():
        # Recalculate subtree sizes after updates
        subtree_sizes = [0] * (n + 1)
        
        def dfs(node):
            subtree_sizes[node] = 1
            for child in tree[node]:
                subtree_sizes[node] += dfs(child)
            return subtree_sizes[node]
        
        dfs(1)
        return subtree_sizes
    
    # Process operations
    results = []
    for operation in operations:
        if operation[0] == 'add_employee':
            # Add new employee
            employee, superior = operation[1], operation[2]
            tree[superior].append(employee)
        elif operation[0] == 'remove_employee':
            # Remove employee
            employee, superior = operation[1], operation[2]
            tree[superior].remove(employee)
        elif operation[0] == 'query':
            # Subtree size query
            employee = operation[1]
            subtree_sizes = calculate_subtree_sizes()
            results.append(subtree_sizes[employee])
    
    return results
```

#### **2. Company Queries with Weighted Subtrees**
```python
def weighted_subtree_queries(n, superiors, weights, queries):
    # Handle subtree queries with weighted nodes
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store weighted subtree sizes
    weighted_subtree_sizes = [0] * (n + 1)
    
    def calculate_weighted_subtree_sizes():
        def dfs(node):
            weighted_subtree_sizes[node] = weights[node]
            for child in tree[node]:
                weighted_subtree_sizes[node] += dfs(child)
            return weighted_subtree_sizes[node]
        
        dfs(1)
    
    # Calculate all weighted subtree sizes
    calculate_weighted_subtree_sizes()
    
    # Process queries
    results = []
    for employee in queries:
        results.append(weighted_subtree_sizes[employee])
    
    return results
```

#### **3. Company Queries with Range Constraints**
```python
def constrained_subtree_queries(n, superiors, queries, constraints):
    # Handle subtree queries with range constraints
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store subtree sizes
    subtree_sizes = [0] * (n + 1)
    
    def calculate_subtree_sizes():
        def dfs(node):
            subtree_sizes[node] = 1
            for child in tree[node]:
                subtree_sizes[node] += dfs(child)
            return subtree_sizes[node]
        
        dfs(1)
    
    # Calculate all subtree sizes
    calculate_subtree_sizes()
    
    def count_employees_in_range(employee, min_level, max_level):
        # Count employees in subtree within level range
        count = 0
        
        def dfs_with_level(node, level):
            nonlocal count
            if min_level <= level <= max_level:
                count += 1
            
            for child in tree[node]:
                dfs_with_level(child, level + 1)
        
        dfs_with_level(employee, 0)
        return count
    
    # Process queries
    results = []
    for query in queries:
        employee = query[0]
        if len(query) == 1:
            # Simple subtree size query
            results.append(subtree_sizes[employee])
        else:
            # Range-constrained query
            min_level, max_level = query[1], query[2]
            count = count_employees_in_range(employee, min_level, max_level)
            results.append(count)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Company Queries**: Various company hierarchy problems
- **Subtree Queries**: Tree subtree query problems
- **Tree Algorithms**: Tree traversal and query problems
- **DFS**: Depth-first search problems

## 📚 Learning Points

### Key Takeaways
- **DFS** is ideal for subtree size calculations
- **Post-order traversal** processes children before parents
- **Precomputation** enables O(1) query responses
- **Tree structure** enables efficient subtree operations

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