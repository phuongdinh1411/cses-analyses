---
layout: simple
title: "Course Schedule II
permalink: /problem_soulutions/advanced_graph_problems/course_schedule_ii_analysis/"
---


# Course Schedule II

## Problem Statement
Given n courses and m prerequisites, find a valid order to take all courses. Each prerequisite is a pair (a,b) meaning course a must be taken before course b.

### Input
The first input line has two integers n and m: the number of courses and prerequisites.
Then there are m lines describing the prerequisites. Each line has two integers a and b: course a must be taken before course b.

### Output"
Print a valid order to take all courses, or "IMPOSSIBLE" if no valid order exists.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 3
1 2
2 3
3 4

Output:
1 2 3 4
```

## Solution Progression

### Approach 1: Topological Sort with DFS - O(n + m)
**Description**: Use topological sort with DFS to find a valid course order.

```python
def course_schedule_ii_naive(n, m, prerequisites):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in prerequisites:
        adj[a].append(b)
    
    # Topological sort using DFS
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    order = []
    
    def dfs(node):
        if in_stack[node]:
            return False  # Cycle detected
        if visited[node]:
            return True
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if not dfs(neighbor):
                return False
        
        in_stack[node] = False
        order.append(node)
        return True
    
    # Try to visit all nodes
    for i in range(1, n + 1):
        if not visited[i]:
            if not dfs(i):
                return "IMPOSSIBLE"
    
    # Reverse order to get topological sort
    return order[::-1]
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Kahn's Algorithm - O(n + m)
**Description**: Use Kahn's algorithm (BFS-based topological sort) for better efficiency.

```python
def course_schedule_ii_kahn(n, m, prerequisites):
    # Build adjacency list and in-degree
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in prerequisites:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    # Add all nodes with in-degree 0
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        # Remove edges from this node
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed
    if len(order) != n:
        return "IMPOSSIBLE"
    
    return order
```

**Why this improvement works**: Kahn's algorithm is more efficient and easier to understand than DFS-based topological sort.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
prerequisites = []
for _ in range(m):
    a, b = map(int, input().split())
    prerequisites.append((a, b))

def find_course_order(n, m, prerequisites):
    # Build adjacency list and in-degree
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in prerequisites:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm
    queue = deque()
    
    # Add all nodes with in-degree 0
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        # Remove edges from this node
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed
    if len(order) != n:
        return "IMPOSSIBLE"
    
    return order

result = find_course_order(n, m, prerequisites)
if result == "IMPOSSIBLE":
    print(result)
else:
    print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS Topological Sort | O(n + m) | O(n) | Cycle detection with DFS |
| Kahn's Algorithm | O(n + m) | O(n) | BFS-based topological sort |

## Key Insights for Other Problems

### 1. **Topological Sort Properties**
**Principle**: Topological sort orders nodes so that all edges point forward, possible only in DAGs.
**Applicable to**: Dependency problems, scheduling problems, DAG problems

### 2. **Kahn's Algorithm**
**Principle**: Use BFS to iteratively remove nodes with no incoming edges.
**Applicable to**: Topological sort problems, dependency resolution, graph problems

### 3. **Cycle Detection**
**Principle**: Topological sort is impossible if the graph contains cycles.
**Applicable to**: Cycle detection problems, dependency problems, graph problems

## Notable Techniques

### 1. **Kahn's Algorithm Implementation**
```python
def kahn_algorithm(n, adj):
    from collections import deque
    
    # Calculate in-degrees
    in_degree = [0] * (n + 1)
    for i in range(1, n + 1):
        for neighbor in adj[i]:
            in_degree[neighbor] += 1
    
    # Initialize queue with nodes having in-degree 0
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Process nodes
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return order
```

### 2. **DFS Topological Sort**
```python
def dfs_topological_sort(n, adj):
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    order = []
    
    def dfs(node):
        if in_stack[node]:
            return False  # Cycle detected
        if visited[node]:
            return True
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if not dfs(neighbor):
                return False
        
        in_stack[node] = False
        order.append(node)
        return True
    
    for i in range(1, n + 1):
        if not visited[i]:
            if not dfs(i):
                return None  # Cycle detected
    
    return order[::-1]
```

### 3. **Cycle Detection**
```python
def has_cycle(n, adj):
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    
    def dfs(node):
        if in_stack[node]:
            return True  # Cycle detected
        if visited[node]:
            return False
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if dfs(neighbor):
                return True
        
        in_stack[node] = False
        return False
    
    for i in range(1, n + 1):
        if not visited[i]:
            if dfs(i):
                return True
    
    return False
```

## Problem-Solving Framework

1. **Identify problem type**: This is a topological sort problem with dependency constraints
2. **Choose approach**: Use Kahn's algorithm for efficient topological sort
3. **Initialize data structure**: Build adjacency list and calculate in-degrees
4. **Find starting nodes**: Add all nodes with in-degree 0 to queue
5. **Process nodes**: Remove nodes and update in-degrees of neighbors
6. **Check completion**: Verify all nodes were processed
7. **Return result**: Output topological order or "IMPOSSIBLE"

---

*This analysis shows how to efficiently solve course scheduling using Kahn's algorithm for topological sort.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Course Schedule II with Costs**
**Variation**: Each course has a cost, find minimum cost schedule.
**Approach**: Use weighted topological sort with cost optimization.
```python
def cost_based_course_schedule_ii(n, m, prerequisites, course_costs):
    # course_costs[i] = cost of taking course i
    
    # Build adjacency list and in-degree
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in prerequisites:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm with cost tracking
    from collections import deque
    queue = deque()
    
    # Add all nodes with in-degree 0
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    order = []
    total_cost = 0
    
    while queue:
        # Sort by cost to prioritize cheaper courses
        queue = deque(sorted(queue, key=lambda x: course_costs[x]))
        node = queue.popleft()
        
        order.append(node)
        total_cost += course_costs[node]
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != n:
        return "IMPOSSIBLE", float('inf')
    
    return order, total_cost
```

#### 2. **Course Schedule II with Constraints**
**Variation**: Limited budget, restricted courses, or specific scheduling requirements.
**Approach**: Use constraint satisfaction with topological sort.
```python
def constrained_course_schedule_ii(n, m, prerequisites, budget, restricted_courses):
    # budget = maximum cost allowed
    # restricted_courses = set of courses that cannot be taken
    
    # Build adjacency list and in-degree
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in prerequisites:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm with constraints
    from collections import deque
    queue = deque()
    
    # Add all nodes with in-degree 0 (excluding restricted)
    for i in range(1, n + 1):
        if in_degree[i] == 0 and i not in restricted_courses:
            queue.append(i)
    
    order = []
    total_cost = 0
    
    while queue:
        node = queue.popleft()
        
        if total_cost + 1 > budget:  # Assuming unit cost
            break
        
        order.append(node)
        total_cost += 1
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0 and neighbor not in restricted_courses:
                queue.append(neighbor)
    
    if len(order) != n:
        return "IMPOSSIBLE", total_cost
    
    return order, total_cost
```

#### 3. **Course Schedule II with Probabilities**
**Variation**: Each course has a probability of being available.
**Approach**: Use Monte Carlo simulation or expected value calculation.
```python
def probabilistic_course_schedule_ii(n, m, prerequisites, availability_probabilities):
    # availability_probabilities[i] = probability course i is available
    
    def monte_carlo_simulation(trials=1000):
        successful_schedules = []
        
        for _ in range(trials):
            # Simulate course availability
            available_courses = set()
            for i in range(1, n + 1):
                if random.random() < availability_probabilities.get(i, 0.8):
                    available_courses.add(i)
            
            # Try to schedule available courses
            schedule = schedule_available_courses(n, m, prerequisites, available_courses)
            if schedule != "IMPOSSIBLE":
                successful_schedules.append(schedule)
        
        return successful_schedules
    
    def schedule_available_courses(n, m, prerequisites, available_courses):
        # Build adjacency list and in-degree for available courses
        adj = [[] for _ in range(n + 1)]
        in_degree = [0] * (n + 1)
        
        for a, b in prerequisites:
            if a in available_courses and b in available_courses:
                adj[a].append(b)
                in_degree[b] += 1
        
        # Kahn's algorithm
        from collections import deque
        queue = deque()
        
        for i in available_courses:
            if in_degree[i] == 0:
                queue.append(i)
        
        order = []
        
        while queue:
            node = queue.popleft()
            order.append(node)
            
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(order) != len(available_courses):
            return "IMPOSSIBLE"
        
        return order
    
    return monte_carlo_simulation()
```

#### 4. **Course Schedule II with Multiple Criteria**
**Variation**: Optimize for multiple objectives (cost, time, difficulty).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_course_schedule_ii(n, m, prerequisites, criteria_weights):
    # criteria_weights = {'cost': 0.4, 'time': 0.3, 'difficulty': 0.3}
    # Each course has multiple attributes
    
    def calculate_course_score(course_attributes):
        return (criteria_weights['cost'] * course_attributes['cost'] + 
                criteria_weights['time'] * course_attributes['time'] + 
                criteria_weights['difficulty'] * course_attributes['difficulty'])
    
    # Build adjacency list and in-degree
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in prerequisites:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm with multi-criteria selection
    from collections import deque
    queue = deque()
    
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    order = []
    total_score = 0
    
    while queue:
        # Sort by multi-criteria score
        queue = deque(sorted(queue, key=lambda x: calculate_course_score({
            'cost': 1, 'time': 1, 'difficulty': 1  # Simplified attributes
        })))
        
        node = queue.popleft()
        order.append(node)
        total_score += calculate_course_score({
            'cost': 1, 'time': 1, 'difficulty': 1
        })
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != n:
        return "IMPOSSIBLE", float('inf')
    
    return order, total_score
```

#### 5. **Course Schedule II with Dynamic Updates**
**Variation**: Prerequisites can be added or removed dynamically.
**Approach**: Use dynamic graph algorithms or incremental updates.
```python
class DynamicCourseScheduleII:
    def __init__(self, n):
        self.n = n
        self.prerequisites = []
        self.adj = [[] for _ in range(n + 1)]
        self.in_degree = [0] * (n + 1)
        self.order_cache = None
    
    def add_prerequisite(self, a, b):
        self.prerequisites.append((a, b))
        self.adj[a].append(b)
        self.in_degree[b] += 1
        self.invalidate_cache()
    
    def remove_prerequisite(self, a, b):
        if (a, b) in self.prerequisites:
            self.prerequisites.remove((a, b))
            self.adj[a].remove(b)
            self.in_degree[b] -= 1
            self.invalidate_cache()
    
    def invalidate_cache(self):
        self.order_cache = None
    
    def get_schedule(self):
        if self.order_cache is None:
            self.order_cache = self.compute_schedule()
        return self.order_cache
    
    def compute_schedule(self):
        # Kahn's algorithm
        from collections import deque
        queue = deque()
        
        # Add all nodes with in-degree 0
        for i in range(1, self.n + 1):
            if self.in_degree[i] == 0:
                queue.append(i)
        
        order = []
        
        while queue:
            node = queue.popleft()
            order.append(node)
            
            for neighbor in self.adj[node]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(order) != self.n:
            return "IMPOSSIBLE"
        
        return order
    
    def has_cycle(self):
        # Check if adding any prerequisite creates a cycle
        visited = [False] * (self.n + 1)
        in_stack = [False] * (self.n + 1)
        
        def dfs(node):
            if in_stack[node]:
                return True  # Cycle detected
            if visited[node]:
                return False
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor in self.adj[node]:
                if dfs(neighbor):
                    return True
            
            in_stack[node] = False
            return False
        
        for i in range(1, self.n + 1):
            if not visited[i]:
                if dfs(i):
                    return True
        
        return False
```

### Related Problems & Concepts

#### 1. **Topological Sort Problems**
- **Course Schedule I**: Check if valid schedule exists
- **Alien Dictionary**: Order characters from alien language
- **Build Order**: Construction project dependencies
- **Task Scheduling**: Job dependencies and ordering

#### 2. **Graph Algorithms**
- **Depth-First Search**: Recursive exploration
- **Breadth-First Search**: Level-by-level traversal
- **Cycle Detection**: Detecting cycles in directed graphs
- **Strongly Connected Components**: Tarjan's, Kosaraju's

#### 3. **Dependency Problems**
- **Package Management**: Software dependencies
- **Build Systems**: Compilation order
- **Workflow Management**: Task dependencies
- **Resource Allocation**: Resource constraints

#### 4. **Scheduling Problems**
- **Job Scheduling**: Task ordering with constraints
- **Project Planning**: Critical path analysis
- **Event Planning**: Event dependencies
- **Academic Planning**: Course prerequisites

#### 5. **Dynamic Graph Problems**
- **Incremental Topological Sort**: Adding edges
- **Decremental Topological Sort**: Removing edges
- **Fully Dynamic**: Both adding and removing
- **Online Algorithms**: Real-time updates

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large graphs
- **Edge Cases**: Robust cycle detection

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient graph traversal
- **Sliding Window**: Optimal subgraph problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Combinatorics**
- **Permutation Counting**: Valid orderings
- **Combination Problems**: Course selections
- **Catalan Numbers**: Valid dependency sequences
- **Stirling Numbers**: Partitioning courses

#### 2. **Probability Theory**
- **Expected Values**: Average completion time
- **Markov Chains**: State transitions
- **Random Graphs**: Erdős-Rényi model
- **Monte Carlo**: Simulation methods

#### 3. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special graph cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime courses

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Course schedule problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Graph Problems**: Topological sort, cycle detection
- **Scheduling Problems**: Course planning, job scheduling
- **Dynamic Problems**: Incremental, decremental
- **Dependency Problems**: Package management, build systems 