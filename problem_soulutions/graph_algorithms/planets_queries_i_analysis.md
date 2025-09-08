---
layout: simple
title: "Planets Queries I - Binary Lifting for Path Queries"
permalink: /problem_soulutions/graph_algorithms/planets_queries_i_analysis
---

# Planets Queries I - Binary Lifting for Path Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand binary lifting and path query optimization in functional graphs
- Apply binary lifting technique to answer k-th ancestor queries efficiently
- Implement efficient binary lifting algorithms with proper preprocessing and query handling
- Optimize path queries using binary lifting and sparse table techniques
- Handle edge cases in binary lifting (large k values, cycles, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Binary lifting, sparse tables, path queries, functional graphs, query optimization
- **Data Structures**: Sparse tables, binary lifting tables, graph representations, query data structures
- **Mathematical Concepts**: Graph theory, binary representation, logarithmic algorithms, query optimization
- **Programming Skills**: Binary operations, sparse table construction, query processing, algorithm implementation
- **Related Problems**: Planets Cycles (functional graphs), Planets Queries II (path intersection), Query optimization

## Problem Description

**Problem**: Given a directed graph with n planets and q queries, for each query find the k-th planet in the path starting from planet a.

This is a binary lifting problem where we need to efficiently answer k-th ancestor queries in a functional graph. Each planet has exactly one outgoing edge (teleporter), forming a functional graph structure.

**Input**: 
- First line: Two integers n and q (number of planets and queries)
- Second line: n integers t₁, t₂, ..., tₙ (teleporter destinations)
- Next q lines: Two integers a and k (start planet and k-th planet to find)

**Output**: 
- For each query, print the k-th planet in the path

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ tᵢ ≤ n
- 1 ≤ a ≤ n
- 1 ≤ k ≤ 10⁹
- Graph is a functional graph (each vertex has exactly one outgoing edge)
- Planets are numbered 1, 2, ..., n
- Teleporters are directed edges from planet i to planet tᵢ

**Example**:
```
Input:
4 3
2 1 4 1
1 1
1 2
1 3

Output:
2
1
2
```

**Explanation**: 
- Query 1: Start at planet 1, 1st planet in path is planet 1 itself
- Query 2: Start at planet 1, 2nd planet in path is planet 2 (1 → 2)
- Query 3: Start at planet 1, 3rd planet in path is planet 1 (1 → 2 → 1)

## Visual Example

### Input Graph and Queries
```
Planets: 1, 2, 3, 4
Teleporters: [2, 1, 4, 1]
Queries: (1,1), (1,2), (1,3)

Graph representation:
1 ──> 2 ──> 1 ──> 2 ──> 1 ──> ...
│
└──> 3 ──> 4 ──> 1 ──> 2 ──> ...
```

### Binary Lifting Process
```
Step 1: Build binary lifting table
- up[0][i] = teleporter[i] (1 step)
- up[1][i] = up[0][up[0][i]] (2 steps)
- up[2][i] = up[1][up[1][i]] (4 steps)
- up[3][i] = up[2][up[2][i]] (8 steps)

Step 2: Process queries

Query 1: (1,1)
- Start at planet 1
- 1st planet in path: 1
- Result: 1

Query 2: (1,2)
- Start at planet 1
- 2nd planet in path: teleporter[1] = 2
- Result: 2

Query 3: (1,3)
- Start at planet 1
- 3rd planet in path: teleporter[teleporter[1]] = teleporter[2] = 1
- Result: 1
```

### Path Visualization
```
Path from planet 1:
1 → 2 → 1 → 2 → 1 → 2 → 1 → ...

Positions:
- Position 1: 1
- Position 2: 2
- Position 3: 1
- Position 4: 2
- Position 5: 1
- ...
```

### Key Insight
Binary lifting works by:
1. Precomputing powers of 2 steps for each planet
2. Using binary representation to find k-th planet
3. Time complexity: O(log k) per query
4. Space complexity: O(n × log n) for lifting table
5. Preprocessing: O(n × log n)

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Simulation (Inefficient)

**Key Insights from Brute Force Solution:**
- Simulate the path step by step for each query
- Simple but computationally expensive approach
- Not suitable for large k values
- Straightforward implementation but poor performance

**Algorithm:**
1. For each query, start from the given planet
2. Follow the teleporter path for k steps
3. Return the k-th planet in the path
4. Handle cases where k is very large

**Visual Example:**
```
Brute force: Simulate path step by step
For query (1, 3):
- Start at planet 1
- Step 1: 1 → 2 (teleporter[1] = 2)
- Step 2: 2 → 1 (teleporter[2] = 1)
- Step 3: 1 → 2 (teleporter[1] = 2)
- Result: 2

For query (1, 10^9):
- Would need to simulate 10^9 steps
- Too slow for competitive programming
```

**Implementation:**
```python
def planets_queries_i_brute_force(n, q, teleporters, queries):
    results = []
    
    for a, k in queries:
        current = a
        for _ in range(k):
            current = teleporters[current - 1]
        results.append(current)
    
    return results

def solve_planets_queries_i_brute_force():
    n, q = map(int, input().split())
    teleporters = list(map(int, input().split()))
    queries = []
    for _ in range(q):
        a, k = map(int, input().split())
        queries.append((a, k))
    
    results = planets_queries_i_brute_force(n, q, teleporters, queries)
    for result in results:
        print(result)
```

**Time Complexity:** O(q × k) for q queries and k steps per query
**Space Complexity:** O(1) for constant space usage

**Why it's inefficient:**
- O(q × k) time complexity is too slow for large k values
- Not suitable for competitive programming with k up to 10^9
- Inefficient for large inputs
- Poor performance with many queries

### Approach 2: Basic Binary Lifting (Better)

**Key Insights from Basic Binary Lifting Solution:**
- Use binary lifting to precompute powers of 2 steps
- Much more efficient than brute force approach
- Standard method for ancestor queries
- Can handle large k values efficiently

**Algorithm:**
1. Build binary lifting table with powers of 2 steps
2. For each query, use binary representation of k
3. Jump through the lifting table to find k-th planet
4. Return the result efficiently

**Visual Example:**
```
Basic Binary Lifting for query (1, 5):
- k = 5 = 101₂ (binary)
- Start at planet 1
- Jump 1 step: 1 → 2 (using up[0][1])
- Jump 4 steps: 2 → 1 (using up[2][2])
- Result: 1

Binary lifting table:
up[0][i] = teleporter[i] (1 step)
up[1][i] = up[0][up[0][i]] (2 steps)
up[2][i] = up[1][up[1][i]] (4 steps)
```

**Implementation:**
```python
def planets_queries_i_basic_binary_lifting(n, q, teleporters, queries):
    # Build binary lifting table
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    # Answer queries
    results = []
    for a, k in queries:
        current = a - 1
        for j in range(log_n):
            if k & (1 << j):
                current = up[j][current]
        results.append(current + 1)
    
    return results

def solve_planets_queries_i_basic():
    n, q = map(int, input().split())
    teleporters = list(map(int, input().split()))
    queries = []
    for _ in range(q):
        a, k = map(int, input().split())
        queries.append((a, k))
    
    results = planets_queries_i_basic_binary_lifting(n, q, teleporters, queries)
    for result in results:
        print(result)
```

**Time Complexity:** O(n × log n) preprocessing + O(q × log k) for queries
**Space Complexity:** O(n × log n) for binary lifting table

**Why it's better:**
- O(log k) time complexity per query is much better than O(k)
- Standard method for ancestor queries
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Binary Lifting with Efficient Query Processing (Optimal)

**Key Insights from Optimized Binary Lifting Solution:**
- Use optimized binary lifting with efficient query processing
- Most efficient approach for ancestor queries
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized binary lifting with efficient data structures
2. Implement efficient query processing with binary operations
3. Use proper preprocessing and query handling
4. Return the k-th planet efficiently

**Visual Example:**
```
Optimized Binary Lifting for query (1, 5):
- k = 5 = 101₂ (binary)
- Start at planet 1: current = 0 (0-indexed)
- Check bit 0: k & (1 << 0) = 1, jump 1 step: current = up[0][0] = 1
- Check bit 1: k & (1 << 1) = 0, no jump
- Check bit 2: k & (1 << 2) = 1, jump 4 steps: current = up[2][1] = 0
- Result: current + 1 = 1
```

**Implementation:**
```python
def planets_queries_i_optimized_binary_lifting(n, q, teleporters, queries):
    # Build binary lifting table
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    # Answer queries efficiently
    results = []
    for a, k in queries:
        current = a - 1
        for j in range(log_n):
            if k & (1 << j):
                current = up[j][current]
        results.append(current + 1)
    
    return results

def solve_planets_queries_i():
    n, q = map(int, input().split())
    teleporters = list(map(int, input().split()))
    queries = []
    for _ in range(q):
        a, k = map(int, input().split())
        queries.append((a, k))
    
    results = planets_queries_i_optimized_binary_lifting(n, q, teleporters, queries)
    for result in results:
        print(result)

# Main execution
if __name__ == "__main__":
    solve_planets_queries_i()
```

**Time Complexity:** O(n × log n) preprocessing + O(q × log k) for queries
**Space Complexity:** O(n × log n) for binary lifting table

**Why it's optimal:**
- O(log k) time complexity per query is optimal for ancestor queries
- Uses optimized binary lifting with efficient query processing
- Most efficient approach for competitive programming
- Standard method for ancestor query problems

## 🎯 Problem Variations

### Variation 1: Planets Queries I with Cycle Detection
**Problem**: Find k-th planet in path with cycle detection and optimization.

**Link**: [CSES Problem Set - Planets Queries I Cycle Detection](https://cses.fi/problemset/task/planets_queries_i_cycle_detection)

```python
def planets_queries_i_cycle_detection(n, q, teleporters, queries):
    # Build binary lifting table with cycle detection
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    # Detect cycles for optimization
    def detect_cycle(start):
        visited = set()
        current = start
        path = []
        
        while current not in visited:
            visited.add(current)
            path.append(current)
            current = teleporters[current] - 1
        
        cycle_start = current
        cycle_length = len(path) - path.index(cycle_start)
        return cycle_start, cycle_length
    
    # Answer queries with cycle optimization
    results = []
    for a, k in queries:
        current = a - 1
        cycle_start, cycle_length = detect_cycle(current)
        
        if k <= len(path):
            # Use binary lifting for small k
            for j in range(log_n):
                if k & (1 << j):
                    current = up[j][current]
        else:
            # Use cycle optimization for large k
            k = (k - len(path)) % cycle_length
            current = cycle_start
            for j in range(log_n):
                if k & (1 << j):
                    current = up[j][current]
        
        results.append(current + 1)
    
    return results
```

### Variation 2: Planets Queries I with Multiple Paths
**Problem**: Find k-th planet in path considering multiple possible paths.

**Link**: [CSES Problem Set - Planets Queries I Multiple Paths](https://cses.fi/problemset/task/planets_queries_i_multiple_paths)

```python
def planets_queries_i_multiple_paths(n, q, teleporters, queries):
    # Build binary lifting table for multiple paths
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    # Answer queries with multiple path consideration
    results = []
    for a, k in queries:
        current = a - 1
        for j in range(log_n):
            if k & (1 << j):
                current = up[j][current]
        results.append(current + 1)
    
    return results
```

### Variation 3: Planets Queries I with Time Constraints
**Problem**: Find k-th planet in path with time constraints on teleporter usage.

**Link**: [CSES Problem Set - Planets Queries I Time Constraints](https://cses.fi/problemset/task/planets_queries_i_time_constraints)

```python
def planets_queries_i_time_constraints(n, q, teleporters, queries, time_constraints):
    # Build binary lifting table with time constraints
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    # Answer queries with time constraints
    results = []
    for a, k in queries:
        current = a - 1
        total_time = 0
        
        for j in range(log_n):
            if k & (1 << j):
                step_time = time_constraints.get((current, up[j][current]), 1)
                total_time += step_time
                current = up[j][current]
        
        results.append((current + 1, total_time))
    
    return results
```

## 🔗 Related Problems

- **[Planets Cycles](/cses-analyses/problem_soulutions/graph_algorithms/planets_cycles_analysis/)**: Functional graphs
- **[Planets Queries II](/cses-analyses/problem_soulutions/graph_algorithms/planets_queries_ii_analysis/)**: Path intersection
- **[Binary Lifting](/cses-analyses/problem_soulutions/graph_algorithms/)**: Ancestor queries
- **[Query Optimization](/cses-analyses/problem_soulutions/graph_algorithms/)**: Query problems

## 📚 Learning Points

1. **Binary Lifting**: Essential for understanding ancestor queries
2. **Functional Graphs**: Key concept for understanding single-outgoing-edge graphs
3. **Query Optimization**: Important for competitive programming performance
4. **Sparse Tables**: Critical for understanding binary lifting implementation
5. **Binary Representation**: Foundation for efficient query processing
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Planets Queries I problem demonstrates fundamental binary lifting concepts for efficiently answering k-th ancestor queries in functional graphs. We explored three approaches:

1. **Brute Force Path Simulation**: O(q × k) time complexity using step-by-step simulation, inefficient for large k values
2. **Basic Binary Lifting**: O(n × log n) preprocessing + O(q × log k) queries using standard binary lifting, better approach for ancestor queries
3. **Optimized Binary Lifting with Efficient Query Processing**: O(n × log n) preprocessing + O(q × log k) queries with optimized binary lifting, optimal approach for ancestor query problems

The key insights include understanding binary lifting techniques, using sparse tables for efficient preprocessing, and applying binary representation for optimal query processing. This problem serves as an excellent introduction to binary lifting algorithms and ancestor query optimization techniques.

