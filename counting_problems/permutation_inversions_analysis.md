# CSES Permutation Inversions - Problem Analysis

## Problem Statement
Given a permutation of numbers from 1 to n, count the number of inversions. An inversion is a pair of indices (i,j) where i < j and a[i] > a[j].

### Input
The first input line has an integer n: the size of the permutation.
The second line has n integers: the permutation.

### Output
Print one integer: the number of inversions.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- The input is a valid permutation of 1 to n

### Example
```
Input:
4
3 1 4 2

Output:
3
```

## Solution Progression

### Approach 1: Check All Pairs - O(n²)
**Description**: Check all possible pairs of indices to count inversions.

```python
def permutation_inversions_naive(n, arr):
    count = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    
    return count
```

**Why this is inefficient**: We need to check all possible pairs, leading to O(n²) time complexity.

### Improvement 1: Merge Sort with Inversion Counting - O(n log n)
**Description**: Use merge sort to count inversions efficiently.

```python
def permutation_inversions_merge_sort(n, arr):
    def merge_sort_and_count(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left, left_inversions = merge_sort_and_count(arr[:mid])
        right, right_inversions = merge_sort_and_count(arr[mid:])
        
        merged, split_inversions = merge_and_count(left, right)
        total_inversions = left_inversions + right_inversions + split_inversions
        
        return merged, total_inversions
    
    def merge_and_count(left, right):
        merged = []
        inversions = 0
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len(left) - i
                j += 1
        
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, inversions
    
    _, count = merge_sort_and_count(arr)
    return count
```

**Why this improvement works**: Merge sort allows us to count inversions in O(n log n) time by counting split inversions during merging.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

def count_inversions(n, arr):
    def merge_sort_and_count(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left, left_inversions = merge_sort_and_count(arr[:mid])
        right, right_inversions = merge_sort_and_count(arr[mid:])
        
        merged, split_inversions = merge_and_count(left, right)
        total_inversions = left_inversions + right_inversions + split_inversions
        
        return merged, total_inversions
    
    def merge_and_count(left, right):
        merged = []
        inversions = 0
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len(left) - i
                j += 1
        
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, inversions
    
    _, count = merge_sort_and_count(arr)
    return count

result = count_inversions(n, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n²) | O(1) | Check all pairs |
| Merge Sort | O(n log n) | O(n) | Use merge sort to count inversions |

## Key Insights for Other Problems

### 1. **Inversion Counting Problems**
**Principle**: Use divide and conquer algorithms to count inversions efficiently.
**Applicable to**: Sorting problems, counting problems, divide and conquer problems

### 2. **Merge Sort for Counting**
**Principle**: Use merge sort to count inversions during the merging process.
**Applicable to**: Sorting problems, counting problems, merge sort applications

### 3. **Split Inversion Counting**
**Principle**: Count inversions that span across the divide point during merging.
**Applicable to**: Divide and conquer problems, counting problems, merge sort variations

## Notable Techniques

### 1. **Merge Sort with Inversion Counting**
```python
def merge_sort_with_inversions(arr):
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_inv = merge_sort_with_inversions(arr[:mid])
    right, right_inv = merge_sort_with_inversions(arr[mid:])
    
    merged, split_inv = merge_and_count(left, right)
    return merged, left_inv + right_inv + split_inv
```

### 2. **Merge and Count Inversions**
```python
def merge_and_count(left, right):
    merged = []
    inversions = 0
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged, inversions
```

### 3. **Inversion Check**
```python
def count_inversions_naive(arr):
    count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                count += 1
    return count
```

## Problem-Solving Framework

1. **Identify problem type**: This is an inversion counting problem
2. **Choose approach**: Use merge sort to count inversions efficiently
3. **Implement merge sort**: Modify merge sort to count split inversions
4. **Count inversions**: Track inversions during the merging process
5. **Return result**: Sum up all inversions (left + right + split)

---

*This analysis shows how to efficiently count inversions in a permutation using merge sort with inversion counting.* 