---
layout: simple
title: "Intervals"
permalink: /problem_soulutions/dynamic_programming_at/intervals_analysis
---

# Intervals

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand interval covering DP
- Apply DP to solve interval problems
- Handle interval optimization
- Use coordinate compression

## 📋 Problem Description

Given M intervals [l_i, r_i] with scores a_i, select intervals such that no two overlap and total score is maximized.

**Input**: 
- First line: N, M (1 ≤ N ≤ 10^5, 1 ≤ M ≤ 10^5)
- Next M lines: l_i, r_i, a_i

**Output**: 
- Maximum total score

**Constraints**:
- 1 ≤ N, M ≤ 10^5
- 1 ≤ l_i ≤ r_i ≤ N

## 🔍 Solution Analysis

### Approach: DP with Interval Sorting

**Key Insight**: Sort intervals by right endpoint, use DP to track maximum score.

**DP State Definition**:
- `dp[i]` = maximum score using intervals ending at or before position i
- Process intervals sorted by right endpoint

**Recurrence Relation**:
- For interval [l, r] with score a:
  - `dp[r] = max(dp[r], dp[l-1] + a)`
- Also: `dp[i] = max(dp[i], dp[i-1])` (propagate)

**Implementation**:
```python
def intervals_max_score(n, m, intervals):
    """
    DP solution for Intervals problem
    
    Args:
        n: range size
        m: number of intervals
        intervals: list of (l, r, score) tuples
    
    Returns:
        int: maximum total score
    """
    # Sort by right endpoint
    intervals.sort(key=lambda x: x[1])
    
    # dp[i] = max score using intervals ending at or before i
    dp = [0] * (n + 1)
    
    interval_idx = 0
    for i in range(1, n + 1):
        # Propagate from previous position
        dp[i] = dp[i - 1]
        
        # Process intervals ending at i
        while interval_idx < m and intervals[interval_idx][1] == i:
            l, r, score = intervals[interval_idx]
            dp[i] = max(dp[i], dp[l - 1] + score)
            interval_idx += 1
    
    return dp[n]

# Example usage
n, m = 5, 3
intervals = [(1, 3, 10), (2, 4, 20), (3, 5, 30)]
result = intervals_max_score(n, m, intervals)
print(f"Maximum score: {result}")
```

**Time Complexity**: O(N + M log M)
**Space Complexity**: O(N)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DP + Sorting | O(N + M log M) | O(N) | Process by right endpoint |

### Why This Solution Works
- **Sorting**: Process intervals by right endpoint
- **DP Propagation**: Track maximum score at each position
- **Non-overlapping**: Ensure intervals don't overlap

## 🚀 Related Problems
- Interval scheduling
- Interval covering problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem W](https://atcoder.jp/contests/dp/tasks/dp_w) - Original problem
- Interval DP techniques

