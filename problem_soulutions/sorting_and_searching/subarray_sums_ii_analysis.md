---
layout: simple
title: CSES Subarray Sums II - Problem Analysis
permalink: /problem_soulutions/sorting_and_searching/subarray_sums_ii_analysis/
---

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Subarray Sums with Negative Numbers and Constraints**
**Problem**: Find subarrays with sum x where elements must satisfy certain constraints.
```python
def subarray_sums_with_negative_constraints(n, x, arr, constraints):
    # constraints[i] = list of indices that cannot be used with index i
    count = 0
    prefix_sum = 0
    sum_positions = {0: [0]}
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum - x in sum_positions:
            for pos in sum_positions[prefix_sum - x]:
                # Check if subarray [pos, i] satisfies constraints
                valid = True
                for j in range(pos, i + 1):
                    for constraint_idx in constraints.get(j, []):
                        if pos <= constraint_idx <= i:
                            valid = False
                            break
                    if not valid:
                        break
                
                if valid:
                    count += 1
        
        if prefix_sum not in sum_positions:
            sum_positions[prefix_sum] = []
        sum_positions[prefix_sum].append(i + 1)
    
    return count
```

#### **Variation 2: Subarray Sums with Range Constraints and Negative Numbers**
**Problem**: Find subarrays with sum in range [L, R] including negative numbers.
```python
def subarray_sums_negative_range(n, L, R, arr):
    count = 0
    prefix_sum = 0
    sum_positions = {0: [0]}
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # Count subarrays with sum in [L, R]
        for target in range(L, R + 1):
            if prefix_sum - target in sum_positions:
                count += len(sum_positions[prefix_sum - target])
        
        if prefix_sum not in sum_positions:
            sum_positions[prefix_sum] = []
        sum_positions[prefix_sum].append(i + 1)
    
    return count
```

#### **Variation 3: Subarray Sums with Modulo Constraints and Negative Numbers**
**Problem**: Find subarrays with sum congruent to x modulo m, handling negative numbers.
```python
def subarray_sums_negative_modulo(n, x, m, arr):
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}
    
    for i in range(n):
        prefix_sum += arr[i]
        # Handle negative numbers in modulo arithmetic
        prefix_sum_mod = ((prefix_sum % m) + m) % m
        
        # Find target modulo that gives sum x
        target_mod = ((prefix_sum_mod - x) % m + m) % m
        if target_mod in mod_count:
            count += mod_count[target_mod]
        
        mod_count[prefix_sum_mod] = mod_count.get(prefix_sum_mod, 0) + 1
    
    return count
```

#### **Variation 4: Subarray Sums with Dynamic Updates and Negative Numbers**
**Problem**: Support adding and removing elements dynamically, including negative numbers.
```python
class DynamicSubarraySumsNegative:
    def __init__(self, target_sum):
        self.target_sum = target_sum
        self.arr = []
        self.prefix_sums = [0]
        self.sum_count = {0: 1}
        self.count = 0
    
    def add_element(self, element):
        self.arr.append(element)
        new_prefix = self.prefix_sums[-1] + element
        self.prefix_sums.append(new_prefix)
        
        # Update count
        if new_prefix - self.target_sum in self.sum_count:
            self.count += self.sum_count[new_prefix - self.target_sum]
        
        self.sum_count[new_prefix] = self.sum_count.get(new_prefix, 0) + 1
        return self.count
    
    def remove_element(self, index):
        if 0 <= index < len(self.arr):
            # Remove element and rebuild prefix sums
            self.arr.pop(index)
            self.prefix_sums = [0]
            self.sum_count = {0: 1}
            self.count = 0
            
            for element in self.arr:
                new_prefix = self.prefix_sums[-1] + element
                self.prefix_sums.append(new_prefix)
                
                if new_prefix - self.target_sum in self.sum_count:
                    self.count += self.sum_count[new_prefix - self.target_sum]
                
                self.sum_count[new_prefix] = self.sum_count.get(new_prefix, 0) + 1
        
        return self.count
```

#### **Variation 5: Subarray Sums with Weighted Elements and Negative Numbers**
**Problem**: Each element has a weight. Find subarrays with sum x and total weight ≤ W.
```python
def subarray_sums_negative_weighted(n, x, arr, weights, max_weight):
    count = 0
    prefix_sum = 0
    prefix_weight = 0
    sum_positions = {0: [(0, 0)]}  # (position, weight)
    
    for i in range(n):
        prefix_sum += arr[i]
        prefix_weight += weights[i]
        
        if prefix_sum - x in sum_positions:
            for pos, weight in sum_positions[prefix_sum - x]:
                current_weight = prefix_weight - weight
                if current_weight <= max_weight:
                    count += 1
        
        if prefix_sum not in sum_positions:
            sum_positions[prefix_sum] = []
        sum_positions[prefix_sum].append((i + 1, prefix_weight))
    
    return count
```

### 🔗 **Related Problems & Concepts**

#### **1. Prefix Sum Problems**
- **Range Sum Queries**: Answer range sum queries efficiently
- **2D Prefix Sum**: Handle 2D range queries
- **Difference Array**: Handle range updates efficiently
- **Binary Indexed Tree**: Dynamic range queries

#### **2. Hash Table Problems**
- **Hash Table Implementation**: Custom hash table design
- **Collision Resolution**: Handle hash collisions
- **Load Factor**: Optimize hash table performance
- **Hash Functions**: Design good hash functions

#### **3. Subarray Problems**
- **Maximum Subarray Sum**: Find maximum subarray sum
- **Subarray with Given Sum**: Find subarray with given sum
- **Subarray Divisibility**: Find subarrays divisible by k
- **Subarray with Zero Sum**: Find subarrays with zero sum

#### **4. Negative Number Problems**
- **Negative Number Handling**: Handle negative numbers in algorithms
- **Modulo Arithmetic**: Work with negative numbers in modulo
- **Absolute Values**: Work with absolute values
- **Sign Analysis**: Analyze signs of numbers

#### **5. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Integer Programming**: Discrete optimization
- **Combinatorial Optimization**: Optimize discrete structures
- **Approximation Algorithms**: Find approximate solutions

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum - x in sum_count:
            count += sum_count[prefix_sum - x]
        
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    print(count)
```

#### **2. Range Queries**
```python
# Precompute subarray sums for different ranges with negative numbers
def precompute_subarray_sums_negative(arr):
    n = len(arr)
    sum_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            current_sum = 0
            for k in range(i, j + 1):
                current_sum += arr[k]
            sum_matrix[i][j] = current_sum
    
    return sum_matrix

# Answer queries about subarray sums for ranges
def sum_query_negative(sum_matrix, l, r):
    return sum_matrix[l][r]
```

#### **3. Interactive Problems**
```python
# Interactive subarray sum finder with negative numbers
def interactive_subarray_sums_negative():
    n = int(input("Enter array size: "))
    x = int(input("Enter target sum: "))
    arr = list(map(int, input("Enter array (can include negative numbers): ").split()))
    
    print(f"Array: {arr}")
    print(f"Target sum: {x}")
    
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}
    subarrays = []
    
    for i in range(n):
        prefix_sum += arr[i]
        print(f"Position {i}: prefix_sum = {prefix_sum}")
        
        if prefix_sum - x in sum_count:
            # Found subarrays ending at position i
            for start_pos in range(sum_count[prefix_sum - x]):
                subarray = arr[start_pos:i+1]
                subarrays.append(subarray)
                count += 1
                print(f"Found subarray: {subarray} with sum {x}")
        
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
        print(f"Updated sum_count: {sum_count}")
    
    print(f"Total subarrays with sum {x}: {count}")
    print(f"Subarrays: {subarrays}")
```

### 🧮 **Mathematical Extensions**

#### **1. Number Theory**
- **Properties of Sums**: Properties of number sums including negative numbers
- **Divisibility**: Properties of divisibility with negative numbers
- **Modular Arithmetic**: Working with remainders and negative numbers
- **Prime Factorization**: Breaking numbers into primes

#### **2. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Prefix Sum Analysis**: Analysis of prefix sum technique with negative numbers
- **Hash Table Analysis**: Analysis of hash table performance
- **Lower Bounds**: Establishing problem lower bounds

#### **3. Mathematical Properties**
- **Negative Number Properties**: Properties of negative numbers
- **Modular Properties**: Properties of modular arithmetic with negative numbers
- **Sum Properties**: Properties of sums including negative numbers
- **Combinatorics**: Counting and arrangement

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Prefix Sum**: Efficient range sum calculation with negative numbers
- **Hash Tables**: Efficient lookup data structures
- **Two Pointers**: Efficient array processing
- **Sliding Window**: Two-pointer technique

#### **2. Mathematical Concepts**
- **Number Theory**: Properties of numbers including negative numbers
- **Modular Arithmetic**: Working with remainders and negative numbers
- **Algorithm Analysis**: Complexity and correctness
- **Discrete Mathematics**: Discrete structures

#### **3. Programming Concepts**
- **Hash Table Usage**: Efficient data structures
- **Array Manipulation**: Efficient array operations with negative numbers
- **Algorithm Design**: Problem-solving strategies
- **Complexity Analysis**: Performance evaluation

---

*This analysis demonstrates prefix sum and hash table techniques for subarray problems with negative numbers.* 