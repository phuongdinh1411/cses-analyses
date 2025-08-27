# CSES Nearest Shops - Problem Analysis

## Problem Statement
Given a tree with n nodes and q queries, for each query find the nearest shop to a given node. Each node is either a shop or not.

### Input
The first input line has two integers n and q: the number of nodes and queries.
Then there are n-1 lines describing the tree edges. Each line has two integers a and b: there is an edge between nodes a and b.
Then there are n lines with integers s_1,s_2,…,s_n: s_i=1 if node i is a shop, and s_i=0 otherwise.
Finally, there are q lines describing the queries. Each line has one integer x: find the nearest shop to node x.

### Output
Print the answer to each query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ a,b ≤ n
- 1 ≤ x ≤ n

### Example
```
Input:
5 3
1 2
2 3
3 4
4 5
1 0 1 0 1
1
3
5

Output:
1
3
5
```

## Solution Progression

### Approach 1: BFS for Each Query - O(n*q)
**Description**: Use BFS for each query to find the nearest shop.

```python
def nearest_shops_naive(n, q, edges, shops, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def find_nearest_shop(start):
        if shops[start] == 1:
            return start
        
        # BFS to find nearest shop
        from collections import deque
        queue = deque([(start, 0)])
        visited = [False] * (n + 1)
        visited[start] = True
        
        while queue:
            node, distance = queue.popleft()
            
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    if shops[neighbor] == 1:
                        return neighbor
                    queue.append((neighbor, distance + 1))
        
        return -1  # No shop found
    
    result = []
    for query in queries:
        nearest = find_nearest_shop(query)
        result.append(nearest)
    
    return result
```

**Why this is inefficient**: Each query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Multi-Source BFS - O(n + q)
**Description**: Use multi-source BFS from all shops to precompute distances.

```python
def nearest_shops_multisource(n, q, edges, shops, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Multi-source BFS from all shops
    from collections import deque
    queue = deque()
    distance = [float('inf')] * (n + 1)
    nearest_shop = [-1] * (n + 1)
    
    # Add all shops to queue
    for i in range(1, n + 1):
        if shops[i] == 1:
            queue.append(i)
            distance[i] = 0
            nearest_shop[i] = i
    
    # BFS
    while queue:
        node = queue.popleft()
        
        for neighbor in adj[node]:
            if distance[neighbor] > distance[node] + 1:
                distance[neighbor] = distance[node] + 1
                nearest_shop[neighbor] = nearest_shop[node]
                queue.append(neighbor)
    
    # Answer queries
    result = []
    for query in queries:
        result.append(nearest_shop[query])
    
    return result
```

**Why this improvement works**: Multi-source BFS precomputes the nearest shop for all nodes in O(n) time, then queries can be answered in O(1) time.

## Final Optimal Solution

```python
from collections import deque

n, q = map(int, input().split())
edges = []
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges.append((a, b))
shops = [0] + list(map(int, input().split()))
queries = []
for _ in range(q):
    x = int(input())
    queries.append(x)

def find_nearest_shops(n, q, edges, shops, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Multi-source BFS from all shops
    queue = deque()
    distance = [float('inf')] * (n + 1)
    nearest_shop = [-1] * (n + 1)
    
    # Add all shops to queue
    for i in range(1, n + 1):
        if shops[i] == 1:
            queue.append(i)
            distance[i] = 0
            nearest_shop[i] = i
    
    # BFS
    while queue:
        node = queue.popleft()
        
        for neighbor in adj[node]:
            if distance[neighbor] > distance[node] + 1:
                distance[neighbor] = distance[node] + 1
                nearest_shop[neighbor] = nearest_shop[node]
                queue.append(neighbor)
    
    # Answer queries
    result = []
    for query in queries:
        result.append(nearest_shop[query])
    
    return result

result = find_nearest_shops(n, q, edges, shops, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| BFS per Query | O(n*q) | O(n) | Simple but inefficient |
| Multi-Source BFS | O(n + q) | O(n) | Precompute all distances |

## Key Insights for Other Problems

### 1. **Multi-Source BFS**
**Principle**: Use multi-source BFS to find shortest distances from multiple sources.
**Applicable to**: Nearest neighbor problems, distance problems, graph traversal problems

### 2. **Precomputation for Queries**
**Principle**: Precompute answers for all possible queries to answer each query in O(1) time.
**Applicable to**: Query optimization problems, distance problems, graph problems

### 3. **Tree Properties**
**Principle**: Trees have unique paths between any two nodes, making distance calculations simpler.
**Applicable to**: Tree problems, path problems, distance problems

## Notable Techniques

### 1. **Multi-Source BFS Implementation**
```python
def multi_source_bfs(n, adj, sources):
    from collections import deque
    queue = deque()
    distance = [float('inf')] * (n + 1)
    
    # Add all sources to queue
    for source in sources:
        queue.append(source)
        distance[source] = 0
    
    # BFS
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if distance[neighbor] > distance[node] + 1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    
    return distance
```

### 2. **Nearest Source Tracking**
```python
def nearest_source_bfs(n, adj, sources):
    from collections import deque
    queue = deque()
    distance = [float('inf')] * (n + 1)
    nearest_source = [-1] * (n + 1)
    
    for source in sources:
        queue.append(source)
        distance[source] = 0
        nearest_source[source] = source
    
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if distance[neighbor] > distance[node] + 1:
                distance[neighbor] = distance[node] + 1
                nearest_source[neighbor] = nearest_source[node]
                queue.append(neighbor)
    
    return distance, nearest_source
```

### 3. **Query Processing**
```python
def process_queries(nearest_source, queries):
    result = []
    for query in queries:
        result.append(nearest_source[query])
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a nearest neighbor problem on a tree
2. **Choose approach**: Use multi-source BFS for efficient preprocessing
3. **Initialize data structure**: Build adjacency list from edges
4. **Precompute distances**: Run multi-source BFS from all shops
5. **Track nearest sources**: Keep track of which shop is nearest to each node
6. **Process queries**: Answer each query in O(1) time using precomputed results
7. **Return result**: Output answers for all queries

---

*This analysis shows how to efficiently find nearest shops using multi-source BFS.* 