---
layout: simple
title: "Tree Matching - Maximum Matching in Trees"
permalink: /problem_soulutions/tree_algorithms/tree_matching_analysis
---

# Tree Matching - Maximum Matching in Trees

## 📋 Problem Description

Given a tree with n nodes, find the maximum number of edges that can be removed so that the remaining graph is a matching (each node has degree at most 1).

This is a maximum matching problem on trees. A matching is a set of edges where no two edges share a common vertex. We need to find the maximum number of edges that can be kept such that each node has degree at most 1.

**Input**: 
- First line: Integer n (number of nodes)
- Next n-1 lines: Two integers a and b (edge between nodes a and b)

**Output**: 
- One integer: maximum number of edges that can be removed

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n

**Example**:
```
Input:
5
1 2
1 3
3 4
3 5

Output:
2
```

**Explanation**: 
- Tree structure: 1-2, 1-3, 3-4, 3-5
- Maximum matching: (1,2) and (3,4) or (1,2) and (3,5)
- We can keep 2 edges, so we remove 2 edges
- Each node in the matching has degree at most 1

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find maximum matching in a tree (maximum number of edges with no shared vertices)
- **Key Insight**: Use greedy DFS approach processing nodes bottom-up
- **Challenge**: Ensure optimal matching while maintaining tree structure

### Step 2: Initial Approach
**Greedy DFS approach for maximum matching in trees:**

```python
def tree_matching_greedy(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Track matched nodes
    matched = [False] * (n + 1)
    matching_edges = 0
    
    def dfs(node, parent):
        nonlocal matching_edges
        
        # Process children first
        for child in tree[node]:
            if child != parent:
                dfs(child, node)
        
        # Try to match with unmatched child
        for child in tree[node]:
            if child != parent and not matched[child] and not matched[node]:
                matched[node] = True
                matched[child] = True
                matching_edges += 1
                break
    
    # Start DFS from root (node 1)
    dfs(1, -1)
    
    # Return number of edges that can be removed
    return (n - 1) - matching_edges
```

**Why this is efficient**: Greedy approach processes nodes bottom-up and matches nodes optimally.

### Improvement 1: Dynamic Programming on Trees - O(n)
**Description**: Use dynamic programming to find maximum matching with better state management.

```python
def tree_matching_dp(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # DP states: dp[node][matched] = max matching in subtree
    dp = {}
    
    def dfs(node, parent, matched):
        state = (node, matched)
        if state in dp:
            return dp[state]
        
        # If current node is matched, children must be unmatched
        if matched:
            result = 0
            for child in tree[node]:
                if child != parent:
                    result += dfs(child, node, False)
            dp[state] = result
            return result
        
        # If current node is unmatched, try matching with children
        unmatched_sum = 0
        for child in tree[node]:
            if child != parent:
                unmatched_sum += dfs(child, node, False)
        
        # Try matching with each child
        best = unmatched_sum
        for child in tree[node]:
            if child != parent:
                # Match with this child
                match_with_child = 1 + dfs(child, node, True)
                # Add unmatched children
                other_children = unmatched_sum - dfs(child, node, False)
                best = max(best, match_with_child + other_children)
        
        dp[state] = best
        return best
    
    # Find maximum matching
    max_matching = dfs(1, -1, False)
    
    # Return number of edges that can be removed
    return (n - 1) - max_matching
```

**Why this improvement works**: Dynamic programming considers all possible matching states and finds the optimal solution.

### Step 3: Optimization/Alternative
**Optimized greedy approach with post-order traversal:**

```python
def tree_matching_optimized_greedy(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Track matched nodes
    matched = [False] * (n + 1)
    matching_edges = 0
    
    def dfs(node, parent):
        nonlocal matching_edges
        
        # Process all children first
        unmatched_children = []
        for child in tree[node]:
            if child != parent:
                dfs(child, node)
                if not matched[child]:
                    unmatched_children.append(child)
        
        # Try to match with an unmatched child
        if unmatched_children and not matched[node]:
            matched[node] = True
            matched[unmatched_children[0]] = True
            matching_edges += 1
    
    # Start DFS from root (node 1)
    dfs(1, -1)
    
    # Return number of edges that can be removed
    return (n - 1) - matching_edges
```

**Why this improvement works**: Optimized greedy approach is simpler and more efficient than DP for this problem.

### Alternative: BFS with Level Order - O(n)
**Description**: Use BFS with level order traversal for educational purposes.

```python
from collections import deque

def tree_matching_bfs(n, edges):
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Track matched nodes
    matched = [False] * (n + 1)
    matching_edges = 0
    
    # BFS with level order traversal
    queue = deque([(1, -1)])
    visited = [False] * (n + 1)
    visited[1] = True
    
    while queue:
        node, parent = queue.popleft()
        
        # Add children to queue
        for child in tree[node]:
            if child != parent and not visited[child]:
                visited[child] = True
                queue.append((child, node))
        
        # Try to match with unmatched child
        if not matched[node]:
            for child in tree[node]:
                if child != parent and not matched[child]:
                    matched[node] = True
                    matched[child] = True
                    matching_edges += 1
                    break
    
    # Return number of edges that can be removed
    return (n - 1) - matching_edges
```

**Why this works**: BFS approach processes nodes level by level, which can be useful for understanding.

### Step 4: Complete Solution

```python
n = int(input())
edges = [tuple(map(int, input().split())) for _ in range(n - 1)]

# Build adjacency list
tree = [[] for _ in range(n + 1)]
for a, b in edges:
    tree[a].append(b)
    tree[b].append(a)

# Track matched nodes
matched = [False] * (n + 1)
matching_edges = 0

def dfs(node, parent):
    global matching_edges
    
    # Process all children first
    unmatched_children = []
    for child in tree[node]:
        if child != parent:
            dfs(child, node)
            if not matched[child]:
                unmatched_children.append(child)
    
    # Try to match with an unmatched child
    if unmatched_children and not matched[node]:
        matched[node] = True
        matched[unmatched_children[0]] = True
        matching_edges += 1

# Start DFS from root (node 1)
dfs(1, -1)

# Print number of edges that can be removed
print((n - 1) - matching_edges)
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple tree (should return correct matching)
- **Test 2**: Linear tree (should return optimal matching)
- **Test 3**: Star tree (should return 1 matching)
- **Test 4**: Complex tree (should find maximum matching)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Greedy DFS | O(n) | O(n) | Bottom-up matching |
| Dynamic Programming | O(n) | O(n) | Optimal substructure |
| Optimized Greedy | O(n) | O(n) | Most efficient approach |
| BFS | O(n) | O(n) | Level-based processing |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Maximum Matching**: Find maximum number of edges with no shared vertices
- **Tree DP**: Dynamic programming on trees with optimal substructure
- **Greedy Approach**: Bottom-up processing for optimal matching
- **Post-order Traversal**: Process children before parent for tree problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted Tree Matching**
```python
def weighted_tree_matching(n, edges, weights):
    # Find maximum weight matching in tree
    
    # Build adjacency list with weights
    tree = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        tree[a].append((b, weights[i]))
        tree[b].append((a, weights[i]))
    
    # DP states: dp[node][matched] = max weight matching in subtree
    dp = {}
    
    def dfs(node, parent, matched):
        state = (node, matched)
        if state in dp:
            return dp[state]
        
        if matched:
            # Current node is matched, children must be unmatched
            result = 0
            for child, weight in tree[node]:
                if child != parent:
                    result += dfs(child, node, False)
            dp[state] = result
            return result
        
        # Current node is unmatched, try matching with children
        unmatched_sum = 0
        for child, weight in tree[node]:
            if child != parent:
                unmatched_sum += dfs(child, node, False)
        
        # Try matching with each child
        best = unmatched_sum
        for child, weight in tree[node]:
            if child != parent:
                # Match with this child
                match_with_child = weight + dfs(child, node, True)
                # Add unmatched children
                other_children = unmatched_sum - dfs(child, node, False)
                best = max(best, match_with_child + other_children)
        
        dp[state] = best
        return best
    
    return dfs(1, -1, False)
```

#### **2. Tree Matching with Constraints**
```python
def constrained_tree_matching(n, edges, constraints):
    # Find maximum matching with additional constraints
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Track matched nodes
    matched = [False] * (n + 1)
    matching_edges = 0
    
    def dfs(node, parent):
        nonlocal matching_edges
        
        # Process all children first
        unmatched_children = []
        for child in tree[node]:
            if child != parent:
                dfs(child, node)
                if not matched[child]:
                    unmatched_children.append(child)
        
        # Apply constraints
        if constraints.get('max_degree', float('inf')) <= len(unmatched_children):
            return
        
        # Try to match with unmatched children
        if unmatched_children and not matched[node]:
            # Check if matching is allowed by constraints
            if constraints.get('allow_matching', True):
                matched[node] = True
                matched[unmatched_children[0]] = True
                matching_edges += 1
    
    # Start DFS from root
    dfs(1, -1)
    
    return matching_edges
```

#### **3. Dynamic Tree Matching**
```python
def dynamic_tree_matching(n, edges, updates):
    # Handle dynamic updates to tree matching
    
    # Build adjacency list
    tree = [[] for _ in range(n + 1)]
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    def compute_matching():
        # Track matched nodes
        matched = [False] * (n + 1)
        matching_edges = 0
        
        def dfs(node, parent):
            nonlocal matching_edges
            
            # Process all children first
            unmatched_children = []
            for child in tree[node]:
                if child != parent:
                    dfs(child, node)
                    if not matched[child]:
                        unmatched_children.append(child)
            
            # Try to match with an unmatched child
            if unmatched_children and not matched[node]:
                matched[node] = True
                matched[unmatched_children[0]] = True
                matching_edges += 1
        
        # Start DFS from root
        dfs(1, -1)
        return matching_edges
    
    # Process updates
    results = []
    for update in updates:
        if update[0] == 'add':
            # Add edge
            a, b = update[1], update[2]
            tree[a].append(b)
            tree[b].append(a)
        elif update[0] == 'remove':
            # Remove edge
            a, b = update[1], update[2]
            tree[a].remove(b)
            tree[b].remove(a)
        
        # Recompute matching
        result = compute_matching()
        results.append(result)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Maximum Matching**: Various matching problems
- **Tree DP**: Dynamic programming on trees
- **Graph Algorithms**: Matching and tree problems
- **Greedy Algorithms**: Greedy tree algorithms

## 📚 Learning Points

### Key Takeaways
- **Greedy approach** works well for tree matching problems
- **Dynamic programming** provides optimal solutions
- **Post-order traversal** is crucial for tree problems
- **Tree structure** simplifies matching algorithms

## Key Insights for Other Problems

### 1. **Tree Matching Problems**
**Principle**: Use greedy approaches for tree matching problems, processing nodes bottom-up.
**Applicable to**:
- Tree matching problems
- Graph algorithms
- Greedy algorithms
- Algorithm design

**Example Problems**:
- Tree matching problems
- Graph algorithms
- Greedy algorithms
- Algorithm design

### 2. **Bottom-up Processing**
**Principle**: Process tree nodes bottom-up when decisions depend on children's states.
**Applicable to**:
- Tree algorithms
- Dynamic programming on trees
- Greedy algorithms
- Algorithm design

**Example Problems**:
- Tree algorithms
- Dynamic programming on trees
- Greedy algorithms
- Algorithm design

### 3. **Greedy vs Dynamic Programming**
**Principle**: Choose between greedy and DP based on problem characteristics and optimality requirements.
**Applicable to**:
- Algorithm selection
- Problem solving
- Optimization problems
- Algorithm design

**Example Problems**:
- Algorithm selection
- Problem solving
- Optimization problems
- Algorithm design

### 4. **State Management**
**Principle**: Manage states efficiently when dealing with matching or selection problems.
**Applicable to**:
- State management
- Algorithm design
- Problem solving
- Optimization

**Example Problems**:
- State management
- Algorithm design
- Problem solving
- Optimization

## Notable Techniques

### 1. **Greedy Tree Matching Pattern**
```python
def greedy_tree_matching(tree, n):
    matched = [False] * (n + 1)
    matching_edges = 0
    
    def dfs(node, parent):
        nonlocal matching_edges
        for child in tree[node]:
            if child != parent:
                dfs(child, node)
        
        # Try to match with unmatched child
        if not matched[node]:
            for child in tree[node]:
                if child != parent and not matched[child]:
                    matched[node] = matched[child] = True
                    matching_edges += 1
                    break
    
    dfs(1, -1)
    return matching_edges
```

### 2. **DP Tree Matching Pattern**
```python
def dp_tree_matching(tree, n):
    dp = {}
    
    def dfs(node, parent, matched):
        state = (node, matched)
        if state in dp:
            return dp[state]
        
        if matched:
            result = sum(dfs(child, node, False) 
                        for child in tree[node] if child != parent)
        else:
            unmatched_sum = sum(dfs(child, node, False) 
                               for child in tree[node] if child != parent)
            best = unmatched_sum
            for child in tree[node]:
                if child != parent:
                    match_with_child = 1 + dfs(child, node, True)
                    other_children = unmatched_sum - dfs(child, node, False)
                    best = max(best, match_with_child + other_children)
            result = best
        
        dp[state] = result
        return result
    
    return dfs(1, -1, False)
```

### 3. **Post-order Matching Pattern**
```python
def post_order_matching(tree, n):
    matched = [False] * (n + 1)
    matching_edges = 0
    
    def dfs(node, parent):
        nonlocal matching_edges
        unmatched_children = []
        
        for child in tree[node]:
            if child != parent:
                dfs(child, node)
                if not matched[child]:
                    unmatched_children.append(child)
        
        if unmatched_children and not matched[node]:
            matched[node] = True
            matched[unmatched_children[0]] = True
            matching_edges += 1
    
    dfs(1, -1)
    return matching_edges
```

## Edge Cases to Remember

1. **Single node**: Tree with only one node
2. **Linear tree**: Tree with no branching
3. **Star tree**: Tree with one central node
4. **Perfect binary tree**: Balanced tree structure
5. **Large trees**: Handle deep recursion properly

## Problem-Solving Framework

1. **Identify matching nature**: This is a tree matching problem
2. **Choose approach**: Use greedy bottom-up approach
3. **Handle state**: Track matched nodes efficiently
4. **Optimize performance**: Use post-order traversal
5. **Calculate result**: Return edges that can be removed

---

*This analysis shows how to efficiently solve tree matching problems using greedy algorithms and tree traversal.* 