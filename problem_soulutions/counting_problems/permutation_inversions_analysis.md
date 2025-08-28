---
layout: simple
title: CSES Permutation Inversions - Problem Analysis
permalink: /problem_soulutions/counting_problems/permutation_inversions_analysis/
---

# CSES Permutation Inversions - Problem Analysis

## Problem Statement
Given a permutation of numbers from 1 to n, count the number of inversions. An inversion is a pair of indices (i,j) where i < j and a[i] > a[j].

### Input
The first input line has an integer n: the size of the permutation.
The second line has n integers: the permutation.

### Output
Print one integer: the number of inversions.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- The input is a valid permutation of 1 to n

### Example
```
Input:
4
3 1 4 2

Output:
3
```

## Solution Progression

### Approach 1: Check All Pairs - O(n²)
**Description**: Check all possible pairs of indices to count inversions.

```python
def permutation_inversions_naive(n, arr):
    count = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    
    return count
```

**Why this is inefficient**: We need to check all possible pairs, leading to O(n²) time complexity.

### Improvement 1: Merge Sort with Inversion Counting - O(n log n)
**Description**: Use merge sort to count inversions efficiently.

```python
def permutation_inversions_merge_sort(n, arr):
    def merge_sort_and_count(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left, left_inversions = merge_sort_and_count(arr[:mid])
        right, right_inversions = merge_sort_and_count(arr[mid:])
        
        merged, split_inversions = merge_and_count(left, right)
        total_inversions = left_inversions + right_inversions + split_inversions
        
        return merged, total_inversions
    
    def merge_and_count(left, right):
        merged = []
        inversions = 0
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len(left) - i
                j += 1
        
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, inversions
    
    _, count = merge_sort_and_count(arr)
    return count
```

**Why this improvement works**: Merge sort allows us to count inversions in O(n log n) time by counting split inversions during merging.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

def count_inversions(n, arr):
    def merge_sort_and_count(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left, left_inversions = merge_sort_and_count(arr[:mid])
        right, right_inversions = merge_sort_and_count(arr[mid:])
        
        merged, split_inversions = merge_and_count(left, right)
        total_inversions = left_inversions + right_inversions + split_inversions
        
        return merged, total_inversions
    
    def merge_and_count(left, right):
        merged = []
        inversions = 0
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len(left) - i
                j += 1
        
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, inversions
    
    _, count = merge_sort_and_count(arr)
    return count

result = count_inversions(n, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n²) | O(1) | Check all pairs |
| Merge Sort | O(n log n) | O(n) | Use merge sort to count inversions |

## Key Insights for Other Problems

### 1. **Inversion Counting Problems**
**Principle**: Use divide and conquer algorithms to count inversions efficiently.
**Applicable to**: Sorting problems, counting problems, divide and conquer problems

### 2. **Merge Sort for Counting**
**Principle**: Use merge sort to count inversions during the merging process.
**Applicable to**: Sorting problems, counting problems, merge sort applications

### 3. **Split Inversion Counting**
**Principle**: Count inversions that span across the divide point during merging.
**Applicable to**: Divide and conquer problems, counting problems, merge sort variations

## Notable Techniques

### 1. **Merge Sort with Inversion Counting**
```python
def merge_sort_with_inversions(arr):
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_inv = merge_sort_with_inversions(arr[:mid])
    right, right_inv = merge_sort_with_inversions(arr[mid:])
    
    merged, split_inv = merge_and_count(left, right)
    return merged, left_inv + right_inv + split_inv
```

### 2. **Merge and Count Inversions**
```python
def merge_and_count(left, right):
    merged = []
    inversions = 0
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged, inversions
```

### 3. **Inversion Check**
```python
def count_inversions_naive(arr):
    count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                count += 1
    return count
```

## Problem-Solving Framework

1. **Identify problem type**: This is an inversion counting problem
2. **Choose approach**: Use merge sort to count inversions efficiently
3. **Implement merge sort**: Modify merge sort to count split inversions
4. **Count inversions**: Track inversions during the merging process
5. **Return result**: Sum up all inversions (left + right + split)

---

*This analysis shows how to efficiently count permutation inversions using merge sort with inversion counting and binary indexed trees.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Permutation Inversions**
**Problem**: Each inversion has a weight. Find total weight of all inversions.
```python
def weighted_permutation_inversions(arr, weights):
    # weights[i] = weight of element arr[i]
    n = len(arr)
    total_weight = 0
    
    def merge_sort_with_weights(left, right):
        if left >= right:
            return 0
        
        mid = (left + right) // 2
        weight = merge_sort_with_weights(left, mid)
        weight += merge_sort_with_weights(mid + 1, right)
        weight += merge_with_weights(left, mid, right)
        return weight
    
    def merge_with_weights(left, mid, right):
        i, j, k = left, mid + 1, 0
        temp = [0] * (right - left + 1)
        weight = 0
        
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                # Count inversions and add weights
                for x in range(i, mid + 1):
                    weight += weights[arr[x]-1] * weights[arr[j]-1]
                j += 1
            k += 1
        
        while i <= mid:
            temp[k] = arr[i]
            i += 1
            k += 1
        
        while j <= right:
            temp[k] = arr[j]
            j += 1
            k += 1
        
        for i in range(k):
            arr[left + i] = temp[i]
        
        return weight
    
    return merge_sort_with_weights(0, n - 1)
```

#### **Variation 2: Constrained Permutation Inversions**
**Problem**: Count inversions only if elements are within a certain distance.
```python
def constrained_permutation_inversions(arr, max_distance):
    n = len(arr)
    inversions = 0
    
    for i in range(n):
        for j in range(i + 1, min(i + max_distance + 1, n)):
            if arr[i] > arr[j]:
                inversions += 1
    
    return inversions
```

#### **Variation 3: Circular Permutation Inversions**
**Problem**: Handle circular permutations where the array wraps around.
```python
def circular_permutation_inversions(arr):
    n = len(arr)
    # Create circular array by duplicating
    circular_arr = arr + arr
    inversions = 0
    
    # Count inversions for each starting position
    for start in range(n):
        current_arr = circular_arr[start:start + n]
        inversions += count_inversions(current_arr)
    
    return inversions

def count_inversions(arr):
    n = len(arr)
    inversions = 0
    
    def merge_sort(left, right):
        if left >= right:
            return 0
        
        mid = (left + right) // 2
        inv = merge_sort(left, mid)
        inv += merge_sort(mid + 1, right)
        inv += merge(left, mid, right)
        return inv
    
    def merge(left, mid, right):
        i, j, k = left, mid + 1, 0
        temp = [0] * (right - left + 1)
        inv = 0
        
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                inv += mid - i + 1
                j += 1
            k += 1
        
        while i <= mid:
            temp[k] = arr[i]
            i += 1
            k += 1
        
        while j <= right:
            temp[k] = arr[j]
            j += 1
            k += 1
        
        for i in range(k):
            arr[left + i] = temp[i]
        
        return inv
    
    return merge_sort(0, n - 1)
```

#### **Variation 4: Range-Based Permutation Inversions**
**Problem**: Count inversions in a specific range of the permutation.
```python
def range_permutation_inversions(arr, start, end):
    # Count inversions in arr[start:end+1]
    range_arr = arr[start:end+1]
    return count_inversions(range_arr)

def count_inversions(arr):
    n = len(arr)
    inversions = 0
    
    def merge_sort(left, right):
        if left >= right:
            return 0
        
        mid = (left + right) // 2
        inv = merge_sort(left, mid)
        inv += merge_sort(mid + 1, right)
        inv += merge(left, mid, right)
        return inv
    
    def merge(left, mid, right):
        i, j, k = left, mid + 1, 0
        temp = [0] * (right - left + 1)
        inv = 0
        
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                inv += mid - i + 1
                j += 1
            k += 1
        
        while i <= mid:
            temp[k] = arr[i]
            i += 1
            k += 1
        
        while j <= right:
            temp[k] = arr[j]
            j += 1
            k += 1
        
        for i in range(k):
            arr[left + i] = temp[i]
        
        return inv
    
    return merge_sort(0, n - 1)
```

#### **Variation 5: Dynamic Permutation Inversion Updates**
**Problem**: Support dynamic updates to the permutation and answer inversion queries efficiently.
```python
class DynamicInversionCounter:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr[:]
        self.inversions = self._count_inversions()
    
    def _count_inversions(self):
        inversions = 0
        
        def merge_sort(left, right):
            if left >= right:
                return 0
            
            mid = (left + right) // 2
            inv = merge_sort(left, mid)
            inv += merge_sort(mid + 1, right)
            inv += merge(left, mid, right)
            return inv
        
        def merge(left, mid, right):
            i, j, k = left, mid + 1, 0
            temp = [0] * (right - left + 1)
            inv = 0
            
            while i <= mid and j <= right:
                if self.arr[i] <= self.arr[j]:
                    temp[k] = self.arr[i]
                    i += 1
                else:
                    temp[k] = self.arr[j]
                    inv += mid - i + 1
                    j += 1
                k += 1
            
            while i <= mid:
                temp[k] = self.arr[i]
                i += 1
                k += 1
            
            while j <= right:
                temp[k] = self.arr[j]
                j += 1
                k += 1
            
            for i in range(k):
                self.arr[left + i] = temp[i]
            
            return inv
        
        return merge_sort(0, self.n - 1)
    
    def swap_elements(self, i, j):
        if i != j:
            # Update inversions after swap
            self.inversions = self._count_inversions()
    
    def get_inversion_count(self):
        return self.inversions
```

### 🔗 **Related Problems & Concepts**

#### **1. Permutation Problems**
- **Permutation Analysis**: Analyze permutation properties
- **Permutation Generation**: Generate permutations
- **Permutation Optimization**: Optimize permutation algorithms
- **Permutation Counting**: Count permutation properties

#### **2. Inversion Problems**
- **Inversion Counting**: Count inversions efficiently
- **Inversion Analysis**: Analyze inversion properties
- **Inversion Optimization**: Optimize inversion algorithms
- **Inversion Patterns**: Find inversion patterns

#### **3. Sorting Problems**
- **Merge Sort**: Efficient sorting with inversion counting
- **Sorting Analysis**: Analyze sorting algorithms
- **Sorting Optimization**: Optimize sorting operations
- **Sorting Patterns**: Find sorting patterns

#### **4. Array Problems**
- **Array Traversal**: Traverse arrays efficiently
- **Array Manipulation**: Manipulate arrays
- **Array Analysis**: Analyze array properties
- **Array Optimization**: Optimize array operations

#### **5. Counting Problems**
- **Counting Algorithms**: Efficient counting algorithms
- **Counting Optimization**: Optimize counting operations
- **Counting Analysis**: Analyze counting properties
- **Counting Techniques**: Various counting techniques

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    
    result = count_permutation_inversions(arr)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute inversions for different array segments
def precompute_inversions(arr):
    n = len(arr)
    inversions = {}
    
    for start in range(n):
        for end in range(start, n):
            segment = arr[start:end+1]
            inv = count_inversions(segment)
            inversions[(start, end)] = inv
    
    return inversions

# Answer range queries efficiently
def range_query(inversions, start, end):
    return inversions.get((start, end), 0)
```

#### **3. Interactive Problems**
```python
# Interactive inversion analyzer
def interactive_inversion_analyzer():
    n = int(input("Enter array length: "))
    arr = list(map(int, input("Enter array: ").split()))
    
    print("Array:", arr)
    
    while True:
        query = input("Enter query (inversions/weighted/constrained/circular/range/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "inversions":
            result = count_permutation_inversions(arr)
            print(f"Inversions: {result}")
        elif query == "weighted":
            weights = list(map(int, input("Enter weights: ").split()))
            result = weighted_permutation_inversions(arr, weights)
            print(f"Weighted inversions: {result}")
        elif query == "constrained":
            max_dist = int(input("Enter max distance: "))
            result = constrained_permutation_inversions(arr, max_dist)
            print(f"Constrained inversions: {result}")
        elif query == "circular":
            result = circular_permutation_inversions(arr)
            print(f"Circular inversions: {result}")
        elif query == "range":
            start, end = map(int, input("Enter start and end: ").split())
            result = range_permutation_inversions(arr, start, end)
            print(f"Range inversions: {result}")
        elif query == "dynamic":
            counter = DynamicInversionCounter(arr)
            print(f"Initial inversions: {counter.get_inversion_count()}")
            
            while True:
                cmd = input("Enter command (swap/count/back): ")
                if cmd == "back":
                    break
                elif cmd == "swap":
                    i, j = map(int, input("Enter indices to swap: ").split())
                    counter.swap_elements(i, j)
                    print("Elements swapped")
                elif cmd == "count":
                    result = counter.get_inversion_count()
                    print(f"Current inversions: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Permutation Theory**: Mathematical theory of permutations
- **Inversion Theory**: Properties of inversions
- **Sorting Theory**: Mathematical properties of sorting
- **Inclusion-Exclusion**: Count using inclusion-exclusion

#### **2. Number Theory**
- **Permutation Patterns**: Mathematical patterns in permutations
- **Inversion Sequences**: Sequences of inversion counts
- **Modular Arithmetic**: Permutation operations with modular arithmetic
- **Number Sequences**: Sequences in permutation counting

#### **3. Optimization Theory**
- **Permutation Optimization**: Optimize permutation operations
- **Inversion Optimization**: Optimize inversion counting
- **Algorithm Optimization**: Optimize algorithms
- **Complexity Analysis**: Analyze algorithm complexity

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Merge Sort**: Efficient sorting algorithms
- **Binary Indexed Trees**: For range queries
- **Segment Trees**: For dynamic updates
- **Dynamic Programming**: For optimization problems

#### **2. Mathematical Concepts**
- **Combinatorics**: Foundation for counting problems
- **Permutation Theory**: Mathematical properties of permutations
- **Inversion Theory**: Properties of inversions
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Sorting Techniques**: Efficient sorting techniques
- **Inversion Analysis**: Inversion analysis techniques

---

*This analysis demonstrates efficient permutation inversion counting techniques and shows various extensions for permutation and sorting problems.* 