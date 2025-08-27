# CSES Hamiltonian Flights - Problem Analysis

## Problem Statement
Given a directed graph with n cities and m flights, count the number of different Hamiltonian paths from city 1 to city n.

### Input
The first input line has two integers n and m: the number of cities and flights.
Then there are m lines describing the flights. Each line has two integers a and b: there is a flight from city a to city b.

### Output
Print the number of different Hamiltonian paths from city 1 to city n modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 20
- 1 ≤ m ≤ n(n-1)
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 4
1 2
2 3
3 4
1 4

Output:
2
```

## Solution Progression

### Approach 1: Dynamic Programming with Bitmask - O(n * 2^n)
**Description**: Use dynamic programming with bitmask to count Hamiltonian paths.

```python
def hamiltonian_flights_naive(n, m, flights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    # dp[mask][last] = number of paths ending at 'last' with visited cities in 'mask'
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1 << 0][1] = 1  # 1 << 0 = 1, represents city 1 visited
    
    # Iterate through all possible subsets of cities
    for mask in range(1 << n):
        for last in range(1, n + 1):
            # If 'last' city is not in the current mask, skip
            if not (mask & (1 << (last - 1))):
                continue
            
            # If there are paths ending at 'last' with current mask
            if dp[mask][last] > 0:
                # Try to extend path from 'last' to 'next_city'
                for next_city in adj[last]:
                    # If 'next_city' is not yet visited in the current mask
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % (10**9 + 7)
    
    # The answer is the number of paths ending at city n with all cities visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n]
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Bitmask DP - O(n * 2^n)
**Description**: Use optimized dynamic programming with better bitmask handling.

```python
def hamiltonian_flights_optimized(n, m, flights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1][1] = 1
    
    # Iterate through all possible subsets
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    # Return paths ending at city n with all cities visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n]
```

**Why this improvement works**: We use optimized dynamic programming with bitmask to count Hamiltonian paths efficiently.

## Final Optimal Solution

```python
n, m = map(int, input().split())
flights = []
for _ in range(m):
    a, b = map(int, input().split())
    flights.append((a, b))

def count_hamiltonian_flights(n, m, flights):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in flights:
        adj[a].append(b)
    
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    
    # Base case: start at city 1
    dp[1][1] = 1
    
    # Iterate through all possible subsets of cities
    for mask in range(1 << n):
        for last in range(1, n + 1):
            # If 'last' city is not in the current mask, skip
            if not (mask & (1 << (last - 1))):
                continue
            
            # If there are paths ending at 'last' with current mask
            if dp[mask][last] > 0:
                # Try to extend path from 'last' to 'next_city'
                for next_city in adj[last]:
                    # If 'next_city' is not yet visited in the current mask
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    # The answer is the number of paths ending at city n with all cities visited
    full_mask = (1 << n) - 1
    return dp[full_mask][n]

result = count_hamiltonian_flights(n, m, flights)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Bitmask DP | O(n * 2^n) | O(n * 2^n) | Use dynamic programming with bitmask |
| Optimized Bitmask DP | O(n * 2^n) | O(n * 2^n) | Optimized bitmask implementation |

## Key Insights for Other Problems

### 1. **Hamiltonian Path**
**Principle**: Use dynamic programming with bitmask to count Hamiltonian paths.
**Applicable to**: Hamiltonian path problems, path counting problems, graph problems

### 2. **Bitmask Dynamic Programming**
**Principle**: Use bitmask to represent visited states in dynamic programming.
**Applicable to**: State compression problems, path problems, optimization problems

### 3. **Path Counting**
**Principle**: Use dynamic programming to count different paths in graphs.
**Applicable to**: Path counting problems, graph problems, combinatorics problems

## Notable Techniques

### 1. **Bitmask DP for Hamiltonian Path**
```python
def hamiltonian_path_dp(n, adj):
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    dp[1][1] = 1  # Start at city 1
    
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] += dp[mask][last]
    
    return dp[(1 << n) - 1][n]
```

### 2. **Bitmask Operations**
```python
def bitmask_operations(n):
    # Set bit
    mask = 1 << (n - 1)
    
    # Check if bit is set
    is_set = (mask & (1 << (n - 1))) != 0
    
    # Toggle bit
    mask ^= (1 << (n - 1))
    
    # Count set bits
    count = bin(mask).count('1')
    
    return mask, is_set, count
```

### 3. **State Compression**
```python
def state_compression_dp(n, adj):
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(1 << n)]
    dp[1][1] = 1
    
    for mask in range(1 << n):
        for last in range(1, n + 1):
            if not (mask & (1 << (last - 1))):
                continue
            
            if dp[mask][last] > 0:
                for next_city in adj[last]:
                    if not (mask & (1 << (next_city - 1))):
                        new_mask = mask | (1 << (next_city - 1))
                        dp[new_mask][next_city] = (dp[new_mask][next_city] + dp[mask][last]) % MOD
    
    return dp[(1 << n) - 1][n]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a Hamiltonian path counting problem
2. **Choose approach**: Use dynamic programming with bitmask
3. **Build graph**: Create adjacency list representation
4. **Initialize DP**: Set base case for starting city
5. **Iterate states**: Process all possible subsets of cities
6. **Count paths**: Use DP to count different Hamiltonian paths
7. **Return result**: Output count modulo 10^9 + 7

---

*This analysis shows how to efficiently count Hamiltonian paths using dynamic programming with bitmask.* 