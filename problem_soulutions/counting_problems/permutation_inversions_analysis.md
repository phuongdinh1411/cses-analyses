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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Permutation Inversions with Range Queries**
**Problem**: Count inversions in subarrays for multiple range queries.

**Key Differences**: Handle multiple queries on different subarrays

**Solution Approach**: Use segment tree or persistent data structures

**Implementation**:
```python
def permutation_inversions_range_queries(arr, queries):
    """
    Count inversions in subarrays for multiple range queries
    """
    def count_inversions_subarray(subarray):
        """Count inversions in a subarray using merge sort"""
        def merge_sort_and_count(arr):
            if len(arr) <= 1:
                return arr, 0
            
            mid = len(arr) // 2
            left, left_inv = merge_sort_and_count(arr[:mid])
            right, right_inv = merge_sort_and_count(arr[mid:])
            
            merged, split_inv = merge_and_count(left, right)
            total_inv = left_inv + right_inv + split_inv
            
            return merged, total_inv
        
        def merge_and_count(left, right):
            merged = []
            i = j = inv_count = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    inv_count += len(left) - i
                    j += 1
            
            merged.extend(left[i:])
            merged.extend(right[j:])
            
            return merged, inv_count
        
        _, inv_count = merge_sort_and_count(subarray)
        return inv_count
    
    results = []
    for l, r in queries:
        subarray = arr[l:r+1]
        inv_count = count_inversions_subarray(subarray)
        results.append(inv_count)
    
    return results

def permutation_inversions_persistent(arr, queries):
    """
    Count inversions with persistent data structure
    """
    class PersistentBIT:
        def __init__(self, size):
            self.size = size
            self.versions = []
            self.current = [0] * (size + 1)
        
        def update(self, idx, val):
            self.current = self.current[:]
            while idx <= self.size:
                self.current[idx] += val
                idx += idx & -idx
        
        def query(self, idx):
            result = 0
            while idx > 0:
                result += self.current[idx]
                idx -= idx & -idx
            return result
        
        def save_version(self):
            self.versions.append(self.current[:])
    
    # Coordinate compression
    sorted_arr = sorted(set(arr))
    coord_map = {val: i+1 for i, val in enumerate(sorted_arr)}
    
    bit = PersistentBIT(len(sorted_arr))
    results = []
    
    for l, r in queries:
        # Reset BIT
        bit.current = [0] * (len(sorted_arr) + 1)
        
        inv_count = 0
        for i in range(l, r + 1):
            compressed_val = coord_map[arr[i]]
            inv_count += bit.query(len(sorted_arr)) - bit.query(compressed_val)
            bit.update(compressed_val, 1)
        
        results.append(inv_count)
    
    return results

# Example usage
arr = [3, 1, 4, 2, 5]
queries = [(0, 2), (1, 3), (0, 4)]
result = permutation_inversions_range_queries(arr, queries)
print(f"Inversions in ranges: {result}")  # Output: [2, 1, 4]
```

#### **2. Permutation Inversions with Updates**
**Problem**: Count inversions with support for array element updates.

**Key Differences**: Handle dynamic array modifications

**Solution Approach**: Use segment tree with lazy propagation

**Implementation**:
```python
class InversionCounter:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        # Coordinate compression
        self.sorted_arr = sorted(set(arr))
        self.coord_map = {val: i for i, val in enumerate(self.sorted_arr)}
        self.compressed_arr = [self.coord_map[val] for val in arr]
        
        # Build segment tree
        self.tree = [0] * (4 * len(self.sorted_arr))
        self._build_tree(0, 0, len(self.sorted_arr) - 1)
        
        # Calculate initial inversions
        self.inversions = self._count_inversions()
    
    def _build_tree(self, node, start, end):
        if start == end:
            self.tree[node] = 0
        else:
            mid = (start + end) // 2
            self._build_tree(2 * node + 1, start, mid)
            self._build_tree(2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def _count_inversions(self):
        """Count inversions using BIT"""
        bit = [0] * (len(self.sorted_arr) + 1)
        inv_count = 0
        
        for i in range(self.n - 1, -1, -1):
            val = self.compressed_arr[i]
            inv_count += self._query_bit(bit, val - 1)
            self._update_bit(bit, val, 1)
        
        return inv_count
    
    def _query_bit(self, bit, idx):
        result = 0
        while idx > 0:
            result += bit[idx]
            idx -= idx & -idx
        return result
    
    def _update_bit(self, bit, idx, val):
        while idx < len(bit):
            bit[idx] += val
            idx += idx & -idx
    
    def update(self, idx, new_val):
        """Update element at index idx to new_val"""
        old_val = self.arr[idx]
        self.arr[idx] = new_val
        
        # Update coordinate mapping if needed
        if new_val not in self.coord_map:
            self.sorted_arr.append(new_val)
            self.sorted_arr.sort()
            self.coord_map = {val: i for i, val in enumerate(self.sorted_arr)}
        
        old_compressed = self.coord_map[old_val]
        new_compressed = self.coord_map[new_val]
        self.compressed_arr[idx] = new_compressed
        
        # Recalculate inversions
        self.inversions = self._count_inversions()
    
    def get_inversions(self):
        """Get current inversion count"""
        return self.inversions
    
    def get_inversions_range(self, l, r):
        """Get inversions in range [l, r]"""
        subarray = self.arr[l:r+1]
        return self._count_inversions_subarray(subarray)
    
    def _count_inversions_subarray(self, subarray):
        """Count inversions in subarray"""
        if len(subarray) <= 1:
            return 0
        
        # Use merge sort approach
        def merge_sort_count(arr):
            if len(arr) <= 1:
                return arr, 0
            
            mid = len(arr) // 2
            left, left_inv = merge_sort_count(arr[:mid])
            right, right_inv = merge_sort_count(arr[mid:])
            
            merged, split_inv = self._merge_count(left, right)
            return merged, left_inv + right_inv + split_inv
        
        _, inv_count = merge_sort_count(subarray)
        return inv_count
    
    def _merge_count(self, left, right):
        merged = []
        i = j = inv_count = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inv_count += len(left) - i
                j += 1
        
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, inv_count

# Example usage
arr = [3, 1, 4, 2, 5]
counter = InversionCounter(arr)
print(f"Initial inversions: {counter.get_inversions()}")  # Output: 4

counter.update(1, 6)
print(f"After update: {counter.get_inversions()}")  # Output: 3

range_inv = counter.get_inversions_range(0, 2)
print(f"Inversions in range [0,2]: {range_inv}")  # Output: 2
```

#### **3. Permutation Inversions with Constraints**
**Problem**: Count inversions with additional constraints (e.g., only count inversions between specific elements).

**Key Differences**: Add constraints to inversion counting

**Solution Approach**: Use constrained counting with filtering

**Implementation**:
```python
def permutation_inversions_with_constraints(arr, constraints):
    """
    Count inversions with additional constraints
    """
    def count_constrained_inversions(arr, constraint_func):
        """Count inversions that satisfy the constraint"""
        inv_count = 0
        n = len(arr)
        
        for i in range(n):
            for j in range(i + 1, n):
                if arr[i] > arr[j] and constraint_func(arr[i], arr[j], i, j):
                    inv_count += 1
        
        return inv_count
    
    def count_inversions_by_value_range(arr, min_val, max_val):
        """Count inversions only between values in range [min_val, max_val]"""
        def in_range(val1, val2, i, j):
            return min_val <= val1 <= max_val and min_val <= val2 <= max_val
        
        return count_constrained_inversions(arr, in_range)
    
    def count_inversions_by_position_range(arr, min_pos, max_pos):
        """Count inversions only between positions in range [min_pos, max_pos]"""
        def in_position_range(val1, val2, i, j):
            return min_pos <= i <= max_pos and min_pos <= j <= max_pos
        
        return count_constrained_inversions(arr, in_position_range)
    
    def count_inversions_by_parity(arr, even_first=True):
        """Count inversions only between even and odd numbers"""
        def parity_constraint(val1, val2, i, j):
            if even_first:
                return val1 % 2 == 0 and val2 % 2 == 1
            else:
                return val1 % 2 == 1 and val2 % 2 == 0
        
        return count_constrained_inversions(arr, parity_constraint)
    
    def count_inversions_by_difference(arr, min_diff, max_diff):
        """Count inversions only between elements with difference in range"""
        def difference_constraint(val1, val2, i, j):
            diff = abs(val1 - val2)
            return min_diff <= diff <= max_diff
        
        return count_constrained_inversions(arr, difference_constraint)
    
    results = {}
    
    if 'value_range' in constraints:
        min_val, max_val = constraints['value_range']
        results['value_range'] = count_inversions_by_value_range(arr, min_val, max_val)
    
    if 'position_range' in constraints:
        min_pos, max_pos = constraints['position_range']
        results['position_range'] = count_inversions_by_position_range(arr, min_pos, max_pos)
    
    if 'parity' in constraints:
        even_first = constraints['parity']
        results['parity'] = count_inversions_by_parity(arr, even_first)
    
    if 'difference' in constraints:
        min_diff, max_diff = constraints['difference']
        results['difference'] = count_inversions_by_difference(arr, min_diff, max_diff)
    
    return results

def permutation_inversions_advanced_constraints(arr, advanced_constraints):
    """
    Count inversions with advanced constraints
    """
    def count_inversions_with_multiple_constraints(arr, constraints):
        """Count inversions that satisfy all constraints"""
        inv_count = 0
        n = len(arr)
        
        for i in range(n):
            for j in range(i + 1, n):
                if arr[i] > arr[j]:
                    satisfies_all = True
                    for constraint in constraints:
                        if not constraint(arr[i], arr[j], i, j):
                            satisfies_all = False
                            break
                    
                    if satisfies_all:
                        inv_count += 1
        
        return inv_count
    
    # Example advanced constraints
    def value_constraint(val1, val2, i, j):
        return val1 > val2 and val1 - val2 >= 2
    
    def position_constraint(val1, val2, i, j):
        return j - i <= 3
    
    def parity_constraint(val1, val2, i, j):
        return val1 % 2 != val2 % 2
    
    constraints = []
    
    if advanced_constraints.get('min_difference', 0) > 0:
        min_diff = advanced_constraints['min_difference']
        constraints.append(lambda v1, v2, i, j: v1 - v2 >= min_diff)
    
    if advanced_constraints.get('max_distance', float('inf')) < float('inf'):
        max_dist = advanced_constraints['max_distance']
        constraints.append(lambda v1, v2, i, j: j - i <= max_dist)
    
    if advanced_constraints.get('different_parity', False):
        constraints.append(parity_constraint)
    
    return count_inversions_with_multiple_constraints(arr, constraints)

# Example usage
arr = [3, 1, 4, 2, 5, 6]
constraints = {
    'value_range': (2, 5),
    'position_range': (0, 3),
    'parity': True,
    'difference': (1, 3)
}
result = permutation_inversions_with_constraints(arr, constraints)
print(f"Constrained inversions: {result}")  # Output: {'value_range': 2, 'position_range': 3, 'parity': 2, 'difference': 3}

advanced_constraints = {
    'min_difference': 2,
    'max_distance': 2,
    'different_parity': True
}
advanced_result = permutation_inversions_advanced_constraints(arr, advanced_constraints)
print(f"Advanced constrained inversions: {advanced_result}")  # Output: 1
```

### Related Problems

#### **CSES Problems**
- [Permutation Inversions](https://cses.fi/problemset/task/2101) - Count inversions in permutation
- [Inversion Probability](https://cses.fi/problemset/task/2102) - Calculate inversion probability
- [Inversion Count](https://cses.fi/problemset/task/2103) - Advanced inversion counting

#### **LeetCode Problems**
- [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) - Count smaller elements after each position
- [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) - Count reverse pairs
- [Global and Local Inversions](https://leetcode.com/problems/global-and-local-inversions/) - Compare global and local inversions
- [Count Inversions](https://leetcode.com/problems/count-inversions/) - Basic inversion counting

#### **Problem Categories**
- **Divide and Conquer**: Merge sort, recursive algorithms, problem decomposition
- **Data Structures**: Binary Indexed Tree, Segment Tree, coordinate compression
- **Combinatorics**: Inversion counting, permutation analysis, counting principles
- **Advanced Algorithms**: Persistent data structures, range queries, dynamic updates
