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