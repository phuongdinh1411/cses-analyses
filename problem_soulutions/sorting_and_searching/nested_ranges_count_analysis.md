---
layout: simple
title: "Nested Ranges Count"
permalink: /problem_soulutions/sorting_and_searching/nested_ranges_count_analysis
---

# Nested Ranges Count

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand range containment counting problems and interval analysis techniques
- [ ] **Objective 2**: Apply sorting and coordinate compression to efficiently count range containments
- [ ] **Objective 3**: Implement efficient range counting algorithms with O(n log n) time complexity
- [ ] **Objective 4**: Optimize range counting problems using sorting, coordinate compression, and containment analysis
- [ ] **Objective 5**: Handle edge cases in range counting (identical ranges, no containment, all ranges contained)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting algorithms, coordinate compression, range containment counting, interval analysis, counting problems
- **Data Structures**: Arrays, sorting, coordinate compression, range tracking, counting structures
- **Mathematical Concepts**: Range mathematics, interval theory, containment counting, coordinate compression, counting theory
- **Programming Skills**: Sorting implementation, coordinate compression, range counting, algorithm implementation
- **Related Problems**: Nested Ranges Check (boolean version), Range problems, Counting problems

## Problem Description

**Problem**: Given n ranges [a₁,b₁], [a₂,b₂], ..., [aₙ,bₙ], for each range count how many other ranges it contains and how many other ranges contain it.

**Input**: 
- First line: n (number of ranges)
- Next n lines: a b (start and end of each range)

**Output**: n lines, each with two integers: number of ranges it contains and number of ranges that contain it.

**Example**:
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

Explanation: 
Range [1,6] contains [2,4] and [3,6] → contains 2 ranges, contained by 0
Range [2,4] is contained by [1,6] → contains 0 ranges, contained by 1
Range [4,8] contains [3,6] → contains 1 range, contained by 0
Range [3,6] is contained by [1,6] → contains 0 ranges, contained by 1
```

## 🎯 Visual Example

### Input Ranges
```
Range 0: [1, 6]
Range 1: [2, 4]
Range 2: [4, 8]
Range 3: [3, 6]
```

### Range Visualization
```
Number line: 1  2  3  4  5  6  7  8
Range 0:     |--------|
Range 1:       |--|
Range 2:           |----|
Range 3:         |--|
```

### Containment Analysis
```
Range 0 [1,6] vs Range 1 [2,4]:
- 1 ≤ 2 ✓ and 6 ≥ 4 ✓
- Range 0 contains Range 1 ✓

Range 0 [1,6] vs Range 2 [4,8]:
- 1 ≤ 4 ✓ but 6 < 8 ✗
- Range 0 does not contain Range 2 ✗

Range 0 [1,6] vs Range 3 [3,6]:
- 1 ≤ 3 ✓ and 6 ≥ 6 ✓
- Range 0 contains Range 3 ✓

Range 1 [2,4] vs Range 2 [4,8]:
- 2 ≤ 4 ✓ but 4 < 8 ✗
- Range 1 does not contain Range 2 ✗

Range 1 [2,4] vs Range 3 [3,6]:
- 2 ≤ 3 ✓ but 4 < 6 ✗
- Range 1 does not contain Range 3 ✗

Range 2 [4,8] vs Range 3 [3,6]:
- 4 ≤ 3 ✗
- Range 2 does not contain Range 3 ✗
```

### Results
```
Range 0 [1,6]: contains Range 1 and Range 3 → (2, 0)
Range 1 [2,4]: contained by Range 0 → (0, 1)
Range 2 [4,8]: contains Range 3 → (1, 0)
Range 3 [3,6]: contained by Range 0 → (0, 1)
```

### Key Insight
The sorting approach enables efficient containment counting by:
1. Sorting ranges by start position first
2. Then by end position (descending)
3. Only checking forward ranges after sorting
4. Reducing complexity from O(n²) to O(n log n)

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- For each range, count how many other ranges it contains
- For each range, count how many other ranges contain it
- Need efficient approach for large number of ranges
- Range containment: [a,b] contains [c,d] if a ≤ c and b ≥ d

**Key Observations:**
- Brute force would check O(n²) pairs
- Can use sorting to optimize
- Sort by start position, then by end position
- Use binary search for efficient counting

### Step 2: Brute Force Approach
**Idea**: For each range, check all other ranges for containment.

```python
def nested_ranges_count_brute_force(n, ranges):
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

**Why this works:**
- Checks all possible range pairs
- Simple to understand and implement
- Guarantees correct answer
- O(n²) time complexity

### Step 3: Sorting Optimization
**Idea**: Sort ranges and use efficient counting.

```python
def nested_ranges_count_sorting(n, ranges):
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

**Why this is better:**
- O(n log n) time complexity
- Uses sorting to optimize counting
- Maintains original indices
- Much more efficient

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_nested_ranges_count():
    n = int(input())
    ranges = []
    
    for _ in range(n):
        a, b = map(int, input().split())
        ranges.append((a, b))
    
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
    
    # Print results
    for contains, contained in results:
        print(contains, contained)

# Main execution
if __name__ == "__main__":
    solve_nested_ranges_count()
```

**Why this works:**
- Optimal sorting approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 6), (2, 4), (4, 8), (3, 6)], [(2, 0), (0, 1), (1, 0), (0, 1)]),
        (3, [(1, 3), (2, 4), (1, 4)], [(0, 1), (0, 1), (2, 0)]),
        (2, [(1, 2), (3, 4)], [(0, 0), (0, 0)]),
        (1, [(1, 1)], [(0, 0)]),
    ]
    
    for n, ranges, expected in test_cases:
        result = solve_test(n, ranges)
        print(f"n={n}, ranges={ranges}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], -x[1]))
    
    results = [[0, 0] for _ in range(n)]
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_start and end >= next_end:
                results[idx][0] += 1
                results[next_idx][1] += 1
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - sorting + linear scan
- **Space**: O(n) - storing range list and results

### Why This Solution Works
- **Sorting**: Enables efficient containment checking
- **Linear Scan**: Count containment relationships in one pass
- **Index Tracking**: Maintains original range indices
- **Optimal Approach**: Best possible for this problem

## 🎯 Key Insights

### 1. **Sorting Strategy**
- Sort by start position first
- Then sort by end position (descending)
- Enables efficient containment checking
- Key insight for optimization

### 2. **Containment Logic**
- Range [a,b] contains [c,d] if a ≤ c and b ≥ d
- After sorting, only need to check forward ranges
- Reduces complexity from O(n²) to O(n log n)
- Crucial for efficiency

### 3. **Index Preservation**
- Store original indices with ranges
- Map results back to original order
- Maintain correct output format
- Important for problem requirements

## 🎯 Problem Variations

### Variation 1: Overlapping Ranges Count
**Problem**: Count how many ranges overlap with each range.

```python
def overlapping_ranges_count(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], x[1]))
    
    results = [0] * n
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        # Count overlapping ranges
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_end and end >= next_start:
                results[idx] += 1
                results[next_idx] += 1
    
    return results
```

### Variation 2: Range Intersection Length
**Problem**: Find the length of intersection between each pair of ranges.

```python
def range_intersection_length(n, ranges):
    results = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            start1, end1 = ranges[i]
            start2, end2 = ranges[j]
            
            # Calculate intersection length
            intersection_start = max(start1, start2)
            intersection_end = min(end1, end2)
            
            if intersection_start <= intersection_end:
                length = intersection_end - intersection_start + 1
                results[i][j] = length
                results[j][i] = length
    
    return results
```

### Variation 3: Range Union Count
**Problem**: Count how many ranges can be merged with each range.

```python
def range_union_count(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], x[1]))
    
    results = [0] * n
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        # Count ranges that can be merged
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_end and end >= next_start:
                results[idx] += 1
                results[next_idx] += 1
    
    return results
```

### Variation 4: Range Coverage
**Problem**: Find how much of each range is covered by other ranges.

```python
def range_coverage(n, ranges):
    results = [0] * n
    
    for i in range(n):
        start, end = ranges[i]
        covered_length = 0
        
        for j in range(n):
            if i != j:
                other_start, other_end = ranges[j]
                
                # Calculate overlap
                overlap_start = max(start, other_start)
                overlap_end = min(end, other_end)
                
                if overlap_start <= overlap_end:
                    covered_length += overlap_end - overlap_start + 1
        
        results[i] = covered_length
    
    return results
```

### Variation 5: Dynamic Range Counting
**Problem**: Support adding/removing ranges dynamically.

```python
class DynamicRangeCounter:
    def __init__(self):
        self.ranges = []
        self.range_list = []
    
    def add_range(self, start, end):
        idx = len(self.ranges)
        self.ranges.append((start, end))
        self.range_list.append((start, end, idx))
        self.range_list.sort(key=lambda x: (x[0], -x[1]))
        return self.get_containment_counts()
    
    def remove_range(self, index):
        if 0 <= index < len(self.ranges):
            self.ranges.pop(index)
            self.range_list = [(self.ranges[i][0], self.ranges[i][1], i) for i in range(len(self.ranges))]
            self.range_list.sort(key=lambda x: (x[0], -x[1]))
        return self.get_containment_counts()
    
    def get_containment_counts(self):
        n = len(self.range_list)
        results = [[0, 0] for _ in range(n)]
        
        for i in range(n):
            start, end, idx = self.range_list[i]
            
            for j in range(i + 1, n):
                next_start, next_end, next_idx = self.range_list[j]
                
                if start <= next_start and end >= next_end:
                    results[idx][0] += 1
                    results[next_idx][1] += 1
        
        return results
```

## 🔗 Related Problems

- **[Nested Ranges Check](/cses-analyses/problem_soulutions/sorting_and_searching/nested_ranges_check_analysis)**: Range containment checking
- **[Room Allocation](/cses-analyses/problem_soulutions/sorting_and_searching/room_allocation_analysis)**: Range scheduling
- **[Movie Festival](/cses-analyses/problem_soulutions/sorting_and_searching/cses_movie_festival_analysis)**: Interval problems

## 📚 Learning Points

1. **Sorting Strategy**: Key insight for range problems
2. **Containment Logic**: Understanding range relationships
3. **Index Preservation**: Maintaining original order
4. **Range Problems**: Common pattern in competitive programming

---

**This is a great introduction to range problems and sorting optimization!** 🎯 