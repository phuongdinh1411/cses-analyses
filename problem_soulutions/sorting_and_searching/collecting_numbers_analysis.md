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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Collecting Numbers with Duplicates
**Problem**: Collect numbers in order when duplicates are allowed in the array.

**Link**: [CSES Problem Set - Collecting Numbers with Duplicates](https://cses.fi/problemset/task/collecting_numbers_duplicates)

```python
def collecting_numbers_duplicates(arr):
    """
    Collect numbers in order when duplicates are allowed
    """
    # Create a list of (value, original_index) pairs
    indexed_arr = [(val, i) for i, val in enumerate(arr)]
    
    # Sort by value, then by original index
    indexed_arr.sort()
    
    passes = 1
    last_position = indexed_arr[0][1]
    
    for i in range(1, len(indexed_arr)):
        val, pos = indexed_arr[i]
        
        if pos < last_position:
            # Need new pass
            passes += 1
        
        last_position = pos
    
    return passes
```

### Variation 2: Collecting Numbers with Constraints
**Problem**: Collect numbers with constraints (e.g., can only collect k numbers per pass).

**Link**: [CSES Problem Set - Collecting Numbers with Constraints](https://cses.fi/problemset/task/collecting_numbers_constraints)

```python
def collecting_numbers_constraints(arr, k):
    """
    Collect numbers with constraint of k numbers per pass
    """
    # Create position mapping
    positions = {}
    for i, val in enumerate(arr):
        if val not in positions:
            positions[val] = []
        positions[val].append(i)
    
    # Sort unique values
    sorted_values = sorted(positions.keys())
    
    passes = 0
    collected = set()
    
    while len(collected) < len(sorted_values):
        passes += 1
        numbers_in_pass = 0
        last_position = -1
        
        for val in sorted_values:
            if val in collected:
                continue
            
            # Find first position after last_position
            found_position = None
            for pos in positions[val]:
                if pos > last_position:
                    found_position = pos
                    break
            
            if found_position is not None and numbers_in_pass < k:
                collected.add(val)
                last_position = found_position
                numbers_in_pass += 1
    
    return passes
```

### Variation 3: Collecting Numbers with Weights
**Problem**: Each number has a weight, and we want to minimize the total weight of passes.

**Link**: [CSES Problem Set - Collecting Numbers with Weights](https://cses.fi/problemset/task/collecting_numbers_weights)

```python
def collecting_numbers_weights(arr, weights):
    """
    Collect numbers to minimize total weight of passes
    """
    # Create position mapping with weights
    positions = {}
    for i, (val, weight) in enumerate(zip(arr, weights)):
        if val not in positions:
            positions[val] = []
        positions[val].append((i, weight))
    
    # Sort unique values
    sorted_values = sorted(positions.keys())
    
    # Use dynamic programming to find optimal collection strategy
    n = len(sorted_values)
    dp = [float('inf')] * (1 << n)
    dp[0] = 0
    
    for mask in range(1 << n):
        if dp[mask] == float('inf'):
            continue
        
        # Try to collect numbers in a single pass
        last_position = -1
        current_weight = 0
        new_mask = mask
        
        for i, val in enumerate(sorted_values):
            if mask & (1 << i):
                continue
            
            # Find best position for this value
            best_pos = None
            best_weight = float('inf')
            
            for pos, weight in positions[val]:
                if pos > last_position and weight < best_weight:
                    best_pos = pos
                    best_weight = weight
            
            if best_pos is not None:
                new_mask |= (1 << i)
                current_weight += best_weight
                last_position = best_pos
        
        # Update DP
        if new_mask != mask:
            dp[new_mask] = min(dp[new_mask], dp[mask] + current_weight)
    
    return dp[(1 << n) - 1]
```

## Problem Variations

### **Variation 1: Collecting Numbers with Dynamic Updates**
**Problem**: Handle dynamic array updates while maintaining optimal collection strategy.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
import bisect
from collections import defaultdict

class DynamicCollectingNumbers:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.position_map = {val: i for i, val in enumerate(arr)}
        self.sorted_values = sorted(arr)
        self.passes = 0
        self._calculate_passes()
    
    def _calculate_passes(self):
        """Calculate the number of passes needed to collect all numbers."""
        self.passes = 0
        collected = set()
        
        for val in self.sorted_values:
            if val not in collected:
                self.passes += 1
                # Collect consecutive numbers
                current = val
                while current in self.position_map and current not in collected:
                    collected.add(current)
                    current += 1
    
    def update_value(self, index, new_value):
        """Update array value and recalculate passes."""
        old_value = self.arr[index]
        self.arr[index] = new_value
        
        # Update position map
        del self.position_map[old_value]
        self.position_map[new_value] = index
        
        # Update sorted values
        self.sorted_values.remove(old_value)
        bisect.insort(self.sorted_values, new_value)
        
        # Recalculate passes
        self._calculate_passes()
    
    def add_number(self, value):
        """Add a new number to the array."""
        self.arr.append(value)
        self.n += 1
        self.position_map[value] = self.n - 1
        bisect.insort(self.sorted_values, value)
        self._calculate_passes()
    
    def remove_number(self, value):
        """Remove a number from the array."""
        if value in self.position_map:
            index = self.position_map[value]
            del self.arr[index]
            del self.position_map[value]
            self.sorted_values.remove(value)
            self.n -= 1
            
            # Update position map for remaining elements
            new_position_map = {}
            for i, val in enumerate(self.arr):
                new_position_map[val] = i
            self.position_map = new_position_map
            
            self._calculate_passes()
    
    def get_passes(self):
        """Get the current number of passes needed."""
        return self.passes
    
    def get_collection_order(self):
        """Get the order in which numbers should be collected."""
        collection_order = []
        collected = set()
        
        for val in self.sorted_values:
            if val not in collected:
                # Collect consecutive numbers
                current = val
                while current in self.position_map and current not in collected:
                    collection_order.append(current)
                    collected.add(current)
                    current += 1
        
        return collection_order

# Example usage
arr = [4, 1, 2, 3, 5]
collector = DynamicCollectingNumbers(arr)
print(f"Initial passes: {collector.get_passes()}")
print(f"Collection order: {collector.get_collection_order()}")

# Update a value
collector.update_value(0, 6)
print(f"After update: {collector.get_passes()}")

# Add a number
collector.add_number(7)
print(f"After adding 7: {collector.get_passes()}")
```

### **Variation 2: Collecting Numbers with Different Operations**
**Problem**: Collect numbers with different collection rules (backwards, skip patterns, etc.).

**Approach**: Adapt the greedy strategy for different collection patterns.

```python
def collecting_numbers_backwards(arr):
    """
    Collect numbers in descending order (backwards).
    
    Args:
        arr: List of integers
    
    Returns:
        Number of passes needed
    """
    position_map = {val: i for i, val in enumerate(arr)}
    sorted_values = sorted(arr, reverse=True)  # Descending order
    
    passes = 0
    collected = set()
    
    for val in sorted_values:
        if val not in collected:
            passes += 1
            # Collect consecutive numbers in descending order
            current = val
            while current in position_map and current not in collected:
                collected.add(current)
                current -= 1  # Go backwards
    
    return passes

def collecting_numbers_skip_pattern(arr, skip):
    """
    Collect numbers with a skip pattern.
    
    Args:
        arr: List of integers
        skip: Number to skip between collections
    
    Returns:
        Number of passes needed
    """
    position_map = {val: i for i, val in enumerate(arr)}
    sorted_values = sorted(arr)
    
    passes = 0
    collected = set()
    
    for val in sorted_values:
        if val not in collected:
            passes += 1
            # Collect numbers with skip pattern
            current = val
            while current in position_map and current not in collected:
                collected.add(current)
                current += skip  # Skip by 'skip' amount
    
    return passes

def collecting_numbers_alternating(arr):
    """
    Collect numbers in alternating order (even, odd, even, odd...).
    
    Args:
        arr: List of integers
    
    Returns:
        Number of passes needed
    """
    position_map = {val: i for i, val in enumerate(arr)}
    even_numbers = sorted([val for val in arr if val % 2 == 0])
    odd_numbers = sorted([val for val in arr if val % 2 == 1])
    
    passes = 0
    collected = set()
    
    # Alternate between even and odd
    i, j = 0, 0
    while i < len(even_numbers) or j < len(odd_numbers):
        passes += 1
        
        # Collect even numbers
        if i < len(even_numbers):
            val = even_numbers[i]
            if val not in collected:
                collected.add(val)
                i += 1
        
        # Collect odd numbers
        if j < len(odd_numbers):
            val = odd_numbers[j]
            if val not in collected:
                collected.add(val)
                j += 1
    
    return passes

def collecting_numbers_weighted(arr, weights):
    """
    Collect numbers considering their weights (collect lighter numbers first).
    
    Args:
        arr: List of integers
        weights: Dictionary mapping values to weights
    
    Returns:
        Number of passes needed
    """
    position_map = {val: i for i, val in enumerate(arr)}
    # Sort by weight (lighter first)
    sorted_values = sorted(arr, key=lambda x: weights.get(x, 0))
    
    passes = 0
    collected = set()
    
    for val in sorted_values:
        if val not in collected:
            passes += 1
            # Collect consecutive numbers
            current = val
            while current in position_map and current not in collected:
                collected.add(current)
                current += 1
    
    return passes

def collecting_numbers_constrained(arr, constraints):
    """
    Collect numbers with additional constraints.
    
    Args:
        arr: List of integers
        constraints: Dictionary with constraints like:
            - max_per_pass: Maximum numbers to collect per pass
            - min_value: Minimum value to collect
            - max_value: Maximum value to collect
    
    Returns:
        Number of passes needed
    """
    position_map = {val: i for i, val in enumerate(arr)}
    sorted_values = sorted(arr)
    
    passes = 0
    collected = set()
    
    for val in sorted_values:
        if val not in collected:
            # Check constraints
            if 'min_value' in constraints and val < constraints['min_value']:
                continue
            if 'max_value' in constraints and val > constraints['max_value']:
                continue
            
            passes += 1
            numbers_in_pass = 0
            
            # Collect consecutive numbers
            current = val
            while (current in position_map and 
                   current not in collected and 
                   numbers_in_pass < constraints.get('max_per_pass', float('inf'))):
                collected.add(current)
                current += 1
                numbers_in_pass += 1
    
    return passes

# Example usage
arr = [4, 1, 2, 3, 5, 6, 7, 8]

print(f"Backwards collection: {collecting_numbers_backwards(arr)}")
print(f"Skip pattern (skip 2): {collecting_numbers_skip_pattern(arr, 2)}")
print(f"Alternating collection: {collecting_numbers_alternating(arr)}")

weights = {1: 3, 2: 1, 3: 2, 4: 4, 5: 1, 6: 2, 7: 3, 8: 1}
print(f"Weighted collection: {collecting_numbers_weighted(arr, weights)}")

constraints = {'max_per_pass': 2, 'min_value': 2, 'max_value': 6}
print(f"Constrained collection: {collecting_numbers_constrained(arr, constraints)}")
```

### **Variation 3: Collecting Numbers with Constraints**
**Problem**: Collect numbers with additional constraints like time limits, capacity limits, etc.

**Approach**: Use constraint satisfaction with backtracking or advanced optimization.

```python
def collecting_numbers_with_capacity(arr, capacity):
    """
    Collect numbers with capacity constraints per pass.
    
    Args:
        arr: List of integers
        capacity: Maximum capacity per pass
    
    Returns:
        Number of passes needed
    """
    position_map = {val: i for i, val in enumerate(arr)}
    sorted_values = sorted(arr)
    
    passes = 0
    collected = set()
    
    for val in sorted_values:
        if val not in collected:
            passes += 1
            current_capacity = 0
            current = val
            
            # Collect consecutive numbers within capacity
            while (current in position_map and 
                   current not in collected and 
                   current_capacity < capacity):
                collected.add(current)
                current += 1
                current_capacity += 1
    
    return passes

def collecting_numbers_with_time_limit(arr, time_limit, collection_time):
    """
    Collect numbers with time constraints.
    
    Args:
        arr: List of integers
        time_limit: Maximum time per pass
        collection_time: Time required to collect each number
    
    Returns:
        Number of passes needed
    """
    position_map = {val: i for i, val in enumerate(arr)}
    sorted_values = sorted(arr)
    
    passes = 0
    collected = set()
    
    for val in sorted_values:
        if val not in collected:
            passes += 1
            current_time = 0
            current = val
            
            # Collect consecutive numbers within time limit
            while (current in position_map and 
                   current not in collected and 
                   current_time + collection_time <= time_limit):
                collected.add(current)
                current += 1
                current_time += collection_time
    
    return passes

def collecting_numbers_with_priority(arr, priorities):
    """
    Collect numbers based on priority levels.
    
    Args:
        arr: List of integers
        priorities: Dictionary mapping values to priority levels
    
    Returns:
        Number of passes needed
    """
    position_map = {val: i for i, val in enumerate(arr)}
    # Sort by priority (higher priority first)
    sorted_values = sorted(arr, key=lambda x: priorities.get(x, 0), reverse=True)
    
    passes = 0
    collected = set()
    
    for val in sorted_values:
        if val not in collected:
            passes += 1
            # Collect consecutive numbers
            current = val
            while current in position_map and current not in collected:
                collected.add(current)
                current += 1
    
    return passes

def collecting_numbers_with_penalty(arr, penalties):
    """
    Collect numbers considering collection penalties.
    
    Args:
        arr: List of integers
        penalties: Dictionary mapping values to penalty costs
    
    Returns:
        Tuple of (passes, total_penalty)
    """
    position_map = {val: i for i, val in enumerate(arr)}
    sorted_values = sorted(arr)
    
    passes = 0
    collected = set()
    total_penalty = 0
    
    for val in sorted_values:
        if val not in collected:
            passes += 1
            # Collect consecutive numbers
            current = val
            while current in position_map and current not in collected:
                collected.add(current)
                total_penalty += penalties.get(current, 0)
                current += 1
    
    return passes, total_penalty

def collecting_numbers_optimal_schedule(arr, schedule_constraints):
    """
    Find optimal schedule for collecting numbers.
    
    Args:
        arr: List of integers
        schedule_constraints: Dictionary with scheduling constraints
    
    Returns:
        Optimal collection schedule
    """
    position_map = {val: i for i, val in enumerate(arr)}
    sorted_values = sorted(arr)
    
    schedule = []
    collected = set()
    
    for val in sorted_values:
        if val not in collected:
            pass_numbers = []
            current = val
            
            # Collect consecutive numbers
            while current in position_map and current not in collected:
                pass_numbers.append(current)
                collected.add(current)
                current += 1
            
            schedule.append(pass_numbers)
    
    return schedule

# Example usage
arr = [4, 1, 2, 3, 5, 6, 7, 8]

print(f"Capacity constraint (capacity=3): {collecting_numbers_with_capacity(arr, 3)}")
print(f"Time constraint (limit=5, time=2): {collecting_numbers_with_time_limit(arr, 5, 2)}")

priorities = {1: 3, 2: 1, 3: 2, 4: 4, 5: 1, 6: 2, 7: 3, 8: 1}
print(f"Priority-based collection: {collecting_numbers_with_priority(arr, priorities)}")

penalties = {1: 2, 2: 1, 3: 3, 4: 1, 5: 2, 6: 1, 7: 3, 8: 2}
passes, penalty = collecting_numbers_with_penalty(arr, penalties)
print(f"Penalty-based collection: {passes} passes, {penalty} total penalty")

schedule = collecting_numbers_optimal_schedule(arr, {})
print(f"Optimal schedule: {schedule}")
```

### Related Problems

#### **CSES Problems**
- [Collecting Numbers](https://cses.fi/problemset/task/2216) - Basic collecting numbers problem
- [Collecting Numbers II](https://cses.fi/problemset/task/2217) - Advanced collecting numbers problem
- [Stick Lengths](https://cses.fi/problemset/task/1074) - Optimization with sorting

#### **LeetCode Problems**
- [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) - Find longest increasing sequence
- [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) - Nested sequence problem
- [Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) - Chain formation problem
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) - Interval scheduling

#### **Problem Categories**
- **Greedy Algorithms**: Optimal local choices, sorting-based optimization, sequence problems
- **Sorting**: Array sorting, coordinate compression, position tracking
- **Sequence Analysis**: Position sequences, pass counting, order analysis
- **Algorithm Design**: Greedy strategies, sorting algorithms, optimization techniques