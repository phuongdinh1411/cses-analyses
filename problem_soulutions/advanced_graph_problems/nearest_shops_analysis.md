---
layout: simple
title: CSES Nearest Shops - Problem Analysis
permalink: /problem_soulutions/advanced_graph_problems/nearest_shops_analysis/
---

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

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Nearest Shops with Costs**
**Variation**: Each edge has a cost, find minimum cost path to nearest shop.
**Approach**: Use weighted multi-source BFS or Dijkstra's algorithm.
```python
def cost_based_nearest_shops(n, q, edges, edge_costs, shops, queries):
    # Build weighted adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        cost = edge_costs.get((a, b), 1)
        adj[a].append((b, cost))
        adj[b].append((a, cost))
    
    # Multi-source Dijkstra from all shops
    import heapq
    distance = [float('inf')] * (n + 1)
    nearest_shop = [-1] * (n + 1)
    heap = []
    
    # Add all shops to heap
    for i in range(1, n + 1):
        if shops[i] == 1:
            distance[i] = 0
            nearest_shop[i] = i
            heapq.heappush(heap, (0, i))
    
    # Dijkstra's algorithm
    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distance[node]:
            continue
        
        for neighbor, cost in adj[node]:
            new_dist = distance[node] + cost
            if new_dist < distance[neighbor]:
                distance[neighbor] = new_dist
                nearest_shop[neighbor] = nearest_shop[node]
                heapq.heappush(heap, (new_dist, neighbor))
    
    # Process queries
    result = []
    for query in queries:
        result.append(nearest_shop[query])
    
    return result
```

#### 2. **Nearest Shops with Constraints**
**Variation**: Limited budget, restricted paths, or specific shop requirements.
**Approach**: Use constraint satisfaction with modified BFS.
```python
def constrained_nearest_shops(n, q, edges, shops, budget, restricted_edges, queries):
    # Build adjacency list excluding restricted edges
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in restricted_edges and (b, a) not in restricted_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    # Multi-source BFS with budget constraint
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
    
    # BFS with budget constraint
    while queue:
        node = queue.popleft()
        if distance[node] >= budget:
            continue
        
        for neighbor in adj[node]:
            if distance[neighbor] > distance[node] + 1:
                distance[neighbor] = distance[node] + 1
                nearest_shop[neighbor] = nearest_shop[node]
                queue.append(neighbor)
    
    # Process queries
    result = []
    for query in queries:
        if distance[query] <= budget:
            result.append(nearest_shop[query])
        else:
            result.append(-1)  # No shop within budget
    
    return result
```

#### 3. **Nearest Shops with Probabilities**
**Variation**: Each shop has a probability of being open, find expected nearest shop.
**Approach**: Use probabilistic BFS or Monte Carlo simulation.
```python
def probabilistic_nearest_shops(n, q, edges, shops, shop_probabilities, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Multi-source BFS with probability tracking
    from collections import deque
    queue = deque()
    distance = [float('inf')] * (n + 1)
    nearest_shop = [-1] * (n + 1)
    shop_prob = [0.0] * (n + 1)
    
    # Add all shops to queue
    for i in range(1, n + 1):
        if shops[i] == 1:
            queue.append(i)
            distance[i] = 0
            nearest_shop[i] = i
            shop_prob[i] = shop_probabilities.get(i, 0.5)
    
    # BFS
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if distance[neighbor] > distance[node] + 1:
                distance[neighbor] = distance[node] + 1
                nearest_shop[neighbor] = nearest_shop[node]
                shop_prob[neighbor] = shop_prob[node]
                queue.append(neighbor)
    
    # Process queries
    result = []
    for query in queries:
        if nearest_shop[query] != -1:
            result.append((nearest_shop[query], shop_prob[query]))
        else:
            result.append((-1, 0.0))
    
    return result
```

#### 4. **Nearest Shops with Multiple Criteria**
**Variation**: Optimize for multiple objectives (distance, cost, probability).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_nearest_shops(n, q, edges, shops, criteria_weights, queries):
    # criteria_weights = {'distance': 0.4, 'cost': 0.3, 'probability': 0.3}
    
    def calculate_shop_score(shop_attributes):
        return (criteria_weights['distance'] * shop_attributes['distance'] + 
                criteria_weights['cost'] * shop_attributes['cost'] + 
                criteria_weights['probability'] * shop_attributes['probability'])
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Multi-source BFS
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
    
    # Process queries
    result = []
    for query in queries:
        if nearest_shop[query] != -1:
            shop_attrs = {
                'distance': distance[query],
                'cost': distance[query],  # Simplified
                'probability': 0.5  # Simplified
            }
            score = calculate_shop_score(shop_attrs)
            result.append((nearest_shop[query], score))
        else:
            result.append((-1, float('inf')))
    
    return result
```

#### 5. **Nearest Shops with Dynamic Updates**
**Variation**: Shop locations can be modified dynamically.
**Approach**: Use dynamic graph algorithms or incremental updates.
```python
class DynamicNearestShops:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.shops = [0] * (n + 1)
        self.distance_cache = None
        self.nearest_shop_cache = None
    
    def add_edge(self, a, b):
        self.adj[a].append(b)
        self.adj[b].append(a)
        self.invalidate_cache()
    
    def remove_edge(self, a, b):
        self.adj[a].remove(b)
        self.adj[b].remove(a)
        self.invalidate_cache()
    
    def add_shop(self, node):
        self.shops[node] = 1
        self.invalidate_cache()
    
    def remove_shop(self, node):
        self.shops[node] = 0
        self.invalidate_cache()
    
    def invalidate_cache(self):
        self.distance_cache = None
        self.nearest_shop_cache = None
    
    def get_nearest_shop(self, query):
        if self.distance_cache is None:
            self.compute_distances()
        return self.nearest_shop_cache[query]
    
    def compute_distances(self):
        from collections import deque
        queue = deque()
        self.distance_cache = [float('inf')] * (self.n + 1)
        self.nearest_shop_cache = [-1] * (self.n + 1)
        
        # Add all shops to queue
        for i in range(1, self.n + 1):
            if self.shops[i] == 1:
                queue.append(i)
                self.distance_cache[i] = 0
                self.nearest_shop_cache[i] = i
        
        # BFS
        while queue:
            node = queue.popleft()
            for neighbor in self.adj[node]:
                if self.distance_cache[neighbor] > self.distance_cache[node] + 1:
                    self.distance_cache[neighbor] = self.distance_cache[node] + 1
                    self.nearest_shop_cache[neighbor] = self.nearest_shop_cache[node]
                    queue.append(neighbor)
```

### Related Problems & Concepts

#### 1. **Nearest Neighbor Problems**
- **Nearest Shop**: Find closest shop to a location
- **Nearest Hospital**: Find closest hospital to a location
- **Nearest Restaurant**: Find closest restaurant to a location
- **Nearest Facility**: Find closest facility of any type

#### 2. **Graph Traversal Problems**
- **BFS**: Breadth-first search for shortest paths
- **Multi-Source BFS**: BFS from multiple starting points
- **Dijkstra's Algorithm**: Shortest path with weighted edges
- **Floyd-Warshall**: All pairs shortest paths

#### 3. **Tree Problems**
- **Tree Traversal**: Navigate tree structure
- **Tree Diameter**: Longest path in tree
- **Tree Distance**: Distance between nodes in tree
- **Tree Queries**: Query operations on trees

#### 4. **Query Processing Problems**
- **Range Queries**: Querying ranges of data
- **Point Queries**: Querying specific points
- **Batch Queries**: Processing multiple queries
- **Online Queries**: Real-time query processing

#### 5. **Distance Problems**
- **Shortest Path**: Minimum distance between nodes
- **All Pairs Shortest Path**: Shortest paths between all pairs
- **Distance Matrix**: Matrix of distances between nodes
- **Distance Queries**: Querying distances efficiently

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large graphs
- **Edge Cases**: Robust graph operations

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient graph traversal
- **Sliding Window**: Optimal subgraph problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Graph Theory**
- **Graph Properties**: Connectivity, diameter, girth
- **Tree Properties**: Unique paths, leaf nodes, internal nodes
- **Distance Metrics**: Euclidean, Manhattan, Chebyshev
- **Graph Algorithms**: BFS, DFS, Dijkstra, Floyd-Warshall

#### 2. **Optimization Theory**
- **Shortest Path**: Minimum cost paths
- **Facility Location**: Optimal facility placement
- **Network Flow**: Maximum flow, minimum cut
- **Linear Programming**: Mathematical optimization

#### 3. **Computational Geometry**
- **Nearest Neighbor**: Geometric nearest neighbor
- **Voronoi Diagrams**: Partitioning space by proximity
- **Convex Hull**: Minimum convex polygon
- **Point Location**: Locating points in subdivisions

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Graph and tree problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Graph Problems**: BFS, DFS, shortest paths
- **Tree Problems**: Tree traversal, tree queries
- **Distance Problems**: Nearest neighbor, facility location
- **Query Problems**: Range queries, point queries 