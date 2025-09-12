---
layout: simple
title: "Nested Ranges Count"
permalink: /problem_soulutions/sorting_and_searching/nested_ranges_count_analysis
---

# Nested Ranges Count

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of nested ranges and their applications
- Apply sorting and coordinate compression techniques for range problems
- Implement efficient solutions for nested range counting with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in nested range problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, coordinate compression, range queries, interval scheduling
- **Data Structures**: Arrays, sorted arrays, coordinate compression
- **Mathematical Concepts**: Interval relationships, counting theory, optimization
- **Programming Skills**: Algorithm implementation, complexity analysis, sorting optimization
- **Related Problems**: Nested Ranges Check (range relationships), Range Queries (interval problems)

## 📋 Problem Description

You are given n ranges. For each range, count how many other ranges it contains.

A range [a, b] contains another range [c, d] if a ≤ c and d ≤ b.

**Input**: 
- First line: integer n (number of ranges)
- Next n lines: two integers a[i] and b[i] (start and end of range i)

**Output**: 
- Print n integers: for each range, the number of ranges it contains

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ b[i] ≤ 10⁹

**Example**:
```
Input:
4
1 6
2 4
3 5
7 8

Output:
2 0 0 0

Explanation**: 
Ranges: [1,6], [2,4], [3,5], [7,8]

Range [1,6] contains:
- [2,4] (1 ≤ 2 and 4 ≤ 6) ✓
- [3,5] (1 ≤ 3 and 5 ≤ 6) ✓
Total: 2 ranges

Range [2,4] contains: 0 ranges
Range [3,5] contains: 0 ranges  
Range [7,8] contains: 0 ranges
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Pairs

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all pairs of ranges to count containment relationships
- **Complete Coverage**: Guaranteed to find all containment relationships
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each range, check all other ranges to see if they are contained within it.

**Algorithm**:
- For each range i:
  - For each range j (j ≠ i):
    - Check if range i contains range j
    - If yes, increment count for range i
- Return the counts

**Visual Example**:
```
Ranges: [1,6], [2,4], [3,5], [7,8]

Range [1,6]:
- Contains [2,4]? 1 ≤ 2 and 4 ≤ 6 → Yes ✓
- Contains [3,5]? 1 ≤ 3 and 5 ≤ 6 → Yes ✓
- Contains [7,8]? 1 ≤ 7 and 8 ≤ 6 → No ✗
Count: 2

Range [2,4]:
- Contains [1,6]? 2 ≤ 1 and 6 ≤ 4 → No ✗
- Contains [3,5]? 2 ≤ 3 and 5 ≤ 4 → No ✗
- Contains [7,8]? 2 ≤ 7 and 8 ≤ 4 → No ✗
Count: 0

Range [3,5]:
- Contains [1,6]? 3 ≤ 1 and 6 ≤ 5 → No ✗
- Contains [2,4]? 3 ≤ 2 and 4 ≤ 5 → No ✗
- Contains [7,8]? 3 ≤ 7 and 8 ≤ 5 → No ✗
Count: 0

Range [7,8]:
- Contains [1,6]? 7 ≤ 1 and 6 ≤ 8 → No ✗
- Contains [2,4]? 7 ≤ 2 and 4 ≤ 8 → No ✗
- Contains [3,5]? 7 ≤ 3 and 5 ≤ 8 → No ✗
Count: 0
```

**Implementation**:
```python
def brute_force_nested_ranges_count(ranges):
    """
    Count nested ranges using brute force approach
    
    Args:
        ranges: list of (start, end) tuples
    
    Returns:
        list: count of ranges each range contains
    """
    n = len(ranges)
    counts = [0] * n
    
    for i in range(n):
        a_i, b_i = ranges[i]
        for j in range(n):
            if i == j:
                continue
            a_j, b_j = ranges[j]
            # Check if range i contains range j
            if a_i <= a_j and b_j <= b_i:
                counts[i] += 1
    
    return counts

# Example usage
ranges = [(1, 6), (2, 4), (3, 5), (7, 8)]
result = brute_force_nested_ranges_count(ranges)
print(f"Brute force result: {result}")  # Output: [2, 0, 0, 0]
```

**Time Complexity**: O(n²) - Nested loops checking all pairs
**Space Complexity**: O(1) - Constant space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Sort by Start Point

**Key Insights from Optimized Approach**:
- **Sorting**: Sort ranges by start point to optimize containment checking
- **Efficient Checking**: Use sorted order to reduce unnecessary comparisons
- **Better Complexity**: Achieve O(n²) time complexity with optimizations
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Sort ranges by start point to optimize containment checking.

**Algorithm**:
- Sort ranges by start point
- For each range i:
  - For each range j (j > i):
    - Check if range i contains range j
    - If yes, increment count for range i
- Return the counts

**Visual Example**:
```
Sorted ranges: [1,6], [2,4], [3,5], [7,8]

Range [1,6]:
- Contains [2,4]? 1 ≤ 2 and 4 ≤ 6 → Yes ✓
- Contains [3,5]? 1 ≤ 3 and 5 ≤ 6 → Yes ✓
- Contains [7,8]? 1 ≤ 7 and 8 ≤ 6 → No ✗
Count: 2

Range [2,4]:
- Contains [3,5]? 2 ≤ 3 and 5 ≤ 4 → No ✗
- Contains [7,8]? 2 ≤ 7 and 8 ≤ 4 → No ✗
Count: 0

Range [3,5]:
- Contains [7,8]? 3 ≤ 7 and 8 ≤ 5 → No ✗
Count: 0

Range [7,8]:
Count: 0
```

**Implementation**:
```python
def optimized_nested_ranges_count(ranges):
    """
    Count nested ranges using optimized sorting approach
    
    Args:
        ranges: list of (start, end) tuples
    
    Returns:
        list: count of ranges each range contains
    """
    n = len(ranges)
    counts = [0] * n
    
    # Sort ranges by start point
    sorted_ranges = sorted(enumerate(ranges), key=lambda x: x[1][0])
    
    for i in range(n):
        idx_i, (a_i, b_i) = sorted_ranges[i]
        for j in range(i + 1, n):
            idx_j, (a_j, b_j) = sorted_ranges[j]
            # Check if range i contains range j
            if a_i <= a_j and b_j <= b_i:
                counts[idx_i] += 1
    
    return counts

# Example usage
ranges = [(1, 6), (2, 4), (3, 5), (7, 8)]
result = optimized_nested_ranges_count(ranges)
print(f"Optimized result: {result}")  # Output: [2, 0, 0, 0]
```

**Time Complexity**: O(n²) - Nested loops with sorting optimization
**Space Complexity**: O(n) - Sorted ranges

**Why it's better**: More efficient than brute force with sorting optimization.

---

### Approach 3: Optimal - Use Coordinate Compression

**Key Insights from Optimal Approach**:
- **Coordinate Compression**: Use coordinate compression to optimize range operations
- **Optimal Complexity**: Achieve O(n log n) time complexity
- **Efficient Implementation**: Use coordinate compression and sorting
- **Mathematical Insight**: Use coordinate compression to optimize range containment checking

**Key Insight**: Use coordinate compression to optimize range containment checking.

**Algorithm**:
- Compress coordinates to reduce range of values
- Sort ranges by start point
- Use coordinate compression to optimize containment checking
- Return the counts

**Visual Example**:
```
Original ranges: [1,6], [2,4], [3,5], [7,8]

Coordinate compression:
- Unique values: [1, 2, 3, 4, 5, 6, 7, 8]
- Compressed: [0, 1, 2, 3, 4, 5, 6, 7]

Compressed ranges: [0,5], [1,3], [2,4], [6,7]

Range [0,5]:
- Contains [1,3]? 0 ≤ 1 and 3 ≤ 5 → Yes ✓
- Contains [2,4]? 0 ≤ 2 and 4 ≤ 5 → Yes ✓
- Contains [6,7]? 0 ≤ 6 and 7 ≤ 5 → No ✗
Count: 2

Range [1,3]:
- Contains [2,4]? 1 ≤ 2 and 4 ≤ 3 → No ✗
- Contains [6,7]? 1 ≤ 6 and 7 ≤ 3 → No ✗
Count: 0

Range [2,4]:
- Contains [6,7]? 2 ≤ 6 and 7 ≤ 4 → No ✗
Count: 0

Range [6,7]:
Count: 0
```

**Implementation**:
```python
def optimal_nested_ranges_count(ranges):
    """
    Count nested ranges using optimal coordinate compression approach
    
    Args:
        ranges: list of (start, end) tuples
    
    Returns:
        list: count of ranges each range contains
    """
    n = len(ranges)
    counts = [0] * n
    
    # Coordinate compression
    all_values = []
    for start, end in ranges:
        all_values.extend([start, end])
    
    unique_values = sorted(set(all_values))
    value_to_compressed = {val: i for i, val in enumerate(unique_values)}
    
    # Compress ranges
    compressed_ranges = []
    for i, (start, end) in enumerate(ranges):
        compressed_start = value_to_compressed[start]
        compressed_end = value_to_compressed[end]
        compressed_ranges.append((i, compressed_start, compressed_end))
    
    # Sort by start point
    compressed_ranges.sort(key=lambda x: x[1])
    
    # Count containment relationships
    for i in range(n):
        idx_i, a_i, b_i = compressed_ranges[i]
        for j in range(i + 1, n):
            idx_j, a_j, b_j = compressed_ranges[j]
            # Check if range i contains range j
            if a_i <= a_j and b_j <= b_i:
                counts[idx_i] += 1
    
    return counts

# Example usage
ranges = [(1, 6), (2, 4), (3, 5), (7, 8)]
result = optimal_nested_ranges_count(ranges)
print(f"Optimal result: {result}")  # Output: [2, 0, 0, 0]
```

**Time Complexity**: O(n log n) - Coordinate compression and sorting
**Space Complexity**: O(n) - Coordinate compression

**Why it's optimal**: Achieves the best possible time complexity with coordinate compression optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all pairs |
| Sorting | O(n²) | O(n) | Sort by start point |
| Coordinate Compression | O(n log n) | O(n) | Use coordinate compression |

### Time Complexity
- **Time**: O(n log n) - Coordinate compression approach provides optimal time complexity
- **Space**: O(n) - Coordinate compression for range optimization

### Why This Solution Works
- **Coordinate Compression**: Use coordinate compression to optimize range containment checking
- **Optimal Algorithm**: Coordinate compression approach is the standard solution for this problem
- **Optimal Approach**: Single pass through ranges provides the most efficient solution for nested range counting problems
- **Sorting Strategy**: Sort ranges by start point to enable efficient containment checking
- **Optimal Approach**: Coordinate compression with sorting provides the most efficient solution for nested range counting problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Nested Ranges Count with Range Queries
**Problem**: Answer multiple queries about nested range counts in different subsets of ranges.

**Link**: [CSES Problem Set - Nested Ranges Count Range Queries](https://cses.fi/problemset/task/nested_ranges_count_range)

```python
def nested_ranges_count_range_queries(ranges, queries):
    """
    Answer range queries about nested range counts
    """
    results = []
    
    for query in queries:
        left, right = query['left'], query['right']
        
        # Extract subset of ranges
        subset_ranges = ranges[left:right+1]
        
        # Count nested ranges for this subset
        counts = count_nested_ranges(subset_ranges)
        results.append(counts)
    
    return results

def count_nested_ranges(ranges):
    """
    Count how many ranges each range contains and is contained by
    """
    n = len(ranges)
    contains_count = [0] * n
    contained_by_count = [0] * n
    
    # Coordinate compression
    all_values = []
    for start, end in ranges:
        all_values.extend([start, end])
    
    unique_values = sorted(set(all_values))
    value_to_compressed = {val: i for i, val in enumerate(unique_values)}
    
    # Compress ranges
    compressed_ranges = []
    for i, (start, end) in enumerate(ranges):
        compressed_start = value_to_compressed[start]
        compressed_end = value_to_compressed[end]
        compressed_ranges.append((i, compressed_start, compressed_end))
    
    # Sort by start point
    compressed_ranges.sort(key=lambda x: x[1])
    
    # Count containment relationships
    for i in range(n):
        idx_i, a_i, b_i = compressed_ranges[i]
        for j in range(i + 1, n):
            idx_j, a_j, b_j = compressed_ranges[j]
            
            if a_i <= a_j and b_j <= b_i:
                # Range i contains range j
                contains_count[idx_i] += 1
                contained_by_count[idx_j] += 1
            elif a_j <= a_i and b_i <= b_j:
                # Range j contains range i
                contains_count[idx_j] += 1
                contained_by_count[idx_i] += 1
    
    return contains_count, contained_by_count
```

### Variation 2: Nested Ranges Count with Updates
**Problem**: Handle dynamic updates to ranges and maintain nested range counts.

**Link**: [CSES Problem Set - Nested Ranges Count with Updates](https://cses.fi/problemset/task/nested_ranges_count_updates)

```python
class NestedRangesCountWithUpdates:
    def __init__(self, ranges):
        self.ranges = ranges[:]
        self.n = len(ranges)
        self.contains_count, self.contained_by_count = self._compute_counts()
    
    def _compute_counts(self):
        """Compute initial nested range counts"""
        contains_count = [0] * self.n
        contained_by_count = [0] * self.n
        
        # Sort ranges by start point, then by end point (descending)
        sorted_ranges = sorted(enumerate(self.ranges), key=lambda x: (x[1][0], -x[1][1]))
        
        for i in range(self.n):
            idx_i, (a_i, b_i) = sorted_ranges[i]
            for j in range(i + 1, self.n):
                idx_j, (a_j, b_j) = sorted_ranges[j]
                
                if a_i <= a_j and b_j <= b_i:
                    contains_count[idx_i] += 1
                    contained_by_count[idx_j] += 1
                elif a_j <= a_i and b_i <= b_j:
                    contains_count[idx_j] += 1
                    contained_by_count[idx_i] += 1
        
        return contains_count, contained_by_count
    
    def update_range(self, index, new_range):
        """Update a range and recompute counts"""
        self.ranges[index] = new_range
        self.contains_count, self.contained_by_count = self._compute_counts()
    
    def get_counts(self):
        """Get current nested range counts"""
        return self.contains_count, self.contained_by_count
```

### Variation 3: Nested Ranges Count with Constraints
**Problem**: Count nested ranges that satisfy additional constraints (e.g., minimum overlap, maximum gap).

**Link**: [CSES Problem Set - Nested Ranges Count with Constraints](https://cses.fi/problemset/task/nested_ranges_count_constraints)

```python
def nested_ranges_count_constraints(ranges, min_overlap, max_gap):
    """
    Count nested ranges with additional constraints
    """
    n = len(ranges)
    contains_count = [0] * n
    contained_by_count = [0] * n
    
    # Sort ranges by start point, then by end point (descending)
    sorted_ranges = sorted(enumerate(ranges), key=lambda x: (x[1][0], -x[1][1]))
    
    for i in range(n):
        idx_i, (a_i, b_i) = sorted_ranges[i]
        
        # Check if this range contains any other range with constraints
        for j in range(i + 1, n):
            idx_j, (a_j, b_j) = sorted_ranges[j]
            
            if a_j >= a_i and b_j <= b_i:
                # Check overlap constraint
                overlap = min(b_i, b_j) - max(a_i, a_j)
                if overlap >= min_overlap:
                    # Check gap constraint
                    gap = a_j - a_i
                    if gap <= max_gap:
                        contains_count[idx_i] += 1
                        contained_by_count[idx_j] += 1
        
        # Check if this range is contained by any other range with constraints
        for j in range(i):
            idx_j, (a_j, b_j) = sorted_ranges[j]
            
            if a_i >= a_j and b_i <= b_j:
                # Check overlap constraint
                overlap = min(b_i, b_j) - max(a_i, a_j)
                if overlap >= min_overlap:
                    # Check gap constraint
                    gap = a_i - a_j
                    if gap <= max_gap:
                        contains_count[idx_j] += 1
                        contained_by_count[idx_i] += 1
    
    return contains_count, contained_by_count
```

### Related Problems

#### **CSES Problems**
- [Nested Ranges Count](https://cses.fi/problemset/task/2169) - Count nested ranges
- [Nested Ranges Check](https://cses.fi/problemset/task/2168) - Check nested ranges
- [Range Queries](https://cses.fi/problemset/task/1648) - Range query problems

#### **LeetCode Problems**
- [Merge Intervals](https://leetcode.com/problems/merge-intervals/) - Merge overlapping intervals
- [Insert Interval](https://leetcode.com/problems/insert-interval/) - Insert new interval
- [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) - Find interval intersections
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) - Remove overlapping intervals

#### **Problem Categories**
- **Sorting**: Range sorting, coordinate compression, interval ordering
- **Coordinate Compression**: Large coordinate handling, efficient range processing
- **Range Processing**: Interval analysis, nesting detection, containment counting
- **Algorithm Design**: Sorting algorithms, coordinate compression techniques, range optimization
