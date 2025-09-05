---
layout: simple
title: "Mail Delivery - Eulerian Circuit Finding"
permalink: /problem_soulutions/graph_algorithms/mail_delivery_analysis
---

# Mail Delivery - Eulerian Circuit Finding

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand Eulerian circuit problems and graph connectivity concepts
- [ ] **Objective 2**: Apply Hierholzer's algorithm or DFS-based approach to find Eulerian circuits
- [ ] **Objective 3**: Implement efficient Eulerian circuit algorithms with proper edge tracking
- [ ] **Objective 4**: Optimize Eulerian circuit solutions using graph representations and circuit construction
- [ ] **Objective 5**: Handle edge cases in Eulerian circuits (no circuit exists, disconnected components, degree conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Eulerian circuits, Hierholzer's algorithm, DFS-based circuits, graph connectivity, circuit algorithms
- **Data Structures**: Adjacency lists, edge tracking, circuit data structures, graph representations
- **Mathematical Concepts**: Graph theory, Eulerian circuits, graph connectivity, degree properties, circuit theory
- **Programming Skills**: Graph traversal, circuit construction, edge tracking, algorithm implementation
- **Related Problems**: Teleporters Path (Eulerian trails), De Bruijn Sequence (Eulerian paths), Graph connectivity

## 📋 Problem Description

Given an undirected graph with n nodes and m edges, find an Eulerian circuit (a path that visits every edge exactly once and returns to the starting node).

An Eulerian circuit is a path that traverses every edge in a graph exactly once and returns to the starting vertex. This problem is a classic application of graph theory in routing and delivery systems.

**Input**: 
- First line: Two integers n and m (number of nodes and edges)
- Next m lines: Two integers a and b (edge between nodes a and b)

**Output**: 
- Nodes in order visited in the Eulerian circuit, or "IMPOSSIBLE" if no circuit exists

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
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
1 2 3 4 1
```

**Explanation**: 
- The graph forms a cycle: 1→2→3→4→1
- All vertices have even degree (2 each)
- Eulerian circuit exists: 1→2→3→4→1
- Each edge is traversed exactly once

## 🎯 Visual Example

### Input Graph
```
Nodes: 1, 2, 3, 4
Edges: (1,2), (2,3), (3,4), (4,1)

Graph representation:
1 ── 2 ── 3 ── 4
│              │
└──────────────┘
```

### Eulerian Circuit Algorithm Process
```
Step 1: Check Eulerian circuit conditions
- Degree of vertex 1: 2 (even)
- Degree of vertex 2: 2 (even)
- Degree of vertex 3: 2 (even)
- Degree of vertex 4: 2 (even)
- All vertices have even degree ✓
- Graph is connected ✓
- Eulerian circuit exists

Step 2: Find starting vertex
- Any vertex can be starting point (all have even degree)
- Start from vertex 1

Step 3: Hierholzer's algorithm
- Current path: [1]
- Available edges: (1,2), (2,3), (3,4), (4,1)

Step 4: Build circuit
- From 1: go to 2
- Current path: [1, 2]
- Available edges: (2,3), (3,4), (4,1)

- From 2: go to 3
- Current path: [1, 2, 3]
- Available edges: (3,4), (4,1)

- From 3: go to 4
- Current path: [1, 2, 3, 4]
- Available edges: (4,1)

- From 4: go to 1
- Current path: [1, 2, 3, 4, 1]
- No more edges available

Step 5: Complete circuit
- Eulerian circuit: 1 → 2 → 3 → 4 → 1
- All edges visited exactly once
```

### Circuit Analysis
```
Eulerian circuit found:
1 → 2 → 3 → 4 → 1

Edges used:
- (1,2): visited once
- (2,3): visited once
- (3,4): visited once
- (4,1): visited once

All edges visited exactly once ✓
Returns to starting vertex ✓
```

### Key Insight
Hierholzer's algorithm works by:
1. Checking Eulerian circuit conditions (all even degrees)
2. Starting from any vertex
3. Following edges until no more edges available
4. Backtracking and inserting cycles if needed
5. Time complexity: O(m) where m is number of edges
6. Space complexity: O(n + m) for graph representation

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find Eulerian circuit visiting every edge exactly once
- **Key Insight**: All vertices must have even degree for Eulerian circuit to exist
- **Challenge**: Handle large graphs efficiently and manage edge removal

### Step 2: Brute Force Approach
**Check all possible paths and find Eulerian circuit:**

```python
def mail_delivery_naive(n, m, edges):
    # Check if Eulerian circuit exists
    # All vertices must have even degree
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm
    def find_eulerian_circuit():
        # Start from any vertex
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                # Take an edge
                next_node = adj[current].pop()
                # Remove the reverse edge
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                # No more edges from current vertex
                path.append(stack.pop())
        
        return path[::-1]  # Reverse to get correct order
    
    circuit = find_eulerian_circuit()
    
    # Check if all edges were used
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, circuit))
```

**Complexity**: O(n + m) - optimal for this problem

### Step 3: Optimization
**Use optimized Hierholzer's algorithm with better edge management:**

```python
def mail_delivery_optimized(n, m, edges):
    # Check if Eulerian circuit exists
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm with edge tracking
    def find_eulerian_circuit():
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, circuit))
```

**Why this improvement works**: We use Hierholzer's algorithm with optimized edge management to find Eulerian circuit efficiently.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_mail_delivery_route(n, m, edges):
    # Check if Eulerian circuit exists
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm
    def find_eulerian_circuit():
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    # Check if all edges were used
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, circuit))

result = find_mail_delivery_route(n, m, edges)
print(result)

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((4, 4, [(1, 2), (2, 3), (3, 4), (4, 1)]), "1 2 3 4 1"),
        ((3, 3, [(1, 2), (2, 3), (3, 1)]), "1 2 3 1"),
        ((4, 3, [(1, 2), (2, 3), (3, 4)]), "IMPOSSIBLE"),  # Odd degrees
    ]
    
    for (n, m, edges), expected in test_cases:
        result = find_eulerian_circuit(n, m, edges)
        print(f"n={n}, m={m}, edges={edges}")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_eulerian_circuit(n, m, edges):
    # Check if Eulerian circuit exists
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm
    def find_circuit():
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_circuit()
    
    # Check if all edges were used
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, circuit))

test_solution()
```
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - single pass through graph
- **Space**: O(n + m) - adjacency list and stack storage

### Why This Solution Works
- **Hierholzer's Algorithm**: Optimal for finding Eulerian circuits
- **Degree Check**: Ensures Eulerian circuit exists
- **Stack-based Approach**: Efficiently manages path construction
- **Edge Management**: Properly removes used edges

## 🎨 Visual Example

### Input Example
```
4 nodes, 4 edges:
Edge 1-2
Edge 2-3
Edge 3-4
Edge 4-1
```

### Graph Visualization
```
Undirected graph:
1 ──── 2
│      │
│      │
4 ──── 3

All edges:
- Edge 1-2
- Edge 2-3
- Edge 3-4
- Edge 4-1
```

### Degree Check
```
Check if Eulerian circuit exists:

Node 1: degree = 2 (connected to 2 and 4)
Node 2: degree = 2 (connected to 1 and 3)
Node 3: degree = 2 (connected to 2 and 4)
Node 4: degree = 2 (connected to 3 and 1)

All nodes have even degree → Eulerian circuit exists
```

### Hierholzer's Algorithm Process
```
Step 1: Start from node 1
- Current path: [1]
- Current node: 1
- Available edges: 1-2, 1-4

Step 2: Choose edge 1-2
- Current path: [1, 2]
- Current node: 2
- Available edges: 2-3

Step 3: Choose edge 2-3
- Current path: [1, 2, 3]
- Current node: 3
- Available edges: 3-4

Step 4: Choose edge 3-4
- Current path: [1, 2, 3, 4]
- Current node: 4
- Available edges: 4-1

Step 5: Choose edge 4-1
- Current path: [1, 2, 3, 4, 1]
- Current node: 1
- No available edges

Eulerian circuit: 1 → 2 → 3 → 4 → 1
```

### Stack-based Approach
```
Alternative approach using stack:

Step 1: Initialize
- Stack: [1]
- Current node: 1

Step 2: From node 1, choose edge 1-2
- Stack: [1, 2]
- Current node: 2

Step 3: From node 2, choose edge 2-3
- Stack: [1, 2, 3]
- Current node: 3

Step 4: From node 3, choose edge 3-4
- Stack: [1, 2, 3, 4]
- Current node: 4

Step 5: From node 4, choose edge 4-1
- Stack: [1, 2, 3, 4, 1]
- Current node: 1

Step 6: No more edges from node 1
- Pop from stack: 1
- Add to result: [1]
- Current node: 4

Step 7: No more edges from node 4
- Pop from stack: 4
- Add to result: [1, 4]
- Current node: 3

Continue until stack is empty...
Final result: [1, 4, 3, 2, 1]
```

### Edge Management
```
Track used edges to avoid revisiting:

Initial edges:
- 1-2: available
- 2-3: available
- 3-4: available
- 4-1: available

After using edge 1-2:
- 1-2: used
- 2-3: available
- 3-4: available
- 4-1: available

After using edge 2-3:
- 1-2: used
- 2-3: used
- 3-4: available
- 4-1: available

Continue until all edges used...
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Hierholzer's    │ O(m)         │ O(m)         │ Stack-based  │
│                 │              │              │ construction │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DFS + Stack     │ O(m)         │ O(m)         │ Recursive    │
│                 │              │              │ with stack   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Fleury's        │ O(m²)        │ O(m)         │ Edge         │
│                 │              │              │ removal      │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Eulerian Circuit**
- Use Hierholzer's algorithm to find Eulerian circuit
- Important for understanding
- Enables efficient circuit construction
- Essential for algorithm

### 2. **Degree Check**
- Check if all vertices have even degree for Eulerian circuit
- Important for understanding
- Ensures circuit existence
- Essential for correctness

### 3. **Hierholzer's Algorithm**
- Use stack-based approach to find Eulerian circuit
- Important for understanding
- Provides optimal solution
- Essential for performance

## 🎯 Problem Variations

### Variation 1: Mail Delivery with Costs
**Problem**: Each street has a delivery cost, find minimum cost Eulerian circuit.

## Notable Techniques

### 1. **Hierholzer's Algorithm Implementation**
```python
def hierholzer_algorithm(n, adj):
    # Check if Eulerian circuit exists
    degree = [0] * (n + 1)
    for u in range(1, n + 1):
        degree[u] = len(adj[u])
    
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return None  # No Eulerian circuit
    
    # Find Eulerian circuit
    start = 1
    path = []
    stack = [start]
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node = adj[current].pop()
            adj[next_node].remove(current)
            stack.append(next_node)
        else:
            path.append(stack.pop())
    
    return path[::-1]
```

### 2. **Eulerian Circuit Check**
```python
def check_eulerian_circuit(n, adj):
    for i in range(1, n + 1):
        if len(adj[i]) % 2 != 0:
            return False
    return True
```

### 3. **Edge Management**
```python
def remove_edge(adj, u, v):
    adj[u].remove(v)
    adj[v].remove(u)
```

## Problem-Solving Framework

1. **Identify problem type**: This is an Eulerian circuit problem
2. **Choose approach**: Use Hierholzer's algorithm
3. **Check conditions**: Verify all vertices have even degree
4. **Build graph**: Create adjacency list representation
5. **Find circuit**: Use Hierholzer's algorithm to find Eulerian circuit
6. **Verify result**: Check if all edges were used
7. **Return result**: Output circuit or "IMPOSSIBLE"

---

*This analysis shows how to efficiently find Eulerian circuit using Hierholzer's algorithm.*

---

## 🔗 Related Problems

- **[Eulerian Path](/cses-analyses/problem_soulutions/graph_algorithms/)**: Path visiting every edge exactly once
- **[Graph Traversal](/cses-analyses/problem_soulutions/graph_algorithms/)**: Pathfinding problems
- **[Connectivity](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph connectivity problems

## 📚 Learning Points

1. **Hierholzer's Algorithm**: Essential for Eulerian circuit problems
2. **Degree Analysis**: Important for graph property verification
3. **Stack-based Search**: Key technique for circuit construction
4. **Edge Management**: Critical for efficient graph traversal
5. **Graph Theory**: Foundation for many algorithmic problems

---

**This is a great introduction to Eulerian circuits and Hierholzer's algorithm!** 🎯 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Mail Delivery with Costs**
**Problem**: Each street has a delivery cost, find minimum cost Eulerian circuit.
```python
def cost_based_mail_delivery(n, edges, costs):
    # costs[(a, b)] = cost of delivering mail on street (a, b)
    
    # Calculate degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Check Eulerian circuit conditions
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Build adjacency list with costs
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        cost = costs.get((a, b), 0)
        adj[a].append((b, cost))
        adj[b].append((a, cost))
    
    # Use Hierholzer's algorithm with cost tracking
    start = 1
    path = []
    stack = [start]
    total_cost = 0
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node, cost = adj[current].pop()
            # Remove reverse edge
            for i, (node, _) in enumerate(adj[next_node]):
                if node == current:
                    adj[next_node].pop(i)
                    break
            stack.append(next_node)
            total_cost += cost
        else:
            path.append(stack.pop())
    
    if len(path) != len(edges) + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, path[::-1])), total_cost
```

#### **Variation 2: Mail Delivery with Constraints**
**Problem**: Find Eulerian circuit with constraints on street usage.
```python
def constrained_mail_delivery(n, edges, constraints):
    # constraints = {'max_uses': x, 'forbidden_streets': [(a, b), ...]}
    
    # Calculate degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Check Eulerian circuit conditions
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        # Check if street is forbidden
        if (a, b) not in constraints.get('forbidden_streets', []):
            adj[a].append(b)
            adj[b].append(a)
    
    # Use Hierholzer's algorithm
    start = 1
    path = []
    stack = [start]
    edge_uses = {}  # Track edge usage
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node = adj[current].pop()
            edge = tuple(sorted([current, next_node]))
            
            # Check usage constraints
            if edge_uses.get(edge, 0) < constraints.get('max_uses', float('inf')):
                edge_uses[edge] = edge_uses.get(edge, 0) + 1
                # Remove reverse edge
                adj[next_node].remove(current)
                stack.append(next_node)
        else:
            path.append(stack.pop())
    
    if len(path) != len(edges) + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, path[::-1]))
```

#### **Variation 3: Mail Delivery with Probabilities**
**Problem**: Each street has a success probability, find most reliable Eulerian circuit.
```python
def probabilistic_mail_delivery(n, edges, probabilities):
    # probabilities[(a, b)] = probability that mail delivery succeeds on street (a, b)
    
    # Calculate degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Check Eulerian circuit conditions
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Build adjacency list with probabilities
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        prob = probabilities.get((a, b), 0.5)
        adj[a].append((b, prob))
        adj[b].append((a, prob))
    
    # Use Hierholzer's algorithm with probability tracking
    start = 1
    path = []
    stack = [start]
    total_probability = 1.0
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node, prob = adj[current].pop()
            # Remove reverse edge
            for i, (node, _) in enumerate(adj[next_node]):
                if node == current:
                    adj[next_node].pop(i)
                    break
            stack.append(next_node)
            total_probability *= prob
        else:
            path.append(stack.pop())
    
    if len(path) != len(edges) + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, path[::-1])), total_probability
```

#### **Variation 4: Mail Delivery with Multiple Criteria**
**Problem**: Find Eulerian circuit optimizing multiple objectives (cost, time, reliability).
```python
def multi_criteria_mail_delivery(n, edges, costs, times, reliabilities):
    # costs[(a, b)] = cost, times[(a, b)] = time, reliabilities[(a, b)] = reliability
    
    # Calculate degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Check Eulerian circuit conditions
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Normalize values
    max_cost = max(costs.values()) if costs else 1
    max_time = max(times.values()) if times else 1
    max_reliability = max(reliabilities.values()) if reliabilities else 1
    
    # Build adjacency list with weighted scores
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        cost = costs.get((a, b), 0) / max_cost
        time = times.get((a, b), 0) / max_time
        reliability = reliabilities.get((a, b), 1) / max_reliability
        
        # Weighted score (lower is better)
        score = 0.4 * cost + 0.3 * time - 0.3 * reliability
        adj[a].append((b, score))
        adj[b].append((a, score))
    
    # Sort edges by score for greedy approach
    for i in range(1, n + 1):
        adj[i].sort(key=lambda x: x[1])
    
    # Use Hierholzer's algorithm
    start = 1
    path = []
    stack = [start]
    total_cost = 0
    total_time = 0
    total_reliability = 1.0
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node, score = adj[current].pop()
            # Remove reverse edge
            for i, (node, _) in enumerate(adj[next_node]):
                if node == current:
                    adj[next_node].pop(i)
                    break
            
            stack.append(next_node)
            
            # Track actual values
            edge = tuple(sorted([current, next_node]))
            total_cost += costs.get(edge, 0)
            total_time += times.get(edge, 0)
            total_reliability *= reliabilities.get(edge, 1)
        else:
            path.append(stack.pop())
    
    if len(path) != len(edges) + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, path[::-1])), total_cost, total_time, total_reliability
```

#### **Variation 5: Mail Delivery with Dynamic Updates**
**Problem**: Handle dynamic updates to street network and find Eulerian circuit after each update.
```python
def dynamic_mail_delivery(n, initial_edges, updates):
    # updates = [(edge_to_add, edge_to_remove), ...]
    
    edges = initial_edges.copy()
    results = []
    
    for edge_to_add, edge_to_remove in updates:
        # Update edges
        if edge_to_remove in edges:
            edges.remove(edge_to_remove)
        if edge_to_add:
            edges.append(edge_to_add)
        
        # Recompute Eulerian circuit
        # Calculate degrees
        degree = [0] * (n + 1)
        for a, b in edges:
            degree[a] += 1
            degree[b] += 1
        
        # Check Eulerian circuit conditions
        possible = True
        for i in range(1, n + 1):
            if degree[i] % 2 != 0:
                possible = False
                break
        
        if not possible:
            results.append("IMPOSSIBLE")
            continue
        
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        
        # Use Hierholzer's algorithm
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        if len(path) != len(edges) + 1:
            results.append("IMPOSSIBLE")
        else:
            results.append(" ".join(map(str, path[::-1])))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Eulerian Path Problems**
- **Eulerian Circuit**: Circuit using each edge exactly once
- **Eulerian Trail**: Trail using each edge exactly once
- **Semi-Eulerian**: Graph with Eulerian trail but not circuit
- **Eulerian Graph**: Graph with Eulerian circuit

#### **2. Graph Traversal Problems**
- **Hamiltonian Path**: Path visiting each vertex exactly once
- **Hamiltonian Cycle**: Cycle visiting each vertex exactly once
- **Chinese Postman**: Find shortest closed walk using all edges
- **Traveling Salesman**: Find shortest Hamiltonian cycle

#### **3. Path Problems**
- **Shortest Path**: Find shortest path between vertices
- **All Pairs Shortest Path**: Find shortest paths between all pairs
- **K-Shortest Paths**: Find k shortest paths
- **Disjoint Paths**: Find edge-disjoint paths

#### **4. Graph Theory Problems**
- **Connectivity**: Study of graph connectivity
- **Degree Analysis**: Analyze vertex degrees
- **Graph Properties**: Study graph properties
- **Trail Theory**: Theory of trails and paths

#### **5. Algorithmic Techniques**
- **Hierholzer's Algorithm**: Find Eulerian trail/circuit
- **DFS**: Depth-first search for path finding
- **BFS**: Breadth-first search for path finding
- **Graph Algorithms**: Various graph algorithms

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Networks**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = find_mail_delivery_route(n, m, edges)
    print(result)
```

#### **2. Range Queries on Mail Delivery**
```python
def range_mail_delivery_queries(n, edges, queries):
    # queries = [(start_edge, end_edge), ...] - find circuit using edges in range
    
    results = []
    for start, end in queries: subset_edges = edges[
start: end+1]
        result = find_mail_delivery_route(n, len(subset_edges), subset_edges)
        results.append(result)
    
    return results
```

#### **3. Interactive Mail Delivery Problems**
```python
def interactive_mail_delivery():
    n, m = map(int, input("Enter n and m: ").split())
    print("Enter edges (a b):")
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = find_mail_delivery_route(n, m, edges)
    print(f"Mail delivery route: {result}")
    
    # Show the circuit
    if result != "IMPOSSIBLE":
        circuit = result.split()
        print(f"Circuit: {' -> '.join(circuit)}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Euler's Theorem**: Conditions for Eulerian trail/circuit
- **Degree Theory**: Properties of vertex degrees
- **Connectivity Theory**: Theory of graph connectivity
- **Trail Theory**: Mathematical theory of trails

#### **2. Linear Algebra**
- **Adjacency Matrix**: Matrix representation of graphs
- **Incidence Matrix**: Edge-vertex incidence matrix
- **Laplacian Matrix**: Graph Laplacian matrix
- **Spectral Graph Theory**: Study of graph eigenvalues

#### **3. Combinatorics**
- **Path Counting**: Count number of paths
- **Trail Counting**: Count number of trails
- **Graph Enumeration**: Enumerate graphs with properties
- **Permutation Theory**: Theory of permutations

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Eulerian Algorithms**: Hierholzer's, Fleury's algorithms
- **Path Algorithms**: DFS, BFS, Dijkstra, Floyd-Warshall
- **Graph Algorithms**: Connectivity, traversal algorithms
- **Optimization Algorithms**: Linear programming, integer programming

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Linear Algebra**: Matrix representations of graphs
- **Combinatorics**: Combinatorial graph theory
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Path Finding**: Efficient path finding algorithms
- **Trail Construction**: Building trails from graph data
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient Eulerian circuit techniques and shows various extensions for mail delivery problems.* 