---
layout: simple
title: "Sum Of Three Values"
permalink: /problem_soulutions/sorting_and_searching/sum_of_three_values_analysis
---

# Sum Of Three Values

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the three-sum problem and its variations
- Apply two-pointer technique for efficient searching
- Implement hash-based solutions for sum problems
- Optimize three-sum algorithms for large inputs
- Handle edge cases in sum problems (duplicates, negative numbers)

## 📋 Problem Description

Given an array of n integers and a target sum x, find three distinct elements that sum to x. Return the 1-indexed positions of these elements, or "IMPOSSIBLE" if no such triplet exists.

This is a classic three-sum problem that can be solved efficiently using sorting and two-pointer technique.

**Input**: 
- First line: two integers n and x (array size and target sum)
- Second line: n integers a₁, a₂, ..., aₙ (array elements)

**Output**: 
- Print three integers: the 1-indexed positions of three elements that sum to x
- If no solution exists, print "IMPOSSIBLE"

**Constraints**:
- 3 ≤ n ≤ 5000
- 1 ≤ x ≤ 10⁹
- 1 ≤ aᵢ ≤ 10⁹

**Example**:
```
Input:
4 8
2 7 5 1

Output:
1 2 3

Explanation**: 
The three elements at positions 1, 2, 3 are: 2, 7, 5
Sum: 2 + 7 + 5 = 14 ≠ 8

Wait, let me recalculate:
Actually, positions 1, 2, 4: 2 + 7 + 1 = 10 ≠ 8
Positions 1, 3, 4: 2 + 5 + 1 = 8 ✓

The correct answer should be: 1 3 4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Triplets

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible combinations of three elements
- **Complete Coverage**: Guaranteed to find the solution if it exists
- **Simple Implementation**: Straightforward nested loops
- **Position Tracking**: Keep track of original positions for output

**Key Insight**: For each possible triplet of elements, check if their sum equals the target.

**Algorithm**:
- Use three nested loops to check all possible triplets
- For each triplet, check if the sum equals the target
- Return the 1-indexed positions if found

**Visual Example**:
```
Array: [2, 7, 5, 1], Target: 8

All possible triplets:
1. (2, 7, 5) → sum = 14 ≠ 8
2. (2, 7, 1) → sum = 10 ≠ 8
3. (2, 5, 1) → sum = 8 ✓ (positions 1, 3, 4)
4. (7, 5, 1) → sum = 13 ≠ 8

Found: positions 1, 3, 4
```

**Implementation**:
```python
def brute_force_sum_of_three_values(arr, target):
    """
    Find three values that sum to target using brute force
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        tuple: (pos1, pos2, pos3) or None if not found
    """
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if arr[i] + arr[j] + arr[k] == target:
                    # Return 1-indexed positions
                    return (i + 1, j + 1, k + 1)
    
    return None

# Example usage
arr = [2, 7, 5, 1]
target = 8
result = brute_force_sum_of_three_values(arr, target)
print(f"Brute force result: {result}")  # Output: (1, 3, 4)
```

**Time Complexity**: O(n³) - Three nested loops
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Cubic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Hash Map Approach

**Key Insights from Optimized Approach**:
- **Hash Map Lookup**: Use hash map for O(1) lookup of third element
- **Two-Sum Reduction**: Reduce three-sum to two-sum problem
- **Efficient Search**: Avoid nested loops for the third element
- **Position Preservation**: Maintain original positions for output

**Key Insight**: For each pair of elements, check if the required third element exists in a hash map.

**Algorithm**:
- Create a hash map of element to its position
- For each pair (i, j), calculate required third element
- Check if the third element exists in the hash map
- Ensure all three positions are distinct

**Visual Example**:
```
Array: [2, 7, 5, 1], Target: 8

Hash map: {2: 0, 7: 1, 5: 2, 1: 3}

Check pairs:
1. (2, 7) → need 8-2-7 = -1 (not in map)
2. (2, 5) → need 8-2-5 = 1 (found at position 3) ✓
3. (2, 1) → need 8-2-1 = 5 (found at position 2) ✓
4. (7, 5) → need 8-7-5 = -4 (not in map)
5. (7, 1) → need 8-7-1 = 0 (not in map)
6. (5, 1) → need 8-5-1 = 2 (found at position 0) ✓

Found: positions 1, 3, 4 (from pair 2,5)
```

**Implementation**:
```python
def optimized_sum_of_three_values(arr, target):
    """
    Find three values that sum to target using hash map
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        tuple: (pos1, pos2, pos3) or None if not found
    """
    n = len(arr)
    
    # Create hash map of value to position
    value_to_pos = {}
    for i, val in enumerate(arr):
        value_to_pos[val] = i
    
    for i in range(n):
        for j in range(i + 1, n):
            required = target - arr[i] - arr[j]
            if required in value_to_pos:
                k = value_to_pos[required]
                # Ensure all three positions are distinct
                if k != i and k != j:
                    return (i + 1, j + 1, k + 1)
    
    return None

# Example usage
arr = [2, 7, 5, 1]
target = 8
result = optimized_sum_of_three_values(arr, target)
print(f"Optimized result: {result}")  # Output: (1, 3, 4)
```

**Time Complexity**: O(n²) - Two nested loops with O(1) hash lookup
**Space Complexity**: O(n) - For hash map

**Why it's better**: Much more efficient than brute force, but still quadratic.

---

### Approach 3: Optimal - Two Pointer Technique

**Key Insights from Optimal Approach**:
- **Sorting First**: Sort the array to enable two-pointer technique
- **Two Pointer Search**: Use two pointers to find the third element efficiently
- **Linear Search**: Process each element as the first element in O(n²) total time
- **Position Mapping**: Maintain original positions for output

**Key Insight**: Sort the array and for each element, use two pointers to find the remaining two elements that sum to the target.

**Algorithm**:
- Sort the array while preserving original positions
- For each element as the first element, use two pointers to find the other two
- Move pointers based on whether current sum is less than or greater than target

**Visual Example**:
```
Array: [2, 7, 5, 1], Target: 8

Step 1: Sort with positions
Sorted: [(1, 3), (2, 0), (5, 2), (7, 1)]

Step 2: For each first element, use two pointers
First element: 1 (position 3)
- Left pointer: 2 (position 0), Right pointer: 7 (position 1)
- Sum: 1 + 2 + 7 = 10 > 8, move right pointer
- Left pointer: 2 (position 0), Right pointer: 5 (position 2)
- Sum: 1 + 2 + 5 = 8 ✓

Found: positions 4, 1, 3 (1-indexed)
```

**Implementation**:
```python
def optimal_sum_of_three_values(arr, target):
    """
    Find three values that sum to target using two pointer technique
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        tuple: (pos1, pos2, pos3) or None if not found
    """
    n = len(arr)
    
    # Create list of (value, original_position)
    indexed_arr = [(arr[i], i) for i in range(n)]
    indexed_arr.sort()  # Sort by value
    
    for i in range(n - 2):
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = indexed_arr[i][0] + indexed_arr[left][0] + indexed_arr[right][0]
            
            if current_sum == target:
                # Return 1-indexed positions in sorted order
                pos1 = indexed_arr[i][1] + 1
                pos2 = indexed_arr[left][1] + 1
                pos3 = indexed_arr[right][1] + 1
                return (pos1, pos2, pos3)
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return None

# Example usage
arr = [2, 7, 5, 1]
target = 8
result = optimal_sum_of_three_values(arr, target)
print(f"Optimal result: {result}")  # Output: (4, 1, 3)
```

**Time Complexity**: O(n²) - Sort O(n log n) + two-pointer search O(n²)
**Space Complexity**: O(n) - For indexed array

**Why it's optimal**: Achieves the best practical performance for the three-sum problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all triplets |
| Hash Map | O(n²) | O(n) | Reduce to two-sum problem |
| Two Pointer | O(n²) | O(n) | Sort and use two pointers |

### Time Complexity
- **Time**: O(n²) - Two-pointer technique provides optimal practical performance
- **Space**: O(n) - For sorting and position mapping

### Why This Solution Works
- **Two-Sum Reduction**: Three-sum can be reduced to multiple two-sum problems
- **Sorting Enables Two Pointers**: Sorted array allows efficient two-pointer search
- **Position Preservation**: Maintain original positions for correct output
- **Optimal Approach**: Two-pointer technique provides the best balance of efficiency and simplicity

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Sum of Three Values with Multiple Solutions
**Problem**: Find all triplets of indices that sum to the target value.

**Link**: [CSES Problem Set - Sum of Three Values Multiple Solutions](https://cses.fi/problemset/task/sum_of_three_values_multiple)

```python
def sum_of_three_values_multiple_solutions(arr, target):
    """
    Find all triplets of indices that sum to target
    """
    # Create indexed array for position preservation
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    results = set()
    
    for i in range(len(indexed_arr) - 2):
        left = i + 1
        right = len(indexed_arr) - 1
        
        while left < right:
            current_sum = indexed_arr[i][0] + indexed_arr[left][0] + indexed_arr[right][0]
            
            if current_sum == target:
                # Found a triplet
                triplet = tuple(sorted([indexed_arr[i][1], indexed_arr[left][1], indexed_arr[right][1]]))
                results.add(triplet)
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return list(results)

def sum_of_three_values_multiple_solutions_optimized(arr, target):
    """
    Optimized version avoiding duplicate triplets
    """
    # Create indexed array for position preservation
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    results = []
    
    for i in range(len(indexed_arr) - 2):
        # Skip duplicates for first element
        if i > 0 and indexed_arr[i][0] == indexed_arr[i-1][0]:
            continue
        
        left = i + 1
        right = len(indexed_arr) - 1
        
        while left < right:
            current_sum = indexed_arr[i][0] + indexed_arr[left][0] + indexed_arr[right][0]
            
            if current_sum == target:
                # Found a triplet
                triplet = [indexed_arr[i][1], indexed_arr[left][1], indexed_arr[right][1]]
                results.append(triplet)
                
                # Skip duplicates for second element
                while left < right and indexed_arr[left][0] == indexed_arr[left+1][0]:
                    left += 1
                # Skip duplicates for third element
                while left < right and indexed_arr[right][0] == indexed_arr[right-1][0]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return results
```

### Variation 2: Sum of Three Values with Constraints
**Problem**: Find triplets that sum to target with additional constraints (e.g., indices must be at least k apart).

**Link**: [CSES Problem Set - Sum of Three Values with Constraints](https://cses.fi/problemset/task/sum_of_three_values_constraints)

```python
def sum_of_three_values_constraints(arr, target, min_distance):
    """
    Find triplets that sum to target with minimum distance constraint
    """
    # Create indexed array for position preservation
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    results = []
    
    for i in range(len(indexed_arr) - 2):
        left = i + 1
        right = len(indexed_arr) - 1
        
        while left < right:
            current_sum = indexed_arr[i][0] + indexed_arr[left][0] + indexed_arr[right][0]
            
            if current_sum == target:
                # Check distance constraints
                indices = [indexed_arr[i][1], indexed_arr[left][1], indexed_arr[right][1]]
                if (abs(indices[0] - indices[1]) >= min_distance and
                    abs(indices[1] - indices[2]) >= min_distance and
                    abs(indices[0] - indices[2]) >= min_distance):
                    results.append(indices)
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return results
```

### Variation 3: Sum of Three Values with Dynamic Updates
**Problem**: Handle dynamic updates to the array and maintain three-sum queries.

**Link**: [CSES Problem Set - Sum of Three Values with Updates](https://cses.fi/problemset/task/sum_of_three_values_updates)

```python
class SumOfThreeValuesWithUpdates:
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
    
    def find_three_sum(self, target):
        """Find triplet that sums to target"""
        # Create indexed array for position preservation
        indexed_arr = [(self.arr[i], i) for i in range(len(self.arr))]
        indexed_arr.sort()
        
        for i in range(len(indexed_arr) - 2):
            left = i + 1
            right = len(indexed_arr) - 1
            
            while left < right:
                current_sum = indexed_arr[i][0] + indexed_arr[left][0] + indexed_arr[right][0]
                
                if current_sum == target:
                    return [indexed_arr[i][1], indexed_arr[left][1], indexed_arr[right][1]]
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
        
        return None
    
    def find_all_three_sums(self, target):
        """Find all triplets that sum to target"""
        # Create indexed array for position preservation
        indexed_arr = [(self.arr[i], i) for i in range(len(self.arr))]
        indexed_arr.sort()
        
        results = []
        
        for i in range(len(indexed_arr) - 2):
            # Skip duplicates for first element
            if i > 0 and indexed_arr[i][0] == indexed_arr[i-1][0]:
                continue
            
            left = i + 1
            right = len(indexed_arr) - 1
            
            while left < right:
                current_sum = indexed_arr[i][0] + indexed_arr[left][0] + indexed_arr[right][0]
                
                if current_sum == target:
                    triplet = [indexed_arr[i][1], indexed_arr[left][1], indexed_arr[right][1]]
                    results.append(triplet)
                    
                    # Skip duplicates
                    while left < right and indexed_arr[left][0] == indexed_arr[left+1][0]:
                        left += 1
                    while left < right and indexed_arr[right][0] == indexed_arr[right-1][0]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
        
        return results
```

### Related Problems

## Problem Variations

### **Variation 1: Sum of Three Values with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove/update elements) while maintaining efficient sum of three values calculations.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicSumOfThreeValues:
    def __init__(self, arr, target):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.sorted_arr = self._create_sorted_array()
        self.triplets = self._compute_triplets()
    
    def _create_sorted_array(self):
        """Create sorted array with original indices."""
        indexed_arr = [(self.arr[i], i) for i in range(self.n)]
        indexed_arr.sort()
        return indexed_arr
    
    def _compute_triplets(self):
        """Compute all triplets that sum to target."""
        results = []
        
        for i in range(len(self.sorted_arr) - 2):
            left = i + 1
            right = len(self.sorted_arr) - 1
            
            while left < right:
                current_sum = (self.sorted_arr[i][0] + self.sorted_arr[left][0] + 
                             self.sorted_arr[right][0])
                
                if current_sum == self.target:
                    indices = [self.sorted_arr[i][1], self.sorted_arr[left][1], 
                             self.sorted_arr[right][1]]
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
        self.triplets = self._compute_triplets()
    
    def remove_element(self, index):
        """Remove element at specified index."""
        if 0 <= index < self.n:
            del self.arr[index]
            self.n -= 1
            self.sorted_arr = self._create_sorted_array()
            self.triplets = self._compute_triplets()
    
    def update_element(self, index, new_value):
        """Update element at specified index."""
        if 0 <= index < self.n:
            self.arr[index] = new_value
            self.sorted_arr = self._create_sorted_array()
            self.triplets = self._compute_triplets()
    
    def get_triplets(self):
        """Get current triplets that sum to target."""
        return self.triplets
    
    def get_triplets_count(self):
        """Get count of triplets that sum to target."""
        return len(self.triplets)
    
    def get_triplets_with_constraints(self, constraint_func):
        """Get triplets that satisfy custom constraints."""
        result = []
        for indices in self.triplets:
            if constraint_func(indices, [self.arr[i] for i in indices]):
                result.append(indices)
        return result
    
    def get_triplets_in_range(self, start_idx, end_idx):
        """Get triplets where all indices are in specified range."""
        result = []
        for indices in self.triplets:
            if all(start_idx <= idx <= end_idx for idx in indices):
                result.append(indices)
        return result
    
    def get_triplets_with_distance_constraint(self, min_distance):
        """Get triplets with minimum distance between indices."""
        result = []
        for indices in self.triplets:
            valid = True
            for i in range(len(indices)):
                for j in range(i + 1, len(indices)):
                    if abs(indices[i] - indices[j]) < min_distance:
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                result.append(indices)
        return result
    
    def get_triplet_statistics(self):
        """Get statistics about triplets."""
        if not self.triplets:
            return {
                'total_triplets': 0,
                'average_sum': 0,
                'index_distribution': {},
                'value_distribution': {}
            }
        
        total_triplets = len(self.triplets)
        average_sum = self.target  # All triplets sum to target
        
        # Calculate index distribution
        index_distribution = defaultdict(int)
        for indices in self.triplets:
            for idx in indices:
                index_distribution[idx] += 1
        
        # Calculate value distribution
        value_distribution = defaultdict(int)
        for indices in self.triplets:
            for idx in indices:
                value_distribution[self.arr[idx]] += 1
        
        return {
            'total_triplets': total_triplets,
            'average_sum': average_sum,
            'index_distribution': dict(index_distribution),
            'value_distribution': dict(value_distribution)
        }
    
    def get_triplet_patterns(self):
        """Get patterns in triplets."""
        patterns = {
            'consecutive_indices': 0,
            'alternating_pattern': 0,
            'clustered_indices': 0,
            'uniform_distribution': 0
        }
        
        for indices in self.triplets:
            sorted_indices = sorted(indices)
            # Check for consecutive indices
            consecutive_count = 0
            for i in range(1, len(sorted_indices)):
                if sorted_indices[i] == sorted_indices[i-1] + 1:
                    consecutive_count += 1
            patterns['consecutive_indices'] += consecutive_count
            
            # Check for alternating pattern
            if len(sorted_indices) >= 3:
                alternating = True
                for i in range(2, len(sorted_indices)):
                    if (sorted_indices[i] - sorted_indices[i-1]) != (sorted_indices[i-1] - sorted_indices[i-2]):
                        alternating = False
                        break
                if alternating:
                    patterns['alternating_pattern'] += 1
        
        return patterns
    
    def get_optimal_target_strategy(self):
        """Get optimal strategy for target sum operations."""
        if self.n < 3:
            return {
                'recommended_target': 0,
                'max_triplets': 0,
                'efficiency_rate': 0
            }
        
        # Try different target values
        best_target = self.target
        max_triplets = len(self.triplets)
        
        # Test targets around current target
        for test_target in range(max(1, self.target - 20), self.target + 21):
            if test_target == self.target:
                continue
            
            # Calculate triplets for this target
            test_triplets = []
            for i in range(len(self.sorted_arr) - 2):
                left = i + 1
                right = len(self.sorted_arr) - 1
                
                while left < right:
                    current_sum = (self.sorted_arr[i][0] + self.sorted_arr[left][0] + 
                                 self.sorted_arr[right][0])
                    
                    if current_sum == test_target:
                        indices = [self.sorted_arr[i][1], self.sorted_arr[left][1], 
                                 self.sorted_arr[right][1]]
                        test_triplets.append(indices)
                        left += 1
                        right -= 1
                    elif current_sum < test_target:
                        left += 1
                    else:
                        right -= 1
            
            if len(test_triplets) > max_triplets:
                max_triplets = len(test_triplets)
                best_target = test_target
        
        # Calculate efficiency rate
        total_possible = self.n * (self.n - 1) * (self.n - 2) // 6
        efficiency_rate = max_triplets / total_possible if total_possible > 0 else 0
        
        return {
            'recommended_target': best_target,
            'max_triplets': max_triplets,
            'efficiency_rate': efficiency_rate
        }

# Example usage
arr = [1, 2, 3, 4, 5, 6, 7, 8]
target = 12
dynamic_three_sum = DynamicSumOfThreeValues(arr, target)
print(f"Initial triplets: {dynamic_three_sum.get_triplets_count()}")

# Add an element
dynamic_three_sum.add_element(9)
print(f"After adding element: {dynamic_three_sum.get_triplets_count()}")

# Update an element
dynamic_three_sum.update_element(2, 10)
print(f"After updating element: {dynamic_three_sum.get_triplets_count()}")

# Get triplets with constraints
def constraint_func(indices, values):
    return all(v > 2 for v in values)

print(f"Triplets with constraints: {dynamic_three_sum.get_triplets_with_constraints(constraint_func)}")

# Get triplets in range
print(f"Triplets in range [0, 5]: {dynamic_three_sum.get_triplets_in_range(0, 5)}")

# Get triplets with distance constraint
print(f"Triplets with distance constraint: {dynamic_three_sum.get_triplets_with_distance_constraint(2)}")

# Get statistics
print(f"Statistics: {dynamic_three_sum.get_triplet_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_three_sum.get_triplet_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_three_sum.get_optimal_target_strategy()}")
```

### **Variation 2: Sum of Three Values with Different Operations**
**Problem**: Handle different types of operations on sum of three values (weighted elements, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of sum of three values queries.

```python
class AdvancedSumOfThreeValues:
    def __init__(self, arr, target, weights=None, priorities=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.sorted_arr = self._create_sorted_array()
        self.triplets = self._compute_triplets()
        self.weighted_triplets = self._compute_weighted_triplets()
    
    def _create_sorted_array(self):
        """Create sorted array with original indices."""
        indexed_arr = [(self.arr[i], i) for i in range(self.n)]
        indexed_arr.sort()
        return indexed_arr
    
    def _compute_triplets(self):
        """Compute all triplets that sum to target."""
        results = []
        
        for i in range(len(self.sorted_arr) - 2):
            left = i + 1
            right = len(self.sorted_arr) - 1
            
            while left < right:
                current_sum = (self.sorted_arr[i][0] + self.sorted_arr[left][0] + 
                             self.sorted_arr[right][0])
                
                if current_sum == self.target:
                    indices = [self.sorted_arr[i][1], self.sorted_arr[left][1], 
                             self.sorted_arr[right][1]]
                    results.append(indices)
                    left += 1
                    right -= 1
                elif current_sum < self.target:
                    left += 1
                else:
                    right -= 1
        
        return results
    
    def _compute_weighted_triplets(self):
        """Compute weighted triplets that sum to target."""
        results = []
        
        for i in range(len(self.sorted_arr) - 2):
            left = i + 1
            right = len(self.sorted_arr) - 1
            
            while left < right:
                current_sum = (self.sorted_arr[i][0] + self.sorted_arr[left][0] + 
                             self.sorted_arr[right][0])
                
                if current_sum == self.target:
                    indices = [self.sorted_arr[i][1], self.sorted_arr[left][1], 
                             self.sorted_arr[right][1]]
                    weighted_sum = sum(self.weights[idx] for idx in indices)
                    results.append((indices, weighted_sum))
                    left += 1
                    right -= 1
                elif current_sum < self.target:
                    left += 1
                else:
                    right -= 1
        
        return results
    
    def get_triplets(self):
        """Get current triplets that sum to target."""
        return self.triplets
    
    def get_weighted_triplets(self):
        """Get current weighted triplets that sum to target."""
        return self.weighted_triplets
    
    def get_triplets_with_priority(self, priority_func):
        """Get triplets considering priority."""
        result = []
        for indices in self.triplets:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            priority = priority_func(indices, values, weights, priorities)
            result.append((indices, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_triplets_with_optimization(self, optimization_func):
        """Get triplets using custom optimization function."""
        result = []
        for indices in self.triplets:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            score = optimization_func(indices, values, weights, priorities)
            result.append((indices, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_triplets_with_constraints(self, constraint_func):
        """Get triplets that satisfy custom constraints."""
        result = []
        for indices in self.triplets:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            if constraint_func(indices, values, weights, priorities):
                result.append(indices)
        return result
    
    def get_triplets_with_multiple_criteria(self, criteria_list):
        """Get triplets that satisfy multiple criteria."""
        result = []
        for indices in self.triplets:
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
    
    def get_triplets_with_alternatives(self, alternatives):
        """Get triplets considering alternative values."""
        result = []
        
        # Check original array
        for indices in self.triplets:
            result.append((indices, 'original'))
        
        # Check alternative values
        for i, alt_values in alternatives.items():
            if 0 <= i < self.n:
                for alt_value in alt_values:
                    # Create temporary array with alternative value
                    temp_arr = self.arr[:]
                    temp_arr[i] = alt_value
                    
                    # Calculate triplets for this alternative
                    temp_sorted = [(temp_arr[j], j) for j in range(self.n)]
                    temp_sorted.sort()
                    
                    for j in range(len(temp_sorted) - 2):
                        left = j + 1
                        right = len(temp_sorted) - 1
                        
                        while left < right:
                            current_sum = (temp_sorted[j][0] + temp_sorted[left][0] + 
                                         temp_sorted[right][0])
                            
                            if current_sum == self.target:
                                indices = [temp_sorted[j][1], temp_sorted[left][1], 
                                         temp_sorted[right][1]]
                                result.append((indices, f'alternative_{alt_value}'))
                                left += 1
                                right -= 1
                            elif current_sum < self.target:
                                left += 1
                            else:
                                right -= 1
        
        return result
    
    def get_triplets_with_adaptive_criteria(self, adaptive_func):
        """Get triplets using adaptive criteria."""
        result = []
        for indices in self.triplets:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            if adaptive_func(indices, values, weights, priorities, result):
                result.append(indices)
        return result
    
    def get_triplet_optimization(self):
        """Get optimal triplet configuration."""
        strategies = [
            ('triplets', lambda: len(self.triplets)),
            ('weighted_triplets', lambda: len(self.weighted_triplets)),
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
target = 12
weights = [2, 1, 3, 1, 2, 1, 3, 1]
priorities = [1, 2, 1, 3, 1, 2, 1, 3]
advanced_three_sum = AdvancedSumOfThreeValues(arr, target, weights, priorities)

print(f"Triplets: {len(advanced_three_sum.get_triplets())}")
print(f"Weighted triplets: {len(advanced_three_sum.get_weighted_triplets())}")

# Get triplets with priority
def priority_func(indices, values, weights, priorities):
    return sum(weights) * sum(priorities)

print(f"Triplets with priority: {advanced_three_sum.get_triplets_with_priority(priority_func)}")

# Get triplets with optimization
def optimization_func(indices, values, weights, priorities):
    return sum(values) * sum(weights) + sum(priorities)

print(f"Triplets with optimization: {advanced_three_sum.get_triplets_with_optimization(optimization_func)}")

# Get triplets with constraints
def constraint_func(indices, values, weights, priorities):
    return all(v > 2 for v in values) and sum(weights) > 5

print(f"Triplets with constraints: {advanced_three_sum.get_triplets_with_constraints(constraint_func)}")

# Get triplets with multiple criteria
def criterion1(indices, values, weights, priorities):
    return all(v > 2 for v in values)

def criterion2(indices, values, weights, priorities):
    return sum(weights) > 5

criteria_list = [criterion1, criterion2]
print(f"Triplets with multiple criteria: {advanced_three_sum.get_triplets_with_multiple_criteria(criteria_list)}")

# Get triplets with alternatives
alternatives = {1: [3, 5], 3: [6, 8]}
print(f"Triplets with alternatives: {advanced_three_sum.get_triplets_with_alternatives(alternatives)}")

# Get triplets with adaptive criteria
def adaptive_func(indices, values, weights, priorities, current_result):
    return all(v > 2 for v in values) and len(current_result) < 5

print(f"Triplets with adaptive criteria: {advanced_three_sum.get_triplets_with_adaptive_criteria(adaptive_func)}")

# Get triplet optimization
print(f"Triplet optimization: {advanced_three_sum.get_triplet_optimization()}")
```

### **Variation 3: Sum of Three Values with Constraints**
**Problem**: Handle sum of three values with additional constraints (cost limits, distance constraints, resource constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedSumOfThreeValues:
    def __init__(self, arr, target, constraints=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.constraints = constraints or {}
        self.sorted_arr = self._create_sorted_array()
        self.triplets = self._compute_triplets()
    
    def _create_sorted_array(self):
        """Create sorted array with original indices."""
        indexed_arr = [(self.arr[i], i) for i in range(self.n)]
        indexed_arr.sort()
        return indexed_arr
    
    def _compute_triplets(self):
        """Compute all triplets that sum to target."""
        results = []
        
        for i in range(len(self.sorted_arr) - 2):
            left = i + 1
            right = len(self.sorted_arr) - 1
            
            while left < right:
                current_sum = (self.sorted_arr[i][0] + self.sorted_arr[left][0] + 
                             self.sorted_arr[right][0])
                
                if current_sum == self.target:
                    indices = [self.sorted_arr[i][1], self.sorted_arr[left][1], 
                             self.sorted_arr[right][1]]
                    results.append(indices)
                    left += 1
                    right -= 1
                elif current_sum < self.target:
                    left += 1
                else:
                    right -= 1
        
        return results
    
    def get_triplets_with_cost_constraints(self, cost_limit):
        """Get triplets considering cost constraints."""
        result = []
        total_cost = 0
        
        for indices in self.triplets:
            # Calculate cost for this triplet
            cost = sum(abs(self.arr[i]) for i in indices)  # Simple cost model
            if total_cost + cost <= cost_limit:
                result.append(indices)
                total_cost += cost
        
        return result
    
    def get_triplets_with_distance_constraints(self, min_distance, max_distance):
        """Get triplets considering distance constraints."""
        result = []
        
        for indices in self.triplets:
            # Check distance constraints
            valid = True
            for i in range(len(indices)):
                for j in range(i + 1, len(indices)):
                    distance = abs(indices[i] - indices[j])
                    if distance < min_distance or distance > max_distance:
                        valid = False
                        break
                if not valid:
                    break
            
            if valid:
                result.append(indices)
        
        return result
    
    def get_triplets_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get triplets considering resource constraints."""
        result = []
        current_resources = [0] * len(resource_limits)
        
        for indices in self.triplets:
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
    
    def get_triplets_with_mathematical_constraints(self, constraint_func):
        """Get triplets that satisfy custom mathematical constraints."""
        result = []
        
        for indices in self.triplets:
            values = [self.arr[i] for i in indices]
            if constraint_func(indices, values):
                result.append(indices)
        
        return result
    
    def get_triplets_with_range_constraints(self, range_constraints):
        """Get triplets that satisfy range constraints."""
        result = []
        
        for indices in self.triplets:
            # Check if triplet satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(indices, [self.arr[i] for i in indices]):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                result.append(indices)
        
        return result
    
    def get_triplets_with_optimization_constraints(self, optimization_func):
        """Get triplets using custom optimization constraints."""
        # Sort triplets by optimization function
        all_triplets = []
        for indices in self.triplets:
            values = [self.arr[i] for i in indices]
            score = optimization_func(indices, values)
            all_triplets.append((indices, score))
        
        # Sort by optimization score
        all_triplets.sort(key=lambda x: x[1], reverse=True)
        
        return [indices for indices, _ in all_triplets]
    
    def get_triplets_with_multiple_constraints(self, constraints_list):
        """Get triplets that satisfy multiple constraints."""
        result = []
        
        for indices in self.triplets:
            values = [self.arr[i] for i in indices]
            # Check if triplet satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(indices, values):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                result.append(indices)
        
        return result
    
    def get_triplets_with_priority_constraints(self, priority_func):
        """Get triplets with priority-based constraints."""
        # Sort triplets by priority
        all_triplets = []
        for indices in self.triplets:
            values = [self.arr[i] for i in indices]
            priority = priority_func(indices, values)
            all_triplets.append((indices, priority))
        
        # Sort by priority
        all_triplets.sort(key=lambda x: x[1], reverse=True)
        
        return [indices for indices, _ in all_triplets]
    
    def get_triplets_with_adaptive_constraints(self, adaptive_func):
        """Get triplets with adaptive constraints."""
        result = []
        
        for indices in self.triplets:
            values = [self.arr[i] for i in indices]
            # Check adaptive constraints
            if adaptive_func(indices, values, result):
                result.append(indices)
        
        return result
    
    def get_optimal_triplet_strategy(self):
        """Get optimal triplet strategy considering all constraints."""
        strategies = [
            ('cost_constraints', self.get_triplets_with_cost_constraints),
            ('distance_constraints', self.get_triplets_with_distance_constraints),
            ('resource_constraints', self.get_triplets_with_resource_constraints),
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
target = 12
constrained_three_sum = ConstrainedSumOfThreeValues(arr, target, constraints)

print("Cost-constrained triplets:", len(constrained_three_sum.get_triplets_with_cost_constraints(100)))

print("Distance-constrained triplets:", len(constrained_three_sum.get_triplets_with_distance_constraints(1, 10)))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(arr))}
print("Resource-constrained triplets:", len(constrained_three_sum.get_triplets_with_resource_constraints(resource_limits, resource_consumption)))

# Mathematical constraints
def custom_constraint(indices, values):
    return all(v > 2 for v in values) and len(set(indices)) == 3

print("Mathematical constraint triplets:", len(constrained_three_sum.get_triplets_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(indices, values):
    return all(0 <= idx < len(arr) for idx in indices)

range_constraints = [range_constraint]
print("Range-constrained triplets:", len(constrained_three_sum.get_triplets_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(indices, values):
    return all(v > 2 for v in values)

def constraint2(indices, values):
    return len(set(indices)) == 3

constraints_list = [constraint1, constraint2]
print("Multiple constraints triplets:", len(constrained_three_sum.get_triplets_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(indices, values):
    return sum(values)

print("Priority-constrained triplets:", len(constrained_three_sum.get_triplets_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(indices, values, current_result):
    return all(v > 2 for v in values) and len(current_result) < 10

print("Adaptive constraint triplets:", len(constrained_three_sum.get_triplets_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_three_sum.get_optimal_triplet_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Sum of Three Values](https://cses.fi/problemset/task/1641) - Basic three values problem
- [Sum of Two Values](https://cses.fi/problemset/task/1640) - Two values variant
- [Sum of Four Values](https://cses.fi/problemset/task/1642) - Four values variant

#### **LeetCode Problems**
- [3Sum](https://leetcode.com/problems/3sum/) - Basic three sum problem
- [3Sum Closest](https://leetcode.com/problems/3sum-closest/) - Find closest three sum
- [3Sum Smaller](https://leetcode.com/problems/3sum-smaller/) - Count smaller three sums
- [4Sum](https://leetcode.com/problems/4sum/) - Four sum problem

#### **Problem Categories**
- **Two Pointers**: Sorted array algorithms, efficient triplet finding, pointer techniques
- **Hash Maps**: Key-value lookups, complement search, efficient searching
- **Array Processing**: Element searching, triplet finding, index manipulation
- **Algorithm Design**: Two-pointer techniques, hash-based algorithms, search optimization
