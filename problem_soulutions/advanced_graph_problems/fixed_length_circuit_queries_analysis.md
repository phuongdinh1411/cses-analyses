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