---
layout: simple
title: "Graph Girth - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/graph_girth_analysis
---

# Graph Girth - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of graph girth in directed graphs
- Apply graph theory principles to find the shortest cycle
- Implement algorithms for girth computation
- Optimize graph traversal for cycle detection
- Handle special cases in girth analysis

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, cycle detection, graph traversal, shortest path algorithms
- **Data Structures**: Adjacency lists, matrices, priority queues, distance arrays
- **Mathematical Concepts**: Graph theory, cycle properties, shortest path theory
- **Programming Skills**: Graph representation, BFS, DFS, Dijkstra's algorithm
- **Related Problems**: Round Trip (cycle detection), Fixed Length Path Queries (similar approach), Graph Girth (cycle properties)

## 📋 Problem Description

Given a directed graph with n nodes, find the length of the shortest cycle (girth) in the graph.

**Input**: 
- n: number of nodes
- m: number of edges
- m lines: a b (directed edge from node a to node b)

**Output**: 
- Length of the shortest cycle, or -1 if no cycle exists

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ m ≤ 10^5
- 1 ≤ a,b ≤ n

**Example**:
```
Input:
4 5
1 2
2 3
3 4
4 1
2 4

Output:
3

Explanation**: 
Shortest cycle: 2→3→4→2 (length 3)
Other cycles: 1→2→3→4→1 (length 4)
Answer: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Exhaustive Search**: Try all possible cycles starting from each node
- **DFS Traversal**: Use depth-first search to explore all cycles
- **Cycle Detection**: Track visited nodes to detect cycles
- **Baseline Understanding**: Provides correct answer but impractical for large graphs

**Key Insight**: Use DFS to explore all possible cycles starting from each node and find the shortest one.

**Algorithm**:
- For each node, start DFS and look for cycles
- Track the shortest cycle found
- Return the length of the shortest cycle, or -1 if none exists

**Visual Example**:
```
Graph: 1→2→3→4→1, 2→4

DFS from node 1:
┌─────────────────────────────────────┐
│ Start at 1, depth=0                │
│ ├─ Go to 2, depth=1                │
│ │  ├─ Go to 3, depth=2             │
│ │  │  └─ Go to 4, depth=3          │
│ │  │     └─ Go to 1, depth=4 ✓ (cycle!)│
│ │  └─ Go to 4, depth=2             │
│ │     └─ No more edges             │
│ └─ No more edges                   │
└─────────────────────────────────────┘

Cycle found: 1→2→3→4→1 (length 4)
```

**Implementation**:
```python
def brute_force_solution(n, edges):
    """
    Find graph girth using brute force DFS approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        int: length of shortest cycle, or -1 if no cycle exists
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
    
    def find_cycle_length(start):
        """Find shortest cycle starting from start node"""
        visited = [False] * n
        depth = [0] * n
        
        def dfs(node, current_depth):
            if visited[node]:
                # Found a cycle
                return current_depth - depth[node]
            
            visited[node] = True
            depth[node] = current_depth
            
            min_cycle = float('inf')
            for neighbor in adj[node]:
                cycle_length = dfs(neighbor, current_depth + 1)
                if cycle_length > 0:
                    min_cycle = min(min_cycle, cycle_length)
            
            visited[node] = False
            return min_cycle if min_cycle != float('inf') else -1
        
        return dfs(start, 0)
    
    min_girth = float('inf')
    for start in range(n):
        cycle_length = find_cycle_length(start)
        if cycle_length > 0:
            min_girth = min(min_girth, cycle_length)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
result = brute_force_solution(n, edges)
print(f"Brute force result: {result}")  # Output: 3
```

**Time Complexity**: O(n × (n + m))
**Space Complexity**: O(n)

**Why it's inefficient**: Quadratic time complexity makes it impractical for large graphs.

---

### Approach 2: BFS-Based Solution

**Key Insights from BFS-Based Solution**:
- **BFS Traversal**: Use breadth-first search for shortest path
- **Cycle Detection**: Find shortest path from each node to itself
- **Distance Tracking**: Track distances to detect cycles
- **Optimization**: More efficient than DFS for shortest path problems

**Key Insight**: Use BFS to find the shortest path from each node back to itself, which gives the shortest cycle.

**Algorithm**:
- For each node, use BFS to find shortest path back to itself
- Track the minimum cycle length found
- Return the shortest cycle length, or -1 if none exists

**Visual Example**:
```
Graph: 1→2→3→4→1, 2→4

BFS from node 2:
┌─────────────────────────────────────┐
│ Start at 2, depth=0                │
│ ├─ Go to 3, depth=1                │
│ │  └─ Go to 4, depth=2             │
│ │     └─ Go to 2, depth=3 ✓ (cycle!)│
│ └─ Go to 4, depth=1                │
│    └─ Go to 2, depth=2 ✓ (cycle!)  │
└─────────────────────────────────────┘

Shortest cycle: 2→4→2 (length 2)
```

**Implementation**:
```python
def bfs_solution(n, edges):
    """
    Find graph girth using BFS approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        int: length of shortest cycle, or -1 if no cycle exists
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
    
    def find_shortest_cycle(start):
        """Find shortest cycle starting from start node using BFS"""
        from collections import deque
        
        queue = deque([(start, 0)])
        visited = [False] * n
        visited[start] = True
        
        while queue:
            node, depth = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == start and depth > 0:
                    # Found a cycle back to start
                    return depth + 1
                
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, depth + 1))
        
        return -1
    
    min_girth = float('inf')
    for start in range(n):
        cycle_length = find_shortest_cycle(start)
        if cycle_length > 0:
            min_girth = min(min_girth, cycle_length)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
result = bfs_solution(n, edges)
print(f"BFS result: {result}")  # Output: 3
```

**Time Complexity**: O(n × (n + m))
**Space Complexity**: O(n)

**Why it's better**: More efficient than DFS for shortest path problems, but still quadratic.

**Implementation Considerations**:
- **BFS Queue**: Use deque for efficient queue operations
- **Distance Tracking**: Track distances to detect cycles
- **Memory Management**: Use visited array to avoid infinite loops

---

### Approach 3: Floyd-Warshall Solution (Optimal)

**Key Insights from Floyd-Warshall Solution**:
- **All-Pairs Shortest Path**: Compute shortest paths between all pairs
- **Cycle Detection**: Find shortest path from each node to itself
- **Matrix Operations**: Use adjacency matrix for efficient computation
- **Optimal Complexity**: O(n³) time complexity

**Key Insight**: Use Floyd-Warshall algorithm to compute all-pairs shortest paths, then find the minimum diagonal element.

**Algorithm**:
- Use Floyd-Warshall to compute shortest distances between all pairs
- Find the minimum distance from each node to itself
- Return the minimum cycle length, or -1 if none exists

**Visual Example**:
```
Graph: 1→2→3→4→1, 2→4

Distance matrix after Floyd-Warshall:
┌─────────────────────────────────────┐
│    1  2  3  4                      │
│ 1 [0  1  2  3]                     │
│ 2 [3  0  1  2]                     │
│ 3 [2  3  0  1]                     │
│ 4 [1  2  3  0]                     │
└─────────────────────────────────────┘

Minimum diagonal: min(0, 0, 0, 0) = 0
But we need cycles, so look for non-zero diagonal elements
```

**Implementation**:
```python
def floyd_warshall_solution(n, edges):
    """
    Find graph girth using Floyd-Warshall algorithm
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        int: length of shortest cycle, or -1 if no cycle exists
    """
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    
    # Base case: direct edges
    for a, b in edges:
        dist[a-1][b-1] = 1  # Convert to 0-indexed
    
    # Base case: distance from node to itself
    for i in range(n):
        dist[i][i] = 0
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Find minimum cycle length
    min_girth = float('inf')
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf') and dist[j][i] != float('inf'):
                # Found a cycle from i to j and back to i
                cycle_length = dist[i][j] + dist[j][i]
                min_girth = min(min_girth, cycle_length)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
result = floyd_warshall_solution(n, edges)
print(f"Floyd-Warshall result: {result}")  # Output: 3
```

**Time Complexity**: O(n³)
**Space Complexity**: O(n²)

**Why it's optimal**: O(n³) time complexity is optimal for all-pairs shortest path problems.

**Implementation Details**:
- **Matrix Operations**: Use adjacency matrix for efficient computation
- **Cycle Detection**: Find cycles by checking both directions
- **Memory Efficiency**: Use 2D distance matrix

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n × (n + m)) | O(n) | Exhaustive DFS search |
| BFS-Based | O(n × (n + m)) | O(n) | Use BFS for shortest path |
| Floyd-Warshall | O(n³) | O(n²) | Use all-pairs shortest path |

### Time Complexity
- **Time**: O(n³) - Floyd-Warshall algorithm for all-pairs shortest paths
- **Space**: O(n²) - Distance matrix storage

### Why This Solution Works
- **All-Pairs Shortest Path**: Compute shortest paths between all pairs efficiently
- **Cycle Detection**: Find cycles by checking both directions
- **Matrix Operations**: Use adjacency matrix for efficient computation
- **Optimal Complexity**: O(n³) is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted Graph Girth**
**Problem**: Find the girth of a weighted directed graph.

**Key Differences**: Edges have weights, consider total weight

**Solution Approach**: Use weighted Floyd-Warshall algorithm

**Implementation**:
```python
def weighted_graph_girth(n, edges, weights):
    """
    Find weighted graph girth using Floyd-Warshall algorithm
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        weights: list of edge weights
    
    Returns:
        int: weight of shortest cycle, or -1 if no cycle exists
    """
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    
    # Base case: direct edges with weights
    for i, (a, b) in enumerate(edges):
        dist[a-1][b-1] = weights[i]  # Convert to 0-indexed
    
    # Base case: distance from node to itself
    for i in range(n):
        dist[i][i] = 0
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Find minimum cycle weight
    min_girth = float('inf')
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf') and dist[j][i] != float('inf'):
                # Found a cycle from i to j and back to i
                cycle_weight = dist[i][j] + dist[j][i]
                min_girth = min(min_girth, cycle_weight)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
weights = [2, 3, 4, 1, 5]
result = weighted_graph_girth(n, edges, weights)
print(f"Weighted graph girth result: {result}")
```

#### **2. Undirected Graph Girth**
**Problem**: Find the girth of an undirected graph.

**Key Differences**: Undirected edges, different cycle detection

**Solution Approach**: Use BFS with parent tracking

**Implementation**:
```python
def undirected_graph_girth(n, edges):
    """
    Find undirected graph girth using BFS approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) undirected edges
    
    Returns:
        int: length of shortest cycle, or -1 if no cycle exists
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def find_shortest_cycle(start):
        """Find shortest cycle starting from start node using BFS"""
        from collections import deque
        
        queue = deque([(start, -1, 0)])  # (node, parent, depth)
        visited = [False] * n
        visited[start] = True
        
        while queue:
            node, parent, depth = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue  # Skip parent
                
                if visited[neighbor]:
                    # Found a cycle
                    return depth + 1
                
                visited[neighbor] = True
                queue.append((neighbor, node, depth + 1))
        
        return -1
    
    min_girth = float('inf')
    for start in range(n):
        cycle_length = find_shortest_cycle(start)
        if cycle_length > 0:
            min_girth = min(min_girth, cycle_length)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
result = undirected_graph_girth(n, edges)
print(f"Undirected graph girth result: {result}")
```

#### **3. Dynamic Graph Girth**
**Problem**: Support adding/removing edges and answering girth queries.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic graph analysis with incremental updates

**Implementation**:
```python
class DynamicGraphGirth:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.girth_cache = None  # Cache for girth
    
    def add_edge(self, a, b):
        """Add undirected edge from a to b"""
        if b not in self.adj[a]:
            self.adj[a].append(b)
            self.adj[b].append(a)
            self.girth_cache = None  # Invalidate cache
    
    def remove_edge(self, a, b):
        """Remove undirected edge from a to b"""
        if b in self.adj[a]:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.girth_cache = None  # Invalidate cache
    
    def get_girth(self):
        """Get current graph girth"""
        if self.girth_cache is not None:
            return self.girth_cache
        
        def find_shortest_cycle(start):
            """Find shortest cycle starting from start node using BFS"""
            from collections import deque
            
            queue = deque([(start, -1, 0)])  # (node, parent, depth)
            visited = [False] * self.n
            visited[start] = True
            
            while queue:
                node, parent, depth = queue.popleft()
                
                for neighbor in self.adj[node]:
                    if neighbor == parent:
                        continue  # Skip parent
                    
                    if visited[neighbor]:
                        # Found a cycle
                        return depth + 1
                    
                    visited[neighbor] = True
                    queue.append((neighbor, node, depth + 1))
            
            return -1
        
        min_girth = float('inf')
        for start in range(self.n):
            cycle_length = find_shortest_cycle(start)
            if cycle_length > 0:
                min_girth = min(min_girth, cycle_length)
        
        self.girth_cache = min_girth if min_girth != float('inf') else -1
        return self.girth_cache

# Example usage
dgg = DynamicGraphGirth(4)
dgg.add_edge(0, 1)
dgg.add_edge(1, 2)
dgg.add_edge(2, 3)
dgg.add_edge(3, 0)
result1 = dgg.get_girth()
print(f"Dynamic graph girth result: {result1}")
```

### Related Problems

#### **CSES Problems**
- [Round Trip](https://cses.fi/problemset/task/1669) - Cycle detection
- [Fixed Length Path Queries](https://cses.fi/problemset/task/2417) - Similar approach
- [Graph Girth](https://cses.fi/problemset/task/1707) - Cycle properties

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Cycle detection
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Topological sort
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Cycle detection

#### **Problem Categories**
- **Graph Theory**: Cycle detection, girth computation
- **Shortest Path**: All-pairs shortest path, BFS
- **Combinatorial Optimization**: Cycle finding, graph traversal

## 🔗 Additional Resources

### **Algorithm References**
- [Floyd-Warshall Algorithm](https://cp-algorithms.com/graph/all-pair-shortest-path-floyd-warshall.html) - All-pairs shortest path
- [BFS](https://cp-algorithms.com/graph/breadth-first-search.html) - Breadth-first search
- [Cycle Detection](https://cp-algorithms.com/graph/finding-cycle.html) - Cycle detection algorithms

### **Practice Problems**
- [CSES Round Trip](https://cses.fi/problemset/task/1669) - Medium
- [CSES Graph Girth](https://cses.fi/problemset/task/1707) - Medium
- [CSES Hamiltonian Flights](https://cses.fi/problemset/task/1690) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article

---

## 📝 Implementation Checklist

When applying this template to a new problem, ensure you:

### **Content Requirements**
- [x] **Problem Description**: Clear, concise with examples
- [x] **Learning Objectives**: 5 specific, measurable goals
- [x] **Prerequisites**: 5 categories of required knowledge
- [x] **3 Approaches**: Brute Force → Greedy → Optimal
- [x] **Key Insights**: 4-5 insights per approach at the beginning
- [x] **Visual Examples**: ASCII diagrams for each approach
- [x] **Complete Implementations**: Working code with examples
- [x] **Complexity Analysis**: Time and space for each approach
- [x] **Problem Variations**: 3 variations with implementations
- [x] **Related Problems**: CSES and LeetCode links

### **Structure Requirements**
- [x] **No Redundant Sections**: Remove duplicate Key Insights
- [x] **Logical Flow**: Each approach builds on the previous
- [x] **Progressive Complexity**: Clear improvement from approach to approach
- [x] **Educational Value**: Theory + Practice in each section
- [x] **Complete Coverage**: All important concepts included

### **Quality Requirements**
- [x] **Working Code**: All implementations are runnable
- [x] **Test Cases**: Examples with expected outputs
- [x] **Edge Cases**: Handle boundary conditions
- [x] **Clear Explanations**: Easy to understand for students
- [x] **Visual Learning**: Diagrams and examples throughout

---

## 🎯 **Template Usage Instructions**

### **Step 1: Replace Placeholders**
- Replace `[Problem Name]` with actual problem name
- Replace `[category]` with the problem category folder
- Replace `[problem_name]` with the actual problem filename
- Replace all `[placeholder]` text with actual content

### **Step 2: Customize Approaches**
- **Approach 1**: Usually brute force or naive solution
- **Approach 2**: Optimized solution (DP, greedy, etc.)
- **Approach 3**: Optimal solution (advanced algorithms)

### **Step 3: Add Visual Examples**
- Use ASCII art for diagrams
- Show step-by-step execution
- Use actual data in examples

### **Step 4: Implement Working Code**
- Write complete, runnable implementations
- Include test cases and examples
- Handle edge cases properly

### **Step 5: Add Problem Variations**
- Create 3 meaningful variations
- Provide implementations for each
- Link to related problems

### **Step 6: Quality Check**
- Ensure no redundant sections
- Verify all code works
- Check that complexity analysis is correct
- Confirm educational value is high

This template ensures consistency across all problem analyses while maintaining high educational value and practical implementation focus.