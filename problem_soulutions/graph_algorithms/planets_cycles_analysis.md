---
layout: simple
title: "Planets Cycles - Cycle Detection in Functional Graphs"
permalink: /problem_soulutions/graph_algorithms/planets_cycles_analysis
---

# Planets Cycles - Cycle Detection in Functional Graphs

## 📋 Problem Description

Given a directed graph with n planets, find the length of the cycle that each planet enters.

**Input**: 
- First line: Integer n (number of planets)
- Second line: n integers t₁, t₂, ..., tₙ (teleporter destinations)

**Output**: 
- n integers: length of the cycle that each planet enters

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ tᵢ ≤ n

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

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find cycle length for each planet in a functional graph
- **Key Insight**: Use Floyd's cycle finding algorithm for efficient detection
- **Challenge**: Avoid quadratic complexity when processing each planet individually

### Step 2: Brute Force Approach
**Use DFS to find cycles for each planet:**

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

**Complexity**: O(n²) - too slow for large graphs

### Step 3: Optimization
**Use Floyd's cycle finding algorithm for efficient cycle detection:**

```python
def planets_cycles_optimized(n, teleporters):
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
    
    # Find cycle entry and length for each planet
    results = []
    for i in range(1, n + 1):
        cycle_entry = find_cycle_entry(i)
        cycle_length = find_cycle_length(cycle_entry)
        results.append(cycle_length)
    
    return results
```

**Key Insight**: Use Floyd's algorithm to find cycle entry points efficiently

### Step 4: Complete Solution

```python
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
    
    # Find cycle entry and length for each planet
    results = []
    for i in range(1, n + 1):
        cycle_entry = find_cycle_entry(i)
        cycle_length = find_cycle_length(cycle_entry)
        results.append(cycle_length)
    
    return results

def solve_planets_cycles():
    n = int(input())
    teleporters = list(map(int, input().split()))
    
    result = find_planet_cycles(n, teleporters)
    print(*result)

if __name__ == "__main__":
    solve_planets_cycles()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    # Test case 1: Simple cycle
    n1 = 5
    teleporters1 = [2, 3, 4, 5, 3]
    result1 = find_planet_cycles(n1, teleporters1)
    print(f"Test 1: {result1}")
    
    # Test case 2: Self-loop
    n2 = 3
    teleporters2 = [1, 2, 3]
    result2 = find_planet_cycles(n2, teleporters2)
    print(f"Test 2: {result2}")
    
    # Test case 3: Multiple cycles
    n3 = 6
    teleporters3 = [2, 1, 4, 3, 6, 5]
    result3 = find_planet_cycles(n3, teleporters3)
    print(f"Test 3: {result3}")

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through all planets
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Floyd's Algorithm**: Efficiently finds cycle entry points
- **Functional Graph**: Each planet has exactly one outgoing edge
- **Cycle Properties**: All planets in the same component enter the same cycle
- **Optimal Algorithm**: Best possible complexity for this problem

## 🎨 Visual Example

### Input Example
```
5 planets:
Planet 1 → Planet 2
Planet 2 → Planet 3
Planet 3 → Planet 4
Planet 4 → Planet 5
Planet 5 → Planet 3
```

### Graph Visualization
```
Functional graph:
1 → 2 → 3 → 4 → 5
         ↑       │
         └───────┘

Cycle: 3 → 4 → 5 → 3 (length 3)
```

### Floyd's Cycle Finding
```
For planet 1:
- Slow pointer: 1 → 2 → 3 → 4 → 5 → 3
- Fast pointer: 1 → 3 → 5 → 3 → 5 → 3
- Meet at planet 3 (cycle entry)

Cycle length calculation:
- Start from planet 3
- Count steps: 3 → 4 → 5 → 3
- Cycle length: 3
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Floyd's Cycle   │ O(n)         │ O(1)         │ Two pointers │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DFS + Visited   │ O(n)         │ O(n)         │ Mark visited │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Union-Find      │ O(n α(n))    │ O(n)         │ Component    │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Functional Graph Properties**
- Each planet has exactly one teleporter destination
- Paths eventually lead to cycles
- All planets in the same component enter the same cycle
- Cycle length is the same for all planets in a component

### 2. **Floyd's Cycle Finding**
- Use two pointers (slow and fast) to detect cycles
- Fast pointer moves twice as fast as slow pointer
- When they meet, a cycle is detected
- Efficiently finds cycle entry points

### 3. **Cycle Length Calculation**
- Once cycle entry is found, count steps to complete the cycle
- Cycle length is independent of starting planet
- All planets in the same component have the same cycle length
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
def planets_cycles_optimized(n, teleporters):
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
    
    # Find cycle entry and length for each planet
    results = []
    for i in range(1, n + 1):
        cycle_entry = find_cycle_entry(i)
        cycle_length = find_cycle_length(cycle_entry)
        results.append(cycle_length)
    
    return results

def solve_planets_cycles():
    n = int(input())
    teleporters = list(map(int, input().split()))
    
    result = find_planet_cycles(n, teleporters)
    print(*result)

def test_solution():
    # Test case 1: Simple cycle
    n1 = 5
    teleporters1 = [2, 3, 4, 5, 3]
    result1 = find_planet_cycles(n1, teleporters1)
    print(f"Test 1: {result1}")
    
    # Test case 2: Self-loop
    n2 = 3
    teleporters2 = [1, 2, 3]
    result2 = find_planet_cycles(n2, teleporters2)
    print(f"Test 2: {result2}")
    
    # Test case 3: Multiple cycles
    n3 = 6
    teleporters3 = [2, 1, 4, 3, 6, 5]
    result3 = find_planet_cycles(n3, teleporters3)
    print(f"Test 3: {result3}")

if __name__ == "__main__":
    solve_planets_cycles()
        
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

### Problem Variations

### **Variation 1: Cycle Detection with Costs**
**Problem**: Find cycle length and total cost for each planet.
```python
def planets_cycles_with_costs(n, teleporters, costs):
    # costs[i] = cost of teleporter from planet i to teleporters[i]
    
    def find_cycle_entry(start):
        slow = fast = start - 1
        while True:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            if slow == fast:
                break
        
        slow = start - 1
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
        
        return slow + 1
    
    def find_cycle_info(cycle_entry):
        length = 1
        total_cost = costs[cycle_entry - 1]
        current = teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            total_cost += costs[current - 1]
            current = teleporters[current - 1]
        
        return length, total_cost
    
    results = []
    for i in range(1, n + 1):
        cycle_entry = find_cycle_entry(i)
        length, cost = find_cycle_info(cycle_entry)
        results.append((length, cost))
    
    return results
```

### **Variation 2: Cycle Detection with Probabilities**
**Problem**: Find expected cycle length considering teleporter failure probabilities.
```python
def planets_cycles_with_probabilities(n, teleporters, probabilities):
    # probabilities[i] = probability that teleporter from i works
    
    def find_cycle_entry(start):
        slow = fast = start - 1
        while True:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            if slow == fast:
                break
        
        slow = start - 1
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
        
        return slow + 1
    
    def find_expected_cycle_length(cycle_entry):
        length = 1
        prob = probabilities[cycle_entry - 1]
        current = teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            prob *= probabilities[current - 1]
            current = teleporters[current - 1]
        
        return length, prob
    
    results = []
    for i in range(1, n + 1):
        cycle_entry = find_cycle_entry(i)
        length, prob = find_expected_cycle_length(cycle_entry)
        results.append((length, prob))
    
    return results
```

### **Variation 3: Dynamic Cycle Detection**
**Problem**: Handle dynamic updates to teleporter destinations.
```python
class DynamicPlanetsCycles:
    def __init__(self, n, teleporters):
        self.n = n
        self.teleporters = teleporters.copy()
        self.cycle_cache = {}
        self._compute_cycles()
    
    def _compute_cycles(self):
        """Recompute all cycle information"""
        self.cycle_cache.clear()
        
        for i in range(1, self.n + 1):
            if i not in self.cycle_cache:
                cycle_entry = self._find_cycle_entry(i)
                cycle_length = self._find_cycle_length(cycle_entry)
                
                # Cache for all planets in this cycle
                current = i
                while current not in self.cycle_cache:
                    self.cycle_cache[current] = (cycle_entry, cycle_length)
                    current = self.teleporters[current - 1]
    
    def _find_cycle_entry(self, start):
        slow = fast = start - 1
        while True:
            slow = self.teleporters[slow] - 1
            fast = self.teleporters[self.teleporters[fast] - 1] - 1
            if slow == fast:
                break
        
        slow = start - 1
        while slow != fast:
            slow = self.teleporters[slow] - 1
            fast = self.teleporters[fast] - 1
        
        return slow + 1
    
    def _find_cycle_length(self, cycle_entry):
        length = 1
        current = self.teleporters[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            current = self.teleporters[current - 1]
        
        return length
    
    def update_teleporter(self, planet, new_destination):
        """Update teleporter destination for a planet"""
        self.teleporters[planet - 1] = new_destination
        self._compute_cycles()
    
    def get_cycle_length(self, planet):
        """Get cycle length for a specific planet"""
        if planet in self.cycle_cache:
            return self.cycle_cache[planet][1]
        return None
```

### **Variation 4: Multi-Dimensional Cycles**
**Problem**: Detect cycles in multi-dimensional coordinate space.
```python
def multi_dimensional_cycles(n, teleporters_3d):
    # teleporters_3d = [(x, y, z) for each planet] - 3D coordinates
    
    def find_cycle_entry_3d(start):
        slow = fast = start - 1
        while True:
            slow = teleporters_3d[slow]
            fast = teleporters_3d[teleporters_3d[fast]]
            if slow == fast:
                break
        
        slow = start - 1
        while slow != fast:
            slow = teleporters_3d[slow]
            fast = teleporters_3d[fast]
        
        return slow + 1
    
    def find_cycle_length_3d(cycle_entry):
        length = 1
        current = teleporters_3d[cycle_entry - 1]
        
        while current != cycle_entry:
            length += 1
            current = teleporters_3d[current - 1]
        
        return length
    
    results = []
    for i in range(1, n + 1):
        cycle_entry = find_cycle_entry_3d(i)
        cycle_length = find_cycle_length_3d(cycle_entry)
        results.append(cycle_length)
    
    return results
```

### **Variation 5: Cycle Detection with Constraints**
**Problem**: Find cycles that satisfy specific constraints (e.g., minimum/maximum length).
```python
def constrained_cycle_detection(n, teleporters, min_length=1, max_length=float('inf')):
    def find_cycle_entry(start):
        slow = fast = start - 1
        while True:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            if slow == fast:
                break
        
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
    
    results = []
    for i in range(1, n + 1):
        cycle_entry = find_cycle_entry(i)
        cycle_length = find_cycle_length(cycle_entry)
        
        # Apply constraints
        if min_length <= cycle_length <= max_length:
            results.append(cycle_length)
        else:
            results.append(-1)  # Constraint violated
    
    return results
```

## 🎯 **Competitive Programming Variations**

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

## Related Problems

### **1. Cycle Detection Problems**
- **Cycle Detection in Linked Lists**: Find cycles in linked list structures
- **Cycle Detection in Arrays**: Detect cycles in array-based graphs
- **Functional Graph Cycles**: Handle cycles in functional graphs
- **Directed Graph Cycles**: Find cycles in directed graphs

### **2. Graph Traversal Problems**
- **DFS/BFS**: Graph traversal algorithms for cycle detection
- **Union-Find**: Connectivity data structure for cycle analysis
- **Topological Sorting**: Detect cycles in DAGs
- **Strongly Connected Components**: Find cycles in directed graphs

### **3. Two-Pointer Problems**
- **Floyd's Cycle Finding**: Two-pointer technique for cycle detection
- **Linked List Problems**: Various linked list cycle problems
- **Array Cycle Problems**: Cycle detection in arrays
- **String Cycle Problems**: Find cycles in string patterns

## Learning Points

### **1. Algorithm Design**
- **Floyd's Algorithm**: Essential technique for efficient cycle detection
- **Two-Pointer Technique**: Use slow and fast pointers for cycle finding
- **Functional Graph Analysis**: Understand properties of graphs with single outgoing edges
- **Cycle Properties**: Leverage cycle properties for efficient solutions

### **2. Implementation Techniques**
- **Cycle Entry Detection**: Find where cycles begin in paths
- **Cycle Length Calculation**: Efficiently compute cycle lengths
- **Caching Strategies**: Cache cycle information to avoid recomputation
- **Dynamic Updates**: Handle changes to graph structure

### **3. Problem-Solving Strategies**
- **Graph Decomposition**: Break graphs into cycles and paths
- **Efficient Traversal**: Avoid quadratic complexity through smart algorithms
- **Mathematical Properties**: Use mathematical properties of cycles
- **Optimization Techniques**: Trade space for time when appropriate

---

*This analysis demonstrates efficient cycle detection techniques and shows various extensions for planets cycles problems.* 