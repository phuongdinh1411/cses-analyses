---
layout: simple
title: "Fixed Length Tour Queries - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_tour_queries_analysis
---

# Fixed Length Tour Queries - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of fixed length tours in directed graphs
- Apply graph theory principles to determine tour existence
- Implement algorithms for finding tours of specific lengths
- Optimize graph traversal for multiple tour queries
- Handle special cases in tour analysis

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, tour algorithms, graph traversal, dynamic programming
- **Data Structures**: Adjacency lists, matrices, dynamic programming tables
- **Mathematical Concepts**: Graph theory, tour properties, combinatorial optimization
- **Programming Skills**: Graph representation, DFS, BFS, matrix operations
- **Related Problems**: Fixed Length Path Queries (similar approach), Round Trip (cycle detection), Graph Girth (cycle properties)

## 📋 Problem Description

Given a directed graph with n nodes and q queries, for each query determine if there exists a tour of length k starting and ending at node a.

**Input**: 
- n: number of nodes
- q: number of queries
- n lines: adjacency matrix (1 if edge exists, 0 otherwise)
- q lines: a k (check for tour from node a to a of length k)

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
1 3
2 2

Output:
1
1

Explanation**: 
Query 1: Tour of length 3 from node 1 to 1
Tour: 1→2→3→1 (length 3, returns to start)
Answer: 1

Query 2: Tour of length 2 from node 2 to 2
Tour: 2→3→2 (length 2, returns to start)
Answer: 1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Exhaustive Search**: Try all possible tours of length k
- **DFS Traversal**: Use depth-first search to explore all tours
- **Exponential Growth**: Number of tours grows exponentially with k
- **Baseline Understanding**: Provides correct answer but impractical for large k

**Key Insight**: Use DFS to explore all possible tours of length k from start to start.

**Algorithm**:
- Start DFS from node a
- Explore all tours of length exactly k
- Return 1 if any tour returns to node a, 0 otherwise

**Visual Example**:
```
Graph: 1↔2↔3↔1, k=3, start=1

DFS exploration:
┌─────────────────────────────────────┐
│ Start at 1, depth=0                │
│ ├─ Go to 2, depth=1                │
│ │  └─ Go to 3, depth=2             │
│ │     └─ Go to 1, depth=3 ✓ (found!)│
│ └─ Go to 3, depth=1                │
│    └─ Go to 2, depth=2             │
│       └─ Go to 1, depth=3 ✓ (found!)│
└─────────────────────────────────────┘

Tour found: 1→2→3→1 (length 3)
Result: 1
```

**Implementation**:
```python
def brute_force_solution(n, adj_matrix, queries):
    """
    Find tour existence using brute force DFS approach
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    def has_tour(start, k):
        """Check if tour of length k exists from start to start using DFS"""
        if k == 0:
            return True  # Empty tour
        
        if k == 1:
            return adj_matrix[start][start] == 1  # Self-loop
        
        # DFS to find tour of length k
        def dfs(current, remaining_length):
            if remaining_length == 0:
                return current == start  # Must return to start
            
            for next_node in range(n):
                if adj_matrix[current][next_node] == 1:
                    if dfs(next_node, remaining_length - 1):
                        return True
            return False
        
        return dfs(start, k)
    
    results = []
    for a, k in queries:
        result = 1 if has_tour(a - 1, k) else 0  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 3), (2, 2)]
result = brute_force_solution(n, adj_matrix, queries)
print(f"Brute force result: {result}")  # Output: [1, 1]
```

**Time Complexity**: O(n^k)
**Space Complexity**: O(k)

**Why it's inefficient**: Exponential time complexity makes it impractical for large k.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **State Definition**: dp[i][j][k] = can reach node j from node i in exactly k steps
- **State Transition**: dp[i][j][k] = OR of dp[i][l][k-1] AND adj[l][j] for all l
- **Matrix Multiplication**: Use adjacency matrix powers for tour counting
- **Memoization**: Cache results to avoid recomputation

**Key Insight**: Use dynamic programming to compute tour existence for all pairs and lengths.

**Algorithm**:
- Use DP to compute tour existence for all (i,j,k) combinations
- For each query, return precomputed result
- Use matrix operations for efficient computation

**Visual Example**:
```
Graph: 1↔2↔3↔1, k=3

DP table for length 3:
┌─────────────────────────────────────┐
│ dp[1][1][3] = dp[1][2][2] & adj[2][1] │
│ dp[1][1][3] = 1 & 1 = 1 ✓          │
│ dp[2][2][2] = dp[2][3][1] & adj[3][2] │
│ dp[2][2][2] = 1 & 1 = 1 ✓          │
└─────────────────────────────────────┘

Tour exists for both queries
Result: [1, 1]
```

**Implementation**:
```python
def dp_solution(n, adj_matrix, queries):
    """
    Find tour existence using dynamic programming
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    # Find maximum k value
    max_k = max(k for _, k in queries)
    
    # DP table: dp[i][j][k] = can reach node j from node i in exactly k steps
    dp = [[[False] * (max_k + 1) for _ in range(n)] for _ in range(n)]
    
    # Base case: tours of length 0
    for i in range(n):
        dp[i][i][0] = True
    
    # Base case: tours of length 1
    for i in range(n):
        for j in range(n):
            dp[i][j][1] = (adj_matrix[i][j] == 1)
    
    # Fill DP table
    for k in range(2, max_k + 1):
        for i in range(n):
            for j in range(n):
                for l in range(n):
                    if dp[i][l][k-1] and adj_matrix[l][j] == 1:
                        dp[i][j][k] = True
                        break
    
    # Answer queries
    results = []
    for a, k in queries:
        if k <= max_k:
            result = 1 if dp[a-1][a-1][k] else 0  # Convert to 0-indexed
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
queries = [(1, 3), (2, 2)]
result = dp_solution(n, adj_matrix, queries)
print(f"DP result: {result}")  # Output: [1, 1]
```

**Time Complexity**: O(n³ × max_k)
**Space Complexity**: O(n² × max_k)

**Why it's better**: Much faster than brute force, but still limited by max_k.

**Implementation Considerations**:
- **Matrix Operations**: Use adjacency matrix for efficient edge checking
- **State Transitions**: Check all intermediate nodes for tour construction
- **Memory Management**: Use 3D DP table for state storage

---

### Approach 3: Matrix Exponentiation Solution (Optimal)

**Key Insights from Matrix Exponentiation Solution**:
- **Matrix Powers**: Use adjacency matrix powers for tour counting
- **Binary Exponentiation**: Compute matrix powers efficiently
- **Logarithmic Time**: O(log k) time per query
- **Efficient Storage**: Store only necessary matrix powers

**Key Insight**: Use matrix exponentiation to compute adjacency matrix powers for efficient tour queries.

**Algorithm**:
- Compute adjacency matrix powers using binary exponentiation
- For each query, use appropriate matrix power to check tour existence
- Return 1 if tour exists, 0 otherwise

**Visual Example**:
```
Graph: 1↔2↔3↔1

Adjacency matrix A:
┌─────────────────────────────────────┐
│ A = [0 1 1]                        │
│     [1 0 1]                        │
│     [1 1 0]                        │
└─────────────────────────────────────┘

A³ = A × A × A:
┌─────────────────────────────────────┐
│ A³ = [2 3 3]                       │
│      [3 2 3]                       │
│      [3 3 2]                       │
└─────────────────────────────────────┘

Query 1: A³[0][0] = 2 ✓ (tour of length 3)
Query 2: A²[1][1] = 2 ✓ (tour of length 2)
```

**Implementation**:
```python
def matrix_exponentiation_solution(n, adj_matrix, queries):
    """
    Find tour existence using matrix exponentiation
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    def matrix_multiply(A, B):
        """Multiply two n×n matrices"""
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_power(matrix, power):
        """Compute matrix^power using binary exponentiation"""
        if power == 0:
            # Return identity matrix
            identity = [[0] * n for _ in range(n)]
            for i in range(n):
                identity[i][i] = 1
            return identity
        
        if power == 1:
            return matrix
        
        if power % 2 == 0:
            half_power = matrix_power(matrix, power // 2)
            return matrix_multiply(half_power, half_power)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, power - 1))
    
    # Find unique k values
    unique_k_values = sorted(set(k for _, k in queries))
    
    # Precompute matrix powers
    matrix_powers = {}
    for k in unique_k_values:
        matrix_powers[k] = matrix_power(adj_matrix, k)
    
    # Answer queries
    results = []
    for a, k in queries:
        if k in matrix_powers:
            result = 1 if matrix_powers[k][a-1][a-1] > 0 else 0  # Convert to 0-indexed
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
queries = [(1, 3), (2, 2)]
result = matrix_exponentiation_solution(n, adj_matrix, queries)
print(f"Matrix exponentiation result: {result}")  # Output: [1, 1]
```

**Time Complexity**: O(n³ × log(max_k) + q)
**Space Complexity**: O(n² × unique_k_values)

**Why it's optimal**: O(log k) time per query after O(n³ × log(max_k)) preprocessing, making it efficient for large k values.

**Implementation Details**:
- **Binary Exponentiation**: Compute matrix powers efficiently
- **Query Optimization**: Answer queries in constant time
- **Memory Efficiency**: Store only necessary matrix powers
- **Matrix Operations**: Use efficient matrix multiplication

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^k) | O(k) | Exhaustive DFS search |
| Dynamic Programming | O(n³ × max_k) | O(n² × max_k) | Use DP for all tour lengths |
| Matrix Exponentiation | O(n³ × log(max_k) + q) | O(n² × unique_k_values) | Use matrix powers for O(log k) queries |

### Time Complexity
- **Time**: O(n³ × log(max_k) + q) - Precompute matrix powers, then O(1) per query
- **Space**: O(n² × unique_k_values) - Store matrix powers

### Why This Solution Works
- **Matrix Exponentiation**: Use adjacency matrix powers for tour counting
- **Binary Exponentiation**: Compute matrix powers efficiently
- **Query Optimization**: Answer queries in constant time
- **Efficient Storage**: Store only necessary matrix powers

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted Tour Queries**
**Problem**: Find if there exists a tour of length k with total weight w.

**Key Differences**: Edges have weights, consider total weight

**Solution Approach**: Use weighted adjacency matrix with matrix exponentiation

**Implementation**:
```python
def weighted_tour_queries(n, adj_matrix, weights, queries):
    """
    Find weighted tour existence using matrix exponentiation
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        weights: weight matrix
        queries: list of (a, k, w) queries
    
    Returns:
        list: answers to queries
    """
    def matrix_multiply(A, B):
        """Multiply two n×n matrices"""
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_power(matrix, power):
        """Compute matrix^power using binary exponentiation"""
        if power == 0:
            # Return identity matrix
            identity = [[0] * n for _ in range(n)]
            for i in range(n):
                identity[i][i] = 1
            return identity
        
        if power == 1:
            return matrix
        
        if power % 2 == 0:
            half_power = matrix_power(matrix, power // 2)
            return matrix_multiply(half_power, half_power)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, power - 1))
    
    # Create weighted adjacency matrix
    weighted_adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j] == 1:
                weighted_adj[i][j] = weights[i][j]
    
    # Find unique k values
    unique_k_values = sorted(set(k for _, k, _ in queries))
    
    # Precompute matrix powers
    matrix_powers = {}
    for k in unique_k_values:
        matrix_powers[k] = matrix_power(weighted_adj, k)
    
    # Answer queries
    results = []
    for a, k, w in queries:
        if k in matrix_powers:
            result = 1 if matrix_powers[k][a-1][a-1] == w else 0  # Convert to 0-indexed
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
queries = [(1, 3, 9), (2, 2, 4)]
result = weighted_tour_queries(n, adj_matrix, weights, queries)
print(f"Weighted tour result: {result}")
```

#### **2. Shortest Tour Queries**
**Problem**: Find the shortest tour length from a node to itself.

**Key Differences**: Find minimum tour length instead of fixed length

**Solution Approach**: Use Floyd-Warshall or Dijkstra's algorithm

**Implementation**:
```python
def shortest_tour_queries(n, adj_matrix, queries):
    """
    Find shortest tour lengths using Floyd-Warshall algorithm
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a,) queries
    
    Returns:
        list: shortest tour lengths
    """
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    
    # Base case: direct edges
    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j] == 1:
                dist[i][j] = 1
            elif i == j:
                dist[i][j] = 0
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Answer queries
    results = []
    for a, in queries:
        shortest_length = dist[a-1][a-1]  # Convert to 0-indexed
        if shortest_length == float('inf'):
            results.append(-1)  # No tour exists
        else:
            results.append(shortest_length)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1,), (2,)]
result = shortest_tour_queries(n, adj_matrix, queries)
print(f"Shortest tour result: {result}")
```

#### **3. Dynamic Tour Queries**
**Problem**: Support adding/removing edges and answering tour queries.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic graph analysis with incremental updates

**Implementation**:
```python
class DynamicTourQueries:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]
        self.weights = [[0] * n for _ in range(n)]
        self.tour_cache = {}  # Cache for tour existence
    
    def add_edge(self, a, b, weight=1):
        """Add edge from a to b with weight"""
        if self.adj_matrix[a][b] == 0:
            self.adj_matrix[a][b] = 1
            self.weights[a][b] = weight
            self.tour_cache.clear()  # Invalidate cache
    
    def remove_edge(self, a, b):
        """Remove edge from a to b"""
        if self.adj_matrix[a][b] == 1:
            self.adj_matrix[a][b] = 0
            self.weights[a][b] = 0
            self.tour_cache.clear()  # Invalidate cache
    
    def has_tour(self, start, k):
        """Check if tour of length k exists from start to start"""
        # Check cache first
        cache_key = (start, k)
        if cache_key in self.tour_cache:
            return self.tour_cache[cache_key]
        
        # Use DFS to find tour
        def dfs(current, remaining_length):
            if remaining_length == 0:
                return current == start  # Must return to start
            
            for next_node in range(self.n):
                if self.adj_matrix[current][next_node] == 1:
                    if dfs(next_node, remaining_length - 1):
                        return True
            return False
        
        result = dfs(start, k)
        
        # Cache result
        self.tour_cache[cache_key] = result
        return result

# Example usage
dtq = DynamicTourQueries(3)
dtq.add_edge(0, 1, 2)
dtq.add_edge(1, 2, 3)
dtq.add_edge(2, 0, 4)
result1 = dtq.has_tour(0, 3)
print(f"Dynamic tour result: {result1}")
```

### Related Problems

#### **CSES Problems**
- [Fixed Length Path Queries](https://cses.fi/problemset/task/2417) - Similar approach
- [Round Trip](https://cses.fi/problemset/task/1669) - Cycle detection
- [Graph Girth](https://cses.fi/problemset/task/1707) - Cycle properties

#### **LeetCode Problems**
- [Unique Paths III](https://leetcode.com/problems/unique-paths-iii/) - Hamiltonian path
- [Word Ladder](https://leetcode.com/problems/word-ladder/) - Graph traversal
- [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/) - All shortest paths

#### **Problem Categories**
- **Graph Theory**: Tour algorithms, matrix exponentiation
- **Dynamic Programming**: Matrix powers, state transitions
- **Combinatorial Optimization**: Tour counting, graph traversal

## 🔗 Additional Resources

### **Algorithm References**
- [Matrix Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html) - Matrix power algorithms
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/) - DP techniques
- [Graph Algorithms](https://cp-algorithms.com/graph/) - Graph traversal algorithms

### **Practice Problems**
- [CSES Round Trip](https://cses.fi/problemset/task/1669) - Medium
- [CSES Graph Girth](https://cses.fi/problemset/task/1707) - Medium
- [CSES Hamiltonian Flights](https://cses.fi/problemset/task/1690) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
