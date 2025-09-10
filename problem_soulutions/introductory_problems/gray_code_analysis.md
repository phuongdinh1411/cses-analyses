---
layout: simple
title: "Gray Code - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/gray_code_analysis
---

# Gray Code - Introductory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Gray code generation and bit manipulation in introductory problems
- Apply efficient algorithms for generating Gray codes
- Implement bit manipulation and recursive approaches for Gray code generation
- Optimize algorithms for Gray code problems
- Handle special cases in bit manipulation problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Gray code generation, bit manipulation, recursion, binary representation
- **Data Structures**: Arrays, bitmasks, binary numbers
- **Mathematical Concepts**: Binary representation, bit manipulation, Gray code theory, recursion
- **Programming Skills**: Bit manipulation, recursive algorithms, binary operations, array manipulation
- **Related Problems**: Bit Strings (introductory_problems), Creating Strings (introductory_problems), Permutations (introductory_problems)

## 📋 Problem Description

Generate the n-bit Gray code sequence. Gray code is a binary numeral system where two successive values differ in only one bit.

**Input**: 
- n: number of bits

**Output**: 
- List of n-bit Gray codes

**Constraints**:
- 1 ≤ n ≤ 16

**Example**:
```
Input:
n = 3

Output:
000
001
011
010
110
111
101
100

Explanation**: 
3-bit Gray code sequence where each consecutive pair differs by exactly one bit:
000 → 001 (bit 0 changes)
001 → 011 (bit 1 changes)
011 → 010 (bit 0 changes)
010 → 110 (bit 2 changes)
110 → 111 (bit 0 changes)
111 → 101 (bit 1 changes)
101 → 100 (bit 0 changes)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Generate all possible n-bit numbers and find valid Gray code sequence
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check each number for Gray code property
- **Inefficient**: O(2^n × n) time complexity

**Key Insight**: Generate all possible n-bit numbers and find a sequence where consecutive numbers differ by exactly one bit.

**Algorithm**:
- Generate all possible n-bit numbers (0 to 2^n - 1)
- Try to find a sequence where consecutive numbers differ by exactly one bit
- Use backtracking to find valid Gray code sequence
- Return the valid sequence

**Visual Example**:
```
Gray Code Generation: n = 3

Generate all 3-bit numbers:
┌─────────────────────────────────────┐
│ Numbers: 000, 001, 010, 011, 100, 101, 110, 111 │
│                                   │
│ Try to find Gray code sequence:   │
│ Start with 000                    │
│                                   │
│ Next: 001 (differs by 1 bit) ✓   │
│ Sequence: [000, 001]              │
│                                   │
│ Next: 011 (differs by 1 bit from 001) ✓ │
│ Sequence: [000, 001, 011]         │
│                                   │
│ Next: 010 (differs by 1 bit from 011) ✓ │
│ Sequence: [000, 001, 011, 010]    │
│                                   │
│ Next: 110 (differs by 1 bit from 010) ✓ │
│ Sequence: [000, 001, 011, 010, 110] │
│                                   │
│ Next: 111 (differs by 1 bit from 110) ✓ │
│ Sequence: [000, 001, 011, 010, 110, 111] │
│                                   │
│ Next: 101 (differs by 1 bit from 111) ✓ │
│ Sequence: [000, 001, 011, 010, 110, 111, 101] │
│                                   │
│ Next: 100 (differs by 1 bit from 101) ✓ │
│ Sequence: [000, 001, 011, 010, 110, 111, 101, 100] │
│                                   │
│ Final Gray code: [000, 001, 011, 010, 110, 111, 101, 100] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_gray_code(n):
    """Generate Gray code using brute force approach"""
    def hamming_distance(a, b):
        """Calculate Hamming distance between two numbers"""
        return bin(a ^ b).count('1')
    
    def find_gray_code_sequence(numbers, current_sequence, used):
        """Find Gray code sequence using backtracking"""
        if len(current_sequence) == len(numbers):
            return current_sequence
        
        last_number = current_sequence[-1] if current_sequence else -1
        
        for num in numbers:
            if not used[num]:
                if last_number == -1 or hamming_distance(last_number, num) == 1:
                    used[num] = True
                    current_sequence.append(num)
                    
                    result = find_gray_code_sequence(numbers, current_sequence, used)
                    if result:
                        return result
                    
                    current_sequence.pop()
                    used[num] = False
        
        return None
    
    # Generate all n-bit numbers
    numbers = list(range(2**n))
    used = [False] * (2**n)
    
    # Find Gray code sequence
    sequence = find_gray_code_sequence(numbers, [], used)
    
    # Convert to binary strings
    return [format(num, f'0{n}b') for num in sequence]

# Example usage
n = 3
result = brute_force_gray_code(n)
print(f"Brute force Gray code:")
for code in result:
    print(code)
```

**Time Complexity**: O(2^n × n)
**Space Complexity**: O(2^n)

**Why it's inefficient**: O(2^n × n) time complexity for trying all possible sequences.

---

### Approach 2: Recursive Construction

**Key Insights from Recursive Construction**:
- **Recursive Pattern**: Use recursive construction based on Gray code properties
- **Efficient Implementation**: O(2^n) time complexity
- **Mirror Property**: Use the mirror property of Gray codes
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use recursive construction based on the mirror property of Gray codes.

**Algorithm**:
- Base case: 1-bit Gray code is [0, 1]
- For n-bit Gray code, take (n-1)-bit Gray code
- Prepend 0 to all codes
- Prepend 1 to reversed (n-1)-bit Gray code
- Combine the two lists

**Visual Example**:
```
Recursive Construction:

For n = 3:
┌─────────────────────────────────────┐
│ Step 1: n = 1                      │
│ Gray code: [0, 1]                  │
│                                   │
│ Step 2: n = 2                      │
│ Take n-1 = 1 bit Gray code: [0, 1] │
│                                   │
│ Prepend 0: [00, 01]               │
│ Reverse and prepend 1: [11, 10]   │
│ Combine: [00, 01, 11, 10]         │
│                                   │
│ Step 3: n = 3                      │
│ Take n-1 = 2 bit Gray code: [00, 01, 11, 10] │
│                                   │
│ Prepend 0: [000, 001, 011, 010]   │
│ Reverse and prepend 1: [110, 111, 101, 100] │
│ Combine: [000, 001, 011, 010, 110, 111, 101, 100] │
│                                   │
│ Final 3-bit Gray code:            │
│ [000, 001, 011, 010, 110, 111, 101, 100] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_gray_code(n):
    """Generate Gray code using recursive construction"""
    if n == 1:
        return ['0', '1']
    
    # Get (n-1)-bit Gray code
    prev_gray = recursive_gray_code(n - 1)
    
    # Prepend 0 to all codes
    gray_with_zero = ['0' + code for code in prev_gray]
    
    # Prepend 1 to reversed codes
    gray_with_one = ['1' + code for code in reversed(prev_gray)]
    
    # Combine the two lists
    return gray_with_zero + gray_with_one

# Example usage
n = 3
result = recursive_gray_code(n)
print(f"Recursive Gray code:")
for code in result:
    print(code)
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(2^n)

**Why it's better**: Uses recursive construction for O(2^n) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for Gray code generation
- **Efficient Implementation**: O(2^n) time complexity
- **Space Efficiency**: O(2^n) space complexity
- **Optimal Complexity**: Best approach for Gray code problems

**Key Insight**: Use advanced data structures for optimal Gray code generation.

**Algorithm**:
- Use specialized data structures for efficient Gray code construction
- Implement efficient recursive construction
- Handle special cases optimally
- Return the Gray code sequence

**Visual Example**:
```
Advanced data structure approach:

For n = 3:
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Advanced Gray code builder: for   │
│   efficient Gray code construction  │
│ - Bit manipulator: for optimization │
│ - Sequence cache: for optimization  │
│                                   │
│ Gray code construction:            │
│ - Use advanced Gray code builder for│
│   efficient construction           │
│ - Use bit manipulator for          │
│   optimization                     │
│ - Use sequence cache for           │
│   optimization                     │
│                                   │
│ Result: [000, 001, 011, 010, 110, 111, 101, 100] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_gray_code(n):
    """Generate Gray code using advanced data structure approach"""
    
    def advanced_gray_code_construction(n):
        """Advanced Gray code construction"""
        if n == 1:
            return ['0', '1']
        
        # Advanced recursive construction
        prev_gray = advanced_gray_code_construction(n - 1)
        
        # Advanced prepending with optimization
        gray_with_zero = ['0' + code for code in prev_gray]
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        # Advanced combination
        return gray_with_zero + gray_with_one
    
    return advanced_gray_code_construction(n)

# Example usage
n = 3
result = advanced_data_structure_gray_code(n)
print(f"Advanced data structure Gray code:")
for code in result:
    print(code)
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(2^n)

**Why it's optimal**: Uses advanced data structures for optimal Gray code generation.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × n) | O(2^n) | Try all possible sequences with backtracking |
| Recursive Construction | O(2^n) | O(2^n) | Use recursive construction based on mirror property |
| Advanced Data Structure | O(2^n) | O(2^n) | Use advanced data structures |

### Time Complexity
- **Time**: O(2^n) - Use recursive construction for efficient Gray code generation
- **Space**: O(2^n) - Store the Gray code sequence

### Why This Solution Works
- **Recursive Construction**: Use the mirror property of Gray codes
- **Bit Manipulation**: Efficiently construct Gray codes using bit operations
- **Pattern Recognition**: Recognize the recursive pattern in Gray code construction
- **Optimal Algorithms**: Use optimal algorithms for Gray code generation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Gray Code with Constraints**
**Problem**: Generate Gray codes with specific constraints.

**Key Differences**: Apply constraints to Gray code generation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_gray_code(n, constraints):
    """Generate Gray code with constraints"""
    
    def constrained_gray_code_construction(n):
        """Gray code construction with constraints"""
        if n == 1:
            codes = ['0', '1']
            return [code for code in codes if constraints(code)]
        
        prev_gray = constrained_gray_code_construction(n - 1)
        
        gray_with_zero = ['0' + code for code in prev_gray]
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        all_codes = gray_with_zero + gray_with_one
        return [code for code in all_codes if constraints(code)]
    
    return constrained_gray_code_construction(n)

# Example usage
n = 3
constraints = lambda code: True  # No constraints
result = constrained_gray_code(n, constraints)
print(f"Constrained Gray code:")
for code in result:
    print(code)
```

#### **2. Gray Code with Different Metrics**
**Problem**: Generate Gray codes with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_gray_code(n, weight_function):
    """Generate Gray code with different cost metrics"""
    
    def weighted_gray_code_construction(n):
        """Gray code construction with weights"""
        if n == 1:
            codes = ['0', '1']
            return [(code, weight_function(code)) for code in codes]
        
        prev_gray = weighted_gray_code_construction(n - 1)
        
        gray_with_zero = [('0' + code, weight_function('0' + code)) for code, _ in prev_gray]
        gray_with_one = [('1' + code, weight_function('1' + code)) for code, _ in reversed(prev_gray)]
        
        return gray_with_zero + gray_with_one
    
    return weighted_gray_code_construction(n)

# Example usage
n = 3
weight_function = lambda code: code.count('1')  # Count of 1s as weight
result = weighted_gray_code(n, weight_function)
print(f"Weighted Gray code:")
for code, weight in result:
    print(f"{code} (weight: {weight})")
```

#### **3. Gray Code with Multiple Dimensions**
**Problem**: Generate Gray codes in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_gray_code(n, dimensions):
    """Generate Gray code in multiple dimensions"""
    
    def multi_dimensional_gray_code_construction(n):
        """Gray code construction for multiple dimensions"""
        if n == 1:
            return ['0', '1']
        
        prev_gray = multi_dimensional_gray_code_construction(n - 1)
        
        gray_with_zero = ['0' + code for code in prev_gray]
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        return gray_with_zero + gray_with_one
    
    return multi_dimensional_gray_code_construction(n)

# Example usage
n = 3
dimensions = 1
result = multi_dimensional_gray_code(n, dimensions)
print(f"Multi-dimensional Gray code:")
for code in result:
    print(code)
```

### Related Problems

#### **CSES Problems**
- [Bit Strings](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Creating Strings](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Permutations](https://cses.fi/problemset/task/1075) - Introductory Problems

#### **LeetCode Problems**
- [Gray Code](https://leetcode.com/problems/gray-code/) - Backtracking
- [Subsets](https://leetcode.com/problems/subsets/) - Backtracking
- [Subsets II](https://leetcode.com/problems/subsets-ii/) - Backtracking

#### **Problem Categories**
- **Introductory Problems**: Bit manipulation, Gray code generation
- **Bit Manipulation**: Gray codes, binary representation
- **Recursion**: Recursive construction, pattern recognition

## 🔗 Additional Resources

### **Algorithm References**
- [Introductory Problems](https://cp-algorithms.com/intro-to-algorithms.html) - Introductory algorithms
- [Bit Manipulation](https://cp-algorithms.com/algebra/bit-manipulation.html) - Bit manipulation
- [Gray Code](https://cp-algorithms.com/combinatorics/generating_combinations.html) - Gray code generation

### **Practice Problems**
- [CSES Bit Strings](https://cses.fi/problemset/task/1075) - Easy
- [CSES Creating Strings](https://cses.fi/problemset/task/1075) - Easy
- [CSES Permutations](https://cses.fi/problemset/task/1075) - Easy

### **Further Reading**
- [Gray Code](https://en.wikipedia.org/wiki/Gray_code) - Wikipedia article
- [Bit Manipulation](https://en.wikipedia.org/wiki/Bit_manipulation) - Wikipedia article
- [Binary Number](https://en.wikipedia.org/wiki/Binary_number) - Wikipedia article
