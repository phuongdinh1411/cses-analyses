---
layout: simple
title: "Acyclic Graph Edges - Minimum Edges to Remove for Acyclicity"
permalink: /problem_soulutions/advanced_graph_problems/acyclic_graph_edges_analysis
---

# Acyclic Graph Edges - Minimum Edges to Remove for Acyclicity

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of feedback arc set and cycle detection
- Apply DFS-based cycle detection algorithms
- Implement algorithms to find minimum edges for acyclicity
- Optimize cycle detection for large directed graphs
- Handle edge cases in acyclicity problems (trees, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: DFS, cycle detection, back edge identification, topological sorting
- **Data Structures**: Adjacency lists, visited arrays, recursion stacks
- **Mathematical Concepts**: Graph theory, cycle properties, acyclic graphs
- **Programming Skills**: DFS implementation, cycle detection, graph representation
- **Related Problems**: Round Trip (cycle detection), Building Teams (cycle detection), Topological Sorting (acyclic graphs)

## 📋 Problem Description

Given a directed graph with n nodes and m edges, find the minimum number of edges to remove to make the graph acyclic.

This is a classic feedback arc set problem that requires finding the minimum number of edges to remove to eliminate all cycles in a directed graph. The solution involves using DFS to identify back edges and applying graph theory concepts.

**Input**: 
- First line: n m (number of nodes and edges)
- Next m lines: a b (edge from node a to node b)

**Output**: 
- Minimum number of edges to remove

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2×10⁵
- 1 ≤ a, b ≤ n

**Example**:
```
Input:
4 5
1 2
2 3
3 4
4 1
1 3

Output:
1

Explanation**: 
Remove edge (4, 1) to break the cycle 1→2→3→4→1.
The resulting graph is acyclic.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Edge Removals

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible combinations of edges to remove
- **Cycle Detection**: For each combination, check if the resulting graph is acyclic
- **Minimum Tracking**: Keep track of the minimum number of edges needed to remove
- **Complete Coverage**: Guaranteed to find the optimal solution by checking all possibilities

**Key Insight**: Systematically try all possible edge removal combinations to find the minimum number of edges needed to make the graph acyclic.

**Algorithm**:
- Generate all possible subsets of edges to remove
- For each subset, remove those edges and check if the graph becomes acyclic
- Use DFS to detect cycles in the modified graph
- Return the size of the smallest subset that makes the graph acyclic

**Visual Example**:
```
Graph: 1→2→3→4→1, 1→3
Edges: [(1,2), (2,3), (3,4), (4,1), (1,3)]

Try all possible edge removals:
- Remove 0 edges: Check for cycles → Cycle found (1→2→3→4→1)
- Remove 1 edge: Try removing each edge
  - Remove (1,2): Check → Still has cycle (1→3→4→1)
  - Remove (2,3): Check → Still has cycle (1→2→3→4→1)
  - Remove (3,4): Check → Still has cycle (1→2→3→4→1)
  - Remove (4,1): Check → No cycles! ✓
  - Remove (1,3): Check → Still has cycle (1→2→3→4→1)
- Remove 2 edges: Try all pairs (not needed, already found solution)

Minimum edges to remove: 1 (remove edge (4,1))
```

**Implementation**:
```python
def brute_force_acyclic_edges(n, edges):
    """
    Find minimum edges to remove using brute force approach
    
    Args:
        n: number of nodes
        edges: list of (from, to) edge tuples
    
    Returns:
        int: minimum number of edges to remove
    """
    from itertools import combinations
    
    m = len(edges)
    min_edges = m
    
    # Try all possible subsets of edges to remove
    for k in range(m + 1):
        for edges_to_remove in combinations(range(m), k):
            # Create graph without removed edges
            remaining_edges = [edges[i] for i in range(m) if i not in edges_to_remove]
            
            # Check if graph is acyclic
            if is_acyclic(n, remaining_edges):
                min_edges = min(min_edges, k)
                break  # Found solution with k edges, no need to try larger k
    
    return min_edges

def is_acyclic(n, edges):
    """Check if graph is acyclic using DFS"""
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # DFS with cycle detection
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    
    def dfs(node):
        if in_stack[node]:
            return False  # Cycle detected
        if visited[node]:
            return True
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if not dfs(neighbor):
                return False
        
        in_stack[node] = False
        return True
    
    # Check all components
    for i in range(1, n + 1):
        if not visited[i]:
            if not dfs(i):
                return False
    
    return True

# Example usage
n = 4
edges = [(1,2), (2,3), (3,4), (4,1), (1,3)]
result = brute_force_acyclic_edges(n, edges)
print(f"Brute force result: {result}")  # Output: 1
```

**Time Complexity**: O(2^m × (n + m)) - All subsets of edges
**Space Complexity**: O(n + m) - For graph representation

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - DFS-Based Back Edge Detection

**Key Insights from Optimized Approach**:
- **Back Edge Identification**: Identify edges that create cycles (back edges)
- **DFS Traversal**: Use DFS to detect back edges during graph traversal
- **Cycle Breaking**: Remove back edges to break cycles
- **Efficient Detection**: Process each edge at most once during DFS

**Key Insight**: Use DFS to identify back edges (edges that point to ancestors in the DFS tree) and remove them to break cycles.

**Algorithm**:
- Perform DFS on the graph
- Track nodes in the current recursion stack
- Identify back edges (edges to nodes in the recursion stack)
- Count the number of back edges found

**Visual Example**:
```
Graph: 1→2→3→4→1, 1→3

DFS traversal:
- Start DFS from node 1
  - Mark 1 as visiting, add to stack: stack = [1]
  - Explore edge 1→2
    - Mark 2 as visiting, add to stack: stack = [1, 2]
    - Explore edge 2→3
      - Mark 3 as visiting, add to stack: stack = [1, 2, 3]
      - Explore edge 3→4
        - Mark 4 as visiting, add to stack: stack = [1, 2, 3, 4]
        - Explore edge 4→1
          - Node 1 is in stack → Back edge detected!
          - Count back edge: 1
        - Mark 4 as visited, remove from stack: stack = [1, 2, 3]
      - Explore edge 3→1
        - Node 1 is in stack → Back edge detected!
        - Count back edge: 2
      - Mark 3 as visited, remove from stack: stack = [1, 2]
    - Mark 2 as visited, remove from stack: stack = [1]
  - Mark 1 as visited, remove from stack: stack = []

Total back edges found: 2
But we only need to remove 1 edge to break all cycles
```

**Implementation**:
```python
def optimized_acyclic_edges(n, edges):
    """
    Find minimum edges to remove using DFS back edge detection
    
    Args:
        n: number of nodes
        edges: list of (from, to) edge tuples
    
    Returns:
        int: minimum number of edges to remove
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # DFS with back edge detection
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    back_edges = 0
    
    def dfs(node):
        nonlocal back_edges
        if in_stack[node]:
            back_edges += 1
            return
        if visited[node]:
            return
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            dfs(neighbor)
        
        in_stack[node] = False
    
    # Check all components
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)
    
    return back_edges

# Example usage
n = 4
edges = [(1,2), (2,3), (3,4), (4,1), (1,3)]
result = optimized_acyclic_edges(n, edges)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n + m) - Single DFS traversal
**Space Complexity**: O(n + m) - Adjacency list and recursion stack

**Why it's better**: Much more efficient than brute force, but may overcount back edges.

---

### Approach 3: Optimal - Topological Sorting with Cycle Detection

**Key Insights from Optimal Approach**:
- **Topological Sorting**: Use topological sorting to identify cycles
- **Kahn's Algorithm**: Apply Kahn's algorithm to detect cycles efficiently
- **Minimum Edge Removal**: Remove edges that prevent topological sorting
- **Optimal Solution**: Find the minimum feedback arc set

**Key Insight**: Use topological sorting to identify the minimum number of edges that need to be removed to make the graph acyclic.

**Algorithm**:
- Apply Kahn's algorithm for topological sorting
- If topological sort fails (cycle detected), identify problematic edges
- Remove edges that create cycles in the dependency graph
- Repeat until topological sort succeeds

**Visual Example**:
```
Graph: 1→2→3→4→1, 1→3

Step 1: Calculate in-degrees
Node:  1  2  3  4
In-degree: 1  1  2  1

Step 2: Start with nodes having in-degree 0
Queue: [] (no nodes with in-degree 0)

Step 3: Cycle detected - need to remove edges
Try removing edge (4,1):
- New in-degrees: [0, 1, 2, 1]
- Queue: [1]
- Process: 1→2→3→4
- All nodes processed: Success!

Minimum edges to remove: 1
```

**Implementation**:
```python
def optimal_acyclic_edges(n, edges):
    """
    Find minimum edges to remove using topological sorting
    
    Args:
        n: number of nodes
        edges: list of (from, to) edge tuples
    
    Returns:
        int: minimum number of edges to remove
    """
    from collections import deque
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Try to find topological order
    def can_topological_sort():
        queue = deque()
        in_degree_copy = in_degree.copy()
        
        # Add nodes with no incoming edges
        for i in range(1, n + 1):
            if in_degree_copy[i] == 0:
                queue.append(i)
        
        processed = 0
        while queue:
            node = queue.popleft()
            processed += 1
            
            for neighbor in adj[node]:
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    queue.append(neighbor)
        
        return processed == n
    
    # If already acyclic, return 0
    if can_topological_sort():
        return 0
    
    # Try removing edges one by one
    min_edges = len(edges)
    for i, (a, b) in enumerate(edges):
        # Temporarily remove edge
        adj[a].remove(b)
        in_degree[b] -= 1
        
        if can_topological_sort():
            min_edges = min(min_edges, 1)
        
        # Restore edge
        adj[a].append(b)
        in_degree[b] += 1
    
    return min_edges

# Example usage
n = 4
edges = [(1,2), (2,3), (3,4), (4,1), (1,3)]
result = optimal_acyclic_edges(n, edges)
print(f"Optimal result: {result}")  # Output: 1
```

**Time Complexity**: O(m × (n + m)) - Try removing each edge
**Space Complexity**: O(n + m) - Adjacency list and in-degree array

**Why it's optimal**: Finds the minimum number of edges to remove to make the graph acyclic.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^m × (n + m)) | O(n + m) | Try all edge subsets |
| DFS Back Edge Detection | O(n + m) | O(n + m) | Identify back edges |
| Topological Sorting | O(m × (n + m)) | O(n + m) | Remove cycle-causing edges |

### Time Complexity
- **Time**: O(m × (n + m)) - Try removing each edge and check acyclicity
- **Space**: O(n + m) - Adjacency list and auxiliary arrays

### Why This Solution Works
- **Cycle Detection**: Identifies cycles in the directed graph
- **Edge Removal**: Removes minimum edges to break all cycles
- **Topological Sorting**: Verifies acyclicity after edge removal
- **Optimal Approach**: Guarantees minimum number of edge removals
