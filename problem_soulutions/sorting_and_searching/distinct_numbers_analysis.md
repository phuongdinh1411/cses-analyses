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