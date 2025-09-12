---
layout: simple
title: "Sum of Two Values - Find Pair with Target Sum"
permalink: /problem_soulutions/sorting_and_searching/sum_of_two_values_analysis
---

# Sum of Two Values - Find Pair with Target Sum

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the two-sum problem and its variations
- Apply hash map techniques for efficient pair finding
- Implement two-pointer technique for sorted arrays
- Optimize search algorithms using different data structures
- Handle edge cases in pair finding (no solution, duplicate elements)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Hash maps, two-pointer technique, binary search, sorting
- **Data Structures**: Arrays, hash maps, sorted arrays
- **Mathematical Concepts**: Pair finding, complement searching, optimization
- **Programming Skills**: Hash map operations, two-pointer implementation, binary search
- **Related Problems**: Apartments (two pointers), Distinct Numbers (hash sets), Maximum Subarray Sum (optimization)

## 📋 Problem Description

Given an array of n integers and a target sum x, find two distinct elements that sum to x. Return the 1-indexed positions of the two elements, or "IMPOSSIBLE" if no such pair exists.

This is the classic two-sum problem that can be solved using multiple approaches, each with different trade-offs in time and space complexity.

**Input**: 
- First line: two integers n and x (array size and target sum)
- Second line: n integers (the array elements)

**Output**: 
- Print two 1-indexed positions, or "IMPOSSIBLE" if no solution exists

**Constraints**:
- 2 ≤ n ≤ 2×10⁵
- 1 ≤ x ≤ 10⁹
- 1 ≤ a_i ≤ 10⁹

**Example**:
```
Input:
4 8
2 7 5 1

Output:
1 2

Explanation**: 
The array [2, 7, 5, 1] with target sum 8:
- Elements at positions 1 and 2: 2 + 7 = 9 ≠ 8
- Elements at positions 1 and 3: 2 + 5 = 7 ≠ 8
- Elements at positions 1 and 4: 2 + 1 = 3 ≠ 8
- Elements at positions 2 and 3: 7 + 5 = 12 ≠ 8
- Elements at positions 2 and 4: 7 + 1 = 8 ✓

Solution: positions 2 and 4 (1-indexed: 1 and 2)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Pairs

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible pairs of elements
- **Sum Validation**: For each pair, check if their sum equals the target
- **Complete Coverage**: Guaranteed to find a solution if it exists
- **Simple Implementation**: Nested loops approach

**Key Insight**: Systematically check all possible pairs of elements to find one that sums to the target value.

**Algorithm**:
- Use nested loops to check all pairs (i,j) where i < j
- For each pair, check if a[i] + a[j] = x
- Return the first valid pair found

**Visual Example**:
```
Array: [2, 7, 5, 1], Target: 8

All possible pairs:
1. (0,1): a[0] + a[1] = 2 + 7 = 9 ≠ 8
2. (0,2): a[0] + a[2] = 2 + 5 = 7 ≠ 8
3. (0,3): a[0] + a[3] = 2 + 1 = 3 ≠ 8
4. (1,2): a[1] + a[2] = 7 + 5 = 12 ≠ 8
5. (1,3): a[1] + a[3] = 7 + 1 = 8 ✓

Solution: positions 1 and 3 (1-indexed: 2 and 4)
```

**Implementation**:
```python
def brute_force_two_sum(arr, target):
    """
    Find two elements that sum to target using brute force
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        tuple: (index1, index2) or None if no solution
    """
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return (i + 1, j + 1)  # 1-indexed
    
    return None

# Example usage
arr = [2, 7, 5, 1]
target = 8
result = brute_force_two_sum(arr, target)
print(f"Brute force result: {result}")  # Output: (2, 4)
```

**Time Complexity**: O(n²) - Check all pairs
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Hash Map with Complement Search

**Key Insights from Optimized Approach**:
- **Complement Concept**: For each element, look for its complement (target - element)
- **Hash Map Storage**: Store seen elements and their indices for O(1) lookup
- **Single Pass**: Process each element exactly once
- **Efficient Lookup**: O(1) average time for complement search

**Key Insight**: For each element, check if its complement (target - element) has been seen before using a hash map.

**Algorithm**:
- Create a hash map to store seen elements and their indices
- For each element, calculate its complement
- Check if complement exists in the hash map
- If found, return the indices; otherwise, add current element to map

**Visual Example**:
```
Array: [2, 7, 5, 1], Target: 8

Hash map: {}
Processing:
1. Element 2 (index 0): complement = 8 - 2 = 6
   - 6 not in map → add 2 to map: {2: 0}

2. Element 7 (index 1): complement = 8 - 7 = 1
   - 1 not in map → add 7 to map: {2: 0, 7: 1}

3. Element 5 (index 2): complement = 8 - 5 = 3
   - 3 not in map → add 5 to map: {2: 0, 7: 1, 5: 2}

4. Element 1 (index 3): complement = 8 - 1 = 7
   - 7 in map at index 1 → Found solution!
   → Return (2, 4) - 1-indexed positions
```

**Implementation**:
```python
def optimized_two_sum(arr, target):
    """
    Find two elements that sum to target using hash map
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        tuple: (index1, index2) or None if no solution
    """
    seen = {}  # value -> index mapping
    
    for i, num in enumerate(arr):
        complement = target - num
        
        if complement in seen:
            return (seen[complement] + 1, i + 1)  # 1-indexed
        
        seen[num] = i
    
    return None

# Example usage
arr = [2, 7, 5, 1]
target = 8
result = optimized_two_sum(arr, target)
print(f"Optimized result: {result}")  # Output: (2, 4)
```

**Time Complexity**: O(n) - Single pass through array
**Space Complexity**: O(n) - For hash map storage

**Why it's better**: Linear time complexity with efficient complement search.

---

### Approach 3: Optimal - Two Pointer Technique (Sorted Array)

**Key Insights from Optimal Approach**:
- **Sorted Array Benefit**: After sorting, we can use two pointers efficiently
- **Pointer Movement**: Move pointers based on current sum compared to target
- **Optimal Search**: Eliminate half of remaining elements in each comparison
- **Space Efficient**: O(1) extra space if sorting in-place

**Key Insight**: Sort the array first, then use two pointers to find the target sum efficiently.

**Algorithm**:
- Sort the array while preserving original indices
- Use two pointers: one at start, one at end
- Move pointers based on current sum vs target
- Return original indices when sum equals target

**Visual Example**:
```
Array: [2, 7, 5, 1], Target: 8

Step 1: Sort with original indices
Sorted: [(1, 3), (2, 0), (5, 2), (7, 1)]
        value, original_index

Step 2: Two pointer search
Left pointer: 0, Right pointer: 3

1. Sum = 1 + 7 = 8 = target ✓
   → Found solution: original indices 3 and 1
   → Return (2, 4) - 1-indexed positions
```

**Implementation**:
```python
def optimal_two_sum(arr, target):
    """
    Find two elements that sum to target using two pointers
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        tuple: (index1, index2) or None if no solution
    """
    # Create list of (value, original_index) pairs
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    
    # Sort by value
    indexed_arr.sort()
    
    left, right = 0, len(indexed_arr) - 1
    
    while left < right:
        current_sum = indexed_arr[left][0] + indexed_arr[right][0]
        
        if current_sum == target:
            # Return original indices (1-indexed)
            idx1, idx2 = indexed_arr[left][1], indexed_arr[right][1]
            return (min(idx1, idx2) + 1, max(idx1, idx2) + 1)
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None

# Example usage
arr = [2, 7, 5, 1]
target = 8
result = optimal_two_sum(arr, target)
print(f"Optimal result: {result}")  # Output: (2, 4)
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(n) - For storing indexed array

**Why it's optimal**: Efficient two-pointer technique with good space-time trade-off.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all pairs |
| Hash Map | O(n) | O(n) | Complement search |
| Two Pointers | O(n log n) | O(n) | Sorted array search |

### Time Complexity
- **Time**: O(n) - Hash map approach provides best time complexity
- **Space**: O(n) - For hash map or indexed array storage

### Why This Solution Works
- **Complement Search**: Efficiently find pairs by looking for complements
- **Hash Map Efficiency**: O(1) average lookup time for complement search
- **Single Pass**: Process each element exactly once
- **Optimal Approach**: Hash map provides best practical performance for most cases

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Sum of Two Values with Multiple Solutions
**Problem**: Find all pairs of indices that sum to the target value.

**Link**: [CSES Problem Set - Sum of Two Values Multiple Solutions](https://cses.fi/problemset/task/sum_of_two_values_multiple)

```python
def sum_of_two_values_multiple_solutions(arr, target):
    """
    Find all pairs of indices that sum to target
    """
    value_to_indices = {}
    results = []
    
    for i, num in enumerate(arr):
        complement = target - num
        
        if complement in value_to_indices:
            # Add all pairs with this complement
            for j in value_to_indices[complement]:
                if i != j:  # Ensure different indices
                    results.append((min(i, j), max(i, j)))
        
        # Add current number to map
        if num not in value_to_indices:
            value_to_indices[num] = []
        value_to_indices[num].append(i)
    
    return results

def sum_of_two_values_multiple_solutions_optimized(arr, target):
    """
    Optimized version avoiding duplicate pairs
    """
    value_to_indices = {}
    results = set()  # Use set to avoid duplicates
    
    for i, num in enumerate(arr):
        complement = target - num
        
        if complement in value_to_indices:
            for j in value_to_indices[complement]:
                if i != j:
                    results.add((min(i, j), max(i, j)))
        
        if num not in value_to_indices:
            value_to_indices[num] = []
        value_to_indices[num].append(i)
    
    return list(results)
```

### Variation 2: Sum of Two Values with Constraints
**Problem**: Find pairs that sum to target with additional constraints (e.g., indices must be at least k apart).

**Link**: [CSES Problem Set - Sum of Two Values with Constraints](https://cses.fi/problemset/task/sum_of_two_values_constraints)

```python
def sum_of_two_values_constraints(arr, target, min_distance):
    """
    Find pairs that sum to target with minimum distance constraint
    """
    value_to_indices = {}
    results = []
    
    for i, num in enumerate(arr):
        complement = target - num
        
        if complement in value_to_indices:
            for j in value_to_indices[complement]:
                if abs(i - j) >= min_distance:
                    results.append((min(i, j), max(i, j)))
        
        if num not in value_to_indices:
            value_to_indices[num] = []
        value_to_indices[num].append(i)
    
    return results

def sum_of_two_values_constraints_optimized(arr, target, min_distance):
    """
    Optimized version using sliding window approach
    """
    # Sort array with original indices
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    left, right = 0, len(indexed_arr) - 1
    results = []
    
    while left < right:
        current_sum = indexed_arr[left][0] + indexed_arr[right][0]
        
        if current_sum == target:
            i, j = indexed_arr[left][1], indexed_arr[right][1]
            if abs(i - j) >= min_distance:
                results.append((min(i, j), max(i, j)))
            
            # Move both pointers to find more solutions
            left += 1
            right -= 1
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return results
```

### Variation 3: Sum of Two Values with Updates
**Problem**: Handle dynamic updates to the array and maintain sum queries.

**Link**: [CSES Problem Set - Sum of Two Values with Updates](https://cses.fi/problemset/task/sum_of_two_values_updates)

```python
class SumOfTwoValuesWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.value_to_indices = {}
        self._build_index_map()
    
    def _build_index_map(self):
        """Build the value to indices mapping"""
        self.value_to_indices = {}
        for i, num in enumerate(self.arr):
            if num not in self.value_to_indices:
                self.value_to_indices[num] = []
            self.value_to_indices[num].append(i)
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        old_value = self.arr[index]
        self.arr[index] = new_value
        
        # Remove old value from map
        if old_value in self.value_to_indices:
            self.value_to_indices[old_value].remove(index)
            if not self.value_to_indices[old_value]:
                del self.value_to_indices[old_value]
        
        # Add new value to map
        if new_value not in self.value_to_indices:
            self.value_to_indices[new_value] = []
        self.value_to_indices[new_value].append(index)
    
    def find_sum(self, target):
        """Find pair that sums to target"""
        for i, num in enumerate(self.arr):
            complement = target - num
            
            if complement in self.value_to_indices:
                for j in self.value_to_indices[complement]:
                    if i != j:
                        return (min(i, j), max(i, j))
        
        return None
    
    def find_all_sums(self, target):
        """Find all pairs that sum to target"""
        results = set()
        
        for i, num in enumerate(self.arr):
            complement = target - num
            
            if complement in self.value_to_indices:
                for j in self.value_to_indices[complement]:
                    if i != j:
                        results.add((min(i, j), max(i, j)))
        
        return list(results)
```

### Related Problems

## Problem Variations

### **Variation 1: Sum of Two Values with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove/update elements) while maintaining efficient sum of two values calculations.

**Approach**: Use balanced binary search trees or hash maps for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicSumOfTwoValues:
    def __init__(self, arr, target):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.sorted_arr = self._create_sorted_array()
        self.pairs = self._compute_pairs()
    
    def _create_sorted_array(self):
        """Create sorted array with original indices."""
        indexed_arr = [(self.arr[i], i) for i in range(self.n)]
        indexed_arr.sort()
        return indexed_arr
    
    def _compute_pairs(self):
        """Compute all pairs that sum to target."""
        results = []
        left = 0
        right = len(self.sorted_arr) - 1
        
        while left < right:
            current_sum = self.sorted_arr[left][0] + self.sorted_arr[right][0]
            
            if current_sum == self.target:
                indices = [self.sorted_arr[left][1], self.sorted_arr[right][1]]
                results.append(indices)
                left += 1
                right -= 1
            elif current_sum < self.target:
                left += 1
            else:
                right -= 1
        
        return results
    
    def add_element(self, value, index=None):
        """Add a new element to the array."""
        if index is None:
            index = self.n
        self.arr.insert(index, value)
        self.n += 1
        self.sorted_arr = self._create_sorted_array()
        self.pairs = self._compute_pairs()
    
    def remove_element(self, index):
        """Remove element at specified index."""
        if 0 <= index < self.n:
            del self.arr[index]
            self.n -= 1
            self.sorted_arr = self._create_sorted_array()
            self.pairs = self._compute_pairs()
    
    def update_element(self, index, new_value):
        """Update element at specified index."""
        if 0 <= index < self.n:
            self.arr[index] = new_value
            self.sorted_arr = self._create_sorted_array()
            self.pairs = self._compute_pairs()
    
    def get_pairs(self):
        """Get current pairs that sum to target."""
        return self.pairs
    
    def get_pairs_count(self):
        """Get count of pairs that sum to target."""
        return len(self.pairs)
    
    def get_pairs_with_constraints(self, constraint_func):
        """Get pairs that satisfy custom constraints."""
        result = []
        for indices in self.pairs:
            if constraint_func(indices, [self.arr[i] for i in indices]):
                result.append(indices)
        return result
    
    def get_pairs_in_range(self, start_idx, end_idx):
        """Get pairs where all indices are in specified range."""
        result = []
        for indices in self.pairs:
            if all(start_idx <= idx <= end_idx for idx in indices):
                result.append(indices)
        return result
    
    def get_pairs_with_distance_constraint(self, min_distance):
        """Get pairs with minimum distance between indices."""
        result = []
        for indices in self.pairs:
            if abs(indices[0] - indices[1]) >= min_distance:
                result.append(indices)
        return result
    
    def get_pair_statistics(self):
        """Get statistics about pairs."""
        if not self.pairs:
            return {
                'total_pairs': 0,
                'average_sum': 0,
                'index_distribution': {},
                'value_distribution': {}
            }
        
        total_pairs = len(self.pairs)
        average_sum = self.target  # All pairs sum to target
        
        # Calculate index distribution
        index_distribution = defaultdict(int)
        for indices in self.pairs:
            for idx in indices:
                index_distribution[idx] += 1
        
        # Calculate value distribution
        value_distribution = defaultdict(int)
        for indices in self.pairs:
            for idx in indices:
                value_distribution[self.arr[idx]] += 1
        
        return {
            'total_pairs': total_pairs,
            'average_sum': average_sum,
            'index_distribution': dict(index_distribution),
            'value_distribution': dict(value_distribution)
        }
    
    def get_pair_patterns(self):
        """Get patterns in pairs."""
        patterns = {
            'consecutive_indices': 0,
            'alternating_pattern': 0,
            'clustered_indices': 0,
            'uniform_distribution': 0
        }
        
        for indices in self.pairs:
            sorted_indices = sorted(indices)
            # Check for consecutive indices
            if sorted_indices[1] == sorted_indices[0] + 1:
                patterns['consecutive_indices'] += 1
            
            # Check for alternating pattern
            if len(self.pairs) > 1:
                for i in range(1, len(self.pairs)):
                    if (self.pairs[i][0] != self.pairs[i-1][1] and 
                        self.pairs[i][1] != self.pairs[i-1][0]):
                        patterns['alternating_pattern'] += 1
        
        return patterns
    
    def get_optimal_target_strategy(self):
        """Get optimal strategy for target sum operations."""
        if self.n < 2:
            return {
                'recommended_target': 0,
                'max_pairs': 0,
                'efficiency_rate': 0
            }
        
        # Try different target values
        best_target = self.target
        max_pairs = len(self.pairs)
        
        # Test targets around current target
        for test_target in range(max(1, self.target - 20), self.target + 21):
            if test_target == self.target:
                continue
            
            # Calculate pairs for this target
            test_pairs = []
            left = 0
            right = len(self.sorted_arr) - 1
            
            while left < right:
                current_sum = self.sorted_arr[left][0] + self.sorted_arr[right][0]
                
                if current_sum == test_target:
                    indices = [self.sorted_arr[left][1], self.sorted_arr[right][1]]
                    test_pairs.append(indices)
                    left += 1
                    right -= 1
                elif current_sum < test_target:
                    left += 1
                else:
                    right -= 1
            
            if len(test_pairs) > max_pairs:
                max_pairs = len(test_pairs)
                best_target = test_target
        
        # Calculate efficiency rate
        total_possible = self.n * (self.n - 1) // 2
        efficiency_rate = max_pairs / total_possible if total_possible > 0 else 0
        
        return {
            'recommended_target': best_target,
            'max_pairs': max_pairs,
            'efficiency_rate': efficiency_rate
        }

# Example usage
arr = [1, 2, 3, 4, 5, 6, 7, 8]
target = 9
dynamic_two_sum = DynamicSumOfTwoValues(arr, target)
print(f"Initial pairs: {dynamic_two_sum.get_pairs_count()}")

# Add an element
dynamic_two_sum.add_element(9)
print(f"After adding element: {dynamic_two_sum.get_pairs_count()}")

# Update an element
dynamic_two_sum.update_element(2, 10)
print(f"After updating element: {dynamic_two_sum.get_pairs_count()}")

# Get pairs with constraints
def constraint_func(indices, values):
    return all(v > 2 for v in values)

print(f"Pairs with constraints: {dynamic_two_sum.get_pairs_with_constraints(constraint_func)}")

# Get pairs in range
print(f"Pairs in range [0, 5]: {dynamic_two_sum.get_pairs_in_range(0, 5)}")

# Get pairs with distance constraint
print(f"Pairs with distance constraint: {dynamic_two_sum.get_pairs_with_distance_constraint(2)}")

# Get statistics
print(f"Statistics: {dynamic_two_sum.get_pair_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_two_sum.get_pair_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_two_sum.get_optimal_target_strategy()}")
```

### **Variation 2: Sum of Two Values with Different Operations**
**Problem**: Handle different types of operations on sum of two values (weighted elements, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of sum of two values queries.

```python
class AdvancedSumOfTwoValues:
    def __init__(self, arr, target, weights=None, priorities=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.sorted_arr = self._create_sorted_array()
        self.pairs = self._compute_pairs()
        self.weighted_pairs = self._compute_weighted_pairs()
    
    def _create_sorted_array(self):
        """Create sorted array with original indices."""
        indexed_arr = [(self.arr[i], i) for i in range(self.n)]
        indexed_arr.sort()
        return indexed_arr
    
    def _compute_pairs(self):
        """Compute all pairs that sum to target."""
        results = []
        left = 0
        right = len(self.sorted_arr) - 1
        
        while left < right:
            current_sum = self.sorted_arr[left][0] + self.sorted_arr[right][0]
            
            if current_sum == self.target:
                indices = [self.sorted_arr[left][1], self.sorted_arr[right][1]]
                results.append(indices)
                left += 1
                right -= 1
            elif current_sum < self.target:
                left += 1
            else:
                right -= 1
        
        return results
    
    def _compute_weighted_pairs(self):
        """Compute weighted pairs that sum to target."""
        results = []
        left = 0
        right = len(self.sorted_arr) - 1
        
        while left < right:
            current_sum = self.sorted_arr[left][0] + self.sorted_arr[right][0]
            
            if current_sum == self.target:
                indices = [self.sorted_arr[left][1], self.sorted_arr[right][1]]
                weighted_sum = sum(self.weights[idx] for idx in indices)
                results.append((indices, weighted_sum))
                left += 1
                right -= 1
            elif current_sum < self.target:
                left += 1
            else:
                right -= 1
        
        return results
    
    def get_pairs(self):
        """Get current pairs that sum to target."""
        return self.pairs
    
    def get_weighted_pairs(self):
        """Get current weighted pairs that sum to target."""
        return self.weighted_pairs
    
    def get_pairs_with_priority(self, priority_func):
        """Get pairs considering priority."""
        result = []
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            priority = priority_func(indices, values, weights, priorities)
            result.append((indices, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_pairs_with_optimization(self, optimization_func):
        """Get pairs using custom optimization function."""
        result = []
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            score = optimization_func(indices, values, weights, priorities)
            result.append((indices, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_pairs_with_constraints(self, constraint_func):
        """Get pairs that satisfy custom constraints."""
        result = []
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            if constraint_func(indices, values, weights, priorities):
                result.append(indices)
        return result
    
    def get_pairs_with_multiple_criteria(self, criteria_list):
        """Get pairs that satisfy multiple criteria."""
        result = []
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(indices, values, weights, priorities):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(indices)
        return result
    
    def get_pairs_with_alternatives(self, alternatives):
        """Get pairs considering alternative values."""
        result = []
        
        # Check original array
        for indices in self.pairs:
            result.append((indices, 'original'))
        
        # Check alternative values
        for i, alt_values in alternatives.items():
            if 0 <= i < self.n:
                for alt_value in alt_values:
                    # Create temporary array with alternative value
                    temp_arr = self.arr[:]
                    temp_arr[i] = alt_value
                    
                    # Calculate pairs for this alternative
                    temp_sorted = [(temp_arr[j], j) for j in range(self.n)]
                    temp_sorted.sort()
                    
                    left = 0
                    right = len(temp_sorted) - 1
                    
                    while left < right:
                        current_sum = temp_sorted[left][0] + temp_sorted[right][0]
                        
                        if current_sum == self.target:
                            indices = [temp_sorted[left][1], temp_sorted[right][1]]
                            result.append((indices, f'alternative_{alt_value}'))
                            left += 1
                            right -= 1
                        elif current_sum < self.target:
                            left += 1
                        else:
                            right -= 1
        
        return result
    
    def get_pairs_with_adaptive_criteria(self, adaptive_func):
        """Get pairs using adaptive criteria."""
        result = []
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            if adaptive_func(indices, values, weights, priorities, result):
                result.append(indices)
        return result
    
    def get_pair_optimization(self):
        """Get optimal pair configuration."""
        strategies = [
            ('pairs', lambda: len(self.pairs)),
            ('weighted_pairs', lambda: len(self.weighted_pairs)),
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
arr = [1, 2, 3, 4, 5, 6, 7, 8]
target = 9
weights = [2, 1, 3, 1, 2, 1, 3, 1]
priorities = [1, 2, 1, 3, 1, 2, 1, 3]
advanced_two_sum = AdvancedSumOfTwoValues(arr, target, weights, priorities)

print(f"Pairs: {len(advanced_two_sum.get_pairs())}")
print(f"Weighted pairs: {len(advanced_two_sum.get_weighted_pairs())}")

# Get pairs with priority
def priority_func(indices, values, weights, priorities):
    return sum(weights) * sum(priorities)

print(f"Pairs with priority: {advanced_two_sum.get_pairs_with_priority(priority_func)}")

# Get pairs with optimization
def optimization_func(indices, values, weights, priorities):
    return sum(values) * sum(weights) + sum(priorities)

print(f"Pairs with optimization: {advanced_two_sum.get_pairs_with_optimization(optimization_func)}")

# Get pairs with constraints
def constraint_func(indices, values, weights, priorities):
    return all(v > 2 for v in values) and sum(weights) > 3

print(f"Pairs with constraints: {advanced_two_sum.get_pairs_with_constraints(constraint_func)}")

# Get pairs with multiple criteria
def criterion1(indices, values, weights, priorities):
    return all(v > 2 for v in values)

def criterion2(indices, values, weights, priorities):
    return sum(weights) > 3

criteria_list = [criterion1, criterion2]
print(f"Pairs with multiple criteria: {advanced_two_sum.get_pairs_with_multiple_criteria(criteria_list)}")

# Get pairs with alternatives
alternatives = {1: [3, 5], 3: [6, 8]}
print(f"Pairs with alternatives: {advanced_two_sum.get_pairs_with_alternatives(alternatives)}")

# Get pairs with adaptive criteria
def adaptive_func(indices, values, weights, priorities, current_result):
    return all(v > 2 for v in values) and len(current_result) < 5

print(f"Pairs with adaptive criteria: {advanced_two_sum.get_pairs_with_adaptive_criteria(adaptive_func)}")

# Get pair optimization
print(f"Pair optimization: {advanced_two_sum.get_pair_optimization()}")
```

### **Variation 3: Sum of Two Values with Constraints**
**Problem**: Handle sum of two values with additional constraints (cost limits, distance constraints, resource constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedSumOfTwoValues:
    def __init__(self, arr, target, constraints=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.constraints = constraints or {}
        self.sorted_arr = self._create_sorted_array()
        self.pairs = self._compute_pairs()
    
    def _create_sorted_array(self):
        """Create sorted array with original indices."""
        indexed_arr = [(self.arr[i], i) for i in range(self.n)]
        indexed_arr.sort()
        return indexed_arr
    
    def _compute_pairs(self):
        """Compute all pairs that sum to target."""
        results = []
        left = 0
        right = len(self.sorted_arr) - 1
        
        while left < right:
            current_sum = self.sorted_arr[left][0] + self.sorted_arr[right][0]
            
            if current_sum == self.target:
                indices = [self.sorted_arr[left][1], self.sorted_arr[right][1]]
                results.append(indices)
                left += 1
                right -= 1
            elif current_sum < self.target:
                left += 1
            else:
                right -= 1
        
        return results
    
    def get_pairs_with_cost_constraints(self, cost_limit):
        """Get pairs considering cost constraints."""
        result = []
        total_cost = 0
        
        for indices in self.pairs:
            # Calculate cost for this pair
            cost = sum(abs(self.arr[i]) for i in indices)  # Simple cost model
            if total_cost + cost <= cost_limit:
                result.append(indices)
                total_cost += cost
        
        return result
    
    def get_pairs_with_distance_constraints(self, min_distance, max_distance):
        """Get pairs considering distance constraints."""
        result = []
        
        for indices in self.pairs:
            # Check distance constraints
            distance = abs(indices[0] - indices[1])
            if min_distance <= distance <= max_distance:
                result.append(indices)
        
        return result
    
    def get_pairs_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get pairs considering resource constraints."""
        result = []
        current_resources = [0] * len(resource_limits)
        
        for indices in self.pairs:
            # Check resource constraints
            can_afford = True
            for idx in indices:
                consumption = resource_consumption.get(idx, [0] * len(resource_limits))
                for j, res_consumption in enumerate(consumption):
                    if current_resources[j] + res_consumption > resource_limits[j]:
                        can_afford = False
                        break
                if not can_afford:
                    break
            
            if can_afford:
                result.append(indices)
                for idx in indices:
                    consumption = resource_consumption.get(idx, [0] * len(resource_limits))
                    for j, res_consumption in enumerate(consumption):
                        current_resources[j] += res_consumption
        
        return result
    
    def get_pairs_with_mathematical_constraints(self, constraint_func):
        """Get pairs that satisfy custom mathematical constraints."""
        result = []
        
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            if constraint_func(indices, values):
                result.append(indices)
        
        return result
    
    def get_pairs_with_range_constraints(self, range_constraints):
        """Get pairs that satisfy range constraints."""
        result = []
        
        for indices in self.pairs:
            # Check if pair satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(indices, [self.arr[i] for i in indices]):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                result.append(indices)
        
        return result
    
    def get_pairs_with_optimization_constraints(self, optimization_func):
        """Get pairs using custom optimization constraints."""
        # Sort pairs by optimization function
        all_pairs = []
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            score = optimization_func(indices, values)
            all_pairs.append((indices, score))
        
        # Sort by optimization score
        all_pairs.sort(key=lambda x: x[1], reverse=True)
        
        return [indices for indices, _ in all_pairs]
    
    def get_pairs_with_multiple_constraints(self, constraints_list):
        """Get pairs that satisfy multiple constraints."""
        result = []
        
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            # Check if pair satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(indices, values):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                result.append(indices)
        
        return result
    
    def get_pairs_with_priority_constraints(self, priority_func):
        """Get pairs with priority-based constraints."""
        # Sort pairs by priority
        all_pairs = []
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            priority = priority_func(indices, values)
            all_pairs.append((indices, priority))
        
        # Sort by priority
        all_pairs.sort(key=lambda x: x[1], reverse=True)
        
        return [indices for indices, _ in all_pairs]
    
    def get_pairs_with_adaptive_constraints(self, adaptive_func):
        """Get pairs with adaptive constraints."""
        result = []
        
        for indices in self.pairs:
            values = [self.arr[i] for i in indices]
            # Check adaptive constraints
            if adaptive_func(indices, values, result):
                result.append(indices)
        
        return result
    
    def get_optimal_pair_strategy(self):
        """Get optimal pair strategy considering all constraints."""
        strategies = [
            ('cost_constraints', self.get_pairs_with_cost_constraints),
            ('distance_constraints', self.get_pairs_with_distance_constraints),
            ('resource_constraints', self.get_pairs_with_resource_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'cost_constraints':
                    current_count = len(strategy_func(100))  # Cost limit of 100
                elif strategy_name == 'distance_constraints':
                    current_count = len(strategy_func(1, 10))  # Distance between 1 and 10
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {i: [10, 5] for i in range(self.n)}
                    current_count = len(strategy_func(resource_limits, resource_consumption))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'max_cost': 100,
    'min_distance': 1,
    'max_distance': 10
}

arr = [1, 2, 3, 4, 5, 6, 7, 8]
target = 9
constrained_two_sum = ConstrainedSumOfTwoValues(arr, target, constraints)

print("Cost-constrained pairs:", len(constrained_two_sum.get_pairs_with_cost_constraints(100)))

print("Distance-constrained pairs:", len(constrained_two_sum.get_pairs_with_distance_constraints(1, 10)))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(arr))}
print("Resource-constrained pairs:", len(constrained_two_sum.get_pairs_with_resource_constraints(resource_limits, resource_consumption)))

# Mathematical constraints
def custom_constraint(indices, values):
    return all(v > 2 for v in values) and len(set(indices)) == 2

print("Mathematical constraint pairs:", len(constrained_two_sum.get_pairs_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(indices, values):
    return all(0 <= idx < len(arr) for idx in indices)

range_constraints = [range_constraint]
print("Range-constrained pairs:", len(constrained_two_sum.get_pairs_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(indices, values):
    return all(v > 2 for v in values)

def constraint2(indices, values):
    return len(set(indices)) == 2

constraints_list = [constraint1, constraint2]
print("Multiple constraints pairs:", len(constrained_two_sum.get_pairs_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(indices, values):
    return sum(values)

print("Priority-constrained pairs:", len(constrained_two_sum.get_pairs_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(indices, values, current_result):
    return all(v > 2 for v in values) and len(current_result) < 10

print("Adaptive constraint pairs:", len(constrained_two_sum.get_pairs_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_two_sum.get_optimal_pair_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Sum of Two Values](https://cses.fi/problemset/task/1640) - Basic sum of two values problem
- [Sum of Three Values](https://cses.fi/problemset/task/1641) - Three values variant
- [Sum of Four Values](https://cses.fi/problemset/task/1642) - Four values variant

#### **LeetCode Problems**
- [Two Sum](https://leetcode.com/problems/two-sum/) - Basic two sum problem
- [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) - Sorted array variant
- [Two Sum III - Data Structure Design](https://leetcode.com/problems/two-sum-iii-data-structure-design/) - Design data structure
- [Two Sum IV - Input is a BST](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/) - BST variant

#### **Problem Categories**
- **Hash Maps**: Key-value lookups, complement search, efficient searching
- **Two Pointers**: Sorted array algorithms, efficient pairing, pointer techniques
- **Array Processing**: Element searching, pair finding, index manipulation
- **Algorithm Design**: Hash-based algorithms, two-pointer techniques, search optimization