# CSES Sum of Four Values - Problem Analysis

## Problem Statement
Given an array of n integers and a target sum x, find four distinct indices such that the sum of the values at those indices equals x.

### Input
The first input line has two integers n and x: the size of the array and the target sum.
The second line has n integers a1,a2,…,an: the array.

### Output
Print four distinct indices (1-indexed) such that the sum equals x, or "IMPOSSIBLE" if no solution exists.

### Constraints
- 1 ≤ n ≤ 1000
- 1 ≤ x ≤ 10^9
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
5 15
1 3 4 6 8

Output:
1 2 3 4
```

## Solution Progression

### Approach 1: Brute Force - O(n⁴)
**Description**: Try all possible combinations of four indices.

```python
def sum_of_four_values_naive(n, x, arr):
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    if arr[i] + arr[j] + arr[k] + arr[l] == x:
                        return (i + 1, j + 1, k + 1, l + 1)
    return "IMPOSSIBLE"
```

**Why this is inefficient**: We try all O(n⁴) combinations, leading to quartic time complexity.

### Improvement 1: Two Pointers - O(n³)
**Description**: Fix two elements and use two pointers for the remaining two.

```python
def sum_of_four_values_optimized(n, x, arr):
    # Create list of (value, index) pairs
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()  # Sort by value
    
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            target = x - pairs[i][0] - pairs[j][0]
            
            while left < right:
                current_sum = pairs[left][0] + pairs[right][0]
                
                if current_sum == target:
                    return (pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1])
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return "IMPOSSIBLE"
```

**Why this improvement works**: We fix two elements and use two pointers to find the remaining two elements that sum to the target. This reduces the complexity from O(n⁴) to O(n³).

## Final Optimal Solution

```python
n, x = map(int, input().split())
arr = list(map(int, input().split()))

def find_four_values(n, x, arr):
    # Create list of (value, index) pairs
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()  # Sort by value
    
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            target = x - pairs[i][0] - pairs[j][0]
            
            while left < right:
                current_sum = pairs[left][0] + pairs[right][0]
                
                if current_sum == target:
                    return (pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1])
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return "IMPOSSIBLE"

result = find_four_values(n, x, arr)
if result == "IMPOSSIBLE":
    print(result)
else:
    print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n⁴) | O(1) | Try all combinations |
| Two Pointers | O(n³) | O(n) | Fix two elements and use two pointers |

## Key Insights for Other Problems

### 1. **Four Sum Problems**
**Principle**: Fix two elements and use two pointers to find the remaining two elements.
**Applicable to**: Four sum problems, k-sum problems, pointer problems

### 2. **Two Pointers Technique**
**Principle**: Use two pointers to efficiently find pairs that sum to a target value.
**Applicable to**: Two sum problems, pointer problems, search problems

### 3. **Sorting for Efficiency**
**Principle**: Sort the array to enable efficient two-pointer search.
**Applicable to**: Sorting problems, search problems, optimization problems

## Notable Techniques

### 1. **Four Sum with Two Pointers**
```python
def four_sum_with_pointers(arr, target):
    pairs = [(arr[i], i) for i in range(len(arr))]
    pairs.sort()
    
    for i in range(len(arr) - 3):
        for j in range(i + 1, len(arr) - 2):
            left = j + 1
            right = len(arr) - 1
            current_target = target - pairs[i][0] - pairs[j][0]
            
            while left < right:
                current_sum = pairs[left][0] + pairs[right][0]
                
                if current_sum == current_target:
                    return (pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1])
                elif current_sum < current_target:
                    left += 1
                else:
                    right -= 1
    
    return None
```

### 2. **Two Pointer Search**
```python
def two_pointer_search(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        
        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None
```

### 3. **Index Tracking**
```python
def track_indices_with_values(arr):
    # Create pairs of (value, original_index)
    pairs = [(arr[i], i + 1) for i in range(len(arr))]
    pairs.sort(key=lambda x: x[0])
    return pairs
```

## Problem-Solving Framework

1. **Identify problem type**: This is a four sum problem with index tracking
2. **Choose approach**: Use two pointers technique after sorting
3. **Create pairs**: Store (value, index) pairs to track original indices
4. **Sort pairs**: Sort by value to enable two-pointer search
5. **Fix two elements**: Iterate through all possible pairs of first two elements
6. **Two pointer search**: Use two pointers to find remaining two elements
7. **Return result**: Output the four indices or "IMPOSSIBLE"

---

*This analysis shows how to efficiently find four values that sum to a target using two pointers technique.* 