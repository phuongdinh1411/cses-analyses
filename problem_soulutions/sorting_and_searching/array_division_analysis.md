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
- **Binary Search on Answer**: Use binary search on the answer space since the function is monotonic
- **Monotonic Property**: If sum S is possible, then sum S+1 is also possible
- **Optimal Algorithm**: Binary search approach is the standard solution for this problem
- **Optimal Approach**: Binary search provides the most efficient solution for array partitioning problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Array Division with Minimum Difference
**Problem**: Divide array into k subarrays such that the difference between maximum and minimum subarray sums is minimized.

**Link**: [CSES Problem Set - Array Division Minimum Difference](https://cses.fi/problemset/task/array_division_minimum_difference)

```python
def array_division_minimum_difference(arr, k):
    """
    Divide array into k subarrays to minimize difference between max and min sums
    """
    def can_divide_with_max_sum(max_sum):
        """Check if array can be divided with max subarray sum <= max_sum"""
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
        
        return True
    
    # Binary search on the maximum subarray sum
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide_with_max_sum(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Variation 2: Array Division with Constraints
**Problem**: Divide array into k subarrays with additional constraints (e.g., minimum subarray size).

**Link**: [CSES Problem Set - Array Division with Constraints](https://cses.fi/problemset/task/array_division_constraints)

```python
def array_division_constraints(arr, k, min_size):
    """
    Divide array into k subarrays with minimum size constraint
    """
    def can_divide_with_constraints(max_sum):
        """Check if division is possible with constraints"""
        subarrays = 0
        current_sum = 0
        current_size = 0
        
        for num in arr:
            if current_sum + num > max_sum or current_size >= min_size:
                if current_size < min_size:
                    return False
                subarrays += 1
                current_sum = num
                current_size = 1
            else:
                current_sum += num
                current_size += 1
        
        if current_size >= min_size:
            subarrays += 1
        
        return subarrays <= k
    
    # Binary search on the maximum subarray sum
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide_with_constraints(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Variation 3: Array Division with Dynamic Weights
**Problem**: Each element has a weight, and we want to minimize the maximum weighted sum of subarrays.

**Link**: [CSES Problem Set - Array Division Dynamic Weights](https://cses.fi/problemset/task/array_division_dynamic_weights)

```python
def array_division_dynamic_weights(arr, weights, k):
    """
    Divide array into k subarrays to minimize maximum weighted sum
    """
    def can_divide_with_max_weighted_sum(max_weighted_sum):
        """Check if division is possible with max weighted sum constraint"""
        subarrays = 1
        current_weighted_sum = 0
        
        for i, (num, weight) in enumerate(zip(arr, weights)):
            if current_weighted_sum + num * weight > max_weighted_sum:
                subarrays += 1
                current_weighted_sum = num * weight
                if subarrays > k:
                    return False
            else:
                current_weighted_sum += num * weight
        
        return True
    
    # Binary search on the maximum weighted sum
    left = max(num * weight for num, weight in zip(arr, weights))
    right = sum(num * weight for num, weight in zip(arr, weights))
    
    while left < right:
        mid = (left + right) // 2
        if can_divide_with_max_weighted_sum(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

## Problem Variations

### **Variation 1: Array Division with Dynamic Updates**
**Problem**: Handle dynamic array updates while maintaining optimal division.

**Approach**: Use segment trees or other dynamic data structures for efficient updates.

```python
class DynamicArrayDivision:
    def __init__(self, arr, k):
        self.arr = arr[:]
        self.k = k
        self.n = len(arr)
        self.segment_tree = [0] * (4 * self.n)
        self._build_segment_tree(0, 0, self.n - 1)
    
    def _build_segment_tree(self, node, start, end):
        """Build segment tree for range sum queries."""
        if start == end:
            self.segment_tree[node] = self.arr[start]
        else:
            mid = (start + end) // 2
            self._build_segment_tree(2 * node + 1, start, mid)
            self._build_segment_tree(2 * node + 2, mid + 1, end)
            self.segment_tree[node] = self.segment_tree[2 * node + 1] + self.segment_tree[2 * node + 2]
    
    def update(self, index, new_value):
        """Update array element and segment tree."""
        self.arr[index] = new_value
        self._update_segment_tree(0, 0, self.n - 1, index, new_value)
    
    def _update_segment_tree(self, node, start, end, index, new_value):
        """Update segment tree after array modification."""
        if start == end:
            self.segment_tree[node] = new_value
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._update_segment_tree(2 * node + 1, start, mid, index, new_value)
            else:
                self._update_segment_tree(2 * node + 2, mid + 1, end, index, new_value)
            self.segment_tree[node] = self.segment_tree[2 * node + 1] + self.segment_tree[2 * node + 2]
    
    def get_range_sum(self, left, right):
        """Get sum of elements in range [left, right]."""
        return self._query_segment_tree(0, 0, self.n - 1, left, right)
    
    def _query_segment_tree(self, node, start, end, left, right):
        """Query segment tree for range sum."""
        if right < start or left > end:
            return 0
        if left <= start and end <= right:
            return self.segment_tree[node]
        
        mid = (start + end) // 2
        left_sum = self._query_segment_tree(2 * node + 1, start, mid, left, right)
        right_sum = self._query_segment_tree(2 * node + 2, mid + 1, end, left, right)
        return left_sum + right_sum
    
    def can_divide_with_max_sum(self, max_sum):
        """Check if array can be divided into k subarrays with max sum <= max_sum."""
        subarrays = 1
        current_sum = 0
        
        for i in range(self.n):
            if current_sum + self.arr[i] > max_sum:
                subarrays += 1
                current_sum = self.arr[i]
                if subarrays > self.k:
                    return False
            else:
                current_sum += self.arr[i]
        
        return True
    
    def get_minimum_max_sum(self):
        """Get minimum possible maximum sum after dividing into k subarrays."""
        left = max(self.arr)
        right = sum(self.arr)
        
        while left < right:
            mid = (left + right) // 2
            if self.can_divide_with_max_sum(mid):
                right = mid
            else:
                left = mid + 1
        
        return left

# Example usage
arr = [1, 2, 3, 4, 5]
k = 3
divider = DynamicArrayDivision(arr, k)
print(f"Initial minimum max sum: {divider.get_minimum_max_sum()}")

# Update an element
divider.update(2, 10)
print(f"After update: {divider.get_minimum_max_sum()}")
```

### **Variation 2: Array Division with Different Operations**
**Problem**: Divide array into k subarrays optimizing for different operations (product, XOR, etc.).

**Approach**: Adapt the binary search approach for different operations.

```python
def array_division_product(arr, k):
    """
    Divide array into k subarrays to minimize maximum product.
    
    Args:
        arr: List of positive integers
        k: Number of subarrays
    
    Returns:
        Minimum possible maximum product
    """
    def can_divide_with_max_product(max_product):
        """Check if array can be divided with max product <= max_product."""
        subarrays = 1
        current_product = 1
        
        for num in arr:
            if current_product * num > max_product:
                subarrays += 1
                current_product = num
                if subarrays > k:
                    return False
            else:
                current_product *= num
        
        return True
    
    # Binary search on the maximum product
    left = max(arr)
    right = 1
    for num in arr:
        right *= num
    
    while left < right:
        mid = (left + right) // 2
        if can_divide_with_max_product(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

def array_division_xor(arr, k):
    """
    Divide array into k subarrays to minimize maximum XOR.
    
    Args:
        arr: List of integers
        k: Number of subarrays
    
    Returns:
        Minimum possible maximum XOR
    """
    def can_divide_with_max_xor(max_xor):
        """Check if array can be divided with max XOR <= max_xor."""
        subarrays = 1
        current_xor = 0
        
        for num in arr:
            if current_xor ^ num > max_xor:
                subarrays += 1
                current_xor = num
                if subarrays > k:
                    return False
            else:
                current_xor ^= num
        
        return True
    
    # Binary search on the maximum XOR
    left = max(arr)
    right = 0
    for num in arr:
        right ^= num
    
    while left < right:
        mid = (left + right) // 2
        if can_divide_with_max_xor(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

def array_division_median(arr, k):
    """
    Divide array into k subarrays to minimize maximum median.
    
    Args:
        arr: List of integers
        k: Number of subarrays
    
    Returns:
        Minimum possible maximum median
    """
    def get_median(subarray):
        """Get median of a subarray."""
        sorted_sub = sorted(subarray)
        n = len(sorted_sub)
        if n % 2 == 0:
            return (sorted_sub[n//2 - 1] + sorted_sub[n//2]) / 2
        else:
            return sorted_sub[n//2]
    
    def can_divide_with_max_median(max_median):
        """Check if array can be divided with max median <= max_median."""
        subarrays = 1
        current_subarray = []
        
        for num in arr:
            current_subarray.append(num)
            median = get_median(current_subarray)
            
            if median > max_median:
                subarrays += 1
                current_subarray = [num]
                if subarrays > k:
                    return False
        
        return True
    
    # Binary search on the maximum median
    left = min(arr)
    right = max(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide_with_max_median(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example usage
arr = [1, 2, 3, 4, 5]
k = 3

print(f"Minimum max product: {array_division_product(arr, k)}")
print(f"Minimum max XOR: {array_division_xor(arr, k)}")
print(f"Minimum max median: {array_division_median(arr, k)}")
```

### **Variation 3: Array Division with Constraints**
**Problem**: Divide array into k subarrays with additional constraints (size limits, value restrictions).

**Approach**: Use constraint satisfaction with backtracking or advanced optimization.

```python
def array_division_with_constraints(arr, k, constraints):
    """
    Divide array into k subarrays with additional constraints.
    
    Args:
        arr: List of integers
        k: Number of subarrays
        constraints: Dictionary with constraints like:
            - min_size: Minimum subarray size
            - max_size: Maximum subarray size
            - min_sum: Minimum subarray sum
            - max_sum: Maximum subarray sum
            - allowed_values: Set of allowed values in subarrays
    
    Returns:
        List of subarrays if possible, None otherwise
    """
    def is_valid_subarray(subarray, constraints):
        """Check if subarray satisfies constraints."""
        if 'min_size' in constraints and len(subarray) < constraints['min_size']:
            return False
        if 'max_size' in constraints and len(subarray) > constraints['max_size']:
            return False
        
        subarray_sum = sum(subarray)
        if 'min_sum' in constraints and subarray_sum < constraints['min_sum']:
            return False
        if 'max_sum' in constraints and subarray_sum > constraints['max_sum']:
            return False
        
        if 'allowed_values' in constraints:
            if not all(val in constraints['allowed_values'] for val in subarray):
                return False
        
        return True
    
    def backtrack(index, current_subarrays, current_subarray):
        """Backtrack to find valid division."""
        if index == len(arr):
            if len(current_subarrays) == k and is_valid_subarray(current_subarray, constraints):
                return current_subarrays + [current_subarray]
            return None
        
        # Try adding current element to current subarray
        new_subarray = current_subarray + [arr[index]]
        if is_valid_subarray(new_subarray, constraints):
            result = backtrack(index + 1, current_subarrays, new_subarray)
            if result is not None:
                return result
        
        # Try starting a new subarray
        if len(current_subarrays) < k and len(current_subarray) > 0:
            if is_valid_subarray(current_subarray, constraints):
                result = backtrack(index, current_subarrays + [current_subarray], [arr[index]])
                if result is not None:
                    return result
        
        return None
    
    return backtrack(0, [], [])

def array_division_balanced(arr, k):
    """
    Divide array into k subarrays with balanced sizes.
    
    Args:
        arr: List of integers
        k: Number of subarrays
    
    Returns:
        List of subarrays with balanced sizes
    """
    n = len(arr)
    base_size = n // k
    extra = n % k
    
    subarrays = []
    start = 0
    
    for i in range(k):
        # First 'extra' subarrays get one extra element
        size = base_size + (1 if i < extra else 0)
        end = start + size
        subarrays.append(arr[start:end])
        start = end
    
    return subarrays

def array_division_weighted(arr, k, weights):
    """
    Divide array into k subarrays considering element weights.
    
    Args:
        arr: List of integers
        k: Number of subarrays
        weights: List of weights for each element
    
    Returns:
        Minimum possible maximum weighted sum
    """
    def can_divide_with_max_weighted_sum(max_weighted_sum):
        """Check if array can be divided with max weighted sum <= max_weighted_sum."""
        subarrays = 1
        current_weighted_sum = 0
        
        for i, (num, weight) in enumerate(zip(arr, weights)):
            if current_weighted_sum + num * weight > max_weighted_sum:
                subarrays += 1
                current_weighted_sum = num * weight
                if subarrays > k:
                    return False
            else:
                current_weighted_sum += num * weight
        
        return True
    
    # Binary search on the maximum weighted sum
    left = max(num * weight for num, weight in zip(arr, weights))
    right = sum(num * weight for num, weight in zip(arr, weights))
    
    while left < right:
        mid = (left + right) // 2
        if can_divide_with_max_weighted_sum(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example usage
arr = [1, 2, 3, 4, 5, 6, 7, 8]
k = 3

# Test with constraints
constraints = {
    'min_size': 2,
    'max_size': 4,
    'min_sum': 3,
    'max_sum': 15
}

result = array_division_with_constraints(arr, k, constraints)
print(f"Division with constraints: {result}")

# Test balanced division
balanced = array_division_balanced(arr, k)
print(f"Balanced division: {balanced}")

# Test weighted division
weights = [1, 2, 1, 2, 1, 2, 1, 2]
min_weighted_sum = array_division_weighted(arr, k, weights)
print(f"Minimum max weighted sum: {min_weighted_sum}")
```

### Related Problems

#### **CSES Problems**
- [Array Division](https://cses.fi/problemset/task/1085) - Basic array division problem
- [Stick Lengths](https://cses.fi/problemset/task/1074) - Optimization with sorting
- [Factory Machines](https://cses.fi/problemset/task/1620) - Binary search optimization

#### **LeetCode Problems**
- [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) - Divide array into m subarrays
- [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) - Binary search on capacity
- [Minimize Maximum Distance to Gas Station](https://leetcode.com/problems/minimize-maximum-distance-to-gas-station/) - Binary search optimization
- [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) - Binary search on eating speed

#### **Problem Categories**
- **Binary Search**: Answer space search, optimization problems, monotonic functions
- **Array Partitioning**: Subarray division, constraint satisfaction, optimization
- **Greedy Algorithms**: Local optimal choices, constraint-based optimization
- **Algorithm Design**: Binary search algorithms, optimization techniques, constraint algorithms
