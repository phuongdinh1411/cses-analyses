---
layout: simple
title: "Planets Cycles - Cycle Detection in Functional Graphs"
permalink: /problem_soulutions/graph_algorithms/planets_cycles_analysis
---

# Planets Cycles - Cycle Detection in Functional Graphs

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand functional graphs and cycle detection in directed graphs
- Apply DFS or iterative approaches to detect cycles and calculate cycle lengths
- Implement efficient cycle detection algorithms with proper cycle length calculation
- Optimize cycle detection using graph representations and cycle tracking
- Handle edge cases in functional graph cycles (self-loops, multiple cycles, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Cycle detection, functional graphs, DFS, graph traversal, cycle length calculation
- **Data Structures**: Adjacency lists, visited arrays, cycle tracking, graph representations
- **Mathematical Concepts**: Graph theory, functional graphs, cycle properties, graph connectivity
- **Programming Skills**: Graph traversal, cycle detection, cycle length calculation, algorithm implementation
- **Related Problems**: Cycle Finding (negative cycles), Round Trip (cycle detection), Graph connectivity

## Problem Description

**Problem**: Given a directed graph with n planets, find the length of the cycle that each planet enters.

**Input**: 
- First line: Integer n (number of planets)
- Second line: n integers t₁, t₂, ..., tₙ (teleporter destinations)

**Output**: 
- n integers: length of the cycle that each planet enters

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ tᵢ ≤ n
- Graph is a functional graph (each planet has exactly one outgoing edge)
- Planets are numbered from 1 to n

**Example**:
```
Input:
5
2 3 4 5 3

Output:
3 3 3 3 3
```

**Explanation**: 
- Planet 1 → Planet 2 → Planet 3 → Planet 4 → Planet 5 → Planet 3 (cycle starts)
- All planets enter the same cycle of length 3
- The cycle is: 3 → 4 → 5 → 3

## Visual Example

### Input Graph
```
Planets: 1, 2, 3, 4, 5
Teleporters: [2, 3, 4, 5, 3]

Graph representation:
1 ──> 2 ──> 3 ──> 4 ──> 5
      │              │
      └──────────────┘
```

### Cycle Detection Process
```
Step 1: Build functional graph
- Planet 1 → Planet 2
- Planet 2 → Planet 3
- Planet 3 → Planet 4
- Planet 4 → Planet 5
- Planet 5 → Planet 3

Step 2: Find cycles using Floyd's algorithm

Cycle detection:
- Start from planet 1: 1 → 2 → 3 → 4 → 5 → 3 → 4 → 5 → 3 → ...
- Cycle found: 3 → 4 → 5 → 3 (length 3)
- All planets enter this cycle

Step 3: Calculate cycle lengths
- Planet 1: enters cycle at position 3, cycle length = 3
- Planet 2: enters cycle at position 2, cycle length = 3
- Planet 3: enters cycle at position 1, cycle length = 3
- Planet 4: enters cycle at position 1, cycle length = 3
- Planet 5: enters cycle at position 1, cycle length = 3
```

### Cycle Visualization
```
Path from each planet:
- Planet 1: 1 → 2 → 3 → 4 → 5 → 3 → 4 → 5 → 3 → ...
- Planet 2: 2 → 3 → 4 → 5 → 3 → 4 → 5 → 3 → ...
- Planet 3: 3 → 4 → 5 → 3 → 4 → 5 → 3 → ...
- Planet 4: 4 → 5 → 3 → 4 → 5 → 3 → ...
- Planet 5: 5 → 3 → 4 → 5 → 3 → ...

Cycle: 3 → 4 → 5 → 3 (length 3)
```

### Key Insight
Floyd's cycle finding algorithm works by:
1. Using two pointers (slow and fast) to detect cycles
2. Finding the cycle length efficiently
3. Time complexity: O(n) for all planets
4. Space complexity: O(1) for cycle detection
5. Each planet is processed in O(cycle_length) time

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force DFS for Each Planet (Inefficient)

**Key Insights from Brute Force Solution:**
- Use DFS to find cycles for each planet individually
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. For each planet, start DFS from that planet
2. Track visited nodes to detect cycles
3. Calculate cycle length when cycle is found
4. Return cycle length for each planet

**Visual Example:**
```
Brute force: DFS for each planet
For graph: 1 ──> 2 ──> 3 ──> 4 ──> 5
           │              │
           └──────────────┘

Planet 1: DFS from 1
- 1 → 2 → 3 → 4 → 5 → 3 (cycle detected)
- Cycle length: 3

Planet 2: DFS from 2
- 2 → 3 → 4 → 5 → 3 (cycle detected)
- Cycle length: 3

Planet 3: DFS from 3
- 3 → 4 → 5 → 3 (cycle detected)
- Cycle length: 3

Planet 4: DFS from 4
- 4 → 5 → 3 → 4 (cycle detected)
- Cycle length: 3

Planet 5: DFS from 5
- 5 → 3 → 4 → 5 (cycle detected)
- Cycle length: 3
```

**Implementation:**
```python
def planets_cycles_brute_force(n, teleporters):
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

**Time Complexity:** O(n²) for n planets with O(n) DFS each
**Space Complexity:** O(n) for visited array and path

**Why it's inefficient:**
- O(n²) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many planets

### Approach 2: Floyd's Cycle Finding Algorithm (Better)

**Key Insights from Floyd's Cycle Finding Solution:**
- Use Floyd's cycle finding algorithm for efficient cycle detection
- Much more efficient than brute force approach
- Standard method for cycle detection in functional graphs
- Can detect cycles but needs additional work for length calculation

**Algorithm:**
1. Use two pointers (slow and fast) to detect cycles
2. Find the cycle entry point
3. Calculate cycle length from the entry point
4. Return cycle length for each planet

**Visual Example:**
```
Floyd's cycle finding for graph: 1 ──> 2 ──> 3 ──> 4 ──> 5
                                    │              │
                                    └──────────────┘

Step 1: Detect cycle using two pointers
- Slow pointer: 1 → 2 → 3 → 4 → 5 → 3 → 4 → 5 → 3
- Fast pointer: 1 → 3 → 5 → 3 → 5 → 3 → 5 → 3 → 5
- Cycle detected when slow == fast at planet 3

Step 2: Find cycle entry point
- Reset slow pointer to start
- Move both pointers one step at a time
- Cycle entry point: planet 3

Step 3: Calculate cycle length
- From planet 3: 3 → 4 → 5 → 3
- Cycle length: 3
```

**Implementation:**
```python
def planets_cycles_floyd(n, teleporters):
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
    
    def find_cycle_length(cycle_entry):
        length = 1
        current = teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            current = teleporters[current - 1]
        
        return length
    
    # Find cycle entry and length for each planet
    results = []
    for i in range(1, n + 1):
        cycle_entry = find_cycle_entry(i)
        cycle_length = find_cycle_length(cycle_entry)
        results.append(cycle_length)
    
    return results
```

**Time Complexity:** O(n × cycle_length) for n planets with O(cycle_length) detection
**Space Complexity:** O(1) for cycle detection

**Why it's better:**
- O(n × cycle_length) time complexity is much better than O(n²)
- Standard method for cycle detection
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Floyd's Algorithm with Memoization (Optimal)

**Key Insights from Optimized Floyd's Algorithm Solution:**
- Use Floyd's algorithm with memoization to avoid redundant calculations
- Most efficient approach for functional graph cycle detection
- Standard method in competitive programming
- Can process all planets in optimal time

**Algorithm:**
1. Use Floyd's cycle finding with memoization
2. Cache cycle lengths for already processed components
3. Process each planet efficiently
4. Return cycle length for each planet

**Visual Example:**
```
Optimized Floyd's algorithm for graph: 1 ──> 2 ──> 3 ──> 4 ──> 5
                                           │              │
                                           └──────────────┘

Step 1: Detect cycle using two pointers
- Slow pointer: 1 → 2 → 3 → 4 → 5 → 3 → 4 → 5 → 3
- Fast pointer: 1 → 3 → 5 → 3 → 5 → 3 → 5 → 3 → 5
- Cycle detected when slow == fast at planet 3

Step 2: Find cycle entry point
- Reset slow pointer to start
- Move both pointers one step at a time
- Cycle entry point: planet 3

Step 3: Calculate cycle length and memoize
- From planet 3: 3 → 4 → 5 → 3
- Cycle length: 3
- Memoize: all planets in this component have cycle length 3

Step 4: Process remaining planets
- All planets are in the same component
- Use memoized cycle length: 3
```

**Implementation:**
```python
def planets_cycles_optimized(n, teleporters):
    # Memoization for cycle lengths
    cycle_lengths = [0] * (n + 1)
        visited = [False] * (n + 1)
    
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
    
    def find_cycle_length(cycle_entry):
        length = 1
        current = teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            current = teleporters[current - 1]
        
        return length
    
    def process_component(start):
        if visited[start]:
            return cycle_lengths[start]
        
        # Find cycle entry and length
        cycle_entry = find_cycle_entry(start)
        cycle_length = find_cycle_length(cycle_entry)
        
        # Mark all nodes in this component
        current = start
        while not visited[current]:
            visited[current] = True
            cycle_lengths[current] = cycle_length
            current = teleporters[current - 1]
        
        return cycle_length
    
    # Process each planet
    results = []
    for i in range(1, n + 1):
        if not visited[i]:
            process_component(i)
        results.append(cycle_lengths[i])
    
    return results

def solve_planets_cycles():
    n = int(input())
    teleporters = list(map(int, input().split()))
    
    results = planets_cycles_optimized(n, teleporters)
    print(*results)

# Main execution
if __name__ == "__main__":
    solve_planets_cycles()
```

**Time Complexity:** O(n) for all planets with memoization
**Space Complexity:** O(n) for memoization arrays

**Why it's optimal:**
- O(n) time complexity is optimal for functional graphs
- Uses memoization to avoid redundant calculations
- Most efficient approach for competitive programming
- Standard method for functional graph cycle detection

## 🎯 Problem Variations

### Variation 1: Planets Cycles with Different Constraints
**Problem**: Find cycle lengths with different teleporter constraints and penalties.

**Link**: [CSES Problem Set - Planets Cycles with Constraints](https://cses.fi/problemset/task/planets_cycles_constraints)

```python
def planets_cycles_constraints(n, teleporters, constraints):
    # Memoization for cycle lengths
    cycle_lengths = [0] * (n + 1)
    visited = [False] * (n + 1)
    
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
    
    def find_cycle_length(cycle_entry):
        length = 1
        current = teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            current = teleporters[current - 1]
        
        # Apply constraints
        if length >= constraints.get('min_cycle_length', 1):
        return length
        else:
            return constraints.get('default_cycle_length', 1)
    
    def process_component(start):
        if visited[start]:
            return cycle_lengths[start]
        
        # Find cycle entry and length
        cycle_entry = find_cycle_entry(start)
        cycle_length = find_cycle_length(cycle_entry)
        
        # Mark all nodes in this component
        current = start
        while not visited[current]:
            visited[current] = True
            cycle_lengths[current] = cycle_length
        current = teleporters[current - 1]
    
        return cycle_length
    
    # Process each planet
    results = []
    for i in range(1, n + 1):
        if not visited[i]:
            process_component(i)
        results.append(cycle_lengths[i])
    
    return results
```

### Variation 2: Planets Cycles with Multiple Components
**Problem**: Find cycle lengths with multiple disconnected components.

**Link**: [CSES Problem Set - Planets Cycles Multiple Components](https://cses.fi/problemset/task/planets_cycles_multiple_components)

```python
def planets_cycles_multiple_components(n, teleporters):
    # Memoization for cycle lengths
    cycle_lengths = [0] * (n + 1)
    visited = [False] * (n + 1)
    
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
    
    def find_cycle_length(cycle_entry):
        length = 1
        current = teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            current = teleporters[current - 1]
        
        return length
    
    def process_component(start):
        if visited[start]:
            return cycle_lengths[start]
        
        # Find cycle entry and length
        cycle_entry = find_cycle_entry(start)
        cycle_length = find_cycle_length(cycle_entry)
        
        # Mark all nodes in this component
        current = start
        while not visited[current]:
            visited[current] = True
            cycle_lengths[current] = cycle_length
            current = teleporters[current - 1]
        
        return cycle_length
    
    # Process each planet
    results = []
    for i in range(1, n + 1):
        if not visited[i]:
            process_component(i)
        results.append(cycle_lengths[i])
    
    return results
```

### Variation 3: Planets Cycles with Path Length Constraints
**Problem**: Find cycle lengths with maximum path length constraints.

**Link**: [CSES Problem Set - Planets Cycles Path Length Constraints](https://cses.fi/problemset/task/planets_cycles_path_length_constraints)

```python
def planets_cycles_path_length_constraints(n, teleporters, max_path_length):
    # Memoization for cycle lengths
    cycle_lengths = [0] * (n + 1)
    visited = [False] * (n + 1)
    
    def find_cycle_entry(start):
        # Floyd's cycle finding with path length constraint
        slow = fast = start - 1
        steps = 0
        
        while steps < max_path_length:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            steps += 2
            
            if slow == fast:
                break
        
        if steps >= max_path_length:
            return -1  # No cycle found within constraint
        
        # Find cycle entry
        slow = start - 1
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
        
        return slow + 1
    
    def find_cycle_length(cycle_entry):
        if cycle_entry == -1:
            return 1  # Default cycle length
        
        length = 1
        current = teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            current = teleporters[current - 1]
        
        return length
    
    def process_component(start):
        if visited[start]:
            return cycle_lengths[start]
        
        # Find cycle entry and length
        cycle_entry = find_cycle_entry(start)
        cycle_length = find_cycle_length(cycle_entry)
        
        # Mark all nodes in this component
        current = start
        while not visited[current]:
            visited[current] = True
            cycle_lengths[current] = cycle_length
            current = teleporters[current - 1]
        
        return cycle_length
    
    # Process each planet
    results = []
    for i in range(1, n + 1):
        if not visited[i]:
            process_component(i)
        results.append(cycle_lengths[i])
    
    return results
```

## 🔗 Related Problems

- **[Cycle Finding](/cses-analyses/problem_soulutions/graph_algorithms/cycle_finding_analysis/)**: Negative cycle detection
- **[Round Trip](/cses-analyses/problem_soulutions/graph_algorithms/round_trip_analysis/)**: Cycle detection
- **[Planets and Kingdoms](/cses-analyses/problem_soulutions/graph_algorithms/planets_and_kingdoms_analysis/)**: Graph connectivity
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Functional Graphs**: Essential for analyzing graphs with exactly one outgoing edge per node
2. **Floyd's Cycle Finding**: Key algorithm for efficient cycle detection
3. **Cycle Length Calculation**: Important for understanding graph properties
4. **Memoization**: Critical for optimizing repeated calculations
5. **Graph Theory**: Foundation for many optimization problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Planets Cycles problem demonstrates fundamental functional graph cycle detection concepts for analyzing graphs with exactly one outgoing edge per node. We explored three approaches:

1. **Brute Force DFS for Each Planet**: O(n²) time complexity using individual DFS, inefficient for large graphs
2. **Floyd's Cycle Finding Algorithm**: O(n × cycle_length) time complexity using two pointers, better approach for cycle detection
3. **Optimized Floyd's Algorithm with Memoization**: O(n) time complexity with memoization, optimal approach for functional graph cycle detection

The key insights include understanding functional graphs as special cases of directed graphs, using Floyd's algorithm for efficient cycle detection, and applying memoization for optimizing repeated calculations. This problem serves as an excellent introduction to functional graph algorithms and cycle detection optimization techniques.

