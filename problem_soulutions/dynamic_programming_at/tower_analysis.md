---
layout: simple
title: "Tower - AtCoder Educational DP Contest Problem X"
permalink: /problem_soulutions/dynamic_programming_at/tower_analysis
---

# Tower - AtCoder Educational DP Contest Problem X

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand DP with sorting
- Apply DP to solve box stacking problems
- Handle 3D optimization problems
- Recognize LIS-like patterns

### 📚 **Prerequisites**
- Dynamic Programming, longest increasing subsequence
- Arrays, sorting
- Related: Box stacking, LIS problems

## 📋 Problem Description

Given N boxes with dimensions (w_i, s_i, v_i), stack boxes such that w_i < w_j and s_i < s_j for boxes i below j. Find maximum total value.

**Input**: 
- First line: N (1 ≤ N ≤ 1000)
- Next N lines: w_i, s_i, v_i

**Output**: 
- Maximum total value

**Constraints**:
- 1 ≤ N ≤ 1000
- 1 ≤ w_i, s_i, v_i ≤ 10^9

## 🔍 Solution Analysis

### Approach: DP with Sorting

**Key Insight**: Sort boxes by (w_i + s_i), then use DP similar to LIS.

**DP State Definition**:
- `dp[i]` = maximum value with box i on top
- Sort boxes by (w + s) to ensure valid stacking

**Recurrence Relation**:
- For box i, try placing it on top of box j:
  - `dp[i] = max(dp[j] + v_i)` for all j where w_j < w_i and s_j < s_i
- Or start new stack: `dp[i] = v_i`

**Implementation**:
```python
def tower_max_value(n, boxes):
    """
    DP solution for Tower problem
    
    Args:
        n: number of boxes
        boxes: list of (w, s, v) tuples
    
    Returns:
        int: maximum total value
    """
    # Sort by (w + s) to ensure valid stacking order
    boxes.sort(key=lambda x: x[0] + x[1])
    
    # dp[i] = max value with box i on top
    dp = [0] * n
    
    for i in range(n):
        w_i, s_i, v_i = boxes[i]
        dp[i] = v_i  # Can start new stack
        
        # Try placing on top of previous boxes
        for j in range(i):
            w_j, s_j, v_j = boxes[j]
            if w_j < w_i and s_j < s_i:
                dp[i] = max(dp[i], dp[j] + v_i)
    
    return max(dp)

# Example usage
n = 3
boxes = [(10, 20, 100), (20, 30, 200), (30, 40, 300)]
result = tower_max_value(n, boxes)
print(f"Maximum value: {result}")
```

**Time Complexity**: O(N^2)
**Space Complexity**: O(N)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DP + Sorting | O(N^2) | O(N) | Sort by (w+s) for valid order |

### Why This Solution Works
- **Sorting**: Ensure valid stacking order
- **LIS-like**: Similar to longest increasing subsequence
- **DP**: Track maximum value with each box on top

## 🚀 Related Problems
- Box stacking problems
- LIS variants

## 🔗 Additional Resources
- [AtCoder DP Contest Problem X](https://atcoder.jp/contests/dp/tasks/dp_x) - Original problem
- Box stacking techniques

