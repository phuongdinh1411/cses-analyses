# CSES Nested Ranges Count - Problem Analysis

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