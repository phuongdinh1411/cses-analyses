---
layout: simple
title: "Distinct Numbers - Count Unique Elements"
permalink: /problem_soulutions/sorting_and_searching/distinct_numbers_analysis
---

# Distinct Numbers - Count Unique Elements

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of distinct elements in arrays
- Apply sorting algorithms to find unique elements
- Implement efficient counting algorithms using hash sets
- Optimize space and time complexity for distinct element counting
- Handle edge cases in distinct element problems (empty arrays, single elements)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting algorithms, hash sets, counting techniques
- **Data Structures**: Arrays, hash sets, sorted arrays
- **Mathematical Concepts**: Set theory, counting principles, uniqueness
- **Programming Skills**: Array manipulation, hash set operations, sorting
- **Related Problems**: Apartments (two-pointer), Sum of Two Values (hash map), Collecting Numbers (sorting)

## 📋 Problem Description

Given an array of n integers, count the number of distinct (unique) elements in the array.

This is a fundamental problem that tests understanding of uniqueness and efficient counting techniques. The solution involves identifying and counting unique elements using various approaches.

**Input**: 
- First line: integer n (number of elements)
- Second line: n integers (the array elements)

**Output**: 
- Print one integer: the number of distinct elements

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ x_i ≤ 10⁹

**Example**:
```
Input:
5
2 3 2 2 3

Output:
2

Explanation**: 
The array [2, 3, 2, 2, 3] contains 2 distinct elements: 2 and 3.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Pairs

**Key Insights from Brute Force Approach**:
- **Exhaustive Comparison**: Compare each element with all previous elements
- **Uniqueness Tracking**: Keep track of elements that have been seen before
- **Complete Coverage**: Guaranteed to find all distinct elements
- **Simple Implementation**: Nested loops approach

**Key Insight**: For each element, check if it has appeared before by comparing with all previous elements.

**Algorithm**:
- For each element, check if it's the first occurrence
- Count elements that haven't appeared before
- Return the total count

**Visual Example**:
```
Array: [2, 3, 2, 2, 3]

Processing:
1. Element 2 (index 0): First occurrence → count = 1
2. Element 3 (index 1): First occurrence → count = 2
3. Element 2 (index 2): Seen before (index 0) → count = 2
4. Element 2 (index 3): Seen before (index 0) → count = 2
5. Element 3 (index 4): Seen before (index 1) → count = 2

Total distinct elements: 2
```

**Implementation**:
```python
def brute_force_distinct_numbers(arr):
    """
    Count distinct numbers using brute force approach
    
    Args:
        arr: list of integers
    
    Returns:
        int: number of distinct elements
    """
    n = len(arr)
    count = 0
    
    for i in range(n):
        # Check if this is the first occurrence
        is_first_occurrence = True
        for j in range(i):
            if arr[i] == arr[j]:
                is_first_occurrence = False
                break
        
        if is_first_occurrence:
            count += 1
    
    return count

# Example usage
arr = [2, 3, 2, 2, 3]
result = brute_force_distinct_numbers(arr)
print(f"Brute force result: {result}")  # Output: 2
```

**Time Complexity**: O(n²) - For each element, check all previous elements
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Sorting with Linear Scan

**Key Insights from Optimized Approach**:
- **Sorting Benefit**: After sorting, identical elements are adjacent
- **Linear Scan**: Scan through sorted array to count unique elements
- **Adjacent Comparison**: Compare each element with the previous one
- **Efficient Counting**: Count elements that differ from their predecessor

**Key Insight**: Sort the array first, then count elements that are different from their previous element.

**Algorithm**:
- Sort the array
- Count elements that are different from the previous element
- Handle the first element separately

**Visual Example**:
```
Array: [2, 3, 2, 2, 3]

Step 1: Sort
Sorted: [2, 2, 2, 3, 3]

Step 2: Count distinct elements
- Element 2 (index 0): First element → count = 1
- Element 2 (index 1): Same as previous → count = 1
- Element 2 (index 2): Same as previous → count = 1
- Element 3 (index 3): Different from previous → count = 2
- Element 3 (index 4): Same as previous → count = 2

Total distinct elements: 2
```

**Implementation**:
```python
def optimized_distinct_numbers(arr):
    """
    Count distinct numbers using sorting approach
    
    Args:
        arr: list of integers
    
    Returns:
        int: number of distinct elements
    """
    if not arr:
        return 0
    
    # Sort the array
    sorted_arr = sorted(arr)
    
    count = 1  # First element is always distinct
    
    # Count elements that differ from previous
    for i in range(1, len(sorted_arr)):
        if sorted_arr[i] != sorted_arr[i-1]:
            count += 1
    
    return count

# Example usage
arr = [2, 3, 2, 2, 3]
result = optimized_distinct_numbers(arr)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(1) - If sorting in-place, O(n) if creating new array

**Why it's better**: Much more efficient than brute force, but still has room for optimization.

---

### Approach 3: Optimal - Hash Set

**Key Insights from Optimal Approach**:
- **Hash Set Properties**: Hash sets automatically handle uniqueness
- **Single Pass**: Process each element exactly once
- **Efficient Lookup**: O(1) average time for insertions and lookups
- **Optimal Complexity**: Achieve linear time complexity

**Key Insight**: Use a hash set to automatically track unique elements, inserting each element and counting the final size.

**Algorithm**:
- Create an empty hash set
- Insert all elements into the set
- Return the size of the set

**Visual Example**:
```
Array: [2, 3, 2, 2, 3]

Hash Set Operations:
1. Insert 2 → Set: {2}
2. Insert 3 → Set: {2, 3}
3. Insert 2 → Set: {2, 3} (already exists)
4. Insert 2 → Set: {2, 3} (already exists)
5. Insert 3 → Set: {2, 3} (already exists)

Final set size: 2
```

**Implementation**:
```python
def optimal_distinct_numbers(arr):
    """
    Count distinct numbers using hash set
    
    Args:
        arr: list of integers
    
    Returns:
        int: number of distinct elements
    """
    # Use set to automatically handle uniqueness
    distinct_elements = set(arr)
    return len(distinct_elements)

# Example usage
arr = [2, 3, 2, 2, 3]
result = optimal_distinct_numbers(arr)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n) - Single pass through array
**Space Complexity**: O(n) - For hash set storage

**Why it's optimal**: Linear time complexity with automatic uniqueness handling.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all previous elements |
| Sorting | O(n log n) | O(1) | Sort and count adjacent differences |
| Hash Set | O(n) | O(n) | Automatic uniqueness handling |

### Time Complexity
- **Time**: O(n) - Single pass through array with hash set
- **Space**: O(n) - For hash set storage

### Why This Solution Works
- **Uniqueness Detection**: Hash sets automatically handle duplicate detection
- **Efficient Storage**: Only store unique elements
- **Single Pass**: Process each element exactly once
- **Optimal Approach**: Linear time complexity with clean implementation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Distinct Numbers with Frequency
**Problem**: Count distinct numbers and also return their frequencies.

**Link**: [CSES Problem Set - Distinct Numbers with Frequency](https://cses.fi/problemset/task/distinct_numbers_frequency)

```python
def distinct_numbers_frequency(arr):
    """
    Count distinct numbers and their frequencies
    """
    from collections import Counter
    
    # Count frequencies of all elements
    frequency_map = Counter(arr)
    
    # Return count and frequency map
    distinct_count = len(frequency_map)
    return distinct_count, frequency_map

def distinct_numbers_frequency_manual(arr):
    """
    Count distinct numbers and frequencies manually
    """
    frequency_map = {}
    
    for num in arr:
        frequency_map[num] = frequency_map.get(num, 0) + 1
    
    distinct_count = len(frequency_map)
    return distinct_count, frequency_map
```

### Variation 2: Distinct Numbers in Range
**Problem**: Count distinct numbers in a given range [L, R] of the array.

**Link**: [CSES Problem Set - Distinct Numbers in Range](https://cses.fi/problemset/task/distinct_numbers_range)

```python
def distinct_numbers_in_range(arr, queries):
    """
    Count distinct numbers in multiple ranges
    """
    results = []
    
    for L, R in queries:
        # Extract subarray
        subarray = arr[L:R+1]
        
        # Count distinct elements in subarray
        distinct_count = len(set(subarray))
        results.append(distinct_count)
    
    return results

def distinct_numbers_in_range_optimized(arr, queries):
    """
    Optimized version using coordinate compression
    """
    # Coordinate compression
    unique_values = sorted(set(arr))
    value_to_index = {val: i for i, val in enumerate(unique_values)}
    
    # Compress array
    compressed_arr = [value_to_index[val] for val in arr]
    
    results = []
    
    for L, R in queries:
        # Use set on compressed array
        distinct_count = len(set(compressed_arr[L:R+1]))
        results.append(distinct_count)
    
    return results
```

### Variation 3: Distinct Numbers with Updates
**Problem**: Handle dynamic updates to the array and maintain distinct count.

**Link**: [CSES Problem Set - Distinct Numbers with Updates](https://cses.fi/problemset/task/distinct_numbers_updates)

```python
class DistinctNumbersWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.frequency_map = {}
        self.distinct_count = 0
        
        # Initialize frequency map
        for num in self.arr:
            if num not in self.frequency_map:
                self.frequency_map[num] = 0
                self.distinct_count += 1
            self.frequency_map[num] += 1
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        old_value = self.arr[index]
        self.arr[index] = new_value
        
        # Update frequency map for old value
        self.frequency_map[old_value] -= 1
        if self.frequency_map[old_value] == 0:
            del self.frequency_map[old_value]
            self.distinct_count -= 1
        
        # Update frequency map for new value
        if new_value not in self.frequency_map:
            self.frequency_map[new_value] = 0
            self.distinct_count += 1
        self.frequency_map[new_value] += 1
    
    def get_distinct_count(self):
        """Get current distinct count"""
        return self.distinct_count
    
    def get_frequency(self, value):
        """Get frequency of a specific value"""
        return self.frequency_map.get(value, 0)
```

## Problem Variations

### **Variation 1: Distinct Numbers with Dynamic Updates**
**Problem**: Handle dynamic array updates while maintaining distinct count efficiently.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
import bisect
from collections import defaultdict

class DynamicDistinctNumbers:
    def __init__(self, arr):
        self.arr = arr[:]
        self.frequency_map = defaultdict(int)
        self.distinct_count = 0
        
        # Initialize frequency map and distinct count
        for num in arr:
            if self.frequency_map[num] == 0:
                self.distinct_count += 1
            self.frequency_map[num] += 1
    
    def update_value(self, index, new_value):
        """Update array value and maintain distinct count."""
        old_value = self.arr[index]
        self.arr[index] = new_value
        
        # Update frequency map
        self.frequency_map[old_value] -= 1
        if self.frequency_map[old_value] == 0:
            self.distinct_count -= 1
            del self.frequency_map[old_value]
        
        if self.frequency_map[new_value] == 0:
            self.distinct_count += 1
        self.frequency_map[new_value] += 1
    
    def add_element(self, value):
        """Add new element to the array."""
        self.arr.append(value)
        if self.frequency_map[value] == 0:
            self.distinct_count += 1
        self.frequency_map[value] += 1
    
    def remove_element(self, value):
        """Remove element from the array."""
        if value in self.arr and self.frequency_map[value] > 0:
            self.arr.remove(value)
            self.frequency_map[value] -= 1
            if self.frequency_map[value] == 0:
                self.distinct_count -= 1
                del self.frequency_map[value]
    
    def get_distinct_count(self):
        """Get current distinct count."""
        return self.distinct_count
    
    def get_frequency(self, value):
        """Get frequency of a specific value."""
        return self.frequency_map.get(value, 0)
    
    def get_most_frequent(self):
        """Get the most frequent element."""
        if not self.frequency_map:
            return None
        return max(self.frequency_map.items(), key=lambda x: x[1])
    
    def get_distinct_elements(self):
        """Get all distinct elements."""
        return list(self.frequency_map.keys())

# Example usage
arr = [1, 2, 3, 2, 1, 4]
distinct_counter = DynamicDistinctNumbers(arr)
print(f"Initial distinct count: {distinct_counter.get_distinct_count()}")
print(f"Distinct elements: {distinct_counter.get_distinct_elements()}")

# Update a value
distinct_counter.update_value(0, 5)
print(f"After update: {distinct_counter.get_distinct_count()}")

# Add element
distinct_counter.add_element(6)
print(f"After adding 6: {distinct_counter.get_distinct_count()}")

# Remove element
distinct_counter.remove_element(2)
print(f"After removing 2: {distinct_counter.get_distinct_count()}")
```

### **Variation 2: Distinct Numbers with Different Operations**
**Problem**: Handle different types of operations on distinct numbers (range queries, frequency analysis).

**Approach**: Use advanced data structures for efficient range operations and frequency tracking.

```python
class AdvancedDistinctNumbers:
    def __init__(self, arr):
        self.arr = arr[:]
        self.frequency_map = defaultdict(int)
        self.distinct_count = 0
        
        # Initialize
        for num in arr:
            if self.frequency_map[num] == 0:
                self.distinct_count += 1
            self.frequency_map[num] += 1
    
    def get_distinct_in_range(self, left, right):
        """Get distinct count in range [left, right]."""
        if left < 0 or right >= len(self.arr) or left > right:
            return 0
        
        range_frequency = defaultdict(int)
        distinct_in_range = 0
        
        for i in range(left, right + 1):
            num = self.arr[i]
            if range_frequency[num] == 0:
                distinct_in_range += 1
            range_frequency[num] += 1
        
        return distinct_in_range
    
    def get_frequency_in_range(self, left, right, value):
        """Get frequency of value in range [left, right]."""
        if left < 0 or right >= len(self.arr) or left > right:
            return 0
        
        count = 0
        for i in range(left, right + 1):
            if self.arr[i] == value:
                count += 1
        
        return count
    
    def get_most_frequent_in_range(self, left, right):
        """Get most frequent element in range [left, right]."""
        if left < 0 or right >= len(self.arr) or left > right:
            return None
        
        range_frequency = defaultdict(int)
        for i in range(left, right + 1):
            range_frequency[self.arr[i]] += 1
        
        if not range_frequency:
            return None
        
        return max(range_frequency.items(), key=lambda x: x[1])
    
    def get_distinct_elements_in_range(self, left, right):
        """Get all distinct elements in range [left, right]."""
        if left < 0 or right >= len(self.arr) or left > right:
            return []
        
        distinct_set = set()
        for i in range(left, right + 1):
            distinct_set.add(self.arr[i])
        
        return list(distinct_set)
    
    def get_frequency_distribution(self):
        """Get frequency distribution of all elements."""
        return dict(self.frequency_map)
    
    def get_elements_by_frequency(self, min_frequency=1):
        """Get elements with frequency >= min_frequency."""
        return [num for num, freq in self.frequency_map.items() if freq >= min_frequency]

# Example usage
arr = [1, 2, 3, 2, 1, 4, 2, 5, 1]
advanced_counter = AdvancedDistinctNumbers(arr)

print(f"Total distinct count: {advanced_counter.get_distinct_count()}")
print(f"Distinct in range [2, 6]: {advanced_counter.get_distinct_in_range(2, 6)}")
print(f"Frequency of 2 in range [1, 5]: {advanced_counter.get_frequency_in_range(1, 5, 2)}")
print(f"Most frequent in range [0, 4]: {advanced_counter.get_most_frequent_in_range(0, 4)}")
print(f"Distinct elements in range [3, 7]: {advanced_counter.get_distinct_elements_in_range(3, 7)}")
print(f"Elements with frequency >= 2: {advanced_counter.get_elements_by_frequency(2)}")
```

### **Variation 3: Distinct Numbers with Constraints**
**Problem**: Handle distinct numbers with additional constraints (value ranges, frequency limits, etc.).

**Approach**: Use constraint satisfaction with advanced filtering and optimization.

```python
class ConstrainedDistinctNumbers:
    def __init__(self, arr, constraints=None):
        self.arr = arr[:]
        self.frequency_map = defaultdict(int)
        self.distinct_count = 0
        self.constraints = constraints or {}
        
        # Initialize with constraints
        for num in arr:
            if self._is_valid_number(num):
                if self.frequency_map[num] == 0:
                    self.distinct_count += 1
                self.frequency_map[num] += 1
    
    def _is_valid_number(self, num):
        """Check if number satisfies constraints."""
        if 'min_value' in self.constraints and num < self.constraints['min_value']:
            return False
        if 'max_value' in self.constraints and num > self.constraints['max_value']:
            return False
        if 'allowed_values' in self.constraints and num not in self.constraints['allowed_values']:
            return False
        if 'forbidden_values' in self.constraints and num in self.constraints['forbidden_values']:
            return False
        return True
    
    def add_element_with_constraints(self, value):
        """Add element if it satisfies constraints."""
        if self._is_valid_number(value):
            if self.frequency_map[value] == 0:
                self.distinct_count += 1
            self.frequency_map[value] += 1
            self.arr.append(value)
            return True
        return False
    
    def get_distinct_with_frequency_limit(self, max_frequency):
        """Get distinct count considering frequency limit."""
        count = 0
        for num, freq in self.frequency_map.items():
            if freq <= max_frequency:
                count += 1
        return count
    
    def get_distinct_in_value_range(self, min_val, max_val):
        """Get distinct count in value range [min_val, max_val]."""
        count = 0
        for num in self.frequency_map.keys():
            if min_val <= num <= max_val:
                count += 1
        return count
    
    def get_distinct_with_pattern(self, pattern_func):
        """Get distinct count for numbers matching pattern."""
        count = 0
        for num in self.frequency_map.keys():
            if pattern_func(num):
                count += 1
        return count
    
    def get_distinct_by_category(self, category_func):
        """Get distinct count grouped by category."""
        categories = defaultdict(int)
        for num in self.frequency_map.keys():
            category = category_func(num)
            categories[category] += 1
        return dict(categories)
    
    def get_distinct_with_operations(self, operations):
        """Get distinct count after applying operations."""
        result = set()
        for num in self.frequency_map.keys():
            current = num
            for op in operations:
                if op == 'square':
                    current = current ** 2
                elif op == 'double':
                    current = current * 2
                elif op == 'increment':
                    current = current + 1
                elif op == 'modulo':
                    current = current % 10
            result.add(current)
        return len(result)

# Example usage
arr = [1, 2, 3, 2, 1, 4, 5, 6, 7, 8, 9, 10]
constraints = {
    'min_value': 2,
    'max_value': 8,
    'forbidden_values': {5}
}

constrained_counter = ConstrainedDistinctNumbers(arr, constraints)
print(f"Constrained distinct count: {constrained_counter.get_distinct_count()}")

# Test frequency limit
print(f"Distinct with frequency <= 1: {constrained_counter.get_distinct_with_frequency_limit(1)}")

# Test value range
print(f"Distinct in range [3, 7]: {constrained_counter.get_distinct_in_value_range(3, 7)}")

# Test pattern matching
even_pattern = lambda x: x % 2 == 0
print(f"Distinct even numbers: {constrained_counter.get_distinct_with_pattern(even_pattern)}")

# Test categorization
category_func = lambda x: 'small' if x < 5 else 'large'
print(f"Distinct by category: {constrained_counter.get_distinct_by_category(category_func)}")

# Test operations
operations = ['square', 'modulo']
print(f"Distinct after operations: {constrained_counter.get_distinct_with_operations(operations)}")
```

### Related Problems

#### **CSES Problems**
- [Distinct Numbers](https://cses.fi/problemset/task/1621) - Basic distinct numbers problem
- [Distinct Values Queries](https://cses.fi/problemset/task/1734) - Range queries for distinct values
- [Subarray Distinct Values](https://cses.fi/problemset/task/2428) - Distinct values in subarrays

#### **LeetCode Problems**
- [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) - Check if array has duplicates
- [Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) - Duplicates within k distance
- [Contains Duplicate III](https://leetcode.com/problems/contains-duplicate-iii/) - Duplicates within value and index range
- [Single Number](https://leetcode.com/problems/single-number/) - Find unique element

#### **Problem Categories**
- **Hash Sets**: Uniqueness detection, frequency counting, set operations
- **Sorting**: Array sorting, adjacent comparison, uniqueness analysis
- **Counting**: Element counting, frequency analysis, distinct element tracking
- **Algorithm Design**: Hash-based algorithms, sorting algorithms, counting techniques