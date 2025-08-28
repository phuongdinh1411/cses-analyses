---
layout: simple
title: Common Mistakes
permalink: /quick_reference/common_mistakes/
---

# Common Mistakes and Pitfalls

## 🚨 Time Complexity Mistakes

### ❌ Nested Loops = O(n²)
**Mistake**: Thinking nested loops are O(n)
**Correct**: Nested loops are O(n²) or worse
**Example**:
```python
# Wrong: O(n)
for i in range(n):
    for j in range(n):
        # operations
```
**Fix**: Look for ways to reduce nested loops

### ❌ String Operations = O(1)
**Mistake**: Thinking string concatenation is O(1)
**Correct**: String operations are often O(n)
**Example**:
```python
# Wrong: O(1)
result = result + "string"  # O(n) each time

# Correct: O(n)
result = "".join(strings)   # O(n) total
```

### ❌ List Operations = O(1)
**Mistake**: Thinking list operations are O(1)
**Correct**: Many list operations are O(n)
**Example**:
```python
# Wrong: O(1)
list.insert(0, item)  # O(n)
list.pop(0)           # O(n)

# Correct: O(1)
list.append(item)     # O(1) amortized
list.pop()            # O(1)
```

## 💾 Memory Issues

### ❌ Large Arrays Without Optimization
**Mistake**: Creating large arrays when not needed
**Correct**: Use sparse representations
**Example**:
```python
# Wrong: O(n²) space
dp = [[0] * n for _ in range(n)]

# Correct: O(n) space
dp = [0] * n  # if only current row needed
```

### ❌ Deep Recursion
**Mistake**: Deep recursion causing stack overflow
**Correct**: Use iterative approach or tail recursion
**Example**:
```python
# Wrong: Stack overflow for large n
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n-1)

# Correct: Iterative
def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result
```

### ❌ String Concatenation in Loops
**Mistake**: Building strings with + in loops
**Correct**: Use list and join
**Example**:
```python
# Wrong: O(n²)
result = ""
for i in range(n):
    result += str(i)

# Correct: O(n)
result = "".join(str(i) for i in range(n))
```

## ⚠️ Edge Cases

### ❌ Empty Input
**Mistake**: Not checking for empty input
**Correct**: Always check edge cases
**Example**:
```python
# Wrong: Crashes on empty array
def max_element(arr):
    return max(arr)

# Correct: Handle empty case
def max_element(arr):
    if not arr:
        return None
    return max(arr)
```

### ❌ Single Element
**Mistake**: Not handling single element case
**Correct**: Check for single element
**Example**:
```python
# Wrong: May fail for single element
def find_second_max(arr):
    return sorted(arr)[-2]

# Correct: Handle single element
def find_second_max(arr):
    if len(arr) < 2:
        return None
    return sorted(arr)[-2]
```

### ❌ Negative Numbers
**Mistake**: Not considering negative numbers
**Correct**: Check bounds and signs
**Example**:
```python
# Wrong: May fail with negatives
def sqrt_floor(n):
    return int(n ** 0.5)

# Correct: Handle negatives
def sqrt_floor(n):
    if n < 0:
        return None
    return int(n ** 0.5)
```

### ❌ Integer Overflow
**Mistake**: Not handling large numbers
**Correct**: Use appropriate data types
**Example**:
```python
# Wrong: Overflow for large numbers
def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

# Correct: Use modular arithmetic
def factorial_mod(n, mod):
    result = 1
    for i in range(1, n+1):
        result = (result * i) % mod
    return result
```

## 🔍 Algorithm Selection Mistakes

### ❌ Wrong Algorithm for Constraints
**Mistake**: Using O(n²) for n ≤ 10⁶
**Correct**: Choose algorithm based on constraints
**Example**:
```python
# Wrong: O(n²) for large n
def find_pair_sum(arr, target):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] + arr[j] == target:
                return (i, j)
    return None

# Correct: O(n) with hash set
def find_pair_sum(arr, target):
    seen = set()
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return (arr.index(complement), i)
        seen.add(num)
    return None
```

### ❌ Over-engineering Simple Problems
**Mistake**: Using complex algorithms for simple problems
**Correct**: Start simple, optimize if needed
**Example**:
```python
# Wrong: Complex DP for simple problem
def sum_array(arr):
    dp = [0] * len(arr)
    dp[0] = arr[0]
    for i in range(1, len(arr)):
        dp[i] = dp[i-1] + arr[i]
    return dp[-1]

# Correct: Simple solution
def sum_array(arr):
    return sum(arr)
```

## 🔢 Mathematical Mistakes

### ❌ Division by Zero
**Mistake**: Not checking for division by zero
**Correct**: Always check denominator
**Example**:
```python
# Wrong: Division by zero
def average(arr):
    return sum(arr) / len(arr)

# Correct: Check for empty array
def average(arr):
    if not arr:
        return 0
    return sum(arr) / len(arr)
```

### ❌ Floating Point Precision
**Mistake**: Using floating point for exact comparisons
**Correct**: Use integer arithmetic when possible
**Example**:
```python
# Wrong: Floating point comparison
def is_equal(a, b):
    return abs(a - b) < 1e-9

# Correct: Integer comparison
def is_equal(a, b):
    return a == b
```

### ❌ Modulo with Negative Numbers
**Mistake**: Incorrect modulo with negative numbers
**Correct**: Handle negative numbers properly
**Example**:
```python
# Wrong: Incorrect for negative numbers
def mod(a, m):
    return a % m

# Correct: Handle negatives
def mod(a, m):
    return ((a % m) + m) % m
```

## 🎯 Prevention Strategies

### 📋 Before Coding
1. **Read constraints carefully**
2. **Identify edge cases**
3. **Choose appropriate algorithm**
4. **Plan implementation steps**

### 📋 During Coding
1. **Check bounds and edge cases**
2. **Use appropriate data types**
3. **Test with small examples**
4. **Verify time complexity**

### 📋 After Coding
1. **Test with edge cases**
2. **Check for overflow**
3. **Verify correctness**
4. **Optimize if needed**

## 🚀 Best Practices

### ✅ Always Do
- Check input constraints
- Handle edge cases
- Use appropriate data types
- Test with examples
- Verify time complexity

### ❌ Never Do
- Assume input is valid
- Ignore edge cases
- Use wrong data types
- Skip testing
- Ignore time complexity

## 📊 Common Complexity Mistakes

### ⏰ Time Complexity
- **Nested loops**: O(n²) not O(n)
- **String operations**: O(n) not O(1)
- **List operations**: O(n) not O(1)
- **Sorting**: O(n log n) not O(n)

### 💾 Space Complexity
- **Recursion**: O(depth) not O(1)
- **Large arrays**: O(n²) not O(n)
- **String building**: O(n²) not O(n)
- **Hash maps**: O(n) not O(1)
