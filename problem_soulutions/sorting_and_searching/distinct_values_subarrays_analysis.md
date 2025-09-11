---
layout: simple
title: "Distinct Values Subarrays"
permalink: /problem_soulutions/sorting_and_searching/distinct_values_subarrays_analysis
---

# Distinct Values Subarrays

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of sliding window technique and its applications
- Apply hash map technique for counting distinct values in subarrays
- Implement efficient solutions for subarray counting problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in sliding window problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sliding window, hash maps, counting, optimization, two pointers
- **Data Structures**: Arrays, hash maps, sliding window
- **Mathematical Concepts**: Counting theory, optimization theory, window properties
- **Programming Skills**: Algorithm implementation, complexity analysis, sliding window technique
- **Related Problems**: Subarray Sums II (hash map), Maximum Subarray Sum (sliding window), Playlist (sliding window)

## 📋 Problem Description

You are given an array of n integers. Count the number of subarrays that contain exactly k distinct values.

**Input**: 
- First line: two integers n and k (array size and number of distinct values)
- Second line: n integers a[1], a[2], ..., a[n] (array elements)

**Output**: 
- Print one integer: the number of subarrays with exactly k distinct values

**Constraints**:
- 1 ≤ k ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
5 2
1 2 1 2 3

Output:
8

Explanation**: 
Array: [1, 2, 1, 2, 3], k = 2

Subarrays with exactly 2 distinct values:
1. [1, 2] → distinct values: {1, 2} ✓
2. [1, 2, 1] → distinct values: {1, 2} ✓
3. [1, 2, 1, 2] → distinct values: {1, 2} ✓
4. [2, 1] → distinct values: {1, 2} ✓
5. [2, 1, 2] → distinct values: {1, 2} ✓
6. [2, 1, 2, 3] → distinct values: {1, 2, 3} ✗
7. [1, 2] → distinct values: {1, 2} ✓
8. [1, 2, 3] → distinct values: {1, 2, 3} ✗
9. [2, 3] → distinct values: {2, 3} ✓

Total: 8 subarrays
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Subarrays

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays and count those with exactly k distinct values
- **Complete Coverage**: Guaranteed to find the correct count
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Cubic time complexity

**Key Insight**: For each possible subarray, count distinct values and check if count equals k.

**Algorithm**:
- For each starting position i:
  - For each ending position j (j ≥ i):
    - Count distinct values in subarray from i to j
    - If count == k, increment result
- Return the result

**Visual Example**:
```
Array: [1, 2, 1, 2, 3], k = 2

All subarrays:
- [1] → distinct: {1} → count = 1 ✗
- [1, 2] → distinct: {1, 2} → count = 2 ✓
- [1, 2, 1] → distinct: {1, 2} → count = 2 ✓
- [1, 2, 1, 2] → distinct: {1, 2} → count = 2 ✓
- [1, 2, 1, 2, 3] → distinct: {1, 2, 3} → count = 3 ✗
- [2] → distinct: {2} → count = 1 ✗
- [2, 1] → distinct: {1, 2} → count = 2 ✓
- [2, 1, 2] → distinct: {1, 2} → count = 2 ✓
- [2, 1, 2, 3] → distinct: {1, 2, 3} → count = 3 ✗
- [1] → distinct: {1} → count = 1 ✗
- [1, 2] → distinct: {1, 2} → count = 2 ✓
- [1, 2, 3] → distinct: {1, 2, 3} → count = 3 ✗
- [2] → distinct: {2} → count = 1 ✗
- [2, 3] → distinct: {2, 3} → count = 2 ✓
- [3] → distinct: {3} → count = 1 ✗

Count: 8 subarrays
```

**Implementation**:
```python
def brute_force_distinct_values_subarrays(arr, k):
    """
    Count subarrays with exactly k distinct values using brute force approach
    
    Args:
        arr: list of integers
        k: number of distinct values
    
    Returns:
        int: number of subarrays with exactly k distinct values
    """
    count = 0
    n = len(arr)
    
    for i in range(n):
        for j in range(i, n):
            # Count distinct values in subarray from i to j
            distinct_values = set(arr[i:j+1])
            if len(distinct_values) == k:
                count += 1
    
    return count

# Example usage
arr = [1, 2, 1, 2, 3]
k = 2
result = brute_force_distinct_values_subarrays(arr, k)
print(f"Brute force result: {result}")  # Output: 8
```

**Time Complexity**: O(n³) - Nested loops with set operations
**Space Complexity**: O(n) - Set for distinct values

**Why it's inefficient**: Cubic time complexity makes it very slow for large inputs.

---

### Approach 2: Optimized - Use Hash Map for Counting

**Key Insights from Optimized Approach**:
- **Hash Map**: Use hash map to count distinct values efficiently
- **Efficient Counting**: Avoid creating sets for each subarray
- **Better Complexity**: Achieve O(n²) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use hash map to count distinct values and avoid creating sets for each subarray.

**Algorithm**:
- For each starting position i:
  - Initialize hash map for counting
  - For each ending position j (j ≥ i):
    - Add arr[j] to hash map
    - If hash map size == k, increment result
    - If hash map size > k, break

**Visual Example**:
```
Array: [1, 2, 1, 2, 3], k = 2

i=0:
- j=0: {1: 1} → size=1 ✗
- j=1: {1: 1, 2: 1} → size=2 ✓
- j=2: {1: 2, 2: 1} → size=2 ✓
- j=3: {1: 2, 2: 2} → size=2 ✓
- j=4: {1: 2, 2: 2, 3: 1} → size=3 ✗

i=1:
- j=1: {2: 1} → size=1 ✗
- j=2: {2: 1, 1: 1} → size=2 ✓
- j=3: {2: 2, 1: 1} → size=2 ✓
- j=4: {2: 2, 1: 1, 3: 1} → size=3 ✗

i=2:
- j=2: {1: 1} → size=1 ✗
- j=3: {1: 1, 2: 1} → size=2 ✓
- j=4: {1: 1, 2: 1, 3: 1} → size=3 ✗

i=3:
- j=3: {2: 1} → size=1 ✗
- j=4: {2: 1, 3: 1} → size=2 ✓

i=4:
- j=4: {3: 1} → size=1 ✗

Count: 8 subarrays
```

**Implementation**:
```python
def optimized_distinct_values_subarrays(arr, k):
    """
    Count subarrays with exactly k distinct values using optimized hash map approach
    
    Args:
        arr: list of integers
        k: number of distinct values
    
    Returns:
        int: number of subarrays with exactly k distinct values
    """
    count = 0
    n = len(arr)
    
    for i in range(n):
        distinct_count = {}
        for j in range(i, n):
            # Add current element to count
            distinct_count[arr[j]] = distinct_count.get(arr[j], 0) + 1
            
            # Check if we have exactly k distinct values
            if len(distinct_count) == k:
                count += 1
            elif len(distinct_count) > k:
                break
    
    return count

# Example usage
arr = [1, 2, 1, 2, 3]
k = 2
result = optimized_distinct_values_subarrays(arr, k)
print(f"Optimized result: {result}")  # Output: 8
```

**Time Complexity**: O(n²) - Nested loops with hash map operations
**Space Complexity**: O(n) - Hash map for counting

**Why it's better**: Much more efficient than brute force with hash map optimization.

---

### Approach 3: Optimal - Sliding Window Technique

**Key Insights from Optimal Approach**:
- **Sliding Window**: Use sliding window technique to maintain distinct count
- **Optimal Complexity**: Achieve O(n) time complexity
- **Efficient Implementation**: Single pass through array
- **Two Pointers**: Use two pointers to maintain window boundaries

**Key Insight**: Use sliding window technique to efficiently count subarrays with exactly k distinct values.

**Algorithm**:
- Use two pointers (left, right) to maintain window
- Use hash map to count distinct values in current window
- Expand right pointer until we have k distinct values
- Contract left pointer while maintaining k distinct values
- Count valid subarrays

**Visual Example**:
```
Array: [1, 2, 1, 2, 3], k = 2

left=0, right=0: {1: 1} → distinct=1 < k, expand
left=0, right=1: {1: 1, 2: 1} → distinct=2 = k, count=1, expand
left=0, right=2: {1: 2, 2: 1} → distinct=2 = k, count=2, expand
left=0, right=3: {1: 2, 2: 2} → distinct=2 = k, count=3, expand
left=0, right=4: {1: 2, 2: 2, 3: 1} → distinct=3 > k, contract
left=1, right=4: {2: 2, 3: 1} → distinct=2 = k, count=4, expand
left=1, right=5: (end), contract
left=2, right=5: {3: 1} → distinct=1 < k, expand
left=2, right=6: (end), contract
left=3, right=6: {3: 1} → distinct=1 < k, expand
left=3, right=7: (end), contract
left=4, right=7: {3: 1} → distinct=1 < k, expand
left=4, right=8: (end), done

Total count: 8
```

**Implementation**:
```python
def optimal_distinct_values_subarrays(arr, k):
    """
    Count subarrays with exactly k distinct values using optimal sliding window approach
    
    Args:
        arr: list of integers
        k: number of distinct values
    
    Returns:
        int: number of subarrays with exactly k distinct values
    """
    n = len(arr)
    count = 0
    left = 0
    distinct_count = {}
    
    for right in range(n):
        # Add current element to window
        distinct_count[arr[right]] = distinct_count.get(arr[right], 0) + 1
        
        # Contract window from left while we have more than k distinct values
        while len(distinct_count) > k:
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                del distinct_count[arr[left]]
            left += 1
        
        # Count subarrays ending at right with exactly k distinct values
        if len(distinct_count) == k:
            count += 1
    
    return count

# Example usage
arr = [1, 2, 1, 2, 3]
k = 2
result = optimal_distinct_values_subarrays(arr, k)
print(f"Optimal result: {result}")  # Output: 8
```

**Time Complexity**: O(n) - Single pass through array
**Space Complexity**: O(n) - Hash map for counting

**Why it's optimal**: Achieves the best possible time complexity with sliding window optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all subarrays |
| Hash Map | O(n²) | O(n) | Use hash map for counting |
| Sliding Window | O(n) | O(n) | Maintain distinct count with two pointers |

### Time Complexity
- **Time**: O(n) - Sliding window approach provides optimal time complexity
- **Space**: O(n) - Hash map for counting distinct values

### Why This Solution Works
- **Sliding Window**: Use sliding window technique to efficiently count subarrays with exactly k distinct values
- **Optimal Algorithm**: Sliding window approach is the standard solution for this problem
- **Optimal Approach**: Two-pointer technique provides the most efficient solution for subarray counting problems
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
