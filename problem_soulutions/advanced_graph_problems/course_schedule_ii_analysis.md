# CSES Course Schedule II - Problem Analysis

## Problem Statement
Given n courses and m prerequisites, find a valid order to take all courses. Each prerequisite is a pair (a,b) meaning course a must be taken before course b.

### Input
The first input line has two integers n and m: the number of courses and prerequisites.
Then there are m lines describing the prerequisites. Each line has two integers a and b: course a must be taken before course b.

### Output
Print a valid order to take all courses, or "IMPOSSIBLE" if no valid order exists.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 3
1 2
2 3
3 4

Output:
1 2 3 4
```

## Solution Progression

### Approach 1: Topological Sort with DFS - O(n + m)
**Description**: Use topological sort with DFS to find a valid course order.

```python
def course_schedule_ii_naive(n, m, prerequisites):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in prerequisites:
        adj[a].append(b)
    
    # Topological sort using DFS
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    order = []
    
    def dfs(node):
        if in_stack[node]:
            return False  # Cycle detected
        if visited[node]:
            return True
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if not dfs(neighbor):
                return False
        
        in_stack[node] = False
        order.append(node)
        return True
    
    # Try to visit all nodes
    for i in range(1, n + 1):
        if not visited[i]:
            if not dfs(i):
                return "IMPOSSIBLE"
    
    # Reverse order to get topological sort
    return order[::-1]
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Kahn's Algorithm - O(n + m)
**Description**: Use Kahn's algorithm (BFS-based topological sort) for better efficiency.

```python
def course_schedule_ii_kahn(n, m, prerequisites):
    # Build adjacency list and in-degree
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in prerequisites:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    # Add all nodes with in-degree 0
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        # Remove edges from this node
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed
    if len(order) != n:
        return "IMPOSSIBLE"
    
    return order
```

**Why this improvement works**: Kahn's algorithm is more efficient and easier to understand than DFS-based topological sort.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
prerequisites = []
for _ in range(m):
    a, b = map(int, input().split())
    prerequisites.append((a, b))

def find_course_order(n, m, prerequisites):
    # Build adjacency list and in-degree
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in prerequisites:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm
    queue = deque()
    
    # Add all nodes with in-degree 0
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        # Remove edges from this node
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed
    if len(order) != n:
        return "IMPOSSIBLE"
    
    return order

result = find_course_order(n, m, prerequisites)
if result == "IMPOSSIBLE":
    print(result)
else:
    print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS Topological Sort | O(n + m) | O(n) | Cycle detection with DFS |
| Kahn's Algorithm | O(n + m) | O(n) | BFS-based topological sort |

## Key Insights for Other Problems

### 1. **Topological Sort Properties**
**Principle**: Topological sort orders nodes so that all edges point forward, possible only in DAGs.
**Applicable to**: Dependency problems, scheduling problems, DAG problems

### 2. **Kahn's Algorithm**
**Principle**: Use BFS to iteratively remove nodes with no incoming edges.
**Applicable to**: Topological sort problems, dependency resolution, graph problems

### 3. **Cycle Detection**
**Principle**: Topological sort is impossible if the graph contains cycles.
**Applicable to**: Cycle detection problems, dependency problems, graph problems

## Notable Techniques

### 1. **Kahn's Algorithm Implementation**
```python
def kahn_algorithm(n, adj):
    from collections import deque
    
    # Calculate in-degrees
    in_degree = [0] * (n + 1)
    for i in range(1, n + 1):
        for neighbor in adj[i]:
            in_degree[neighbor] += 1
    
    # Initialize queue with nodes having in-degree 0
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Process nodes
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return order
```

### 2. **DFS Topological Sort**
```python
def dfs_topological_sort(n, adj):
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    order = []
    
    def dfs(node):
        if in_stack[node]:
            return False  # Cycle detected
        if visited[node]:
            return True
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if not dfs(neighbor):
                return False
        
        in_stack[node] = False
        order.append(node)
        return True
    
    for i in range(1, n + 1):
        if not visited[i]:
            if not dfs(i):
                return None  # Cycle detected
    
    return order[::-1]
```

### 3. **Cycle Detection**
```python
def has_cycle(n, adj):
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    
    def dfs(node):
        if in_stack[node]:
            return True  # Cycle detected
        if visited[node]:
            return False
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if dfs(neighbor):
                return True
        
        in_stack[node] = False
        return False
    
    for i in range(1, n + 1):
        if not visited[i]:
            if dfs(i):
                return True
    
    return False
```

## Problem-Solving Framework

1. **Identify problem type**: This is a topological sort problem with dependency constraints
2. **Choose approach**: Use Kahn's algorithm for efficient topological sort
3. **Initialize data structure**: Build adjacency list and calculate in-degrees
4. **Find starting nodes**: Add all nodes with in-degree 0 to queue
5. **Process nodes**: Remove nodes and update in-degrees of neighbors
6. **Check completion**: Verify all nodes were processed
7. **Return result**: Output topological order or "IMPOSSIBLE"

---

*This analysis shows how to efficiently solve course scheduling using Kahn's algorithm for topological sort.* 