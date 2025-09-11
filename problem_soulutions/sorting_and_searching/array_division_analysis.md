---
layout: simple
title: "Array Division"
permalink: /problem_soulutions/sorting_and_searching/array_division_analysis
---

# Array Division

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of binary search on answer and its applications
- Apply binary search for optimization problems with monotonic properties
- Implement efficient solutions for array partitioning problems
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in binary search problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Binary search, optimization, array partitioning, monotonic functions
- **Data Structures**: Arrays, binary search implementation
- **Mathematical Concepts**: Optimization theory, monotonic functions, array partitioning
- **Programming Skills**: Algorithm implementation, complexity analysis, binary search
- **Related Problems**: Factory Machines (binary search on answer), Reading Books (optimization), Tasks and Deadlines (optimization)

## 📋 Problem Description

You are given an array of n integers. You need to divide the array into k subarrays such that the maximum sum of any subarray is minimized.

Find the minimum possible maximum sum.

**Input**: 
- First line: two integers n and k (array size and number of subarrays)
- Second line: n integers a[1], a[2], ..., a[n] (array elements)

**Output**: 
- Print one integer: the minimum possible maximum sum

**Constraints**:
- 1 ≤ k ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
5 3
4 2 4 5 1

Output:
6

Explanation**: 
Array: [4, 2, 4, 5, 1], k = 3

Optimal division:
- Subarray 1: [4, 2] → sum = 6
- Subarray 2: [4] → sum = 4
- Subarray 3: [5, 1] → sum = 6

Maximum sum: max(6, 4, 6) = 6

Alternative division:
- Subarray 1: [4] → sum = 4
- Subarray 2: [2, 4] → sum = 6
- Subarray 3: [5, 1] → sum = 6

Maximum sum: max(4, 6, 6) = 6

Minimum possible maximum sum: 6
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Divisions

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible ways to divide the array into k subarrays
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward approach with recursive partitioning
- **Inefficient**: Exponential time complexity

**Key Insight**: For each possible way to divide the array into k subarrays, calculate the maximum sum and find the minimum.

**Algorithm**:
- Use recursive approach to try all possible divisions
- For each division, calculate the maximum sum of subarrays
- Return the minimum maximum sum

**Visual Example**:
```
Array: [4, 2, 4, 5, 1], k = 3

All possible divisions:
1. [4] [2] [4,5,1] → max(4, 2, 10) = 10
2. [4] [2,4] [5,1] → max(4, 6, 6) = 6
3. [4] [2,4,5] [1] → max(4, 11, 1) = 11
4. [4,2] [4] [5,1] → max(6, 4, 6) = 6
5. [4,2] [4,5] [1] → max(6, 9, 1) = 9
6. [4,2,4] [5] [1] → max(10, 5, 1) = 10

Minimum maximum sum: 6
```

**Implementation**:
```python
def brute_force_array_division(arr, k):
    """
    Find minimum maximum sum using brute force approach
    
    Args:
        arr: list of integers
        k: number of subarrays
    
    Returns:
        int: minimum possible maximum sum
    """
    def try_divisions(start, remaining_k):
        if remaining_k == 1:
            return sum(arr[start:])
        
        min_max_sum = float('inf')
        for end in range(start + 1, len(arr) - remaining_k + 2):
            current_sum = sum(arr[start:end])
            remaining_max = try_divisions(end, remaining_k - 1)
            min_max_sum = min(min_max_sum, max(current_sum, remaining_max))
        
        return min_max_sum
    
    return try_divisions(0, k)

# Example usage
arr = [4, 2, 4, 5, 1]
k = 3
result = brute_force_array_division(arr, k)
print(f"Brute force result: {result}")  # Output: 6
```

**Time Complexity**: O(C(n-1, k-1) × n) - Try all combinations of divisions
**Space Complexity**: O(n) - Recursive call stack

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Dynamic Programming

**Key Insights from Optimized Approach**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Efficient Calculation**: Calculate optimal divisions for subproblems
- **Better Complexity**: Achieve O(n² × k) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use dynamic programming to store optimal solutions for subproblems.

**Algorithm**:
- dp[i][j] = minimum maximum sum for first i elements divided into j subarrays
- For each position, try all possible previous divisions

**Visual Example**:
```
Array: [4, 2, 4, 5, 1], k = 3

DP table:
dp[1][1] = 4
dp[2][1] = 6, dp[2][2] = max(4, 2) = 4
dp[3][1] = 10, dp[3][2] = min(max(4,6), max(6,4)) = 6, dp[3][3] = max(4,2,4) = 4
...

Final answer: dp[5][3] = 6
```

**Implementation**:
```python
def optimized_array_division(arr, k):
    """
    Find minimum maximum sum using dynamic programming
    
    Args:
        arr: list of integers
        k: number of subarrays
    
    Returns:
        int: minimum possible maximum sum
    """
    n = len(arr)
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(1, n + 1):
        dp[i][1] = sum(arr[:i])
    
    for i in range(1, n + 1):
        for j in range(2, min(i + 1, k + 1)):
            for l in range(j - 1, i):
                current_sum = sum(arr[l:i])
                dp[i][j] = min(dp[i][j], max(dp[l][j - 1], current_sum))
    
    return dp[n][k]

# Example usage
arr = [4, 2, 4, 5, 1]
k = 3
result = optimized_array_division(arr, k)
print(f"Optimized result: {result}")  # Output: 6
```

**Time Complexity**: O(n² × k) - DP with nested loops
**Space Complexity**: O(n × k) - DP table

**Why it's better**: Much more efficient than brute force with dynamic programming optimization.

---

### Approach 3: Optimal - Binary Search on Answer

**Key Insights from Optimal Approach**:
- **Binary Search**: Use binary search on the answer space
- **Monotonic Property**: If sum S is possible, then sum S+1 is also possible
- **Optimal Complexity**: Achieve O(n × log(sum)) time complexity
- **Efficient Implementation**: No need for complex DP

**Key Insight**: Use binary search on the answer space since the function is monotonic.

**Algorithm**:
- Binary search on the maximum sum from max_element to total_sum
- For each candidate sum, check if it's possible to divide array into k subarrays
- Use greedy approach to check feasibility

**Visual Example**:
```
Array: [4, 2, 4, 5, 1], k = 3
Search space: [5, 16] (max element to total sum)

Binary search:
- left=5, right=16, mid=10
  Can divide with max sum 10? Yes → search [5, 10]
- left=5, right=10, mid=7
  Can divide with max sum 7? No → search [8, 10]
- left=8, right=10, mid=9
  Can divide with max sum 9? No → search [10, 10]
- left=10, right=10 → answer = 10

Wait, let's check 6:
- Can divide with max sum 6? Yes → [4,2] [4] [5,1] → max(6,4,6) = 6 ✓
```

**Implementation**:
```python
def optimal_array_division(arr, k):
    """
    Find minimum maximum sum using binary search on answer
    
    Args:
        arr: list of integers
        k: number of subarrays
    
    Returns:
        int: minimum possible maximum sum
    """
    def can_divide(max_sum):
        """Check if we can divide array into k subarrays with max sum <= max_sum"""
        subarrays = 1
        current_sum = 0
        
        for num in arr:
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
                if subarrays > k:
                    return False
            else:
                current_sum += num
        
        return subarrays <= k
    
    left = max(arr)  # Minimum possible maximum sum
    right = sum(arr)  # Maximum possible maximum sum
    
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example usage
arr = [4, 2, 4, 5, 1]
k = 3
result = optimal_array_division(arr, k)
print(f"Optimal result: {result}")  # Output: 6
```

**Time Complexity**: O(n × log(sum)) - Binary search with linear feasibility check
**Space Complexity**: O(1) - Constant extra space

**Why it's optimal**: Achieves the best possible time complexity with binary search optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(C(n-1, k-1) × n) | O(n) | Try all divisions |
| Dynamic Programming | O(n² × k) | O(n × k) | Store subproblem solutions |
| Binary Search | O(n × log(sum)) | O(1) | Binary search on answer |

### Time Complexity
- **Time**: O(n × log(sum)) - Binary search approach provides optimal time complexity
- **Space**: O(1) - Constant extra space

### Why This Solution Works
- **Binary Search on Answer**: Use binary search on the answer space since the function is monotonic
- **Monotonic Property**: If sum S is possible, then sum S+1 is also possible
- **Optimal Algorithm**: Binary search approach is the standard solution for this problem
- **Optimal Approach**: Binary search provides the most efficient solution for array partitioning problems
- **Space**: O([complexity]) - [Explanation]

### Why This Solution Works
- **[Reason 1]**: [Explanation]
- **[Reason 2]**: [Explanation]
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
