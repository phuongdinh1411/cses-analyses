---
layout: simple
title: "Counting Sequences - Combinatorial Problem"
permalink: /problem_soulutions/counting_problems/counting_sequences_analysis
---

# Counting Sequences - Combinatorial Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of sequence counting in combinatorics
- Apply counting techniques for sequence analysis
- Implement efficient algorithms for sequence counting
- Optimize sequence calculations for large numbers
- Handle special cases in sequence counting

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Combinatorics, counting techniques, mathematical formulas
- **Data Structures**: Arrays, mathematical computations, factorial calculations
- **Mathematical Concepts**: Sequences, combinations, permutations, modular arithmetic
- **Programming Skills**: Mathematical computations, modular arithmetic, large number handling
- **Related Problems**: Counting Permutations (combinatorics), Counting Combinations (combinatorics), Counting Reorders (combinatorics)

## 📋 Problem Description

Given n and k, count the number of sequences of length k using elements from 1 to n.

**Input**: 
- n: maximum element value
- k: sequence length

**Output**: 
- Number of sequences modulo 10^9+7

**Constraints**:
- 1 ≤ n, k ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3, k = 2

Output:
9

Explanation**: 
Sequences of length 2 using elements 1, 2, 3:
[1,1], [1,2], [1,3]
[2,1], [2,2], [2,3]
[3,1], [3,2], [3,3]
Total: 9 sequences
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Sequence Solution

**Key Insights from Recursive Sequence Solution**:
- **Recursive Approach**: Use recursion to generate all sequences
- **Complete Enumeration**: Enumerate all possible sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to generate all possible sequences of length k using elements from 1 to n.

**Algorithm**:
- Use recursive function to build sequences element by element
- Count all valid sequences
- Apply modulo operation to prevent overflow

**Visual Example**:
```
n = 3, k = 2

Recursive generation:
┌─────────────────────────────────────┐
│ Position 1: can be 1, 2, or 3      │
│ Position 2: can be 1, 2, or 3      │
│ Total combinations: 3 × 3 = 9      │
└─────────────────────────────────────┘

Sequence enumeration:
┌─────────────────────────────────────┐
│ [1,1], [1,2], [1,3]               │
│ [2,1], [2,2], [2,3]               │
│ [3,1], [3,2], [3,3]               │
│ Total: 9 sequences                 │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_sequence_count(n, k, mod=10**9+7):
    """
    Count sequences using recursive approach
    
    Args:
        n: maximum element value
        k: sequence length
        mod: modulo value
    
    Returns:
        int: number of sequences modulo mod
    """
    def count_sequences(position, current_sequence):
        """Count sequences recursively"""
        if position == k:
            return 1  # Valid sequence found
        
        count = 0
        for element in range(1, n + 1):
            current_sequence.append(element)
            count = (count + count_sequences(position + 1, current_sequence)) % mod
            current_sequence.pop()  # Backtrack
        
        return count
    
    return count_sequences(0, [])

def recursive_sequence_count_optimized(n, k, mod=10**9+7):
    """
    Optimized recursive sequence counting
    
    Args:
        n: maximum element value
        k: sequence length
        mod: modulo value
    
    Returns:
        int: number of sequences modulo mod
    """
    def count_sequences_optimized(position):
        """Count sequences with optimization"""
        if position == k:
            return 1  # Valid sequence found
        
        count = 0
        for element in range(1, n + 1):
            count = (count + count_sequences_optimized(position + 1)) % mod
        
        return count
    
    return count_sequences_optimized(0)

# Example usage
n, k = 3, 2
result1 = recursive_sequence_count(n, k)
result2 = recursive_sequence_count_optimized(n, k)
print(f"Recursive sequence count: {result1}")
print(f"Optimized recursive count: {result2}")
```

**Time Complexity**: O(n^k)
**Space Complexity**: O(k)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Mathematical Formula Solution

**Key Insights from Mathematical Formula Solution**:
- **Mathematical Formula**: Use n^k formula for sequences
- **Direct Calculation**: Calculate result directly without enumeration
- **Efficient Computation**: O(log k) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use the mathematical formula that each position can have any of n values.

**Algorithm**:
- Use formula: number of sequences = n^k
- Calculate n^k efficiently using modular exponentiation
- Apply modulo operation throughout

**Visual Example**:
```
Mathematical formula:
┌─────────────────────────────────────┐
│ For k positions and n elements:    │
│ - Position 1: n choices            │
│ - Position 2: n choices            │
│ - ...                              │
│ - Position k: n choices            │
│ Total: n × n × ... × n = n^k      │
└─────────────────────────────────────┘

Modular exponentiation:
┌─────────────────────────────────────┐
│ n^k mod mod = (n mod mod)^k mod mod │
│ Use binary exponentiation for efficiency │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def mathematical_sequence_count(n, k, mod=10**9+7):
    """
    Count sequences using mathematical formula
    
    Args:
        n: maximum element value
        k: sequence length
        mod: modulo value
    
    Returns:
        int: number of sequences modulo mod
    """
    def mod_pow(base, exp, mod):
        """Calculate base^exp mod mod efficiently"""
        result = 1
        base = base % mod
        
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        
        return result
    
    # Number of sequences = n^k
    return mod_pow(n, k, mod)

def mathematical_sequence_count_v2(n, k, mod=10**9+7):
    """
    Alternative mathematical approach using built-in pow
    
    Args:
        n: maximum element value
        k: sequence length
        mod: modulo value
    
    Returns:
        int: number of sequences modulo mod
    """
    # Use built-in pow with modular arithmetic
    return pow(n, k, mod)

# Example usage
n, k = 3, 2
result1 = mathematical_sequence_count(n, k)
result2 = mathematical_sequence_count_v2(n, k)
print(f"Mathematical sequence count: {result1}")
print(f"Mathematical sequence count v2: {result2}")
```

**Time Complexity**: O(log k)
**Space Complexity**: O(1)

**Why it's better**: Uses mathematical formula for O(log k) time complexity.

**Implementation Considerations**:
- **Mathematical Formula**: Use n^k formula for sequences
- **Modular Exponentiation**: Use efficient modular exponentiation
- **Direct Calculation**: Calculate result directly without enumeration

---

### Approach 3: Advanced Mathematical Solution (Optimal)

**Key Insights from Advanced Mathematical Solution**:
- **Advanced Mathematics**: Use advanced mathematical properties
- **Efficient Computation**: O(log k) time complexity
- **Mathematical Optimization**: Use mathematical optimizations
- **Optimal Complexity**: Best approach for sequence counting

**Key Insight**: Use advanced mathematical properties and optimizations for efficient sequence counting.

**Algorithm**:
- Use advanced mathematical properties
- Apply mathematical optimizations
- Calculate result efficiently

**Visual Example**:
```
Advanced mathematical properties:
┌─────────────────────────────────────┐
│ For sequences:                     │
│ - Each position has n choices      │
│ - Total number = n^k               │
│ - Can be calculated efficiently    │
└─────────────────────────────────────┘

Mathematical optimizations:
┌─────────────────────────────────────┐
│ - Use modular exponentiation       │
│ - Apply mathematical properties    │
│ - Optimize for large numbers       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_mathematical_sequence_count(n, k, mod=10**9+7):
    """
    Count sequences using advanced mathematical approach
    
    Args:
        n: maximum element value
        k: sequence length
        mod: modulo value
    
    Returns:
        int: number of sequences modulo mod
    """
    def fast_mod_pow(base, exp, mod):
        """Fast modular exponentiation with optimizations"""
        if exp == 0:
            return 1
        if exp == 1:
            return base % mod
        
        # Use binary exponentiation
        result = 1
        base = base % mod
        
        while exp > 0:
            if exp & 1:  # If exp is odd
                result = (result * base) % mod
            exp = exp >> 1  # Divide exp by 2
            base = (base * base) % mod
        
        return result
    
    # Handle edge cases
    if k == 0:
        return 1
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Number of sequences = n^k
    return fast_mod_pow(n, k, mod)

def optimized_sequence_count(n, k, mod=10**9+7):
    """
    Optimized sequence counting with additional optimizations
    
    Args:
        n: maximum element value
        k: sequence length
        mod: modulo value
    
    Returns:
        int: number of sequences modulo mod
    """
    # Use built-in pow with optimizations
    if k == 0:
        return 1
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # For large k, use built-in pow which is highly optimized
    return pow(n, k, mod)

def sequence_count_with_precomputation(max_n, max_k, mod=10**9+7):
    """
    Precompute sequence counts for multiple queries
    
    Args:
        max_n: maximum value of n
        max_k: maximum value of k
        mod: modulo value
    
    Returns:
        list: precomputed sequence counts
    """
    results = [[0] * (max_k + 1) for _ in range(max_n + 1)]
    
    for i in range(max_n + 1):
        for j in range(max_k + 1):
            if j == 0:
                results[i][j] = 1
            elif i == 0:
                results[i][j] = 0
            elif i == 1:
                results[i][j] = 1
            else:
                results[i][j] = pow(i, j, mod)
    
    return results

# Example usage
n, k = 3, 2
result1 = advanced_mathematical_sequence_count(n, k)
result2 = optimized_sequence_count(n, k)
print(f"Advanced mathematical sequence count: {result1}")
print(f"Optimized sequence count: {result2}")

# Precompute for multiple queries
max_n, max_k = 1000, 1000
precomputed = sequence_count_with_precomputation(max_n, max_k)
print(f"Precomputed result for n={n}, k={k}: {precomputed[n][k]}")
```

**Time Complexity**: O(log k)
**Space Complexity**: O(1)

**Why it's optimal**: Uses advanced mathematical properties for O(log k) time complexity.

**Implementation Details**:
- **Advanced Mathematics**: Use advanced mathematical properties
- **Efficient Computation**: Use optimized modular exponentiation
- **Mathematical Optimizations**: Apply mathematical optimizations
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(n^k) | O(k) | Complete enumeration of all sequences |
| Mathematical Formula | O(log k) | O(1) | Use n^k formula with modular exponentiation |
| Advanced Mathematical | O(log k) | O(1) | Use advanced mathematical properties and optimizations |

### Time Complexity
- **Time**: O(log k) - Use modular exponentiation for efficient calculation
- **Space**: O(1) - Use only necessary variables

### Why This Solution Works
- **Mathematical Formula**: Use n^k formula for sequences
- **Modular Exponentiation**: Use efficient modular exponentiation
- **Mathematical Properties**: Leverage mathematical properties
- **Efficient Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Sequence Count with Constraints**
**Problem**: Count sequences with certain constraints.

**Key Differences**: Apply constraints to sequences

**Solution Approach**: Modify counting formula to include constraints

**Implementation**:
```python
def constrained_sequence_count(n, k, constraints, mod=10**9+7):
    """
    Count sequences with constraints
    
    Args:
        n: maximum element value
        k: sequence length
        constraints: list of constraints for each position
        mod: modulo value
    
    Returns:
        int: number of constrained sequences modulo mod
    """
    def count_constrained_sequences(position):
        """Count constrained sequences recursively"""
        if position == k:
            return 1  # Valid constrained sequence found
        
        count = 0
        for element in constraints[position]:  # Only consider allowed elements
            count = (count + count_constrained_sequences(position + 1)) % mod
        
        return count
    
    return count_constrained_sequences(0)

def constrained_sequence_count_optimized(n, k, constraints, mod=10**9+7):
    """
    Optimized constrained sequence counting
    
    Args:
        n: maximum element value
        k: sequence length
        constraints: list of constraints for each position
        mod: modulo value
    
    Returns:
        int: number of constrained sequences modulo mod
    """
    # Calculate total number of constrained sequences
    total = 1
    for i in range(k):
        total = (total * len(constraints[i])) % mod
    
    return total

# Example usage
n, k = 3, 2
constraints = [
    [1, 2],  # Position 0 can be 1 or 2
    [2, 3]   # Position 1 can be 2 or 3
]
result1 = constrained_sequence_count(n, k, constraints)
result2 = constrained_sequence_count_optimized(n, k, constraints)
print(f"Constrained sequence count: {result1}")
print(f"Optimized constrained count: {result2}")
```

#### **2. Sequence Count with Repetition Constraints**
**Problem**: Count sequences with repetition constraints.

**Key Differences**: Limit repetition of elements

**Solution Approach**: Use inclusion-exclusion principle

**Implementation**:
```python
def repetition_constrained_sequence_count(n, k, max_repetition, mod=10**9+7):
    """
    Count sequences with repetition constraints
    
    Args:
        n: maximum element value
        k: sequence length
        max_repetition: maximum number of repetitions allowed
        mod: modulo value
    
    Returns:
        int: number of repetition-constrained sequences modulo mod
    """
    def count_repetition_constrained_sequences(position, element_counts):
        """Count sequences with repetition constraints"""
        if position == k:
            return 1  # Valid repetition-constrained sequence found
        
        count = 0
        for element in range(1, n + 1):
            if element_counts[element] < max_repetition:  # Check repetition limit
                element_counts[element] += 1
                count = (count + count_repetition_constrained_sequences(position + 1, element_counts)) % mod
                element_counts[element] -= 1  # Backtrack
        
        return count
    
    element_counts = [0] * (n + 1)
    return count_repetition_constrained_sequences(0, element_counts)

# Example usage
n, k = 3, 2
max_repetition = 1  # No element can appear more than once
result = repetition_constrained_sequence_count(n, k, max_repetition)
print(f"Repetition constrained sequence count: {result}")
```

#### **3. Sequence Count with Pattern Constraints**
**Problem**: Count sequences that match specific patterns.

**Key Differences**: Sequences must match specific patterns

**Solution Approach**: Use pattern matching techniques

**Implementation**:
```python
def pattern_constrained_sequence_count(n, k, pattern, mod=10**9+7):
    """
    Count sequences that match specific patterns
    
    Args:
        n: maximum element value
        k: sequence length
        pattern: pattern to match
        mod: modulo value
    
    Returns:
        int: number of pattern-matching sequences modulo mod
    """
    def count_pattern_sequences(position, current_sequence):
        """Count sequences that match pattern"""
        if position == k:
            # Check if sequence matches pattern
            if matches_pattern(current_sequence, pattern):
                return 1
            return 0
        
        count = 0
        for element in range(1, n + 1):
            current_sequence.append(element)
            count = (count + count_pattern_sequences(position + 1, current_sequence)) % mod
            current_sequence.pop()  # Backtrack
        
        return count
    
    def matches_pattern(sequence, pattern):
        """Check if sequence matches pattern"""
        if len(sequence) != len(pattern):
            return False
        
        for i in range(len(sequence)):
            if not matches_element_pattern(sequence[i], pattern[i]):
                return False
        
        return True
    
    def matches_element_pattern(element, pattern_element):
        """Check if element matches pattern element"""
        if isinstance(pattern_element, set):
            return element in pattern_element
        elif isinstance(pattern_element, list):
            return element in pattern_element
        else:
            return element == pattern_element
    
    return count_pattern_sequences(0, [])

# Example usage
n, k = 3, 2
pattern = [1, {2, 3}]  # First element must be 1, second element must be 2 or 3
result = pattern_constrained_sequence_count(n, k, pattern)
print(f"Pattern constrained sequence count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Counting Permutations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Combinations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Reorders](https://cses.fi/problemset/task/1075) - Combinatorics

#### **LeetCode Problems**
- [Permutations](https://leetcode.com/problems/permutations/) - Permutations
- [Permutations II](https://leetcode.com/problems/permutations-ii/) - Permutations with duplicates
- [Combinations](https://leetcode.com/problems/combinations/) - Combinations

#### **Problem Categories**
- **Combinatorics**: Mathematical counting, sequences, permutations
- **Dynamic Programming**: DP optimization, mathematical DP
- **Mathematical Algorithms**: Modular arithmetic, number theory

## 🔗 Additional Resources

### **Algorithm References**
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Binomial coefficients
- [Sequences](https://cp-algorithms.com/combinatorics/inclusion-exclusion.html) - Inclusion-exclusion principle
- [Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html) - Modular arithmetic

### **Practice Problems**
- [CSES Counting Permutations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Reorders](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Combinatorics](https://en.wikipedia.org/wiki/Combinatorics) - Wikipedia article

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