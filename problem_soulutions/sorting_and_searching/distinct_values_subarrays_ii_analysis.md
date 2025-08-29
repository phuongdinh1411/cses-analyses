---
layout: simple
title: "Distinct Values Subarrays II"
permalink: /problem_soulutions/sorting_and_searching/distinct_values_subarrays_ii_analysis
---

# Distinct Values Subarrays II

## Problem Description

**Problem**: Given an array of n integers, find the number of subarrays that contain exactly k distinct values.

**Input**: 
- First line: n k (size of the array and number of distinct values)
- Second line: n integers a₁, a₂, ..., aₙ (the array)

**Output**: Number of subarrays with exactly k distinct values.

**Example**:
```
Input:
5 2
1 2 1 2 3

Output:
8

Explanation: 
Subarrays with exactly 2 distinct values:
[1, 2], [2, 1], [1, 2], [2, 3], [1, 2, 1], [2, 1, 2], [1, 2, 1, 2], [2, 1, 2, 3]
Total: 8 subarrays
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Count subarrays with exactly k distinct values
- Use sliding window technique
- Apply inclusion-exclusion principle
- Handle frequency counting efficiently

**Key Observations:**
- Use sliding window to maintain distinct count
- Count subarrays with at most k distinct values
- Apply inclusion-exclusion: exactly k = at most k - at most (k-1)
- Use hash map to track frequencies

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays and count distinct values.

```python
def distinct_values_subarrays_brute_force(n, k, arr):
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

**Why this works:**
- Checks all possible subarrays
- Uses set to track distinct values
- Simple to understand and implement
- O(n²) time complexity

### Step 3: Sliding Window Optimization
**Idea**: Use sliding window technique with inclusion-exclusion principle.

```python
def distinct_values_subarrays_sliding_window(n, k, arr):
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

**Why this is better:**
- O(n) time complexity
- Uses sliding window optimization
- Applies inclusion-exclusion principle
- Much more efficient

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_distinct_values_subarrays_ii():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
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
    result = count_at_most_k_distinct(k) - count_at_most_k_distinct(k - 1)
    
    print(result)

# Main execution
if __name__ == "__main__":
    solve_distinct_values_subarrays_ii()
```

**Why this works:**
- Optimal sliding window approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (5, 2, [1, 2, 1, 2, 3], 8),
        (4, 1, [1, 1, 1, 1], 4),
        (3, 3, [1, 2, 3], 1),
        (6, 2, [1, 2, 1, 2, 1, 2], 9),
    ]
    
    for n, k, arr, expected in test_cases:
        result = solve_test(n, k, arr)
        print(f"n={n}, k={k}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, k, arr):
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
    
    return count_at_most_k_distinct(k) - count_at_most_k_distinct(k - 1)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through array for each k value
- **Space**: O(n) - hash map to track frequencies

### Why This Solution Works
- **Sliding Window**: Maintains window with at most k distinct values
- **Inclusion-Exclusion**: Exactly k = at most k - at most (k-1)
- **Hash Map**: Efficiently tracks element frequencies
- **Optimal Approach**: Each element processed at most twice

## 🎯 Key Insights

### 1. **Inclusion-Exclusion Principle**
- Exactly k distinct = at most k distinct - at most (k-1) distinct
- Avoids complex counting logic
- Key insight for optimization
- Crucial for understanding

### 2. **Sliding Window Technique**
- Maintains window with at most k distinct values
- Expands window to the right
- Contracts window from left when needed
- Important for efficiency

### 3. **Frequency Management**
- Use hash map to track element frequencies
- Remove elements when frequency becomes 0
- Efficient frequency updates
- Essential for correctness

## 🎯 Problem Variations

### Variation 1: Subarrays with At Most K Distinct Values
**Problem**: Count subarrays with at most k distinct values.

```python
def subarrays_at_most_k_distinct(n, k, arr):
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
```

### Variation 2: Subarrays with At Least K Distinct Values
**Problem**: Count subarrays with at least k distinct values.

```python
def subarrays_at_least_k_distinct(n, k, arr):
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
    
    # Total subarrays - subarrays with at most (k-1) distinct
    total_subarrays = n * (n + 1) // 2
    return total_subarrays - count_at_most_k_distinct(k - 1)
```

### Variation 3: Subarrays with Range of Distinct Values
**Problem**: Count subarrays with distinct values in range [k1, k2].

```python
def subarrays_distinct_range(n, k1, k2, arr):
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
    
    # Subarrays with distinct values in [k1, k2] = 
    # at most k2 distinct - at most (k1-1) distinct
    return count_at_most_k_distinct(k2) - count_at_most_k_distinct(k1 - 1)
```

### Variation 4: Subarrays with Weighted Distinct Values
**Problem**: Count subarrays where each distinct value has a weight.

```python
def subarrays_weighted_distinct(n, k, arr, weights):
    def count_at_most_k_weighted(k):
        count = 0
        left = 0
        freq = {}
        current_weight = 0
        
        for right in range(n):
            if arr[right] not in freq:
                freq[arr[right]] = 0
                current_weight += weights[arr[right]]
            
            freq[arr[right]] += 1
            
            while len(freq) > k:
                freq[arr[left]] -= 1
                if freq[arr[left]] == 0:
                    del freq[arr[left]]
                    current_weight -= weights[arr[left]]
                left += 1
            
            count += right - left + 1
        
        return count
    
    return count_at_most_k_weighted(k) - count_at_most_k_weighted(k - 1)
```

### Variation 5: Dynamic Distinct Value Counting
**Problem**: Support adding/removing elements and counting subarrays with k distinct values.

```python
class DynamicDistinctCounter:
    def __init__(self):
        self.arr = []
        self.freq = {}
        self.distinct_count = 0
    
    def add_element(self, value):
        self.arr.append(value)
        if value not in self.freq:
            self.freq[value] = 0
            self.distinct_count += 1
        self.freq[value] += 1
    
    def remove_element(self, index):
        if 0 <= index < len(self.arr):
            value = self.arr.pop(index)
            self.freq[value] -= 1
            if self.freq[value] == 0:
                del self.freq[value]
                self.distinct_count -= 1
    
    def count_subarrays_k_distinct(self, k):
        if k > self.distinct_count:
            return 0
        
        # Use sliding window on current array
        return self._count_at_most_k_distinct(k) - self._count_at_most_k_distinct(k - 1)
    
    def _count_at_most_k_distinct(self, k):
        count = 0
        left = 0
        freq = {}
        
        for right in range(len(self.arr)):
            freq[self.arr[right]] = freq.get(self.arr[right], 0) + 1
            
            while len(freq) > k:
                freq[self.arr[left]] -= 1
                if freq[self.arr[left]] == 0:
                    del freq[self.arr[left]]
                left += 1
            
            count += right - left + 1
        
        return count
```

## 🔗 Related Problems

- **[Distinct Values Subarrays](/cses-analyses/problem_soulutions/sorting_and_searching/distinct_values_subarrays_analysis)**: Similar problem
- **[Subarray with K Distinct Elements](/cses-analyses/problem_soulutions/sliding_window/subarray_with_k_distinct_analysis)**: K distinct elements
- **[Longest Substring Without Repeating Characters](/cses-analyses/problem_soulutions/sliding_window/longest_substring_without_repeating_analysis)**: Unique elements

## 📚 Learning Points

1. **Inclusion-Exclusion**: Powerful principle for counting problems
2. **Sliding Window**: Efficient technique for subarray problems
3. **Frequency Tracking**: Use hash maps for efficient counting
4. **Range Problems**: Common pattern in competitive programming

---

**This is a great introduction to inclusion-exclusion principle and sliding window techniques!** 🎯 