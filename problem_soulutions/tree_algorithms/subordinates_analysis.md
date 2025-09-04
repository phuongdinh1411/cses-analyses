---
layout: simple
title: "Subordinates - Tree Subtree Size Calculation"
permalink: /problem_soulutions/tree_algorithms/subordinates_analysis
---

# Subordinates - Tree Subtree Size Calculation

## 📋 Problem Description

You are given a company hierarchy with a tree structure. The company has n employees, numbered 1,2,…,n. Each employee except 1 has exactly one superior. Your task is to find for each employee the number of subordinates.

This is a tree subtree size calculation problem. We need to find the size of the subtree rooted at each node, which represents the number of subordinates for each employee.

**Input**: 
- First line: Integer n (number of employees)
- Second line: n-1 integers p₂, p₃, ..., pₙ (superior of employee i)

**Output**: 
- n integers: number of subordinates for each employee

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ pᵢ < i

**Example**:
```
Input:
5
1 1 2 2

Output:
4 2 0 0 0
```

**Explanation**: 
- Employee 1 has 4 subordinates (2, 3, 4, 5)
- Employee 2 has 2 subordinates (3, 4)
- Employees 3, 4, 5 have 0 subordinates (leaves)
- Tree structure: 1 → 2 → 3, 1 → 2 → 4, 1 → 5

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find subtree size for each node in a tree
- **Key Insight**: Use DFS to calculate subtree sizes bottom-up
- **Challenge**: Efficiently compute subtree sizes for all nodes

### Step 2: Initial Approach
**DFS with recursion to count subordinates for each node:**

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

### Step 3: Optimization/Alternative
**Single DFS with post-order traversal:**

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

### Step 4: Complete Solution

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

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple tree (should return correct subtree sizes)
- **Test 2**: Linear tree (should return correct counts)
- **Test 3**: Star tree (should return correct counts)
- **Test 4**: Complex tree (should find all subtree sizes)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS with Recursion | O(n) | O(n) | Natural tree traversal |
| DFS with Memoization | O(n) | O(n) | Avoid redundant calculations |
| Single DFS | O(n) | O(n) | Most efficient approach |
| BFS | O(n) | O(n) | Level-based traversal |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Subtree Size**: Calculate size of subtree rooted at each node
- **Post-order Traversal**: Process children before parent for tree problems
- **Tree DP**: Dynamic programming on trees with optimal substructure
- **DFS Traversal**: Depth-first search for tree problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Subtree Sum Calculation**
```python
def subtree_sum(n, superiors, values):
    # Calculate sum of values in each subtree
    
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store subtree sums
    subtree_sums = [0] * (n + 1)
    
    def dfs(node):
        sum_val = values[node - 1]  # Node's own value
        for child in tree[node]:
            sum_val += dfs(child)
        subtree_sums[node] = sum_val
        return sum_val
    
    # Start DFS from root
    dfs(1)
    
    return subtree_sums[1:n + 1]
```

#### **2. Subtree Maximum Value**
```python
def subtree_maximum(n, superiors, values):
    # Find maximum value in each subtree
    
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Array to store subtree maximums
    subtree_maxs = [0] * (n + 1)
    
    def dfs(node):
        max_val = values[node - 1]  # Node's own value
        for child in tree[node]:
            max_val = max(max_val, dfs(child))
        subtree_maxs[node] = max_val
        return max_val
    
    # Start DFS from root
    dfs(1)
    
    return subtree_maxs[1:n + 1]
```

#### **3. Subtree Statistics**
```python
def subtree_statistics(n, superiors, values):
    # Calculate various statistics for each subtree
    
    # Build adjacency list (tree)
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        superior = superiors[i - 2]
        tree[superior].append(i)
    
    # Arrays to store subtree statistics
    subtree_sizes = [0] * (n + 1)
    subtree_sums = [0] * (n + 1)
    subtree_maxs = [0] * (n + 1)
    subtree_mins = [0] * (n + 1)
    
    def dfs(node):
        size = 1
        sum_val = values[node - 1]
        max_val = values[node - 1]
        min_val = values[node - 1]
        
        for child in tree[node]:
            child_size, child_sum, child_max, child_min = dfs(child)
            size += child_size
            sum_val += child_sum
            max_val = max(max_val, child_max)
            min_val = min(min_val, child_min)
        
        subtree_sizes[node] = size
        subtree_sums[node] = sum_val
        subtree_maxs[node] = max_val
        subtree_mins[node] = min_val
        
        return size, sum_val, max_val, min_val
    
    # Start DFS from root
    dfs(1)
    
    return {
        'sizes': subtree_sizes[1:n + 1],
        'sums': subtree_sums[1:n + 1],
        'maxs': subtree_maxs[1:n + 1],
        'mins': subtree_mins[1:n + 1]
    }
```

## 🔗 Related Problems

### Links to Similar Problems
- **Subtree Size**: Various subtree calculation problems
- **Tree DP**: Dynamic programming on trees
- **Tree Traversal**: DFS and BFS tree problems
- **Tree Statistics**: Tree aggregation problems

## 📚 Learning Points

### Key Takeaways
- **Post-order traversal** is essential for subtree calculations
- **Single DFS** is more efficient than multiple recursive calls
- **Tree structure** simplifies subtree size calculations
- **Memoization** can optimize overlapping calculations

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