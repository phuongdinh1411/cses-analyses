---
layout: simple
title: "Knapsack 1 - AtCoder Educational DP Contest Problem D"
permalink: /problem_soulutions/dynamic_programming_at/knapsack_1_analysis
---

# Knapsack 1 - AtCoder Educational DP Contest Problem D

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the classic 0/1 Knapsack problem
- Apply 2D DP to solve knapsack problems
- Implement space-optimized knapsack solutions
- Recognize when to use knapsack DP pattern
- Optimize DP solutions for large capacity constraints

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic Programming, 2D DP, knapsack problems
- **Data Structures**: Arrays, 2D arrays
- **Mathematical Concepts**: Maximum value computation, optimization
- **Programming Skills**: Multi-dimensional array manipulation, space optimization
- **Related Problems**: Book Shop (CSES), Coin Change (LeetCode)

## 📋 Problem Description

There are N items, numbered 1, 2, ..., N. For each i (1 ≤ i ≤ N), Item i has a weight of w_i and a value of v_i. Taro has decided to choose some of the N items and carry them home in a knapsack. The capacity of the knapsack is W. Here, we want to maximize the sum of the values of the items Taro takes home.

Find the maximum possible sum of the values of items that Taro takes home.

**Input**: 
- First line: N, W (1 ≤ N ≤ 100, 1 ≤ W ≤ 10^5)
- Next N lines: w_i, v_i (1 ≤ w_i ≤ W, 1 ≤ v_i ≤ 10^9)

**Output**: 
- Print the maximum possible sum of values

**Constraints**:
- 1 ≤ N ≤ 100
- 1 ≤ W ≤ 10^5
- 1 ≤ w_i ≤ W
- 1 ≤ v_i ≤ 10^9

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
Items: (weight, value)
- Item 1: (3, 30)
- Item 2: (4, 50)
- Item 3: (5, 60)

Knapsack capacity: 8

Possible combinations:
- Item 1 + Item 2: weight = 7, value = 80
- Item 1 + Item 3: weight = 8, value = 90 ✓
- Item 2 + Item 3: weight = 9 (exceeds capacity)
- Item 1: weight = 3, value = 30
- Item 2: weight = 4, value = 50
- Item 3: weight = 5, value = 60

Maximum value: 90 (Item 1 + Item 3)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution (Brute Force)

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Try all possible item combinations
- **Complete Enumeration**: Explore all subsets of items
- **Simple Implementation**: Easy to understand
- **Inefficient**: Exponential time complexity O(2^n)

**Key Insight**: Use recursion to explore all possible ways to select items within the weight capacity.

**Algorithm**:
- For each item, decide whether to take it or not
- If taking, subtract weight and add value
- Track maximum value achieved

**Visual Example**:
```
Items: [(3,30), (4,50), (5,60)], Capacity: 8

Recursive exploration:
┌─────────────────────────────────────┐
│ Item 1: Take or Skip?              │
│ - Take: weight=3, value=30, recurse │
│ - Skip: weight=0, value=0, recurse │
│                                     │
│ Item 2: Take or Skip?              │
│ ... (explores all 2^3 = 8 subsets) │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def knapsack_1_recursive(n, w, weights, values):
    """
    Recursive solution for Knapsack 1 problem
    
    Args:
        n: number of items
        w: knapsack capacity
        weights: list of item weights
        values: list of item values
    
    Returns:
        int: maximum possible sum of values
    """
    def max_value(i, remaining_capacity):
        """Calculate maximum value from item i onwards"""
        # Base case: no more items
        if i == n:
            return 0
        
        # Option 1: Skip current item
        skip_value = max_value(i + 1, remaining_capacity)
        
        # Option 2: Take current item (if possible)
        take_value = 0
        if weights[i] <= remaining_capacity:
            take_value = values[i] + max_value(i + 1, remaining_capacity - weights[i])
        
        return max(skip_value, take_value)
    
    return max_value(0, w)

# Example usage
n, w = 3, 8
weights = [3, 4, 5]
values = [30, 50, 60]
result = knapsack_1_recursive(n, w, weights, values)
print(f"Maximum value: {result}")  # Output: 90
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to recalculating the same subproblems.

---

### Approach 2: Memoized Recursive Solution

**Key Insights from Memoized Solution**:
- **Memoization**: Store results of (item_index, capacity) pairs
- **Top-Down DP**: Recursive approach with caching
- **Efficient**: O(n*W) time complexity
- **Memory Trade-off**: O(n*W) space for memoization

**Implementation**:
```python
def knapsack_1_memoized(n, w, weights, values):
    """
    Memoized recursive solution for Knapsack 1 problem
    
    Args:
        n: number of items
        w: knapsack capacity
        weights: list of item weights
        values: list of item values
    
    Returns:
        int: maximum possible sum of values
    """
    memo = {}
    
    def max_value(i, remaining_capacity):
        """Calculate maximum value from item i onwards"""
        # Check memo
        if (i, remaining_capacity) in memo:
            return memo[(i, remaining_capacity)]
        
        # Base case
        if i == n:
            memo[(i, remaining_capacity)] = 0
            return 0
        
        # Option 1: Skip current item
        skip_value = max_value(i + 1, remaining_capacity)
        
        # Option 2: Take current item (if possible)
        take_value = 0
        if weights[i] <= remaining_capacity:
            take_value = values[i] + max_value(i + 1, remaining_capacity - weights[i])
        
        result = max(skip_value, take_value)
        memo[(i, remaining_capacity)] = result
        return result
    
    return max_value(0, w)

# Example usage
n, w = 3, 8
weights = [3, 4, 5]
values = [30, 50, 60]
result = knapsack_1_memoized(n, w, weights, values)
print(f"Maximum value: {result}")  # Output: 90
```

**Time Complexity**: O(n*W)
**Space Complexity**: O(n*W)

**Why it's better**: Uses memoization to achieve O(n*W) time complexity.

---

### Approach 3: Bottom-Up Dynamic Programming (Optimal)

**Key Insights from Bottom-Up DP Solution**:
- **Bottom-Up DP**: Build solution from base cases
- **2D DP Table**: dp[i][j] represents maximum value using first i items with capacity j
- **Efficient**: O(n*W) time, O(n*W) space
- **Optimal**: Best approach for this problem

**Key Insight**: Use 2D DP where dp[i][j] represents maximum value achievable using first i items with capacity j.

#### 📌 **DP State Definition**

**What does `dp[i][j]` represent?**
- `dp[i][j]` = **maximum value** achievable using the first i items (items 0 to i-1) with a knapsack capacity of j
- i ranges from 0 to n (0 means no items, n means all items)
- j ranges from 0 to W (0 means no capacity, W means full capacity)
- `dp[n][W]` = our final answer (maximum value using all n items with capacity W)

**In plain language:**
- For each number of items and each possible capacity, we store the maximum value achievable
- We can compute dp[i][j] by considering whether to take item i-1 or not

#### 🎯 **DP Thinking Process**

**Step 1: Identify the Subproblem**
- What are we trying to maximize? The total value of items in the knapsack
- What information do we need? For each number of items and each capacity, the maximum value achievable

**Step 2: Define the DP State** (See DP State Definition section above)

**Step 3: Find the Recurrence Relation (State Transition)**
- How do we compute `dp[i][j]`?
- We consider item i-1 (the i-th item, 0-indexed)
- Option 1: Don't take item i-1 → `dp[i][j] = dp[i-1][j]`
- Option 2: Take item i-1 (if weight[i-1] ≤ j) → `dp[i][j] = dp[i-1][j - weights[i-1]] + values[i-1]`
- Therefore: `dp[i][j] = max(dp[i-1][j], dp[i-1][j - weights[i-1]] + values[i-1])` (if weight allows)

**Step 4: Determine Base Cases**
- `dp[0][j] = 0` for all j: No items, so no value
- `dp[i][0] = 0` for all i: No capacity, so no value

**Step 5: Identify the Answer**
- The answer is `dp[n][W]` - maximum value using all n items with capacity W

#### 📊 **Visual DP Table Construction**

For `n=3, W=8, weights=[3,4,5], values=[30,50,60]`:
```
Step-by-step DP table filling:

Base cases:
dp[0][j] = 0 for all j (no items)

For i=1 (considering first item: weight=3, value=30):
dp[1][0] = 0 (no capacity)
dp[1][1] = 0 (weight 3 > 1, can't take)
dp[1][2] = 0 (weight 3 > 2, can't take)
dp[1][3] = max(dp[0][3], dp[0][0]+30) = max(0, 30) = 30
dp[1][4] = max(dp[0][4], dp[0][1]+30) = max(0, 30) = 30
...
dp[1][8] = 30

For i=2 (considering first 2 items):
dp[2][0] = 0
dp[2][1] = 0
dp[2][2] = 0
dp[2][3] = max(dp[1][3], dp[1][0]+30) = max(30, 30) = 30
dp[2][4] = max(dp[1][4], dp[1][1]+30, dp[1][4], dp[1][0]+50) 
         = max(30, 30, 30, 50) = 50
dp[2][5] = max(dp[1][5], dp[1][2]+30, dp[1][5], dp[1][1]+50)
         = max(30, 30, 30, 50) = 50
dp[2][7] = max(dp[1][7], dp[1][4]+30, dp[1][7], dp[1][3]+50)
         = max(30, 60, 30, 80) = 80
dp[2][8] = max(dp[1][8], dp[1][5]+30, dp[1][8], dp[1][4]+50)
         = max(30, 60, 30, 80) = 80

For i=3 (considering all 3 items):
dp[3][8] = max(dp[2][8], dp[2][3]+60) = max(80, 90) = 90

Final answer: dp[3][8] = 90
```

**Algorithm**:
- Initialize `dp[0][j] = 0` for all j
- For i from 1 to n:
  - For j from 0 to W:
    - `dp[i][j] = dp[i-1][j]` (skip item i-1)
    - If `weights[i-1] <= j`:
      - `dp[i][j] = max(dp[i][j], dp[i-1][j - weights[i-1]] + values[i-1])`
- Return `dp[n][W]`

**Visual Example**:
```
DP table for n=3, W=8:
┌─────────────────────────────────────┐
│     Capacity (j)                    │
│ i\j|  0  1  2  3  4  5  6  7  8    │
│  0 |  0  0  0  0  0  0  0  0  0     │
│  1 |  0  0  0 30 30 30 30 30 30     │
│  2 |  0  0  0 30 50 50 50 80 80     │
│  3 |  0  0  0 30 50 60 60 80 90     │
│                                     │
│ Items: (3,30), (4,50), (5,60)      │
│ Final answer: dp[3][8] = 90        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def knapsack_1_dp(n, w, weights, values):
    """
    Bottom-up DP solution for Knapsack 1 problem
    
    Args:
        n: number of items
        w: knapsack capacity
        weights: list of item weights
        values: list of item values
    
    Returns:
        int: maximum possible sum of values
    """
    # Create DP table: dp[i][j] = max value using first i items with capacity j
    dp = [[0] * (w + 1) for _ in range(n + 1)]
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(w + 1):
            # Option 1: Don't take item i-1
            dp[i][j] = dp[i - 1][j]
            
            # Option 2: Take item i-1 (if possible)
            if weights[i - 1] <= j:
                dp[i][j] = max(dp[i][j], 
                              dp[i - 1][j - weights[i - 1]] + values[i - 1])
    
    return dp[n][w]

# Example usage
n, w = 3, 8
weights = [3, 4, 5]
values = [30, 50, 60]
result = knapsack_1_dp(n, w, weights, values)
print(f"Maximum value: {result}")  # Output: 90
```

**Time Complexity**: O(n*W)
**Space Complexity**: O(n*W)

**Why it's optimal**: Uses bottom-up DP for O(n*W) time and space complexity.

---

### Approach 4: Space-Optimized DP Solution

**Key Insights from Space-Optimized Solution**:
- **Space Optimization**: Only need previous row of DP table
- **Rolling Array**: Use 1D array instead of 2D
- **Efficient**: O(n*W) time, O(W) space
- **Optimal Space**: Best space complexity for this problem

**Key Insight**: Since we only need dp[i-1] to compute dp[i], we can use a 1D array and iterate backwards through capacities.

**Implementation**:
```python
def knapsack_1_space_optimized(n, w, weights, values):
    """
    Space-optimized DP solution for Knapsack 1 problem
    
    Args:
        n: number of items
        w: knapsack capacity
        weights: list of item weights
        values: list of item values
    
    Returns:
        int: maximum possible sum of values
    """
    # Only need 1D array: dp[j] = max value with capacity j
    dp = [0] * (w + 1)
    
    # Process each item
    for i in range(n):
        # Iterate backwards to avoid using updated values
        for j in range(w, weights[i] - 1, -1):
            # Option: Take item i
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
    
    return dp[w]

# Example usage
n, w = 3, 8
weights = [3, 4, 5]
values = [30, 50, 60]
result = knapsack_1_space_optimized(n, w, weights, values)
print(f"Maximum value: {result}")  # Output: 90
```

**Time Complexity**: O(n*W)
**Space Complexity**: O(W)

**Why it's optimal**: Uses O(W) space while maintaining O(n*W) time complexity.

**Important Note**: We iterate backwards through capacities (from W to weights[i]) to ensure we don't use updated values when computing dp[j]. This is crucial for the 0/1 knapsack problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Complete enumeration of all subsets |
| Memoized | O(n*W) | O(n*W) | Cache subproblem results |
| Bottom-Up DP | O(n*W) | O(n*W) | Build solution iteratively |
| Space-Optimized DP | O(n*W) | O(W) | Only need previous row |

### Time Complexity
- **Time**: O(n*W) - For each of n items, consider each capacity up to W
- **Space**: O(W) - Only one array of size W+1 needed for space-optimized version

### Why This Solution Works
- **Optimal Substructure**: Maximum value with capacity j depends on maximum value with smaller capacities
- **Overlapping Subproblems**: Same subproblems are solved multiple times
- **DP Optimization**: Bottom-up approach avoids redundant calculations
- **Backward Iteration**: Critical for space-optimized version to maintain correctness

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Knapsack 1 - Item Selection Reconstruction**
**Problem**: Find maximum value and reconstruct which items were selected.

**Implementation**:
```python
def knapsack_1_with_items(n, w, weights, values):
    """
    DP solution with item selection reconstruction
    
    Args:
        n: number of items
        w: knapsack capacity
        weights: list of item weights
        values: list of item values
    
    Returns:
        tuple: (maximum value, list of selected item indices)
    """
    dp = [[0] * (w + 1) for _ in range(n + 1)]
    selected = [[False] * (w + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(w + 1):
            dp[i][j] = dp[i - 1][j]
            selected[i][j] = False
            
            if weights[i - 1] <= j:
                take_value = dp[i - 1][j - weights[i - 1]] + values[i - 1]
                if take_value > dp[i][j]:
                    dp[i][j] = take_value
                    selected[i][j] = True
    
    # Reconstruct selected items
    items = []
    current_capacity = w
    for i in range(n, 0, -1):
        if selected[i][current_capacity]:
            items.append(i - 1)  # Convert to 0-indexed
            current_capacity -= weights[i - 1]
    
    items.reverse()
    return dp[n][w], items

# Example usage
n, w = 3, 8
weights = [3, 4, 5]
values = [30, 50, 60]
max_value, selected_items = knapsack_1_with_items(n, w, weights, values)
print(f"Maximum value: {max_value}")  # Output: 90
print(f"Selected items: {selected_items}")  # Output: [0, 2] (items 1 and 3)
```

#### **2. Knapsack 1 - Count Solutions**
**Problem**: Count the number of ways to achieve maximum value.

**Implementation**:
```python
def knapsack_1_count_ways(n, w, weights, values):
    """
    Count number of ways to achieve maximum value
    
    Args:
        n: number of items
        w: knapsack capacity
        weights: list of item weights
        values: list of item values
    
    Returns:
        int: number of ways to achieve maximum value
    """
    # First, find maximum value
    dp = [0] * (w + 1)
    for i in range(n):
        for j in range(w, weights[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
    
    max_value = dp[w]
    
    # Count ways to achieve max_value
    # ways[j] = number of ways to achieve value using capacity j
    ways = [0] * (w + 1)
    ways[0] = 1
    
    for i in range(n):
        for j in range(w, weights[i] - 1, -1):
            if dp[j - weights[i]] + values[i] == max_value or \
               (dp[j - weights[i]] + values[i] == dp[j] and ways[j - weights[i]] > 0):
                ways[j] += ways[j - weights[i]]
    
    return ways[w]

# Example usage
n, w = 3, 8
weights = [3, 4, 5]
values = [30, 50, 60]
result = knapsack_1_count_ways(n, w, weights, values)
print(f"Number of ways: {result}")
```

### Related Problems

#### **AtCoder Problems**
- [Knapsack 2](https://atcoder.jp/contests/dp/tasks/dp_e) - Same problem with different constraints (large values, small weights)

#### **CSES Problems**
- [Book Shop](https://cses.fi/problemset/task/1158) - Similar knapsack problem
- [Money Sums](https://cses.fi/problemset/task/1745) - Related DP problem

#### **LeetCode Problems**
- [0/1 Knapsack](https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/) - Classic problem
- [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) - Knapsack variant
- [Target Sum](https://leetcode.com/problems/target-sum/) - Knapsack variant

#### **Problem Categories**
- **0/1 Knapsack**: Classic DP problem
- **2D DP**: Two-dimensional state space
- **Optimization**: Maximum value problems

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming Introduction](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP fundamentals
- [Knapsack Problems](https://cp-algorithms.com/dynamic_programming/knapsack.html) - Knapsack algorithms

### **Practice Problems**
- [AtCoder DP Contest Problem D](https://atcoder.jp/contests/dp/tasks/dp_d) - Original problem
- [AtCoder DP Contest Problem E](https://atcoder.jp/contests/dp/tasks/dp_e) - Next problem (Knapsack 2)
- [CSES Book Shop](https://cses.fi/problemset/task/1158) - Similar problem

### **Further Reading**
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms) - Dynamic Programming chapter
- [Competitive Programming Handbook](https://cses.fi/book/book.pdf) - DP section

