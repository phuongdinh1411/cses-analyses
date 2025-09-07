---
layout: simple
title: "School Dance - Maximum Bipartite Matching"
permalink: /problem_soulutions/graph_algorithms/school_dance_analysis
---

# School Dance - Maximum Bipartite Matching

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand bipartite matching problems and maximum matching concepts
- Apply maximum flow algorithms or Hungarian algorithm to solve bipartite matching
- Implement efficient bipartite matching algorithms with proper graph construction
- Optimize bipartite matching solutions using flow networks and matching algorithms
- Handle edge cases in bipartite matching (no matches possible, complete matching, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Maximum flow, bipartite matching, Hungarian algorithm, flow networks, matching algorithms
- **Data Structures**: Bipartite graphs, flow networks, matching data structures, graph representations
- **Mathematical Concepts**: Graph theory, bipartite graphs, matching theory, flow networks, optimization
- **Programming Skills**: Graph construction, flow algorithms, matching implementation, algorithm implementation
- **Related Problems**: Download Speed (maximum flow), Police Chase (flow problems), Bipartite matching

## 📋 Problem Description

Given n boys and m girls, where each boy can dance with certain girls, find the maximum number of boys and girls that can be matched for dancing.

This is a maximum bipartite matching problem where we need to find the maximum number of pairs that can be formed between boys and girls based on their preferences.

**Input**: 
- First line: Two integers n and m (number of boys and girls)
- Next n lines: k integers (girls that boy i can dance with)

**Output**: 
- Maximum number of boys and girls that can be matched

**Constraints**:
- 1 ≤ n, m ≤ 500
- 1 ≤ k ≤ m

**Example**:
```
Input:
3 3
1 2
2 3
1 3

Output:
3
```

**Explanation**: 
- Boy 1 can dance with girls 1, 2
- Boy 2 can dance with girls 2, 3
- Boy 3 can dance with girls 1, 3
- Maximum matching: (1,1), (2,2), (3,3) = 3 pairs

## 🎯 Visual Example

### Input Preferences
```
Boys: 3, Girls: 3
Preferences:
- Boy 1: can dance with girls 1, 2
- Boy 2: can dance with girls 2, 3
- Boy 3: can dance with girls 1, 3
```

### Bipartite Graph Construction
```
Step 1: Build bipartite graph
- Left side: Boys {1, 2, 3}
- Right side: Girls {1, 2, 3}
- Edges: (1,1), (1,2), (2,2), (2,3), (3,1), (3,3)

Graph representation:
Boys    Girls
1 ────── 1
│       │
└───────┼─── 2
        │   │
2 ──────┼───┼─── 3
        │   │
3 ──────┼───┘
        │
        └───── 3
```

### Maximum Matching Algorithm Process
```
Step 1: Initialize matching
- Matching: {}

Step 2: Find augmenting paths
- Start from unmatched boy 1
- Path: 1 → 1 (girl 1 unmatched)
- Add (1,1) to matching

- Start from unmatched boy 2
- Path: 2 → 2 (girl 2 unmatched)
- Add (2,2) to matching

- Start from unmatched boy 3
- Path: 3 → 3 (girl 3 unmatched)
- Add (3,3) to matching

Step 3: No more augmenting paths
- Maximum matching: {(1,1), (2,2), (3,3)}
- Size: 3
```

### Matching Analysis
```
Maximum matching found:
- Boy 1 ↔ Girl 1
- Boy 2 ↔ Girl 2
- Boy 3 ↔ Girl 3

All boys and girls are matched ✓
Maximum matching size: 3
```

### Key Insight
Maximum bipartite matching algorithm works by:
1. Building bipartite graph from preferences
2. Finding augmenting paths using DFS/BFS
3. Updating matching after each augmenting path
4. Time complexity: O(n × m) for bipartite matching
5. Space complexity: O(n + m) for graph representation

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find maximum number of boy-girl pairs that can dance together
- **Key Insight**: Convert to maximum flow problem with bipartite graph
- **Challenge**: Efficiently find maximum matching using flow algorithms

### Step 2: Initial Approach
**Maximum flow algorithm for bipartite matching:**

```python
def school_dance_naive(n, m, preferences):
    # Build bipartite graph
    # Source -> Boys -> Girls -> Sink
    total_nodes = 2 + n + m  # source + boys + girls + sink
    source = 0
    sink = total_nodes - 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys (capacity 1)
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls (capacity 1)
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink (capacity 1)
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs(source, sink):
        # Find augmenting path using BFS
        parent = [-1] * total_nodes
        parent[source] = source
        queue = [source]
        
        while queue:
            current = queue.pop(0)
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0  # No augmenting path found
        
        # Find bottleneck capacity
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(source, sink)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Step 3: Optimization/Alternative
**Optimized bipartite matching with better flow algorithms:**

```python
def school_dance_optimized(n, m, preferences):
    from collections import deque
    
    # Build bipartite graph
    total_nodes = 2 + n + m
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs(source, sink):
        parent = [-1] * total_nodes
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0
        
        # Find bottleneck and update residual graph
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(source, sink)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

**Why this improvement works**: We use optimized Ford-Fulkerson algorithm to find maximum bipartite matching efficiently.

### Step 4: Complete Solution

```python
from collections import deque

n, m = map(int, input().split())
preferences = []
for _ in range(n):
    line = list(map(int, input().split()))
    k = line[0]
    girls = line[1:]
    preferences.append(girls)

def find_maximum_matching(n, m, preferences):
    # Build bipartite graph
    total_nodes = 2 + n + m  # source + boys + girls + sink
    source = 0
    sink = total_nodes - 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys (capacity 1)
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls (capacity 1)
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink (capacity 1)
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs(source, sink):
        # Find augmenting path using BFS
        parent = [-1] * total_nodes
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0  # No augmenting path found
        
        # Find bottleneck capacity
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(source, sink)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow

result = find_maximum_matching(n, m, preferences)
print(result)
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple bipartite graph (should return maximum matching)
- **Test 2**: Complete bipartite graph (should return min(n,m))
- **Test 3**: No possible matches (should return 0)
- **Test 4**: Complex preferences (should find optimal matching)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Bipartite Matching via Max Flow | O(n * m * max_flow) | O((n+m)²) | Use max flow for bipartite matching |
| Optimized Bipartite Matching | O(n * m * max_flow) | O((n+m)²) | Optimized max flow implementation |

## 🎨 Visual Example

### Input Example
```
3 boys, 3 girls:
Boy 1 can dance with: girls 1, 2
Boy 2 can dance with: girls 2, 3
Boy 3 can dance with: girls 1, 3
```

### Bipartite Graph Visualization
```
Boys: 1, 2, 3
Girls: 1, 2, 3

    1 ──── 1
    │      │
    │      │
    2 ──── 2
    │      │
    │      │
    3 ──── 3

Edges: (1,1), (1,2), (2,2), (2,3), (3,1), (3,3)
```

### Maximum Flow Network
```
Add source (S) and sink (T):

    S ──1──→ 1 ──── 1 ──1──→ T
    │        │      │
    │        │      │
    └─1──→ 2 ──── 2 ──1──→ T
    │        │      │
    │        │      │
    └─1──→ 3 ──── 3 ──1──→ T

All edges from source to boys: capacity 1
All edges from girls to sink: capacity 1
All boy-girl edges: capacity 1
```

### Ford-Fulkerson Algorithm Process
```
Step 1: Find augmenting path S → 1 → 1 → T
- Flow: min(1, 1, 1) = 1
- Update residual capacities
- Total flow: 1

Step 2: Find augmenting path S → 2 → 2 → T
- Flow: min(1, 1, 1) = 1
- Update residual capacities
- Total flow: 2

Step 3: Find augmenting path S → 3 → 3 → T
- Flow: min(1, 1, 1) = 1
- Update residual capacities
- Total flow: 3

No more augmenting paths found.
Maximum flow: 3
```

### Matching Reconstruction
```
From the final flow:
- Boy 1 → Girl 1 (flow = 1)
- Boy 2 → Girl 2 (flow = 1)
- Boy 3 → Girl 3 (flow = 1)

Maximum matching: 3 pairs
(1,1), (2,2), (3,3)
```

### Alternative Matching
```
Another valid maximum matching:
- Boy 1 → Girl 2 (flow = 1)
- Boy 2 → Girl 3 (flow = 1)
- Boy 3 → Girl 1 (flow = 1)

Maximum matching: 3 pairs
(1,2), (2,3), (3,1)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Ford-Fulkerson  │ O(n×m×f)     │ O(n²)        │ Augmenting   │
│                 │              │              │ paths        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Hopcroft-Karp   │ O(n×m^0.5)   │ O(n+m)       │ BFS + DFS    │
│                 │              │              │ layers       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Hungarian       │ O(n³)        │ O(n²)        │ Assignment   │
│                 │              │              │ problem      │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **Maximum Bipartite Matching**: Find maximum number of pairs in bipartite graph
- **Maximum Flow**: Convert matching problem to flow problem
- **Ford-Fulkerson Algorithm**: Use augmenting paths to find maximum flow
- **Bipartite Graph**: Graph with two disjoint vertex sets

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted Bipartite Matching**
```python
def weighted_bipartite_matching(n, m, preferences, weights):
    # Find maximum weight bipartite matching
    
    from collections import deque
    
    # Build bipartite graph with weights
    total_nodes = 2 + n + m
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    cost = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
        cost[source][boy] = 0
        cost[boy][source] = 0
    
    # Boys to girls with weights
    for boy in range(1, n + 1):
        for i, girl in enumerate(preferences[boy - 1]):
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
            cost[boy][girl_node] = -weights[boy - 1][i]  # Negative for max weight
            cost[girl_node][boy] = weights[boy - 1][i]
    
    # Girls to sink
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
        cost[girl_node][sink] = 0
        cost[sink][girl_node] = 0
    
    # Min cost max flow algorithm
    def min_cost_max_flow():
        total_flow = 0
        total_cost = 0
        
        while True:
            # Bellman-Ford for shortest path
            dist = [float('inf')] * total_nodes
            parent = [-1] * total_nodes
            dist[source] = 0
            
            for _ in range(total_nodes - 1):
                for u in range(total_nodes):
                    for v in adj[u]:
                        if capacity[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                            dist[v] = dist[u] + cost[u][v]
                            parent[v] = u
            
            if parent[sink] == -1:
                break
            
            # Find bottleneck
            bottleneck = float('inf')
            current = sink
            while current != source:
                bottleneck = min(bottleneck, capacity[parent[current]][current])
                current = parent[current]
            
            # Update flow and cost
            current = sink
            while current != source:
                capacity[parent[current]][current] -= bottleneck
                capacity[current][parent[current]] += bottleneck
                total_cost += bottleneck * cost[parent[current]][current]
                current = parent[current]
            
            total_flow += bottleneck
        
        return total_flow, -total_cost  # Return positive cost
    
    flow, max_weight = min_cost_max_flow()
    return flow, max_weight
```

#### **2. Stable Marriage Problem**
```python
def stable_marriage(n, men_preferences, women_preferences):
    # Find stable matching using Gale-Shapley algorithm
    
    # Initialize
    men_free = list(range(n))
    women_engaged = [-1] * n
    men_proposals = [0] * n  # Track how many proposals each man made
    
    while men_free:
        man = men_free[0]
        
        # Get next woman to propose to
        if men_proposals[man] < n:
            woman = men_preferences[man][men_proposals[man]]
            men_proposals[man] += 1
            
            if women_engaged[woman] == -1:
                # Woman is free, engage them
                women_engaged[woman] = man
                men_free.pop(0)
            else:
                # Woman is engaged, check if she prefers this man
                current_man = women_engaged[woman]
                
                # Check woman's preference
                current_rank = women_preferences[woman].index(current_man)
                new_rank = women_preferences[woman].index(man)
                
                if new_rank < current_rank:
                    # Woman prefers new man
                    women_engaged[woman] = man
                    men_free.pop(0)
                    men_free.append(current_man)
                # If woman prefers current man, new man remains free
    
    return women_engaged
```

#### **3. Maximum Cardinality Matching with Constraints**
```python
def constrained_bipartite_matching(n, m, preferences, constraints):
    # Find maximum matching with additional constraints
    
    from collections import deque
    
    # Build bipartite graph with constraints
    total_nodes = 2 + n + m
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys with capacity constraints
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = constraints.get('max_boys_per_dance', 1)
    
    # Boys to girls
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink with capacity constraints
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = constraints.get('max_girls_per_dance', 1)
    
    # Ford-Fulkerson algorithm
    def max_flow():
        total_flow = 0
        
        while True:
            parent = [-1] * total_nodes
            parent[source] = source
            queue = deque([source])
            
            while queue:
                current = queue.popleft()
                
                for next_node in adj[current]:
                    if parent[next_node] == -1 and capacity[current][next_node] > 0:
                        parent[next_node] = current
                        queue.append(next_node)
                        
                        if next_node == sink:
                            break
            
            if parent[sink] == -1:
                break
            
            # Find bottleneck
            bottleneck = float('inf')
            current = sink
            while current != source:
                bottleneck = min(bottleneck, capacity[parent[current]][current])
                current = parent[current]
            
            # Update residual graph
            current = sink
            while current != source:
                capacity[parent[current]][current] -= bottleneck
                capacity[current][parent[current]] += bottleneck
                current = parent[current]
            
            total_flow += bottleneck
        
        return total_flow
    
    return max_flow()
```

## 🔗 Related Problems

### Links to Similar Problems
- **Maximum Bipartite Matching**: Various matching problems
- **Maximum Flow**: Flow network problems
- **Stable Marriage**: Preference-based matching problems
- **Graph Algorithms**: Bipartite graph problems

## 📚 Learning Points

### Key Takeaways
- **Maximum flow** can solve bipartite matching problems
- **Ford-Fulkerson algorithm** is efficient for finding maximum flow
- **Bipartite graphs** have special properties for matching
- **Augmenting paths** are key to finding maximum flow

## Key Insights for Other Problems

### 1. **Bipartite Matching**
**Principle**: Use maximum flow to find maximum bipartite matching.
**Applicable to**: Matching problems, assignment problems, network problems

### 2. **Network Flow Reduction**
**Principle**: Reduce bipartite matching to maximum flow problem.
**Applicable to**: Matching problems, flow problems, network problems

### 3. **Assignment Problems**
**Principle**: Use bipartite matching to solve assignment problems.
**Applicable to**: Assignment problems, matching problems, optimization problems

## Notable Techniques

### 1. **Bipartite Graph Construction**
```python
def build_bipartite_graph(n, m, preferences):
    total_nodes = 2 + n + m
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    return adj, capacity, source, sink
```

### 2. **Maximum Flow for Matching**
```python
def max_flow_matching(n, m, adj, capacity, source, sink):
    def bfs():
        parent = [-1] * len(adj)
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0
        
        # Find bottleneck
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    max_flow = 0
    while True:
        flow = bfs()
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

### 3. **Matching Extraction**
```python
def extract_matching(n, m, adj, capacity):
    matches = []
    for boy in range(1, n + 1):
        for girl in range(1, m + 1):
            girl_node = n + girl
            if capacity[girl_node][boy] > 0:  # Flow in reverse direction
                matches.append((boy, girl))
    return matches
```

## Problem-Solving Framework

1. **Identify problem type**: This is a bipartite matching problem
2. **Choose approach**: Use maximum flow to find maximum matching
3. **Build bipartite graph**: Create network with source, boys, girls, and sink
4. **Set capacities**: Assign unit capacities for matching constraints
5. **Find maximum flow**: Use Ford-Fulkerson algorithm
6. **Extract matching**: Convert flow to matching pairs
7. **Return result**: Output maximum number of matches

---

*This analysis shows how to efficiently find maximum bipartite matching using maximum flow algorithm.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: School Dance with Capacities**
**Problem**: Each boy/girl can dance with multiple partners (up to a capacity limit).
```python
def school_dance_with_capacities(n, m, preferences, boy_capacities, girl_capacities):
    # boy_capacities[i] = max partners for boy i
    # girl_capacities[i] = max partners for girl i
    
    total_nodes = n + m + 2
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys with capacities
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = boy_capacities[boy - 1]
    
    # Boys to girls
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink with capacities
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = girl_capacities[girl - 1]
    
    # Use Ford-Fulkerson
    def bfs():
        parent = [-1] * total_nodes
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0
        
        # Find bottleneck
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    max_flow = 0
    while True:
        flow = bfs()
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

#### **Variation 2: School Dance with Costs**
**Problem**: Each potential dance pair has a cost, find maximum matching with minimum total cost.
```python
def cost_based_school_dance(n, m, preferences, costs):
    # costs[(boy, girl)] = cost of dance pair
    
    total_nodes = n + m + 2
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    cost = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls with costs
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
            cost[boy][girl_node] = costs.get((boy, girl), 0)
            cost[girl_node][boy] = -cost[boy][girl_node]  # Reverse edge cost
    
    # Girls to sink
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    # Use minimum cost maximum flow
    def bellman_ford():
        dist = [float('inf')] * total_nodes
        parent = [-1] * total_nodes
        dist[source] = 0
        
        for _ in range(total_nodes - 1):
            for u in range(total_nodes):
                for v in adj[u]:
                    if capacity[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                        dist[v] = dist[u] + cost[u][v]
                        parent[v] = u
        
        return parent if dist[sink] != float('inf') else None
    
    total_cost = 0
    max_flow = 0
    
    while True:
        parent = bellman_ford()
        if parent is None:
            break
        
        # Find bottleneck
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update flow and cost
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            total_cost += bottleneck * cost[parent[current]][current]
            current = parent[current]
        
        max_flow += bottleneck
    
    return max_flow, total_cost
```

#### **Variation 3: School Dance with Probabilities**
**Problem**: Each potential dance pair has a probability of success, find expected maximum matching.
```python
def probabilistic_school_dance(n, m, preferences, probabilities):
    # probabilities[(boy, girl)] = probability of successful dance
    
    total_nodes = n + m + 2
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    # Calculate expected matching
    expected_matches = 0
    
    # For each potential pair, calculate expected contribution
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            prob = probabilities.get((boy, girl), 0.5)
            expected_matches += prob
    
    return expected_matches
```

#### **Variation 4: School Dance with Preferences**
**Problem**: Each boy/girl has preferences, find stable matching (no blocking pairs).
```python
def stable_school_dance(n, m, boy_preferences, girl_preferences):
    # boy_preferences[i] = list of girls in order of preference for boy i
    # girl_preferences[i] = list of boys in order of preference for girl i
    
    # Gale-Shapley algorithm for stable matching
    boy_partners = [-1] * n
    girl_partners = [-1] * m
    boy_proposals = [0] * n  # Track next girl to propose to
    
    # Keep track of proposals
    while True:
        # Find a boy who hasn't proposed to all his preferences
        current_boy = -1
        for boy in range(n):
            if boy_partners[boy] == -1 and boy_proposals[boy] < len(boy_preferences[boy]):
                current_boy = boy
                break
        
        if current_boy == -1:
            break  # All boys are matched or have proposed to all preferences
        
        # Boy proposes to next girl in his preference list
        girl = boy_preferences[current_boy][boy_proposals[current_boy]] - 1
        boy_proposals[current_boy] += 1
        
        if girl_partners[girl] == -1:
            # Girl is free, accept proposal
            boy_partners[current_boy] = girl
            girl_partners[girl] = current_boy
        else:
            # Girl is engaged, check if she prefers current boy
            current_partner = girl_partners[girl]
            
            # Check girl's preference order
            current_rank = girl_preferences[girl].index(current_partner + 1)
            new_rank = girl_preferences[girl].index(current_boy + 1)
            
            if new_rank < current_rank:
                # Girl prefers new boy, break engagement
                boy_partners[current_partner] = -1
                boy_partners[current_boy] = girl
                girl_partners[girl] = current_boy
    
    # Count matches
    matches = 0
    for boy in range(n):
        if boy_partners[boy] != -1:
            matches += 1
    
    return matches
```

#### **Variation 5: School Dance with Dynamic Updates**
**Problem**: Handle dynamic updates to preferences and find maximum matching after each update.
```python
def dynamic_school_dance(n, m, initial_preferences, updates):
    # updates = [(boy, new_preferences), ...]
    
    preferences = [pref[:] for pref in initial_preferences]
    results = []
    
    for boy, new_preferences in updates:
        # Update preferences
        preferences[boy - 1] = new_preferences[:]
        
        # Recompute maximum matching
        total_nodes = n + m + 2
        source = 0
        sink = total_nodes - 1
        
        adj = [[] for _ in range(total_nodes)]
        capacity = [[0] * total_nodes for _ in range(total_nodes)]
        
        # Source to boys
        for b in range(1, n + 1):
            adj[source].append(b)
            adj[b].append(source)
            capacity[source][b] = 1
        
        # Boys to girls
        for b in range(1, n + 1):
            for girl in preferences[b - 1]:
                girl_node = n + girl
                adj[b].append(girl_node)
                adj[girl_node].append(b)
                capacity[b][girl_node] = 1
        
        # Girls to sink
        for girl in range(1, m + 1):
            girl_node = n + girl
            adj[girl_node].append(sink)
            adj[sink].append(girl_node)
            capacity[girl_node][sink] = 1
        
        # Use Ford-Fulkerson
        def bfs():
            parent = [-1] * total_nodes
            parent[source] = source
            queue = deque([source])
            
            while queue:
                current = queue.popleft()
                for next_node in adj[current]:
                    if parent[next_node] == -1 and capacity[current][next_node] > 0:
                        parent[next_node] = current
                        queue.append(next_node)
                        if next_node == sink:
                            break
            
            if parent[sink] == -1:
                return 0
            
            # Find bottleneck
            bottleneck = float('inf')
            current = sink
            while current != source:
                bottleneck = min(bottleneck, capacity[parent[current]][current])
                current = parent[current]
            
            # Update residual graph
            current = sink
            while current != source:
                capacity[parent[current]][current] -= bottleneck
                capacity[current][parent[current]] += bottleneck
                current = parent[current]
            
            return bottleneck
        
        max_flow = 0
        while True:
            flow = bfs()
            if flow == 0:
                break
            max_flow += flow
        
        results.append(max_flow)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Matching Problems**
- **Maximum Matching**: Find maximum number of matches
- **Perfect Matching**: Matching where everyone is matched
- **Weighted Matching**: Matching with costs/weights
- **Stable Matching**: Matching with no blocking pairs

#### **2. Network Flow Problems**
- **Maximum Flow**: Find maximum flow in network
- **Bipartite Flow**: Flow in bipartite graphs
- **Minimum Cost Flow**: Flow with minimum cost
- **Multi-commodity Flow**: Multiple flows

#### **3. Graph Theory Problems**
- **Bipartite Graphs**: Graphs with two partitions
- **Matching Theory**: Theory of matchings in graphs
- **Hall's Marriage Theorem**: Condition for perfect matching
- **König's Theorem**: Relates matching to vertex cover

#### **4. Assignment Problems**
- **Job Assignment**: Assign jobs to workers
- **Room Assignment**: Assign rooms to people
- **Task Assignment**: Assign tasks to resources
- **Resource Allocation**: Allocate resources optimally

#### **5. Algorithmic Techniques**
- **Ford-Fulkerson**: Maximum flow algorithm
- **Gale-Shapley**: Stable matching algorithm
- **Hungarian Algorithm**: Weighted bipartite matching
- **Hopcroft-Karp**: Faster bipartite matching

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Sizes**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    preferences = []
    for _ in range(n):
        pref = list(map(int, input().split()))
        preferences.append(pref)
    
    result = school_dance(n, m, preferences)
    print(result)
```

#### **2. Range Queries on School Dance**
```python
def range_school_dance_queries(n, m, preferences, queries):
    # queries = [(start_boy, end_boy), ...] - find matching for subset of boys
    
    results = []
    for start, end in queries:
        subset_preferences = preferences[start-1:end]
        result = school_dance(end - start + 1, m, subset_preferences)
        results.append(result)
    
    return results
```

#### **3. Interactive School Dance Problems**
```python
def interactive_school_dance():
    n, m = map(int, input("Enter n and m: ").split())
    print("Enter boy preferences:")
    preferences = []
    for i in range(n):
        pref = list(map(int, input(f"Boy {i+1} preferences: ").split()))
        preferences.append(pref)
    
    result = school_dance(n, m, preferences)
    print(f"Maximum matches: {result}")
    
    # Show the matching
    matches = find_matching_pairs(n, m, preferences)
    print(f"Matching pairs: {matches}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Bipartite Graph Properties**: Properties of bipartite graphs
- **Matching Theory**: Mathematical theory of matchings
- **Flow Theory**: Theory of network flows
- **Stability Theory**: Theory of stable matchings

#### **2. Linear Programming**
- **Matching LP**: Linear programming formulation of matching
- **Flow LP**: Linear programming formulation of flow
- **Dual Problems**: Dual of matching problems
- **Integer Programming**: Integer solutions for matching

#### **3. Combinatorial Optimization**
- **Assignment Problems**: Combinatorial assignment problems
- **Resource Allocation**: Optimal resource allocation
- **Scheduling**: Optimal scheduling problems
- **Network Design**: Optimal network design

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Matching Algorithms**: Ford-Fulkerson, Gale-Shapley, Hungarian
- **Flow Algorithms**: Maximum flow, minimum cost flow
- **Graph Algorithms**: BFS, DFS, connectivity algorithms
- **Optimization Algorithms**: Linear programming, integer programming

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Linear Algebra**: Matrix representations of graphs
- **Optimization**: Mathematical optimization techniques
- **Combinatorics**: Combinatorial optimization

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Flow Networks**: Representing flow problems
- **Matching Extraction**: Finding actual matches from flow
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient matching techniques and shows various extensions for school dance problems.* 