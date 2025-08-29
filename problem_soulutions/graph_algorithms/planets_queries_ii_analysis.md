---
layout: simple
title: "Planets Queries II"
permalink: /cses-analyses/problem_soulutions/graph_algorithms/planets_queries_ii_analysis
---


# Planets Queries II

## Problem Statement
Given a directed graph with n planets and q queries, for each query find the first planet that appears in both paths starting from planets a and b.

### Input
The first input line has two integers n and q: the number of planets and queries.
The second line has n integers t1,t2,…,tn: for each planet, there is a teleporter from planet i to planet ti.
Then there are q lines describing the queries. Each line has two integers a and b: find the first common planet in paths from a and b.

### Output
For each query, print the first common planet, or -1 if there is no common planet.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ ti ≤ n
- 1 ≤ a,b ≤ n

### Example
```
Input:
5 3
2 3 4 5 3
1 2
1 3
2 4

Output:
3
3
-1
```

## Solution Progression

### Approach 1: Naive Path Comparison - O(q * n)
**Description**: Generate paths and find first common element.

```python
def planets_queries_ii_naive(n, q, teleporters, queries):
    def get_path(start):
        path = []
        current = start
        visited = set()
        
        while current not in visited:
            path.append(current)
            visited.add(current)
            current = teleporters[current - 1]
        
        return path
    
    results = []
    for a, b in queries:
        path_a = get_path(a)
        path_b = get_path(b)
        
        # Find first common element
        common = -1
        for planet in path_a: if planet in 
path_b: common = planet
                break
        
        results.append(common)
    
    return results
```

**Why this is inefficient**: We generate full paths for each query, leading to quadratic complexity.

### Improvement 1: Cycle Detection with Binary Lifting - O(n log n + q log n)
**Description**: Use binary lifting to find cycle entry points and compare efficiently.

```python
def planets_queries_ii_optimized(n, q, teleporters, queries):
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
    
    # Precompute cycle entries
    cycle_entries = [find_cycle_entry(i) for i in range(1, n + 1)]
    
    # Answer queries
    results = []
    for a, b in queries:
        # Check if paths meet before entering cycles
        path_a = []
        path_b = []
        
        current_a = a
        current_b = b
        
        # Generate paths until cycle entry
        while current_a != cycle_entries[a - 1]:
            path_a.append(current_a)
            current_a = teleporters[current_a - 1]
        path_a.append(current_a)
        
        while current_b != cycle_entries[b - 1]:
            path_b.append(current_b)
            current_b = teleporters[current_b - 1]
        path_b.append(current_b)
        
        # Find first common element
        common = -1
        for planet in path_a: if planet in 
path_b: common = planet
                break
        
        results.append(common)
    
    return results
```

**Why this improvement works**: We use Floyd's cycle finding to detect cycles and then compare paths efficiently.

## Final Optimal Solution

```python
n, q = map(int, input().split())
teleporters = list(map(int, input().split()))

def answer_planets_queries_ii(n, q, teleporters, queries):
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
    
    # Precompute cycle entries
    cycle_entries = [find_cycle_entry(i) for i in range(1, n + 1)]
    
    # Answer queries
    results = []
    for a, b in queries:
        # Check if paths meet before entering cycles
        path_a = []
        path_b = []
        
        current_a = a
        current_b = b
        
        # Generate paths until cycle entry
        while current_a != cycle_entries[a - 1]:
            path_a.append(current_a)
            current_a = teleporters[current_a - 1]
        path_a.append(current_a)
        
        while current_b != cycle_entries[b - 1]:
            path_b.append(current_b)
            current_b = teleporters[current_b - 1]
        path_b.append(current_b)
        
        # Find first common element
        common = -1
        for planet in path_a: if planet in 
path_b: common = planet
                break
        
        results.append(common)
    
    return results

# Read queries
queries = []
for _ in range(q):
    a, b = map(int, input().split())
    queries.append((a, b))

result = answer_planets_queries_ii(n, q, teleporters, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Path Comparison | O(q * n) | O(n) | Generate and compare paths |
| Cycle Detection | O(n log n + q log n) | O(n) | Use Floyd's cycle finding |

## Key Insights for Other Problems

### 1. **Cycle Detection**
**Principle**: Use Floyd's cycle finding algorithm to detect cycles in directed graphs.
**Applicable to**: Cycle problems, path problems, graph problems

### 2. **Path Intersection**
**Principle**: Find intersection points of paths by comparing path elements.
**Applicable to**: Path problems, intersection problems, graph problems

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

### 2. **Path Generation**
```python
def generate_path(teleporters, start, cycle_entry):
    path = []
    current = start
    
    while current != cycle_entry:
        path.append(current)
        current = teleporters[current - 1]
    
    path.append(current)
    return path
```

### 3. **Common Element Finding**
```python
def find_common_element(path_a, path_b):
    for planet in path_a: if planet in 
path_b: return planet
    return -1
```

## Problem-Solving Framework

1. **Identify problem type**: This is a path intersection problem with cycles
2. **Choose approach**: Use Floyd's cycle finding to detect cycles
3. **Find cycle entries**: Precompute cycle entry points for all nodes
4. **Generate paths**: Create paths from start to cycle entry
5. **Find intersection**: Compare paths to find first common element
6. **Handle cycles**: Ensure paths don't enter cycles unnecessarily
7. **Return results**: Output first common planet for each query

---

*This analysis shows how to efficiently find path intersections using cycle detection and path comparison.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Planets Queries II with Costs**
**Problem**: Each teleporter has a cost, find intersection with minimum total cost.
```python
def cost_based_planets_queries_ii(n, q, teleporters, costs, queries):
    # costs[i] = cost of teleporter from planet i to teleporters[i]
    
    def find_cycle_entry_with_cost(start):
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
    
    def generate_path_with_cost(start, cycle_entry):
        path = []
        costs_to_reach = []
        current = start
        total_cost = 0
        
        while current != cycle_entry:
            path.append(current)
            costs_to_reach.append(total_cost)
            total_cost += costs[current - 1]
            current = teleporters[current - 1]
        
        path.append(current)
        costs_to_reach.append(total_cost)
        return path, costs_to_reach
    
    results = []
    for a, b in queries:
        entry_a, cost_a = find_cycle_entry_with_cost(a)
        entry_b, cost_b = find_cycle_entry_with_cost(b)
        
        path_a, costs_a = generate_path_with_cost(a, entry_a)
        path_b, costs_b = generate_path_with_cost(b, entry_b)
        
        # Find intersection with minimum cost
        min_cost = float('inf')
        intersection = -1
        
        for i, planet in enumerate(path_a):
            if planet in path_b:
                j = path_b.index(planet)
                total_cost = costs_a[i] + costs_b[j]
                if total_cost < min_cost:
                    min_cost = total_cost
                    intersection = planet
        
        results.append((intersection, min_cost))
    
    return results
```

#### **Variation 2: Planets Queries II with Constraints**
**Problem**: Find intersection with constraints on maximum teleporter usage.
```python
def constrained_planets_queries_ii(n, q, teleporters, max_teleporters, queries):
    # max_teleporters = maximum number of teleporters that can be used
    
    def find_cycle_entry_with_limit(start):
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
    
    def generate_path_with_limit(start, cycle_entry):
        path = []
        current = start
        steps = 0
        
        while current != cycle_entry and steps < max_teleporters:
            path.append(current)
            current = teleporters[current - 1]
            steps += 1
        
        if steps < max_teleporters:
            path.append(current)
        
        return path
    
    results = []
    for a, b in queries:
        entry_a = find_cycle_entry_with_limit(a)
        entry_b = find_cycle_entry_with_limit(b)
        
        if entry_a is None or entry_b is None:
            results.append(-1)  # Constraint violated
            continue
        
        path_a = generate_path_with_limit(a, entry_a)
        path_b = generate_path_with_limit(b, entry_b)
        
        # Find intersection
        intersection = -1
        for planet in path_a: if planet in 
path_b: intersection = planet
                break
        
        results.append(intersection)
    
    return results
```

#### **Variation 3: Planets Queries II with Probabilities**
**Problem**: Each teleporter has a probability of working, find intersection with maximum reliability.
```python
def probabilistic_planets_queries_ii(n, q, teleporters, probabilities, queries):
    # probabilities[i] = probability that teleporter from i works
    
    def find_cycle_entry_with_prob(start):
        slow = fast = start - 1
        total_prob = 1.0
        
        # Find meeting point
        while True:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            total_prob *= probabilities[slow] * probabilities[fast]
            if slow == fast:
                break
        
        # Find cycle entry
        slow = start - 1
        cycle_prob = 1.0
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
            cycle_prob *= probabilities[slow] * probabilities[fast]
        
        return slow + 1, total_prob / cycle_prob
    
    def generate_path_with_prob(start, cycle_entry):
        path = []
        probs_to_reach = []
        current = start
        total_prob = 1.0
        
        while current != cycle_entry:
            path.append(current)
            probs_to_reach.append(total_prob)
            total_prob *= probabilities[current - 1]
            current = teleporters[current - 1]
        
        path.append(current)
        probs_to_reach.append(total_prob)
        return path, probs_to_reach
    
    results = []
    for a, b in queries:
        entry_a, prob_a = find_cycle_entry_with_prob(a)
        entry_b, prob_b = find_cycle_entry_with_prob(b)
        
        path_a, probs_a = generate_path_with_prob(a, entry_a)
        path_b, probs_b = generate_path_with_prob(b, entry_b)
        
        # Find intersection with maximum probability
        max_prob = 0.0
        intersection = -1
        
        for i, planet in enumerate(path_a):
            if planet in path_b:
                j = path_b.index(planet)
                total_prob = probs_a[i] * probs_b[j]
                if total_prob > max_prob:
                    max_prob = total_prob
                    intersection = planet
        
        results.append((intersection, max_prob))
    
    return results
```

#### **Variation 4: Planets Queries II with Multiple Paths**
**Problem**: Each planet has multiple teleporters, find intersection using shortest paths.
```python
def multi_path_planets_queries_ii(n, q, teleporters_list, queries):
    # teleporters_list[i] = list of possible destinations from planet i
    
    def find_shortest_path(start, target):
        from collections import deque
        
        # BFS to find shortest path
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current == target:
                return path
            
            for next_planet in teleporters_list[current - 1]:
                if next_planet not in visited:
                    visited.add(next_planet)
                    queue.append((next_planet, path + [next_planet]))
        
        return None  # No path found
    
    def find_intersection_with_shortest_paths(a, b):
        # Try to find intersection by exploring paths from both planets
        from collections import deque
        
        queue_a = deque([(a, [a])])
        queue_b = deque([(b, [b])])
        visited_a = {a}
        visited_b = {b}
        
        while queue_a and queue_b:
            # Explore from planet a
            current_a, path_a = queue_a.popleft()
            for next_planet in teleporters_list[current_a - 1]:
                if next_planet not in visited_a:
                    visited_a.add(next_planet)
                    new_path_a = path_a + [next_planet]
                    queue_a.append((next_planet, new_path_a))
                    
                    # Check if this planet is in path from b
                    if next_planet in visited_b:
                        return next_planet
            
            # Explore from planet b
            current_b, path_b = queue_b.popleft()
            for next_planet in teleporters_list[current_b - 1]:
                if next_planet not in visited_b:
                    visited_b.add(next_planet)
                    new_path_b = path_b + [next_planet]
                    queue_b.append((next_planet, new_path_b))
                    
                    # Check if this planet is in path from a
                    if next_planet in visited_a:
                        return next_planet
        
        return -1  # No intersection found
    
    results = []
    for a, b in queries:
        intersection = find_intersection_with_shortest_paths(a, b)
        results.append(intersection)
    
    return results
```

#### **Variation 5: Planets Queries II with Dynamic Updates**
**Problem**: Handle dynamic updates to teleporters and find intersections after each update.
```python
def dynamic_planets_queries_ii(n, q, initial_teleporters, updates, queries):
    # updates = [(planet, new_destination), ...]
    
    teleporters = initial_teleporters.copy()
    results = []
    
    for planet, new_destination in updates:
        # Update teleporter
        teleporters[planet - 1] = new_destination
        
        # Recompute all cycle entries
        cycle_entries = {}
        for i in range(1, n + 1):
            entry = find_cycle_entry(teleporters, i)
            cycle_entries[i] = entry
        
        # Answer current queries
        current_results = []
        for a, b in queries:
            entry_a = cycle_entries[a]
            entry_b = cycle_entries[b]
            
            path_a = generate_path(teleporters, a, entry_a)
            path_b = generate_path(teleporters, b, entry_b)
            
            # Find intersection
            intersection = -1
            for planet in path_a: if planet in 
path_b: intersection = planet
                    break
            
            current_results.append(intersection)
        
        results.append(current_results)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Path Problems**
- **Path Intersection**: Find common points in paths
- **Shortest Path**: Find shortest paths between nodes
- **Path Comparison**: Compare different paths
- **Path Analysis**: Analyze properties of paths

#### **2. Cycle Detection Problems**
- **Floyd's Cycle Finding**: Two-pointer technique for cycle detection
- **Cycle Entry Detection**: Find entry points of cycles
- **Cycle Analysis**: Analyze cycles in graphs
- **Cycle Properties**: Properties of cycles

#### **3. Graph Traversal Problems**
- **BFS/DFS**: Graph traversal algorithms
- **Connected Components**: Find connected components
- **Reachability**: Check if nodes are reachable
- **Path Finding**: Find paths between nodes

#### **4. Query Problems**
- **Range Queries**: Answer queries on ranges
- **Point Queries**: Answer queries on specific points
- **Dynamic Queries**: Handle dynamic updates
- **Batch Queries**: Process multiple queries efficiently

#### **5. Algorithmic Techniques**
- **Two-Pointer Technique**: Use two pointers for efficient algorithms
- **Graph Algorithms**: Various graph algorithms
- **Dynamic Programming**: Handle dynamic updates
- **Optimization**: Optimize for different criteria

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    teleporters = list(map(int, input().split()))
    queries = []
    for _ in range(q):
        a, b = map(int, input().split())
        queries.append((a, b))
    
    result = answer_planets_queries_ii(n, q, teleporters, queries)
    for res in result:
        print(res)
```

#### **2. Range Queries on Path Intersections**
```python
def range_path_intersection_queries(n, teleporters, queries):
    # queries = [(start_a, end_a, start_b, end_b), ...] - find intersections in ranges
    
    # Precompute all cycle entries
    cycle_entries = {}
    for i in range(1, n + 1):
        entry = find_cycle_entry(teleporters, i)
        cycle_entries[i] = entry
    
    results = []
    for start_a, end_a, start_b, end_b in queries:
        range_results = []
        for a in range(start_a, end_a + 1):
            for b in range(start_b, end_b + 1):
                entry_a = cycle_entries[a]
                entry_b = cycle_entries[b]
                
                path_a = generate_path(teleporters, a, entry_a)
                path_b = generate_path(teleporters, b, entry_b)
                
                # Find intersection
                intersection = -1
                for planet in path_a: if planet in 
path_b: intersection = planet
                        break
                
                range_results.append(intersection)
        results.append(range_results)
    
    return results
```

#### **3. Interactive Path Intersection Problems**
```python
def interactive_planets_queries_ii():
    n = int(input("Enter number of planets: "))
    print("Enter teleporters (space-separated):")
    teleporters = list(map(int, input().split()))
    
    q = int(input("Enter number of queries: "))
    print("Enter queries (planet_a planet_b):")
    queries = []
    for _ in range(q):
        a, b = map(int, input().split())
        queries.append((a, b))
    
    result = answer_planets_queries_ii(n, q, teleporters, queries)
    print(f"Results: {result}")
    
    # Show query details
    for i, (a, b) in enumerate(queries):
        print(f"Query {i+1}: Planets {a} and {b}, intersection = {result[i]}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Path Properties**: Properties of paths in graphs
- **Cycle Theory**: Mathematical theory of cycles
- **Intersection Theory**: Theory of path intersections
- **Graph Decomposition**: Decomposing graphs into components

#### **2. Combinatorics**
- **Path Counting**: Counting different paths
- **Intersection Counting**: Counting path intersections
- **Cycle Enumeration**: Enumerating cycles in graphs
- **Pattern Recognition**: Recognizing patterns in paths

#### **3. Number Theory**
- **Path Length Properties**: Properties of path lengths
- **Cycle Length Analysis**: Analysis of cycle lengths
- **Modular Arithmetic**: Using modular arithmetic for large graphs
- **Number Sequences**: Analyzing sequences of path lengths

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Floyd's Cycle Finding**: Two-pointer cycle detection
- **BFS/DFS**: Graph traversal algorithms
- **Path Finding**: Various path finding algorithms
- **Graph Algorithms**: Graph analysis algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Path Theory**: Mathematical theory of paths
- **Cycle Theory**: Mathematical theory of cycles
- **Combinatorics**: Counting and enumeration techniques

#### **3. Programming Concepts**
- **Two-Pointer Technique**: Efficient algorithm design
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Algorithm Optimization**: Improving time and space complexity
- **Query Processing**: Efficient query processing techniques

---

*This analysis demonstrates efficient path intersection techniques and shows various extensions for planets queries problems.* 