---
layout: simple
title: "Permutation Inversions"
permalink: /problem_soulutions/counting_problems/permutation_inversions_analysis
---


# Permutation Inversions

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of inversions in permutations and their properties
- Apply merge sort algorithm to count inversions efficiently
- Implement binary indexed tree (Fenwick tree) for inversion counting
- Optimize inversion counting algorithms for large permutations
- Handle edge cases in inversion counting (sorted arrays, reverse sorted arrays)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Merge sort, binary indexed tree, segment tree, divide and conquer
- **Data Structures**: Arrays, binary indexed trees, segment trees, merge sort arrays
- **Mathematical Concepts**: Permutations, inversions, divide and conquer, counting principles
- **Programming Skills**: Merge sort implementation, binary indexed tree operations, divide and conquer
- **Related Problems**: Counting Permutations (permutation properties), Sorting algorithms (merge sort), Range Queries (binary indexed tree)

## 📋 Problem Description

Given a permutation of numbers from 1 to n, count the number of inversions. An inversion is a pair of indices (i,j) where i < j and a[i] > a[j].

This is a classic algorithmic problem where we need to count the number of inversions in a permutation. An inversion occurs when a larger element appears before a smaller element. We can solve this using merge sort, binary indexed tree, or segment tree.

**Input**: 
- First line: integer n (size of the permutation)
- Second line: n integers (the permutation)

**Output**: 
- Print one integer: the number of inversions

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- The input is a valid permutation of 1 to n

**Example**:
```
Input:
4
3 1 4 2

Output:
3
```

**Explanation**: 
In the permutation [3, 1, 4, 2], there are 3 inversions:
1. (0, 1): 3 > 1 (indices 0 and 1)
2. (0, 3): 3 > 2 (indices 0 and 3)
3. (2, 3): 4 > 2 (indices 2 and 3)

These are the pairs where a larger element appears before a smaller element.

### 📊 Visual Example

**Input Permutation:**
```
Position: 0  1  2  3
Value:    3  1  4  2
```

**Inversion Analysis:**
```
Check all pairs (i,j) where i < j:

Pair (0,1): a[0]=3, a[1]=1
┌─────────────────────────────────────┐
│ 3 > 1 ✓ (inversion found)          │
│ Count: 1                            │
└─────────────────────────────────────┘

Pair (0,2): a[0]=3, a[2]=4
┌─────────────────────────────────────┐
│ 3 < 4 ✗ (not an inversion)         │
│ Count: 1                            │
└─────────────────────────────────────┘

Pair (0,3): a[0]=3, a[3]=2
┌─────────────────────────────────────┐
│ 3 > 2 ✓ (inversion found)          │
│ Count: 2                            │
└─────────────────────────────────────┘

Pair (1,2): a[1]=1, a[2]=4
┌─────────────────────────────────────┐
│ 1 < 4 ✗ (not an inversion)         │
│ Count: 2                            │
└─────────────────────────────────────┘

Pair (1,3): a[1]=1, a[3]=2
┌─────────────────────────────────────┐
│ 1 < 2 ✗ (not an inversion)         │
│ Count: 2                            │
└─────────────────────────────────────┘

Pair (2,3): a[2]=4, a[3]=2
┌─────────────────────────────────────┐
│ 4 > 2 ✓ (inversion found)          │
│ Count: 3                            │
└─────────────────────────────────────┘

Total inversions: 3
```

**Merge Sort Approach:**
```
Divide the array into two halves and count inversions:
┌─────────────────────────────────────┐
│ Left half: [3, 1]                  │
│ Right half: [4, 2]                 │
│                                     │
│ Inversions within left: 1          │
│ Inversions within right: 1         │
│ Inversions across: 1               │
│ Total: 1 + 1 + 1 = 3              │
└─────────────────────────────────────┘
```

**Merge Sort Process:**
```
Step 1: Divide
┌─────────────────────────────────────┐
│ [3, 1, 4, 2]                       │
│         │                           │
│    [3, 1]    [4, 2]                │
│       │         │                   │
│    [3] [1]   [4] [2]               │
└─────────────────────────────────────┘

Step 2: Merge and count inversions
┌─────────────────────────────────────┐
│ Merge [3] and [1]:                 │
│ - 3 > 1, so 3 goes after 1        │
│ - Inversion count: 1               │
│ - Result: [1, 3]                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Merge [4] and [2]:                 │
│ - 4 > 2, so 4 goes after 2        │
│ - Inversion count: 1               │
│ - Result: [2, 4]                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Merge [1, 3] and [2, 4]:           │
│ - 1 < 2, so 1 goes first           │
│ - 3 > 2, so 2 goes next            │
│ - Inversion count: 1 (3 > 2)       │
│ - Result: [1, 2, 3, 4]             │
└─────────────────────────────────────┘
```

**Binary Indexed Tree Approach:**
```
Coordinate compression and BIT:
┌─────────────────────────────────────┐
│ Original: [3, 1, 4, 2]             │
│ Compressed: [2, 0, 3, 1]           │
│                                     │
│ Process from right to left:        │
│ - Element 2: query(0) = 0          │
│ - Element 4: query(2) = 0          │
│ - Element 1: query(1) = 1          │
│ - Element 3: query(3) = 2          │
│ Total: 0 + 0 + 1 + 2 = 3          │
└─────────────────────────────────────┘
```

**Algorithm Flowchart:**
```
┌─────────────────────────────────────┐
│ Start: Read permutation            │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Use merge sort to count inversions │
│ while sorting the array            │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return total inversion count       │
└─────────────────────────────────────┘
```

**Key Insight Visualization:**
```
During merge sort, when we merge two sorted halves:
┌─────────────────────────────────────┐
│ Left: [1, 3] (sorted)              │
│ Right: [2, 4] (sorted)             │
│                                     │
│ When 3 > 2:                        │
│ - All elements after 3 in left     │
│   are also > 2                     │
│ - Inversion count += 1             │
│ - This counts all inversions       │
│   between left and right           │
└─────────────────────────────────────┘

Example:
┌─────────────────────────────────────┐
│ Left: [1, 3]                       │
│ Right: [2, 4]                      │
│                                     │
│ Merge: 1 < 2, so 1 goes first      │
│ Merge: 3 > 2, so 2 goes next       │
│ - Inversion: (3, 2)                │
│ - Count: 1                         │
│                                     │
│ Continue: 3 < 4, so 3 goes next    │
│ Continue: 4 goes last              │
└─────────────────────────────────────┘
```

**Time Complexity Analysis:**
```
Brute Force: O(n²)
- Check all n(n-1)/2 pairs
- For each pair, compare values

Merge Sort: O(n log n)
- Divide: O(log n) levels
- Merge: O(n) work per level
- Total: O(n log n)

Binary Indexed Tree: O(n log n)
- Coordinate compression: O(n log n)
- BIT operations: O(log n) per element
- Total: O(n log n)
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
## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n²) for the naive approach, O(n log n) for merge sort approach
- **Space Complexity**: O(n) for storing the array and temporary arrays
- **Why it works**: We use merge sort to count inversions during the merging process

### Key Implementation Points
- Use merge sort to count inversions efficiently
- Count inversions during the merge step
- Handle edge cases like single elements
- Optimize by using binary indexed tree for dynamic updates

## 🎯 Key Insights

### Important Concepts and Patterns
- **Merge Sort**: Essential for counting inversions efficiently
- **Binary Indexed Tree**: Useful for dynamic inversion counting
- **Permutation Analysis**: Understanding inversion properties
- **Divide and Conquer**: Breaking down the problem into smaller parts

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Permutation Inversions with Range Queries**
```python
def permutation_inversions_range_queries(n, arr, queries):
    # Count inversions for range queries
    results = []
    
    for query in queries:
        l, r = query
        # Extract subarray
        subarray = arr[l:r+1]
        
        # Count inversions in subarray using merge sort
        def merge_sort_count(arr):
            if len(arr) <= 1:
                return arr, 0
            
            mid = len(arr) // 2
            left, left_inversions = merge_sort_count(arr[:mid])
            right, right_inversions = merge_sort_count(arr[mid:])
            
            merged, split_inversions = merge(left, right)
            total_inversions = left_inversions + right_inversions + split_inversions
            
            return merged, total_inversions
        
        def merge(left, right):
            result = []
            i = j = 0
            inversions = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    inversions += len(left) - i
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            
            return result, inversions
        
        _, inversions = merge_sort_count(subarray)
        results.append(inversions)
    
    return results

# Example usage
n = 5
arr = [3, 1, 4, 2, 5]
queries = [(0, 2), (1, 3), (0, 4)]
results = permutation_inversions_range_queries(n, arr, queries)
for i, count in enumerate(results):
    print(f"Query {i} inversions: {count}")
```

#### **2. Permutation Inversions with Updates**
```python
def permutation_inversions_with_updates(n, arr, updates):
    # Count inversions with dynamic updates
    results = []
    
    def count_inversions(arr):
        def merge_sort_count(arr):
            if len(arr) <= 1:
                return arr, 0
            
            mid = len(arr) // 2
            left, left_inversions = merge_sort_count(arr[:mid])
            right, right_inversions = merge_sort_count(arr[mid:])
            
            merged, split_inversions = merge(left, right)
            total_inversions = left_inversions + right_inversions + split_inversions
            
            return merged, total_inversions
        
        def merge(left, right):
            result = []
            i = j = 0
            inversions = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    inversions += len(left) - i
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            
            return result, inversions
        
        _, inversions = merge_sort_count(arr)
        return inversions
    
    # Initial count
    current_inversions = count_inversions(arr)
    results.append(current_inversions)
    
    # Process updates
    for update in updates:
        pos, new_value = update
        arr[pos] = new_value
        current_inversions = count_inversions(arr)
        results.append(current_inversions)
    
    return results

# Example usage
n = 4
arr = [3, 1, 4, 2]
updates = [(1, 5), (2, 1)]
results = permutation_inversions_with_updates(n, arr, updates)
for i, count in enumerate(results):
    print(f"After update {i} inversions: {count}")
```

#### **3. Permutation Inversions with Multiple Arrays**
```python
def permutation_inversions_multiple_arrays(arrays):
    # Count inversions for multiple arrays
    results = {}
    
    for i, arr in enumerate(arrays):
        def merge_sort_count(arr):
            if len(arr) <= 1:
                return arr, 0
            
            mid = len(arr) // 2
            left, left_inversions = merge_sort_count(arr[:mid])
            right, right_inversions = merge_sort_count(arr[mid:])
            
            merged, split_inversions = merge(left, right)
            total_inversions = left_inversions + right_inversions + split_inversions
            
            return merged, total_inversions
        
        def merge(left, right):
            result = []
            i = j = 0
            inversions = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    inversions += len(left) - i
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            
            return result, inversions
        
        _, inversions = merge_sort_count(arr)
        results[i] = inversions
    
    return results

# Example usage
arrays = [
    [3, 1, 4, 2],
    [1, 2, 3, 4],
    [4, 3, 2, 1]
]
results = permutation_inversions_multiple_arrays(arrays)
for i, count in results.items():
    print(f"Array {i} inversions: {count}")
```

#### **4. Permutation Inversions with Statistics**
```python
def permutation_inversions_with_statistics(n, arr):
    # Count inversions and provide statistics
    def merge_sort_count(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left, left_inversions = merge_sort_count(arr[:mid])
        right, right_inversions = merge_sort_count(arr[mid:])
        
        merged, split_inversions = merge(left, right)
        total_inversions = left_inversions + right_inversions + split_inversions
        
        return merged, total_inversions
    
    def merge(left, right):
        result = []
        i = j = 0
        inversions = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                inversions += len(left) - i
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result, inversions
    
    _, total_inversions = merge_sort_count(arr)
    
    # Calculate statistics
    max_possible_inversions = n * (n - 1) // 2
    inversion_rate = total_inversions / max_possible_inversions if max_possible_inversions > 0 else 0
    
    # Count inversions for each element
    element_inversions = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                element_inversions[i] += 1
    
    statistics = {
        "total_inversions": total_inversions,
        "array_size": n,
        "max_possible_inversions": max_possible_inversions,
        "inversion_rate": inversion_rate,
        "element_inversions": element_inversions,
        "max_element_inversions": max(element_inversions) if element_inversions else 0
    }
    
    return total_inversions, statistics

# Example usage
n = 4
arr = [3, 1, 4, 2]
count, stats = permutation_inversions_with_statistics(n, arr)
print(f"Total inversions: {count}")
print(f"Statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **Sorting Algorithms**: Merge sort, Quick sort
- **Data Structures**: Binary indexed tree, Segment tree
- **Combinatorics**: Permutation counting, Arrangement counting
- **Divide and Conquer**: Merge sort, Binary search

## 📚 Learning Points

### Key Takeaways
- **Merge sort** is essential for counting inversions efficiently
- **Binary indexed tree** is useful for dynamic inversion counting
- **Permutation analysis** requires understanding inversion properties
- **Divide and conquer** helps break down complex problems

---

*This analysis demonstrates efficient permutation inversion counting techniques and shows various extensions for permutation and sorting problems.* 