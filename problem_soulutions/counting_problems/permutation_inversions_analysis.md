---
layout: simple
title: "Permutation Inversions"
permalink: /problem_soulutions/counting_problems/permutation_inversions_analysis
---


# Permutation Inversions

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of inversions in permutations and their properties
- Apply merge sort algorithm to count inversions efficiently
- Implement binary indexed tree (Fenwick tree) for inversion counting
- Optimize inversion counting algorithms for large permutations
- Handle edge cases in inversion counting (sorted arrays, reverse sorted arrays)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Merge sort, binary indexed tree, segment tree, divide and conquer
- **Data Structures**: Arrays, binary indexed trees, segment trees, merge sort arrays
- **Mathematical Concepts**: Permutations, inversions, divide and conquer, counting principles
- **Programming Skills**: Merge sort implementation, binary indexed tree operations, divide and conquer
- **Related Problems**: Counting Permutations (permutation properties), Sorting algorithms (merge sort), Range Queries (binary indexed tree)

## 📋 Problem Description

Given a permutation of numbers from 1 to n, count the number of inversions. An inversion is a pair of indices (i,j) where i < j and a[i] > a[j].

**Input**: 
- First line: integer n (size of the permutation)
- Second line: n integers (the permutation)

**Output**: 
- Print one integer: the number of inversions

**Constraints**:
- 1 ≤ n ≤ 2×10^5
- The input is a valid permutation of 1 to n

**Example**:
```
Input:
4
3 1 4 2

Output:
3

Explanation**: 
In the permutation [3, 1, 4, 2], there are 3 inversions:
1. (0, 1): 3 > 1 (indices 0 and 1)
2. (0, 3): 3 > 2 (indices 0 and 3)
3. (2, 3): 4 > 2 (indices 2 and 3)

These are the pairs where a larger element appears before a smaller element.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Pairs

**Key Insights from Brute Force Approach**:
- **Exhaustive Pair Checking**: Check all possible pairs (i,j) where i < j
- **Inversion Detection**: Count pairs where a[i] > a[j]
- **Complete Coverage**: Guaranteed to find all inversions
- **Simple Implementation**: Nested loops approach

**Key Insight**: Systematically check all possible pairs of indices to count inversions where a larger element appears before a smaller element.

**Algorithm**:
- Use nested loops to check all pairs (i,j) where i < j
- Count pairs where a[i] > a[j]
- Return the total count

**Visual Example**:
```
Permutation: [3, 1, 4, 2]

All possible pairs (i,j) where i < j:
1. (0,1): a[0]=3, a[1]=1 → 3 > 1 ✓ (inversion)
2. (0,2): a[0]=3, a[2]=4 → 3 < 4 ✗
3. (0,3): a[0]=3, a[3]=2 → 3 > 2 ✓ (inversion)
4. (1,2): a[1]=1, a[2]=4 → 1 < 4 ✗
5. (1,3): a[1]=1, a[3]=2 → 1 < 2 ✗
6. (2,3): a[2]=4, a[3]=2 → 4 > 2 ✓ (inversion)

Total inversions: 3
```

**Implementation**:
```python
def brute_force_inversions(arr):
    """
    Count inversions using brute force approach
    
    Args:
        arr: list of integers (permutation)
    
    Returns:
        int: number of inversions
    """
    n = len(arr)
    count = 0
    
    # Check all possible pairs
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    
    return count

# Example usage
arr = [3, 1, 4, 2]
result = brute_force_inversions(arr)
print(f"Brute force result: {result}")  # Output: 3
```

**Time Complexity**: O(n²) - Check all pairs
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Merge Sort with Inversion Counting

**Key Insights from Optimized Approach**:
- **Divide and Conquer**: Use merge sort's divide and conquer approach
- **Inversion Counting**: Count inversions during the merge process
- **Efficient Merging**: Count cross-inversions between left and right halves
- **Recursive Solution**: Solve subproblems recursively

**Key Insight**: Use merge sort's merge process to count inversions efficiently by counting cross-inversions between sorted halves.

**Algorithm**:
- Divide the array into two halves
- Recursively count inversions in each half
- Count cross-inversions during merge
- Return total inversions

**Visual Example**:
```
Permutation: [3, 1, 4, 2]

Step 1: Divide
Left: [3, 1], Right: [4, 2]

Step 2: Recursively sort and count
Left: [1, 3] (1 inversion: 3 > 1)
Right: [2, 4] (1 inversion: 4 > 2)

Step 3: Merge and count cross-inversions
Merge [1, 3] and [2, 4]:
- 1 < 2 → Take 1, no cross-inversions
- 3 > 2 → Take 2, cross-inversion: 3 > 2
- 3 < 4 → Take 3, no cross-inversions
- Take 4

Result: [1, 2, 3, 4]
Total inversions: 1 + 1 + 1 = 3
```

**Implementation**:
```python
def optimized_inversions(arr):
    """
    Count inversions using merge sort approach
    
    Args:
        arr: list of integers (permutation)
    
    Returns:
        int: number of inversions
    """
    def merge_sort_and_count(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left, left_inv = merge_sort_and_count(arr[:mid])
        right, right_inv = merge_sort_and_count(arr[mid:])
        
        merged, cross_inv = merge_and_count(left, right)
        total_inv = left_inv + right_inv + cross_inv
        
        return merged, total_inv
    
    def merge_and_count(left, right):
        merged = []
        i = j = 0
        cross_inversions = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                cross_inversions += len(left) - i
                j += 1
        
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, cross_inversions
    
    _, total_inversions = merge_sort_and_count(arr)
    return total_inversions

# Example usage
arr = [3, 1, 4, 2]
result = optimized_inversions(arr)
print(f"Optimized result: {result}")  # Output: 3
```

**Time Complexity**: O(n log n) - Merge sort complexity
**Space Complexity**: O(n) - For temporary arrays during merge

**Why it's better**: Much more efficient than brute force, using divide and conquer.

---

### Approach 3: Optimal - Binary Indexed Tree (Fenwick Tree)

**Key Insights from Optimal Approach**:
- **Coordinate Compression**: Map values to compressed coordinates
- **Binary Indexed Tree**: Use BIT for efficient range queries
- **Right-to-Left Processing**: Process elements from right to left
- **Efficient Counting**: Count smaller elements to the right efficiently

**Key Insight**: Use coordinate compression and Binary Indexed Tree to efficiently count inversions by processing elements from right to left and counting smaller elements to the right.

**Algorithm**:
- Compress coordinates to handle large values
- Process elements from right to left
- For each element, count smaller elements to the right using BIT
- Update BIT with current element

**Visual Example**:
```
Permutation: [3, 1, 4, 2]

Step 1: Coordinate compression
Original: [3, 1, 4, 2]
Compressed: [2, 0, 3, 1] (sorted: [1, 2, 3, 4] → [0, 1, 2, 3])

Step 2: Process from right to left
BIT: [0, 0, 0, 0]

i=3: arr[3]=2, compressed=1
- Count smaller elements to right: 0
- Update BIT[1] = 1
- BIT: [0, 1, 0, 0]

i=2: arr[2]=4, compressed=3
- Count smaller elements to right: 1 (element 2)
- Update BIT[3] = 1
- BIT: [0, 1, 0, 1]

i=1: arr[1]=1, compressed=0
- Count smaller elements to right: 0
- Update BIT[0] = 1
- BIT: [1, 1, 0, 1]

i=0: arr[0]=3, compressed=2
- Count smaller elements to right: 2 (elements 1 and 2)
- Update BIT[2] = 1
- BIT: [1, 1, 1, 1]

Total inversions: 0 + 1 + 0 + 2 = 3
```

**Implementation**:
```python
def optimal_inversions(arr):
    """
    Count inversions using Binary Indexed Tree
    
    Args:
        arr: list of integers (permutation)
    
    Returns:
        int: number of inversions
    """
    # Coordinate compression
    sorted_arr = sorted(arr)
    compressed = {}
    for i, val in enumerate(sorted_arr):
        compressed[val] = i
    
    # Binary Indexed Tree implementation
    class BIT:
        def __init__(self, size):
            self.size = size
            self.tree = [0] * (size + 1)
        
        def update(self, idx, delta):
            while idx <= self.size:
                self.tree[idx] += delta
                idx += idx & -idx
        
        def query(self, idx):
            result = 0
            while idx > 0:
                result += self.tree[idx]
                idx -= idx & -idx
            return result
    
    n = len(arr)
    bit = BIT(n)
    inversions = 0
    
    # Process from right to left
    for i in range(n - 1, -1, -1):
        compressed_val = compressed[arr[i]] + 1  # 1-indexed
        inversions += bit.query(compressed_val - 1)
        bit.update(compressed_val, 1)
    
    return inversions

# Example usage
arr = [3, 1, 4, 2]
result = optimal_inversions(arr)
print(f"Optimal result: {result}")  # Output: 3
```

**Time Complexity**: O(n log n) - Coordinate compression + BIT operations
**Space Complexity**: O(n) - For BIT and coordinate mapping

**Why it's optimal**: Efficient algorithm using advanced data structures for optimal performance.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all pairs |
| Merge Sort | O(n log n) | O(n) | Divide and conquer |
| Binary Indexed Tree | O(n log n) | O(n) | Coordinate compression + BIT |

### Time Complexity
- **Time**: O(n log n) - Optimal for inversion counting
- **Space**: O(n) - For auxiliary data structures

### Why This Solution Works
- **Inversion Definition**: Count pairs where larger element appears before smaller element
- **Efficient Counting**: Use divide and conquer or advanced data structures
- **Coordinate Compression**: Handle large values efficiently
- **Optimal Approach**: Binary Indexed Tree provides best practical performance
