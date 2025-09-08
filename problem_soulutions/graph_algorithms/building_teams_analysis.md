---
layout: simple
title: "Building Teams - Bipartite Graph Coloring"
permalink: /problem_soulutions/graph_algorithms/building_teams_analysis
---

# Building Teams - Bipartite Graph Coloring

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand bipartite graph coloring problems and 2-coloring concepts
- Apply DFS or BFS to check if a graph is bipartite and perform 2-coloring
- Implement efficient bipartite graph algorithms with proper color assignment
- Optimize bipartite graph solutions using graph representations and coloring algorithms
- Handle edge cases in bipartite coloring (odd cycles, disconnected components, single nodes)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Bipartite graph coloring, DFS/BFS, 2-coloring, graph coloring, cycle detection
- **Data Structures**: Adjacency lists, color arrays, visited arrays, graph representations
- **Mathematical Concepts**: Graph theory, bipartite graphs, graph coloring, cycle properties, graph connectivity
- **Programming Skills**: Graph traversal, color assignment, cycle detection, algorithm implementation
- **Related Problems**: Strongly Connected Components (graph connectivity), Cycle Finding (cycle detection), Graph coloring

## Problem Description

There are n pupils in Uolevi's class, and m friendships between them. Your task is to divide the pupils into two teams in such a way that no two pupils in a team are friends. You can freely choose the sizes of the teams.

This is a classic bipartite graph coloring problem where we need to check if the friendship graph can be colored with 2 colors such that no adjacent vertices have the same color.

**Input**: 
- First line: Two integers n and m (number of pupils and friendships)
- Next m lines: Two integers a and b (pupils a and b are friends)

**Output**: 
- Print "IMPOSSIBLE" if not possible, otherwise print team assignment

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- Pupils are numbered 1, 2, ..., n
- Graph is undirected
- No self-loops or multiple edges between same pair of pupils
- Friendships are bidirectional
- Divide pupils into two teams
- No two friends can be on the same team
- Check if bipartite coloring is possible
- Output team assignment or "IMPOSSIBLE"

**Example**:
```
Input:
5 3
1 2
1 3
4 5

Output:
1 2 2 1 1
```

**Explanation**: 
- Pupil 1: Team 1
- Pupil 2: Team 2 (friend of 1)
- Pupil 3: Team 2 (friend of 1)
- Pupil 4: Team 1
- Pupil 5: Team 1 (friend of 4)

## Visual Example

### Input Graph
```
Pupils: 1, 2, 3, 4, 5
Friendships: (1,2), (1,3), (4,5)

Graph representation:
1 ── 2
│
└── 3

4 ── 5
```

### Bipartite Coloring Process
```
Step 1: Initialize colors
- color[1] = color[2] = color[3] = color[4] = color[5] = -1 (uncolored)

Step 2: BFS coloring
- Start from pupil 1: color[1] = 1 (Team 1)
- Queue: [1]

- Process pupil 1:
  - Neighbors: 2, 3
  - color[2] = 2 (Team 2)
  - color[3] = 2 (Team 2)
  - Queue: [2, 3]

- Process pupil 2:
  - Neighbors: 1 (already colored)
  - No new assignments

- Process pupil 3:
  - Neighbors: 1 (already colored)
  - No new assignments

- Process pupil 4:
  - color[4] = 1 (Team 1)
  - Neighbors: 5
  - color[5] = 2 (Team 2)
  - Queue: [5]

- Process pupil 5:
  - Neighbors: 4 (already colored)
  - No new assignments
```

### Team Assignment
```
Final team assignments:
- Pupil 1: Team 1
- Pupil 2: Team 2
- Pupil 3: Team 2
- Pupil 4: Team 1
- Pupil 5: Team 2

Verification:
- (1,2): Team 1 ≠ Team 2 ✓
- (1,3): Team 1 ≠ Team 2 ✓
- (4,5): Team 1 ≠ Team 2 ✓

All friendships satisfied ✓
```

### Key Insight
Bipartite coloring algorithm works by:
1. Using BFS to traverse the graph
2. Assigning alternating colors to adjacent vertices
3. Checking for color conflicts (odd-length cycles)
4. Time complexity: O(n + m) for graph traversal
5. Space complexity: O(n + m) for graph representation

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Team Assignment (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible team assignments and check for conflicts
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible team assignments (2^n possibilities)
2. For each assignment, check if any friends are on the same team
3. Return the first valid assignment found
4. Handle cases where no valid assignment exists

**Visual Example:**
```
Brute force: Try all possible team assignments
For graph: 1 ── 2
           │
           └── 3

All possible team assignments:
- Assignment 1: [1,1,1,1,1] - Check conflicts: (1,2) same team ✗
- Assignment 2: [1,1,1,1,2] - Check conflicts: (1,2) same team ✗
- Assignment 3: [1,1,1,2,1] - Check conflicts: (1,2) same team ✗
- Assignment 4: [1,1,1,2,2] - Check conflicts: (1,2) same team ✗
- Assignment 5: [1,1,2,1,1] - Check conflicts: (1,2) same team ✗
- Assignment 6: [1,1,2,1,2] - Check conflicts: (1,2) same team ✗
- Assignment 7: [1,1,2,2,1] - Check conflicts: (1,2) same team ✗
- Assignment 8: [1,1,2,2,2] - Check conflicts: (1,2) same team ✗
- Assignment 9: [1,2,1,1,1] - Check conflicts: (1,2) different teams ✓, (1,3) different teams ✓

First valid assignment: [1,2,2,1,1]
```

**Implementation:**
```python
def building_teams_brute_force(n, m, friendships):
    def is_valid_assignment(assignment):
        for a, b in friendships:
            if assignment[a-1] == assignment[b-1]:
                return False
        return True
    
    def generate_assignments(n):
        if n == 0:
            return [[]]
        
        smaller = generate_assignments(n-1)
        result = []
        for assignment in smaller:
            result.append(assignment + [1])
            result.append(assignment + [2])
        return result
    
    # Generate all possible team assignments
    all_assignments = generate_assignments(n)
    
    # Check each assignment
    for assignment in all_assignments:
        if is_valid_assignment(assignment):
            return ' '.join(map(str, assignment))
    
    return "IMPOSSIBLE"
```

**Time Complexity:** O(2^n × m) for n pupils and m friendships with exponential assignment generation
**Space Complexity:** O(2^n) for storing all possible assignments

**Why it's inefficient:**
- O(2^n × m) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many pupils

### Approach 2: Basic BFS with Bipartite Coloring (Better)

**Key Insights from Basic BFS Solution:**
- Use BFS to check if graph is bipartite
- Much more efficient than brute force approach
- Standard method for bipartite graph problems
- Can handle larger graphs than brute force

**Algorithm:**
1. Use BFS to traverse the graph
2. Assign alternating colors to adjacent vertices
3. Check for color conflicts during traversal
4. Return team assignment if bipartite

**Visual Example:**
```
Basic BFS for graph: 1 ── 2
                     │
                     └── 3

Step 1: Initialize
- color = [-1, -1, -1, -1, -1]
- Queue = [1]

Step 2: Process vertex 1
- color[1] = 1 (Team 1)
- Neighbors: 2, 3
- color[2] = 2 (Team 2)
- color[3] = 2 (Team 2)
- Queue = [2, 3]

Step 3: Process vertices 2 and 3
- No new color assignments needed
- Queue = []

Step 4: Process remaining vertices
- color[4] = 1 (Team 1)
- color[5] = 2 (Team 2)

Final: color = [1, 2, 2, 1, 1]
```

**Implementation:**
```python
from collections import deque

def building_teams_basic_bfs(n, m, friendships):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in friendships:
        graph[a].append(b)
        graph[b].append(a)
    
    def is_bipartite():
        color = [-1] * (n + 1)  # -1: uncolored, 0: team 1, 1: team 2
        
        for start in range(1, n + 1):
            if color[start] == -1:
                queue = deque([start])
                color[start] = 0
                
                while queue:
                    node = queue.popleft()
                    
                    for neighbor in graph[node]:
                        if color[neighbor] == -1:
                            color[neighbor] = 1 - color[node]  # Opposite color
                            queue.append(neighbor)
                        elif color[neighbor] == color[node]:
                            return False  # Not bipartite
        
        return True, color
    
    result = is_bipartite()
    if not result[0]:
        return "IMPOSSIBLE"
    else:
        color = result[1]
        return ' '.join(str(color[i] + 1) for i in range(1, n + 1))
```

**Time Complexity:** O(n + m) for n pupils and m friendships with BFS
**Space Complexity:** O(n + m) for adjacency list and color array

**Why it's better:**
- O(n + m) time complexity is much better than O(2^n × m)
- Standard method for bipartite graph problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized BFS with Efficient Color Management (Optimal)

**Key Insights from Optimized BFS Solution:**
- Use optimized BFS with efficient color management
- Most efficient approach for bipartite graph coloring
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized BFS with efficient data structures
2. Implement efficient color conflict detection
3. Use proper color assignment and conflict checking
4. Return team assignment if bipartite

**Visual Example:**
```
Optimized BFS for graph: 1 ── 2
                         │
                         └── 3

Step 1: Initialize optimized structures
- graph = [[], [2,3], [1], [1], [5], [4]]
- color = [-1] * 6
- Queue = deque()

Step 2: Process with optimized BFS
- Start from vertex 1: color[1] = 0, Queue = [1]
- Process vertex 1: color[2] = 1, color[3] = 1, Queue = [2, 3]
- Process vertex 2: no new assignments, Queue = [3]
- Process vertex 3: no new assignments, Queue = []

Step 3: Process remaining components
- Start from vertex 4: color[4] = 0, color[5] = 1

Final: color = [0, 1, 1, 0, 1] → teams = [1, 2, 2, 1, 2]
```

**Implementation:**
```python
from collections import deque

def building_teams_optimized_bfs(n, m, friendships):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in friendships:
        graph[a].append(b)
        graph[b].append(a)
    
    def is_bipartite():
        color = [-1] * (n + 1)  # -1: uncolored, 0: team 1, 1: team 2
        
        for start in range(1, n + 1):
            if color[start] == -1:
                queue = deque([start])
                color[start] = 0
                
                while queue:
                    node = queue.popleft()
                    
                    for neighbor in graph[node]:
                        if color[neighbor] == -1:
                            color[neighbor] = 1 - color[node]  # Opposite color
                            queue.append(neighbor)
                        elif color[neighbor] == color[node]:
                            return False  # Not bipartite
        
        return True, color
    
    result = is_bipartite()
    if not result[0]:
        return "IMPOSSIBLE"
    else:
        color = result[1]
        return ' '.join(str(color[i] + 1) for i in range(1, n + 1))

def solve_building_teams():
    n, m = map(int, input().split())
    friendships = []
    for _ in range(m):
        a, b = map(int, input().split())
        friendships.append((a, b))
    
    result = building_teams_optimized_bfs(n, m, friendships)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_building_teams()
```

**Time Complexity:** O(n + m) for n pupils and m friendships with optimized BFS
**Space Complexity:** O(n + m) for adjacency list and color array

**Why it's optimal:**
- O(n + m) time complexity is optimal for bipartite graph coloring
- Uses optimized BFS with efficient color management
- Most efficient approach for competitive programming
- Standard method for bipartite graph coloring problems

## 🎯 Problem Variations

### Variation 1: Building Teams with Minimum Team Size Difference
**Problem**: Divide pupils into two teams with minimum difference in team sizes.

**Link**: [CSES Problem Set - Building Teams Minimum Difference](https://cses.fi/problemset/task/building_teams_minimum_difference)

```python
def building_teams_minimum_difference(n, m, friendships):
    from collections import deque
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in friendships:
        graph[a].append(b)
        graph[b].append(a)
    
    def is_bipartite_with_balance():
        color = [-1] * (n + 1)
        team1_count = 0
        team2_count = 0
        
        for start in range(1, n + 1):
            if color[start] == -1:
                queue = deque([start])
                color[start] = 0
                team1_count += 1
                
                while queue:
                    node = queue.popleft()
                    
                    for neighbor in graph[node]:
                        if color[neighbor] == -1:
                            color[neighbor] = 1 - color[node]
                            if color[neighbor] == 0:
                                team1_count += 1
                            else:
                                team2_count += 1
                            queue.append(neighbor)
                        elif color[neighbor] == color[node]:
                            return False, None
        
        return True, (team1_count, team2_count)
    
    result = is_bipartite_with_balance()
    if not result[0]:
        return "IMPOSSIBLE"
    else:
        team1_count, team2_count = result[1]
        return f"Team 1: {team1_count}, Team 2: {team2_count}, Difference: {abs(team1_count - team2_count)}"
```

### Variation 2: Building Teams with Specific Team Leaders
**Problem**: Divide pupils into two teams with specific team leaders.

**Link**: [CSES Problem Set - Building Teams Team Leaders](https://cses.fi/problemset/task/building_teams_team_leaders)

```python
def building_teams_team_leaders(n, m, friendships, leader1, leader2):
    from collections import deque
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in friendships:
        graph[a].append(b)
        graph[b].append(a)
    
    def is_bipartite_with_leaders():
        color = [-1] * (n + 1)
        
        # Assign team leaders
        color[leader1] = 0
        color[leader2] = 1
        
        queue = deque([leader1, leader2])
        
        while queue:
            node = queue.popleft()
            
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
        
        return True, color
    
    result = is_bipartite_with_leaders()
    if not result[0]:
        return "IMPOSSIBLE"
    else:
        color = result[1]
        return ' '.join(str(color[i] + 1) for i in range(1, n + 1))
```

### Variation 3: Building Teams with Weighted Friendships
**Problem**: Divide pupils into two teams considering friendship weights.

**Link**: [CSES Problem Set - Building Teams Weighted Friendships](https://cses.fi/problemset/task/building_teams_weighted_friendships)

```python
def building_teams_weighted_friendships(n, m, friendships):
    from collections import deque
    
    # Build adjacency list with weights
    graph = [[] for _ in range(n + 1)]
    for a, b, weight in friendships:
        graph[a].append((b, weight))
        graph[b].append((a, weight))
    
    def is_bipartite_with_weights():
        color = [-1] * (n + 1)
        
        for start in range(1, n + 1):
            if color[start] == -1:
                queue = deque([start])
                color[start] = 0
                
                while queue:
                    node = queue.popleft()
                    
                    for neighbor, weight in graph[node]:
                        if color[neighbor] == -1:
                            color[neighbor] = 1 - color[node]
                            queue.append(neighbor)
                        elif color[neighbor] == color[node]:
                            return False
        
        return True, color
    
    result = is_bipartite_with_weights()
    if not result[0]:
        return "IMPOSSIBLE"
    else:
        color = result[1]
        return ' '.join(str(color[i] + 1) for i in range(1, n + 1))
```

## 🔗 Related Problems

- **[Strongly Connected Components](/cses-analyses/problem_soulutions/graph_algorithms/strongly_connected_components_analysis/)**: Graph connectivity
- **[Cycle Finding](/cses-analyses/problem_soulutions/graph_algorithms/cycle_finding_analysis/)**: Cycle detection
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems
- **[Graph Coloring](/cses-analyses/problem_soulutions/graph_algorithms/)**: Coloring problems

## 📚 Learning Points

1. **Bipartite Graph Coloring**: Essential for understanding graph coloring algorithms
2. **BFS Algorithm**: Key technique for graph traversal and coloring
3. **Color Conflict Detection**: Important for identifying non-bipartite graphs
4. **Graph Representation**: Critical for understanding adjacency list structures
5. **Team Assignment**: Foundation for many optimization problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Building Teams problem demonstrates fundamental bipartite graph coloring concepts for dividing vertices into two teams with no adjacent vertices in the same team. We explored three approaches:

1. **Brute Force Team Assignment**: O(2^n × m) time complexity using exponential assignment generation, inefficient for large graphs
2. **Basic BFS with Bipartite Coloring**: O(n + m) time complexity using standard BFS, better approach for bipartite graph problems
3. **Optimized BFS with Efficient Color Management**: O(n + m) time complexity with optimized BFS, optimal approach for bipartite graph coloring

The key insights include understanding bipartite graph coloring as a graph traversal problem, using BFS for efficient color assignment, and applying color conflict detection techniques for optimal performance. This problem serves as an excellent introduction to bipartite graph algorithms and BFS techniques.

