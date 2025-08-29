---
layout: simple
title: "Fixed Length Circuit Queries"
permalink: /cses-analyses/problem_soulutions/advanced_graph_problems/fixed_length_circuit_queries_analysis
---


# Fixed Length Circuit Queries

## Problem Statement
Given a directed graph with n nodes and q queries, for each query find the number of circuits of length k starting and ending at node a.

### Input
The first input line has two integers n and q: the number of nodes and queries.
Then there are n lines describing the adjacency matrix. Each line has n integers: 1 if there is an edge, 0 otherwise.
Finally, there are q lines describing the queries. Each line has two integers a and k: find circuits from a to a of length k.

### Output
Print the answer to each query modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 100
- 1 ≤ q ≤ 10^5
- 1 ≤ k ≤ 10^9
- 1 ≤ a ≤ n

### Example
```
Input:
3 2
0 1 0
0 0 1
1 0 0
1 3
2 3

Output:
1
1
```

## Solution Progression

### Approach 1: Matrix Exponentiation for Circuits - O(n³ log k)
**Description**: Use matrix exponentiation to find the number of circuits of length k.

```python
def fixed_length_circuit_queries_naive(n, q, adjacency_matrix, queries):
    MOD = 10**9 + 7
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % MOD
        return result
    
    def matrix_power(matrix, power):
        # Initialize result as identity matrix
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        
        # Binary exponentiation
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2
        
        return result
    
    # Process queries
    result = []
    for a, k in queries:
        # Convert to 0-indexed
        a = a - 1
        
        # Calculate matrix power
        powered_matrix = matrix_power(adjacency_matrix, k)
        circuits = powered_matrix[a][a]  # Circuits start and end at same node
        result.append(circuits)
    
    return result
```

**Why this is inefficient**: This counts all walks that start and end at the same node, which includes circuits but also other types of walks.

### Improvement 1: Optimized Matrix Exponentiation - O(n³ log k)
**Description**: Use optimized matrix exponentiation with better implementation.

```python
def fixed_length_circuit_queries_optimized(n, q, adjacency_matrix, queries):
    MOD = 10**9 + 7
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % MOD
        return result
    
    def matrix_power(matrix, power):
        # Initialize result as identity matrix
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        
        # Binary exponentiation
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2
        
        return result
    
    # Process queries
    result = []
    for a, k in queries:
        # Convert to 0-indexed
        a = a - 1
        
        # Handle edge case: circuits of length 0
        if k == 0:
            result.append(1)  # Empty circuit
        else:
            # Calculate matrix power
            powered_matrix = matrix_power(adjacency_matrix, k)
            circuits = powered_matrix[a][a]
            result.append(circuits)
    
    return result
```

**Why this improvement works**: Handles the edge case for circuits of length 0.

### Approach 2: Correct Circuit Counting - O(n³ log k)
**Description**: Use matrix exponentiation with proper circuit handling.

```python
def fixed_length_circuit_queries_correct(n, q, adjacency_matrix, queries):
    MOD = 10**9 + 7
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % MOD
        return result
    
    def matrix_power(matrix, power):
        # Initialize result as identity matrix
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        
        # Binary exponentiation
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2
        
        return result
    
    # Process queries
    result = []
    for a, k in queries:
        # Convert to 0-indexed
        a = a - 1
        
        # Handle edge cases for circuits
        if k == 0:
            # Empty circuit (staying at the same node)
            result.append(1)
        elif k == 1:
            # Self-loop
            circuits = adjacency_matrix[a][a]
            result.append(circuits)
        else:
            # Calculate matrix power
            powered_matrix = matrix_power(adjacency_matrix, k)
            circuits = powered_matrix[a][a]
            result.append(circuits)
    
    return result
```

**Why this improvement works**: Properly handles all edge cases for circuit counting.

## Final Optimal Solution

```python
n, q = map(int, input().split())
adjacency_matrix = []
for _ in range(n):
    row = list(map(int, input().split()))
    adjacency_matrix.append(row)
queries = []
for _ in range(q):
    a, k = map(int, input().split())
    queries.append((a, k))

def process_fixed_length_circuit_queries(n, q, adjacency_matrix, queries):
    MOD = 10**9 + 7
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % MOD
        return result
    
    def matrix_power(matrix, power):
        # Initialize result as identity matrix
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        
        # Binary exponentiation
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2
        
        return result
    
    # Process queries
    result = []
    for a, k in queries:
        # Convert to 0-indexed
        a = a - 1
        
        # Handle edge cases for circuits
        if k == 0:
            # Empty circuit (staying at the same node)
            result.append(1)
        elif k == 1:
            # Self-loop
            circuits = adjacency_matrix[a][a]
            result.append(circuits)
        else:
            # Calculate matrix power
            powered_matrix = matrix_power(adjacency_matrix, k)
            circuits = powered_matrix[a][a]
            result.append(circuits)
    
    return result

result = process_fixed_length_circuit_queries(n, q, adjacency_matrix, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Matrix Exponentiation | O(n³ log k) | O(n²) | Matrix power for circuit counting |
| Optimized Matrix Exponentiation | O(n³ log k) | O(n²) | Binary exponentiation with edge cases |
| Correct Circuit Counting | O(n³ log k) | O(n²) | Proper edge case handling |

## Key Insights for Other Problems

### 1. **Circuit Counting with Matrix Exponentiation**
**Principle**: The diagonal elements of the k-th power of the adjacency matrix give the number of circuits of length k.
**Applicable to**: Circuit counting problems, graph analysis problems, matrix problems

### 2. **Self-Loop Handling**
**Principle**: Circuits of length 1 are self-loops in the adjacency matrix.
**Applicable to**: Graph theory problems, circuit detection problems, matrix analysis problems

### 3. **Empty Circuit Definition**
**Principle**: An empty circuit (length 0) represents staying at the same node.
**Applicable to**: Graph theory problems, circuit analysis problems, path counting problems

## Notable Techniques

### 1. **Matrix Multiplication**
```python
def matrix_multiply(a, b, n, MOD):
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % MOD
    return result
```

### 2. **Binary Matrix Exponentiation**
```python
def matrix_power(matrix, power, n, MOD):
    # Initialize result as identity matrix
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    
    # Binary exponentiation
    base = matrix
    while power > 0:
        if power % 2 == 1:
            result = matrix_multiply(result, base, n, MOD)
        base = matrix_multiply(base, base, n, MOD)
        power //= 2
    
    return result
```

### 3. **Circuit Counting**
```python
def count_circuits(adjacency_matrix, node, length, n, MOD):
    if length == 0:
        return 1  # Empty circuit
    elif length == 1:
        return adjacency_matrix[node][node]  # Self-loop
    else:
        powered_matrix = matrix_power(adjacency_matrix, length, n, MOD)
        return powered_matrix[node][node]  # Diagonal element
```

### 4. **Query Processing**
```python
def process_circuit_queries(n, q, adjacency_matrix, queries, MOD):
    result = []
    for a, k in queries:
        # Convert to 0-indexed
        a = a - 1
        
        # Handle edge cases
        if k == 0:
            circuits = 1
        elif k == 1:
            circuits = adjacency_matrix[a][a]
        else:
            powered_matrix = matrix_power(adjacency_matrix, k, n, MOD)
            circuits = powered_matrix[a][a]
        
        result.append(circuits)
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a circuit counting problem using matrix exponentiation
2. **Choose approach**: Use matrix exponentiation with proper edge case handling
3. **Initialize data structure**: Use adjacency matrix representation
4. **Implement matrix multiplication**: Multiply matrices with modular arithmetic
5. **Implement matrix power**: Use binary exponentiation for efficiency
6. **Handle edge cases**: Check for k=0, k=1 cases
7. **Process queries**: Calculate circuits for each query using diagonal elements
8. **Return result**: Output circuit counts for all queries

---

*This analysis shows how to efficiently count circuits of fixed length using matrix exponentiation with proper edge case handling.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Fixed Length Circuit Queries with Costs**
**Variation**: Each edge has a cost, find minimum cost circuits of length k.
**Approach**: Use weighted matrix exponentiation with cost tracking.
```python
def cost_based_fixed_length_circuit_queries(n, q, adjacency_matrix, edge_costs, queries):
    MOD = 10**9 + 7
    
    def weighted_matrix_multiply(a, b):
        result = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if a[i][k] != float('inf') and b[k][j] != float('inf'):
                        new_cost = a[i][k] + b[k][j]
                        if new_cost < result[i][j]:
                            result[i][j] = new_cost
        return result
    
    def weighted_matrix_power(matrix, power):
        # Initialize result as identity matrix (0 cost for self-loops)
        result = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 0
        
        # Binary exponentiation
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = weighted_matrix_multiply(result, base)
            base = weighted_matrix_multiply(base, base)
            power //= 2
        
        return result
    
    # Build weighted adjacency matrix
    weighted_matrix = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if adjacency_matrix[i][j] == 1:
                weighted_matrix[i][j] = edge_costs.get((i, j), 1)
    
    # Process queries
    result = []
    for a, k in queries:
        a = a - 1  # Convert to 0-indexed
        
        if k == 0:
            min_cost = 0
        elif k == 1:
            min_cost = weighted_matrix[a][a] if weighted_matrix[a][a] != float('inf') else -1
        else:
            powered_matrix = weighted_matrix_power(weighted_matrix, k)
            min_cost = powered_matrix[a][a] if powered_matrix[a][a] != float('inf') else -1
        
        result.append(min_cost)
    
    return result
```

#### 2. **Fixed Length Circuit Queries with Constraints**
**Variation**: Limited budget, restricted edges, or specific circuit requirements.
**Approach**: Use constraint satisfaction with matrix exponentiation.
```python
def constrained_fixed_length_circuit_queries(n, q, adjacency_matrix, budget, restricted_edges, queries):
    MOD = 10**9 + 7
    
    def constrained_matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    # Check if edge (i,k) and (k,j) are not restricted
                    if (i, k) not in restricted_edges and (k, j) not in restricted_edges:
                        result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % MOD
        return result
    
    def constrained_matrix_power(matrix, power):
        # Initialize result as identity matrix
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        
        # Binary exponentiation
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = constrained_matrix_multiply(result, base)
            base = constrained_matrix_multiply(base, base)
            power //= 2
        
        return result
    
    # Process queries
    result = []
    for a, k in queries:
        a = a - 1  # Convert to 0-indexed
        
        if k == 0:
            circuits = 1
        elif k == 1:
            circuits = adjacency_matrix[a][a] if (a, a) not in restricted_edges else 0
        else:
            powered_matrix = constrained_matrix_power(adjacency_matrix, k)
            circuits = powered_matrix[a][a]
        
        result.append(circuits)
    
    return result
```

#### 3. **Fixed Length Circuit Queries with Probabilities**
**Variation**: Each edge has a probability, find expected number of circuits.
**Approach**: Use probabilistic matrix exponentiation or Monte Carlo simulation.
```python
def probabilistic_fixed_length_circuit_queries(n, q, adjacency_matrix, edge_probabilities, queries):
    MOD = 10**9 + 7
    
    def probabilistic_matrix_multiply(a, b):
        result = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def probabilistic_matrix_power(matrix, power):
        # Initialize result as identity matrix
        result = [[0.0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1.0
        
        # Binary exponentiation
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = probabilistic_matrix_multiply(result, base)
            base = probabilistic_matrix_multiply(base, base)
            power //= 2
        
        return result
    
    # Build probabilistic adjacency matrix
    prob_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if adjacency_matrix[i][j] == 1:
                prob_matrix[i][j] = edge_probabilities.get((i, j), 0.5)
    
    # Process queries
    result = []
    for a, k in queries:
        a = a - 1  # Convert to 0-indexed
        
        if k == 0:
            expected_circuits = 1.0
        elif k == 1:
            expected_circuits = prob_matrix[a][a]
        else:
            powered_matrix = probabilistic_matrix_power(prob_matrix, k)
            expected_circuits = powered_matrix[a][a]
        
        result.append(expected_circuits)
    
    return result
```

#### 4. **Fixed Length Circuit Queries with Multiple Criteria**
**Variation**: Optimize for multiple objectives (circuit count, cost, probability).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_fixed_length_circuit_queries(n, q, adjacency_matrix, criteria_weights, queries):
    # criteria_weights = {'count': 0.4, 'cost': 0.3, 'probability': 0.3}
    
    def calculate_circuit_score(circuit_attributes):
        return (criteria_weights['count'] * circuit_attributes['count'] + 
                criteria_weights['cost'] * circuit_attributes['cost'] + 
                criteria_weights['probability'] * circuit_attributes['probability'])
    
    def multi_criteria_matrix_multiply(a, b):
        result = [[{'count': 0, 'cost': 0, 'probability': 0.0} for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    # Combine attributes
                    new_count = a[i][k]['count'] * b[k][j]['count']
                    new_cost = a[i][k]['cost'] + b[k][j]['cost']
                    new_prob = a[i][k]['probability'] * b[k][j]['probability']
                    
                    result[i][j]['count'] += new_count
                    result[i][j]['cost'] = min(result[i][j]['cost'], new_cost) if result[i][j]['cost'] > 0 else new_cost
                    result[i][j]['probability'] += new_prob
        
        return result
    
    # Process queries
    result = []
    for a, k in queries:
        a = a - 1  # Convert to 0-indexed
        
        if k == 0:
            circuit_attrs = {'count': 1, 'cost': 0, 'probability': 1.0}
        elif k == 1:
            circuit_attrs = {
                'count': adjacency_matrix[a][a],
                'cost': 1 if adjacency_matrix[a][a] else 0,
                'probability': 0.5 if adjacency_matrix[a][a] else 0.0
            }
        else:
            # Simplified for demonstration
            circuit_attrs = {'count': 1, 'cost': k, 'probability': 0.5}
        
        score = calculate_circuit_score(circuit_attrs)
        result.append(score)
    
    return result
```

#### 5. **Fixed Length Circuit Queries with Dynamic Updates**
**Variation**: Graph structure can be modified dynamically.
**Approach**: Use dynamic graph algorithms or incremental updates.
```python
class DynamicFixedLengthCircuitQueries:
    def __init__(self, n):
        self.n = n
        self.adjacency_matrix = [[0] * n for _ in range(n)]
        self.circuit_cache = {}
    
    def add_edge(self, a, b):
        self.adjacency_matrix[a][b] = 1
        self.invalidate_cache()
    
    def remove_edge(self, a, b):
        self.adjacency_matrix[a][b] = 0
        self.invalidate_cache()
    
    def invalidate_cache(self):
        self.circuit_cache.clear()
    
    def get_circuit_count(self, node, length, MOD=10**9 + 7):
        cache_key = (node, length)
        if cache_key in self.circuit_cache:
            return self.circuit_cache[cache_key]
        
        if length == 0:
            result = 1
        elif length == 1:
            result = self.adjacency_matrix[node][node]
        else:
            powered_matrix = self.matrix_power(self.adjacency_matrix, length, MOD)
            result = powered_matrix[node][node]
        
        self.circuit_cache[cache_key] = result
        return result
    
    def matrix_multiply(self, a, b, MOD):
        result = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % MOD
        return result
    
    def matrix_power(self, matrix, power, MOD):
        result = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            result[i][i] = 1
        
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = self.matrix_multiply(result, base, MOD)
            base = self.matrix_multiply(base, base, MOD)
            power //= 2
        
        return result
```

### Related Problems & Concepts

#### 1. **Circuit Counting Problems**
- **Hamiltonian Circuits**: Circuits visiting each node once
- **Eulerian Circuits**: Circuits using each edge once
- **Simple Circuits**: Circuits without repeated nodes
- **Directed Circuits**: Circuits in directed graphs

#### 2. **Matrix Problems**
- **Matrix Exponentiation**: Fast matrix power computation
- **Adjacency Matrix**: Graph representation
- **Transition Matrix**: State transition probabilities
- **Markov Chains**: Probabilistic state transitions

#### 3. **Graph Theory Problems**
- **Path Counting**: Count paths between nodes
- **Walk Counting**: Count walks of given length
- **Cycle Detection**: Find cycles in graphs
- **Connectivity**: Graph connectivity analysis

#### 4. **Dynamic Programming Problems**
- **State Transitions**: Dynamic state changes
- **Memoization**: Caching computed results
- **Optimal Substructure**: Breaking into subproblems
- **Overlapping Subproblems**: Reusing solutions

#### 5. **Query Processing Problems**
- **Range Queries**: Querying ranges of data
- **Point Queries**: Querying specific points
- **Batch Queries**: Processing multiple queries
- **Online Queries**: Real-time query processing

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large matrices
- **Edge Cases**: Robust matrix operations

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient matrix traversal
- **Sliding Window**: Optimal submatrix problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Linear Algebra**
- **Matrix Operations**: Multiplication, exponentiation
- **Eigenvalues**: Matrix spectral properties
- **Determinants**: Matrix determinants
- **Inverses**: Matrix inverses

#### 2. **Probability Theory**
- **Expected Values**: Average circuit counts
- **Markov Chains**: State transition probabilities
- **Random Walks**: Probabilistic graph traversal
- **Monte Carlo**: Simulation methods

#### 3. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special matrix cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime circuits

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Matrix and graph problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Matrix Problems**: Exponentiation, multiplication
- **Graph Problems**: Circuit counting, path finding
- **Dynamic Problems**: State transitions, caching
- **Query Problems**: Range queries, batch processing 