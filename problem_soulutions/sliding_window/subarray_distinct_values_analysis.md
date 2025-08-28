---
layout: simple
title: "Subarray Distinct Values
permalink: /problem_soulutions/sliding_window/subarray_distinct_values_analysis/
---

# Subarray Distinct Values

## Problem Statement
Given an array of n integers, your task is to find the number of subarrays with at most k distinct values.

### Input
The first input line has two integers n and k: the size of the array and the maximum number of distinct values.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print one integer: the number of subarrays with at most k distinct values.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ k ≤ n
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
5 2
1 2 1 3 4

Output:
10
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n² × k)
**Description**: Check all possible subarrays to count those with at most k distinct values.

```python
def subarray_distinct_naive(n, k, arr):
    count = 0
    
    for i in range(n):
        distinct_values = set()
        for j in range(i, n):
            distinct_values.add(arr[j])
            if len(distinct_values) <= k:
                count += 1
            else:
                break
    
    return count
```

**Why this is inefficient**: Quadratic time complexity and inefficient distinct value counting.

### Improvement 1: Sliding Window with Hash Map - O(n)
**Description**: Use sliding window technique with hash map to track distinct values efficiently.

```python
def subarray_distinct_sliding_window(n, k, arr):
    from collections import defaultdict
    
    left = 0
    count = 0
    distinct_count = defaultdict(int)
    distinct_values = 0
    
    for right in range(n):
        # Add current element
        if distinct_count[arr[right]] == 0:
            distinct_values += 1
        distinct_count[arr[right]] += 1
        
        # Shrink window if we have more than k distinct values
        while distinct_values > k:
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                distinct_values -= 1
            left += 1
        
        # Add all valid subarrays ending at right
        count += right - left + 1
    
    return count
```

**Why this improvement works**: Sliding window efficiently maintains the constraint of at most k distinct values.

### Alternative: Two Pointers with Counter - O(n)
**Description**: Use two pointers with a counter to track distinct values.

```python
def subarray_distinct_two_pointers(n, k, arr):
    from collections import Counter
    
    left = 0
    count = 0
    counter = Counter()
    
    for right in range(n):
        counter[arr[right]] += 1
        
        while len(counter) > k:
            counter[arr[left]] -= 1
            if counter[arr[left]] == 0:
                del counter[arr[left]]
            left += 1
        
        count += right - left + 1
    
    return count
```

**Why this works**: Two pointers efficiently maintain the window with at most k distinct values.

## Final Optimal Solution

```python
n, k = map(int, input().split())
arr = list(map(int, input().split()))

def subarray_distinct_sliding_window(n, k, arr):
    from collections import defaultdict
    
    left = 0
    count = 0
    distinct_count = defaultdict(int)
    distinct_values = 0
    
    for right in range(n):
        # Add current element
        if distinct_count[arr[right]] == 0:
            distinct_values += 1
        distinct_count[arr[right]] += 1
        
        # Shrink window if we have more than k distinct values
        while distinct_values > k:
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                distinct_values -= 1
            left += 1
        
        # Add all valid subarrays ending at right
        count += right - left + 1
    
    return count

result = subarray_distinct_sliding_window(n, k, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n² × k) | O(k) | Check all subarrays |
| Sliding Window | O(n) | O(k) | Use hash map for distinct values |
| Two Pointers | O(n) | O(k) | Use counter for frequency |

## Key Insights for Other Problems

### 1. **Distinct Value Problems**
**Principle**: Use sliding window with hash map to efficiently track distinct values in subarrays.
**Applicable to**:
- Distinct value problems
- Subarray problems
- Window-based problems
- Hash map applications

**Example Problems**:
- Distinct value problems
- Subarray problems
- Window-based problems
- Hash map applications

### 2. **Sliding Window Technique**
**Principle**: Use sliding window to maintain constraints while expanding and contracting the window.
**Applicable to**:
- Window-based problems
- Subarray problems
- Two pointer problems
- Algorithm design

**Example Problems**:
- Window-based problems
- Subarray problems
- Two pointer problems
- Algorithm design

### 3. **Hash Map for Frequency**
**Principle**: Use hash map to efficiently track frequency of elements in the current window.
**Applicable to**:
- Frequency counting
- Hash map applications
- Algorithm design
- Problem solving

**Example Problems**:
- Frequency counting
- Hash map applications
- Algorithm design
- Problem solving

### 4. **Two Pointer Applications**
**Principle**: Use two pointers to maintain a valid window that satisfies the given constraints.
**Applicable to**:
- Two pointer problems
- Window-based problems
- Subarray problems
- Algorithm design

**Example Problems**:
- Two pointer problems
- Window-based problems
- Subarray problems
- Algorithm design

## Notable Techniques

### 1. **Sliding Window with Hash Map Pattern**
```python
def sliding_window_distinct_values(arr, k):
    from collections import defaultdict
    
    left = 0
    count = 0
    distinct_count = defaultdict(int)
    distinct_values = 0
    
    for right in range(len(arr)):
        # Add current element
        if distinct_count[arr[right]] == 0:
            distinct_values += 1
        distinct_count[arr[right]] += 1
        
        # Shrink window if needed
        while distinct_values > k:
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                distinct_values -= 1
            left += 1
        
        # Count valid subarrays
        count += right - left + 1
    
    return count
```

### 2. **Two Pointers with Counter Pattern**
```python
def two_pointers_distinct_values(arr, k):
    from collections import Counter
    
    left = 0
    count = 0
    counter = Counter()
    
    for right in range(len(arr)):
        counter[arr[right]] += 1
        
        while len(counter) > k:
            counter[arr[left]] -= 1
            if counter[arr[left]] == 0:
                del counter[arr[left]]
            left += 1
        
        count += right - left + 1
    
    return count
```

### 3. **Window Maintenance Pattern**
```python
def maintain_window_constraint(arr, constraint_func):
    left = 0
    result = 0
    
    for right in range(len(arr)):
        # Add element to window
        # Update constraint
        
        # Shrink window while constraint is violated
        while not constraint_func(left, right):
            # Remove left element
            left += 1
        
        # Process valid window
        result += right - left + 1
    
    return result
```

## Edge Cases to Remember

1. **k = 1**: Only single elements are valid
2. **k = n**: All subarrays are valid
3. **All same elements**: All subarrays are valid
4. **All distinct elements**: Limited by k
5. **Empty array**: Handle appropriately

## Problem-Solving Framework

1. **Identify window nature**: This is a sliding window problem with distinct value constraint
2. **Choose approach**: Use sliding window with hash map for efficiency
3. **Track distinct values**: Maintain count of distinct values in current window
4. **Maintain constraint**: Shrink window when distinct values exceed k
5. **Count subarrays**: Add all valid subarrays ending at current position

---

*This analysis shows how to efficiently count subarrays with at most k distinct values using sliding window technique.*"