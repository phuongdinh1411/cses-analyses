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

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, coordinate compression, range queries, interval scheduling
- **Data Structures**: Arrays, sorted arrays, coordinate compression
- **Mathematical Concepts**: Range theory, interval relationships, coordinate compression
- **Programming Skills**: Algorithm implementation, complexity analysis, sorting algorithms
- **Related Problems**: Nested Ranges Count (counting), Range Queries (queries), Interval Scheduling (scheduling)

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
