---
layout: simple
title: "Frog 3"
permalink: /problem_soulutions/dynamic_programming_at/frog_3_analysis
---

# Frog 3

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand convex hull trick for DP optimization
- Apply advanced DP optimization techniques
- Handle quadratic transitions in DP
- Optimize DP with convex hull trick

## 📋 Problem Description

There are N stones. Frog jumps from stone i to j with cost (h_i - h_j)^2 + C. Find minimum cost to reach stone N.

**Input**: 
- First line: N, C (2 ≤ N ≤ 2*10^5, 1 ≤ C ≤ 10^12)
- Second line: h_1, h_2, ..., h_N (1 ≤ h_i ≤ 10^6)

**Output**: 
- Minimum total cost

**Constraints**:
- 2 ≤ N ≤ 2*10^5
- 1 ≤ C ≤ 10^12

## 🔍 Solution Analysis

### Approach: Convex Hull Trick

**Key Insight**: DP transition is quadratic. Use convex hull trick to optimize from O(N^2) to O(N).

**DP State Definition**:
- `dp[i]` = minimum cost to reach stone i
- `dp[i] = min(dp[j] + (h_i - h_j)^2 + C)` for j < i

**Expanding the transition**:
- `dp[i] = min(dp[j] + h_i^2 - 2*h_i*h_j + h_j^2 + C)`
- `dp[i] = h_i^2 + C + min(-2*h_i*h_j + dp[j] + h_j^2)`
- This is linear in h_j: `m = -2*h_i, x = h_j, b = dp[j] + h_j^2`

**Convex Hull Trick**:
- Maintain lines and query minimum at point h_i
- Use Li Chao tree or line container

**Implementation**:
```python
class LiChaoTree:
    def __init__(self, xs):
        self.xs = sorted(set(xs))
        self.size = 1
        while self.size < len(self.xs):
            self.size *= 2
        self.lines = [None] * (2 * self.size)
    
    def f(self, line, x):
        """Evaluate line at point x"""
        if line is None:
            return float('inf')
        m, b = line
        return m * x + b
    
    def update(self, line, node=1, l=0, r=None):
        if r is None:
            r = len(self.xs)
        if r - l == 1:
            if self.f(line, self.xs[l]) < self.f(self.lines[node], self.xs[l]):
                self.lines[node] = line
            return
        
        mid = (l + r) // 2
        x_mid = self.xs[mid]
        
        if self.f(line, x_mid) < self.f(self.lines[node], x_mid):
            line, self.lines[node] = self.lines[node], line
        
        if self.f(line, self.xs[l]) < self.f(self.lines[node], self.xs[l]):
            self.update(line, 2*node, l, mid)
        else:
            self.update(line, 2*node+1, mid, r)
    
    def query(self, x, node=1, l=0, r=None):
        if r is None:
            r = len(self.xs)
        if r - l == 1:
            return self.f(self.lines[node], x)
        
        mid = (l + r) // 2
        if x < self.xs[mid]:
            return min(self.f(self.lines[node], x), 
                      self.query(x, 2*node, l, mid))
        else:
            return min(self.f(self.lines[node], x),
                      self.query(x, 2*node+1, mid, r))

def frog_3_min_cost(n, c, heights):
    """
    Convex hull trick solution for Frog 3
    
    Args:
        n: number of stones
        c: constant cost
        heights: list of stone heights
    
    Returns:
        int: minimum total cost
    """
    # Build Li Chao tree
    tree = LiChaoTree(heights)
    
    dp = [0] * n
    dp[0] = 0
    
    # Add line for stone 0
    tree.update((-2 * heights[0], dp[0] + heights[0]**2))
    
    for i in range(1, n):
        # Query minimum at h_i
        min_val = tree.query(heights[i])
        dp[i] = heights[i]**2 + c + min_val
        
        # Add line for stone i
        tree.update((-2 * heights[i], dp[i] + heights[i]**2))
    
    return dp[n - 1]

# Example usage
n, c = 5, 100
heights = [10, 20, 30, 40, 50]
result = frog_3_min_cost(n, c, heights)
print(f"Minimum cost: {result}")
```

**Time Complexity**: O(N log N)
**Space Complexity**: O(N)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive DP | O(N^2) | O(N) | Too slow |
| Convex Hull Trick | O(N log N) | O(N) | Optimize quadratic transitions |

### Why This Solution Works
- **Convex Hull Trick**: Optimize quadratic DP transitions
- **Line Container**: Maintain and query lines efficiently
- **DP Optimization**: Reduce from O(N^2) to O(N log N)

## 🚀 Related Problems
- Advanced DP optimization problems
- Convex hull trick problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem Z](https://atcoder.jp/contests/dp/tasks/dp_z) - Original problem
- Convex hull trick techniques

