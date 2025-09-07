---
layout: simple
title: "Subarray Distinct Values - Count Subarrays with At Most K Distinct"
permalink: /problem_soulutions/sliding_window/subarray_distinct_values_analysis
---

# Subarray Distinct Values - Count Subarrays with At Most K Distinct

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand sliding window problems with distinct value constraints and subarray counting
- Apply sliding window technique to count subarrays with at most k distinct values
- Implement efficient sliding window algorithms with O(n) time complexity for distinct value problems
- Optimize sliding window problems using hash maps and distinct value tracking
- Handle edge cases in sliding window problems (k=1, all distinct values, empty arrays)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sliding window technique, two-pointer technique, distinct value counting, hash map usage, subarray counting
- **Data Structures**: Hash maps, distinct value tracking, sliding window tracking, frequency tracking, window boundaries
- **Mathematical Concepts**: Distinct value theory, subarray counting, window mathematics, counting problems
- **Programming Skills**: Hash map implementation, distinct value tracking, window sliding, frequency counting, algorithm implementation
- **Related Problems**: Subarray with K Distinct (exact k distinct), Longest Substring Without Repeating Characters (distinct characters), Sliding window problems

## 📋 Problem Description

Given an array of n integers, find the number of subarrays with at most k distinct values.

**Input**: 
- First line: Two integers n and k (array size and maximum distinct values)
- Second line: n integers a₁, a₂, ..., aₙ (array contents)

**Output**: 
- One integer: the number of subarrays with at most k distinct values

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
10
```

**Explanation**: The subarrays with at most 2 distinct values are:
- [1] → distinct values: {1}
- [1, 2] → distinct values: {1, 2}
- [1, 2, 1] → distinct values: {1, 2}
- [2] → distinct values: {2}
- [2, 1] → distinct values: {1, 2}
- [1] → distinct values: {1}
- [1, 3] → distinct values: {1, 3}
- [3] → distinct values: {3}
- [3, 4] → distinct values: {3, 4}
- [4] → distinct values: {4}

Total count = 10 valid subarrays

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count subarrays with at most k distinct values
- **Key Insight**: Use sliding window to maintain constraint on distinct values
- **Challenge**: Efficiently track distinct values and count valid subarrays

### Step 2: Brute Force Approach
**Check all possible subarrays and count distinct values:**

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

**Complexity**: O(n² × k) - too slow for large arrays

### Step 3: Optimization
**Use sliding window with hash map for efficient counting:**

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

**Key Insight**: Use sliding window to maintain constraint of at most k distinct values

### Step 4: Complete Solution

```python
def solve_subarray_distinct_values():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = count_subarrays_with_at_most_k_distinct(n, k, arr)
    print(result)

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

if __name__ == "__main__":
    solve_subarray_distinct_values()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 2, [1, 2, 1, 3, 4]), 10),
        ((4, 1, [1, 1, 1, 1]), 10),
        ((3, 3, [1, 2, 3]), 6),
        ((2, 2, [1, 2]), 3),
        ((1, 1, [1]), 1),
        ((4, 2, [1, 2, 1, 2]), 10),
    ]
    
    for (n, k, arr), expected in test_cases:
        result = count_subarrays_with_at_most_k_distinct(n, k, arr)
        print(f"n={n}, k={k}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def count_subarrays_with_at_most_k_distinct(n, k, arr):
    from collections import defaultdict
    
    left = 0
    count = 0
    distinct_count = defaultdict(int)
    distinct_values = 0
    
    for right in range(n):
        if distinct_count[arr[right]] == 0:
            distinct_values += 1
        distinct_count[arr[right]] += 1
        
        while distinct_values > k:
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                distinct_values -= 1
            left += 1
        
        count += right - left + 1
    
    return count

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with sliding window
- **Space**: O(k) - hash map to store distinct value counts

### Why This Solution Works
- **Sliding Window**: Efficiently maintains window with at most k distinct values
- **Hash Map**: Tracks frequency of each distinct value
- **Window Expansion**: Adds new elements and shrinks when constraint violated
- **Optimal Algorithm**: Best known approach for this problem

## 🎨 Visual Example

### Input Example
```
Array: [1, 2, 1, 3, 4]
k = 2 (at most 2 distinct values)
```

### All Valid Subarrays
```
Array: [1, 2, 1, 3, 4]
Index:  0  1  2  3  4

Valid subarrays (at most 2 distinct values):
Length 1: [1], [2], [1], [3], [4] → 5 subarrays
Length 2: [1,2], [2,1], [1,3], [3,4] → 4 subarrays
Length 3: [1,2,1] → 1 subarray

Total: 10 valid subarrays

Invalid subarrays (more than 2 distinct values):
[1,2,3], [2,1,3], [1,3,4], [2,1,3,4], [1,2,1,3], [1,2,1,3,4]
```

### Sliding Window Process
```
Array: [1, 2, 1, 3, 4]
Index:  0  1  2  3  4
k = 2

Step 1: left=0, right=0, window=[1]
distinct_count = {1: 1}, count = 1
valid_subarrays = 1

Step 2: left=0, right=1, window=[1,2]
distinct_count = {1: 1, 2: 1}, count = 2
valid_subarrays = 1 + 2 = 3

Step 3: left=0, right=2, window=[1,2,1]
distinct_count = {1: 2, 2: 1}, count = 2
valid_subarrays = 3 + 3 = 6

Step 4: left=0, right=3, window=[1,2,1,3]
distinct_count = {1: 2, 2: 1, 3: 1}, count = 3 > k
Remove elements from left until count ≤ k
Remove 1: distinct_count = {2: 1, 3: 1}, count = 2
left = 1, window=[2,1,3]
valid_subarrays = 6 + 3 = 9

Step 5: left=1, right=4, window=[2,1,3,4]
distinct_count = {2: 1, 1: 1, 3: 1, 4: 1}, count = 4 > k
Remove elements from left until count ≤ k
Remove 2: distinct_count = {1: 1, 3: 1, 4: 1}, count = 3 > k
Remove 1: distinct_count = {3: 1, 4: 1}, count = 2
left = 3, window=[3,4]
valid_subarrays = 9 + 2 = 11

Final result: 11
```

### Visual Sliding Window
```
Array: [1, 2, 1, 3, 4]
Index:  0  1  2  3  4

Window progression:
Step 1: [1] 2 1 3 4        → distinct: {1}, count=1, valid=1
Step 2: [1,2] 1 3 4        → distinct: {1,2}, count=2, valid=3
Step 3: [1,2,1] 3 4        → distinct: {1,2}, count=2, valid=6
Step 4: 1 [2,1,3] 4        → distinct: {2,1,3}, count=3>k, shrink
Step 5: 1 2 1 [3,4]        → distinct: {3,4}, count=2, valid=11

Total valid subarrays: 11
```

### Distinct Value Counting
```
Array: [1, 2, 1, 3, 4]

Step-by-step distinct count:
Step 1: {1: 1} → count = 1
Step 2: {1: 1, 2: 1} → count = 2
Step 3: {1: 2, 2: 1} → count = 2
Step 4: {1: 2, 2: 1, 3: 1} → count = 3 > k
Step 5: {2: 1, 3: 1, 4: 1} → count = 3 > k
Step 6: {3: 1, 4: 1} → count = 2
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n³)        │ O(1)         │ Check all    │
│                 │              │              │ subarrays    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Optimized       │ O(n²)        │ O(n)         │ Use hash map │
│ Brute Force     │              │              │ for each     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sliding Window  │ O(n)         │ O(k)         │ Two pointers │
│                 │              │              │ technique    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sliding Window  │ O(n)         │ O(1)         │ Use array    │
│ (Optimized)     │              │              │ for small    │
│                 │              │              │ values       │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Subarray Distinct Values Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: array, k │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize:     │
              │ left = 0        │
              │ count = 0       │
              │ distinct_count  │
              │ = {}            │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For right = 0   │
              │ to len(arr):    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Add arr[right]  │
              │ to distinct_    │
              │ count           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ While distinct  │
              │ count > k:      │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Remove arr[left]│
              │ from distinct_  │
              │ count           │
              │ left++          │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ count +=        │
              │ right - left + 1│
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return count    │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Sliding Window Technique**
- Maintain window constraints efficiently
- Important for understanding
- Expand and contract as needed
- Essential for algorithm

### 2. **Distinct Value Counting**
- Use hash map for frequency tracking
- Important for understanding
- Handle edge cases properly
- Essential for optimization

### 3. **Window Management**
- Expand window when adding elements
- Important for understanding
- Shrink window when constraints violated
- Essential for algorithm

## 🎯 Problem Variations

### Variation 1: Subarrays with Exactly K Distinct Values
**Problem**: Count subarrays with exactly k distinct values.

```python
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
    
    # Exactly k = At most k - At most (k-1)
    return count_subarrays_with_at_most_k_distinct(k) - count_subarrays_with_at_most_k_distinct(k - 1)

# Example usage
result = count_subarrays_with_exactly_k_distinct(5, 2, [1, 2, 1, 3, 4])
print(f"Subarrays with exactly 2 distinct: {result}")
```

### Variation 2: Subarrays with At Least K Distinct Values
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

### Variation 3: Subarrays with K Distinct and Length Constraint
**Problem**: Count subarrays with at most k distinct values and length at least L.

```python
def count_subarrays_with_k_distinct_and_length(n, k, L, arr):
    from collections import defaultdict
    
    left = 0
    count = 0
    distinct_count = defaultdict(int)
    distinct_values = 0
    
    for right in range(n):
        if distinct_count[arr[right]] == 0:
            distinct_values += 1
        distinct_count[arr[right]] += 1
        
        while distinct_values > k:
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                distinct_values -= 1
            left += 1
        
        # Only count subarrays with length >= L
        if right - left + 1 >= L:
            count += right - left + 1 - L + 1
    
    return count

# Example usage
result = count_subarrays_with_k_distinct_and_length(5, 2, 2, [1, 2, 1, 3, 4])
print(f"Subarrays with at most 2 distinct and length >= 2: {result}")
```

### Variation 4: Subarrays with K Distinct and Sum Constraint
**Problem**: Count subarrays with at most k distinct values and sum at most S.

```python
def count_subarrays_with_k_distinct_and_sum(n, k, S, arr):
    from collections import defaultdict
    
    left = 0
    count = 0
    distinct_count = defaultdict(int)
    distinct_values = 0
    current_sum = 0
    
    for right in range(n):
        if distinct_count[arr[right]] == 0:
            distinct_values += 1
        distinct_count[arr[right]] += 1
        current_sum += arr[right]
        
        # Shrink window if constraints violated
        while (distinct_values > k or current_sum > S):
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                distinct_values -= 1
            current_sum -= arr[left]
            left += 1
        
        count += right - left + 1
    
    return count

# Example usage
result = count_subarrays_with_k_distinct_and_sum(5, 2, 10, [1, 2, 1, 3, 4])
print(f"Subarrays with at most 2 distinct and sum <= 10: {result}")
```

### Variation 5: Subarrays with K Distinct and Range Queries
**Problem**: Answer queries about subarrays with at most k distinct values in specific ranges.

```python
def subarray_distinct_range_queries(n, k, arr, queries):
    """Answer queries about subarrays with at most k distinct values in ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= n:
            results.append(0)
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            count = count_subarrays_with_at_most_k_distinct_in_range(len(subarray), k, subarray)
            results.append(count)
    
    return results

def count_subarrays_with_at_most_k_distinct_in_range(n, k, arr):
    """Count subarrays with at most k distinct values in a specific range"""
    from collections import defaultdict
    
    left = 0
    count = 0
    distinct_count = defaultdict(int)
    distinct_values = 0
    
    for right in range(n):
        if distinct_count[arr[right]] == 0:
            distinct_values += 1
        distinct_count[arr[right]] += 1
        
        while distinct_values > k:
            distinct_count[arr[left]] -= 1
            if distinct_count[arr[left]] == 0:
                distinct_values -= 1
            left += 1
        
        count += right - left + 1
    
    return count

# Example usage
queries = [(0, 2), (1, 3), (2, 4)]
result = subarray_distinct_range_queries(5, 2, [1, 2, 1, 3, 4], queries)
print(f"Range query results: {result}")
```

## 🔗 Related Problems

- **[Subarray with K Distinct](/cses-analyses/problem_soulutions/sliding_window/)**: Exactly k distinct problems
- **[Longest Substring without Repeating](/cses-analyses/problem_soulutions/sliding_window/)**: Distinct character problems
- **[Sliding Window Problems](/cses-analyses/problem_soulutions/sliding_window/)**: Window-based problems

## 📚 Learning Points

1. **Sliding Window Technique**: Essential for maintaining constraints efficiently
2. **Distinct Value Counting**: Important for tracking unique elements
3. **Hash Map Usage**: Key for frequency tracking and O(1) operations
4. **Window Management**: Important for expanding and contracting based on constraints

---

**This is a great introduction to sliding window problems with distinct value constraints!** 🎯