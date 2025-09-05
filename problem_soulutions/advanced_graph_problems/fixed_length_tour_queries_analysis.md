---
layout: simple
title: "Fixed Length Tour Queries"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_tour_queries_analysis
---

# Fixed Length Tour Queries

## Problem Description

**Problem**: Given a graph, answer queries about tours (cycles) of fixed length starting and ending at specific vertices.

**Input**: 
- n, m: number of vertices and edges
- m lines: a b (edge between vertices a and b)
- q: number of queries
- q lines: u k (query: is there a tour of length k starting and ending at vertex u?)

**Output**: For each query, print "YES" if tour exists, "NO" otherwise.

**Example**:
```
Input:
4 4
1 2
2 3
3 4
4 1
3
1 3
1 4
2 2

Output:
NO
YES
NO

Explanation: 
No tour of length 3 starting at vertex 1
Tour 1→2→3→4→1 has length 4 starting at vertex 1
No tour of length 2 starting at vertex 2
```

### 📊 Visual Example

**Input Graph:**
```
    1 ──── 2 ──── 3 ──── 4
    │                     │
    └─────────────────────┘
```

**Tour Query Analysis:**
```
Query 1: Vertex 1, length 3
Possible tours:
- 1 → 2 → 3 → 1 ✗ (no edge 3→1)
- 1 → 2 → 4 → 1 ✗ (no edge 2→4)
- 1 → 4 → 3 → 1 ✗ (no edge 4→3)

No tour of length 3 starting at vertex 1.
Result: NO

Query 2: Vertex 1, length 4
Tour: 1 → 2 → 3 → 4 → 1 ✓
Length: 4 edges ✓
Starts and ends at vertex 1 ✓
Result: YES

Query 3: Vertex 2, length 2
Possible tours:
- 2 → 3 → 2 ✗ (no edge 3→2)
- 2 → 1 → 2 ✗ (no edge 1→2)

No tour of length 2 starting at vertex 2.
Result: NO
```

**Matrix Exponentiation for Tour Counting:**
```
Adjacency Matrix A:
    1  2  3  4
1 [ 0  1  0  1 ]
2 [ 1  0  1  0 ]
3 [ 0  1  0  1 ]
4 [ 1  0  1  0 ]

A³ (tours of length 3):
    1  2  3  4
1 [ 0  0  0  0 ]  ← A[1][1] = 0 (no tour 1→1 of length 3)
2 [ 0  0  0  0 ]
3 [ 0  0  0  0 ]
4 [ 0  0  0  0 ]

A⁴ (tours of length 4):
    1  2  3  4
1 [ 2  0  0  0 ]  ← A[1][1] = 2 (tours 1→1 of length 4)
2 [ 0  2  0  0 ]
3 [ 0  0  2  0 ]
4 [ 0  0  0  2 ]
```

**Tour Properties:**
```
For Tour:
- Must start and end at the same vertex
- Can repeat vertices and edges
- Length = number of edges in the tour
- Graph must be connected
- No restrictions on vertex/edge repetition
```

**Tour vs Cycle vs Circuit:**
```
Tour: Starts and ends at same vertex (can repeat vertices/edges)
- 1 → 2 → 3 → 4 → 1 ✓
- 1 → 2 → 1 → 2 → 1 ✓

Cycle: Simple tour (no repeated vertices except start/end)
- 1 → 2 → 3 → 4 → 1 ✓
- 1 → 2 → 1 → 2 → 1 ✗ (repeats vertices)

Circuit: Same as tour (starts and ends at same vertex)
- 1 → 2 → 3 → 4 → 1 ✓
- 1 → 2 → 1 → 2 → 1 ✓
```

**Tour Examples:**
```
Length 1: 1 → 1 (self-loop) - if exists
Length 2: 1 → 2 → 1
Length 3: None (no direct path of length 3)
Length 4: 1 → 2 → 3 → 4 → 1
Length 5: 1 → 2 → 3 → 4 → 1 → 2 → 1
Length 6: 1 → 2 → 3 → 4 → 1 → 2 → 3 → 1
```

**Tour Construction Process:**
```
Step 1: Start from vertex 1
Current path: [1]

Step 2: Try to extend path
Options: 1 → 2, 1 → 4
Choose: 1 → 2
Current path: [1, 2]

Step 3: Continue extending
Options: 2 → 1, 2 → 3
Choose: 2 → 3
Current path: [1, 2, 3]

Step 4: Continue extending
Options: 3 → 2, 3 → 4
Choose: 3 → 4
Current path: [1, 2, 3, 4]

Step 5: Complete tour
Options: 4 → 1, 4 → 3
Choose: 4 → 1
Final tour: [1, 2, 3, 4, 1]
Length: 4 edges
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find tours (cycles) of specific lengths
- Use graph algorithms and matrix exponentiation
- Handle cycle detection efficiently
- Apply dynamic programming concepts

**Key Observations:**
- This is a cycle detection problem
- Can use adjacency matrix exponentiation
- Need to find cycles starting/ending at specific vertex
- Matrix powers give walk counts

### Step 2: Matrix Exponentiation Approach
**Idea**: Use adjacency matrix exponentiation to find tours of different lengths.

```python
def fixed_length_tour_queries(n, edges, queries):
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

**Why this works:**
- Uses matrix exponentiation for efficient tour counting
- Handles cycle detection correctly
- Efficient implementation
- O(n³ log k) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_fixed_length_tour_queries():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    q = int(input())
    queries = []
    for _ in range(q):
        u, k = map(int, input().split())
        queries.append((u, k))
    
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            print("YES")
        else:
            print("NO")

# Main execution
if __name__ == "__main__":
    solve_fixed_length_tour_queries()
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
        (4, [(1, 2), (2, 3), (3, 4), (4, 1)], [(1, 3), (1, 4), (2, 2)]),
        (3, [(1, 2), (2, 3), (3, 1)], [(1, 3), (2, 3), (3, 3)]),
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
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
- **Matrix Exponentiation**: Efficiently computes tour counts
- **Tour Detection**: Counts tours using each edge exactly once
- **Binary Exponentiation**: Reduces complexity from O(k) to O(log k)
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Tour Detection**
- Tours are cycles starting and ending at same vertex
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Matrix Exponentiation**
- Efficient tour counting algorithm
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Binary Exponentiation**
- Fast matrix power computation
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Tours with Weights
**Problem**: Each edge has a weight, find weighted tours.

```python
def weighted_tour_queries(n, edges, queries, weights):
    # Build weighted adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = weights.get((a, b), 1)
        adj_matrix[b-1][a-1] = weights.get((b, a), 1)
    
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 2: Tours with Constraints
**Problem**: Find tours avoiding certain edges.

```python
def constrained_tour_queries(n, edges, queries, forbidden_edges):
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 3: Dynamic Tours
**Problem**: Support adding/removing edges and maintaining tour counts.

```python
class DynamicTourQueries:
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
    
    def has_tour(self, u, k):
        def matrix_multiply(a, b):
            result = [[0] * self.n for _ in range(self.n)]
            for i in range(self.n):
                for j in range(self.n):
                    for k_idx in range(self.n):
                        result[i][j] += a[i][k_idx] * b[k_idx][j]
            return result
        
        def matrix_power(matrix, power):
            if power == 0:
                # Identity matrix
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
        return powered_matrix[u-1][u-1] > 0
```

### Variation 4: Tours with Multiple Constraints
**Problem**: Find tours satisfying multiple constraints.

```python
def multi_constrained_tour_queries(n, edges, queries, constraints):
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 5: Tours with Edge Replacement
**Problem**: Allow replacing existing edges with new ones.

```python
def edge_replacement_tour_queries(n, edges, queries, replacement_edges):
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
    
    # Try different edge replacements
    best_results = []
    for u, k in queries:
        best_has_tour = False
        
        # Try original edges
        adj_matrix = [[0] * n for _ in range(n)]
        for a, b in edges:
            adj_matrix[a-1][b-1] = 1
            adj_matrix[b-1][a-1] = 1
        
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            best_has_tour = True
        
        # Try each replacement
        for old_edge, new_edge in replacement_edges:
            # Create modified edges
            modified_edges = [e for e in edges if e != old_edge and (e[1], e[0]) != old_edge]
            modified_edges.append(new_edge)
            
            # Build modified matrix
            modified_matrix = [[0] * n for _ in range(n)]
            for a, b in modified_edges:
                modified_matrix[a-1][b-1] = 1
                modified_matrix[b-1][a-1] = 1
            
            # Check if tour exists
            powered_matrix = matrix_power(modified_matrix, k)
            if powered_matrix[u-1][u-1] > 0:
                best_has_tour = True
        
        best_results.append("YES" if best_has_tour else "NO")
    
    return best_results
```

## 🔗 Related Problems

- **[Tour Detection](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Tour detection algorithms
- **[Matrix Exponentiation](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Matrix exponentiation algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts

## 📚 Learning Points

1. **Tour Detection**: Essential for cycle analysis
2. **Matrix Exponentiation**: Efficient tour counting
3. **Binary Exponentiation**: Important optimization technique
4. **Graph Theory**: Important graph theory concept

---

**This is a great introduction to tour detection and matrix exponentiation!** 🎯
        else:
            results.append("NO")
    
    return results
```

**Why this works:**
- Uses matrix exponentiation efficiently
- Finds tours of any length correctly
- Handles multiple queries
- O(n³ log k) per query

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_fixed_length_tour_queries():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    q = int(input())
    queries = []
    for _ in range(q):
        u, k = map(int, input().split())
        queries.append((u, k))
    
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            print("YES")
        else:
            print("NO")

# Main execution
if __name__ == "__main__":
    solve_fixed_length_tour_queries()
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
        (4, [(1, 2), (2, 3), (3, 4), (4, 1)], [(1, 3), (1, 4), (2, 2)]),
        (3, [(1, 2), (2, 3), (3, 1)], [(1, 3), (2, 3)]),
    ]
    
    for n, edges, queries in test_cases:
        result = solve_test(n, edges, queries)
        print(f"n={n}, edges={edges}, queries={queries}")
        print(f"Results: {result}")
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n³ log k) - matrix exponentiation
- **Space**: O(n²) - adjacency matrix

### Why This Solution Works
- **Matrix Exponentiation**: Finds tours efficiently
- **Binary Exponentiation**: Handles large k values
- **Tour Counting**: Counts all possible tours
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Tour Properties**
- Cycles starting and ending at same vertex
- Essential for tour counting
- Key optimization technique
- Enables efficient solution

### 2. **Matrix Exponentiation**
- Adjacency matrix raised to power k
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Binary Exponentiation**
- Efficient power calculation
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Tour with Constraints
**Problem**: Find tours avoiding certain edges.

```python
def constrained_tour_queries(n, edges, queries, forbidden_edges):
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj_matrix[a-1][b-1] = 1
            adj_matrix[b-1][a-1] = 1  # Undirected graph
    
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 2: Weighted Tour Queries
**Problem**: Each edge has a weight, find tours with specific total weight.

```python
def weighted_tour_queries(n, edges, weights, queries):
    # Build weighted adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj_matrix[a-1][b-1] = weight
        adj_matrix[b-1][a-1] = weight
    
    def matrix_multiply(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if a[i][k] > 0 and b[k][j] > 0:
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
    for u, k, target_weight in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] == target_weight:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 3: Tour Length Range Queries
**Problem**: Find tours with length in a given range.

```python
def tour_range_queries(n, edges, queries):
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1  # Undirected graph
    
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
    for u, min_len, max_len in queries:
        has_tour = False
        for k in range(min_len, max_len + 1):
            powered_matrix = matrix_power(adj_matrix, k)
            if powered_matrix[u-1][u-1] > 0:
                has_tour = True
                break
        
        results.append("YES" if has_tour else "NO")
    
    return results
```

### Variation 4: Dynamic Tour Queries
**Problem**: Support adding/removing edges and answering tour queries.

```python
class DynamicTourQueries:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]
    
    def add_edge(self, a, b):
        self.adj_matrix[a-1][b-1] = 1
        self.adj_matrix[b-1][a-1] = 1  # Undirected graph
    
    def remove_edge(self, a, b):
        self.adj_matrix[a-1][b-1] = 0
        self.adj_matrix[b-1][a-1] = 0
    
    def has_tour(self, u, k):
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
        return powered_matrix[u-1][u-1] > 0
```

### Variation 5: Tour with Multiple Constraints
**Problem**: Find tours satisfying multiple constraints.

```python
def multi_constrained_tour_queries(n, edges, queries, constraints):
    # Build adjacency matrix with constraints
    adj_matrix = [[0] * n for _ in range(n)]
    forbidden_edges = constraints.get('forbidden_edges', set())
    
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj_matrix[a-1][b-1] = 1
            adj_matrix[b-1][a-1] = 1  # Undirected graph
    
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

## 🔗 Related Problems

- **[Matrix Exponentiation](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Matrix algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[Tour Counting](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Tour algorithms

## 📚 Learning Points

1. **Tour Properties**: Essential for tour counting
2. **Matrix Exponentiation**: Efficient power calculation
3. **Graph Theory**: Important graph theory concept
4. **Binary Exponentiation**: Important for performance

---

**This is a great introduction to tour queries and matrix exponentiation!** 🎯
        else:
            results.append("NO")
    
    return results
```

**Why this works:**
- Uses matrix exponentiation
- Finds tours of any length efficiently
- Handles multiple queries
- O(n³ log k) per query

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_fixed_length_tour_queries():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    q = int(input())
    queries = []
    
    for _ in range(q):
        u, k = map(int, input().split())
        queries.append((u, k))
    
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            print("YES")
        else:
            print("NO")

# Main execution
if __name__ == "__main__":
    solve_fixed_length_tour_queries()
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
        (4, [(1, 2), (2, 3), (3, 4), (4, 1)], [(1, 3), (1, 4), (2, 2)]),
        (3, [(1, 2), (2, 3), (3, 1)], [(1, 3), (2, 3)]),
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
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
- **Matrix Exponentiation**: Finds tours of any length efficiently
- **Adjacency Matrix**: Represents graph structure
- **Binary Exponentiation**: Efficient power calculation
- **Optimal Approach**: Handles large tour lengths

## 🎯 Key Insights

### 1. **Matrix Exponentiation**
- Adjacency matrix raised to power k gives walk counts
- Key insight for optimization
- Essential for understanding
- Enables efficient solution

### 2. **Tour Detection**
- Check diagonal elements for tours
- Important for performance
- Fundamental concept
- Essential for algorithm

### 3. **Binary Exponentiation**
- Efficient power calculation
- Reduces complexity from O(k) to O(log k)
- Simple but important optimization
- Essential for large k values

## 🎯 Problem Variations

### Variation 1: Weighted Tour Queries
**Problem**: Each edge has a weight. Find tours with specific total weight.

```python
def weighted_tour_queries(n, edges, weights, queries):
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            results.append(powered_matrix[u-1][u-1])
        else:
            results.append(-1)  # No tour
    
    return results
```

### Variation 2: Simple Tour Queries
**Problem**: Find simple tours (no repeated vertices except start/end).

```python
def simple_tour_queries(n, edges, queries):
    # For simple tours, we need to track visited vertices
    # This is more complex and requires state tracking
    
    def has_simple_tour(start, length):
        if length > n:
            return False  # Pigeonhole principle
        
        # Use DFS to find simple tours
        def dfs(node, visited, remaining_length):
            if remaining_length == 0:
                return node == start
            
            for neighbor in range(n):
                if adj_matrix[node][neighbor] and neighbor not in visited:
                    if dfs(neighbor, visited | {neighbor}, remaining_length - 1):
                        return True
            
            return False
        
        return dfs(start, {start}, length - 1)
    
    # Build adjacency matrix
    adj_matrix = [[0] * n for _ in range(n)]
    for a, b in edges:
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1
    
    # Answer queries
    results = []
    for u, k in queries:
        if has_simple_tour(u-1, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 3: Tour Count Queries
**Problem**: Count number of tours of specific length.

```python
def tour_count_queries(n, edges, queries):
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        results.append(powered_matrix[u-1][u-1])
    
    return results
```

### Variation 4: Directed Tour Queries
**Problem**: Handle directed graphs with tour queries.

```python
def directed_tour_queries(n, edges, queries):
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
    for u, k in queries:
        powered_matrix = matrix_power(adj_matrix, k)
        if powered_matrix[u-1][u-1] > 0:
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 5: Dynamic Tour Queries
**Problem**: Support adding/removing edges and answering tour queries.

```python
class DynamicTourQueries:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]
    
    def add_edge(self, a, b):
        self.adj_matrix[a-1][b-1] = 1
        self.adj_matrix[b-1][a-1] = 1
    
    def remove_edge(self, a, b):
        self.adj_matrix[a-1][b-1] = 0
        self.adj_matrix[b-1][a-1] = 0
    
    def query_tour(self, u, k):
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
        return powered_matrix[u-1][u-1] > 0
```

## 🔗 Related Problems

- **[Matrix Exponentiation](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Matrix algorithms
- **[Cycle Detection](/cses-analyses/problem_soulutions/graph_algorithms/cycle_finding_analysis)**: Graph algorithms
- **[Tour Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Tour algorithms

## 📚 Learning Points

1. **Matrix Exponentiation**: Essential for tour counting
2. **Cycle Detection**: Key technique for graph problems
3. **Binary Exponentiation**: Efficient power calculation
4. **Tour Algorithms**: Common pattern in graph problems

---

**This is a great introduction to tour queries and cycle detection!** 🎯 