---
layout: simple
title: "Distinct Values Subarrays"permalink: /problem_soulutions/sorting_and_searching/distinct_values_subarrays_analysis
---


# Distinct Values Subarrays

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Subarrays with At Least K Distinct Values**
**Problem**: Find number of subarrays with at least k distinct values.
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
    
    # Total subarrays - subarrays with at most k-1 distinct
    total_subarrays = n * (n + 1) // 2
    return total_subarrays - count_at_most_k_distinct(k - 1)
```

#### **Variation 2: Subarrays with Distinct Values in Range**
**Problem**: Find subarrays with distinct values between L and R.
```python
def subarrays_distinct_in_range(n, L, R, arr):
    count = 0
    left = 0
    freq = {}
    
    for right in range(n):
        freq[arr[right]] = freq.get(arr[right], 0) + 1
        
        # Shrink window while distinct count > R
        while len(freq) > R:
            freq[arr[left]] -= 1
            if freq[arr[left]] == 0:
                del freq[arr[left]]
            left += 1
        
        # Count subarrays ending at right with distinct count >= L
        if len(freq) >= L:
            count += right - left + 1
    
    return count
```

#### **Variation 3: Subarrays with Weighted Distinct Values**
**Problem**: Each distinct value has a weight. Find subarrays with total weight ≤ W.
```python
def subarrays_weighted_distinct(n, weights, max_weight, arr):
    count = 0
    left = 0
    freq = {}
    current_weight = 0
    
    for right in range(n):
        val = arr[right]
        if val not in freq:
            current_weight += weights.get(val, 1)
        freq[val] = freq.get(val, 0) + 1
        
        # Shrink window while weight > max_weight
        while current_weight > max_weight:
            freq[arr[left]] -= 1
            if freq[arr[left]] == 0:
                current_weight -= weights.get(arr[left], 1)
                del freq[arr[left]]
            left += 1
        
        count += right - left + 1
    
    return count
```

#### **Variation 4: Subarrays with Frequency Constraints**
**Problem**: Find subarrays where each distinct value appears at most F times.
```python
def subarrays_frequency_constraints(n, max_frequency, arr):
    count = 0
    left = 0
    freq = {}
    
    for right in range(n):
        freq[arr[right]] = freq.get(arr[right], 0) + 1
        
        # Shrink window while any value exceeds max frequency
        while freq[arr[right]] > max_frequency:
            freq[arr[left]] -= 1
            if freq[arr[left]] == 0:
                del freq[arr[left]]
            left += 1
        
        count += right - left + 1
    
    return count
```

#### **Variation 5: Subarrays with Dynamic Updates**
**Problem**: Support adding and removing elements dynamically.
```python
class DynamicDistinctSubarrays:
    def __init__(self, k):
        self.k = k
        self.arr = []
        self.freq = {}
        self.count = 0
    
    def add_element(self, element):
        self.arr.append(element)
        self.freq[element] = self.freq.get(element, 0) + 1
        
        # Update count
        if len(self.freq) == self.k:
            self.count += 1
        elif len(self.freq) > self.k:
            # Need to remove elements to get exactly k distinct
            self._adjust_window()
        
        return self.count
    
    def remove_element(self, index):
        if 0 <= index < len(self.arr):
            element = self.arr.pop(index)
            self.freq[element] -= 1
            if self.freq[element] == 0:
                del self.freq[element]
            
            # Recalculate count
            self.count = self._count_exactly_k_distinct()
        
        return self.count
    
    def _adjust_window(self):
        # Remove elements from left until we have exactly k distinct
        left = 0
        while len(self.freq) > self.k:
            self.freq[self.arr[left]] -= 1
            if self.freq[self.arr[left]] == 0:
                del self.freq[self.arr[left]]
            left += 1
    
    def _count_exactly_k_distinct(self):
        if len(self.freq) != self.k:
            return 0
        
        # Count subarrays with exactly k distinct
        count = 0
        left = 0
        temp_freq = {}
        
        for right in range(len(self.arr)):
            temp_freq[self.arr[right]] = temp_freq.get(self.arr[right], 0) + 1
            
            while len(temp_freq) > self.k:
                temp_freq[self.arr[left]] -= 1
                if temp_freq[self.arr[left]] == 0:
                    del temp_freq[self.arr[left]]
                left += 1
            
            if len(temp_freq) == self.k:
                count += 1
        
        return count
```

### 🔗 **Related Problems & Concepts**

#### **1. Sliding Window Problems**
- **Longest Substring Without Repeating**: Find substring with unique characters
- **Minimum Window Substring**: Find smallest substring containing all characters
- **Substring with Concatenation**: Find substring containing all words
- **Longest Substring with At Most K**: Find substring with at most k distinct characters

#### **2. Counting Problems**
- **Frequency Counting**: Count occurrences of each element
- **Subarray Counting**: Count subarrays satisfying conditions
- **Combinatorial Counting**: Count combinations and arrangements
- **Inclusion-Exclusion**: Count using inclusion-exclusion principle

#### **3. Hash Table Problems**
- **Hash Table Implementation**: Custom hash table design
- **Collision Resolution**: Handle hash collisions
- **Load Factor**: Optimize hash table performance
- **Hash Functions**: Design good hash functions

#### **4. Array Manipulation Problems**
- **Array Partitioning**: Partition array based on conditions
- **Array Merging**: Merge sorted arrays
- **Array Sorting**: Sort array efficiently
- **Array Rotation**: Rotate array by k positions

#### **5. Two Pointers Problems**
- **Two Sum**: Find pair with given sum
- **Three Sum**: Find triplet with given sum
- **Container With Most Water**: Find maximum area
- **Trapping Rain Water**: Calculate trapped water

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
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
    
    result = count_at_most_k_distinct(k) - count_at_most_k_distinct(k - 1)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute distinct value counts for different subarrays
def precompute_distinct_counts(arr):
    n = len(arr)
    distinct_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        freq = {}
        for j in range(i, n):
            freq[arr[j]] = freq.get(arr[j], 0) + 1
            distinct_matrix[i][j] = len(freq)
    
    return distinct_matrix

# Answer queries about distinct values in subarrays
def distinct_query(distinct_matrix, l, r):
    return distinct_matrix[l][r]
```

#### **3. Interactive Problems**
```python
# Interactive distinct values subarray counter
def interactive_distinct_subarrays():
    n = int(input("Enter array size: "))
    k = int(input("Enter target distinct values: "))
    arr = list(map(int, input("Enter array: ").split()))
    
    print(f"Array: {arr}")
    print(f"Target distinct values: {k}")
    
    def count_at_most_k_distinct(k):
        count = 0
        left = 0
        freq = {}
        subarrays = []
        
        for right in range(n):
            freq[arr[right]] = freq.get(arr[right], 0) + 1
            print(f"Window [{left}, {right}]: {arr[left:right+1]}, Distinct: {len(freq)}")
            
            while len(freq) > k:
                freq[arr[left]] -= 1
                if freq[arr[left]] == 0:
                    del freq[arr[left]]
                left += 1
                print(f"Shrinking window to [{left}, {right}]: {arr[left:right+1]}")
            
            count += right - left + 1
            subarrays.append(arr[left:right+1])
        
        return count, subarrays
    
    count_at_most_k, subarrays_k = count_at_most_k_distinct(k)
    count_at_most_k_minus_1, subarrays_k_minus_1 = count_at_most_k_distinct(k - 1)
    
    result = count_at_most_k - count_at_most_k_minus_1
    
    print(f"Subarrays with at most {k} distinct: {count_at_most_k}")
    print(f"Subarrays with at most {k-1} distinct: {count_at_most_k_minus_1}")
    print(f"Subarrays with exactly {k} distinct: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Counting Principles**: Fundamental counting principles
- **Inclusion-Exclusion**: Inclusion-exclusion principle
- **Permutations**: Arrangements of elements
- **Combinations**: Selections of elements

#### **2. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Amortized Analysis**: Average case analysis
- **Probabilistic Analysis**: Expected performance
- **Worst Case Analysis**: Upper bounds

#### **3. Mathematical Properties**
- **Monotonicity**: Properties of increasing sequences
- **Invariants**: Properties that remain constant
- **Symmetry**: Symmetric properties
- **Optimality**: Proving optimality of solutions

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Sliding Window**: Two-pointer technique
- **Hash Tables**: Efficient lookup data structures
- **Counting Algorithms**: Efficient counting techniques
- **Two Pointers**: Efficient array processing

#### **2. Mathematical Concepts**
- **Combinatorics**: Counting and arrangement
- **Inclusion-Exclusion**: Mathematical principle
- **Algorithm Analysis**: Complexity and correctness
- **Discrete Mathematics**: Discrete structures

#### **3. Programming Concepts**
- **Array Manipulation**: Efficient array operations
- **Hash Table Usage**: Efficient data structures
- **Algorithm Design**: Problem-solving strategies
- **Complexity Analysis**: Performance evaluation

---

*This analysis demonstrates sliding window techniques and shows various extensions for counting problems.* 