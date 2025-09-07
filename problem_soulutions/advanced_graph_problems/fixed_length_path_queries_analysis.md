---
layout: simple
title: "Fixed Length Path Queries"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_path_queries_analysis
---

# Fixed Length Path Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of path queries and reachability in graphs
- Apply matrix exponentiation for efficient path counting
- Implement dynamic programming for path queries with fixed lengths
- Optimize path query algorithms for multiple queries
- Handle large path lengths using modular arithmetic and matrix operations

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Matrix exponentiation, dynamic programming, graph reachability
- **Data Structures**: Adjacency matrices, matrices, arrays
- **Mathematical Concepts**: Matrix operations, modular arithmetic, graph theory
- **Programming Skills**: Matrix multiplication, modular arithmetic, dynamic programming
- **Related Problems**: Fixed Length Cycle Queries (similar matrix approach), Shortest Routes I (path finding), Message Route (reachability)

## Problem Description

**Problem**: Given a graph, answer queries about paths of fixed length between vertices.

**Input**: 
- n, m: number of vertices and edges
- m lines: a b (edge between vertices a and b)
- q: number of queries
- q lines: u v k (query: is there a path of length k from u to v?)

**Output**: For each query, print "YES" if path exists, "NO" otherwise.

**Example**:
```
Input:
4 4
1 2
2 3
3 4
1 4
3
1 4 1
1 4 2
1 4 3

Output:
YES
NO
YES

Explanation: 
Path 1→4 has length 1 (direct edge)
No path of length 2 from 1 to 4
Path 1→2→3→4 has length 3
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find paths of specific lengths
- Use graph algorithms and matrix exponentiation
- Handle multiple queries efficiently
- Apply dynamic programming concepts

**Key Observations:**
- This is a path counting problem
- Can use adjacency matrix exponentiation
- Need to handle different path lengths
- Matrix multiplication is key

### Step 2: Matrix Exponentiation Approach
**Idea**: Use adjacency matrix exponentiation to find paths of different lengths.

```python
def fixed_length_paths_matrix(n, edges, queries):
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1  # Undirected graph
    
    # Matrix exponentiation for different lengths
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            # Identity matrix
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    results = []
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

**Why this works:**
- Matrix exponentiation efficiently computes path counts
- Handles all path lengths in O(log k) time
- Optimal for multiple queries
- Clear and readable implementation

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_fixed_length_path_queries():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    q = int(input())
    queries = []
    
    for _ in range(q):
        u, v, k = map(int, input().split())
        queries.append((u, v, k))
    
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1  # Undirected graph
    
    # Matrix exponentiation for different lengths
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k_idx in range(n):
                    result[i][j] += a[i][k_idx] * b[k_idx][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            # Identity matrix
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            print("YES")
        else:
            print("NO")

# Main execution
if __name__ == "__main__":
    solve_fixed_length_path_queries()
```

**Why this works:**
- Optimal matrix exponentiation approach
- Handles all edge cases efficiently
- Clear and readable code
- Efficient for multiple queries

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4), (1, 4)], [(1, 4, 1), (1, 4, 2), (1, 4, 3)]),
        (3, [(1, 2), (2, 3)], [(1, 3, 1), (1, 3, 2), (1, 3, 3)]),
    ]
    
    for n, edges, queries in test_cases:
        result = solve_test(n, edges, queries)
        print(f"n={n}, edges={edges}, queries={queries}")
        print(f"Result: {result}")
        print()

def solve_test(n, edges, queries):
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1  # Undirected graph
    
    # Matrix exponentiation for different lengths
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k_idx in range(n):
                    result[i][j] += a[i][k_idx] * b[k_idx][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            # Identity matrix
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    results = []
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n³ log k) - matrix exponentiation for each query
- **Space**: O(n²) - adjacency matrix and result matrices

### Why This Solution Works
- **Matrix Exponentiation**: Efficiently computes path counts
- **Binary Exponentiation**: Reduces complexity from O(k) to O(log k)
- **Adjacency Matrix**: Natural representation for path counting
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Matrix Exponentiation**
- Efficient path counting algorithm
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Adjacency Matrix**
- Natural graph representation
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Binary Exponentiation**
- Fast matrix power computation
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Weighted Path Queries
**Problem**: Each edge has a weight, find paths with specific total weight.

```python
def weighted_path_queries(n, edges, queries, weights):
    # Build weighted adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj_matrix[a-1][b-1] = weight
        adj_matrix[b-1][a-1] = weight  # Undirected graph
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k_idx in range(n):
                    result[i][j] += a[i][k_idx] * b[k_idx][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    results = []
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 2: Constrained Path Queries
**Problem**: Find paths avoiding certain edges.

```python
def constrained_path_queries(n, edges, queries, forbidden_edges):
    # Build adjacency matrix excluding forbidden edges
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj_matrix[a-1][b-1] = 1
            adj_matrix[b-1][a-1] = 1
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k_idx in range(n):
                    result[i][j] += a[i][k_idx] * b[k_idx][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    results = []
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 3: Dynamic Path Queries
**Problem**: Support adding/removing edges and maintaining path information.

```python
class DynamicPathQueries:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]
        self.edges = set()
    
    def add_edge(self, a, b):
        if (a, b) not in self.edges and (b, a) not in self.edges:
            self.edges.add((a, b))
            self.adj_matrix[a-1][b-1] = 1
            self.adj_matrix[b-1][a-1] = 1
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.edges.remove((a, b))
            self.adj_matrix[a-1][b-1] = 0
            self.adj_matrix[b-1][a-1] = 0
            return True
        elif (b, a) in self.edges:
            self.edges.remove((b, a))
            self.adj_matrix[a-1][b-1] = 0
            self.adj_matrix[b-1][a-1] = 0
            return True
        return False
    
    def has_path(self, u, v, k):
        def matrix_multiply(a, b):
            result = [[0] * self.n for _ in range(self.n)]
            for i in range(self.n):
                for j in range(self.n):
                    for k_idx in range(self.n):
                        result[i][j] += a[i][k_idx] * b[k_idx][j]
            return result
        
        def matrix_power(matrix, power):
            if power == 0:
                return [[1 if i == j else 0 for j in range(self.n)] for i in range(self.n)]
            if power == 1:
                return matrix
            
            half = matrix_power(matrix, power // 2)
            squared = matrix_multiply(half, half)
            
            if power % 2 == 0:
                return squared
            else:
                return matrix_multiply(squared, matrix)
        
        powered_matrix = matrix_power(self.adj_matrix, k)
        return powered_matrix[u-1][v-1] > 0
```

### Variation 4: Multiple Constraint Path Queries
**Problem**: Find paths satisfying multiple constraints.

```python
def multi_constrained_path_queries(n, edges, queries, constraints):
    # Apply multiple constraints
    forbidden_edges = constraints.get('forbidden_edges', set())
    required_edges = constraints.get('required_edges', set())
    
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj_matrix[a-1][b-1] = 1
            adj_matrix[b-1][a-1] = 1
    
    # Add required edges
    for a, b in required_edges:
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k_idx in range(n):
                    result[i][j] += a[i][k_idx] * b[k_idx][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    results = []
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 5: Edge Replacement Path Queries
**Problem**: Allow replacing existing edges with new ones.

```python
def edge_replacement_path_queries(n, edges, queries, replacement_edges):
    def has_path_with_matrix(adj_matrix, u, v, k):
        def matrix_multiply(a, b):
            result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k_idx in range(n):
                        result[i][j] += a[i][k_idx] * b[k_idx][j]
            return result
        
        def matrix_power(matrix, power):
            if power == 0:
                return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            if power == 1:
                return matrix
            
            half = matrix_power(matrix, power // 2)
            squared = matrix_multiply(half, half)
            
            if power % 2 == 0:
                return squared
            else:
                return matrix_multiply(squared, matrix)
        
        powered_matrix = matrix_power(adj_matrix, k)
        return powered_matrix[u-1][v-1] > 0
    
    # Build original adjacency matrix
    original_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        original_matrix[a-1][b-1] = 1
        original_matrix[b-1][a-1] = 1
    
    # Try different edge replacements
    best_results = []
    for u, v, k in queries:
        best_result = False
        
        # Try original matrix
        if has_path_with_matrix(original_matrix, u, v, k):
            best_result = True
        
        # Try each replacement
        for old_edge, new_edge in replacement_edges:
            # Create modified matrix
            modified_matrix = [row[:] for row in original_matrix]
            old_a, old_b = old_edge
            new_a, new_b = new_edge
            
            # Remove old edge
            modified_matrix[old_a-1][old_b-1] = 0
            modified_matrix[old_b-1][old_a-1] = 0
            
            # Add new edge
            modified_matrix[new_a-1][new_b-1] = 1
            modified_matrix[new_b-1][new_a-1] = 1
            
            # Check path
            if has_path_with_matrix(modified_matrix, u, v, k):
                best_result = True
        
        best_results.append("YES" if best_result else "NO")
    
    return best_results
```

## 🔗 Related Problems

- **[Matrix Exponentiation](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Matrix exponentiation algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[Dynamic Programming](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Dynamic programming techniques

## 📚 Learning Points

1. **Matrix Exponentiation**: Essential for path counting
2. **Adjacency Matrix**: Natural graph representation
3. **Binary Exponentiation**: Important optimization technique
4. **Graph Theory**: Important graph theory concept

---

**This is a great introduction to path queries and matrix exponentiation!** 🎯
        else:
            results.append("NO")
    
    return results
```

**Why this works:**
- Uses matrix exponentiation
- Finds paths of any length efficiently
- Handles multiple queries
- O(n³ log k) per query

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_fixed_length_paths():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    q = int(input())
    queries = []
    
    for _ in range(q):
        u, v, k = map(int, input().split())
        queries.append((u, v, k))
    
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1  # Undirected graph
    
    # Matrix exponentiation for different lengths
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            # Identity matrix
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            print("YES")
        else:
            print("NO")

# Main execution
if __name__ == "__main__":
    solve_fixed_length_paths()
```

**Why this works:**
- Optimal matrix exponentiation approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4), (1, 4)], [(1, 4, 1), (1, 4, 2), (1, 4, 3)]),
        (3, [(1, 2), (2, 3)], [(1, 3, 1), (1, 3, 2)]),
    ]
    
    for n, edges, queries in test_cases:
        result = solve_test(n, edges, queries)
        print(f"n={n}, edges={edges}, queries={queries}")
        print(f"Result: {result}")
        print()

def solve_test(n, edges, queries):
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    results = []
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n³ log k) per query - matrix exponentiation
- **Space**: O(n²) - adjacency matrix

### Why This Solution Works
- **Matrix Exponentiation**: Finds paths of any length efficiently
- **Adjacency Matrix**: Represents graph structure
- **Binary Exponentiation**: Efficient power calculation
- **Optimal Approach**: Handles large path lengths

## 🎯 Key Insights

### 1. **Matrix Exponentiation**
- Adjacency matrix raised to power k gives paths of length k
- Key insight for optimization
- Essential for understanding
- Enables efficient solution

### 2. **Path Counting**
- Matrix multiplication counts paths
- Important for performance
- Fundamental concept
- Essential for algorithm

### 3. **Binary Exponentiation**
- Efficient power calculation
- Reduces complexity from O(k) to O(log k)
- Simple but important optimization
- Essential for large k values

## 🎯 Problem Variations

### Variation 1: Weighted Path Queries
**Problem**: Each edge has a weight. Find paths with specific total weight.

```python
def weighted_path_queries(n, edges, weights, queries):
    # Build weighted adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        adj_matrix[a-1][b-1] = weights[i]
        adj_matrix[b-1][a-1] = weights[i]
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if a[i][k] > 0 and b[k][j] > 0:
                        result[i][j] = max(result[i][j], a[i][k] + b[k][j])
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            return [[0 if i != j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    results = []
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            results.append(powered_matrix[u-1][v-1])
        else:
            results.append(-1)  # No path
    
    return results
```

### Variation 2: Shortest Path Queries
**Problem**: Find shortest path length between vertices.

```python
def shortest_path_queries(n, edges, queries):
    # Floyd-Warshall for all pairs shortest paths
    dist = [[float('inf')] * n for _ in range(n)]
    
    # Initialize distances
    for i in range(n):
        dist[i][i] = 0
    
    for a, b in edges:
        dist[a-1][b-1] = 1
        dist[b-1][a-1] = 1
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Answer queries
    results = []
    for u, v in queries:
        if dist[u-1][v-1] == float('inf'):
            results.append(-1)  # No path
        else:
            results.append(dist[u-1][v-1])
    
    return results
```

### Variation 3: Path Count Queries
**Problem**: Count number of paths of specific length.

```python
def path_count_queries(n, edges, queries):
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    results = []
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        results.append(powered_matrix[u-1][v-1])
    
    return results
```

### Variation 4: Directed Graph Paths
**Problem**: Handle directed graphs with path queries.

```python
def directed_path_queries(n, edges, queries):
    # Build directed adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = 1  # Directed edge
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def matrix_power(matrix, power):
        if power == 0:
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if power == 1:
            return matrix
        
        half = matrix_power(matrix, power // 2)
        squared = matrix_multiply(half, half)
        
        if power % 2 == 0:
            return squared
        else:
            return matrix_multiply(squared, matrix)
    
    # Answer queries
    results = []
    for u, v, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][v-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 5: Dynamic Path Queries
**Problem**: Support adding/removing edges and answering path queries.

```python
class DynamicPathQueries:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]
    
    def add_edge(self, a, b):
        self.adj_matrix[a-1][b-1] = 1
        self.adj_matrix[b-1][a-1] = 1
    
    def remove_edge(self, a, b):
        self.adj_matrix[a-1][b-1] = 0
        self.adj_matrix[b-1][a-1] = 0
    
    def query_path(self, u, v, k):
        def matrix_multiply(a, b):
            result = [[0] * self.n for _ in range(self.n)]
            for i in range(self.n):
                for j in range(self.n):
                    for k in range(self.n):
                        result[i][j] += a[i][k] * b[k][j]
            return result
        
        def matrix_power(matrix, power):
            if power == 0:
                return [[1 if i == j else 0 for j in range(self.n)] for i in range(self.n)]
            if power == 1:
                return matrix
            
            half = matrix_power(matrix, power // 2)
            squared = matrix_multiply(half, half)
            
            if power % 2 == 0:
                return squared
            else:
                return matrix_multiply(squared, matrix)
        
        powered_matrix = matrix_power(self.adj_matrix, k)
        return powered_matrix[u-1][v-1] > 0
```

## 🔗 Related Problems

- **[Matrix Exponentiation](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Matrix algorithms
- **[Graph Traversal](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms
- **[Path Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Path algorithms

## 📚 Learning Points

1. **Matrix Exponentiation**: Essential for path counting
2. **Adjacency Matrix**: Key representation for graph algorithms
3. **Binary Exponentiation**: Efficient power calculation
4. **Path Algorithms**: Common pattern in graph problems

---

**This is a great introduction to matrix exponentiation and path counting!** 🎯 