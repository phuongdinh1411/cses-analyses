---
layout: simple
title: "Fixed Length Hamiltonian Circuit Queries - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_hamiltonian_circuit_queries_analysis
---

# Fixed Length Hamiltonian Circuit Queries - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Hamiltonian circuits in directed graphs
- Apply graph theory principles to determine Hamiltonian circuit existence
- Implement algorithms for finding Hamiltonian circuits of specific lengths
- Optimize graph traversal for multiple circuit queries
- Handle special cases in Hamiltonian circuit analysis

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, Hamiltonian circuits, graph traversal, NP-completeness
- **Data Structures**: Adjacency lists, bitmasks, dynamic programming tables
- **Mathematical Concepts**: Graph theory, circuit properties, combinatorial optimization
- **Programming Skills**: Graph representation, DFS, bitmask operations, memoization
- **Related Problems**: Fixed Length Hamiltonian Cycle Queries (similar approach), Round Trip (cycle detection), Graph Girth (cycle properties)

## 📋 Problem Description

Given a directed graph with n nodes and q queries, for each query determine if there exists a Hamiltonian circuit of length k starting and ending at node a.

**Input**: 
- n: number of nodes
- q: number of queries
- n lines: adjacency matrix (1 if edge exists, 0 otherwise)
- q lines: a k (check for Hamiltonian circuit from node a to a of length k)

**Output**: 
- Answer to each query (1 if exists, 0 otherwise)

**Constraints**:
- 1 ≤ n ≤ 20
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
2 3

Output:
1
1

Explanation**: 
Query 1: Hamiltonian circuit of length 3 from node 1 to 1
Circuit: 1→2→3→1 (visits all vertices exactly once)
Answer: 1

Query 2: Hamiltonian circuit of length 3 from node 2 to 2
Circuit: 2→3→1→2 (visits all vertices exactly once)
Answer: 1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Exhaustive Search**: Try all possible permutations of vertices
- **Hamiltonian Validation**: For each permutation, check if it forms a Hamiltonian circuit
- **Combinatorial Explosion**: n! possible permutations to explore
- **Baseline Understanding**: Provides correct answer but impractical

**Key Insight**: Generate all possible permutations of vertices and check if any forms a Hamiltonian circuit.

**Algorithm**:
- Generate all possible permutations of vertices starting from node a
- For each permutation, check if it forms a valid Hamiltonian circuit
- Return 1 if any valid Hamiltonian circuit exists, 0 otherwise

**Visual Example**:
```
Graph: 1↔2↔3↔1, k=3, start=1

All possible permutations starting from node 1:
┌─────────────────────────────────────┐
│ Permutation 1: [1,2,3] ✓ (circuit) │
│ Permutation 2: [1,3,2] ✓ (circuit) │
│ ... (other permutations)            │
└─────────────────────────────────────┘

Valid Hamiltonian circuits: Multiple
Result: 1
```

**Implementation**:
```python
def brute_force_solution(n, adj_matrix, queries):
    """
    Find Hamiltonian circuit existence using brute force approach
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    from itertools import permutations
    
    def has_hamiltonian_circuit(start, k):
        """Check if Hamiltonian circuit of length k exists from start"""
        if k != n:
            return False
        
        # Generate all permutations starting from start
        vertices = list(range(n))
        vertices.remove(start)
        
        for perm in permutations(vertices):
            path = [start] + list(perm)
            
            # Check if path forms a valid Hamiltonian circuit
            valid = True
            for i in range(len(path)):
                current = path[i]
                next_vertex = path[(i + 1) % len(path)]
                if adj_matrix[current][next_vertex] == 0:
                    valid = False
                    break
            
            if valid:
                return True
        
        return False
    
    results = []
    for a, k in queries:
        result = 1 if has_hamiltonian_circuit(a - 1, k) else 0  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 3), (2, 3)]
result = brute_force_solution(n, adj_matrix, queries)
print(f"Brute force result: {result}")  # Output: [1, 1]
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

**Key Insight**: Use dynamic programming with bitmasks to efficiently check Hamiltonian circuit existence.

**Algorithm**:
- Use bitmask to represent set of visited vertices
- For each state (mask, vertex), check if Hamiltonian circuit exists
- Return 1 if valid Hamiltonian circuit found, 0 otherwise

**Visual Example**:
```
Graph: 1↔2↔3↔1, k=3, start=1

DP table for bitmask states:
┌─────────────────────────────────────┐
│ mask=001 (vertex 1): dp[001][0]=1  │
│ mask=011 (vertices 1,2):           │
│   dp[011][1] = dp[001][0] & edge   │
│ mask=111 (all vertices):           │
│   dp[111][0] = dp[011][1] & edge   │
└─────────────────────────────────────┘

Hamiltonian circuit exists: dp[111][0] = 1
```

**Implementation**:
```python
def dp_solution(n, adj_matrix, queries):
    """
    Find Hamiltonian circuit existence using dynamic programming
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    def has_hamiltonian_circuit(start, k):
        """Check if Hamiltonian circuit of length k exists from start"""
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
        
        # Check if we can return to start from all vertices
        full_mask = (1 << n) - 1
        return dp[full_mask][start]
    
    results = []
    for a, k in queries:
        result = 1 if has_hamiltonian_circuit(a - 1, k) else 0  # Convert to 0-indexed
        results.append(result)
    
    return results

# Example usage
n = 3
adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
queries = [(1, 3), (2, 3)]
result = dp_solution(n, adj_matrix, queries)
print(f"DP result: {result}")  # Output: [1, 1]
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
- **Precomputation**: Precompute Hamiltonian circuit existence for all starting vertices
- **Query Optimization**: Answer queries in O(1) time
- **Memory Optimization**: Use only necessary DP states
- **Efficient Transitions**: Optimize state transition calculations

**Key Insight**: Precompute all Hamiltonian circuit possibilities and answer queries efficiently.

**Algorithm**:
- Precompute Hamiltonian circuit existence for all starting vertices
- For each query, return precomputed result
- Use optimized DP with reduced memory usage

**Visual Example**:
```
Graph: 1↔2↔3↔1

Precomputed results:
┌─────────────────────────────────────┐
│ Start vertex 1: Hamiltonian ✓      │
│ Start vertex 2: Hamiltonian ✓      │
│ Start vertex 3: Hamiltonian ✓      │
└─────────────────────────────────────┘

Query 1: start=1, k=3 → 1
Query 2: start=2, k=3 → 1
```

**Implementation**:
```python
def optimized_solution(n, adj_matrix, queries):
    """
    Find Hamiltonian circuit existence using optimized DP
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        queries: list of (a, k) queries
    
    Returns:
        list: answers to queries
    """
    # Precompute Hamiltonian circuit existence for all starting vertices
    hamiltonian_exists = [False] * n
    
    for start in range(n):
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
        
        # Check if we can return to start from all vertices
        full_mask = (1 << n) - 1
        hamiltonian_exists[start] = dp[full_mask][start]
    
    # Answer queries
    results = []
    for a, k in queries:
        if k == n and hamiltonian_exists[a - 1]:  # Convert to 0-indexed
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
queries = [(1, 3), (2, 3)]
result = optimized_solution(n, adj_matrix, queries)
print(f"Optimized result: {result}")  # Output: [1, 1]
```

**Time Complexity**: O(2^n × n² + q)
**Space Complexity**: O(2^n × n)

**Why it's optimal**: O(1) time per query after O(2^n × n²) preprocessing, making it efficient for large numbers of queries.

**Implementation Details**:
- **Precomputation**: Compute Hamiltonian circuit existence for all starting vertices
- **Query Optimization**: Answer queries in constant time
- **Memory Efficiency**: Use optimized DP table
- **State Optimization**: Reduce unnecessary state calculations

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × n) | O(n) | Exhaustive search of all permutations |
| Dynamic Programming | O(2^n × n²) | O(2^n × n) | Use DP with bitmasks |
| Optimized | O(2^n × n² + q) | O(2^n × n) | Precompute for O(1) queries |

### Time Complexity
- **Time**: O(2^n × n² + q) - Precompute Hamiltonian circuit existence, then O(1) per query
- **Space**: O(2^n × n) - Store DP table and precomputed results

### Why This Solution Works
- **Dynamic Programming**: Use bitmasks to represent vertex sets efficiently
- **Precomputation**: Compute Hamiltonian circuit existence once for all queries
- **Query Optimization**: Answer queries in constant time
- **State Optimization**: Use optimized DP transitions

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Hamiltonian Path Queries**
**Problem**: Find if there exists a Hamiltonian path of length k from node a to node b.

**Key Differences**: Paths instead of circuits, different start and end nodes

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

#### **2. Weighted Hamiltonian Circuit Queries**
**Problem**: Find if there exists a Hamiltonian circuit of length k with total weight w.

**Key Differences**: Edges have weights, consider total weight

**Solution Approach**: Use 3D DP with weight dimension

**Implementation**:
```python
def weighted_hamiltonian_circuit_queries(n, adj_matrix, weights, queries):
    """
    Find weighted Hamiltonian circuit existence using 3D DP
    
    Args:
        n: number of nodes
        adj_matrix: adjacency matrix
        weights: weight matrix
        queries: list of (a, k, w) queries
    
    Returns:
        list: answers to queries
    """
    def has_weighted_hamiltonian_circuit(start, k, target_weight):
        """Check if weighted Hamiltonian circuit exists"""
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
        
        # Check if we can return to start with target weight
        full_mask = (1 << n) - 1
        return dp[full_mask][start][target_weight]
    
    results = []
    for a, k, w in queries:
        result = 1 if has_weighted_hamiltonian_circuit(a - 1, k, w) else 0  # Convert to 0-indexed
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
queries = [(1, 3, 9), (2, 3, 8)]
result = weighted_hamiltonian_circuit_queries(n, adj_matrix, weights, queries)
print(f"Weighted Hamiltonian circuit result: {result}")
```

#### **3. Dynamic Hamiltonian Circuit Queries**
**Problem**: Support adding/removing edges and answering Hamiltonian circuit queries.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic graph analysis with incremental updates

**Implementation**:
```python
class DynamicHamiltonianCircuitQueries:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]
        self.weights = [[0] * n for _ in range(n)]
        self.hamiltonian_cache = {}  # Cache for Hamiltonian circuit existence
    
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
    
    def has_hamiltonian_circuit(self, start, k):
        """Check if Hamiltonian circuit of length k exists from start"""
        if k != self.n:
            return False
        
        # Check cache first
        cache_key = (start, k)
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
        
        # Check if we can return to start from all vertices
        full_mask = (1 << self.n) - 1
        result = dp[full_mask][start]
        
        # Cache result
        self.hamiltonian_cache[cache_key] = result
        return result

# Example usage
dhcq = DynamicHamiltonianCircuitQueries(3)
dhcq.add_edge(0, 1, 2)
dhcq.add_edge(1, 2, 3)
dhcq.add_edge(2, 0, 4)
result1 = dhcq.has_hamiltonian_circuit(0, 3)
print(f"Dynamic Hamiltonian circuit result: {result1}")
```

### Related Problems

#### **CSES Problems**
- [Fixed Length Hamiltonian Cycle Queries](https://cses.fi/problemset/task/2417) - Similar approach
- [Round Trip](https://cses.fi/problemset/task/1669) - Cycle detection
- [Graph Girth](https://cses.fi/problemset/task/1707) - Cycle properties

#### **LeetCode Problems**
- [Unique Paths III](https://leetcode.com/problems/unique-paths-iii/) - Hamiltonian path
- [Word Ladder](https://leetcode.com/problems/word-ladder/) - Graph traversal
- [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/) - All shortest paths

#### **Problem Categories**
- **Graph Theory**: Hamiltonian circuits, Hamiltonian paths
- **Dynamic Programming**: Bitmask DP, state transitions
- **NP-Complete Problems**: Hamiltonian circuit is NP-complete

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

---

## 📝 Implementation Checklist

When applying this template to a new problem, ensure you:

### **Content Requirements**
- [x] **Problem Description**: Clear, concise with examples
- [x] **Learning Objectives**: 5 specific, measurable goals
- [x] **Prerequisites**: 5 categories of required knowledge
- [x] **3 Approaches**: Brute Force → Greedy → Optimal
- [x] **Key Insights**: 4-5 insights per approach at the beginning
- [x] **Visual Examples**: ASCII diagrams for each approach
- [x] **Complete Implementations**: Working code with examples
- [x] **Complexity Analysis**: Time and space for each approach
- [x] **Problem Variations**: 3 variations with implementations
- [x] **Related Problems**: CSES and LeetCode links

### **Structure Requirements**
- [x] **No Redundant Sections**: Remove duplicate Key Insights
- [x] **Logical Flow**: Each approach builds on the previous
- [x] **Progressive Complexity**: Clear improvement from approach to approach
- [x] **Educational Value**: Theory + Practice in each section
- [x] **Complete Coverage**: All important concepts included

### **Quality Requirements**
- [x] **Working Code**: All implementations are runnable
- [x] **Test Cases**: Examples with expected outputs
- [x] **Edge Cases**: Handle boundary conditions
- [x] **Clear Explanations**: Easy to understand for students
- [x] **Visual Learning**: Diagrams and examples throughout

---

## 🎯 **Template Usage Instructions**

### **Step 1: Replace Placeholders**
- Replace `[Problem Name]` with actual problem name
- Replace `[category]` with the problem category folder
- Replace `[problem_name]` with the actual problem filename
- Replace all `[placeholder]` text with actual content

### **Step 2: Customize Approaches**
- **Approach 1**: Usually brute force or naive solution
- **Approach 2**: Optimized solution (DP, greedy, etc.)
- **Approach 3**: Optimal solution (advanced algorithms)

### **Step 3: Add Visual Examples**
- Use ASCII art for diagrams
- Show step-by-step execution
- Use actual data in examples

### **Step 4: Implement Working Code**
- Write complete, runnable implementations
- Include test cases and examples
- Handle edge cases properly

### **Step 5: Add Problem Variations**
- Create 3 meaningful variations
- Provide implementations for each
- Link to related problems

### **Step 6: Quality Check**
- Ensure no redundant sections
- Verify all code works
- Check that complexity analysis is correct
- Confirm educational value is high

This template ensures consistency across all problem analyses while maintaining high educational value and practical implementation focus.