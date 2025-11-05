---
layout: simple
title: "Grid 2 - AtCoder Educational DP Contest Problem Y"
permalink: /problem_soulutions/dynamic_programming_at/grid_2_analysis
---

# Grid 2 - AtCoder Educational DP Contest Problem Y

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand inclusion-exclusion in DP
- Apply DP to solve grid problems with obstacles
- Handle large number of obstacles
- Use inclusion-exclusion principle

### 📚 **Prerequisites**
- Dynamic Programming, inclusion-exclusion, combinatorics
- Arrays, 2D arrays, modular arithmetic
- Related: Grid paths, inclusion-exclusion

## 📋 Problem Description

Given H×W grid with N obstacles, count paths from (1,1) to (H,W) avoiding obstacles, modulo 10^9+7.

**Input**: 
- First line: H, W, N (1 ≤ H, W ≤ 10^5, 0 ≤ N ≤ 3000)
- Next N lines: obstacle positions (r_i, c_i)

**Output**: 
- Number of paths modulo 10^9+7

**Constraints**:
- 1 ≤ H, W ≤ 10^5
- 0 ≤ N ≤ 3000

## 🔍 Solution Analysis

### Approach: Inclusion-Exclusion DP

**Key Insight**: Use inclusion-exclusion to count paths avoiding obstacles.

**Algorithm**:
1. Sort obstacles by distance from start
2. For each obstacle, count paths that pass through it
3. Use inclusion-exclusion to combine

**DP State Definition**:
- `dp[i]` = number of paths from start to obstacle i that don't pass through other obstacles
- Use inclusion-exclusion: subtract paths through previous obstacles

**Implementation**:
```python
def grid_2_paths(h, w, n, obstacles):
    """
    Inclusion-exclusion DP for Grid 2 problem
    
    Args:
        h: grid height
        w: grid width
        n: number of obstacles
        obstacles: list of (r, c) tuples
    
    Returns:
        int: number of paths modulo 10^9+7
    """
    MOD = 10**9 + 7
    
    # Precompute factorials and inverse factorials
    max_n = h + w
    fact = [1] * (max_n + 1)
    inv_fact = [1] * (max_n + 1)
    
    for i in range(1, max_n + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    inv_fact[max_n] = pow(fact[max_n], MOD-2, MOD)
    for i in range(max_n, 0, -1):
        inv_fact[i-1] = (inv_fact[i] * i) % MOD
    
    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        return (fact[n] * inv_fact[r] % MOD * inv_fact[n-r]) % MOD
    
    def paths(r1, c1, r2, c2):
        """Paths from (r1,c1) to (r2,c2)"""
        dr = r2 - r1
        dc = c2 - c1
        if dr < 0 or dc < 0:
            return 0
        return nCr(dr + dc, dr)
    
    # Sort obstacles by distance from start
    obstacles = [(r-1, c-1) for r, c in obstacles]
    obstacles.sort(key=lambda x: x[0] + x[1])
    obstacles.append((h-1, w-1))  # Add destination
    
    # dp[i] = paths to obstacle i avoiding previous obstacles
    dp = [0] * (n + 1)
    
    for i in range(n + 1):
        r_i, c_i = obstacles[i]
        dp[i] = paths(0, 0, r_i, c_i)
        
        # Subtract paths through previous obstacles
        for j in range(i):
            r_j, c_j = obstacles[j]
            if r_j <= r_i and c_j <= c_i:
                dp[i] = (dp[i] - dp[j] * paths(r_j, c_j, r_i, c_i)) % MOD
    
    return dp[n] % MOD

# Example usage
h, w, n = 3, 4, 2
obstacles = [(2, 2), (3, 3)]
result = grid_2_paths(h, w, n, obstacles)
print(f"Number of paths: {result}")
```

**Time Complexity**: O(N^2 + H + W)
**Space Complexity**: O(N + H + W)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Inclusion-Exclusion | O(N^2 + H+W) | O(N+H+W) | Count paths avoiding obstacles |

### Why This Solution Works
- **Inclusion-Exclusion**: Subtract paths through obstacles
- **Combinatorics**: Use combinations for path counting
- **Sorting**: Process obstacles in order

## 🚀 Related Problems
- Grid path problems with obstacles
- Inclusion-exclusion problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem Y](https://atcoder.jp/contests/dp/tasks/dp_y) - Original problem
- Inclusion-exclusion techniques

