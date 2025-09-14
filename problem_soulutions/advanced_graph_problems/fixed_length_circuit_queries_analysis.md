---
layout: simple
title: "Fixed Length Circuit Queries - Matrix Exponentiation Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_circuit_queries_analysis
---

# Fixed Length Circuit Queries - Matrix Exponentiation Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of circuits (closed walks) in directed graphs
- Apply matrix exponentiation for efficient circuit counting
- Implement modular arithmetic for large circuit counts
- Optimize matrix operations for multiple circuit queries
- Handle large circuit lengths using binary exponentiation

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Matrix exponentiation, binary exponentiation, circuit counting, cycle detection
- **Data Structures**: Adjacency matrices, matrices, arrays
- **Mathematical Concepts**: Matrix operations, modular arithmetic, graph theory, circuit properties
- **Programming Skills**: Matrix multiplication, modular arithmetic, binary exponentiation
- **Related Problems**: Fixed Length Cycle Queries (similar matrix approach), Round Trip (cycle detection), Graph Girth (cycle properties)

## 📋 Problem Description

Given a directed graph with n nodes and q queries, for each query find the number of circuits of length k starting and ending at node a.

**Input**: 
- n: number of nodes
- q: number of queries
- n lines: adjacency matrix (1 if edge exists, 0 otherwise)
- q lines: a k (find circuits from node a to a of length k)

**Output**: 
- Answer to each query modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ q ≤ 10^5
- 1 ≤ k ≤ 10^9
- 1 ≤ a ≤ n

**Example**:
```
Input:
3 2
0 1 0
0 0 1
1 0 0
1 3
2 2

Output:
1
0

Explanation**: 
Query 1: Circuits of length 3 from node 1 to 1
Path: 1→2→3→1 (circuit of length 3)
Answer: 1

Query 2: Circuits of length 2 from node 2 to 2
No circuit of length 2 exists from node 2
Answer: 0
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Exhaustive Search**: Try all possible paths of length k
- **Path Validation**: For each path, check if it forms a circuit
- **Combinatorial Explosion**: n^k possible paths to explore
- **Baseline Understanding**: Provides correct answer but impractical

**Key Insight**: Generate all possible paths of length k and count those that form circuits.

**Algorithm**:
- Generate all possible paths of length k starting from node a
- For each path, check if it ends at node a (forms a circuit)
- Count valid circuits and return the result

**Visual Example**:
```
Graph: 1→2→3→1, k=3, start=1

All possible paths of length 3 from node 1:
┌─────────────────────────────────────┐
│ Path 1: 1→2→3→1 ✓ (circuit)        │
│ Path 2: 1→2→3→2 ✗ (not circuit)    │
│ Path 3: 1→2→3→3 ✗ (not circuit)    │
│ Path 4: 1→2→1→2 ✗ (not circuit)    │
│ Path 5: 1→2→1→3 ✗ (not circuit)    │
│ Path 6: 1→2→1→1 ✗ (not circuit)    │
│ ... (all other paths)               │
└─────────────────────────────────────┘

Valid circuits: 1
Result: 1
```

**Implementation**:
```python
def brute_force_solution(n, adj_matrix, queries):
    """
    Find circuit counts using brute force approach
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    def count_circuits(start, k):
        """Count circuits of length k starting from start"""
        def dfs(node, remaining_length):
            if remaining_length == 0:
                return 1 if node == start else 0
            
            count = 0
            for neighbor in range(n):
                if adj_matrix[node][neighbor] == 1:
                    count += dfs(neighbor, remaining_length - 1)
            return count
        
        return dfs(start, k)
    
    results = []
    for a, k in queries:
        result = count_circuits(a - 1, k)  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
]
queries = [(1, 3), (2, 2)]
result = brute_force_solution(n, adj_matrix, queries)
print(f"Brute force result: {result}")  # Output: [1, 0]
```

**Time Complexity**: O(n^k × q)
**Space Complexity**: O(k)

**Why it's inefficient**: Exponential time complexity makes it impractical for large k.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **State Definition**: dp[i][j][k] = number of paths from i to j of length k
- **State Transition**: dp[i][j][k] = sum of dp[i][m][k-1] * adj_matrix[m][j]
- **Base Case**: dp[i][j][0] = 1 if i == j, else 0
- **Memory Optimization**: Use 2D arrays instead of 3D

**Key Insight**: Use dynamic programming to count paths of different lengths efficiently.

**Algorithm**:
- Initialize DP table for paths of length 0
- For each length from 1 to k, compute paths using previous lengths
- Return dp[start][start][k] for circuit count

**Visual Example**:
```
Graph: 1→2→3→1, k=3, start=1

DP table for paths of length k from node 1:
┌─────────────────────────────────────┐
│ k=0: [1, 0, 0] (only self-loops)   │
│ k=1: [0, 1, 0] (1→2)               │
│ k=2: [0, 0, 1] (1→2→3)             │
│ k=3: [1, 0, 0] (1→2→3→1) ✓         │
└─────────────────────────────────────┘

Circuit count: dp[1][1][3] = 1
```

**Implementation**:
```python
def dp_solution(n, adj_matrix, queries):
    """
    Find circuit counts using dynamic programming
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    def count_circuits(start, k):
        """Count circuits of length k starting from start"""
        # dp[i][j] = number of paths from start to j of length i
        dp = [[0] * n for _ in range(k + 1)]
        
        # Base case: paths of length 0
        dp[0][start] = 1
        
        # Fill DP table
        for length in range(1, k + 1):
            for j in range(n):
                for m in range(n):
                    if adj_matrix[m][j] == 1:
                        dp[length][j] += dp[length - 1][m]
        
        return dp[k][start]
    
    results = []
    for a, k in queries:
        result = count_circuits(a - 1, k)  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
]
queries = [(1, 3), (2, 2)]
result = dp_solution(n, adj_matrix, queries)
print(f"DP result: {result}")  # Output: [1, 0]
```

**Time Complexity**: O(n³ × k × q)
**Space Complexity**: O(n × k)

**Why it's better**: Much faster than brute force, but still not optimal for large k.

**Implementation Considerations**:
- **State Transition**: Use matrix multiplication for state updates
- **Memory Management**: Use 2D arrays instead of 3D
- **Modular Arithmetic**: Apply modulo to prevent overflow

---

### Approach 3: Matrix Exponentiation Solution (Optimal)

**Key Insights from Matrix Exponentiation Solution**:
- **Matrix Power**: Adjacency matrix raised to power k gives path counts
- **Binary Exponentiation**: Compute matrix powers efficiently
- **Modular Arithmetic**: Handle large numbers with modulo operations
- **Query Optimization**: Precompute matrix powers for multiple queries

**Key Insight**: The number of circuits of length k from node a to a is the (a,a) entry of the adjacency matrix raised to power k.

**Algorithm**:
- Raise adjacency matrix to power k using binary exponentiation
- Return the (a,a) entry of the resulting matrix
- Apply modular arithmetic throughout

**Visual Example**:
```
Graph: 1→2→3→1

Adjacency matrix A:
┌─────────────────────────────────────┐
│ A = [0, 1, 0]                      │
│     [0, 0, 1]                      │
│     [1, 0, 0]                      │
└─────────────────────────────────────┘

A³ = A × A × A:
┌─────────────────────────────────────┐
│ A³ = [1, 0, 0]                     │
│      [0, 1, 0]                     │
│      [0, 0, 1]                     │
└─────────────────────────────────────┘

Circuits of length 3 from node 1: A³[1][1] = 1
```

**Implementation**:
```python
def matrix_exponentiation_solution(n, adj_matrix, queries):
    """
    Find circuit counts using matrix exponentiation
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    MOD = 10**9 + 7
    
    def matrix_multiply(A, B):
        """Multiply two matrices with modular arithmetic"""
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % MOD
        return result
    
    def matrix_power(matrix, power):
        """Compute matrix^power using binary exponentiation"""
        result = [[0] * n for _ in range(n)]
        # Initialize result as identity matrix
        for i in range(n):
            result[i][i] = 1
        
        base = [row[:] for row in matrix]
        
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2
        
        return result
    
    def count_circuits(start, k):
        """Count circuits of length k starting from start"""
        powered_matrix = matrix_power(adj_matrix, k)
        return powered_matrix[start][start]
    
    results = []
    for a, k in queries:
        result = count_circuits(a - 1, k)  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
]
queries = [(1, 3), (2, 2)]
result = matrix_exponentiation_solution(n, adj_matrix, queries)
print(f"Matrix exponentiation result: {result}")  # Output: [1, 0]
```

**Time Complexity**: O(n³ × log k × q)
**Space Complexity**: O(n²)

**Why it's optimal**: O(log k) complexity for each query using binary exponentiation, making it efficient for large k values.

**Implementation Details**:
- **Binary Exponentiation**: Compute matrix powers in O(log k) time
- **Modular Arithmetic**: Apply modulo operations to prevent overflow
- **Matrix Multiplication**: Use efficient matrix multiplication
- **Query Optimization**: Handle multiple queries efficiently

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^k × q) | O(k) | Exhaustive search of all paths |
| Dynamic Programming | O(n³ × k × q) | O(n × k) | Count paths using DP |
| Matrix Exponentiation | O(n³ × log k × q) | O(n²) | Use matrix powers for path counting |

### Time Complexity
- **Time**: O(n³ × log k × q) - Matrix exponentiation with binary exponentiation
- **Space**: O(n²) - Matrix storage

### Why This Solution Works
- **Matrix Power Property**: Adjacency matrix^k gives path counts of length k
- **Binary Exponentiation**: Efficiently compute large matrix powers
- **Modular Arithmetic**: Handle large numbers with modulo operations
- **Query Optimization**: Process multiple queries efficiently

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Fixed Length Path Queries**
**Problem**: Find number of paths of length k from node a to node b.

**Key Differences**: Paths instead of circuits, different start and end nodes

**Solution Approach**: Use same matrix exponentiation but return (a,b) entry

**Implementation**:
```python
def fixed_length_path_queries(n, adj_matrix, queries):
    """
    Find path counts using matrix exponentiation
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, b, k) queries
    
    Returns:
        list: answers to queries
    """
    MOD = 10**9 + 7
    
    def matrix_multiply(A, B):
        """Multiply two matrices with modular arithmetic"""
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % MOD
        return result
    
    def matrix_power(matrix, power):
        """Compute matrix^power using binary exponentiation"""
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        
        base = [row[:] for row in matrix]
        
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2
        
        return result
    
    def count_paths(start, end, k):
        """Count paths of length k from start to end"""
        powered_matrix = matrix_power(adj_matrix, k)
        return powered_matrix[start][end]
    
    results = []
    for a, b, k in queries:
        result = count_paths(a - 1, b - 1, k)  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
]
queries = [(1, 3, 2), (2, 1, 3)]
result = fixed_length_path_queries(n, adj_matrix, queries)
print(f"Fixed length path result: {result}")
```

#### **2. Weighted Graph Circuit Queries**
**Problem**: Find number of circuits of length k with total weight w.

**Key Differences**: Edges have weights, consider total weight

**Solution Approach**: Use 3D DP with weight dimension

**Implementation**:
```python
def weighted_circuit_queries(n, adj_matrix, weights, queries):
    """
    Find weighted circuit counts using 3D DP
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        weights: weight matrix
        queries: list of (a, k, w) queries
    
    Returns:
        list: answers to queries
    """
    MOD = 10**9 + 7
    
    def count_weighted_circuits(start, k, target_weight):
        """Count circuits of length k with total weight target_weight"""
        # dp[i][j][w] = number of paths from start to j of length i with weight w
        max_weight = target_weight + 1
        dp = [[[0] * max_weight for _ in range(n)] for _ in range(k + 1)]
        
        # Base case: paths of length 0
        dp[0][start][0] = 1
        
        # Fill DP table
        for length in range(1, k + 1):
            for j in range(n):
                for w in range(max_weight):
                    for m in range(n):
                        if adj_matrix[m][j] == 1:
                            edge_weight = weights[m][j]
                            if w >= edge_weight:
                                dp[length][j][w] = (dp[length][j][w] + dp[length - 1][m][w - edge_weight]) % MOD
        
        return dp[k][start][target_weight]
    
    results = []
    for a, k, w in queries:
        result = count_weighted_circuits(a - 1, k, w)  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
]
weights = [
    [0, 2, 0],
    [0, 0, 3],
    [1, 0, 0]
]
queries = [(1, 3, 6), (2, 2, 5)]
result = weighted_circuit_queries(n, adj_matrix, weights, queries)
print(f"Weighted circuit result: {result}")
```

#### **3. Dynamic Graph Circuit Queries**
**Problem**: Support adding/removing edges and answering circuit queries.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic matrix updates with lazy evaluation

**Implementation**:
```python
class DynamicCircuitQueries:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]
        self.matrix_cache = {}  # Cache for matrix powers
        self.MOD = 10**9 + 7
    
    def add_edge(self, a, b):
        """Add edge from a to b"""
        self.adj_matrix[a][b] = 1
        self.matrix_cache.clear()  # Invalidate cache
    
    def remove_edge(self, a, b):
        """Remove edge from a to b"""
        self.adj_matrix[a][b] = 0
        self.matrix_cache.clear()  # Invalidate cache
    
    def matrix_multiply(self, A, B):
        """Multiply two matrices with modular arithmetic"""
        result = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % self.MOD
        return result
    
    def matrix_power(self, power):
        """Compute matrix^power using binary exponentiation with caching"""
        if power in self.matrix_cache:
            return self.matrix_cache[power]
        
        result = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            result[i][i] = 1
        
        base = [row[:] for row in self.adj_matrix]
        
        while power > 0:
            if power % 2 == 1:
                result = self.matrix_multiply(result, base)
            base = self.matrix_multiply(base, base)
            power //= 2
        
        self.matrix_cache[power] = result
        return result
    
    def count_circuits(self, start, k):
        """Count circuits of length k starting from start"""
        powered_matrix = self.matrix_power(k)
        return powered_matrix[start][start]

# Example usage
dcq = DynamicCircuitQueries(3)
dcq.add_edge(0, 1)
dcq.add_edge(1, 2)
dcq.add_edge(2, 0)
result1 = dcq.count_circuits(0, 3)
print(f"Dynamic circuit result: {result1}")
```

## Problem Variations

### **Variation 1: Fixed Length Circuit Queries with Dynamic Updates**
**Problem**: Handle dynamic graph updates (add/remove/update edges) while maintaining fixed length circuit query calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic graph management with circuit detection.

```python
from collections import defaultdict, deque
import heapq

class DynamicFixedLengthCircuitQueries:
    def __init__(self, n=None, edges=None, target_length=None):
        self.n = n or 0
        self.edges = edges or []
        self.target_length = target_length or 0
        self.graph = defaultdict(list)
        self._update_circuit_query_info()
    
    def _update_circuit_query_info(self):
        """Update circuit query feasibility information."""
        self.circuit_query_feasibility = self._calculate_circuit_query_feasibility()
    
    def _calculate_circuit_query_feasibility(self):
        """Calculate circuit query feasibility."""
        if self.n <= 0 or self.target_length <= 0:
            return 0.0
        
        # Check if we can have circuits of target length
        return 1.0 if self.n > 0 and self.target_length > 0 else 0.0
    
    def update_graph(self, new_n, new_edges, new_target_length=None):
        """Update the graph with new vertices, edges, and target length."""
        self.n = new_n
        self.edges = new_edges
        if new_target_length is not None:
            self.target_length = new_target_length
        self._build_graph()
        self._update_circuit_query_info()
    
    def add_edge(self, u, v):
        """Add an edge to the graph."""
        if 1 <= u <= self.n and 1 <= v <= self.n:
            self.edges.append((u, v))
            self.graph[u].append(v)
            self.graph[v].append(u)
            self._update_circuit_query_info()
    
    def remove_edge(self, u, v):
        """Remove an edge from the graph."""
        if (u, v) in self.edges:
            self.edges.remove((u, v))
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            self._update_circuit_query_info()
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def find_circuits_of_length(self, start_vertex=None):
        """Find circuits of the target length."""
        if not self.circuit_query_feasibility:
            return []
        
        circuits = []
        if start_vertex is None:
            # Try all vertices as starting points
            for start in range(1, self.n + 1):
                circuits.extend(self._find_circuits_from_vertex(start))
        else:
            circuits = self._find_circuits_from_vertex(start_vertex)
        
        return circuits
    
    def _find_circuits_from_vertex(self, start):
        """Find circuits starting from a specific vertex."""
        circuits = []
        visited = set()
        path = []
        
        def dfs(current, length):
            if length == self.target_length:
                if current == start and len(path) == self.target_length:
                    circuits.append(path[:])
                return
            
            if length > self.target_length:
                return
            
            for neighbor in self.graph[current]:
                if neighbor not in visited or (length == self.target_length - 1 and neighbor == start):
                    if neighbor == start and length == self.target_length - 1:
                        path.append(neighbor)
                        dfs(neighbor, length + 1)
                        path.pop()
                    elif neighbor != start:
                        visited.add(neighbor)
                        path.append(neighbor)
                        dfs(neighbor, length + 1)
                        path.pop()
                        visited.remove(neighbor)
        
        visited.add(start)
        path.append(start)
        dfs(start, 1)
        visited.remove(start)
        path.pop()
        
        return circuits
    
    def find_circuits_with_priorities(self, priorities, start_vertex=None):
        """Find circuits considering vertex priorities."""
        if not self.circuit_query_feasibility:
            return []
        
        circuits = self.find_circuits_of_length(start_vertex)
        if not circuits:
            return []
        
        # Create priority-based circuits
        priority_circuits = []
        for circuit in circuits:
            total_priority = sum(priorities.get(vertex, 1) for vertex in circuit)
            priority_circuits.append((circuit, total_priority))
        
        # Sort by priority (descending for maximization)
        priority_circuits.sort(key=lambda x: x[1], reverse=True)
        
        return priority_circuits
    
    def get_circuits_with_constraints(self, constraint_func, start_vertex=None):
        """Get circuits that satisfies custom constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        circuits = self.find_circuits_of_length(start_vertex)
        if circuits and constraint_func(self.n, self.edges, circuits, self.target_length):
            return circuits
        else:
            return []
    
    def get_circuits_in_range(self, min_length, max_length, start_vertex=None):
        """Get circuits within specified length range."""
        if not self.circuit_query_feasibility:
            return []
        
        if min_length <= self.target_length <= max_length:
            return self.find_circuits_of_length(start_vertex)
        else:
            return []
    
    def get_circuits_with_pattern(self, pattern_func, start_vertex=None):
        """Get circuits matching specified pattern."""
        if not self.circuit_query_feasibility:
            return []
        
        circuits = self.find_circuits_of_length(start_vertex)
        if pattern_func(self.n, self.edges, circuits, self.target_length):
            return circuits
        else:
            return []
    
    def get_circuit_query_statistics(self):
        """Get statistics about the circuit queries."""
        if not self.circuit_query_feasibility:
            return {
                'n': 0,
                'circuit_query_feasibility': 0,
                'has_circuits': False,
                'target_length': 0,
                'circuit_count': 0
            }
        
        circuits = self.find_circuits_of_length()
        return {
            'n': self.n,
            'circuit_query_feasibility': self.circuit_query_feasibility,
            'has_circuits': len(circuits) > 0,
            'target_length': self.target_length,
            'circuit_count': len(circuits)
        }
    
    def get_circuit_query_patterns(self):
        """Get patterns in circuit queries."""
        patterns = {
            'has_edges': 0,
            'has_valid_graph': 0,
            'optimal_circuit_possible': 0,
            'has_large_graph': 0
        }
        
        if not self.circuit_query_feasibility:
            return patterns
        
        # Check if has edges
        if len(self.edges) > 0:
            patterns['has_edges'] = 1
        
        # Check if has valid graph
        if self.n > 0:
            patterns['has_valid_graph'] = 1
        
        # Check if optimal circuit is possible
        if self.circuit_query_feasibility == 1.0:
            patterns['optimal_circuit_possible'] = 1
        
        # Check if has large graph
        if self.n > 100:
            patterns['has_large_graph'] = 1
        
        return patterns
    
    def get_optimal_circuit_query_strategy(self):
        """Get optimal strategy for circuit query management."""
        if not self.circuit_query_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'circuit_query_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.circuit_query_feasibility
        
        # Calculate circuit query feasibility
        circuit_query_feasibility = self.circuit_query_feasibility
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'dfs_circuit_search'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_dfs'
        else:
            recommended_strategy = 'advanced_circuit_detection'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'circuit_query_feasibility': circuit_query_feasibility
        }

# Example usage
n = 5
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
target_length = 5
dynamic_circuit_queries = DynamicFixedLengthCircuitQueries(n, edges, target_length)
print(f"Circuit query feasibility: {dynamic_circuit_queries.circuit_query_feasibility}")

# Update graph
dynamic_circuit_queries.update_graph(6, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)], 6)
print(f"After updating graph: n={dynamic_circuit_queries.n}, target_length={dynamic_circuit_queries.target_length}")

# Add edge
dynamic_circuit_queries.add_edge(6, 1)
print(f"After adding edge (6,1): {dynamic_circuit_queries.edges}")

# Remove edge
dynamic_circuit_queries.remove_edge(6, 1)
print(f"After removing edge (6,1): {dynamic_circuit_queries.edges}")

# Find circuits
circuits = dynamic_circuit_queries.find_circuits_of_length()
print(f"Circuits of length {target_length}: {circuits}")

# Find circuits with priorities
priorities = {i: i for i in range(1, n + 1)}
priority_circuits = dynamic_circuit_queries.find_circuits_with_priorities(priorities)
print(f"Circuits with priorities: {priority_circuits}")

# Get circuits with constraints
def constraint_func(n, edges, circuits, target_length):
    return len(circuits) > 0 and target_length > 0

print(f"Circuits with constraints: {dynamic_circuit_queries.get_circuits_with_constraints(constraint_func)}")

# Get circuits in range
print(f"Circuits in range 3-7: {dynamic_circuit_queries.get_circuits_in_range(3, 7)}")

# Get circuits with pattern
def pattern_func(n, edges, circuits, target_length):
    return len(circuits) > 0 and target_length > 0

print(f"Circuits with pattern: {dynamic_circuit_queries.get_circuits_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_circuit_queries.get_circuit_query_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_circuit_queries.get_circuit_query_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_circuit_queries.get_optimal_circuit_query_strategy()}")
```

### **Variation 2: Fixed Length Circuit Queries with Different Operations**
**Problem**: Handle different types of circuit query operations (weighted circuits, priority-based selection, advanced circuit analysis).

**Approach**: Use advanced data structures for efficient different types of circuit query operations.

```python
class AdvancedFixedLengthCircuitQueries:
    def __init__(self, n=None, edges=None, target_length=None, weights=None, priorities=None):
        self.n = n or 0
        self.edges = edges or []
        self.target_length = target_length or 0
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.graph = defaultdict(list)
        self._update_circuit_query_info()
    
    def _update_circuit_query_info(self):
        """Update circuit query feasibility information."""
        self.circuit_query_feasibility = self._calculate_circuit_query_feasibility()
    
    def _calculate_circuit_query_feasibility(self):
        """Calculate circuit query feasibility."""
        if self.n <= 0 or self.target_length <= 0:
            return 0.0
        
        # Check if we can have circuits of target length
        return 1.0 if self.n > 0 and self.target_length > 0 else 0.0
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def find_circuits_of_length(self, start_vertex=None):
        """Find circuits of the target length."""
        if not self.circuit_query_feasibility:
            return []
        
        self._build_graph()
        
        circuits = []
        if start_vertex is None:
            # Try all vertices as starting points
            for start in range(1, self.n + 1):
                circuits.extend(self._find_circuits_from_vertex(start))
        else:
            circuits = self._find_circuits_from_vertex(start_vertex)
        
        return circuits
    
    def _find_circuits_from_vertex(self, start):
        """Find circuits starting from a specific vertex."""
        circuits = []
        visited = set()
        path = []
        
        def dfs(current, length):
            if length == self.target_length:
                if current == start and len(path) == self.target_length:
                    circuits.append(path[:])
                return
            
            if length > self.target_length:
                return
            
            for neighbor in self.graph[current]:
                if neighbor not in visited or (length == self.target_length - 1 and neighbor == start):
                    if neighbor == start and length == self.target_length - 1:
                        path.append(neighbor)
                        dfs(neighbor, length + 1)
                        path.pop()
                    elif neighbor != start:
                        visited.add(neighbor)
                        path.append(neighbor)
                        dfs(neighbor, length + 1)
                        path.pop()
                        visited.remove(neighbor)
        
        visited.add(start)
        path.append(start)
        dfs(start, 1)
        visited.remove(start)
        path.pop()
        
        return circuits
    
    def get_weighted_circuits(self, start_vertex=None):
        """Get circuits with weights and priorities applied."""
        if not self.circuit_query_feasibility:
            return []
        
        circuits = self.find_circuits_of_length(start_vertex)
        if not circuits:
            return []
        
        # Create weighted circuits
        weighted_circuits = []
        for circuit in circuits:
            total_weight = 0
            total_priority = 0
            
            for i in range(len(circuit)):
                vertex = circuit[i]
                next_vertex = circuit[(i + 1) % len(circuit)]
                
                edge_weight = self.weights.get((vertex, next_vertex), 1)
                vertex_priority = self.priorities.get(vertex, 1)
                
                total_weight += edge_weight
                total_priority += vertex_priority
            
            weighted_score = total_weight * total_priority
            weighted_circuits.append((circuit, weighted_score))
        
        # Sort by weighted score (descending for maximization)
        weighted_circuits.sort(key=lambda x: x[1], reverse=True)
        
        return weighted_circuits
    
    def get_circuits_with_priority(self, priority_func, start_vertex=None):
        """Get circuits considering priority."""
        if not self.circuit_query_feasibility:
            return []
        
        circuits = self.find_circuits_of_length(start_vertex)
        if not circuits:
            return []
        
        # Create priority-based circuits
        priority_circuits = []
        for circuit in circuits:
            priority = priority_func(circuit, self.weights, self.priorities)
            priority_circuits.append((circuit, priority))
        
        # Sort by priority (descending for maximization)
        priority_circuits.sort(key=lambda x: x[1], reverse=True)
        
        return priority_circuits
    
    def get_circuits_with_optimization(self, optimization_func, start_vertex=None):
        """Get circuits using custom optimization function."""
        if not self.circuit_query_feasibility:
            return []
        
        circuits = self.find_circuits_of_length(start_vertex)
        if not circuits:
            return []
        
        # Create optimization-based circuits
        optimized_circuits = []
        for circuit in circuits:
            score = optimization_func(circuit, self.weights, self.priorities)
            optimized_circuits.append((circuit, score))
        
        # Sort by optimization score (descending for maximization)
        optimized_circuits.sort(key=lambda x: x[1], reverse=True)
        
        return optimized_circuits
    
    def get_circuits_with_constraints(self, constraint_func, start_vertex=None):
        """Get circuits that satisfies custom constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        if constraint_func(self.n, self.edges, self.weights, self.priorities, self.target_length):
            return self.get_weighted_circuits(start_vertex)
        else:
            return []
    
    def get_circuits_with_multiple_criteria(self, criteria_list, start_vertex=None):
        """Get circuits that satisfies multiple criteria."""
        if not self.circuit_query_feasibility:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.n, self.edges, self.weights, self.priorities, self.target_length):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_circuits(start_vertex)
        else:
            return []
    
    def get_circuits_with_alternatives(self, alternatives, start_vertex=None):
        """Get circuits considering alternative weights/priorities."""
        result = []
        
        # Check original circuits
        original_circuits = self.get_weighted_circuits(start_vertex)
        result.append((original_circuits, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedFixedLengthCircuitQueries(self.n, self.edges, self.target_length, alt_weights, alt_priorities)
            temp_circuits = temp_instance.get_weighted_circuits(start_vertex)
            result.append((temp_circuits, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_circuits_with_adaptive_criteria(self, adaptive_func, start_vertex=None):
        """Get circuits using adaptive criteria."""
        if not self.circuit_query_feasibility:
            return []
        
        if adaptive_func(self.n, self.edges, self.weights, self.priorities, self.target_length, []):
            return self.get_weighted_circuits(start_vertex)
        else:
            return []
    
    def get_circuits_optimization(self, start_vertex=None):
        """Get optimal circuits configuration."""
        strategies = [
            ('weighted_circuits', lambda: len(self.get_weighted_circuits(start_vertex))),
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
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
target_length = 5
weights = {(u, v): (u + v) * 2 for u, v in edges}  # Weight based on vertex sum
priorities = {i: i for i in range(1, n + 1)}  # Priority based on vertex number
advanced_circuit_queries = AdvancedFixedLengthCircuitQueries(n, edges, target_length, weights, priorities)

print(f"Weighted circuits: {advanced_circuit_queries.get_weighted_circuits()}")

# Get circuits with priority
def priority_func(circuit, weights, priorities):
    return sum(priorities.get(vertex, 1) for vertex in circuit)

print(f"Circuits with priority: {advanced_circuit_queries.get_circuits_with_priority(priority_func)}")

# Get circuits with optimization
def optimization_func(circuit, weights, priorities):
    return sum(weights.get((circuit[i], circuit[(i+1)%len(circuit)]), 1) for i in range(len(circuit)))

print(f"Circuits with optimization: {advanced_circuit_queries.get_circuits_with_optimization(optimization_func)}")

# Get circuits with constraints
def constraint_func(n, edges, weights, priorities, target_length):
    return len(edges) > 0 and n > 0 and target_length > 0

print(f"Circuits with constraints: {advanced_circuit_queries.get_circuits_with_constraints(constraint_func)}")

# Get circuits with multiple criteria
def criterion1(n, edges, weights, priorities, target_length):
    return len(edges) > 0

def criterion2(n, edges, weights, priorities, target_length):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Circuits with multiple criteria: {advanced_circuit_queries.get_circuits_with_multiple_criteria(criteria_list)}")

# Get circuits with alternatives
alternatives = [({(u, v): 1 for u, v in edges}, {i: 1 for i in range(1, n + 1)}), ({(u, v): (u + v)*3 for u, v in edges}, {i: 2 for i in range(1, n + 1)})]
print(f"Circuits with alternatives: {advanced_circuit_queries.get_circuits_with_alternatives(alternatives)}")

# Get circuits with adaptive criteria
def adaptive_func(n, edges, weights, priorities, target_length, current_result):
    return len(edges) > 0 and len(current_result) < 10

print(f"Circuits with adaptive criteria: {advanced_circuit_queries.get_circuits_with_adaptive_criteria(adaptive_func)}")

# Get circuits optimization
print(f"Circuits optimization: {advanced_circuit_queries.get_circuits_optimization()}")
```

### **Variation 3: Fixed Length Circuit Queries with Constraints**
**Problem**: Handle circuit queries with additional constraints (length limits, circuit constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedFixedLengthCircuitQueries:
    def __init__(self, n=None, edges=None, target_length=None, constraints=None):
        self.n = n or 0
        self.edges = edges or []
        self.target_length = target_length or 0
        self.constraints = constraints or {}
        self.graph = defaultdict(list)
        self._update_circuit_query_info()
    
    def _update_circuit_query_info(self):
        """Update circuit query feasibility information."""
        self.circuit_query_feasibility = self._calculate_circuit_query_feasibility()
    
    def _calculate_circuit_query_feasibility(self):
        """Calculate circuit query feasibility."""
        if self.n <= 0 or self.target_length <= 0:
            return 0.0
        
        # Check if we can have circuits of target length
        return 1.0 if self.n > 0 and self.target_length > 0 else 0.0
    
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
                if not constraint(u, v, self.n, self.edges, self.target_length):
                    return False
        
        return True
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            if self._is_valid_edge(u, v):
                self.graph[u].append(v)
                self.graph[v].append(u)
    
    def find_circuits_of_length(self, start_vertex=None):
        """Find circuits of the target length."""
        if not self.circuit_query_feasibility:
            return []
        
        self._build_graph()
        
        circuits = []
        if start_vertex is None:
            # Try all vertices as starting points
            for start in range(1, self.n + 1):
                circuits.extend(self._find_circuits_from_vertex(start))
        else:
            circuits = self._find_circuits_from_vertex(start_vertex)
        
        return circuits
    
    def _find_circuits_from_vertex(self, start):
        """Find circuits starting from a specific vertex."""
        circuits = []
        visited = set()
        path = []
        
        def dfs(current, length):
            if length == self.target_length:
                if current == start and len(path) == self.target_length:
                    circuits.append(path[:])
                return
            
            if length > self.target_length:
                return
            
            for neighbor in self.graph[current]:
                if neighbor not in visited or (length == self.target_length - 1 and neighbor == start):
                    if neighbor == start and length == self.target_length - 1:
                        path.append(neighbor)
                        dfs(neighbor, length + 1)
                        path.pop()
                    elif neighbor != start:
                        visited.add(neighbor)
                        path.append(neighbor)
                        dfs(neighbor, length + 1)
                        path.pop()
                        visited.remove(neighbor)
        
        visited.add(start)
        path.append(start)
        dfs(start, 1)
        visited.remove(start)
        path.pop()
        
        return circuits
    
    def get_circuits_with_length_constraints(self, min_length, max_length, start_vertex=None):
        """Get circuits considering length constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        if min_length <= self.target_length <= max_length:
            return self.find_circuits_of_length(start_vertex)
        else:
            return []
    
    def get_circuits_with_circuit_constraints(self, circuit_constraints, start_vertex=None):
        """Get circuits considering circuit constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        satisfies_constraints = True
        for constraint in circuit_constraints:
            if not constraint(self.n, self.edges, self.target_length):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self.find_circuits_of_length(start_vertex)
        else:
            return []
    
    def get_circuits_with_pattern_constraints(self, pattern_constraints, start_vertex=None):
        """Get circuits considering pattern constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.n, self.edges, self.target_length):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self.find_circuits_of_length(start_vertex)
        else:
            return []
    
    def get_circuits_with_mathematical_constraints(self, constraint_func, start_vertex=None):
        """Get circuits that satisfies custom mathematical constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        circuits = self.find_circuits_of_length(start_vertex)
        if circuits and constraint_func(self.n, self.edges, self.target_length):
            return circuits
        else:
            return []
    
    def get_circuits_with_optimization_constraints(self, optimization_func, start_vertex=None):
        """Get circuits using custom optimization constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        # Calculate optimization score for circuits
        score = optimization_func(self.n, self.edges, self.target_length)
        
        if score > 0:
            return self.find_circuits_of_length(start_vertex)
        else:
            return []
    
    def get_circuits_with_multiple_constraints(self, constraints_list, start_vertex=None):
        """Get circuits that satisfies multiple constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.n, self.edges, self.target_length):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self.find_circuits_of_length(start_vertex)
        else:
            return []
    
    def get_circuits_with_priority_constraints(self, priority_func, start_vertex=None):
        """Get circuits with priority-based constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        # Calculate priority for circuits
        priority = priority_func(self.n, self.edges, self.target_length)
        
        if priority > 0:
            return self.find_circuits_of_length(start_vertex)
        else:
            return []
    
    def get_circuits_with_adaptive_constraints(self, adaptive_func, start_vertex=None):
        """Get circuits with adaptive constraints."""
        if not self.circuit_query_feasibility:
            return []
        
        circuits = self.find_circuits_of_length(start_vertex)
        if circuits and adaptive_func(self.n, self.edges, self.target_length, []):
            return circuits
        else:
            return []
    
    def get_optimal_circuits_strategy(self, start_vertex=None):
        """Get optimal circuits strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_circuits_with_length_constraints),
            ('circuit_constraints', self.get_circuits_with_circuit_constraints),
            ('pattern_constraints', self.get_circuits_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    result = strategy_func(1, 1000, start_vertex)
                elif strategy_name == 'circuit_constraints':
                    circuit_constraints = [lambda n, edges, target_length: len(edges) > 0]
                    result = strategy_func(circuit_constraints, start_vertex)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda n, edges, target_length: len(edges) > 0]
                    result = strategy_func(pattern_constraints, start_vertex)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_edges': [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)],
    'forbidden_edges': [(1, 3), (2, 4)],
    'max_vertex': 10,
    'min_vertex': 1,
    'pattern_constraints': [lambda u, v, n, edges, target_length: u > 0 and v > 0 and u <= n and v <= n]
}

n = 5
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
target_length = 5
constrained_circuit_queries = ConstrainedFixedLengthCircuitQueries(n, edges, target_length, constraints)

print("Length-constrained circuits:", constrained_circuit_queries.get_circuits_with_length_constraints(3, 7))

print("Circuit-constrained circuits:", constrained_circuit_queries.get_circuits_with_circuit_constraints([lambda n, edges, target_length: len(edges) > 0]))

print("Pattern-constrained circuits:", constrained_circuit_queries.get_circuits_with_pattern_constraints([lambda n, edges, target_length: len(edges) > 0]))

# Mathematical constraints
def custom_constraint(n, edges, target_length):
    return len(edges) > 0 and target_length > 0

print("Mathematical constraint circuits:", constrained_circuit_queries.get_circuits_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(n, edges, target_length):
    return 1 <= target_length <= 20

range_constraints = [range_constraint]
print("Range-constrained circuits:", constrained_circuit_queries.get_circuits_with_length_constraints(1, 20))

# Multiple constraints
def constraint1(n, edges, target_length):
    return len(edges) > 0

def constraint2(n, edges, target_length):
    return target_length > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints circuits:", constrained_circuit_queries.get_circuits_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(n, edges, target_length):
    return n + len(edges) + target_length

print("Priority-constrained circuits:", constrained_circuit_queries.get_circuits_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(n, edges, target_length, current_result):
    return len(edges) > 0 and len(current_result) < 10

print("Adaptive constraint circuits:", constrained_circuit_queries.get_circuits_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_circuit_queries.get_optimal_circuits_strategy()
print(f"Optimal circuits strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Fixed Length Cycle Queries](https://cses.fi/problemset/task/2417) - Similar matrix approach
- [Round Trip](https://cses.fi/problemset/task/1669) - Cycle detection
- [Graph Girth](https://cses.fi/problemset/task/1707) - Cycle properties

#### **LeetCode Problems**
- [Number of Ways to Arrive at Destination](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/) - Path counting
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Path counting
- [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) - Path counting with obstacles

#### **Problem Categories**
- **Matrix Exponentiation**: Matrix powers, binary exponentiation
- **Graph Theory**: Circuits, cycles, paths
- **Dynamic Programming**: State transitions, path counting

## 🔗 Additional Resources

### **Algorithm References**
- [Matrix Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html) - Binary exponentiation
- [Graph Theory](https://cp-algorithms.com/graph/) - Graph algorithms
- [Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html) - Modular operations

### **Practice Problems**
- [CSES Fixed Length Cycle Queries](https://cses.fi/problemset/task/2417) - Medium
- [CSES Round Trip](https://cses.fi/problemset/task/1669) - Medium
- [CSES Graph Girth](https://cses.fi/problemset/task/1707) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
