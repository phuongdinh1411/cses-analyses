---
layout: simple
title: "Fixed Length Hamiltonian Trail Queries - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_hamiltonian_trail_queries_analysis
---

# Fixed Length Hamiltonian Trail Queries - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Hamiltonian trails in directed graphs
- Apply graph theory principles to determine Hamiltonian trail existence
- Implement algorithms for finding Hamiltonian trails of specific lengths
- Optimize graph traversal for multiple trail queries
- Handle special cases in Hamiltonian trail analysis

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, Hamiltonian trails, graph traversal, NP-completeness
- **Data Structures**: Adjacency lists, bitmasks, dynamic programming tables
- **Mathematical Concepts**: Graph theory, trail properties, combinatorial optimization
- **Programming Skills**: Graph representation, DFS, bitmask operations, memoization
- **Related Problems**: Fixed Length Hamiltonian Path Queries (similar approach), Round Trip (cycle detection), Graph Girth (cycle properties)

## 📋 Problem Description

Given a directed graph with n nodes and q queries, for each query determine if there exists a Hamiltonian trail of length k from node a to node b.

**Input**: 
- n: number of nodes
- q: number of queries
- n lines: adjacency matrix (1 if edge exists, 0 otherwise)
- q lines: a b k (check for Hamiltonian trail from node a to b of length k)

**Output**: 
- Answer to each query (1 if exists, 0 otherwise)

**Constraints**:
- 1 ≤ n ≤ 20
- 1 ≤ q ≤ 10^5
- 1 ≤ k ≤ 10^9
- 1 ≤ a,b ≤ n

**Example**:
```
Input:
3 2
0 1 1
1 0 1
1 1 0
1 3 3
2 1 2

Output:
1
0

Explanation**: 
Query 1: Hamiltonian trail of length 3 from node 1 to 3
Trail: 1→2→3 (visits all vertices exactly once)
Answer: 1

Query 2: Hamiltonian trail of length 2 from node 2 to 1
No Hamiltonian trail of length 2 exists (only 3 vertices)
Answer: 0
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Exhaustive Search**: Try all possible permutations of vertices
- **Hamiltonian Validation**: For each permutation, check if it forms a Hamiltonian trail
- **Combinatorial Explosion**: n! possible permutations to explore
- **Baseline Understanding**: Provides correct answer but impractical

**Key Insight**: Generate all possible permutations of vertices and check if any forms a Hamiltonian trail from a to b.

**Algorithm**:
- Generate all possible permutations of vertices starting from node a
- For each permutation, check if it forms a valid Hamiltonian trail ending at node b
- Return 1 if any valid Hamiltonian trail exists, 0 otherwise

**Visual Example**:
```
Graph: 1↔2↔3↔1, k=3, start=1, end=3

All possible permutations starting from node 1:
┌─────────────────────────────────────┐
│ Permutation 1: [1,2,3] ✓ (trail)   │
│ Permutation 2: [1,3,2] ✗ (ends at 2)│
│ ... (other permutations)            │
└─────────────────────────────────────┘

Valid Hamiltonian trails: [1,2,3]
Result: 1
```

**Implementation**:
```python
def brute_force_solution(n, adj_matrix, queries):
    """
    Find Hamiltonian trail existence using brute force approach
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, b, k) queries
    
    Returns:
        list: answers to queries
    """
    from itertools import permutations
    
    def has_hamiltonian_trail(start, end, k):
        """Check if Hamiltonian trail of length k exists from start to end"""
        if k != n:
            return False
        
        # Generate all permutations starting from start
        vertices = list(range(n))
        vertices.remove(start)
        
        for perm in permutations(vertices):
            path = [start] + list(perm)
            
            # Check if path forms a valid Hamiltonian trail
            valid = True
            for i in range(len(path) - 1):
                current = path[i]
                next_vertex = path[i + 1]
                if adj_matrix[current][next_vertex] == 0:
                    valid = False
                    break
            
            # Check if path ends at the correct vertex
            if valid and path[-1] == end:
                return True
        
        return False
    
    results = []
    for a, b, k in queries:
        result = 1 if has_hamiltonian_trail(a - 1, b - 1, k) else 0  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 3, 3), (2, 1, 2)]
result = brute_force_solution(n, adj_matrix, queries)
print(f"Brute force result: {result}")  # Output: [1, 0]
```

**Time Complexity**: O(n! × n)
**Space Complexity**: O(n)

**Why it's inefficient**: Factorial time complexity makes it impractical for large n.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **State Definition**: dp[mask][i] = can reach vertex i using vertices in mask
- **State Transition**: dp[mask][i] = OR of dp[mask-{i}][j] for all j with edge (j,i)
- **Bitmask Representation**: Use bitmasks to represent vertex sets
- **Memoization**: Cache results to avoid recomputation

**Key Insight**: Use dynamic programming with bitmasks to efficiently check Hamiltonian trail existence.

**Algorithm**:
- Use bitmask to represent set of visited vertices
- For each state (mask, vertex), check if Hamiltonian trail exists from start to end
- Return 1 if valid Hamiltonian trail found, 0 otherwise

**Visual Example**:
```
Graph: 1↔2↔3↔1, k=3, start=1, end=3

DP table for bitmask states:
┌─────────────────────────────────────┐
│ mask=001 (vertex 1): dp[001][0]=1  │
│ mask=011 (vertices 1,2):           │
│   dp[011][1] = dp[001][0] & edge   │
│ mask=111 (all vertices):           │
│   dp[111][2] = dp[011][1] & edge   │
└─────────────────────────────────────┘

Hamiltonian trail exists: dp[111][2] = 1
```

**Implementation**:
```python
def dp_solution(n, adj_matrix, queries):
    """
    Find Hamiltonian trail existence using dynamic programming
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, b, k) queries
    
    Returns:
        list: answers to queries
    """
    def has_hamiltonian_trail(start, end, k):
        """Check if Hamiltonian trail of length k exists from start to end"""
        if k != n:
            return False
        
        # DP table: dp[mask][i] = can reach vertex i using vertices in mask
        dp = [[False] * n for _ in range(1 << n)]
        
        # Base case: start vertex with only itself
        dp[1 << start][start] = True
        
        # Fill DP table
        for mask in range(1 << n):
            for i in range(n):
                if dp[mask][i]:
                    for j in range(n):
                        if (adj_matrix[i][j] == 1 and 
                            (mask & (1 << j)) == 0):
                            new_mask = mask | (1 << j)
                            dp[new_mask][j] = True
        
        # Check if we can reach end from all vertices
        full_mask = (1 << n) - 1
        return dp[full_mask][end]
    
    results = []
    for a, b, k in queries:
        result = 1 if has_hamiltonian_trail(a - 1, b - 1, k) else 0  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 3, 3), (2, 1, 2)]
result = dp_solution(n, adj_matrix, queries)
print(f"DP result: {result}")  # Output: [1, 0]
```

**Time Complexity**: O(2^n × n²)
**Space Complexity**: O(2^n × n)

**Why it's better**: Much faster than brute force, but still exponential in n.

**Implementation Considerations**:
- **Bitmask Operations**: Use bitwise operations for efficient set representation
- **State Transitions**: Check all possible transitions from current state
- **Memory Management**: Use 2D DP table for state storage

---

### Approach 3: Optimized Dynamic Programming Solution (Optimal)

**Key Insights from Optimized Dynamic Programming Solution**:
- **Precomputation**: Precompute Hamiltonian trail existence for all pairs
- **Query Optimization**: Answer queries in O(1) time
- **Memory Optimization**: Use only necessary DP states
- **Efficient Transitions**: Optimize state transition calculations

**Key Insight**: Precompute all Hamiltonian trail possibilities and answer queries efficiently.

**Algorithm**:
- Precompute Hamiltonian trail existence for all (start, end) pairs
- For each query, return precomputed result
- Use optimized DP with reduced memory usage

**Visual Example**:
```
Graph: 1↔2↔3↔1

Precomputed results:
┌─────────────────────────────────────┐
│ (1,2): Hamiltonian trail ✓         │
│ (1,3): Hamiltonian trail ✓         │
│ (2,1): Hamiltonian trail ✓         │
│ (2,3): Hamiltonian trail ✓         │
│ (3,1): Hamiltonian trail ✓         │
│ (3,2): Hamiltonian trail ✓         │
└─────────────────────────────────────┘

Query 1: start=1, end=3, k=3 → 1
Query 2: start=2, end=1, k=2 → 0
```

**Implementation**:
```python
def optimized_solution(n, adj_matrix, queries):
    """
    Find Hamiltonian trail existence using optimized DP
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, b, k) queries
    
    Returns:
        list: answers to queries
    """
    # Precompute Hamiltonian trail existence for all pairs
    hamiltonian_trails = [[False] * n for _ in range(n)]
    
    for start in range(n):
        for end in range(n):
            if start == end:
                continue
            
            # DP table: dp[mask][i] = can reach vertex i using vertices in mask
            dp = [[False] * n for _ in range(1 << n)]
            
            # Base case: start vertex with only itself
            dp[1 << start][start] = True
            
            # Fill DP table
            for mask in range(1 << n):
                for i in range(n):
                    if dp[mask][i]:
                        for j in range(n):
                            if (adj_matrix[i][j] == 1 and 
                                (mask & (1 << j)) == 0):
                                new_mask = mask | (1 << j)
                                dp[new_mask][j] = True
            
            # Check if we can reach end from all vertices
            full_mask = (1 << n) - 1
            hamiltonian_trails[start][end] = dp[full_mask][end]
    
    # Answer queries
    results = []
    for a, b, k in queries:
        if k == n and hamiltonian_trails[a - 1][b - 1]:  # Convert to 0-indexed
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
queries = [(1, 3, 3), (2, 1, 2)]
result = optimized_solution(n, adj_matrix, queries)
print(f"Optimized result: {result}")  # Output: [1, 0]
```

**Time Complexity**: O(2^n × n³ + q)
**Space Complexity**: O(2^n × n + n²)

**Why it's optimal**: O(1) time per query after O(2^n × n³) preprocessing, making it efficient for large numbers of queries.

**Implementation Details**:
- **Precomputation**: Compute Hamiltonian trail existence for all pairs once
- **Query Optimization**: Answer queries in constant time
- **Memory Efficiency**: Use optimized DP table and result cache
- **State Optimization**: Reduce unnecessary state calculations

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × n) | O(n) | Exhaustive search of all permutations |
| Dynamic Programming | O(2^n × n²) | O(2^n × n) | Use DP with bitmasks |
| Optimized | O(2^n × n³ + q) | O(2^n × n + n²) | Precompute for O(1) queries |

### Time Complexity
- **Time**: O(2^n × n³ + q) - Precompute Hamiltonian trail existence for all pairs, then O(1) per query
- **Space**: O(2^n × n + n²) - Store DP table and precomputed results

### Why This Solution Works
- **Dynamic Programming**: Use bitmasks to represent vertex sets efficiently
- **Precomputation**: Compute Hamiltonian trail existence once for all pairs
- **Query Optimization**: Answer queries in constant time
- **State Optimization**: Use optimized DP transitions

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Hamiltonian Path Queries**
**Problem**: Find if there exists a Hamiltonian path of length k from node a to node b.

**Key Differences**: Paths instead of trails, different start and end nodes

**Solution Approach**: Use similar DP but don't require return to start

**Implementation**:
```python
def hamiltonian_path_queries(n, adj_matrix, queries):
    """
    Find Hamiltonian path existence using DP
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, b, k) queries
    
    Returns:
        list: answers to queries
    """
    def has_hamiltonian_path(start, end, k):
        """Check if Hamiltonian path of length k exists from start to end"""
        if k != n:
            return False
        
        # DP table: dp[mask][i] = can reach vertex i using vertices in mask
        dp = [[False] * n for _ in range(1 << n)]
        
        # Base case: start vertex with only itself
        dp[1 << start][start] = True
        
        # Fill DP table
        for mask in range(1 << n):
            for i in range(n):
                if dp[mask][i]:
                    for j in range(n):
                        if (adj_matrix[i][j] == 1 and 
                            (mask & (1 << j)) == 0):
                            new_mask = mask | (1 << j)
                            dp[new_mask][j] = True
        
        # Check if we can reach end from all vertices
        full_mask = (1 << n) - 1
        return dp[full_mask][end]
    
    results = []
    for a, b, k in queries:
        result = 1 if has_hamiltonian_path(a - 1, b - 1, k) else 0  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 3, 3), (2, 1, 3)]
result = hamiltonian_path_queries(n, adj_matrix, queries)
print(f"Hamiltonian path result: {result}")
```

#### **2. Weighted Hamiltonian Trail Queries**
**Problem**: Find if there exists a Hamiltonian trail of length k with total weight w.

**Key Differences**: Edges have weights, consider total weight

**Solution Approach**: Use 3D DP with weight dimension

**Implementation**:
```python
def weighted_hamiltonian_trail_queries(n, adj_matrix, weights, queries):
    """
    Find weighted Hamiltonian trail existence using 3D DP
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        weights: weight matrix
        queries: list of (a, b, k, w) queries
    
    Returns:
        list: answers to queries
    """
    def has_weighted_hamiltonian_trail(start, end, k, target_weight):
        """Check if weighted Hamiltonian trail exists"""
        if k != n:
            return False
        
        # DP table: dp[mask][i][w] = can reach vertex i with weight w using vertices in mask
        max_weight = target_weight + 1
        dp = [[[False] * max_weight for _ in range(n)] for _ in range(1 << n)]
        
        # Base case: start vertex with only itself
        dp[1 << start][start][0] = True
        
        # Fill DP table
        for mask in range(1 << n):
            for i in range(n):
                for w in range(max_weight):
                    if dp[mask][i][w]:
                        for j in range(n):
                            if (adj_matrix[i][j] == 1 and 
                                (mask & (1 << j)) == 0):
                                new_mask = mask | (1 << j)
                                new_weight = w + weights[i][j]
                                if new_weight < max_weight:
                                    dp[new_mask][j][new_weight] = True
        
        # Check if we can reach end with target weight
        full_mask = (1 << n) - 1
        return dp[full_mask][end][target_weight]
    
    results = []
    for a, b, k, w in queries:
        result = 1 if has_weighted_hamiltonian_trail(a - 1, b - 1, k, w) else 0  # Convert to 0-indexed
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
queries = [(1, 3, 3, 6), (2, 1, 2, 4)]
result = weighted_hamiltonian_trail_queries(n, adj_matrix, weights, queries)
print(f"Weighted Hamiltonian trail result: {result}")
```

#### **3. Dynamic Hamiltonian Trail Queries**
**Problem**: Support adding/removing edges and answering Hamiltonian trail queries.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic graph analysis with incremental updates

**Implementation**:
```python
class DynamicHamiltonianTrailQueries:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]
        self.weights = [[0] * n for _ in range(n)]
        self.hamiltonian_cache = {}  # Cache for Hamiltonian trail existence
    
    def add_edge(self, a, b, weight=1):
        """Add edge from a to b with weight"""
        if self.adj_matrix[a][b] == 0:
            self.adj_matrix[a][b] = 1
            self.weights[a][b] = weight
            self.hamiltonian_cache.clear()  # Invalidate cache
    
    def remove_edge(self, a, b):
        """Remove edge from a to b"""
        if self.adj_matrix[a][b] == 1:
            self.adj_matrix[a][b] = 0
            self.weights[a][b] = 0
            self.hamiltonian_cache.clear()  # Invalidate cache
    
    def has_hamiltonian_trail(self, start, end, k):
        """Check if Hamiltonian trail of length k exists from start to end"""
        if k != self.n:
            return False
        
        # Check cache first
        cache_key = (start, end, k)
        if cache_key in self.hamiltonian_cache:
            return self.hamiltonian_cache[cache_key]
        
        # DP table: dp[mask][i] = can reach vertex i using vertices in mask
        dp = [[False] * self.n for _ in range(1 << self.n)]
        
        # Base case: start vertex with only itself
        dp[1 << start][start] = True
        
        # Fill DP table
        for mask in range(1 << self.n):
            for i in range(self.n):
                if dp[mask][i]:
                    for j in range(self.n):
                        if (self.adj_matrix[i][j] == 1 and 
                            (mask & (1 << j)) == 0):
                            new_mask = mask | (1 << j)
                            dp[new_mask][j] = True
        
        # Check if we can reach end from all vertices
        full_mask = (1 << self.n) - 1
        result = dp[full_mask][end]
        
        # Cache result
        self.hamiltonian_cache[cache_key] = result
        return result

# Example usage
dhtq = DynamicHamiltonianTrailQueries(3)
dhtq.add_edge(0, 1, 2)
dhtq.add_edge(1, 2, 3)
dhtq.add_edge(2, 0, 4)
result1 = dhtq.has_hamiltonian_trail(0, 2, 3)
print(f"Dynamic Hamiltonian trail result: {result1}")
```

### Related Problems

#### **CSES Problems**
- [Fixed Length Hamiltonian Path Queries](https://cses.fi/problemset/task/2417) - Similar approach
- [Round Trip](https://cses.fi/problemset/task/1669) - Cycle detection
- [Graph Girth](https://cses.fi/problemset/task/1707) - Cycle properties

#### **LeetCode Problems**
- [Unique Paths III](https://leetcode.com/problems/unique-paths-iii/) - Hamiltonian path
- [Word Ladder](https://leetcode.com/problems/word-ladder/) - Graph traversal
- [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/) - All shortest paths

#### **Problem Categories**
- **Graph Theory**: Hamiltonian trails, Hamiltonian paths
- **Dynamic Programming**: Bitmask DP, state transitions
- **NP-Complete Problems**: Hamiltonian trail is NP-complete

## 🔗 Additional Resources

### **Algorithm References**
- [Hamiltonian Path](https://cp-algorithms.com/graph/hamiltonian_path.html) - Hamiltonian path algorithms
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/) - DP techniques
- [Bitmask DP](https://cp-algorithms.com/dynamic_programming/profile-dynamics.html) - Bitmask techniques

### **Practice Problems**
- [CSES Round Trip](https://cses.fi/problemset/task/1669) - Medium
- [CSES Graph Girth](https://cses.fi/problemset/task/1707) - Medium
- [CSES Hamiltonian Flights](https://cses.fi/problemset/task/1690) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
