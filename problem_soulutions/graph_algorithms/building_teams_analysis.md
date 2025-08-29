---
layout: simple
title: "Building Teams"
permalink: /problem_soulutions/graph_algorithms/building_teams_analysis
---


# Building Teams

## Problem Statement
There are n pupils in Uolevi's class, and m friendships between them. Your task is to divide the pupils into two teams in such a way that no two pupils in a team are friends. You can freely choose the sizes of the teams.

### Input
The first input line has two integers n and m: the number of pupils and friendships. The pupils are numbered 1,2,…,n.
Then, there are m lines describing the friendships. Each line has two integers a and b: pupils a and b are friends.

### Output
Print "IMPOSSIBLE" if this is not possible, and otherwise print the team assignment.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5

### Example
```
Input:
5 3
1 2
1 3
4 5

Output:
1 2 2 1 1
```

## Solution Progression

### Approach 1: BFS with Bipartition - O(n + m)
**Description**: Use breadth-first search to check if the graph is bipartite and assign teams.

```python
from collections import deque

def building_teams_bfs(n, m, friendships):
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

**Why this is efficient**: We visit each node and edge at most once, giving us O(n + m) complexity.

### Improvement 1: DFS with Bipartition - O(n + m)
**Description**: Use depth-first search for bipartition checking.

```python
def building_teams_dfs(n, m, friendships):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in friendships:
        graph[a].append(b)
        graph[b].append(a)
    
    def is_bipartite_dfs():
        color = [-1] * (n + 1)
        
        def dfs(node, current_color):
            color[node] = current_color
            
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    if not dfs(neighbor, 1 - current_color):
                        return False
                elif color[neighbor] == current_color:
                    return False
            return True
        
        for start in range(1, n + 1):
            if color[start] == -1:
                if not dfs(start, 0):
                    return False, None
        
        return True, color
    
    result = is_bipartite_dfs()
    if not result[0]:
        return "IMPOSSIBLE"
    else:
        color = result[1]
        return ' '.join(str(color[i] + 1) for i in range(1, n + 1))
```

**Why this improvement works**: DFS can be more memory-efficient and is often simpler to implement.

### Improvement 2: Union-Find with Bipartition - O(n + m * α(n))
**Description**: Use union-find with additional tracking for bipartition.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)
        self.opposite = [-1] * (n + 1)  # Track opposite team
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return True  # Same component
        
        # Union x and y's opposite
        if self.opposite[px] != -1 and self.opposite[py] != -1:
            ox, oy = self.find(self.opposite[px]), self.find(self.opposite[py])
            if ox == oy:
                return False  # Conflict
            if self.rank[ox] < self.rank[oy]:
                ox, oy = oy, ox
            self.parent[oy] = ox
            if self.rank[ox] == self.rank[oy]:
                self.rank[ox] += 1
        
        # Set opposites
        if self.opposite[px] == -1:
            self.opposite[px] = py
        if self.opposite[py] == -1:
            self.opposite[py] = px
        
        return True

def building_teams_union_find(n, m, friendships):
    uf = UnionFind(n)
    
    for a, b in friendships:
        if not uf.union(a, b):
            return "IMPOSSIBLE"
    
    # Assign teams
    color = [-1] * (n + 1)
    for i in range(1, n + 1):
        if color[i] == -1:
            color[i] = 0
            opposite = uf.opposite[uf.find(i)]
            if opposite != -1:
                color[opposite] = 1
    
    return ' '.join(str(color[i] + 1) for i in range(1, n + 1))
```

**Why this improvement works**: Union-find can handle dynamic connectivity changes and is very efficient.

### Alternative: Two-Color BFS - O(n + m)
**Description**: Use a simplified two-color BFS approach.

```python
from collections import deque

def building_teams_two_color(n, m, friendships):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in friendships:
        graph[a].append(b)
        graph[b].append(a)
    
    def two_color_bfs():
        team = [0] * (n + 1)  # 0: unassigned, 1: team 1, 2: team 2
        
        for start in range(1, n + 1):
            if team[start] == 0:
                queue = deque([start])
                team[start] = 1
                
                while queue:
                    node = queue.popleft()
                    current_team = team[node]
                    opposite_team = 3 - current_team  # 1->2, 2->1
                    
                    for neighbor in graph[node]:
                        if team[neighbor] == 0:
                            team[neighbor] = opposite_team
                            queue.append(neighbor)
                        elif team[neighbor] == current_team:
                            return False  # Conflict
        
        return True, team
    
    result = two_color_bfs()
    if not result[0]:
        return "IMPOSSIBLE"
    else:
        team = result[1]
        return ' '.join(str(team[i]) for i in range(1, n + 1))
```

**Why this works**: This approach directly assigns team numbers (1 and 2) and is very intuitive.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
friendships = [tuple(map(int, input().split())) for _ in range(m)]

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
    print("IMPOSSIBLE")
else:
    color = result[1]
    print(' '.join(str(color[i] + 1) for i in range(1, n + 1)))
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| BFS Bipartition | O(n + m) | O(n + m) | Check bipartiteness |
| DFS Bipartition | O(n + m) | O(n) | Recursive approach |
| Union-Find | O(n + m * α(n)) | O(n) | Dynamic connectivity |
| Two-Color BFS | O(n + m) | O(n + m) | Direct team assignment |

## Key Insights for Other Problems

### 1. **Bipartite Graph Detection**
**Principle**: Use graph coloring to detect if a graph is bipartite (can be divided into two independent sets).
**Applicable to**:
- Bipartite graphs
- Graph coloring
- Team assignment
- Graph theory

**Example Problems**:
- Bipartite graphs
- Graph coloring
- Team assignment
- Graph theory

### 2. **Graph Coloring**
**Principle**: Use graph traversal to assign colors/teams to nodes while maintaining constraints.
**Applicable to**:
- Graph coloring
- Constraint satisfaction
- Assignment problems
- Algorithm design

**Example Problems**:
- Graph coloring
- Constraint satisfaction
- Assignment problems
- Algorithm design

### 3. **Conflict Detection**
**Principle**: Detect conflicts when adjacent nodes are assigned the same color/team.
**Applicable to**:
- Conflict detection
- Constraint checking
- Validation problems
- Algorithm design

**Example Problems**:
- Conflict detection
- Constraint checking
- Validation problems
- Algorithm design

### 4. **Independent Sets**
**Principle**: Find independent sets in graphs where no two nodes in the same set are adjacent.
**Applicable to**:
- Independent sets
- Graph theory
- Optimization problems
- Algorithm design

**Example Problems**:
- Independent sets
- Graph theory
- Optimization problems
- Algorithm design

## Notable Techniques

### 1. **Bipartite Detection Pattern**
```python
def is_bipartite(graph, n):
    color = [-1] * (n + 1)
    for start in range(1, n + 1):
        if color[start] == -1:
            if not bfs_color(start, graph, color):
                return False
    return True
```

### 2. **Two-Color Assignment**
```python
def bfs_color(start, graph, color):
    queue = deque([start])
    color[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if color[neighbor] == -1:
                color[neighbor] = 1 - color[node]
                queue.append(neighbor)
            elif color[neighbor] == color[node]:
                return False
    return True
```

### 3. **Conflict Detection**
```python
def has_conflict(graph, color, node):
    for neighbor in graph[node]:
        if color[neighbor] == color[node]:
            return True
    return False
```

## Edge Cases to Remember

1. **No friendships**: Any assignment works
2. **All pupils are friends**: Impossible to assign teams
3. **Single pupil**: Can be assigned to either team
4. **Large graph**: Use efficient algorithm
5. **Disconnected components**: Handle each component separately

## Problem-Solving Framework

1. **Identify bipartite nature**: This is a bipartite graph detection problem
2. **Choose algorithm**: Use BFS or DFS for bipartition
3. **Assign colors**: Use two colors (teams) for nodes
4. **Check conflicts**: Ensure no adjacent nodes have same color
5. **Handle output**: Print team assignments or "IMPOSSIBLE"

---

*This analysis shows how to efficiently solve bipartite graph detection and team assignment problems using graph coloring algorithms.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Building Teams with Costs**
**Problem**: Each team assignment has a cost, find minimum cost team assignment.
```python
def cost_based_building_teams(n, m, edges, costs):
    # costs[(a, b)] = cost of assigning different teams to a and b
    
    # Build adjacency list with costs
    graph = [[] for _ in range(n + 1)]
    for a, b in edges:
        cost = costs.get((a, b), 1)
        graph[a].append((b, cost))
        graph[b].append((a, cost))
    
    # Check if bipartite first
    color = [-1] * (n + 1)
    
    def bfs_color(start):
        queue = deque([start])
        color[start] = 0
        total_cost = 0
        
        while queue:
            node = queue.popleft()
            for neighbor, cost in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    total_cost += cost
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False, 0
        return True, total_cost
    
    total_cost = 0
    for start in range(1, n + 1):
        if color[start] == -1:
            success, component_cost = bfs_color(start)
            if not success:
                return False, None, float('inf')
            total_cost += component_cost
    
    return True, color, total_cost
```

#### **Variation 2: Building Teams with Constraints**
**Problem**: Find team assignment with constraints on team sizes or preferences.
```python
def constrained_building_teams(n, m, edges, constraints):
    # constraints = {'max_team1': x, 'max_team2': y, 'preferences': {node: team}}
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    # Check if bipartite first
    color = [-1] * (n + 1)
    
    def bfs_color(start):
        queue = deque([start])
        color[start] = 0
        
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
        return True
    
    # Check bipartiteness
    for start in range(1, n + 1):
        if color[start] == -1:
            if not bfs_color(start):
                return False, None
    
    # Apply constraints
    team1_count = sum(1 for c in color[1:] if c == 0)
    team2_count = sum(1 for c in color[1:] if c == 1)
    
    # Check team size constraints
    if 'max_team1' in constraints and team1_count > constraints['max_team1']:
        return False, None
    if 'max_team2' in constraints and team2_count > constraints['max_team2']:
        return False, None
    
    # Apply preferences
    preferences = constraints.get('preferences', {})
    for node, preferred_team in preferences.items():
        if color[node] != preferred_team:
            # Try to swap if possible
            # (Simplified - would need more complex logic)
            pass
    
    return True, color
```

#### **Variation 3: Building Teams with Probabilities**
**Problem**: Each edge has a probability of conflict, find expected team assignment.
```python
def probabilistic_building_teams(n, m, edges, probabilities):
    # probabilities[(a, b)] = probability of conflict between a and b
    
    # Use Monte Carlo simulation
    import random
    
    def simulate_team_assignment():
        # Randomly sample edges based on probabilities
        conflict_edges = []
        for a, b in edges:
            if random.random() < probabilities.get((a, b), 0.0):
                conflict_edges.append((a, b))
        
        # Build graph with conflict edges
        graph = [[] for _ in range(n + 1)]
        for a, b in conflict_edges:
            graph[a].append(b)
            graph[b].append(a)
        
        # Check bipartiteness
        color = [-1] * (n + 1)
        
        def bfs_color(start):
            queue = deque([start])
            color[start] = 0
            
            while queue:
                node = queue.popleft()
                for neighbor in graph[node]:
                    if color[neighbor] == -1:
                        color[neighbor] = 1 - color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        return False
            return True
        
        for start in range(1, n + 1):
            if color[start] == -1:
                if not bfs_color(start):
                    return False, None
        
        return True, color
    
    # Run multiple simulations
    num_simulations = 1000
    success_count = 0
    total_conflicts = 0
    
    for _ in range(num_simulations):
        success, color = simulate_team_assignment()
        if success:
            success_count += 1
            # Count conflicts
            conflicts = 0
            for a, b in edges:
                if color[a] == color[b]:
                    conflicts += 1
            total_conflicts += conflicts
    
    success_probability = success_count / num_simulations
    expected_conflicts = total_conflicts / num_simulations if success_count > 0 else 0
    
    return success_probability, expected_conflicts
```

#### **Variation 4: Building Teams with Multiple Criteria**
**Problem**: Find team assignment considering multiple criteria (conflicts, preferences, balance).
```python
def multi_criteria_building_teams(n, m, edges, criteria):
    # criteria = {'conflict_weight': x, 'preference_weight': y, 'balance_weight': z}
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    # Check if bipartite first
    color = [-1] * (n + 1)
    
    def bfs_color(start):
        queue = deque([start])
        color[start] = 0
        
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
        return True
    
    # Check bipartiteness
    for start in range(1, n + 1):
        if color[start] == -1:
            if not bfs_color(start):
                return False, None, float('inf')
    
    # Calculate multi-criteria score
    team1_count = sum(1 for c in color[1:] if c == 0)
    team2_count = sum(1 for c in color[1:] if c == 1)
    
    # Conflict score (should be 0 for valid assignment)
    conflict_score = 0
    for a, b in edges:
        if color[a] == color[b]:
            conflict_score += 1
    
    # Preference score
    preference_score = 0
    preferences = criteria.get('preferences', {})
    for node, preferred_team in preferences.items():
        if color[node] == preferred_team:
            preference_score += 1
    
    # Balance score
    balance_score = abs(team1_count - team2_count)
    
    # Calculate total score
    total_score = (conflict_score * criteria.get('conflict_weight', 1) + 
                  preference_score * criteria.get('preference_weight', 1) + 
                  balance_score * criteria.get('balance_weight', 1))
    
    return True, color, total_score
```

#### **Variation 5: Building Teams with Dynamic Updates**
**Problem**: Handle dynamic updates to relationships and find team assignment after each update.
```python
def dynamic_building_teams(n, m, initial_edges, updates):
    # updates = [(edge_to_add, edge_to_remove), ...]
    
    edges = initial_edges.copy()
    results = []
    
    for edge_to_add, edge_to_remove in updates:
        # Update edges
        if edge_to_remove in edges:
            edges.remove(edge_to_remove)
        if edge_to_add:
            edges.append(edge_to_add)
        
        # Rebuild graph
        graph = [[] for _ in range(n + 1)]
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        
        # Check bipartiteness
        color = [-1] * (n + 1)
        
        def bfs_color(start):
            queue = deque([start])
            color[start] = 0
            
            while queue:
                node = queue.popleft()
                for neighbor in graph[node]:
                    if color[neighbor] == -1:
                        color[neighbor] = 1 - color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        return False
            return True
        
        success = True
        for start in range(1, n + 1):
            if color[start] == -1:
                if not bfs_color(start):
                    success = False
                    break
        
        results.append((success, color if success else None))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Bipartite Graph Problems**
- **Bipartite Detection**: Detect if a graph is bipartite
- **Bipartite Coloring**: Color bipartite graphs with two colors
- **Bipartite Matching**: Find maximum matching in bipartite graphs
- **Bipartite Partitioning**: Partition graphs into two independent sets

#### **2. Graph Coloring Problems**
- **Two-Color Graphs**: Color graphs with two colors
- **Graph Coloring**: General graph coloring problems
- **Conflict-Free Coloring**: Color graphs without conflicts
- **Proper Coloring**: Proper vertex coloring

#### **3. Team Assignment Problems**
- **Team Formation**: Form teams from individuals
- **Conflict Resolution**: Resolve conflicts in assignments
- **Preference Matching**: Match preferences in assignments
- **Balanced Assignment**: Create balanced team assignments

#### **4. Constraint Satisfaction Problems**
- **Constraint Satisfaction**: Satisfy constraints in assignments
- **Conflict Detection**: Detect conflicts in assignments
- **Preference Handling**: Handle preferences in assignments
- **Validation Problems**: Validate assignment constraints

#### **5. Independent Set Problems**
- **Independent Sets**: Find independent sets in graphs
- **Maximum Independent Set**: Find maximum independent set
- **Independent Set Partitioning**: Partition into independent sets
- **Independent Set Optimization**: Optimize independent sets

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    success, color = build_teams(n, m, edges)
    if success:
        print(' '.join(str(color[i] + 1) for i in range(1, n + 1)))
    else:
        print("IMPOSSIBLE")
```

#### **2. Range Queries on Team Assignments**
```python
def range_team_queries(n, edges, queries):
    # queries = [(start_node, end_node), ...] - find team assignment in range
    
    results = []
    for start, end in queries:
        # Filter edges in range
        range_edges = [(a, b) for a, b in edges if start <= a <= end and start <= b <= end]
        
        success, color = build_teams(end - start + 1, len(range_edges), range_edges)
        results.append((success, color))
    
    return results
```

#### **3. Interactive Team Building Problems**
```python
def interactive_building_teams():
    n = int(input("Enter number of students: "))
    m = int(input("Enter number of relationships: "))
    print("Enter relationships (student1 student2):")
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    success, color = build_teams(n, m, edges)
    if success: print(f"Team 
assignment: {[color[i] + 1 for i in range(1, n + 1)]}")
    else:
        print("IMPOSSIBLE")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Bipartite Graph Theory**: Mathematical theory of bipartite graphs
- **Graph Coloring Theory**: Mathematical theory of graph coloring
- **Independent Set Theory**: Mathematical theory of independent sets
- **Graph Partitioning**: Mathematical graph partitioning

#### **2. Optimization Theory**
- **Assignment Optimization**: Mathematical assignment optimization
- **Conflict Optimization**: Mathematical conflict optimization
- **Preference Optimization**: Mathematical preference optimization
- **Balance Optimization**: Mathematical balance optimization

#### **3. Probability Theory**
- **Probabilistic Assignments**: Probability theory in assignments
- **Expected Conflicts**: Expected conflict calculations
- **Probability Distributions**: Probability distributions in assignments
- **Stochastic Optimization**: Stochastic optimization techniques

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **BFS/DFS**: Graph traversal algorithms
- **Graph Coloring**: Graph coloring algorithms
- **Bipartite Detection**: Bipartite graph detection algorithms
- **Constraint Satisfaction**: Constraint satisfaction algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Optimization Theory**: Mathematical optimization techniques
- **Probability Theory**: Mathematical probability theory
- **Constraint Theory**: Mathematical constraint theory

#### **3. Programming Concepts**
- **Graph Representations**: Efficient graph representations
- **Color Assignment**: Efficient color assignment techniques
- **Conflict Detection**: Efficient conflict detection
- **Validation Algorithms**: Efficient validation algorithms

---

*This analysis demonstrates efficient bipartite graph detection techniques and shows various extensions for team building problems.* 