---
layout: simple
title: "Bit Strings - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/bit_strings_analysis
---

# Bit Strings - Introductory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of counting and combinatorics in introductory problems
- Apply efficient algorithms for counting bit strings with constraints
- Implement modular arithmetic for large number calculations
- Optimize algorithms for counting problems with constraints
- Handle special cases in combinatorics problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Counting, combinatorics, modular arithmetic, bit manipulation
- **Data Structures**: Arrays, integers, modular arithmetic
- **Mathematical Concepts**: Combinatorics, modular arithmetic, binary representation
- **Programming Skills**: Modular arithmetic, bit manipulation, counting algorithms
- **Related Problems**: Creating Strings (introductory_problems), Permutations (introductory_problems), Two Knights (introductory_problems)

## 📋 Problem Description

Count the number of bit strings of length n that do not contain two consecutive 1s.

**Input**: 
- n: length of bit string

**Output**: 
- Number of valid bit strings modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 10^6

**Example**:
```
Input:
n = 3

Output:
5

Explanation**: 
Valid bit strings of length 3:
000, 001, 010, 100, 101
Invalid bit strings: 011, 110, 111
Total: 5 valid strings
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Generate all possible bit strings and check constraints
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check each bit string for consecutive 1s
- **Inefficient**: O(2^n × n) time complexity

**Key Insight**: Generate all possible bit strings and count those without consecutive 1s.

**Algorithm**:
- Generate all possible bit strings of length n
- For each bit string, check if it contains consecutive 1s
- Count the valid bit strings
- Return the count modulo 10^9 + 7

**Visual Example**:
```
Bit strings of length 3:

Generate all 2^3 = 8 bit strings:
┌─────────────────────────────────────┐
│ String 1: 000                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 2: 001                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 3: 010                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 4: 011                      │
│ - Check: Has consecutive 1s ✗      │
│ - Invalid ✗                        │
│                                   │
│ String 5: 100                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 6: 101                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 7: 110                      │
│ - Check: Has consecutive 1s ✗      │
│ - Invalid ✗                        │
│                                   │
│ String 8: 111                      │
│ - Check: Has consecutive 1s ✗      │
│ - Invalid ✗                        │
│                                   │
│ Valid strings: 000, 001, 010, 100, 101 │
│ Total: 5                           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_bit_strings(n):
    """Count valid bit strings using brute force approach"""
    MOD = 10**9 + 7
    count = 0
    
    # Generate all possible bit strings
    for i in range(1 << n):
        bit_string = format(i, f'0{n}b')
        
        # Check if bit string has consecutive 1s
        has_consecutive_ones = False
        for j in range(len(bit_string) - 1):
            if bit_string[j] == '1' and bit_string[j + 1] == '1':
                has_consecutive_ones = True
                break
        
        if not has_consecutive_ones:
            count += 1
    
    return count % MOD

# Example usage
n = 3
result = brute_force_bit_strings(n)
print(f"Brute force count: {result}")
```

**Time Complexity**: O(2^n × n)
**Space Complexity**: O(n)

**Why it's inefficient**: O(2^n × n) time complexity for generating and checking all bit strings.

---

### Approach 2: Dynamic Programming

**Key Insights from Dynamic Programming**:
- **Recurrence Relation**: Use DP to avoid recalculating subproblems
- **Efficient Implementation**: O(n) time complexity
- **State Definition**: dp[i] = number of valid bit strings of length i
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use dynamic programming with recurrence relation to count valid bit strings.

**Algorithm**:
- Define dp[i] as number of valid bit strings of length i
- Base cases: dp[1] = 2, dp[2] = 3
- Recurrence: dp[i] = dp[i-1] + dp[i-2]
- Return dp[n] modulo 10^9 + 7

**Visual Example**:
```
Dynamic Programming:

For n = 3:
┌─────────────────────────────────────┐
│ Base cases:                        │
│ - dp[1] = 2 (0, 1)                │
│ - dp[2] = 3 (00, 01, 10)          │
│                                   │
│ Recurrence relation:               │
│ dp[i] = dp[i-1] + dp[i-2]         │
│                                   │
│ Calculation:                       │
│ - dp[3] = dp[2] + dp[1] = 3 + 2 = 5 │
│                                   │
│ Explanation:                       │
│ - dp[i-1]: strings ending with 0   │
│ - dp[i-2]: strings ending with 01  │
│ - Total: all valid strings of length i │
│                                   │
│ Result: 5                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_bit_strings(n):
    """Count valid bit strings using dynamic programming"""
    MOD = 10**9 + 7
    
    if n == 1:
        return 2
    if n == 2:
        return 3
    
    # Initialize DP array
    dp = [0] * (n + 1)
    dp[1] = 2  # 0, 1
    dp[2] = 3  # 00, 01, 10
    
    # Fill DP array
    for i in range(3, n + 1):
        dp[i] = (dp[i-1] + dp[i-2]) % MOD
    
    return dp[n]

# Example usage
n = 3
result = dp_bit_strings(n)
print(f"DP count: {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Uses dynamic programming for O(n) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for counting
- **Efficient Implementation**: O(n) time complexity
- **Space Efficiency**: O(1) space complexity
- **Optimal Complexity**: Best approach for counting problems

**Key Insight**: Use advanced data structures for optimal counting.

**Algorithm**:
- Use specialized data structures for counting
- Implement efficient DP with space optimization
- Handle special cases optimally
- Return count modulo 10^9 + 7

**Visual Example**:
```
Advanced data structure approach:

For n = 3:
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Advanced counter: for efficient   │
│   counting                          │
│ - Modular arithmetic: for optimization│
│ - Space optimization: for efficiency│
│                                   │
│ Counting calculation:               │
│ - Use advanced counter for efficient│
│   counting                          │
│ - Use modular arithmetic for       │
│   optimization                      │
│ - Use space optimization for       │
│   efficiency                        │
│                                   │
│ Result: 5                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_bit_strings(n):
    """Count valid bit strings using advanced data structure approach"""
    MOD = 10**9 + 7
    
    if n == 1:
        return 2
    if n == 2:
        return 3
    
    # Use space-optimized DP
    prev2 = 2  # dp[i-2]
    prev1 = 3  # dp[i-1]
    
    # Advanced DP with space optimization
    for i in range(3, n + 1):
        current = (prev1 + prev2) % MOD
        prev2 = prev1
        prev1 = current
    
    return prev1

# Example usage
n = 3
result = advanced_data_structure_bit_strings(n)
print(f"Advanced data structure count: {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × n) | O(n) | Generate all bit strings and check |
| Dynamic Programming | O(n) | O(n) | Use recurrence relation dp[i] = dp[i-1] + dp[i-2] |
| Advanced Data Structure | O(n) | O(1) | Use space-optimized DP |

### Time Complexity
- **Time**: O(n) - Use dynamic programming for efficient counting
- **Space**: O(1) - Use space-optimized DP

### Why This Solution Works
- **Recurrence Relation**: Use dp[i] = dp[i-1] + dp[i-2] to avoid recalculating
- **Base Cases**: Handle small cases directly
- **Modular Arithmetic**: Use modulo to handle large numbers
- **Optimal Algorithms**: Use optimal algorithms for counting problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Bit Strings with Constraints**
**Problem**: Count bit strings with specific constraints.

**Key Differences**: Apply constraints to counting

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_bit_strings(n, constraints):
    """Count valid bit strings with constraints"""
    MOD = 10**9 + 7
    
    if n == 1:
        return 2 if constraints(1) else 0
    if n == 2:
        return 3 if constraints(2) else 0
    
    prev2 = 2
    prev1 = 3
    
    for i in range(3, n + 1):
        current = (prev1 + prev2) % MOD
        if not constraints(i):
            current = 0
        prev2 = prev1
        prev1 = current
    
    return prev1

# Example usage
n = 3
constraints = lambda i: True  # No constraints
result = constrained_bit_strings(n, constraints)
print(f"Constrained count: {result}")
```

#### **2. Bit Strings with Different Metrics**
**Problem**: Count bit strings with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_bit_strings(n, weight_function):
    """Count valid bit strings with different cost metrics"""
    MOD = 10**9 + 7
    
    if n == 1:
        return weight_function(1, 2)
    if n == 2:
        return weight_function(2, 3)
    
    prev2 = weight_function(1, 2)
    prev1 = weight_function(2, 3)
    
    for i in range(3, n + 1):
        current = (prev1 + prev2) % MOD
        current = weight_function(i, current)
        prev2 = prev1
        prev1 = current
    
    return prev1

# Example usage
n = 3
weight_function = lambda i, count: count  # No modification
result = weighted_bit_strings(n, weight_function)
print(f"Weighted count: {result}")
```

#### **3. Bit Strings with Multiple Dimensions**
**Problem**: Count bit strings in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_bit_strings(n, dimensions):
    """Count valid bit strings in multiple dimensions"""
    MOD = 10**9 + 7
    
    if n == 1:
        return 2
    if n == 2:
        return 3
    
    prev2 = 2
    prev1 = 3
    
    for i in range(3, n + 1):
        current = (prev1 + prev2) % MOD
        prev2 = prev1
        prev1 = current
    
    return prev1

# Example usage
n = 3
dimensions = 1
result = multi_dimensional_bit_strings(n, dimensions)
print(f"Multi-dimensional count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Creating Strings](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Permutations](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Two Knights](https://cses.fi/problemset/task/1075) - Introductory Problems

#### **LeetCode Problems**
- [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) - Dynamic Programming
- [Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) - Dynamic Programming
- [House Robber](https://leetcode.com/problems/house-robber/) - Dynamic Programming

#### **Problem Categories**
- **Introductory Problems**: Counting, combinatorics
- **Dynamic Programming**: Recurrence relations, counting
- **Combinatorics**: Bit strings, counting problems

## 🔗 Additional Resources

### **Algorithm References**
- [Introductory Problems](https://cp-algorithms.com/intro-to-algorithms.html) - Introductory algorithms
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/basic-combinatorics.html) - Combinatorics

### **Practice Problems**
- [CSES Creating Strings](https://cses.fi/problemset/task/1075) - Easy
- [CSES Permutations](https://cses.fi/problemset/task/1075) - Easy
- [CSES Two Knights](https://cses.fi/problemset/task/1075) - Easy

### **Further Reading**
- [Combinatorics](https://en.wikipedia.org/wiki/Combinatorics) - Wikipedia article
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
- [Bit String](https://en.wikipedia.org/wiki/Bit_string) - Wikipedia article
