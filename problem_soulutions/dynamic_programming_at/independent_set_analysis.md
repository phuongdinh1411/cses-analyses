---
layout: simple
title: "Independent Set"
permalink: /problem_soulutions/dynamic_programming_at/independent_set_analysis
---

# Independent Set

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand tree DP
- Apply DP to solve independent set on trees
- Recognize tree DP patterns
- Handle tree coloring problems

## 📋 Problem Description

Given a tree with N vertices, color each vertex black or white such that no two adjacent vertices are both black. Find the number of valid colorings modulo 10^9+7.

**Input**: 
- First line: N (1 ≤ N ≤ 10^5)
- Next N-1 lines: edges (u, v)

**Output**: 
- Number of valid colorings modulo 10^9+7

**Constraints**:
- 1 ≤ N ≤ 10^5
- Tree is given

## 🔍 Solution Analysis

### Approach: Tree DP

**Key Insight**: Use tree DP with two states per node: black or white.

**DP State Definition**:
- `dp[v][0]` = number of colorings for subtree rooted at v where v is white
- `dp[v][1]` = number of colorings for subtree rooted at v where v is black
- Answer: `dp[root][0] + dp[root][1]`

**Recurrence Relation**:
- For node v with children:
  - If v is white: children can be white or black
    - `dp[v][0] = product(dp[u][0] + dp[u][1])` for all children u
  - If v is black: children must be white
    - `dp[v][1] = product(dp[u][0])` for all children u

**Implementation**:
```python
def independent_set_tree(n, edges):
    """
    Tree DP solution for Independent Set problem
    
    Args:
        n: number of vertices
        edges: list of (u, v) tuples
    
    Returns:
        int: number of colorings modulo 10^9+7
    """
    MOD = 10**9 + 7
    
    # Build tree
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # dp[v][0] = colorings with v white, dp[v][1] = with v black
    dp = [[0, 0] for _ in range(n + 1)]
    
    def dfs(v, parent):
        dp[v][0] = 1  # White
        dp[v][1] = 1  # Black
        
        for u in graph[v]:
            if u == parent:
                continue
            
            dfs(u, v)
            
            # If v is white, u can be white or black
            dp[v][0] = (dp[v][0] * (dp[u][0] + dp[u][1])) % MOD
            # If v is black, u must be white
            dp[v][1] = (dp[v][1] * dp[u][0]) % MOD
    
    dfs(1, -1)
    return (dp[1][0] + dp[1][1]) % MOD

# Example usage
n = 3
edges = [(1, 2), (2, 3)]
result = independent_set_tree(n, edges)
print(f"Number of colorings: {result}")
```

**Time Complexity**: O(N)
**Space Complexity**: O(N)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Tree DP | O(N) | O(N) | Combine subtree results |

### Why This Solution Works
- **Optimal Substructure**: Coloring of tree depends on subtree colorings
- **Tree DP**: Process children and combine results
- **Two States**: Track black/white for each node

## 🚀 Related Problems
- [Tree Coloring](https://cses.fi/problemset/task/1139) - Similar problem
- Tree DP problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem P](https://atcoder.jp/contests/dp/tasks/dp_p) - Original problem
- Tree DP techniques

