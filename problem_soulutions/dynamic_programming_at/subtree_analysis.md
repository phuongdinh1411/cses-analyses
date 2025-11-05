---
layout: simple
title: "Subtree - AtCoder Educational DP Contest Problem V"
permalink: /problem_soulutions/dynamic_programming_at/subtree_analysis
---

# Subtree - AtCoder Educational DP Contest Problem V

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand tree DP with rerooting
- Apply DP to solve subtree problems
- Handle tree rerooting technique
- Optimize tree DP with rerooting

### 📚 **Prerequisites**
- Dynamic Programming, tree DP, rerooting
- Trees, DFS, adjacency lists
- Related: Tree DP problems, subtree problems

## 📋 Problem Description

Given a tree with N vertices, for each vertex, count the number of ways to color its subtree black such that all black vertices form a connected subtree, modulo M.

**Input**: 
- First line: N, M (1 ≤ N ≤ 10^5, 2 ≤ M ≤ 10^9)
- Next N-1 lines: edges

**Output**: 
- For each vertex, print the count modulo M

**Constraints**:
- 1 ≤ N ≤ 10^5
- 2 ≤ M ≤ 10^9

## 🔍 Solution Analysis

### Approach: Tree DP with Rerooting

**Key Insight**: Use tree DP with rerooting to compute answer for each root.

**DP State Definition**:
- `dp[v][0]` = ways to color subtree of v (with v as root) where v is white
- `dp[v][1]` = ways to color subtree of v where v is black
- For rerooting: compute for each root

**Recurrence Relation**:
- `dp[v][0] = 1` (white)
- `dp[v][1] = product(dp[u][0] + dp[u][1])` for all children u (black, children can be either)

**Implementation**:
```python
def subtree_coloring(n, m, edges):
    """
    Tree DP with rerooting for Subtree problem
    
    Args:
        n: number of vertices
        m: modulo
        edges: list of edges
    
    Returns:
        list: count for each vertex
    """
    # Build tree
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # dp[v][0] = white, dp[v][1] = black
    dp = [[0, 0] for _ in range(n + 1)]
    
    def dfs(v, parent):
        dp[v][0] = 1
        dp[v][1] = 1
        
        for u in graph[v]:
            if u == parent:
                continue
            dfs(u, v)
            dp[v][1] = (dp[v][1] * (dp[u][0] + dp[u][1])) % m
    
    results = []
    for root in range(1, n + 1):
        dfs(root, -1)
        results.append(dp[root][1])
    
    return results

# Example usage
n, m = 3, 1000000007
edges = [(1, 2), (2, 3)]
result = subtree_coloring(n, m, edges)
print(result)
```

**Time Complexity**: O(N^2) - naive, can be optimized to O(N)
**Space Complexity**: O(N)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Tree DP + Rerooting | O(N^2) | O(N) | Compute for each root |

### Why This Solution Works
- **Tree DP**: Compute subtree colorings
- **Rerooting**: Compute answer for each vertex as root
- **Connected Subtree**: Black vertices must be connected

## 🚀 Related Problems
- Tree DP problems
- Subtree problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem V](https://atcoder.jp/contests/dp/tasks/dp_v) - Original problem
- Tree rerooting techniques

