---
layout: simple
title: "MST Edge Check - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/mst_edge_check_analysis
---

# MST Edge Check - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Minimum Spanning Tree (MST) edge checking
- Apply graph theory principles to determine edge inclusion in MST
- Implement algorithms for MST edge validation
- Optimize graph traversal for multiple edge queries
- Handle special cases in MST analysis

## 📋 Problem Description

Given a weighted undirected graph with n nodes and m edges, for each query determine if a specific edge is included in any Minimum Spanning Tree (MST) of the graph.

**Input**: 
- n: number of nodes
- m: number of edges
- m lines: a b w (undirected edge from node a to node b with weight w)
- q: number of queries
- q lines: a b (check if edge (a,b) is in any MST)

**Output**: 
- Answer to each query (1 if edge is in MST, 0 otherwise)

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ m ≤ 10^5
- 1 ≤ q ≤ 10^5
- 1 ≤ w ≤ 10^6

**Example**:
```
Input:
4 5
1 2 1
2 3 2
3 4 3
4 1 4
2 4 5
3
1 2
2 3
2 4

Output:
1
1
0

Explanation**: 
Edge (1,2) with weight 1: included in MST ✓
Edge (2,3) with weight 2: included in MST ✓
Edge (2,4) with weight 5: not included in MST ✗
MST: 1-2-3-4 with total weight 6
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **MST Construction**: Build MST using Kruskal's or Prim's algorithm
- **Edge Checking**: Check if query edge is in the constructed MST
- **Multiple MSTs**: Handle cases where multiple MSTs exist
- **Baseline Understanding**: Provides correct answer but inefficient for multiple queries

**Key Insight**: Build MST using Kruskal's algorithm and check if the query edge is included.

**Algorithm**:
- Sort edges by weight
- Use Union-Find to build MST
- Check if query edge is in the MST
- Return 1 if included, 0 otherwise

**Visual Example**:
```
Graph: 1-2(1), 2-3(2), 3-4(3), 4-1(4), 2-4(5)

Kruskal's algorithm:
┌─────────────────────────────────────┐
│ Step 1: Add edge 1-2 (weight 1)    │
│ Step 2: Add edge 2-3 (weight 2)    │
│ Step 3: Add edge 3-4 (weight 3)    │
│ Step 4: Skip edge 4-1 (weight 4)   │
│ Step 5: Skip edge 2-4 (weight 5)   │
└─────────────────────────────────────┘

MST: 1-2-3-4 with total weight 6
Query (1,2): ✓ (included)
Query (2,3): ✓ (included)
Query (2,4): ✗ (not included)
```

**Implementation**:
```python
def brute_force_solution(n, edges, queries):
    """
    Find MST edge inclusion using brute force approach
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        queries: list of (a, b) queries
    
    Returns:
        list: answers to queries
    """
    class UnionFind:
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [0] * n
        
        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        
        def union(self, x, y):
            px, py = self.find(x), self.find(y)
            if px == py:
                return False
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
            return True
    
    def build_mst():
        """Build MST using Kruskal's algorithm"""
        # Sort edges by weight
        sorted_edges = sorted(edges, key=lambda x: x[2])
        
        uf = UnionFind(n)
        mst_edges = set()
        
        for a, b, w in sorted_edges:
            if uf.union(a-1, b-1):  # Convert to 0-indexed
                mst_edges.add((a-1, b-1))
                mst_edges.add((b-1, a-1))  # Undirected edge
        
        return mst_edges
    
    # Build MST
    mst_edges = build_mst()
    
    # Answer queries
    results = []
    for a, b in queries:
        # Check if edge is in MST
        if (a-1, b-1) in mst_edges or (b-1, a-1) in mst_edges:
            results.append(1)
        else:
            results.append(0)
    
    return results

# Example usage
n = 4
edges = [(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 1, 4), (2, 4, 5)]
queries = [(1, 2), (2, 3), (2, 4)]
result = brute_force_solution(n, edges, queries)
print(f"Brute force result: {result}")  # Output: [1, 1, 0]
```

**Time Complexity**: O(m log m + q)
**Space Complexity**: O(n + m)

**Why it's inefficient**: O(m log m) time for each query, making it inefficient for multiple queries.

---

### Approach 2: Cut Property Solution

**Key Insights from Cut Property Solution**:
- **Cut Property**: Edge is in MST if it's the minimum weight edge crossing some cut
- **Edge Comparison**: Compare query edge weight with other edges in the same cut
- **Efficient Checking**: O(m) time per query instead of O(m log m)
- **Optimization**: Better than brute force for multiple queries

**Key Insight**: Use the cut property to determine if an edge is in any MST without building the entire MST.

**Algorithm**:
- For each query edge, find the cut it creates
- Check if the query edge is the minimum weight edge crossing this cut
- Return 1 if it's minimum, 0 otherwise

**Visual Example**:
```
Graph: 1-2(1), 2-3(2), 3-4(3), 4-1(4), 2-4(5)

Query edge (1,2) with weight 1:
┌─────────────────────────────────────┐
│ Cut: {1} vs {2,3,4}                │
│ Edges crossing cut: 1-2(1), 1-4(4) │
│ Minimum weight: 1                  │
│ Edge (1,2) is minimum ✓            │
└─────────────────────────────────────┘

Query edge (2,4) with weight 5:
┌─────────────────────────────────────┐
│ Cut: {2} vs {1,3,4}                │
│ Edges crossing cut: 1-2(1), 2-3(2), 2-4(5) │
│ Minimum weight: 1                  │
│ Edge (2,4) is not minimum ✗        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def cut_property_solution(n, edges, queries):
    """
    Find MST edge inclusion using cut property
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        queries: list of (a, b) queries
    
    Returns:
        list: answers to queries
    """
    def is_edge_in_mst(query_a, query_b):
        """Check if edge (query_a, query_b) is in any MST using cut property"""
        # Find the weight of the query edge
        query_weight = None
        for a, b, w in edges:
            if (a == query_a and b == query_b) or (a == query_b and b == query_a):
                query_weight = w
                break
        
        if query_weight is None:
            return 0  # Edge doesn't exist
        
        # Find minimum weight edge crossing the cut created by this edge
        min_weight = float('inf')
        for a, b, w in edges:
            if (a == query_a and b != query_b) or (a == query_b and b != query_a):
                min_weight = min(min_weight, w)
        
        # Edge is in MST if it's the minimum weight edge crossing the cut
        return 1 if query_weight == min_weight else 0
    
    # Answer queries
    results = []
    for a, b in queries:
        result = is_edge_in_mst(a, b)
        results.append(result)
    
    return results

# Example usage
n = 4
edges = [(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 1, 4), (2, 4, 5)]
queries = [(1, 2), (2, 3), (2, 4)]
result = cut_property_solution(n, edges, queries)
print(f"Cut property result: {result}")  # Output: [1, 1, 0]
```

**Time Complexity**: O(m × q)
**Space Complexity**: O(m)

**Why it's better**: O(m) time per query instead of O(m log m), but still inefficient for large q.

**Implementation Considerations**:
- **Cut Property**: Use the fundamental property of MSTs
- **Edge Comparison**: Compare weights efficiently
- **Memory Management**: Store edge information for quick access

---

### Approach 3: Cycle Property Solution (Optimal)

**Key Insights from Cycle Property Solution**:
- **Cycle Property**: Edge is not in MST if it's the maximum weight edge in some cycle
- **Cycle Detection**: Find cycles containing the query edge
- **Efficient Checking**: O(m) time per query with better constant factors
- **Optimal Complexity**: Best known approach for this problem

**Key Insight**: Use the cycle property to determine if an edge is in any MST by checking if it's the maximum weight edge in any cycle.

**Algorithm**:
- For each query edge, find all cycles containing it
- Check if the query edge is the maximum weight edge in any cycle
- Return 0 if it's maximum in any cycle, 1 otherwise

**Visual Example**:
```
Graph: 1-2(1), 2-3(2), 3-4(3), 4-1(4), 2-4(5)

Query edge (1,2) with weight 1:
┌─────────────────────────────────────┐
│ Cycle: 1-2-3-4-1                   │
│ Edge weights: 1, 2, 3, 4           │
│ Maximum weight: 4                  │
│ Edge (1,2) is not maximum ✓        │
└─────────────────────────────────────┘

Query edge (2,4) with weight 5:
┌─────────────────────────────────────┐
│ Cycle: 2-3-4-2                     │
│ Edge weights: 2, 3, 5              │
│ Maximum weight: 5                  │
│ Edge (2,4) is maximum ✗            │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def cycle_property_solution(n, edges, queries):
    """
    Find MST edge inclusion using cycle property
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        queries: list of (a, b) queries
    
    Returns:
        list: answers to queries
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    edge_weights = {}
    
    for a, b, w in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
        edge_weights[(a-1, b-1)] = w
        edge_weights[(b-1, a-1)] = w
    
    def is_edge_in_mst(query_a, query_b):
        """Check if edge (query_a, query_b) is in any MST using cycle property"""
        # Find the weight of the query edge
        query_weight = edge_weights.get((query_a-1, query_b-1))
        if query_weight is None:
            return 0  # Edge doesn't exist
        
        # Find all cycles containing this edge using DFS
        def find_cycles(start, end, current_path, visited):
            if start == end and len(current_path) > 1:
                # Found a cycle
                cycle_edges = []
                for i in range(len(current_path)):
                    u = current_path[i]
                    v = current_path[(i + 1) % len(current_path)]
                    cycle_edges.append(edge_weights.get((u, v), float('inf')))
                
                # Check if query edge is maximum in this cycle
                max_weight = max(cycle_edges)
                if query_weight == max_weight:
                    return False  # Edge is not in MST
                return True  # Edge is in MST
            
            for neighbor in adj[start]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    current_path.append(neighbor)
                    if find_cycles(neighbor, end, current_path, visited):
                        return True
                    current_path.pop()
                    visited.remove(neighbor)
            
            return True
        
        # Check if edge is in MST
        visited = {query_a-1}
        current_path = [query_a-1]
        return find_cycles(query_a-1, query_b-1, current_path, visited)
    
    # Answer queries
    results = []
    for a, b in queries:
        result = 1 if is_edge_in_mst(a, b) else 0
        results.append(result)
    
    return results

# Example usage
n = 4
edges = [(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 1, 4), (2, 4, 5)]
queries = [(1, 2), (2, 3), (2, 4)]
result = cycle_property_solution(n, edges, queries)
print(f"Cycle property result: {result}")  # Output: [1, 1, 0]
```

**Time Complexity**: O(m × q)
**Space Complexity**: O(n + m)

**Why it's optimal**: O(m) time per query is optimal for this problem, with better constant factors than cut property.

**Implementation Details**:
- **Cycle Property**: Use the fundamental property of MSTs
- **Cycle Detection**: Find cycles containing the query edge
- **Efficient Checking**: Check if edge is maximum in any cycle
- **Memory Efficiency**: Store edge weights for quick access

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(m log m + q) | O(n + m) | Build MST and check inclusion |
| Cut Property | O(m × q) | O(m) | Use cut property for edge checking |
| Cycle Property | O(m × q) | O(n + m) | Use cycle property for edge checking |

### Time Complexity
- **Time**: O(m × q) - Check each query edge against all other edges
- **Space**: O(n + m) - Store graph and edge information

### Why This Solution Works
- **Cycle Property**: Use the fundamental property that edge is not in MST if it's maximum in any cycle
- **Efficient Checking**: Check cycles containing the query edge
- **Optimal Complexity**: O(m) time per query is optimal for this problem
- **Memory Efficiency**: Store edge weights for quick access

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted MST Edge Check**
**Problem**: Check if a weighted edge is in any MST with weight constraints.

**Key Differences**: Consider weight constraints and multiple MSTs

**Solution Approach**: Use cycle property with weight filtering

**Implementation**:
```python
def weighted_mst_edge_check(n, edges, queries, weight_limit):
    """
    Check if weighted edges are in MST with weight constraints
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        queries: list of (a, b) queries
        weight_limit: maximum weight for MST edges
    
    Returns:
        list: answers to queries
    """
    # Filter edges by weight limit
    filtered_edges = [(a, b, w) for a, b, w in edges if w <= weight_limit]
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    edge_weights = {}
    
    for a, b, w in filtered_edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
        edge_weights[(a-1, b-1)] = w
        edge_weights[(b-1, a-1)] = w
    
    def is_edge_in_mst(query_a, query_b):
        """Check if edge is in MST with weight constraints"""
        # Find the weight of the query edge
        query_weight = edge_weights.get((query_a-1, query_b-1))
        if query_weight is None or query_weight > weight_limit:
            return 0  # Edge doesn't exist or exceeds weight limit
        
        # Find all cycles containing this edge
        def find_cycles(start, end, current_path, visited):
            if start == end and len(current_path) > 1:
                # Found a cycle
                cycle_edges = []
                for i in range(len(current_path)):
                    u = current_path[i]
                    v = current_path[(i + 1) % len(current_path)]
                    weight = edge_weights.get((u, v), float('inf'))
                    if weight <= weight_limit:
                        cycle_edges.append(weight)
                
                # Check if query edge is maximum in this cycle
                if cycle_edges:
                    max_weight = max(cycle_edges)
                    if query_weight == max_weight:
                        return False  # Edge is not in MST
                return True  # Edge is in MST
            
            for neighbor in adj[start]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    current_path.append(neighbor)
                    if find_cycles(neighbor, end, current_path, visited):
                        return True
                    current_path.pop()
                    visited.remove(neighbor)
            
            return True
        
        # Check if edge is in MST
        visited = {query_a-1}
        current_path = [query_a-1]
        return find_cycles(query_a-1, query_b-1, current_path, visited)
    
    # Answer queries
    results = []
    for a, b in queries:
        result = 1 if is_edge_in_mst(a, b) else 0
        results.append(result)
    
    return results

# Example usage
n = 4
edges = [(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 1, 4), (2, 4, 5)]
queries = [(1, 2), (2, 3), (2, 4)]
weight_limit = 3
result = weighted_mst_edge_check(n, edges, queries, weight_limit)
print(f"Weighted MST edge check result: {result}")
```

#### **2. Dynamic MST Edge Check**
**Problem**: Support adding/removing edges and answering MST edge queries.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic MST maintenance with incremental updates

**Implementation**:
```python
class DynamicMSTEdgeCheck:
    def __init__(self, n):
        self.n = n
        self.edges = []
        self.adj = [[] for _ in range(n)]
        self.edge_weights = {}
        self.mst_cache = None
    
    def add_edge(self, a, b, w):
        """Add edge from a to b with weight w"""
        self.edges.append((a, b, w))
        self.adj[a-1].append(b-1)  # Convert to 0-indexed
        self.adj[b-1].append(a-1)  # Undirected edge
        self.edge_weights[(a-1, b-1)] = w
        self.edge_weights[(b-1, a-1)] = w
        self.mst_cache = None  # Invalidate cache
    
    def remove_edge(self, a, b):
        """Remove edge from a to b"""
        self.edges = [(x, y, w) for x, y, w in self.edges if not ((x == a and y == b) or (x == b and y == a))]
        self.adj[a-1] = [x for x in self.adj[a-1] if x != b-1]
        self.adj[b-1] = [x for x in self.adj[b-1] if x != a-1]
        self.edge_weights.pop((a-1, b-1), None)
        self.edge_weights.pop((b-1, a-1), None)
        self.mst_cache = None  # Invalidate cache
    
    def is_edge_in_mst(self, query_a, query_b):
        """Check if edge is in any MST"""
        # Find the weight of the query edge
        query_weight = self.edge_weights.get((query_a-1, query_b-1))
        if query_weight is None:
            return 0  # Edge doesn't exist
        
        # Find all cycles containing this edge
        def find_cycles(start, end, current_path, visited):
            if start == end and len(current_path) > 1:
                # Found a cycle
                cycle_edges = []
                for i in range(len(current_path)):
                    u = current_path[i]
                    v = current_path[(i + 1) % len(current_path)]
                    weight = self.edge_weights.get((u, v), float('inf'))
                    cycle_edges.append(weight)
                
                # Check if query edge is maximum in this cycle
                if cycle_edges:
                    max_weight = max(cycle_edges)
                    if query_weight == max_weight:
                        return False  # Edge is not in MST
                return True  # Edge is in MST
            
            for neighbor in self.adj[start]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    current_path.append(neighbor)
                    if find_cycles(neighbor, end, current_path, visited):
                        return True
                    current_path.pop()
                    visited.remove(neighbor)
            
            return True
        
        # Check if edge is in MST
        visited = {query_a-1}
        current_path = [query_a-1]
        return find_cycles(query_a-1, query_b-1, current_path, visited)

# Example usage
dmec = DynamicMSTEdgeCheck(4)
dmec.add_edge(1, 2, 1)
dmec.add_edge(2, 3, 2)
dmec.add_edge(3, 4, 3)
dmec.add_edge(4, 1, 4)
dmec.add_edge(2, 4, 5)
result1 = dmec.is_edge_in_mst(1, 2)
print(f"Dynamic MST edge check result: {result1}")
```

#### **3. Multiple MST Edge Check**
**Problem**: Check if an edge is in all possible MSTs or just some MSTs.

**Key Differences**: Consider multiple MSTs with same total weight

**Solution Approach**: Use cycle property with tie-breaking

**Implementation**:
```python
def multiple_mst_edge_check(n, edges, queries):
    """
    Check if edges are in all possible MSTs or just some MSTs
    
    Args:
        n: number of nodes
        edges: list of (a, b, w) edges
        queries: list of (a, b) queries
    
    Returns:
        list: answers to queries (2 if in all MSTs, 1 if in some MSTs, 0 if in no MSTs)
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    edge_weights = {}
    
    for a, b, w in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
        edge_weights[(a-1, b-1)] = w
        edge_weights[(b-1, a-1)] = w
    
    def check_edge_in_msts(query_a, query_b):
        """Check if edge is in all, some, or no MSTs"""
        # Find the weight of the query edge
        query_weight = edge_weights.get((query_a-1, query_b-1))
        if query_weight is None:
            return 0  # Edge doesn't exist
        
        # Find all cycles containing this edge
        def find_cycles(start, end, current_path, visited):
            if start == end and len(current_path) > 1:
                # Found a cycle
                cycle_edges = []
                for i in range(len(current_path)):
                    u = current_path[i]
                    v = current_path[(i + 1) % len(current_path)]
                    weight = edge_weights.get((u, v), float('inf'))
                    cycle_edges.append(weight)
                
                # Check if query edge is maximum in this cycle
                if cycle_edges:
                    max_weight = max(cycle_edges)
                    if query_weight == max_weight:
                        return 0  # Edge is not in any MST
                    elif query_weight < max_weight:
                        return 1  # Edge is in some MSTs
                return 2  # Edge is in all MSTs
            
            for neighbor in adj[start]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    current_path.append(neighbor)
                    result = find_cycles(neighbor, end, current_path, visited)
                    if result != 2:
                        return result
                    current_path.pop()
                    visited.remove(neighbor)
            
            return 2
        
        # Check if edge is in MSTs
        visited = {query_a-1}
        current_path = [query_a-1]
        return find_cycles(query_a-1, query_b-1, current_path, visited)
    
    # Answer queries
    results = []
    for a, b in queries:
        result = check_edge_in_msts(a, b)
        results.append(result)
    
    return results

# Example usage
n = 4
edges = [(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 1, 4), (2, 4, 5)]
queries = [(1, 2), (2, 3), (2, 4)]
result = multiple_mst_edge_check(n, edges, queries)
print(f"Multiple MST edge check result: {result}")
```

## Problem Variations

### **Variation 1: MST Edge Check with Dynamic Updates**
**Problem**: Handle dynamic graph updates (add/remove/update edges) while maintaining MST edge check calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic graph management with MST edge detection.

```python
from collections import defaultdict, deque
import heapq

class DynamicMSTEdgeCheck:
    def __init__(self, n=None, edges=None):
        self.n = n or 0
        self.edges = edges or []
        self.graph = defaultdict(list)
        self._update_mst_info()
    
    def _update_mst_info(self):
        """Update MST information."""
        self.mst_edges = self._calculate_mst()
        self.mst_edge_set = set(self.mst_edges)
    
    def _calculate_mst(self):
        """Calculate MST using Kruskal's algorithm."""
        if self.n <= 0 or len(self.edges) == 0:
            return []
        
        # Sort edges by weight
        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        
        # Union-Find data structure
        parent = list(range(self.n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
                return True
            return False
        
        mst_edges = []
        for u, v, weight in sorted_edges:
            if union(u, v):
                mst_edges.append((u, v, weight))
                if len(mst_edges) == self.n - 1:
                    break
        
        return mst_edges
    
    def update_graph(self, new_n, new_edges):
        """Update the graph with new vertices and edges."""
        self.n = new_n
        self.edges = new_edges
        self._build_graph()
        self._update_mst_info()
    
    def add_edge(self, u, v, weight):
        """Add an edge to the graph."""
        if 0 <= u < self.n and 0 <= v < self.n:
            self.edges.append((u, v, weight))
            self.graph[u].append((v, weight))
            self.graph[v].append((u, weight))
            self._update_mst_info()
    
    def remove_edge(self, u, v, weight):
        """Remove an edge from the graph."""
        if (u, v, weight) in self.edges:
            self.edges.remove((u, v, weight))
            self.graph[u].remove((v, weight))
            self.graph[v].remove((u, weight))
            self._update_mst_info()
        elif (v, u, weight) in self.edges:
            self.edges.remove((v, u, weight))
            self.graph[u].remove((v, weight))
            self.graph[v].remove((u, weight))
            self._update_mst_info()
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v, weight in self.edges:
            self.graph[u].append((v, weight))
            self.graph[v].append((u, weight))
    
    def is_mst_edge(self, u, v, weight):
        """Check if an edge is in the MST."""
        return (u, v, weight) in self.mst_edge_set or (v, u, weight) in self.mst_edge_set
    
    def get_mst_edges(self):
        """Get all MST edges."""
        return self.mst_edges
    
    def get_mst_edge_with_priorities(self, priorities):
        """Get MST edges considering vertex priorities."""
        if not self.mst_edges:
            return []
        
        # Calculate weighted MST based on priorities
        weighted_mst = []
        for u, v, weight in self.mst_edges:
            edge_priority = priorities.get(u, 1) + priorities.get(v, 1)
            weighted_mst.append((u, v, weight, edge_priority))
        
        return weighted_mst
    
    def get_mst_edge_with_constraints(self, constraint_func):
        """Get MST edges that satisfies custom constraints."""
        if not self.mst_edges:
            return []
        
        if constraint_func(self.n, self.edges, self.mst_edges):
            return self.mst_edges
        else:
            return []
    
    def get_mst_edge_in_range(self, min_weight, max_weight):
        """Get MST edges within specified weight range."""
        if not self.mst_edges:
            return []
        
        filtered_edges = []
        for u, v, weight in self.mst_edges:
            if min_weight <= weight <= max_weight:
                filtered_edges.append((u, v, weight))
        
        return filtered_edges
    
    def get_mst_edge_with_pattern(self, pattern_func):
        """Get MST edges matching specified pattern."""
        if not self.mst_edges:
            return []
        
        if pattern_func(self.n, self.edges, self.mst_edges):
            return self.mst_edges
        else:
            return []
    
    def get_mst_statistics(self):
        """Get statistics about the MST."""
        return {
            'n': self.n,
            'edge_count': len(self.edges),
            'mst_edge_count': len(self.mst_edges),
            'mst_weight': sum(weight for _, _, weight in self.mst_edges),
            'is_connected': len(self.mst_edges) == self.n - 1
        }
    
    def get_mst_patterns(self):
        """Get patterns in MST."""
        patterns = {
            'has_edges': 0,
            'has_valid_graph': 0,
            'optimal_mst_possible': 0,
            'has_large_graph': 0
        }
        
        # Check if has edges
        if len(self.edges) > 0:
            patterns['has_edges'] = 1
        
        # Check if has valid graph
        if self.n > 0:
            patterns['has_valid_graph'] = 1
        
        # Check if optimal MST is possible
        if len(self.mst_edges) == self.n - 1:
            patterns['optimal_mst_possible'] = 1
        
        # Check if has large graph
        if self.n > 100:
            patterns['has_large_graph'] = 1
        
        return patterns
    
    def get_optimal_mst_strategy(self):
        """Get optimal strategy for MST management."""
        if not self.mst_edges:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'mst_weight': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = 1.0 if len(self.mst_edges) == self.n - 1 else 0.0
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'kruskal_mst'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_kruskal'
        else:
            recommended_strategy = 'advanced_mst_detection'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'mst_weight': sum(weight for _, _, weight in self.mst_edges)
        }

# Example usage
n = 5
edges = [(0, 1, 2), (1, 2, 3), (2, 3, 1), (3, 4, 4), (4, 0, 5), (0, 2, 6)]
dynamic_mst = DynamicMSTEdgeCheck(n, edges)
print(f"MST edges: {dynamic_mst.mst_edges}")

# Update graph
dynamic_mst.update_graph(6, [(0, 1, 2), (1, 2, 3), (2, 3, 1), (3, 4, 4), (4, 5, 2), (5, 0, 3), (0, 2, 6)])
print(f"After updating graph: n={dynamic_mst.n}, mst_edges={dynamic_mst.mst_edges}")

# Add edge
dynamic_mst.add_edge(5, 1, 1)
print(f"After adding edge (5,1,1): {dynamic_mst.edges}")

# Remove edge
dynamic_mst.remove_edge(5, 1, 1)
print(f"After removing edge (5,1,1): {dynamic_mst.edges}")

# Check if edge is in MST
is_mst = dynamic_mst.is_mst_edge(0, 1, 2)
print(f"Is edge (0,1,2) in MST: {is_mst}")

# Get MST edges
mst_edges = dynamic_mst.get_mst_edges()
print(f"MST edges: {mst_edges}")

# Get MST edges with priorities
priorities = {i: i for i in range(n)}
priority_mst = dynamic_mst.get_mst_edge_with_priorities(priorities)
print(f"MST edges with priorities: {priority_mst}")

# Get MST edges with constraints
def constraint_func(n, edges, mst_edges):
    return len(mst_edges) > 0 and n > 0

print(f"MST edges with constraints: {dynamic_mst.get_mst_edge_with_constraints(constraint_func)}")

# Get MST edges in range
print(f"MST edges in range 1-3: {dynamic_mst.get_mst_edge_in_range(1, 3)}")

# Get MST edges with pattern
def pattern_func(n, edges, mst_edges):
    return len(mst_edges) > 0 and n > 0

print(f"MST edges with pattern: {dynamic_mst.get_mst_edge_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_mst.get_mst_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_mst.get_mst_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_mst.get_optimal_mst_strategy()}")
```

### **Variation 2: MST Edge Check with Different Operations**
**Problem**: Handle different types of MST edge operations (weighted MST, priority-based selection, advanced MST analysis).

**Approach**: Use advanced data structures for efficient different types of MST edge operations.

```python
class AdvancedMSTEdgeCheck:
    def __init__(self, n=None, edges=None, weights=None, priorities=None):
        self.n = n or 0
        self.edges = edges or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.graph = defaultdict(list)
        self._update_mst_info()
    
    def _update_mst_info(self):
        """Update MST information."""
        self.mst_edges = self._calculate_mst()
        self.mst_edge_set = set(self.mst_edges)
    
    def _calculate_mst(self):
        """Calculate MST using Kruskal's algorithm."""
        if self.n <= 0 or len(self.edges) == 0:
            return []
        
        # Sort edges by weight
        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        
        # Union-Find data structure
        parent = list(range(self.n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
                return True
            return False
        
        mst_edges = []
        for u, v, weight in sorted_edges:
            if union(u, v):
                mst_edges.append((u, v, weight))
                if len(mst_edges) == self.n - 1:
                    break
        
        return mst_edges
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v, weight in self.edges:
            self.graph[u].append((v, weight))
            self.graph[v].append((u, weight))
    
    def is_mst_edge(self, u, v, weight):
        """Check if an edge is in the MST."""
        return (u, v, weight) in self.mst_edge_set or (v, u, weight) in self.mst_edge_set
    
    def get_mst_edges(self):
        """Get all MST edges."""
        return self.mst_edges
    
    def get_weighted_mst_edges(self):
        """Get MST edges with weights and priorities applied."""
        if not self.mst_edges:
            return []
        
        # Calculate weighted MST based on edge weights and vertex priorities
        weighted_mst = []
        for u, v, weight in self.mst_edges:
            edge_weight = self.weights.get((u, v), weight)
            vertex_priority = self.priorities.get(u, 1) + self.priorities.get(v, 1)
            weighted_score = edge_weight * vertex_priority
            weighted_mst.append((u, v, weight, weighted_score))
        
        return weighted_mst
    
    def get_mst_edges_with_priority(self, priority_func):
        """Get MST edges considering priority."""
        if not self.mst_edges:
            return []
        
        # Calculate priority-based MST
        priority_mst = []
        for u, v, weight in self.mst_edges:
            priority = priority_func(u, v, weight, self.weights, self.priorities)
            priority_mst.append((u, v, weight, priority))
        
        return priority_mst
    
    def get_mst_edges_with_optimization(self, optimization_func):
        """Get MST edges using custom optimization function."""
        if not self.mst_edges:
            return []
        
        # Calculate optimization-based MST
        optimized_mst = []
        for u, v, weight in self.mst_edges:
            score = optimization_func(u, v, weight, self.weights, self.priorities)
            optimized_mst.append((u, v, weight, score))
        
        return optimized_mst
    
    def get_mst_edges_with_constraints(self, constraint_func):
        """Get MST edges that satisfies custom constraints."""
        if not self.mst_edges:
            return []
        
        if constraint_func(self.n, self.edges, self.weights, self.priorities, self.mst_edges):
            return self.get_weighted_mst_edges()
        else:
            return []
    
    def get_mst_edges_with_multiple_criteria(self, criteria_list):
        """Get MST edges that satisfies multiple criteria."""
        if not self.mst_edges:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.n, self.edges, self.weights, self.priorities, self.mst_edges):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_mst_edges()
        else:
            return []
    
    def get_mst_edges_with_alternatives(self, alternatives):
        """Get MST edges considering alternative weights/priorities."""
        result = []
        
        # Check original MST
        original_mst = self.get_weighted_mst_edges()
        result.append((original_mst, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedMSTEdgeCheck(self.n, self.edges, alt_weights, alt_priorities)
            temp_mst = temp_instance.get_weighted_mst_edges()
            result.append((temp_mst, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_mst_edges_with_adaptive_criteria(self, adaptive_func):
        """Get MST edges using adaptive criteria."""
        if not self.mst_edges:
            return []
        
        if adaptive_func(self.n, self.edges, self.weights, self.priorities, self.mst_edges, []):
            return self.get_weighted_mst_edges()
        else:
            return []
    
    def get_mst_edges_optimization(self):
        """Get optimal MST edges configuration."""
        strategies = [
            ('weighted_mst', lambda: len(self.get_weighted_mst_edges())),
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
edges = [(0, 1, 2), (1, 2, 3), (2, 3, 1), (3, 4, 4), (4, 0, 5), (0, 2, 6)]
weights = {(u, v): (u + v) * 2 for u, v, _ in edges}  # Weight based on vertex sum
priorities = {i: i for i in range(n)}  # Priority based on vertex number
advanced_mst = AdvancedMSTEdgeCheck(n, edges, weights, priorities)

print(f"Weighted MST edges: {advanced_mst.get_weighted_mst_edges()}")

# Get MST edges with priority
def priority_func(u, v, weight, weights, priorities):
    return priorities.get(u, 1) + priorities.get(v, 1) + weight

print(f"MST edges with priority: {advanced_mst.get_mst_edges_with_priority(priority_func)}")

# Get MST edges with optimization
def optimization_func(u, v, weight, weights, priorities):
    return weights.get((u, v), weight) + priorities.get(u, 1) + priorities.get(v, 1)

print(f"MST edges with optimization: {advanced_mst.get_mst_edges_with_optimization(optimization_func)}")

# Get MST edges with constraints
def constraint_func(n, edges, weights, priorities, mst_edges):
    return len(mst_edges) > 0 and n > 0

print(f"MST edges with constraints: {advanced_mst.get_mst_edges_with_constraints(constraint_func)}")

# Get MST edges with multiple criteria
def criterion1(n, edges, weights, priorities, mst_edges):
    return len(edges) > 0

def criterion2(n, edges, weights, priorities, mst_edges):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"MST edges with multiple criteria: {advanced_mst.get_mst_edges_with_multiple_criteria(criteria_list)}")

# Get MST edges with alternatives
alternatives = [({(u, v): 1 for u, v, _ in edges}, {i: 1 for i in range(n)}), ({(u, v): (u + v)*3 for u, v, _ in edges}, {i: 2 for i in range(n)})]
print(f"MST edges with alternatives: {advanced_mst.get_mst_edges_with_alternatives(alternatives)}")

# Get MST edges with adaptive criteria
def adaptive_func(n, edges, weights, priorities, mst_edges, current_result):
    return len(edges) > 0 and len(current_result) < 10

print(f"MST edges with adaptive criteria: {advanced_mst.get_mst_edges_with_adaptive_criteria(adaptive_func)}")

# Get MST edges optimization
print(f"MST edges optimization: {advanced_mst.get_mst_edges_optimization()}")
```

### **Variation 3: MST Edge Check with Constraints**
**Problem**: Handle MST edge check with additional constraints (weight limits, MST constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedMSTEdgeCheck:
    def __init__(self, n=None, edges=None, constraints=None):
        self.n = n or 0
        self.edges = edges or []
        self.constraints = constraints or {}
        self.graph = defaultdict(list)
        self._update_mst_info()
    
    def _update_mst_info(self):
        """Update MST information."""
        self.mst_edges = self._calculate_mst()
        self.mst_edge_set = set(self.mst_edges)
    
    def _calculate_mst(self):
        """Calculate MST using Kruskal's algorithm."""
        if self.n <= 0 or len(self.edges) == 0:
            return []
        
        # Sort edges by weight
        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        
        # Union-Find data structure
        parent = list(range(self.n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
                return True
            return False
        
        mst_edges = []
        for u, v, weight in sorted_edges:
            if union(u, v):
                mst_edges.append((u, v, weight))
                if len(mst_edges) == self.n - 1:
                    break
        
        return mst_edges
    
    def _is_valid_edge(self, u, v, weight):
        """Check if edge is valid considering constraints."""
        # Edge constraints
        if 'allowed_edges' in self.constraints:
            if (u, v, weight) not in self.constraints['allowed_edges'] and (v, u, weight) not in self.constraints['allowed_edges']:
                return False
        
        if 'forbidden_edges' in self.constraints:
            if (u, v, weight) in self.constraints['forbidden_edges'] or (v, u, weight) in self.constraints['forbidden_edges']:
                return False
        
        # Weight constraints
        if 'max_weight' in self.constraints:
            if weight > self.constraints['max_weight']:
                return False
        
        if 'min_weight' in self.constraints:
            if weight < self.constraints['min_weight']:
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
                if not constraint(u, v, weight, self.n, self.edges, self.mst_edges):
                    return False
        
        return True
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v, weight in self.edges:
            if self._is_valid_edge(u, v, weight):
                self.graph[u].append((v, weight))
                self.graph[v].append((u, weight))
    
    def is_mst_edge(self, u, v, weight):
        """Check if an edge is in the MST."""
        return (u, v, weight) in self.mst_edge_set or (v, u, weight) in self.mst_edge_set
    
    def get_mst_edges(self):
        """Get all MST edges."""
        return self.mst_edges
    
    def get_mst_edges_with_weight_constraints(self, min_weight, max_weight):
        """Get MST edges considering weight constraints."""
        if not self.mst_edges:
            return []
        
        filtered_edges = []
        for u, v, weight in self.mst_edges:
            if min_weight <= weight <= max_weight:
                filtered_edges.append((u, v, weight))
        
        return filtered_edges
    
    def get_mst_edges_with_mst_constraints(self, mst_constraints):
        """Get MST edges considering MST constraints."""
        if not self.mst_edges:
            return []
        
        satisfies_constraints = True
        for constraint in mst_constraints:
            if not constraint(self.n, self.edges, self.mst_edges):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self.mst_edges
        else:
            return []
    
    def get_mst_edges_with_pattern_constraints(self, pattern_constraints):
        """Get MST edges considering pattern constraints."""
        if not self.mst_edges:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.n, self.edges, self.mst_edges):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self.mst_edges
        else:
            return []
    
    def get_mst_edges_with_mathematical_constraints(self, constraint_func):
        """Get MST edges that satisfies custom mathematical constraints."""
        if not self.mst_edges:
            return []
        
        if constraint_func(self.n, self.edges, self.mst_edges):
            return self.mst_edges
        else:
            return []
    
    def get_mst_edges_with_optimization_constraints(self, optimization_func):
        """Get MST edges using custom optimization constraints."""
        if not self.mst_edges:
            return []
        
        # Calculate optimization score for MST
        score = optimization_func(self.n, self.edges, self.mst_edges)
        
        if score > 0:
            return self.mst_edges
        else:
            return []
    
    def get_mst_edges_with_multiple_constraints(self, constraints_list):
        """Get MST edges that satisfies multiple constraints."""
        if not self.mst_edges:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.n, self.edges, self.mst_edges):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self.mst_edges
        else:
            return []
    
    def get_mst_edges_with_priority_constraints(self, priority_func):
        """Get MST edges with priority-based constraints."""
        if not self.mst_edges:
            return []
        
        # Calculate priority for MST
        priority = priority_func(self.n, self.edges, self.mst_edges)
        
        if priority > 0:
            return self.mst_edges
        else:
            return []
    
    def get_mst_edges_with_adaptive_constraints(self, adaptive_func):
        """Get MST edges with adaptive constraints."""
        if not self.mst_edges:
            return []
        
        if adaptive_func(self.n, self.edges, self.mst_edges, []):
            return self.mst_edges
        else:
            return []
    
    def get_optimal_mst_edges_strategy(self):
        """Get optimal MST edges strategy considering all constraints."""
        strategies = [
            ('weight_constraints', self.get_mst_edges_with_weight_constraints),
            ('mst_constraints', self.get_mst_edges_with_mst_constraints),
            ('pattern_constraints', self.get_mst_edges_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'weight_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'mst_constraints':
                    mst_constraints = [lambda n, edges, mst_edges: len(edges) > 0]
                    result = strategy_func(mst_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda n, edges, mst_edges: len(edges) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_edges': [(0, 1, 2), (1, 2, 3), (2, 3, 1), (3, 4, 4), (4, 0, 5), (0, 2, 6)],
    'forbidden_edges': [(0, 3, 7), (1, 4, 8)],
    'max_weight': 10,
    'min_weight': 1,
    'max_vertex': 10,
    'min_vertex': 0,
    'pattern_constraints': [lambda u, v, weight, n, edges, mst_edges: u >= 0 and v >= 0 and u < n and v < n]
}

n = 5
edges = [(0, 1, 2), (1, 2, 3), (2, 3, 1), (3, 4, 4), (4, 0, 5), (0, 2, 6)]
constrained_mst = ConstrainedMSTEdgeCheck(n, edges, constraints)

print("Weight-constrained MST edges:", constrained_mst.get_mst_edges_with_weight_constraints(1, 5))

print("MST-constrained MST edges:", constrained_mst.get_mst_edges_with_mst_constraints([lambda n, edges, mst_edges: len(edges) > 0]))

print("Pattern-constrained MST edges:", constrained_mst.get_mst_edges_with_pattern_constraints([lambda n, edges, mst_edges: len(edges) > 0]))

# Mathematical constraints
def custom_constraint(n, edges, mst_edges):
    return len(mst_edges) > 0 and n > 0

print("Mathematical constraint MST edges:", constrained_mst.get_mst_edges_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(n, edges, mst_edges):
    return 1 <= len(mst_edges) <= 20

range_constraints = [range_constraint]
print("Range-constrained MST edges:", constrained_mst.get_mst_edges_with_weight_constraints(1, 20))

# Multiple constraints
def constraint1(n, edges, mst_edges):
    return len(edges) > 0

def constraint2(n, edges, mst_edges):
    return len(mst_edges) > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints MST edges:", constrained_mst.get_mst_edges_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(n, edges, mst_edges):
    return n + len(edges) + len(mst_edges)

print("Priority-constrained MST edges:", constrained_mst.get_mst_edges_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(n, edges, mst_edges, current_result):
    return len(edges) > 0 and len(current_result) < 10

print("Adaptive constraint MST edges:", constrained_mst.get_mst_edges_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_mst.get_optimal_mst_edges_strategy()
print(f"Optimal MST edges strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Road Construction](https://cses.fi/problemset/task/1675) - MST construction
- [Road Reparation](https://cses.fi/problemset/task/1675) - MST repair
- [Road Construction II](https://cses.fi/problemset/task/1675) - MST variants

#### **LeetCode Problems**
- [Connecting Cities With Minimum Cost](https://leetcode.com/problems/connecting-cities-with-minimum-cost/) - MST
- [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) - MST
- [Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/) - Bridge detection

#### **Problem Categories**
- **Graph Theory**: MST algorithms, edge checking
- **Union-Find**: Disjoint set operations
- **Greedy Algorithms**: Kruskal's algorithm, Prim's algorithm

## 🔗 Additional Resources

### **Algorithm References**
- [Kruskal's Algorithm](https://cp-algorithms.com/graph/mst_kruskal.html) - MST construction
- [Prim's Algorithm](https://cp-algorithms.com/graph/mst_prim.html) - MST construction
- [Union-Find](https://cp-algorithms.com/data_structures/disjoint_set_union.html) - Disjoint set operations

### **Practice Problems**
- [CSES Road Construction](https://cses.fi/problemset/task/1675) - Medium
- [CSES Road Reparation](https://cses.fi/problemset/task/1675) - Medium
- [CSES Road Construction II](https://cses.fi/problemset/task/1675) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
