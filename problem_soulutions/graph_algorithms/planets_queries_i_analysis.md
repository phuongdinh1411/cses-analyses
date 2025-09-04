---
layout: simple
title: "Planets Queries I - Binary Lifting for Path Queries"
permalink: /problem_soulutions/graph_algorithms/planets_queries_i_analysis
---

# Planets Queries I - Binary Lifting for Path Queries

## 📋 Problem Description

Given a directed graph with n planets and q queries, for each query find the k-th planet in the path starting from planet a.

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

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find k-th planet in path from starting planet
- **Key Insight**: Use binary lifting for efficient ancestor queries
- **Challenge**: Handle very large k values efficiently

### Step 2: Brute Force Approach
**Simulate the path for each query:**

```python
def planets_queries_i_naive(n, q, teleporters, queries):
    results = []
    
    for a, k in queries:
        current = a
        for _ in range(k):
            current = teleporters[current - 1]
        results.append(current)
    
    return results
```

**Complexity**: O(q × k) - too slow for large k values

### Step 3: Optimization
**Use binary lifting to precompute ancestors:**

```python
def planets_queries_i_optimized(n, q, teleporters, queries):
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
```

**Key Insight**: Precompute 2^j-th ancestors for O(log k) query time

### Step 4: Complete Solution

```python
n, q = map(int, input().split())
teleporters = list(map(int, input().split()))

def answer_planets_queries(n, q, teleporters, queries):
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

# Read queries
queries = []
for _ in range(q):
    a, k = map(int, input().split())
    queries.append((a, k))

result = answer_planets_queries(n, q, teleporters, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Simulation | O(q * k) | O(1) | Simulate path for each query |
| Binary Lifting | O(n log n + q log k) | O(n log n) | Precompute ancestors for efficient queries |

## Implementation Details

### 1. **Binary Lifting Table Construction**
- **Table Structure**: 2D array where `up[j][i]` represents the 2^j-th ancestor of node i
- **Initialization**: First row contains direct teleporter destinations
- **Recursive Building**: Each row is built using the previous row: `up[j][i] = up[j-1][up[j-1][i]]`
- **Logarithmic Height**: Table height is log₂(n) for efficient queries

### 2. **Query Processing**
- **Binary Decomposition**: Decompose k into powers of 2 using bit manipulation
- **Ancestor Traversal**: Use the lifting table to jump 2^j steps at a time
- **Efficient Lookup**: Each query takes O(log k) time regardless of k's magnitude

### 3. **Memory Management**
- **Space Optimization**: Use 0-indexed arrays internally, convert to 1-indexed for output
- **Table Size**: O(n log n) space for the lifting table
- **Query Storage**: O(q) space for storing query results

## Key Insights

### 1. **Binary Lifting Strategy**
- **Power of 2 Decomposition**: Break down large jumps into powers of 2 for efficient traversal
- **Precomputation**: Build lookup tables to answer queries in logarithmic time
- **Recursive Structure**: Each level of the table builds upon the previous level
- **Query Efficiency**: Transform O(k) path simulation into O(log k) table lookups

### 2. **Functional Graph Properties**
- **Single Outgoing Edge**: Each planet has exactly one teleporter destination
- **Path Structure**: Paths eventually lead to cycles or fixed points
- **Cycle Detection**: Binary lifting can detect cycles by checking if 2^j-th ancestor exists
- **Efficient Simulation**: Avoid actual path traversal for large k values

### 3. **Query Optimization**
- **Bit Manipulation**: Use bitwise operations to decompose k into powers of 2
- **Table Lookup**: Access precomputed ancestors for O(1) lookup time
- **Memory Trade-off**: Use O(n log n) space to achieve O(log k) query time
- **Scalability**: Handle queries with k up to 10^9 efficiently

## Key Insights for Other Problems

### 1. **Binary Lifting**
**Principle**: Precompute 2^j-th ancestors to answer queries efficiently.
**Applicable to**: Tree problems, ancestor queries, path problems

### 2. **Ancestor Queries**
**Principle**: Use binary lifting to find k-th ancestor in logarithmic time.
**Applicable to**: Tree problems, ancestor problems, query problems

### 3. **Path Simulation**
**Principle**: Use precomputed data structures to simulate paths efficiently.
**Applicable to**: Path problems, simulation problems, query problems

## Notable Techniques

### 1. **Binary Lifting Implementation**
```python
def build_binary_lifting(n, teleporters):
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    return up
```

### 2. **Query Answering**
```python
def answer_query(up, start, k):
    current = start - 1
    for j in range(20):
        if k & (1 << j):
            current = up[j][current]
    return current + 1
```

### 3. **Binary Lifting Table**
```python
def build_lifting_table(n, teleporters):
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    return up
```

## Problem-Solving Framework

1. **Identify problem type**: This is a binary lifting problem for ancestor queries
2. **Choose approach**: Use binary lifting to precompute ancestors
3. **Build lifting table**: Create 2^j-th ancestor table
4. **Initialize table**: Set up first row with direct teleporters
5. **Fill table**: Use recurrence to fill remaining rows
6. **Answer queries**: Use binary representation of k to find k-th ancestor
7. **Return results**: Output answers for all queries

## Related Problems

### **1. Tree and Ancestor Problems**
- **Lowest Common Ancestor (LCA)**: Find common ancestor of two nodes
- **K-th Ancestor**: Find k-th ancestor of a node in a tree
- **Tree Path Queries**: Answer queries about paths in trees

### **2. Graph Traversal Problems**
- **Shortest Path**: Find shortest path between nodes
- **Cycle Detection**: Detect cycles in directed graphs
- **Functional Graphs**: Handle graphs with single outgoing edges per node

### **3. Query Processing Problems**
- **Range Queries**: Answer queries over ranges of data
- **Binary Lifting**: Use power-of-2 decomposition for efficient queries
- **Sparse Tables**: Precompute data for fast range queries

## Learning Points

### **1. Algorithm Design**
- **Binary Lifting**: Essential technique for efficient ancestor queries
- **Precomputation**: Trade space for time to achieve logarithmic query complexity
- **Bit Manipulation**: Use binary representation to decompose large values

### **2. Implementation Techniques**
- **Table Construction**: Build lookup tables incrementally
- **Query Processing**: Efficiently answer queries using precomputed data
- **Memory Management**: Balance space usage with query efficiency

### **3. Problem-Solving Strategies**
- **Functional Graph Analysis**: Understand properties of graphs with single outgoing edges
- **Query Optimization**: Transform linear-time operations into logarithmic-time queries
- **Scalability**: Handle very large input values efficiently

---

*This analysis shows how to efficiently answer ancestor queries using binary lifting technique.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Planets Queries I with Costs**
**Problem**: Each teleporter has a cost, find total cost to reach k-th ancestor.
```python
def cost_based_planets_queries_i(n, q, teleporters, costs, queries):
    # costs[i] = cost of teleporter from planet i to teleporters[i]
    
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    cost_up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
        cost_up[0][i] = costs[i]
    
    # Build binary lifting table with costs
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
            cost_up[j][i] = cost_up[j-1][i] + cost_up[j-1][up[j-1][i]]
    
    results = []
    for a, k in queries:
        current = a - 1
        total_cost = 0
        for j in range(log_n):
            if k & (1 << j):
                total_cost += cost_up[j][current]
                current = up[j][current]
        results.append((current + 1, total_cost))
    
    return results
```

#### **Variation 2: Planets Queries I with Constraints**
**Problem**: Find k-th ancestor with constraints on maximum teleporter usage.
```python
def constrained_planets_queries_i(n, q, teleporters, max_teleporters, queries):
    # max_teleporters = maximum number of teleporters that can be used
    
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    results = []
    for a, k in queries: if k > 
max_teleporters: results.append(-1)  # Constraint violated
            continue
        
        current = a - 1
        for j in range(log_n):
            if k & (1 << j):
                current = up[j][current]
        results.append(current + 1)
    
    return results
```

#### **Variation 3: Planets Queries I with Probabilities**
**Problem**: Each teleporter has a probability of working, find expected k-th ancestor.
```python
def probabilistic_planets_queries_i(n, q, teleporters, probabilities, queries):
    # probabilities[i] = probability that teleporter from i works
    
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    prob_up = [[1.0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
        prob_up[0][i] = probabilities[i]
    
    # Build binary lifting table with probabilities
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
            prob_up[j][i] = prob_up[j-1][i] * prob_up[j-1][up[j-1][i]]
    
    results = []
    for a, k in queries:
        current = a - 1
        expected_prob = 1.0
        for j in range(log_n):
            if k & (1 << j):
                expected_prob *= prob_up[j][current]
                current = up[j][current]
        results.append((current + 1, expected_prob))
    
    return results
```

#### **Variation 4: Planets Queries I with Multiple Paths**
**Problem**: Each planet has multiple teleporters, find k-th ancestor using shortest path.
```python
def multi_path_planets_queries_i(n, q, teleporters_list, queries):
    # teleporters_list[i] = list of possible destinations from planet i
    
    def find_kth_ancestor(start, k):
        from collections import deque
        
        # BFS to find k-th ancestor
        queue = deque([(start, 0)])
        visited = {start}
        
        while queue:
            current, steps = queue.popleft()
            
            if steps == k:
                return current
            
            for next_planet in teleporters_list[current - 1]:
                if next_planet not in visited:
                    visited.add(next_planet)
                    queue.append((next_planet, steps + 1))
        
        return -1  # No k-th ancestor found
    
    results = []
    for a, k in queries:
        ancestor = find_kth_ancestor(a, k)
        results.append(ancestor)
    
    return results
```

#### **Variation 5: Planets Queries I with Dynamic Updates**
**Problem**: Handle dynamic updates to teleporters and answer queries after each update.
```python
def dynamic_planets_queries_i(n, q, initial_teleporters, updates, queries):
    # updates = [(planet, new_destination), ...]
    
    teleporters = initial_teleporters.copy()
    results = []
    
    for planet, new_destination in updates:
        # Update teleporter
        teleporters[planet - 1] = new_destination
        
        # Rebuild binary lifting table
        log_n = 20
        up = [[0] * n for _ in range(log_n)]
        
        for i in range(n):
            up[0][i] = teleporters[i] - 1
        
        for j in range(1, log_n):
            for i in range(n):
                up[j][i] = up[j-1][up[j-1][i]]
        
        # Answer current queries
        current_results = []
        for a, k in queries:
            current = a - 1
            for j in range(log_n):
                if k & (1 << j):
                    current = up[j][current]
            current_results.append(current + 1)
        
        results.append(current_results)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Tree Problems**
- **Binary Lifting**: Precompute ancestors for efficient queries
- **Lowest Common Ancestor**: Find LCA of two nodes
- **Tree Traversal**: Various tree traversal algorithms
- **Tree Queries**: Answer queries on tree structures

#### **2. Graph Traversal Problems**
- **BFS/DFS**: Graph traversal algorithms
- **Shortest Path**: Find shortest paths in graphs
- **Path Queries**: Answer queries about paths
- **Reachability**: Check if nodes are reachable

#### **3. Query Problems**
- **Range Queries**: Answer queries on ranges
- **Point Queries**: Answer queries on specific points
- **Dynamic Queries**: Handle dynamic updates
- **Batch Queries**: Process multiple queries efficiently

#### **4. Algorithmic Techniques**
- **Binary Lifting**: Efficient ancestor queries
- **Sparse Tables**: Precompute data for range queries
- **Dynamic Programming**: Handle dynamic updates
- **Optimization**: Optimize for different criteria

#### **5. Mathematical Concepts**
- **Tree Theory**: Properties of trees
- **Graph Theory**: Properties of graphs
- **Combinatorics**: Counting paths and ancestors
- **Probability**: Probabilistic path analysis

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Trees**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    teleporters = list(map(int, input().split()))
    queries = []
    for _ in range(q):
        a, k = map(int, input().split())
        queries.append((a, k))
    
    result = answer_planets_queries(n, q, teleporters, queries)
    for res in result:
        print(res)
```

#### **2. Range Queries on Ancestors**
```python
def range_ancestor_queries(n, teleporters, queries):
    # queries = [(start_planet, end_planet, k), ...] - find k-th ancestors in range
    
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    results = []
    for start, end, k in queries:
        range_results = []
        for planet in range(start, end + 1):
            current = planet - 1
            for j in range(log_n):
                if k & (1 << j):
                    current = up[j][current]
            range_results.append(current + 1)
        results.append(range_results)
    
    return results
```

#### **3. Interactive Ancestor Query Problems**
```python
def interactive_planets_queries_i():
    n = int(input("Enter number of planets: "))
    print("Enter teleporters (space-separated):")
    teleporters = list(map(int, input().split()))
    
    q = int(input("Enter number of queries: "))
    print("Enter queries (planet k):")
    queries = []
    for _ in range(q):
        a, k = map(int, input().split())
        queries.append((a, k))
    
    result = answer_planets_queries(n, q, teleporters, queries)
    print(f"Results: {result}")
    
    # Show query details
    for i, (a, k) in enumerate(queries):
        print(f"Query {i+1}: Planet {a}, {k}-th ancestor = {result[i]}")
```

### 🧮 **Mathematical Extensions**

#### **1. Tree Theory**
- **Tree Properties**: Properties of trees and ancestors
- **Binary Lifting Theory**: Mathematical theory of binary lifting
- **Ancestor Analysis**: Analysis of ancestor relationships
- **Tree Decomposition**: Decomposing trees into components

#### **2. Graph Theory**
- **Functional Graph Properties**: Properties of functional graphs
- **Path Analysis**: Analysis of paths in graphs
- **Cycle Analysis**: Analysis of cycles in graphs
- **Component Analysis**: Analysis of graph components

#### **3. Number Theory**
- **Binary Representation**: Using binary representation for queries
- **Modular Arithmetic**: Using modular arithmetic for large queries
- **Number Sequences**: Analyzing sequences of ancestors
- **Pattern Recognition**: Recognizing patterns in ancestor sequences

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Binary Lifting**: Efficient ancestor queries
- **Sparse Tables**: Range query data structures
- **Tree Algorithms**: Various tree algorithms
- **Graph Algorithms**: Graph traversal and query algorithms

#### **2. Mathematical Concepts**
- **Tree Theory**: Properties and theorems about trees
- **Graph Theory**: Properties and theorems about graphs
- **Binary Analysis**: Analysis of binary representations
- **Combinatorics**: Counting and enumeration techniques

#### **3. Programming Concepts**
- **Data Structures**: Efficient data structures for queries
- **Algorithm Optimization**: Improving time and space complexity
- **Dynamic Programming**: Handling dynamic updates
- **Query Processing**: Efficient query processing techniques

---

*This analysis demonstrates efficient ancestor query techniques and shows various extensions for planets queries problems.* 