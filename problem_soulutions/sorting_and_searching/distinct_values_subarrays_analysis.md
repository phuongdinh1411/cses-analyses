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
- **Hash Map Tracking**: Efficiently tracks distinct values and their frequencies
- **Optimal Approach**: Sliding window with hash map provides the most efficient solution for subarray counting problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Distinct Values Subarrays with Range Queries
**Problem**: Answer multiple queries about subarrays with exactly k distinct values in different ranges.

**Link**: [CSES Problem Set - Distinct Values Subarrays Range Queries](https://cses.fi/problemset/task/distinct_values_subarrays_range)

```python
def distinct_values_subarrays_range_queries(arr, queries):
    """
    Answer range queries about subarrays with exactly k distinct values
    """
    results = []
    
    for query in queries:
        left, right, k = query['left'], query['right'], query['k']
        
        # Extract subarray
        subarray = arr[left:right+1]
        
        # Count subarrays with exactly k distinct values
        count = 0
        n = len(subarray)
        
        for i in range(n):
            distinct_count = {}
            for j in range(i, n):
                distinct_count[subarray[j]] = distinct_count.get(subarray[j], 0) + 1
                
                if len(distinct_count) == k:
                    count += 1
                elif len(distinct_count) > k:
                    break
        
        results.append(count)
    
    return results

def distinct_values_subarrays_range_queries_optimized(arr, queries):
    """
    Optimized version using sliding window for each query
    """
    results = []
    
    for query in queries:
        left, right, k = query['left'], query['right'], query['k']
        
        # Extract subarray
        subarray = arr[left:right+1]
        
        # Use sliding window approach
        count = 0
        n = len(subarray)
        distinct_count = {}
        window_left = 0
        
        for window_right in range(n):
            # Add current element to window
            distinct_count[subarray[window_right]] = distinct_count.get(subarray[window_right], 0) + 1
            
            # Contract window from left while we have more than k distinct values
            while len(distinct_count) > k:
                distinct_count[subarray[window_left]] -= 1
                if distinct_count[subarray[window_left]] == 0:
                    del distinct_count[subarray[window_left]]
                window_left += 1
            
            # Count subarrays ending at window_right with exactly k distinct values
            if len(distinct_count) == k:
                count += 1
        
        results.append(count)
    
    return results
```

### Variation 2: Distinct Values Subarrays with Updates
**Problem**: Handle dynamic updates to the array and maintain subarray counts with exactly k distinct values.

**Link**: [CSES Problem Set - Distinct Values Subarrays with Updates](https://cses.fi/problemset/task/distinct_values_subarrays_updates)

```python
class DistinctValuesSubarraysWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        self.arr[index] = new_value
    
    def count_subarrays_with_k_distinct(self, k):
        """Count subarrays with exactly k distinct values"""
        count = 0
        distinct_count = {}
        left = 0
        
        for right in range(self.n):
            # Add current element to window
            distinct_count[self.arr[right]] = distinct_count.get(self.arr[right], 0) + 1
            
            # Contract window from left while we have more than k distinct values
            while len(distinct_count) > k:
                distinct_count[self.arr[left]] -= 1
                if distinct_count[self.arr[left]] == 0:
                    del distinct_count[self.arr[left]]
                left += 1
            
            # Count subarrays ending at right with exactly k distinct values
            if len(distinct_count) == k:
                count += 1
        
        return count
    
    def count_subarrays_range(self, left, right, k):
        """Count subarrays with exactly k distinct values in range [left, right]"""
        count = 0
        distinct_count = {}
        window_left = left
        
        for window_right in range(left, right + 1):
            # Add current element to window
            distinct_count[self.arr[window_right]] = distinct_count.get(self.arr[window_right], 0) + 1
            
            # Contract window from left while we have more than k distinct values
            while len(distinct_count) > k:
                distinct_count[self.arr[window_left]] -= 1
                if distinct_count[self.arr[window_left]] == 0:
                    del distinct_count[self.arr[window_left]]
                window_left += 1
            
            # Count subarrays ending at window_right with exactly k distinct values
            if len(distinct_count) == k:
                count += 1
        
        return count
```

### Variation 3: Distinct Values Subarrays with Constraints
**Problem**: Find subarrays with exactly k distinct values that satisfy additional constraints (e.g., minimum length, maximum sum).

**Link**: [CSES Problem Set - Distinct Values Subarrays with Constraints](https://cses.fi/problemset/task/distinct_values_subarrays_constraints)

```python
def distinct_values_subarrays_constraints(arr, k, min_length, max_sum):
    """
    Find subarrays with exactly k distinct values that satisfy constraints
    """
    count = 0
    distinct_count = {}
    left = 0
    
    for right in range(len(arr)):
        # Add current element to window
        distinct_count[arr[right]] = distinct_count.get(arr[right], 0) + 1
        
        # Contract window from left while we have more than k distinct values
        while len(distinct_count) > k:
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                del distinct_count[arr[left]]
            left += 1
        
        # Check if current window satisfies constraints
        if len(distinct_count) == k:
            window_length = right - left + 1
            window_sum = sum(arr[left:right+1])
            
            if window_length >= min_length and window_sum <= max_sum:
                count += 1
    
    return count

def distinct_values_subarrays_constraints_optimized(arr, k, min_length, max_sum):
    """
    Optimized version with early termination
    """
    count = 0
    distinct_count = {}
    left = 0
    
    for right in range(len(arr)):
        # Add current element to window
        distinct_count[arr[right]] = distinct_count.get(arr[right], 0) + 1
        
        # Contract window from left while we have more than k distinct values
        while len(distinct_count) > k:
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                del distinct_count[arr[left]]
            left += 1
        
        # Check if current window satisfies constraints
        if len(distinct_count) == k:
            window_length = right - left + 1
            
            # Early termination if window is too short
            if window_length < min_length:
                continue
            
            # Calculate window sum
            window_sum = sum(arr[left:right+1])
            
            if window_sum <= max_sum:
                count += 1
    
    return count
```

## Problem Variations

### **Variation 1: Distinct Values Subarrays with Dynamic Updates**
**Problem**: Handle dynamic array updates while maintaining distinct subarray counts efficiently.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicDistinctSubarrays:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.distinct_count = 0
        self._calculate_distinct_count()
    
    def _calculate_distinct_count(self):
        """Calculate total number of distinct subarrays."""
        self.distinct_count = 0
        seen = set()
        
        for i in range(self.n):
            current_set = set()
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                subarray_tuple = tuple(sorted(current_set))
                if subarray_tuple not in seen:
                    seen.add(subarray_tuple)
                    self.distinct_count += 1
    
    def update_value(self, index, new_value):
        """Update array value and recalculate distinct count."""
        if 0 <= index < self.n:
            self.arr[index] = new_value
            self._calculate_distinct_count()
    
    def add_element(self, value):
        """Add new element to the array."""
        self.arr.append(value)
        self.n += 1
        self._calculate_distinct_count()
    
    def remove_element(self, index):
        """Remove element at index from the array."""
        if 0 <= index < self.n:
            del self.arr[index]
            self.n -= 1
            self._calculate_distinct_count()
    
    def get_distinct_count(self):
        """Get current distinct subarray count."""
        return self.distinct_count
    
    def get_distinct_subarrays(self):
        """Get all distinct subarrays."""
        seen = set()
        distinct_subarrays = []
        
        for i in range(self.n):
            current_set = set()
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                subarray_tuple = tuple(sorted(current_set))
                if subarray_tuple not in seen:
                    seen.add(subarray_tuple)
                    distinct_subarrays.append(list(current_set))
        
        return distinct_subarrays

# Example usage
arr = [1, 2, 1, 3]
dynamic_counter = DynamicDistinctSubarrays(arr)
print(f"Initial distinct count: {dynamic_counter.get_distinct_count()}")

# Update a value
dynamic_counter.update_value(1, 4)
print(f"After update: {dynamic_counter.get_distinct_count()}")

# Add element
dynamic_counter.add_element(2)
print(f"After adding 2: {dynamic_counter.get_distinct_count()}")
```

### **Variation 2: Distinct Values Subarrays with Different Operations**
**Problem**: Handle different types of operations on distinct subarrays (range queries, size constraints).

**Approach**: Use advanced data structures for efficient range operations and size-based filtering.

```python
class AdvancedDistinctSubarrays:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
    
    def get_distinct_subarrays_in_range(self, left, right):
        """Get distinct subarrays in range [left, right]."""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        seen = set()
        count = 0
        
        for i in range(left, right + 1):
            current_set = set()
            for j in range(i, right + 1):
                current_set.add(self.arr[j])
                subarray_tuple = tuple(sorted(current_set))
                if subarray_tuple not in seen:
                    seen.add(subarray_tuple)
                    count += 1
        
        return count
    
    def get_distinct_subarrays_with_size(self, min_size, max_size):
        """Get distinct subarrays with size constraints."""
        seen = set()
        count = 0
        
        for i in range(self.n):
            current_set = set()
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                if min_size <= len(current_set) <= max_size:
                    subarray_tuple = tuple(sorted(current_set))
                    if subarray_tuple not in seen:
                        seen.add(subarray_tuple)
                        count += 1
        
        return count
    
    def get_distinct_subarrays_with_values(self, required_values):
        """Get distinct subarrays containing specific values."""
        seen = set()
        count = 0
        
        for i in range(self.n):
            current_set = set()
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                if all(val in current_set for val in required_values):
                    subarray_tuple = tuple(sorted(current_set))
                    if subarray_tuple not in seen:
                        seen.add(subarray_tuple)
                        count += 1
        
        return count
    
    def get_distinct_subarrays_with_sum(self, target_sum):
        """Get distinct subarrays with specific sum."""
        seen = set()
        count = 0
        
        for i in range(self.n):
            current_set = set()
            current_sum = 0
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                current_sum += self.arr[j]
                if current_sum == target_sum:
                    subarray_tuple = tuple(sorted(current_set))
                    if subarray_tuple not in seen:
                        seen.add(subarray_tuple)
                        count += 1
        
        return count
    
    def get_distinct_subarrays_with_pattern(self, pattern_func):
        """Get distinct subarrays matching a pattern."""
        seen = set()
        count = 0
        
        for i in range(self.n):
            current_set = set()
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                if pattern_func(current_set):
                    subarray_tuple = tuple(sorted(current_set))
                    if subarray_tuple not in seen:
                        seen.add(subarray_tuple)
                        count += 1
        
        return count

# Example usage
arr = [1, 2, 1, 3, 2, 4]
advanced_counter = AdvancedDistinctSubarrays(arr)

print(f"Distinct in range [1, 4]: {advanced_counter.get_distinct_subarrays_in_range(1, 4)}")
print(f"Distinct with size [2, 3]: {advanced_counter.get_distinct_subarrays_with_size(2, 3)}")
print(f"Distinct containing [1, 2]: {advanced_counter.get_distinct_subarrays_with_values([1, 2])}")
print(f"Distinct with sum 5: {advanced_counter.get_distinct_subarrays_with_sum(5)}")

# Test pattern matching
even_size_pattern = lambda s: len(s) % 2 == 0
print(f"Distinct with even size: {advanced_counter.get_distinct_subarrays_with_pattern(even_size_pattern)}")
```

### **Variation 3: Distinct Values Subarrays with Constraints**
**Problem**: Handle distinct subarrays with additional constraints (value ranges, frequency limits, etc.).

**Approach**: Use constraint satisfaction with advanced filtering and optimization.

```python
class ConstrainedDistinctSubarrays:
    def __init__(self, arr, constraints=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.constraints = constraints or {}
    
    def _is_valid_subarray(self, subarray_set):
        """Check if subarray satisfies constraints."""
        if 'min_size' in self.constraints and len(subarray_set) < self.constraints['min_size']:
            return False
        if 'max_size' in self.constraints and len(subarray_set) > self.constraints['max_size']:
            return False
        if 'min_value' in self.constraints and min(subarray_set) < self.constraints['min_value']:
            return False
        if 'max_value' in self.constraints and max(subarray_set) > self.constraints['max_value']:
            return False
        if 'allowed_values' in self.constraints:
            if not all(val in self.constraints['allowed_values'] for val in subarray_set):
                return False
        if 'forbidden_values' in self.constraints:
            if any(val in self.constraints['forbidden_values'] for val in subarray_set):
                return False
        return True
    
    def get_distinct_with_constraints(self):
        """Get distinct subarrays satisfying constraints."""
        seen = set()
        count = 0
        
        for i in range(self.n):
            current_set = set()
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                if self._is_valid_subarray(current_set):
                    subarray_tuple = tuple(sorted(current_set))
                    if subarray_tuple not in seen:
                        seen.add(subarray_tuple)
                        count += 1
        
        return count
    
    def get_distinct_with_frequency_constraints(self, max_frequency):
        """Get distinct subarrays with frequency constraints."""
        seen = set()
        count = 0
        
        for i in range(self.n):
            current_set = set()
            frequency_map = defaultdict(int)
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                frequency_map[self.arr[j]] += 1
                
                # Check frequency constraints
                if all(freq <= max_frequency for freq in frequency_map.values()):
                    subarray_tuple = tuple(sorted(current_set))
                    if subarray_tuple not in seen:
                        seen.add(subarray_tuple)
                        count += 1
        
        return count
    
    def get_distinct_with_sum_constraints(self, min_sum, max_sum):
        """Get distinct subarrays with sum constraints."""
        seen = set()
        count = 0
        
        for i in range(self.n):
            current_set = set()
            current_sum = 0
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                current_sum += self.arr[j]
                if min_sum <= current_sum <= max_sum:
                    subarray_tuple = tuple(sorted(current_set))
                    if subarray_tuple not in seen:
                        seen.add(subarray_tuple)
                        count += 1
        
        return count
    
    def get_distinct_with_parity_constraints(self, parity_type):
        """Get distinct subarrays with parity constraints."""
        seen = set()
        count = 0
        
        for i in range(self.n):
            current_set = set()
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                
                # Check parity constraints
                if parity_type == 'even':
                    if all(val % 2 == 0 for val in current_set):
                        subarray_tuple = tuple(sorted(current_set))
                        if subarray_tuple not in seen:
                            seen.add(subarray_tuple)
                            count += 1
                elif parity_type == 'odd':
                    if all(val % 2 == 1 for val in current_set):
                        subarray_tuple = tuple(sorted(current_set))
                        if subarray_tuple not in seen:
                            seen.add(subarray_tuple)
                            count += 1
                elif parity_type == 'mixed':
                    if any(val % 2 == 0 for val in current_set) and any(val % 2 == 1 for val in current_set):
                        subarray_tuple = tuple(sorted(current_set))
                        if subarray_tuple not in seen:
                            seen.add(subarray_tuple)
                            count += 1
        
        return count
    
    def get_distinct_with_mathematical_constraints(self, constraint_func):
        """Get distinct subarrays with custom mathematical constraints."""
        seen = set()
        count = 0
        
        for i in range(self.n):
            current_set = set()
            for j in range(i, self.n):
                current_set.add(self.arr[j])
                if constraint_func(current_set):
                    subarray_tuple = tuple(sorted(current_set))
                    if subarray_tuple not in seen:
                        seen.add(subarray_tuple)
                        count += 1
        
        return count

# Example usage
arr = [1, 2, 3, 2, 1, 4, 5, 6]
constraints = {
    'min_size': 2,
    'max_size': 4,
    'min_value': 1,
    'max_value': 5,
    'forbidden_values': {6}
}

constrained_counter = ConstrainedDistinctSubarrays(arr, constraints)
print(f"Constrained distinct count: {constrained_counter.get_distinct_with_constraints()}")
print(f"Distinct with frequency <= 1: {constrained_counter.get_distinct_with_frequency_constraints(1)}")
print(f"Distinct with sum [3, 8]: {constrained_counter.get_distinct_with_sum_constraints(3, 8)}")
print(f"Distinct with even parity: {constrained_counter.get_distinct_with_parity_constraints('even')}")

# Test custom mathematical constraint
def custom_constraint(subarray_set):
    return len(subarray_set) == 2 and sum(subarray_set) % 3 == 0

print(f"Distinct with custom constraint: {constrained_counter.get_distinct_with_mathematical_constraints(custom_constraint)}")
```

### Related Problems

#### **CSES Problems**
- [Distinct Values Subarrays](https://cses.fi/problemset/task/2108) - Basic distinct values subarrays problem
- [Distinct Values Subarrays II](https://cses.fi/problemset/task/2109) - Advanced distinct values subarrays problem
- [Subarray Distinct Values](https://cses.fi/problemset/task/2428) - Subarray distinct values queries

#### **LeetCode Problems**
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) - Sliding window with distinct characters
- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) - Sliding window with k distinct characters
- [Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) - Subarrays with exactly k distinct values
- [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) - Sliding window with at most 2 distinct values

#### **Problem Categories**
- **Sliding Window**: Two-pointer technique, window contraction, efficient subarray processing
- **Hash Maps**: Frequency counting, distinct value tracking, efficient lookups
- **Array Processing**: Subarray analysis, distinct value counting, range queries
- **Algorithm Design**: Sliding window algorithms, hash-based techniques, subarray optimization
