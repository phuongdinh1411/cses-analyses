# CSES Stick Lengths - Problem Analysis

## Problem Statement
There are n sticks with some lengths. Your task is to modify the lengths so that all sticks have equal lengths. You can either lengthen or shorten each stick. Both operations cost x where x is the difference between the new and original length.

What is the minimum total cost?

### Input
The first input line has an integer n: the number of sticks.
The second line has n integers p1,p2,…,pn: the lengths of the sticks.

### Output
Print one integer: the minimum total cost.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ pi ≤ 10^9

### Example
```
Input:
5
2 3 1 5 2

Output:
5
```

## Solution Progression

### Approach 1: Brute Force - O(n * range)
**Description**: Try all possible target lengths and calculate the cost for each.

```python
def stick_lengths_brute_force(lengths):
    n = len(lengths)
    min_length = min(lengths)
    max_length = max(lengths)
    
    min_cost = float('inf')
    
    # Try all possible target lengths
    for target in range(min_length, max_length + 1):
        cost = 0
        for length in lengths:
            cost += abs(length - target)
        min_cost = min(min_cost, cost)
    
    return min_cost
```

**Why this is inefficient**: We're trying every possible target length between min and max, which can be very large (up to 10^9). This leads to O(n * range) complexity, which is too slow.

### Improvement 1: Median as Target - O(n log n)
**Description**: The optimal target length is the median of the array.

```python
def stick_lengths_median(lengths):
    n = len(lengths)
    
    # Sort to find median
    lengths.sort()
    
    # Median is the middle element (or average of two middle elements)
    if n % 2 == 1:
        target = lengths[n // 2]  # Odd number of elements
    else:
        target = (lengths[n // 2 - 1] + lengths[n // 2]) // 2  # Even number
    
    # Calculate cost
    cost = 0
    for length in lengths:
        cost += abs(length - target)
    
    return cost
```

**Why this improvement works**: The median minimizes the sum of absolute differences. This is because the median is the point that minimizes the total distance to all other points in a one-dimensional space.

### Improvement 2: Optimized Median Calculation - O(n log n)
**Description**: Use the median directly without trying all possible values.

```python
def stick_lengths_optimized(lengths):
    n = len(lengths)
    
    # Sort to find median
    lengths.sort()
    
    # Use the middle element as target (median)
    target = lengths[n // 2]
    
    # Calculate cost
    cost = 0
    for length in lengths:
        cost += abs(length - target)
    
    return cost
```

**Why this improvement works**: For odd n, the median is the middle element. For even n, both middle elements give the same optimal cost, so we can use either. This eliminates the need to try multiple target values.

### Alternative: Quick Select - O(n) average
**Description**: Use quick select to find the median without sorting the entire array.

```python
def quick_select(arr, k):
    """Find the k-th smallest element in arr"""
    if len(arr) == 1:
        return arr[0]
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    if k < len(left):
        return quick_select(left, k)
    elif k < len(left) + len(middle):
        return pivot
    else:
        return quick_select(right, k - len(left) - len(middle))

def stick_lengths_quick_select(lengths):
    n = len(lengths)
    
    # Find median using quick select
    target = quick_select(lengths, n // 2)
    
    # Calculate cost
    cost = 0
    for length in lengths:
        cost += abs(length - target)
    
    return cost
```

**Why this works**: Quick select finds the k-th smallest element in O(n) average time, which is faster than sorting for finding just the median.

## Final Optimal Solution

```python
n = int(input())
lengths = list(map(int, input().split()))

# Sort to find median
lengths.sort()
target = lengths[n // 2]

# Calculate minimum cost
cost = 0
for length in lengths:
    cost += abs(length - target)

print(cost)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n * range) | O(1) | Try all possible targets |
| Median | O(n log n) | O(1) | Use median as optimal target |
| Quick Select | O(n) average | O(n) | Find median without full sort |

## Key Insights for Other Problems

### 1. **Median Minimizes Absolute Differences**
**Principle**: The median minimizes the sum of absolute differences from all points.
**Applicable to**:
- Minimizing total distance problems
- Facility location problems
- Optimization problems with absolute differences
- Cost minimization problems

**Example Problems**:
- Stick lengths
- Meeting point in 1D
- Warehouse location
- Median of medians

### 2. **Sorting for Finding Order Statistics**
**Principle**: Sort to easily find median, quartiles, or other order statistics.
**Applicable to**:
- Finding median, mode, percentiles
- Order-based problems
- Statistical problems
- Optimization problems

**Example Problems**:
- Find median of two sorted arrays
- K-th largest element
- Percentile calculations
- Order statistics

### 3. **Quick Select for Order Statistics**
**Principle**: Use quick select to find k-th smallest element without full sorting.
**Applicable to**:
- Finding order statistics
- Median finding
- K-th largest/smallest element
- Partial sorting problems

**Example Problems**:
- Find k-th largest element
- Median of unsorted array
- Top k elements
- Order statistics

### 4. **Absolute Difference Optimization**
**Principle**: Problems involving absolute differences often have median as optimal solution.
**Applicable to**:
- Distance minimization
- Cost optimization
- Facility location
- Statistical problems

**Example Problems**:
- Minimum moves to equal array
- Meeting point problems
- Warehouse location
- Cost optimization

## Notable Techniques

### 1. **Median Finding Pattern**
```python
# Sort and find median
arr.sort()
median = arr[len(arr) // 2]  # For odd length
# or
median = (arr[len(arr)//2 - 1] + arr[len(arr)//2]) // 2  # For even length
```

### 2. **Quick Select Pattern**
```python
def quick_select(arr, k):
    if len(arr) == 1:
        return arr[0]
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    if k < len(left):
        return quick_select(left, k)
    elif k < len(left) + len(middle):
        return pivot
    else:
        return quick_select(right, k - len(left) - len(middle))
```

### 3. **Absolute Difference Sum**
```python
# Calculate sum of absolute differences
def abs_diff_sum(arr, target):
    return sum(abs(x - target) for x in arr)
```

## Edge Cases to Remember

1. **Single element**: Cost is 0 (already optimal)
2. **All same lengths**: Cost is 0 (no changes needed)
3. **Even number of elements**: Both middle elements give same optimal cost
4. **Large numbers**: Handle integer overflow in cost calculation
5. **Negative numbers**: Algorithm works with negative lengths

## Problem-Solving Framework

1. **Identify optimization nature**: This is a cost minimization problem
2. **Consider median approach**: Median minimizes absolute differences
3. **Choose efficient median finding**: Sort for simplicity, quick select for speed
4. **Handle edge cases**: Single element, all same, etc.
5. **Calculate cost efficiently**: Sum absolute differences

---

*This analysis shows how to systematically improve from O(n * range) to O(n log n) and extracts reusable insights for optimization problems involving absolute differences.* 