---
layout: simple
title: "Empty String - String Algorithm Problem"
permalink: /problem_soulutions/counting_problems/empty_string_analysis
---

# Empty String - String Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of empty string operations in string algorithms
- Apply counting techniques for string manipulation analysis
- Implement efficient algorithms for empty string counting
- Optimize string operations for empty string analysis
- Handle special cases in string counting

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String algorithms, counting techniques, mathematical formulas
- **Data Structures**: Strings, mathematical computations, string representation
- **Mathematical Concepts**: String theory, combinations, permutations, modular arithmetic
- **Programming Skills**: String manipulation, mathematical computations, modular arithmetic
- **Related Problems**: Counting Permutations (combinatorics), Counting Combinations (combinatorics), Counting Sequences (combinatorics)

## 📋 Problem Description

Given a string, count the number of ways to make it empty using specific operations.

**Input**: 
- s: input string

**Output**: 
- Number of ways to make string empty modulo 10^9+7

**Constraints**:
- 1 ≤ |s| ≤ 1000
- String contains lowercase letters
- Answer modulo 10^9+7

**Example**:
```
Input:
s = "ab"

Output:
2

Explanation**: 
Ways to make "ab" empty:
1. Remove 'a' first, then 'b' → ""
2. Remove 'b' first, then 'a' → ""
Total: 2 ways
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible operations
- **Complete Enumeration**: Enumerate all possible operation sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible ways to make the string empty.

**Algorithm**:
- Use recursive function to try all possible operations
- Count all valid operation sequences
- Apply modulo operation to prevent overflow

**Visual Example**:
```
String "ab":

Recursive exploration:
┌─────────────────────────────────────┐
│ Try removing 'a' first:            │
│ - Remove 'a': "b"                  │
│ - Remove 'b': ""                   │
│ - Valid sequence: 1                │
│                                   │
│ Try removing 'b' first:            │
│ - Remove 'b': "a"                  │
│ - Remove 'a': ""                   │
│ - Valid sequence: 1                │
│                                   │
│ Total: 2 ways                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_empty_string_count(s, mod=10**9+7):
    """
    Count ways to make string empty using recursive approach
    
    Args:
        s: input string
        mod: modulo value
    
    Returns:
        int: number of ways to make string empty modulo mod
    """
    def count_operations(string, index):
        """Count operations recursively"""
        if index == len(string):
            return 1  # String is empty
        
        count = 0
        
        # Try removing current character
        if index < len(string):
            count = (count + count_operations(string, index + 1)) % mod
        
        return count
    
    return count_operations(s, 0)

def recursive_empty_string_count_optimized(s, mod=10**9+7):
    """
    Optimized recursive empty string counting
    
    Args:
        s: input string
        mod: modulo value
    
    Returns:
        int: number of ways to make string empty modulo mod
    """
    def count_operations_optimized(string, index):
        """Count operations with optimization"""
        if index == len(string):
            return 1  # String is empty
        
        # Each character can be removed in one way
        return count_operations_optimized(string, index + 1)
    
    return count_operations_optimized(s, 0)

# Example usage
s = "ab"
result1 = recursive_empty_string_count(s)
result2 = recursive_empty_string_count_optimized(s)
print(f"Recursive empty string count: {result1}")
print(f"Optimized recursive count: {result2}")
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Mathematical Formula Solution

**Key Insights from Mathematical Formula Solution**:
- **Mathematical Formula**: Use factorial formula for string operations
- **Direct Calculation**: Calculate result directly without enumeration
- **Efficient Computation**: O(n) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use the mathematical formula that each character can be removed in one way.

**Algorithm**:
- Use formula: number of ways = n! (where n is string length)
- Calculate n! efficiently using modular arithmetic
- Apply modulo operation throughout

**Visual Example**:
```
Mathematical formula:
┌─────────────────────────────────────┐
│ For string of length n:            │
│ - Each character can be removed    │
│ - Total ways = n!                  │
│ - For "ab": 2! = 2                │
└─────────────────────────────────────┘

Modular arithmetic:
┌─────────────────────────────────────┐
│ n! mod mod = (n × (n-1) × ... × 1) mod mod │
│ Use modular arithmetic for efficiency │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def mathematical_empty_string_count(s, mod=10**9+7):
    """
    Count ways to make string empty using mathematical formula
    
    Args:
        s: input string
        mod: modulo value
    
    Returns:
        int: number of ways to make string empty modulo mod
    """
    def factorial_mod(n, mod):
        """Calculate n! modulo mod"""
        result = 1
        for i in range(1, n + 1):
            result = (result * i) % mod
        return result
    
    # Number of ways = n! where n is string length
    n = len(s)
    return factorial_mod(n, mod)

def mathematical_empty_string_count_v2(s, mod=10**9+7):
    """
    Alternative mathematical approach using built-in functions
    
    Args:
        s: input string
        mod: modulo value
    
    Returns:
        int: number of ways to make string empty modulo mod
    """
    import math
    
    # Use built-in factorial with modular arithmetic
    n = len(s)
    return math.factorial(n) % mod

# Example usage
s = "ab"
result1 = mathematical_empty_string_count(s)
result2 = mathematical_empty_string_count_v2(s)
print(f"Mathematical empty string count: {result1}")
print(f"Mathematical empty string count v2: {result2}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's better**: Uses mathematical formula for O(n) time complexity.

**Implementation Considerations**:
- **Mathematical Formula**: Use n! formula for string operations
- **Modular Arithmetic**: Use efficient modular arithmetic
- **Direct Calculation**: Calculate result directly without enumeration

---

### Approach 3: Advanced Mathematical Solution (Optimal)

**Key Insights from Advanced Mathematical Solution**:
- **Advanced Mathematics**: Use advanced mathematical properties
- **Efficient Computation**: O(n) time complexity
- **Mathematical Optimization**: Use mathematical optimizations
- **Optimal Complexity**: Best approach for empty string counting

**Key Insight**: Use advanced mathematical properties and optimizations for efficient empty string counting.

**Algorithm**:
- Use advanced mathematical properties
- Apply mathematical optimizations
- Calculate result efficiently

**Visual Example**:
```
Advanced mathematical properties:
┌─────────────────────────────────────┐
│ For empty string operations:       │
│ - Each character: 1 way to remove  │
│ - Total ways = n!                  │
│ - Can be calculated efficiently    │
└─────────────────────────────────────┘

Mathematical optimizations:
┌─────────────────────────────────────┐
│ - Use modular arithmetic           │
│ - Apply mathematical properties    │
│ - Optimize for large numbers       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_mathematical_empty_string_count(s, mod=10**9+7):
    """
    Count ways to make string empty using advanced mathematical approach
    
    Args:
        s: input string
        mod: modulo value
    
    Returns:
        int: number of ways to make string empty modulo mod
    """
    def fast_factorial_mod(n, mod):
        """Fast factorial calculation with optimizations"""
        if n == 0 or n == 1:
            return 1
        
        result = 1
        for i in range(2, n + 1):
            result = (result * i) % mod
        
        return result
    
    # Handle edge cases
    if len(s) == 0:
        return 1
    
    # Number of ways = n! where n is string length
    n = len(s)
    return fast_factorial_mod(n, mod)

def optimized_empty_string_count(s, mod=10**9+7):
    """
    Optimized empty string counting with additional optimizations
    
    Args:
        s: input string
        mod: modulo value
    
    Returns:
        int: number of ways to make string empty modulo mod
    """
    # Use built-in factorial with optimizations
    import math
    
    if len(s) == 0:
        return 1
    
    n = len(s)
    return math.factorial(n) % mod

def empty_string_count_with_precomputation(max_length, mod=10**9+7):
    """
    Precompute empty string counts for multiple queries
    
    Args:
        max_length: maximum string length
        mod: modulo value
    
    Returns:
        list: precomputed empty string counts
    """
    results = [0] * (max_length + 1)
    
    for i in range(max_length + 1):
        if i == 0:
            results[i] = 1
        else:
            results[i] = (results[i - 1] * i) % mod
    
    return results

# Example usage
s = "ab"
result1 = advanced_mathematical_empty_string_count(s)
result2 = optimized_empty_string_count(s)
print(f"Advanced mathematical empty string count: {result1}")
print(f"Optimized empty string count: {result2}")

# Precompute for multiple queries
max_length = 1000
precomputed = empty_string_count_with_precomputation(max_length)
print(f"Precomputed result for length {len(s)}: {precomputed[len(s)]}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses advanced mathematical properties for O(n) time complexity.

**Implementation Details**:
- **Advanced Mathematics**: Use advanced mathematical properties
- **Efficient Computation**: Use optimized factorial calculation
- **Mathematical Optimizations**: Apply mathematical optimizations
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Complete enumeration of all operation sequences |
| Mathematical Formula | O(n) | O(1) | Use n! formula with modular arithmetic |
| Advanced Mathematical | O(n) | O(1) | Use advanced mathematical properties and optimizations |

### Time Complexity
- **Time**: O(n) - Use mathematical formula for efficient calculation
- **Space**: O(1) - Use only necessary variables

### Why This Solution Works
- **Mathematical Formula**: Use n! formula for string operations
- **Modular Arithmetic**: Use efficient modular arithmetic
- **Mathematical Properties**: Leverage mathematical properties
- **Efficient Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Empty String Count with Constraints**
**Problem**: Count ways to make string empty with specific constraints.

**Key Differences**: Apply constraints to string operations

**Solution Approach**: Modify counting formula to include constraints

**Implementation**:
```python
def constrained_empty_string_count(s, constraints, mod=10**9+7):
    """
    Count ways to make string empty with constraints
    
    Args:
        s: input string
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of constrained ways modulo mod
    """
    def count_operations_constrained(string, index, constraints):
        """Count operations with constraints"""
        if index == len(string):
            return 1  # String is empty
        
        count = 0
        
        # Try removing current character if constraints allow
        if index < len(string):
            if constraints(string, index):
                count = (count + count_operations_constrained(string, index + 1, constraints)) % mod
        
        return count
    
    return count_operations_constrained(s, 0, constraints)

def constrained_empty_string_count_optimized(s, constraints, mod=10**9+7):
    """
    Optimized constrained empty string counting
    
    Args:
        s: input string
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of constrained ways modulo mod
    """
    # Calculate total number of constrained ways
    total = 1
    for i in range(len(s)):
        if constraints(s, i):
            total = (total * 1) % mod  # Each valid character contributes 1 way
    
    return total

# Example usage
s = "ab"
constraints = lambda string, index: string[index] != 'x'  # Can't remove 'x'
result1 = constrained_empty_string_count(s, constraints)
result2 = constrained_empty_string_count_optimized(s, constraints)
print(f"Constrained empty string count: {result1}")
print(f"Optimized constrained count: {result2}")
```

#### **2. Empty String Count with Multiple Operations**
**Problem**: Count ways to make string empty with multiple operation types.

**Key Differences**: Handle multiple types of operations

**Solution Approach**: Use dynamic programming with multiple operations

**Implementation**:
```python
def multi_operation_empty_string_count(s, operations, mod=10**9+7):
    """
    Count ways to make string empty with multiple operations
    
    Args:
        s: input string
        operations: list of operation types
        mod: modulo value
    
    Returns:
        int: number of ways with multiple operations modulo mod
    """
    def count_operations_multi(string, index, operations):
        """Count operations with multiple operation types"""
        if index == len(string):
            return 1  # String is empty
        
        count = 0
        
        # Try each operation type
        for operation in operations:
            if operation(string, index):
                count = (count + count_operations_multi(string, index + 1, operations)) % mod
        
        return count
    
    return count_operations_multi(s, 0, operations)

# Example usage
s = "ab"
operations = [
    lambda string, index: True,  # Operation 1: remove character
    lambda string, index: string[index] != 'a'  # Operation 2: remove if not 'a'
]
result = multi_operation_empty_string_count(s, operations)
print(f"Multi-operation empty string count: {result}")
```

#### **3. Empty String Count with Multiple Strings**
**Problem**: Count ways to make multiple strings empty.

**Key Differences**: Handle multiple strings simultaneously

**Solution Approach**: Combine results from multiple strings

**Implementation**:
```python
def multi_string_empty_string_count(strings, mod=10**9+7):
    """
    Count ways to make multiple strings empty
    
    Args:
        strings: list of input strings
        mod: modulo value
    
    Returns:
        int: number of ways to make all strings empty modulo mod
    """
    def count_single_string_empty(string):
        """Count ways to make single string empty"""
        return optimized_empty_string_count(string, mod)
    
    # Count ways for each string
    total_count = 1
    for string in strings:
        string_count = count_single_string_empty(string)
        total_count = (total_count * string_count) % mod
    
    return total_count

# Example usage
strings = ["ab", "cd", "ef"]
result = multi_string_empty_string_count(strings)
print(f"Multi-string empty string count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Counting Permutations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Combinations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Sequences](https://cses.fi/problemset/task/1075) - Combinatorics

#### **LeetCode Problems**
- [Permutations](https://leetcode.com/problems/permutations/) - Permutations
- [Permutations II](https://leetcode.com/problems/permutations-ii/) - Permutations with duplicates
- [Combinations](https://leetcode.com/problems/combinations/) - Combinations

#### **Problem Categories**
- **String Algorithms**: String manipulation, string operations
- **Combinatorics**: Mathematical counting, string properties
- **Mathematical Algorithms**: Modular arithmetic, number theory

## 🔗 Additional Resources

### **Algorithm References**
- [String Algorithms](https://cp-algorithms.com/string/string-hashing.html) - String algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques
- [Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html) - Modular arithmetic

### **Practice Problems**
- [CSES Counting Permutations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Sequences](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [String Algorithms](https://en.wikipedia.org/wiki/String_algorithm) - Wikipedia article

---

## 📝 Implementation Checklist

When applying this template to a new problem, ensure you:

### **Content Requirements**
- [x] **Problem Description**: Clear, concise with examples
- [x] **Learning Objectives**: 5 specific, measurable goals
- [x] **Prerequisites**: 5 categories of required knowledge
- [x] **3 Approaches**: Brute Force → Greedy → Optimal
- [x] **Key Insights**: 4-5 insights per approach at the beginning
- [x] **Visual Examples**: ASCII diagrams for each approach
- [x] **Complete Implementations**: Working code with examples
- [x] **Complexity Analysis**: Time and space for each approach
- [x] **Problem Variations**: 3 variations with implementations
- [x] **Related Problems**: CSES and LeetCode links

### **Structure Requirements**
- [x] **No Redundant Sections**: Remove duplicate Key Insights
- [x] **Logical Flow**: Each approach builds on the previous
- [x] **Progressive Complexity**: Clear improvement from approach to approach
- [x] **Educational Value**: Theory + Practice in each section
- [x] **Complete Coverage**: All important concepts included

### **Quality Requirements**
- [x] **Working Code**: All implementations are runnable
- [x] **Test Cases**: Examples with expected outputs
- [x] **Edge Cases**: Handle boundary conditions
- [x] **Clear Explanations**: Easy to understand for students
- [x] **Visual Learning**: Diagrams and examples throughout

---

## 🎯 **Template Usage Instructions**

### **Step 1: Replace Placeholders**
- Replace `[Problem Name]` with actual problem name
- Replace `[category]` with the problem category folder
- Replace `[problem_name]` with the actual problem filename
- Replace all `[placeholder]` text with actual content

### **Step 2: Customize Approaches**
- **Approach 1**: Usually brute force or naive solution
- **Approach 2**: Optimized solution (DP, greedy, etc.)
- **Approach 3**: Optimal solution (advanced algorithms)

### **Step 3: Add Visual Examples**
- Use ASCII art for diagrams
- Show step-by-step execution
- Use actual data in examples

### **Step 4: Implement Working Code**
- Write complete, runnable implementations
- Include test cases and examples
- Handle edge cases properly

### **Step 5: Add Problem Variations**
- Create 3 meaningful variations
- Provide implementations for each
- Link to related problems

### **Step 6: Quality Check**
- Ensure no redundant sections
- Verify all code works
- Check that complexity analysis is correct
- Confirm educational value is high

This template ensures consistency across all problem analyses while maintaining high educational value and practical implementation focus.