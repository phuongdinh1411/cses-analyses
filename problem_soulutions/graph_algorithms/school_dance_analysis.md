# CSES School Dance - Problem Analysis

## Problem Statement
Given n boys and m girls, where each boy can dance with certain girls, find the maximum number of boys and girls that can be matched for dancing.

### Input
The first input line has two integers n and m: the number of boys and girls.
Then there are n lines describing the preferences. The i-th line has k integers: the girls that boy i can dance with.

### Output
Print the maximum number of boys and girls that can be matched.

### Constraints
- 1 ≤ n,m ≤ 500
- 1 ≤ k ≤ m

### Example
```
Input:
3 3
1 2
2 3
1 3

Output:
3
```

## Solution Progression

### Approach 1: Maximum Bipartite Matching - O(n * m * max_flow)
**Description**: Use maximum flow to find maximum bipartite matching.

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

### Improvement 1: Optimized Bipartite Matching - O(n * m * max_flow)
**Description**: Use optimized Ford-Fulkerson algorithm for bipartite matching.

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

## Final Optimal Solution

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

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Bipartite Matching via Max Flow | O(n * m * max_flow) | O((n+m)²) | Use max flow for bipartite matching |
| Optimized Bipartite Matching | O(n * m * max_flow) | O((n+m)²) | Optimized max flow implementation |

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