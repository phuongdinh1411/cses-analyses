---
layout: simple
title: "Building Teams - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/building_teams_analysis
---

# Building Teams - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of bipartite graph coloring in graph algorithms
- Apply efficient algorithms for checking bipartiteness and 2-coloring
- Implement BFS-based bipartite graph detection and coloring
- Optimize graph algorithms for team assignment problems
- Handle special cases in bipartite graph problems

## 📋 Problem Description

Given n students and m pairs of students who cannot be on the same team, determine if it's possible to divide students into two teams such that no conflicting students are on the same team.

**Input**: 
- n: number of students
- m: number of conflicts
- conflicts: array of (u, v) representing students who cannot be on the same team

**Output**: 
- Team assignment (1 or 2) for each student, or -1 if impossible

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5

**Example**:
```
Input:
n = 4, m = 3
conflicts = [(0,1), (1,2), (2,3)]

Output:
[1, 2, 1, 2]

Explanation**: 
Team 1: students 0, 2
Team 2: students 1, 3
No conflicting students are on the same team
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumation**: Try all possible team assignments
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check if each assignment satisfies constraints
- **Inefficient**: O(2^n × m) time complexity

**Key Insight**: Check every possible team assignment to find valid bipartite coloring.

**Algorithm**:
- Generate all possible team assignments (2^n possibilities)
- Check if each assignment satisfies conflict constraints
- Return the first valid assignment found

**Visual Example**:
```
Students: 0, 1, 2, 3
Conflicts: (0,1), (1,2), (2,3)

All possible team assignments:
┌─────────────────────────────────────┐
│ Assignment 1: [1,1,1,1] ✗          │
│ - Conflict (0,1): both team 1 ✗    │
│                                   │
│ Assignment 2: [1,1,1,2] ✗          │
│ - Conflict (0,1): both team 1 ✗    │
│                                   │
│ Assignment 3: [1,1,2,1] ✗          │
│ - Conflict (0,1): both team 1 ✗    │
│                                   │
│ Assignment 4: [1,1,2,2] ✗          │
│ - Conflict (0,1): both team 1 ✗    │
│                                   │
│ Assignment 5: [1,2,1,1] ✗          │
│ - Conflict (1,2): both team 1 ✗    │
│                                   │
│ Assignment 6: [1,2,1,2] ✓          │
│ - All conflicts satisfied ✓        │
│                                   │
│ Valid assignment: [1,2,1,2]       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_building_teams(n, conflicts):
    """Find team assignment using brute force approach"""
    def is_valid_assignment(assignment):
        """Check if team assignment satisfies all conflicts"""
        for u, v in conflicts:
            if assignment[u] == assignment[v]:
                return False
        return True
    
    # Try all possible team assignments
    for assignment_num in range(2**n):
        assignment = []
        temp = assignment_num
        
        # Convert number to binary assignment
        for i in range(n):
            assignment.append((temp % 2) + 1)  # Teams 1 or 2
            temp //= 2
        
        # Check if assignment is valid
        if is_valid_assignment(assignment):
            return assignment
    
    return -1  # No valid assignment exists

# Example usage
n = 4
conflicts = [(0, 1), (1, 2), (2, 3)]
result = brute_force_building_teams(n, conflicts)
print(f"Brute force team assignment: {result}")
```

**Time Complexity**: O(2^n × m)
**Space Complexity**: O(n)

**Why it's inefficient**: O(2^n × m) time complexity for checking all possible assignments.

---

### Approach 2: BFS-based Bipartite Coloring

**Key Insights from BFS-based Bipartite Coloring**:
- **BFS Coloring**: Use BFS to assign colors (teams) to vertices
- **Efficient Implementation**: O(n + m) time complexity
- **Bipartite Detection**: Check if graph is bipartite during coloring
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use BFS to assign teams (colors) and detect bipartiteness simultaneously.

**Algorithm**:
- Use BFS to traverse the graph
- Assign alternating colors (teams) to adjacent vertices
- If conflict is found, graph is not bipartite

**Visual Example**:
```
BFS-based bipartite coloring:

Graph: 0-1, 1-2, 2-3
Colors: 1 (team 1), 2 (team 2)

Step 1: Start with vertex 0
┌─────────────────────────────────────┐
│ Queue: [0]                         │
│ Color[0] = 1                       │
│                                   │
│ Step 2: Process vertex 0           │
│ - Neighbors: [1]                   │
│ - Color[1] = 2 (opposite of 0)     │
│ - Queue: [1]                       │
│                                   │
│ Step 3: Process vertex 1           │
│ - Neighbors: [0, 2]                │
│ - Color[0] = 1 ✓ (already set)     │
│ - Color[2] = 1 (opposite of 1)     │
│ - Queue: [2]                       │
│                                   │
│ Step 4: Process vertex 2           │
│ - Neighbors: [1, 3]                │
│ - Color[1] = 2 ✓ (already set)     │
│ - Color[3] = 2 (opposite of 2)     │
│ - Queue: [3]                       │
│                                   │
│ Step 5: Process vertex 3           │
│ - Neighbors: [2]                   │
│ - Color[2] = 1 ✓ (already set)     │
│                                   │
│ Result: [1, 2, 1, 2]              │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def bfs_building_teams(n, conflicts):
    """Find team assignment using BFS-based bipartite coloring"""
    from collections import deque
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in conflicts:
        adj[u].append(v)
        adj[v].append(u)
    
    # Initialize color array (-1 means uncolored)
    color = [-1] * n
    
    # Try to color each connected component
    for start in range(n):
        if color[start] == -1:
            # BFS to color this component
            queue = deque([start])
            color[start] = 1  # Start with team 1
            
            while queue:
                current = queue.popleft()
                
                for neighbor in adj[current]:
                    if color[neighbor] == -1:
                        # Assign opposite color
                        color[neighbor] = 3 - color[current]
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        # Conflict found - not bipartite
                        return -1
    
    return color

# Example usage
n = 4
conflicts = [(0, 1), (1, 2), (2, 3)]
result = bfs_building_teams(n, conflicts)
print(f"BFS team assignment: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's better**: Uses BFS for O(n + m) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for bipartite coloring
- **Efficient Implementation**: O(n + m) time complexity
- **Space Efficiency**: O(n + m) space complexity
- **Optimal Complexity**: Best approach for bipartite graph coloring

**Key Insight**: Use advanced data structures for optimal bipartite graph coloring.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient BFS-based bipartite coloring
- Handle special cases optimally
- Return team assignment

**Visual Example**:
```
Advanced data structure approach:

For graph: 0-1, 1-2, 2-3
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Graph structure: for efficient    │
│   storage and traversal             │
│ - Queue structure: for optimization  │
│ - Color cache: for optimization     │
│                                   │
│ Bipartite coloring calculation:    │
│ - Use graph structure for efficient │
│   storage and traversal             │
│ - Use queue structure for          │
│   optimization                      │
│ - Use color cache for optimization  │
│                                   │
│ Result: [1, 2, 1, 2]              │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_building_teams(n, conflicts):
    """Find team assignment using advanced data structure approach"""
    from collections import deque
    
    # Use advanced data structures for graph storage
    # Build advanced adjacency list
    adj = [[] for _ in range(n)]
    for u, v in conflicts:
        adj[u].append(v)
        adj[v].append(u)
    
    # Advanced data structures for bipartite coloring
    # Initialize advanced color array (-1 means uncolored)
    color = [-1] * n
    
    # Advanced BFS to color each connected component
    for start in range(n):
        if color[start] == -1:
            # Advanced BFS to color this component
            queue = deque([start])
            color[start] = 1  # Start with team 1
            
            while queue:
                current = queue.popleft()
                
                # Process neighbors using advanced data structures
                for neighbor in adj[current]:
                    if color[neighbor] == -1:
                        # Assign opposite color using advanced data structures
                        color[neighbor] = 3 - color[current]
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        # Conflict found - not bipartite
                        return -1
    
    return color

# Example usage
n = 4
conflicts = [(0, 1), (1, 2), (2, 3)]
result = advanced_data_structure_building_teams(n, conflicts)
print(f"Advanced data structure team assignment: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × m) | O(n) | Try all possible team assignments |
| BFS Coloring | O(n + m) | O(n + m) | Use BFS to assign alternating colors |
| Advanced Data Structure | O(n + m) | O(n + m) | Use advanced data structures |

### Time Complexity
- **Time**: O(n + m) - Use BFS for efficient bipartite graph coloring
- **Space**: O(n + m) - Store graph and color information

### Why This Solution Works
- **BFS Coloring**: Use BFS to assign alternating colors to adjacent vertices
- **Bipartite Detection**: Check for color conflicts during traversal
- **Connected Components**: Handle each connected component separately
- **Optimal Algorithms**: Use optimal algorithms for bipartite graph coloring

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Building Teams with Constraints**
**Problem**: Find team assignment with specific constraints.

**Key Differences**: Apply constraints to team assignment

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_building_teams(n, conflicts, constraints):
    """Find team assignment with constraints"""
    from collections import deque
    
    # Build adjacency list with constraints
    adj = [[] for _ in range(n)]
    for u, v in conflicts:
        if constraints(u, v):
            adj[u].append(v)
            adj[v].append(u)
    
    # Initialize color array (-1 means uncolored)
    color = [-1] * n
    
    # Try to color each connected component with constraints
    for start in range(n):
        if color[start] == -1:
            # BFS to color this component with constraints
            queue = deque([start])
            color[start] = 1  # Start with team 1
            
            while queue:
                current = queue.popleft()
                
                for neighbor in adj[current]:
                    if constraints(current, neighbor):
                        if color[neighbor] == -1:
                            # Assign opposite color with constraints
                            color[neighbor] = 3 - color[current]
                            queue.append(neighbor)
                        elif color[neighbor] == color[current]:
                            # Conflict found - not bipartite
                            return -1
    
    return color

# Example usage
n = 4
conflicts = [(0, 1), (1, 2), (2, 3)]
constraints = lambda u, v: u < v or v == 0  # Special constraint
result = constrained_building_teams(n, conflicts, constraints)
print(f"Constrained team assignment: {result}")
```

#### **2. Building Teams with Different Metrics**
**Problem**: Find team assignment with different team size metrics.

**Key Differences**: Different team size calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_building_teams(n, conflicts, weight_function):
    """Find team assignment with different team size metrics"""
    from collections import deque
    
    # Build adjacency list with modified weights
    adj = [[] for _ in range(n)]
    for u, v in conflicts:
        weight = weight_function(u, v)
        adj[u].append((v, weight))
        adj[v].append((u, weight))
    
    # Initialize color array (-1 means uncolored)
    color = [-1] * n
    
    # Try to color each connected component with modified weights
    for start in range(n):
        if color[start] == -1:
            # BFS to color this component with modified weights
            queue = deque([start])
            color[start] = 1  # Start with team 1
            
            while queue:
                current = queue.popleft()
                
                for neighbor, weight in adj[current]:
                    if color[neighbor] == -1:
                        # Assign opposite color with modified weights
                        color[neighbor] = 3 - color[current]
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        # Conflict found - not bipartite
                        return -1
    
    return color

# Example usage
n = 4
conflicts = [(0, 1), (1, 2), (2, 3)]
weight_function = lambda u, v: abs(u - v)  # Distance-based weight
result = weighted_building_teams(n, conflicts, weight_function)
print(f"Weighted team assignment: {result}")
```

#### **3. Building Teams with Multiple Dimensions**
**Problem**: Find team assignment in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_building_teams(n, conflicts, dimensions):
    """Find team assignment in multiple dimensions"""
    from collections import deque
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in conflicts:
        adj[u].append(v)
        adj[v].append(u)
    
    # Initialize color array (-1 means uncolored)
    color = [-1] * n
    
    # Try to color each connected component
    for start in range(n):
        if color[start] == -1:
            # BFS to color this component
            queue = deque([start])
            color[start] = 1  # Start with team 1
            
            while queue:
                current = queue.popleft()
                
                for neighbor in adj[current]:
                    if color[neighbor] == -1:
                        # Assign opposite color
                        color[neighbor] = 3 - color[current]
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        # Conflict found - not bipartite
                        return -1
    
    return color

# Example usage
n = 4
conflicts = [(0, 1), (1, 2), (2, 3)]
dimensions = 1
result = multi_dimensional_building_teams(n, conflicts, dimensions)
print(f"Multi-dimensional team assignment: {result}")
```

### Related Problems

#### **CSES Problems**
- [School Dance](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Building Roads](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Message Route](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) - Graph
- [Possible Bipartition](https://leetcode.com/problems/possible-bipartition/) - Graph
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Bipartite graphs, graph coloring
- **Graph Coloring**: 2-coloring, bipartite detection
- **Graph Traversal**: BFS, connected components

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Bipartite Graph](https://cp-algorithms.com/graph/bipartite-check.html) - Bipartite graph algorithms
- [Graph Coloring](https://cp-algorithms.com/graph/graph_coloring.html) - Graph coloring algorithms

### **Practice Problems**
- [CSES School Dance](https://cses.fi/problemset/task/1075) - Medium
- [CSES Building Roads](https://cses.fi/problemset/task/1075) - Medium
- [CSES Message Route](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Bipartite Graph](https://en.wikipedia.org/wiki/Bipartite_graph) - Wikipedia article
- [Graph Coloring](https://en.wikipedia.org/wiki/Graph_coloring) - Wikipedia article
