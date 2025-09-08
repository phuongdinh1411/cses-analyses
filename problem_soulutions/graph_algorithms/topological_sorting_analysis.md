---
layout: simple
title: "Topological Sorting - Graph Ordering Algorithm"
permalink: /problem_soulutions/graph_algorithms/topological_sorting_analysis
---

# Topological Sorting - Graph Ordering Algorithm

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand topological sorting and DAG ordering concepts
- Apply Kahn's algorithm or DFS-based approach to find topological orderings
- Implement efficient topological sorting algorithms with proper cycle detection
- Optimize topological sorting solutions using graph representations and algorithm optimizations
- Handle edge cases in topological sorting (cycles, single nodes, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Topological sorting, Kahn's algorithm, DFS-based sorting, cycle detection, DAG algorithms
- **Data Structures**: Queues, stacks, adjacency lists, in-degree tracking, graph representations
- **Mathematical Concepts**: Graph theory, DAG properties, topological ordering, cycle detection, graph ordering
- **Programming Skills**: Graph traversal, cycle detection, topological sorting, algorithm implementation
- **Related Problems**: Cycle Finding (cycle detection), Building Teams (graph coloring), DAG algorithms

## Problem Description

**Problem**: Given a directed acyclic graph (DAG) with n nodes and m edges, find a topological ordering of the nodes. A topological ordering is a linear ordering of vertices such that for every directed edge (u, v), vertex u comes before vertex v in the ordering.

**Input**: 
- First line: Two integers n and m (number of nodes and edges)
- Next m lines: Two integers a and b (edge from node a to node b)

**Output**: 
- A valid topological ordering of the nodes

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n
- Graph must be a DAG (no cycles)
- Graph is directed
- No self-loops or multiple edges between same pair of nodes
- Edges are directed from a to b

**Example**:
```
Input:
5 4
1 2
2 3
1 3
4 5

Output:
1 4 2 5 3
```

**Explanation**: 
- Node 1 has edges to nodes 2 and 3, so it must come before them
- Node 2 has an edge to node 3, so it must come before node 3
- Node 4 has an edge to node 5, so it must come before node 5
- Valid orderings include: [1, 4, 2, 5, 3], [4, 1, 2, 5, 3], etc.

## Visual Example

### Input Graph
```
Nodes: 1, 2, 3, 4, 5
Edges: (1→2), (2→3), (1→3), (4→5)

Graph representation:
1 ──> 2 ──> 3
│     │
└─────┼─────┘
      │
      └────────┘

4 ──> 5
```

### Topological Sorting Process
```
Step 1: Build adjacency list and in-degrees
- Node 1: [2, 3], in-degree: 0
- Node 2: [3], in-degree: 1
- Node 3: [], in-degree: 2
- Node 4: [5], in-degree: 0
- Node 5: [], in-degree: 1

Step 2: Kahn's algorithm (BFS-based)
- Queue: [1, 4] (nodes with in-degree 0)
- Result: []

- Process node 1:
  - Remove 1 from queue
  - Add 1 to result: [1]
  - Update in-degrees: 2→0, 3→1
  - Add 2 to queue: [4, 2]

- Process node 4:
  - Remove 4 from queue
  - Add 4 to result: [1, 4]
  - Update in-degrees: 5→0
  - Add 5 to queue: [2, 5]

- Process node 2:
  - Remove 2 from queue
  - Add 2 to result: [1, 4, 2]
  - Update in-degrees: 3→0
  - Add 3 to queue: [5, 3]

- Process node 5:
  - Remove 5 from queue
  - Add 5 to result: [1, 4, 2, 5]
  - No new nodes to add

- Process node 3:
  - Remove 3 from queue
  - Add 3 to result: [1, 4, 2, 5, 3]
  - No new nodes to add

Step 3: Verify ordering
- All edges point forward ✓
- 1 → 2: 1 comes before 2 ✓
- 2 → 3: 2 comes before 3 ✓
- 1 → 3: 1 comes before 3 ✓
- 4 → 5: 4 comes before 5 ✓
```

### Key Insight
Kahn's algorithm works by:
1. Finding nodes with no incoming edges (in-degree 0)
2. Processing them in BFS order
3. Updating in-degrees of neighbors
4. Time complexity: O(n + m)
5. Space complexity: O(n + m) for graph representation

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Permutation Check (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible orderings and check if they satisfy topological constraints
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible permutations of nodes
2. For each permutation, check if it satisfies all edge constraints
3. Return the first valid topological ordering found
4. Handle cases where no valid ordering exists (cycles)

**Visual Example:**
```
Brute force: Try all possible orderings
For 5 nodes: 5! = 120 possible orderings
- Ordering 1: [1, 2, 3, 4, 5] - Check constraints
- Ordering 2: [1, 2, 3, 5, 4] - Check constraints
- Ordering 3: [1, 2, 4, 3, 5] - Check constraints
- ...
- Ordering 120: [5, 4, 3, 2, 1] - Check constraints

Check each ordering against edge constraints
```

**Implementation:**
```python
def topological_sorting_brute_force(n, m, edges):
    from itertools import permutations
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Try all possible orderings
    for ordering in permutations(range(1, n + 1)):
        valid = True
        for a, b in edges:
            if ordering.index(a) > ordering.index(b):
                valid = False
                break
        if valid:
            return list(ordering)
    
    return []  # No valid ordering (cycle exists)

def solve_topological_sorting_brute_force():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = topological_sorting_brute_force(n, m, edges)
    if result:
        print(' '.join(map(str, result)))
    else:
        print("IMPOSSIBLE")
```

**Time Complexity:** O(n! × m) for n nodes and m edges with exponential permutation generation
**Space Complexity:** O(n) for storing ordering

**Why it's inefficient:**
- O(n!) time complexity is too slow for large n values
- Not suitable for competitive programming with n up to 10^5
- Inefficient for large inputs
- Poor performance with many nodes

### Approach 2: Basic DFS-based Topological Sorting (Better)

**Key Insights from Basic DFS Solution:**
- Use DFS with finish times to find topological ordering
- Much more efficient than brute force approach
- Standard method for topological sorting
- Can handle larger graphs than brute force

**Algorithm:**
1. Use DFS to traverse the graph
2. Record finish times of nodes
3. Sort nodes by finish times in reverse order
4. Return the topological ordering

**Visual Example:**
```
Basic DFS for graph: 1→2→3, 1→3, 4→5
- DFS from node 1: visit 1, 2, 3
- DFS from node 4: visit 4, 5
- Finish times: 3, 2, 1, 5, 4
- Reverse order: 4, 5, 1, 2, 3
- Topological ordering: [4, 5, 1, 2, 3]
```

**Implementation:**
```python
def topological_sorting_basic_dfs(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)
    
    # Reverse to get topological order
    return finish_order[::-1]

def solve_topological_sorting_basic_dfs():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = topological_sorting_basic_dfs(n, m, edges)
    print(' '.join(map(str, result)))
```

**Time Complexity:** O(n + m) for n nodes and m edges with DFS traversal
**Space Complexity:** O(n + m) for graph representation and recursion stack

**Why it's better:**
- O(n + m) time complexity is much better than O(n! × m)
- Standard method for topological sorting
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Kahn's Algorithm with Efficient Queue Management (Optimal)

**Key Insights from Optimized Kahn's Solution:**
- Use Kahn's algorithm with efficient queue management
- Most efficient approach for topological sorting
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use Kahn's algorithm with efficient data structures
2. Implement efficient in-degree tracking and queue management
3. Use optimized BFS-based approach for topological sorting
4. Return the topological ordering efficiently

**Visual Example:**
```
Optimized Kahn's for graph: 1→2→3, 1→3, 4→5
- Initialize in-degrees: [0, 0, 2, 0, 1]
- Queue: [1, 4] (nodes with in-degree 0)
- Process with optimized queue management
- Final ordering: [1, 4, 2, 5, 3]
```

**Implementation:**
```python
def topological_sorting_optimized_kahn(n, m, edges):
    # Build adjacency list and in-degrees
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm with optimized queue
    from collections import deque
    queue = deque()
    
    # Add all nodes with in-degree 0
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        # Update in-degrees of neighbors
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed
    if len(result) != n:
        return []  # Cycle exists
    
    return result

def solve_topological_sorting():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = topological_sorting_optimized_kahn(n, m, edges)
    if result:
        print(' '.join(map(str, result)))
    else:
        print("IMPOSSIBLE")

# Main execution
if __name__ == "__main__":
    solve_topological_sorting()
```

**Time Complexity:** O(n + m) for n nodes and m edges with optimized Kahn's algorithm
**Space Complexity:** O(n + m) for graph representation and queue

**Why it's optimal:**
- O(n + m) time complexity is optimal for topological sorting
- Uses optimized Kahn's algorithm with efficient queue management
- Most efficient approach for competitive programming
- Standard method for topological sorting problems

## 🎯 Problem Variations

### Variation 1: Topological Sorting with Cycle Detection
**Problem**: Find topological ordering and detect cycles in the graph.

**Link**: [CSES Problem Set - Topological Sorting Cycle Detection](https://cses.fi/problemset/task/topological_sorting_cycle_detection)

```python
def topological_sorting_cycle_detection(n, m, edges):
    # Build adjacency list and in-degrees
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm with cycle detection
    from collections import deque
    queue = deque()
    
    # Add all nodes with in-degree 0
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        # Update in-degrees of neighbors
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed
    if len(result) != n:
        return "IMPOSSIBLE"  # Cycle exists
    
    return ' '.join(map(str, result))
```

### Variation 2: Topological Sorting with Multiple Orderings
**Problem**: Find all possible topological orderings of the graph.

**Link**: [CSES Problem Set - Topological Sorting Multiple Orderings](https://cses.fi/problemset/task/topological_sorting_multiple_orderings)

```python
def topological_sorting_multiple_orderings(n, m, edges):
    # Build adjacency list and in-degrees
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Find all possible topological orderings
    def find_all_orderings(current_ordering, remaining_in_degree):
        if len(current_ordering) == n:
            return [current_ordering[:]]
        
        orderings = []
        for i in range(1, n + 1):
            if i not in current_ordering and remaining_in_degree[i] == 0:
                new_ordering = current_ordering + [i]
                new_in_degree = remaining_in_degree[:]
                
                # Update in-degrees
                for neighbor in adj[i]:
                    new_in_degree[neighbor] -= 1
                
                orderings.extend(find_all_orderings(new_ordering, new_in_degree))
        
        return orderings
    
    # Check if graph is a DAG
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    processed = 0
    while queue:
        current = queue.popleft()
        processed += 1
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if processed != n:
        return "IMPOSSIBLE"  # Cycle exists
    
    # Find all orderings
    all_orderings = find_all_orderings([], in_degree)
    return all_orderings
```

### Variation 3: Topological Sorting with Weights
**Problem**: Find topological ordering that minimizes total weight.

**Link**: [CSES Problem Set - Topological Sorting Weights](https://cses.fi/problemset/task/topological_sorting_weights)

```python
def topological_sorting_weights(n, m, edges, weights):
    # Build adjacency list and in-degrees
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm with weight consideration
    from collections import deque
    queue = deque()
    
    # Add all nodes with in-degree 0
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    total_weight = 0
    
    while queue:
        # Choose node with minimum weight
        current = min(queue, key=lambda x: weights[x])
        queue.remove(current)
        
        result.append(current)
        total_weight += weights[current]
        
        # Update in-degrees of neighbors
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed
    if len(result) != n:
        return "IMPOSSIBLE"  # Cycle exists
    
    return ' '.join(map(str, result))
```

## 🔗 Related Problems

- **[Cycle Finding](/cses-analyses/problem_soulutions/graph_algorithms/cycle_finding_analysis/)**: Cycle detection
- **[Building Teams](/cses-analyses/problem_soulutions/graph_algorithms/building_teams_analysis/)**: Graph coloring
- **[DAG Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: DAG problems
- **[Graph Ordering](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph ordering problems

## 📚 Learning Points

1. **Topological Sorting**: Essential for understanding DAG algorithms
2. **Kahn's Algorithm**: Key technique for topological sorting
3. **DFS-based Sorting**: Important for understanding graph traversal
4. **Cycle Detection**: Critical for understanding DAG properties
5. **Graph Ordering**: Foundation for many graph algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Topological Sorting problem demonstrates fundamental DAG ordering concepts for finding linear orderings that respect edge directions. We explored three approaches:

1. **Brute Force Permutation Check**: O(n! × m) time complexity using exponential permutation generation, inefficient for large n values
2. **Basic DFS-based Topological Sorting**: O(n + m) time complexity using standard DFS algorithm, better approach for topological sorting
3. **Optimized Kahn's Algorithm with Efficient Queue Management**: O(n + m) time complexity with optimized Kahn's algorithm, optimal approach for topological sorting

The key insights include understanding DAG properties, using Kahn's algorithm for efficient topological sorting, and applying DFS-based approaches for optimal performance. This problem serves as an excellent introduction to topological sorting algorithms and DAG ordering techniques.

