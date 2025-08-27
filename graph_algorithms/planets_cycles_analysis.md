# CSES Planets Cycles - Problem Analysis

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