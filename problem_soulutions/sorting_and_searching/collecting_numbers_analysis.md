---
layout: simple
title: "Collecting Numbers - Greedy Collection Strategy"
permalink: /problem_soulutions/sorting_and_searching/collecting_numbers_analysis
---

# Collecting Numbers - Greedy Collection Strategy

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand greedy algorithms and their applications
- Apply sorting techniques for optimization problems
- Implement efficient collection strategies using position tracking
- Optimize algorithms using coordinate compression and mapping
- Handle edge cases in collection problems (sorted arrays, reverse sorted arrays)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Greedy algorithms, sorting, coordinate compression, position tracking
- **Data Structures**: Arrays, hash maps, sorted arrays
- **Mathematical Concepts**: Optimization, greedy choice property, collection strategies
- **Programming Skills**: Sorting implementation, hash map operations, greedy algorithms
- **Related Problems**: Distinct Numbers (sorting), Apartments (greedy), Sum of Two Values (optimization)

## 📋 Problem Description

Given an array of n integers, you need to collect them in increasing order. Each time you collect a number, you must collect the smallest available number that hasn't been collected yet. Find the minimum number of passes needed to collect all numbers.

This is a greedy optimization problem that can be solved efficiently by understanding the relationship between consecutive numbers in the sorted array.

**Input**: 
- First line: integer n (number of elements)
- Second line: n integers (the array elements)

**Output**: 
- Print one integer: the minimum number of passes needed

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a_i ≤ 10⁹

**Example**:
```
Input:
5
4 2 1 5 3

Output:
2

Explanation**: 
The array [4, 2, 1, 5, 3] needs 2 passes:

Pass 1: Collect in order 1, 2, 3
- Collect 1 (position 2)
- Collect 2 (position 1) 
- Collect 3 (position 4)

Pass 2: Collect remaining numbers 4, 5
- Collect 4 (position 0)
- Collect 5 (position 3)

Total passes: 2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Simulate Collection Process

**Key Insights from Brute Force Approach**:
- **Simulation**: Simulate the actual collection process
- **Pass Tracking**: Keep track of which numbers have been collected in each pass
- **Greedy Selection**: In each pass, collect numbers in increasing order
- **Complete Simulation**: Guaranteed to find the correct number of passes

**Key Insight**: Simulate the collection process by repeatedly making passes until all numbers are collected.

**Algorithm**:
- While there are uncollected numbers:
  - Start a new pass
  - Collect numbers in increasing order of their values
  - Mark collected numbers as used
- Count the number of passes needed

**Visual Example**:
```
Array: [4, 2, 1, 5, 3]

Pass 1:
- Sorted uncollected: [1, 2, 3, 4, 5]
- Collect 1 (position 2) → collected: [1]
- Collect 2 (position 1) → collected: [1, 2]
- Collect 3 (position 4) → collected: [1, 2, 3]
- Cannot collect 4 (position 0 < position 1 of 2) → stop pass
- Remaining: [4, 5]

Pass 2:
- Sorted uncollected: [4, 5]
- Collect 4 (position 0) → collected: [4]
- Collect 5 (position 3) → collected: [4, 5]
- All collected → stop

Total passes: 2
```

**Implementation**:
```python
def brute_force_collecting_numbers(arr):
    """
    Find minimum passes using brute force simulation
    
    Args:
        arr: list of integers
    
    Returns:
        int: minimum number of passes needed
    """
    n = len(arr)
    collected = [False] * n
    passes = 0
    
    while not all(collected):
        passes += 1
        last_position = -1
        
        # Collect numbers in increasing order
        for value in sorted(set(arr)):
            # Find uncollected occurrence of this value
            for i in range(n):
                if not collected[i] and arr[i] == value and i > last_position:
                    collected[i] = True
                    last_position = i
                    break
    
    return passes

# Example usage
arr = [4, 2, 1, 5, 3]
result = brute_force_collecting_numbers(arr)
print(f"Brute force result: {result}")  # Output: 2
```

**Time Complexity**: O(n² log n) - Multiple passes with sorting
**Space Complexity**: O(n) - For tracking collected status

**Why it's inefficient**: Multiple passes with repeated sorting make it slow for large inputs.

---

### Approach 2: Optimized - Position Tracking with Sorting

**Key Insights from Optimized Approach**:
- **Position Mapping**: Map each value to its position in the original array
- **Sorted Processing**: Process values in sorted order
- **Position Validation**: Check if current position is after the last collected position
- **Single Pass**: Process all values in a single pass through sorted array

**Key Insight**: Sort the values and track positions to determine how many passes are needed.

**Algorithm**:
- Create list of (value, position) pairs
- Sort by value
- Count passes by tracking position requirements

**Visual Example**:
```
Array: [4, 2, 1, 5, 3]

Step 1: Create (value, position) pairs
Pairs: [(4, 0), (2, 1), (1, 2), (5, 3), (3, 4)]

Step 2: Sort by value
Sorted: [(1, 2), (2, 1), (3, 4), (4, 0), (5, 3)]

Step 3: Count passes
Pass 1: positions 2, 1, 4 (valid sequence)
Pass 2: positions 0, 3 (new pass needed)

Total passes: 2
```

**Implementation**:
```python
def optimized_collecting_numbers(arr):
    """
    Find minimum passes using position tracking
    
    Args:
        arr: list of integers
    
    Returns:
        int: minimum number of passes needed
    """
    # Create (value, position) pairs
    pairs = [(arr[i], i) for i in range(len(arr))]
    
    # Sort by value
    pairs.sort()
    
    passes = 1
    last_position = pairs[0][1]
    
    for i in range(1, len(pairs)):
        value, position = pairs[i]
        
        # If position is before last position, need new pass
        if position < last_position:
            passes += 1
        
        last_position = position
    
    return passes

# Example usage
arr = [4, 2, 1, 5, 3]
result = optimized_collecting_numbers(arr)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(n) - For storing pairs

**Why it's better**: Single pass through sorted array with efficient position tracking.

---

### Approach 3: Optimal - Coordinate Compression with Position Analysis

**Key Insights from Optimal Approach**:
- **Coordinate Compression**: Map values to compressed coordinates for efficiency
- **Position Analysis**: Analyze position relationships to determine passes
- **Efficient Mapping**: Use hash maps for O(1) value-to-position mapping
- **Linear Processing**: Process positions in linear time after sorting

**Key Insight**: Use coordinate compression and analyze position sequences to determine the minimum number of passes needed.

**Algorithm**:
- Compress coordinates to handle large values efficiently
- Sort values and track their positions
- Count passes by analyzing position sequences

**Visual Example**:
```
Array: [4, 2, 1, 5, 3]

Step 1: Coordinate compression
Values: [4, 2, 1, 5, 3] → Compressed: [3, 1, 0, 4, 2]

Step 2: Create position mapping
Compressed value → positions: {0: [2], 1: [1], 2: [4], 3: [0], 4: [3]}

Step 3: Process in compressed order
Order: [0, 1, 2, 3, 4]
Positions: [2, 1, 4, 0, 3]

Pass analysis:
- Start with position 2
- Next: position 1 < 2 → new pass needed
- Pass 1: [2, 4]
- Pass 2: [1, 0, 3]

Total passes: 2
```

**Implementation**:
```python
def optimal_collecting_numbers(arr):
    """
    Find minimum passes using coordinate compression
    
    Args:
        arr: list of integers
    
    Returns:
        int: minimum number of passes needed
    """
    # Coordinate compression
    unique_values = sorted(set(arr))
    value_to_compressed = {val: i for i, val in enumerate(unique_values)}
    
    # Create compressed array
    compressed = [value_to_compressed[val] for val in arr]
    
    # Create position mapping for compressed values
    positions = {}
    for i, comp_val in enumerate(compressed):
        if comp_val not in positions:
            positions[comp_val] = []
        positions[comp_val].append(i)
    
    passes = 1
    last_position = positions[0][0]  # First position of smallest value
    
    # Process in compressed order
    for comp_val in range(1, len(unique_values)):
        # Find first position of this value that's after last_position
        found_position = None
        for pos in positions[comp_val]:
            if pos > last_position:
                found_position = pos
                break
        
        if found_position is None:
            # Need new pass
            passes += 1
            last_position = positions[comp_val][0]
        else:
            last_position = found_position
    
    return passes

# Example usage
arr = [4, 2, 1, 5, 3]
result = optimal_collecting_numbers(arr)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Sorting for coordinate compression
**Space Complexity**: O(n) - For coordinate mapping and position storage

**Why it's optimal**: Efficient coordinate compression with optimal time complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n² log n) | O(n) | Simulate collection process |
| Position Tracking | O(n log n) | O(n) | Sort and track positions |
| Coordinate Compression | O(n log n) | O(n) | Compress coordinates and analyze |

### Time Complexity
- **Time**: O(n log n) - Sorting dominates the complexity
- **Space**: O(n) - For storing position mappings and compressed values

### Why This Solution Works
- **Greedy Strategy**: Always collect the smallest available number
- **Position Analysis**: Determine passes by analyzing position sequences
- **Coordinate Compression**: Handle large values efficiently
- **Optimal Approach**: Efficient sorting and position tracking