---
layout: simple
title: "Missing Number"
permalink: /problem_soulutions/introductory_problems/missing_number_analysis
---

# Missing Number

## Problem Description

**Problem**: You are given all numbers between 1,2,…,n except one. Your task is to find the missing number.

**Input**: 
- First line: n (2 ≤ n ≤ 2×10⁵)
- Second line: n-1 integers (each between 1 and n)

**Output**: The missing number.

**Example**:
```
Input:
5
2 3 1 5

Output:
4

Explanation: The numbers 1,2,3,4,5 are expected, but 4 is missing.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- We have numbers from 1 to n, but one is missing
- We need to find which number is missing
- The input has n-1 numbers, we need to find the nth one

**Key Observations:**
- Numbers are from 1 to n (inclusive)
- Exactly one number is missing
- We can use mathematical formulas to find the missing number

### Step 2: Mathematical Approach
**Idea**: Use the sum formula to find the missing number.

**Key Insight:**
- Sum of numbers from 1 to n = n(n+1)/2
- Sum of given numbers = sum of all except missing number
- Missing number = expected sum - actual sum

```python
def solve_mathematical(n, arr):
    # Expected sum of numbers from 1 to n
    expected_sum = n * (n + 1) // 2
    
    # Actual sum of given numbers
    actual_sum = sum(arr)
    
    # Missing number
    missing = expected_sum - actual_sum
    
    return missing
```

**Why this works:**
- We know the expected sum from 1 to n
- We calculate the actual sum of given numbers
- The difference is the missing number

### Step 3: XOR Approach
**Idea**: Use XOR properties to find the missing number.

```python
def solve_xor(n, arr):
    # XOR all numbers from 1 to n
    expected_xor = 0
    for i in range(1, n + 1):
        expected_xor ^= i
    
    # XOR all given numbers
    actual_xor = 0
    for num in arr:
        actual_xor ^= num
    
    # Missing number
    missing = expected_xor ^ actual_xor
    
    return missing
```

**Why this works:**
- XOR of a number with itself is 0
- XOR is associative and commutative
- XOR of all numbers except one gives us the missing number

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_missing_number():
    n = int(input())
    arr = list(map(int, input().split()))
    
    # Method 1: Mathematical approach
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(arr)
    missing = expected_sum - actual_sum
    
    return missing

# Main execution
if __name__ == "__main__":
    result = solve_missing_number()
    print(result)
```

**Why this works:**
- Simple and efficient mathematical approach
- Handles all edge cases correctly
- Easy to understand and implement

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (5, [2, 3, 1, 5], 4),
        (3, [1, 2], 3),
        (4, [1, 3, 4], 2),
        (2, [1], 2),
    ]
    
    for n, arr, expected in test_cases:
        result = solve_test(n, arr)
        print(f"n={n}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, arr):
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Mathematical Approach**: O(n) - sum the array
- **XOR Approach**: O(n) - XOR all numbers
- **Space**: O(1) - we only use a few variables

### Why These Solutions Work
- **Mathematical**: Uses sum formula to find missing number
- **XOR**: Uses XOR properties to find missing number
- **Both**: Handle all cases correctly

## 🎯 Key Insights

### 1. **Sum Formula**
- Sum of numbers from 1 to n = n(n+1)/2
- Missing number = expected sum - actual sum

### 2. **XOR Properties**
- a ⊕ a = 0 (XOR with itself gives 0)
- a ⊕ 0 = a (XOR with 0 gives the number)
- XOR is associative and commutative

### 3. **Problem Constraints**
- Numbers are from 1 to n (inclusive)
- Exactly one number is missing
- This makes the problem solvable with simple math

## 🔗 Related Problems

- **[Two Sets](/cses-analyses/problem_soulutions/introductory_problems/two_sets_analysis)**: Array manipulation
- **[Increasing Array](/cses-analyses/problem_soulutions/introductory_problems/increasing_array_analysis)**: Array problems
- **[Repetitions](/cses-analyses/problem_soulutions/introductory_problems/repetitions_analysis)**: Pattern problems

## 🎯 Problem Variations

### Variation 1: Multiple Missing Numbers
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

### Variation 2: Range with Gaps
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

### Variation 3: Duplicate Numbers Allowed
**Problem**: Find the number that appears odd number of times (others appear even times).

```python
def odd_frequency_number(numbers):
    result = 0
    for num in numbers:
        result ^= num
    return result
```

### Variation 4: Missing Number with Constraints
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

### Variation 5: Missing Number in Sorted Array
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

## 📚 Learning Points

1. **Mathematical Formulas**: Using sum formulas efficiently
2. **XOR Operations**: Understanding XOR properties
3. **Problem Analysis**: Identifying mathematical patterns
4. **Multiple Approaches**: Different ways to solve the same problem

---

**This is a great introduction to mathematical problem-solving and XOR operations!** 🎯 