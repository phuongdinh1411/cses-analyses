# CSES Subarray Divisibility - Problem Analysis

## Problem Statement
Given an array of n integers and a positive integer k, find the number of subarrays whose sum is divisible by k.

### Input
The first input line has two integers n and k: the size of the array and the divisor.
The second line has n integers a1,a2,…,an: the array.

### Output
Print one integer: the number of subarrays with sum divisible by k.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ k ≤ 10^9
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
5 3
1 2 3 4 5

Output:
4
```

## Solution Progression

### Approach 1: Brute Force - O(n²)
**Description**: Check all possible subarrays and count those with sum divisible by k.

```python
def subarray_divisibility_naive(n, k, arr):
    count = 0
    
    for start in range(n):
        current_sum = 0
        for end in range(start, n):
            current_sum += arr[end]
            if current_sum % k == 0:
                count += 1
    
    return count
```

**Why this is inefficient**: We check all O(n²) subarrays, leading to quadratic time complexity.

### Improvement 1: Prefix Sum with Modulo - O(n)
**Description**: Use prefix sum with modulo arithmetic to count subarrays divisible by k.

```python
def subarray_divisibility_optimized(n, k, arr):
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}  # Count of prefix sums with each remainder
    
    for i in range(n):
        prefix_sum += arr[i]
        remainder = prefix_sum % k
        
        # If we have seen this remainder before, we found subarrays divisible by k
        if remainder in mod_count:
            count += mod_count[remainder]
        
        # Update count of current remainder
        mod_count[remainder] = mod_count.get(remainder, 0) + 1
    
    return count
```

**Why this improvement works**: We use prefix sum with modulo arithmetic. For each position, we check if there exists a previous prefix sum with the same remainder when divided by k. This gives us the count of subarrays ending at the current position with sum divisible by k.

## Final Optimal Solution

```python
n, k = map(int, input().split())
arr = list(map(int, input().split()))

def count_divisible_subarrays(n, k, arr):
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}  # Count of prefix sums with each remainder
    
    for i in range(n):
        prefix_sum += arr[i]
        remainder = prefix_sum % k
        
        # If we have seen this remainder before, we found subarrays divisible by k
        if remainder in mod_count:
            count += mod_count[remainder]
        
        # Update count of current remainder
        mod_count[remainder] = mod_count.get(remainder, 0) + 1
    
    return count

result = count_divisible_subarrays(n, k, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all subarrays |
| Prefix Sum with Modulo | O(n) | O(k) | Use modulo arithmetic |

## Key Insights for Other Problems

### 1. **Divisibility Problems**
**Principle**: Use modulo arithmetic to efficiently check divisibility conditions.
**Applicable to**: Divisibility problems, modulo problems, remainder problems

### 2. **Prefix Sum with Modulo**
**Principle**: Use prefix sum with modulo to find subarrays with specific remainder properties.
**Applicable to**: Subarray problems, modulo problems, remainder problems

### 3. **Remainder Counting**
**Principle**: Count occurrences of remainders to find subarrays with specific divisibility properties.
**Applicable to**: Counting problems, remainder problems, modulo problems

## Notable Techniques

### 1. **Modulo Arithmetic**
```python
def modulo_arithmetic(arr, k):
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}
    
    for num in arr:
        prefix_sum += num
        remainder = prefix_sum % k
        
        if remainder in mod_count:
            count += mod_count[remainder]
        
        mod_count[remainder] = mod_count.get(remainder, 0) + 1
    
    return count
```

### 2. **Remainder Tracking**
```python
def track_remainders(arr, k):
    n = len(arr)
    count = 0
    prefix_sum = 0
    remainder_freq = {0: 1}
    
    for i in range(n):
        prefix_sum += arr[i]
        remainder = prefix_sum % k
        
        # Count subarrays ending at i with sum divisible by k
        if remainder in remainder_freq:
            count += remainder_freq[remainder]
        
        # Update frequency of current remainder
        remainder_freq[remainder] = remainder_freq.get(remainder, 0) + 1
    
    return count
```

### 3. **Divisibility Check**
```python
def check_divisibility(prefix_sum, k):
    return prefix_sum % k == 0
```

## Problem-Solving Framework

1. **Identify problem type**: This is a subarray divisibility problem with modulo arithmetic
2. **Choose approach**: Use prefix sum with modulo arithmetic for efficiency
3. **Initialize variables**: Start with prefix_sum = 0 and mod_count = {0: 1}
4. **Process elements**: For each element, update prefix sum
5. **Calculate remainder**: Find remainder when prefix sum is divided by k
6. **Count subarrays**: Add frequency of current remainder to result
7. **Update frequency**: Increment frequency of current remainder
8. **Return result**: Output the total count of divisible subarrays

---

*This analysis shows how to efficiently count subarrays with sum divisible by k using modulo arithmetic.* 