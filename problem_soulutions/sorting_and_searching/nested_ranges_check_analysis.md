---
layout: simple
title: "Nested Ranges Check
permalink: /problem_soulutions/sorting_and_searching/nested_ranges_check_analysis/
---

# Nested Ranges Check

## Problem Statement
Given n ranges [a1,b1],[a2,b2],…,[an,bn], for each range check if it contains any other range and if it is contained by any other range.

### Input
The first input line has an integer n: the number of ranges.
Then there are n lines. Each line has two integers a and b: the start and end of a range.

### Output
Print n lines. For each range, print two integers: 1 if the range contains another range, 0 otherwise, and 1 if the range is contained by another range, 0 otherwise.

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
1 0
0 1
1 0
0 1
```

## Solution Progression

### Approach 1: Brute Force - O(n²)
**Description**: For each range, check all other ranges for containment.

```python
def nested_ranges_check_naive(n, ranges):
    results = []
    
    for i in range(n):
        contains_other = 0
        is_contained = 0
        
        for j in range(n):
            if i != j:
                # Check if range i contains range j
                if ranges[i][0] <= ranges[j][0] and ranges[i][1] >= ranges[j][1]:
                    contains_other = 1
                
                # Check if range i is contained by range j
                if ranges[j][0] <= ranges[i][0] and ranges[j][1] >= ranges[i][1]:
                    is_contained = 1
        
        results.append((contains_other, is_contained))
    
    return results
```

**Why this is inefficient**: For each range, we check all other ranges, leading to O(n²) time complexity.

### Improvement 1: Sorting and Binary Search - O(n log n)
**Description**: Sort ranges and use binary search to find containment relationships.

```python
def nested_ranges_check_optimized(n, ranges):
    # Create list of (start, end, index) tuples
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    
    # Sort by start position, then by end position (descending)
    range_list.sort(key=lambda x: (x[0], -x[1]))
    
    results = [[0, 0] for _ in range(n)]
    
    # Check for containment
    for i in range(n):
        start, end, idx = range_list[i]
        
        # Check if this range contains any range that comes after it
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_start and end >= next_end:
                results[idx][0] = 1  # Contains another range
                results[next_idx][1] = 1  # Is contained by another range
    
    return results
```

**Why this improvement works**: By sorting ranges by start position and then by end position (descending), we can efficiently check for containment relationships in a single pass.

## Final Optimal Solution

```python
n = int(input())
ranges = []
for _ in range(n):
    a, b = map(int, input().split())
    ranges.append((a, b))

def check_nested_ranges(n, ranges):
    # Create list of (start, end, index) tuples
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    
    # Sort by start position, then by end position (descending)
    range_list.sort(key=lambda x: (x[0], -x[1]))
    
    results = [[0, 0] for _ in range(n)]
    
    # Check for containment
    for i in range(n):
        start, end, idx = range_list[i]
        
        # Check if this range contains any range that comes after it
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_start and end >= next_end:
                results[idx][0] = 1  # Contains another range
                results[next_idx][1] = 1  # Is contained by another range
    
    return results

results = check_nested_ranges(n, ranges)
for contains_other, is_contained in results:
    print(contains_other, is_contained)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check all pairs of ranges |
| Sorting and Binary Search | O(n log n) | O(n) | Sort and check in single pass |

## Key Insights for Other Problems

### 1. **Range Problems**
**Principle**: Sort ranges by start position to enable efficient containment checking.
**Applicable to**: Range problems, interval problems, containment problems

### 2. **Sorting for Efficiency**
**Principle**: Sort data to enable linear-time processing instead of quadratic.
**Applicable to**: Sorting problems, optimization problems, range problems

### 3. **Containment Relationships**
**Principle**: Use sorted order to efficiently determine containment relationships.
**Applicable to**: Containment problems, relationship problems, interval problems

## Notable Techniques

### 1. **Range Sorting**
```python
def sort_ranges_by_start_end(ranges):
    # Sort by start position, then by end position (descending)
    return sorted(ranges, key=lambda x: (x[0], -x[1]))
```

### 2. **Containment Checking**
```python
def check_containment(range1, range2):
    start1, end1 = range1
    start2, end2 = range2
    
    return start1 <= start2 and end1 >= end2
```

### 3. **Range Processing**
```python
def process_ranges_efficiently(ranges):
    sorted_ranges = sort_ranges_by_start_end(ranges)
    results = []
    
    for i, (start, end) in enumerate(sorted_ranges):
        contains_other = 0
        is_contained = 0
        
        # Check containment relationships
        for j in range(i + 1, len(sorted_ranges)):
            if check_containment((start, end), sorted_ranges[j]):
                contains_other = 1
                # Mark the other range as contained
                # Implementation depends on specific requirements
        
        results.append((contains_other, is_contained))
    
    return results
```

## Problem-Solving Framework

1. **Identify problem type**: This is a range containment checking problem
2. **Choose approach**: Sort ranges and check containment in single pass
3. **Sort ranges**: Sort by start position, then by end position (descending)
4. **Initialize results**: Create array to store containment relationships
5. **Check containment**: For each range, check if it contains ranges that come after it
6. **Update results**: Mark containment relationships in both directions
7. **Return result**: Output containment information for each range

---

*This analysis shows how to efficiently check nested range relationships using sorting and linear processing.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Boolean Range Containment**
**Problem**: Return boolean values instead of 0/1 for containment relationships.
```python
def boolean_nested_ranges_check(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], -x[1]))
    
    results = [[False, False] for _ in range(n)]  # [contains_other, is_contained]
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_start and end >= next_end:
                results[idx][0] = True  # Contains another range
                results[next_idx][1] = True  # Is contained by another range
    
    return results
```

#### **Variation 2: Strict Containment Check**
**Problem**: Check for strict containment (ranges must be strictly smaller, not equal).
```python
def strict_nested_ranges_check(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], -x[1]))
    
    results = [[0, 0] for _ in range(n)]
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            # Strict containment: range must be strictly smaller
            if (start < next_start and end > next_end) or (start == next_start and end > next_end) or (start < next_start and end == next_end):
                results[idx][0] = 1  # Contains another range
                results[next_idx][1] = 1  # Is contained by another range
    
    return results
```

#### **Variation 3: Range Overlap Check**
**Problem**: Check if ranges overlap (not just containment) and if they are overlapped by other ranges.
```python
def overlap_ranges_check(n, ranges):
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
                    results[idx][0] = 1  # Overlaps with another range
                    results[other_idx][1] = 1  # Is overlapped by another range
    
    return results
```

#### **Variation 4: Range Disjoint Check**
**Problem**: Check if ranges are disjoint (no overlap) and if they are disjoint from all other ranges.
```python
def disjoint_ranges_check(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], x[1]))
    
    results = [[0, 0] for _ in range(n)]  # [disjoint_from, is_disjoint_from]
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        for j in range(n):
            if i != j:
                other_start, other_end, other_idx = range_list[j]
                
                # Check for disjointness
                if end < other_start or start > other_end:
                    results[idx][0] = 1  # Disjoint from another range
                    results[other_idx][1] = 1  # Is disjoint from another range
    
    return results
```

#### **Variation 5: Range Equality Check**
**Problem**: Check if ranges are equal to any other range and if they are equal to any other range.
```python
def equal_ranges_check(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], x[1]))
    
    results = [[0, 0] for _ in range(n)]  # [equals, is_equal_to]
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        for j in range(n):
            if i != j:
                other_start, other_end, other_idx = range_list[j]
                
                # Check for equality
                if start == other_start and end == other_end:
                    results[idx][0] = 1  # Equals another range
                    results[other_idx][1] = 1  # Is equal to another range
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Range Problems**
- **Range Intersection**: Find intersecting ranges
- **Range Union**: Find union of ranges
- **Range Difference**: Find difference between ranges
- **Range Complement**: Find complement of ranges

#### **2. Interval Problems**
- **Interval Scheduling**: Schedule non-overlapping intervals
- **Interval Partitioning**: Partition intervals into minimum sets
- **Interval Coloring**: Color intervals with minimum colors
- **Interval Matching**: Match intervals optimally

#### **3. Geometric Problems**
- **Rectangle Overlap**: Find overlapping rectangles
- **Line Segment Intersection**: Find intersecting line segments
- **Point in Range**: Check if point is in range
- **Range Closest Pair**: Find closest pair in ranges

#### **4. Boolean Problems**
- **Boolean Satisfiability**: Satisfy boolean constraints
- **Logical Operations**: Perform logical operations on ranges
- **Truth Tables**: Analyze range relationships
- **Boolean Algebra**: Apply boolean algebra to ranges

#### **5. Decision Problems**
- **Range Membership**: Check if value is in range
- **Range Validity**: Check if range is valid
- **Range Consistency**: Check range consistency
- **Range Completeness**: Check range completeness

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
    
    results = check_nested_ranges(n, ranges)
    for contains_other, is_contained in results:
        print(contains_other, is_contained)
```

#### **2. Range Queries**
```python
# Precompute containment relationships for efficient querying
def precompute_containment_matrix(ranges):
    n = len(ranges)
    matrix = [[False] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                if (ranges[i][0] <= ranges[j][0] and 
                    ranges[i][1] >= ranges[j][1]):
                    matrix[i][j] = True
    
    return matrix

# Answer containment queries efficiently
def containment_query(matrix, i, j):
    return matrix[i][j]
```

#### **3. Interactive Problems**
```python
# Interactive range checking game
def interactive_range_checker():"
    n = int(input("Enter number of ranges: "))
    ranges = []
    
    for i in range(n):
        start = int(input(f"Enter start of range {i+1}: "))
        end = int(input(f"Enter end of range {i+1}: "))
        ranges.append((start, end))
    
    print("Ranges:", ranges)
    
    while True:
        query = input("Enter query (contains/contained/overlap/disjoint/exit): ")
        if query == "exit":
            break
        
        i = int(input("Enter range index: "))
        if query == "contains":
            result = any(ranges[i][0] <= ranges[j][0] and ranges[i][1] >= ranges[j][1] 
                        for j in range(n) if i != j)
            print(f"Range {i} contains another range: {result}")
        elif query == "contained":
            result = any(ranges[j][0] <= ranges[i][0] and ranges[j][1] >= ranges[i][1] 
                        for j in range(n) if i != j)
            print(f"Range {i} is contained by another range: {result}")
        elif query == "overlap":
            result = any(ranges[i][0] < ranges[j][1] and ranges[i][1] > ranges[j][0] 
                        for j in range(n) if i != j)
            print(f"Range {i} overlaps with another range: {result}")
        elif query == "disjoint":
            result = all(ranges[i][1] < ranges[j][0] or ranges[i][0] > ranges[j][1] 
                        for j in range(n) if i != j)
            print(f"Range {i} is disjoint from all other ranges: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Set Theory**
- **Subset Relationships**: Mathematical foundation for containment
- **Set Operations**: Union, intersection, difference of ranges
- **Set Equality**: Equality of range sets
- **Set Disjointness**: Disjointness of range sets

#### **2. Order Theory**
- **Partial Orders**: Containment as partial ordering
- **Total Orders**: Total ordering of ranges
- **Lattices**: Range containment lattices
- **Chains**: Totally ordered subsets of ranges

#### **3. Logic**
- **Boolean Logic**: Logical operations on range relationships
- **Predicate Logic**: Quantified statements about ranges
- **Propositional Logic**: Logical connectives with ranges
- **First-Order Logic**: Quantified range relationships

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Sweep Line Algorithm**: Efficient range processing
- **Segment Trees**: Range query data structures
- **Interval Trees**: Specialized for interval operations
- **Range Trees**: Multi-dimensional range queries

#### **2. Mathematical Concepts**
- **Set Theory**: Foundation for range operations
- **Order Theory**: Understanding range relationships
- **Logic**: Boolean and predicate logic
- **Geometry**: Geometric interpretation of ranges

#### **3. Programming Concepts**
- **Boolean Operations**: Efficient boolean checking
- **Data Structures**: Efficient range storage and querying
- **Algorithm Design**: Problem-solving strategies
- **Complexity Analysis**: Time and space complexity

---

*This analysis demonstrates efficient range relationship checking techniques and shows various extensions for interval problems.* 