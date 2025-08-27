# CSES Even Outdegree Edges - Problem Analysis

## Problem Statement
Given an undirected graph with n nodes and m edges, find the minimum number of edges to remove so that every node has even outdegree.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print the minimum number of edges to remove.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 4
1 2
2 3
3 4
4 1

Output:
0
```

## Solution Progression

### Approach 1: Naive Edge Removal - O(m²)
**Description**: Try removing edges one by one and check if all nodes have even degree.

```python
def even_outdegree_edges_naive(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def check_even_degrees():
        for i in range(1, n + 1):
            if len(adj[i]) % 2 != 0:
                return False
        return True
    
    # Try removing edges
    min_removals = m
    for i in range(m):
        # Remove edge i
        a, b = edges[i]
        adj[a].remove(b)
        adj[b].remove(a)
        
        if check_even_degrees():
            min_removals = min(min_removals, 1)
        
        # Restore edge
        adj[a].append(b)
        adj[b].append(a)
    
    return min_removals
```

**Why this is inefficient**: This approach tries all possible edge removals, leading to exponential complexity.

### Improvement 1: Eulerian Circuit Analysis - O(n + m)
**Description**: Use properties of Eulerian circuits to find minimum edge removals.

```python
def even_outdegree_edges_eulerian(n, m, edges):
    # Count degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Count nodes with odd degree
    odd_nodes = sum(1 for i in range(1, n + 1) if degree[i] % 2 != 0)
    
    # For an Eulerian circuit, all nodes must have even degree
    # We need to remove edges to make all degrees even
    # Each edge removal affects exactly 2 nodes
    # So we need to remove odd_nodes // 2 edges
    return odd_nodes // 2
```

**Why this improvement works**: Uses the property that for an Eulerian circuit, all nodes must have even degree, and each edge removal affects exactly 2 nodes.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_minimum_edges_to_remove(n, m, edges):
    # Count degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Count nodes with odd degree
    odd_nodes = sum(1 for i in range(1, n + 1) if degree[i] % 2 != 0)
    
    # For an Eulerian circuit, all nodes must have even degree
    # Each edge removal affects exactly 2 nodes
    # So we need to remove odd_nodes // 2 edges
    return odd_nodes // 2

result = find_minimum_edges_to_remove(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Edge Removal | O(m²) | O(n + m) | Exponential complexity |
| Eulerian Analysis | O(n + m) | O(n) | Eulerian circuit properties |

## Key Insights for Other Problems

### 1. **Eulerian Circuit Properties**
**Principle**: For an Eulerian circuit, all nodes must have even degree.
**Applicable to**: Eulerian circuit problems, degree problems, graph optimization problems

### 2. **Degree Parity Analysis**
**Principle**: Each edge removal affects exactly 2 nodes' degrees.
**Applicable to**: Degree problems, edge removal problems, graph optimization problems

### 3. **Handshake Lemma**
**Principle**: The sum of all degrees in a graph is always even (twice the number of edges).
**Applicable to**: Degree problems, graph theory problems, parity problems

## Notable Techniques

### 1. **Degree Counting**
```python
def count_degrees(n, edges):
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    return degree
```

### 2. **Odd Degree Counting**
```python
def count_odd_degrees(degree):
    odd_nodes = sum(1 for i in range(1, len(degree)) if degree[i] % 2 != 0)
    return odd_nodes
```

### 3. **Eulerian Circuit Check**
```python
def is_eulerian_circuit_possible(n, edges):
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return False
    return True
```

### 4. **Minimum Edge Removals**
```python
def minimum_edge_removals_for_even_degrees(n, edges):
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    odd_nodes = sum(1 for i in range(1, n + 1) if degree[i] % 2 != 0)
    return odd_nodes // 2
```

## Problem-Solving Framework

1. **Identify problem type**: This is an Eulerian circuit problem with edge removal
2. **Choose approach**: Use Eulerian circuit properties and degree analysis
3. **Initialize data structure**: Count degrees of all nodes
4. **Analyze degrees**: Count nodes with odd degree
5. **Calculate removals**: Use the fact that each edge removal affects 2 nodes
6. **Apply formula**: Minimum removals = odd_nodes // 2
7. **Return result**: Output the minimum number of edges to remove

---

*This analysis shows how to efficiently find the minimum edges to remove for even degrees using Eulerian circuit properties.* 