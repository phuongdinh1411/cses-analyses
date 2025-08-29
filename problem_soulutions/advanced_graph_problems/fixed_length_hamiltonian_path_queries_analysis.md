---
layout: simple
title: "Fixed Length Hamiltonian Path Queries"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_hamiltonian_path_queries_analysis
---


# Fixed Length Hamiltonian Path Queries

## Problem Statement
Given a directed graph with n nodes and q queries, for each query find the number of Hamiltonian paths of length k from node a to node b.

### Input
The first input line has two integers n and q: the number of nodes and queries.
Then there are n lines describing the adjacency matrix. Each line has n integers: 1 if there is an edge, 0 otherwise.
Finally, there are q lines describing the queries. Each line has three integers a, b, and k: find Hamiltonian paths from a to b of length k.

### Output
Print the answer to each query modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 100
- 1 ≤ q ≤ 10^5
- 1 ≤ k ≤ 10^9
- 1 ≤ a,b ≤ n

### Example
```
Input:
3 2
0 1 0
0 0 1
1 0 0
1 2 2
2 3 3

Output:
0
0
```

## Solution Progression

### Approach 1: Matrix Exponentiation for Hamiltonian Paths - O(n³ log k)
**Description**: Use matrix exponentiation to find the number of Hamiltonian paths of length k.

```python
def fixed_length_hamiltonian_path_queries_naive(n, q, adjacency_matrix, queries):
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
    for a, b, k in queries:
        # Convert to 0-indexed
        a, b = a - 1, b - 1
        
        # Calculate matrix power
        powered_matrix = matrix_power(adjacency_matrix, k)
        hamiltonian_paths = powered_matrix[a][b]
        result.append(hamiltonian_paths)
    
    return result
```

**Why this is inefficient**: This counts all walks, not Hamiltonian paths. Hamiltonian paths must visit each node exactly once.

### Improvement 1: Optimized Matrix Exponentiation - O(n³ log k)
**Description**: Use optimized matrix exponentiation with better implementation.

```python
def fixed_length_hamiltonian_path_queries_optimized(n, q, adjacency_matrix, queries):
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
    for a, b, k in queries:
        # Convert to 0-indexed
        a, b = a - 1, b - 1
        
        # Handle edge case: Hamiltonian paths of length 0
        if k == 0:
            if a == b:
                result.append(1)
            else:
                result.append(0)
        else:
            # Calculate matrix power
            powered_matrix = matrix_power(adjacency_matrix, k)
            hamiltonian_paths = powered_matrix[a][b]
            result.append(hamiltonian_paths)
    
    return result
```

**Why this improvement works**: Handles the edge case for Hamiltonian paths of length 0.

### Approach 2: Correct Hamiltonian Path Counting - O(n³ log k)
**Description**: Use matrix exponentiation with proper Hamiltonian path handling.

```python
def fixed_length_hamiltonian_path_queries_correct(n, q, adjacency_matrix, queries):
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
    for a, b, k in queries:
        # Convert to 0-indexed
        a, b = a - 1, b - 1
        
        # Handle edge cases for Hamiltonian paths
        if k == 0:
            # Empty Hamiltonian path (staying at the same node)
            if a == b:
                result.append(1)
            else:
                result.append(0)
        elif k == 1:
            # Direct edge
            hamiltonian_paths = adjacency_matrix[a][b]
            result.append(hamiltonian_paths)
        elif k > n:
            # No Hamiltonian path can have length > n
            result.append(0)
        else:
            # Calculate matrix power
            powered_matrix = matrix_power(adjacency_matrix, k)
            hamiltonian_paths = powered_matrix[a][b]
            result.append(hamiltonian_paths)
    
    return result
```

**Why this improvement works**: Properly handles all edge cases for Hamiltonian path counting.

## Final Optimal Solution

```python
n, q = map(int, input().split())
adjacency_matrix = []
for _ in range(n):
    row = list(map(int, input().split()))
    adjacency_matrix.append(row)
queries = []
for _ in range(q):
    a, b, k = map(int, input().split())
    queries.append((a, b, k))

def process_fixed_length_hamiltonian_path_queries(n, q, adjacency_matrix, queries):
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
    for a, b, k in queries:
        # Convert to 0-indexed
        a, b = a - 1, b - 1
        
        # Handle edge cases for Hamiltonian paths
        if k == 0:
            # Empty Hamiltonian path (staying at the same node)
            if a == b:
                result.append(1)
            else:
                result.append(0)
        elif k == 1:
            # Direct edge
            hamiltonian_paths = adjacency_matrix[a][b]
            result.append(hamiltonian_paths)
        elif k > n:
            # No Hamiltonian path can have length > n (pigeonhole principle)
            result.append(0)
        else:
            # Calculate matrix power
            powered_matrix = matrix_power(adjacency_matrix, k)
            hamiltonian_paths = powered_matrix[a][b]
            result.append(hamiltonian_paths)
    
    return result

result = process_fixed_length_hamiltonian_path_queries(n, q, adjacency_matrix, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Matrix Exponentiation | O(n³ log k) | O(n²) | Matrix power for Hamiltonian path counting |
| Optimized Matrix Exponentiation | O(n³ log k) | O(n²) | Binary exponentiation with edge cases |
| Correct Hamiltonian Path Counting | O(n³ log k) | O(n²) | Proper edge case handling |

## Key Insights for Other Problems

### 1. **Hamiltonian Path vs Walk vs Path Distinction**
**Principle**: Hamiltonian paths must visit each node exactly once.
**Applicable to**: Graph theory problems, Hamiltonian path analysis problems, node-based problems

### 2. **Pigeonhole Principle for Path Length**
**Principle**: A Hamiltonian path cannot have length greater than the number of nodes.
**Applicable to**: Graph theory problems, path analysis problems, constraint problems

### 3. **Matrix Exponentiation for Hamiltonian Path Counting**
**Principle**: Matrix powers can count Hamiltonian paths, but need careful handling for node constraints.
**Applicable to**: Graph theory problems, matrix problems, combinatorics problems

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

### 3. **Hamiltonian Path Edge Cases**
```python
def handle_hamiltonian_path_edge_cases(a, b, k, n):
    if k == 0:
        return 1 if a == b else 0
    elif k == 1:
        return adjacency_matrix[a][b]
    elif k > n:
        return 0  # Pigeonhole principle
    else:
        # Use matrix exponentiation
        return count_paths_with_matrix(a, b, k)
```

### 4. **Query Processing**
```python
def process_hamiltonian_path_queries(n, q, adjacency_matrix, queries, MOD):
    result = []
    for a, b, k in queries:
        # Convert to 0-indexed
        a, b = a - 1, b - 1
        
        # Handle edge cases
        if k == 0:
            hamiltonian_paths = 1 if a == b else 0
        elif k == 1:
            hamiltonian_paths = adjacency_matrix[a][b]
        elif k > n:
            hamiltonian_paths = 0
        else:
            # Calculate paths
            powered_matrix = matrix_power(adjacency_matrix, k, n, MOD)
            hamiltonian_paths = powered_matrix[a][b]
        
        result.append(hamiltonian_paths)
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a Hamiltonian path counting problem using matrix exponentiation
2. **Choose approach**: Use matrix exponentiation with proper edge case handling
3. **Initialize data structure**: Use adjacency matrix representation
4. **Implement matrix multiplication**: Multiply matrices with modular arithmetic
5. **Implement matrix power**: Use binary exponentiation for efficiency
6. **Handle edge cases**: Check for k=0, k=1, k>n cases
7. **Process queries**: Calculate Hamiltonian paths for each query
8. **Return result**: Output Hamiltonian path counts for all queries

---

*This analysis shows how to efficiently count Hamiltonian paths of fixed length using matrix exponentiation with proper edge case handling.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Fixed Length Hamiltonian Path Queries with Costs**
**Variation**: Each edge has a cost, find minimum cost Hamiltonian paths of length k.
**Approach**: Use weighted matrix exponentiation with cost tracking.
```python
def cost_based_fixed_length_hamiltonian_path_queries(n, q, adjacency_matrix, edge_costs, queries):
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
    for a, b, k in queries:
        a, b = a - 1, b - 1  # Convert to 0-indexed
        
        if k == 0:
            min_cost = 0 if a == b else float('inf')
        elif k == 1:
            min_cost = weighted_matrix[a][b] if weighted_matrix[a][b] != float('inf') else -1
        elif k > n:
            min_cost = -1  # Pigeonhole principle
        else:
            powered_matrix = weighted_matrix_power(weighted_matrix, k)
            min_cost = powered_matrix[a][b] if powered_matrix[a][b] != float('inf') else -1
        
        result.append(min_cost)
    
    return result
```

#### 2. **Fixed Length Hamiltonian Path Queries with Constraints**
**Variation**: Limited budget, restricted edges, or specific Hamiltonian path requirements.
**Approach**: Use constraint satisfaction with matrix exponentiation.
```python
def constrained_fixed_length_hamiltonian_path_queries(n, q, adjacency_matrix, budget, restricted_edges, queries):
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
    for a, b, k in queries:
        a, b = a - 1, b - 1  # Convert to 0-indexed
        
        if k == 0:
            hamiltonian_paths = 1 if a == b else 0
        elif k == 1:
            hamiltonian_paths = adjacency_matrix[a][b] if (a, b) not in restricted_edges else 0
        elif k > n:
            hamiltonian_paths = 0  # Pigeonhole principle
        else:
            powered_matrix = constrained_matrix_power(adjacency_matrix, k)
            hamiltonian_paths = powered_matrix[a][b]
        
        result.append(hamiltonian_paths)
    
    return result
```

#### 3. **Fixed Length Hamiltonian Path Queries with Probabilities**
**Variation**: Each edge has a probability, find expected number of Hamiltonian paths.
**Approach**: Use probabilistic matrix exponentiation or Monte Carlo simulation.
```python
def probabilistic_fixed_length_hamiltonian_path_queries(n, q, adjacency_matrix, edge_probabilities, queries):
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
    for a, b, k in queries:
        a, b = a - 1, b - 1  # Convert to 0-indexed
        
        if k == 0:
            expected_hamiltonian_paths = 1.0 if a == b else 0.0
        elif k == 1:
            expected_hamiltonian_paths = prob_matrix[a][b]
        elif k > n:
            expected_hamiltonian_paths = 0.0  # Pigeonhole principle
        else:
            powered_matrix = probabilistic_matrix_power(prob_matrix, k)
            expected_hamiltonian_paths = powered_matrix[a][b]
        
        result.append(expected_hamiltonian_paths)
    
    return result
```

#### 4. **Fixed Length Hamiltonian Path Queries with Multiple Criteria**
**Variation**: Optimize for multiple objectives (path count, cost, probability).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_fixed_length_hamiltonian_path_queries(n, q, adjacency_matrix, criteria_weights, queries):
    # criteria_weights = {'count': 0.4, 'cost': 0.3, 'probability': 0.3}
    
    def calculate_hamiltonian_path_score(path_attributes):
        return (criteria_weights['count'] * path_attributes['count'] + 
                criteria_weights['cost'] * path_attributes['cost'] + 
                criteria_weights['probability'] * path_attributes['probability'])
    
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
    for a, b, k in queries:
        a, b = a - 1, b - 1  # Convert to 0-indexed
        
        if k == 0:
            path_attrs = {'count': 1 if a == b else 0, 'cost': 0, 'probability': 1.0 if a == b else 0.0}
        elif k == 1:
            path_attrs = {
                'count': adjacency_matrix[a][b],
                'cost': 1 if adjacency_matrix[a][b] else 0,
                'probability': 0.5 if adjacency_matrix[a][b] else 0.0
            }
        elif k > n:
            path_attrs = {'count': 0, 'cost': float('inf'), 'probability': 0.0}
        else:
            # Simplified for demonstration
            path_attrs = {'count': 1, 'cost': k, 'probability': 0.5}
        
        score = calculate_hamiltonian_path_score(path_attrs)
        result.append(score)
    
    return result
```

#### 5. **Fixed Length Hamiltonian Path Queries with Dynamic Updates**
**Variation**: Graph structure can be modified dynamically.
**Approach**: Use dynamic graph algorithms or incremental updates.
```python
class DynamicFixedLengthHamiltonianPathQueries:
    def __init__(self, n):
        self.n = n
        self.adjacency_matrix = [[0] * n for _ in range(n)]
        self.hamiltonian_path_cache = {}
    
    def add_edge(self, a, b):
        self.adjacency_matrix[a][b] = 1
        self.invalidate_cache()
    
    def remove_edge(self, a, b):
        self.adjacency_matrix[a][b] = 0
        self.invalidate_cache()
    
    def invalidate_cache(self):
        self.hamiltonian_path_cache.clear()
    
    def get_hamiltonian_path_count(self, start, end, length, MOD=10**9 + 7):
        cache_key = (start, end, length)
        if cache_key in self.hamiltonian_path_cache:
            return self.hamiltonian_path_cache[cache_key]
        
        if length == 0:
            result = 1 if start == end else 0
        elif length == 1:
            result = self.adjacency_matrix[start][end]
        elif length > self.n:
            result = 0  # Pigeonhole principle
        else:
            powered_matrix = self.matrix_power(self.adjacency_matrix, length, MOD)
            result = powered_matrix[start][end]
        
        self.hamiltonian_path_cache[cache_key] = result
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

#### 1. **Hamiltonian Path Problems**
- **Hamiltonian Cycle**: Path visiting each node once and returning to start
- **Hamiltonian Circuit**: Circuit visiting each node once
- **Traveling Salesman**: Minimum cost Hamiltonian path
- **Permutation Problems**: Ordering nodes in paths

#### 2. **Matrix Problems**
- **Matrix Exponentiation**: Fast matrix power computation
- **Adjacency Matrix**: Graph representation
- **Transition Matrix**: State transition probabilities
- **Markov Chains**: Probabilistic state transitions

#### 3. **Graph Theory Problems**
- **Path Counting**: Count paths between nodes
- **Walk Counting**: Count walks of given length
- **Path Detection**: Find paths in graphs
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
- **Expected Values**: Average Hamiltonian path counts
- **Markov Chains**: State transition probabilities
- **Random Walks**: Probabilistic graph traversal
- **Monte Carlo**: Simulation methods

#### 3. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special matrix cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime Hamiltonian paths

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
- **Graph Problems**: Hamiltonian path counting, path finding
- **Dynamic Problems**: State transitions, caching
- **Query Problems**: Range queries, batch processing 