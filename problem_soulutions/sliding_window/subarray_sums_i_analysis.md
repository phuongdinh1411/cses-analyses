---
layout: simple
title: "Subarray Sums I - Count Subarrays with Sum X"
permalink: /problem_soulutions/sliding_window/subarray_sums_i_analysis
---

# Subarray Sums I - Count Subarrays with Sum X

## 📋 Problem Description

Given an array of n integers, find the number of subarrays with sum x.

**Input**: 
- First line: Two integers n and x (array size and target sum)
- Second line: n integers a₁, a₂, ..., aₙ (array contents)

**Output**: 
- One integer: the number of subarrays with sum x

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- −10⁹ ≤ x, aᵢ ≤ 10⁹

**Example**:
```
Input:
5 7
2 -1 3 5 -2

Output:
2
```

**Explanation**: The subarrays with sum 7 are:
- [2, -1, 3, 5, -2] → sum = 2 + (-1) + 3 + 5 + (-2) = 7
- [3, 5, -1] → sum = 3 + 5 + (-1) = 7

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count subarrays with exactly sum x
- **Key Insight**: Use prefix sum to find subarray sums efficiently
- **Challenge**: Handle negative numbers and find all valid subarrays

### Step 2: Brute Force Approach
**Check all possible subarrays and calculate their sums:**

```python
def subarray_sums_naive(n, x, arr):
    count = 0
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum == x:
                count += 1
    
    return count
```

**Complexity**: O(n²) - too slow for large arrays

### Step 3: Optimization
**Use prefix sum with hash map for efficient counting:**

```python
def subarray_sums_prefix_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count
```

**Key Insight**: Use prefix sum difference to find subarrays with target sum

### Step 4: Complete Solution

```python
def solve_subarray_sums_i():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = count_subarrays_with_sum(n, x, arr)
    print(result)

def count_subarrays_with_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count

if __name__ == "__main__":
    solve_subarray_sums_i()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 7, [2, -1, 3, 5, -2]), 2),
        ((4, 6, [1, 2, 3, 4]), 1),
        ((3, 0, [1, -1, 0]), 3),
        ((2, 5, [1, 4]), 1),
        ((1, 1, [1]), 1),
        ((4, 10, [2, 3, 4, 1]), 1),
    ]
    
    for (n, x, arr), expected in test_cases:
        result = count_subarrays_with_sum(n, x, arr)
        print(f"n={n}, x={x}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def count_subarrays_with_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    
    for num in arr:
        prefix_sum += num
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with prefix sum
- **Space**: O(n) - hash map to store prefix sum frequencies

### Why This Solution Works
- **Prefix Sum**: Efficiently calculates subarray sums
- **Hash Map**: Tracks frequency of prefix sums for O(1) lookup
- **Difference Calculation**: Uses prefix_sum - x to find target subarrays
- **Optimal Algorithm**: Best known approach for this problem

## 🎨 Visual Example

### Input Example
```
Input: n=5, x=7, arr=[2, -1, 3, 5, -2]
Output: 2 (subarrays with sum 7)
```

### Array Visualization
```
Array: [2, -1, 3, 5, -2]
Index:  0   1  2  3   4
```

### Prefix Sum Calculation
```
Index:  -1   0   1   2   3   4
Array:  [ ]  [2] [-1] [3] [5] [-2]
Prefix:  0    2   1   4   9   7

Prefix[0] = 0
Prefix[1] = 0 + 2 = 2
Prefix[2] = 2 + (-1) = 1
Prefix[3] = 1 + 3 = 4
Prefix[4] = 4 + 5 = 9
Prefix[5] = 9 + (-2) = 7
```

### Subarray Sum Analysis
```
Target sum: x = 7

For each position i, find how many j < i have:
Prefix[i] - Prefix[j] = x
Prefix[j] = Prefix[i] - x

Position 0: Prefix[0] = 2
Target: 2 - 7 = -5
Count of prefix sum -5: 0
Subarrays ending at 0: 0

Position 1: Prefix[1] = 1  
Target: 1 - 7 = -6
Count of prefix sum -6: 0
Subarrays ending at 1: 0

Position 2: Prefix[2] = 4
Target: 4 - 7 = -3
Count of prefix sum -3: 0
Subarrays ending at 2: 0

Position 3: Prefix[3] = 9
Target: 9 - 7 = 2
Count of prefix sum 2: 1 (at position 0)
Subarrays ending at 3: 1
Subarray: [1,3] = arr[1:4] = [-1, 3, 5] → sum = 7

Position 4: Prefix[4] = 7
Target: 7 - 7 = 0
Count of prefix sum 0: 1 (at position -1)
Subarrays ending at 4: 1
Subarray: [0,4] = arr[0:5] = [2, -1, 3, 5, -2] → sum = 7

Total subarrays with sum 7: 2
```

### Hash Map Tracking
```
Hash map: {prefix_sum → count}

Initialize: {0: 1} (empty subarray)

i=0: prefix=2, target=2-7=-5
- Count subarrays: 0
- Update map: {0: 1, 2: 1}

i=1: prefix=1, target=1-7=-6  
- Count subarrays: 0
- Update map: {0: 1, 2: 1, 1: 1}

i=2: prefix=4, target=4-7=-3
- Count subarrays: 0
- Update map: {0: 1, 2: 1, 1: 1, 4: 1}

i=3: prefix=9, target=9-7=2
- Count subarrays: 1 (map[2] = 1)
- Update map: {0: 1, 2: 1, 1: 1, 4: 1, 9: 1}

i=4: prefix=7, target=7-7=0
- Count subarrays: 1 (map[0] = 1)
- Update map: {0: 1, 2: 1, 1: 1, 4: 1, 9: 1, 7: 1}

Total: 2 subarrays
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Prefix Sum +    │ O(n)         │ O(n)         │ Hash map     │
│ Hash Map        │              │              │ frequency    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n²)        │ O(1)         │ Check all    │
│                 │              │              │ subarrays    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sliding Window  │ O(n)         │ O(1)         │ Only for     │
│                 │              │              │ positive     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Prefix Sum Technique**
- Convert range queries to point queries
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Hash Map for Frequency**
- Track frequency of prefix sums efficiently
- Important for understanding
- Enable O(1) lookup time
- Essential for algorithm

### 3. **Subarray Sum Calculation**
- Use prefix sum difference for subarray sums
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Subarray Sums with Length Constraint
**Problem**: Count subarrays with sum x and length at least k.

```python
def count_subarrays_with_sum_and_length(n, x, k, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(list)  # Map sum to list of indices
    sum_count[0] = [-1]  # Empty subarray at index -1
    
    for i, num in enumerate(arr):
        prefix_sum += num
        
        if prefix_sum - x in sum_count:
            # Check if any previous index gives us length >= k
            for prev_idx in sum_count[prefix_sum - x]:
                if i - prev_idx >= k:
                    count += 1
        
        sum_count[prefix_sum].append(i)
    
    return count

# Example usage
result = count_subarrays_with_sum_and_length(5, 7, 2, [2, -1, 3, 5, -2])
print(f"Subarrays with sum 7 and length >= 2: {result}")
```

### Variation 2: Subarray Sums with Even/Odd Constraint
**Problem**: Count subarrays with sum x where the sum is even/odd.

```python
def count_subarrays_with_sum_and_parity(n, x, arr, want_even=True):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    even_sums = defaultdict(int)  # Track even prefix sums
    odd_sums = defaultdict(int)   # Track odd prefix sums
    even_sums[0] = 1  # Empty subarray has even sum 0
    
    for num in arr:
        prefix_sum += num
        
        if want_even and prefix_sum % 2 == 0:
            # Looking for even sum, check if (prefix_sum - x) is even
            if (prefix_sum - x) % 2 == 0:
                count += even_sums[prefix_sum - x]
            even_sums[prefix_sum] += 1
        elif not want_even and prefix_sum % 2 == 1:
            # Looking for odd sum, check if (prefix_sum - x) is odd
            if (prefix_sum - x) % 2 == 1:
                count += odd_sums[prefix_sum - x]
            odd_sums[prefix_sum] += 1
        else:
            # Update appropriate counter
            if prefix_sum % 2 == 0:
                even_sums[prefix_sum] += 1
            else:
                odd_sums[prefix_sum] += 1
    
    return count

# Example usage
even_count = count_subarrays_with_sum_and_parity(5, 7, [2, -1, 3, 5, -2], True)
odd_count = count_subarrays_with_sum_and_parity(5, 7, [2, -1, 3, 5, -2], False)
print(f"Even sum subarrays: {even_count}, Odd sum subarrays: {odd_count}")
```

### Variation 3: Subarray Sums with Range Constraint
**Problem**: Count subarrays with sum in range [L, R].

```python
def count_subarrays_with_sum_range(n, L, R, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    
    for num in arr:
        prefix_sum += num
        
        # Count subarrays with sum in [L, R]
        for target in range(L, R + 1):
            if prefix_sum - target in sum_count:
                count += sum_count[prefix_sum - target]
        
        sum_count[prefix_sum] += 1
    
    return count

# Example usage
result = count_subarrays_with_sum_range(5, 5, 10, [2, -1, 3, 5, -2])
print(f"Subarrays with sum in [5, 10]: {result}")
```

### Variation 4: Subarray Sums with K Occurrences
**Problem**: Count subarrays with sum x that appear exactly k times.

```python
def count_subarrays_with_sum_k_occurrences(n, x, k, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    
    for num in arr:
        prefix_sum += num
        
        # Check if we have exactly k occurrences of (prefix_sum - x)
        if prefix_sum - x in sum_count and sum_count[prefix_sum - x] == k:
            count += 1
        
        sum_count[prefix_sum] += 1
    
    return count

# Example usage
result = count_subarrays_with_sum_k_occurrences(5, 7, 1, [2, -1, 3, 5, -2])
print(f"Subarrays with sum 7 appearing exactly 1 time: {result}")
```

### Variation 5: Subarray Sums with Range Queries
**Problem**: Answer queries about subarray sums in specific ranges.

```python
def subarray_sums_range_queries(n, x, arr, queries):
    """Answer queries about subarray sums with target x in ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= n:
            results.append(0)
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            count = count_subarrays_with_sum_in_range(len(subarray), x, subarray)
            results.append(count)
    
    return results

def count_subarrays_with_sum_in_range(n, x, arr):
    """Count subarrays with sum x in a specific range"""
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    
    for num in arr:
        prefix_sum += num
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count

# Example usage
queries = [(0, 2), (1, 3), (0, 3)]
result = subarray_sums_range_queries(5, 7, [2, -1, 3, 5, -2], queries)
print(f"Range query results: {result}")
```

## 🔗 Related Problems

- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray existence problems
- **[Longest Subarray with Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Longest subarray problems
- **[Shortest Subarray with Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Shortest subarray problems

## 📚 Learning Points

1. **Prefix Sum Technique**: Essential for subarray sum problems
2. **Hash Map for Frequency**: Important for efficient counting
3. **Subarray Sum Calculation**: Key for understanding prefix sum differences
4. **Range Query Handling**: Important for complex subarray problems

---

**This is a great introduction to subarray sum counting problems!** 🎯