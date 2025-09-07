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

## 📋 Problem Description

Given a directed acyclic graph (DAG) with n nodes and m edges, find a topological ordering of the nodes. A topological ordering is a linear ordering of vertices such that for every directed edge (u, v), vertex u comes before vertex v in the ordering.

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

## 🎯 Visual Example

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

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find linear ordering where all edges point forward
- **Key Insight**: Use DFS finish times or Kahn's algorithm (BFS-based)
- **Challenge**: Handle disconnected components and ensure DAG property

### Step 2: Brute Force Approach
**Try all possible orderings and check validity:**

```python
def topological_sorting_naive(n, m, edges):
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
```

**Complexity**: O(n! × m) - extremely slow for large graphs

### Step 3: Optimization
**Use DFS with finish times for efficient topological sorting:**

```python
def topological_sorting_dfs(n, m, edges):
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

def solve_topological_sorting():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = topological_sorting_dfs(n, m, edges)
    print(*result)

if __name__ == "__main__":
    solve_topological_sorting()
        if not visited[i]:
            dfs(i)
    
    return finish_order[::-1]
```

**Key Insight**: Process nodes in reverse order of DFS finish times

### Step 4: Complete Solution

```python
def solve_topological_sorting():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = topological_sorting_kahn(n, m, edges)
    if result:
        print(*result)
    else:
        print("IMPOSSIBLE")  # Cycle detected

def topological_sorting_kahn(n, m, edges):
    from collections import deque
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed
    if len(topo_order) == n:
        return topo_order
    else:
        return []  # Cycle detected

if __name__ == "__main__":
    solve_topological_sorting()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 4, [(1, 2), (2, 3), (1, 3), (4, 5)]), [1, 4, 2, 5, 3]),
        ((3, 2, [(1, 2), (2, 3)]), [1, 2, 3]),
        ((4, 3, [(1, 2), (2, 3), (3, 4)]), [1, 2, 3, 4]),
        ((2, 1, [(1, 2)]), [1, 2]),
        ((3, 0, []), [1, 2, 3]),  # No edges
    ]
    
    for (n, m, edges), expected in test_cases:
        result = topological_sorting_kahn(n, m, edges)
        print(f"n={n}, m={m}, edges={edges}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if len(result) == n else '✗ FAIL'}")
        print()

def topological_sorting_kahn(n, m, edges):
    from collections import deque
    
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(topo_order) == n:
        return topo_order
    else:
        return []

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - single pass through nodes and edges
- **Space**: O(n + m) - adjacency list and in-degree arrays

### Why This Solution Works
- **Kahn's Algorithm**: Processes nodes with zero in-degree first
- **DAG Property**: Ensures no cycles exist in the graph
- **Queue Management**: Maintains nodes ready for processing
- **Optimal Algorithm**: Best known approach for topological sorting

## 🎨 Visual Example

### Input Example
```
5 nodes, 4 edges:
Edge 1: 1 → 2
Edge 2: 2 → 3
Edge 3: 1 → 3
Edge 4: 4 → 5
```

### Graph Visualization
```
Nodes: 1, 2, 3, 4, 5
Edges: (1→2), (2→3), (1→3), (4→5)

    1 ──→ 2 ──→ 3
    │     │
    └─────┘
    
    4 ──→ 5
```

### In-Degree Calculation
```
Node 1: 0 incoming edges (in-degree = 0)
Node 2: 1 incoming edge from 1 (in-degree = 1)
Node 3: 2 incoming edges from 1,2 (in-degree = 2)
Node 4: 0 incoming edges (in-degree = 0)
Node 5: 1 incoming edge from 4 (in-degree = 1)

In-degree array: [0, 1, 2, 0, 1]
```

### Kahn's Algorithm Process
```
Step 1: Initialize
- Queue: [1, 4] (nodes with in-degree 0)
- Result: []
- In-degrees: [0, 1, 2, 0, 1]

Step 2: Process Node 1
- Remove 1 from queue
- Add 1 to result: [1]
- Update neighbors: 2, 3
  - Node 2: in-degree 1 → 0, add to queue
  - Node 3: in-degree 2 → 1
- Queue: [4, 2]
- In-degrees: [0, 0, 1, 0, 1]

Step 3: Process Node 4
- Remove 4 from queue
- Add 4 to result: [1, 4]
- Update neighbors: 5
  - Node 5: in-degree 1 → 0, add to queue
- Queue: [2, 5]
- In-degrees: [0, 0, 1, 0, 0]

Step 4: Process Node 2
- Remove 2 from queue
- Add 2 to result: [1, 4, 2]
- Update neighbors: 3
  - Node 3: in-degree 1 → 0, add to queue
- Queue: [5, 3]
- In-degrees: [0, 0, 0, 0, 0]

Step 5: Process Node 5
- Remove 5 from queue
- Add 5 to result: [1, 4, 2, 5]
- No neighbors to update
- Queue: [3]

Step 6: Process Node 3
- Remove 3 from queue
- Add 3 to result: [1, 4, 2, 5, 3]
- No neighbors to update
- Queue: []

Final result: [1, 4, 2, 5, 3]
```

### DFS Alternative (Finish Times)
```
Step 1: DFS from Node 1
- Visit 1, explore neighbors: 2, 3
- DFS from 2, explore neighbors: 3
- DFS from 3, no neighbors, finish time = 1
- Back to 2, finish time = 2
- Back to 1, finish time = 3

Step 2: DFS from Node 4
- Visit 4, explore neighbors: 5
- DFS from 5, no neighbors, finish time = 4
- Back to 4, finish time = 5

Finish times: [3, 2, 1, 5, 4]
Reverse order: [4, 5, 1, 2, 3] → [1, 4, 2, 5, 3]
```

### Valid Ordering Verification
```
Check if all edges point forward in ordering [1, 4, 2, 5, 3]:

Edge 1→2: 1 comes before 2 ✓
Edge 2→3: 2 comes before 3 ✓
Edge 1→3: 1 comes before 3 ✓
Edge 4→5: 4 comes before 5 ✓

All edges point forward - valid topological ordering!
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Kahn's Algorithm│ O(n + m)     │ O(n + m)     │ In-degree    │
│                 │              │              │ tracking     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DFS with Finish │ O(n + m)     │ O(n + m)     │ Finish times │
│ Times           │              │              │ ordering     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DFS Recursive   │ O(n + m)     │ O(n)         │ Recursive    │
│                 │              │              │ traversal    │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## Key Insights

### 1. **Topological Ordering Property**
- **Forward Edge Constraint**: All edges must point forward in the ordering
- **Dependency Satisfaction**: Ensures all dependency relationships are satisfied
- **Linear Ordering**: Creates a valid linear sequence of nodes
- **DAG Requirement**: Only works on directed acyclic graphs

### 2. **In-Degree Tracking Strategy**
- **Incoming Edge Count**: Track the number of incoming edges for each node
- **Zero In-Degree Priority**: Process nodes with zero in-degree first
- **Queue Management**: Maintain a queue of nodes ready for processing
- **Dynamic Updates**: Update in-degrees as nodes are processed

### 3. **Cycle Detection Mechanism**
- **Processing Count**: If not all nodes are processed, a cycle exists
- **Natural Detection**: Kahn's algorithm naturally detects cycles
- **Validation**: Provides a way to validate DAG properties
- **Error Handling**: Returns empty result when cycles are detected

## 🎯 Problem Variations

### Variation 1: Topological Sorting with Cycle Detection
**Problem**: Detect if a cycle exists in the graph and find topological order if possible.

```python
def topological_sorting_with_cycle_detection(n, m, edges):
    from collections import deque
    
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    processed = 0
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        processed += 1
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if processed == n:
        return topo_order, False  # No cycle
    else:
        return [], True  # Cycle detected

# Example usage
result, has_cycle = topological_sorting_with_cycle_detection(5, 4, [(1, 2), (2, 3), (1, 3), (4, 5)])
if has_cycle:
    print("Cycle detected!")
else:
    print(f"Topological order: {result}")
```

### Variation 2: Topological Sorting with Multiple Valid Orders
**Problem**: Find all possible topological orderings of the graph.

```python
def find_all_topological_orderings(n, m, edges):
    from collections import deque
    import copy
    
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    def backtrack(current_order, remaining_in_degree, available_nodes):
        if len(current_order) == n:
            return [current_order[:]]
        
        results = []
        for node in available_nodes:
            if remaining_in_degree[node] == 0:
                # Choose this node
                current_order.append(node)
                new_available = available_nodes.copy()
                new_available.remove(node)
                
                # Update in-degrees
                new_in_degree = remaining_in_degree.copy()
                for neighbor in adj[node]:
                    new_in_degree[neighbor] -= 1
                    if new_in_degree[neighbor] == 0:
                        new_available.add(neighbor)
                
                # Recurse
                results.extend(backtrack(current_order, new_in_degree, new_available))
                
                # Backtrack
                current_order.pop()
        
        return results
    
    # Find initial available nodes
    available = set()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            available.add(i)
    
    return backtrack([], in_degree, available)

# Example usage
all_orders = find_all_topological_orderings(5, 4, [(1, 2), (2, 3), (1, 3), (4, 5)])
print(f"Found {len(all_orders)} valid orderings:")
for order in all_orders:
    print(order)
```

### Variation 3: Topological Sorting with Weights
**Problem**: Find topological ordering that minimizes total weight of edges pointing backward.

```python
def topological_sorting_minimize_backward_edges(n, m, edges, weights):
    from collections import deque
    import heapq
    
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, weights[i]))
        in_degree[b] += 1
    
    # Use priority queue to process nodes with higher out-degree first
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            # Priority based on out-degree (higher first)
            heapq.heappush(queue, (-len(adj[i]), i))
    
    topo_order = []
    
    while queue:
        _, node = heapq.heappop(queue)
        topo_order.append(node)
        
        for neighbor, weight in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(queue, (-len(adj[neighbor]), neighbor))
    
    return topo_order

# Example usage
edges = [(1, 2), (2, 3), (1, 3), (4, 5)]
weights = [1, 2, 3, 4]
result = topological_sorting_minimize_backward_edges(5, 4, edges, weights)
print(f"Optimized topological order: {result}")
```

### Variation 4: Topological Sorting with Constraints
**Problem**: Find topological ordering that satisfies additional constraints (e.g., certain nodes must come first/last).

```python
def topological_sorting_with_constraints(n, m, edges, first_nodes, last_nodes):
    from collections import deque
    
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Process first nodes first
    queue = deque()
    topo_order = []
    
    # Add first nodes to queue
    for node in first_nodes:
        if in_degree[node] == 0:
            queue.append(node)
            topo_order.append(node)
    
    # Process remaining nodes
    for i in range(1, n + 1):
        if i not in first_nodes and i not in last_nodes and in_degree[i] == 0:
            queue.append(i)
    
    while queue:
        node = queue.popleft()
        if node not in topo_order:
            topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0 and neighbor not in last_nodes:
                queue.append(neighbor)
    
    # Add last nodes at the end
    for node in last_nodes:
        if node not in topo_order:
            topo_order.append(node)
    
    return topo_order

# Example usage
first_nodes = [1, 4]
last_nodes = [3, 5]
result = topological_sorting_with_constraints(5, 4, [(1, 2), (2, 3), (1, 3), (4, 5)], first_nodes, last_nodes)
print(f"Constrained topological order: {result}")
```

### Variation 5: Topological Sorting with Dynamic Updates
**Problem**: Maintain topological ordering as edges are added/removed dynamically.

```python
class DynamicTopologicalSorter:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.in_degree = [0] * (n + 1)
        self.topo_order = list(range(1, n + 1))
    
    def add_edge(self, a, b):
        """Add edge from a to b and update topological order"""
        self.adj[a].append(b)
        self.in_degree[b] += 1
        
        # Check if this creates a cycle
        if self.has_cycle():
            # Remove the edge
            self.adj[a].pop()
            self.in_degree[b] -= 1
            return False
        
        # Update topological order
        self.update_topological_order()
        return True
    
    def remove_edge(self, a, b):
        """Remove edge from a to b and update topological order"""
        if b in self.adj[a]:
            self.adj[a].remove(b)
            self.in_degree[b] -= 1
            self.update_topological_order()
            return True
        return False
    
    def has_cycle(self):
        """Check if graph has a cycle using DFS"""
        visited = [False] * (self.n + 1)
        rec_stack = [False] * (self.n + 1)
        
        def dfs(node):
            visited[node] = True
            rec_stack[node] = True
            
            for neighbor in self.adj[node]:
                if not visited[neighbor]:
                    if dfs(neighbor):
                        return True
                elif rec_stack[neighbor]:
                    return True
            
            rec_stack[node] = False
            return False
        
        for i in range(1, self.n + 1):
            if not visited[i]:
                if dfs(i):
                    return True
        return False
    
    def update_topological_order(self):
        """Update topological ordering using Kahn's algorithm"""
        from collections import deque
        
        temp_in_degree = self.in_degree.copy()
        queue = deque()
        
        for i in range(1, self.n + 1):
            if temp_in_degree[i] == 0:
                queue.append(i)
        
        self.topo_order = []
        
        while queue:
            node = queue.popleft()
            self.topo_order.append(node)
            
            for neighbor in self.adj[node]:
                temp_in_degree[neighbor] -= 1
                if temp_in_degree[neighbor] == 0:
                    queue.append(neighbor)
    
    def get_topological_order(self):
        """Get current topological ordering"""
        return self.topo_order

# Example usage
sorter = DynamicTopologicalSorter(5)
print(f"Initial order: {sorter.get_topological_order()}")

sorter.add_edge(1, 2)
print(f"After adding edge (1,2): {sorter.get_topological_order()}")

sorter.add_edge(2, 3)
print(f"After adding edge (2,3): {sorter.get_topological_order()}")

sorter.add_edge(1, 3)
print(f"After adding edge (1,3): {sorter.get_topological_order()}")
```

## 🔗 Related Problems

- **[Strongly Connected Components](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph connectivity problems
- **[Cycle Finding](/cses-analyses/problem_soulutions/graph_algorithms/)**: Cycle detection problems
- **[Building Teams](/cses-analyses/problem_soulutions/graph_algorithms/)**: Bipartite graph problems

## 📚 Learning Points

1. **Topological Ordering**: Essential for dependency resolution and scheduling
2. **Kahn's Algorithm**: Important BFS-based approach for topological sorting
3. **DFS Finish Times**: Alternative approach using depth-first search
4. **Cycle Detection**: Key for validating DAG properties
5. **Dynamic Updates**: Important for maintaining ordering as graph changes

---

**This is a great introduction to topological sorting and graph ordering algorithms!** 🎯 