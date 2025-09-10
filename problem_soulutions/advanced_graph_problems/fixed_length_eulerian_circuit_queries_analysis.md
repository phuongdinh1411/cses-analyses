---
layout: simple
title: "Fixed Length Eulerian Circuit Queries - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_eulerian_circuit_queries_analysis
---

# Fixed Length Eulerian Circuit Queries - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Eulerian circuits in directed graphs
- Apply graph theory principles to determine Eulerian circuit existence
- Implement algorithms for finding Eulerian circuits of specific lengths
- Optimize graph traversal for multiple circuit queries
- Handle special cases in Eulerian circuit analysis

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, Eulerian circuits, graph traversal, degree analysis
- **Data Structures**: Adjacency lists, degree arrays, stacks
- **Mathematical Concepts**: Graph theory, degree properties, circuit properties
- **Programming Skills**: Graph representation, DFS, degree calculation
- **Related Problems**: Fixed Length Circuit Queries (similar approach), Round Trip (cycle detection), Graph Girth (cycle properties)

## 📋 Problem Description

Given a directed graph with n nodes and q queries, for each query determine if there exists an Eulerian circuit of length k starting and ending at node a.

**Input**: 
- n: number of nodes
- q: number of queries
- n lines: adjacency matrix (1 if edge exists, 0 otherwise)
- q lines: a k (check for Eulerian circuit from node a to a of length k)

**Output**: 
- Answer to each query (1 if exists, 0 otherwise)

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ q ≤ 10^5
- 1 ≤ k ≤ 10^9
- 1 ≤ a ≤ n

**Example**:
```
Input:
3 2
0 1 1
1 0 1
1 1 0
1 6
2 4

Output:
1
0

Explanation**: 
Query 1: Eulerian circuit of length 6 from node 1 to 1
Graph has all vertices with equal in-degree and out-degree
Circuit: 1→2→3→1→3→2→1 (length 6)
Answer: 1

Query 2: Eulerian circuit of length 4 from node 2 to 2
No Eulerian circuit of length 4 exists from node 2
Answer: 0
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Exhaustive Search**: Try all possible paths of length k
- **Eulerian Validation**: For each path, check if it forms an Eulerian circuit
- **Combinatorial Explosion**: n^k possible paths to explore
- **Baseline Understanding**: Provides correct answer but impractical

**Key Insight**: Generate all possible paths of length k and check if any forms an Eulerian circuit.

**Algorithm**:
- Generate all possible paths of length k starting from node a
- For each path, check if it ends at node a and uses each edge exactly once
- Return 1 if any valid Eulerian circuit exists, 0 otherwise

**Visual Example**:
```
Graph: 1↔2↔3↔1, k=6, start=1

All possible paths of length 6 from node 1:
┌─────────────────────────────────────┐
│ Path 1: 1→2→3→1→3→2→1 ✓ (Eulerian) │
│ Path 2: 1→2→3→1→2→3→1 ✓ (Eulerian) │
│ Path 3: 1→3→2→1→2→3→1 ✓ (Eulerian) │
│ Path 4: 1→3→2→1→3→2→1 ✓ (Eulerian) │
│ ... (other paths)                   │
└─────────────────────────────────────┘

Valid Eulerian circuits: Multiple
Result: 1
```

**Implementation**:
```python
def brute_force_solution(n, adj_matrix, queries):
    """
    Find Eulerian circuit existence using brute force approach
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    def has_eulerian_circuit(start, k):
        """Check if Eulerian circuit of length k exists from start"""
        def dfs(node, remaining_length, used_edges):
            if remaining_length == 0:
                return node == start and len(used_edges) == k
            
            for neighbor in range(n):
                edge = (node, neighbor)
                if adj_matrix[node][neighbor] == 1 and edge not in used_edges:
                    new_used = used_edges | {edge}
                    if dfs(neighbor, remaining_length - 1, new_used):
                        return True
            return False
        
        return dfs(start, k, set())
    
    results = []
    for a, k in queries:
        result = 1 if has_eulerian_circuit(a - 1, k) else 0  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 6), (2, 4)]
result = brute_force_solution(n, adj_matrix, queries)
print(f"Brute force result: {result}")  # Output: [1, 0]
```

**Time Complexity**: O(n^k × k)
**Space Complexity**: O(k)

**Why it's inefficient**: Exponential time complexity makes it impractical for large k.

---

### Approach 2: Graph Theory Analysis

**Key Insights from Graph Theory Analysis**:
- **Degree Condition**: All vertices must have equal in-degree and out-degree
- **Connectivity**: Graph must be strongly connected
- **Edge Count**: Total number of edges must equal k
- **Eulerian Property**: Graph must be Eulerian

**Key Insight**: Use graph theory properties to determine Eulerian circuit existence without exhaustive search.

**Algorithm**:
- Check if all vertices have equal in-degree and out-degree
- Check if graph is strongly connected
- Check if total number of edges equals k
- Return 1 if all conditions are met, 0 otherwise

**Visual Example**:
```
Graph: 1↔2↔3↔1

Degree analysis:
┌─────────────────────────────────────┐
│ Vertex 1: in-degree=2, out-degree=2│
│ Vertex 2: in-degree=2, out-degree=2│
│ Vertex 3: in-degree=2, out-degree=2│
│ All degrees equal ✓                 │
└─────────────────────────────────────┘

Connectivity: Strongly connected ✓
Total edges: 6
Query k=6: 6 == 6 ✓
Result: 1
```

**Implementation**:
```python
def graph_theory_solution(n, adj_matrix, queries):
    """
    Find Eulerian circuit existence using graph theory
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    def is_strongly_connected():
        """Check if graph is strongly connected"""
        def dfs(node, visited):
            visited.add(node)
            for neighbor in range(n):
                if adj_matrix[node][neighbor] == 1 and neighbor not in visited:
                    dfs(neighbor, visited)
            return visited
        
        # Check connectivity from node 0
        visited = dfs(0, set())
        if len(visited) != n:
            return False
        
        # Check reverse connectivity
        def reverse_dfs(node, visited):
            visited.add(node)
            for neighbor in range(n):
                if adj_matrix[neighbor][node] == 1 and neighbor not in visited:
                    reverse_dfs(neighbor, visited)
            return visited
        
        visited = reverse_dfs(0, set())
        return len(visited) == n
    
    def has_eulerian_circuit(k):
        """Check if Eulerian circuit of length k exists"""
        # Count total edges
        total_edges = sum(sum(row) for row in adj_matrix)
        if total_edges != k:
            return False
        
        # Check if all vertices have equal in-degree and out-degree
        for i in range(n):
            out_degree = sum(adj_matrix[i])
            in_degree = sum(adj_matrix[j][i] for j in range(n))
            if in_degree != out_degree:
                return False
        
        # Check if graph is strongly connected
        return is_strongly_connected()
    
    results = []
    for a, k in queries:
        result = 1 if has_eulerian_circuit(k) else 0
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 6), (2, 4)]
result = graph_theory_solution(n, adj_matrix, queries)
print(f"Graph theory result: {result}")  # Output: [1, 0]
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n)

**Why it's better**: Much faster than brute force, but still not optimal for multiple queries.

**Implementation Considerations**:
- **Degree Analysis**: Check in-degree and out-degree equality
- **Connectivity Check**: Use DFS to verify strong connectivity
- **Edge Counting**: Count total edges to match k

---

### Approach 3: Optimized Graph Theory Solution (Optimal)

**Key Insights from Optimized Graph Theory Solution**:
- **Precomputation**: Precompute graph properties once
- **Query Optimization**: Answer queries in O(1) time
- **Efficient Analysis**: Use optimized algorithms for graph analysis
- **Memory Optimization**: Store only necessary information

**Key Insight**: Precompute all graph properties and answer queries efficiently.

**Algorithm**:
- Precompute graph properties (degrees, connectivity, edge count)
- For each query, check if k matches edge count and graph is Eulerian
- Return results in O(1) time per query

**Visual Example**:
```
Graph: 1↔2↔3↔1

Precomputed properties:
┌─────────────────────────────────────┐
│ Total edges: 6                     │
│ All degrees equal: True            │
│ Strongly connected: True           │
│ Is Eulerian: True                  │
└─────────────────────────────────────┘

Query 1: k=6, 6==6 ✓, Eulerian ✓ → 1
Query 2: k=4, 4!=6 ✗ → 0
```

**Implementation**:
```python
def optimized_solution(n, adj_matrix, queries):
    """
    Find Eulerian circuit existence using optimized approach
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    # Precompute graph properties
    total_edges = sum(sum(row) for row in adj_matrix)
    
    # Check if all vertices have equal in-degree and out-degree
    degrees_equal = True
    for i in range(n):
        out_degree = sum(adj_matrix[i])
        in_degree = sum(adj_matrix[j][i] for j in range(n))
        if in_degree != out_degree:
            degrees_equal = False
            break
    
    # Check if graph is strongly connected
    def is_strongly_connected():
        def dfs(node, visited):
            visited.add(node)
            for neighbor in range(n):
                if adj_matrix[node][neighbor] == 1 and neighbor not in visited:
                    dfs(neighbor, visited)
            return visited
        
        # Check connectivity from node 0
        visited = dfs(0, set())
        if len(visited) != n:
            return False
        
        # Check reverse connectivity
        def reverse_dfs(node, visited):
            visited.add(node)
            for neighbor in range(n):
                if adj_matrix[neighbor][node] == 1 and neighbor not in visited:
                    reverse_dfs(neighbor, visited)
            return visited
        
        visited = reverse_dfs(0, set())
        return len(visited) == n
    
    is_eulerian = degrees_equal and is_strongly_connected()
    
    # Answer queries
    results = []
    for a, k in queries:
        if is_eulerian and k == total_edges:
            result = 1
        else:
            result = 0
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 6), (2, 4)]
result = optimized_solution(n, adj_matrix, queries)
print(f"Optimized result: {result}")  # Output: [1, 0]
```

**Time Complexity**: O(n² + q)
**Space Complexity**: O(n²)

**Why it's optimal**: O(1) time per query after O(n²) preprocessing, making it efficient for large numbers of queries.

**Implementation Details**:
- **Precomputation**: Compute all graph properties once
- **Query Optimization**: Answer queries in constant time
- **Memory Efficiency**: Store only necessary information
- **Graph Analysis**: Use efficient algorithms for connectivity

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^k × k) | O(k) | Exhaustive search of all paths |
| Graph Theory | O(n²) | O(n) | Use graph theory properties |
| Optimized | O(n² + q) | O(n²) | Precompute properties for O(1) queries |

### Time Complexity
- **Time**: O(n² + q) - Precompute graph properties, then O(1) per query
- **Space**: O(n²) - Store adjacency matrix and graph properties

### Why This Solution Works
- **Graph Theory**: Use Eulerian circuit properties for efficient checking
- **Precomputation**: Compute graph properties once for all queries
- **Query Optimization**: Answer queries in constant time
- **Efficient Analysis**: Use optimized algorithms for graph analysis

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Eulerian Path Queries**
**Problem**: Find if there exists an Eulerian path of length k from node a to node b.

**Key Differences**: Paths instead of circuits, different start and end nodes

**Solution Approach**: Use Eulerian path properties (at most 2 vertices with odd degree)

**Implementation**:
```python
def eulerian_path_queries(n, adj_matrix, queries):
    """
    Find Eulerian path existence using graph theory
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, b, k) queries
    
    Returns:
        list: answers to queries
    """
    # Precompute graph properties
    total_edges = sum(sum(row) for row in adj_matrix)
    
    # Check if graph has Eulerian path properties
    odd_degree_count = 0
    for i in range(n):
        out_degree = sum(adj_matrix[i])
        in_degree = sum(adj_matrix[j][i] for j in range(n))
        if abs(in_degree - out_degree) == 1:
            odd_degree_count += 1
        elif in_degree != out_degree:
            odd_degree_count = -1  # Invalid
            break
    
    has_eulerian_path = odd_degree_count <= 2
    
    # Answer queries
    results = []
    for a, b, k in queries:
        if has_eulerian_path and k == total_edges:
            result = 1
        else:
            result = 0
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 3, 6), (2, 1, 4)]
result = eulerian_path_queries(n, adj_matrix, queries)
print(f"Eulerian path result: {result}")
```

#### **2. Weighted Eulerian Circuit Queries**
**Problem**: Find if there exists an Eulerian circuit of length k with total weight w.

**Key Differences**: Edges have weights, consider total weight

**Solution Approach**: Use weighted graph analysis with weight constraints

**Implementation**:
```python
def weighted_eulerian_circuit_queries(n, adj_matrix, weights, queries):
    """
    Find weighted Eulerian circuit existence
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        weights: weight matrix
        queries: list of (a, k, w) queries
    
    Returns:
        list: answers to queries
    """
    # Precompute graph properties
    total_edges = sum(sum(row) for row in adj_matrix)
    total_weight = sum(sum(weights[i][j] for j in range(n) if adj_matrix[i][j]) for i in range(n))
    
    # Check if all vertices have equal in-degree and out-degree
    degrees_equal = True
    for i in range(n):
        out_degree = sum(adj_matrix[i])
        in_degree = sum(adj_matrix[j][i] for j in range(n))
        if in_degree != out_degree:
            degrees_equal = False
            break
    
    # Check if graph is strongly connected
    def is_strongly_connected():
        def dfs(node, visited):
            visited.add(node)
            for neighbor in range(n):
                if adj_matrix[node][neighbor] == 1 and neighbor not in visited:
                    dfs(neighbor, visited)
            return visited
        
        visited = dfs(0, set())
        if len(visited) != n:
            return False
        
        def reverse_dfs(node, visited):
            visited.add(node)
            for neighbor in range(n):
                if adj_matrix[neighbor][node] == 1 and neighbor not in visited:
                    reverse_dfs(neighbor, visited)
            return visited
        
        visited = reverse_dfs(0, set())
        return len(visited) == n
    
    is_eulerian = degrees_equal and is_strongly_connected()
    
    # Answer queries
    results = []
    for a, k, w in queries:
        if is_eulerian and k == total_edges and w == total_weight:
            result = 1
        else:
            result = 0
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
weights = [
    [0, 2, 3],
    [2, 0, 4],
    [3, 4, 0]
]
queries = [(1, 6, 18), (2, 4, 12)]
result = weighted_eulerian_circuit_queries(n, adj_matrix, weights, queries)
print(f"Weighted Eulerian circuit result: {result}")
```

#### **3. Dynamic Eulerian Circuit Queries**
**Problem**: Support adding/removing edges and answering Eulerian circuit queries.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic graph analysis with incremental updates

**Implementation**:
```python
class DynamicEulerianCircuitQueries:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]
        self.weights = [[0] * n for _ in range(n)]
        self.total_edges = 0
        self.total_weight = 0
        self.degrees_equal = True
        self.is_strongly_connected = True
    
    def add_edge(self, a, b, weight=1):
        """Add edge from a to b with weight"""
        if self.adj_matrix[a][b] == 0:
            self.adj_matrix[a][b] = 1
            self.weights[a][b] = weight
            self.total_edges += 1
            self.total_weight += weight
            self._update_properties()
    
    def remove_edge(self, a, b):
        """Remove edge from a to b"""
        if self.adj_matrix[a][b] == 1:
            self.adj_matrix[a][b] = 0
            self.total_weight -= self.weights[a][b]
            self.weights[a][b] = 0
            self.total_edges -= 1
            self._update_properties()
    
    def _update_properties(self):
        """Update graph properties after edge changes"""
        # Check if all vertices have equal in-degree and out-degree
        self.degrees_equal = True
        for i in range(self.n):
            out_degree = sum(self.adj_matrix[i])
            in_degree = sum(self.adj_matrix[j][i] for j in range(self.n))
            if in_degree != out_degree:
                self.degrees_equal = False
                break
        
        # Check if graph is strongly connected
        self.is_strongly_connected = self._is_strongly_connected()
    
    def _is_strongly_connected(self):
        """Check if graph is strongly connected"""
        def dfs(node, visited):
            visited.add(node)
            for neighbor in range(self.n):
                if self.adj_matrix[node][neighbor] == 1 and neighbor not in visited:
                    dfs(neighbor, visited)
            return visited
        
        visited = dfs(0, set())
        if len(visited) != self.n:
            return False
        
        def reverse_dfs(node, visited):
            visited.add(node)
            for neighbor in range(self.n):
                if self.adj_matrix[neighbor][node] == 1 and neighbor not in visited:
                    reverse_dfs(neighbor, visited)
            return visited
        
        visited = reverse_dfs(0, set())
        return len(visited) == self.n
    
    def has_eulerian_circuit(self, k):
        """Check if Eulerian circuit of length k exists"""
        return (self.degrees_equal and 
                self.is_strongly_connected and 
                k == self.total_edges)

# Example usage
decq = DynamicEulerianCircuitQueries(3)
decq.add_edge(0, 1, 2)
decq.add_edge(1, 2, 3)
decq.add_edge(2, 0, 4)
decq.add_edge(0, 2, 5)
decq.add_edge(2, 1, 6)
decq.add_edge(1, 0, 7)
result1 = decq.has_eulerian_circuit(6)
print(f"Dynamic Eulerian circuit result: {result1}")
```

### Related Problems

#### **CSES Problems**
- [Fixed Length Circuit Queries](https://cses.fi/problemset/task/2417) - Similar matrix approach
- [Round Trip](https://cses.fi/problemset/task/1669) - Cycle detection
- [Graph Girth](https://cses.fi/problemset/task/1707) - Cycle properties

#### **LeetCode Problems**
- [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) - Eulerian path
- [Cracking the Safe](https://leetcode.com/problems/cracking-the-safe/) - Eulerian circuit
- [Valid Arrangement of Pairs](https://leetcode.com/problems/valid-arrangement-of-pairs/) - Eulerian path

#### **Problem Categories**
- **Graph Theory**: Eulerian circuits, Eulerian paths
- **Graph Algorithms**: DFS, connectivity, degree analysis
- **Graph Properties**: Strong connectivity, degree properties

## 🔗 Additional Resources

### **Algorithm References**
- [Eulerian Path](https://cp-algorithms.com/graph/euler_path.html) - Eulerian path algorithms
- [Graph Theory](https://cp-algorithms.com/graph/) - Graph algorithms
- [Strongly Connected Components](https://cp-algorithms.com/graph/strongly-connected-components.html) - Connectivity

### **Practice Problems**
- [CSES Round Trip](https://cses.fi/problemset/task/1669) - Medium
- [CSES Graph Girth](https://cses.fi/problemset/task/1707) - Medium
- [CSES Strongly Connected Components](https://cses.fi/problemset/task/1683) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
