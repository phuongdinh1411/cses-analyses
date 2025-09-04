---
layout: simple
title: "Topological Sorting - Graph Ordering Algorithm"
permalink: /problem_soulutions/graph_algorithms/topological_sorting_analysis
---

# Topological Sorting - Graph Ordering Algorithm

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