---
layout: simple
title: "Array Division"
permalink: /problem_soulutions/sorting_and_searching/array_division_analysis
---

# Array Division

## Problem Description

**Problem**: Given an array of n integers, divide it into k subarrays such that the maximum sum of any subarray is minimized.

**Input**: 
- First line: n and k (size of array and number of subarrays)
- Second line: n integers a₁, a₂, ..., aₙ

**Output**: Print the minimum possible maximum sum of any subarray.

**Example**:
```
Input:
5 3
2 4 7 3 5

Output:
7

Explanation: One optimal division is [2,4], [7], [3,5] with sums 6, 7, 8. Maximum is 8.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Divide array into exactly k subarrays
- Minimize the maximum sum among all subarrays
- Each element must be in exactly one subarray
- Subarrays must be consecutive

**Key Observations:**
- If k = 1, answer is sum of entire array
- If k = n, answer is maximum element
- For other k, answer is between max(arr) and sum(arr)
- Can use binary search to find optimal value

### Step 2: Binary Search Approach
**Idea**: Use binary search to find the minimum maximum sum.

```python
def array_division_binary_search(n, k, arr):
    def can_divide(max_sum):
        subarrays = 1
        current_sum = 0
        
        for num in arr:
            if num > max_sum:
                return False  # Single element exceeds limit
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
            else:
                current_sum += num
        
        return subarrays <= k
    
    # Binary search bounds
    left = max(arr)  # Minimum possible answer
    right = sum(arr)  # Maximum possible answer
    
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

**Why this works:**
- Binary search on the answer space
- `can_divide()` checks if it's possible to divide with given max sum
- Greedy approach: add elements to current subarray until limit is reached

### Step 3: Optimized Binary Search
**Idea**: Optimize the binary search implementation.

```python
def array_division_optimized(n, k, arr):
    def can_divide(max_sum):
        subarrays = 1
        current_sum = 0
        
        for num in arr:
            if num > max_sum:
                return False
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
                if subarrays > k:
                    return False
            else:
                current_sum += num
        
        return subarrays <= k
    
    # Binary search
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

**Why this is better:**
- Early termination in `can_divide()`
- More efficient bounds checking
- Cleaner implementation

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_array_division():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    def can_divide(max_sum):
        subarrays = 1
        current_sum = 0
        
        for num in arr:
            if num > max_sum:
                return False
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
                if subarrays > k:
                    return False
            else:
                current_sum += num
        
        return subarrays <= k
    
    # Binary search
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    print(left)

# Main execution
if __name__ == "__main__":
    solve_array_division()
```

**Why this works:**
- Efficient binary search approach
- Handles all edge cases correctly
- Optimal time complexity

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 3, [2, 4, 7, 3, 5]), 8),
        ((4, 2, [1, 2, 3, 4]), 6),
        ((3, 3, [1, 2, 3]), 3),
        ((5, 1, [1, 2, 3, 4, 5]), 15),
    ]
    
    for (n, k, arr), expected in test_cases:
        result = solve_test(n, k, arr)
        print(f"n = {n}, k = {k}, arr = {arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, k, arr):
    def can_divide(max_sum):
        subarrays = 1
        current_sum = 0
        
        for num in arr:
            if num > max_sum:
                return False
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
                if subarrays > k:
                    return False
            else:
                current_sum += num
        
        return subarrays <= k
    
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log(sum(arr))) - binary search with linear check
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Binary Search**: Efficiently finds optimal value
- **Greedy Check**: `can_divide()` uses greedy approach
- **Correct Bounds**: Search space is properly bounded

## 🎯 Key Insights

### 1. **Binary Search on Answer**
- Search space: [max(arr), sum(arr)]
- Each check takes O(n) time
- Total complexity: O(n log(sum(arr)))

### 2. **Greedy Division**
- Add elements to current subarray until limit
- Start new subarray when limit is exceeded
- This is optimal for given maximum sum

### 3. **Monotonicity**
- If max_sum works, any larger value also works
- If max_sum doesn't work, any smaller value also doesn't work
- This enables binary search

## 🎯 Problem Variations

### Variation 1: Minimum Sum Division
**Problem**: Divide array into k subarrays to minimize the minimum sum.

```python
def min_sum_division(n, k, arr):
    def can_divide(min_sum):
        subarrays = 0
        current_sum = 0
        
        for num in arr:
            current_sum += num
            if current_sum >= min_sum:
                subarrays += 1
                current_sum = 0
        
        return subarrays >= k
    
    # Binary search
    left = 0
    right = sum(arr)
    
    while left < right:
        mid = (left + right + 1) // 2
        if can_divide(mid):
            left = mid
        else:
            right = mid - 1
    
    return left
```

### Variation 2: Balanced Division
**Problem**: Divide array into k subarrays with minimum difference between max and min sums.

```python
def balanced_division(n, k, arr):
    def can_achieve_difference(diff):
        # Check if we can divide with max difference <= diff
        min_sum = max(arr)
        max_sum = min_sum + diff
        
        def can_divide_with_bounds(max_sum, min_sum):
            subarrays = 1
            current_sum = 0
            
            for num in arr:
                if num > max_sum:
                    return False
                if current_sum + num > max_sum:
                    subarrays += 1
                    current_sum = num
                else:
                    current_sum += num
            
            return subarrays <= k and current_sum >= min_sum
        
        return can_divide_with_bounds(max_sum, min_sum)
    
    # Binary search on difference
    left = 0
    right = sum(arr) - max(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_achieve_difference(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Variation 3: Weighted Division
**Problem**: Each subarray has a weight based on its sum. Minimize maximum weight.

```python
def weighted_division(n, k, arr, weights):
    def can_divide(max_weight):
        subarrays = 1
        current_sum = 0
        
        for num in arr:
            if current_sum + num > max_weight:
                subarrays += 1
                current_sum = num
                if subarrays > k:
                    return False
            else:
                current_sum += num
        
        return subarrays <= k
    
    # Binary search on weight
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Variation 4: Circular Array Division
**Problem**: Array is circular. Divide into k subarrays minimizing maximum sum.

```python
def circular_array_division(n, k, arr):
    def can_divide(max_sum):
        # Try all possible starting positions
        for start in range(n):
            subarrays = 1
            current_sum = 0
            
            for i in range(n):
                num = arr[(start + i) % n]
                if num > max_sum:
                    break
                if current_sum + num > max_sum:
                    subarrays += 1
                    current_sum = num
                    if subarrays > k:
                        break
                else:
                    current_sum += num
            else:
                return True
        
        return False
    
    # Binary search
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Variation 5: Constrained Division
**Problem**: Each subarray must have at least L and at most R elements.

```python
def constrained_division(n, k, arr, L, R):
    def can_divide(max_sum):
        subarrays = 0
        current_sum = 0
        current_length = 0
        
        for num in arr:
            if num > max_sum:
                return False
            
            if current_sum + num > max_sum or current_length >= R:
                if current_length < L:
                    return False
                subarrays += 1
                current_sum = num
                current_length = 1
            else:
                current_sum += num
                current_length += 1
        
        if current_length > 0:
            if current_length < L:
                return False
            subarrays += 1
        
        return subarrays <= k
    
    # Binary search
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

## 🔗 Related Problems

- **[Subarray Sums I](/cses-analyses/problem_soulutions/sorting_and_searching/subarray_sums_i_analysis)**: Subarray sum problems
- **[Subarray Sums II](/cses-analyses/problem_soulutions/sorting_and_searching/subarray_sums_ii_analysis)**: Advanced subarray problems
- **[Maximum Subarray Sum](/cses-analyses/problem_soulutions/sorting_and_searching/cses_maximum_subarray_sum_analysis)**: Maximum subarray problems

## 📚 Learning Points

1. **Binary Search on Answer**: Using binary search when answer is monotonic
2. **Greedy Algorithms**: Greedy approach for feasibility checking
3. **Subarray Problems**: Techniques for dividing arrays
4. **Optimization Problems**: Minimizing maximum values

---

**This is a great introduction to binary search and optimization problems!** 🎯 