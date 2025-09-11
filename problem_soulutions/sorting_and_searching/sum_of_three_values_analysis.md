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

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Two-pointer technique, hash maps, sorting, three-sum problem
- **Data Structures**: Arrays, hash maps, sorted arrays
- **Mathematical Concepts**: Sum problems, combination theory, optimization
- **Programming Skills**: Two-pointer implementation, hash map usage, sorting algorithms
- **Related Problems**: Sum of Two Values (two-sum), Sum of Four Values (four-sum), Apartments (matching)

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
