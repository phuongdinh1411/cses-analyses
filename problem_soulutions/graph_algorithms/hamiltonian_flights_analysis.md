---
layout: simple
title: "Hamiltonian Flights - Path Counting with Bitmask DP"
permalink: /problem_soulutions/graph_algorithms/hamiltonian_flights_analysis
---

# Hamiltonian Flights - Path Counting with Bitmask DP

## 📋 Problem Description

Given a directed graph with n cities and m flights, count the number of different Hamiltonian paths from city 1 to city n.

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

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count all Hamiltonian paths from start to end city
- **Key Insight**: Use bitmask DP to represent visited cities efficiently
- **Challenge**: Handle exponential state space and modular arithmetic

### Step 2: Brute Force Approach
**Try all possible paths and count Hamiltonian ones:**

```python
def hamiltonian_flights_naive(n, m, flights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    # dp[mask][last] = number of paths ending at 'last' with visited cities in 'mask'
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1 << 0][1] = 1  # 1 << 0 = 1, represents city 1 visited
    
    # Iterate through all possible subsets of cities
    for mask in range(1 << n):
        for last in range(1, n + 1):
            # If 'last' city is not in the current mask, skip
            if not (mask & (1 << (last - 1))):
                continue
            
            # If there are paths ending at 'last' with current mask
            if dp[mask][last] > 0:
                # Try to extend path from 'last' to 'next_city'
                for next_city in adj[last]:
                    # If 'next_city' is not yet visited in the current mask
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % (10**9 + 7)
    
    # The answer is the number of paths ending at city n with all cities visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n]
```

**Complexity**: O(n × 2ⁿ) - exponential growth with n, optimal for this problem

### Step 3: Optimization
**Use optimized dynamic programming with better bitmask handling:**

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
```

**Why this improvement works**: We use optimized dynamic programming with bitmask to count Hamiltonian paths efficiently.

## Final Optimal Solution

```python
n, m = map(int, input().split())
flights = []
for _ in range(m):
    a, b = map(int, input().split())
    flights.append((a, b))

def count_hamiltonian_flights(n, m, flights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1][1] = 1
    
    # Iterate through all possible subsets of cities
    for mask in range(1 << n):
        for last in range(1, n + 1):
            # If 'last' city is not in the current mask, skip
            if not (mask & (1 << (last - 1))):
                continue
            
            # If there are paths ending at 'last' with current mask
            if dp[mask][last] > 0:
                # Try to extend path from 'last' to 'next_city'
                for next_city in adj[last]:
                    # If 'next_city' is not yet visited in the current mask
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    # The answer is the number of paths ending at city n with all cities visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n]

result = count_hamiltonian_flights(n, m, flights)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Bitmask DP | O(n * 2^n) | O(n * 2^n) | Use dynamic programming with bitmask |
| Optimized Bitmask DP | O(n * 2^n) | O(n * 2^n) | Optimized bitmask implementation |

## 🎨 Visual Example

### Input Example
```
4 cities, 4 flights:
Flight 1→2
Flight 2→3
Flight 3→4
Flight 1→4
```

### Graph Visualization
```
Cities with flights:
1 ──→ 2 ──→ 3 ──→ 4
│              ↗
└──────────────┘

All possible Hamiltonian paths from 1 to 4:
- Path 1: 1 → 2 → 3 → 4
- Path 2: 1 → 4 → 2 → 3 (invalid - 4→2 doesn't exist)
- Path 3: 1 → 4 → 3 → 2 (invalid - 4→3 doesn't exist)

Valid Hamiltonian paths: 1
```

### Bitmask Representation
```
Cities: 1, 2, 3, 4
Bitmask: 4 bits representing visited cities

Bit positions:
- Bit 0: City 1
- Bit 1: City 2
- Bit 2: City 3
- Bit 3: City 4

Examples:
- 0001: Only city 1 visited
- 0011: Cities 1 and 2 visited
- 1111: All cities visited
```

### Dynamic Programming Process
```
DP state: dp[mask][last_city] = number of paths

Step 1: Initialize
- dp[0001][1] = 1 (start at city 1)
- All other states = 0

Step 2: Process mask 0001
- From city 1, can go to cities 2 and 4
- dp[0011][2] += dp[0001][1] = 1
- dp[1001][4] += dp[0001][1] = 1

Step 3: Process mask 0011
- From city 2, can go to city 3
- dp[0111][3] += dp[0011][2] = 1

Step 4: Process mask 0111
- From city 3, can go to city 4
- dp[1111][4] += dp[0111][3] = 1

Step 5: Process mask 1001
- From city 4, no valid moves (no outgoing edges)

Final result: dp[1111][4] = 1
```

### Path Reconstruction
```
To find the actual path:
- Start from state (1111, 4)
- Check predecessors: city 3
- Move to state (0111, 3)
- Check predecessors: city 2
- Move to state (0011, 2)
- Check predecessors: city 1
- Move to state (0001, 1)
- No predecessors

Path: 1 → 2 → 3 → 4
```

### Bitmask Operations
```
Key bitmask operations:

1. Check if city i is visited:
   mask & (1 << (i-1))

2. Mark city i as visited:
   mask | (1 << (i-1))

3. Check if all cities visited:
   mask == (1 << n) - 1

4. Count visited cities:
   bin(mask).count('1')

Example with mask 0111:
- City 1: 0111 & 0001 = 0001 ✓ (visited)
- City 2: 0111 & 0010 = 0010 ✓ (visited)
- City 3: 0111 & 0100 = 0100 ✓ (visited)
- City 4: 0111 & 1000 = 0000 ✗ (not visited)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bitmask DP      │ O(n * 2^n)   │ O(n * 2^n)   │ State        │
│                 │              │              │ compression  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DFS + Memo      │ O(n * 2^n)   │ O(n * 2^n)   │ Recursive    │
│                 │              │              │ with cache   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n!)        │ O(n)         │ Generate all │
│                 │              │              │ permutations │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## Key Insights for Other Problems

### 1. **Hamiltonian Path**
**Principle**: Use dynamic programming with bitmask to count Hamiltonian paths.
**Applicable to**: Hamiltonian path problems, path counting problems, graph problems

### 2. **Bitmask Dynamic Programming**
**Principle**: Use bitmask to represent visited states in dynamic programming.
**Applicable to**: State compression problems, path problems, optimization problems

### 3. **Path Counting**
**Principle**: Use dynamic programming to count different paths in graphs.
**Applicable to**: Path counting problems, graph problems, combinatorics problems

## Notable Techniques

### 1. **Bitmask DP for Hamiltonian Path**
```python
def hamiltonian_path_dp(n, adj):
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    dp[1][1] = 1  # Start at city 1
    
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] += dp[mask][last]
    
    return dp[(1 << n) - 1][n]
```

### 2. **Bitmask Operations**
```python
def bitmask_operations(n):
    # Set bit
    mask = 1 << (n - 1)
    
    # Check if bit is set
    is_set = (mask & (1 << (n - 1))) != 0
    
    # Toggle bit
    mask ^= (1 << (n - 1))
    
    # Count set bits
    count = bin(mask).count('1')
    
    return mask, is_set, count
```

### 3. **State Compression**
```python
def state_compression_dp(n, adj):
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    dp[1][1] = 1
    
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    return dp[(1 << n) - 1][n]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a Hamiltonian path counting problem
2. **Choose approach**: Use dynamic programming with bitmask
3. **Build graph**: Create adjacency list representation
4. **Initialize DP**: Set base case for starting city
5. **Iterate states**: Process all possible subsets of cities
6. **Count paths**: Use DP to count different Hamiltonian paths
7. **Return result**: Output count modulo 10^9 + 7

---

*This analysis shows how to efficiently count Hamiltonian paths using dynamic programming with bitmask.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Hamiltonian Flights with Costs**
**Problem**: Each flight has a cost, find minimum cost Hamiltonian path.
```python
def cost_based_hamiltonian_flights(n, flights, costs):
    # costs[(a, b)] = cost of flight from a to b
    
    # Build adjacency list with costs
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        cost = costs.get((a, b), 0)
        adj[a].append((b, cost))
    
    # Use bitmask DP with cost tracking
    dp = [[float('inf')] * (n + 1) for _ in range(1 << n)]
    dp[1][1] = 0  # Start at city 1 with cost 0
    
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] != float('inf'):
                for next_city, cost in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = min(dp[new_mask][next_city], 
                                                     dp[mask][last] + cost)
    
    return dp[(1 << n) - 1][n] if dp[(1 << n) - 1][n] != float('inf') else -1
```

#### **Variation 2: Hamiltonian Flights with Constraints**
**Problem**: Find Hamiltonian path with constraints on flight sequences.
```python
def constrained_hamiltonian_flights(n, flights, constraints):
    # constraints = {'forbidden_sequences': [(a, b, c), ...], 'required_sequences': [(a, b, c), ...]}
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    # Use bitmask DP with constraint checking
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    dp[1][1] = 1  # Start at city 1
    
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        # Check constraints
                        path_so_far = []
                        temp_mask = mask
                        temp_last = last
                        
                        # Reconstruct path to check constraints
                        while temp_mask != 1:
                            path_so_far.append(temp_last)
                            for prev in range(1, n + 1):
                                if (temp_mask & (1 << (prev - 1))) and prev in adj and temp_last in adj[prev]:
                                    temp_mask ^= (1 << (temp_last - 1))
                                    temp_last = prev
                                    break
                        path_so_far.append(1)
                        path_so_far = path_so_far[::-1]
                        
                        # Check forbidden sequences
                        valid = True
                        for forbidden in constraints.get('forbidden_sequences', []):
                            if len(path_so_far) >= 3:
                                for i in range(len(path_so_far) - 2):
                                    if (path_so_far[i], path_so_far[i+1], path_so_far[i+2]) == forbidden:
                                        valid = False
                                        break
                        
                        if valid:
                            new_mask = mask | (1 << (next_city - 1))
                            dp[new_mask][next_city] += dp[mask][last]
    
    return dp[(1 << n) - 1][n]
```

#### **Variation 3: Hamiltonian Flights with Probabilities**
**Problem**: Each flight has a success probability, find expected number of successful Hamiltonian paths.
```python
def probabilistic_hamiltonian_flights(n, flights, probabilities):
    # probabilities[(a, b)] = probability that flight from a to b succeeds
    
    # Build adjacency list with probabilities
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        prob = probabilities.get((a, b), 0.5)
        adj[a].append((b, prob))
    
    # Use bitmask DP with probability tracking
    dp = [[0.0] * (n + 1) for _ in range(1 << n)]
    dp[1][1] = 1.0  # Start at city 1 with probability 1
    
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city, prob in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] += dp[mask][last] * prob
    
    return dp[(1 << n) - 1][n]
```

#### **Variation 4: Hamiltonian Flights with Multiple Criteria**
**Problem**: Find Hamiltonian path optimizing multiple objectives (cost, time, reliability).
```python
def multi_criteria_hamiltonian_flights(n, flights, costs, times, reliabilities):
    # costs[(a, b)] = cost, times[(a, b)] = time, reliabilities[(a, b)] = reliability
    
    # Build adjacency list with multiple criteria
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        cost = costs.get((a, b), 0)
        time = times.get((a, b), 0)
        reliability = reliabilities.get((a, b), 1)
        adj[a].append((b, cost, time, reliability))
    
    # Normalize values
    max_cost = max(costs.values()) if costs else 1
    max_time = max(times.values()) if times else 1
    max_reliability = max(reliabilities.values()) if reliabilities else 1
    
    # Use bitmask DP with weighted scoring
    dp = [[(float('inf'), 0, 0)] * (n + 1) for _ in range(1 << n)]
    dp[1][1] = (0, 0, 1.0)  # (cost, time, reliability)
    
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last][0] != float('inf'):
                for next_city, cost, time, reliability in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        new_cost = dp[mask][last][0] + cost
                        new_time = dp[mask][last][1] + time
                        new_reliability = dp[mask][last][2] * reliability
                        
                        # Weighted score (lower is better)
                        current_score = (new_cost / max_cost + new_time / max_time - new_reliability / max_reliability)
                        existing_score = (dp[new_mask][next_city][0] / max_cost + 
                                        dp[new_mask][next_city][1] / max_time - 
                                        dp[new_mask][next_city][2] / max_reliability)
                        
                        if current_score < existing_score:
                            dp[new_mask][next_city] = (new_cost, new_time, new_reliability)
    
    return dp[(1 << n) - 1][n]
```

#### **Variation 5: Hamiltonian Flights with Dynamic Updates**
**Problem**: Handle dynamic updates to flight network and find Hamiltonian paths after each update.
```python
def dynamic_hamiltonian_flights(n, initial_flights, updates):
    # updates = [(flight_to_add, flight_to_remove), ...]
    
    flights = initial_flights.copy()
    results = []
    
    for flight_to_add, flight_to_remove in updates:
        # Update flights
        if flight_to_remove in flights:
            flights.remove(flight_to_remove)
        if flight_to_add:
            flights.append(flight_to_add)
        
        # Rebuild adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b in flights:
            adj[a].append(b)
        
        # Use bitmask DP
        dp = [[0] * (n + 1) for _ in range(1 << n)]
        dp[1][1] = 1
        
        for mask in range(1 << n):
            for last in range(1, n + 1):
                if not (mask & (1 << (last - 1))):
                    continue
                
                if dp[mask][last] > 0:
                    for next_city in adj[last]:
                        if not (mask & (1 << (next_city - 1))):
                            new_mask = mask | (1 << (next_city - 1))
                            dp[new_mask][next_city] += dp[mask][last]
        
        results.append(dp[(1 << n) - 1][n])
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Hamiltonian Path Problems**
- **Hamiltonian Path**: Path visiting each vertex exactly once
- **Hamiltonian Cycle**: Cycle visiting each vertex exactly once
- **Traveling Salesman**: Find shortest Hamiltonian cycle
- **Path Enumeration**: Enumerate all Hamiltonian paths

#### **2. Dynamic Programming Problems**
- **State Compression**: Use bitmasks to represent states
- **Path Counting**: Count different paths in graphs
- **Optimization**: Find optimal paths with constraints
- **Multi-criteria**: Optimize multiple objectives

#### **3. Graph Theory Problems**
- **Path Problems**: Find paths with specific properties
- **Cycle Problems**: Find cycles with specific properties
- **Connectivity**: Study graph connectivity
- **Traversal**: Various graph traversal algorithms

#### **4. Combinatorial Problems**
- **Permutation Problems**: Problems involving permutations
- **Path Counting**: Count different types of paths
- **Enumeration**: Enumerate objects with properties
- **Optimization**: Optimize combinatorial structures

#### **5. Algorithmic Techniques**
- **Bitmask DP**: Dynamic programming with state compression
- **Graph Algorithms**: Various graph algorithms
- **Path Finding**: Find paths with specific properties
- **State Space Search**: Search through state space

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Networks**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    flights = []
    for _ in range(m):
        a, b = map(int, input().split())
        flights.append((a, b))
    
    result = count_hamiltonian_flights(n, m, flights)
    print(result)
```

#### **2. Range Queries on Hamiltonian Flights**
```python
def range_hamiltonian_flights_queries(n, flights, queries):
    # queries = [(start_flight, end_flight), ...] - find paths using flights in range
    
    results = []
    for start, end in queries: subset_flights = flights[
start: end+1]
        result = count_hamiltonian_flights(n, len(subset_flights), subset_flights)
        results.append(result)
    
    return results
```

#### **3. Interactive Hamiltonian Flights Problems**
```python
def interactive_hamiltonian_flights():
    n, m = map(int, input("Enter n and m: ").split())
    print("Enter flights (a b):")
    flights = []
    for _ in range(m):
        a, b = map(int, input().split())
        flights.append((a, b))
    
    result = count_hamiltonian_flights(n, m, flights)
    print(f"Number of Hamiltonian paths: {result}")
    
    # Show some paths
    paths = find_hamiltonian_paths(n, flights)
    print(f"Sample paths: {paths[:3]}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Hamiltonian Graph Properties**: Properties of Hamiltonian graphs
- **Path Theory**: Mathematical theory of paths
- **Cycle Theory**: Theory of cycles in graphs
- **Connectivity Theory**: Theory of graph connectivity

#### **2. Combinatorics**
- **Path Counting**: Mathematical counting of paths
- **Permutation Theory**: Theory of permutations
- **Enumeration Theory**: Theory of enumeration
- **Optimization Theory**: Mathematical optimization

#### **3. Complexity Theory**
- **NP-Complete Problems**: Complexity of Hamiltonian problems
- **Approximation Algorithms**: Approximate solutions
- **Heuristic Methods**: Heuristic approaches
- **Exact Algorithms**: Exact solution methods

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Hamiltonian Algorithms**: Various Hamiltonian path algorithms
- **Dynamic Programming**: State compression, bitmask DP
- **Graph Algorithms**: Path finding, traversal algorithms
- **Combinatorial Algorithms**: Enumeration, counting algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Combinatorics**: Combinatorial mathematics
- **Complexity Theory**: Computational complexity
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **State Compression**: Efficient state representation
- **Bit Manipulation**: Efficient bit operations
- **Dynamic Programming**: Optimal substructure, overlapping subproblems
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient Hamiltonian path techniques and shows various extensions for flight path problems.*

---

## 🔗 Related Problems

- **[Hamiltonian Path](/cses-analyses/problem_soulutions/graph_algorithms/)**: Path visiting all vertices exactly once
- **[Bitmask DP](/cses-analyses/problem_soulutions/graph_algorithms/)**: State compression problems
- **[Path Counting](/cses-analyses/problem_soulutions/graph_algorithms/)**: Counting problems with constraints

## 📚 Learning Points

1. **Bitmask DP**: Essential for state compression problems
2. **Hamiltonian Path**: Important for path enumeration problems
3. **State Space Management**: Key technique for exponential problems
4. **Modular Arithmetic**: Critical for large number handling
5. **Graph Theory**: Foundation for many algorithmic problems

---

**This is a great introduction to Hamiltonian paths and bitmask dynamic programming!** 🎯 