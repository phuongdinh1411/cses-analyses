# CSES Subarray Sums II - Problem Analysis

## Problem Statement
Given an array of n integers and a target sum x, find the number of subarrays that have sum x. The array may contain negative numbers.

### Input
The first input line has two integers n and x: the size of the array and the target sum.
The second line has n integers a1,a2,…,an: the array.

### Output
Print one integer: the number of subarrays with sum x.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ x ≤ 10^9
- -10^9 ≤ ai ≤ 10^9

### Example
```
Input:
5 7
2 -1 3 5 -2

Output:
2
```

## Solution Progression

### Approach 1: Brute Force - O(n²)
**Description**: Check all possible subarrays and count those with sum x.

```python
def subarray_sums_ii_naive(n, x, arr):
    count = 0
    
    for start in range(n):
        current_sum = 0
        for end in range(start, n):
            current_sum += arr[end]
            if current_sum == x:
                count += 1
    
    return count
```

**Why this is inefficient**: We check all O(n²) subarrays, leading to quadratic time complexity.

### Improvement 1: Prefix Sum with Hash Map - O(n)
**Description**: Use prefix sum and hash map to count subarrays with sum x.

```python
def subarray_sums_ii_optimized(n, x, arr):
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}  # Count of prefix sums
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # If prefix_sum - x exists, we found a subarray with sum x
        if prefix_sum - x in sum_count:
            count += sum_count[prefix_sum - x]
        
        # Update count of current prefix sum
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count
```

**Why this improvement works**: We use prefix sum to efficiently calculate subarray sums. For each position, we check if there exists a previous prefix sum such that the difference equals x. This gives us the count of subarrays ending at the current position with sum x.

## Final Optimal Solution

```python
n, x = map(int, input().split())
arr = list(map(int, input().split()))

def count_subarrays_with_sum(n, x, arr):
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}  # Count of prefix sums
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # If prefix_sum - x exists, we found a subarray with sum x
        if prefix_sum - x in sum_count:
            count += sum_count[prefix_sum - x]
        
        # Update count of current prefix sum
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count

result = count_subarrays_with_sum(n, x, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all subarrays |
| Prefix Sum with Hash Map | O(n) | O(n) | Use prefix sum and hash map |

## Key Insights for Other Problems

### 1. **Subarray Sum Problems**
**Principle**: Use prefix sum and hash map to efficiently count subarrays with target sum.
**Applicable to**: Subarray problems, sum problems, counting problems

### 2. **Prefix Sum Technique**
**Principle**: Use prefix sum to calculate subarray sums in O(1) time.
**Applicable to**: Range sum problems, subarray problems, sum problems

### 3. **Hash Map Counting**
**Principle**: Use hash map to count occurrences of prefix sums for efficient lookup.
**Applicable to**: Counting problems, hash map problems, frequency problems

## Notable Techniques

### 1. **Prefix Sum with Hash Map**
```python
def prefix_sum_with_hashmap(arr, target):
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}
    
    for num in arr:
        prefix_sum += num
        
        if prefix_sum - target in sum_count:
            count += sum_count[prefix_sum - target]
        
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count
```

### 2. **Subarray Sum Counting**
```python
def count_subarray_sums(arr, target):
    n = len(arr)
    count = 0
    prefix_sum = 0
    sum_freq = {0: 1}
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # Check if we can form a subarray ending at i with sum target
        if prefix_sum - target in sum_freq:
            count += sum_freq[prefix_sum - target]
        
        # Update frequency of current prefix sum
        sum_freq[prefix_sum] = sum_freq.get(prefix_sum, 0) + 1
    
    return count
```

### 3. **Hash Map Management**
```python
def manage_sum_frequency(sum_freq, current_sum):
    # Update frequency of current prefix sum
    sum_freq[current_sum] = sum_freq.get(current_sum, 0) + 1
    return sum_freq
```

## Problem-Solving Framework

1. **Identify problem type**: This is a subarray sum counting problem
2. **Choose approach**: Use prefix sum with hash map for efficiency
3. **Initialize variables**: Start with prefix_sum = 0 and hash map {0: 1}
4. **Process elements**: For each element, update prefix sum
5. **Check for target**: Look for prefix_sum - target in hash map
6. **Update count**: Add frequency of prefix_sum - target to result
7. **Update hash map**: Increment frequency of current prefix sum
8. **Return result**: Output the total count of subarrays

---

*This analysis shows how to efficiently count subarrays with a target sum using prefix sum and hash map technique.* 