---
layout: simple
title: "Planets Cycles
permalink: /problem_soulutions/graph_algorithms/planets_cycles_analysis/"
---


# Planets Cycles

## Problem Statement
Given a directed graph with n planets, find the length of the cycle that each planet enters.

### Input
The first input line has an integer n: the number of planets.
The second line has n integers t1,t2,…,tn: for each planet, there is a teleporter from planet i to planet ti.

### Output
Print n integers: the length of the cycle that each planet enters.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ti ≤ n

### Example
```
Input:
5
2 3 4 5 3

Output:
3 3 3 3 3
```

## Solution Progression

### Approach 1: DFS with Cycle Detection - O(n²)
**Description**: Use DFS to find cycles for each planet.

```python
def planets_cycles_naive(n, teleporters):
    def find_cycle_length(start):
        visited = [False] * (n + 1)
        path = []
        current = start
        
        while not visited[current]:
            visited[current] = True
            path.append(current)
            current = teleporters[current - 1]
        
        # Find cycle length
        cycle_start = path.index(current)
        return len(path) - cycle_start
    
    results = []
    for i in range(1, n + 1):
        cycle_length = find_cycle_length(i)
        results.append(cycle_length)
    
    return results
```

**Why this is inefficient**: We perform DFS for each planet, leading to quadratic complexity.

### Improvement 1: Union-Find with Cycle Detection - O(n)
**Description**: Use Union-Find to group planets in the same cycle.

```python
def planets_cycles_optimized(n, teleporters):"
    # Find cycle entry points using Floyd's cycle finding
    def find_cycle_entry(start):
        # Floyd's cycle finding
        slow = fast = start - 1
        while True:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            if slow == fast:
                break
        
        # Find cycle entry
        slow = start - 1
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
        
        return slow + 1
    
    # Find cycle length for a given cycle entry
    def find_cycle_length(cycle_entry):
        length = 1
        current = teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            current = teleporters[current - 1]
        
        return length
    
    # Precompute cycle entries and lengths
    cycle_entries = [find_cycle_entry(i) for i in range(1, n + 1)]
    cycle_lengths = {}
    
    for entry in set(cycle_entries):
        cycle_lengths[entry] = find_cycle_length(entry)
    
    # Answer for each planet
    results = []
    for i in range(1, n + 1):
        cycle_entry = cycle_entries[i - 1]
        results.append(cycle_lengths[cycle_entry])
    
    return results
```

**Why this improvement works**: We use Floyd's cycle finding to detect cycles and then compute cycle lengths efficiently.

## Final Optimal Solution

```python
n = int(input())
teleporters = list(map(int, input().split()))

def find_planet_cycles(n, teleporters):
    # Find cycle entry points using Floyd's cycle finding
    def find_cycle_entry(start):
        # Floyd's cycle finding
        slow = fast = start - 1
        while True:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            if slow == fast:
                break
        
        # Find cycle entry
        slow = start - 1
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
        
        return slow + 1
    
    # Find cycle length for a given cycle entry
    def find_cycle_length(cycle_entry):
        length = 1
        current = teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            current = teleporters[current - 1]
        
        return length
    
    # Precompute cycle entries and lengths
    cycle_entries = [find_cycle_entry(i) for i in range(1, n + 1)]
    cycle_lengths = {}
    
    for entry in set(cycle_entries):
        cycle_lengths[entry] = find_cycle_length(entry)
    
    # Answer for each planet
    results = []
    for i in range(1, n + 1):
        cycle_entry = cycle_entries[i - 1]
        results.append(cycle_lengths[cycle_entry])
    
    return results

result = find_planet_cycles(n, teleporters)
print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS with Cycle Detection | O(n²) | O(n) | Use DFS for each planet |
| Floyd's Cycle Finding | O(n) | O(n) | Use Floyd's algorithm to detect cycles |

## Key Insights for Other Problems

### 1. **Cycle Detection**
**Principle**: Use Floyd's cycle finding algorithm to detect cycles in directed graphs.
**Applicable to**: Cycle problems, graph problems, path problems

### 2. **Cycle Length Calculation**
**Principle**: Calculate cycle length by traversing from cycle entry point.
**Applicable to**: Cycle problems, length problems, graph problems

### 3. **Floyd's Cycle Finding**
**Principle**: Use two pointers (slow and fast) to detect cycles efficiently.
**Applicable to**: Cycle detection problems, linked list problems, graph problems

## Notable Techniques

### 1. **Floyd's Cycle Finding**
```python
def floyd_cycle_finding(teleporters, start):
    slow = fast = start - 1
    
    # Find meeting point
    while True:
        slow = teleporters[slow] - 1
        fast = teleporters[teleporters[fast] - 1] - 1
        if slow == fast:
            break
    
    # Find cycle entry
    slow = start - 1
    while slow != fast:
        slow = teleporters[slow] - 1
        fast = teleporters[fast] - 1
    
    return slow + 1
```

### 2. **Cycle Length Calculation**
```python
def calculate_cycle_length(teleporters, cycle_entry):
    length = 1
    current = teleporters[cycle_entry - 1]
    
    while current != cycle_entry:
        length += 1
        current = teleporters[current - 1]
    
    return length
```

### 3. **Cycle Entry Mapping**
```python
def map_cycle_entries(n, teleporters):
    cycle_entries = []
    
    for i in range(1, n + 1):
        entry = find_cycle_entry(teleporters, i)
        cycle_entries.append(entry)
    
    return cycle_entries
```

## Problem-Solving Framework

1. **Identify problem type**: This is a cycle length finding problem
2. **Choose approach**: Use Floyd's cycle finding to detect cycles
3. **Find cycle entries**: Precompute cycle entry points for all nodes
4. **Calculate cycle lengths**: Compute length for each unique cycle
5. **Map results**: Associate each planet with its cycle length
6. **Handle duplicates**: Use set to avoid recalculating same cycles
7. **Return results**: Output cycle length for each planet

---

*This analysis shows how to efficiently find cycle lengths using Floyd's cycle finding algorithm.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Planets Cycles with Costs**
**Problem**: Each teleporter has a cost, find cycle length with minimum total cost.
```python
def cost_based_planets_cycles(n, teleporters, costs):
    # costs[i] = cost of teleporter from planet i to teleporters[i]
    
    def find_cycle_with_cost(start):
        slow = fast = start - 1
        total_cost = 0
        
        # Find meeting point
        while True:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            total_cost += costs[slow] + costs[fast]
            if slow == fast:
                break
        
        # Find cycle entry
        slow = start - 1
        cycle_cost = 0
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
            cycle_cost += costs[slow] + costs[fast]
        
        return slow + 1, total_cost - cycle_cost
    
    results = []
    for i in range(1, n + 1):
        entry, cost = find_cycle_with_cost(i)
        results.append((entry, cost))
    
    return results
```

#### **Variation 2: Planets Cycles with Constraints**
**Problem**: Find cycle length with constraints on maximum teleporter usage.
```python
def constrained_planets_cycles(n, teleporters, max_teleporters):
    # max_teleporters = maximum number of teleporters that can be used
    
    def find_cycle_with_constraint(start):
        slow = fast = start - 1
        teleporter_count = 0
        
        # Find meeting point
        while teleporter_count < max_teleporters:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            teleporter_count += 2
            if slow == fast:
                break
        
        if teleporter_count >= max_teleporters:
            return None  # Constraint violated
        
        # Find cycle entry
        slow = start - 1
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
        
        return slow + 1
    
    results = []
    for i in range(1, n + 1):
        entry = find_cycle_with_constraint(i)
        results.append(entry)
    
    return results
```

#### **Variation 3: Planets Cycles with Probabilities**
**Problem**: Each teleporter has a probability of working, find expected cycle length.
```python
def probabilistic_planets_cycles(n, teleporters, probabilities):
    # probabilities[i] = probability that teleporter from i works
    
    def find_expected_cycle_length(start):
        slow = fast = start - 1
        expected_length = 0
        prob_success = 1.0
        
        # Find meeting point
        while True:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            expected_length += 2
            prob_success *= probabilities[slow] * probabilities[fast]
            if slow == fast:
                break
        
        # Find cycle entry
        slow = start - 1
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
            expected_length += 2
            prob_success *= probabilities[slow] * probabilities[fast]
        
        return expected_length * prob_success
    
    results = []
    for i in range(1, n + 1):
        expected_length = find_expected_cycle_length(i)
        results.append(expected_length)
    
    return results
```

#### **Variation 4: Planets Cycles with Multiple Paths**
**Problem**: Each planet has multiple teleporters, find shortest cycle length.
```python
def multi_path_planets_cycles(n, teleporters_list):
    # teleporters_list[i] = list of possible destinations from planet i
    
    def find_shortest_cycle(start):
        from collections import deque
        
        # BFS to find shortest cycle
        queue = deque([(start, [start])])
        visited = set()
        
        while queue:
            current, path = queue.popleft()
            
            for next_planet in teleporters_list[current - 1]:
                if next_planet in path:
                    # Found cycle
                    cycle_start = path.index(next_planet)
                    return len(path) - cycle_start
                
                if next_planet not in visited:
                    visited.add(next_planet)
                    queue.append((next_planet, path + [next_planet]))
        
        return None  # No cycle found
    
    results = []
    for i in range(1, n + 1):
        cycle_length = find_shortest_cycle(i)
        results.append(cycle_length)
    
    return results
```

#### **Variation 5: Planets Cycles with Dynamic Updates**
**Problem**: Handle dynamic updates to teleporters and find cycle lengths after each update.
```python
def dynamic_planets_cycles(n, initial_teleporters, updates):
    # updates = [(planet, new_destination), ...]
    
    teleporters = initial_teleporters.copy()
    results = []
    
    for planet, new_destination in updates:
        # Update teleporter
        teleporters[planet - 1] = new_destination
        
        # Recompute all cycle lengths
        cycle_entries = [find_cycle_entry(teleporters, i) for i in range(1, n + 1)]
        cycle_lengths = {}
        
        for entry in set(cycle_entries):
            cycle_lengths[entry] = find_cycle_length(teleporters, entry)
        
        # Answer for each planet
        current_results = []
        for i in range(1, n + 1):
            cycle_entry = cycle_entries[i - 1]
            current_results.append(cycle_lengths[cycle_entry])
        
        results.append(current_results)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Cycle Detection Problems**
- **Floyd's Cycle Finding**: Two-pointer technique for cycle detection
- **DFS Cycle Detection**: Depth-first search for cycles
- **BFS Cycle Detection**: Breadth-first search for cycles
- **Union-Find Cycle Detection**: Using Union-Find data structure

#### **2. Graph Traversal Problems**
- **Connected Components**: Find connected components in graphs
- **Strongly Connected Components**: Find SCCs in directed graphs
- **Topological Sorting**: Find topological order in DAGs
- **Path Finding**: Find paths between nodes

#### **3. Functional Graph Problems**
- **Functional Graph Properties**: Properties of functional graphs
- **Cycle Analysis**: Analyze cycles in functional graphs
- **Tree Analysis**: Analyze trees in functional graphs
- **Component Analysis**: Analyze components in functional graphs

#### **4. Algorithmic Techniques**
- **Two-Pointer Technique**: Use two pointers for efficient algorithms
- **Graph Algorithms**: Various graph traversal algorithms
- **Dynamic Programming**: Handle dynamic updates
- **Optimization**: Optimize for different criteria

#### **5. Mathematical Concepts**
- **Cycle Theory**: Mathematical theory of cycles
- **Graph Theory**: Properties of graphs and cycles
- **Combinatorics**: Counting cycles and paths
- **Probability**: Probabilistic cycle analysis

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    teleporters = list(map(int, input().split()))
    
    result = find_planet_cycles(n, teleporters)
    print(*result)
```

#### **2. Range Queries on Cycle Lengths**
```python
def range_cycle_length_queries(n, teleporters, queries):
    # queries = [(start_planet, end_planet), ...] - find cycle lengths in range
    
    # Precompute all cycle lengths
    cycle_entries = [find_cycle_entry(teleporters, i) for i in range(1, n + 1)]
    cycle_lengths = {}
    
    for entry in set(cycle_entries):
        cycle_lengths[entry] = find_cycle_length(teleporters, entry)
    
    results = []
    for start, end in queries:
        range_results = []
        for i in range(start, end + 1):
            cycle_entry = cycle_entries[i - 1]
            range_results.append(cycle_lengths[cycle_entry])
        results.append(range_results)
    
    return results
```

#### **3. Interactive Cycle Detection Problems**
```python
def interactive_planets_cycles():
    n = int(input("Enter number of planets: "))
    print("Enter teleporters (space-separated):")
    teleporters = list(map(int, input().split()))
    
    result = find_planet_cycles(n, teleporters)
    print(f"Cycle lengths: {result}")
    
    # Show cycle details
    for i, length in enumerate(result, 1):
        print(f"Planet {i}: Cycle length = {length}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Cycle Properties**: Properties of cycles in graphs
- **Functional Graph Theory**: Theory of functional graphs
- **Cycle Enumeration**: Counting different types of cycles
- **Cycle Decomposition**: Decomposing graphs into cycles

#### **2. Number Theory**
- **Cycle Length Properties**: Properties of cycle lengths
- **Modular Arithmetic**: Using modular arithmetic for cycle analysis
- **Prime Factorization**: Analyzing cycle lengths in terms of primes
- **Number Sequences**: Analyzing sequences of cycle lengths

#### **3. Combinatorics**
- **Cycle Counting**: Counting cycles in graphs
- **Permutation Cycles**: Cycles in permutations
- **Cycle Patterns**: Patterns in cycle structures
- **Cycle Statistics**: Statistical properties of cycles

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Floyd's Cycle Finding**: Two-pointer cycle detection
- **DFS/BFS**: Graph traversal algorithms
- **Union-Find**: Connectivity data structure
- **Graph Algorithms**: Various graph algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Cycle Theory**: Mathematical theory of cycles
- **Functional Analysis**: Analysis of functional graphs
- **Combinatorics**: Counting and enumeration techniques

#### **3. Programming Concepts**
- **Two-Pointer Technique**: Efficient algorithm design
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Algorithm Optimization**: Improving time and space complexity
- **Dynamic Programming**: Handling dynamic updates

---

*This analysis demonstrates efficient cycle detection techniques and shows various extensions for planets cycles problems.* 