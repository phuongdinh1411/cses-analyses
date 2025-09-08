---
layout: simple
title: "Gray Code"
permalink: /problem_soulutions/introductory_problems/gray_code_analysis
---

# Gray Code

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand Gray code sequences and bit manipulation concepts
- Apply bit manipulation and XOR operations to generate Gray code sequences
- Implement efficient Gray code generation algorithms with proper bit operations
- Optimize Gray code generation using mathematical formulas and bit manipulation
- Handle edge cases in Gray code problems (large n, bit overflow, sequence validation)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Gray code generation, bit manipulation, XOR operations, sequence generation
- **Data Structures**: Bit operations, sequence tracking, binary representation, bit manipulation
- **Mathematical Concepts**: Binary representation, bit manipulation, Gray code theory, XOR properties
- **Programming Skills**: Bit operations, XOR implementation, sequence generation, algorithm implementation
- **Related Problems**: Bit manipulation, Sequence generation, Binary problems, XOR operations

## Problem Description

**Problem**: Generate a Gray code sequence of length 2ⁿ where consecutive numbers differ by exactly one bit.

**Input**: An integer n (1 ≤ n ≤ 16)

**Output**: Print the Gray code sequence.

**Constraints**:
- 1 ≤ n ≤ 16
- Generate sequence of length 2ⁿ
- Consecutive numbers must differ by exactly one bit
- Sequence must contain all possible n-bit numbers
- Output each number on a separate line

**Example**:
```
Input: 2

Output:
0
1
3
2

Explanation: Binary representation shows consecutive numbers differ by one bit:
00 → 01 → 11 → 10
```

## Visual Example

### Input and Gray Code Properties
```
Input: n = 2

Gray Code Properties:
- Length: 2ⁿ = 2² = 4 numbers
- Consecutive numbers differ by exactly one bit
- Contains all possible 2-bit numbers
- Binary representation: 00, 01, 10, 11
```

### Gray Code Sequence Generation
```
For n = 2, Gray code sequence:

Index  Binary  Gray Code  Decimal
0      00      00         0
1      01      01         1
2      10      11         3
3      11      10         2

Sequence: 0 → 1 → 3 → 2
```

### Bit Difference Verification
```
Consecutive pairs and bit differences:

0 (00) → 1 (01): Only bit 0 changes
1 (01) → 3 (11): Only bit 1 changes  
3 (11) → 2 (10): Only bit 0 changes

Each consecutive pair differs by exactly one bit ✓
```

### Mathematical Formula Application
```
Using formula: gray = i ^ (i >> 1)

i=0: 00 ^ (00 >> 1) = 00 ^ 00 = 00 = 0
i=1: 01 ^ (01 >> 1) = 01 ^ 00 = 01 = 1
i=2: 10 ^ (10 >> 1) = 10 ^ 01 = 11 = 3
i=3: 11 ^ (11 >> 1) = 11 ^ 01 = 10 = 2
```

### Key Insight
The solution works by:
1. Using the mathematical formula i ^ (i >> 1) to convert binary to Gray code
2. Generating all 2ⁿ numbers in sequence
3. Ensuring consecutive numbers differ by exactly one bit
4. Time complexity: O(2ⁿ) for generating the sequence
5. Space complexity: O(1) for generating without storage

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Naive Recursive Construction (Inefficient)

**Key Insights from Naive Recursive Solution:**
- Use recursive construction with reflection and leading bit addition
- Simple but has overhead from recursion and copying
- Not suitable for large n due to memory usage
- Straightforward implementation but poor scalability

**Algorithm:**
1. Start with base case (n=0) returning [0]
2. For each step, get previous Gray code sequence
3. Reflect the sequence and add leading 1
4. Combine original and reflected sequences

**Visual Example:**
```
Naive recursive construction: Build by reflection
For n = 2:

n=0: [0]
n=1: [0] + [1] = [0, 1]
n=2: [0, 1] + [3, 2] = [0, 1, 3, 2]

Reflection process:
[0, 1] → reverse → [1, 0] → add leading 1 → [3, 2]
```

**Implementation:**
```python
def gray_code_recursive(n):
    if n == 0:
        return [0]
    
    # Get Gray code for n-1 bits
    prev = gray_code_recursive(n - 1)
    result = prev.copy()
    
    # Add reflected sequence with leading 1
    for i in range(len(prev) - 1, -1, -1):
        result.append(prev[i] | (1 << (n - 1)))
    
    return result

def solve_gray_code_recursive():
    n = int(input())
    sequence = gray_code_recursive(n)
    for num in sequence:
        print(num)
```

**Time Complexity:** O(2ⁿ) for generating the sequence
**Space Complexity:** O(2ⁿ) for storing the sequence and recursion stack

**Why it's inefficient:**
- O(2ⁿ) space complexity for storing sequence
- Recursion overhead for large n
- Memory-intensive for large sequences
- Poor performance with exponential growth

### Approach 2: Iterative Construction (Better)

**Key Insights from Iterative Construction Solution:**
- Use iterative approach to build Gray code sequence
- More memory-efficient than recursive approach
- Standard method for Gray code generation
- Can handle larger n than recursive approach

**Algorithm:**
1. Start with [0] for n=0
2. For each bit position, reflect current sequence
3. Add leading 1 to reflected part
4. Combine sequences iteratively

**Visual Example:**
```
Iterative construction: Build step by step
For n = 2:

Step 0: [0]
Step 1: [0] + [1] = [0, 1]
Step 2: [0, 1] + [3, 2] = [0, 1, 3, 2]

Each step doubles the sequence length
```

**Implementation:**
```python
def gray_code_iterative(n):
    result = [0]
    
    for i in range(n):
        # Reflect and add leading 1
        size = len(result)
        for j in range(size - 1, -1, -1):
            result.append(result[j] | (1 << i))
    
    return result

def solve_gray_code_iterative():
    n = int(input())
    sequence = gray_code_iterative(n)
    for num in sequence:
        print(num)
```

**Time Complexity:** O(2ⁿ) for generating the sequence
**Space Complexity:** O(2ⁿ) for storing the sequence

**Why it's better:**
- No recursion overhead
- More memory-efficient than recursive approach
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Mathematical Formula (Optimal)

**Key Insights from Mathematical Formula Solution:**
- Use the proven formula i ^ (i >> 1) to generate Gray code
- Most efficient approach for Gray code generation
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use the mathematical formula gray = i ^ (i >> 1)
2. Generate numbers from 0 to 2ⁿ - 1
3. Apply formula to each number
4. Print results directly without storage

**Visual Example:**
```
Mathematical formula: i ^ (i >> 1)
For n = 2:

i=0: 00 ^ (00 >> 1) = 00 ^ 00 = 00 = 0
i=1: 01 ^ (01 >> 1) = 01 ^ 00 = 01 = 1
i=2: 10 ^ (10 >> 1) = 10 ^ 01 = 11 = 3
i=3: 11 ^ (11 >> 1) = 11 ^ 01 = 10 = 2

Result: 0, 1, 3, 2
```

**Implementation:**
```python
def solve_gray_code():
    n = int(input())
    
    # Generate Gray code using formula
    for i in range(1 << n):
        gray = i ^ (i >> 1)
        print(gray)

# Main execution
if __name__ == "__main__":
    solve_gray_code()
```

**Time Complexity:** O(2ⁿ) for generating the sequence
**Space Complexity:** O(1) for generating without storage

**Why it's optimal:**
- O(1) space complexity is optimal for this problem
- Uses mathematical formula for efficient generation
- Most efficient approach for competitive programming
- Standard method for Gray code generation

## 🎯 Problem Variations

### Variation 1: Gray Code with Custom Starting Point
**Problem**: Generate Gray code sequence starting from a specific number.

**Link**: [CSES Problem Set - Custom Gray Code](https://cses.fi/problemset/task/custom_gray_code)

```python
def custom_gray_code(n, start):
    result = []
    for i in range(1 << n):
        gray = (start + i) ^ ((start + i) >> 1)
        result.append(gray)
    return result
```

### Variation 2: Gray Code Distance
**Problem**: Find the number of bit differences between two Gray codes.

**Link**: [CSES Problem Set - Gray Code Distance](https://cses.fi/problemset/task/gray_code_distance)

```python
def gray_code_distance(a, b):
    # Convert to Gray code
    gray_a = a ^ (a >> 1)
    gray_b = b ^ (b >> 1)
    
    # Count bit differences
    xor_result = gray_a ^ gray_b
    return bin(xor_result).count('1')
```

### Variation 3: Gray Code Subsequence
**Problem**: Find the longest subsequence that forms a valid Gray code.

**Link**: [CSES Problem Set - Gray Code Subsequence](https://cses.fi/problemset/task/gray_code_subsequence)

```python
def gray_code_subsequence(arr):
    result = [arr[0]]
    
    for i in range(1, len(arr)):
        # Check if adding this number maintains Gray code property
        if bin(arr[i] ^ result[-1]).count('1') == 1:
            result.append(arr[i])
    
    return result
```

## 🔗 Related Problems

- **[Bit Manipulation Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Bit manipulation problems
- **[Sequence Generation Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Sequence generation problems
- **[Binary Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Binary problems
- **[XOR Operations Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: XOR operations problems

## 📚 Learning Points

1. **Gray Code Theory**: Essential for understanding binary sequences
2. **Bit Manipulation**: Key technique for efficient bit operations
3. **Mathematical Formulas**: Important for understanding Gray code generation
4. **XOR Properties**: Critical for understanding bit manipulation
5. **Sequence Generation**: Foundation for many combinatorial algorithms
6. **Binary Representation**: Critical for understanding number systems

## 📝 Summary

The Gray Code problem demonstrates bit manipulation and mathematical formula concepts for efficient sequence generation. We explored three approaches:

1. **Naive Recursive Construction**: O(2ⁿ) space complexity using recursive reflection, inefficient due to memory usage
2. **Iterative Construction**: O(2ⁿ) space complexity using iterative building, better approach for Gray code generation
3. **Mathematical Formula**: O(1) space complexity using the formula i ^ (i >> 1), optimal approach for competitive programming

The key insights include understanding Gray code properties, using mathematical formulas for efficient generation, and applying bit manipulation techniques for optimal performance. This problem serves as an excellent introduction to bit manipulation and mathematical sequence generation in competitive programming.
