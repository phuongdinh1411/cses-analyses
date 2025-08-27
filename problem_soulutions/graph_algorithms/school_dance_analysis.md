# CSES School Dance - Problem Analysis

## Problem Statement
Given n boys and m girls, where each boy can dance with certain girls, find the maximum number of boys and girls that can be matched for dancing.

### Input
The first input line has two integers n and m: the number of boys and girls.
Then there are n lines describing the preferences. The i-th line has k integers: the girls that boy i can dance with.

### Output
Print the maximum number of boys and girls that can be matched.

### Constraints
- 1 ≤ n,m ≤ 500
- 1 ≤ k ≤ m

### Example
```
Input:
3 3
1 2
2 3
1 3

Output:
3
```

## Solution Progression

### Approach 1: Maximum Bipartite Matching - O(n * m * max_flow)
**Description**: Use maximum flow to find maximum bipartite matching.

```python
def school_dance_naive(n, m, preferences):
    # Build bipartite graph
    # Source -> Boys -> Girls -> Sink
    total_nodes = 2 + n + m  # source + boys + girls + sink
    source = 0
    sink = total_nodes - 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys (capacity 1)
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls (capacity 1)
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink (capacity 1)
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs(source, sink):
        # Find augmenting path using BFS
        parent = [-1] * total_nodes
        parent[source] = source
        queue = [source]
        
        while queue:
            current = queue.pop(0)
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0  # No augmenting path found
        
        # Find bottleneck capacity
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(source, sink)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Bipartite Matching - O(n * m * max_flow)
**Description**: Use optimized Ford-Fulkerson algorithm for bipartite matching.

```python
def school_dance_optimized(n, m, preferences):
    from collections import deque
    
    # Build bipartite graph
    total_nodes = 2 + n + m
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs(source, sink):
        parent = [-1] * total_nodes
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0
        
        # Find bottleneck and update residual graph
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(source, sink)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

**Why this improvement works**: We use optimized Ford-Fulkerson algorithm to find maximum bipartite matching efficiently.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
preferences = []
for _ in range(n):
    line = list(map(int, input().split()))
    k = line[0]
    girls = line[1:]
    preferences.append(girls)

def find_maximum_matching(n, m, preferences):
    # Build bipartite graph
    total_nodes = 2 + n + m  # source + boys + girls + sink
    source = 0
    sink = total_nodes - 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys (capacity 1)
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls (capacity 1)
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink (capacity 1)
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs(source, sink):
        # Find augmenting path using BFS
        parent = [-1] * total_nodes
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0  # No augmenting path found
        
        # Find bottleneck capacity
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(source, sink)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow

result = find_maximum_matching(n, m, preferences)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Bipartite Matching via Max Flow | O(n * m * max_flow) | O((n+m)²) | Use max flow for bipartite matching |
| Optimized Bipartite Matching | O(n * m * max_flow) | O((n+m)²) | Optimized max flow implementation |

## Key Insights for Other Problems

### 1. **Bipartite Matching**
**Principle**: Use maximum flow to find maximum bipartite matching.
**Applicable to**: Matching problems, assignment problems, network problems

### 2. **Network Flow Reduction**
**Principle**: Reduce bipartite matching to maximum flow problem.
**Applicable to**: Matching problems, flow problems, network problems

### 3. **Assignment Problems**
**Principle**: Use bipartite matching to solve assignment problems.
**Applicable to**: Assignment problems, matching problems, optimization problems

## Notable Techniques

### 1. **Bipartite Graph Construction**
```python
def build_bipartite_graph(n, m, preferences):
    total_nodes = 2 + n + m
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    return adj, capacity, source, sink
```

### 2. **Maximum Flow for Matching**
```python
def max_flow_matching(n, m, adj, capacity, source, sink):
    def bfs():
        parent = [-1] * len(adj)
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0
        
        # Find bottleneck
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    max_flow = 0
    while True:
        flow = bfs()
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

### 3. **Matching Extraction**
```python
def extract_matching(n, m, adj, capacity):
    matches = []
    for boy in range(1, n + 1):
        for girl in range(1, m + 1):
            girl_node = n + girl
            if capacity[girl_node][boy] > 0:  # Flow in reverse direction
                matches.append((boy, girl))
    return matches
```

## Problem-Solving Framework

1. **Identify problem type**: This is a bipartite matching problem
2. **Choose approach**: Use maximum flow to find maximum matching
3. **Build bipartite graph**: Create network with source, boys, girls, and sink
4. **Set capacities**: Assign unit capacities for matching constraints
5. **Find maximum flow**: Use Ford-Fulkerson algorithm
6. **Extract matching**: Convert flow to matching pairs
7. **Return result**: Output maximum number of matches

---

*This analysis shows how to efficiently find maximum bipartite matching using maximum flow algorithm.* 