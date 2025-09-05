---
layout: simple
title: "Tree Matching - Maximum Matching in Trees"
permalink: /problem_soulutions/tree_algorithms/tree_matching_analysis
---

# Tree Matching - Maximum Matching in Trees

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand maximum matching problems in trees and matching algorithms
- [ ] **Objective 2**: Apply dynamic programming or greedy algorithms to find maximum matching in trees
- [ ] **Objective 3**: Implement efficient tree matching algorithms with O(n) time complexity
- [ ] **Objective 4**: Optimize tree matching using dynamic programming, greedy approaches, and tree properties
- [ ] **Objective 5**: Handle edge cases in tree matching (single node, linear tree, star tree, no matching possible)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Maximum matching, dynamic programming, greedy algorithms, tree algorithms, matching theory
- **Data Structures**: Trees, adjacency lists, matching tracking, edge tracking, tree representation
- **Mathematical Concepts**: Matching theory, tree theory, graph theory, optimization mathematics, matching analysis
- **Programming Skills**: Dynamic programming implementation, tree traversal, matching algorithms, algorithm implementation
- **Related Problems**: Tree algorithms, Matching problems, Dynamic programming problems

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

## 🎯 Visual Example

### Input
```
n = 5
Edges: [(1,2), (1,3), (3,4), (3,5)]
```

### Tree Structure
```
Node 1
├── Node 2
└── Node 3
    ├── Node 4
    └── Node 5

Tree representation:
    1
   / \
  2   3
     / \
    4   5
```

### Maximum Matching Analysis
```
All possible matchings:
1. (1,2) - covers nodes 1,2
2. (3,4) - covers nodes 3,4
3. (3,5) - covers nodes 3,5

Valid combinations:
- (1,2) and (3,4): covers nodes 1,2,3,4
- (1,2) and (3,5): covers nodes 1,2,3,5

Maximum matching size: 2 edges
Edges to remove: 5 - 2 = 3 edges
But the expected output is 2, let me recalculate...

Wait, let me check the problem statement again:
- We need to find maximum number of edges that can be REMOVED
- So if maximum matching has 2 edges, we remove 3 edges
- But expected output is 2, which suggests the maximum matching has 3 edges

Let me recalculate:
- Maximum matching: (1,2), (3,4), (3,5) - but this is invalid (node 3 has degree 2)
- Valid maximum matching: (1,2), (3,4) or (1,2), (3,5)
- Size: 2 edges
- Edges to remove: 4 - 2 = 2 edges
- This matches the expected output: 2
```

### Greedy DFS Approach
```
DFS traversal order: 2, 4, 5, 3, 1

Step 1: Process leaf nodes
- Node 2: no children, can be matched with parent
- Node 4: no children, can be matched with parent
- Node 5: no children, can be matched with parent

Step 2: Process internal nodes
- Node 3: has children 4,5
- Can match with one child (e.g., 3-4)
- Node 1: has children 2,3
- Can match with one child (e.g., 1-2)

Final matching: (1,2), (3,4)
Edges removed: 2
```

### Key Insight
Maximum matching in trees works by:
1. Using greedy DFS approach
2. Process nodes bottom-up
3. For each node, decide whether to match with parent or child
4. Ensure no node has degree > 1
5. Time complexity: O(n) for single DFS traversal
6. Space complexity: O(n) for recursion stack

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

## 🎨 Visual Example

### Input Example
```
Tree:
5
1 2
1 3
3 4
3 5
```

### Tree Structure Visualization
```
Tree Structure:
    1
   / \
  2   3
     / \
    4   5

All edges: (1,2), (1,3), (3,4), (3,5)
Total edges: 4
```

### Understanding Maximum Matching
```
A matching is a set of edges where no two edges share a common vertex.
Each node can be incident to at most one edge in the matching.

Possible matchings:
1. {(1,2), (3,4)} - size 2
2. {(1,2), (3,5)} - size 2  
3. {(1,3), (3,4)} - invalid (node 3 has degree 2)
4. {(1,3), (3,5)} - invalid (node 3 has degree 2)
5. {(3,4), (3,5)} - invalid (node 3 has degree 2)

Maximum matching size: 2
Edges to remove: 4 - 2 = 2
```

### Greedy DFS Approach
```
Step 1: Post-order traversal
    1
   / \
  2   3
     / \
    4   5

Process nodes in order: 4, 5, 3, 2, 1

Step 2: Process leaf nodes
Node 4: unmatched, can be matched with parent
Node 5: unmatched, can be matched with parent

Step 3: Process node 3
Node 3 has children 4 and 5
- Both children are unmatched
- Can match with either child
- Choose to match with child 4: (3,4)
- Node 3: matched
- Node 4: matched
- Node 5: unmatched

Step 4: Process node 2
Node 2 is a leaf, unmatched
- Can be matched with parent 1
- Node 2: can be matched

Step 5: Process node 1
Node 1 has children 2 and 3
- Child 2: unmatched
- Child 3: matched
- Can match with child 2: (1,2)
- Node 1: matched
- Node 2: matched

Final matching: {(1,2), (3,4)}
Size: 2
```

### Dynamic Programming Approach
```
DP State: dp[node][matched] = max matching in subtree rooted at node
- matched = true: node is matched with its parent
- matched = false: node is not matched with its parent

Tree with DP states:
    1 (dp[1][false] = 2)
   / \
  2   3 (dp[3][false] = 1)
     / \
    4   5 (dp[4][false] = 0, dp[5][false] = 0)

DP Calculation:
Node 4: dp[4][false] = 0, dp[4][true] = 0
Node 5: dp[5][false] = 0, dp[5][true] = 0
Node 3: 
- dp[3][false] = max(dp[4][false] + dp[5][false], 
                     dp[4][true] + dp[5][false] + 1,
                     dp[4][false] + dp[5][true] + 1) = 1
- dp[3][true] = dp[4][false] + dp[5][false] = 0
Node 2: dp[2][false] = 0, dp[2][true] = 0
Node 1:
- dp[1][false] = max(dp[2][false] + dp[3][false],
                     dp[2][true] + dp[3][false] + 1,
                     dp[2][false] + dp[3][true] + 1) = 2
- dp[1][true] = dp[2][false] + dp[3][false] = 1

Result: dp[1][false] = 2
```

### Step-by-Step Matching Process
```
Initial state: All nodes unmatched
    1
   / \
  2   3
     / \
    4   5

Step 1: Process node 4
- Node 4 is leaf, unmatched
- Can match with parent 3
- Match (3,4)
- Node 3: matched
- Node 4: matched

Step 2: Process node 5
- Node 5 is leaf, unmatched
- Parent 3 is already matched
- Node 5: remains unmatched

Step 3: Process node 2
- Node 2 is leaf, unmatched
- Can match with parent 1
- Match (1,2)
- Node 1: matched
- Node 2: matched

Final state:
    1 (matched)
   / \
  2   3 (matched)
     / \
    4   5 (unmatched)
   (matched)

Matching: {(1,2), (3,4)}
Size: 2
```

### Alternative Matching
```
Alternative approach: Match (1,2) and (3,5)

Step 1: Process node 5
- Node 5 is leaf, unmatched
- Can match with parent 3
- Match (3,5)
- Node 3: matched
- Node 5: matched

Step 2: Process node 4
- Node 4 is leaf, unmatched
- Parent 3 is already matched
- Node 4: remains unmatched

Step 3: Process node 2
- Node 2 is leaf, unmatched
- Can match with parent 1
- Match (1,2)
- Node 1: matched
- Node 2: matched

Final state:
    1 (matched)
   / \
  2   3 (matched)
     / \
    4   5 (matched)
   (unmatched)

Matching: {(1,2), (3,5)}
Size: 2
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Greedy DFS      │ O(n)         │ O(n)         │ Bottom-up    │
│                 │              │              │ matching     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Dynamic Prog    │ O(n)         │ O(n)         │ Optimal      │
│                 │              │              │ substructure │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Optimized Greedy│ O(n)         │ O(n)         │ Most         │
│                 │              │              │ efficient    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ BFS             │ O(n)         │ O(n)         │ Level-based  │
│                 │              │              │ processing   │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Tree Matching Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: tree     │
              │ (n nodes, edges)│
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Choose Algorithm│
              │ (Greedy DFS/    │
              │  Dynamic Prog)  │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Post-order DFS  │
              │ Traversal       │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For each node:  │
              │ - If leaf and   │
              │   parent free:  │
              │   match with    │
              │   parent        │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return Maximum  │
              │ Matching Size   │
              └─────────────────┘
                      │
                      ▼
                    End
```

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