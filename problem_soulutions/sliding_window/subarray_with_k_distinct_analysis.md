---
layout: simple
title: "Subarray with K Distinct
permalink: /problem_soulutions/sliding_window/subarray_with_k_distinct_analysis/"
---


# Subarray with K Distinct

## Problem Statement
Given an array of n integers, your task is to find the number of subarrays with exactly k distinct values.

### Input
The first input line has two integers n and k: the size of the array and the required number of distinct values.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print one integer: the number of subarrays with exactly k distinct values.

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
3
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n² × k)
**Description**: Check all possible subarrays to count those with exactly k distinct values.

```python
def subarray_k_distinct_naive(n, k, arr):
    count = 0
    
    for i in range(n):
        distinct_values = set()
        for j in range(i, n):
            distinct_values.add(arr[j])
            if len(distinct_values) == k:
                count += 1
            elif len(distinct_values) > k:
                break
    
    return count
```

**Why this is inefficient**: Quadratic time complexity and inefficient distinct value counting.

### Improvement 1: Sliding Window with Hash Map - O(n)
**Description**: Use sliding window technique with hash map to track distinct values efficiently.

```python
def subarray_k_distinct_sliding_window(n, k, arr):
    from collections import defaultdict
    
    def count_subarrays_with_at_most_k_distinct(k_limit):
        left = 0
        count = 0
        distinct_count = defaultdict(int)
        distinct_values = 0
        
        for right in range(n):
            # Add current element
            if distinct_count[arr[right]] == 0:
                distinct_values += 1
            distinct_count[arr[right]] += 1
            
            # Shrink window if we have more than k_limit distinct values
            while distinct_values > k_limit:
                distinct_count[arr[left]] -= 1
                if distinct_count[arr[left]] == 0:
                    distinct_values -= 1
                left += 1
            
            # Add all valid subarrays ending at right
            count += right - left + 1
        
        return count
    
    # Count subarrays with at most k distinct - count subarrays with at most (k-1) distinct
    return count_subarrays_with_at_most_k_distinct(k) - count_subarrays_with_at_most_k_distinct(k - 1)
```

**Why this improvement works**: Use inclusion-exclusion principle to find exactly k distinct values.

## Final Optimal Solution

```python
n, k = map(int, input().split())
arr = list(map(int, input().split()))

def subarray_k_distinct_sliding_window(n, k, arr):
    from collections import defaultdict
    
    def count_subarrays_with_at_most_k_distinct(k_limit):
        left = 0
        count = 0
        distinct_count = defaultdict(int)
        distinct_values = 0
        
        for right in range(n):
            # Add current element
            if distinct_count[arr[right]] == 0:
                distinct_values += 1
            distinct_count[arr[right]] += 1
            
            # Shrink window if we have more than k_limit distinct values
            while distinct_values > k_limit:
                distinct_count[arr[left]] -= 1
                if distinct_count[arr[left]] == 0:
                    distinct_values -= 1
                left += 1
            
            # Add all valid subarrays ending at right
            count += right - left + 1
        
        return count
    
    # Count subarrays with at most k distinct - count subarrays with at most (k-1) distinct
    return count_subarrays_with_at_most_k_distinct(k) - count_subarrays_with_at_most_k_distinct(k - 1)

result = subarray_k_distinct_sliding_window(n, k, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n² × k) | O(k) | Check all subarrays |
| Sliding Window | O(n) | O(k) | Use inclusion-exclusion principle |

## Key Insights for Other Problems

### 1. **Exactly K Distinct Problems**
**Principle**: Use inclusion-exclusion principle to find exactly k distinct values.
**Applicable to**: Exactly k distinct problems, subarray problems, inclusion-exclusion principle

### 2. **Inclusion-Exclusion Principle**"
**Principle**: Count "at most k" minus "at most k-1" to get "exactly k".
**Applicable to**: Counting problems, inclusion-exclusion principle, algorithm design

### 3. **Sliding Window Technique**
**Principle**: Use sliding window to maintain constraints while expanding and contracting the window.
**Applicable to**: Window-based problems, subarray problems, two pointer problems

## Notable Techniques

### 1. **Inclusion-Exclusion Pattern**
```python
def exactly_k_distinct(arr, k):
    def at_most_k_distinct(k_limit):
        # Count subarrays with at most k_limit distinct values
        pass
    
    return at_most_k_distinct(k) - at_most_k_distinct(k - 1)
```

### 2. **Sliding Window with Hash Map Pattern**
```python
def sliding_window_k_distinct(arr, k):
    from collections import defaultdict
    
    def count_at_most_k_distinct(k_limit):
        left = 0
        count = 0
        distinct_count = defaultdict(int)
        distinct_values = 0
        
        for right in range(len(arr)):
            if distinct_count[arr[right]] == 0:
                distinct_values += 1
            distinct_count[arr[right]] += 1
            
            while distinct_values > k_limit:
                distinct_count[arr[left]] -= 1
                if distinct_count[arr[left]] == 0:
                    distinct_values -= 1
                left += 1
            
            count += right - left + 1
        
        return count
    
    return count_at_most_k_distinct(k) - count_at_most_k_distinct(k - 1)
```

## Problem-Solving Framework

1. **Identify exactly k nature**: This is an exactly k distinct problem
2. **Choose approach**: Use inclusion-exclusion principle
3. **Count at most k**: Count subarrays with at most k distinct values
4. **Count at most k-1**: Count subarrays with at most k-1 distinct values
5. **Return difference**: Return exactly k = at most k - at most k-1

---

*This analysis shows how to efficiently count subarrays with exactly k distinct values using inclusion-exclusion principle and sliding window technique.* 