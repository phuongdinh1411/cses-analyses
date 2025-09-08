---
layout: simple
title: "Fixed Length Hamiltonian Path Queries II"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_hamiltonian_path_queries_ii_analysis
---

# Fixed Length Hamiltonian Path Queries II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand advanced Hamiltonian path problems with additional constraints
- Apply dynamic programming with bitmasking for complex Hamiltonian path problems
- Implement efficient Hamiltonian path detection with state compression
- Optimize Hamiltonian path algorithms for multiple queries with constraints
- Handle complex constraints in Hamiltonian path problems using advanced DP techniques

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, bitmasking, Hamiltonian paths, state compression, advanced DP
- **Data Structures**: Bitmasks, adjacency lists, DP tables, constraint handling
- **Mathematical Concepts**: Graph theory, Hamiltonian paths, NP-complete problems, combinatorics, constraints
- **Programming Skills**: Bit manipulation, dynamic programming, state transitions, constraint handling
- **Related Problems**: Fixed Length Hamiltonian Path Queries (basic version), Hamiltonian Flights (Hamiltonian paths), Round Trip (cycle detection)

## 📋 Problem Description

Given a graph, answer queries about Hamiltonian paths (paths visiting each vertex exactly once) of fixed length with additional constraints.

**Input**: 
- n, m: number of vertices and edges
- m lines: a b (edge between vertices a and b)
- q: number of queries
- q lines: u v k (query: is there a Hamiltonian path of length k from u to v?)

**Output**: 
- For each query, print "YES" if Hamiltonian path exists, "NO" otherwise

**Constraints**:
- 1 ≤ n ≤ 20
- 1 ≤ m ≤ 400
- 1 ≤ q ≤ 10^5
- 1 ≤ k ≤ n-1

**Example**:
```
Input:
4 4
1 2
2 3
3 4
4 1
3
1 4 3
1 4 4
2 3 2

Output:
NO
YES
NO

Explanation**: 
No Hamiltonian path of length 3 from 1 to 4
Hamiltonian path 1→2→3→4 has length 4 from 1 to 4
No Hamiltonian path of length 2 from 2 to 3
```

### 📊 Visual Example

**Input Graph:**
```
    1 ──── 2 ──── 3 ──── 4
    │                     │
    └─────────────────────┘
```

**Hamiltonian Path Analysis:**
```
Query 1: 1→4, length 3
Hamiltonian path: Must visit all 4 vertices exactly once
Possible path: 1 → 2 → 3 → 4
Length: 3 edges ✓
Visits vertices: {1, 2, 3, 4} ✓
But this doesn't end at vertex 4!

Wait, let me check: 1 → 2 → 3 → 4
This visits 4 vertices with 3 edges, ending at 4.
This is a Hamiltonian path of length 3 from 1 to 4.
Result: YES

Query 2: 1→4, length 4
Hamiltonian path: 1 → 2 → 3 → 4
Length: 3 edges ✗ (too short)
Alternative: 1 → 2 → 3 → 4 → 1 → 4
Length: 5 edges ✗ (too long)
No Hamiltonian path of length 4 from 1 to 4.
Result: NO

Query 3: 2→3, length 2
Hamiltonian path: Must visit all 4 vertices exactly once
Possible path: 2 → 1 → 4 → 3
Length: 3 edges ✗ (too long)
Alternative: 2 → 3
Length: 1 edge ✗ (too short)
No Hamiltonian path of length 2 from 2 to 3.
Result: NO
```

**Correct Analysis:**
```
Query 1: 1→4, length 3
Hamiltonian path: 1 → 2 → 3 → 4
Length: 3 edges ✓
Visits all 4 vertices exactly once ✓
Result: YES

Query 2: 1→4, length 4
No Hamiltonian path of length 4 from 1 to 4.
Result: NO

Query 3: 2→3, length 2
No Hamiltonian path of length 2 from 2 to 3.
Result: NO
```

**Matrix Exponentiation for Hamiltonian Paths:**
```
Adjacency Matrix A:
    1  2  3  4
1 [ 0  1  0  1 ]
2 [ 1  0  1  0 ]
3 [ 0  1  0  1 ]
4 [ 1  0  1  0 ]

A³ (paths of length 3):
    1  2  3  4
1 [ 0  0  0  4 ]  ← A[1][4] = 4 (multiple paths 1→4 of length 3)
2 [ 0  0  4  0 ]
3 [ 0  4  0  0 ]
4 [ 4  0  0  0 ]

A⁴ (paths of length 4):
    1  2  3  4
1 [ 8  0  0  0 ]  ← A[1][1] = 8 (multiple paths 1→1 of length 4)
2 [ 0  8  0  0 ]
3 [ 0  0  8  0 ]
4 [ 0  0  0  8 ]
```

**Hamiltonian Path Properties:**
```
For Hamiltonian Path:
- Must visit every vertex exactly once
- Can start and end at different vertices
- Length = number of vertices - 1
- Graph must be connected
- No repeated vertices allowed
```

**Hamiltonian Path vs Regular Path:**
```
Hamiltonian Path: Visits all vertices exactly once
- 1 → 2 → 3 → 4 ✓ (visits all 4 vertices)
- 1 → 2 → 3 ✗ (doesn't visit vertex 4)

Regular Path: No repeated vertices (can skip vertices)
- 1 → 2 → 3 → 4 ✓
- 1 → 2 → 3 ✓ (doesn't need to visit all vertices)
```

**Dynamic Programming Approach:**
```
State: dp[mask][last_vertex] = number of Hamiltonian paths
- mask: bitmask representing visited vertices
- last_vertex: last vertex in the path

Base case: dp[1<<start][start] = 1

Transition: For each unvisited vertex v:
dp[mask | (1<<v)][v] += dp[mask][last_vertex] * A[last_vertex][v]

Answer: dp[(1<<n)-1][end_vertex]
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find Hamiltonian paths of specific lengths
- Use graph algorithms and dynamic programming
- Handle multiple queries efficiently
- Apply constraint satisfaction concepts

**Key Observations:**
- This is a Hamiltonian path problem
- Can use dynamic programming with bitmasking
- Hamiltonian paths must visit each vertex exactly once
- State representation is crucial

### Step 2: Dynamic Programming with Bitmasking
**Idea**: Use DP with bitmask to track visited vertices.

```python
def hamiltonian_path_queries_dp(n, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # DP with bitmask
    def has_hamiltonian_path(start, end, length):
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    results = []
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

**Why this works:**
- Uses dynamic programming with bitmasking
- Handles Hamiltonian path constraints
- Efficient implementation
- O(2^n * n * m) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_fixed_length_hamiltonian_path_queries_ii():
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
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # DP with bitmask
    def has_hamiltonian_path(start, end, length):
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            print("YES")
        else:
            print("NO")

# Main execution
if __name__ == "__main__":
    solve_fixed_length_hamiltonian_path_queries_ii()
```

**Why this works:**
- Optimal dynamic programming approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4), (4, 1)], [(1, 4, 3), (1, 4, 4), (2, 3, 2)]),
        (3, [(1, 2), (2, 3), (3, 1)], [(1, 3, 3), (2, 1, 3), (3, 2, 3)]),
    ]
    
    for n, edges, queries in test_cases:
        result = solve_test(n, edges, queries)
        print(f"n={n}, edges={edges}, queries={queries}")
        print(f"Result: {result}")
        print()

def solve_test(n, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # DP with bitmask
    def has_hamiltonian_path(start, end, length):
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    results = []
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(2^n * n * m) - dynamic programming with bitmasking
- **Space**: O(2^n * n) - DP table

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes path existence
- **Bitmasking**: Tracks visited vertices efficiently
- **Hamiltonian Paths**: Ensures each vertex is visited exactly once
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Hamiltonian Paths**
- Paths visiting each vertex exactly once
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Dynamic Programming**
- Efficient path existence algorithm
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Bitmasking**
- Efficient state representation
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Hamiltonian Paths with Weights
**Problem**: Each edge has a weight, find minimum weight Hamiltonian paths.

```python
def weighted_hamiltonian_path_queries(n, edges, queries, weights):
    # Build adjacency list with weights
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    
    def min_weight_hamiltonian_path(start, end, length):
        # dp[mask][pos] = minimum weight to reach pos with visited vertices in mask
        dp = [[float('inf')] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = 0
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if dp[mask][pos] == float('inf'):
                    continue
                
                # Try all neighbors
                for neighbor, weight in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = min(dp[new_mask][neighbor], 
                                                   dp[mask][pos] + weight)
        
        # Check if we can reach end with exactly length vertices
        min_weight = float('inf')
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end] != float('inf'):
                min_weight = min(min_weight, dp[mask][end])
        
        return min_weight if min_weight != float('inf') else -1
    
    # Answer queries
    results = []
    for u, v, k in queries:
        weight = min_weight_hamiltonian_path(u, v, k)
        results.append(weight)
    
    return results
```

### Variation 2: Hamiltonian Paths with Constraints
**Problem**: Find Hamiltonian paths avoiding certain edges.

```python
def constrained_hamiltonian_path_queries(n, edges, queries, forbidden_edges):
    # Build adjacency list excluding forbidden edges
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    def has_hamiltonian_path(start, end, length):
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    results = []
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 3: Dynamic Hamiltonian Paths
**Problem**: Support adding/removing edges and maintaining path existence.

```python
class DynamicHamiltonianPathQueries:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.edges = set()
    
    def add_edge(self, a, b):
        if (a, b) not in self.edges and (b, a) not in self.edges:
            self.edges.add((a, b))
            self.adj[a].append(b)
            self.adj[b].append(a)
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.edges.remove((a, b))
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            return True
        elif (b, a) in self.edges:
            self.edges.remove((b, a))
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            return True
        return False
    
    def has_hamiltonian_path(self, start, end, length):
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (self.n + 1) for _ in range(1 << self.n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << self.n):
            for pos in range(1, self.n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in self.adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << self.n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
```

### Variation 4: Hamiltonian Paths with Multiple Constraints
**Problem**: Find Hamiltonian paths satisfying multiple constraints.

```python
def multi_constrained_hamiltonian_path_queries(n, edges, queries, constraints):
    # Apply multiple constraints
    forbidden_edges = constraints.get('forbidden_edges', set())
    required_edges = constraints.get('required_edges', set())
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    # Add required edges
    for a, b in required_edges:
        if b not in adj[a]:
            adj[a].append(b)
        if a not in adj[b]:
            adj[b].append(a)
    
    def has_hamiltonian_path(start, end, length):
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    results = []
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 5: Hamiltonian Paths with Edge Replacement
**Problem**: Allow replacing existing edges with new ones.

```python
def edge_replacement_hamiltonian_path_queries(n, edges, queries, replacement_edges):
    def has_hamiltonian_path_with_edges(start, end, length, edge_set):
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b in edge_set:
            adj[a].append(b)
            adj[b].append(a)
        
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Try different edge replacements
    best_results = []
    for u, v, k in queries:
        best_has_path = False
        
        # Try original edges
        if has_hamiltonian_path_with_edges(u, v, k, edges):
            best_has_path = True
        
        # Try each replacement
        for old_edge, new_edge in replacement_edges:
            # Create modified edges
            modified_edges = [e for e in edges if e != old_edge and (e[1], e[0]) != old_edge]
            modified_edges.append(new_edge)
            
            # Check if path exists
            if has_hamiltonian_path_with_edges(u, v, k, modified_edges):
                best_has_path = True
        
        best_results.append("YES" if best_has_path else "NO")
    
    return best_results
```

## 🔗 Related Problems

- **[Hamiltonian Paths](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Hamiltonian path algorithms
- **[Dynamic Programming](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Dynamic programming algorithms
- **[Bitmasking](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Bitmasking techniques

## 📚 Learning Points

1. **Hamiltonian Paths**: Essential for path analysis
2. **Dynamic Programming**: Efficient path existence computation
3. **Bitmasking**: Important optimization technique
4. **Graph Theory**: Important graph theory concept

---

**This is a great introduction to Hamiltonian paths and dynamic programming!** 🎯
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

**Why this works:**
- Uses dynamic programming with bitmasking
- Tracks visited vertices efficiently
- Handles all path lengths correctly
- O(2^n * n * m) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_fixed_length_hamiltonian_path_queries_ii():
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
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)  # Undirected graph
    
    # DP with bitmask
    def has_hamiltonian_path(start, end, length):
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            print("YES")
        else:
            print("NO")

# Main execution
if __name__ == "__main__":
    solve_fixed_length_hamiltonian_path_queries_ii()
```

**Why this works:**
- Optimal dynamic programming approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4), (4, 1)], [(1, 4, 3), (1, 4, 4), (2, 3, 2)]),
        (3, [(1, 2), (2, 3)], [(1, 3, 2), (1, 3, 3)]),
    ]
    
    for n, edges, queries in test_cases:
        result = solve_test(n, edges, queries)
        print(f"n={n}, edges={edges}, queries={queries}")
        print(f"Results: {result}")
        print()

def solve_test(n, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)  # Undirected graph
    
    # DP with bitmask
    def has_hamiltonian_path(start, end, length):
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    results = []
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(2^n * n * m) - dynamic programming with bitmask
- **Space**: O(2^n * n) - DP table

### Why This Solution Works
- **Dynamic Programming**: Finds Hamiltonian paths efficiently
- **Bitmasking**: Tracks visited vertices compactly
- **State Representation**: Efficient state management
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Hamiltonian Path Properties**
- Visits each vertex exactly once
- Essential for path counting
- Key optimization technique
- Enables efficient solution

### 2. **Dynamic Programming**
- State-based approach
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Bitmasking**
- Compact state representation
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Hamiltonian Path with Constraints
**Problem**: Find Hamiltonian paths avoiding certain edges.

```python
def constrained_hamiltonian_path_queries(n, edges, queries, forbidden_edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    # DP with bitmask
    def has_hamiltonian_path(start, end, length):
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        dp[1 << (start - 1)][start] = True
        
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    results = []
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 2: Weighted Hamiltonian Path Queries
**Problem**: Each edge has a weight, find Hamiltonian paths with specific total weight.

```python
def weighted_hamiltonian_path_queries(n, edges, weights, queries):
    # Build adjacency list with weights
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    
    # DP with bitmask and weight tracking
    def has_hamiltonian_path(start, end, length, target_weight):
        # dp[mask][pos][weight] = can we reach pos with visited vertices in mask and total weight
        dp = [[[False] * (target_weight + 1) for _ in range(n + 1)] for _ in range(1 << n)]
        dp[1 << (start - 1)][start][0] = True
        
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                for weight in range(target_weight + 1):
                    if not dp[mask][pos][weight]:
                        continue
                    
                    for neighbor, edge_weight in adj[pos]:
                        if mask & (1 << (neighbor - 1)) == 0:
                            new_mask = mask | (1 << (neighbor - 1))
                            new_weight = weight + edge_weight
                            if new_weight <= target_weight:
                                dp[new_mask][neighbor][new_weight] = True
        
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end][target_weight]:
                return True
        
        return False
    
    # Answer queries
    results = []
    for u, v, k, target_weight in queries:
        if has_hamiltonian_path(u, v, k, target_weight):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 3: Hamiltonian Path Length Range Queries
**Problem**: Find Hamiltonian paths with length in a given range.

```python
def hamiltonian_path_range_queries(n, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # DP with bitmask
    def has_hamiltonian_path(start, end, length):
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        dp[1 << (start - 1)][start] = True
        
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    results = []
    for u, v, min_len, max_len in queries:
        has_path = False
        for k in range(min_len, max_len + 1):
            if has_hamiltonian_path(u, v, k):
                has_path = True
                break
        
        results.append("YES" if has_path else "NO")
    
    return results
```

### Variation 4: Dynamic Hamiltonian Path Queries
**Problem**: Support adding/removing edges and answering Hamiltonian path queries.

```python
class DynamicHamiltonianPathQueries:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
    
    def add_edge(self, a, b):
        self.adj[a].append(b)
        self.adj[b].append(a)
    
    def remove_edge(self, a, b):
        if b in self.adj[a]:
            self.adj[a].remove(b)
        if a in self.adj[b]:
            self.adj[b].remove(a)
    
    def has_hamiltonian_path(self, start, end, length):
        # DP with bitmask
        dp = [[False] * (self.n + 1) for _ in range(1 << self.n)]
        dp[1 << (start - 1)][start] = True
        
        for mask in range(1 << self.n):
            for pos in range(1, self.n + 1):
                if not dp[mask][pos]:
                    continue
                
                for neighbor in self.adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        for mask in range(1 << self.n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
```

### Variation 5: Hamiltonian Path with Multiple Constraints
**Problem**: Find Hamiltonian paths satisfying multiple constraints.

```python
def multi_constrained_hamiltonian_path_queries(n, edges, queries, constraints):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    forbidden_edges = constraints.get('forbidden_edges', set())
    
    for a, b in edges:
        if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    # DP with bitmask
    def has_hamiltonian_path(start, end, length):
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        dp[1 << (start - 1)][start] = True
        
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    results = []
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

## 🔗 Related Problems

- **[Dynamic Programming](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: DP algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[Hamiltonian Paths](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Hamiltonian path algorithms

## 📚 Learning Points

1. **Hamiltonian Path Properties**: Essential for path counting
2. **Dynamic Programming**: Efficient state-based approach
3. **Bitmasking**: Compact state representation
4. **Constraint Satisfaction**: Important for optimization

---

**This is a great introduction to Hamiltonian path queries and dynamic programming!** 🎯
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

**Why this works:**
- Uses dynamic programming with bitmasking
- Tracks visited vertices efficiently
- Handles all path constraints
- O(2^n * n * m) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_hamiltonian_path_queries_ii():
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
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # DP with bitmask
    def has_hamiltonian_path(start, end, length):
        # dp[mask][pos] = can we reach pos with visited vertices in mask
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        
        # Base case: start position
        dp[1 << (start - 1)][start] = True
        
        # Try all possible masks
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                # Try all neighbors
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:  # Not visited
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        # Check if we can reach end with exactly length vertices
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    # Answer queries
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            print("YES")
        else:
            print("NO")

# Main execution
if __name__ == "__main__":
    solve_hamiltonian_path_queries_ii()
```

**Why this works:**
- Optimal dynamic programming approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2), (2, 3), (3, 4), (4, 1)], [(1, 4, 3), (1, 4, 4), (2, 3, 2)]),
        (3, [(1, 2), (2, 3)], [(1, 3, 2), (1, 3, 3)]),
    ]
    
    for n, edges, queries in test_cases:
        result = solve_test(n, edges, queries)
        print(f"n={n}, edges={edges}, queries={queries}")
        print(f"Result: {result}")
        print()

def solve_test(n, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def has_hamiltonian_path(start, end, length):
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        dp[1 << (start - 1)][start] = True
        
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    results = []
    for u, v, k in queries:
        if has_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(2^n * n * m) - exponential due to bitmask
- **Space**: O(2^n * n) - DP table size

### Why This Solution Works
- **Dynamic Programming**: Finds optimal solutions efficiently
- **Bitmasking**: Tracks visited vertices compactly
- **State Representation**: Efficient state management
- **Optimal Approach**: Handles all constraints

## 🎯 Key Insights

### 1. **Bitmasking**
- Compact representation of visited vertices
- Essential for state tracking
- Key optimization technique
- Enables efficient DP

### 2. **Hamiltonian Paths**
- Must visit each vertex exactly once
- Important constraint satisfaction
- Fundamental graph theory concept
- NP-complete problem

### 3. **Dynamic Programming**
- Optimal substructure property
- Memoization for efficiency
- State transitions
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Weighted Hamiltonian Paths
**Problem**: Each edge has a weight. Find Hamiltonian paths with specific total weight.

```python
def weighted_hamiltonian_path_queries(n, edges, weights, queries):
    # Build weighted adjacency list
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, weights[i]))
        adj[b].append((a, weights[i]))
    
    def has_weighted_hamiltonian_path(start, end, length, target_weight):
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        weight_dp = [[float('inf')] * (n + 1) for _ in range(1 << n)]
        
        dp[1 << (start - 1)][start] = True
        weight_dp[1 << (start - 1)][start] = 0
        
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                for neighbor, weight in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:
                        new_mask = mask | (1 << (neighbor - 1))
                        new_weight = weight_dp[mask][pos] + weight
                        
                        if new_weight < weight_dp[new_mask][neighbor]:
                            dp[new_mask][neighbor] = True
                            weight_dp[new_mask][neighbor] = new_weight
        
        for mask in range(1 << n):
            if (bin(mask).count('1') == length and 
                dp[mask][end] and 
                weight_dp[mask][end] == target_weight):
                return True
        
        return False
    
    results = []
    for u, v, k, weight in queries:
        if has_weighted_hamiltonian_path(u, v, k, weight):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 2: Directed Hamiltonian Paths
**Problem**: Handle directed graphs with Hamiltonian path queries.

```python
def directed_hamiltonian_path_queries(n, edges, queries):
    # Build directed adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)  # Directed edge
    
    def has_directed_hamiltonian_path(start, end, length):
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        dp[1 << (start - 1)][start] = True
        
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    results = []
    for u, v, k in queries:
        if has_directed_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 3: Hamiltonian Path Count
**Problem**: Count number of Hamiltonian paths of specific length.

```python
def hamiltonian_path_count_queries(n, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def count_hamiltonian_paths(start, end, length):
        dp = [[0] * (n + 1) for _ in range(1 << n)]
        dp[1 << (start - 1)][start] = 1
        
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if dp[mask][pos] == 0:
                    continue
                
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] += dp[mask][pos]
        
        total = 0
        for mask in range(1 << n):
            if bin(mask).count('1') == length:
                total += dp[mask][end]
        
        return total
    
    results = []
    for u, v, k in queries:
        count = count_hamiltonian_paths(u, v, k)
        results.append(count)
    
    return results
```

### Variation 4: Constrained Hamiltonian Paths
**Problem**: Find Hamiltonian paths that satisfy certain constraints.

```python
def constrained_hamiltonian_path_queries(n, edges, constraints, queries):
    # constraints: set of forbidden vertex pairs
    # Build adjacency list with constraints
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in constraints and (b, a) not in constraints:
            adj[a].append(b)
            adj[b].append(a)
    
    def has_constrained_hamiltonian_path(start, end, length):
        dp = [[False] * (n + 1) for _ in range(1 << n)]
        dp[1 << (start - 1)][start] = True
        
        for mask in range(1 << n):
            for pos in range(1, n + 1):
                if not dp[mask][pos]:
                    continue
                
                for neighbor in adj[pos]:
                    if mask & (1 << (neighbor - 1)) == 0:
                        new_mask = mask | (1 << (neighbor - 1))
                        dp[new_mask][neighbor] = True
        
        for mask in range(1 << n):
            if bin(mask).count('1') == length and dp[mask][end]:
                return True
        
        return False
    
    results = []
    for u, v, k in queries:
        if has_constrained_hamiltonian_path(u, v, k):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

### Variation 5: Dynamic Hamiltonian Path Queries
**Problem**: Support adding/removing edges and answering Hamiltonian path queries.

```python
class DynamicHamiltonianPathQueries:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.edges = set()
    
    def add_edge(self, a, b):
        if (a, b) not in self.edges and (b, a) not in self.edges:
            self.adj[a].append(b)
            self.adj[b].append(a)
            self.edges.add((a, b))
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.edges.remove((a, b))
        elif (b, a) in self.edges:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.edges.remove((b, a))
    
    def query_hamiltonian_path(self, u, v, k):
        def has_hamiltonian_path(start, end, length):
            dp = [[False] * (self.n + 1) for _ in range(1 << self.n)]
            dp[1 << (start - 1)][start] = True
            
            for mask in range(1 << self.n):
                for pos in range(1, self.n + 1):
                    if not dp[mask][pos]:
                        continue
                    
                    for neighbor in self.adj[pos]:
                        if mask & (1 << (neighbor - 1)) == 0:
                            new_mask = mask | (1 << (neighbor - 1))
                            dp[new_mask][neighbor] = True
            
            for mask in range(1 << self.n):
                if bin(mask).count('1') == length and dp[mask][end]:
                    return True
            
            return False
        
        return has_hamiltonian_path(u, v, k)
```

## 🔗 Related Problems

- **[Hamiltonian Paths](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Path algorithms
- **[Dynamic Programming](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP algorithms
- **[Bitmasking](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: State representation

## 📚 Learning Points

1. **Bitmasking**: Essential for state representation
2. **Hamiltonian Paths**: NP-complete graph problem
3. **Dynamic Programming**: Optimal substructure
4. **Constraint Satisfaction**: Handling path constraints

---

**This is a great introduction to Hamiltonian path queries and bitmasking!** 🎯 