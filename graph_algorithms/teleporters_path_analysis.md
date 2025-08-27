# CSES Teleporters Path - Problem Analysis

## Problem Statement
Given a directed graph with n nodes and m edges, find a path that visits every edge exactly once (Eulerian trail).

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge from node a to node b.

### Output
Print the nodes in the order they are visited in the Eulerian trail, or "IMPOSSIBLE" if no Eulerian trail exists.

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

### Approach 1: Hierholzer's Algorithm for Eulerian Trail - O(n + m)
**Description**: Use Hierholzer's algorithm to find Eulerian trail.

```python
def teleporters_path_naive(n, m, edges):
    # Check if Eulerian trail exists
    # All vertices except start and end must have in_degree = out_degree
    # Start vertex: out_degree = in_degree + 1
    # End vertex: in_degree = out_degree + 1
    
    in_degree = [0] * (n + 1)
    out_degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        out_degree[a] += 1
        in_degree[b] += 1
        adj[a].append(b)
    
    # Find start and end vertices
    start = None
    end = None
    
    for i in range(1, n + 1):
        if out_degree[i] == in_degree[i] + 1:
            if start is None:
                start = i
            else:
                return "IMPOSSIBLE"  # Multiple start vertices
        elif in_degree[i] == out_degree[i] + 1:
            if end is None:
                end = i
            else:
                return "IMPOSSIBLE"  # Multiple end vertices
        elif out_degree[i] != in_degree[i]:
            return "IMPOSSIBLE"  # Other vertices must have equal degrees
    
    if start is None or end is None:
        return "IMPOSSIBLE"
    
    # Hierholzer's algorithm
    def find_eulerian_trail():
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    trail = find_eulerian_trail()
    
    # Check if all edges were used
    if len(trail) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, trail))
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Eulerian Trail Algorithm - O(n + m)
**Description**: Use optimized Hierholzer's algorithm with better degree checking.

```python
def teleporters_path_optimized(n, m, edges):
    # Check if Eulerian trail exists
    in_degree = [0] * (n + 1)
    out_degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        out_degree[a] += 1
        in_degree[b] += 1
        adj[a].append(b)
    
    # Find start and end vertices
    start = None
    end = None
    
    for i in range(1, n + 1):
        diff = out_degree[i] - in_degree[i]
        if diff == 1:
            if start is None:
                start = i
            else:
                return "IMPOSSIBLE"
        elif diff == -1:
            if end is None:
                end = i
            else:
                return "IMPOSSIBLE"
        elif diff != 0:
            return "IMPOSSIBLE"
    
    if start is None or end is None:
        return "IMPOSSIBLE"
    
    # Hierholzer's algorithm
    def find_eulerian_trail():
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    trail = find_eulerian_trail()
    
    if len(trail) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, trail))
```

**Why this improvement works**: We use optimized Hierholzer's algorithm with better degree checking to find Eulerian trail efficiently.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_teleporters_path(n, m, edges):
    # Check if Eulerian trail exists
    in_degree = [0] * (n + 1)
    out_degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        out_degree[a] += 1
        in_degree[b] += 1
        adj[a].append(b)
    
    # Find start and end vertices
    start = None
    end = None
    
    for i in range(1, n + 1):
        diff = out_degree[i] - in_degree[i]
        if diff == 1:
            if start is None:
                start = i
            else:
                return "IMPOSSIBLE"
        elif diff == -1:
            if end is None:
                end = i
            else:
                return "IMPOSSIBLE"
        elif diff != 0:
            return "IMPOSSIBLE"
    
    if start is None or end is None:
        return "IMPOSSIBLE"
    
    # Hierholzer's algorithm
    def find_eulerian_trail():
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    trail = find_eulerian_trail()
    
    # Check if all edges were used
    if len(trail) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, trail))

result = find_teleporters_path(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Hierholzer's Algorithm | O(n + m) | O(n + m) | Use Hierholzer's for Eulerian trail |
| Optimized Hierholzer's | O(n + m) | O(n + m) | Optimized Hierholzer's implementation |

## Key Insights for Other Problems

### 1. **Eulerian Trail**
**Principle**: Use Hierholzer's algorithm to find Eulerian trail.
**Applicable to**: Eulerian path problems, trail problems, graph traversal problems

### 2. **Degree Check for Eulerian Trail**
**Principle**: Check degree conditions for Eulerian trail existence.
**Applicable to**: Eulerian problems, graph analysis problems, connectivity problems

### 3. **Start and End Vertex Detection**
**Principle**: Identify start and end vertices based on degree differences.
**Applicable to**: Eulerian trail problems, path problems, graph problems

## Notable Techniques

### 1. **Eulerian Trail Check**
```python
def check_eulerian_trail(n, in_degree, out_degree):
    start = None
    end = None
    
    for i in range(1, n + 1):
        diff = out_degree[i] - in_degree[i]
        if diff == 1:
            if start is None:
                start = i
            else:
                return None, None  # Multiple start vertices
        elif diff == -1:
            if end is None:
                end = i
            else:
                return None, None  # Multiple end vertices
        elif diff != 0:
            return None, None  # Invalid degrees
    
    return start, end
```

### 2. **Hierholzer's Algorithm for Trail**
```python
def hierholzer_trail(adj, start):
    path = []
    stack = [start]
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node = adj[current].pop()
            stack.append(next_node)
        else:
            path.append(stack.pop())
    
    return path[::-1]
```

### 3. **Degree Calculation**
```python
def calculate_degrees(n, edges):
    in_degree = [0] * (n + 1)
    out_degree = [0] * (n + 1)
    
    for a, b in edges:
        out_degree[a] += 1
        in_degree[b] += 1
    
    return in_degree, out_degree
```

## Problem-Solving Framework

1. **Identify problem type**: This is an Eulerian trail problem
2. **Choose approach**: Use Hierholzer's algorithm
3. **Check conditions**: Verify degree conditions for Eulerian trail
4. **Find start/end**: Identify start and end vertices
5. **Build graph**: Create adjacency list representation
6. **Find trail**: Use Hierholzer's algorithm to find Eulerian trail
7. **Verify result**: Check if all edges were used
8. **Return result**: Output trail or "IMPOSSIBLE"

---

*This analysis shows how to efficiently find Eulerian trail using Hierholzer's algorithm.* 