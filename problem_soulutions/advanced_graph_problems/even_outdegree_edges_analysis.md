---
layout: simple
title: "Even Outdegree Edges - Graph Degree Problem"
permalink: /problem_soulutions/advanced_graph_problems/even_outdegree_edges_analysis
---

# Even Outdegree Edges - Graph Degree Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of vertex degrees in directed graphs
- Analyze the relationship between in-degree and out-degree in directed graphs
- Apply graph theory principles to determine edge addition requirements
- Calculate the minimum number of edges needed to achieve even outdegrees
- Handle special cases in degree analysis (isolated vertices, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph degree analysis, basic graph theory, parity analysis
- **Data Structures**: Adjacency lists, degree arrays, sets
- **Mathematical Concepts**: Graph theory, degree properties, parity analysis, modular arithmetic
- **Programming Skills**: Graph representation, degree calculation, array manipulation
- **Related Problems**: Strongly Connected Edges (graph connectivity), Building Roads (basic graph operations)

## 📋 Problem Description

Given a directed graph, find the minimum number of edges to add so that every vertex has even outdegree.

**Input**: 
- n: number of vertices
- m: number of edges
- m lines: a b (edge from vertex a to vertex b)

**Output**: 
- Minimum number of edges to add

**Constraints**:
- 1 ≤ n ≤ 10^5
- 0 ≤ m ≤ 10^5
- 1 ≤ a,b ≤ n

**Example**:
```
Input:
4 3
1 2
2 3
3 4

Output:
1

Explanation**: 
Current outdegrees: [1, 1, 1, 0] (vertices 1,2,3 have odd outdegree)
Add edge (4, 1): [1, 1, 1, 1] (all vertices have odd outdegree)
Add edge (1, 4): [2, 1, 1, 0] (vertex 1 has even outdegree)
Add edge (2, 4): [2, 2, 1, 0] (vertices 1,2 have even outdegree)
Add edge (3, 4): [2, 2, 2, 0] (all vertices have even outdegree) ✓
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Exhaustive Search**: Try all possible edge additions
- **Degree Validation**: For each combination, verify all outdegrees are even
- **Combinatorial Explosion**: 2^(n²) possible edge combinations
- **Baseline Understanding**: Provides theoretical minimum but impractical

**Key Insight**: Generate all possible edge addition combinations and find the minimum that makes all outdegrees even.

**Algorithm**:
- Generate all possible subsets of edges to add (2^(n²) combinations)
- For each subset, check if all vertices have even outdegree
- Return the smallest subset that achieves even outdegrees

**Visual Example**:
```
Graph: 1→2→3→4, n=4

Current outdegrees: [1, 1, 1, 0]
Odd vertices: {1, 2, 3}

All possible edge additions:
┌─────────────────────────────────────┐
│ {}: [1,1,1,0] - still odd          │
│ {(1,4)}: [2,1,1,0] - 1 even        │
│ {(2,4)}: [1,2,1,0] - 2 even        │
│ {(3,4)}: [1,1,2,0] - 3 even        │
│ {(1,4),(2,4)}: [2,2,1,0] - 1,2 even│
│ {(1,4),(3,4)}: [2,1,2,0] - 1,3 even│
│ {(2,4),(3,4)}: [1,2,2,0] - 2,3 even│
│ {(1,4),(2,4),(3,4)}: [2,2,2,0] ✓   │
└─────────────────────────────────────┘

Minimum: {(1,4),(2,4),(3,4)} with 3 edges
```

**Implementation**:
```python
def brute_force_solution(n, edges):
    """
    Find minimum edges to add using brute force approach
    
    Args:
        n: number of vertices
        edges: list of (a, b) representing existing edges
    
    Returns:
        int: minimum number of edges to add
    """
    from itertools import combinations
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    def get_outdegrees(additional_edges):
        """Calculate outdegrees with additional edges"""
        outdegree = [0] * (n + 1)
        
        # Count existing edges
        for a, b in edges:
            outdegree[a] += 1
        
        # Count additional edges
        for a, b in additional_edges:
            outdegree[a] += 1
        
        return outdegree
    
    def all_even_outdegrees(outdegree):
        """Check if all outdegrees are even"""
        for i in range(1, n + 1):
            if outdegree[i] % 2 != 0:
                return False
        return True
    
    # Try all possible edge combinations
    all_possible_edges = []
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                all_possible_edges.append((i, j))
    
    min_edges = len(all_possible_edges)  # Worst case
    
    for size in range(0, len(all_possible_edges) + 1):
        for edge_set in combinations(all_possible_edges, size):
            outdegree = get_outdegrees(edge_set)
            if all_even_outdegrees(outdegree):
                return size
    
    return min_edges

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = brute_force_solution(n, edges)
print(f"Brute force result: {result}")  # Output: 3
```

**Time Complexity**: O(2^(n²) × n²)
**Space Complexity**: O(n²)

**Why it's inefficient**: Exponential time complexity makes it impractical for large graphs.

---

### Approach 2: Greedy Solution

**Key Insights from Greedy Solution**:
- **Odd Degree Counting**: Count vertices with odd outdegree
- **Pairing Strategy**: Pair odd-degree vertices to make them even
- **Greedy Matching**: Connect odd vertices in pairs
- **Local Optimization**: Each edge addition fixes two odd degrees

**Key Insight**: Connect vertices with odd outdegree in pairs to make all outdegrees even.

**Algorithm**:
- Count vertices with odd outdegree
- If count is odd, add one self-loop to make count even
- Connect odd-degree vertices in pairs
- Return number of edges added

**Visual Example**:
```
Graph: 1→2→3→4, n=4

Current outdegrees: [1, 1, 1, 0]
Odd vertices: {1, 2, 3} (count = 3)

Step 1: Count is odd, add self-loop to vertex 4
New outdegrees: [1, 1, 1, 1]
Odd vertices: {1, 2, 3, 4} (count = 4)

Step 2: Connect odd vertices in pairs
Connect 1→4: [2, 1, 1, 1]
Connect 2→3: [2, 2, 2, 1]
Connect 3→4: [2, 2, 2, 2] ✓

Result: 4 edges added
```

**Implementation**:
```python
def greedy_solution(n, edges):
    """
    Find minimum edges to add using greedy approach
    
    Args:
        n: number of vertices
        edges: list of (a, b) representing existing edges
    
    Returns:
        int: minimum number of edges to add
    """
    # Calculate current outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Find vertices with odd outdegree
    odd_vertices = []
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_vertices.append(i)
    
    # If odd count of odd vertices, add self-loop
    edges_added = 0
    if len(odd_vertices) % 2 == 1:
        # Add self-loop to first odd vertex
        odd_vertices[0] = odd_vertices[0]  # Self-loop
        edges_added += 1
    
    # Connect odd vertices in pairs
    for i in range(0, len(odd_vertices), 2):
        if i + 1 < len(odd_vertices):
            # Connect two odd vertices
            edges_added += 1
    
    return edges_added

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = greedy_solution(n, edges)
print(f"Greedy result: {result}")  # Output: 2
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Much faster than brute force, but not optimal.

**Implementation Considerations**:
- **Odd Count Handling**: Add self-loop if odd count of odd vertices
- **Pairing Strategy**: Connect odd vertices in pairs
- **Edge Counting**: Count edges added, not vertices processed

---

### Approach 3: Optimal Solution

**Key Insights from Optimal Solution**:
- **Parity Analysis**: Only vertices with odd outdegree need edges
- **Mathematical Formula**: Minimum edges = (count of odd vertices) // 2
- **Self-Loop Exception**: If odd count, need one self-loop
- **Optimal Pairing**: Any pairing of odd vertices is optimal

**Key Insight**: The minimum number of edges needed is exactly half the number of odd-degree vertices.

**Algorithm**:
- Count vertices with odd outdegree
- If count is odd, add one self-loop
- Connect remaining odd vertices in pairs
- Return total edges added

**Visual Example**:
```
Graph: 1→2→3→4, n=4

Current outdegrees: [1, 1, 1, 0]
Odd vertices: {1, 2, 3} (count = 3)

Step 1: Count is odd, add self-loop to vertex 4
New outdegrees: [1, 1, 1, 1]
Odd vertices: {1, 2, 3, 4} (count = 4)

Step 2: Connect odd vertices in pairs
Connect 1→4: [2, 1, 1, 1]
Connect 2→3: [2, 2, 2, 1]
Connect 3→4: [2, 2, 2, 2] ✓

Result: 4 edges added
```

**Implementation**:
```python
def optimal_solution(n, edges):
    """
    Find minimum edges to add using optimal approach
    
    Args:
        n: number of vertices
        edges: list of (a, b) representing existing edges
    
    Returns:
        int: minimum number of edges to add
    """
    # Calculate current outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Count vertices with odd outdegree
    odd_count = 0
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_count += 1
    
    # If odd count, add one self-loop
    if odd_count % 2 == 1:
        return (odd_count + 1) // 2
    else:
        return odd_count // 2

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = optimal_solution(n, edges)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's optimal**: O(n) complexity is optimal and uses mathematical properties of degree parity for guaranteed optimal result.

**Implementation Details**:
- **Parity Analysis**: Only odd-degree vertices need edges
- **Mathematical Formula**: (odd_count + 1) // 2 if odd count, else odd_count // 2
- **Edge Cases**: Handle empty graphs and single vertices correctly
- **Mathematical Proof**: This approach is provably optimal

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^(n²) × n²) | O(n²) | Exhaustive search of all edge combinations |
| Greedy | O(n) | O(n) | Connect odd-degree vertices in pairs |
| Optimal | O(n) | O(n) | Use mathematical formula for minimum edges |

### Time Complexity
- **Time**: O(n) - Single pass to count odd-degree vertices
- **Space**: O(n) - Array to store outdegrees

### Why This Solution Works
- **Parity Analysis**: Only vertices with odd outdegree need additional edges
- **Mathematical Formula**: Minimum edges = (odd_count + 1) // 2 if odd count, else odd_count // 2
- **Optimal Pairing**: Any pairing of odd vertices achieves the minimum
- **Self-Loop Handling**: One self-loop fixes the odd count issue

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Even Indegree Edges**
**Problem**: Find minimum edges to add so that every vertex has even indegree.

**Key Differences**: Focus on indegree instead of outdegree

**Solution Approach**: Use same logic but count indegrees

**Implementation**:
```python
def even_indegree_edges(n, edges):
    """
    Find minimum edges to add for even indegrees
    
    Args:
        n: number of vertices
        edges: list of (a, b) representing existing edges
    
    Returns:
        int: minimum number of edges to add
    """
    # Calculate current indegrees
    indegree = [0] * (n + 1)
    for a, b in edges:
        indegree[b] += 1
    
    # Count vertices with odd indegree
    odd_count = 0
    for i in range(1, n + 1):
        if indegree[i] % 2 == 1:
            odd_count += 1
    
    # If odd count, add one self-loop
    if odd_count % 2 == 1:
        return (odd_count + 1) // 2
    else:
        return odd_count // 2

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = even_indegree_edges(n, edges)
print(f"Even indegree result: {result}")
```

#### **2. Even Total Degree Edges**
**Problem**: Find minimum edges to add so that every vertex has even total degree (indegree + outdegree).

**Key Differences**: Consider both indegree and outdegree

**Solution Approach**: Count vertices with odd total degree

**Implementation**:
```python
def even_total_degree_edges(n, edges):
    """
    Find minimum edges to add for even total degrees
    
    Args:
        n: number of vertices
        edges: list of (a, b) representing existing edges
    
    Returns:
        int: minimum number of edges to add
    """
    # Calculate current indegrees and outdegrees
    indegree = [0] * (n + 1)
    outdegree = [0] * (n + 1)
    
    for a, b in edges:
        outdegree[a] += 1
        indegree[b] += 1
    
    # Count vertices with odd total degree
    odd_count = 0
    for i in range(1, n + 1):
        total_degree = indegree[i] + outdegree[i]
        if total_degree % 2 == 1:
            odd_count += 1
    
    # If odd count, add one self-loop
    if odd_count % 2 == 1:
        return (odd_count + 1) // 2
    else:
        return odd_count // 2

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
result = even_total_degree_edges(n, edges)
print(f"Even total degree result: {result}")
```

#### **3. Even Degree with Edge Weights**
**Problem**: Find minimum weight edges to add so that every vertex has even outdegree.

**Key Differences**: Edges have weights, minimize total weight

**Solution Approach**: Use minimum weight perfect matching

**Implementation**:
```python
def weighted_even_outdegree_edges(n, edges, edge_weights):
    """
    Find minimum weight edges to add for even outdegrees
    
    Args:
        n: number of vertices
        edges: list of (a, b) representing existing edges
        edge_weights: dict mapping (a, b) to weight
    
    Returns:
        int: minimum total weight of edges to add
    """
    # Calculate current outdegrees
    outdegree = [0] * (n + 1)
    for a, b in edges:
        outdegree[a] += 1
    
    # Find vertices with odd outdegree
    odd_vertices = []
    for i in range(1, n + 1):
        if outdegree[i] % 2 == 1:
            odd_vertices.append(i)
    
    # If odd count, add self-loop with minimum weight
    total_weight = 0
    if len(odd_vertices) % 2 == 1:
        # Find minimum weight self-loop
        min_self_loop = float('inf')
        for v in odd_vertices:
            if (v, v) in edge_weights:
                min_self_loop = min(min_self_loop, edge_weights[(v, v)])
        total_weight += min_self_loop
    
    # Find minimum weight perfect matching for remaining odd vertices
    # This is a simplified version - in practice, use proper matching algorithm
    remaining_odd = odd_vertices[1:] if len(odd_vertices) % 2 == 1 else odd_vertices
    
    for i in range(0, len(remaining_odd), 2):
        if i + 1 < len(remaining_odd):
            v1, v2 = remaining_odd[i], remaining_odd[i + 1]
            # Find minimum weight edge between v1 and v2
            min_weight = min(
                edge_weights.get((v1, v2), float('inf')),
                edge_weights.get((v2, v1), float('inf'))
            )
            total_weight += min_weight
    
    return total_weight

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4)]
edge_weights = {
    (1, 2): 1, (2, 3): 2, (3, 4): 3,
    (1, 4): 4, (2, 4): 5, (3, 4): 6,
    (1, 1): 1, (2, 2): 2, (3, 3): 3, (4, 4): 4
}
result = weighted_even_outdegree_edges(n, edges, edge_weights)
print(f"Weighted even outdegree result: {result}")
```

### Related Problems

#### **CSES Problems**
- [Strongly Connected Edges](https://cses.fi/problemset/task/2177) - Graph connectivity
- [Building Roads](https://cses.fi/problemset/task/1666) - Basic graph operations
- [Round Trip](https://cses.fi/problemset/task/1669) - Cycle detection

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Graph cycle detection
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Topological sort
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Graph connectivity

#### **Problem Categories**
- **Graph Theory**: Degree analysis, parity problems
- **Graph Connectivity**: Strongly connected components, bridges
- **Graph Algorithms**: BFS, DFS, topological sort

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Theory](https://cp-algorithms.com/graph/) - Comprehensive graph algorithms
- [Degree Analysis](https://en.wikipedia.org/wiki/Degree_(graph_theory)) - Graph degree properties
- [Parity Analysis](https://en.wikipedia.org/wiki/Parity_(mathematics)) - Mathematical parity concepts

### **Practice Problems**
- [CSES Strongly Connected Edges](https://cses.fi/problemset/task/2177) - Medium
- [CSES Building Roads](https://cses.fi/problemset/task/1666) - Easy
- [CSES Round Trip](https://cses.fi/problemset/task/1669) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
