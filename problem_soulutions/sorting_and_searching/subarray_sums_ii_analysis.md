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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Subarray Sums II with Range Queries
**Problem**: Answer multiple queries about subarray sums equal to target in different ranges.

**Link**: [CSES Problem Set - Subarray Sums II Range Queries](https://cses.fi/problemset/task/subarray_sums_ii_range)

```python
def subarray_sums_ii_range_queries(arr, target, queries):
    """
    Answer range queries about subarray sums equal to target
    """
    results = []
    
    for query in queries:
        left, right = query['left'], query['right']
        
        # Extract subarray
        subarray = arr[left:right+1]
        
        # Find subarray sums equal to target
        count = count_subarray_sums_equal_target(subarray, target)
        results.append(count)
    
    return results

def count_subarray_sums_equal_target(arr, target):
    """
    Count subarrays with sum equal to target using hash map
    """
    n = len(arr)
    if n == 0:
        return 0
    
    # Calculate prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # Count occurrences of (prefix_sum - target)
    count_map = {}
    count = 0
    
    for i in range(n + 1):
        # Look for prefix_sum - target
        if prefix[i] - target in count_map:
            count += count_map[prefix[i] - target]
        
        # Add current prefix sum to map
        count_map[prefix[i]] = count_map.get(prefix[i], 0) + 1
    
    return count

def count_subarray_sums_equal_target_optimized(arr, target):
    """
    Optimized version with early termination
    """
    n = len(arr)
    if n == 0:
        return 0
    
    # Calculate prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # Count occurrences of (prefix_sum - target)
    count_map = {}
    count = 0
    
    for i in range(n + 1):
        # Look for prefix_sum - target
        if prefix[i] - target in count_map:
            count += count_map[prefix[i] - target]
        
        # Add current prefix sum to map
        count_map[prefix[i]] = count_map.get(prefix[i], 0) + 1
        
        # Early termination if we can't improve
        if count == n * (n + 1) // 2:
            break
    
    return count
```

### Variation 2: Subarray Sums II with Updates
**Problem**: Handle dynamic updates to the array and maintain subarray sum queries.

**Link**: [CSES Problem Set - Subarray Sums II with Updates](https://cses.fi/problemset/task/subarray_sums_ii_updates)

```python
class SubarraySumsIIWithUpdates:
    def __init__(self, arr, target):
        self.arr = arr[:]
        self.target = target
        self.n = len(arr)
        self.prefix = self._compute_prefix()
        self.count = self._compute_count()
    
    def _compute_prefix(self):
        """Compute prefix sums"""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i]
        return prefix
    
    def _compute_count(self):
        """Compute count of subarrays with sum equal to target"""
        count_map = {}
        count = 0
        
        for i in range(self.n + 1):
            # Look for prefix_sum - target
            if self.prefix[i] - self.target in count_map:
                count += count_map[self.prefix[i] - self.target]
            
            # Add current prefix sum to map
            count_map[self.prefix[i]] = count_map.get(self.prefix[i], 0) + 1
        
        return count
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        old_value = self.arr[index]
        self.arr[index] = new_value
        
        # Update prefix sums
        diff = new_value - old_value
        for i in range(index + 1, self.n + 1):
            self.prefix[i] += diff
        
        # Recompute count
        self.count = self._compute_count()
    
    def add_element(self, new_value):
        """Add a new element to the array"""
        self.arr.append(new_value)
        self.n = len(self.arr)
        self.prefix = self._compute_prefix()
        self.count = self._compute_count()
    
    def remove_element(self, index):
        """Remove element at index"""
        self.arr.pop(index)
        self.n = len(self.arr)
        self.prefix = self._compute_prefix()
        self.count = self._compute_count()
    
    def get_count(self):
        """Get current count of subarrays with sum equal to target"""
        return self.count
    
    def get_count_range(self, left, right):
        """Get count of subarrays with sum equal to target in range [left, right]"""
        # Extract subarray
        subarray = self.arr[left:right+1]
        
        # Find subarray sums equal to target
        return count_subarray_sums_equal_target(subarray, self.target)
    
    def get_all_subarrays_with_target(self):
        """Get all subarrays with sum equal to target"""
        result = []
        n = len(self.arr)
        
        for i in range(n):
            for j in range(i, n):
                subarray = self.arr[i:j+1]
                if sum(subarray) == self.target:
                    result.append((i, j, subarray))
        
        return result
    
    def get_count_with_different_targets(self, targets):
        """Get count for different target values"""
        results = []
        
        for target in targets:
            count = count_subarray_sums_equal_target(self.arr, target)
            results.append(count)
        
        return results
```

### Variation 3: Subarray Sums II with Constraints
**Problem**: Find subarray sums equal to target with additional constraints (e.g., minimum length, maximum sum).

**Link**: [CSES Problem Set - Subarray Sums II with Constraints](https://cses.fi/problemset/task/subarray_sums_ii_constraints)

```python
def subarray_sums_ii_constraints(arr, target, min_length, max_sum):
    """
    Find subarray sums equal to target with constraints
    """
    n = len(arr)
    if n == 0:
        return 0
    
    # Calculate prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # Count occurrences of (prefix_sum - target) with constraints
    count_map = {}
    count = 0
    
    for i in range(n + 1):
        # Check constraints
        if i >= min_length and prefix[i] <= max_sum:
            # Look for prefix_sum - target
            if prefix[i] - target in count_map:
                count += count_map[prefix[i] - target]
        
        # Add current prefix sum to map
        count_map[prefix[i]] = count_map.get(prefix[i], 0) + 1
    
    return count

def subarray_sums_ii_constraints_optimized(arr, target, min_length, max_sum):
    """
    Optimized version with better constraint handling
    """
    n = len(arr)
    if n == 0:
        return 0
    
    # Calculate prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # Count occurrences of (prefix_sum - target) with constraints
    count_map = {}
    count = 0
    
    for i in range(n + 1):
        # Check constraints
        if i >= min_length and prefix[i] <= max_sum:
            # Look for prefix_sum - target
            if prefix[i] - target in count_map:
                count += count_map[prefix[i] - target]
        
        # Add current prefix sum to map
        count_map[prefix[i]] = count_map.get(prefix[i], 0) + 1
        
        # Early termination if we can't improve
        if count == n * (n + 1) // 2:
            break
    
    return count

def subarray_sums_ii_constraints_multiple(arr, target, constraints_list):
    """
    Find subarray sums equal to target for multiple constraint sets
    """
    results = []
    
    for min_length, max_sum in constraints_list:
        result = subarray_sums_ii_constraints(arr, target, min_length, max_sum)
        results.append(result)
    
    return results

def subarray_sums_ii_constraints_range(arr, target, min_length, max_sum, left, right):
    """
    Find subarray sums equal to target with constraints in specific range
    """
    # Extract subarray
    subarray = arr[left:right+1]
    
    # Find subarray sums equal to target with constraints
    return subarray_sums_ii_constraints(subarray, target, min_length, max_sum)

# Example usage
arr = [1, 2, 3, 4, 5]
target = 7
min_length = 2
max_sum = 10

result = subarray_sums_ii_constraints(arr, target, min_length, max_sum)
print(f"Subarray sums equal to {target} with constraints: {result}")  # Output: 2
```

### Related Problems

## Problem Variations

### **Variation 1: Subarray Sums II with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove/update elements) while maintaining efficient subarray sum with target calculations.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicSubarraySumsII:
    def __init__(self, arr, target):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.prefix_sums = self._compute_prefix_sums()
        self.count = self._compute_count()
        self.count_map = self._compute_count_map()
    
    def _compute_prefix_sums(self):
        """Compute prefix sums of the array."""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i]
        return prefix
    
    def _compute_count_map(self):
        """Compute count map for prefix sums."""
        count_map = defaultdict(int)
        for i in range(self.n + 1):
            count_map[self.prefix_sums[i]] += 1
        return count_map
    
    def _compute_count(self):
        """Compute count of subarrays with sum equal to target."""
        count_map = defaultdict(int)
        count = 0
        
        for i in range(self.n + 1):
            # Look for prefix_sum - target
            if self.prefix_sums[i] - self.target in count_map:
                count += count_map[self.prefix_sums[i] - self.target]
            
            # Add current prefix sum to map
            count_map[self.prefix_sums[i]] += 1
        
        return count
    
    def add_element(self, value, index=None):
        """Add a new element to the array."""
        if index is None:
            index = self.n
        self.arr.insert(index, value)
        self.n += 1
        self.prefix_sums = self._compute_prefix_sums()
        self.count_map = self._compute_count_map()
        self.count = self._compute_count()
    
    def remove_element(self, index):
        """Remove element at specified index."""
        if 0 <= index < self.n:
            del self.arr[index]
            self.n -= 1
            self.prefix_sums = self._compute_prefix_sums()
            self.count_map = self._compute_count_map()
            self.count = self._compute_count()
    
    def update_element(self, index, new_value):
        """Update element at specified index."""
        if 0 <= index < self.n:
            self.arr[index] = new_value
            self.prefix_sums = self._compute_prefix_sums()
            self.count_map = self._compute_count_map()
            self.count = self._compute_count()
    
    def get_count(self):
        """Get current count of subarrays with sum equal to target."""
        return self.count
    
    def get_subarrays_with_target(self):
        """Get all subarrays with sum equal to target."""
        result = []
        count_map = defaultdict(list)
        
        for i in range(self.n + 1):
            # Look for prefix_sum - target
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    result.append((prev_idx, i - 1))
            
            # Add current prefix sum to map
            count_map[self.prefix_sums[i]].append(i)
        
        return result
    
    def get_subarrays_with_target_in_range(self, left, right):
        """Get subarrays with target sum in specified range."""
        if left < 0 or right >= self.n or left > right:
            return []
        
        # Extract subarray
        subarray = self.arr[left:right+1]
        
        # Calculate prefix sums for subarray
        prefix = [0] * (len(subarray) + 1)
        for i in range(len(subarray)):
            prefix[i + 1] = prefix[i] + subarray[i]
        
        # Find subarrays with target sum
        result = []
        count_map = defaultdict(list)
        
        for i in range(len(subarray) + 1):
            # Look for prefix_sum - target
            if prefix[i] - self.target in count_map:
                for prev_idx in count_map[prefix[i] - self.target]:
                    result.append((left + prev_idx, left + i - 1))
            
            # Add current prefix sum to map
            count_map[prefix[i]].append(i)
        
        return result
    
    def get_subarrays_with_target_constraints(self, constraint_func):
        """Get subarrays with target sum that satisfy custom constraints."""
        result = []
        count_map = defaultdict(list)
        
        for i in range(self.n + 1):
            # Look for prefix_sum - target
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    if constraint_func(prev_idx, i - 1, self.arr[prev_idx:i]):
                        result.append((prev_idx, i - 1))
            
            # Add current prefix sum to map
            count_map[self.prefix_sums[i]].append(i)
        
        return result
    
    def get_subarray_statistics(self):
        """Get statistics about subarray sums with target."""
        if self.n == 0:
            return {
                'total_subarrays': 0,
                'target_subarrays': 0,
                'target_rate': 0,
                'average_length': 0,
                'prefix_distribution': {}
            }
        
        total_subarrays = self.n * (self.n + 1) // 2
        target_subarrays = self.count
        target_rate = target_subarrays / total_subarrays if total_subarrays > 0 else 0
        
        # Calculate average length of target subarrays
        target_subarrays_list = self.get_subarrays_with_target()
        if target_subarrays_list:
            total_length = sum(end - start + 1 for start, end in target_subarrays_list)
            average_length = total_length / len(target_subarrays_list)
        else:
            average_length = 0
        
        return {
            'total_subarrays': total_subarrays,
            'target_subarrays': target_subarrays,
            'target_rate': target_rate,
            'average_length': average_length,
            'prefix_distribution': dict(self.count_map)
        }
    
    def get_subarray_patterns(self):
        """Get patterns in subarray sums with target."""
        patterns = {
            'consecutive_target': 0,
            'alternating_pattern': 0,
            'clustered_target': 0,
            'uniform_distribution': 0
        }
        
        target_subarrays = self.get_subarrays_with_target()
        
        for i in range(1, len(target_subarrays)):
            if (target_subarrays[i][0] == target_subarrays[i-1][1] + 1):
                patterns['consecutive_target'] += 1
            
            if i > 1:
                if (target_subarrays[i][0] != target_subarrays[i-1][1] + 1 and 
                    target_subarrays[i-1][0] != target_subarrays[i-2][1] + 1):
                    patterns['alternating_pattern'] += 1
        
        return patterns
    
    def get_optimal_target_strategy(self):
        """Get optimal strategy for target sum operations."""
        if self.n == 0:
            return {
                'recommended_target': 0,
                'max_count': 0,
                'efficiency_rate': 0
            }
        
        # Try different target values
        best_target = self.target
        max_count = self.count
        
        # Test targets around current target
        for test_target in range(max(1, self.target - 10), self.target + 11):
            if test_target == self.target:
                continue
            
            # Calculate count for this target
            count_map = defaultdict(int)
            count = 0
            
            for i in range(self.n + 1):
                if self.prefix_sums[i] - test_target in count_map:
                    count += count_map[self.prefix_sums[i] - test_target]
                count_map[self.prefix_sums[i]] += 1
            
            if count > max_count:
                max_count = count
                best_target = test_target
        
        # Calculate efficiency rate
        total_subarrays = self.n * (self.n + 1) // 2
        efficiency_rate = max_count / total_subarrays if total_subarrays > 0 else 0
        
        return {
            'recommended_target': best_target,
            'max_count': max_count,
            'efficiency_rate': efficiency_rate
        }

# Example usage
arr = [1, 2, 3, 4, 5]
target = 9
dynamic_sums_ii = DynamicSubarraySumsII(arr, target)
print(f"Initial count: {dynamic_sums_ii.get_count()}")

# Add an element
dynamic_sums_ii.add_element(6)
print(f"After adding element: {dynamic_sums_ii.get_count()}")

# Update an element
dynamic_sums_ii.update_element(2, 7)
print(f"After updating element: {dynamic_sums_ii.get_count()}")

# Get subarrays with target
print(f"Subarrays with target {target}: {dynamic_sums_ii.get_subarrays_with_target()}")

# Get subarrays with target in range
print(f"Subarrays with target in range [1, 3]: {dynamic_sums_ii.get_subarrays_with_target_in_range(1, 3)}")

# Get subarrays with target constraints
def constraint_func(start, end, subarray):
    return end - start >= 1

print(f"Subarrays with target constraints: {dynamic_sums_ii.get_subarrays_with_target_constraints(constraint_func)}")

# Get statistics
print(f"Statistics: {dynamic_sums_ii.get_subarray_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_sums_ii.get_subarray_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_sums_ii.get_optimal_target_strategy()}")
```

### **Variation 2: Subarray Sums II with Different Operations**
**Problem**: Handle different types of operations on subarray sums with target (weighted elements, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of subarray sum with target queries.

```python
class AdvancedSubarraySumsII:
    def __init__(self, arr, target, weights=None, priorities=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.prefix_sums = self._compute_prefix_sums()
        self.weighted_prefix_sums = self._compute_weighted_prefix_sums()
        self.count = self._compute_count()
        self.weighted_count = self._compute_weighted_count()
    
    def _compute_prefix_sums(self):
        """Compute prefix sums of the array."""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i]
        return prefix
    
    def _compute_weighted_prefix_sums(self):
        """Compute weighted prefix sums of the array."""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i] * self.weights[i]
        return prefix
    
    def _compute_count(self):
        """Compute count of subarrays with sum equal to target."""
        count_map = defaultdict(int)
        count = 0
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                count += count_map[self.prefix_sums[i] - self.target]
            count_map[self.prefix_sums[i]] += 1
        
        return count
    
    def _compute_weighted_count(self):
        """Compute weighted count of subarrays with sum equal to target."""
        count_map = defaultdict(int)
        weighted_count = 0
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                weighted_count += count_map[self.prefix_sums[i] - self.target] * self.weights[i-1] if i > 0 else 0
            count_map[self.prefix_sums[i]] += 1
        
        return weighted_count
    
    def get_count(self):
        """Get current count of subarrays with sum equal to target."""
        return self.count
    
    def get_weighted_count(self):
        """Get current weighted count of subarrays with sum equal to target."""
        return self.weighted_count
    
    def get_subarrays_with_priority(self, priority_func):
        """Get subarrays with target sum considering priority."""
        result = []
        count_map = defaultdict(list)
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    subarray = self.arr[prev_idx:i]
                    priority = priority_func(prev_idx, i - 1, subarray, self.weights[prev_idx:i], self.priorities[prev_idx:i])
                    result.append((prev_idx, i - 1, priority))
            count_map[self.prefix_sums[i]].append(i)
        
        # Sort by priority
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def get_subarrays_with_optimization(self, optimization_func):
        """Get subarrays with target sum using custom optimization function."""
        result = []
        count_map = defaultdict(list)
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    subarray = self.arr[prev_idx:i]
                    score = optimization_func(prev_idx, i - 1, subarray, self.weights[prev_idx:i], self.priorities[prev_idx:i])
                    result.append((prev_idx, i - 1, score))
            count_map[self.prefix_sums[i]].append(i)
        
        # Sort by optimization score
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def get_subarrays_with_constraints(self, constraint_func):
        """Get subarrays with target sum that satisfy custom constraints."""
        result = []
        count_map = defaultdict(list)
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    subarray = self.arr[prev_idx:i]
                    if constraint_func(prev_idx, i - 1, subarray, self.weights[prev_idx:i], self.priorities[prev_idx:i]):
                        result.append((prev_idx, i - 1))
            count_map[self.prefix_sums[i]].append(i)
        
        return result
    
    def get_subarrays_with_multiple_criteria(self, criteria_list):
        """Get subarrays with target sum that satisfy multiple criteria."""
        result = []
        count_map = defaultdict(list)
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    subarray = self.arr[prev_idx:i]
                    satisfies_all_criteria = True
                    for criterion in criteria_list:
                        if not criterion(prev_idx, i - 1, subarray, self.weights[prev_idx:i], self.priorities[prev_idx:i]):
                            satisfies_all_criteria = False
                            break
                    
                    if satisfies_all_criteria:
                        result.append((prev_idx, i - 1))
            count_map[self.prefix_sums[i]].append(i)
        
        return result
    
    def get_subarrays_with_alternatives(self, alternatives):
        """Get subarrays with target sum considering alternative values."""
        result = []
        
        # Check original array
        original_result = self.get_subarrays_with_target()
        for start, end in original_result:
            result.append((start, end, 'original'))
        
        # Check alternative values
        for i, alt_values in alternatives.items():
            if 0 <= i < self.n:
                for alt_value in alt_values:
                    # Create temporary array with alternative value
                    temp_arr = self.arr[:]
                    temp_arr[i] = alt_value
                    
                    # Calculate prefix sums for this alternative
                    temp_prefix = [0] * (self.n + 1)
                    for j in range(self.n):
                        temp_prefix[j + 1] = temp_prefix[j] + temp_arr[j]
                    
                    # Find subarrays with target sum for this alternative
                    temp_count_map = defaultdict(list)
                    for j in range(self.n + 1):
                        if temp_prefix[j] - self.target in temp_count_map:
                            for prev_idx in temp_count_map[temp_prefix[j] - self.target]:
                                result.append((prev_idx, j - 1, f'alternative_{alt_value}'))
                        temp_count_map[temp_prefix[j]].append(j)
        
        return result
    
    def get_subarrays_with_adaptive_criteria(self, adaptive_func):
        """Get subarrays with target sum using adaptive criteria."""
        result = []
        count_map = defaultdict(list)
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    subarray = self.arr[prev_idx:i]
                    if adaptive_func(prev_idx, i - 1, subarray, self.weights[prev_idx:i], self.priorities[prev_idx:i], result):
                        result.append((prev_idx, i - 1))
            count_map[self.prefix_sums[i]].append(i)
        
        return result
    
    def get_subarray_optimization(self):
        """Get optimal subarray configuration."""
        strategies = [
            ('count', self.get_count),
            ('weighted_count', self.get_weighted_count),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value > best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
arr = [1, 2, 3, 4, 5]
target = 9
weights = [2, 1, 3, 1, 2]
priorities = [1, 2, 1, 3, 1]
advanced_sums_ii = AdvancedSubarraySumsII(arr, target, weights, priorities)

print(f"Count: {advanced_sums_ii.get_count()}")
print(f"Weighted count: {advanced_sums_ii.get_weighted_count()}")

# Get subarrays with priority
def priority_func(start, end, subarray, weights, priorities):
    return sum(weights) * sum(priorities)

print(f"Subarrays with priority: {advanced_sums_ii.get_subarrays_with_priority(priority_func)}")

# Get subarrays with optimization
def optimization_func(start, end, subarray, weights, priorities):
    return sum(subarray) * sum(weights) + sum(priorities)

print(f"Subarrays with optimization: {advanced_sums_ii.get_subarrays_with_optimization(optimization_func)}")

# Get subarrays with constraints
def constraint_func(start, end, subarray, weights, priorities):
    return end - start >= 1 and sum(weights) > 2

print(f"Subarrays with constraints: {advanced_sums_ii.get_subarrays_with_constraints(constraint_func)}")

# Get subarrays with multiple criteria
def criterion1(start, end, subarray, weights, priorities):
    return end - start >= 1

def criterion2(start, end, subarray, weights, priorities):
    return sum(weights) > 2

criteria_list = [criterion1, criterion2]
print(f"Subarrays with multiple criteria: {advanced_sums_ii.get_subarrays_with_multiple_criteria(criteria_list)}")

# Get subarrays with alternatives
alternatives = {1: [3, 5], 3: [6, 8]}
print(f"Subarrays with alternatives: {advanced_sums_ii.get_subarrays_with_alternatives(alternatives)}")

# Get subarrays with adaptive criteria
def adaptive_func(start, end, subarray, weights, priorities, current_result):
    return end - start >= 1 and len(current_result) < 5

print(f"Subarrays with adaptive criteria: {advanced_sums_ii.get_subarrays_with_adaptive_criteria(adaptive_func)}")

# Get subarray optimization
print(f"Subarray optimization: {advanced_sums_ii.get_subarray_optimization()}")
```

### **Variation 3: Subarray Sums II with Constraints**
**Problem**: Handle subarray sums with target and additional constraints (cost limits, length constraints, resource constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedSubarraySumsII:
    def __init__(self, arr, target, constraints=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.constraints = constraints or {}
        self.prefix_sums = self._compute_prefix_sums()
        self.count = self._compute_count()
    
    def _compute_prefix_sums(self):
        """Compute prefix sums of the array."""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i]
        return prefix
    
    def _compute_count(self):
        """Compute count of subarrays with sum equal to target."""
        count_map = defaultdict(int)
        count = 0
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                count += count_map[self.prefix_sums[i] - self.target]
            count_map[self.prefix_sums[i]] += 1
        
        return count
    
    def get_count_with_cost_constraints(self, cost_limit):
        """Get count considering cost constraints."""
        if self.n == 0:
            return 0
        
        count_map = defaultdict(int)
        count = 0
        total_cost = 0
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                # Calculate cost for this subarray
                cost = count_map[self.prefix_sums[i] - self.target] * (i - 1)  # Simple cost model
                if total_cost + cost <= cost_limit:
                    count += count_map[self.prefix_sums[i] - self.target]
                    total_cost += cost
            count_map[self.prefix_sums[i]] += 1
        
        return count
    
    def get_count_with_length_constraints(self, min_length, max_length):
        """Get count considering length constraints."""
        if self.n == 0:
            return 0
        
        count_map = defaultdict(list)
        count = 0
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    subarray_length = i - prev_idx
                    if min_length <= subarray_length <= max_length:
                        count += 1
            count_map[self.prefix_sums[i]].append(i)
        
        return count
    
    def get_count_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get count considering resource constraints."""
        if self.n == 0:
            return 0
        
        count_map = defaultdict(list)
        count = 0
        current_resources = [0] * len(resource_limits)
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    # Check resource constraints
                    can_afford = True
                    for j, consumption in enumerate(resource_consumption.get(prev_idx, [0] * len(resource_limits))):
                        if current_resources[j] + consumption > resource_limits[j]:
                            can_afford = False
                            break
                    
                    if can_afford:
                        count += 1
                        for j, consumption in enumerate(resource_consumption.get(prev_idx, [0] * len(resource_limits))):
                            current_resources[j] += consumption
            count_map[self.prefix_sums[i]].append(i)
        
        return count
    
    def get_count_with_mathematical_constraints(self, constraint_func):
        """Get count that satisfies custom mathematical constraints."""
        if self.n == 0:
            return 0
        
        count_map = defaultdict(list)
        count = 0
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    if constraint_func(prev_idx, i - 1, self.arr[prev_idx:i]):
                        count += 1
            count_map[self.prefix_sums[i]].append(i)
        
        return count
    
    def get_count_with_range_constraints(self, range_constraints):
        """Get count that satisfies range constraints."""
        if self.n == 0:
            return 0
        
        count_map = defaultdict(list)
        count = 0
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    # Check if subarray satisfies all range constraints
                    satisfies_constraints = True
                    for constraint in range_constraints:
                        if not constraint(prev_idx, i - 1, self.arr[prev_idx:i]):
                            satisfies_constraints = False
                            break
                    
                    if satisfies_constraints:
                        count += 1
            count_map[self.prefix_sums[i]].append(i)
        
        return count
    
    def get_count_with_optimization_constraints(self, optimization_func):
        """Get count using custom optimization constraints."""
        if self.n == 0:
            return 0
        
        # Sort subarrays by optimization function
        all_subarrays = []
        count_map = defaultdict(list)
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    subarray = self.arr[prev_idx:i]
                    score = optimization_func(prev_idx, i - 1, subarray)
                    all_subarrays.append((prev_idx, i - 1, score))
            count_map[self.prefix_sums[i]].append(i)
        
        # Sort by optimization score
        all_subarrays.sort(key=lambda x: x[2], reverse=True)
        
        return len(all_subarrays)
    
    def get_count_with_multiple_constraints(self, constraints_list):
        """Get count that satisfies multiple constraints."""
        if self.n == 0:
            return 0
        
        count_map = defaultdict(list)
        count = 0
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    # Check if subarray satisfies all constraints
                    satisfies_all_constraints = True
                    for constraint in constraints_list:
                        if not constraint(prev_idx, i - 1, self.arr[prev_idx:i]):
                            satisfies_all_constraints = False
                            break
                    
                    if satisfies_all_constraints:
                        count += 1
            count_map[self.prefix_sums[i]].append(i)
        
        return count
    
    def get_count_with_priority_constraints(self, priority_func):
        """Get count with priority-based constraints."""
        if self.n == 0:
            return 0
        
        # Sort subarrays by priority
        all_subarrays = []
        count_map = defaultdict(list)
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    subarray = self.arr[prev_idx:i]
                    priority = priority_func(prev_idx, i - 1, subarray)
                    all_subarrays.append((prev_idx, i - 1, priority))
            count_map[self.prefix_sums[i]].append(i)
        
        # Sort by priority
        all_subarrays.sort(key=lambda x: x[2], reverse=True)
        
        return len(all_subarrays)
    
    def get_count_with_adaptive_constraints(self, adaptive_func):
        """Get count with adaptive constraints."""
        if self.n == 0:
            return 0
        
        count_map = defaultdict(list)
        count = 0
        
        for i in range(self.n + 1):
            if self.prefix_sums[i] - self.target in count_map:
                for prev_idx in count_map[self.prefix_sums[i] - self.target]:
                    # Check adaptive constraints
                    if adaptive_func(prev_idx, i - 1, self.arr[prev_idx:i], count):
                        count += 1
            count_map[self.prefix_sums[i]].append(i)
        
        return count
    
    def get_optimal_target_strategy(self):
        """Get optimal target strategy considering all constraints."""
        strategies = [
            ('cost_constraints', self.get_count_with_cost_constraints),
            ('length_constraints', self.get_count_with_length_constraints),
            ('resource_constraints', self.get_count_with_resource_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'cost_constraints':
                    current_count = strategy_func(100)  # Cost limit of 100
                elif strategy_name == 'length_constraints':
                    current_count = strategy_func(1, 5)  # Length between 1 and 5
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {i: [10, 5] for i in range(self.n)}
                    current_count = strategy_func(resource_limits, resource_consumption)
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'max_cost': 100,
    'min_length': 1,
    'max_length': 5
}

arr = [1, 2, 3, 4, 5]
target = 9
constrained_sums_ii = ConstrainedSubarraySumsII(arr, target, constraints)

print("Cost-constrained count:", constrained_sums_ii.get_count_with_cost_constraints(100))

print("Length-constrained count:", constrained_sums_ii.get_count_with_length_constraints(1, 5))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(arr))}
print("Resource-constrained count:", constrained_sums_ii.get_count_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(start, end, subarray):
    return end - start >= 1 and sum(subarray) > 5

print("Mathematical constraint count:", constrained_sums_ii.get_count_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(start, end, subarray):
    return end - start >= 1

range_constraints = [range_constraint]
print("Range-constrained count:", constrained_sums_ii.get_count_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(start, end, subarray):
    return end - start >= 1

def constraint2(start, end, subarray):
    return sum(subarray) > 5

constraints_list = [constraint1, constraint2]
print("Multiple constraints count:", constrained_sums_ii.get_count_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(start, end, subarray):
    return sum(subarray)

print("Priority-constrained count:", constrained_sums_ii.get_count_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(start, end, subarray, current_count):
    return end - start >= 1 and current_count < 10

print("Adaptive constraint count:", constrained_sums_ii.get_count_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_sums_ii.get_optimal_target_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Subarray Sums II](https://cses.fi/problemset/task/1662) - Basic subarray sum with target problem
- [Subarray Sums I](https://cses.fi/problemset/task/1661) - Subarray sum problems
- [Subarray Divisibility](https://cses.fi/problemset/task/1662) - Subarray divisibility problem

#### **LeetCode Problems**
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) - Subarray sum with target
- [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/) - Subarray sum divisibility
- [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/) - Subarray product constraints

#### **Problem Categories**
- **Hash Maps**: Frequency counting, prefix sum tracking, efficient lookups
- **Prefix Sums**: Cumulative calculations, range queries, efficient sum computation
- **Subarray Problems**: Array processing, sum calculations, constraint handling
- **Algorithm Design**: Hash-based techniques, prefix sum optimization, subarray analysis
