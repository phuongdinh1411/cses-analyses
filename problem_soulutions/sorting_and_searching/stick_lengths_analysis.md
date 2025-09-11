---
layout: simple
title: "Stick Lengths"
permalink: /problem_soulutions/sorting_and_searching/stick_lengths_analysis
---

# Stick Lengths

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of median and its applications in optimization
- Apply sorting algorithms for finding optimal solutions
- Implement efficient solutions for minimizing sum of absolute differences
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in optimization problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, median finding, optimization, greedy algorithms
- **Data Structures**: Arrays, sorting algorithms
- **Mathematical Concepts**: Median, absolute difference, optimization theory
- **Programming Skills**: Algorithm implementation, complexity analysis, sorting
- **Related Problems**: Array Division (optimization), Nearest Smaller Values (optimization), Sum of Two Values (searching)

## 📋 Problem Description

There are n sticks with some lengths. Your task is to modify the lengths of the sticks so that all sticks have the same length. You can either increase or decrease the length of each stick by 1 unit at a cost of 1 unit.

Find the minimum cost to make all sticks have the same length.

**Input**: 
- First line: integer n (number of sticks)
- Second line: n integers a[1], a[2], ..., a[n] (lengths of sticks)

**Output**: 
- Print one integer: the minimum cost to make all sticks the same length

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
5
2 3 1 5 2

Output:
5

Explanation**: 
Stick lengths: [2, 3, 1, 5, 2]

If we make all sticks length 2:
- Stick 1: 2 → 2 (cost: 0)
- Stick 2: 3 → 2 (cost: 1)
- Stick 3: 1 → 2 (cost: 1)
- Stick 4: 5 → 2 (cost: 3)
- Stick 5: 2 → 2 (cost: 0)

Total cost: 0 + 1 + 1 + 3 + 0 = 5

This is the minimum cost (length 2 is the median).
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Target Lengths

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible target lengths
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward nested loops approach
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each possible target length, calculate the total cost to make all sticks that length.

**Algorithm**:
- For each possible target length (from min to max stick length):
  - Calculate the cost to make all sticks that length
  - Keep track of the minimum cost

**Visual Example**:
```
Stick lengths: [2, 3, 1, 5, 2]
Possible targets: [1, 2, 3, 4, 5]

Target 1: |2-1| + |3-1| + |1-1| + |5-1| + |2-1| = 1 + 2 + 0 + 4 + 1 = 8
Target 2: |2-2| + |3-2| + |1-2| + |5-2| + |2-2| = 0 + 1 + 1 + 3 + 0 = 5 ✓
Target 3: |2-3| + |3-3| + |1-3| + |5-3| + |2-3| = 1 + 0 + 2 + 2 + 1 = 6
Target 4: |2-4| + |3-4| + |1-4| + |5-4| + |2-4| = 2 + 1 + 3 + 1 + 2 = 9
Target 5: |2-5| + |3-5| + |1-5| + |5-5| + |2-5| = 3 + 2 + 4 + 0 + 3 = 12

Minimum cost: 5 (target length 2)
```

**Implementation**:
```python
def brute_force_stick_lengths(sticks):
    """
    Find minimum cost using brute force approach
    
    Args:
        sticks: list of stick lengths
    
    Returns:
        int: minimum cost to make all sticks the same length
    """
    min_length = min(sticks)
    max_length = max(sticks)
    min_cost = float('inf')
    
    # Try all possible target lengths
    for target in range(min_length, max_length + 1):
        cost = 0
        for stick in sticks:
            cost += abs(stick - target)
        min_cost = min(min_cost, cost)
    
    return min_cost

# Example usage
sticks = [2, 3, 1, 5, 2]
result = brute_force_stick_lengths(sticks)
print(f"Brute force result: {result}")  # Output: 5
```

**Time Complexity**: O(n × (max - min)) - For each target, check all sticks
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Use Median

**Key Insights from Optimized Approach**:
- **Median Property**: The median minimizes the sum of absolute differences
- **Efficient Calculation**: Calculate median in O(n log n) time
- **Better Complexity**: Achieve O(n log n) time complexity
- **Mathematical Insight**: Median is the optimal target length

**Key Insight**: The median of the stick lengths is the optimal target length that minimizes the total cost.

**Algorithm**:
- Sort the stick lengths
- Find the median (middle element)
- Calculate the cost to make all sticks the median length

**Visual Example**:
```
Stick lengths: [2, 3, 1, 5, 2]
Sorted: [1, 2, 2, 3, 5]
Median: 2 (middle element)

Cost calculation:
|2-2| + |3-2| + |1-2| + |5-2| + |2-2| = 0 + 1 + 1 + 3 + 0 = 5
```

**Implementation**:
```python
def optimized_stick_lengths(sticks):
    """
    Find minimum cost using median approach
    
    Args:
        sticks: list of stick lengths
    
    Returns:
        int: minimum cost to make all sticks the same length
    """
    sorted_sticks = sorted(sticks)
    n = len(sorted_sticks)
    
    # Find median (middle element)
    median = sorted_sticks[n // 2]
    
    # Calculate cost to make all sticks the median length
    cost = 0
    for stick in sticks:
        cost += abs(stick - median)
    
    return cost

# Example usage
sticks = [2, 3, 1, 5, 2]
result = optimized_stick_lengths(sticks)
print(f"Optimized result: {result}")  # Output: 5
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(n) - For sorted array

**Why it's better**: Much more efficient than brute force with mathematical insight.

---

### Approach 3: Optimal - Quick Select for Median

**Key Insights from Optimal Approach**:
- **Quick Select**: Use quick select algorithm to find median in O(n) time
- **Optimal Complexity**: Achieve O(n) time complexity
- **Efficient Implementation**: No need to sort the entire array
- **Optimal Performance**: Best possible time complexity

**Key Insight**: Use quick select algorithm to find the median in O(n) time without sorting the entire array.

**Algorithm**:
- Use quick select to find the median in O(n) time
- Calculate the cost to make all sticks the median length

**Visual Example**:
```
Stick lengths: [2, 3, 1, 5, 2]
Quick select to find median: 2

Cost calculation:
|2-2| + |3-2| + |1-2| + |5-2| + |2-2| = 0 + 1 + 1 + 3 + 0 = 5
```

**Implementation**:
```python
def optimal_stick_lengths(sticks):
    """
    Find minimum cost using quick select for median
    
    Args:
        sticks: list of stick lengths
    
    Returns:
        int: minimum cost to make all sticks the same length
    """
    def quick_select(arr, k):
        """Find k-th smallest element using quick select"""
        if len(arr) == 1:
            return arr[0]
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        if k < len(left):
            return quick_select(left, k)
        elif k < len(left) + len(middle):
            return pivot
        else:
            return quick_select(right, k - len(left) - len(middle))
    
    n = len(sticks)
    median = quick_select(sticks, n // 2)
    
    # Calculate cost to make all sticks the median length
    cost = 0
    for stick in sticks:
        cost += abs(stick - median)
    
    return cost

# Example usage
sticks = [2, 3, 1, 5, 2]
result = optimal_stick_lengths(sticks)
print(f"Optimal result: {result}")  # Output: 5
```

**Time Complexity**: O(n) - Quick select for median
**Space Complexity**: O(n) - For recursive calls

**Why it's optimal**: Achieves the best possible time complexity for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n × (max - min)) | O(1) | Try all possible target lengths |
| Median Sort | O(n log n) | O(n) | Use median to minimize cost |
| Quick Select | O(n) | O(n) | Find median in linear time |

### Time Complexity
- **Time**: O(n) - Quick select algorithm provides optimal time complexity
- **Space**: O(n) - For recursive calls in quick select

### Why This Solution Works
- **Median Property**: The median minimizes the sum of absolute differences
- **Mathematical Proof**: Median is the optimal target length for this problem
- **Efficient Algorithm**: Quick select finds median in O(n) time
- **Optimal Approach**: Quick select provides the most efficient solution for finding the median
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
