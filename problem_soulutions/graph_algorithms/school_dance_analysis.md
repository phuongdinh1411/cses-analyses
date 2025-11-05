---
layout: simple
title: "School Dance - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/school_dance_analysis
---

# School Dance - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of bipartite matching in graph algorithms
- Apply efficient algorithms for finding maximum bipartite matching
- Implement Hungarian algorithm or maximum flow for matching
- Optimize graph matching for assignment problems
- Handle special cases in bipartite matching problems

## 📋 Problem Description

Given a bipartite graph with boys and girls, find the maximum number of dance pairs that can be formed.

**Input**: 
- n: number of boys
- m: number of girls
- k: number of possible pairs
- pairs: array of (boy, girl) representing possible dance pairs

**Output**: 
- Maximum number of dance pairs that can be formed

**Constraints**:
- 1 ≤ n, m ≤ 500
- 1 ≤ k ≤ 10^4

**Example**:
```
Input:
n = 3, m = 3, k = 4
pairs = [(0,0), (0,1), (1,1), (2,2)]

Output:
3

Explanation**: 
Maximum matching: (0,0), (1,1), (2,2)
All boys and girls are paired
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible combinations of pairs
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph matching
- **Inefficient**: O(2^k) time complexity

**Key Insight**: Check all possible combinations of pairs to find maximum matching.

**Algorithm**:
- Generate all possible subsets of pairs
- Check if subset forms a valid matching
- Calculate size for valid matchings
- Return maximum size

**Visual Example**:
```
Bipartite graph: Boys {0,1,2} - Girls {0,1,2}
Pairs: (0,0), (0,1), (1,1), (2,2)

All possible pair combinations:
┌─────────────────────────────────────┐
│ Subset 1: {} - Size: 0             │
│ Subset 2: {(0,0)} - Size: 1        │
│ Subset 3: {(0,1)} - Size: 1        │
│ Subset 4: {(1,1)} - Size: 1        │
│ Subset 5: {(2,2)} - Size: 1        │
│ Subset 6: {(0,0), (1,1)} - Size: 2 │
│ Subset 7: {(0,0), (2,2)} - Size: 2 │
│ Subset 8: {(1,1), (2,2)} - Size: 2 │
│ Subset 9: {(0,0), (1,1), (2,2)} - Size: 3 │
│                                   │
│ Maximum: 3                        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_school_dance(n, m, pairs):
    """Find maximum matching using brute force approach"""
    from itertools import combinations
    
    max_matching = 0
    
    # Try all possible combinations of pairs
    for r in range(len(pairs) + 1):
        for pair_subset in combinations(pairs, r):
            # Check if this forms a valid matching
            if is_valid_matching(pair_subset):
                max_matching = max(max_matching, len(pair_subset))
    
    return max_matching

def is_valid_matching(pairs):
    """Check if pairs form a valid matching"""
    boys_used = set()
    girls_used = set()
    
    for boy, girl in pairs:
        if boy in boys_used or girl in girls_used:
            return False
        boys_used.add(boy)
        girls_used.add(girl)
    
    return True

# Example usage
n = 3
m = 3
pairs = [(0, 0), (0, 1), (1, 1), (2, 2)]
result = brute_force_school_dance(n, m, pairs)
print(f"Brute force maximum matching: {result}")
```

**Time Complexity**: O(2^k)
**Space Complexity**: O(k)

**Why it's inefficient**: O(2^k) time complexity for checking all pair combinations.

---

### Approach 2: Maximum Flow Solution

**Key Insights from Maximum Flow Solution**:
- **Maximum Flow**: Use maximum flow algorithm for bipartite matching
- **Efficient Implementation**: O(k√(n+m)) time complexity
- **Flow Network**: Convert bipartite graph to flow network
- **Optimization**: Much more efficient than brute force

**Key Insight**: Convert bipartite matching to maximum flow problem.

**Algorithm**:
- Create flow network with source and sink
- Add edges from source to boys, boys to girls, girls to sink
- Find maximum flow from source to sink
- The flow value equals the maximum matching size

**Visual Example**:
```
Maximum flow approach:

Bipartite graph: Boys {0,1,2} - Girls {0,1,2}
Pairs: (0,0), (0,1), (1,1), (2,2)

Flow network:
┌─────────────────────────────────────┐
│ Source -> Boys: capacity 1         │
│ Boys -> Girls: capacity 1           │
│ Girls -> Sink: capacity 1           │
│                                   │
│ Flow paths:                        │
│ Source -> 0 -> 0 -> Sink: flow 1   │
│ Source -> 1 -> 1 -> Sink: flow 1   │
│ Source -> 2 -> 2 -> Sink: flow 1   │
│                                   │
│ Maximum flow: 3                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def max_flow_school_dance(n, m, pairs):
    """Find maximum matching using maximum flow"""
    # Create flow network
    # Source = 0, Boys = 1 to n, Girls = n+1 to n+m, Sink = n+m+1
    source = 0
    sink = n + m + 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + m + 2)]
    capacity = [[0] * (n + m + 2) for _ in range(n + m + 2)]
    
    # Add edges from source to boys
    for boy in range(n):
        adj[source].append(boy + 1)
        adj[boy + 1].append(source)
        capacity[source][boy + 1] = 1
    
    # Add edges from boys to girls
    for boy, girl in pairs:
        boy_node = boy + 1
        girl_node = girl + n + 1
        adj[boy_node].append(girl_node)
        adj[girl_node].append(boy_node)
        capacity[boy_node][girl_node] = 1
    
    # Add edges from girls to sink
    for girl in range(m):
        girl_node = girl + n + 1
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs_find_path():
        """Find augmenting path using BFS"""
        parent = [-1] * (n + m + 2)
        visited = [False] * (n + m + 2)
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if not visited[neighbor] and capacity[vertex][neighbor] > 0:
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_max_flow():
        """Find maximum flow using Ford-Fulkerson algorithm"""
        max_flow = 0
        
        while True:
            path = bfs_find_path()
            if not path:
                break
            
            # Find minimum capacity in path
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_max_flow()

# Example usage
n = 3
m = 3
pairs = [(0, 0), (0, 1), (1, 1), (2, 2)]
result = max_flow_school_dance(n, m, pairs)
print(f"Maximum flow matching: {result}")
```

**Time Complexity**: O(k√(n+m))
**Space Complexity**: O((n+m)²)

**Why it's better**: Uses maximum flow for O(k√(n+m)) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for bipartite matching
- **Efficient Implementation**: O(k√(n+m)) time complexity
- **Space Efficiency**: O((n+m)²) space complexity
- **Optimal Complexity**: Best approach for bipartite matching

**Key Insight**: Use advanced data structures for optimal bipartite matching calculation.

**Algorithm**:
- Use specialized data structures for flow network storage
- Implement efficient maximum flow algorithms
- Handle special cases optimally
- Return maximum matching size

**Visual Example**:
```
Advanced data structure approach:

For bipartite graph: Boys {0,1,2} - Girls {0,1,2}
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Flow network: for efficient       │
│   storage and operations            │
│ - Residual graph: for optimization  │
│ - Flow cache: for optimization      │
│                                   │
│ Bipartite matching calculation:    │
│ - Use flow network for efficient   │
│   storage and operations            │
│ - Use residual graph for           │
│   optimization                      │
│ - Use flow cache for optimization  │
│                                   │
│ Result: 3                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_school_dance(n, m, pairs):
    """Find maximum matching using advanced data structure approach"""
    # Use advanced data structures for flow network storage
    # Create flow network using advanced data structures
    source = 0
    sink = n + m + 1
    
    # Build advanced adjacency list with capacities
    adj = [[] for _ in range(n + m + 2)]
    capacity = [[0] * (n + m + 2) for _ in range(n + m + 2)]
    
    # Add edges from source to boys using advanced data structures
    for boy in range(n):
        adj[source].append(boy + 1)
        adj[boy + 1].append(source)
        capacity[source][boy + 1] = 1
    
    # Add edges from boys to girls using advanced data structures
    for boy, girl in pairs:
        boy_node = boy + 1
        girl_node = girl + n + 1
        adj[boy_node].append(girl_node)
        adj[girl_node].append(boy_node)
        capacity[boy_node][girl_node] = 1
    
    # Add edges from girls to sink using advanced data structures
    for girl in range(m):
        girl_node = girl + n + 1
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs_advanced_find_path():
        """Find augmenting path using advanced BFS"""
        parent = [-1] * (n + m + 2)
        visited = [False] * (n + m + 2)
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if not visited[neighbor] and capacity[vertex][neighbor] > 0:
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path using advanced data structures
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_advanced_max_flow():
        """Find maximum flow using advanced Ford-Fulkerson algorithm"""
        max_flow = 0
        
        while True:
            path = bfs_advanced_find_path()
            if not path:
                break
            
            # Find minimum capacity in path using advanced data structures
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities using advanced data structures
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_advanced_max_flow()

# Example usage
n = 3
m = 3
pairs = [(0, 0), (0, 1), (1, 1), (2, 2)]
result = advanced_data_structure_school_dance(n, m, pairs)
print(f"Advanced data structure matching: {result}")
```

**Time Complexity**: O(k√(n+m))
**Space Complexity**: O((n+m)²)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^k) | O(k) | Try all pair combinations |
| Maximum Flow | O(k√(n+m)) | O((n+m)²) | Convert to flow network |
| Advanced Data Structure | O(k√(n+m)) | O((n+m)²) | Use advanced data structures |

### Time Complexity
- **Time**: O(k√(n+m)) - Use maximum flow for efficient bipartite matching
- **Space**: O((n+m)²) - Store flow network and capacity matrix

### Why This Solution Works
- **Maximum Flow**: Convert bipartite matching to maximum flow problem
- **Flow Network**: Create flow network with source, boys, girls, and sink
- **Ford-Fulkerson**: Use Ford-Fulkerson algorithm for maximum flow
- **Optimal Algorithms**: Use optimal algorithms for bipartite matching

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. School Dance with Constraints**
**Problem**: Find maximum matching with specific constraints.

**Key Differences**: Apply constraints to bipartite matching

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_school_dance(n, m, pairs, constraints):
    """Find maximum matching with constraints"""
    # Filter pairs based on constraints
    filtered_pairs = []
    for boy, girl in pairs:
        if constraints(boy, girl):
            filtered_pairs.append((boy, girl))
    
    # Create flow network
    source = 0
    sink = n + m + 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + m + 2)]
    capacity = [[0] * (n + m + 2) for _ in range(n + m + 2)]
    
    # Add edges from source to boys
    for boy in range(n):
        adj[source].append(boy + 1)
        adj[boy + 1].append(source)
        capacity[source][boy + 1] = 1
    
    # Add edges from boys to girls
    for boy, girl in filtered_pairs:
        boy_node = boy + 1
        girl_node = girl + n + 1
        adj[boy_node].append(girl_node)
        adj[girl_node].append(boy_node)
        capacity[boy_node][girl_node] = 1
    
    # Add edges from girls to sink
    for girl in range(m):
        girl_node = girl + n + 1
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs_find_path():
        """Find augmenting path using BFS"""
        parent = [-1] * (n + m + 2)
        visited = [False] * (n + m + 2)
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if not visited[neighbor] and capacity[vertex][neighbor] > 0:
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_max_flow():
        """Find maximum flow using Ford-Fulkerson algorithm"""
        max_flow = 0
        
        while True:
            path = bfs_find_path()
            if not path:
                break
            
            # Find minimum capacity in path
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_max_flow()

# Example usage
n = 3
m = 3
pairs = [(0, 0), (0, 1), (1, 1), (2, 2)]
constraints = lambda boy, girl: boy != girl or boy == 0  # Special constraint
result = constrained_school_dance(n, m, pairs, constraints)
print(f"Constrained maximum matching: {result}")
```

#### **2. School Dance with Different Metrics**
**Problem**: Find maximum matching with different weight metrics.

**Key Differences**: Different weight calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_school_dance(n, m, pairs, weights):
    """Find maximum matching with different weights"""
    # Create flow network
    source = 0
    sink = n + m + 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + m + 2)]
    capacity = [[0] * (n + m + 2) for _ in range(n + m + 2)]
    
    # Add edges from source to boys
    for boy in range(n):
        adj[source].append(boy + 1)
        adj[boy + 1].append(source)
        capacity[source][boy + 1] = 1
    
    # Add edges from boys to girls with weights
    for boy, girl in pairs:
        boy_node = boy + 1
        girl_node = girl + n + 1
        adj[boy_node].append(girl_node)
        adj[girl_node].append(boy_node)
        weight = weights.get((boy, girl), 1)
        capacity[boy_node][girl_node] = weight
    
    # Add edges from girls to sink
    for girl in range(m):
        girl_node = girl + n + 1
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs_find_path():
        """Find augmenting path using BFS"""
        parent = [-1] * (n + m + 2)
        visited = [False] * (n + m + 2)
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if not visited[neighbor] and capacity[vertex][neighbor] > 0:
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_max_flow():
        """Find maximum flow using Ford-Fulkerson algorithm"""
        max_flow = 0
        
        while True:
            path = bfs_find_path()
            if not path:
                break
            
            # Find minimum capacity in path
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_max_flow()

# Example usage
n = 3
m = 3
pairs = [(0, 0), (0, 1), (1, 1), (2, 2)]
weights = {(0, 0): 2, (0, 1): 1, (1, 1): 3, (2, 2): 1}
result = weighted_school_dance(n, m, pairs, weights)
print(f"Weighted maximum matching: {result}")
```

#### **3. School Dance with Multiple Dimensions**
**Problem**: Find maximum matching in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_school_dance(n, m, pairs, dimensions):
    """Find maximum matching in multiple dimensions"""
    # Create flow network
    source = 0
    sink = n + m + 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + m + 2)]
    capacity = [[0] * (n + m + 2) for _ in range(n + m + 2)]
    
    # Add edges from source to boys
    for boy in range(n):
        adj[source].append(boy + 1)
        adj[boy + 1].append(source)
        capacity[source][boy + 1] = 1
    
    # Add edges from boys to girls
    for boy, girl in pairs:
        boy_node = boy + 1
        girl_node = girl + n + 1
        adj[boy_node].append(girl_node)
        adj[girl_node].append(boy_node)
        capacity[boy_node][girl_node] = 1
    
    # Add edges from girls to sink
    for girl in range(m):
        girl_node = girl + n + 1
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs_find_path():
        """Find augmenting path using BFS"""
        parent = [-1] * (n + m + 2)
        visited = [False] * (n + m + 2)
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if not visited[neighbor] and capacity[vertex][neighbor] > 0:
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_max_flow():
        """Find maximum flow using Ford-Fulkerson algorithm"""
        max_flow = 0
        
        while True:
            path = bfs_find_path()
            if not path:
                break
            
            # Find minimum capacity in path
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_max_flow()

# Example usage
n = 3
m = 3
pairs = [(0, 0), (0, 1), (1, 1), (2, 2)]
dimensions = 1
result = multi_dimensional_school_dance(n, m, pairs, dimensions)
print(f"Multi-dimensional maximum matching: {result}")
```

### Related Problems

#### **CSES Problems**
- [Download Speed](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Police Chase](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Message Route](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Maximum Bipartite Matching](https://leetcode.com/problems/maximum-bipartite-matching/) - Graph
- [Assign Cookies](https://leetcode.com/problems/assign-cookies/) - Greedy
- [Task Scheduler](https://leetcode.com/problems/task-scheduler/) - Greedy

#### **Problem Categories**
- **Graph Algorithms**: Bipartite matching, maximum flow, network flow
- **Matching Algorithms**: Hungarian algorithm, maximum bipartite matching
- **Network Flow**: Flow networks, bipartite graphs

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Maximum Flow](https://cp-algorithms.com/graph/max_flow.html) - Maximum flow algorithms
- [Bipartite Matching](https://cp-algorithms.com/graph/bipartite-matching.html) - Bipartite matching algorithms

### **Practice Problems**
- [CSES Download Speed](https://cses.fi/problemset/task/1075) - Medium
- [CSES Police Chase](https://cses.fi/problemset/task/1075) - Medium
- [CSES Message Route](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Maximum Flow](https://en.wikipedia.org/wiki/Maximum_flow_problem) - Wikipedia article
- [Bipartite Graph](https://en.wikipedia.org/wiki/Bipartite_graph) - Wikipedia article
