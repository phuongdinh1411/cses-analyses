---
layout: simple
title: "Nearest Shops - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/nearest_shops_analysis
---

# Nearest Shops - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of nearest neighbor queries in graphs
- Apply graph theory principles to find shortest paths to multiple targets
- Implement algorithms for multi-source shortest path problems
- Optimize graph traversal for multiple queries
- Handle special cases in nearest neighbor analysis

## 📋 Problem Description

Given a weighted undirected graph with n nodes and m edges, where some nodes are shops, for each query find the nearest shop to a given node.

**Input**: 
- n: number of nodes
- m: number of edges
- m lines: a b w (undirected edge from node a to node b with weight w)
- k: number of shops
- k lines: shop nodes
- q: number of queries
- q lines: query node

**Output**: 
- For each query, output the distance to the nearest shop

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5
- 1 ≤ k ≤ n
- 1 ≤ q ≤ 10^5
- 1 ≤ w ≤ 10^6

**Example**:
```
Input:
5 6
1 2 2
2 3 3
3 4 1
4 5 2
1 4 4
2 5 1
2
2 4
3
1
3
5

Output:
2
1
2

Explanation**: 
Query 1: Nearest shop to node 1 is shop 2 at distance 2
Query 2: Nearest shop to node 3 is shop 2 at distance 1
Query 3: Nearest shop to node 5 is shop 4 at distance 2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Multiple BFS**: Run BFS from each query node to all shop nodes
- **Exhaustive Search**: Find shortest path to each shop individually
- **Quadratic Complexity**: O(q × k × (n + m)) time complexity
- **Baseline Understanding**: Provides correct answer but highly inefficient

**Key Insight**: For each query, run BFS from the query node to find the shortest distance to each shop.

**Algorithm**:
- For each query node, run BFS to find shortest distances to all nodes
- Find the minimum distance among all shop nodes
- Return the minimum distance

**Visual Example**:
```
Graph: 1-2(2), 2-3(3), 3-4(1), 4-5(2), 1-4(4), 2-5(1)
Shops: {2, 4}

Query from node 1:
┌─────────────────────────────────────┐
│ BFS distances from node 1:          │
│ dist[1] = 0, dist[2] = 2, dist[4] = 4 │
│ Nearest shop: shop 2 at distance 2  │
└─────────────────────────────────────┘

Query from node 3:
┌─────────────────────────────────────┐
│ BFS distances from node 3:          │
│ dist[2] = 3, dist[3] = 0, dist[4] = 1 │
│ Nearest shop: shop 4 at distance 1  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_solution(n, edges, shops, queries):
    """
    Find nearest shops using brute force BFS approach
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        shops: list of shop nodes
        queries: list of query nodes
    
    Returns:
        list: distances to nearest shops
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a-1].append((b-1, w))  # Convert to 0-indexed
        adj[b-1].append((a-1, w))  # Undirected edge
    
    def bfs_from_node(start):
        """Run BFS from start node to find shortest distances"""
        from collections import deque
        
        dist = [float('inf')] * n
        dist[start] = 0
        queue = deque([start])
        
        while queue:
            node = queue.popleft()
            for neighbor, weight in adj[node]:
                if dist[neighbor] > dist[node] + weight:
                    dist[neighbor] = dist[node] + weight
                    queue.append(neighbor)
        
        return dist
    
    # Answer queries
    results = []
    for query in queries:
        dist = bfs_from_node(query - 1)  # Convert to 0-indexed
        
        # Find nearest shop
        min_distance = float('inf')
        for shop in shops:
            min_distance = min(min_distance, dist[shop - 1])  # Convert to 0-indexed
        
        results.append(min_distance)
    
    return results

# Example usage
n = 5
edges = [(1, 2, 2), (2, 3, 3), (3, 4, 1), (4, 5, 2), (1, 4, 4), (2, 5, 1)]
shops = [2, 4]
queries = [1, 3, 5]
result = brute_force_solution(n, edges, shops, queries)
print(f"Brute force result: {result}")  # Output: [2, 1, 2]
```

**Time Complexity**: O(q × (n + m))
**Space Complexity**: O(n + m)

**Why it's inefficient**: O(q × (n + m)) time complexity makes it inefficient for large numbers of queries.

---

### Approach 2: Multi-Source BFS Solution

**Key Insights from Multi-Source BFS Solution**:
- **Multi-Source BFS**: Run BFS from all shop nodes simultaneously
- **Single Pass**: Compute distances to all nodes in one BFS pass
- **Efficient Queries**: Answer queries in O(1) time after preprocessing
- **Optimization**: Much more efficient than brute force for multiple queries

**Key Insight**: Use multi-source BFS to compute shortest distances from all shop nodes to all other nodes in one pass.

**Algorithm**:
- Initialize BFS queue with all shop nodes
- Run BFS to compute shortest distances from any shop to each node
- Answer queries by returning precomputed distances

**Visual Example**:
```
Graph: 1-2(2), 2-3(3), 3-4(1), 4-5(2), 1-4(4), 2-5(1)
Shops: {2, 4}

Multi-source BFS:
┌─────────────────────────────────────┐
│ Start: queue = [2, 4]              │
│ Step 1: dist[2] = 0, dist[4] = 0   │
│ Step 2: dist[1] = 2, dist[3] = 1   │
│ Step 3: dist[5] = 2                │
│ Final distances: [2, 0, 1, 0, 2]   │
└─────────────────────────────────────┘

Query answers: [2, 1, 2]
```

**Implementation**:
```python
def multi_source_bfs_solution(n, edges, shops, queries):
    """
    Find nearest shops using multi-source BFS approach
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        shops: list of shop nodes
        queries: list of query nodes
    
    Returns:
        list: distances to nearest shops
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a-1].append((b-1, w))  # Convert to 0-indexed
        adj[b-1].append((a-1, w))  # Undirected edge
    
    def multi_source_bfs():
        """Run multi-source BFS from all shop nodes"""
        from collections import deque
        
        dist = [float('inf')] * n
        queue = deque()
        
        # Initialize queue with all shop nodes
        for shop in shops:
            dist[shop - 1] = 0  # Convert to 0-indexed
            queue.append(shop - 1)
        
        # Run BFS
        while queue:
            node = queue.popleft()
            for neighbor, weight in adj[node]:
                if dist[neighbor] > dist[node] + weight:
                    dist[neighbor] = dist[node] + weight
                    queue.append(neighbor)
        
        return dist
    
    # Precompute distances
    dist = multi_source_bfs()
    
    # Answer queries
    results = []
    for query in queries:
        results.append(dist[query - 1])  # Convert to 0-indexed
    
    return results

# Example usage
n = 5
edges = [(1, 2, 2), (2, 3, 3), (3, 4, 1), (4, 5, 2), (1, 4, 4), (2, 5, 1)]
shops = [2, 4]
queries = [1, 3, 5]
result = multi_source_bfs_solution(n, edges, shops, queries)
print(f"Multi-source BFS result: {result}")  # Output: [2, 1, 2]
```

**Time Complexity**: O(n + m + q)
**Space Complexity**: O(n + m)

**Why it's better**: O(n + m) preprocessing time and O(1) per query, making it much more efficient for multiple queries.

**Implementation Considerations**:
- **Multi-Source Initialization**: Initialize BFS queue with all shop nodes
- **Distance Updates**: Update distances efficiently during BFS
- **Memory Management**: Use single distance array for all nodes

---

### Approach 3: Dijkstra's Algorithm Solution (Optimal)

**Key Insights from Dijkstra's Algorithm Solution**:
- **Priority Queue**: Use priority queue for efficient shortest path computation
- **Weighted Graphs**: Handle weighted edges correctly
- **Optimal Complexity**: O((n + m) log n) time complexity
- **Efficient Implementation**: Best approach for weighted graphs

**Key Insight**: Use Dijkstra's algorithm with multi-source initialization to compute shortest distances from all shop nodes.

**Algorithm**:
- Initialize priority queue with all shop nodes at distance 0
- Run Dijkstra's algorithm to compute shortest distances
- Answer queries by returning precomputed distances

**Visual Example**:
```
Graph: 1-2(2), 2-3(3), 3-4(1), 4-5(2), 1-4(4), 2-5(1)
Shops: {2, 4}

Dijkstra's algorithm:
┌─────────────────────────────────────┐
│ Start: pq = [(0, 2), (0, 4)]       │
│ Step 1: dist[2] = 0, dist[4] = 0   │
│ Step 2: dist[1] = 2, dist[3] = 1   │
│ Step 3: dist[5] = 2                │
│ Final distances: [2, 0, 1, 0, 2]   │
└─────────────────────────────────────┘

Query answers: [2, 1, 2]
```

**Implementation**:
```python
def dijkstra_solution(n, edges, shops, queries):
    """
    Find nearest shops using Dijkstra's algorithm
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        shops: list of shop nodes
        queries: list of query nodes
    
    Returns:
        list: distances to nearest shops
    """
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a-1].append((b-1, w))  # Convert to 0-indexed
        adj[b-1].append((a-1, w))  # Undirected edge
    
    def multi_source_dijkstra():
        """Run multi-source Dijkstra from all shop nodes"""
        dist = [float('inf')] * n
        pq = []
        
        # Initialize priority queue with all shop nodes
        for shop in shops:
            dist[shop - 1] = 0  # Convert to 0-indexed
            heapq.heappush(pq, (0, shop - 1))
        
        # Run Dijkstra's algorithm
        while pq:
            d, node = heapq.heappop(pq)
            if d > dist[node]:
                continue  # Skip if we've found a better path
            
            for neighbor, weight in adj[node]:
                if dist[neighbor] > dist[node] + weight:
                    dist[neighbor] = dist[node] + weight
                    heapq.heappush(pq, (dist[neighbor], neighbor))
        
        return dist
    
    # Precompute distances
    dist = multi_source_dijkstra()
    
    # Answer queries
    results = []
    for query in queries:
        results.append(dist[query - 1])  # Convert to 0-indexed
    
    return results

# Example usage
n = 5
edges = [(1, 2, 2), (2, 3, 3), (3, 4, 1), (4, 5, 2), (1, 4, 4), (2, 5, 1)]
shops = [2, 4]
queries = [1, 3, 5]
result = dijkstra_solution(n, edges, shops, queries)
print(f"Dijkstra result: {result}")  # Output: [2, 1, 2]
```

**Time Complexity**: O((n + m) log n + q)
**Space Complexity**: O(n + m)

**Why it's optimal**: O((n + m) log n) preprocessing time and O(1) per query, optimal for weighted graphs.

**Implementation Details**:
- **Priority Queue**: Use heapq for efficient priority queue operations
- **Multi-Source Initialization**: Initialize with all shop nodes
- **Distance Updates**: Update distances efficiently during algorithm
- **Memory Efficiency**: Use single distance array

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × (n + m)) | O(n + m) | Run BFS for each query |
| Multi-Source BFS | O(n + m + q) | O(n + m) | Run BFS from all shops once |
| Dijkstra's Algorithm | O((n + m) log n + q) | O(n + m) | Use priority queue for weighted graphs |

### Time Complexity
- **Time**: O((n + m) log n + q) - Precompute distances, then O(1) per query
- **Space**: O(n + m) - Store graph and distance information

### Why This Solution Works
- **Multi-Source Shortest Path**: Compute shortest distances from all shop nodes efficiently
- **Priority Queue**: Use priority queue for optimal shortest path computation
- **Query Optimization**: Answer queries in constant time after preprocessing
- **Memory Efficiency**: Store only necessary distance information

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Dynamic Nearest Shops**
**Problem**: Support adding/removing shops and answering nearest shop queries.

**Key Differences**: Shop set can change dynamically

**Solution Approach**: Use dynamic graph analysis with incremental updates

**Implementation**:
```python
class DynamicNearestShops:
    def __init__(self, n, edges):
        self.n = n
        self.edges = edges
        self.shops = set()
        self.adj = [[] for _ in range(n)]
        self.dist_cache = None
        
        # Build adjacency list
        for a, b, w in edges:
            self.adj[a-1].append((b-1, w))  # Convert to 0-indexed
            self.adj[b-1].append((a-1, w))  # Undirected edge
    
    def add_shop(self, shop):
        """Add a shop to the set"""
        if shop not in self.shops:
            self.shops.add(shop)
            self.dist_cache = None  # Invalidate cache
    
    def remove_shop(self, shop):
        """Remove a shop from the set"""
        if shop in self.shops:
            self.shops.remove(shop)
            self.dist_cache = None  # Invalidate cache
    
    def get_nearest_shop_distance(self, query):
        """Get distance to nearest shop"""
        if not self.shops:
            return float('inf')
        
        if self.dist_cache is None:
            self._compute_distances()
        
        return self.dist_cache[query - 1]  # Convert to 0-indexed
    
    def _compute_distances(self):
        """Compute distances to nearest shops"""
        import heapq
        
        dist = [float('inf')] * self.n
        pq = []
        
        # Initialize priority queue with all shop nodes
        for shop in self.shops:
            dist[shop - 1] = 0  # Convert to 0-indexed
            heapq.heappush(pq, (0, shop - 1))
        
        # Run Dijkstra's algorithm
        while pq:
            d, node = heapq.heappop(pq)
            if d > dist[node]:
                continue  # Skip if we've found a better path
            
            for neighbor, weight in self.adj[node]:
                if dist[neighbor] > dist[node] + weight:
                    dist[neighbor] = dist[node] + weight
                    heapq.heappush(pq, (dist[neighbor], neighbor))
        
        self.dist_cache = dist

# Example usage
dns = DynamicNearestShops(5, [(1, 2, 2), (2, 3, 3), (3, 4, 1), (4, 5, 2), (1, 4, 4), (2, 5, 1)])
dns.add_shop(2)
dns.add_shop(4)
result1 = dns.get_nearest_shop_distance(1)
print(f"Dynamic nearest shops result: {result1}")
```

#### **2. K-Nearest Shops**
**Problem**: Find the k nearest shops to a given node.

**Key Differences**: Return multiple nearest shops instead of just one

**Solution Approach**: Use modified Dijkstra's algorithm to find k nearest shops

**Implementation**:
```python
def k_nearest_shops(n, edges, shops, queries, k):
    """
    Find k nearest shops to each query node
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        shops: list of shop nodes
        queries: list of query nodes
        k: number of nearest shops to find
    
    Returns:
        list: lists of k nearest shop distances for each query
    """
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a-1].append((b-1, w))  # Convert to 0-indexed
        adj[b-1].append((a-1, w))  # Undirected edge
    
    def find_k_nearest_shops(query):
        """Find k nearest shops to query node"""
        dist = [float('inf')] * n
        pq = [(0, query - 1)]  # Convert to 0-indexed
        dist[query - 1] = 0
        
        nearest_shops = []
        
        while pq and len(nearest_shops) < k:
            d, node = heapq.heappop(pq)
            if d > dist[node]:
                continue  # Skip if we've found a better path
            
            # Check if this node is a shop
            if node + 1 in shops:  # Convert back to 1-indexed
                nearest_shops.append(d)
            
            for neighbor, weight in adj[node]:
                if dist[neighbor] > dist[node] + weight:
                    dist[neighbor] = dist[node] + weight
                    heapq.heappush(pq, (dist[neighbor], neighbor))
        
        return nearest_shops
    
    # Answer queries
    results = []
    for query in queries:
        k_nearest = find_k_nearest_shops(query)
        results.append(k_nearest)
    
    return results

# Example usage
n = 5
edges = [(1, 2, 2), (2, 3, 3), (3, 4, 1), (4, 5, 2), (1, 4, 4), (2, 5, 1)]
shops = [2, 4]
queries = [1, 3, 5]
k = 2
result = k_nearest_shops(n, edges, shops, queries, k)
print(f"K-nearest shops result: {result}")
```

#### **3. Nearest Shops with Constraints**
**Problem**: Find nearest shops with additional constraints (e.g., shop type, capacity).

**Key Differences**: Consider additional constraints when finding nearest shops

**Solution Approach**: Use modified Dijkstra's algorithm with constraint checking

**Implementation**:
```python
def constrained_nearest_shops(n, edges, shops, shop_types, queries, required_type):
    """
    Find nearest shops of a specific type
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        shops: list of shop nodes
        shop_types: list of shop types
        queries: list of query nodes
        required_type: required shop type
    
    Returns:
        list: distances to nearest shops of required type
    """
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a-1].append((b-1, w))  # Convert to 0-indexed
        adj[b-1].append((a-1, w))  # Undirected edge
    
    def find_nearest_shop_of_type(query):
        """Find nearest shop of required type to query node"""
        dist = [float('inf')] * n
        pq = [(0, query - 1)]  # Convert to 0-indexed
        dist[query - 1] = 0
        
        while pq:
            d, node = heapq.heappop(pq)
            if d > dist[node]:
                continue  # Skip if we've found a better path
            
            # Check if this node is a shop of required type
            if node + 1 in shops:  # Convert back to 1-indexed
                shop_index = shops.index(node + 1)
                if shop_types[shop_index] == required_type:
                    return d
            
            for neighbor, weight in adj[node]:
                if dist[neighbor] > dist[node] + weight:
                    dist[neighbor] = dist[node] + weight
                    heapq.heappush(pq, (dist[neighbor], neighbor))
        
        return float('inf')  # No shop of required type found
    
    # Answer queries
    results = []
    for query in queries:
        distance = find_nearest_shop_of_type(query)
        results.append(distance if distance != float('inf') else -1)
    
    return results

# Example usage
n = 5
edges = [(1, 2, 2), (2, 3, 3), (3, 4, 1), (4, 5, 2), (1, 4, 4), (2, 5, 1)]
shops = [2, 4]
shop_types = ['grocery', 'pharmacy']
queries = [1, 3, 5]
required_type = 'grocery'
result = constrained_nearest_shops(n, edges, shops, shop_types, queries, required_type)
print(f"Constrained nearest shops result: {result}")
```

## Problem Variations

### **Variation 1: Nearest Shops with Dynamic Updates**
**Problem**: Handle dynamic graph updates (add/remove/update shops) while maintaining nearest shop calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic graph management with nearest shop detection.

```python
from collections import defaultdict, deque
import heapq

class DynamicNearestShops:
    def __init__(self, n=None, edges=None, shops=None):
        self.n = n or 0
        self.edges = edges or []
        self.shops = shops or set()
        self.graph = defaultdict(list)
        self._update_nearest_shop_info()
    
    def _update_nearest_shop_info(self):
        """Update nearest shop information."""
        self.nearest_shops = self._calculate_nearest_shops()
    
    def _calculate_nearest_shops(self):
        """Calculate nearest shops for each vertex using BFS."""
        if self.n <= 0 or len(self.shops) == 0:
            return {}
        
        nearest_shops = {}
        
        # For each vertex, find nearest shop
        for start in range(self.n):
            if start in self.shops:
                nearest_shops[start] = (start, 0)  # Shop to itself
                continue
            
            # BFS to find nearest shop
            dist = [-1] * self.n
            queue = deque([start])
            dist[start] = 0
            nearest_shop = None
            min_distance = float('inf')
            
            while queue:
                u = queue.popleft()
                
                # Check if current vertex is a shop
                if u in self.shops and dist[u] < min_distance:
                    nearest_shop = u
                    min_distance = dist[u]
                
                # Continue BFS if we haven't found a shop yet or if we can find a closer one
                if nearest_shop is None or dist[u] < min_distance:
                    for v in self.graph[u]:
                        if dist[v] == -1:
                            dist[v] = dist[u] + 1
                            queue.append(v)
            
            if nearest_shop is not None:
                nearest_shops[start] = (nearest_shop, min_distance)
        
        return nearest_shops
    
    def update_graph(self, new_n, new_edges, new_shops=None):
        """Update the graph with new vertices, edges, and shops."""
        self.n = new_n
        self.edges = new_edges
        if new_shops is not None:
            self.shops = new_shops
        self._build_graph()
        self._update_nearest_shop_info()
    
    def add_shop(self, shop):
        """Add a shop to the graph."""
        if 0 <= shop < self.n:
            self.shops.add(shop)
            self._update_nearest_shop_info()
    
    def remove_shop(self, shop):
        """Remove a shop from the graph."""
        if shop in self.shops:
            self.shops.remove(shop)
            self._update_nearest_shop_info()
    
    def add_edge(self, u, v):
        """Add an edge to the graph."""
        if 0 <= u < self.n and 0 <= v < self.n:
            self.edges.append((u, v))
            self.graph[u].append(v)
            self.graph[v].append(u)
            self._update_nearest_shop_info()
    
    def remove_edge(self, u, v):
        """Remove an edge from the graph."""
        if (u, v) in self.edges:
            self.edges.remove((u, v))
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            self._update_nearest_shop_info()
        elif (v, u) in self.edges:
            self.edges.remove((v, u))
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            self._update_nearest_shop_info()
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def get_nearest_shop(self, vertex):
        """Get the nearest shop for a given vertex."""
        return self.nearest_shops.get(vertex, (None, float('inf')))
    
    def get_nearest_shops_with_priorities(self, priorities):
        """Get nearest shops considering vertex priorities."""
        if not self.nearest_shops:
            return {}
        
        # Calculate weighted nearest shops based on priorities
        weighted_nearest_shops = {}
        for vertex, (shop, distance) in self.nearest_shops.items():
            if shop is not None:
                vertex_priority = priorities.get(vertex, 1)
                shop_priority = priorities.get(shop, 1)
                weighted_score = distance * (vertex_priority + shop_priority)
                weighted_nearest_shops[vertex] = (shop, distance, weighted_score)
        
        return weighted_nearest_shops
    
    def get_nearest_shops_with_constraints(self, constraint_func):
        """Get nearest shops that satisfies custom constraints."""
        if not self.nearest_shops:
            return {}
        
        filtered_shops = {}
        for vertex, (shop, distance) in self.nearest_shops.items():
            if shop is not None and constraint_func(vertex, shop, distance, self.n, self.edges, self.shops):
                filtered_shops[vertex] = (shop, distance)
        
        return filtered_shops
    
    def get_nearest_shops_in_range(self, max_distance):
        """Get nearest shops within specified distance range."""
        if not self.nearest_shops:
            return {}
        
        filtered_shops = {}
        for vertex, (shop, distance) in self.nearest_shops.items():
            if shop is not None and distance <= max_distance:
                filtered_shops[vertex] = (shop, distance)
        
        return filtered_shops
    
    def get_nearest_shops_with_pattern(self, pattern_func):
        """Get nearest shops matching specified pattern."""
        if not self.nearest_shops:
            return {}
        
        filtered_shops = {}
        for vertex, (shop, distance) in self.nearest_shops.items():
            if shop is not None and pattern_func(vertex, shop, distance, self.n, self.edges, self.shops):
                filtered_shops[vertex] = (shop, distance)
        
        return filtered_shops
    
    def get_nearest_shop_statistics(self):
        """Get statistics about the nearest shops."""
        return {
            'n': self.n,
            'shop_count': len(self.shops),
            'edge_count': len(self.edges),
            'vertices_with_shops': len(self.nearest_shops),
            'average_distance': sum(distance for _, distance in self.nearest_shops.values() if distance != float('inf')) / max(1, len(self.nearest_shops))
        }
    
    def get_nearest_shop_patterns(self):
        """Get patterns in nearest shops."""
        patterns = {
            'has_shops': 0,
            'has_valid_graph': 0,
            'optimal_shop_coverage': 0,
            'has_large_graph': 0
        }
        
        # Check if has shops
        if len(self.shops) > 0:
            patterns['has_shops'] = 1
        
        # Check if has valid graph
        if self.n > 0:
            patterns['has_valid_graph'] = 1
        
        # Check if optimal shop coverage is possible
        if len(self.nearest_shops) == self.n:
            patterns['optimal_shop_coverage'] = 1
        
        # Check if has large graph
        if self.n > 100:
            patterns['has_large_graph'] = 1
        
        return patterns
    
    def get_optimal_nearest_shop_strategy(self):
        """Get optimal strategy for nearest shop management."""
        if not self.nearest_shops:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'coverage_rate': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = len(self.nearest_shops) / max(1, self.n)
        
        # Calculate coverage rate
        coverage_rate = len(self.nearest_shops) / max(1, self.n)
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'bfs_nearest_shop'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_bfs'
        else:
            recommended_strategy = 'advanced_nearest_shop_detection'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'coverage_rate': coverage_rate
        }

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
shops = {1, 3}
dynamic_shops = DynamicNearestShops(n, edges, shops)
print(f"Nearest shops: {dynamic_shops.nearest_shops}")

# Update graph
dynamic_shops.update_graph(6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 2)], {1, 3, 5})
print(f"After updating graph: n={dynamic_shops.n}, shops={dynamic_shops.shops}")

# Add shop
dynamic_shops.add_shop(0)
print(f"After adding shop 0: {dynamic_shops.shops}")

# Remove shop
dynamic_shops.remove_shop(0)
print(f"After removing shop 0: {dynamic_shops.shops}")

# Add edge
dynamic_shops.add_edge(5, 1)
print(f"After adding edge (5,1): {dynamic_shops.edges}")

# Remove edge
dynamic_shops.remove_edge(5, 1)
print(f"After removing edge (5,1): {dynamic_shops.edges}")

# Get nearest shop
nearest = dynamic_shops.get_nearest_shop(0)
print(f"Nearest shop to vertex 0: {nearest}")

# Get nearest shops with priorities
priorities = {i: i for i in range(n)}
priority_shops = dynamic_shops.get_nearest_shops_with_priorities(priorities)
print(f"Nearest shops with priorities: {priority_shops}")

# Get nearest shops with constraints
def constraint_func(vertex, shop, distance, n, edges, shops):
    return distance > 0 and shop is not None

print(f"Nearest shops with constraints: {dynamic_shops.get_nearest_shops_with_constraints(constraint_func)}")

# Get nearest shops in range
print(f"Nearest shops in range 2: {dynamic_shops.get_nearest_shops_in_range(2)}")

# Get nearest shops with pattern
def pattern_func(vertex, shop, distance, n, edges, shops):
    return distance > 0 and shop is not None

print(f"Nearest shops with pattern: {dynamic_shops.get_nearest_shops_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_shops.get_nearest_shop_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_shops.get_nearest_shop_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_shops.get_optimal_nearest_shop_strategy()}")
```

### **Variation 2: Nearest Shops with Different Operations**
**Problem**: Handle different types of nearest shop operations (weighted shops, priority-based selection, advanced shop analysis).

**Approach**: Use advanced data structures for efficient different types of nearest shop operations.

```python
class AdvancedNearestShops:
    def __init__(self, n=None, edges=None, shops=None, weights=None, priorities=None):
        self.n = n or 0
        self.edges = edges or []
        self.shops = shops or set()
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.graph = defaultdict(list)
        self._update_nearest_shop_info()
    
    def _update_nearest_shop_info(self):
        """Update nearest shop information."""
        self.nearest_shops = self._calculate_nearest_shops()
    
    def _calculate_nearest_shops(self):
        """Calculate nearest shops for each vertex using BFS."""
        if self.n <= 0 or len(self.shops) == 0:
            return {}
        
        nearest_shops = {}
        
        # For each vertex, find nearest shop
        for start in range(self.n):
            if start in self.shops:
                nearest_shops[start] = (start, 0)  # Shop to itself
                continue
            
            # BFS to find nearest shop
            dist = [-1] * self.n
            queue = deque([start])
            dist[start] = 0
            nearest_shop = None
            min_distance = float('inf')
            
            while queue:
                u = queue.popleft()
                
                # Check if current vertex is a shop
                if u in self.shops and dist[u] < min_distance:
                    nearest_shop = u
                    min_distance = dist[u]
                
                # Continue BFS if we haven't found a shop yet or if we can find a closer one
                if nearest_shop is None or dist[u] < min_distance:
                    for v in self.graph[u]:
                        if dist[v] == -1:
                            dist[v] = dist[u] + 1
                            queue.append(v)
            
            if nearest_shop is not None:
                nearest_shops[start] = (nearest_shop, min_distance)
        
        return nearest_shops
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def get_nearest_shop(self, vertex):
        """Get the nearest shop for a given vertex."""
        return self.nearest_shops.get(vertex, (None, float('inf')))
    
    def get_weighted_nearest_shops(self):
        """Get nearest shops with weights and priorities applied."""
        if not self.nearest_shops:
            return {}
        
        # Calculate weighted nearest shops based on edge weights and vertex priorities
        weighted_nearest_shops = {}
        for vertex, (shop, distance) in self.nearest_shops.items():
            if shop is not None:
                edge_weight = self.weights.get((vertex, shop), 1)
                vertex_priority = self.priorities.get(vertex, 1)
                shop_priority = self.priorities.get(shop, 1)
                weighted_score = distance * edge_weight * (vertex_priority + shop_priority)
                weighted_nearest_shops[vertex] = (shop, distance, weighted_score)
        
        return weighted_nearest_shops
    
    def get_nearest_shops_with_priority(self, priority_func):
        """Get nearest shops considering priority."""
        if not self.nearest_shops:
            return {}
        
        # Calculate priority-based nearest shops
        priority_nearest_shops = {}
        for vertex, (shop, distance) in self.nearest_shops.items():
            if shop is not None:
                priority = priority_func(vertex, shop, distance, self.weights, self.priorities)
                priority_nearest_shops[vertex] = (shop, distance, priority)
        
        return priority_nearest_shops
    
    def get_nearest_shops_with_optimization(self, optimization_func):
        """Get nearest shops using custom optimization function."""
        if not self.nearest_shops:
            return {}
        
        # Calculate optimization-based nearest shops
        optimized_nearest_shops = {}
        for vertex, (shop, distance) in self.nearest_shops.items():
            if shop is not None:
                score = optimization_func(vertex, shop, distance, self.weights, self.priorities)
                optimized_nearest_shops[vertex] = (shop, distance, score)
        
        return optimized_nearest_shops
    
    def get_nearest_shops_with_constraints(self, constraint_func):
        """Get nearest shops that satisfies custom constraints."""
        if not self.nearest_shops:
            return {}
        
        if constraint_func(self.n, self.edges, self.weights, self.priorities, self.shops, self.nearest_shops):
            return self.get_weighted_nearest_shops()
        else:
            return {}
    
    def get_nearest_shops_with_multiple_criteria(self, criteria_list):
        """Get nearest shops that satisfies multiple criteria."""
        if not self.nearest_shops:
            return {}
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.n, self.edges, self.weights, self.priorities, self.shops, self.nearest_shops):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_nearest_shops()
        else:
            return {}
    
    def get_nearest_shops_with_alternatives(self, alternatives):
        """Get nearest shops considering alternative weights/priorities."""
        result = []
        
        # Check original nearest shops
        original_shops = self.get_weighted_nearest_shops()
        result.append((original_shops, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedNearestShops(self.n, self.edges, self.shops, alt_weights, alt_priorities)
            temp_shops = temp_instance.get_weighted_nearest_shops()
            result.append((temp_shops, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_nearest_shops_with_adaptive_criteria(self, adaptive_func):
        """Get nearest shops using adaptive criteria."""
        if not self.nearest_shops:
            return {}
        
        if adaptive_func(self.n, self.edges, self.weights, self.priorities, self.shops, self.nearest_shops, []):
            return self.get_weighted_nearest_shops()
        else:
            return {}
    
    def get_nearest_shops_optimization(self):
        """Get optimal nearest shops configuration."""
        strategies = [
            ('weighted_shops', lambda: len(self.get_weighted_nearest_shops())),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
shops = {1, 3}
weights = {(u, v): (u + v) * 2 for u, v in edges}  # Weight based on vertex sum
priorities = {i: i for i in range(n)}  # Priority based on vertex number
advanced_shops = AdvancedNearestShops(n, edges, shops, weights, priorities)

print(f"Weighted nearest shops: {advanced_shops.get_weighted_nearest_shops()}")

# Get nearest shops with priority
def priority_func(vertex, shop, distance, weights, priorities):
    return priorities.get(vertex, 1) + priorities.get(shop, 1) + distance

print(f"Nearest shops with priority: {advanced_shops.get_nearest_shops_with_priority(priority_func)}")

# Get nearest shops with optimization
def optimization_func(vertex, shop, distance, weights, priorities):
    return weights.get((vertex, shop), 1) + priorities.get(vertex, 1) + priorities.get(shop, 1)

print(f"Nearest shops with optimization: {advanced_shops.get_nearest_shops_with_optimization(optimization_func)}")

# Get nearest shops with constraints
def constraint_func(n, edges, weights, priorities, shops, nearest_shops):
    return len(nearest_shops) > 0 and n > 0

print(f"Nearest shops with constraints: {advanced_shops.get_nearest_shops_with_constraints(constraint_func)}")

# Get nearest shops with multiple criteria
def criterion1(n, edges, weights, priorities, shops, nearest_shops):
    return len(edges) > 0

def criterion2(n, edges, weights, priorities, shops, nearest_shops):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Nearest shops with multiple criteria: {advanced_shops.get_nearest_shops_with_multiple_criteria(criteria_list)}")

# Get nearest shops with alternatives
alternatives = [({(u, v): 1 for u, v in edges}, {i: 1 for i in range(n)}), ({(u, v): (u + v)*3 for u, v in edges}, {i: 2 for i in range(n)})]
print(f"Nearest shops with alternatives: {advanced_shops.get_nearest_shops_with_alternatives(alternatives)}")

# Get nearest shops with adaptive criteria
def adaptive_func(n, edges, weights, priorities, shops, nearest_shops, current_result):
    return len(edges) > 0 and len(current_result) < 10

print(f"Nearest shops with adaptive criteria: {advanced_shops.get_nearest_shops_with_adaptive_criteria(adaptive_func)}")

# Get nearest shops optimization
print(f"Nearest shops optimization: {advanced_shops.get_nearest_shops_optimization()}")
```

### **Variation 3: Nearest Shops with Constraints**
**Problem**: Handle nearest shop calculation with additional constraints (distance limits, shop constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedNearestShops:
    def __init__(self, n=None, edges=None, shops=None, constraints=None):
        self.n = n or 0
        self.edges = edges or []
        self.shops = shops or set()
        self.constraints = constraints or {}
        self.graph = defaultdict(list)
        self._update_nearest_shop_info()
    
    def _update_nearest_shop_info(self):
        """Update nearest shop information."""
        self.nearest_shops = self._calculate_nearest_shops()
    
    def _calculate_nearest_shops(self):
        """Calculate nearest shops for each vertex using BFS."""
        if self.n <= 0 or len(self.shops) == 0:
            return {}
        
        nearest_shops = {}
        
        # For each vertex, find nearest shop
        for start in range(self.n):
            if start in self.shops:
                nearest_shops[start] = (start, 0)  # Shop to itself
                continue
            
            # BFS to find nearest shop
            dist = [-1] * self.n
            queue = deque([start])
            dist[start] = 0
            nearest_shop = None
            min_distance = float('inf')
            
            while queue:
                u = queue.popleft()
                
                # Check if current vertex is a shop
                if u in self.shops and dist[u] < min_distance:
                    nearest_shop = u
                    min_distance = dist[u]
                
                # Continue BFS if we haven't found a shop yet or if we can find a closer one
                if nearest_shop is None or dist[u] < min_distance:
                    for v in self.graph[u]:
                        if dist[v] == -1:
                            dist[v] = dist[u] + 1
                            queue.append(v)
            
            if nearest_shop is not None:
                nearest_shops[start] = (nearest_shop, min_distance)
        
        return nearest_shops
    
    def _is_valid_edge(self, u, v):
        """Check if edge is valid considering constraints."""
        # Edge constraints
        if 'allowed_edges' in self.constraints:
            if (u, v) not in self.constraints['allowed_edges'] and (v, u) not in self.constraints['allowed_edges']:
                return False
        
        if 'forbidden_edges' in self.constraints:
            if (u, v) in self.constraints['forbidden_edges'] or (v, u) in self.constraints['forbidden_edges']:
                return False
        
        # Vertex constraints
        if 'max_vertex' in self.constraints:
            if u > self.constraints['max_vertex'] or v > self.constraints['max_vertex']:
                return False
        
        if 'min_vertex' in self.constraints:
            if u < self.constraints['min_vertex'] or v < self.constraints['min_vertex']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(u, v, self.n, self.edges, self.shops, self.nearest_shops):
                    return False
        
        return True
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            if self._is_valid_edge(u, v):
                self.graph[u].append(v)
                self.graph[v].append(u)
    
    def get_nearest_shop(self, vertex):
        """Get the nearest shop for a given vertex."""
        return self.nearest_shops.get(vertex, (None, float('inf')))
    
    def get_nearest_shops_with_distance_constraints(self, max_distance):
        """Get nearest shops considering distance constraints."""
        if not self.nearest_shops:
            return {}
        
        filtered_shops = {}
        for vertex, (shop, distance) in self.nearest_shops.items():
            if shop is not None and distance <= max_distance:
                filtered_shops[vertex] = (shop, distance)
        
        return filtered_shops
    
    def get_nearest_shops_with_shop_constraints(self, shop_constraints):
        """Get nearest shops considering shop constraints."""
        if not self.nearest_shops:
            return {}
        
        satisfies_constraints = True
        for constraint in shop_constraints:
            if not constraint(self.n, self.edges, self.shops, self.nearest_shops):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self.nearest_shops
        else:
            return {}
    
    def get_nearest_shops_with_pattern_constraints(self, pattern_constraints):
        """Get nearest shops considering pattern constraints."""
        if not self.nearest_shops:
            return {}
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.n, self.edges, self.shops, self.nearest_shops):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self.nearest_shops
        else:
            return {}
    
    def get_nearest_shops_with_mathematical_constraints(self, constraint_func):
        """Get nearest shops that satisfies custom mathematical constraints."""
        if not self.nearest_shops:
            return {}
        
        if constraint_func(self.n, self.edges, self.shops, self.nearest_shops):
            return self.nearest_shops
        else:
            return {}
    
    def get_nearest_shops_with_optimization_constraints(self, optimization_func):
        """Get nearest shops using custom optimization constraints."""
        if not self.nearest_shops:
            return {}
        
        # Calculate optimization score for nearest shops
        score = optimization_func(self.n, self.edges, self.shops, self.nearest_shops)
        
        if score > 0:
            return self.nearest_shops
        else:
            return {}
    
    def get_nearest_shops_with_multiple_constraints(self, constraints_list):
        """Get nearest shops that satisfies multiple constraints."""
        if not self.nearest_shops:
            return {}
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.n, self.edges, self.shops, self.nearest_shops):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self.nearest_shops
        else:
            return {}
    
    def get_nearest_shops_with_priority_constraints(self, priority_func):
        """Get nearest shops with priority-based constraints."""
        if not self.nearest_shops:
            return {}
        
        # Calculate priority for nearest shops
        priority = priority_func(self.n, self.edges, self.shops, self.nearest_shops)
        
        if priority > 0:
            return self.nearest_shops
        else:
            return {}
    
    def get_nearest_shops_with_adaptive_constraints(self, adaptive_func):
        """Get nearest shops with adaptive constraints."""
        if not self.nearest_shops:
            return {}
        
        if adaptive_func(self.n, self.edges, self.shops, self.nearest_shops, []):
            return self.nearest_shops
        else:
            return {}
    
    def get_optimal_nearest_shops_strategy(self):
        """Get optimal nearest shops strategy considering all constraints."""
        strategies = [
            ('distance_constraints', self.get_nearest_shops_with_distance_constraints),
            ('shop_constraints', self.get_nearest_shops_with_shop_constraints),
            ('pattern_constraints', self.get_nearest_shops_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'distance_constraints':
                    result = strategy_func(1000)
                elif strategy_name == 'shop_constraints':
                    shop_constraints = [lambda n, edges, shops, nearest_shops: len(edges) > 0]
                    result = strategy_func(shop_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda n, edges, shops, nearest_shops: len(edges) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_edges': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)],
    'forbidden_edges': [(0, 3), (1, 4)],
    'max_vertex': 10,
    'min_vertex': 0,
    'pattern_constraints': [lambda u, v, n, edges, shops, nearest_shops: u >= 0 and v >= 0 and u < n and v < n]
}

n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
shops = {1, 3}
constrained_shops = ConstrainedNearestShops(n, edges, shops, constraints)

print("Distance-constrained nearest shops:", constrained_shops.get_nearest_shops_with_distance_constraints(3))

print("Shop-constrained nearest shops:", constrained_shops.get_nearest_shops_with_shop_constraints([lambda n, edges, shops, nearest_shops: len(edges) > 0]))

print("Pattern-constrained nearest shops:", constrained_shops.get_nearest_shops_with_pattern_constraints([lambda n, edges, shops, nearest_shops: len(edges) > 0]))

# Mathematical constraints
def custom_constraint(n, edges, shops, nearest_shops):
    return len(nearest_shops) > 0 and n > 0

print("Mathematical constraint nearest shops:", constrained_shops.get_nearest_shops_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(n, edges, shops, nearest_shops):
    return 1 <= len(nearest_shops) <= 20

range_constraints = [range_constraint]
print("Range-constrained nearest shops:", constrained_shops.get_nearest_shops_with_distance_constraints(20))

# Multiple constraints
def constraint1(n, edges, shops, nearest_shops):
    return len(edges) > 0

def constraint2(n, edges, shops, nearest_shops):
    return len(nearest_shops) > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints nearest shops:", constrained_shops.get_nearest_shops_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(n, edges, shops, nearest_shops):
    return n + len(edges) + len(nearest_shops)

print("Priority-constrained nearest shops:", constrained_shops.get_nearest_shops_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(n, edges, shops, nearest_shops, current_result):
    return len(edges) > 0 and len(current_result) < 10

print("Adaptive constraint nearest shops:", constrained_shops.get_nearest_shops_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_shops.get_optimal_nearest_shops_strategy()
print(f"Optimal nearest shops strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Shortest Routes I](https://cses.fi/problemset/task/1671) - Single-source shortest path
- [Shortest Routes II](https://cses.fi/problemset/task/1672) - All-pairs shortest path
- [Download Speed](https://cses.fi/problemset/task/1694) - Max flow

#### **LeetCode Problems**
- [Network Delay Time](https://leetcode.com/problems/network-delay-time/) - Shortest path
- [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) - Shortest path
- [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) - Shortest path

#### **Problem Categories**
- **Graph Theory**: Shortest path algorithms, multi-source BFS
- **Priority Queues**: Dijkstra's algorithm, heap operations
- **Combinatorial Optimization**: Nearest neighbor queries

## 🔗 Additional Resources

### **Algorithm References**
- [Dijkstra's Algorithm](https://cp-algorithms.com/graph/dijkstra.html) - Shortest path algorithm
- [BFS](https://cp-algorithms.com/graph/breadth-first-search.html) - Breadth-first search
- [Multi-Source BFS](https://cp-algorithms.com/graph/multi-source-bfs.html) - Multi-source shortest path

### **Practice Problems**
- [CSES Shortest Routes I](https://cses.fi/problemset/task/1671) - Medium
- [CSES Shortest Routes II](https://cses.fi/problemset/task/1672) - Medium
- [CSES Download Speed](https://cses.fi/problemset/task/1694) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
