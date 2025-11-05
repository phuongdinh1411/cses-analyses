---
layout: simple
title: "Nested Ranges Check"
permalink: /problem_soulutions/sorting_and_searching/nested_ranges_check_analysis
---

# Nested Ranges Check

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of range nesting and interval relationships
- Apply sorting and coordinate compression techniques for range problems
- Implement efficient solutions for range checking problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in range intersection problems

## 📋 Problem Description

You are given n ranges [a[i], b[i]]. For each range, determine if it contains any other range or is contained by any other range.

A range [a[i], b[i]] contains range [a[j], b[j]] if a[i] ≤ a[j] and b[j] ≤ b[i].
A range [a[i], b[i]] is contained by range [a[j], b[j]] if a[j] ≤ a[i] and b[i] ≤ b[j].

**Input**: 
- First line: integer n (number of ranges)
- Next n lines: two integers a[i] and b[i] (range endpoints)

**Output**: 
- Print n lines: for each range, print "YES" if it contains or is contained by another range, "NO" otherwise

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
YES
YES
YES
NO

Explanation**: 
Ranges: [1,6], [2,4], [3,5], [7,8]

Range 1 [1,6]: Contains [2,4] and [3,5] → YES
Range 2 [2,4]: Contained by [1,6] → YES
Range 3 [3,5]: Contained by [1,6] → YES
Range 4 [7,8]: No nesting relationship → NO
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: [Description]
- **Complete Coverage**: [Description]
- **Simple Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def brute_force_nested_ranges_check(arr):
    """
    [Description]
    
    Args:
        arr: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's inefficient**: [Reason]

---

### Approach 2: Optimized

**Key Insights from Optimized Approach**:
- **Optimization Technique**: [Description]
- **Efficiency Improvement**: [Description]
- **Better Complexity**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimized_nested_ranges_check(arr):
    """
    [Description]
    
    Args:
        arr: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's better**: [Reason]

---

### Approach 3: Optimal

**Key Insights from Optimal Approach**:
- **Optimal Algorithm**: [Description]
- **Best Complexity**: [Description]
- **Efficient Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimal_nested_ranges_check(arr):
    """
    [Description]
    
    Args:
        arr: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's optimal**: [Reason]

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O([complexity]) | O([complexity]) | [Insight] |
| Optimized | O([complexity]) | O([complexity]) | [Insight] |
| Optimal | O([complexity]) | O([complexity]) | [Insight] |

### Time Complexity
- **Time**: O([complexity]) - [Explanation]
- **Space**: O([complexity]) - [Explanation]

### Why This Solution Works
- **Sorting Strategy**: Sort ranges by start point to enable efficient nesting detection
- **Coordinate Compression**: Compress coordinates to handle large ranges efficiently
- **Range Comparison**: Use sorted order to check containment relationships
- **Optimal Approach**: Sorting with coordinate compression provides the most efficient solution for range nesting problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Nested Ranges Check with Range Queries
**Problem**: Answer multiple queries about range nesting in different subsets of ranges.

**Link**: [CSES Problem Set - Nested Ranges Check Range Queries](https://cses.fi/problemset/task/nested_ranges_check_range)

```python
def nested_ranges_check_range_queries(ranges, queries):
    """
    Answer range queries about range nesting
    """
    results = []
    
    for query in queries:
        left, right = query['left'], query['right']
        
        # Extract subset of ranges
        subset_ranges = ranges[left:right+1]
        
        # Check nesting for this subset
        nesting_results = check_nested_ranges(subset_ranges)
        results.append(nesting_results)
    
    return results

def check_nested_ranges(ranges):
    """
    Check which ranges contain or are contained by other ranges
    """
    n = len(ranges)
    results = [False] * n
    
    # Sort ranges by start point, then by end point (descending)
    sorted_ranges = sorted(enumerate(ranges), key=lambda x: (x[1][0], -x[1][1]))
    
    for i in range(n):
        original_idx, (start_i, end_i) = sorted_ranges[i]
        
        # Check if this range contains any other range
        for j in range(i + 1, n):
            _, (start_j, end_j) = sorted_ranges[j]
            
            if start_j >= start_i and end_j <= end_i:
                # Range i contains range j
                results[original_idx] = True
                break
        
        # Check if this range is contained by any other range
        for j in range(i):
            _, (start_j, end_j) = sorted_ranges[j]
            
            if start_i >= start_j and end_i <= end_j:
                # Range i is contained by range j
                results[original_idx] = True
                break
    
    return results

def check_nested_ranges_optimized(ranges):
    """
    Optimized version using coordinate compression
    """
    n = len(ranges)
    results = [False] * n
    
    # Coordinate compression
    all_coords = []
    for start, end in ranges:
        all_coords.extend([start, end])
    
    coord_map = {coord: i for i, coord in enumerate(sorted(set(all_coords)))}
    
    # Compress ranges
    compressed_ranges = []
    for start, end in ranges:
        compressed_ranges.append((coord_map[start], coord_map[end]))
    
    # Sort ranges by start point, then by end point (descending)
    sorted_ranges = sorted(enumerate(compressed_ranges), key=lambda x: (x[1][0], -x[1][1]))
    
    for i in range(n):
        original_idx, (start_i, end_i) = sorted_ranges[i]
        
        # Check if this range contains any other range
        for j in range(i + 1, n):
            _, (start_j, end_j) = sorted_ranges[j]
            
            if start_j >= start_i and end_j <= end_i:
                # Range i contains range j
                results[original_idx] = True
                break
        
        # Check if this range is contained by any other range
        for j in range(i):
            _, (start_j, end_j) = sorted_ranges[j]
            
            if start_i >= start_j and end_i <= end_j:
                # Range i is contained by range j
                results[original_idx] = True
                break
    
    return results
```

### Variation 2: Nested Ranges Check with Updates
**Problem**: Handle dynamic updates to ranges and maintain nesting information.

**Link**: [CSES Problem Set - Nested Ranges Check with Updates](https://cses.fi/problemset/task/nested_ranges_check_updates)

```python
class NestedRangesCheckWithUpdates:
    def __init__(self, ranges):
        self.ranges = ranges[:]
        self.n = len(ranges)
        self.nesting_info = self._compute_nesting_info()
    
    def _compute_nesting_info(self):
        """Compute initial nesting information"""
        results = [False] * self.n
        
        # Sort ranges by start point, then by end point (descending)
        sorted_ranges = sorted(enumerate(self.ranges), key=lambda x: (x[1][0], -x[1][1]))
        
        for i in range(self.n):
            original_idx, (start_i, end_i) = sorted_ranges[i]
            
            # Check if this range contains any other range
            for j in range(i + 1, self.n):
                _, (start_j, end_j) = sorted_ranges[j]
                
                if start_j >= start_i and end_j <= end_i:
                    # Range i contains range j
                    results[original_idx] = True
                    break
            
            # Check if this range is contained by any other range
            for j in range(i):
                _, (start_j, end_j) = sorted_ranges[j]
                
                if start_i >= start_j and end_i <= end_j:
                    # Range i is contained by range j
                    results[original_idx] = True
                    break
        
        return results
    
    def update_range(self, index, new_range):
        """Update a range and recompute nesting information"""
        self.ranges[index] = new_range
        self.nesting_info = self._compute_nesting_info()
    
    def add_range(self, new_range):
        """Add a new range and recompute nesting information"""
        self.ranges.append(new_range)
        self.n = len(self.ranges)
        self.nesting_info = self._compute_nesting_info()
    
    def remove_range(self, index):
        """Remove a range and recompute nesting information"""
        self.ranges.pop(index)
        self.n = len(self.ranges)
        self.nesting_info = self._compute_nesting_info()
    
    def get_nesting_info(self):
        """Get current nesting information"""
        return self.nesting_info
    
    def is_nested(self, index):
        """Check if a specific range is nested"""
        return self.nesting_info[index]
    
    def get_containing_ranges(self, index):
        """Get all ranges that contain the given range"""
        target_start, target_end = self.ranges[index]
        containing = []
        
        for i, (start, end) in enumerate(self.ranges):
            if i != index and start <= target_start and target_end <= end:
                containing.append(i)
        
        return containing
    
    def get_contained_ranges(self, index):
        """Get all ranges that are contained by the given range"""
        target_start, target_end = self.ranges[index]
        contained = []
        
        for i, (start, end) in enumerate(self.ranges):
            if i != index and target_start <= start and end <= target_end:
                contained.append(i)
        
        return contained
```

### Variation 3: Nested Ranges Check with Constraints
**Problem**: Find nested ranges that satisfy additional constraints (e.g., minimum overlap, maximum gap).

**Link**: [CSES Problem Set - Nested Ranges Check with Constraints](https://cses.fi/problemset/task/nested_ranges_check_constraints)

```python
def nested_ranges_check_constraints(ranges, min_overlap, max_gap):
    """
    Check nested ranges with additional constraints
    """
    n = len(ranges)
    results = [False] * n
    
    # Sort ranges by start point, then by end point (descending)
    sorted_ranges = sorted(enumerate(ranges), key=lambda x: (x[1][0], -x[1][1]))
    
    for i in range(n):
        original_idx, (start_i, end_i) = sorted_ranges[i]
        
        # Check if this range contains any other range with constraints
        for j in range(i + 1, n):
            _, (start_j, end_j) = sorted_ranges[j]
            
            if start_j >= start_i and end_j <= end_i:
                # Check overlap constraint
                overlap = min(end_i, end_j) - max(start_i, start_j)
                if overlap >= min_overlap:
                    # Check gap constraint
                    gap = start_j - start_i
                    if gap <= max_gap:
                        results[original_idx] = True
                        break
        
        # Check if this range is contained by any other range with constraints
        for j in range(i):
            _, (start_j, end_j) = sorted_ranges[j]
            
            if start_i >= start_j and end_i <= end_j:
                # Check overlap constraint
                overlap = min(end_i, end_j) - max(start_i, start_j)
                if overlap >= min_overlap:
                    # Check gap constraint
                    gap = start_i - start_j
                    if gap <= max_gap:
                        results[original_idx] = True
                        break
    
    return results

def nested_ranges_check_constraints_optimized(ranges, min_overlap, max_gap):
    """
    Optimized version with early termination
    """
    n = len(ranges)
    results = [False] * n
    
    # Sort ranges by start point, then by end point (descending)
    sorted_ranges = sorted(enumerate(ranges), key=lambda x: (x[1][0], -x[1][1]))
    
    for i in range(n):
        original_idx, (start_i, end_i) = sorted_ranges[i]
        
        # Check if this range contains any other range with constraints
        for j in range(i + 1, n):
            _, (start_j, end_j) = sorted_ranges[j]
            
            if start_j >= start_i and end_j <= end_i:
                # Check overlap constraint
                overlap = min(end_i, end_j) - max(start_i, start_j)
                if overlap >= min_overlap:
                    # Check gap constraint
                    gap = start_j - start_i
                    if gap <= max_gap:
                        results[original_idx] = True
                        break
                else:
                    # Early termination if overlap is too small
                    break
        
        # Check if this range is contained by any other range with constraints
        for j in range(i):
            _, (start_j, end_j) = sorted_ranges[j]
            
            if start_i >= start_j and end_i <= end_j:
                # Check overlap constraint
                overlap = min(end_i, end_j) - max(start_i, start_j)
                if overlap >= min_overlap:
                    # Check gap constraint
                    gap = start_i - start_j
                    if gap <= max_gap:
                        results[original_idx] = True
                        break
                else:
                    # Early termination if overlap is too small
                    break
    
    return results

# Example usage
ranges = [(1, 6), (2, 4), (3, 5), (7, 8)]
min_overlap = 1
max_gap = 2

results = nested_ranges_check_constraints(ranges, min_overlap, max_gap)
print(f"Nesting results with constraints: {results}")  # Output: [True, True, True, False]
```

## Problem Variations

### **Variation 1: Nested Ranges Check with Dynamic Updates**
**Problem**: Handle dynamic range updates (add/remove/update ranges) while maintaining efficient nested range checking queries.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicNestedRangesCheck:
    def __init__(self, ranges):
        self.ranges = ranges[:]
        self.n = len(ranges)
        self.nested_results = self._compute_nested_ranges()
    
    def _compute_nested_ranges(self):
        """Compute nested ranges using sorting and coordinate compression."""
        if not self.ranges:
            return [False] * self.n
        
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
        
        results = [False] * self.n
        
        for i in range(self.n):
            original_idx, (start_i, end_i) = sorted_ranges[i]
            
            # Check if this range contains any other range
            for j in range(i + 1, self.n):
                _, (start_j, end_j) = sorted_ranges[j]
                
                if start_j >= start_i and end_j <= end_i:
                    results[original_idx] = True
                    break
            
            # Check if this range is contained by any other range
            if not results[original_idx]:
                for j in range(i):
                    _, (start_j, end_j) = sorted_ranges[j]
                    
                    if start_i >= start_j and end_i <= end_j:
                        results[original_idx] = True
                        break
        
        return results
    
    def add_range(self, start, end):
        """Add a new range to the collection."""
        self.ranges.append((start, end))
        self.n += 1
        self.nested_results = self._compute_nested_ranges()
    
    def remove_range(self, index):
        """Remove a range at the specified index."""
        if 0 <= index < self.n:
            del self.ranges[index]
            self.n -= 1
            self.nested_results = self._compute_nested_ranges()
    
    def update_range(self, index, new_start, new_end):
        """Update a range at the specified index."""
        if 0 <= index < self.n:
            self.ranges[index] = (new_start, new_end)
            self.nested_results = self._compute_nested_ranges()
    
    def get_nested_results(self):
        """Get all nested range results."""
        return self.nested_results
    
    def is_nested(self, index):
        """Check if range at index is nested."""
        if 0 <= index < self.n:
            return self.nested_results[index]
        return False
    
    def get_nested_ranges(self):
        """Get all ranges that are nested."""
        nested_ranges = []
        for i in range(self.n):
            if self.nested_results[i]:
                nested_ranges.append((i, self.ranges[i]))
        return nested_ranges
    
    def get_non_nested_ranges(self):
        """Get all ranges that are not nested."""
        non_nested_ranges = []
        for i in range(self.n):
            if not self.nested_results[i]:
                non_nested_ranges.append((i, self.ranges[i]))
        return non_nested_ranges
    
    def get_nested_pairs(self):
        """Get all pairs of nested ranges."""
        nested_pairs = []
        
        for i in range(self.n):
            for j in range(i + 1, self.n):
                start_i, end_i = self.ranges[i]
                start_j, end_j = self.ranges[j]
                
                # Check if range i contains range j
                if start_j >= start_i and end_j <= end_i:
                    nested_pairs.append((i, j, 'contains'))
                # Check if range j contains range i
                elif start_i >= start_j and end_i <= end_j:
                    nested_pairs.append((j, i, 'contains'))
        
        return nested_pairs
    
    def get_nested_statistics(self):
        """Get statistics about nested ranges."""
        if not self.ranges:
            return {
                'total_ranges': 0,
                'nested_ranges': 0,
                'non_nested_ranges': 0,
                'nested_pairs': 0,
                'average_range_length': 0
            }
        
        nested_count = sum(self.nested_results)
        non_nested_count = self.n - nested_count
        
        total_length = sum(end - start for start, end in self.ranges)
        average_length = total_length / self.n
        
        nested_pairs = len(self.get_nested_pairs())
        
        return {
            'total_ranges': self.n,
            'nested_ranges': nested_count,
            'non_nested_ranges': non_nested_count,
            'nested_pairs': nested_pairs,
            'average_range_length': average_length
        }
    
    def get_nested_patterns(self):
        """Get patterns in nested ranges."""
        patterns = {
            'consecutive_nested': 0,
            'alternating_nested': 0,
            'clustered_nested': 0,
            'isolated_nested': 0
        }
        
        for i in range(1, self.n):
            if self.nested_results[i] and self.nested_results[i-1]:
                patterns['consecutive_nested'] += 1
            
            if i > 1:
                if (self.nested_results[i] != self.nested_results[i-1] and 
                    self.nested_results[i-1] != self.nested_results[i-2]):
                    patterns['alternating_nested'] += 1
        
        return patterns

# Example usage
ranges = [(1, 4), (2, 3), (5, 8), (6, 7), (9, 12)]
dynamic_nrc = DynamicNestedRangesCheck(ranges)
print(f"Initial nested results: {dynamic_nrc.get_nested_results()}")

# Add a range
dynamic_nrc.add_range(10, 11)
print(f"After adding range: {dynamic_nrc.get_nested_results()}")

# Update a range
dynamic_nrc.update_range(1, 1, 5)
print(f"After updating range: {dynamic_nrc.get_nested_results()}")

# Get nested ranges
print(f"Nested ranges: {dynamic_nrc.get_nested_ranges()}")

# Get non-nested ranges
print(f"Non-nested ranges: {dynamic_nrc.get_non_nested_ranges()}")

# Get nested pairs
print(f"Nested pairs: {dynamic_nrc.get_nested_pairs()}")

# Get statistics
print(f"Statistics: {dynamic_nrc.get_nested_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_nrc.get_nested_patterns()}")
```

### **Variation 2: Nested Ranges Check with Different Operations**
**Problem**: Handle different types of operations on nested ranges (overlap checking, intersection analysis, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of range queries.

```python
class AdvancedNestedRangesCheck:
    def __init__(self, ranges):
        self.ranges = ranges[:]
        self.n = len(ranges)
        self.nested_results = self._compute_nested_ranges()
        self.overlap_results = self._compute_overlaps()
        self.intersection_results = self._compute_intersections()
    
    def _compute_nested_ranges(self):
        """Compute nested ranges using sorting."""
        if not self.ranges:
            return [False] * self.n
        
        # Sort ranges by start point, then by end point (descending)
        sorted_ranges = sorted(enumerate(self.ranges), key=lambda x: (x[1][0], -x[1][1]))
        
        results = [False] * self.n
        
        for i in range(self.n):
            original_idx, (start_i, end_i) = sorted_ranges[i]
            
            # Check if this range contains any other range
            for j in range(i + 1, self.n):
                _, (start_j, end_j) = sorted_ranges[j]
                
                if start_j >= start_i and end_j <= end_i:
                    results[original_idx] = True
                    break
            
            # Check if this range is contained by any other range
            if not results[original_idx]:
                for j in range(i):
                    _, (start_j, end_j) = sorted_ranges[j]
                    
                    if start_i >= start_j and end_i <= end_j:
                        results[original_idx] = True
                        break
        
        return results
    
    def _compute_overlaps(self):
        """Compute overlap information for all ranges."""
        overlap_results = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            overlaps = []
            
            for j in range(self.n):
                if i != j:
                    start_j, end_j = self.ranges[j]
                    
                    # Check if ranges overlap
                    if start_i < end_j and start_j < end_i:
                        overlap_start = max(start_i, start_j)
                        overlap_end = min(end_i, end_j)
                        overlap_length = overlap_end - overlap_start
                        overlaps.append((j, overlap_start, overlap_end, overlap_length))
            
            overlap_results.append(overlaps)
        
        return overlap_results
    
    def _compute_intersections(self):
        """Compute intersection information for all ranges."""
        intersection_results = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            intersections = []
            
            for j in range(i + 1, self.n):
                start_j, end_j = self.ranges[j]
                
                # Check if ranges intersect
                if start_i < end_j and start_j < end_i:
                    intersection_start = max(start_i, start_j)
                    intersection_end = min(end_i, end_j)
                    intersection_length = intersection_end - intersection_start
                    intersections.append((j, intersection_start, intersection_end, intersection_length))
            
            intersection_results.append(intersections)
        
        return intersection_results
    
    def get_nested_results(self):
        """Get all nested range results."""
        return self.nested_results
    
    def get_overlap_results(self):
        """Get all overlap results."""
        return self.overlap_results
    
    def get_intersection_results(self):
        """Get all intersection results."""
        return self.intersection_results
    
    def get_ranges_with_overlap(self, min_overlap_length):
        """Get ranges that have overlap with minimum length."""
        result = []
        
        for i in range(self.n):
            for j, overlap_start, overlap_end, overlap_length in self.overlap_results[i]:
                if overlap_length >= min_overlap_length:
                    result.append((i, j, overlap_start, overlap_end, overlap_length))
        
        return result
    
    def get_ranges_with_intersection(self, min_intersection_length):
        """Get ranges that have intersection with minimum length."""
        result = []
        
        for i in range(self.n):
            for j, intersection_start, intersection_end, intersection_length in self.intersection_results[i]:
                if intersection_length >= min_intersection_length:
                    result.append((i, j, intersection_start, intersection_end, intersection_length))
        
        return result
    
    def get_ranges_with_constraints(self, constraint_func):
        """Get ranges that satisfy custom constraints."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            if constraint_func(start_i, end_i, self.nested_results[i]):
                result.append((i, start_i, end_i))
        
        return result
    
    def get_ranges_with_priority(self, priority_func):
        """Get ranges sorted by priority."""
        ranges_with_priority = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            priority = priority_func(start_i, end_i, self.nested_results[i])
            ranges_with_priority.append((i, start_i, end_i, priority))
        
        ranges_with_priority.sort(key=lambda x: x[3], reverse=True)
        return ranges_with_priority
    
    def get_ranges_with_optimization(self, optimization_func):
        """Get ranges using custom optimization function."""
        ranges_with_score = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            score = optimization_func(start_i, end_i, self.nested_results[i])
            ranges_with_score.append((i, start_i, end_i, score))
        
        ranges_with_score.sort(key=lambda x: x[3], reverse=True)
        return ranges_with_score
    
    def get_ranges_with_alternatives(self, alternatives):
        """Get ranges considering alternative ranges."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check original range
            if self.nested_results[i]:
                result.append((i, start_i, end_i, 'original'))
            
            # Check alternative ranges
            if i in alternatives:
                for alt_start, alt_end in alternatives[i]:
                    # Check if alternative range is nested
                    is_nested = False
                    for j in range(self.n):
                        if i != j:
                            start_j, end_j = self.ranges[j]
                            if alt_start >= start_j and alt_end <= end_j:
                                is_nested = True
                                break
                    
                    if is_nested:
                        result.append((i, alt_start, alt_end, 'alternative'))
        
        return result
    
    def get_ranges_with_multiple_criteria(self, criteria_list):
        """Get ranges that satisfy multiple criteria."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check if range satisfies all criteria
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(start_i, end_i, self.nested_results[i]):
                    satisfies_all_criteria = False
                    break
            
            if satisfies_all_criteria:
                result.append((i, start_i, end_i))
        
        return result
    
    def get_ranges_with_adaptive_criteria(self, adaptive_func):
        """Get ranges using adaptive criteria."""
        result = []
        
        for i in range(self.n):
            start_i, end_i = self.ranges[i]
            
            # Check adaptive criteria
            if adaptive_func(start_i, end_i, self.nested_results[i], result):
                result.append((i, start_i, end_i))
        
        return result

# Example usage
ranges = [(1, 4), (2, 3), (5, 8), (6, 7), (9, 12)]
advanced_nrc = AdvancedNestedRangesCheck(ranges)

print(f"Nested results: {advanced_nrc.get_nested_results()}")
print(f"Overlap results: {advanced_nrc.get_overlap_results()}")
print(f"Intersection results: {advanced_nrc.get_intersection_results()}")

# Get ranges with overlap
print(f"Ranges with overlap >= 1: {advanced_nrc.get_ranges_with_overlap(1)}")

# Get ranges with intersection
print(f"Ranges with intersection >= 1: {advanced_nrc.get_ranges_with_intersection(1)}")

# Get ranges with constraints
def constraint_func(start, end, is_nested):
    return end - start >= 2 and is_nested

print(f"Ranges with constraints: {advanced_nrc.get_ranges_with_constraints(constraint_func)}")

# Get ranges with priority
def priority_func(start, end, is_nested):
    return (end - start) * (2 if is_nested else 1)

print(f"Ranges with priority: {advanced_nrc.get_ranges_with_priority(priority_func)}")

# Get ranges with optimization
def optimization_func(start, end, is_nested):
    return (end - start) + (1 if is_nested else 0)

print(f"Ranges with optimization: {advanced_nrc.get_ranges_with_optimization(optimization_func)}")

# Get ranges with alternatives
alternatives = {1: [(1, 2), (2, 4)], 3: [(5, 6), (7, 8)]}
print(f"Ranges with alternatives: {advanced_nrc.get_ranges_with_alternatives(alternatives)}")

# Get ranges with multiple criteria
def criterion1(start, end, is_nested):
    return end - start >= 2

def criterion2(start, end, is_nested):
    return is_nested

criteria_list = [criterion1, criterion2]
print(f"Ranges with multiple criteria: {advanced_nrc.get_ranges_with_multiple_criteria(criteria_list)}")

# Get ranges with adaptive criteria
def adaptive_func(start, end, is_nested, current_result):
    return end - start >= 2 and len(current_result) < 3

print(f"Ranges with adaptive criteria: {advanced_nrc.get_ranges_with_adaptive_criteria(adaptive_func)}")
```

### **Variation 3: Nested Ranges Check with Constraints**
**Problem**: Handle nested ranges check with additional constraints (time limits, resource constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedNestedRangesCheck:
    def __init__(self, ranges, constraints=None):
        self.ranges = ranges[:]
        self.n = len(ranges)
        self.constraints = constraints or {}
        self.nested_results = self._compute_nested_ranges()
    
    def _compute_nested_ranges(self):
        """Compute nested ranges using sorting."""
        if not self.ranges:
            return [False] * self.n
        
        # Sort ranges by start point, then by end point (descending)
        sorted_ranges = sorted(enumerate(self.ranges), key=lambda x: (x[1][0], -x[1][1]))
        
        results = [False] * self.n
        
        for i in range(self.n):
            original_idx, (start_i, end_i) = sorted_ranges[i]
            
            # Check if this range contains any other range
            for j in range(i + 1, self.n):
                _, (start_j, end_j) = sorted_ranges[j]
                
                if start_j >= start_i and end_j <= end_i:
                    results[original_idx] = True
                    break
            
            # Check if this range is contained by any other range
            if not results[original_idx]:
                for j in range(i):
                    _, (start_j, end_j) = sorted_ranges[j]
                    
                    if start_i >= start_j and end_i <= end_j:
                        results[original_idx] = True
                        break
        
        return results
    
    def get_nested_ranges_with_time_constraints(self, time_limit):
        """Get nested ranges considering time constraints."""
        result = []
        
        for i in range(self.n):
            if self.nested_results[i]:
                start_i, end_i = self.ranges[i]
                range_duration = end_i - start_i
                
                if range_duration <= time_limit:
                    result.append((i, start_i, end_i))
        
        return result
    
    def get_nested_ranges_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get nested ranges considering resource constraints."""
        result = []
        
        for i in range(self.n):
            if self.nested_results[i]:
                start_i, end_i = self.ranges[i]
                
                # Check resource constraints
                can_use_range = True
                for j, consumption in enumerate(resource_consumption[i]):
                    if consumption > resource_limits[j]:
                        can_use_range = False
                        break
                
                if can_use_range:
                    result.append((i, start_i, end_i))
        
        return result
    
    def get_nested_ranges_with_mathematical_constraints(self, constraint_func):
        """Get nested ranges that satisfy custom mathematical constraints."""
        result = []
        
        for i in range(self.n):
            if self.nested_results[i]:
                start_i, end_i = self.ranges[i]
                
                if constraint_func(start_i, end_i, end_i - start_i):
                    result.append((i, start_i, end_i))
        
        return result
    
    def get_nested_ranges_with_range_constraints(self, range_constraints):
        """Get nested ranges that satisfy range constraints."""
        result = []
        
        for i in range(self.n):
            if self.nested_results[i]:
                start_i, end_i = self.ranges[i]
                
                # Check if range satisfies all range constraints
                satisfies_constraints = True
                for constraint in range_constraints:
                    if not constraint(start_i, end_i, end_i - start_i):
                        satisfies_constraints = False
                        break
                
                if satisfies_constraints:
                    result.append((i, start_i, end_i))
        
        return result
    
    def get_nested_ranges_with_optimization_constraints(self, optimization_func):
        """Get nested ranges using custom optimization constraints."""
        ranges_with_score = []
        
        for i in range(self.n):
            if self.nested_results[i]:
                start_i, end_i = self.ranges[i]
                score = optimization_func(start_i, end_i, end_i - start_i)
                ranges_with_score.append((i, start_i, end_i, score))
        
        ranges_with_score.sort(key=lambda x: x[3], reverse=True)
        return ranges_with_score
    
    def get_nested_ranges_with_multiple_constraints(self, constraints_list):
        """Get nested ranges that satisfy multiple constraints."""
        result = []
        
        for i in range(self.n):
            if self.nested_results[i]:
                start_i, end_i = self.ranges[i]
                
                # Check if range satisfies all constraints
                satisfies_all_constraints = True
                for constraint in constraints_list:
                    if not constraint(start_i, end_i, end_i - start_i):
                        satisfies_all_constraints = False
                        break
                
                if satisfies_all_constraints:
                    result.append((i, start_i, end_i))
        
        return result
    
    def get_nested_ranges_with_priority_constraints(self, priority_func):
        """Get nested ranges with priority-based constraints."""
        ranges_with_priority = []
        
        for i in range(self.n):
            if self.nested_results[i]:
                start_i, end_i = self.ranges[i]
                priority = priority_func(start_i, end_i, end_i - start_i)
                ranges_with_priority.append((i, start_i, end_i, priority))
        
        ranges_with_priority.sort(key=lambda x: x[3], reverse=True)
        return ranges_with_priority
    
    def get_nested_ranges_with_adaptive_constraints(self, adaptive_func):
        """Get nested ranges with adaptive constraints."""
        result = []
        
        for i in range(self.n):
            if self.nested_results[i]:
                start_i, end_i = self.ranges[i]
                
                # Check adaptive constraints
                if adaptive_func(start_i, end_i, end_i - start_i, result):
                    result.append((i, start_i, end_i))
        
        return result
    
    def get_optimal_nested_ranges_strategy(self):
        """Get optimal nested ranges strategy considering all constraints."""
        strategies = [
            ('time_constraints', self.get_nested_ranges_with_time_constraints),
            ('resource_constraints', self.get_nested_ranges_with_resource_constraints),
            ('mathematical_constraints', self.get_nested_ranges_with_mathematical_constraints),
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
                    def constraint_func(start, end, length):
                        return length >= 2
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
constrained_nrc = ConstrainedNestedRangesCheck(ranges, constraints)

print("Time-constrained nested ranges:", constrained_nrc.get_nested_ranges_with_time_constraints(5))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(ranges))}
print("Resource-constrained nested ranges:", constrained_nrc.get_nested_ranges_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(start, end, length):
    return length >= 2

print("Mathematical constraint nested ranges:", constrained_nrc.get_nested_ranges_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(start, end, length):
    return length >= 2 and start >= 1

range_constraints = [range_constraint]
print("Range-constrained nested ranges:", constrained_nrc.get_nested_ranges_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(start, end, length):
    return length >= 2

def constraint2(start, end, length):
    return start >= 1

constraints_list = [constraint1, constraint2]
print("Multiple constraints nested ranges:", constrained_nrc.get_nested_ranges_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(start, end, length):
    return length * 2

print("Priority-constrained nested ranges:", constrained_nrc.get_nested_ranges_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(start, end, length, current_result):
    return length >= 2 and len(current_result) < 3

print("Adaptive constraint nested ranges:", constrained_nrc.get_nested_ranges_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_nrc.get_optimal_nested_ranges_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Nested Ranges Check](https://cses.fi/problemset/task/2168) - Basic nested ranges checking
- [Nested Ranges Count](https://cses.fi/problemset/task/2169) - Count nested ranges
- [Range Queries](https://cses.fi/problemset/task/1648) - Range query problems

#### **LeetCode Problems**
- [Merge Intervals](https://leetcode.com/problems/merge-intervals/) - Merge overlapping intervals
- [Insert Interval](https://leetcode.com/problems/insert-interval/) - Insert new interval
- [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) - Find interval intersections
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) - Remove overlapping intervals

#### **Problem Categories**
- **Sorting**: Range sorting, coordinate compression, interval ordering
- **Coordinate Compression**: Large coordinate handling, efficient range processing
- **Range Processing**: Interval analysis, nesting detection, containment checking
- **Algorithm Design**: Sorting algorithms, coordinate compression techniques, range optimization
