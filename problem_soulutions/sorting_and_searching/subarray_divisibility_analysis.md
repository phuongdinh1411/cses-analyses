---
layout: simple
title: CSES Subarray Divisibility - Problem Analysis
permalink: /problem_soulutions/sorting_and_searching/subarray_divisibility_analysis/
---

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Subarray Divisibility with Range Constraints**
**Problem**: Find subarrays with sum divisible by k and length in range [L, R].
```python
def subarray_divisibility_with_length_constraints(n, k, arr, L, R):
    count = 0
    prefix_sum = 0
    mod_positions = {0: [0]}  # Store positions for each remainder
    
    for i in range(n):
        prefix_sum += arr[i]
        remainder = prefix_sum % k
        
        if remainder in mod_positions:
            # Check positions that satisfy length constraints
            for pos in mod_positions[remainder]:
                length = i - pos
                if L <= length <= R:
                    count += 1
        
        if remainder not in mod_positions:
            mod_positions[remainder] = []
        mod_positions[remainder].append(i + 1)
    
    return count
```

#### **Variation 2: Subarray Divisibility with Multiple Divisors**
**Problem**: Find subarrays divisible by any of the given divisors.
```python
def subarray_divisibility_multiple_divisors(n, divisors, arr):
    count = 0
    prefix_sum = 0
    mod_counts = {divisor: {0: 1} for divisor in divisors}
    
    for i in range(n):
        prefix_sum += arr[i]
        
        for divisor in divisors:
            remainder = prefix_sum % divisor
            
            if remainder in mod_counts[divisor]:
                count += mod_counts[divisor][remainder]
            
            mod_counts[divisor][remainder] = mod_counts[divisor].get(remainder, 0) + 1
    
    return count
```

#### **Variation 3: Subarray Divisibility with Constraints**
**Problem**: Find subarrays divisible by k that satisfy additional constraints.
```python
def subarray_divisibility_with_constraints(n, k, arr, constraints):
    # constraints[i] = list of indices that cannot be used with index i
    count = 0
    prefix_sum = 0
    mod_positions = {0: [0]}
    
    for i in range(n):
        prefix_sum += arr[i]
        remainder = prefix_sum % k
        
        if remainder in mod_positions:
            for pos in mod_positions[remainder]:
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
        
        if remainder not in mod_positions:
            mod_positions[remainder] = []
        mod_positions[remainder].append(i + 1)
    
    return count
```

#### **Variation 4: Subarray Divisibility with Dynamic Updates**
**Problem**: Support adding and removing elements dynamically.
```python
class DynamicSubarrayDivisibility:
    def __init__(self, k):
        self.k = k
        self.arr = []
        self.prefix_sums = [0]
        self.mod_counts = {0: 1}
        self.count = 0
    
    def add_element(self, element):
        self.arr.append(element)
        new_prefix = self.prefix_sums[-1] + element
        self.prefix_sums.append(new_prefix)
        
        remainder = new_prefix % self.k
        
        if remainder in self.mod_counts:
            self.count += self.mod_counts[remainder]
        
        self.mod_counts[remainder] = self.mod_counts.get(remainder, 0) + 1
        return self.count
    
    def remove_element(self, index):
        if 0 <= index < len(self.arr):
            # Remove element and rebuild prefix sums
            self.arr.pop(index)
            self.prefix_sums = [0]
            self.mod_counts = {0: 1}
            self.count = 0
            
            for element in self.arr:
                new_prefix = self.prefix_sums[-1] + element
                self.prefix_sums.append(new_prefix)
                
                remainder = new_prefix % self.k
                if remainder in self.mod_counts:
                    self.count += self.mod_counts[remainder]
                
                self.mod_counts[remainder] = self.mod_counts.get(remainder, 0) + 1
        
        return self.count
    
    def get_count(self):
        return self.count
```

#### **Variation 5: Subarray Divisibility with Weighted Elements**
**Problem**: Each element has a weight. Find subarrays divisible by k with total weight ≤ W.
```python
def subarray_divisibility_weighted(n, k, arr, weights, max_weight):
    count = 0
    prefix_sum = 0
    prefix_weight = 0
    mod_positions = {0: [(0, 0)]}  # (position, weight)
    
    for i in range(n):
        prefix_sum += arr[i]
        prefix_weight += weights[i]
        remainder = prefix_sum % k
        
        if remainder in mod_positions:
            for pos, weight in mod_positions[remainder]:
                current_weight = prefix_weight - weight
                if current_weight <= max_weight:
                    count += 1
        
        if remainder not in mod_positions:
            mod_positions[remainder] = []
        mod_positions[remainder].append((i + 1, prefix_weight))
    
    return count
```

### 🔗 **Related Problems & Concepts**

#### **1. Prefix Sum Problems**
- **Range Sum Queries**: Answer range sum queries efficiently
- **2D Prefix Sum**: Handle 2D range queries
- **Difference Array**: Handle range updates efficiently
- **Binary Indexed Tree**: Dynamic range queries

#### **2. Modular Arithmetic Problems**
- **Modular Exponentiation**: Efficient modular exponentiation
- **Modular Inverse**: Find modular inverse
- **Chinese Remainder Theorem**: Solve modular equations
- **Fermat's Little Theorem**: Modular arithmetic properties

#### **3. Subarray Problems**
- **Maximum Subarray Sum**: Find maximum subarray sum
- **Subarray with Given Sum**: Find subarray with given sum
- **Subarray with Zero Sum**: Find subarrays with zero sum
- **Subarray Problems**: Various subarray problems

#### **4. Number Theory Problems**
- **Divisibility**: Properties of divisibility
- **Prime Factorization**: Breaking numbers into primes
- **GCD/LCM**: Greatest common divisor and least common multiple
- **Number Theory**: Properties of numbers

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
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}
    
    for i in range(n):
        prefix_sum += arr[i]
        remainder = prefix_sum % k
        
        if remainder in mod_count:
            count += mod_count[remainder]
        
        mod_count[remainder] = mod_count.get(remainder, 0) + 1
    
    print(count)
```

#### **2. Range Queries**
```python
# Precompute divisible subarray counts for different ranges
def precompute_divisible_counts(arr, k):
    n = len(arr)
    count_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            subarray = arr[i:j+1]
            count = 0
            prefix_sum = 0
            mod_count = {0: 1}
            
            for element in subarray:
                prefix_sum += element
                remainder = prefix_sum % k
                
                if remainder in mod_count:
                    count += mod_count[remainder]
                
                mod_count[remainder] = mod_count.get(remainder, 0) + 1
            
            count_matrix[i][j] = count
    
    return count_matrix

# Answer queries about divisible subarray counts for ranges
def divisible_count_query(count_matrix, l, r):
    return count_matrix[l][r]
```

#### **3. Interactive Problems**
```python
# Interactive subarray divisibility finder
def interactive_subarray_divisibility():
    n = int(input("Enter array size: "))
    k = int(input("Enter divisor: "))
    arr = list(map(int, input("Enter array: ").split()))
    
    print(f"Array: {arr}")
    print(f"Divisor: {k}")
    
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}
    subarrays = []
    
    for i in range(n):
        prefix_sum += arr[i]
        remainder = prefix_sum % k
        print(f"Position {i}: prefix_sum = {prefix_sum}, remainder = {remainder}")
        
        if remainder in mod_count:
            # Found subarrays ending at position i
            for start_pos in range(mod_count[remainder]):
                subarray = arr[start_pos:i+1]
                subarrays.append(subarray)
                count += 1
                print(f"Found subarray: {subarray} with sum {prefix_sum} divisible by {k}")
        
        mod_count[remainder] = mod_count.get(remainder, 0) + 1
        print(f"Updated mod_count: {mod_count}")
    
    print(f"Total subarrays divisible by {k}: {count}")
    print(f"Subarrays: {subarrays}")
```

### 🧮 **Mathematical Extensions**

#### **1. Number Theory**
- **Divisibility Properties**: Properties of divisibility
- **Modular Arithmetic**: Working with remainders
- **Prime Factorization**: Breaking numbers into primes
- **GCD/LCM**: Greatest common divisor and least common multiple

#### **2. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Prefix Sum Analysis**: Analysis of prefix sum technique
- **Modular Arithmetic Analysis**: Analysis of modular operations
- **Lower Bounds**: Establishing problem lower bounds

#### **3. Mathematical Properties**
- **Divisibility Rules**: Rules for divisibility
- **Modular Properties**: Properties of modular arithmetic
- **Number Theory**: Properties of numbers
- **Combinatorics**: Counting and arrangement

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Prefix Sum**: Efficient range sum calculation
- **Modular Arithmetic**: Efficient modular operations
- **Number Theory**: Efficient number theory algorithms
- **Subarray Algorithms**: Efficient subarray algorithms

#### **2. Mathematical Concepts**
- **Number Theory**: Properties of numbers
- **Modular Arithmetic**: Working with remainders
- **Divisibility**: Properties of divisibility
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Prefix Sum Implementation**: Efficient prefix sum
- **Modular Arithmetic**: Efficient modular operations
- **Algorithm Design**: Problem-solving strategies
- **Complexity Analysis**: Performance evaluation

---

*This analysis demonstrates prefix sum and modular arithmetic techniques for subarray divisibility problems.* 