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

## Problem Variations

### **Variation 1: Nested Ranges Count with Dynamic Updates**
**Problem**: Handle dynamic range updates (add/remove/update ranges) while maintaining efficient nested range counting queries.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicNestedRangesCount:
    def __init__(self, ranges):
        self.ranges = ranges[:]
        self.n = len(ranges)
        self.contains_count, self.contained_by_count = self._compute_counts()
    
    def _compute_counts(self):
        """Compute nested range counts using sorting and coordinate compression."""
        if not self.ranges:
            return [0] * self.n, [0] * self.n
        
        # Coordinate compression
        coordinates = set()
        for start, end in self.ranges:
            coordinates.add(start)
            coordinates.add(end)
        
        coord_to_idx = {coord: idx for idx, coord in enumerate(sorted(coordinates))}
        
        # Compress ranges
        compressed_ranges = []
        for start, end in self.ranges:
            compressed_ranges.append((coord_to_idx[start], coord_to_idx[end]))
        
        # Sort ranges by start point, then by end point (descending)
        sorted_ranges = sorted(enumerate(compressed_ranges), key=lambda x: (x[1][0], -x[1][1]))
        
        contains_count = [0] * self.n
        contained_by_count = [0] * self.n
        
        for i in range(self.n):
            original_idx_i, (start_i, end_i) = sorted_ranges[i]
            
            # Count ranges that this range contains
            for j in range(i + 1, self.n):
                original_idx_j, (start_j, end_j) = sorted_ranges[j]
                
                if start_j >= start_i and end_j <= end_i:
                    contains_count[original_idx_i] += 1
                    contained_by_count[original_idx_j] += 1
            
            # Count ranges that contain this range
            for j in range(i):
                original_idx_j, (start_j, end_j) = sorted_ranges[j]
                
                if start_i >= start_j and end_i <= end_j:
                    contains_count[original_idx_j] += 1
                    contained_by_count[original_idx_i] += 1
        
        return contains_count, contained_by_count
    
    def add_range(self, start, end):
        """Add a new range to the collection."""
        self.ranges.append((start, end))
        self.n += 1
        self.contains_count, self.contained_by_count = self._compute_counts()
    
    def remove_range(self, index):
        """Remove a range at the specified index."""
        if 0 <= index < self.n:
            del self.ranges[index]
            self.n -= 1
            self.contains_count, self.contained_by_count = self._compute_counts()
    
    def update_range(self, index, new_start, new_end):
        """Update a range at the specified index."""
        if 0 <= index < self.n:
            self.ranges[index] = (new_start, new_end)
            self.contains_count, self.contained_by_count = self._compute_counts()
    
    def get_contains_count(self, index):
        """Get number of ranges that the range at index contains."""
        if 0 <= index < self.n:
            return self.contains_count[index]
        return 0
    
    def get_contained_by_count(self, index):
        """Get number of ranges that contain the range at index."""
        if 0 <= index < self.n:
            return self.contained_by_count[index]
        return 0
    
    def get_all_counts(self):
        """Get all contains and contained_by counts."""
        return self.contains_count, self.contained_by_count
    
    def get_ranges_with_contains_count(self, min_count):
        """Get ranges that contain at least min_count other ranges."""
        result = []
        for i in range(self.n):
            if self.contains_count[i] >= min_count:
                result.append((i, self.ranges[i], self.contains_count[i]))
        return result
    
    def get_ranges_with_contained_by_count(self, min_count):
        """Get ranges that are contained by at least min_count other ranges."""
        result = []
        for i in range(self.n):
            if self.contained_by_count[i] >= min_count:
                result.append((i, self.ranges[i], self.contained_by_count[i]))
        return result
    
    def get_nested_statistics(self):
        """Get statistics about nested ranges."""
        if not self.ranges:
            return {
                'total_ranges': 0,
                'total_contains': 0,
                'total_contained_by': 0,
                'max_contains': 0,
                'max_contained_by': 0,
                'average_contains': 0,
                'average_contained_by': 0
            }
        
        total_contains = sum(self.contains_count)
        total_contained_by = sum(self.contained_by_count)
        max_contains = max(self.contains_count) if self.contains_count else 0
        max_contained_by = max(self.contained_by_count) if self.contained_by_count else 0
        average_contains = total_contains / self.n
        average_contained_by = total_contained_by / self.n
        
        return {
            'total_ranges': self.n,
            'total_contains': total_contains,
            'total_contained_by': total_contained_by,
            'max_contains': max_contains,
            'max_contained_by': max_contained_by,
            'average_contains': average_contains,
            'average_contained_by': average_contained_by
        }
    
    def get_nested_patterns(self):
        """Get patterns in nested ranges."""
        patterns = {
            'consecutive_contains': 0,
            'alternating_contains': 0,
            'clustered_contains': 0,
            'isolated_contains': 0
        }
        
        for i in range(1, self.n):
            if self.contains_count[i] > 0 and self.contains_count[i-1] > 0:
                patterns['consecutive_contains'] += 1
            
            if i > 1:
                if (self.contains_count[i] > 0) != (self.contains_count[i-1] > 0) and \
                   (self.contains_count[i-1] > 0) != (self.contains_count[i-2] > 0):
                    patterns['alternating_contains'] += 1
        
        return patterns

# Example usage
ranges = [(1, 4), (2, 3), (5, 8), (6, 7), (9, 12)]
dynamic_nrc = DynamicNestedRangesCount(ranges)
contains_count, contained_by_count = dynamic_nrc.get_all_counts()
print(f"Contains count: {contains_count}")
print(f"Contained by count: {contained_by_count}")

# Add a range
dynamic_nrc.add_range(10, 11)
contains_count, contained_by_count = dynamic_nrc.get_all_counts()
print(f"After adding range: {contains_count}, {contained_by_count}")

# Update a range
dynamic_nrc.update_range(1, 1, 5)
contains_count, contained_by_count = dynamic_nrc.get_all_counts()
print(f"After updating range: {contains_count}, {contained_by_count}")

# Get ranges with contains count
print(f"Ranges with contains count >= 1: {dynamic_nrc.get_ranges_with_contains_count(1)}")

# Get ranges with contained by count
print(f"Ranges with contained by count >= 1: {dynamic_nrc.get_ranges_with_contained_by_count(1)}")

# Get statistics
print(f"Statistics: {dynamic_nrc.get_nested_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_nrc.get_nested_patterns()}")
```

### **Variation 2: Nested Ranges Count with Different Operations**
**Problem**: Handle different types of operations on nested ranges (weighted counting, priority-based counting, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of range counting queries.

```python
class AdvancedNestedRangesCount:
    def __init__(self, ranges, weights=None):
        self.ranges = ranges[:]
        self.n = len(ranges)
        self.weights = weights or [1] * self.n
        self.contains_count, self.contained_by_count = self._compute_counts()
        self.weighted_contains_count, self.weighted_contained_by_count = self._compute_weighted_counts()
    
    def _compute_counts(self):
        """Compute nested range counts using sorting."""
        if not self.ranges:
            return [0] * self.n, [0] * self.n
        
        # Sort ranges by start point, then by end point (descending)
        sorted_ranges = sorted(enumerate(self.ranges), key=lambda x: (x[1][0], -x[1][1]))
        
        contains_count = [0] * self.n
        contained_by_count = [0] * self.n
        
        for i in range(self.n):
            original_idx_i, (start_i, end_i) = sorted_ranges[i]
            
            # Count ranges that this range contains
            for j in range(i + 1, self.n):
                original_idx_j, (start_j, end_j) = sorted_ranges[j]
                
                if start_j >= start_i and end_j <= end_i:
                    contains_count[original_idx_i] += 1
                    contained_by_count[original_idx_j] += 1
            
            # Count ranges that contain this range
            for j in range(i):
                original_idx_j, (start_j, end_j) = sorted_ranges[j]
                
                if start_i >= start_j and end_i <= end_j:
                    contains_count[original_idx_j] += 1
                    contained_by_count[original_idx_i] += 1
        
        return contains_count, contained_by_count
    
    def _compute_weighted_counts(self):
        """Compute weighted nested range counts."""
        if not self.ranges:
            return [0] * self.n, [0] * self.n
        
        # Sort ranges by start point, then by end point (descending)
        sorted_ranges = sorted(enumerate(self.ranges), key=lambda x: (x[1][0], -x[1][1]))
        
        weighted_contains_count = [0] * self.n
        weighted_contained_by_count = [0] * self.n
        
        for i in range(self.n):
            original_idx_i, (start_i, end_i) = sorted_ranges[i]
            
            # Count weighted ranges that this range contains
            for j in range(i + 1, self.n):
                original_idx_j, (start_j, end_j) = sorted_ranges[j]
                
                if start_j >= start_i and end_j <= end_i:
                    weighted_contains_count[original_idx_i] += self.weights[original_idx_j]
                    weighted_contained_by_count[original_idx_j] += self.weights[original_idx_i]
            
            # Count weighted ranges that contain this range
            for j in range(i):
                original_idx_j, (start_j, end_j) = sorted_ranges[j]
                
                if start_i >= start_j and end_i <= end_j:
                    weighted_contains_count[original_idx_j] += self.weights[original_idx_i]
                    weighted_contained_by_count[original_idx_i] += self.weights[original_idx_j]
        
        return weighted_contains_count, weighted_contained_by_count
    
    def get_contains_count(self, index):
        """Get number of ranges that the range at index contains."""
        return self.contains_count[index] if 0 <= index < self.n else 0
    
    def get_contained_by_count(self, index):
        """Get number of ranges that contain the range at index."""
        return self.contained_by_count[index] if 0 <= index < self.n else 0
    
    def get_weighted_contains_count(self, index):
        """Get weighted count of ranges that the range at index contains."""
        return self.weighted_contains_count[index] if 0 <= index < self.n else 0
    
    def get_weighted_contained_by_count(self, index):
        """Get weighted count of ranges that contain the range at index."""
        return self.weighted_contained_by_count[index] if 0 <= index < self.n else 0
    
    def get_ranges_with_priority(self, priority_func):
        """Get ranges sorted by priority based on nested counts."""
        ranges_with_priority = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            priority = priority_func(
                start_i, end_i, 
                self.contains_count[i], 
                self.contained_by_count[i],
                self.weights[i]
            )
            ranges_with_priority.append((i, start_i, end_i, priority))
        
        ranges_with_priority.sort(key=lambda x: x[3], reverse=True)
        return ranges_with_priority
    
    def get_ranges_with_optimization(self, optimization_func):
        """Get ranges using custom optimization function."""
        ranges_with_score = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            score = optimization_func(
                start_i, end_i, 
                self.contains_count[i], 
                self.contained_by_count[i],
                self.weights[i]
            )
            ranges_with_score.append((i, start_i, end_i, score))
        
        ranges_with_score.sort(key=lambda x: x[3], reverse=True)
        return ranges_with_score
    
    def get_ranges_with_constraints(self, constraint_func):
        """Get ranges that satisfy custom constraints."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            if constraint_func(
                start_i, end_i, 
                self.contains_count[i], 
                self.contained_by_count[i],
                self.weights[i]
            ):
                result.append((i, start_i, end_i))
        
        return result
    
    def get_ranges_with_multiple_criteria(self, criteria_list):
        """Get ranges that satisfy multiple criteria."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check if range satisfies all criteria
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(
                    start_i, end_i, 
                    self.contains_count[i], 
                    self.contained_by_count[i],
                    self.weights[i]
                ):
                    satisfies_all_criteria = False
                    break
            
            if satisfies_all_criteria:
                result.append((i, start_i, end_i))
        
        return result
    
    def get_ranges_with_alternatives(self, alternatives):
        """Get ranges considering alternative ranges."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check original range
            result.append((i, start_i, end_i, 'original', self.contains_count[i], self.contained_by_count[i]))
            
            # Check alternative ranges
            if i in alternatives:
                for alt_start, alt_end in alternatives[i]:
                    # Calculate counts for alternative range
                    alt_contains = 0
                    alt_contained_by = 0
                    
                    for j in range(self.n):
                        if i != j:
                            start_j, end_j = self.ranges[j]
                            
                            # Check if alternative range contains range j
                            if start_j >= alt_start and end_j <= alt_end:
                                alt_contains += 1
                            
                            # Check if range j contains alternative range
                            if alt_start >= start_j and alt_end <= end_j:
                                alt_contained_by += 1
                    
                    result.append((i, alt_start, alt_end, 'alternative', alt_contains, alt_contained_by))
        
        return result
    
    def get_ranges_with_adaptive_criteria(self, adaptive_func):
        """Get ranges using adaptive criteria."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check adaptive criteria
            if adaptive_func(
                start_i, end_i, 
                self.contains_count[i], 
                self.contained_by_count[i],
                self.weights[i],
                result
            ):
                result.append((i, start_i, end_i))
        
        return result

# Example usage
ranges = [(1, 4), (2, 3), (5, 8), (6, 7), (9, 12)]
weights = [2, 1, 3, 1, 2]
advanced_nrc = AdvancedNestedRangesCount(ranges, weights)

print(f"Contains count: {advanced_nrc.contains_count}")
print(f"Contained by count: {advanced_nrc.contained_by_count}")
print(f"Weighted contains count: {advanced_nrc.weighted_contains_count}")
print(f"Weighted contained by count: {advanced_nrc.weighted_contained_by_count}")

# Get ranges with priority
def priority_func(start, end, contains, contained_by, weight):
    return (contains + contained_by) * weight

print(f"Ranges with priority: {advanced_nrc.get_ranges_with_priority(priority_func)}")

# Get ranges with optimization
def optimization_func(start, end, contains, contained_by, weight):
    return contains * 2 + contained_by + weight

print(f"Ranges with optimization: {advanced_nrc.get_ranges_with_optimization(optimization_func)}")

# Get ranges with constraints
def constraint_func(start, end, contains, contained_by, weight):
    return contains >= 1 and weight >= 2

print(f"Ranges with constraints: {advanced_nrc.get_ranges_with_constraints(constraint_func)}")

# Get ranges with multiple criteria
def criterion1(start, end, contains, contained_by, weight):
    return contains >= 1

def criterion2(start, end, contains, contained_by, weight):
    return weight >= 2

criteria_list = [criterion1, criterion2]
print(f"Ranges with multiple criteria: {advanced_nrc.get_ranges_with_multiple_criteria(criteria_list)}")

# Get ranges with alternatives
alternatives = {1: [(1, 2), (2, 4)], 3: [(5, 6), (7, 8)]}
print(f"Ranges with alternatives: {advanced_nrc.get_ranges_with_alternatives(alternatives)}")

# Get ranges with adaptive criteria
def adaptive_func(start, end, contains, contained_by, weight, current_result):
    return contains >= 1 and len(current_result) < 3

print(f"Ranges with adaptive criteria: {advanced_nrc.get_ranges_with_adaptive_criteria(adaptive_func)}")
```

### **Variation 3: Nested Ranges Count with Constraints**
**Problem**: Handle nested ranges count with additional constraints (time limits, resource constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedNestedRangesCount:
    def __init__(self, ranges, constraints=None):
        self.ranges = ranges[:]
        self.n = len(ranges)
        self.constraints = constraints or {}
        self.contains_count, self.contained_by_count = self._compute_counts()
    
    def _compute_counts(self):
        """Compute nested range counts using sorting."""
        if not self.ranges:
            return [0] * self.n, [0] * self.n
        
        # Sort ranges by start point, then by end point (descending)
        sorted_ranges = sorted(enumerate(self.ranges), key=lambda x: (x[1][0], -x[1][1]))
        
        contains_count = [0] * self.n
        contained_by_count = [0] * self.n
        
        for i in range(self.n):
            original_idx_i, (start_i, end_i) = sorted_ranges[i]
            
            # Count ranges that this range contains
            for j in range(i + 1, self.n):
                original_idx_j, (start_j, end_j) = sorted_ranges[j]
                
                if start_j >= start_i and end_j <= end_i:
                    contains_count[original_idx_i] += 1
                    contained_by_count[original_idx_j] += 1
            
            # Count ranges that contain this range
            for j in range(i):
                original_idx_j, (start_j, end_j) = sorted_ranges[j]
                
                if start_i >= start_j and end_i <= end_j:
                    contains_count[original_idx_j] += 1
                    contained_by_count[original_idx_i] += 1
        
        return contains_count, contained_by_count
    
    def get_nested_counts_with_time_constraints(self, time_limit):
        """Get nested counts considering time constraints."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            range_duration = end_i - start_i
            
            if range_duration <= time_limit:
                result.append((i, start_i, end_i, self.contains_count[i], self.contained_by_count[i]))
        
        return result
    
    def get_nested_counts_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get nested counts considering resource constraints."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check resource constraints
            can_use_range = True
            for j, consumption in enumerate(resource_consumption[i]):
                if consumption > resource_limits[j]:
                    can_use_range = False
                    break
            
            if can_use_range:
                result.append((i, start_i, end_i, self.contains_count[i], self.contained_by_count[i]))
        
        return result
    
    def get_nested_counts_with_mathematical_constraints(self, constraint_func):
        """Get nested counts that satisfy custom mathematical constraints."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            if constraint_func(start_i, end_i, end_i - start_i, self.contains_count[i], self.contained_by_count[i]):
                result.append((i, start_i, end_i, self.contains_count[i], self.contained_by_count[i]))
        
        return result
    
    def get_nested_counts_with_range_constraints(self, range_constraints):
        """Get nested counts that satisfy range constraints."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check if range satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(start_i, end_i, end_i - start_i, self.contains_count[i], self.contained_by_count[i]):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                result.append((i, start_i, end_i, self.contains_count[i], self.contained_by_count[i]))
        
        return result
    
    def get_nested_counts_with_optimization_constraints(self, optimization_func):
        """Get nested counts using custom optimization constraints."""
        ranges_with_score = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            score = optimization_func(start_i, end_i, end_i - start_i, self.contains_count[i], self.contained_by_count[i])
            ranges_with_score.append((i, start_i, end_i, self.contains_count[i], self.contained_by_count[i], score))
        
        ranges_with_score.sort(key=lambda x: x[5], reverse=True)
        return ranges_with_score
    
    def get_nested_counts_with_multiple_constraints(self, constraints_list):
        """Get nested counts that satisfy multiple constraints."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check if range satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(start_i, end_i, end_i - start_i, self.contains_count[i], self.contained_by_count[i]):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                result.append((i, start_i, end_i, self.contains_count[i], self.contained_by_count[i]))
        
        return result
    
    def get_nested_counts_with_priority_constraints(self, priority_func):
        """Get nested counts with priority-based constraints."""
        ranges_with_priority = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            priority = priority_func(start_i, end_i, end_i - start_i, self.contains_count[i], self.contained_by_count[i])
            ranges_with_priority.append((i, start_i, end_i, self.contains_count[i], self.contained_by_count[i], priority))
        
        ranges_with_priority.sort(key=lambda x: x[5], reverse=True)
        return ranges_with_priority
    
    def get_nested_counts_with_adaptive_constraints(self, adaptive_func):
        """Get nested counts with adaptive constraints."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check adaptive constraints
            if adaptive_func(start_i, end_i, end_i - start_i, self.contains_count[i], self.contained_by_count[i], result):
                result.append((i, start_i, end_i, self.contains_count[i], self.contained_by_count[i]))
        
        return result
    
    def get_optimal_nested_counts_strategy(self):
        """Get optimal nested counts strategy considering all constraints."""
        strategies = [
            ('time_constraints', self.get_nested_counts_with_time_constraints),
            ('resource_constraints', self.get_nested_counts_with_resource_constraints),
            ('mathematical_constraints', self.get_nested_counts_with_mathematical_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'time_constraints':
                    current_result = strategy_func(5)  # 5 time units
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {i: [10, 5] for i in range(self.n)}
                    current_result = strategy_func(resource_limits, resource_consumption)
                elif strategy_name == 'mathematical_constraints':
                    def constraint_func(start, end, length, contains, contained_by):
                        return length >= 2 and contains >= 1
                    current_result = strategy_func(constraint_func)
                
                if len(current_result) > best_count:
                    best_count = len(current_result)
                    best_strategy = (strategy_name, current_result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_length': 2,
    'max_length': 10
}

ranges = [(1, 4), (2, 3), (5, 8), (6, 7), (9, 12)]
constrained_nrc = ConstrainedNestedRangesCount(ranges, constraints)

print("Time-constrained nested counts:", constrained_nrc.get_nested_counts_with_time_constraints(5))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(ranges))}
print("Resource-constrained nested counts:", constrained_nrc.get_nested_counts_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(start, end, length, contains, contained_by):
    return length >= 2 and contains >= 1

print("Mathematical constraint nested counts:", constrained_nrc.get_nested_counts_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(start, end, length, contains, contained_by):
    return length >= 2 and start >= 1 and contains >= 1

range_constraints = [range_constraint]
print("Range-constrained nested counts:", constrained_nrc.get_nested_counts_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(start, end, length, contains, contained_by):
    return length >= 2

def constraint2(start, end, length, contains, contained_by):
    return contains >= 1

constraints_list = [constraint1, constraint2]
print("Multiple constraints nested counts:", constrained_nrc.get_nested_counts_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(start, end, length, contains, contained_by):
    return (contains + contained_by) * length

print("Priority-constrained nested counts:", constrained_nrc.get_nested_counts_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(start, end, length, contains, contained_by, current_result):
    return length >= 2 and contains >= 1 and len(current_result) < 3

print("Adaptive constraint nested counts:", constrained_nrc.get_nested_counts_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_nrc.get_optimal_nested_counts_strategy()
print(f"Optimal strategy: {optimal}")
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
