---
layout: simple
title: "Subarray with K Distinct Values"
permalink: /problem_soulutions/sliding_window/subarray_with_k_distinct_analysis
---

# Subarray with K Distinct Values

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand sliding window problems with exact distinct value constraints and subarray counting
- Apply sliding window technique to count subarrays with exactly k distinct values
- Implement efficient sliding window algorithms with O(n) time complexity for exact distinct value problems
- Optimize sliding window problems using hash maps and distinct value tracking
- Handle edge cases in sliding window problems (k=1, k=n, all distinct values, no solution)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sliding window technique, two-pointer technique, exact distinct value counting, hash map usage, subarray counting
- **Data Structures**: Hash maps, distinct value tracking, sliding window tracking, frequency tracking, window boundaries
- **Mathematical Concepts**: Distinct value theory, subarray counting, window mathematics, counting problems, exact counting
- **Programming Skills**: Hash map implementation, distinct value tracking, window sliding, frequency counting, algorithm implementation
- **Related Problems**: Subarray Distinct Values (at most k distinct), Longest Substring Without Repeating Characters (distinct characters), Sliding window problems

## 📋 Problem Description

Given an array of n integers, find the number of subarrays with exactly k distinct values.

**Input**: 
- First line: Two integers n and k (array size and required distinct values)
- Second line: n integers a₁, a₂, ..., aₙ (array contents)

**Output**: 
- One integer: the number of subarrays with exactly k distinct values

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ k ≤ n  
- 1 ≤ aᵢ ≤ 10⁹

**Example**:
```
Input:
5 2
1 2 1 3 4

Output:
3
```

**Explanation**: The subarrays with exactly 2 distinct values are:
- [1, 2] → distinct values: {1, 2}
- [2, 1] → distinct values: {1, 2}  
- [1, 3] → distinct values: {1, 3}

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count subarrays with exactly k distinct values
- **Key Insight**: Need to track distinct values in sliding windows
- **Challenge**: Efficiently count "exactly k" vs "at most k"

### Step 2: Brute Force Approach
**Check all possible subarrays and count distinct values:**

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

**Complexity**: O(n² × k) - too slow for large arrays

### Step 3: Optimization
**Use sliding window with inclusion-exclusion principle:**

```python
def subarray_k_distinct_optimized(n, k, arr):
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
    
    # Exactly k = At most k - At most (k-1)
    return count_subarrays_with_at_most_k_distinct(k) - count_subarrays_with_at_most_k_distinct(k - 1)
```

**Key Insight**: Use inclusion-exclusion: exactly k = at most k - at most (k-1)

### Step 4: Complete Solution

```python
def solve_subarray_k_distinct():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = count_subarrays_with_exactly_k_distinct(n, k, arr)
    print(result)

def count_subarrays_with_exactly_k_distinct(n, k, arr):
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
    
    # Exactly k = At most k - At most (k-1)
    return count_subarrays_with_at_most_k_distinct(k) - count_subarrays_with_at_most_k_distinct(k - 1)

if __name__ == "__main__":
    solve_subarray_k_distinct()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 2, [1, 2, 1, 3, 4]), 3),
        ((4, 1, [1, 1, 1, 1]), 4),
        ((3, 3, [1, 2, 3]), 1),
        ((2, 2, [1, 2]), 1),
        ((1, 1, [1]), 1),
        ((4, 2, [1, 2, 1, 2]), 6),
    ]
    
    for (n, k, arr), expected in test_cases:
        result = count_subarrays_with_exactly_k_distinct(n, k, arr)
        print(f"n={n}, k={k}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def count_subarrays_with_exactly_k_distinct(n, k, arr):
    from collections import defaultdict
    
    def count_subarrays_with_at_most_k_distinct(k_limit):
        left = 0
        count = 0
        distinct_count = defaultdict(int)
        distinct_values = 0
        
        for right in range(n):
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
    
    return count_subarrays_with_at_most_k_distinct(k) - count_subarrays_with_at_most_k_distinct(k - 1)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with sliding window
- **Space**: O(k) - hash map to store distinct value counts

### Why This Solution Works
- **Sliding Window**: Efficiently maintains window with at most k distinct values
- **Inclusion-Exclusion**: Converts "exactly k" to "at most k" - "at most k-1"
- **Hash Map**: Tracks frequency of each distinct value
- **Optimal Algorithm**: Best known approach for this problem

## 🎨 Visual Example

### Input Example
```
Input: n=5, k=2, arr=[1, 2, 1, 3, 4]
Output: 3 (subarrays with exactly 2 distinct values)
```

### Array Visualization
```
Array: [1, 2, 1, 3, 4]
Index:  0  1  2  3  4
```

### Subarray Analysis
```
Target: exactly k=2 distinct values

Subarray [0:2] = [1, 2] → distinct: {1, 2} → count = 2 ✓
Subarray [1:3] = [2, 1] → distinct: {1, 2} → count = 2 ✓  
Subarray [2:4] = [1, 3] → distinct: {1, 3} → count = 2 ✓
Subarray [0:3] = [1, 2, 1] → distinct: {1, 2} → count = 2 ✓
Subarray [1:4] = [2, 1, 3] → distinct: {1, 2, 3} → count = 3 ✗
Subarray [0:4] = [1, 2, 1, 3] → distinct: {1, 2, 3} → count = 3 ✗
Subarray [2:5] = [1, 3, 4] → distinct: {1, 3, 4} → count = 3 ✗

Valid subarrays: [1,2], [2,1], [1,3]
Total: 3
```

### Inclusion-Exclusion Approach
```
Count exactly k = Count at most k - Count at most (k-1)

For k=2:
Count at most 2 - Count at most 1 = Count exactly 2

Count at most 2:
- [1] → 1 distinct ✓
- [1,2] → 2 distinct ✓
- [1,2,1] → 2 distinct ✓
- [1,2,1,3] → 3 distinct ✗
- [2] → 1 distinct ✓
- [2,1] → 2 distinct ✓
- [2,1,3] → 3 distinct ✗
- [1] → 1 distinct ✓
- [1,3] → 2 distinct ✓
- [1,3,4] → 3 distinct ✗
- [3] → 1 distinct ✓
- [3,4] → 2 distinct ✓
- [4] → 1 distinct ✓

Count at most 2: 8

Count at most 1:
- [1] → 1 distinct ✓
- [2] → 1 distinct ✓
- [1] → 1 distinct ✓
- [3] → 1 distinct ✓
- [4] → 1 distinct ✓

Count at most 1: 5

Count exactly 2: 8 - 5 = 3 ✓
```

### Sliding Window for "At Most K"
```
Function: count_at_most_k_distinct(arr, k)

Array: [1, 2, 1, 3, 4], k=2

left=0, right=0: window=[1], distinct=1 ≤ 2 ✓
left=0, right=1: window=[1,2], distinct=2 ≤ 2 ✓
left=0, right=2: window=[1,2,1], distinct=2 ≤ 2 ✓
left=0, right=3: window=[1,2,1,3], distinct=3 > 2 ✗
  → shrink: left=1, window=[2,1,3], distinct=3 > 2 ✗
  → shrink: left=2, window=[1,3], distinct=2 ≤ 2 ✓
left=2, right=4: window=[1,3,4], distinct=3 > 2 ✗
  → shrink: left=3, window=[3,4], distinct=2 ≤ 2 ✓

Valid windows: [1], [1,2], [1,2,1], [1,3], [3,4]
Count: 5
```

### Step-by-Step Process
```
Step 1: Count subarrays with at most 2 distinct values
- Use sliding window technique
- Expand right pointer, shrink left when needed
- Count: 8

Step 2: Count subarrays with at most 1 distinct value  
- Use sliding window technique
- Count: 5

Step 3: Calculate exactly 2 distinct values
- Result = 8 - 5 = 3
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Inclusion-      │ O(n)         │ O(n)         │ At most k    │
│ Exclusion       │              │              │ - at most    │
│                 │              │              │ (k-1)        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n²)        │ O(n)         │ Check all    │
│                 │              │              │ subarrays    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Direct Sliding  │ O(n)         │ O(n)         │ Track        │
│ Window          │              │              │ exactly k    │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Inclusion-Exclusion Principle**
- Convert "exactly k" to difference of "at most" problems
- Essential for counting problems
- Key optimization technique
- Enables efficient solution

### 2. **Sliding Window Technique**
- Maintain window constraints efficiently
- Important for understanding
- Expand and contract as needed
- Essential for algorithm

### 3. **Distinct Value Counting**
- Use hash map for frequency tracking
- Important for understanding
- Handle edge cases properly
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Subarray with At Most K Distinct
**Problem**: Count subarrays with at most k distinct values.

```python
def count_subarrays_with_at_most_k_distinct(n, k, arr):
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

# Example usage
result = count_subarrays_with_at_most_k_distinct(5, 2, [1, 2, 1, 3, 4])
print(f"Subarrays with at most 2 distinct: {result}")
```

### Variation 2: Subarray with At Least K Distinct
**Problem**: Count subarrays with at least k distinct values.

```python
def count_subarrays_with_at_least_k_distinct(n, k, arr):
    from collections import defaultdict
    
    def count_subarrays_with_at_most_k_distinct(k_limit):
        left = 0
        count = 0
        distinct_count = defaultdict(int)
        distinct_values = 0
        
        for right in range(n):
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
    
    # Total subarrays - subarrays with at most (k-1) distinct
    total_subarrays = n * (n + 1) // 2
    at_most_k_minus_1 = count_subarrays_with_at_most_k_distinct(k - 1)
    
    return total_subarrays - at_most_k_minus_1

# Example usage
result = count_subarrays_with_at_least_k_distinct(5, 3, [1, 2, 1, 3, 4])
print(f"Subarrays with at least 3 distinct: {result}")
```

### Variation 3: Subarray with K Distinct and Length Constraint
**Problem**: Count subarrays with exactly k distinct values and length at least L.

```python
def count_subarrays_with_k_distinct_and_length(n, k, L, arr):
    from collections import defaultdict
    
    def count_subarrays_with_at_most_k_distinct_and_length(k_limit, min_length):
        left = 0
        count = 0
        distinct_count = defaultdict(int)
        distinct_values = 0
        
        for right in range(n):
            if distinct_count[arr[right]] == 0:
                distinct_values += 1
            distinct_count[arr[right]] += 1
            
            while distinct_values > k_limit:
                distinct_count[arr[left]] -= 1
                if distinct_count[arr[left]] == 0:
                    distinct_values -= 1
                left += 1
            
            # Only count subarrays with length >= min_length
            if right - left + 1 >= min_length:
                count += right - left + 1 - min_length + 1
        
        return count
    
    # Exactly k = At most k - At most (k-1)
    return (count_subarrays_with_at_most_k_distinct_and_length(k, L) - 
            count_subarrays_with_at_most_k_distinct_and_length(k - 1, L))

# Example usage
result = count_subarrays_with_k_distinct_and_length(5, 2, 2, [1, 2, 1, 3, 4])
print(f"Subarrays with exactly 2 distinct and length >= 2: {result}")
```

### Variation 4: Subarray with K Distinct and Sum Constraint
**Problem**: Count subarrays with exactly k distinct values and sum at most S.

```python
def count_subarrays_with_k_distinct_and_sum(n, k, S, arr):
    from collections import defaultdict
    
    def count_subarrays_with_at_most_k_distinct_and_sum(k_limit, max_sum):
        left = 0
        count = 0
        distinct_count = defaultdict(int)
        distinct_values = 0
        current_sum = 0
        
        for right in range(n):
            # Add current element
            if distinct_count[arr[right]] == 0:
                distinct_values += 1
            distinct_count[arr[right]] += 1
            current_sum += arr[right]
            
            # Shrink window if constraints violated
            while (distinct_values > k_limit or current_sum > max_sum):
                distinct_count[arr[left]] -= 1
                if distinct_count[arr[left]] == 0:
                    distinct_values -= 1
                current_sum -= arr[left]
                left += 1
            
            # Add all valid subarrays ending at right
            count += right - left + 1
        
        return count
    
    # Exactly k = At most k - At most (k-1)
    return (count_subarrays_with_at_most_k_distinct_and_sum(k, S) - 
            count_subarrays_with_at_most_k_distinct_and_sum(k - 1, S))

# Example usage
result = count_subarrays_with_k_distinct_and_sum(5, 2, 10, [1, 2, 1, 3, 4])
print(f"Subarrays with exactly 2 distinct and sum <= 10: {result}")
```

### Variation 5: Subarray with K Distinct and Range Queries
**Problem**: Answer queries about subarrays with exactly k distinct values in specific ranges.

```python
def subarray_k_distinct_range_queries(n, k, arr, queries):
    """Answer queries about subarrays with exactly k distinct values in ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= n:
            results.append(0)
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            count = count_subarrays_with_exactly_k_distinct_in_range(len(subarray), k, subarray)
            results.append(count)
    
    return results

def count_subarrays_with_exactly_k_distinct_in_range(n, k, arr):
    """Count subarrays with exactly k distinct values in a specific range"""
    from collections import defaultdict
    
    def count_subarrays_with_at_most_k_distinct(k_limit):
        left = 0
        count = 0
        distinct_count = defaultdict(int)
        distinct_values = 0
        
        for right in range(n):
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
    
    return count_subarrays_with_at_most_k_distinct(k) - count_subarrays_with_at_most_k_distinct(k - 1)

# Example usage
queries = [(0, 4), (1, 3), (2, 4)]
result = subarray_k_distinct_range_queries(5, 2, [1, 2, 1, 3, 4], queries)
print(f"Range query results: {result}")
```

## 🔗 Related Problems

- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray sum problems
- **[Longest Substring without Repeating](/cses-analyses/problem_soulutions/sliding_window/)**: Distinct character problems
- **[Subarray Distinct Values](/cses-analyses/problem_soulutions/sliding_window/)**: Distinct value problems

## 📚 Learning Points

1. **Inclusion-Exclusion Principle**: Essential for counting "exactly k" problems
2. **Sliding Window Technique**: Important for maintaining constraints efficiently
3. **Hash Map for Counting**: Key for tracking distinct values and frequencies
4. **Problem Transformation**: Converting "exactly k" to difference of "at most" problems

---

**This is a great introduction to counting problems with sliding windows!** 🎯 