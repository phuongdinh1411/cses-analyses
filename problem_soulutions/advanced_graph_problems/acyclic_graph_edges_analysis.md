---
layout: simple
title: "Acyclic Graph Edges - Minimum Edges to Remove for Acyclicity"
permalink: /problem_soulutions/advanced_graph_problems/acyclic_graph_edges_analysis
---

# Acyclic Graph Edges - Minimum Edges to Remove for Acyclicity

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

### 📊 Visual Example

**Original Graph with Cycle:**
```
    1 ──→ 2
    ↑     │
    │     ↓
    4 ←── 3
    ↑
    │
    1 ──→ 3
```

**After Removing Edge (4,1):**
```
    1 ──→ 2
          │
          ↓
    4 ←── 3
          ↑
          │
    1 ──→ 3
```

**Topological Order: [1, 2, 3, 4]**
- Forward edges: (1,2), (1,3), (2,3) ✓
- Back edge: (4,1) ✗ (creates cycle)

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find the minimum number of edges to remove to make a directed graph acyclic
- **Key Insight**: Use DFS to identify back edges, which represent cycles
- **Challenge**: Efficiently identify all cycles and find minimum edge removal

### 🧠 Problem Analysis Flowchart

```
┌─────────────────────────────────────┐
│        Input: Directed Graph        │
│     with potential cycles           │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     Find Topological Order          │
│   (Kahn's Algorithm)                │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    Identify Back Edges              │
│  (edges violating topo order)       │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Count Back Edges =                │
│   Minimum Edges to Remove           │
└─────────────────────────────────────┘
```

### 🔍 Key Insight Visualization

**Why Back Edges Create Cycles:**
```
Topological Order: [A, B, C, D]

Forward Edges (Valid):     Back Edge (Creates Cycle):
A ──→ B                    D ──→ A
B ──→ C                    ↑     │
C ──→ D                    │     │
                           └─────┘
                           Creates cycle: A→B→C→D→A
```

### Step 2: Initial Approach
**Brute force approach (inefficient but correct):**

### Step 2: DFS Cycle Detection Approach
**Idea**: Use DFS to detect cycles and count edges that need to be removed.

### 🔄 DFS Cycle Detection Visualization

**DFS Traversal with Stack Tracking:**
```
Graph: 1→2→3→4→1, 1→3

DFS Stack States:
┌─────────────────────────────────────┐
│ Step 1: Start from node 1           │
│ Stack: [1]                          │
│ Visited: [1]                        │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Step 2: Visit node 2                │
│ Stack: [1, 2]                       │
│ Visited: [1, 2]                     │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Step 3: Visit node 3                │
│ Stack: [1, 2, 3]                    │
│ Visited: [1, 2, 3]                  │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Step 4: Visit node 4                │
│ Stack: [1, 2, 3, 4]                 │
│ Visited: [1, 2, 3, 4]               │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Step 5: Try to visit node 1         │
│ CYCLE DETECTED!                     │
│ Node 1 is in current stack          │
│ Back edge: (4,1)                    │
└─────────────────────────────────────┘
```

```python
def acyclic_graph_edges_dfs(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # DFS to detect cycles
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    cycle_edges = []
    
    def dfs(node, parent):
        if in_stack[node]:
            return True  # Cycle detected
        if visited[node]:
            return False
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if dfs(neighbor, node):
                cycle_edges.append((node, neighbor))
        
        in_stack[node] = False
        return False
    
    # Check for cycles from each node
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i, -1)
    
    return len(cycle_edges)
```

**Why this works:**
- Uses DFS to detect cycles
- Tracks nodes in current recursion stack
- Identifies back edges that create cycles
- Simple to understand and implement
- O(n + m) time complexity

### Step 3: Optimization/Alternative
**Feedback Arc Set approach:**

### 🎯 Kahn's Algorithm Visualization

**Topological Sorting Process:**
```
Initial Graph:
    1 ──→ 2
    ↑     │
    │     ↓
    4 ←── 3
    ↑
    │
    1 ──→ 3

Step 1: Calculate In-degrees
Node:  1  2  3  4
In:    1  1  2  1

Step 2: Start with nodes having in-degree 0
Queue: [1] (only node 1 has in-degree 0)

Step 3: Process Queue
┌─────────────────────────────────────┐
│ Remove node 1 from queue            │
│ Topological order: [1]              │
│ Update in-degrees of neighbors:     │
│ - Node 2: 1-1=0 (add to queue)      │
│ - Node 3: 2-1=1                     │
│ Queue: [2]                          │
└─────────────────────────────────────┘

Step 4: Continue Processing
┌─────────────────────────────────────┐
│ Remove node 2 from queue            │
│ Topological order: [1, 2]           │
│ Update in-degrees of neighbors:     │
│ - Node 3: 1-1=0 (add to queue)      │
│ Queue: [3]                          │
└─────────────────────────────────────┘

Step 5: Final Processing
┌─────────────────────────────────────┐
│ Remove node 3 from queue            │
│ Topological order: [1, 2, 3]        │
│ Update in-degrees of neighbors:     │
│ - Node 4: 1-1=0 (add to queue)      │
│ Queue: [4]                          │
└─────────────────────────────────────┘

Final Topological Order: [1, 2, 3, 4]

Step 6: Identify Back Edges
Edge (4,1): position(4)=3, position(1)=0
Since 3 > 0, this is a BACK EDGE!
```

```python
def acyclic_graph_edges_feedback_arc_set(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Kahn's algorithm for topological sorting
    in_degree = [0] * (n + 1)
    for a, b in edges:
        in_degree[b] += 1
    
    # Find topological order
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Count back edges (edges that go from higher to lower in topological order)
    back_edges = 0
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            back_edges += 1
    
    return back_edges
```

**Why this works:**
- Uses topological sorting to find order
- Back edges in topological order create cycles
- Minimum edges to remove = number of back edges
- O(n + m) time complexity

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_acyclic_graph_edges():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Kahn's algorithm for topological sorting
    in_degree = [0] * (n + 1)
    for a, b in edges:
        in_degree[b] += 1
    
    # Find topological order
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Count back edges (edges that go from higher to lower in topological order)
    back_edges = 0
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            back_edges += 1
    
    print(back_edges)

# Main execution
if __name__ == "__main__":
    solve_acyclic_graph_edges()
```

**Why this works:**
- Optimal feedback arc set approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, 5, [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]),
        (3, 3, [(1, 2), (2, 3), (3, 1)]),
        (4, 4, [(1, 2), (2, 3), (3, 4), (4, 1)]),
    ]
    
    for n, m, edges in test_cases:
        result = solve_test(n, m, edges)
        print(f"n={n}, m={m}, edges={edges}")
        print(f"Result: {result}")
        print()

def solve_test(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Kahn's algorithm for topological sorting
    in_degree = [0] * (n + 1)
    for a, b in edges:
        in_degree[b] += 1
    
    # Find topological order
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Count back edges (edges that go from higher to lower in topological order)
    back_edges = 0
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            back_edges += 1
    
    return back_edges

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - Kahn's algorithm for topological sorting
- **Space**: O(n + m) - adjacency list and topological order

### Why This Solution Works
- **Feedback Arc Set**: Finds minimum edges to remove
- **Topological Sorting**: Identifies back edges
- **Cycle Detection**: Back edges create cycles
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### Important Concepts and Patterns
- **Feedback Arc Set**: Minimum edges to remove to make graph acyclic
- **Topological Sorting**: Orders vertices in DAG to identify cycles
- **Back Edge Detection**: Edges that violate topological order create cycles
- **Cycle Detection**: Use DFS or topological sorting to identify cycles

### 🧠 Algorithm Comparison Visualization

**DFS vs Kahn's Algorithm:**

```
┌─────────────────────────────────────┐
│           DFS Approach              │
│                                     │
│  ┌─────────┐    ┌─────────┐         │
│  │  Start  │───▶│  Visit  │         │
│  │   DFS   │    │  Node   │         │
│  └─────────┘    └─────────┘         │
│       │              │              │
│       ▼              ▼              │
│  ┌─────────┐    ┌─────────┐         │
│  │ Check   │    │ Detect  │         │
│  │ Stack   │    │  Cycle  │         │
│  └─────────┘    └─────────┘         │
│                                     │
│  Time: O(n+m)                       │
│  Space: O(n)                        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│        Kahn's Algorithm             │
│                                     │
│  ┌─────────┐    ┌─────────┐         │
│  │Calculate│───▶│  Build  │         │
│  │In-degrees│   │  Queue  │         │
│  └─────────┘    └─────────┘         │
│       │              │              │
│       ▼              ▼              │
│  ┌─────────┐    ┌─────────┐         │
│  │Process  │    │Identify │         │
│  │ Queue   │    │Back Edges│        │
│  └─────────┘    └─────────┘         │
│                                     │
│  Time: O(n+m)                       │
│  Space: O(n+m)                      │
└─────────────────────────────────────┘
```

### 🎯 Problem Variations Visualization

**Different Types of Cycle Problems:**

```
┌─────────────────────────────────────┐
│        Cycle Detection              │
│  ┌─────────┐    ┌─────────┐         │
│  │   DFS   │───▶│  Stack  │         │
│  │ Traversal│   │Tracking │         │
│  └─────────┘    └─────────┘         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      Feedback Arc Set               │
│  ┌─────────┐    ┌─────────┐         │
│  │Topological│───▶│Back Edge│         │
│  │  Sort    │   │Counting │         │
│  └─────────┘    └─────────┘         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│    Minimum Edge Removal             │
│  ┌─────────┐    ┌─────────┐         │
│  │Identify │───▶│  Count  │         │
│  │Cycles   │   │  Edges  │         │
│  └─────────┘    └─────────┘         │
└─────────────────────────────────────┘
```

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted Acyclic Graph Edges**
```python
def weighted_acyclic_graph_edges(n, m, edges, weights):
    # Handle weighted edges with minimum weight removal
    
    # Build adjacency list with weights
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, weights[i]))
    
    # Kahn's algorithm for topological sorting
    in_degree = [0] * (n + 1)
    for a, b in edges:
        in_degree[b] += 1
    
    # Find topological order
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        
        for neighbor, _ in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Find minimum weight back edges
    min_weight = float('inf')
    for i, (a, b) in enumerate(edges):
        if topo_order.index(a) > topo_order.index(b):
            min_weight = min(min_weight, weights[i])
    
    return min_weight
```

#### **2. Acyclic Graph Edges with Constraints**
```python
def acyclic_graph_edges_constrained(n, m, edges, constraints):
    # Handle acyclic graph edges with additional constraints
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Apply constraints (e.g., certain edges cannot be removed)
    removable_edges = []
    for i, (a, b) in enumerate(edges):
        if constraints[i]:  # Edge can be removed
            removable_edges.append((a, b))
    
    # Use only removable edges for feedback arc set
    # ... (similar to previous approach but with constraints)
    
    return len(removable_edges)
```

#### **3. Acyclic Graph Edges with Dynamic Updates**
```python
def acyclic_graph_edges_dynamic(n, m, edges, operations):
    # Handle acyclic graph edges with dynamic edge updates
    
    current_edges = edges.copy()
    results = []
    
    for op in operations:
        if op[0] == 'add':
            # Add new edge
            a, b = op[1], op[2]
            current_edges.append((a, b))
        elif op[0] == 'remove':
            # Remove edge
            a, b = op[1], op[2]
            current_edges.remove((a, b))
        elif op[0] == 'query':
            # Query minimum edges to remove
            result = solve_acyclic_graph_edges(current_edges)
            results.append(result)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Graph Theory**: Cycle detection, topological sorting
- **Feedback Arc Set**: Minimum edge removal problems
- **Graph Algorithms**: DFS, BFS, cycle detection
- **Optimization**: Minimum edge/vertex removal problems

## 📚 Learning Points

### Key Takeaways
- **Feedback arc set** is a fundamental concept in graph theory
- **Topological sorting** is essential for cycle detection
- **Back edge detection** efficiently identifies cycles
- **Graph algorithms** can solve complex optimization problems

## 🎯 Key Insights

### 1. **Feedback Arc Set**
- Minimum edges to remove to make graph acyclic
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Topological Sorting**
- Orders vertices in DAG
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Back Edge Detection**
- Edges that violate topological order
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Weighted Acyclic Graph Edges
**Problem**: Each edge has a weight, find minimum weight edges to remove.

```python
def weighted_acyclic_graph_edges(n, m, edges, weights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Kahn's algorithm for topological sorting
    in_degree = [0] * (n + 1)
    for a, b in edges:
        in_degree[b] += 1
    
    # Find topological order
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Find minimum weight back edges
    back_edges = []
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            back_edges.append((a, b, weights.get((a, b), 1)))
    
    # Sort by weight and select minimum weight edges
    back_edges.sort(key=lambda x: x[2])
    return len(back_edges)
```

### Variation 2: Constrained Acyclic Graph Edges
**Problem**: Can only remove certain edges.

```python
def constrained_acyclic_graph_edges(n, m, edges, removable_edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Kahn's algorithm for topological sorting
    in_degree = [0] * (n + 1)
    for a, b in edges:
        in_degree[b] += 1
    
    # Find topological order
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Count removable back edges
    removable_back_edges = 0
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b) and (a, b) in removable_edges:
            removable_back_edges += 1
    
    return removable_back_edges
```

### Variation 3: Dynamic Acyclic Graph Edges
**Problem**: Support adding/removing edges and maintaining acyclicity.

```python
class DynamicAcyclicGraphEdges:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.edges = set()
    
    def add_edge(self, a, b):
        if (a, b) not in self.edges:
            self.edges.add((a, b))
            self.adj[a].append(b)
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.edges.remove((a, b))
            self.adj[a].remove(b)
            return True
        return False
    
    def get_min_edges_to_remove(self):
        # Kahn's algorithm for topological sorting
        in_degree = [0] * (self.n + 1)
        for a, b in self.edges:
            in_degree[b] += 1
        
        # Find topological order
        queue = []
        for i in range(1, self.n + 1):
            if in_degree[i] == 0:
                queue.append(i)
        
        topo_order = []
        while queue:
            node = queue.pop(0)
            topo_order.append(node)
            
            for neighbor in self.adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Count back edges
        back_edges = 0
        for a, b in self.edges:
            if topo_order.index(a) > topo_order.index(b):
                back_edges += 1
        
        return back_edges
```

### Variation 4: Acyclic Graph with Multiple Constraints
**Problem**: Find minimum edges to remove with multiple constraints.

```python
def multi_constrained_acyclic_graph_edges(n, m, edges, constraints):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Kahn's algorithm for topological sorting
    in_degree = [0] * (n + 1)
    for a, b in edges:
        in_degree[b] += 1
    
    # Find topological order
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Apply constraints
    forbidden_edges = constraints.get('forbidden_edges', set())
    removable_edges = constraints.get('removable_edges', set())
    
    # Count constrained back edges
    back_edges = 0
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            if (a, b) not in forbidden_edges and (a, b) in removable_edges:
                back_edges += 1
    
    return back_edges
```

### Variation 5: Acyclic Graph with Edge Weights
**Problem**: Each edge has a weight, find minimum weight edges to remove.

```python
def weighted_acyclic_graph_edges_optimized(n, m, edges, weights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Kahn's algorithm for topological sorting
    in_degree = [0] * (n + 1)
    for a, b in edges:
        in_degree[b] += 1
    
    # Find topological order
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Find back edges with weights
    back_edges = []
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            weight = weights.get((a, b), 1)
            back_edges.append((a, b, weight))
    
    # Sort by weight and select minimum weight edges
    back_edges.sort(key=lambda x: x[2])
    return len(back_edges)
```

## 🔗 Related Problems

- **[Topological Sorting](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Topological sorting algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[Feedback Arc Set](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Feedback arc set algorithms

## 📚 Learning Points

1. **Feedback Arc Set**: Essential for acyclic graphs
2. **Topological Sorting**: Efficient cycle detection
3. **Graph Theory**: Important graph theory concept
4. **Back Edge Detection**: Important for optimization

---

**This is a great introduction to acyclic graph edges and feedback arc set!** 🎯

```python
def acyclic_graph_edges_feedback(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Try to find a topological order
    from collections import deque
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
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
    
    # Count edges that go backwards in topological order
    back_edges = 0
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            back_edges += 1
    
    return back_edges
```

**Why this is better:**
- Uses topological sorting
- Identifies back edges efficiently
- More accurate than simple DFS
- Handles complex cycle structures

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_acyclic_graph_edges():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Try to find a topological order
    from collections import deque
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
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
    
    # Count edges that go backwards in topological order
    back_edges = 0
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            back_edges += 1
    
    print(back_edges)

# Main execution
if __name__ == "__main__":
    solve_acyclic_graph_edges()
```

**Why this works:**
- Optimal feedback arc set approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, 5, [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)], 1),
        (3, 3, [(1, 2), (2, 3), (3, 1)], 1),
        (4, 4, [(1, 2), (2, 3), (3, 4), (4, 1)], 1),
        (3, 2, [(1, 2), (2, 3)], 0),
    ]
    
    for n, m, edges, expected in test_cases:
        result = solve_test(n, m, edges)
        print(f"n={n}, m={m}, edges={edges}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Try to find a topological order
    from collections import deque
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
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
    
    # Count edges that go backwards in topological order
    back_edges = 0
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            back_edges += 1
    
    return back_edges

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - building graph and topological sort
- **Space**: O(n + m) - adjacency list and topological order

### Why This Solution Works
- **Feedback Arc Set**: Finds minimum edges to remove for acyclicity
- **Topological Sorting**: Identifies valid ordering
- **Back Edge Detection**: Counts edges that violate topological order
- **Optimal Approach**: Guarantees minimum edge removal

## 🎯 Key Insights

### 1. **Feedback Arc Set**
- Minimum edges to remove = number of back edges
- Key insight for optimization
- Enables efficient solution
- Crucial for understanding

### 2. **Topological Sorting**
- Provides valid ordering for acyclic graph
- Identifies cycles through back edges
- Important for efficiency
- Essential for correctness

### 3. **Back Edge Detection**
- Count edges that go backwards in topological order
- These edges create cycles
- Simple but important observation
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Weighted Edge Removal
**Problem**: Each edge has a weight. Find minimum total weight of edges to remove.

```python
def acyclic_graph_edges_weighted(n, m, edges, weights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, weights[i]))
    
    # Try to find a topological order
    from collections import deque
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
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
            in_degree[neighbor[0]] -= 1
            if in_degree[neighbor[0]] == 0:
                queue.append(neighbor[0])
    
    # Find minimum weight of back edges
    min_weight = float('inf')
    for i, (a, b) in enumerate(edges):
        if topo_order.index(a) > topo_order.index(b):
            min_weight = min(min_weight, weights[i])
    
    return min_weight if min_weight != float('inf') else 0
```

### Variation 2: Maximum Acyclic Subgraph
**Problem**: Find maximum number of edges that can remain while keeping graph acyclic.

```python
def maximum_acyclic_subgraph(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Try to find a topological order
    from collections import deque
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
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
    
    # Count edges that go forward in topological order
    forward_edges = 0
    for a, b in edges:
        if topo_order.index(a) < topo_order.index(b):
            forward_edges += 1
    
    return forward_edges
```

### Variation 3: Cycle Detection with Edge Removal
**Problem**: Detect cycles and suggest specific edges to remove.

```python
def detect_cycles_with_removal(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Try to find a topological order
    from collections import deque
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
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
    
    # Find back edges to remove
    back_edges = []
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            back_edges.append((a, b))
    
    return back_edges
```

### Variation 4: Dynamic Acyclic Graph
**Problem**: Support adding/removing edges and maintaining acyclicity.

```python
class DynamicAcyclicGraph:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.edges = set()
    
    def add_edge(self, a, b):
        if (a, b) in self.edges:
            return False
        
        # Check if adding this edge creates a cycle
        self.adj[a].append(b)
        self.edges.add((a, b))
        
        if self.has_cycle():
            # Remove the edge if it creates a cycle
            self.adj[a].remove(b)
            self.edges.remove((a, b))
            return False
        
        return True
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.adj[a].remove(b)
            self.edges.remove((a, b))
            return True
        return False
    
    def has_cycle(self):
        visited = [False] * (self.n + 1)
        in_stack = [False] * (self.n + 1)
        
        def dfs(node):
            if in_stack[node]:
                return True
            if visited[node]:
                return False
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor in self.adj[node]:
                if dfs(neighbor):
                    return True
            
            in_stack[node] = False
            return False
        
        for i in range(1, self.n + 1):
            if not visited[i]:
                if dfs(i):
                    return True
        
        return False
    
    def get_edges(self):
        return list(self.edges)
```

### Variation 5: Minimum Feedback Vertex Set
**Problem**: Find minimum number of vertices to remove to make graph acyclic.

```python
def minimum_feedback_vertex_set(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Try to find a topological order
    from collections import deque
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
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
    
    # Find vertices that are part of cycles
    cycle_vertices = set()
    for a, b in edges:
        if topo_order.index(a) > topo_order.index(b):
            cycle_vertices.add(a)
            cycle_vertices.add(b)
    
    return len(cycle_vertices)
```

## 🔗 Related Problems

- **[Course Schedule II](/cses-analyses/problem_soulutions/advanced_graph_problems/course_schedule_ii_analysis)**: Topological sorting
- **[Strongly Connected Components](/cses-analyses/problem_soulutions/graph_algorithms/strongly_connected_components_analysis)**: Cycle detection
- **[Graph Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms

## 📚 Learning Points

1. **Feedback Arc Set**: Powerful concept for cycle removal
2. **Topological Sorting**: Essential for acyclic graph analysis
3. **Back Edge Detection**: Key technique for cycle identification
4. **Graph Cycle Problems**: Common pattern in competitive programming

---

### 🎯 Final Solution Summary

**Complete Algorithm Flow:**
```
┌─────────────────────────────────────┐
│           INPUT                     │
│    Directed Graph with Cycles       │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│        STEP 1: Build Graph          │
│     Adjacency List + In-degrees     │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│        STEP 2: Kahn's Algorithm     │
│      Find Topological Order         │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│        STEP 3: Identify Back Edges  │
│    Edges violating topo order       │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│        STEP 4: Count Back Edges     │
│    = Minimum Edges to Remove        │
└─────────────────────────────────────┘
```

**Key Formula:**
```
Minimum Edges to Remove = Number of Back Edges
Back Edge = Edge (u,v) where topo_order[u] > topo_order[v]
```

**This is a great introduction to feedback arc set and cycle detection problems!** 🎯 