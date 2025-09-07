---
layout: simple
title: "Subarray with Given Sum Analysis"
permalink: /problem_soulutions/sliding_window/subarray_with_given_sum_analysis
---


# Subarray with Given Sum Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand subarray sum existence problems and prefix sum techniques for sum detection
- Apply hash map and prefix sum techniques to efficiently detect subarrays with target sum
- Implement efficient algorithms with O(n) time complexity using prefix sums and hash maps
- Optimize subarray sum detection using prefix sum theory and hash map techniques
- Handle edge cases in subarray sum detection (negative numbers, zero sum, no solution, large arrays)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Prefix sums, hash maps, subarray sum problems, existence problems, prefix sum theory
- **Data Structures**: Hash maps, prefix sum arrays, sum tracking, existence tracking, frequency tracking
- **Mathematical Concepts**: Prefix sum theory, subarray sum mathematics, existence theory, hash map mathematics
- **Programming Skills**: Hash map implementation, prefix sum calculation, sum detection, algorithm implementation
- **Related Problems**: Subarray Sums I (counting version), Subarray Sum problems, Prefix sum problems, Hash map problems

## Problem Description

**Problem**: Given an array of n integers and a target sum x, find if there exists a subarray with sum x.

**Input**: 
- n: the size of the array
- x: the target sum
- arr: array of n integers

**Output**: "YES" if there exists a subarray with sum x, otherwise "NO".

**Example**:
```
Input:
5 7
2 -1 3 5 -2

Output:
YES

Explanation: 
The subarray [2, -1, 3, 5, -2] has sum 7.
We can verify: 2 + (-1) + 3 + 5 + (-2) = 7.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find if any subarray sums to a target value x
- Handle both positive and negative numbers
- Use efficient algorithms to avoid brute force
- Consider edge cases like empty subarray

**Key Observations:**
- Subarrays can have any length from 1 to n
- Need to track cumulative sums efficiently
- Hash set can help find target sums quickly
- Sliding window works for positive numbers only

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays to find one with sum x.

```python
def subarray_with_sum_naive(n, x, arr):
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum == x:
                return True
    return False
```

**Why this is inefficient:**
- Time complexity: O(n²)
- Lots of redundant calculations
- Not scalable for large inputs
- Inefficient sum calculation

### Step 3: Optimization with Prefix Sum and Hash Set
**Idea**: Use prefix sum and hash set to find subarray with target sum.

```python
def subarray_with_sum_prefix_sum(n, x, arr):
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        if prefix_sum - x in seen_sums:
            return True
        
        seen_sums.add(prefix_sum)
    
    return False
```

**Why this improvement works:**
- Time complexity: O(n)
- Prefix sum allows constant time subarray sum calculation
- Hash set tracks previous prefix sums efficiently
- Handles both positive and negative numbers

### Step 4: Alternative Approach with Sliding Window
**Idea**: Use sliding window technique for arrays with positive numbers.

```python
def subarray_with_sum_sliding_window(n, x, arr):
    # This works only for positive numbers
    left = 0
    current_sum = 0
    
    for right in range(n):
        current_sum += arr[right]
        
        while current_sum > x and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == x:
            return True
    
    return False
```

**Why this works:**
- Sliding window efficiently maintains valid sum
- Time complexity: O(n)
- Good for positive number arrays
- Limited applicability but very efficient

### Step 5: Complete Solution
**Putting it all together:**

```python
def solve_subarray_with_given_sum():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = check_subarray_with_sum(n, x, arr)
    print(result)

def check_subarray_with_sum(n, x, arr):
    """Check if there exists a subarray with sum x using prefix sum and hash set"""
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        if prefix_sum - x in seen_sums:
            return "YES"
        
        seen_sums.add(prefix_sum)
    
    return "NO"

# Main execution
if __name__ == "__main__":
    solve_subarray_with_given_sum()
```

**Why this works:**
- Optimal prefix sum + hash set algorithm approach
- Handles all edge cases correctly
- Efficient sum calculation
- Clear and readable code

```python
n, x = map(int, input().split())
arr = list(map(int, input().split()))

def subarray_with_sum_prefix_sum(n, x, arr):
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        if prefix_sum - x in seen_sums:
            return True
        
        seen_sums.add(prefix_sum)
    
    return False

result = subarray_with_sum_prefix_sum(n, x, arr)
print("YES" if result else "NO")
```

### Step 6: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 7, [2, -1, 3, 5, -2]), "YES"),
        ((4, 6, [1, 2, 3, 4]), "YES"),
        ((3, 10, [1, 2, 3]), "NO"),
        ((2, 5, [1, 4]), "YES"),
        ((1, 1, [1]), "YES"),
        ((3, 0, [1, -1, 0]), "YES"),
    ]
    
    for (n, x, arr), expected in test_cases:
        result = check_subarray_with_sum(n, x, arr)
        print(f"n={n}, x={x}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def check_subarray_with_sum(n, x, arr):
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)
    
    for num in arr:
        prefix_sum += num
        
        if prefix_sum - x in seen_sums:
            return "YES"
        
        seen_sums.add(prefix_sum)
    
    return "NO"

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with prefix sum
- **Space**: O(n) - hash set to store prefix sums

### Why This Solution Works
- **Prefix Sum**: Efficiently calculates subarray sums
- **Hash Set**: Tracks previous prefix sums for existence checking
- **Optimal Algorithm**: Best known approach for this problem
- **Edge Case Handling**: Properly handles empty subarray case

## 🎨 Visual Example

### Input Example
```
Input: n=5, x=7, arr=[2, -1, 3, 5, -2]
Output: YES (subarray with sum 7 exists)
```

### Array Visualization
```
Array: [2, -1, 3, 5, -2]
Index:  0   1  2  3   4
```

### Prefix Sum Calculation
```
Index:  -1   0   1   2   3   4
Array:  [ ]  [2] [-1] [3] [5] [-2]
Prefix:  0    2   1   4   9   7

Prefix[0] = 0
Prefix[1] = 0 + 2 = 2
Prefix[2] = 2 + (-1) = 1
Prefix[3] = 1 + 3 = 4
Prefix[4] = 4 + 5 = 9
Prefix[5] = 9 + (-2) = 7
```

### Subarray Sum Analysis
```
Target sum: x = 7

For each position i, check if any j < i has:
Prefix[i] - Prefix[j] = x
Prefix[j] = Prefix[i] - x

Position 0: Prefix[0] = 2
Target: 2 - 7 = -5
Is -5 in seen sums? No
Continue

Position 1: Prefix[1] = 1
Target: 1 - 7 = -6
Is -6 in seen sums? No
Continue

Position 2: Prefix[2] = 4
Target: 4 - 7 = -3
Is -3 in seen sums? No
Continue

Position 3: Prefix[3] = 9
Target: 9 - 7 = 2
Is 2 in seen sums? Yes! (at position 0)
Found subarray: arr[1:4] = [-1, 3, 5] → sum = 7
Return YES
```

### Hash Set Tracking
```
Hash set: {prefix_sums_seen}

Initialize: {0} (empty subarray)

i=0: prefix=2, target=2-7=-5
- Is -5 in set? No
- Add 2 to set: {0, 2}

i=1: prefix=1, target=1-7=-6
- Is -6 in set? No
- Add 1 to set: {0, 2, 1}

i=2: prefix=4, target=4-7=-3
- Is -3 in set? No
- Add 4 to set: {0, 2, 1, 4}

i=3: prefix=9, target=9-7=2
- Is 2 in set? Yes! ✓
- Found subarray with sum 7
- Return YES
```

### Verification
```
Found subarray: arr[1:4] = [-1, 3, 5]
Sum = (-1) + 3 + 5 = 7 ✓

Alternative subarray: arr[0:5] = [2, -1, 3, 5, -2]
Sum = 2 + (-1) + 3 + 5 + (-2) = 7 ✓
```

### Different Examples
```
Example 1: arr=[1, 2, 3, 4, 5], x=9
- Subarray [2, 3, 4] has sum 9
- Result: YES

Example 2: arr=[1, 2, 3, 4, 5], x=20
- No subarray has sum 20
- Result: NO

Example 3: arr=[-1, -2, -3], x=-6
- Subarray [-1, -2, -3] has sum -6
- Result: YES
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Prefix Sum +    │ O(n)         │ O(n)         │ Hash set     │
│ Hash Set        │              │              │ existence    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n²)        │ O(1)         │ Check all    │
│                 │              │              │ subarrays    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sliding Window  │ O(n)         │ O(1)         │ Only for     │
│                 │              │              │ positive     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Prefix Sum Technique**
- Convert range queries to point queries
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Hash Set for Existence**
- Track previous prefix sums efficiently
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Subarray Sum Calculation**
- Use prefix sum difference for subarray sums
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Subarray with Sum in Range
**Problem**: Check if there exists a subarray with sum in range [L, R].

```python
def check_subarray_with_sum_in_range(n, L, R, arr):
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)
    
    for num in arr:
        prefix_sum += num
        
        # Check if any previous prefix sum gives us a sum in [L, R]
        for prev_sum in seen_sums:
            current_sum = prefix_sum - prev_sum
            if L <= current_sum <= R:
                return "YES"
        
        seen_sums.add(prefix_sum)
    
    return "NO"

# Example usage
result = check_subarray_with_sum_in_range(5, 5, 10, [2, -1, 3, 5, -2])
print(f"Subarray with sum in [5, 10]: {result}")
```

### Variation 2: Subarray with Even Sum
**Problem**: Check if there exists a subarray with even sum.

```python
def check_subarray_with_even_sum(n, arr):
    prefix_sum = 0
    even_seen = set()
    odd_seen = set()
    even_seen.add(0)
    
    for num in arr:
        prefix_sum += num
        
        if prefix_sum % 2 == 0:
            # Even sum, look for previous even prefix sum
            if prefix_sum in even_seen:
                return "YES"
            even_seen.add(prefix_sum)
        else:
            # Odd sum, look for previous odd prefix sum
            if prefix_sum in odd_seen:
                return "YES"
            odd_seen.add(prefix_sum)
    
    return "NO"

# Example usage
result = check_subarray_with_even_sum(5, [2, -1, 3, 5, -2])
print(f"Subarray with even sum: {result}")
```

### Variation 3: Subarray with Sum and Length Constraints
**Problem**: Check if there exists a subarray with sum x and length at least k.

```python
def check_subarray_with_sum_and_length(n, x, k, arr):
    prefix_sum = 0
    seen_sums = {}  # Map prefix sum to earliest index
    seen_sums[0] = -1
    
    for i, num in enumerate(arr):
        prefix_sum += num
        
        if prefix_sum - x in seen_sums:
            length = i - seen_sums[prefix_sum - x]
            if length >= k:
                return "YES"
        
        if prefix_sum not in seen_sums:
            seen_sums[prefix_sum] = i
    
    return "NO"

# Example usage
result = check_subarray_with_sum_and_length(5, 7, 2, [2, -1, 3, 5, -2])
print(f"Subarray with sum 7 and length >= 2: {result}")
```

### Variation 4: Subarray with Sum and Character Constraints
**Problem**: Check if there exists a subarray with sum x where no two adjacent elements are negative.

```python
def check_subarray_with_sum_and_constraints(n, x, arr):
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)
    last_negative = -1
    
    for i, num in enumerate(arr):
        prefix_sum += num
        
        # Check constraint: no two adjacent negative elements
        if num < 0:
            if last_negative == i - 1:
                # Two consecutive negative numbers, reset
                seen_sums.clear()
                seen_sums.add(0)
                prefix_sum = num
            last_negative = i
        
        if prefix_sum - x in seen_sums:
            return "YES"
        
        seen_sums.add(prefix_sum)
    
    return "NO"

# Example usage
result = check_subarray_with_sum_and_constraints(5, 7, [2, -1, 3, 5, -2])
print(f"Subarray with sum 7 and constraints: {result}")
```

### Variation 5: Subarray with Sum and Range Queries
**Problem**: Answer queries about subarray existence with sum x in specific ranges.

```python
def subarray_sum_existence_queries(n, x, arr, queries):
    """Answer subarray existence queries for specific ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= n:
            results.append("NO")
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            exists = check_subarray_with_sum_in_range(len(subarray), x, subarray)
            results.append(exists)
    
    return results

def check_subarray_with_sum_in_range(n, x, arr):
    """Check if there exists a subarray with sum x in a specific range"""
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)
    
    for num in arr:
        prefix_sum += num
        
        if prefix_sum - x in seen_sums:
            return "YES"
        
        seen_sums.add(prefix_sum)
    
    return "NO"

# Example usage
queries = [(0, 4), (1, 3), (2, 4)]
result = subarray_sum_existence_queries(5, 7, [2, -1, 3, 5, -2], queries)
print(f"Range query results: {result}")
```

## 🔗 Related Problems

- **[Longest Subarray with Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Longest subarray problems
- **[Shortest Subarray with Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Shortest subarray problems
- **[Fixed Length Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Fixed-size subarray problems

## 📚 Learning Points

1. **Prefix Sum Technique**: Essential for subarray sum problems
2. **Hash Set for Existence**: Important for efficient existence checking
3. **Subarray Sum Calculation**: Key for understanding prefix sum differences
4. **Edge Case Handling**: Important for robust solutions

---

**This is a great introduction to subarray existence problems!** 🎯
        
        if prefix_sum - target in seen_sums:
            return True
        
        seen_sums.add(prefix_sum)
    
    return False
```

### 2. **Sliding Window Pattern**
```python
def sliding_window_subarray_exists(arr, target):
    left = 0
    current_sum = 0
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > target and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == target:
            return True
    
    return False
```

### 3. **Two Pointer Technique**
```python
def two_pointer_subarray_exists(arr, target):
    left = 0
    current_sum = 0
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target and left <= right: if current_sum == 
target: return True
            current_sum -= arr[left]
            left += 1
    
    return False
```

## Edge Cases to Remember

1. **No valid subarray**: Return "NO"
2. **Empty subarray**: Consider sum 0
3. **Negative numbers**: Use prefix sum approach
4. **Zero target**: Handle carefully
5. **Large numbers**: Use appropriate data types

## Problem-Solving Framework

1. **Identify subarray nature**: This is a subarray existence problem
2. **Choose approach**: Use prefix sum with hash set for efficiency
3. **Track prefix sums**: Maintain running sum and seen sums
4. **Check existence**: Use hash set to find target sum differences
5. **Return result**: Return "YES" or "NO" based on existence

---

*This analysis shows how to efficiently check for subarray existence with target sum using prefix sum and hash set techniques.* 