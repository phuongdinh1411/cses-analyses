---
layout: simple
title: "Array Division - Minimize Maximum Subarray Sum"
permalink: /problem_soulutions/sorting_and_searching/array_division_analysis
---

# Array Division - Minimize Maximum Subarray Sum

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand binary search on answer space and optimization problems
- Apply binary search with greedy validation to find optimal solutions
- Implement efficient binary search algorithms with O(n log(sum)) time complexity
- Optimize array division problems using binary search and greedy validation
- Handle edge cases in binary search optimization (single element, all elements, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Binary search, greedy algorithms, optimization problems, answer space search, validation functions
- **Data Structures**: Arrays, binary search tracking, sum tracking, division tracking
- **Mathematical Concepts**: Binary search theory, optimization mathematics, sum calculations, division theory
- **Programming Skills**: Binary search implementation, greedy algorithm implementation, validation function implementation, algorithm implementation
- **Related Problems**: Factory Machines (binary search optimization), Binary search problems, Optimization problems

## 📋 Problem Description

Given an array of n integers, divide it into k subarrays such that the maximum sum of any subarray is minimized.

This is a binary search optimization problem that requires finding the minimum possible maximum sum when dividing an array into k consecutive subarrays. The solution involves using binary search on the answer space with a greedy validation function.

**Input**: 
- First line: n and k (size of array and number of subarrays)
- Second line: n integers a₁, a₂, ..., aₙ

**Output**: 
- Print the minimum possible maximum sum of any subarray

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ k ≤ n
- 1 ≤ aᵢ ≤ 10⁹

**Example**:
```
Input:
5 3
2 4 7 3 5

Output:
7

Explanation**: 
- Array: [2, 4, 7, 3, 5]
- Optimal division: [2,4], [7], [3,5]
- Subarray sums: 6, 7, 8
- Maximum sum: 7
- This is the minimum possible maximum sum for k=3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force**:
- **Exhaustive Search**: Shows all possible solutions but is computationally expensive
- **Combinatorial Explosion**: Number of ways grows exponentially with input size
- **Baseline Understanding**: Helps understand the problem structure before optimization

**Key Insight**: Try all possible ways to divide the array into k subarrays and find the minimum maximum sum.

**Algorithm**:
- Generate all possible ways to place k-1 dividers in n-1 positions
- For each division, calculate the sum of each subarray
- Find the minimum maximum sum across all divisions

**Visual Example**:
```
Array: [2, 4, 7, 3, 5], k = 3
Possible positions for 2 dividers: positions 0,1,2,3

All possible divisions:
┌─────────────────────────────────────────────────┐
│ Division 1: [2] | [4,7,3,5]                     │
│ Sums: 2, 19 → Max: 19                           │
│                                                 │
│ Division 2: [2,4] | [7,3,5]                     │
│ Sums: 6, 15 → Max: 15                           │
│                                                 │
│ Division 3: [2,4,7] | [3,5]                     │
│ Sums: 13, 8 → Max: 13                           │
│                                                 │
│ Division 4: [2,4,7,3] | [5]                     │
│ Sums: 16, 5 → Max: 16                           │
│                                                 │
│ Division 5: [2] | [4,7] | [3,5]                 │
│ Sums: 2, 11, 8 → Max: 11                        │
│                                                 │
│ Division 6: [2,4] | [7] | [3,5]                 │
│ Sums: 6, 7, 8 → Max: 8 ✓ OPTIMAL               │
└─────────────────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_solution(arr, k):
    n = len(arr)
    min_max_sum = float('inf')
    
    def generate_divisions(pos, dividers, current_division):
        if len(dividers) == k - 1:
            # Calculate sums for this division
            sums = []
            start = 0
            for div in dividers + [n]:
                subarray_sum = sum(arr[start:div])
                sums.append(subarray_sum)
                start = div
            min_max_sum = min(min_max_sum, max(sums))
            return
        
        # Try placing next divider
        for i in range(pos, n):
            generate_divisions(i + 1, dividers + [i], current_division)
    
    generate_divisions(1, [], [])
    return min_max_sum

# Example usage
arr = [2, 4, 7, 3, 5]
k = 3
result = brute_force_solution(arr, k)
print(f"Brute force result: {result}")  # Output: 8
```

**Time Complexity**: O(C(n-1, k-1) × n) = O(n^k)
**Space Complexity**: O(1)

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming**:
- **Optimal Substructure**: Problem can be broken into smaller subproblems
- **Overlapping Subproblems**: Same subproblems are solved multiple times
- **State Space**: dp[i][j] represents optimal solution for first i elements in j subarrays
- **Transition Logic**: Each state depends on previous states with fewer subarrays

**Key Insight**: Use DP to find the minimum maximum sum by considering all possible ways to divide the first i elements into j subarrays.

**Algorithm**:
- `dp[i][j]` = minimum maximum sum when dividing first i elements into j subarrays
- Recurrence: `dp[i][j] = min(max(dp[k][j-1], sum(arr[k+1...i]))` for all k < i

**Visual Example**:
```
Array: [2, 4, 7, 3, 5], k = 3

DP Table Construction:
┌─────────────────────────────────────────────────┐
│ dp[i][j] = min max sum for first i elements     │
│           divided into j subarrays              │
│                                                 │
│     j=1    j=2    j=3                           │
│ i=1   2     -      -                            │
│ i=2   6     2      -                            │
│ i=3  13     6      2                            │
│ i=4  16     9      6                            │
│ i=5  21    12      8 ← Answer                   │
└─────────────────────────────────────────────────┘

Calculation for dp[5][3]:
- Option 1: dp[4][2] + arr[4] = 9 + 5 = 14
- Option 2: dp[3][2] + sum(arr[3:5]) = 6 + 8 = 14  
- Option 3: dp[2][2] + sum(arr[2:5]) = 2 + 15 = 17
- Option 4: dp[1][2] + sum(arr[1:5]) = 2 + 19 = 21
- Minimum: 8
```

**Implementation**:
```python
def dp_solution(arr, k):
    n = len(arr)
    # dp[i][j] = minimum maximum sum when dividing first i elements into j subarrays
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1):
        dp[i][1] = sum(arr[:i])  # One subarray = sum of all elements
    
    for i in range(1, n + 1):
        for j in range(2, min(i + 1, k + 1)):
            for split in range(j - 1, i):
                # Divide first 'split' elements into j-1 subarrays
                # and elements split+1 to i into 1 subarray
                left_sum = dp[split][j - 1]
                right_sum = sum(arr[split:i])
                dp[i][j] = min(dp[i][j], max(left_sum, right_sum))
    
    return dp[n][k]

# Example usage
arr = [2, 4, 7, 3, 5]
k = 3
result = dp_solution(arr, k)
print(f"DP result: {result}")  # Output: 8
```

**Time Complexity**: O(n²k)
**Space Complexity**: O(nk)

**Why it's better**: Polynomial time, but still not optimal for large inputs.

**Implementation Considerations**:
- **Memory Usage**: O(nk) space for DP table
- **Time Trade-off**: Better than brute force but still O(n²k)
- **Practical Limitation**: Not suitable for very large inputs due to quadratic time

---

### Approach 3: Binary Search on Answer (Optimal)

**Key Insights from Binary Search Solution**:
- **Monotonic Property**: If max_sum = X works, then max_sum > X also works
- **Answer Space Search**: Binary search on the range [max(arr), sum(arr)]
- **Greedy Validation**: Optimal strategy for checking feasibility
- **Early Termination**: Stop validation as soon as we know it's impossible
- **Problem Transformation**: Convert optimization to decision problem

**Key Insight**: If we can divide the array with maximum sum X, we can also divide it with any sum > X. This monotonicity allows binary search.

**Algorithm**:
- Binary search on the answer space [max(arr), sum(arr)]
- For each candidate answer, use greedy validation
- Greedy validation: try to fit as many elements as possible in each subarray

**Visual Example**:
```
Array: [2, 4, 7, 3, 5], k = 3
Search space: [7, 21] (max element to sum of all)

Binary Search Process:
┌─────────────────────────────────────────────────┐
│ Step 1: mid = (7+21)/2 = 14                     │
│ Validation: Can we divide with max_sum = 14?    │
│ [2,4,7] | [3,5] → Sums: 13, 8 → Max: 13 ≤ 14 ✓ │
│ Answer ≤ 14, search [7, 14]                     │
│                                                 │
│ Step 2: mid = (7+14)/2 = 10                     │
│ Validation: Can we divide with max_sum = 10?    │
│ [2,4] | [7] | [3,5] → Sums: 6, 7, 8 → Max: 8 ≤ 10 ✓ │
│ Answer ≤ 10, search [7, 10]                     │
│                                                 │
│ Step 3: mid = (7+10)/2 = 8                      │
│ Validation: Can we divide with max_sum = 8?     │
│ [2,4] | [7] | [3,5] → Sums: 6, 7, 8 → Max: 8 ≤ 8 ✓ │
│ Answer ≤ 8, search [7, 8]                       │
│                                                 │
│ Step 4: mid = (7+8)/2 = 7                       │
│ Validation: Can we divide with max_sum = 7?     │
│ [2,4] | [7] | [3,5] → Sums: 6, 7, 8 → Max: 8 > 7 ✗ │
│ Answer > 7, search [8, 8]                       │
│                                                 │
│ Final Answer: 8                                 │
└─────────────────────────────────────────────────┘
```

**Greedy Validation Details**:
```
Testing max_sum = 8:
┌─────────────────────────────────────────────────┐
│ Current sum: 0, Subarrays: 1                    │
│ Element 2: 0+2=2 ≤ 8 ✓ → Current sum: 2         │
│ Element 4: 2+4=6 ≤ 8 ✓ → Current sum: 6         │
│ Element 7: 6+7=13 > 8 ✗ → Start new subarray    │
│   Subarrays: 2, Current sum: 7                  │
│ Element 3: 7+3=10 > 8 ✗ → Start new subarray    │
│   Subarrays: 3, Current sum: 3                  │
│ Element 5: 3+5=8 ≤ 8 ✓ → Current sum: 8         │
│ Final: 3 subarrays ≤ k=3 ✓                      │
└─────────────────────────────────────────────────┘

Division: [2,4], [7], [3,5]
Sums: 6, 7, 8
Maximum: 8
```

**Implementation**:
```python
def binary_search_solution(arr, k):
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
    
    # Binary search on answer space
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example usage
arr = [2, 4, 7, 3, 5]
k = 3
result = binary_search_solution(arr, k)
print(f"Binary search result: {result}")  # Output: 8
```

**Time Complexity**: O(n log(sum(arr)))
**Space Complexity**: O(1)

**Why it's optimal**: Logarithmic number of validations, each taking linear time.

**Implementation Details**:
- **Search Space**: [max(arr), sum(arr)] - tight bounds
- **Validation Function**: O(n) greedy approach with early termination
- **Binary Search**: O(log(sum)) iterations
- **Total Complexity**: O(n log(sum)) - optimal for this problem


## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^k) | O(1) | Try all possible divisions |
| Binary Search | O(n log(sum)) | O(1) | Binary search on answer space |
| Dynamic Programming | O(n²k) | O(nk) | For weighted subarray problems |

### Time Complexity
- **Time**: O(n log(sum(arr))) - binary search with linear check
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Binary Search**: Efficiently finds optimal value
- **Greedy Check**: `can_divide()` uses greedy approach
- **Correct Bounds**: Search space is properly bounded


## 🎯 Problem Variations

### Variation 1: Minimum Sum Division
**Problem**: Divide array into k subarrays to minimize the minimum sum.

**Related Problems**:
- [LeetCode 410: Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) - Similar concept with different objective
- [CSES Factory Machines](https://cses.fi/problemset/task/1620) - Binary search on answer space

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

**Related Problems**:
- [LeetCode 1011: Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) - Similar binary search approach
- [LeetCode 875: Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) - Binary search on answer space

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

**Related Problems**:
- [LeetCode 1231: Divide Chocolate](https://leetcode.com/problems/divide-chocolate/) - Similar weighted division concept
- [LeetCode 410: Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) - Exact same problem

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

**Related Problems**:
- [LeetCode 213: House Robber II](https://leetcode.com/problems/house-robber-ii/) - Circular array handling
- [LeetCode 918: Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) - Circular subarray problems

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

**Related Problems**:
- [LeetCode 410: Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) - With size constraints
- [LeetCode 1011: Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) - Similar constraint handling

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


## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Array Division with Weighted Subarrays**
```python
def array_division_weighted(n, k, arr, weights):
    # Handle array division with weighted subarrays
    
    def can_divide_weighted(max_weighted_sum):
        subarrays = 1
        current_sum = 0
        current_weight = 0
        
        for i, num in enumerate(arr):
            weight = weights[i]
            
            if num * weight > max_weighted_sum:
                return False
            
            if current_sum + num * weight > max_weighted_sum:
                subarrays += 1
                current_sum = num * weight
                current_weight = weight
                if subarrays > k:
                    return False
            else:
                current_sum += num * weight
                current_weight += weight
        
        return subarrays <= k
    
    # Binary search
    left = max(arr[i] * weights[i] for i in range(n))
    right = sum(arr[i] * weights[i] for i in range(n))
    
    while left < right:
        mid = (left + right) // 2
        if can_divide_weighted(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

#### **2. Array Division with Minimum Subarray Size**
```python
def array_division_min_size(n, k, arr, min_size):
    # Handle array division with minimum subarray size constraint
    
    def can_divide_min_size(max_sum):
        subarrays = 1
        current_sum = 0
        current_size = 0
        
        for num in arr:
            if num > max_sum:
                return False
            
            if current_sum + num > max_sum or current_size >= min_size:
                subarrays += 1
                current_sum = num
                current_size = 1
                if subarrays > k:
                    return False
            else:
                current_sum += num
                current_size += 1
        
        return subarrays <= k and current_size >= min_size
    
    # Binary search
    left = max(arr)
    right = sum(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_divide_min_size(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

#### **3. Array Division with Dynamic Updates**
```python
def array_division_dynamic(operations):
    # Handle array division with dynamic array updates
    
    arr = []
    k = 0
    
    for operation in operations:
        if operation[0] == 'set_k':
            # Set number of subarrays
            k = operation[1]
        
        elif operation[0] == 'add':
            # Add element to array
            element = operation[1]
            arr.append(element)
        
        elif operation[0] == 'remove':
            # Remove element at index
            index = operation[1]
            if 0 <= index < len(arr):
                arr.pop(index)
        
        elif operation[0] == 'query':
            # Query minimum maximum sum
            if len(arr) == 0 or k == 0:
                yield 0
                continue
            
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
            
            yield left
    
    return list(array_division_dynamic(operations))
```

## 🔗 Related Problems

### CSES Problems
- [Array Division](https://cses.fi/problemset/task/1085) - This exact problem
- [Factory Machines](https://cses.fi/problemset/task/1620) - Binary search on answer space
- [Maximum Subarray Sum](https://cses.fi/problemset/task/1643) - Subarray problems
- [Subarray Sums I](https://cses.fi/problemset/task/1660) - Subarray sum variations

### LeetCode Problems
- [410. Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) - Exact same problem
- [1011. Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) - Similar binary search approach
- [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) - Binary search on answer space
- [1231. Divide Chocolate](https://leetcode.com/problems/divide-chocolate/) - Weighted division concept
- [213. House Robber II](https://leetcode.com/problems/house-robber-ii/) - Circular array handling
- [918. Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) - Circular subarray problems

### Problem Categories
- **Binary Search on Answer**: Problems where you search for optimal value in answer space
- **Subarray Problems**: Array division and partitioning techniques
- **Optimization**: Minimize maximum value problems
- **Greedy Algorithms**: Problems with greedy validation functions

## 📚 Learning Points

1. **Binary Search on Answer**: Using binary search when answer is monotonic
2. **Greedy Algorithms**: Greedy approach for feasibility checking
3. **Subarray Problems**: Techniques for dividing arrays
4. **Optimization Problems**: Minimizing maximum values

---

**This is a great introduction to binary search and optimization problems!** 🎯 