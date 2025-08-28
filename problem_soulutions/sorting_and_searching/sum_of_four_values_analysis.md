---
layout: simple
title: "Sum of Four Values
permalink: /problem_soulutions/sorting_and_searching/sum_of_four_values_analysis/"
---


# Sum of Four Values

## Problem Statement
Given an array of n integers and a target sum x, find four distinct indices such that the sum of the values at those indices equals x.

### Input
The first input line has two integers n and x: the size of the array and the target sum.
The second line has n integers a1,a2,…,an: the array.

### Output"
Print four distinct indices (1-indexed) such that the sum equals x, or "IMPOSSIBLE" if no solution exists.

### Constraints
- 1 ≤ n ≤ 1000
- 1 ≤ x ≤ 10^9
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
5 15
1 3 4 6 8

Output:
1 2 3 4
```

## Solution Progression

### Approach 1: Brute Force - O(n⁴)
**Description**: Try all possible combinations of four indices.

```python
def sum_of_four_values_naive(n, x, arr):
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    if arr[i] + arr[j] + arr[k] + arr[l] == x:
                        return (i + 1, j + 1, k + 1, l + 1)
    return "IMPOSSIBLE"
```

**Why this is inefficient**: We try all O(n⁴) combinations, leading to quartic time complexity.

### Improvement 1: Two Pointers - O(n³)
**Description**: Fix two elements and use two pointers for the remaining two.

```python
def sum_of_four_values_optimized(n, x, arr):
    # Create list of (value, index) pairs
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()  # Sort by value
    
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            target = x - pairs[i][0] - pairs[j][0]
            
            while left < right:
                current_sum = pairs[left][0] + pairs[right][0]
                
                if current_sum == target:
                    return (pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1])
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return "IMPOSSIBLE"
```

**Why this improvement works**: We fix two elements and use two pointers to find the remaining two elements that sum to the target. This reduces the complexity from O(n⁴) to O(n³).

## Final Optimal Solution

```python
n, x = map(int, input().split())
arr = list(map(int, input().split()))

def find_four_values(n, x, arr):
    # Create list of (value, index) pairs
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()  # Sort by value
    
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            target = x - pairs[i][0] - pairs[j][0]
            
            while left < right:
                current_sum = pairs[left][0] + pairs[right][0]
                
                if current_sum == target:
                    return (pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1])
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return "IMPOSSIBLE"

result = find_four_values(n, x, arr)
if result == "IMPOSSIBLE":
    print(result)
else:
    print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n⁴) | O(1) | Try all combinations |
| Two Pointers | O(n³) | O(n) | Fix two elements and use two pointers |

## Key Insights for Other Problems

### 1. **Four Sum Problems**
**Principle**: Fix two elements and use two pointers to find the remaining two elements.
**Applicable to**: Four sum problems, k-sum problems, pointer problems

### 2. **Two Pointers Technique**
**Principle**: Use two pointers to efficiently find pairs that sum to a target value.
**Applicable to**: Two sum problems, pointer problems, search problems

### 3. **Sorting for Efficiency**
**Principle**: Sort the array to enable efficient two-pointer search.
**Applicable to**: Sorting problems, search problems, optimization problems

## Notable Techniques

### 1. **Four Sum with Two Pointers**
```python
def four_sum_with_pointers(arr, target):
    pairs = [(arr[i], i) for i in range(len(arr))]
    pairs.sort()
    
    for i in range(len(arr) - 3):
        for j in range(i + 1, len(arr) - 2):
            left = j + 1
            right = len(arr) - 1
            current_target = target - pairs[i][0] - pairs[j][0]
            
            while left < right:
                current_sum = pairs[left][0] + pairs[right][0]
                
                if current_sum == current_target:
                    return (pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1])
                elif current_sum < current_target:
                    left += 1
                else:
                    right -= 1
    
    return None
```

### 2. **Two Pointer Search**
```python
def two_pointer_search(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        
        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None
```

### 3. **Index Tracking**
```python
def track_indices_with_values(arr):
    # Create pairs of (value, original_index)
    pairs = [(arr[i], i + 1) for i in range(len(arr))]
    pairs.sort(key=lambda x: x[0])
    return pairs
```

## Problem-Solving Framework

1. **Identify problem type**: This is a four sum problem with index tracking
2. **Choose approach**: Use two pointers technique after sorting
3. **Create pairs**: Store (value, index) pairs to track original indices
4. **Sort pairs**: Sort by value to enable two-pointer search
5. **Fix two elements**: Iterate through all possible pairs of first two elements
6. **Two pointer search**: Use two pointers to find remaining two elements
7. **Return result**: Output the four indices or "IMPOSSIBLE"

---

*This analysis shows how to efficiently find four values that sum to a target using two pointers technique.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Sum of Four Values with Constraints**
**Problem**: Find four values with sum x where values must satisfy certain constraints.
```python
def sum_of_four_values_with_constraints(n, x, arr, constraints):
    # constraints[i] = list of indices that cannot be used with index i
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()
    
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            target = x - pairs[i][0] - pairs[j][0]
            
            while left < right:
                # Check if current combination violates constraints
                idx1, idx2, idx3, idx4 = pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1]
                
                valid = True
                for constraint_idx in constraints.get(idx1, []):
                    if constraint_idx in [idx2, idx3, idx4]:
                        valid = False
                        break
                
                if valid:
                    current_sum = pairs[left][0] + pairs[right][0]
                    
                    if current_sum == target:
                        return (idx1, idx2, idx3, idx4)
                    elif current_sum < target:
                        left += 1
                    else:
                        right -= 1
                else:
                    left += 1
    
    return "IMPOSSIBLE"
```

#### **Variation 2: Sum of Four Values with Range Constraints**
**Problem**: Find four values with sum in range [L, R].
```python
def sum_of_four_values_in_range(n, L, R, arr):
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()
    
    solutions = []
    
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            
            while left < right:
                current_sum = pairs[i][0] + pairs[j][0] + pairs[left][0] + pairs[right][0]
                
                if L <= current_sum <= R:
                    solutions.append((pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1]))
                    left += 1
                    right -= 1
                elif current_sum < L:
                    left += 1
                else:
                    right -= 1
    
    return solutions if solutions else "IMPOSSIBLE"
```

#### **Variation 3: Sum of Four Values with Modulo Constraints**
**Problem**: Find four values with sum congruent to x modulo m.
```python
def sum_of_four_values_modulo(n, x, m, arr):
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()
    
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            target_mod = (x - pairs[i][0] - pairs[j][0]) % m
            
            while left < right:
                current_sum_mod = (pairs[left][0] + pairs[right][0]) % m
                
                if current_sum_mod == target_mod:
                    return (pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1])
                elif current_sum_mod < target_mod:
                    left += 1
                else:
                    right -= 1
    
    return "IMPOSSIBLE"
```

#### **Variation 4: Sum of Four Values with Dynamic Updates**
**Problem**: Support adding and removing elements dynamically.
```python
class DynamicFourSum:
    def __init__(self):
        self.arr = []
        self.pairs = []
    
    def add_element(self, value):
        self.arr.append(value)
        self.pairs = [(self.arr[i], i + 1) for i in range(len(self.arr))]
        self.pairs.sort()
        return self.find_four_sum(0)  # Example target
    
    def remove_element(self, index):
        if 0 <= index < len(self.arr):
            self.arr.pop(index)
            self.pairs = [(self.arr[i], i + 1) for i in range(len(self.arr))]
            self.pairs.sort()
        return self.find_four_sum(0)  # Example target
    
    def find_four_sum(self, x):
        n = len(self.pairs)
        
        for i in range(n - 3):
            for j in range(i + 1, n - 2):
                left = j + 1
                right = n - 1
                target = x - self.pairs[i][0] - self.pairs[j][0]
                
                while left < right:
                    current_sum = self.pairs[left][0] + self.pairs[right][0]
                    
                    if current_sum == target:
                        return (self.pairs[i][1], self.pairs[j][1], 
                                self.pairs[left][1], self.pairs[right][1])
                    elif current_sum < target:
                        left += 1
                    else:
                        right -= 1
        
        return "IMPOSSIBLE"
```

#### **Variation 5: Sum of Four Values with Weighted Constraints**
**Problem**: Each element has a weight. Find four values with sum x and total weight ≤ W.
```python
def sum_of_four_values_weighted(n, x, arr, weights, max_weight):
    # Create list of (value, weight, index) tuples
    tuples = [(arr[i], weights[i], i + 1) for i in range(n)]
    tuples.sort(key=lambda x: x[0])  # Sort by value
    
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            target = x - tuples[i][0] - tuples[j][0]
            
            while left < right:
                current_sum = tuples[left][0] + tuples[right][0]
                total_weight = (tuples[i][1] + tuples[j][1] + 
                              tuples[left][1] + tuples[right][1])
                
                if current_sum == target and total_weight <= max_weight:
                    return (tuples[i][2], tuples[j][2], 
                            tuples[left][2], tuples[right][2])
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return "IMPOSSIBLE"
```

### 🔗 **Related Problems & Concepts**

#### **1. Multi-Pointer Problems**
- **Two Sum**: Find pair with given sum
- **Three Sum**: Find triplet with given sum
- **K Sum**: Find k elements with given sum
- **Multiple Pointers**: Efficient multi-pointer techniques

#### **2. Search Problems**
- **Binary Search**: Find element in sorted array
- **Linear Search**: Find element in unsorted array
- **Interpolation Search**: Search in uniformly distributed array
- **Exponential Search**: Search in unbounded array

#### **3. Array Manipulation Problems**
- **Array Sorting**: Sort array efficiently
- **Array Partitioning**: Partition array based on conditions
- **Array Merging**: Merge sorted arrays
- **Array Rotation**: Rotate array efficiently

#### **4. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Integer Programming**: Discrete optimization
- **Combinatorial Optimization**: Optimize discrete structures
- **Approximation Algorithms**: Find approximate solutions

#### **5. Mathematical Problems**
- **Number Theory**: Properties of numbers
- **Combinatorics**: Counting and arrangement
- **Optimization**: Mathematical optimization
- **Algorithm Analysis**: Complexity and correctness

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()
    
    found = False
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            target = x - pairs[i][0] - pairs[j][0]
            
            while left < right:
                current_sum = pairs[left][0] + pairs[right][0]
                
                if current_sum == target:
                    print(pairs[i][1], pairs[j][1], pairs[left][1], pairs[right][1])
                    found = True
                    break
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
            
            if found:
                break
        
        if found:
            break
    
    if not found:
        print("IMPOSSIBLE")
```

#### **2. Range Queries**
```python
# Precompute four-sum results for different subarrays
def precompute_four_sums(arr):
    n = len(arr)
    result_matrix = [[None] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            subarray = arr[i:j+1]
            if len(subarray) >= 4:
                # Find four-sum for this subarray
                pairs = [(subarray[k], k + i + 1) for k in range(len(subarray))]
                pairs.sort()
                
                found = False
                for k in range(len(pairs) - 3):
                    for l in range(k + 1, len(pairs) - 2):
                        left = l + 1
                        right = len(pairs) - 1
                        target = 0 - pairs[k][0] - pairs[l][0]  # Example target
                        
                        while left < right:
                            current_sum = pairs[left][0] + pairs[right][0]
                            
                            if current_sum == target:
                                result_matrix[i][j] = (pairs[k][1], pairs[l][1], 
                                                     pairs[left][1], pairs[right][1])
                                found = True
                                break
                            elif current_sum < target:
                                left += 1
                            else:
                                right -= 1
                        
                        if found:
                            break
                    
                    if found:
                        break
                
                if not found:
                    result_matrix[i][j] = "IMPOSSIBLE"
    
    return result_matrix

# Answer queries about four-sum for subarrays
def four_sum_query(result_matrix, l, r):
    return result_matrix[l][r]
```

#### **3. Interactive Problems**
```python
# Interactive four-sum finder
def interactive_four_sum():
    n = int(input("Enter array size: "))
    x = int(input("Enter target sum: "))
    arr = list(map(int, input("Enter array: ").split()))
    
    print(f"Array: {arr}")
    print(f"Target sum: {x}")
    
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()
    print(f"Sorted pairs: {pairs}")
    
    found = False
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            target = x - pairs[i][0] - pairs[j][0]
            
            print(f"\nFixing elements {pairs[i][0]} and {pairs[j][0]} at positions {pairs[i][1]} and {pairs[j][1]}")
            print(f"Looking for two elements that sum to {target}")
            
            while left < right:
                current_sum = pairs[left][0] + pairs[right][0]
                print(f"Checking {pairs[left][0]} + {pairs[right][0]} = {current_sum}")
                
                if current_sum == target:
                    print(f"Found solution: {pairs[i][1]} {pairs[j][1]} {pairs[left][1]} {pairs[right][1]}")
                    found = True
                    break
                elif current_sum < target:
                    print(f"Sum too small, moving left pointer")
                    left += 1
                else:
                    print(f"Sum too large, moving right pointer")
                    right -= 1
            
            if found:
                break
        
        if found:
            break
    
    if not found:
        print("IMPOSSIBLE")
```

### 🧮 **Mathematical Extensions**

#### **1. Number Theory**
- **Properties of Sums**: Properties of number sums
- **Divisibility**: Properties of divisibility
- **Modular Arithmetic**: Working with remainders
- **Prime Factorization**: Breaking numbers into primes

#### **2. Combinatorics**
- **Combinations**: Counting combinations
- **Permutations**: Counting permutations
- **Subset Sums**: Counting subset sums
- **Partitions**: Number partitions

#### **3. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Multi-Pointer Analysis**: Analysis of multi-pointer techniques
- **Search Complexity**: Complexity of search algorithms
- **Lower Bounds**: Establishing problem lower bounds

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Multi-Pointers**: Efficient multi-pointer techniques
- **Binary Search**: Efficient search algorithms
- **Sorting Algorithms**: Various sorting techniques
- **Search Algorithms**: Efficient search techniques

#### **2. Mathematical Concepts**
- **Number Theory**: Properties of numbers
- **Combinatorics**: Counting and arrangement
- **Optimization**: Mathematical optimization theory
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Multi-Pointer Implementation**: Efficient multi-pointer techniques
- **Search Implementation**: Efficient search techniques
- **Algorithm Design**: Problem-solving strategies
- **Complexity Analysis**: Performance evaluation

---

*This analysis demonstrates multi-pointer and search techniques for finding four values with given sum.* 