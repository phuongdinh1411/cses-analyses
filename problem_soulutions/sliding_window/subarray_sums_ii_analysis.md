---
layout: simple
title: "Subarray Sums II - Count Subarrays with Sum X (Advanced)"
permalink: /problem_soulutions/sliding_window/subarray_sums_ii_analysis
---

# Subarray Sums II - Count Subarrays with Sum X (Advanced)

## 📋 Problem Description

Given an array of n integers, find the number of subarrays with sum x. This is an advanced version with additional constraints and variations.

**Input**: 
- First line: Two integers n and x (array size and target sum)
- Second line: n integers a₁, a₂, ..., aₙ (array contents)

**Output**: 
- One integer: the number of subarrays with sum x

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- −10⁹ ≤ x, aᵢ ≤ 10⁹
- Array may contain negative numbers
- Multiple subarrays may have the same sum

**Example**:
```
Input:
5 7
2 -1 3 5 -2

Output:
2
```

**Explanation**: The subarrays with sum 7 are:
- [2, -1, 3, 5, -2] → sum = 2 + (-1) + 3 + 5 + (-2) = 7
- [3, 5, -1] → sum = 3 + 5 + (-1) = 7

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count subarrays with exactly sum x
- **Key Insight**: Use prefix sum to find subarray sums efficiently
- **Challenge**: Handle negative numbers, multiple occurrences, and edge cases

### Step 2: Brute Force Approach
**Check all possible subarrays and calculate their sums:**

```python
def subarray_sums_naive(n, x, arr):
    count = 0
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum == x:
                count += 1
    
    return count
```

**Complexity**: O(n²) - too slow for large arrays

### Step 3: Optimization
**Use prefix sum with hash map for efficient counting:**

```python
def subarray_sums_prefix_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count
```

**Key Insight**: Use prefix sum difference to find subarrays with target sum

### Step 4: Complete Solution

```python
def solve_subarray_sums_ii():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = count_subarrays_with_sum_advanced(n, x, arr)
    print(result)

def count_subarrays_with_sum_advanced(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count

if __name__ == "__main__":
    solve_subarray_sums_ii()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 7, [2, -1, 3, 5, -2]), 2),
        ((4, 6, [1, 2, 3, 4]), 1),
        ((3, 0, [1, -1, 0]), 3),
        ((2, 5, [1, 4]), 1),
        ((1, 1, [1]), 1),
        ((4, 10, [2, 3, 4, 1]), 1),
        ((5, 0, [1, -1, 1, -1, 1]), 5),
        ((3, -2, [-1, -1, 0]), 2),
    ]
    
    for (n, x, arr), expected in test_cases:
        result = count_subarrays_with_sum_advanced(n, x, arr)
        print(f"n={n}, x={x}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def count_subarrays_with_sum_advanced(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    
    for num in arr:
        prefix_sum += num
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with prefix sum
- **Space**: O(n) - hash map to store prefix sum frequencies

### Why This Solution Works
- **Prefix Sum**: Efficiently calculates subarray sums
- **Hash Map**: Tracks frequency of prefix sums for O(1) lookup
- **Difference Calculation**: Uses prefix_sum - x to find target subarrays
- **Optimal Algorithm**: Best known approach for this problem

## 🎯 Key Insights

### 1. **Prefix Sum Technique**
- Convert range queries to point queries
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Hash Map for Frequency**
- Track frequency of prefix sums efficiently
- Important for understanding
- Enable O(1) lookup time
- Essential for algorithm

### 3. **Subarray Sum Calculation**
- Use prefix sum difference for subarray sums
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Subarray Sums with Maximum Length Constraint
**Problem**: Count subarrays with sum x and length at most k.

```python
def count_subarrays_with_sum_max_length(n, x, k, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(list)  # Map sum to list of indices
    sum_count[0] = [-1]  # Empty subarray at index -1
    
    for i, num in enumerate(arr):
        prefix_sum += num
        
        if prefix_sum - x in sum_count:
            # Check if any previous index gives us length <= k
            for prev_idx in sum_count[prefix_sum - x]:
                if i - prev_idx <= k:
                    count += 1
        
        sum_count[prefix_sum].append(i)
    
    return count

# Example usage
result = count_subarrays_with_sum_max_length(5, 7, 3, [2, -1, 3, 5, -2])
print(f"Subarrays with sum 7 and length <= 3: {result}")
```

### Variation 2: Subarray Sums with Non-Negative Constraint
**Problem**: Count subarrays with sum x where all elements are non-negative.

```python
def count_subarrays_with_sum_non_negative(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    
    for i, num in enumerate(arr):
        if num < 0:
            # Reset for negative numbers
            sum_count.clear()
            sum_count[0] = 1
            prefix_sum = 0
            continue
            
        prefix_sum += num
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count

# Example usage
result = count_subarrays_with_sum_non_negative(5, 7, [2, -1, 3, 5, -2])
print(f"Subarrays with sum 7 and non-negative elements: {result}")
```

### Variation 3: Subarray Sums with Circular Array
**Problem**: Count subarrays with sum x in a circular array.

```python
def count_subarrays_with_sum_circular(n, x, arr):
    from collections import defaultdict
    
    # Extend array to handle circular nature
    extended_arr = arr + arr
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    
    for i, num in enumerate(extended_arr):
        prefix_sum += num
        
        # Only count if subarray length <= n
        if i >= n:
            # Remove contribution from elements outside original array
            old_prefix = prefix_sum - sum(extended_arr[i-n+1:i+1])
            if old_prefix in sum_count:
                sum_count[old_prefix] -= 1
        
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count

# Example usage
result = count_subarrays_with_sum_circular(5, 7, [2, -1, 3, 5, -2])
print(f"Circular subarrays with sum 7: {result}")
```

### Variation 4: Subarray Sums with K Different Values
**Problem**: Count subarrays with sum x and exactly k different values.

```python
def count_subarrays_with_sum_and_k_values(n, x, k, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    
    for i in range(n):
        # Check subarrays ending at i
        current_sum = 0
        distinct_values = set()
        
        for j in range(i, -1, -1):
            current_sum += arr[j]
            distinct_values.add(arr[j])
            
            if current_sum == x and len(distinct_values) == k:
                count += 1
    
    return count

# Example usage
result = count_subarrays_with_sum_and_k_values(5, 7, 3, [2, -1, 3, 5, -2])
print(f"Subarrays with sum 7 and exactly 3 different values: {result}")
```

### Variation 5: Subarray Sums with Range Queries and Updates
**Problem**: Answer queries about subarray sums with target x, with array updates.

```python
class SubarraySumCounter:
    def __init__(self, arr):
        self.arr = arr.copy()
        self.n = len(arr)
        self.prefix_sums = [0] * (self.n + 1)
        self.update_prefix_sums()
    
    def update_prefix_sums(self):
        """Update prefix sums after array changes"""
        for i in range(self.n):
            self.prefix_sums[i + 1] = self.prefix_sums[i] + self.arr[i]
    
    def update_element(self, index, new_value):
        """Update element at index"""
        if 0 <= index < self.n:
            self.arr[index] = new_value
            self.update_prefix_sums()
    
    def count_subarrays_with_sum(self, x):
        """Count subarrays with sum x"""
        from collections import defaultdict
        
        count = 0
        sum_count = defaultdict(int)
        sum_count[0] = 1
        
        for i in range(1, self.n + 1):
            prefix_sum = self.prefix_sums[i]
            count += sum_count[prefix_sum - x]
            sum_count[prefix_sum] += 1
        
        return count

# Example usage
counter = SubarraySumCounter([2, -1, 3, 5, -2])
print(f"Initial count with sum 7: {counter.count_subarrays_with_sum(7)}")

counter.update_element(1, 2)  # Change -1 to 2
print(f"After update, count with sum 7: {counter.count_subarrays_with_sum(7)}")
```

## 🔗 Related Problems

- **[Subarray Sums I](/cses-analyses/problem_soulutions/sliding_window/)**: Basic subarray sum counting
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray existence problems
- **[Longest Subarray with Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Longest subarray problems

## 📚 Learning Points

1. **Prefix Sum Technique**: Essential for subarray sum problems
2. **Hash Map for Frequency**: Important for efficient counting
3. **Subarray Sum Calculation**: Key for understanding prefix sum differences
4. **Advanced Constraints**: Important for handling complex variations
5. **Dynamic Updates**: Key for problems with array modifications

---

**This is a great introduction to advanced subarray sum counting problems!** 🎯