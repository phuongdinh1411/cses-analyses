---
layout: simple
title: "Subarray Sums II - Advanced Hash Map Technique"
permalink: /problem_soulutions/sliding_window/subarray_sums_ii_analysis
---

# Subarray Sums II - Advanced Hash Map Technique

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement advanced hash map techniques for subarray sum problems
- Apply prefix sum concept to efficiently solve complex subarray problems
- Optimize subarray sum calculations using hash maps with advanced constraints
- Handle edge cases in advanced subarray sum problems
- Recognize when to use advanced hash map techniques

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Hash maps, prefix sums, subarray problems, advanced counting
- **Data Structures**: Arrays, hash maps, prefix sums
- **Mathematical Concepts**: Subarray sum optimization, prefix sum properties, advanced counting
- **Programming Skills**: Array manipulation, hash map implementation, advanced counting
- **Related Problems**: Subarray sums I, subarray with given sum, longest subarray with sum

## 📋 Problem Description

Given an array of integers and a target sum, count the number of contiguous subarrays that sum to the target value, with additional constraints.

**Input**: 
- First line: n (number of elements) and target (target sum)
- Second line: n integers separated by spaces

**Output**: 
- Single integer: number of subarrays with sum equal to target

**Constraints**:
- 1 ≤ n ≤ 10⁵
- -10⁴ ≤ arr[i] ≤ 10⁴
- -10⁹ ≤ target ≤ 10⁹

**Example**:
```
Input:
6 7
1 4 20 3 10 5

Output:
1

Explanation**: 
The subarray [20, 3, 10] has sum 33.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n³)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each starting position i from 0 to n-1
2. For each ending position j from i to n-1
3. Calculate sum of subarray from i to j
4. If sum equals target, increment counter
5. Return counter

**Implementation**:
```python
def brute_force_subarray_sums_ii(arr, target):
    n = len(arr)
    count = 0
    
    for i in range(n):
        for j in range(i, n):
            current_sum = sum(arr[i:j+1])
            if current_sum == target:
                count += 1
    
    return count
```

### Approach 2: Optimized with Prefix Sums
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. Calculate prefix sum array
2. For each starting position i, for each ending position j
3. Calculate subarray sum using prefix sums
4. If sum equals target, increment counter
5. Return counter

**Implementation**:
```python
def optimized_subarray_sums_ii(arr, target):
    n = len(arr)
    
    prefix = [0] * n
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i-1] + arr[i]
    
    count = 0
    
    for i in range(n):
        for j in range(i, n):
            if i == 0:
                current_sum = prefix[j]
            else:
                current_sum = prefix[j] - prefix[i-1]
            if current_sum == target:
                count += 1
    
    return count
```

### Approach 3: Optimal with Hash Map
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Initialize hash map with {0: 1}
2. For each element, add to prefix sum
3. If (prefix_sum - target) exists in hash map, add its frequency to counter
4. Increment frequency of current prefix sum in hash map
5. Return counter

**Implementation**:
```python
def optimal_subarray_sums_ii(arr, target):
    n = len(arr)
    prefix_sum_map = {0: 1}
    prefix_sum = 0
    count = 0
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum - target in prefix_sum_map:
            count += prefix_sum_map[prefix_sum - target]
        
        prefix_sum_map[prefix_sum] = prefix_sum_map.get(prefix_sum, 0) + 1
    
    return count
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all possible subarrays |
| Optimized | O(n²) | O(n) | Use prefix sums for faster calculation |
| Optimal | O(n) | O(n) | Use hash map to count prefix sum frequencies |

### Time Complexity
- **Time**: O(n) - Single pass through the array
- **Space**: O(n) - Hash map for prefix sums

### Why This Solution Works
- **Hash Map Counting**: Use hash map to count frequencies of prefix sums
- **Prefix Sum Property**: If prefix[j] - prefix[i] = target, then subarray from i+1 to j has sum target
- **Frequency Counting**: Count how many times each prefix sum occurs
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Subarray Sums with Range Constraints**
**Problem**: Count subarrays with sum equal to target within a specific range [l, r].

**Key Differences**: Only count subarrays within a specific range

**Solution Approach**: Use prefix sums with range filtering

**Implementation**:
```python
def subarray_sums_range_constraints(arr, target, l, r):
    """
    Count subarrays with sum = target within range [l, r]
    """
    n = len(arr)
    if l < 0 or r >= n or l > r:
        return 0
    
    # Calculate prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    count = 0
    
    # Only consider subarrays within range [l, r]
    for i in range(l, r + 1):
        for j in range(i, r + 1):
            if prefix[j + 1] - prefix[i] == target:
                count += 1
    
    return count

# Example usage
arr = [1, 2, 3, 4, 5]
target = 7
l, r = 1, 3
result = subarray_sums_range_constraints(arr, target, l, r)
print(f"Subarrays with sum {target} in range [{l}, {r}]: {result}")  # Output: 1
```

#### **2. Subarray Sums with Multiple Targets**
**Problem**: Count subarrays with sum equal to any of the given targets.

**Key Differences**: Multiple target values instead of single target

**Solution Approach**: Use hash map with multiple target checking

**Implementation**:
```python
def subarray_sums_multiple_targets(arr, targets):
    """
    Count subarrays with sum equal to any of the given targets
    """
    n = len(arr)
    targets_set = set(targets)
    
    # Calculate prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    count = 0
    
    for i in range(n):
        for j in range(i, n):
            current_sum = prefix[j + 1] - prefix[i]
            if current_sum in targets_set:
                count += 1
    
    return count

# Example usage
arr = [1, 2, 3, 4, 5]
targets = [3, 7, 9]
result = subarray_sums_multiple_targets(arr, targets)
print(f"Subarrays with sum in {targets}: {result}")  # Output: 3
```

#### **3. Subarray Sums with Modulo Operations**
**Problem**: Count subarrays with sum congruent to target modulo m.

**Key Differences**: Use modulo arithmetic instead of exact equality

**Solution Approach**: Use prefix sums with modulo operations

**Implementation**:
```python
def subarray_sums_modulo(arr, target, m):
    """
    Count subarrays with sum ≡ target (mod m)
    """
    n = len(arr)
    
    # Calculate prefix sums with modulo
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = (prefix[i] + arr[i]) % m
    
    count = 0
    
    for i in range(n):
        for j in range(i, n):
            current_sum = (prefix[j + 1] - prefix[i]) % m
            if current_sum == target:
                count += 1
    
    return count

# Example usage
arr = [1, 2, 3, 4, 5]
target = 0
m = 3
result = subarray_sums_modulo(arr, target, m)
print(f"Subarrays with sum ≡ {target} (mod {m}): {result}")  # Output: 4
```

### Related Problems

#### **CSES Problems**
- [Subarray Sums II](https://cses.fi/problemset/task/2101) - Count subarrays with given sum
- [Subarray Sums I](https://cses.fi/problemset/task/2102) - Count subarrays with given sum (simpler version)
- [Maximum Subarray Sum](https://cses.fi/problemset/task/2103) - Find maximum sum of subarray

#### **LeetCode Problems**
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) - Count subarrays with sum k
- [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/) - Subarray sum with modulo
- [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/) - Subarray product
- [Binary Subarray With Sum](https://leetcode.com/problems/binary-subarray-with-sum/) - Binary subarray with sum

#### **Problem Categories**
- **Hash Map**: Prefix sum counting, frequency tracking, efficient lookups
- **Prefix Sums**: Subarray sum calculation, range sum queries
- **Array Processing**: Subarray analysis, sum optimization, counting
- **Modulo Arithmetic**: Modular operations, congruence relations

## 🚀 Key Takeaways

- **Hash Map Counting**: The standard approach for counting subarray sums
- **Prefix Sum Property**: Use prefix sums to efficiently calculate subarray sums
- **Frequency Tracking**: Track frequencies of prefix sums to count valid subarrays
- **Edge Cases**: Handle subarrays starting from index 0 with {0: 1} initialization
- **Pattern Recognition**: This technique applies to many subarray sum counting problems