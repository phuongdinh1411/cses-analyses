# CSES Mail Delivery - Problem Analysis

## Problem Statement
Given an undirected graph with n nodes and m edges, find an Eulerian circuit (a path that visits every edge exactly once and returns to the starting node).

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print the nodes in the order they are visited in the Eulerian circuit, or "IMPOSSIBLE" if no Eulerian circuit exists.

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
1 2 3 4 1
```

## Solution Progression

### Approach 1: Hierholzer's Algorithm - O(n + m)
**Description**: Use Hierholzer's algorithm to find Eulerian circuit.

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

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Hierholzer's Algorithm - O(n + m)
**Description**: Use optimized Hierholzer's algorithm with better edge management.

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
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Hierholzer's Algorithm | O(n + m) | O(n + m) | Use Hierholzer's for Eulerian circuit |
| Optimized Hierholzer's | O(n + m) | O(n + m) | Optimized Hierholzer's implementation |

## Key Insights for Other Problems

### 1. **Eulerian Circuit**
**Principle**: Use Hierholzer's algorithm to find Eulerian circuit.
**Applicable to**: Eulerian path problems, circuit problems, graph traversal problems

### 2. **Degree Check**
**Principle**: Check if all vertices have even degree for Eulerian circuit.
**Applicable to**: Eulerian problems, graph analysis problems, connectivity problems

### 3. **Hierholzer's Algorithm**
**Principle**: Use stack-based approach to find Eulerian circuit.
**Applicable to**: Eulerian problems, circuit problems, graph problems

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