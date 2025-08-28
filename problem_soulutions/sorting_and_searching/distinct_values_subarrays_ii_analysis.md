---
layout: simple
title: "Distinct Values Subarrays II
permalink: /problem_soulutions/sorting_and_searching/distinct_values_subarrays_ii_analysis/"
---


# Distinct Values Subarrays II

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
def distinct_values_subarrays_ii_naive(n, k, arr):
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

**Why this is inefficient**: We check all O(n²) subarrays, leading to quadratic time complexity.

### Improvement 1: Sliding Window - O(n)
**Description**: Use sliding window technique to count subarrays with exactly k distinct values.

```python
def distinct_values_subarrays_ii_optimized(n, k, arr):
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

### 2. **Inclusion-Exclusion Principle**"
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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Distinct Values**
**Problem**: Each distinct value has a weight. Find subarrays with exactly k distinct values and maximum total weight.
```python
def weighted_distinct_values_subarrays(arr, k, weights):
    # weights[i] = weight of value arr[i]
    n = len(arr)
    max_weight = 0
    
    def count_weighted_at_most_k(k):
        count = 0
        left = 0
        freq = {}
        current_weight = 0
        
        for right in range(n):
            val = arr[right]
            if val not in freq:
                freq[val] = 0
                current_weight += weights[right]
            freq[val] += 1
            
            while len(freq) > k:
                freq[arr[left]] -= 1
                if freq[arr[left]] == 0:
                    del freq[arr[left]]
                    current_weight -= weights[left]
                left += 1
            
            if len(freq) == k:
                count = max(count, current_weight)
        
        return count
    
    return count_weighted_at_most_k(k)
```

#### **Variation 2: Range-Based Distinct Values**
**Problem**: Find subarrays with exactly k distinct values where all values are within a given range [min_val, max_val].
```python
def range_based_distinct_values(arr, k, min_val, max_val):
    n = len(arr)
    
    def count_in_range(k):
        count = 0
        left = 0
        freq = {}
        
        for right in range(n):
            val = arr[right]
            if min_val <= val <= max_val:
                freq[val] = freq.get(val, 0) + 1
                
                while len(freq) > k:
                    freq[arr[left]] -= 1
                    if freq[arr[left]] == 0:
                        del freq[arr[left]]
                    left += 1
                
                count += right - left + 1
            else:
                # Reset window when value is out of range
                left = right + 1
                freq.clear()
        
        return count
    
    return count_in_range(k) - count_in_range(k - 1)
```

#### **Variation 3: Dynamic k Values**
**Problem**: Given multiple queries with different k values, find subarrays with exactly k distinct values for each query.
```python
def dynamic_k_distinct_values(arr, queries):
    # queries = list of k values
    n = len(arr)
    results = {}
    
    # Precompute for all possible k values
    for k in set(queries):
        results[k] = count_subarrays_with_k_distinct(n, k, arr)
    
    return [results[k] for k in queries]
```

#### **Variation 4: Minimum Length Constraint**
**Problem**: Find subarrays with exactly k distinct values and minimum length L.
```python
def min_length_distinct_values(arr, k, min_length):
    n = len(arr)
    
    def count_with_min_length(k):
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
            
            # Only count if window length >= min_length
            if right - left + 1 >= min_length:
                count += right - left + 1 - min_length + 1
        
        return count
    
    return count_with_min_length(k) - count_with_min_length(k - 1)
```

#### **Variation 5: Circular Array**
**Problem**: Find subarrays with exactly k distinct values in a circular array.
```python
def circular_distinct_values(arr, k):
    n = len(arr)
    # Extend array to handle circular case
    extended = arr + arr
    
    def count_circular(k):
        count = 0
        left = 0
        freq = {}
        
        for right in range(2 * n):
            freq[extended[right]] = freq.get(extended[right], 0) + 1
            
            while len(freq) > k:
                freq[extended[left]] -= 1
                if freq[extended[left]] == 0:
                    del freq[extended[left]]
                left += 1
            
            # Only count if window doesn't wrap around more than once
            if right - left + 1 <= n:
                count += right - left + 1
        
        return count
    
    return count_circular(k) - count_circular(k - 1)
```

### 🔗 **Related Problems & Concepts**

#### **1. Subarray Problems**
- **Subarray Sum**: Find subarrays with given sum
- **Subarray XOR**: Find subarrays with given XOR value
- **Subarray Product**: Find subarrays with given product
- **Subarray Median**: Find subarrays with given median

#### **2. Sliding Window Problems**
- **Longest Substring Without Repeating**: Find longest substring with unique characters
- **Minimum Window Substring**: Find smallest window containing all characters
- **Subarray with K Different Integers**: Similar to original problem
- **Fruit Into Baskets**: Maximum fruits in two baskets

#### **3. Counting Problems**
- **Count Subarrays with Sum**: Count subarrays with given sum
- **Count Subarrays with XOR**: Count subarrays with given XOR
- **Count Subarrays with Product**: Count subarrays with given product
- **Count Subarrays with Range**: Count subarrays in given range

#### **4. Frequency Problems**
- **Most Frequent Element**: Find most frequent element in subarray
- **Frequency Queries**: Answer frequency-based queries
- **Mode in Subarray**: Find mode of subarray
- **Frequency Distribution**: Analyze frequency distribution

#### **5. Optimization Problems**
- **Maximum Subarray**: Find subarray with maximum sum
- **Minimum Subarray**: Find subarray with minimum sum
- **Optimal Subarray**: Find subarray optimizing given criteria
- **Constrained Subarray**: Find subarray satisfying constraints

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = count_subarrays_with_k_distinct(n, k, arr)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute for different ranges
def precompute_distinct_counts(arr):
    n = len(arr)
    # Precompute for all possible ranges and k values
    dp = {}
    
    for start in range(n):
        for end in range(start, n):
            distinct = len(set(arr[start:end+1]))
            if distinct not in dp:
                dp[distinct] = []
            dp[distinct].append((start, end))
    
    return dp

# Answer range queries efficiently
def range_query(dp, k, start, end):
    if k not in dp:
        return 0
    
    count = 0
    for s, e in dp[k]:
        if s >= start and e <= end:
            count += 1
    
    return count
```

#### **3. Interactive Problems**
```python
# Interactive version where k is revealed gradually
def interactive_distinct_values(arr):
    n = len(arr)
    print(f"Array length: {n}")
    
    while True:
        k = int(input("Enter k (or -1 to exit): "))
        if k == -1:
            break
        
        if k < 1 or k > n:
            print("Invalid k value")
            continue
        
        result = count_subarrays_with_k_distinct(n, k, arr)
        print(f"Subarrays with exactly {k} distinct values: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Inclusion-Exclusion Principle**: Mathematical foundation for exact counting
- **Binomial Coefficients**: Counting combinations in subarrays
- **Permutations**: Arrangements of distinct values
- **Partitions**: Ways to partition array into subarrays

#### **2. Probability Theory**
- **Expected Value**: Expected number of subarrays with k distinct values
- **Probability Distribution**: Distribution of distinct value counts
- **Random Sampling**: Sampling subarrays randomly
- **Statistical Analysis**: Statistical properties of subarrays

#### **3. Number Theory**
- **Prime Factorization**: Distinct prime factors in subarrays
- **GCD/LCM**: Greatest common divisor and least common multiple
- **Modular Arithmetic**: Subarrays with specific modular properties
- **Number Sequences**: Special number sequences in subarrays

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Sliding Window Algorithm**: Core technique for subarray problems
- **Two Pointers Technique**: Efficient array traversal
- **Frequency Counting**: Tracking element frequencies
- **Inclusion-Exclusion**: Mathematical principle for exact counting

#### **2. Mathematical Concepts**
- **Set Theory**: Understanding distinct values as sets
- **Combinatorics**: Counting principles and techniques
- **Optimization**: Finding optimal subarrays
- **Complexity Analysis**: Time and space complexity analysis

#### **3. Programming Concepts**
- **Hash Maps**: Efficient frequency tracking
- **Dynamic Programming**: Alternative approach for some variations
- **Binary Search**: For optimization problems
- **Data Structures**: Efficient storage and retrieval

---

*This analysis demonstrates efficient subarray counting techniques and shows various extensions for distinct value problems.* 