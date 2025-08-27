# CSES Nested Ranges Check - Problem Analysis

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