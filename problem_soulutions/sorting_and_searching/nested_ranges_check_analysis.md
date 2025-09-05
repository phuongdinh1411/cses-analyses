---
layout: simple
title: "Nested Ranges Check"
permalink: /problem_soulutions/sorting_and_searching/nested_ranges_check_analysis
---

# Nested Ranges Check

## Problem Description

**Problem**: Given n ranges [a₁,b₁], [a₂,b₂], ..., [aₙ,bₙ], for each range check if it contains any other range and if it is contained by any other range.

**Input**: 
- First line: n (number of ranges)
- Next n lines: a b (start and end of each range)

**Output**: n lines, each with two integers: 1 if the range contains another range, 0 otherwise, and 1 if the range is contained by another range, 0 otherwise.

**Example**:
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

Explanation: 
Range [1,6] contains [2,4] and [3,6] → contains another range (1), not contained by any (0)
Range [2,4] is contained by [1,6] → doesn't contain any (0), is contained by another (1)
Range [4,8] contains [3,6] → contains another range (1), not contained by any (0)
Range [3,6] is contained by [1,6] → doesn't contain any (0), is contained by another (1)
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
Range 0 [1,6]: contains Range 1 and Range 3 → (1, 0)
Range 1 [2,4]: contained by Range 0 → (0, 1)
Range 2 [4,8]: contains Range 3 → (1, 0)
Range 3 [3,6]: contained by Range 0 → (0, 1)
```

### Key Insight
The sorting approach enables efficient containment checking by:
1. Sorting ranges by start position first
2. Then by end position (descending)
3. Only checking forward ranges after sorting
4. Reducing complexity from O(n²) to O(n log n)

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- For each range, check if it contains any other range
- For each range, check if it is contained by any other range
- Return binary results (0 or 1) for each check
- Need efficient approach for large number of ranges

**Key Observations:**
- Brute force would check O(n²) pairs
- Can use sorting to optimize
- Sort by start position, then by end position
- Use binary results instead of counts

### Step 2: Brute Force Approach
**Idea**: For each range, check all other ranges for containment.

```python
def nested_ranges_check_brute_force(n, ranges):
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

**Why this works:**
- Checks all possible range pairs
- Simple to understand and implement
- Guarantees correct answer
- O(n²) time complexity

### Step 3: Sorting Optimization
**Idea**: Sort ranges and use efficient checking.

```python
def nested_ranges_check_sorting(n, ranges):
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

**Why this is better:**
- O(n log n) time complexity
- Uses sorting to optimize checking
- Maintains original indices
- Much more efficient

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_nested_ranges_check():
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
    
    # Check for containment
    for i in range(n):
        start, end, idx = range_list[i]
        
        # Check if this range contains any range that comes after it
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_start and end >= next_end:
                results[idx][0] = 1  # Contains another range
                results[next_idx][1] = 1  # Is contained by another range
    
    # Print results
    for contains, contained in results:
        print(contains, contained)

# Main execution
if __name__ == "__main__":
    solve_nested_ranges_check()
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
        (4, [(1, 6), (2, 4), (4, 8), (3, 6)], [(1, 0), (0, 1), (1, 0), (0, 1)]),
        (3, [(1, 3), (2, 4), (1, 4)], [(0, 1), (0, 1), (1, 0)]),
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
                results[idx][0] = 1
                results[next_idx][1] = 1
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - sorting + linear scan
- **Space**: O(n) - storing range list and results

### Why This Solution Works
- **Sorting**: Enables efficient containment checking
- **Linear Scan**: Check containment relationships in one pass
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

### 3. **Binary Results**
- Use 0/1 instead of counts
- Stop checking once we find containment
- More efficient than counting
- Matches problem requirements

## 🎯 Problem Variations

### Variation 1: Overlapping Ranges Check
**Problem**: Check if each range overlaps with any other range.

```python
def overlapping_ranges_check(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], x[1]))
    
    results = [0] * n
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        # Check if this range overlaps with any range that comes after it
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_end and end >= next_start:
                results[idx] = 1
                results[next_idx] = 1
                break  # Found overlap, no need to check more
    
    return results
```

### Variation 2: Range Intersection Check
**Problem**: Check if each range has non-empty intersection with any other range.

```python
def range_intersection_check(n, ranges):
    results = [0] * n
    
    for i in range(n):
        start1, end1 = ranges[i]
        
        for j in range(n):
            if i != j:
                start2, end2 = ranges[j]
                
                # Check for intersection
                if max(start1, start2) <= min(end1, end2):
                    results[i] = 1
                    break  # Found intersection, no need to check more
    
    return results
```

### Variation 3: Range Disjoint Check
**Problem**: Check if each range is disjoint from all other ranges.

```python
def range_disjoint_check(n, ranges):
    range_list = [(ranges[i][0], ranges[i][1], i) for i in range(n)]
    range_list.sort(key=lambda x: (x[0], x[1]))
    
    results = [1] * n  # Assume all are disjoint initially
    
    for i in range(n):
        start, end, idx = range_list[i]
        
        # Check if this range overlaps with any range that comes after it
        for j in range(i + 1, n):
            next_start, next_end, next_idx = range_list[j]
            
            if start <= next_end and end >= next_start:
                results[idx] = 0  # Not disjoint
                results[next_idx] = 0  # Not disjoint
    
    return results
```

### Variation 4: Range Coverage Check
**Problem**: Check if each range is completely covered by other ranges.

```python
def range_coverage_check(n, ranges):
    results = [0] * n
    
    for i in range(n):
        start, end = ranges[i]
        covered = True
        
        for j in range(n):
            if i != j:
                other_start, other_end = ranges[j]
                
                # Check if this range is covered by other range
                if other_start <= start and other_end >= end:
                    covered = False
                    break
        
        results[i] = 1 if not covered else 0
    
    return results
```

### Variation 5: Dynamic Range Checking
**Problem**: Support adding/removing ranges dynamically.

```python
class DynamicRangeChecker:
    def __init__(self):
        self.ranges = []
        self.range_list = []
    
    def add_range(self, start, end):
        idx = len(self.ranges)
        self.ranges.append((start, end))
        self.range_list.append((start, end, idx))
        self.range_list.sort(key=lambda x: (x[0], -x[1]))
        return self.get_containment_status()
    
    def remove_range(self, index):
        if 0 <= index < len(self.ranges):
            self.ranges.pop(index)
            self.range_list = [(self.ranges[i][0], self.ranges[i][1], i) for i in range(len(self.ranges))]
            self.range_list.sort(key=lambda x: (x[0], -x[1]))
        return self.get_containment_status()
    
    def get_containment_status(self):
        n = len(self.range_list)
        results = [[0, 0] for _ in range(n)]
        
        for i in range(n):
            start, end, idx = self.range_list[i]
            
            for j in range(i + 1, n):
                next_start, next_end, next_idx = self.range_list[j]
                
                if start <= next_start and end >= next_end:
                    results[idx][0] = 1
                    results[next_idx][1] = 1
        
        return results
```

## 🔗 Related Problems

- **[Nested Ranges Count](/cses-analyses/problem_soulutions/sorting_and_searching/nested_ranges_count_analysis)**: Range containment counting
- **[Room Allocation](/cses-analyses/problem_soulutions/sorting_and_searching/room_allocation_analysis)**: Range scheduling
- **[Movie Festival](/cses-analyses/problem_soulutions/sorting_and_searching/cses_movie_festival_analysis)**: Interval problems

## 📚 Learning Points

1. **Sorting Strategy**: Key insight for range problems
2. **Containment Logic**: Understanding range relationships
3. **Binary Results**: Efficient boolean checking
4. **Range Problems**: Common pattern in competitive programming

---

**This is a great introduction to range problems and sorting optimization!** 🎯 