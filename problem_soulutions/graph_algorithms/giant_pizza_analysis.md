# CSES Giant Pizza - Problem Analysis

## Problem Statement
Given a list of pizza toppings preferences where each person likes some toppings and dislikes others, determine if it's possible to make a pizza that satisfies everyone's preferences.

### Input
The first input line has two integers n and m: the number of people and the number of toppings.
Then there are n lines describing the preferences. Each line has two integers a and b: person likes topping a and dislikes topping b.

### Output
Print "YES" if it's possible to make a pizza that satisfies everyone, or "NO" otherwise.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 10^5
- 1 ≤ a,b ≤ m

### Example
```
Input:
3 3
1 2
2 3
3 1

Output:
YES
```

## Solution Progression

### Approach 1: 2-SAT with Kosaraju's Algorithm - O(n + m)
**Description**: Use 2-SAT problem reduction to strongly connected components.

```python
def giant_pizza_naive(n, m, preferences):
    # Build implication graph for 2-SAT
    # For each preference (a, b): if we choose a, we must not choose b
    # This creates implications: a -> ~b and b -> ~a
    
    # Graph has 2*m nodes: 1 to m for positive, m+1 to 2*m for negative
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        # a -> ~b (if we choose a, we must not choose b)
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        
        # b -> ~a (if we choose b, we must not choose a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Use Kosaraju's algorithm to find SCCs
    visited = [False] * (2*m + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, 2*m + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS to find SCCs
    visited = [False] * (2*m + 1)
    scc_id = [0] * (2*m + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_scc += 1
            second_dfs(node, current_scc)
    
    # Check if any variable and its negation are in the same SCC
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return "NO"
    
    return "YES"
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized 2-SAT Algorithm - O(n + m)
**Description**: Use optimized 2-SAT algorithm with better structure.

```python
def giant_pizza_optimized(n, m, preferences):
    # Build implication graph for 2-SAT
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        # a -> ~b and b -> ~a
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Kosaraju's algorithm
    visited = [False] * (2*m + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, 2*m + 1):
        if not visited[i]:
            first_dfs(i)
    
    visited = [False] * (2*m + 1)
    scc_id = [0] * (2*m + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_scc += 1
            second_dfs(node, current_scc)
    
    # Check 2-SAT satisfiability
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return "NO"
    
    return "YES"
```

**Why this improvement works**: We use 2-SAT problem reduction with optimized Kosaraju's algorithm to check satisfiability efficiently.

## Final Optimal Solution

```python
n, m = map(int, input().split())
preferences = []
for _ in range(n):
    a, b = map(int, input().split())
    preferences.append((a, b))

def check_giant_pizza(n, m, preferences):
    # Build implication graph for 2-SAT
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        # a -> ~b and b -> ~a
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Kosaraju's algorithm
    visited = [False] * (2*m + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, 2*m + 1):
        if not visited[i]:
            first_dfs(i)
    
    visited = [False] * (2*m + 1)
    scc_id = [0] * (2*m + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_scc += 1
            second_dfs(node, current_scc)
    
    # Check 2-SAT satisfiability
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return "NO"
    
    return "YES"

result = check_giant_pizza(n, m, preferences)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| 2-SAT with Kosaraju's | O(n + m) | O(n + m) | Use 2-SAT reduction to SCC |
| Optimized 2-SAT | O(n + m) | O(n + m) | Optimized 2-SAT implementation |

## Key Insights for Other Problems

### 1. **2-SAT Problem**
**Principle**: Reduce 2-SAT to strongly connected components problem.
**Applicable to**: Boolean satisfiability problems, constraint satisfaction problems

### 2. **Implication Graph**
**Principle**: Build directed graph where edges represent logical implications.
**Applicable to**: Logic problems, constraint problems, graph problems

### 3. **SCC for Satisfiability**
**Principle**: Use strongly connected components to check satisfiability.
**Applicable to**: 2-SAT problems, logic problems, constraint problems

## Notable Techniques

### 1. **2-SAT Problem Reduction**
```python
def build_2sat_graph(n, m, preferences):
    # Graph has 2*m nodes: 1 to m for positive, m+1 to 2*m for negative
    adj = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        # a -> ~b and b -> ~a
        adj[a].append(b + m)
        adj[b].append(a + m)
    
    return adj
```

### 2. **2-SAT Satisfiability Check**
```python
def check_2sat_satisfiability(m, scc_id):
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return False
    return True
```

### 3. **Implication Graph Construction**
```python
def build_implication_graph(preferences, m):
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    return adj, adj_rev
```

## Problem-Solving Framework

1. **Identify problem type**: This is a 2-SAT problem
2. **Choose approach**: Use 2-SAT reduction to strongly connected components
3. **Build implication graph**: Create directed graph with logical implications
4. **Find SCCs**: Use Kosaraju's algorithm to find strongly connected components
5. **Check satisfiability**: Verify no variable and its negation are in same SCC
6. **Return result**: Output "YES" if satisfiable, "NO" otherwise

---

*This analysis shows how to efficiently solve 2-SAT problems using strongly connected components.* 