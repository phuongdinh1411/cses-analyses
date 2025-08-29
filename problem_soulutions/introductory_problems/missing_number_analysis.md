---
layout: simple
title: "Missing Number"
permalink: /cses-analyses/problem_soulutions/introductory_problems/missing_number_analysis
---


# Missing Number

## Problem Statement
You are given all numbers between 1,2,…,n except one. Your task is to find the missing number.

### Input
The first input line contains an integer n.
The second line contains n−1 numbers. Each number is distinct and between 1 and n (inclusive).

### Output
Print the missing number.

### Constraints
- 2 ≤ n ≤ 2⋅10^5

### Example
```
Input:
5
2 3 1 5

Output:
4
```

## Solution Progression

### Approach 1: Brute Force Search - O(n²)
**Description**: For each number from 1 to n, check if it exists in the given array.

```python
def missing_number_brute_force(n, numbers):
    for i in range(1, n + 1):
        if i not in numbers:
            return i
    return -1  # Should not happen given problem constraints
```
**Why this is inefficient**: For each number from 1 to n, we're searching through the entire array to check if it exists. This leads to O(n²) complexity.

### Improvement 1: Using Set - O(n)
**Description**: Convert the array to a set for O(1) lookup time.

```python
def missing_number_set(n, numbers):
    number_set = set(numbers)
    
    for i in range(1, n + 1):
        if i not in number_set:
            return i
    return -1
```

**Why this improvement works**: By converting the array to a set, we can check if a number exists in O(1) time instead of O(n). This reduces the overall complexity from O(n²) to O(n).

### Improvement 2: Mathematical Formula - O(n)
**Description**: Use the sum formula to find the missing number.

```python
def missing_number_sum(n, numbers):
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(numbers)
    return expected_sum - actual_sum
```

**Why this improvement works**: The sum of numbers from 1 to n is n(n+1)/2. By calculating the expected sum and subtracting the actual sum of the given numbers, we get the missing number. This is both time and space efficient.

### Alternative: Using XOR - O(n)
**Description**: Use XOR properties to find the missing number.

```python
def missing_number_xor(n, numbers):
    xor_result = 0
    
    # XOR all numbers from 1 to n
    for i in range(1, n + 1):
        xor_result ^= i
    
    # XOR with all given numbers
    for num in numbers:
        xor_result ^= num
    
    return xor_result
```

**Why this works**: XOR has the property that a ^ a = 0 and a ^ 0 = a. By XORing all numbers from 1 to n and then XORing with all given numbers, the missing number will be the result.

## Final Optimal Solution

```python
n = int(input())
numbers = list(map(int, input().split()))

# Mathematical formula approach
expected_sum = n * (n + 1) // 2
actual_sum = sum(numbers)
missing = expected_sum - actual_sum

print(missing)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check each number in array |
| Set | O(n) | O(n) | Use set for O(1) lookup |
| Mathematical Formula | O(n) | O(1) | Use sum formula |
| XOR | O(n) | O(1) | Use XOR properties |

## Key Insights for Other Problems

### 1. **Mathematical Formula Approach**
**Principle**: Use mathematical properties and formulas to solve problems efficiently.
**Applicable to**:
- Sum-based problems
- Arithmetic sequences
- Mathematical properties
- Optimization problems

**Example Problems**:
- Missing number
- Sum of arithmetic sequence
- Mathematical series
- Number theory problems

### 2. **Set for Efficient Lookup**
**Principle**: Use sets when you need to check existence or uniqueness efficiently.
**Applicable to**:
- Existence checking
- Duplicate detection
- Unique element problems
- Lookup optimization

**Example Problems**:
- Two sum
- Duplicate detection
- Unique elements
- Existence problems

### 3. **XOR Properties**
**Principle**: XOR has useful properties for finding missing or duplicate elements.
**Applicable to**:
- Missing element problems
- Duplicate detection
- Bit manipulation
- Mathematical problems

**Example Problems**:
- Missing number
- Single number (duplicate detection)
- Bit manipulation
- Mathematical sequences

### 4. **Arithmetic Sequence Properties**
**Principle**: Use properties of arithmetic sequences to solve problems efficiently.
**Applicable to**:
- Sum problems
- Sequence problems
- Mathematical series
- Number theory

**Example Problems**:
- Sum of arithmetic sequence
- Missing number
- Mathematical series
- Number theory problems

## Notable Techniques

### 1. **Sum Formula Pattern**
```python
# Sum of numbers from 1 to n
expected_sum = n * (n + 1) // 2
actual_sum = sum(numbers)
missing = expected_sum - actual_sum
```

### 2. **Set for Lookup**
```python
# Convert to set for O(1) lookup
number_set = set(numbers)
for i in range(1, n + 1):
    if i not in number_set:
        return i
```

### 3. **XOR Pattern**
```python
# Use XOR to find missing element
xor_result = 0
for i in range(1, n + 1):
    xor_result ^= i
for num in numbers:
    xor_result ^= num
return xor_result
```

## Edge Cases to Remember

1. **n = 2**: Only one number given, missing is the other
2. **Large n**: Handle integer overflow in sum calculation
3. **All numbers present**: Should not happen given problem constraints
4. **Negative numbers**: Not applicable given problem constraints

## Problem-Solving Framework

1. **Identify mathematical properties**: Look for formulas or properties that can help
2. **Consider data structures**: Use appropriate data structures for efficiency
3. **Handle edge cases**: Consider special input values
4. **Choose optimal approach**: Balance time and space complexity
5. **Verify correctness**: Test with examples

---

*This analysis shows how to efficiently find missing elements using mathematical properties and data structures.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Multiple Missing Numbers**
**Problem**: Find k missing numbers from 1 to n.
```python
def multiple_missing_numbers(n, numbers, k):
    number_set = set(numbers)
    missing = []
    
    for i in range(1, n + 1):
        if i not in number_set:
            missing.append(i)
            if len(missing) == k:
                break
    
    return missing
```

#### **Variation 2: Range with Gaps**
**Problem**: Find missing numbers in range [a, b] instead of [1, n].
```python
def missing_in_range(a, b, numbers):
    number_set = set(numbers)
    missing = []
    
    for i in range(a, b + 1):
        if i not in number_set:
            missing.append(i)
    
    return missing
```

#### **Variation 3: Duplicate Numbers Allowed**
**Problem**: Find the number that appears odd number of times (others appear even times).
```python
def odd_frequency_number(numbers):
    result = 0
    for num in numbers:
        result ^= num
    return result
```

#### **Variation 4: Missing Number with Constraints**
**Problem**: Find missing number but you can only use O(1) extra space.
```python
def missing_number_constant_space(n, numbers):
    # Use XOR approach for O(1) space
    xor_result = 0
    
    for i in range(1, n + 1):
        xor_result ^= i
    
    for num in numbers:
        xor_result ^= num
    
    return xor_result
```

#### **Variation 5: Missing Number in Sorted Array**
**Problem**: Find missing number in a sorted array efficiently.
```python
def missing_in_sorted_array(numbers):
    n = len(numbers) + 1
    left, right = 0, len(numbers) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == mid + 1:
            left = mid + 1
        else:
            right = mid - 1
    
    return left + 1
```

### 🔗 **Related Problems & Concepts**

#### **1. Array Manipulation Problems**
- **Find Duplicate**: Find number that appears twice
- **Find Single Number**: Find number that appears once (others twice)
- **Majority Element**: Find element appearing more than n/2 times
- **First Missing Positive**: Find first missing positive integer

#### **2. Mathematical Sequence Problems**
- **Arithmetic Progression**: Find missing term in AP
- **Geometric Progression**: Find missing term in GP
- **Fibonacci Sequence**: Find missing Fibonacci number
- **Prime Numbers**: Find missing prime in sequence

#### **3. Bit Manipulation Problems**
- **Single Number**: Use XOR to find unique element
- **Power of Two**: Check if number is power of 2
- **Bit Counting**: Count set bits in number
- **Bit Manipulation**: Various bit operations

#### **4. Search Problems**
- **Binary Search**: Find element in sorted array
- **Linear Search**: Find element in unsorted array
- **Interpolation Search**: Search in uniformly distributed array
- **Exponential Search**: Search in unbounded array

#### **5. Counting Problems**
- **Frequency Count**: Count occurrences of each element
- **Mode Finding**: Find most frequent element
- **Range Counting**: Count elements in range
- **Distinct Elements**: Count unique elements

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    numbers = list(map(int, input().split()))
    
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(numbers)
    missing = expected_sum - actual_sum
    
    print(missing)
```

#### **2. Range Queries**
```python
# Precompute missing numbers for different ranges
def precompute_missing_numbers(max_n):
    missing_data = {}
    for n in range(2, max_n + 1):
        missing_data[n] = n * (n + 1) // 2
    
    return missing_data

# Answer queries about missing numbers
def missing_query(n, numbers, precomputed):
    expected_sum = precomputed[n]
    actual_sum = sum(numbers)
    return expected_sum - actual_sum
```

#### **3. Interactive Problems**
```python
# Interactive missing number game
def interactive_missing_number():
    n = int(input("Enter n: "))
    print(f"Think of a number from 1 to {n}")
    
    numbers = []
    for i in range(1, n + 1):
        response = input(f"Is {i} in your list? (y/n): ")
        if response.lower() == 'n':
            numbers.append(i)
    
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(numbers)
    missing = expected_sum - actual_sum
    
    print(f"The missing number is: {missing}")
```

### 🧮 **Mathematical Extensions**

#### **1. Sum Formulas**
- **Arithmetic Series**: Sum of consecutive integers
- **Geometric Series**: Sum of powers
- **Harmonic Series**: Sum of reciprocals
- **Square Numbers**: Sum of squares

#### **2. Number Theory**
- **Divisibility**: Properties of numbers
- **Prime Factorization**: Breaking numbers into primes
- **GCD/LCM**: Greatest common divisor and least common multiple
- **Modular Arithmetic**: Working with remainders

#### **3. Sequence Analysis**
- **Pattern Recognition**: Finding patterns in sequences
- **Recurrence Relations**: Mathematical relationships
- **Generating Functions**: Representing sequences as functions
- **Asymptotic Analysis**: Behavior for large numbers

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Search Algorithms**: Linear, binary, interpolation search
- **Sorting Algorithms**: Various sorting techniques
- **Hash Tables**: Efficient lookup data structures
- **Bit Manipulation**: XOR and other bit operations

#### **2. Mathematical Concepts**
- **Summation**: Mathematical sum formulas
- **Number Theory**: Properties of integers
- **Combinatorics**: Counting principles
- **Algebra**: Mathematical operations and properties

#### **3. Programming Concepts**
- **Array Manipulation**: Efficient array operations
- **Space-Time Trade-offs**: Optimizing for different constraints
- **Algorithm Analysis**: Understanding complexity
- **Data Structures**: Choosing appropriate structures

---

*This analysis demonstrates efficient techniques for finding missing numbers and shows various extensions for sequence problems.* 