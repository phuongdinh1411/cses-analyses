# CSES Building Teams - Problem Analysis

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