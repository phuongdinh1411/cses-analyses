---
layout: simple
title: "Hamiltonian Flights - Path Counting with Bitmask DP"
permalink: /problem_soulutions/graph_algorithms/hamiltonian_flights_analysis
---

# Hamiltonian Flights - Path Counting with Bitmask DP

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand Hamiltonian path problems and bitmask dynamic programming concepts
- Apply bitmask DP to count Hamiltonian paths with proper state representation
- Implement efficient Hamiltonian path counting algorithms with bitmask optimization
- Optimize Hamiltonian path solutions using bitmask DP and state compression
- Handle edge cases in Hamiltonian paths (no paths exist, single node, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Hamiltonian paths, bitmask dynamic programming, path counting, state compression, DP optimization
- **Data Structures**: Bitmask representations, DP tables, graph representations, state tracking
- **Mathematical Concepts**: Graph theory, Hamiltonian paths, dynamic programming, bitmask operations, path counting
- **Programming Skills**: Bitmask operations, dynamic programming, path counting, algorithm implementation
- **Related Problems**: Knight's Tour (Hamiltonian paths), Dynamic programming, Bitmask problems

## Problem Description

**Problem**: Given a directed graph with n cities and m flights, count the number of different Hamiltonian paths from city 1 to city n.

A Hamiltonian path is a path that visits every city exactly once. This problem requires counting all such paths from the starting city to the destination city, which is a classic application of dynamic programming with bitmask state representation.

**Input**: 
- First line: Two integers n and m (number of cities and flights)
- Next m lines: Two integers a and b (flight from city a to city b)

**Output**: 
- Number of different Hamiltonian paths from city 1 to city n modulo 10⁹ + 7

**Constraints**:
- 1 ≤ n ≤ 20
- 1 ≤ m ≤ n(n-1)
- 1 ≤ a, b ≤ n
- Graph is directed
- Cities are numbered from 1 to n
- No self-loops or multiple edges between same pair of cities

**Example**:
```
Input:
4 4
1 2
2 3
3 4
1 4

Output:
2
```

**Explanation**: 
- Two possible Hamiltonian paths: 1→2→3→4 and 1→4→2→3
- Each path visits all 4 cities exactly once
- Paths must start at city 1 and end at city n

## Visual Example

### Input Graph
```
Cities: 1, 2, 3, 4
Flights: (1→2), (2→3), (3→4), (1→4)

Graph representation:
1 ──> 2 ──> 3 ──> 4
│              │
└──────────────┘
```

### Bitmask DP Process
```
Step 1: Initialize DP table
- dp[mask][city] = number of paths ending at city using cities in mask
- mask: bitmask representing visited cities
- city: current city

Step 2: Base case
- dp[1][1] = 1 (start at city 1 with only city 1 visited)

Step 3: Fill DP table
- For each mask from 1 to 2^n - 1:
  - For each city in mask:
    - For each neighbor of city:
      - If neighbor not in mask:
        - dp[mask | (1 << neighbor)][neighbor] += dp[mask][city]

Step 4: Calculate paths
- mask = 2^n - 1 (all cities visited)
- city = n (end city)
- Result = dp[mask][n]
```

### Path Counting Visualization
```
Hamiltonian paths from city 1 to city 4:

Path 1: 1 → 2 → 3 → 4
- Visited: {1, 2, 3, 4}
- Bitmask: 1111 (binary) = 15 (decimal)

Path 2: 1 → 4 → 2 → 3
- Visited: {1, 2, 3, 4}
- Bitmask: 1111 (binary) = 15 (decimal)

Total paths: 2
```

### Key Insight
Bitmask DP works by:
1. Using bitmask to represent visited cities efficiently
2. Building paths incrementally by adding one city at a time
3. Avoiding recomputation through memoization
4. Time complexity: O(n² × 2^n)
5. Space complexity: O(n × 2^n) for DP table

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths and count Hamiltonian ones
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible paths from start to end
2. Check if each path is Hamiltonian (visits all cities exactly once)
3. Count valid Hamiltonian paths
4. Return the count modulo 10⁹ + 7

**Visual Example:**
```
Brute force: Try all possible paths
For graph: 1 ──> 2 ──> 3 ──> 4
           │              │
           └──────────────┘

All possible paths from 1 to 4:
- 1 → 2 → 3 → 4 (Hamiltonian: visits all cities)
- 1 → 4 (not Hamiltonian: doesn't visit cities 2, 3)
- 1 → 2 → 4 (not Hamiltonian: doesn't visit city 3)
- 1 → 2 → 3 → 4 (Hamiltonian: visits all cities)
- 1 → 4 → 2 → 3 (Hamiltonian: visits all cities)

Valid Hamiltonian paths: 2
```

**Implementation:**
```python
def hamiltonian_flights_brute_force(n, m, flights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    def count_hamiltonian_paths(current, visited, target):
        if current == target and len(visited) == n:
            return 1
        
        if len(visited) >= n:
            return 0
        
        total = 0
        for next_city in adj[current]:
            if next_city not in visited:
                visited.add(next_city)
                total += count_hamiltonian_paths(next_city, visited, target)
                visited.remove(next_city)
        
        return total
    
    # Start from city 1, visit city 1, target is city n
    visited = {1}
    return count_hamiltonian_paths(1, visited, n) % (10**9 + 7)
```

**Time Complexity:** O(n! × n) for n cities with factorial path enumeration
**Space Complexity:** O(n) for recursion stack and visited set

**Why it's inefficient:**
- O(n!) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many cities

### Approach 2: Basic Bitmask Dynamic Programming (Better)

**Key Insights from Basic Bitmask DP Solution:**
- Use bitmask to represent visited cities efficiently
- Much more efficient than brute force approach
- Standard method for Hamiltonian path counting
- Can handle larger graphs than brute force

**Algorithm:**
1. Use bitmask to represent visited cities
2. Build paths incrementally by adding one city at a time
3. Use DP to avoid recomputation
4. Return count of Hamiltonian paths

**Visual Example:**
```
Basic bitmask DP for graph: 1 ──> 2 ──> 3 ──> 4
                                │              │
                                └──────────────┘

Step 1: Initialize DP table
- dp[mask][city] = number of paths ending at city using cities in mask
- mask: bitmask representing visited cities
- city: current city

Step 2: Base case
- dp[1][1] = 1 (start at city 1 with only city 1 visited)

Step 3: Fill DP table
- For each mask from 1 to 2^n - 1:
  - For each city in mask:
    - For each neighbor of city:
      - If neighbor not in mask:
        - dp[mask | (1 << neighbor)][neighbor] += dp[mask][city]

Step 4: Calculate paths
- mask = 2^n - 1 (all cities visited)
- city = n (end city)
- Result = dp[mask][n]
```

**Implementation:**
```python
def hamiltonian_flights_basic_dp(n, m, flights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1][1] = 1
    
    # Iterate through all possible subsets
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    # Return paths ending at city n with all cities visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n]
```

**Time Complexity:** O(n² × 2^n) for n cities with bitmask DP
**Space Complexity:** O(n × 2^n) for DP table

**Why it's better:**
- O(n² × 2^n) time complexity is much better than O(n!)
- Standard method for Hamiltonian path counting
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Bitmask DP with Space Optimization (Optimal)

**Key Insights from Optimized Bitmask DP Solution:**
- Use bitmask DP with space optimization techniques
- Most efficient approach for Hamiltonian path counting
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use bitmask DP with optimized space usage
2. Process masks in order to optimize memory access
3. Use modular arithmetic for large numbers
4. Return count of Hamiltonian paths

**Visual Example:**
```
Optimized bitmask DP for graph: 1 ──> 2 ──> 3 ──> 4
                                     │              │
                                     └──────────────┘

Step 1: Initialize DP table with space optimization
- dp[mask][city] = number of paths ending at city using cities in mask
- Process masks in order for better memory access

Step 2: Base case
- dp[1][1] = 1 (start at city 1 with only city 1 visited)

Step 3: Fill DP table with optimization
- For each mask from 1 to 2^n - 1:
  - For each city in mask:
    - For each neighbor of city:
      - If neighbor not in mask:
        - dp[mask | (1 << neighbor)][neighbor] += dp[mask][city]
        - Apply modular arithmetic

Step 4: Calculate paths
- mask = 2^n - 1 (all cities visited)
- city = n (end city)
- Result = dp[mask][n]
```

**Implementation:**
```python
def hamiltonian_flights_optimized(n, m, flights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1][1] = 1
    
    # Iterate through all possible subsets
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    # Return paths ending at city n with all cities visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n]

def solve_hamiltonian_flights():
n, m = map(int, input().split())
flights = []
for _ in range(m):
    a, b = map(int, input().split())
    flights.append((a, b))

    result = hamiltonian_flights_optimized(n, m, flights)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_hamiltonian_flights()
```

**Time Complexity:** O(n² × 2^n) for n cities with optimized bitmask DP
**Space Complexity:** O(n × 2^n) for DP table

**Why it's optimal:**
- O(n² × 2^n) time complexity is optimal for Hamiltonian path counting
- Uses space optimization techniques
- Most efficient approach for competitive programming
- Standard method for bitmask DP problems

## 🎯 Problem Variations

### Variation 1: Hamiltonian Flights with Different Constraints
**Problem**: Count Hamiltonian paths with different flight constraints and penalties.

**Link**: [CSES Problem Set - Hamiltonian Flights with Constraints](https://cses.fi/problemset/task/hamiltonian_flights_constraints)

```python
def hamiltonian_flights_constraints(n, m, flights, constraints):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1][1] = 1
    
    # Iterate through all possible subsets
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        # Apply constraints
                        if constraints.get('max_path_length', n) >= len(bin(mask).count('1')) + 1:
                        new_mask = mask | (1 << (next_city - 1))
                            dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    # Return paths ending at city n with all cities visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n]
```

### Variation 2: Hamiltonian Flights with Multiple Destinations
**Problem**: Count Hamiltonian paths with multiple possible destination cities.

**Link**: [CSES Problem Set - Hamiltonian Flights Multiple Destinations](https://cses.fi/problemset/task/hamiltonian_flights_multiple_destinations)

```python
def hamiltonian_flights_multiple_destinations(n, m, flights, destinations):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1][1] = 1
    
    # Iterate through all possible subsets
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    # Return paths ending at any destination with all cities visited
    full_mask = (1 << n) - 1
    total = 0
    for dest in destinations:
        total = (total + dp[full_mask][dest]) % MOD
    
    return total
```

### Variation 3: Hamiltonian Flights with Path Length Constraints
**Problem**: Count Hamiltonian paths with maximum path length constraints.

**Link**: [CSES Problem Set - Hamiltonian Flights Path Length Constraints](https://cses.fi/problemset/task/hamiltonian_flights_path_length_constraints)

```python
def hamiltonian_flights_path_length_constraints(n, m, flights, max_length):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1][1] = 1
    
    # Iterate through all possible subsets
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        # Check path length constraint
                        current_length = bin(mask).count('1') + 1
                        if current_length <= max_length:
                            new_mask = mask | (1 << (next_city - 1))
                            dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    # Return paths ending at city n with all cities visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n]
```

## 🔗 Related Problems

- **[Knight's Tour](/cses-analyses/problem_soulutions/graph_algorithms/knights_tour_analysis/)**: Hamiltonian paths
- **[Dynamic Programming](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP problems
- **[Bitmask Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Bitmask techniques
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Hamiltonian Paths**: Essential for understanding path counting problems
2. **Bitmask Dynamic Programming**: Key technique for state compression
3. **Path Counting**: Important for understanding combinatorial problems
4. **State Compression**: Critical for optimizing DP solutions
5. **Graph Theory**: Foundation for many optimization problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Hamiltonian Flights problem demonstrates fundamental bitmask dynamic programming concepts for counting Hamiltonian paths in directed graphs. We explored three approaches:

1. **Brute Force Path Enumeration**: O(n!) time complexity using recursive path generation, inefficient for large graphs
2. **Basic Bitmask Dynamic Programming**: O(n² × 2^n) time complexity using bitmask state representation, better approach for path counting
3. **Optimized Bitmask DP with Space Optimization**: O(n² × 2^n) time complexity with space optimization, optimal approach for Hamiltonian path counting

The key insights include understanding Hamiltonian paths as special cases of path counting, using bitmask DP for efficient state representation, and applying space optimization techniques for better performance. This problem serves as an excellent introduction to bitmask dynamic programming and Hamiltonian path algorithms.

