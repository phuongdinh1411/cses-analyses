# CSES Distinct Values Subarrays - Problem Analysis

## Problem Statement
Given an array of n integers, find the number of subarrays that contain exactly k distinct values.

### Input
The first input line has two integers n and k: the size of the array and the number of distinct values.
The second line has n integers a1,a2,…,an: the array.

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
1 2 1 2 3

Output:
8
```

## Solution Progression

### Approach 1: Brute Force - O(n²)
**Description**: Check all possible subarrays and count distinct values.

```python
def distinct_values_subarrays_naive(n, k, arr):
    count = 0
    
    for start in range(n):
        distinct = set()
        for end in range(start, n):
            distinct.add(arr[end])
            if len(distinct) == k:
                count += 1
            elif len(distinct) > k:
                break
    
    return count
```

**Why this is inefficient**: We check O(n²) subarrays, leading to O(n²) time complexity.

### Improvement 1: Sliding Window - O(n)
**Description**: Use sliding window technique to count subarrays with exactly k distinct values.

```python
def distinct_values_subarrays_optimized(n, k, arr):
    def count_at_most_k_distinct(k):
        count = 0
        left = 0
        freq = {}
        
        for right in range(n):
            freq[arr[right]] = freq.get(arr[right], 0) + 1
            
            while len(freq) > k:
                freq[arr[left]] -= 1
                if freq[arr[left]] == 0:
                    del freq[arr[left]]
                left += 1
            
            count += right - left + 1
        
        return count
    
    # Number of subarrays with exactly k distinct = 
    # Number of subarrays with at most k distinct - Number of subarrays with at most k-1 distinct
    return count_at_most_k_distinct(k) - count_at_most_k_distinct(k - 1)
```

**Why this improvement works**: We use the inclusion-exclusion principle. The number of subarrays with exactly k distinct values equals the number of subarrays with at most k distinct values minus the number of subarrays with at most k-1 distinct values.

## Final Optimal Solution

```python
n, k = map(int, input().split())
arr = list(map(int, input().split()))

def count_subarrays_with_k_distinct(n, k, arr):
    def count_at_most_k_distinct(k):
        count = 0
        left = 0
        freq = {}
        
        for right in range(n):
            freq[arr[right]] = freq.get(arr[right], 0) + 1
            
            while len(freq) > k:
                freq[arr[left]] -= 1
                if freq[arr[left]] == 0:
                    del freq[arr[left]]
                left += 1
            
            count += right - left + 1
        
        return count
    
    # Number of subarrays with exactly k distinct = 
    # Number of subarrays with at most k distinct - Number of subarrays with at most k-1 distinct
    return count_at_most_k_distinct(k) - count_at_most_k_distinct(k - 1)

result = count_subarrays_with_k_distinct(n, k, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check all subarrays |
| Sliding Window | O(n) | O(n) | Use inclusion-exclusion principle |

## Key Insights for Other Problems

### 1. **Subarray Counting Problems**
**Principle**: Use sliding window with inclusion-exclusion principle for exact counting.
**Applicable to**: Subarray problems, counting problems, window problems

### 2. **Inclusion-Exclusion Principle**
**Principle**: Count "at most k" and subtract "at most k-1" to get "exactly k".
**Applicable to**: Counting problems, range problems, exact value problems

### 3. **Sliding Window with Frequency**
**Principle**: Maintain frequency count and adjust window boundaries based on distinct count.
**Applicable to**: Window problems, frequency problems, distinct value problems

## Notable Techniques

### 1. **Sliding Window with Frequency Tracking**
```python
def sliding_window_with_frequency(arr, k):
    def count_at_most_k(k):
        count = 0
        left = 0
        freq = {}
        
        for right in range(len(arr)):
            freq[arr[right]] = freq.get(arr[right], 0) + 1
            
            while len(freq) > k:
                freq[arr[left]] -= 1
                if freq[arr[left]] == 0:
                    del freq[arr[left]]
                left += 1
            
            count += right - left + 1
        
        return count
    
    return count_at_most_k(k) - count_at_most_k(k - 1)
```

### 2. **Frequency Management**
```python
def manage_frequency(freq, element, delta):
    freq[element] = freq.get(element, 0) + delta
    if freq[element] == 0:
        del freq[element]
    
    return freq
```

### 3. **Window Boundary Adjustment**
```python
def adjust_window_boundaries(arr, freq, left, k):
    while len(freq) > k:
        freq[arr[left]] -= 1
        if freq[arr[left]] == 0:
            del freq[arr[left]]
        left += 1
    
    return left
```

## Problem-Solving Framework

1. **Identify problem type**: This is a subarray counting problem with exact distinct value requirement
2. **Choose approach**: Use sliding window with inclusion-exclusion principle
3. **Implement at-most-k function**: Count subarrays with at most k distinct values
4. **Apply inclusion-exclusion**: Subtract at-most-(k-1) from at-most-k
5. **Manage frequency**: Track element frequencies in the window
6. **Adjust boundaries**: Move left pointer when distinct count exceeds k
7. **Return result**: Output the count of subarrays with exactly k distinct values

---

*This analysis shows how to efficiently count subarrays with exactly k distinct values using sliding window and inclusion-exclusion principle.* 