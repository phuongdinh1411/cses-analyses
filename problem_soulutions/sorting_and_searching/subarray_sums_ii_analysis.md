---
layout: simple
title: "Subarray Sums Ii"
permalink: /problem_soulutions/sorting_and_searching/subarray_sums_ii_analysis
---

# Subarray Sums Ii

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of hash map technique for counting subarrays
- Apply prefix sums and hash map for efficient subarray counting
- Implement efficient solutions for subarray sum problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in hash map counting problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Hash maps, prefix sums, counting, optimization, two-sum technique
- **Data Structures**: Arrays, hash maps, prefix sum arrays
- **Mathematical Concepts**: Counting theory, optimization theory, hash map operations
- **Programming Skills**: Algorithm implementation, complexity analysis, hash map usage
- **Related Problems**: Subarray Sums I (prefix sums), Sum of Two Values (hash map), Maximum Subarray Sum (Kadane's algorithm)

## 📋 Problem Description

You are given an array of n integers and a target sum x. Count the number of subarrays whose sum equals x.

**Input**: 
- First line: two integers n and x (array size and target sum)
- Second line: n integers a[1], a[2], ..., a[n] (array elements)

**Output**: 
- Print one integer: the number of subarrays whose sum equals x

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ x ≤ 10⁹
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
5 7
2 4 1 2 7

Output:
3

Explanation**: 
Array: [2, 4, 1, 2, 7], target sum = 7

Subarrays with sum = 7:
1. [2, 4, 1] → sum = 2 + 4 + 1 = 7 ✓
2. [4, 1, 2] → sum = 4 + 1 + 2 = 7 ✓
3. [7] → sum = 7 ✓

Total: 3 subarrays
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Subarrays

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays and count those with sum equal to target
- **Complete Coverage**: Guaranteed to find all subarrays with target sum
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Cubic time complexity

**Key Insight**: For each possible subarray, calculate its sum and check if it equals the target.

**Algorithm**:
- For each starting position i:
  - For each ending position j (j ≥ i):
    - Calculate sum of subarray from i to j
    - If sum == target, increment result
- Return the result

**Visual Example**:
```
Array: [2, 4, 1, 2, 7], target = 7

All subarrays:
- [2] → sum = 2 ✗
- [2, 4] → sum = 6 ✗
- [2, 4, 1] → sum = 7 ✓
- [2, 4, 1, 2] → sum = 9 ✗
- [2, 4, 1, 2, 7] → sum = 16 ✗
- [4] → sum = 4 ✗
- [4, 1] → sum = 5 ✗
- [4, 1, 2] → sum = 7 ✓
- [4, 1, 2, 7] → sum = 14 ✗
- [1] → sum = 1 ✗
- [1, 2] → sum = 3 ✗
- [1, 2, 7] → sum = 10 ✗
- [2] → sum = 2 ✗
- [2, 7] → sum = 9 ✗
- [7] → sum = 7 ✓

Count: 3 subarrays
```

**Implementation**:
```python
def brute_force_subarray_sums_ii(arr, target):
    """
    Count subarrays with target sum using brute force approach
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        int: number of subarrays with target sum
    """
    count = 0
    n = len(arr)
    
    for i in range(n):
        for j in range(i, n):
            # Calculate sum of subarray from i to j
            current_sum = sum(arr[i:j+1])
            if current_sum == target:
                count += 1
    
    return count

# Example usage
arr = [2, 4, 1, 2, 7]
target = 7
result = brute_force_subarray_sums_ii(arr, target)
print(f"Brute force result: {result}")  # Output: 3
```

**Time Complexity**: O(n³) - Nested loops with sum calculation
**Space Complexity**: O(1) - Constant space

**Why it's inefficient**: Cubic time complexity makes it very slow for large inputs.

---

### Approach 2: Optimized - Use Prefix Sums

**Key Insights from Optimized Approach**:
- **Prefix Sums**: Use prefix sums to calculate subarray sums efficiently
- **Efficient Sum Calculation**: Avoid recalculating sums for each subarray
- **Better Complexity**: Achieve O(n²) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use prefix sums to calculate subarray sums in O(1) time instead of O(n) time.

**Algorithm**:
- Precompute prefix sums for the array
- For each starting position i:
  - For each ending position j (j ≥ i):
    - Calculate sum using prefix sums: prefix[j+1] - prefix[i]
    - If sum == target, increment result
- Return the result

**Visual Example**:
```
Array: [2, 4, 1, 2, 7], target = 7

Prefix sums: [0, 2, 6, 7, 9, 16]

Subarray sums using prefix sums:
- [2] → prefix[1] - prefix[0] = 2 - 0 = 2 ✗
- [2, 4] → prefix[2] - prefix[0] = 6 - 0 = 6 ✗
- [2, 4, 1] → prefix[3] - prefix[0] = 7 - 0 = 7 ✓
- [2, 4, 1, 2] → prefix[4] - prefix[0] = 9 - 0 = 9 ✗
- [2, 4, 1, 2, 7] → prefix[5] - prefix[0] = 16 - 0 = 16 ✗
- [4] → prefix[2] - prefix[1] = 6 - 2 = 4 ✗
- [4, 1] → prefix[3] - prefix[1] = 7 - 2 = 5 ✗
- [4, 1, 2] → prefix[4] - prefix[1] = 9 - 2 = 7 ✓
- [4, 1, 2, 7] → prefix[5] - prefix[1] = 16 - 2 = 14 ✗
- [1] → prefix[3] - prefix[2] = 7 - 6 = 1 ✗
- [1, 2] → prefix[4] - prefix[2] = 9 - 6 = 3 ✗
- [1, 2, 7] → prefix[5] - prefix[2] = 16 - 6 = 10 ✗
- [2] → prefix[4] - prefix[3] = 9 - 7 = 2 ✗
- [2, 7] → prefix[5] - prefix[3] = 16 - 7 = 9 ✗
- [7] → prefix[5] - prefix[4] = 16 - 9 = 7 ✓

Count: 3 subarrays
```

**Implementation**:
```python
def optimized_subarray_sums_ii(arr, target):
    """
    Count subarrays with target sum using optimized prefix sums approach
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        int: number of subarrays with target sum
    """
    n = len(arr)
    count = 0
    
    # Precompute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    for i in range(n):
        for j in range(i, n):
            # Calculate sum using prefix sums
            current_sum = prefix[j + 1] - prefix[i]
            if current_sum == target:
                count += 1
    
    return count

# Example usage
arr = [2, 4, 1, 2, 7]
target = 7
result = optimized_subarray_sums_ii(arr, target)
print(f"Optimized result: {result}")  # Output: 3
```

**Time Complexity**: O(n²) - Nested loops with O(1) sum calculation
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: More efficient than brute force with prefix sum optimization.

---

### Approach 3: Optimal - Use Hash Map

**Key Insights from Optimal Approach**:
- **Hash Map**: Use hash map to count prefix sums efficiently
- **Optimal Complexity**: Achieve O(n) time complexity
- **Efficient Implementation**: Single pass through array
- **Mathematical Insight**: Use hash map to count occurrences of (prefix_sum - target)

**Key Insight**: If prefix[i] - prefix[j] = target, then prefix[i] = prefix[j] + target. Use hash map to count occurrences of (prefix_sum - target).

**Algorithm**:
- Use hash map to count occurrences of each prefix sum
- For each position, check if (current_prefix_sum - target) exists in hash map
- Add current prefix sum to hash map
- Return the result

**Visual Example**:
```
Array: [2, 4, 1, 2, 7], target = 7

Prefix sums: [0, 2, 6, 7, 9, 16]
Hash map: {0: 1, 2: 1, 6: 1, 7: 1, 9: 1, 16: 1}

Processing:
- i=0, prefix=0: Look for 0-7=-7, not found, count=0
- i=1, prefix=2: Look for 2-7=-5, not found, count=0
- i=2, prefix=6: Look for 6-7=-1, not found, count=0
- i=3, prefix=7: Look for 7-7=0, found (count=1), count=1
- i=4, prefix=9: Look for 9-7=2, found (count=1), count=2
- i=5, prefix=16: Look for 16-7=9, found (count=1), count=3

Total count: 3
```

**Implementation**:
```python
def optimal_subarray_sums_ii(arr, target):
    """
    Count subarrays with target sum using optimal hash map approach
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        int: number of subarrays with target sum
    """
    n = len(arr)
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}  # Initialize with prefix sum 0
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # Check if (prefix_sum - target) exists
        if (prefix_sum - target) in sum_count:
            count += sum_count[prefix_sum - target]
        
        # Add current prefix sum to hash map
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count

# Example usage
arr = [2, 4, 1, 2, 7]
target = 7
result = optimal_subarray_sums_ii(arr, target)
print(f"Optimal result: {result}")  # Output: 3
```

**Time Complexity**: O(n) - Single pass through array
**Space Complexity**: O(n) - Hash map for prefix sums

**Why it's optimal**: Achieves the best possible time complexity with hash map optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all subarrays |
| Prefix Sums | O(n²) | O(n) | Use prefix sums for efficient calculation |
| Hash Map | O(n) | O(n) | Count prefix sums with hash map |

### Time Complexity
- **Time**: O(n) - Hash map approach provides optimal time complexity
- **Space**: O(n) - Hash map for prefix sum counting

### Why This Solution Works
- **Hash Map Technique**: Use hash map to count occurrences of (prefix_sum - target) for efficient subarray counting
- **Optimal Algorithm**: Hash map approach is the standard solution for this problem
- **Optimal Approach**: Single pass through array provides the most efficient solution for subarray sum counting problems
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
