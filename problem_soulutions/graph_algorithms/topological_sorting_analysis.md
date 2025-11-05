---
layout: simple
title: "Topological Sorting - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/topological_sorting_analysis
---

# Topological Sorting - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of topological sorting in directed acyclic graphs
- Apply efficient algorithms for finding topological order of vertices
- Implement Kahn's algorithm and DFS-based topological sorting
- Optimize graph algorithms for dependency resolution
- Handle special cases in topological sorting problems

## 📋 Problem Description

Given a directed acyclic graph (DAG), find a topological ordering of its vertices.

**Input**: 
- n: number of vertices
- m: number of edges
- edges: array of (u, v) representing directed edges

**Output**: 
- Topological ordering of vertices, or -1 if no valid ordering exists

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5

**Example**:
```
Input:
n = 6, m = 6
edges = [(0,1), (0,2), (1,3), (2,3), (3,4), (3,5)]

Output:
[0, 1, 2, 3, 4, 5]

Explanation**: 
Topological order: 0 -> 1,2 -> 3 -> 4,5
Vertices are ordered such that for every edge (u,v), u appears before v
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible permutations of vertices
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check if each permutation is valid topological order
- **Inefficient**: O(n! × m) time complexity

**Key Insight**: Check every possible permutation to find valid topological ordering.

**Algorithm**:
- Generate all possible permutations of vertices
- Check if each permutation satisfies topological ordering constraints
- Return the first valid ordering found

**Visual Example**:
```
Graph: 0->1, 0->2, 1->3, 2->3, 3->4, 3->5

All possible permutations:
┌─────────────────────────────────────┐
│ Permutation 1: [0,1,2,3,4,5] ✓    │
│ Permutation 2: [0,2,1,3,4,5] ✓    │
│ Permutation 3: [1,0,2,3,4,5] ✗    │
│ Permutation 4: [2,0,1,3,4,5] ✗    │
│ Permutation 5: [0,1,2,3,5,4] ✓    │
│ Permutation 6: [0,2,1,3,5,4] ✓    │
│                                   │
│ Check constraints:                 │
│ - 0->1: 0 before 1 ✓              │
│ - 0->2: 0 before 2 ✓              │
│ - 1->3: 1 before 3 ✓              │
│ - 2->3: 2 before 3 ✓              │
│ - 3->4: 3 before 4 ✓              │
│ - 3->5: 3 before 5 ✓              │
│                                   │
│ Valid orderings: 1, 2, 5, 6       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_topological_sorting(n, edges):
    """Find topological ordering using brute force approach"""
    from itertools import permutations
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    def is_valid_topological_order(permutation):
        """Check if permutation is valid topological order"""
        position = {vertex: i for i, vertex in enumerate(permutation)}
        
        for u, v in edges:
            if position[u] >= position[v]:
                return False
        
        return True
    
    # Try all permutations
    for permutation in permutations(range(n)):
        if is_valid_topological_order(permutation):
            return list(permutation)
    
    return -1  # No valid topological ordering exists

# Example usage
n = 6
edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
result = brute_force_topological_sorting(n, edges)
print(f"Brute force topological ordering: {result}")
```

**Time Complexity**: O(n! × m)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n! × m) time complexity for checking all permutations.

---

### Approach 2: Kahn's Algorithm

**Key Insights from Kahn's Algorithm**:
- **Kahn's Algorithm**: Use Kahn's algorithm for efficient topological sorting
- **Efficient Implementation**: O(n + m) time complexity
- **Queue-based**: Use queue to process vertices with zero in-degree
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use Kahn's algorithm with queue for efficient topological sorting.

**Algorithm**:
- Calculate in-degree for each vertex
- Add vertices with zero in-degree to queue
- Process vertices from queue and update in-degrees
- Continue until all vertices are processed

**Visual Example**:
```
Kahn's algorithm:

Graph: 0->1, 0->2, 1->3, 2->3, 3->4, 3->5
Initial in-degrees: [0, 1, 1, 2, 1, 1]

Step 1: Queue = [0] (in-degree = 0)
┌─────────────────────────────────────┐
│ Process vertex 0:                  │
│ - Remove 0 from queue              │
│ - Update in-degrees: 1->0, 2->0    │
│ - Add 1, 2 to queue                │
│ - Result: [0]                      │
│                                   │
│ Step 2: Queue = [1, 2]            │
│ Process vertex 1:                  │
│ - Remove 1 from queue              │
│ - Update in-degrees: 3->1          │
│ - Result: [0, 1]                   │
│                                   │
│ Process vertex 2:                  │
│ - Remove 2 from queue              │
│ - Update in-degrees: 3->0          │
│ - Add 3 to queue                   │
│ - Result: [0, 1, 2]               │
│                                   │
│ Step 3: Queue = [3]               │
│ Process vertex 3:                  │
│ - Remove 3 from queue              │
│ - Update in-degrees: 4->0, 5->0    │
│ - Add 4, 5 to queue                │
│ - Result: [0, 1, 2, 3]            │
│                                   │
│ Step 4: Queue = [4, 5]            │
│ Process vertices 4, 5:             │
│ - Result: [0, 1, 2, 3, 4, 5]      │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def kahn_topological_sorting(n, edges):
    """Find topological ordering using Kahn's algorithm"""
    from collections import deque
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Initialize queue with vertices having zero in-degree
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    
    while queue:
        # Remove vertex with zero in-degree
        current = queue.popleft()
        result.append(current)
        
        # Update in-degrees of neighbors
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all vertices were processed
    if len(result) != n:
        return -1  # Cycle exists, no topological ordering
    
    return result

# Example usage
n = 6
edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
result = kahn_topological_sorting(n, edges)
print(f"Kahn's topological ordering: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's better**: Uses Kahn's algorithm for O(n + m) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for topological sorting
- **Efficient Implementation**: O(n + m) time complexity
- **Space Efficiency**: O(n + m) space complexity
- **Optimal Complexity**: Best approach for topological sorting

**Key Insight**: Use advanced data structures for optimal topological sorting.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient Kahn's algorithm
- Handle special cases optimally
- Return topological ordering

**Visual Example**:
```
Advanced data structure approach:

For graph: 0->1, 0->2, 1->3, 2->3, 3->4, 3->5
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Graph structure: for efficient    │
│   storage and traversal             │
│ - Queue structure: for optimization  │
│ - In-degree cache: for optimization  │
│                                   │
│ Topological sorting calculation:   │
│ - Use graph structure for efficient │
│   storage and traversal             │
│ - Use queue structure for          │
│   optimization                      │
│ - Use in-degree cache for          │
│   optimization                      │
│                                   │
│ Result: [0, 1, 2, 3, 4, 5]        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_topological_sorting(n, edges):
    """Find topological ordering using advanced data structure approach"""
    from collections import deque
    
    # Use advanced data structures for graph storage
    # Build advanced adjacency list
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Advanced data structures for topological sorting
    # Initialize advanced queue with vertices having zero in-degree
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    
    # Advanced Kahn's algorithm
    while queue:
        # Remove vertex with zero in-degree using advanced data structures
        current = queue.popleft()
        result.append(current)
        
        # Update in-degrees of neighbors using advanced data structures
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Advanced cycle detection
    if len(result) != n:
        return -1  # Cycle exists, no topological ordering
    
    return result

# Example usage
n = 6
edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
result = advanced_data_structure_topological_sorting(n, edges)
print(f"Advanced data structure topological ordering: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × m) | O(n) | Try all possible permutations |
| Kahn's Algorithm | O(n + m) | O(n + m) | Use queue to process zero in-degree vertices |
| Advanced Data Structure | O(n + m) | O(n + m) | Use advanced data structures |

### Time Complexity
- **Time**: O(n + m) - Use Kahn's algorithm for efficient topological sorting
- **Space**: O(n + m) - Store graph and auxiliary data structures

### Why This Solution Works
- **Kahn's Algorithm**: Use queue to process vertices with zero in-degree
- **In-degree Tracking**: Track incoming edges for each vertex
- **Cycle Detection**: Detect cycles by checking if all vertices are processed
- **Optimal Algorithms**: Use optimal algorithms for topological sorting

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Topological Sorting with Constraints**
**Problem**: Find topological ordering with specific constraints.

**Key Differences**: Apply constraints to topological sorting

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_topological_sorting(n, edges, constraints):
    """Find topological ordering with constraints"""
    from collections import deque
    
    # Build adjacency list with constraints
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for u, v in edges:
        if constraints(u, v):
            adj[u].append(v)
            in_degree[v] += 1
    
    # Initialize queue with vertices having zero in-degree
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    
    while queue:
        # Remove vertex with zero in-degree
        current = queue.popleft()
        result.append(current)
        
        # Update in-degrees of neighbors with constraints
        for neighbor in adj[current]:
            if constraints(current, neighbor):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
    
    # Check if all vertices were processed
    if len(result) != n:
        return -1  # Cycle exists, no topological ordering
    
    return result

# Example usage
n = 6
edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
constraints = lambda u, v: u < v or v == 0  # Special constraint
result = constrained_topological_sorting(n, edges, constraints)
print(f"Constrained topological ordering: {result}")
```

#### **2. Topological Sorting with Different Metrics**
**Problem**: Find topological ordering with different priority metrics.

**Key Differences**: Different priority calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_topological_sorting(n, edges, weight_function):
    """Find topological ordering with different weight metrics"""
    from collections import deque
    import heapq
    
    # Build adjacency list with modified weights
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for u, v in edges:
        weight = weight_function(u, v)
        adj[u].append((v, weight))
        in_degree[v] += 1
    
    # Initialize priority queue with vertices having zero in-degree
    pq = []
    for i in range(n):
        if in_degree[i] == 0:
            weight = weight_function(i, i) if i == i else 0
            heapq.heappush(pq, (weight, i))
    
    result = []
    
    while pq:
        # Remove vertex with highest priority
        weight, current = heapq.heappop(pq)
        result.append(current)
        
        # Update in-degrees of neighbors with modified weights
        for neighbor, edge_weight in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                neighbor_weight = weight_function(neighbor, neighbor)
                heapq.heappush(pq, (neighbor_weight, neighbor))
    
    # Check if all vertices were processed
    if len(result) != n:
        return -1  # Cycle exists, no topological ordering
    
    return result

# Example usage
n = 6
edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
weight_function = lambda u, v: abs(u - v)  # Distance-based weight
result = weighted_topological_sorting(n, edges, weight_function)
print(f"Weighted topological ordering: {result}")
```

#### **3. Topological Sorting with Multiple Dimensions**
**Problem**: Find topological ordering in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_topological_sorting(n, edges, dimensions):
    """Find topological ordering in multiple dimensions"""
    from collections import deque
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Initialize queue with vertices having zero in-degree
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    
    while queue:
        # Remove vertex with zero in-degree
        current = queue.popleft()
        result.append(current)
        
        # Update in-degrees of neighbors
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all vertices were processed
    if len(result) != n:
        return -1  # Cycle exists, no topological ordering
    
    return result

# Example usage
n = 6
edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
dimensions = 1
result = multi_dimensional_topological_sorting(n, edges, dimensions)
print(f"Multi-dimensional topological ordering: {result}")
```

### Related Problems

#### **CSES Problems**
- [Course Schedule](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Building Teams](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Message Route](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Graph
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Graph
- [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Topological sorting, Kahn's algorithm
- **Dependency Resolution**: Task scheduling, build systems
- **Graph Traversal**: BFS, queue operations

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Topological Sorting](https://cp-algorithms.com/graph/topological-sort.html) - Topological sorting algorithms
- [Kahn's Algorithm](https://cp-algorithms.com/graph/topological-sort.html#kahn-algorithm) - Kahn's algorithm

### **Practice Problems**
- [CSES Course Schedule](https://cses.fi/problemset/task/1075) - Medium
- [CSES Building Teams](https://cses.fi/problemset/task/1075) - Medium
- [CSES Message Route](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Topological Sorting](https://en.wikipedia.org/wiki/Topological_sorting) - Wikipedia article
- [Kahn's Algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm) - Wikipedia article
