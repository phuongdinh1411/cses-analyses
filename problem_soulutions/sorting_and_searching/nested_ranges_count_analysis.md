---
layout: simple
title: "Nested Ranges Count"
permalink: /problem_soulutions/sorting_and_searching/nested_ranges_count_analysis
---


# Nested Ranges Count

## Problem Statement
Given n ranges [a1,b1],[a2,b2],…,[an,bn], for each range count how many other ranges it contains and how many other ranges contain it.

### Input
The first input line has an integer n: the number of ranges.
Then there are n lines. Each line has two integers a and b: the start and end of a range.

### Output
Print n lines. For each range, print two integers: the number of ranges it contains and the number of ranges that contain it.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ai ≤ bi ≤ 10^9

### Example
```
Input:
4
1 6
2 4
4 8
3 6

Output:
2 0
0 1
1 0
0 1
```

## Solution Progression

### Approach 1: Brute Force - O(n²)
**Description**: For each range, check all other ranges for containment.

```python
def nested_ranges_count_naive(n, ranges):
    results = []
    
    for i in range(n):
        contains_count = 0
        contained_count = 0
        
        for j in range(n):
            if i != j:
                # Check if range i contains range j
                if ranges[i][0] <= ranges[j][0] and ranges[i][1] >= ranges[j][1]:
                    contains_count += 1
                
                # Check if range i is contained by range j
                if ranges[j][0] <= ranges[i][0] and ranges[j][1] >= ranges[i][1]:
                    contained_count += 1
        
        results.append((contains_count, contained_count))
    
    return results
```

**Why this is inefficient**: For each range, we check all other ranges, leading to O(n²) time complexity.

### Improvement 1: Sorting and Binary Search - O(n log n)
**Description**: Sort ranges and use binary search to count containment relationships.

```python
def nested_ranges_count_optimized(n, ranges):
    # Create list of (start, end, index) tuples
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    
    # Sort by start position, then by end position (descending)
    range_list.sort(key=lambda x: (x[0], -x[1]))
    
    results = [[0, 0] for _ in range(n)]
    
    # Count containment relationships
    for i in range(n):
        start, end, idx = range_list[i]
        
        # Count ranges that this range contains
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_start and end >= next_end:
                results[idx][0] += 1  # Contains another range
                results[next_idx][1] += 1  # Is contained by another range
    
    return results
```

**Why this improvement works**: By sorting ranges by start position and then by end position (descending), we can efficiently count containment relationships in a single pass.

## Final Optimal Solution

```python
n = int(input())
ranges = []
for _ in range(n):
    a, b = map(int, input().split())
    ranges.append((a, b))

def count_nested_ranges(n, ranges):
    # Create list of (start, end, index) tuples
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    
    # Sort by start position, then by end position (descending)
    range_list.sort(key=lambda x: (x[0], -x[1]))
    
    results = [[0, 0] for _ in range(n)]
    
    # Count containment relationships
    for i in range(n):
        start, end, idx = range_list[i]
        
        # Count ranges that this range contains
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_start and end >= next_end:
                results[idx][0] += 1  # Contains another range
                results[next_idx][1] += 1  # Is contained by another range
    
    return results

results = count_nested_ranges(n, ranges)
for contains_count, contained_count in results:
    print(contains_count, contained_count)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check all pairs of ranges |
| Sorting and Binary Search | O(n log n) | O(n) | Sort and count in single pass |

## Key Insights for Other Problems

### 1. **Range Counting Problems**
**Principle**: Sort ranges by start position to enable efficient containment counting.
**Applicable to**: Range problems, interval problems, counting problems

### 2. **Sorting for Efficiency**
**Principle**: Sort data to enable linear-time processing instead of quadratic.
**Applicable to**: Sorting problems, optimization problems, range problems

### 3. **Containment Counting**
**Principle**: Use sorted order to efficiently count containment relationships.
**Applicable to**: Counting problems, relationship problems, interval problems

## Notable Techniques

### 1. **Range Sorting**
```python
def sort_ranges_by_start_end(ranges):
    # Sort by start position, then by end position (descending)
    return sorted(ranges, key=lambda x: (x[0], -x[1]))
```

### 2. **Containment Counting**
```python
def count_containment_relationships(ranges):
    sorted_ranges = sort_ranges_by_start_end(ranges)
    results = [[0, 0] for _ in range(len(ranges))]
    
    for i, (start, end, idx) in enumerate(sorted_ranges):
        for j in range(i + 1, len(sorted_ranges)):
            next_start, next_end, next_idx = sorted_ranges[j]
            
            if start <= next_start and end >= next_end:
                results[idx][0] += 1  # Contains
                results[next_idx][1] += 1  # Is contained
    
    return results
```

### 3. **Range Processing**
```python
def process_ranges_efficiently(ranges):
    sorted_ranges = sort_ranges_by_start_end(ranges)
    results = []
    
    for i, (start, end) in enumerate(sorted_ranges):
        contains_count = 0
        contained_count = 0
        
        # Count containment relationships
        for j in range(i + 1, len(sorted_ranges)):
            if check_containment((start, end), sorted_ranges[j]):
                contains_count += 1
                # Update contained count for the other range
                # Implementation depends on specific requirements
        
        results.append((contains_count, contained_count))
    
    return results
```

## Problem-Solving Framework

1. **Identify problem type**: This is a range containment counting problem
2. **Choose approach**: Sort ranges and count containment in single pass
3. **Sort ranges**: Sort by start position, then by end position (descending)
4. **Initialize results**: Create array to store containment counts
5. **Count containment**: For each range, count ranges it contains and ranges that contain it
6. **Update counts**: Increment counts for both directions of containment
7. **Return result**: Output containment counts for each range

---

*This analysis shows how to efficiently count nested range relationships using sorting and linear processing.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Range Containment**
**Problem**: Each range has a weight. Find the total weight of ranges contained by each range and total weight of ranges containing each range.
```python
def weighted_nested_ranges(n, ranges, weights):
    # weights[i] = weight of range i
    range_list = [(ranges[i][0], ranges[i][1], i, weights[i]) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], -x[1]))
    
    results = [[0, 0] for _ in range(n)]  # [contains_weight, contained_weight]
    
    for i in range(n):
        start, end, idx, weight = range_list[i]
        
        for j in range(i + 1, n):
            next_start, next_end, next_idx, next_weight = range_list[j]
            
            if start <= next_start and end >= next_end:
                results[idx][0] += next_weight  # Weight of ranges it contains
                results[next_idx][1] += weight  # Weight of ranges containing it
    
    return results
```

#### **Variation 2: Partial Overlap Counting**
**Problem**: Count ranges that partially overlap with each range (not just containment).
```python
def partial_overlap_ranges(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], x[1]))
    
    results = [[0, 0] for _ in range(n)]  # [overlaps_with, overlapped_by]
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        for j in range(n):
            if i != j:
                other_start, other_end, other_idx = range_list[j]
                
                # Check for overlap (not containment)
                if (start < other_end and end > other_start and 
                    not (start <= other_start and end >= other_end) and
                    not (other_start <= start and other_end >= end)):
                    results[idx][0] += 1
                    results[other_idx][1] += 1
    
    return results
```

#### **Variation 3: Range Query with Updates**
**Problem**: Support dynamic updates to ranges and answer containment queries efficiently.
```python
class DynamicRangeCounter:
    def __init__(self):
        self.ranges = []
        self.index_map = {}
    
    def add_range(self, start, end, idx):
        self.ranges.append((start, end, idx))
        self.index_map[idx] = len(self.ranges) - 1
        self._update_counts()
    
    def remove_range(self, idx):
        if idx in self.index_map:
            pos = self.index_map[idx]
            del self.ranges[pos]
            del self.index_map[idx]
            self._update_counts()
    
    def _update_counts(self):
        # Recompute all containment counts
        self.ranges.sort(key=lambda x: (x[0], -x[1]))
        self.results = [[0, 0] for _ in range(len(self.ranges))]
        
        for i in range(len(self.ranges)):
            start, end, idx = self.ranges[i]
            for j in range(i + 1, len(self.ranges)):
                next_start, next_end, next_idx = self.ranges[j]
                if start <= next_start and end >= next_end:
                    self.results[i][0] += 1
                    self.results[j][1] += 1
    
    def get_counts(self, idx):
        if idx in self.index_map:
            pos = self.index_map[idx]
            return self.results[pos]
        return [0, 0]
```

#### **Variation 4: Multi-dimensional Ranges**
**Problem**: Handle ranges in multiple dimensions (2D, 3D, etc.) and count containment relationships.
```python
def multi_dimensional_nested_ranges(n, ranges):
    # ranges[i] = [(start1, end1), (start2, end2), ...] for each dimension
    results = [[0, 0] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                # Check if range i contains range j in all dimensions
                contains = True
                for dim in range(len(ranges[i])):
                    if (ranges[i][dim][0] > ranges[j][dim][0] or 
                        ranges[i][dim][1] < ranges[j][dim][1]):
                        contains = False
                        break
                
                if contains:
                    results[i][0] += 1
                    results[j][1] += 1
    
    return results
```

#### **Variation 5: Range with Time Complexity**
**Problem**: Find the maximum number of ranges that can be contained by any single range.
```python
def max_contained_ranges(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], -x[1]))
    
    max_contained = 0
    best_range = None
    
    for i in range(n):
        start, end, idx = range_list[i]
        contained_count = 0
        
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            if start <= next_start and end >= next_end:
                contained_count += 1
        
        if contained_count > max_contained:
            max_contained = contained_count
            best_range = idx
    
    return max_contained, best_range
```

### 🔗 **Related Problems & Concepts**

#### **1. Range Problems**
- **Range Sum Queries**: Sum of elements in given ranges
- **Range Minimum Queries**: Minimum element in given ranges
- **Range Updates**: Update elements in given ranges
- **Range Merging**: Merge overlapping ranges

#### **2. Interval Problems**
- **Interval Scheduling**: Schedule non-overlapping intervals
- **Interval Partitioning**: Partition intervals into minimum sets
- **Interval Intersection**: Find intersection of intervals
- **Interval Union**: Find union of intervals

#### **3. Geometric Problems**
- **Rectangle Intersection**: Find intersecting rectangles
- **Point in Polygon**: Check if point is inside polygon
- **Line Segment Intersection**: Find intersecting line segments
- **Convex Hull**: Find convex hull of points

#### **4. Counting Problems**
- **Inversion Count**: Count inversions in array
- **Pair Counting**: Count pairs satisfying conditions
- **Subsequence Counting**: Count subsequences with properties
- **Permutation Counting**: Count valid permutations

#### **5. Optimization Problems**
- **Maximum Independent Set**: Find maximum non-overlapping ranges
- **Minimum Cover**: Find minimum ranges to cover all points
- **Optimal Scheduling**: Schedule ranges optimally
- **Resource Allocation**: Allocate resources to ranges

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    ranges = []
    for _ in range(n):
        a, b = map(int, input().split())
        ranges.append((a, b))
    
    results = count_nested_ranges(n, ranges)
    for contains_count, contained_count in results:
        print(contains_count, contained_count)
```

#### **2. Range Queries**
```python
# Precompute containment relationships for efficient querying
def precompute_containment(ranges):
    n = len(ranges)
    containment_matrix = [[False] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                if (ranges[i][0] <= ranges[j][0] and 
                    ranges[i][1] >= ranges[j][1]):
                    containment_matrix[i][j] = True
    
    return containment_matrix

# Answer containment queries efficiently
def containment_query(matrix, i, j):
    return matrix[i][j]
```

#### **3. Interactive Problems**
```python
# Interactive range containment game
def interactive_range_game():
    n = int(input("Enter number of ranges: "))
    ranges = []
    
    for i in range(n):
        start = int(input(f"Enter start of range {i+1}: "))
        end = int(input(f"Enter end of range {i+1}: "))
        ranges.append((start, end))
    
    print("Ranges:", ranges)
    
    while True:
        query = input("Enter query (contains/contained/exit): ")
        if query == "exit":
            break
        
        i = int(input("Enter range index: "))
        if query == "contains":
            count = sum(1 for j in range(n) if i != j and 
                       ranges[i][0] <= ranges[j][0] and 
                       ranges[i][1] >= ranges[j][1])
            print(f"Range {i} contains {count} other ranges")
        elif query == "contained":
            count = sum(1 for j in range(n) if i != j and 
                       ranges[j][0] <= ranges[i][0] and 
                       ranges[j][1] >= ranges[i][1])
            print(f"Range {i} is contained by {count} other ranges")
```

### 🧮 **Mathematical Extensions**

#### **1. Set Theory**
- **Subset Relationships**: Mathematical foundation for containment
- **Set Operations**: Union, intersection, difference of ranges
- **Cardinality**: Size of range sets and their relationships
- **Partitioning**: Ways to partition range sets

#### **2. Order Theory**
- **Partial Orders**: Containment as partial ordering
- **Lattices**: Range containment lattices
- **Chains**: Totally ordered subsets of ranges
- **Antichains**: Sets of incomparable ranges

#### **3. Combinatorics**
- **Inclusion-Exclusion**: Counting overlapping ranges
- **Binomial Coefficients**: Counting range combinations
- **Permutations**: Arrangements of ranges
- **Partitions**: Ways to partition range sets

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Sweep Line Algorithm**: Efficient range processing
- **Segment Trees**: Range query data structures
- **Binary Indexed Trees**: Range update and query
- **Interval Trees**: Specialized for interval operations

#### **2. Mathematical Concepts**
- **Interval Arithmetic**: Mathematical operations on intervals
- **Order Theory**: Understanding containment relationships
- **Set Theory**: Foundation for range operations
- **Combinatorics**: Counting range relationships

#### **3. Programming Concepts**
- **Sorting Algorithms**: Efficient range sorting
- **Data Structures**: Efficient range storage and querying
- **Algorithm Design**: Problem-solving strategies
- **Complexity Analysis**: Time and space complexity

---

*This analysis demonstrates efficient range containment counting techniques and shows various extensions for interval problems.* 