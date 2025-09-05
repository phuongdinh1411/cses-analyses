---
layout: simple
title: "Graph Girth - Shortest Cycle Length in Undirected Graph"
permalink: /problem_soulutions/advanced_graph_problems/graph_girth_analysis
---

# Graph Girth - Shortest Cycle Length in Undirected Graph

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand the concept of graph girth and cycle detection in undirected graphs
- [ ] **Objective 2**: Apply BFS-based cycle detection algorithms to find shortest cycles
- [ ] **Objective 3**: Implement efficient cycle detection using parent tracking in BFS
- [ ] **Objective 4**: Optimize cycle detection by avoiding redundant searches
- [ ] **Objective 5**: Handle edge cases in cycle detection (trees, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: BFS, DFS, cycle detection, graph traversal
- **Data Structures**: Adjacency lists, queues, visited arrays, parent arrays
- **Mathematical Concepts**: Graph theory, cycle properties, shortest path concepts
- **Programming Skills**: BFS implementation, graph representation, queue operations
- **Related Problems**: Round Trip (cycle detection), Message Route (BFS), Building Roads (connectivity)

## 📋 Problem Description

Given an undirected graph, find the length of the shortest cycle (girth).

This is a classic graph theory problem that requires finding the shortest cycle in an undirected graph. The solution involves using BFS from each vertex to detect cycles and find the minimum cycle length.

**Input**: 
- n: number of vertices
- m: number of edges
- m lines: a b (edge between vertices a and b)

**Output**: 
- Length of the shortest cycle, or -1 if no cycle exists

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ m ≤ 2000
- 1 ≤ a, b ≤ n

**Example**:
```
Input:
4 4
1 2
2 3
3 4
4 1

Output:
4

Explanation**: 
The shortest cycle is 1 → 2 → 3 → 4 → 1 with length 4.
```

### 📊 Visual Example

**Input Graph:**
```
    1 ──── 2
    │      │
    │      │
    4 ──── 3
```

**Cycle Detection:**
```
Cycle: 1 → 2 → 3 → 4 → 1
Length: 4 edges
```

**BFS from Node 1:**
```
Level 0: [1]
Level 1: [2, 4]  
Level 2: [3, 3]  ← Cycle detected!
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find the shortest cycle length (girth) in an undirected graph
- **Key Insight**: Use BFS from each vertex to detect cycles and find minimum length
- **Challenge**: Efficiently detect cycles and find the shortest one

### 🧠 Problem Analysis Flowchart

```
┌─────────────────────────────────────┐
│        Input: Undirected Graph      │
│     with potential cycles           │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     BFS from Each Vertex            │
│   (Cycle Detection)                 │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    Track Parent and Distance        │
│  (Avoid revisiting parent)          │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Detect Cross Edges                │
│  (Edges to visited nodes)           │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Calculate Cycle Length            │
│   = distance[u] + distance[v] + 1   │
└─────────────────────────────────────┘
```

### 🔍 BFS Cycle Detection Visualization

**BFS Tree Construction:**
```
Graph: 1-2-3-4-1

BFS from Node 1:
┌─────────────────────────────────────┐
│ Level 0: [1]                        │
│ Parent: {1: None}                   │
│ Distance: {1: 0}                    │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Level 1: [2, 4]                     │
│ Parent: {1: None, 2: 1, 4: 1}      │
│ Distance: {1: 0, 2: 1, 4: 1}       │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Level 2: [3, 3]                     │
│ Cross edge detected: (3,3)          │
│ Cycle length = 1 + 1 + 1 = 3        │
│ But this is wrong! Need to check    │
│ if 3 was reached from different     │
│ parents (2 and 4)                   │
└─────────────────────────────────────┘
```

### Step 2: Initial Approach
**DFS approach (inefficient but correct):**

### Step 3: Optimization/Alternative
**BFS approach:**

```python
def graph_girth_bfs(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this works:**
- Uses BFS to find shortest paths
- Detects cycles efficiently
- Handles all vertex pairs
- O(n² + nm) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_graph_girth():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    result = min_cycle if min_cycle != float('inf') else -1
    print(result)

# Main execution
if __name__ == "__main__":
    solve_graph_girth()
```

**Why this works:**
- Optimal BFS-based approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, 4, [(1, 2), (2, 3), (3, 4), (4, 1)]),
        (3, 2, [(1, 2), (2, 3)]),
        (5, 5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]),
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
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n² + nm) - BFS from each vertex
- **Space**: O(n + m) - adjacency list and BFS queue

### Why This Solution Works
- **BFS Cycle Detection**: Finds shortest cycles efficiently
- **Parent Tracking**: Avoids revisiting parent nodes
- **Distance Tracking**: Calculates cycle lengths
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### Important Concepts and Patterns
- **Graph Girth**: Length of shortest cycle in undirected graph
- **BFS Cycle Detection**: Use BFS from each vertex to find shortest cycles
- **Parent Tracking**: Avoid revisiting parent nodes to prevent false cycles
- **Cycle Length Calculation**: Calculate cycle length using distance information

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Graph Girth with Weights**
```python
def graph_girth_weighted(n, edges, weights):
    # Handle graph girth with weighted edges
    
    # Build adjacency list with weights
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest weighted cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor, weight in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + weight
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + weight
                    queue.append((neighbor, node, dist + weight))
    
    return min_cycle if min_cycle != float('inf') else -1
```

#### **2. Graph Girth with Constraints**
```python
def graph_girth_constrained(n, edges, forbidden_edges):
    # Handle graph girth with forbidden edges
    
    # Build adjacency list excluding forbidden edges
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

#### **3. Graph Girth with Dynamic Updates**
```python
def graph_girth_dynamic(n, initial_edges, operations):
    # Handle graph girth with dynamic edge updates
    
    current_edges = initial_edges.copy()
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
            # Query current girth
            result = solve_graph_girth(n, current_edges)
            results.append(result)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Graph Theory**: Cycle detection, shortest paths
- **Graph Algorithms**: BFS, DFS, cycle detection
- **Graph Properties**: Girth, diameter, connectivity
- **Optimization**: Shortest cycle problems

## 📚 Learning Points

### Key Takeaways
- **Graph girth** is a fundamental graph property
- **BFS cycle detection** efficiently finds shortest cycles
- **Parent tracking** prevents false cycle detection
- **Graph algorithms** solve complex cycle problems

## 🎯 Key Insights

### 1. **Graph Girth**
- Length of shortest cycle in graph
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **BFS Cycle Detection**
- Finds shortest paths and cycles
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Parent Tracking**
- Avoids revisiting parent nodes
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Graph Girth with Weights
**Problem**: Each edge has a weight, find shortest weighted cycle.

```python
def weighted_graph_girth(n, edges, weights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest weighted cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor, weight in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + weight
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + weight
                    queue.append((neighbor, node, dist + weight))
    
    return min_cycle if min_cycle != float('inf') else -1
```

### Variation 2: Graph Girth with Constraints
**Problem**: Find shortest cycle avoiding certain edges.

```python
def constrained_graph_girth(n, edges, forbidden_edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

### Variation 3: Dynamic Graph Girth
**Problem**: Support adding/removing edges and maintaining girth.

```python
class DynamicGraphGirth:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.edges = set()
    
    def add_edge(self, a, b):
        if (a, b) not in self.edges and (b, a) not in self.edges:
            self.edges.add((a, b))
            self.adj[a].append(b)
            self.adj[b].append(a)
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.edges.remove((a, b))
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            return True
        elif (b, a) in self.edges:
            self.edges.remove((b, a))
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            return True
        return False
    
    def get_girth(self):
        min_cycle = float('inf')
        
        # Try BFS from each vertex
        for start in range(1, self.n + 1):
            # BFS to find shortest cycle containing start
            from collections import deque
            queue = deque([(start, -1, 0)])  # (node, parent, distance)
            visited = {start: 0}
            
            while queue:
                node, parent, dist = queue.popleft()
                
                for neighbor in self.adj[node]:
                    if neighbor == parent:
                        continue
                    
                    if neighbor in visited:
                        # Found a cycle
                        cycle_length = dist + visited[neighbor] + 1
                        min_cycle = min(min_cycle, cycle_length)
                    else:
                        visited[neighbor] = dist + 1
                        queue.append((neighbor, node, dist + 1))
        
        return min_cycle if min_cycle != float('inf') else -1
```

### Variation 4: Graph Girth with Multiple Constraints
**Problem**: Find shortest cycle satisfying multiple constraints.

```python
def multi_constrained_graph_girth(n, edges, constraints):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    forbidden_edges = constraints.get('forbidden_edges', set())
    allowed_nodes = constraints.get('allowed_nodes', set(range(1, n + 1)))
    
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            if a in allowed_nodes and b in allowed_nodes:
                adj[a].append(b)
                adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each allowed vertex
    for start in allowed_nodes:
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

### Variation 5: Graph Girth with Edge Weights
**Problem**: Each edge has a weight, find shortest weighted cycle.

```python
def weighted_graph_girth_optimized(n, edges, weights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest weighted cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor, weight in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + weight
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + weight
                    queue.append((neighbor, node, dist + weight))
    
    return min_cycle if min_cycle != float('inf') else -1
```

## 🔗 Related Problems

- **[Cycle Detection](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Cycle detection algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[BFS](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Breadth-first search

## 📚 Learning Points

1. **Graph Girth**: Essential for cycle analysis
2. **BFS Cycle Detection**: Efficient cycle finding
3. **Parent Tracking**: Important optimization technique
4. **Graph Theory**: Important graph theory concept

---

**This is a great introduction to graph girth and cycle detection!** 🎯
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    result = min_cycle if min_cycle != float('inf') else -1
    print(result)

# Main execution
if __name__ == "__main__":
    solve_graph_girth()
```

**Why this works:**
- Optimal BFS approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4), (4, 1)]),
        (3, [(1, 2), (2, 3), (3, 1)]),
        (4, [(1, 2), (2, 3), (3, 4)]),  # No cycle
    ]
    
    for n, edges in test_cases:
        result = solve_test(n, edges)
        print(f"n={n}, edges={edges}")
        print(f"Girth: {result}")
        print()

def solve_test(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        from collections import deque
        queue = deque([(start, -1, 0)])
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n² + nm) - BFS from each vertex
- **Space**: O(n + m) - adjacency list and visited set

### Why This Solution Works
- **BFS**: Finds shortest paths efficiently
- **Cycle Detection**: Identifies cycles during traversal
- **Minimum Tracking**: Keeps track of shortest cycle
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **BFS for Shortest Paths**
- Breadth-first search finds shortest paths
- Essential for cycle detection
- Key optimization technique
- Enables efficient solution

### 2. **Cycle Detection**
- Detect cycles during BFS traversal
- Important for graph analysis
- Fundamental concept
- Essential for algorithm

### 3. **Girth Calculation**
- Minimum cycle length in graph
- Important graph property
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Directed Graph Girth
**Problem**: Find girth in a directed graph.

```python
def directed_graph_girth(n, edges):
    # Build directed adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)  # Directed edge
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        from collections import deque
        queue = deque([(start, 0)])  # (node, distance)
        visited = {start: 0}
        
        while queue:
            node, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

### Variation 2: Weighted Graph Girth
**Problem**: Find girth in a weighted graph.

```python
def weighted_graph_girth(n, edges, weights):
    # Build weighted adjacency list
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, weights[i]))
        adj[b].append((a, weights[i]))
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, total_weight)
        visited = {start: 0}
        
        while queue:
            node, parent, weight = queue.popleft()
            
            for neighbor, edge_weight in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_weight = weight + edge_weight
                    min_cycle = min(min_cycle, cycle_weight)
                else:
                    visited[neighbor] = weight + edge_weight
                    queue.append((neighbor, node, weight + edge_weight))
    
    return min_cycle if min_cycle != float('inf') else -1
```

### Variation 3: Girth with Constraints
**Problem**: Find girth avoiding certain edges.

```python
def constrained_graph_girth(n, edges, forbidden_edges):
    # Build adjacency list avoiding forbidden edges
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        from collections import deque
        queue = deque([(start, -1, 0)])
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

### Variation 4: All Cycles Detection
**Problem**: Find all cycles in the graph.

```python
def all_cycles_detection(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    cycles = []
    visited = set()
    
    def dfs(node, parent, path):
        visited.add(node)
        path.append(node)
        
        for neighbor in adj[node]:
            if neighbor == parent:
                continue
            
            if neighbor in path:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
            elif neighbor not in visited:
                dfs(neighbor, node, path)
        
        path.pop()
    
    # Find cycles from each unvisited vertex
    for start in range(1, n + 1):
        if start not in visited:
            dfs(start, -1, [])
    
    return cycles
```

### Variation 5: Dynamic Graph Girth
**Problem**: Support adding/removing edges and answering girth queries.

```python
class DynamicGraphGirth:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.edges = set()
    
    def add_edge(self, a, b):
        if (a, b) not in self.edges and (b, a) not in self.edges:
            self.adj[a].append(b)
            self.adj[b].append(a)
            self.edges.add((a, b))
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.edges.remove((a, b))
        elif (b, a) in self.edges:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.edges.remove((b, a))
    
    def get_girth(self):
        min_cycle = float('inf')
        
        for start in range(1, self.n + 1):
            from collections import deque
            queue = deque([(start, -1, 0)])
            visited = {start: 0}
            
            while queue:
                node, parent, dist = queue.popleft()
                
                for neighbor in self.adj[node]:
                    if neighbor == parent:
                        continue
                    
                    if neighbor in visited:
                        cycle_length = dist + visited[neighbor] + 1
                        min_cycle = min(min_cycle, cycle_length)
                    else:
                        visited[neighbor] = dist + 1
                        queue.append((neighbor, node, dist + 1))
        
        return min_cycle if min_cycle != float('inf') else -1
```

## 🔗 Related Problems

- **[Cycle Detection](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms
- **[BFS](/cses-analyses/problem_soulutions/graph_algorithms/)**: Breadth-first search
- **[Graph Properties](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph analysis

## 📚 Learning Points

1. **BFS**: Essential for shortest path finding
2. **Cycle Detection**: Important graph property
3. **Girth**: Minimum cycle length in graph
4. **Graph Traversal**: Fundamental algorithm technique

---

**This is a great introduction to graph girth and cycle detection!** 🎯
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue and min_cycle > 3:  # Stop if we found a triangle
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this is better:**
- Early termination optimization
- Stops when triangle is found
- More efficient for dense graphs
- Better average case performance

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_graph_girth():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue and min_cycle > 3:  # Stop if we found a triangle
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    result = min_cycle if min_cycle != float('inf') else -1
    print(result)

# Main execution
if __name__ == "__main__":
    solve_graph_girth()
```

**Why this works:**
- Optimal BFS-based approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4), (4, 1)], 4),
        (3, [(1, 2), (2, 3), (3, 1)], 3),
        (4, [(1, 2), (2, 3), (3, 4)], -1),  # No cycle
        (5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)], 5),
    ]
    
    for n, edges, expected in test_cases:
        result = solve_test(n, edges)
        print(f"n={n}, edges={edges}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue and min_cycle > 3:  # Stop if we found a triangle
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n² + nm) - BFS from each vertex
- **Space**: O(n + m) - adjacency list and visited sets

### Why This Solution Works
- **BFS Traversal**: Finds shortest paths efficiently
- **Cycle Detection**: Identifies cycles through visited nodes
- **Early Termination**: Stops when triangle is found
- **Optimal Approach**: Guarantees shortest cycle

## 🎯 Key Insights

### 1. **Graph Girth**
- Length of shortest cycle in graph
- Key insight for optimization
- Essential for understanding
- Enables efficient solution

### 2. **BFS for Shortest Paths**
- Finds shortest paths from each vertex
- Identifies cycles efficiently
- Important for performance
- Fundamental algorithm

### 3. **Cycle Detection**
- Detect cycles through visited nodes
- Calculate cycle length from distances
- Simple but important observation
- Essential for solution

## 🎯 Problem Variations

### Variation 1: Weighted Graph Girth
**Problem**: Each edge has a weight. Find minimum weight cycle.

```python
def weighted_graph_girth(n, edges, weights):
    # Build adjacency list with weights
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, weights[i]))
        adj[b].append((a, weights[i]))
    
    min_cycle_weight = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor, weight in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_weight = dist + visited[neighbor] + weight
                    min_cycle_weight = min(min_cycle_weight, cycle_weight)
                else:
                    visited[neighbor] = dist + weight
                    queue.append((neighbor, node, dist + weight))
    
    return min_cycle_weight if min_cycle_weight != float('inf') else -1
```

### Variation 2: Directed Graph Girth
**Problem**: Find girth in a directed graph.

```python
def directed_graph_girth(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, 0)])  # (node, distance)
        visited = {start: 0}
        
        while queue:
            node, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == start:
                    # Found a cycle back to start
                    cycle_length = dist + 1
                    min_cycle = min(min_cycle, cycle_length)
                elif neighbor not in visited:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

### Variation 3: Girth with Constraints
**Problem**: Find girth while avoiding certain edges.

```python
def constrained_graph_girth(n, edges, forbidden_edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    min_cycle = min(min_cycle, cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

### Variation 4: All Cycles Detection
**Problem**: Find all cycles and their lengths.

```python
def all_cycles_detection(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    cycles = []
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find all cycles containing start
        from collections import deque
        queue = deque([(start, -1, 0)])  # (node, parent, distance)
        visited = {start: 0}
        
        while queue:
            node, parent, dist = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    # Found a cycle
                    cycle_length = dist + visited[neighbor] + 1
                    cycles.append(cycle_length)
                else:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return cycles
```

### Variation 5: Girth with Node Weights
**Problem**: Each node has a weight. Find cycle with minimum total node weight.

```python
def node_weighted_girth(n, edges, node_weights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle_weight = float('inf')
    
    # Try BFS from each vertex
    for start in range(1, n + 1):
        # BFS to find shortest cycle containing start
        from collections import deque
        queue = deque([(start, -1, 0, {start})])  # (node, parent, weight, visited_nodes)
        
        while queue:
            node, parent, weight, visited_nodes = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited_nodes:
                    # Found a cycle
                    cycle_weight = weight + node_weights[neighbor]
                    min_cycle_weight = min(min_cycle_weight, cycle_weight)
                else:
                    new_visited = visited_nodes.copy()
                    new_visited.add(neighbor)
                    new_weight = weight + node_weights[neighbor]
                    queue.append((neighbor, node, new_weight, new_visited))
    
    return min_cycle_weight if min_cycle_weight != float('inf') else -1
```

## 🔗 Related Problems

- **[Cycle Detection](/cses-analyses/problem_soulutions/graph_algorithms/cycle_finding_analysis)**: Graph cycles
- **[Shortest Path](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_i_analysis)**: Path algorithms
- **[Graph Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms

## 📚 Learning Points

1. **Graph Girth**: Essential for cycle analysis
2. **BFS Algorithm**: Efficient shortest path finding
3. **Cycle Detection**: Key technique for graph problems
4. **Graph Traversal**: Common pattern in graph algorithms

---

**This is a great introduction to graph girth and cycle detection!** 🎯 