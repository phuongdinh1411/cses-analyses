---
layout: simple
title: "Knapsack 2"
permalink: /problem_soulutions/dynamic_programming_at/knapsack_2_analysis
---

# Knapsack 2

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the knapsack problem with value-based DP
- Apply DP optimization when weights are large but values are small
- Switch DP state from capacity-based to value-based
- Recognize when to invert the DP state definition
- Optimize DP solutions for different constraint scenarios

## 📋 Problem Description

There are N items, numbered 1, 2, ..., N. For each i (1 ≤ i ≤ N), Item i has a weight of w_i and a value of v_i. Taro has decided to choose some of the N items and carry them home in a knapsack. The capacity of the knapsack is W. Here, we want to maximize the sum of the values of the items Taro takes home.

Find the maximum possible sum of the values of items that Taro takes home.

**Input**: 
- First line: N, W (1 ≤ N ≤ 100, 1 ≤ W ≤ 10^9)
- Next N lines: w_i, v_i (1 ≤ w_i ≤ 10^9, 1 ≤ v_i ≤ 10^3)

**Output**: 
- Print the maximum possible sum of values

**Constraints**:
- 1 ≤ N ≤ 100
- 1 ≤ W ≤ 10^9 (very large!)
- 1 ≤ w_i ≤ 10^9 (very large!)
- 1 ≤ v_i ≤ 10^3 (small!)

**Key Difference from Knapsack 1**: 
- In Knapsack 1: W ≤ 10^5 (small), v_i ≤ 10^9 (large)
- In Knapsack 2: W ≤ 10^9 (large!), v_i ≤ 10^3 (small!)
- We need to invert the DP state: instead of `dp[i][capacity]`, use `dp[i][value]`

**Example**:
```
Input:
3 8
3 30
4 50
5 60

Output:
90

Explanation**: 
Same items as Knapsack 1, but with different constraints.
Optimal solution: Item 1 + Item 3 = value 90
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Standard Knapsack DP (Inefficient)

**Key Insights from Standard Approach**:
- **Standard DP**: Use capacity-based DP like Knapsack 1
- **Problem**: W can be up to 10^9, making dp[i][W] impossible
- **Memory Issue**: Cannot create array of size 10^9
- **Not Feasible**: Need different approach

**Why it doesn't work**: 
- Standard DP uses O(n*W) space
- With W = 10^9, this is impossible

---

### Approach 2: Value-Based DP (Optimal)

**Key Insights from Value-Based DP**:
- **State Inversion**: Instead of `dp[i][capacity]`, use `dp[i][value]`
- **Key Observation**: Total value is bounded (N * max_v_i ≤ 100 * 10^3 = 10^5)
- **DP Definition**: `dp[i][v]` = minimum weight needed to achieve value v using first i items
- **Efficient**: O(n * total_value) time and space

**Key Insight**: Since values are small (≤ 10^3) and there are only 100 items, total possible value is at most 10^5. We can invert the DP state to minimize weight for a given value instead of maximizing value for a given capacity.

#### 📌 **DP State Definition**

**What does `dp[i][v]` represent?**
- `dp[i][v]` = **minimum weight** needed to achieve total value v using the first i items (items 0 to i-1)
- i ranges from 0 to n
- v ranges from 0 to total_max_value (at most N * max_v_i = 100 * 10^3 = 10^5)
- `dp[n][v]` stores minimum weight for each possible value v
- Answer: Find maximum v such that `dp[n][v] ≤ W`

**In plain language:**
- For each number of items and each possible total value, we store the minimum weight needed
- We can compute dp[i][v] by considering whether to take item i-1 or not

#### 🎯 **DP Thinking Process**

**Step 1: Identify the Problem**
- Standard capacity-based DP won't work (W too large)
- Values are small (≤ 10^3), so total value is bounded
- Solution: Invert the DP state

**Step 2: Define the DP State** (See DP State Definition section above)

**Step 3: Find the Recurrence Relation (State Transition)**
- How do we compute `dp[i][v]`?
- We consider item i-1
- Option 1: Don't take item i-1 → `dp[i][v] = dp[i-1][v]`
- Option 2: Take item i-1 (if v ≥ values[i-1]) → `dp[i][v] = dp[i-1][v - values[i-1]] + weights[i-1]`
- Therefore: `dp[i][v] = min(dp[i-1][v], dp[i-1][v - values[i-1]] + weights[i-1])` (if v ≥ values[i-1])

**Step 4: Determine Base Cases**
- `dp[0][0] = 0`: Zero items, zero value, zero weight
- `dp[0][v] = INF` for v > 0: Cannot achieve positive value with zero items
- `dp[i][0] = 0`: Zero value requires zero weight (can skip all items)

**Step 5: Identify the Answer**
- Find maximum v such that `dp[n][v] ≤ W`
- This is the maximum value achievable within weight capacity W

#### 📊 **Visual DP Table Construction**

For `n=3, W=8, weights=[3,4,5], values=[30,50,60]`:
```
Step-by-step DP table filling (value-based):

Total possible value: 3 * 1000 = 3000 (but we only need up to achievable values)

Base cases:
dp[0][0] = 0
dp[0][v] = INF for v > 0

For i=1 (considering first item: weight=3, value=30):
dp[1][0] = 0 (skip item)
dp[1][30] = min(INF, dp[0][0] + 3) = 3
dp[1][v] = INF for v not in {0, 30}

For i=2 (considering first 2 items):
dp[2][0] = 0
dp[2][30] = min(dp[1][30], dp[1][0] + 3) = min(3, 3) = 3
dp[2][50] = min(INF, dp[1][0] + 4) = 4
dp[2][80] = min(INF, dp[1][30] + 4) = 3 + 4 = 7

For i=3 (considering all 3 items):
dp[3][0] = 0
dp[3][30] = 3
dp[3][50] = 4
dp[3][60] = min(INF, dp[2][0] + 5) = 5
dp[3][80] = 7
dp[3][90] = min(INF, dp[2][30] + 5) = 3 + 5 = 8
dp[3][110] = min(INF, dp[2][50] + 5) = 4 + 5 = 9 (exceeds W=8)

Find maximum v where dp[3][v] ≤ 8:
- dp[3][90] = 8 ≤ 8 ✓
- dp[3][110] = 9 > 8 ✗

Final answer: 90
```

**Algorithm**:
- Calculate max_total_value = sum of all values
- Initialize `dp[0][0] = 0`, `dp[0][v] = INF` for v > 0
- For i from 1 to n:
  - For v from 0 to max_total_value:
    - `dp[i][v] = dp[i-1][v]` (skip item i-1)
    - If `v ≥ values[i-1]`:
      - `dp[i][v] = min(dp[i][v], dp[i-1][v - values[i-1]] + weights[i-1])`
- Find maximum v such that `dp[n][v] ≤ W`
- Return that maximum v

**Visual Example**:
```
DP table for n=3, W=8 (value-based):
┌─────────────────────────────────────┐
│ Value (v) | dp[3][v] (min weight)  │
│     0     |      0                  │
│    30     |      3                  │
│    50     |      4                  │
│    60     |      5                  │
│    80     |      7                  │
│    90     |      8 ≤ W ✓            │
│   110     |      9 > W ✗            │
│                                     │
│ Maximum value with weight ≤ 8: 90  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def knapsack_2_dp(n, w, weights, values):
    """
    Value-based DP solution for Knapsack 2 problem
    
    Args:
        n: number of items
        w: knapsack capacity
        weights: list of item weights
        values: list of item values
    
    Returns:
        int: maximum possible sum of values
    """
    # Calculate maximum possible total value
    max_total_value = sum(values)
    
    # dp[i][v] = minimum weight to achieve value v using first i items
    # Use INF to represent impossible
    INF = float('inf')
    dp = [[INF] * (max_total_value + 1) for _ in range(n + 1)]
    
    # Base case: zero value requires zero weight
    dp[0][0] = 0
    
    # Fill DP table
    for i in range(1, n + 1):
        for v in range(max_total_value + 1):
            # Option 1: Don't take item i-1
            dp[i][v] = dp[i - 1][v]
            
            # Option 2: Take item i-1 (if possible)
            if v >= values[i - 1]:
                take_weight = dp[i - 1][v - values[i - 1]] + weights[i - 1]
                dp[i][v] = min(dp[i][v], take_weight)
    
    # Find maximum value achievable within weight capacity
    max_value = 0
    for v in range(max_total_value, -1, -1):
        if dp[n][v] <= w:
            max_value = v
            break
    
    return max_value

# Example usage
n, w = 3, 8
weights = [3, 4, 5]
values = [30, 50, 60]
result = knapsack_2_dp(n, w, weights, values)
print(f"Maximum value: {result}")  # Output: 90
```

**Time Complexity**: O(n * total_value) where total_value = sum of all values
**Space Complexity**: O(n * total_value)

**Why it's optimal**: Uses value-based DP which is feasible since total_value is bounded (≤ 100 * 10^3 = 10^5).

---

### Approach 3: Space-Optimized DP Solution

**Key Insights from Space-Optimized Solution**:
- **Space Optimization**: Only need previous row of DP table
- **Rolling Array**: Use 1D array instead of 2D
- **Efficient**: O(n * total_value) time, O(total_value) space
- **Optimal Space**: Best space complexity

**Key Insight**: Since we only need dp[i-1] to compute dp[i], we can use a 1D array and iterate backwards through values.

**Implementation**:
```python
def knapsack_2_space_optimized(n, w, weights, values):
    """
    Space-optimized value-based DP solution for Knapsack 2 problem
    
    Args:
        n: number of items
        w: knapsack capacity
        weights: list of item weights
        values: list of item values
    
    Returns:
        int: maximum possible sum of values
    """
    max_total_value = sum(values)
    INF = float('inf')
    
    # Only need 1D array: dp[v] = minimum weight to achieve value v
    dp = [INF] * (max_total_value + 1)
    dp[0] = 0  # Base case: zero value requires zero weight
    
    # Process each item
    for i in range(n):
        # Iterate backwards to avoid using updated values
        for v in range(max_total_value, values[i] - 1, -1):
            # Option: Take item i
            dp[v] = min(dp[v], dp[v - values[i]] + weights[i])
    
    # Find maximum value achievable within weight capacity
    for v in range(max_total_value, -1, -1):
        if dp[v] <= w:
            return v
    
    return 0

# Example usage
n, w = 3, 8
weights = [3, 4, 5]
values = [30, 50, 60]
result = knapsack_2_space_optimized(n, w, weights, values)
print(f"Maximum value: {result}")  # Output: 90
```

**Time Complexity**: O(n * total_value)
**Space Complexity**: O(total_value)

**Why it's optimal**: Uses O(total_value) space while maintaining O(n * total_value) time complexity.

**Important Note**: We iterate backwards through values (from max_total_value to values[i]) to ensure we don't use updated values when computing dp[v]. This is crucial for the 0/1 knapsack problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Standard DP | O(n*W) | O(n*W) | Not feasible (W too large) |
| Value-Based DP | O(n*total_value) | O(n*total_value) | Invert state to use values |
| Space-Optimized DP | O(n*total_value) | O(total_value) | Only need previous row |

### Time Complexity
- **Time**: O(n * total_value) - For each of n items, consider each possible value up to total_value
- **Space**: O(total_value) - Only one array of size total_value+1 needed for space-optimized version

### Why This Solution Works
- **State Inversion**: Switch from capacity-based to value-based DP
- **Bounded Values**: Total value is bounded (≤ 100 * 10^3 = 10^5), making it feasible
- **Optimal Substructure**: Minimum weight for value v depends on minimum weights for smaller values
- **Backward Iteration**: Critical for space-optimized version to maintain correctness

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Knapsack 2 - Value Range Query**
**Problem**: Answer queries about maximum value achievable for different capacities.

**Implementation**:
```python
def knapsack_2_with_queries(n, weights, values, capacity_queries):
    """
    Value-based DP with multiple capacity queries
    
    Args:
        n: number of items
        weights: list of item weights
        values: list of item values
        capacity_queries: list of capacity values to query
    
    Returns:
        list: maximum values for each query
    """
    max_total_value = sum(values)
    INF = float('inf')
    
    # Precompute DP for all possible values
    dp = [INF] * (max_total_value + 1)
    dp[0] = 0
    
    for i in range(n):
        for v in range(max_total_value, values[i] - 1, -1):
            dp[v] = min(dp[v], dp[v - values[i]] + weights[i])
    
    # Answer queries
    results = []
    for capacity in capacity_queries:
        max_value = 0
        for v in range(max_total_value, -1, -1):
            if dp[v] <= capacity:
                max_value = v
                break
        results.append(max_value)
    
    return results

# Example usage
n = 3
weights = [3, 4, 5]
values = [30, 50, 60]
queries = [8, 10, 12]
results = knapsack_2_with_queries(n, weights, values, queries)
print(f"Results: {results}")  # Output: [90, 110, 140]
```

#### **2. Knapsack 2 - Item Selection**
**Problem**: Find maximum value and reconstruct which items were selected.

**Implementation**:
```python
def knapsack_2_with_items(n, w, weights, values):
    """
    Value-based DP with item selection reconstruction
    
    Args:
        n: number of items
        w: knapsack capacity
        weights: list of item weights
        values: list of item values
    
    Returns:
        tuple: (maximum value, list of selected item indices)
    """
    max_total_value = sum(values)
    INF = float('inf')
    
    # Use 2D DP to track selections
    dp = [[INF] * (max_total_value + 1) for _ in range(n + 1)]
    selected = [[False] * (max_total_value + 1) for _ in range(n + 1)]
    
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        for v in range(max_total_value + 1):
            dp[i][v] = dp[i - 1][v]
            selected[i][v] = False
            
            if v >= values[i - 1]:
                take_weight = dp[i - 1][v - values[i - 1]] + weights[i - 1]
                if take_weight < dp[i][v]:
                    dp[i][v] = take_weight
                    selected[i][v] = True
    
    # Find maximum achievable value
    max_value = 0
    for v in range(max_total_value, -1, -1):
        if dp[n][v] <= w:
            max_value = v
            break
    
    # Reconstruct selected items
    items = []
    current_value = max_value
    for i in range(n, 0, -1):
        if selected[i][current_value]:
            items.append(i - 1)
            current_value -= values[i - 1]
    
    items.reverse()
    return max_value, items

# Example usage
n, w = 3, 8
weights = [3, 4, 5]
values = [30, 50, 60]
max_value, selected_items = knapsack_2_with_items(n, w, weights, values)
print(f"Maximum value: {max_value}")
print(f"Selected items: {selected_items}")
```

### Related Problems

#### **AtCoder Problems**
- [Knapsack 1](https://atcoder.jp/contests/dp/tasks/dp_d) - Previous problem (capacity-based DP)

#### **CSES Problems**
- [Book Shop](https://cses.fi/problemset/task/1158) - Similar knapsack problem

#### **LeetCode Problems**
- [0/1 Knapsack](https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/) - Classic problem
- Problems where weights are large but values are small

#### **Problem Categories**
- **State Inversion**: Switching DP state dimensions
- **Value-Based DP**: Using values instead of capacity
- **Optimization**: Adapting algorithms to different constraints

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming Introduction](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP fundamentals
- [Knapsack Problems](https://cp-algorithms.com/dynamic_programming/knapsack.html) - Knapsack algorithms

### **Practice Problems**
- [AtCoder DP Contest Problem E](https://atcoder.jp/contests/dp/tasks/dp_e) - Original problem
- [AtCoder DP Contest Problem D](https://atcoder.jp/contests/dp/tasks/dp_d) - Previous problem

### **Further Reading**
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms) - Dynamic Programming chapter
- [Competitive Programming Handbook](https://cses.fi/book/book.pdf) - DP section

