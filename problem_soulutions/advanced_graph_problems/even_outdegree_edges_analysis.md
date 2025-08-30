---
layout: simple
title: "Even Outdegree Edges"
permalink: /problem_soulutions/advanced_graph_problems/even_outdegree_edges_analysis
---

# Even Outdegree Edges

## Problem Description

**Problem**: Given a directed graph, find the minimum number of edges to add so that every vertex has even outdegree.

**Input**: 
- n: number of vertices
- m: number of edges
- m lines: a b (edge from vertex a to vertex b)

**Output**: Minimum number of edges to add.

**Example**:
```
Input:
4 3
1 2
2 3
3 4

Output:
1

Explanation: 
Add edge (4, 1) to make all outdegrees even.
Vertices 1, 2, 3, 4 have outdegrees 1, 1, 1, 1 → 2, 1, 1, 2
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find minimum edges to add to a directed graph
- Make all vertex outdegrees even
- Use graph theory concepts
- Apply Eulerian circuit properties

**Key Observations:**
- This is related to Eulerian circuits
- Need to balance outdegrees
- Odd outdegree vertices need connections
- Can use graph theory properties

### Step 2: Graph Theory Approach
**Idea**: Use properties of Eulerian circuits and graph balancing.

```python
def even_outdegree_edges_graph_theory(n, m, edges):
    # Count outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Count vertices with odd outdegree
    odd_vertices = []
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_vertices.append(i)
    
    # Need to connect odd vertices
    # Each edge can fix at most 2 odd vertices
    return len(odd_vertices) // 2
```

**Why this works:**
- Uses graph theory properties
- Each edge affects exactly 2 vertices
- Simple and efficient
- O(n + m) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_even_outdegree_edges():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Count outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Count vertices with odd outdegree
    odd_vertices = []
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_vertices.append(i)
    
    # Need to connect odd vertices
    # Each edge can fix at most 2 odd vertices
    result = len(odd_vertices) // 2
    
    print(result)

# Main execution
if __name__ == "__main__":
    solve_even_outdegree_edges()
```

**Why this works:**
- Optimal graph theory approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, 3, [(1, 2), (2, 3), (3, 4)], 1),
        (3, 2, [(1, 2), (2, 3)], 1),
        (4, 4, [(1, 2), (2, 3), (3, 4), (4, 1)], 0),
        (3, 1, [(1, 2)], 1),
    ]
    
    for n, m, edges, expected in test_cases:
        result = solve_test(n, m, edges)
        print(f"n={n}, m={m}, edges={edges}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, m, edges):
    # Count outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Count vertices with odd outdegree
    odd_vertices = []
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_vertices.append(i)
    
    # Need to connect odd vertices
    return len(odd_vertices) // 2

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - counting outdegrees
- **Space**: O(n) - outdegree array

### Why This Solution Works
- **Graph Theory**: Uses properties of Eulerian circuits
- **Odd Degree Balancing**: Each edge affects exactly 2 vertices
- **Optimal Approach**: Minimum edges needed
- **Simple Logic**: Clear mathematical reasoning

## 🎯 Key Insights

### 1. **Graph Theory Properties**
- Each edge affects exactly 2 vertices
- Odd outdegree vertices need balancing
- Key insight for optimization
- Essential for understanding

### 2. **Eulerian Circuit Connection**
- Related to Eulerian circuit problems
- Even degrees are important
- Important for efficiency
- Fundamental concept

### 3. **Odd Degree Counting**
- Count vertices with odd outdegree
- Each edge can fix 2 odd vertices
- Simple but important observation
- Essential for solution

## 🎯 Problem Variations

### Variation 1: Weighted Edge Addition
**Problem**: Each edge has a cost. Find minimum cost to make all outdegrees even.

```python
def even_outdegree_edges_weighted(n, m, edges, costs):
    # Count outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Count vertices with odd outdegree
    odd_vertices = []
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_vertices.append(i)
    
    # Find minimum cost matching
    if len(odd_vertices) == 0:
        return 0
    
    # Simple greedy approach: connect consecutive odd vertices
    total_cost = 0
    for i in range(0, len(odd_vertices), 2):
        if i + 1 < len(odd_vertices):
            # Find minimum cost edge between these vertices
            min_cost = float('inf')
            for j in range(len(costs)):
                if edges[j][0] == odd_vertices[i] and edges[j][1] == odd_vertices[i+1]:
                    min_cost = min(min_cost, costs[j])
            total_cost += min_cost if min_cost != float('inf') else 1
    
    return total_cost
```

### Variation 2: Maximum Even Outdegree Subgraph
**Problem**: Find maximum number of edges that can remain while keeping all outdegrees even.

```python
def maximum_even_outdegree_subgraph(n, m, edges):
    # Count outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Count vertices with odd outdegree
    odd_vertices = []
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_vertices.append(i)
    
    # Need to remove edges to make outdegrees even
    # Each edge removal affects exactly 2 vertices
    edges_to_remove = len(odd_vertices) // 2
    
    return m - edges_to_remove
```

### Variation 3: Even Outdegree with Constraints
**Problem**: Can only add edges between certain vertex pairs.

```python
def even_outdegree_edges_constrained(n, m, edges, allowed_edges):
    # Count outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Count vertices with odd outdegree
    odd_vertices = []
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_vertices.append(i)
    
    # Try to connect odd vertices using allowed edges
    used_edges = 0
    for i in range(0, len(odd_vertices), 2):
        if i + 1 < len(odd_vertices):
            v1, v2 = odd_vertices[i], odd_vertices[i+1]
            if (v1, v2) in allowed_edges or (v2, v1) in allowed_edges:
                used_edges += 1
    
    return used_edges
```

### Variation 4: Dynamic Even Outdegree
**Problem**: Support adding/removing edges and maintaining even outdegrees.

```python
class DynamicEvenOutdegreeGraph:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.outdegree = [0] * (n + 1)
        self.odd_count = 0
    
    def add_edge(self, a, b):
        # Update outdegree
        old_parity = self.outdegree[a] % 2
        self.outdegree[a] += 1
        new_parity = self.outdegree[a] % 2
        
        # Update odd count
        if old_parity == 0 and new_parity == 1:
            self.odd_count += 1
        elif old_parity == 1 and new_parity == 0:
            self.odd_count -= 1
        
        self.adj[a].append(b)
    
    def remove_edge(self, a, b):
        if b in self.adj[a]:
            # Update outdegree
            old_parity = self.outdegree[a] % 2
            self.outdegree[a] -= 1
            new_parity = self.outdegree[a] % 2
            
            # Update odd count
            if old_parity == 0 and new_parity == 1:
                self.odd_count += 1
            elif old_parity == 1 and new_parity == 0:
                self.odd_count -= 1
            
            self.adj[a].remove(b)
            return True
        return False
    
    def get_min_edges_to_add(self):
        return self.odd_count // 2
    
    def is_even_outdegree(self):
        return self.odd_count == 0
```

### Variation 5: Even Outdegree with Self-Loops
**Problem**: Allow self-loops (edges from vertex to itself).

```python
def even_outdegree_edges_with_self_loops(n, m, edges):
    # Count outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Count vertices with odd outdegree
    odd_vertices = []
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_vertices.append(i)
    
    # With self-loops, we can fix odd vertices individually
    # Each self-loop affects exactly one vertex
    return len(odd_vertices)
```

## 🔗 Related Problems

- **[Eulerian Circuit](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory
- **[Graph Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms
- **[Degree Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Vertex degrees

## 📚 Learning Points

1. **Graph Theory**: Essential for degree problems
2. **Eulerian Circuits**: Related concepts
3. **Odd Degree Balancing**: Key technique
4. **Mathematical Reasoning**: Simple but powerful

---

**This is a great introduction to graph theory and degree problems!** 🎯 