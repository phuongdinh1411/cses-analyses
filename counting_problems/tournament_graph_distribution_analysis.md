# CSES Tournament Graph Distribution - Problem Analysis

## Problem Statement
Given n teams, count the number of different tournament graphs where each team plays against every other team exactly once, and the result is a valid tournament (no cycles).

### Input
The first input line has an integer n: the number of teams.

### Output
Print the number of different tournament graphs modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 20

### Example
```
Input:
3

Output:
2
```

## Solution Progression

### Approach 1: Generate All Tournaments - O(n!)
**Description**: Generate all possible tournament graphs and count valid ones.

```python
def tournament_graph_distribution_naive(n):
    MOD = 10**9 + 7
    from itertools import permutations
    
    def is_valid_tournament(edges):
        # Check for cycles using DFS
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
        
        visited = [False] * n
        rec_stack = [False] * n
        
        def has_cycle(node):
            visited[node] = True
            rec_stack[node] = True
            
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    if has_cycle(neighbor):
                        return True
                elif rec_stack[neighbor]:
                    return True
            
            rec_stack[node] = False
            return False
        
        for i in range(n):
            if not visited[i]:
                if has_cycle(i):
                    return False
        
        return True
    
    # Generate all possible edge orientations
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((i, j))
    
    count = 0
    # Try all possible orientations
    for orientation in range(2 ** len(edges)):
        tournament_edges = []
        for i, (u, v) in enumerate(edges):
            if orientation & (1 << i):
                tournament_edges.append((u, v))
            else:
                tournament_edges.append((v, u))
        
        if is_valid_tournament(tournament_edges):
            count = (count + 1) % MOD
    
    return count
```

**Why this is inefficient**: O(n!) complexity is too slow for large n.

### Improvement 1: Dynamic Programming - O(n²)
**Description**: Use DP to count valid tournament graphs.

```python
def tournament_graph_distribution_dp(n):
    MOD = 10**9 + 7
    
    # dp[i] = number of valid tournaments with i teams
    dp = [0] * (n + 1)
    
    # Base case
    dp[1] = 1
    
    # Fill DP table
    for i in range(2, n + 1):
        # For i teams, we can have any subset of i-1 teams as winners
        # and the remaining team as loser
        dp[i] = (dp[i-1] * i) % MOD
    
    return dp[n]
```

**Why this improvement works**: Uses mathematical formula for tournament counting.

### Approach 2: Mathematical Formula - O(n)
**Description**: Use mathematical formula for tournament counting.

```python
def tournament_graph_distribution_mathematical(n):
    MOD = 10**9 + 7
    
    if n == 1:
        return 1
    
    # Formula: n! / 2^(n*(n-1)/2)
    # But for valid tournaments, it's just n!
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % MOD
    
    return result
```

**Why this improvement works**: Mathematical formula gives optimal solution.

## Final Optimal Solution

```python
n = int(input())

def count_tournament_graphs(n):
    MOD = 10**9 + 7
    
    if n == 1:
        return 1
    
    # Number of valid tournaments = n!
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % MOD
    
    return result

result = count_tournament_graphs(n)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Generate All Tournaments | O(n!) | O(n²) | Simple but factorial |
| Dynamic Programming | O(n²) | O(n) | DP approach |
| Mathematical Formula | O(n) | O(1) | Optimal solution |

## Key Insights for Other Problems

### 1. **Tournament Graph Properties**
**Principle**: Valid tournaments have no cycles and represent a total ordering.
**Applicable to**: Graph theory problems, tournament problems, ordering problems

### 2. **Mathematical Counting**
**Principle**: The number of valid tournaments with n teams is n!.
**Applicable to**: Combinatorics problems, counting problems, factorial problems

### 3. **Cycle Detection**
**Principle**: Valid tournaments must be acyclic (no cycles).
**Applicable to**: Graph validation problems, cycle detection problems

## Notable Techniques

### 1. **Tournament Counting**
```python
def count_tournaments(n, MOD):
    if n == 1:
        return 1
    
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % MOD
    
    return result
```

### 2. **Cycle Detection**
```python
def has_cycle(adj, n):
    visited = [False] * n
    rec_stack = [False] * n
    
    def dfs(node):
        visited[node] = True
        rec_stack[node] = True
        
        for neighbor in adj[node]:
            if not visited[neighbor]:
                if dfs(neighbor):
                    return True
            elif rec_stack[neighbor]:
                return True
        
        rec_stack[node] = False
        return False
    
    for i in range(n):
        if not visited[i]:
            if dfs(i):
                return True
    
    return False
```

### 3. **Tournament Validation**
```python
def is_valid_tournament(edges, n):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    return not has_cycle(adj, n)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a tournament graph counting problem
2. **Choose approach**: Use mathematical formula
3. **Handle base case**: n = 1 case
4. **Apply formula**: Number of valid tournaments = n!
5. **Use modular arithmetic**: Handle large numbers
6. **Return result**: Output the count modulo 10^9 + 7

---

*This analysis shows how to efficiently count valid tournament graphs using mathematical formulas.* 